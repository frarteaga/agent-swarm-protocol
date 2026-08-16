# Agent Swarm Protocol

GitHub is the fleet's durable coordination layer, shared memory, and source of truth. Agents may run in different providers, models, sessions, or runtimes and MUST NOT assume shared chat context.

## Authority and identity

**[PROTO-HUMAN-01] Authority precedence.** Explicit human instructions have highest authority over agent decisions, handoffs, workflow transitions, architecture proposals, and prior task direction, subject only to immutable platform/safety constraints. When direction changes, stop conflicting work, read the full instruction, record durable consequences in GitHub, normalize ownership/state if needed, and continue under the new direction. Never silently ignore a human instruction.

**[PROTO-IDENTITY-01] Runtime identity.** Every agent MUST know `ROLE`, `AGENT_ID`, `REPOSITORY`, and `WORK_LEASE_TTL_HOURS` (recommended default `4`). `ROLE` defines authority; `AGENT_ID` identifies the instance; `REPOSITORY` defines operational scope; TTL limits claimed work without renewal. Provider/model names are not logical identity.

**[PROTO-SCOPE-01] Repository/role scope.** GitHub operations MUST target `REPOSITORY` unless human-directed otherwise. An agent MUST act only within `ROLE` and MUST NOT silently switch roles because another is unavailable or it believes it can do that work.

**[PROTO-MEMORY-01] Durable state.** Anything another agent needs MUST be in GitHub. Issues carry tasks, requirements, criteria, architecture/product decisions, scope, questions, coordination, and durable human instructions; PRs carry proposed changes, tests, implementation discussion/review, and CI; commits are technical checkpoints and MUST NOT be messages; comments communicate; labels encode workflow. Newer GitHub beats stale private chat; newer explicit human instruction beats both.

## Workflow state and discovery

**[PROTO-LABELS-01] Canonical labels.** Ownership: `agent:specifier|architect|developer|reviewer|qa`, mutually exclusive; active managed work MUST have at most one and normally exactly one owner, while done may have none. State: `state:ready|working|blocked|review|stale|done`, mutually exclusive and exactly one per managed task. A category transition MUST remove all old labels before adding the new one.

**[PROTO-LABEL-RECOVERY-01] Invalid labels.** Reconstruct conflicts by (1) latest explicit human instruction, (2) latest valid HANDOFF, (3) latest valid CLAIM/RECLAIM, (4) latest durable workflow decision. Normalize before continuing; if still unsafe to infer, ask the human.

**[PROTO-STARTUP-01] Startup.** Read runtime configuration, this protocol, `ENGINEERING_RULES.md`, and `roles/<ROLE>.md`; query current `agent:<ROLE>` work; prefer open ready work and inspect working work for expired leases; read the complete relevant Issue/PR/current human instructions, decisions, handoffs, evidence, and relevant repository/CI state; normalize invalid labels; claim/reclaim before working; perform only role responsibilities. No assigned work => stop; do not invent work.

## Claims, leases, and recovery

**[PROTO-MESSAGES-01] Message schemas.** Before emitting any durable swarm message, MUST load `.agent/reference/SWARM_MESSAGES.md` and use the relevant canonical `MSG-*` schema. This file is on-demand at startup but mandatory before the first durable message; never guess required fields.

**[PROTO-CLAIM-01] Claim.** A claim is a temporary lease. Use `MSG-CLAIM-01`; then normalize to `agent:<ROLE>` + `state:working`. The comment timestamp starts the lease.

**[PROTO-HEARTBEAT-01] Renewal.** Long work renews via `MSG-HEARTBEAT-01`. Only protocol messages explicitly identifying that `AGENT_ID` renew its lease; ordinary shared-account activity is not instance liveness.

**[PROTO-STALE-01] Stale predicate.** Work is stale only when it is working, has a valid previous claimant, has no lease-renewing message from that `AGENT_ID` within TTL, and no human reservation for that agent exists.

**[PROTO-RECLAIM-01] Reclaim.** Before reclaim: read Issue/linked PRs, inspect/preserve valid partial work, verify no newer human instruction prevents reassignment. Mark stale; post `MSG-RECLAIM-01`; normalize back to role+working; reclaim starts a new lease. A human may reassign without waiting for TTL.

**[PROTO-RECOVERY-01] No destructive recovery.** Do not delete useful commits, force-push away valid work, close useful PRs because an agent disappeared, or restart unnecessarily. Continue from latest valid repository state.

## Durable coordination

**[PROTO-HANDOFF-01] Handoff.** Use `MSG-HANDOFF-01`; then normalize target owner + ready and stop recipient-owned work. Sender MUST NOT continue recipient work.

**[PROTO-BLOCK-01] Block.** When another role must decide, use `MSG-BLOCKED-01`; normalize to answering role + blocked; ask the smallest necessary question.

**[PROTO-DECISION-01] Decision.** Use `MSG-DECISION-01`. Later agents MUST respect the latest applicable durable decision unless replaced or human-overridden.

## Issue, PR, and specification authority

**[PROTO-ISSUE-PR-01] Issue vs PR.** Issue: requirements, acceptance, scope, visible behavior, architecture/product decisions, ambiguity, cross-agent coordination. PR: implementation, tests, implementation defects, line review, CI, requested code changes. **WHAT** changes go to Issue; **HOW** corrections within accepted scope go to PR. Durable requirement/architecture conclusions discovered in PR MUST also be recorded in Issue.

**[PROTO-PR-01] PR discipline.** PR SHOULD reference its Issue via `Closes #<n>` when auto-close fits or `Related to #<n>` otherwise. Reviewer MUST review actual current PR state, not author summary.

**[PROTO-AUTHORITY-01] Role boundary.** Specifier owns **WHAT** externally visible behavior is required; architect owns **HOW** responsibilities/dependencies are structured. Architecture MUST NOT silently redefine accepted behavior; specifier MUST NOT prescribe implementation structure unless needed to express visible behavior.

**[PROTO-SPEC-BLOCK-01] Spec block.** Specifier MAY inspect implementation/PRs and directly block contradiction of accepted requirement/criterion/agreed behavior/human-approved specification using `MSG-SPEC-BLOCK-01`. While unresolved: PR MUST NOT advance to QA; task MUST NOT be done; PR SHOULD NOT be merged; reviewer approval/architecture preference do not override; human may override.

**[PROTO-SPEC-CLEAR-01] Spec clear.** After fix, developer returns to specifier. When conforming, specifier uses `MSG-SPEC-CLEAR-01`.

## Review, QA, completion, regression

**[PROTO-REVIEW-01] Review outcomes.** Approved -> next valid gate (QA only when architect hardening not required); changes -> developer with actionable findings; architecture question -> architect with one concrete block. Reviewer does not own substantial architecture unless explicitly granted.

**[PROTO-COMPLETE-01] QA outcomes.** PASS uses `MSG-COMPLETE-01`; when completion is valid normalize done/remove owner as appropriate. FAIL hands to developer with reproducible evidence.

**[PROTO-DELIVERY-01] Delivery invariant.** For PR-delivered work, QA PASS is necessary but insufficient for done. PR MUST be merged into intended canonical base, or explicitly closed as superseded by durable Issue/PR comment naming replacement PR/commit and why it delivers same scope. Approved/green open PR remains pending and MUST NOT make Issue done. Non-code work may complete without PR when required durable artifact exists on Issue.

**[PROTO-REGRESSION-01] Regression.** Done is reopenable when evidence invalidates completion. Reopen original Issue for a direct violation of behavior it claimed to implement/verify; otherwise create a linked new Issue for new/indirect/substantially independent work or clearer audit trail. Preserve historical completion; use `MSG-REGRESSION-01`. Confirmed implementation defects normally return developer+ready; architect/QA may own diagnosis. After fix: regression test when practical, original acceptance, normal review, QA, new COMPLETE, then done when appropriate.

**[PROTO-ROLLBACK-01] Fix forward/revert.** For merged faults explicitly choose FIX FORWARD or REVERT. Prefer forward when understood/small/safe and revert loses valid work; revert when severe/unsafe, root cause unclear, or lower-risk known-good recovery. Architect/human SHOULD decide non-trivial cases via DECISION. Revert MUST use normal history (prefer revert commit/PR); do NOT rewrite shared history, delete original PR/evidence, or force-push main to erase it.

## Flow, concurrency, communication

**[PROTO-FLOW-01] Flow.** Default `specifier -> architect -> developer -> reviewer -> qa -> done`; not rigid. Common valid transitions: `specifier->architect|developer`, `architect->developer|specifier`, `developer->reviewer|architect`, `reviewer->developer|architect|qa`, `qa->developer|reviewer|done`. Skip unnecessary roles when appropriate; humans may override.

**[PROTO-CONCURRENCY-01] Parallel work.** Only clearly separable responsibilities: separate Issues/subtasks, one owner/unit, defined boundaries, preferably separate PRs, avoid overlap, reconcile by normal review. Same-role agents keep role labels; CLAIM/RECLAIM identifies instance. Do not duplicate a valid unexpired claim.

**[PROTO-COMMS-01] Communication.** SHOULD be concise, factual, actionable, durable, scannable; avoid repeating GitHub context. Communicate on claim, handoff, block, decision, important finding, stale recovery, completion. Human-facing progress SHOULD lead with semantic outcome/phase/blocker/next step; SHAs/run/CI IDs are supporting evidence unless requested or needed. Exact durable engineering evidence remains required where specified.

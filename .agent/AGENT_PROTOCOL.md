# Agent Swarm Protocol

GitHub is the fleet's durable coordination layer, shared memory, and source of truth. Agents may run in different providers, models, sessions, or runtimes and MUST NOT assume shared chat context.

## Authority and identity

**[PROTO-HUMAN-01] Authority precedence.** Explicit human instructions have highest authority over agent decisions, handoffs, workflow transitions, architecture proposals, and prior task direction, subject only to immutable platform/safety constraints. When direction changes, stop conflicting work, read the full instruction, record durable consequences in GitHub, normalize ownership/state if needed, and continue under the new direction. Never silently ignore a human instruction.

**[PROTO-IDENTITY-01] Runtime identity.** Every agent MUST know `ROLE`, `AGENT_ID`, `REPOSITORY`, and `WORK_LEASE_TTL_HOURS` (recommended default: `4`). `ROLE` defines authority; `AGENT_ID` identifies the instance; `REPOSITORY` defines operational scope; TTL defines how long claimed work may remain active without lease renewal. Provider/model names are not logical identity.

**[PROTO-SCOPE-01] Repository and role scope.** All GitHub operations MUST target `REPOSITORY` unless a human explicitly instructs otherwise. An agent MUST act only within `ROLE` and MUST NOT silently change roles because another role is unavailable or it believes it can do that work.

**[PROTO-MEMORY-01] Durable state.** Anything another agent needs MUST be recorded in GitHub. Issues carry tasks, requirements, acceptance criteria, architectural/product decisions, scope changes, unresolved questions, coordination, and durable human instructions. PRs carry proposed changes, tests, implementation discussion/review, and CI results. Commits are technical checkpoints and MUST NOT be used as messages. Comments communicate; labels encode canonical workflow ownership/state. Newer GitHub state beats stale private chat; newer explicit human instructions beat both.

## Workflow state

**[PROTO-LABELS-01] Canonical labels.** Ownership labels are `agent:specifier|architect|developer|reviewer|qa`; they are mutually exclusive. An active managed task MUST have at most one owner and normally exactly one; `state:done` may have none. State labels are `state:ready|working|blocked|review|stale|done`; a managed task MUST have exactly one and they are mutually exclusive. Ownership/state changes MUST remove every old label in that category before adding the new one; never merely add and assume replacement.

**[PROTO-LABEL-RECOVERY-01] Invalid-label recovery.** If workflow labels conflict, do not infer intent from label order. Reconstruct canonical state by: (1) latest explicit human instruction, (2) latest valid `SWARM HANDOFF`, (3) latest valid `SWARM CLAIM`/`SWARM RECLAIM`, (4) latest durable workflow decision. Normalize before continuing; if intent remains unsafe to infer, ask the human.

**[PROTO-STARTUP-01] Startup/work discovery.** On activation: read runtime configuration, this protocol, `.agent/ENGINEERING_RULES.md`, and `.agent/roles/<ROLE>.md`; query current GitHub state for `agent:<ROLE>` work; prefer open `state:ready`; inspect matching `state:working` for expired leases; read the complete relevant Issue, linked PRs, recent human instructions/decisions/handoffs/evidence, and relevant repository/CI state; normalize invalid labels; then claim/reclaim before working. Perform only configured-role responsibilities. If no work is assigned, stop and do not invent work.

## Claims, leases, and recovery

**[PROTO-CLAIM-01] Claim.** A claim is a temporary lease, not permanent ownership. Post:

```text
[SWARM CLAIM]

AGENT: <AGENT_ID>
ROLE: <ROLE>

LEASE:
<WORK_LEASE_TTL_HOURS> hours

ACTION:
Claiming this task.
```

Then normalize to `agent:<ROLE>` + `state:working`. The comment timestamp starts the lease.

**[PROTO-HEARTBEAT-01] Lease renewal.** Legitimately long work renews explicitly:

```text
[SWARM HEARTBEAT]

AGENT: <AGENT_ID>
ROLE: <ROLE>

STATUS:
Still actively working on this task.

REFS:
Issue #<number>
PR #<number if applicable>
```

Only protocol messages explicitly identifying that `AGENT_ID` renew its lease. Ordinary commits/comments under a shared account do not prove that instance is alive.

**[PROTO-STALE-01] Stale work.** Work is stale only when it is `state:working`, has a valid previous claimant, no lease-renewing protocol message from that `AGENT_ID` exists within TTL, and no human instruction reserves it for that agent.

**[PROTO-RECLAIM-01] Reclaim.** Before reclaiming, read Issue/linked PRs, inspect and preserve valid partial work, and verify no newer human instruction prevents reassignment. Mark `state:stale`, then post:

```text
[SWARM RECLAIM]

AGENT: <AGENT_ID>
ROLE: <ROLE>

PREVIOUS_AGENT:
<previous-agent-id>

REASON:
Previous work lease expired without handoff or heartbeat.

ACTION:
Reclaiming and continuing from the current GitHub state.

REFS:
Issue #<number>
PR #<number if applicable>
```

Normalize back to `agent:<ROLE>` + `state:working`; the reclaim starts a new lease. A human may reassign at any time without waiting for TTL.

**[PROTO-RECOVERY-01] No destructive recovery.** Do not delete useful commits, force-push away valid work, close a useful PR merely because its agent disappeared, or restart implementation unnecessarily. Continue from the latest valid repository state.

## Durable coordination messages

The following schemas and fields are canonical. Do not rely on memory when emitting them.

**[PROTO-HANDOFF-01] Handoff.** Transfers responsibility:

```text
[SWARM HANDOFF]

FROM: <AGENT_ID>
ROLE: <ROLE>
TO: <target-role>
STATUS: READY

ACTION:
<short actionable instruction>

REFS:
Issue #<number>
PR #<number if applicable>
```

After posting: normalize to `agent:<target-role>` + `state:ready`, then stop doing recipient-owned work. The sender MUST NOT continue the recipient's work.

**[PROTO-BLOCK-01] Block.** When another role must decide:

```text
[SWARM BLOCKED]

FROM: <AGENT_ID>
ROLE: <ROLE>
TO: <target-role>

QUESTION:
<one concrete question>

CONTEXT:
<minimum necessary context>

REFS:
Issue #<number>
PR #<number if applicable>
```

Normalize ownership to the answering role and state to `state:blocked`; ask the smallest question necessary.

**[PROTO-DECISION-01] Decision.** Record durable decisions as:

```text
[SWARM DECISION]

FROM: <AGENT_ID>
ROLE: <ROLE>
TO: <role if applicable>

DECISION:
<clear decision>

RATIONALE:
<brief rationale if useful>

REFS:
Issue #<number>
PR #<number if applicable>
```

Later agents MUST respect the latest applicable durable decision unless replaced by a newer one or overridden by a human.

## Issue, PR, and specification authority

**[PROTO-ISSUE-PR-01] Issue vs PR.** Use the Issue for requirements, acceptance criteria, scope, externally visible behavior, architectural/product decisions, ambiguity, and cross-agent coordination. Use the PR for implementation, tests, implementation defects, line-level review, CI failures, and requested code changes. Changes to **WHAT** belongs in the Issue; corrections to **HOW** the current implementation realizes accepted scope belong in the PR. Durable requirement/architecture conclusions discovered in PR discussion MUST also be recorded in the Issue.

**[PROTO-PR-01] PR discipline.** A PR SHOULD reference its Issue with `Closes #<n>` when automatic closure is appropriate or `Related to #<n>` otherwise. A reviewer MUST review the actual current PR state, not merely the author's summary.

**[PROTO-AUTHORITY-01] Role authority boundary.** Specifier owns **WHAT** externally visible behavior is required. Architect owns **HOW** system responsibilities/dependencies are structured. Architecture MUST NOT silently redefine accepted behavior; specifier MUST NOT prescribe implementation structure unless necessary to express externally visible behavior.

**[PROTO-SPEC-BLOCK-01] Specification block.** Specifier MAY inspect implementation/PRs and directly block a contradiction of accepted requirements, criteria, agreed behavior, or human-approved specification:

```text
[SWARM SPEC BLOCK]

FROM: <AGENT_ID>
ROLE: specifier
TO: developer

REQUIREMENT:
<reference to violated requirement>

PROBLEM:
<how implementation contradicts it>

REQUIRED OUTCOME:
<behavior that must be restored>

REFS:
Issue #<number>
PR #<number>
```

While unresolved: PR MUST NOT advance to QA; task MUST NOT be done; PR SHOULD NOT be merged; reviewer approval and architectural preference do not override the block; a human may override it.

**[PROTO-SPEC-CLEAR-01] Specification clear.** After a fix, developer hands back to specifier. When satisfied, specifier posts:

```text
[SWARM SPEC CLEAR]

FROM: <AGENT_ID>
ROLE: specifier

RESULT:
Implementation conforms to the accepted specification.

REFS:
Issue #<number>
PR #<number>
```

## Review, QA, completion, and regression

**[PROTO-REVIEW-01] Review outcomes.** Approved work hands to the next valid gate (QA only when architect hardening is not required); changes required hand to developer with actionable findings; architecture questions block to architect with one concrete question. Reviewer does not own substantial architecture changes unless explicitly granted.

**[PROTO-COMPLETE-01] QA outcomes.** QA PASS posts:

```text
[SWARM COMPLETE]

FROM: <AGENT_ID>
ROLE: qa

RESULT:
PASS

REFS:
Issue #<number>
PR #<number>
```

When completion is valid, normalize to `state:done` and remove ownership when appropriate. QA FAIL hands to developer with reproducible failure evidence.

**[PROTO-DELIVERY-01] Delivery invariant.** For PR-delivered work, QA PASS is necessary but not sufficient for `state:done`. The PR MUST be merged into its intended canonical base, or explicitly closed as superseded by a durable Issue/PR comment naming the replacement PR/commit and explaining why it delivers the same scope. An approved/green open PR is pending delivery and MUST NOT make its Issue done. Non-code tasks may complete without a PR when their required durable artifact is present on the Issue.

**[PROTO-REGRESSION-01] Reopen/regression.** `state:done` is reopenable when new evidence invalidates completion. Reopen the original Issue when a defect directly violates behavior it claimed to implement/verify; otherwise create a new linked Issue for new/indirect/substantially independent work or when a separate audit trail is clearer. Preserve historical completion evidence. For a regression, post:

```text
[SWARM REGRESSION]

FROM: <AGENT_ID>
ROLE: <ROLE>

TYPE:
REGRESSION

OBSERVED:
<reproducible failure>

EXPECTED:
<expected behavior>

ORIGINAL_COMPLETION:
<reference to previous completion>

REFS:
Issue #<number>
PR #<original-pr>
```

Confirmed implementation defects normally return to `agent:developer` + `state:ready`; use architect/QA when diagnosis requires it. After a fix, add a regression test when practical, rerun relevant original acceptance criteria, perform normal review and QA, post a new `SWARM COMPLETE`, then return to done when appropriate.

**[PROTO-ROLLBACK-01] Fix forward vs revert.** For already-merged faults, explicitly choose FIX FORWARD or REVERT. Prefer fix forward when understood/small/safe and revert would remove valid work; prefer revert when severe/unsafe, root cause unclear, or revert is lower-risk known-good recovery. Architect or human SHOULD decide non-trivial cases via `SWARM DECISION`. Reverts MUST use normal history (prefer revert commit/PR); do NOT rewrite shared history, delete original PR/evidence, or force-push main to erase the event.

## Flow, concurrency, and communication

**[PROTO-FLOW-01] Role flow.** Default: `specifier -> architect -> developer -> reviewer -> qa -> done`. It is not rigid. Common valid transitions: `specifier->architect|developer`, `architect->developer|specifier`, `developer->reviewer|architect`, `reviewer->developer|architect|qa`, `qa->developer|reviewer|done`. Unnecessary roles may be skipped when appropriate; humans may override transitions.

**[PROTO-CONCURRENCY-01] Parallel work.** Parallel work is allowed only when responsibilities are clearly separable: use separate Issues or explicit subtasks, one owner per unit, defined boundaries, preferably separate PRs, avoid overlapping modifications, reconcile through normal review. Multiple agents sharing a role still use role-based ownership labels; `SWARM CLAIM`/`RECLAIM` identifies the instance. Do not duplicate a valid unexpired claim.

**[PROTO-COMMS-01] Communication.** Agent communication SHOULD be concise, factual, actionable, durable, and easy to scan; do not repeat large context already in GitHub. Communicate on claim, handoff, block, decision, important finding, stale recovery, or completion. Human-facing progress SHOULD lead with semantic state (meaningful outcome complete, active phase, blockers, next meaningful step); SHAs/run IDs/CI identifiers are supporting evidence unless explicitly requested or needed to reference/diagnose. This does not weaken exact durable engineering evidence where required.

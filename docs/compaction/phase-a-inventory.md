# Phase A — Pre-change semantic inventory

Base: `6763a95d5a877d750c54391d0529f500d5496abc`. IDs below are deterministic migration keys for this refactor; they describe the pre-change normative concepts to be mapped in Phase F.

## Protocol

| Old ID | Source | Normative concept |
|---|---|---|
| OLD-PROTO-001 | AGENT_PROTOCOL §§Purpose,3 | GitHub durable shared memory/source of truth; commits are not messages; cross-agent facts are durable. |
| OLD-PROTO-002 | §1 | Runtime ROLE/AGENT_ID/REPOSITORY/TTL identity and default TTL. |
| OLD-PROTO-003 | §2 | Repository scope and no silent role switching. |
| OLD-PROTO-004 | §§3,12 | Precedence: explicit human > current GitHub > stale private chat. |
| OLD-PROTO-005 | §4 | Ownership labels mutually exclusive and active-task cardinality. |
| OLD-PROTO-006 | §4 | State labels mutually exclusive and exactly-one state. |
| OLD-PROTO-007 | §4 | Atomic ownership-label replacement. |
| OLD-PROTO-008 | §4 | Atomic state-label replacement. |
| OLD-PROTO-009 | §4 | Invalid-label recovery priority and normalize-before-work rule. |
| OLD-PROTO-010 | §5 | Startup/read/discovery/current-state algorithm. |
| OLD-PROTO-011 | §5 | No assigned work => stop; do not invent work. |
| OLD-PROTO-012 | §6 | Claim is lease; CLAIM schema and fields. |
| OLD-PROTO-013 | §6 | Claim normalizes role+working and comment starts lease. |
| OLD-PROTO-014 | §6 | HEARTBEAT schema; only AGENT_ID protocol events renew lease. |
| OLD-PROTO-015 | §7 | Exact stale-work predicate. |
| OLD-PROTO-016 | §7 | Reclaim preconditions, RECLAIM schema, state transitions/new lease. |
| OLD-PROTO-017 | §7 | Human may reassign without TTL wait. |
| OLD-PROTO-018 | §7 | No destructive stale recovery/history loss. |
| OLD-PROTO-019 | §8 | HANDOFF schema; ownership/state transfer; sender stops recipient work. |
| OLD-PROTO-020 | §9 | BLOCKED schema; answering-role ownership + blocked state; smallest question. |
| OLD-PROTO-021 | §10 | DECISION schema and latest-durable-decision authority. |
| OLD-PROTO-022 | §11 | Issue WHAT/durable decisions vs PR HOW/implementation split; durable conclusions copied to Issue. |
| OLD-PROTO-023 | §12 | Human-change procedure and highest authority. |
| OLD-PROTO-024 | §13 | PR issue-link convention and review-current-state requirement. |
| OLD-PROTO-025 | §14 | Specifier conformance authority and SPEC BLOCK schema. |
| OLD-PROTO-026 | §14 | Unresolved spec-block effects and human override. |
| OLD-PROTO-027 | §14 | Developer return to specifier and SPEC CLEAR schema. |
| OLD-PROTO-028 | §14 | Specifier WHAT vs architect HOW boundary. |
| OLD-PROTO-029 | §15 | Review outcomes and architecture escalation boundary. |
| OLD-PROTO-030 | §16 | QA PASS/FAIL, COMPLETE schema, completion normalization. |
| OLD-PROTO-031 | §16 | Delivery invariant: merged or explicit durable supersession before done. |
| OLD-PROTO-032 | §17 | Done is reopenable. |
| OLD-PROTO-033 | §18 | REGRESSION schema and preserved history. |
| OLD-PROTO-034 | §18 | Original-Issue vs new-Issue regression criteria and owner routing. |
| OLD-PROTO-035 | §19 | FIX FORWARD vs REVERT decision criteria. |
| OLD-PROTO-036 | §19 | Revert uses normal history; no destructive rewrite/evidence deletion. |
| OLD-PROTO-037 | §19 | Regression-fix test/review/QA/new-complete flow. |
| OLD-PROTO-038 | §20 | Default role flow, allowed backward/skip transitions, human override. |
| OLD-PROTO-039 | §21 | Parallel-work separability, one owner/unit, claims identify instances, no duplicate valid claim. |
| OLD-PROTO-040 | §22 | Concise durable communication events. |
| OLD-PROTO-041 | §22 | Human-facing semantic status before identifiers; exact durable evidence retained. |

## Engineering rules

| Old ID | Source | Normative concept |
|---|---|---|
| OLD-ENG-001 | ENGINEERING_RULES §1 | Deterministic metrics only; reproducible command/version/scope/result evidence. |
| OLD-ENG-002 | §2 | APS/canonical language tooling and missing-tool escalation. |
| OLD-ENG-003 | §3 | Testable boundaries; structural/documented exclusions; test-suite separation. |
| OLD-ENG-004 | §4 | Unit-TDD cycle, focused-test requirement, exceptions and truthful reporting. |
| OLD-ENG-005 | §5 | APS parse/generate/execute acceptance sequence. |
| OLD-ENG-006 | §6 | Deterministic coverage, project threshold precedence, no invented universal threshold. |
| OLD-ENG-007 | §7 | Deterministic CRAP; changed/new testable code <=6; missing-tool escalation. |
| OLD-ENG-008 | §8 | Deterministic DRY; no invented threshold. |
| OLD-ENG-009 | §9 | Mutation-site count; >100 split unless human exception; manifests not hand-edited. |
| OLD-ENG-010 | §10 Fast-CI | Full mutation excluded from normal push/PR loop; architect/human trigger. |
| OLD-ENG-011 | §10 Generated | Explicit generated/declarative exclusion + alternate deterministic verification; behavior remains testable/mutable. |
| OLD-ENG-012 | §10 Budget | 200 default / 300 ceiling; override conditions and durable rationale. |
| OLD-ENG-013 | §10 Budget | Deterministic changed-first mutant selection; selected survivors block; outside-budget scope advisory. |
| OLD-ENG-014 | §10 Incremental | Exact reviewed scope, differential/cache reuse, invalidation, survivor reruns, max workers 4, progress. |
| OLD-ENG-015 | §10 Incremental | Production revision change makes affected architect mutation evidence stale. |
| OLD-ENG-016 | §11 | Soft APS Gherkin mutation owned by hardening; fix meaningless spec rather than game data. |
| OLD-ENG-017 | §12 | Architect-owned property testing categories and separate execution. |
| OLD-ENG-018 | §13 | Specifier E2E definition, QA real-UI execution, no private API bypass. |
| OLD-ENG-019 | §14 | Role gate ownership matrix and default developer→reviewer→architect→qa path. |
| OLD-ENG-020 | §15 | SWARM QUALITY EVIDENCE schema; omit unowned/unexecuted gates. |

## Role deltas

| Old ID | Source | Normative concept |
|---|---|---|
| OLD-SPEC-001 | roles/specifier Mission/Owns/Does Not Own | Specifier WHAT ownership and non-ownership. |
| OLD-SPEC-002 | Gherkin rules | APS Gherkin determinism, naming, parameter/Background/DRY/mutation-friendly rules. |
| OLD-SPEC-003 | E2E specification | User-visible E2E procedure contents and UI boundary. |
| OLD-SPEC-004 | Feature workflow | Specification workflow and default explicit-human-approval gate. |
| OLD-SPEC-005 | Verification | Specifier verification exclusions. |
| OLD-SPEC-006 | Specification authority/resolution | Inspect PR, block mismatch, clear corrected conformance, no code-quality/architecture takeover. |
| OLD-SPEC-007 | Architecture boundary/transitions/completion | Behavior-vs-architecture escalation, valid outcomes and completion criteria. |
| OLD-ARCH-001 | roles/architect Mission/Owns/Does Not Own | Architect structure+hardening ownership and exclusions. |
| OLD-ARCH-002 | Architecture rules | Boundary/dependency/testability/interface/architecture-check principles. |
| OLD-ARCH-003 | Design phase | Pre-implementation architecture procedure and durable decision/handoff. |
| OLD-ARCH-004 | Hardening phase | Post-review structural/property/mutation/Gherkin/metric hardening. |
| OLD-ARCH-005 | Requirement boundary | No behavior redefinition; block to specifier/human; spec block cannot be overridden. |
| OLD-ARCH-006 | Property/mutation/Gherkin sections | Deterministic property and exact-scope incremental mutation responsibilities. |
| OLD-ARCH-007 | Metrics/sequence/review escalation | Rerun affected gates after architecture changes; return functional changes to independent review. |
| OLD-ARCH-008 | Regression/rollback | Non-trivial FIX FORWARD/REVERT authority and factors; no history rewrite. |
| OLD-ARCH-009 | Transitions/completion | Architect valid outcomes and hardening completion conditions. |
| OLD-DEV-001 | roles/developer Mission/Owns/Does Not Own | Developer implementation/TDD/test ownership and exclusions. |
| OLD-DEV-002 | Acceptance pipeline | APS parser plus project handlers/generator/step-shape rules. |
| OLD-DEV-003 | TDD/testability | Non-vacuous TDD and adapter-boundary rules. |
| OLD-DEV-004 | Working rules | Read/claim/inspect/small-slice/minimal-change/durable-evidence loop. |
| OLD-DEV-005 | Verification/handoff | Unit+acceptance+project verification, quality evidence, reviewer handoff/stop. |
| OLD-DEV-006 | Blocked | Routing behavioral/architecture/tool/human decisions via smallest block. |
| OLD-DEV-007 | Review/spec/QA returns | Fix/retest/escalate paths; spec-block hard gate; QA regression-test-first path. |
| OLD-DEV-008 | Stale recovery | Preserve partial work/history and reclaim before continuation. |
| OLD-DEV-009 | Transitions/completion | Developer outcomes and completion criteria. |
| OLD-REV-001 | roles/reviewer Mission/Owns/Does Not Own | Independent review/gate ownership and exclusions. |
| OLD-REV-002 | Working rules | Actual-diff review, rerun tests, deterministic metrics, actionable findings/evidence. |
| OLD-REV-003 | Coverage/CRAP/DRY/mutation-site | Reviewer gate semantics and thresholds. |
| OLD-REV-004 | Cleanup | Behavior-preserving cleanup findings; reviewer cannot author-and-self-approve substantial changes. |
| OLD-REV-005 | Required verification | Exact advance criteria and no mutation execution. |
| OLD-REV-006 | Outcomes | Developer/specifier/architect routing and default architect hardening destination. |
| OLD-REV-007 | READY handoff | PR/REVIEWED_SHA/BASE_SHA exact fields and active reviewer FROM identity. |
| OLD-REV-008 | Re-review/completion | Fresh diff/metrics after changes and completion criteria. |
| OLD-QA-001 | roles/qa Mission/Owns/Does Not Own | Final behavioral/E2E/quality ownership and exclusions. |
| OLD-QA-002 | Preconditions | Current spec/reviewer/architect/spec-block/revision evidence required. |
| OLD-QA-003 | Working rules | Independent observable real-UI verification and truthful evidence. |
| OLD-QA-004 | Final verification | Unit/acceptance/property/E2E/integration/CRAP/DRY/release gates; no normal mutation rerun. |
| OLD-QA-005 | QA conflicts | Stop/escalate contradictory spec/QA/human artifacts. |
| OLD-QA-006 | PASS | COMPLETE + final evidence + delivery invariant before done. |
| OLD-QA-007 | FAIL | Reproducible defect routing and reviewer/architect re-gating after production fixes. |
| OLD-QA-008 | Regression | Original-vs-new Issue rules, regression schema/history, re-verification. |
| OLD-QA-009 | Rollback/transitions/completion | QA rollback evidence/revalidation, outcomes, final completion conditions. |

## Bootstrap and on-demand hardening diagnostics

| Old ID | Source | Normative concept |
|---|---|---|
| OLD-BOOT-001 | bootstrap Runtime/Startup | Supplied identity authoritative; required protocol/engineering/role read order. |
| OLD-BOOT-002 | Startup | Repository discovery, ready/stale inspection, full Issue/PR/current evidence, normalize/claim/role gates. |
| OLD-BOOT-003 | Protocol Identity | Correct AGENT/ROLE identity in durable messages. |
| OLD-BOOT-004 | Lease Rules | Claim/reclaim/heartbeat lease semantics; ordinary activity not liveness. |
| OLD-BOOT-005 | Engineering Evidence | No fabricated metrics; use canonical quality evidence. |
| OLD-BOOT-006 | Operational Boundary | No role/repo/context/claim/handoff/history/spec-block/metric/manifest violations; durable coordination. |
| OLD-BOOT-007 | Human Authority | Explicit human precedence and durable propagation. |
| OLD-DIAG-001 | HARDENING_DIAGNOSTICS Why | Unusable raw logs MUST NOT cause retry loops; long hardening persists durable evidence. |
| OLD-DIAG-002 | Durable diagnostic contract | Capture output/exit, always persist, durable pointer, restore outcome, no reviewed-revision mutation for observability. |
| OLD-DIAG-003 | Recommended artifact | Context/manifest/budget/log/exit/survivor/cache identity and stable artifact naming. |
| OLD-DIAG-004 | Durable pointer | Self-report run/attempt/gate/revisions/artifact/exit/retrieval; pointer not huge log. |
| OLD-DIAG-005 | Retrieval order | Pointer→artifact→persisted evidence→classify; no repeated unusable raw-log retries. |
| OLD-DIAG-006 | Failure classification | Survivor/harness/resource/Gherkin/missing-evidence routing semantics. |
| OLD-DIAG-007 | Core invariant | Hardening evidence recoverable and attributable to exact reviewed scope. |

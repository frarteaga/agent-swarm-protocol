# Phase F — Semantic equivalence map

Base inventory: `117` pre-change IDs from Phase A. Every ID maps exactly once. Many-to-one rows marked **deduplicated equivalent** consolidate repeated prose without changing trigger, actor, precondition, action/prohibition, transition, exception, override, or normative strength.

| Old inventory ID | New canonical rule ID | Normative strength | Status |
|---|---|---|---|
| `OLD-ARCH-001` | `ROLE-ARCHITECT-01` | same | deduplicated equivalent |
| `OLD-ARCH-002` | `ROLE-ARCHITECT-01` | same | deduplicated equivalent |
| `OLD-ARCH-003` | `ROLE-ARCHITECT-02` | same | equivalent |
| `OLD-ARCH-004` | `ROLE-ARCHITECT-04` | same | deduplicated equivalent |
| `OLD-ARCH-005` | `ROLE-ARCHITECT-03` | same | equivalent |
| `OLD-ARCH-006` | `ROLE-ARCHITECT-05` | same | equivalent |
| `OLD-ARCH-007` | `ROLE-ARCHITECT-04` | same | deduplicated equivalent |
| `OLD-ARCH-008` | `ROLE-ARCHITECT-07` | same | equivalent |
| `OLD-ARCH-009` | `ROLE-ARCHITECT-08` | same | equivalent |
| `OLD-BOOT-001` | `BOOT-IDENTITY-01` | same | equivalent |
| `OLD-BOOT-002` | `BOOT-DISCOVERY-01` | same | equivalent |
| `OLD-BOOT-003` | `PROTO-MESSAGES-01` | same | deduplicated equivalent |
| `OLD-BOOT-004` | `PROTO-HEARTBEAT-01` | same | deduplicated equivalent |
| `OLD-BOOT-005` | `ENG-EVIDENCE-01` | same | deduplicated equivalent |
| `OLD-BOOT-006` | `BOOT-DISCOVERY-01` | same | equivalent |
| `OLD-BOOT-007` | `PROTO-HUMAN-01` | same | deduplicated equivalent |
| `OLD-DEV-001` | `ROLE-DEVELOPER-01` | same | deduplicated equivalent |
| `OLD-DEV-002` | `ROLE-DEVELOPER-01` | same | deduplicated equivalent |
| `OLD-DEV-003` | `ROLE-DEVELOPER-02` | same | equivalent |
| `OLD-DEV-004` | `ROLE-DEVELOPER-04` | same | equivalent |
| `OLD-DEV-005` | `ROLE-DEVELOPER-05` | same | equivalent |
| `OLD-DEV-006` | `ROLE-DEVELOPER-06` | same | equivalent |
| `OLD-DEV-007` | `ROLE-DEVELOPER-07` | same | equivalent |
| `OLD-DEV-008` | `ROLE-DEVELOPER-08` | same | equivalent |
| `OLD-DEV-009` | `ROLE-DEVELOPER-09` | same | equivalent |
| `OLD-DIAG-001` | `DIAG-RETRY-01` | same | equivalent |
| `OLD-DIAG-002` | `DIAG-PERSIST-01` | same | equivalent |
| `OLD-DIAG-003` | `DIAG-ARTIFACT-01` | same | equivalent |
| `OLD-DIAG-004` | `DIAG-POINTER-01` | same | equivalent |
| `OLD-DIAG-005` | `DIAG-RETRIEVE-01` | same | equivalent |
| `OLD-DIAG-006` | `DIAG-CLASSIFY-01` | same | equivalent |
| `OLD-DIAG-007` | `DIAG-INVARIANT-01` | same | equivalent |
| `OLD-ENG-001` | `ENG-EVIDENCE-01` | same | equivalent |
| `OLD-ENG-002` | `ENG-TOOLING-01` | same | equivalent |
| `OLD-ENG-003` | `ENG-BOUNDARY-01` | same | equivalent |
| `OLD-ENG-004` | `ENG-TDD-01` | same | equivalent |
| `OLD-ENG-005` | `ENG-ACCEPTANCE-01` | same | equivalent |
| `OLD-ENG-006` | `ENG-COVERAGE-01` | same | equivalent |
| `OLD-ENG-007` | `ENG-CRAP-01` | same | equivalent |
| `OLD-ENG-008` | `ENG-DRY-01` | same | equivalent |
| `OLD-ENG-009` | `ENG-MUTATION-SITES-01` | same | equivalent |
| `OLD-ENG-010` | `ENG-MUTATION-FASTCI-01` | same | equivalent |
| `OLD-ENG-011` | `ENG-MUTATION-ARTIFACT-01` | same | equivalent |
| `OLD-ENG-012` | `ENG-MUTATION-BUDGET-01` | same | equivalent |
| `OLD-ENG-013` | `ENG-MUTATION-BUDGET-01` | same | deduplicated equivalent |
| `OLD-ENG-014` | `ENG-MUTATION-INCREMENTAL-01` | same | equivalent |
| `OLD-ENG-015` | `ENG-MUTATION-INCREMENTAL-01` | same | deduplicated equivalent |
| `OLD-ENG-016` | `ENG-GHERKIN-MUTATION-01` | same | equivalent |
| `OLD-ENG-017` | `ENG-PROPERTY-01` | same | equivalent |
| `OLD-ENG-018` | `ENG-E2E-01` | same | equivalent |
| `OLD-ENG-019` | `ENG-GATES-01` | same | equivalent |
| `OLD-ENG-020` | `ENG-EVIDENCE-FORMAT-01` | same | equivalent |
| `OLD-PROTO-001` | `PROTO-MEMORY-01` | MUST | equivalent |
| `OLD-PROTO-002` | `PROTO-IDENTITY-01` | MUST | equivalent |
| `OLD-PROTO-003` | `PROTO-SCOPE-01` | MUST | equivalent |
| `OLD-PROTO-004` | `PROTO-HUMAN-01` | highest-authority imperative | deduplicated equivalent |
| `OLD-PROTO-005` | `PROTO-LABELS-01` | MUST | deduplicated equivalent |
| `OLD-PROTO-006` | `PROTO-LABELS-01` | MUST | deduplicated equivalent |
| `OLD-PROTO-007` | `PROTO-LABELS-01` | MUST | deduplicated equivalent |
| `OLD-PROTO-008` | `PROTO-LABELS-01` | MUST | deduplicated equivalent |
| `OLD-PROTO-009` | `PROTO-LABEL-RECOVERY-01` | imperative | equivalent |
| `OLD-PROTO-010` | `PROTO-STARTUP-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-011` | `PROTO-STARTUP-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-012` | `PROTO-CLAIM-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-013` | `PROTO-CLAIM-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-014` | `PROTO-HEARTBEAT-01` | lease invariant | equivalent |
| `OLD-PROTO-015` | `PROTO-STALE-01` | exact predicate | equivalent |
| `OLD-PROTO-016` | `PROTO-RECLAIM-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-017` | `PROTO-RECLAIM-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-018` | `PROTO-RECOVERY-01` | prohibition | equivalent |
| `OLD-PROTO-019` | `PROTO-HANDOFF-01` | MUST/prohibition | equivalent |
| `OLD-PROTO-020` | `PROTO-BLOCK-01` | imperative | equivalent |
| `OLD-PROTO-021` | `PROTO-DECISION-01` | MUST | equivalent |
| `OLD-PROTO-022` | `PROTO-ISSUE-PR-01` | MUST/imperative | equivalent |
| `OLD-PROTO-023` | `PROTO-HUMAN-01` | highest-authority imperative | deduplicated equivalent |
| `OLD-PROTO-024` | `PROTO-PR-01` | SHOULD/MUST | equivalent |
| `OLD-PROTO-025` | `PROTO-SPEC-BLOCK-01` | MAY/MUST/MUST NOT/SHOULD NOT | deduplicated equivalent |
| `OLD-PROTO-026` | `PROTO-SPEC-BLOCK-01` | MAY/MUST/MUST NOT/SHOULD NOT | deduplicated equivalent |
| `OLD-PROTO-027` | `PROTO-SPEC-CLEAR-01` | imperative | equivalent |
| `OLD-PROTO-028` | `PROTO-AUTHORITY-01` | MUST NOT | equivalent |
| `OLD-PROTO-029` | `PROTO-REVIEW-01` | role boundary | equivalent |
| `OLD-PROTO-030` | `PROTO-COMPLETE-01` | completion imperative | equivalent |
| `OLD-PROTO-031` | `PROTO-DELIVERY-01` | MUST/MUST NOT | equivalent |
| `OLD-PROTO-032` | `PROTO-REGRESSION-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-033` | `PROTO-REGRESSION-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-034` | `PROTO-REGRESSION-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-035` | `PROTO-ROLLBACK-01` | SHOULD/MUST/MUST NOT | deduplicated equivalent |
| `OLD-PROTO-036` | `PROTO-ROLLBACK-01` | SHOULD/MUST/MUST NOT | deduplicated equivalent |
| `OLD-PROTO-037` | `PROTO-REGRESSION-01` | imperative | deduplicated equivalent |
| `OLD-PROTO-038` | `PROTO-FLOW-01` | default/allowed | equivalent |
| `OLD-PROTO-039` | `PROTO-CONCURRENCY-01` | prohibition | equivalent |
| `OLD-PROTO-040` | `PROTO-COMMS-01` | SHOULD | deduplicated equivalent |
| `OLD-PROTO-041` | `PROTO-COMMS-01` | SHOULD | deduplicated equivalent |
| `OLD-QA-001` | `ROLE-QA-01` | same | deduplicated equivalent |
| `OLD-QA-002` | `ROLE-QA-01` | same | deduplicated equivalent |
| `OLD-QA-003` | `ROLE-QA-02` | same | equivalent |
| `OLD-QA-004` | `ROLE-QA-03` | same | equivalent |
| `OLD-QA-005` | `ROLE-QA-04` | same | equivalent |
| `OLD-QA-006` | `ROLE-QA-05` | same | equivalent |
| `OLD-QA-007` | `ROLE-QA-06` | same | equivalent |
| `OLD-QA-008` | `ROLE-QA-07` | same | equivalent |
| `OLD-QA-009` | `ROLE-QA-09` | same | equivalent |
| `OLD-REV-001` | `ROLE-REVIEWER-01` | same | deduplicated equivalent |
| `OLD-REV-002` | `ROLE-REVIEWER-01` | same | deduplicated equivalent |
| `OLD-REV-003` | `ROLE-REVIEWER-02` | same | equivalent |
| `OLD-REV-004` | `ROLE-REVIEWER-03` | same | equivalent |
| `OLD-REV-005` | `ROLE-REVIEWER-04` | same | equivalent |
| `OLD-REV-006` | `ROLE-REVIEWER-05` | same | deduplicated equivalent |
| `OLD-REV-007` | `ROLE-REVIEWER-05` | same | deduplicated equivalent |
| `OLD-REV-008` | `ROLE-REVIEWER-06` | same | equivalent |
| `OLD-SPEC-001` | `ROLE-SPECIFIER-01` | same | deduplicated equivalent |
| `OLD-SPEC-002` | `ROLE-SPECIFIER-01` | same | equivalent |
| `OLD-SPEC-003` | `ROLE-SPECIFIER-02` | same | equivalent |
| `OLD-SPEC-004` | `ROLE-SPECIFIER-03` | same | equivalent |
| `OLD-SPEC-005` | `ROLE-SPECIFIER-04` | same | equivalent |
| `OLD-SPEC-006` | `ROLE-SPECIFIER-05` | same | equivalent |
| `OLD-SPEC-007` | `ROLE-SPECIFIER-06` | same | equivalent |

## Durable message schema preservation

Protocol semantics reference the canonical schemas in `.agent/reference/SWARM_MESSAGES.md`: `MSG-CLAIM-01`, `MSG-HEARTBEAT-01`, `MSG-RECLAIM-01`, `MSG-HANDOFF-01`, `MSG-BLOCKED-01`, `MSG-DECISION-01`, `MSG-SPEC-BLOCK-01`, `MSG-SPEC-CLEAR-01`, `MSG-COMPLETE-01`, and `MSG-REGRESSION-01`. Required field names and fixed literals are preserved from the base. `PROTO-MESSAGES-01` makes the reference mandatory before emission, so correctness is not memory-dependent.

## Structural and semantic tripwires

- `scripts/check_protocol_structure.py` verifies required files/sections, unique canonical IDs, exact one-to-one old-ID coverage, canonical message reference, and durable-message required fields.
- `scripts/audit_protocol_semantics.py` reruns exact/similarity duplicate discovery plus RFC 2119 census; count changes are expected from deduplication and are a tripwire rather than an equality target.
- Independent reviewer-role inspection of the exact PR HEAD remains required; structural checks are not semantic proof.

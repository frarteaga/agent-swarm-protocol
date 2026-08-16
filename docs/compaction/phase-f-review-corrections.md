# Phase F — Independent-review audit corrections

This file is part of the Phase F equivalence artifact and closes the two blocking audit-trail findings from the independent review of PR #5. It supplements `phase-f-equivalence.md`; no `.agent` semantics are changed by this correction.

## Core-invariant equivalence supplement

The primary Phase F map covers the original 117 inventory IDs. `phase-a-core-invariants.md` adds the 25 pre-change §23 core-invariant restatements that were omitted from the first inventory pass. Each maps exactly once below to the already-existing canonical rule that represents the same invariant.

| Old inventory ID | New canonical rule ID | Normative strength | Status |
|---|---|---|---|
| `OLD-INVARIANT-001` | `PROTO-MEMORY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-002` | `PROTO-IDENTITY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-003` | `PROTO-IDENTITY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-004` | `PROTO-SCOPE-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-005` | `PROTO-CLAIM-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-006` | `PROTO-RECLAIM-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-007` | `PROTO-LABELS-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-008` | `PROTO-LABELS-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-009` | `PROTO-LABEL-RECOVERY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-010` | `PROTO-ISSUE-PR-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-011` | `PROTO-ISSUE-PR-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-012` | `PROTO-MEMORY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-013` | `PROTO-HANDOFF-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-014` | `PROTO-SCOPE-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-015` | `PROTO-SPEC-BLOCK-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-016` | `PROTO-SPEC-BLOCK-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-017` | `PROTO-AUTHORITY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-018` | `PROTO-REGRESSION-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-019` | `PROTO-REGRESSION-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-020` | `PROTO-ROLLBACK-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-021` | `PROTO-STARTUP-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-022` | `PROTO-MEMORY-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-023` | `PROTO-HUMAN-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-024` | `PROTO-HANDOFF-01` | same | deduplicated equivalent |
| `OLD-INVARIANT-025` | `PROTO-CONCURRENCY-01` | same | deduplicated equivalent |

Combined equivalence coverage is therefore **142/142 pre-change inventory IDs**, with the 25 rows above explicitly identified as deduplicated restatements rather than newly invented rules.

## Recorded baseline inconsistency — review destination after approval

The pre-change corpus contained an internal layering inconsistency that the first Phase F report failed to record:

- `AGENT_PROTOCOL.md` §15 stated the generic review outcome **Approved → Handoff to QA**.
- The pre-change `roles/reviewer.md` and `ENGINEERING_RULES.md` default/full engineering discipline required reviewer quality gates to hand to **architect** for post-review hardening before QA.

This PR does **not** introduce a new resolution. It preserves the pre-existing layered behavior explicitly:

1. the protocol-level transition `reviewer -> qa` remains a valid transition when architect hardening is not required or is explicitly skipped by a human/work mode;
2. under the default/full engineering discipline, `ENG-GATES-01` and the reviewer role require `reviewer -> architect -> qa`;
3. `PROTO-REVIEW-01` expresses that same layering as “Approved -> next valid gate (QA only when architect hardening not required)”.

Accordingly, `OLD-PROTO-029 -> PROTO-REVIEW-01` remains semantically equivalent **with this recorded baseline inconsistency as part of its audit evidence**. The compaction is not silently choosing one contradictory sentence and discarding the other.

## Review-gate disposition

Blocking finding B1 is closed by the explicit 25-ID Phase A inventory supplement plus the 25 exact mappings above. Blocking finding B2 is closed by the recorded baseline inconsistency and preservation statement above. Because these corrections modify only `docs/`, `scripts/`, and workflow audit material—not `.agent` context—the protocol text, role authority, message schemas, thresholds, and measured startup bundles remain unchanged. A fresh final-HEAD CI run and independent reviewer re-check are still required before merge.

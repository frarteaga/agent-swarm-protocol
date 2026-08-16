# Phase A — Core-invariant inventory supplement

Base: `6763a95d5a877d750c54391d0529f500d5496abc`.

The pre-change `AGENT_PROTOCOL.md` §23 contained 25 numbered **Core invariants**. They are mostly concise restatements of normative concepts already inventoried elsewhere, but Issue #4 requires every pre-change core invariant to remain explicitly represented in the equivalence audit. These IDs supplement `phase-a-inventory.md`; they introduce no new semantics.

| Old ID | Source | Pre-change core invariant |
|---|---|---|
| OLD-INVARIANT-001 | AGENT_PROTOCOL §23 #1 | GitHub is shared memory. |
| OLD-INVARIANT-002 | §23 #2 | `ROLE` defines authority. |
| OLD-INVARIANT-003 | §23 #3 | `AGENT_ID` identifies an agent instance. |
| OLD-INVARIANT-004 | §23 #4 | `REPOSITORY` defines operational scope. |
| OLD-INVARIANT-005 | §23 #5 | Claims are leases, not permanent locks. |
| OLD-INVARIANT-006 | §23 #6 | Abandoned work must be recoverable. |
| OLD-INVARIANT-007 | §23 #7 | `agent:*` labels are mutually exclusive. |
| OLD-INVARIANT-008 | §23 #8 | `state:*` labels are mutually exclusive. |
| OLD-INVARIANT-009 | §23 #9 | Invalid workflow labels must be normalized before continuing. |
| OLD-INVARIANT-010 | §23 #10 | Issues define tasks, required behavior, and durable decisions. |
| OLD-INVARIANT-011 | §23 #11 | PRs contain proposed implementation and implementation review. |
| OLD-INVARIANT-012 | §23 #12 | Commits are not messages. |
| OLD-INVARIANT-013 | §23 #13 | Handoffs explicitly transfer responsibility. |
| OLD-INVARIANT-014 | §23 #14 | Agents respect role boundaries. |
| OLD-INVARIANT-015 | §23 #15 | Specifier may block implementation that contradicts accepted behavior. |
| OLD-INVARIANT-016 | §23 #16 | Reviewer approval cannot override an unresolved specification block. |
| OLD-INVARIANT-017 | §23 #17 | Architecture cannot silently redefine accepted behavior. |
| OLD-INVARIANT-018 | §23 #18 | `state:done` may be reopened when new evidence invalidates completion. |
| OLD-INVARIANT-019 | §23 #19 | Regression history must be preserved. |
| OLD-INVARIANT-020 | §23 #20 | Shared Git history must not be destructively rewritten for rollback. |
| OLD-INVARIANT-021 | §23 #21 | Agents read current GitHub state before acting. |
| OLD-INVARIANT-022 | §23 #22 | Agents never assume shared chat context. |
| OLD-INVARIANT-023 | §23 #23 | Human instructions have highest authority. |
| OLD-INVARIANT-024 | §23 #24 | Responsibility transfer causes the sender to stop doing the recipient's work. |
| OLD-INVARIANT-025 | §23 #25 | Multiple agents must not duplicate valid claimed work. |

Combined pre-change inventory size: **142 IDs** = 117 primary inventory IDs + these 25 core-invariant restatement IDs.

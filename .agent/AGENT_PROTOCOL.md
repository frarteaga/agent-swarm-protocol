# Agent Swarm Protocol

## Purpose

This repository is operated by a fleet of independent AI agents. Agents may run in different providers, models, chat sessions, or execution environments. Agents do not share chat context.

**GitHub is the shared coordination layer, durable memory, and source of truth.**

Each agent receives its runtime identity separately through `.agent/bootstrap/AGENT_BOOTSTRAP.md` or equivalent startup instructions.

## 1. Runtime identity

Every agent MUST know:

```text
ROLE: <role>
AGENT_ID: <unique-agent-id>
REPOSITORY: <owner/repository>
WORK_LEASE_TTL_HOURS: <hours>
```

Recommended default:

```text
WORK_LEASE_TTL_HOURS: 4
```

- `ROLE` defines responsibilities and authority.
- `AGENT_ID` identifies the individual agent instance.
- `REPOSITORY` defines the repository where the agent operates.
- `WORK_LEASE_TTL_HOURS` defines how long claimed work may remain active without a lease-renewing protocol event.

Provider/model names are intentionally excluded from logical identity. Prefer `developer-01`, not `developer.chatgpt`.

## 2. Repository and role scope

All GitHub operations MUST target `REPOSITORY` unless a human explicitly instructs otherwise.

An agent MUST act only within its configured `ROLE`. It MUST NOT silently change roles because another role is unavailable or because it believes it can perform the work.

## 3. GitHub object semantics

- **Issue** = task, requirements, acceptance criteria, architectural/product decisions, scope changes, unresolved questions, coordination, and durable human instructions.
- **Pull Request** = proposed repository changes, tests, implementation discussion, review, and CI results.
- **Commit** = technical repository checkpoint only. Commits MUST NOT be used as agent-to-agent messages.
- **Comments** = communication between agents and humans.
- **Labels** = canonical workflow ownership and state fields.

Anything another agent needs MUST be recorded in GitHub. If stale chat context conflicts with newer GitHub state, GitHub wins. Newer explicit human instructions override both.

## 4. Workflow labels

### Ownership labels

```text
agent:specifier
agent:architect
agent:developer
agent:reviewer
agent:qa
```

These labels are **mutually exclusive**. An active managed task MUST have at most one `agent:*` label and normally exactly one. `state:done` may have no owner.

### State labels

```text
state:ready
state:working
state:blocked
state:review
state:stale
state:done
```

These labels are **mutually exclusive**. A managed task MUST have exactly one `state:*` label.

### Atomic label transition rule

When ownership changes:

1. remove every existing workflow `agent:*` label;
2. add the new `agent:<role>` label.

When state changes:

1. remove every existing workflow `state:*` label;
2. add the new `state:<state>` label.

Agents MUST NOT merely add the new label and assume the previous one disappeared.

### Invalid label recovery

If conflicting labels exist, do not infer intent from label order. Reconstruct canonical state using, in priority order:

1. latest explicit human instruction;
2. latest valid `SWARM HANDOFF`;
3. latest valid `SWARM CLAIM` or `SWARM RECLAIM`;
4. latest durable workflow decision.

Normalize the labels before continuing. If intent cannot be determined safely, ask the human.

## 5. Startup procedure

Whenever activated:

1. read runtime configuration;
2. confirm `ROLE`, `AGENT_ID`, `REPOSITORY`, and lease TTL;
3. read this protocol;
4. read `.agent/roles/<ROLE>.md`;
5. query GitHub for work assigned to `agent:<ROLE>`;
6. prefer open `state:ready` work;
7. also inspect `state:working` work for expired leases belonging to this role;
8. read the complete relevant Issue and linked PRs;
9. read recent human instructions, decisions, and handoffs;
10. inspect current repository/CI state when relevant;
11. claim or reclaim the task before working;
12. perform only responsibilities belonging to the configured role.

If no work is assigned, stop. Do not invent work.

## 6. Claim and work lease

A claim is a temporary lease, not permanent ownership.

```text
[SWARM CLAIM]

AGENT: <AGENT_ID>
ROLE: <ROLE>

LEASE:
<WORK_LEASE_TTL_HOURS> hours

ACTION:
Claiming this task.
```

After claiming, normalize the task to:

```text
agent:<ROLE>
state:working
```

The GitHub comment timestamp starts the lease.

### Lease renewal

For legitimately long-running work, renew explicitly:

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

Only protocol messages that explicitly identify the `AGENT_ID` renew that agent's lease. Ordinary commits or comments under a shared GitHub account do not prove that a particular agent instance is alive.

## 7. Stale work and recovery

Work is stale when all are true:

1. task is `state:working`;
2. it has a valid previous claimant;
3. no lease-renewing protocol message from that `AGENT_ID` exists within the TTL;
4. no human instruction explicitly reserves it for that agent.

Before reclaiming:

1. read the Issue and linked PRs;
2. inspect previous partial work;
3. preserve valid existing work;
4. verify no newer human instruction prevents reassignment.

Mark `state:stale`, then post:

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

Then normalize back to `agent:<ROLE>` + `state:working`. The reclaim starts a new lease.

A human may reassign work at any time without waiting for TTL expiration.

### No destructive recovery

Do not delete useful commits, force-push away valid work, close a useful PR merely because its agent disappeared, or restart implementation unnecessarily. Continue from the latest valid repository state.

## 8. Handoff protocol

A handoff transfers responsibility between roles.

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

After posting the handoff:

1. normalize ownership to `agent:<target-role>`;
2. normalize state to `state:ready`;
3. stop performing responsibilities now owned by the recipient.

The sender MUST NOT continue doing the recipient's work.

## 9. Blocking protocol

When another role must decide:

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

Normalize ownership to the role that must answer and state to `state:blocked`. Ask the smallest question necessary to unblock progress.

## 10. Decision protocol

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

Later agents MUST respect the latest applicable durable decision unless replaced by a newer decision or overridden by a human.

## 11. Issue vs PR rule

Use the **Issue** for requirements, acceptance criteria, scope, externally visible behavior, architectural/product decisions, ambiguity, and cross-agent coordination.

Use the **PR** for implementation, tests, implementation defects, line-level review, CI failures, and requested code changes.

> If the discussion changes **WHAT** should be built, use the Issue.

> If the discussion changes **HOW** the current implementation should be corrected, use the PR.

If a PR discussion reveals a durable requirement or architecture decision, record the conclusion in the Issue too.

## 12. Human authority

Explicit human instructions have highest authority and override agent decisions, handoffs, workflow transitions, architecture proposals, and prior task direction, subject only to immutable platform/safety constraints.

When a human changes direction:

1. stop conflicting work;
2. read the full instruction;
3. record durable consequences in GitHub;
4. update ownership/state if needed;
5. continue under the new direction.

Never silently ignore a human instruction.

## 13. Pull request rules

A PR SHOULD reference its Issue using `Closes #<n>` when automatic closure is appropriate or `Related to #<n>` otherwise.

Recommended description:

```text
Implemented:
- <change>

Tests:
- <verification performed>

Requested next:
<role>
```

A reviewer MUST review the actual current PR state, not merely the author's summary.

## 14. Specifier authority and specification gate

The `specifier` owns authoritative interpretation of accepted externally visible behavior. It may inspect an implementation or PR whenever needed to determine conformance.

If a PR violates an accepted requirement, acceptance criterion, explicitly agreed behavior, or human-approved specification, the specifier MAY block progression directly without permission from architect or reviewer:

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

While an unresolved `SWARM SPEC BLOCK` exists:

- the PR MUST NOT advance to QA;
- the task MUST NOT be marked done;
- the PR SHOULD NOT be merged;
- reviewer approval does not override the block;
- architectural preference does not override the block;
- a human may override the block.

After a fix, developer hands back to specifier. When satisfied, specifier posts:

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

Authority boundary:

- **Specifier:** WHAT externally visible behavior is required.
- **Architect:** HOW system responsibilities and dependencies are structured.

Architecture MUST NOT silently redefine accepted behavior. The specifier MUST NOT prescribe implementation structure unless required to express externally visible behavior.

## 15. Review outcomes

Common outcomes:

### Approved

Handoff to QA.

### Changes required

Handoff to developer with actionable review findings.

### Architecture decision required

Block to architect with one concrete architectural question.

Reviewer does not own substantial architecture changes unless explicitly granted by role instructions.

## 16. QA outcomes

### PASS

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

Normalize to `state:done` and remove ownership when appropriate.

### FAIL

Handoff to developer and provide reproducible failure evidence.

## 17. Completed work is reopenable

`state:done` means complete based on evidence available at that time. It does not make the work immutable.

A regression, production failure, security issue, or invalidated assumption may reactivate completed work.

## 18. Regression protocol

Reopen the original Issue when the defect directly violates behavior that Issue claimed to implement or verify.

Post:

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

Keep historical completion messages intact.

Create a **new Issue** instead when the defect is new behavior, only indirectly related, requires substantially independent work, or a separate audit trail is clearer. Link the original Issue and PR.

For a confirmed implementation defect, usually normalize to `agent:developer` + `state:ready`. Use architect or QA ownership when diagnosis requires it.

## 19. Fix forward vs revert

When faulty work is already merged, explicitly decide between **FIX FORWARD** and **REVERT**.

Prefer fix forward when the defect is understood, correction is small/safe, temporary exposure is acceptable, and revert would remove valid work.

Prefer revert when the regression is severe, production is unsafe/unusable, root cause is unclear, or revert restores a known-good state with lower risk.

For non-trivial cases, architect or human SHOULD decide and record a `SWARM DECISION`.

A revert MUST use normal Git history, preferably a revert commit or revert PR. Do NOT rewrite shared branch history, delete the original PR, remove historical evidence, or force-push main to pretend the change never happened.

After a regression fix:

1. add a regression test when practical;
2. rerun relevant original acceptance criteria;
3. perform normal review;
4. perform QA again;
5. post a new `SWARM COMPLETE`;
6. return to `state:done` when appropriate.

## 20. Default role flow

Default flow:

```text
specifier -> architect -> developer -> reviewer -> qa -> done
```

It is not rigid. Common valid transitions:

```text
specifier -> architect
specifier -> developer
architect -> developer
architect -> specifier
developer -> reviewer
developer -> architect
reviewer -> developer
reviewer -> architect
reviewer -> qa
qa -> developer
qa -> reviewer
qa -> done
```

Unnecessary roles may be skipped when appropriate. Human instructions may override any transition.

## 21. Concurrent work

Parallel work is allowed only when responsibilities are clearly separable. Create separate Issues or explicit subtasks, assign one owner to each unit, define boundaries, prefer separate PRs, avoid overlapping modifications, and reconcile through normal review.

When multiple agents share a role, ownership labels remain role-based. A `SWARM CLAIM`/`SWARM RECLAIM` identifies the specific instance. Do not duplicate a valid unexpired claim.

## 22. Communication style

Agent communication SHOULD be concise, factual, actionable, durable, and easy for humans to scan. Do not repeat large amounts of context already present in GitHub. Communicate when claiming, handing off, blocking, deciding, reporting important findings, recovering stale work, or completing work.

## 23. Core invariants

1. GitHub is shared memory.
2. `ROLE` defines authority.
3. `AGENT_ID` identifies an agent instance.
4. `REPOSITORY` defines operational scope.
5. Claims are leases, not permanent locks.
6. Abandoned work must be recoverable.
7. `agent:*` labels are mutually exclusive.
8. `state:*` labels are mutually exclusive.
9. Invalid workflow labels must be normalized before continuing.
10. Issues define tasks, required behavior, and durable decisions.
11. PRs contain proposed implementation and implementation review.
12. Commits are not messages.
13. Handoffs explicitly transfer responsibility.
14. Agents respect role boundaries.
15. Specifier may block implementation that contradicts accepted behavior.
16. Reviewer approval cannot override an unresolved specification block.
17. Architecture cannot silently redefine accepted behavior.
18. `state:done` may be reopened when new evidence invalidates completion.
19. Regression history must be preserved.
20. Shared Git history must not be destructively rewritten for rollback.
21. Agents read current GitHub state before acting.
22. Agents never assume shared chat context.
23. Human instructions have highest authority.
24. Responsibility transfer causes the sender to stop doing the recipient's work.
25. Multiple agents must not duplicate valid claimed work.

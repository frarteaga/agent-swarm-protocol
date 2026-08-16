# Swarm Durable Message Schemas

This file is the canonical schema source for durable swarm messages. Per `PROTO-MESSAGES-01`, an agent MUST load this file before emitting a durable protocol message; do not reconstruct schemas from memory. Field names and required fields are normative.

## Claim — MSG-CLAIM-01

```text
[SWARM CLAIM]

AGENT: <AGENT_ID>
ROLE: <ROLE>

LEASE:
<WORK_LEASE_TTL_HOURS> hours

ACTION:
Claiming this task.
```

## Heartbeat — MSG-HEARTBEAT-01

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

## Reclaim — MSG-RECLAIM-01

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

## Handoff — MSG-HANDOFF-01

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

## Blocked — MSG-BLOCKED-01

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

## Decision — MSG-DECISION-01

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

## Specification block — MSG-SPEC-BLOCK-01

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

## Specification clear — MSG-SPEC-CLEAR-01

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

## Complete — MSG-COMPLETE-01

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

## Regression — MSG-REGRESSION-01

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

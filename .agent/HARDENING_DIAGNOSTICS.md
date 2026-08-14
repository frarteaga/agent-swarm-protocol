# Hardening Diagnostics

GitHub Actions job logs are a convenience, not the durable diagnostic contract for long-running mutation and architecture-hardening work.

## Why a separate diagnostic contract exists

A hardening job may expose a failed/red step while the log endpoint available to an agent returns incomplete, truncated, delayed, or otherwise unusable stdout/stderr. Event-triggered or comment-triggered workflows may also be difficult to rediscover from commit-associated workflow listings.

Agents MUST NOT enter a retry loop repeatedly fetching the same unusable raw job log. Long-running hardening must persist its own durable evidence.

## Durable diagnostic contract

Every mutation or hardening gate that can fail after a long run SHOULD persist diagnostic material independently of the transient job-log view.

A workflow implementing this contract SHOULD:

1. execute the gate while capturing combined stdout/stderr to a deterministic file;
2. preserve the real command exit code separately;
3. upload the diagnostic directory under an always-run/finally-equivalent path so failure does not suppress the artifact;
4. restore the original pass/fail conclusion only after diagnostic persistence and durable self-reporting have had a chance to run;
5. publish a durable Issue/PR pointer containing the run identity, attempt, gate, reviewed revision, base revision, artifact identity, exit code/outcome, and retrieval procedure;
6. avoid changing the exact reviewed production revision merely to improve observability.

One shell-style capture pattern is:

```bash
mkdir -p hardening-diagnostics
set +e
command 2>&1 | tee hardening-diagnostics/<gate>.log
rc=${PIPESTATUS[0]}
set -e
printf '%s\n' "$rc" > hardening-diagnostics/<gate>.exit-code
# persist diagnostics and durable pointers before restoring failure from rc
```

Equivalent mechanisms are valid in other shells/runtimes as long as they preserve the same semantics.

For multi-command gates, save each phase separately and retain enough information to identify the first failing phase and exit code.

## Recommended artifact contents

A hardening diagnostic artifact SHOULD contain, as applicable:

- context with repository, PR/Issue, reviewed SHA, base SHA, run identity/attempt, gate name, runner/runtime/tool versions, and exact command;
- the affected-target or selected-mutant manifest;
- the effective mutation budget when mutation is budgeted;
- complete stdout/stderr for the gate or each phase;
- exit code(s);
- survivor results/diffs or acceptance-mutation output;
- cache/source identity needed to determine whether a retry may safely reuse state.

Use stable artifact names that make the owning task, gate, and execution distinguishable.

Artifacts are evidence, not cache. Mutation caches/manifests keep their own lifecycle and invalidation rules.

## Durable Issue/PR pointer

Hardening workflows that may not be discoverable reliably through ordinary PR/commit workflow listings SHOULD self-report with a concise durable comment such as:

```text
[ARCHITECT HARDENING DIAGNOSTIC]
ISSUE: #<n>
PR: #<n if applicable>
GATE: <gate-name>
STATUS: <success|failure>
RUN_ID: <id>
RUN_ATTEMPT: <attempt>
REVIEWED_SHA: <sha>
BASE_SHA: <sha>
ARTIFACT: <stable artifact identity>
EXIT_CODE: <code>
RETRIEVAL: <deterministic artifact retrieval procedure>
```

Do not paste enormous mutation output into the Issue or PR. The durable comment is the index; the artifact is the complete evidence. A short survivor/error summary may be included when useful.

## Agent retrieval order on failure

When a mutation/hardening run is red:

1. read the owning Issue/PR diagnostic pointer first;
2. retrieve the artifact using the reported run/artifact identity;
3. inspect the persisted log, target/selection manifest, exit code, and relevant cache identity;
4. classify the failure;
5. use job/step status only for coarse localization;
6. raw job logs may be tried opportunistically, but once shown incomplete or unusable for that execution, do not repeatedly retry them instead of using the durable artifact.

## Failure classification

- **Real surviving mutants or inadequate tests:** return focused evidence to `developer`; production/test changes must receive fresh independent review when required before architect hardening becomes current again.
- **Deterministic harness/code/test defect:** hand to the role that owns the defect; any relevant implementation change invalidates evidence for the affected scope.
- **Transient runner/OOM/resource failure:** rerun the exact reviewed revision when safe; preserve the selected scope and lower concurrency if required.
- **Acceptance/Gherkin mutation failure:** classify and report independently from language mutation.
- **Missing or corrupt diagnostic evidence:** do not reinterpret absence of logs as a product/code failure. Repair the observability path or rerun the exact reviewed revision when policy permits.

## Core invariant

Hardening evidence must remain recoverable and attributable to the exact reviewed scope even when a chat session, runner process, workflow view, or raw log endpoint is lost or incomplete.

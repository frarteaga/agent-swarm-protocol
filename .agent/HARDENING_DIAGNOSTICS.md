# Hardening Diagnostics

GitHub Actions job logs are a convenience, not the durable diagnostic contract for long-running mutation and architecture-hardening work.

## Why a separate diagnostic contract exists

**[DIAG-RETRY-01]** A hardening job may be red while an agent-visible log is incomplete, truncated, delayed, or unusable; event/comment workflows may also be hard to rediscover. Agents MUST NOT repeatedly retry the same unusable raw log. Long-running hardening must persist its own durable evidence.

## Durable diagnostic contract

**[DIAG-PERSIST-01]** Every mutation/hardening gate that can fail after a long run SHOULD persist diagnostics independently of transient logs. A conforming workflow SHOULD capture combined stdout/stderr deterministically; preserve real exit code; persist diagnostics on an always-run/finally-equivalent path; restore pass/fail only after persistence/durable self-reporting; publish a durable Issue/PR pointer with run/attempt/gate/reviewed+base revisions/artifact/outcome/exit/retrieval; and avoid changing the exact reviewed production revision merely to improve observability.

One valid shell pattern is:

```bash
mkdir -p hardening-diagnostics
set +e
command 2>&1 | tee hardening-diagnostics/<gate>.log
rc=${PIPESTATUS[0]}
set -e
printf '%s\n' "$rc" > hardening-diagnostics/<gate>.exit-code
# persist diagnostics and durable pointers before restoring failure from rc
```

Equivalent mechanisms are valid if semantics match. Multi-command gates save each phase and identify the first failing phase/exit code.

## Recommended artifact contents

**[DIAG-ARTIFACT-01]** A diagnostic artifact SHOULD include, as applicable: repository/PR/Issue, reviewed/base SHA, run/attempt, gate, runner/runtime/tool versions and exact command; affected-target/selected-mutant manifest; effective mutation budget; complete phase logs; exit codes; survivor/acceptance-mutation output; and cache/source identity needed to judge safe reuse. Use stable task/gate/execution-distinguishing names. Artifacts are evidence, not cache; mutation caches/manifests retain their own lifecycle/invalidation policy.

## Durable Issue/PR pointer

**[DIAG-POINTER-01]** Hardening workflows that are not reliably discoverable SHOULD self-report concisely:

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

Do not paste enormous mutation output into Issue/PR; the durable comment is the index and the artifact holds complete evidence. A short survivor/error summary may be included.

## Agent retrieval order on failure

**[DIAG-RETRIEVE-01]** On red mutation/hardening: read the owning Issue/PR pointer; retrieve the named artifact; inspect persisted log, target/selection manifest, exit code and relevant cache identity; classify failure; use job/step status only for coarse localization. Raw job logs may be tried opportunistically, but after being shown unusable for that execution, do not repeatedly retry them instead of durable evidence.

## Failure classification

**[DIAG-CLASSIFY-01]** Route evidence by class:

- real surviving mutants/inadequate tests -> developer; production/test changes receive fresh independent review when required before hardening is current;
- deterministic harness/code/test defect -> owning role; relevant implementation change invalidates affected evidence;
- transient runner/OOM/resource failure -> rerun exact reviewed revision when safe, preserve selected scope, lower concurrency if required;
- acceptance/Gherkin mutation failure -> classify/report independently from language mutation;
- missing/corrupt diagnostics -> do not reinterpret missing logs as product/code failure; repair observability or rerun exact reviewed revision when policy permits.

## Core invariant

**[DIAG-INVARIANT-01]** Hardening evidence must remain recoverable and attributable to the exact reviewed scope even when chat session, runner process, workflow view, or raw log endpoint is lost/incomplete.

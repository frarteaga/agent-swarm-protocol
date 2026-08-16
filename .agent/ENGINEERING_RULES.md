# Engineering Rules

These rules define the default engineering and verification discipline for the swarm. They are inspired by the testing, quality, and hardening constraints used by Uncle Bob's SwarmForge, while remaining transport- and language-agnostic.

A human or an explicitly selected work mode may narrow these gates for a particular task. Otherwise they are mandatory.

## 1. Deterministic evidence

Quality metrics MUST be produced by deterministic tools. An agent MUST NOT estimate, intuit, or invent coverage, complexity, CRAP, duplication, mutation counts, mutation scores, or test results.

For every quality gate it owns, the agent MUST record enough evidence in the PR or handoff to reproduce the result:

- exact command or project script;
- tool/version when relevant;
- source/test scope;
- numeric result when the tool produces one;
- pass/fail outcome.

Prefer project-local, version-controlled commands and configuration. Given the same revision, configuration, and tool version, the measurement SHOULD be reproducible.

## 2. Canonical tooling

For Gherkin acceptance work, use `github.com/unclebob/Acceptance-Pipeline-Specification` (APS). Use APS-supplied `gherkin-parser` and `gherkin-mutator`; do not reimplement those tools inside the project.

When the project language has canonical SwarmForge tools, prefer them:

- Go: `mutate4go`, `crap4go`, `dry4go`;
- Clojure: `clj-mutate`, `crap4clj`, `dry4clj`;
- Java: `mutate4java`, `crap4java`, `dry4java`.

For other languages, use project-configured deterministic equivalents for mutation, CRAP/complexity+coverage, coverage, and duplication. Do not substitute an LLM judgment for a missing metric. If a required deterministic gate has no viable tool, record the missing gate and escalate to `architect` or the human rather than pretending it passed.

Before relying on an unfamiliar tool, inspect its project documentation/help. Do not use stale cached or vendored quality tools when the project explicitly requires a fresher canonical version and the environment permits obtaining it.

## 3. Testable boundaries

Keep behavior in testable modules whenever possible. Environmentally unsuitable code—GUI launchers, device access, network shells, external-process adapters, framework bootstrapping, or code that cannot run safely under automated tests—SHOULD be isolated behind small adapter boundaries.

Only appropriate testable modules should participate in unit coverage, mutation, CRAP, and similar tools. Exclusions MUST be structural and documented; never exclude difficult code merely to improve metrics.

Keep generated acceptance tests separate from unit tests. Keep property tests separate from normal unit/acceptance verification unless the owning role explicitly runs them.

## 4. Unit TDD

New or changed production behavior is implemented with TDD by default:

1. write or modify a focused unit test first;
2. run it and confirm it fails for the expected reason against the pre-change behavior;
3. write only enough production code to make it pass;
4. refactor while keeping tests green;
5. repeat in small behavior slices.

A generated acceptance test is not a substitute for a focused unit test.

Legitimate exceptions include documentation-only changes, generated artifacts, configuration-only changes without executable behavior, explicitly approved exploratory spikes, or environment-only changes for which a focused automated test cannot reasonably be written first. The exception and rationale MUST be recorded in the PR.

## 5. Acceptance testing

The accepted Gherkin is executable specification.

Running acceptance verification means, where applicable:

1. parse/validate Gherkin with APS `gherkin-parser`;
2. generate the project-specific acceptance entrypoints;
3. execute the generated acceptance tests through the project acceptance runtime/step handlers.

Run acceptance generation and execution sequentially. Do not treat acceptance tests as unit tests.

## 6. Coverage

Coverage MUST be measured with a deterministic coverage tool over the intended testable scope.

There is no invented universal percentage threshold. Follow the project threshold if one exists. Otherwise:

- run coverage on changed behavior;
- increase coverage where reasonable;
- do not accept important new behavior that is untested merely because aggregate coverage is high;
- any meaningful coverage decrease in touched code MUST be explained and resolved or explicitly accepted.

## 7. CRAP gate

Use a deterministic CRAP tool (or a deterministic project-configured equivalent).

Before quality-gate handoff, changed/new testable code MUST be brought to **CRAP <= 6** at the tool's relevant function/method granularity, matching the SwarmForge constraint.

Do not manually calculate or approximate CRAP when a tool is available. If the language lacks a viable deterministic CRAP implementation, escalate the missing gate rather than fabricate a value.

## 8. DRY gate

Run a deterministic duplication/DRY tool over the relevant source scope. Reduce duplicate code where reasonable without introducing worse coupling or premature abstraction.

Do not invent a duplication percentage threshold unless the project defines one.

## 9. Mutation-site size gate

Use the language mutation tool's scan/count mode, or a deterministic equivalent, on every changed or new source file.

If any changed/new source file contains **more than 100 mutation sites**, perform a reasonable behavior-preserving split before quality-gate handoff unless a human explicitly approves an exception.

Preserve mutation manifests across splits. Mutation manifests MUST NOT be hand-edited.

## 10. Language mutation hardening

Mutation testing is a final hardening gate, separate from ordinary developer/reviewer feedback loops.

### Fast-CI rule

Full language mutation MUST NOT run by default on every ordinary `push` or `pull_request` update. The normal fast CI path should keep deterministic gates such as unit tests, acceptance tests, coverage, CRAP, DRY, and mutation-site counting, but reserve mutation execution for the owning hardening stage.

By default, language mutation begins only after reviewer quality gates pass and the task is handed to `architect`, or when a human explicitly requests an earlier mutation run.

A project MAY implement this as a separate hardening workflow, an explicit/manual workflow dispatch, a role-transition trigger, or another deterministic mechanism that avoids putting mutation testing in the edit/push feedback loop.

### Generated and declarative artifacts

Language mutation applies to behavioral production code. Versioned generated or declarative artifacts—such as generated source snapshots, schema snapshots, or declarative database migration revisions—MAY be structurally excluded when mutating them would test representation rather than behavior.

Such exclusions MUST be explicit and project-configured. They MUST instead be verified with deterministic generation, migration, integration, schema, or round-trip tests appropriate to the artifact.

Any reusable transformation, validation, normalization, state rule, or other business behavior used by such an artifact MUST live in ordinary testable code and remains in normal unit/property/mutation scope. Structural exclusions MUST NOT be used to hide difficult behavioral code from mutation testing.

### Budgeted pull-request hardening

Per-PR language mutation is **budgeted**, not an exhaustive full-project campaign.

- The default target is **200 mutant executions per PR**.
- The normal hard ceiling is **300 mutant executions per PR**. Exceed it only when a human explicitly approves the additional cost or when a narrowly bounded critical/security change requires it and the rationale is recorded.
- Select mutants deterministically, prioritizing changed/new behavioral production code first, then directly affected high-value core behavior. Use stable ordering such as repository path plus mutation identifier so the same reviewed revision and configuration reproduce the same selected scope.
- Prefer core policy/domain/runtime behavior over environmentally unsuitable IO/process/network shells. Structural shell exclusions remain subject to the testable-boundary rules above and MUST NOT be used to hide business behavior.
- Mutants inside the selected budget are the PR's blocking mutation gate: meaningful survivors or uncovered selected sites must be killed, covered, behavior-preservingly redesigned, or explicitly accepted by a human.
- Mutants outside the selected budget do **not** block that PR. Report them as deferred diagnostic scope rather than generating tests solely to improve an aggregate mutation score.
- After test-only fixes, rerun only surviving/affected selected mutants when the tool can do so reproducibly; do not restart an unaffected mutation campaign.
- Do not add large volumes of narrow contract tests whose only purpose is to chase mutation score when existing deterministic gates already provide adequate confidence in low-risk adapter/shell behavior.

Full-project mutation remains useful as a **periodic/manual diagnostic** (for example scheduled maintenance or an explicit audit), but it is advisory for individual PR delivery by default. Findings from those broader runs should become focused backlog work when they expose meaningful risk; the mere existence of survivors outside a PR's budget is not a release blocker.

A human or explicit work mode may narrow, expand, or waive the mutation budget for a specific task. Record that override durably with the exact PR/revision and keep all other required deterministic gates in force unless the override says otherwise.

### Incremental execution

When owned by the current role:

- run against the exact reviewed revision/scope being hardened;
- use differential or affected-scope mutation when the configured tool supports it;
- preserve valid mutation manifests, incremental state, and tool cache across retries when safe and reproducible;
- do not delete mutation state merely to force a clean run on every retry;
- after test-only changes intended to kill survivors, prefer rerunning surviving/affected selected mutants instead of recomputing unaffected mutants;
- invalidate/recompute the relevant mutation scope when production targets, mutation configuration, mutation-tool version, dependency/runtime assumptions, selected budget, or cached source identity change materially;
- cover uncovered mutation sites and kill meaningful surviving mutants with focused tests or behavior-preserving design improvements;
- do not hand-edit mutation manifests;
- when supported, use deterministic batching and at most `--max-workers 4`; a one-source-file-at-a-time sequential strategy is not required unless the configured tool/project specifically needs it;
- use progress/verbose output for long runs so a slow run is distinguishable from a hang.

If the reviewed production revision changes after mutation evidence was produced, the architect MUST treat that evidence as stale for the affected scope and rerun the relevant hardening before handing to QA.

Do not weaken assertions or mutate production semantics merely to game the mutation tool.

## 11. Gherkin mutation

Gherkin acceptance mutation is a separate final-hardening gate using APS `gherkin-mutator`; it is not part of the ordinary developer/reviewer hot path by default.

Run soft mutation (`--level soft`) when the owning architect/hardening stage performs final acceptance hardening, or earlier only when explicitly requested. Mutation runs SHOULD expose periodic progress/status.

If mutation reveals a no-op or meaningless Gherkin step, prefer fixing/removing the meaningless specification step rather than adding artificial example data solely to satisfy mutation.

## 12. Property testing

Property tests are owned by the architect/hardening stage unless a task explicitly assigns them elsewhere.

Assess useful properties such as:

- invariants;
- broad input ranges;
- round trips;
- conservation properties;
- idempotence;
- ordering;
- parser/formatter stability.

When property tests exist, run them as a separate explicit verification command. Do not silently fold them into ordinary coverage, mutation, or acceptance commands.

## 13. End-to-end QA

The specifier defines user-visible end-to-end QA procedures. QA converts them into executable checks when practical and executes them through the real user interface.

E2E verification MUST NOT use a private/internal project API to bypass the user interface. CLI flags or explicit QA commands are allowed only when they are legitimate user-interface affordances.

## 14. Required verification by role

Unless a human or explicit work mode says otherwise:

- `specifier`: validates specification structure; does not run language mutation/CRAP/DRY;
- `developer`: unit tests + acceptance tests, with TDD for changed behavior; does not run full language/Gherkin mutation as part of the normal development loop;
- `reviewer`: unit + acceptance + coverage + CRAP + DRY + mutation-site count; does not run language mutation or Gherkin mutation;
- `architect`: after reviewer gates pass, runs unit + acceptance + property tests when present + budgeted changed/affected language mutation hardening + soft Gherkin mutation; reruns deterministic structural metrics affected by architectural changes;
- `qa`: final unit/acceptance verification as relevant + property tests when present + specifier E2E suite + CRAP + DRY + project release checks; does not normally rerun mutation testing.

The default mutation ownership path is therefore:

```text
developer fast feedback -> reviewer deterministic gates -> architect budgeted mutation hardening -> qa
```

Every non-specifier role MUST fix or hand back failures before advancing the task.

## 15. Quality evidence block

Use a concise block in the PR/handoff for the gates owned by the role:

```text
[SWARM QUALITY EVIDENCE]

UNIT: <command> -> <result>
ACCEPTANCE: <command> -> <result>
COVERAGE: <command> -> <numeric result/scope>
CRAP: <command> -> max <value>
DRY: <command> -> <result>
MUTATION_SITES: <command> -> max <count/file>
MUTATION: <command> -> <result>
GHERKIN_MUTATION: <command> -> <result>
PROPERTY: <command> -> <result>
E2E: <command> -> <result>
```

Omit gates that the role does not own; never write `PASS` for a gate that was not actually executed.

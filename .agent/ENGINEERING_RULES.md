# Engineering Rules

These are the swarm's default deterministic engineering and verification rules. A human or explicitly selected work mode may narrow them for a task; otherwise they are mandatory.

## Shared quality policy

**[ENG-EVIDENCE-01] Deterministic evidence.** Quality metrics MUST come from deterministic tools; agents MUST NOT estimate, intuit, or invent coverage, complexity, CRAP, duplication, mutation counts/scores, or test results. For each owned gate, record exact command/project script, relevant tool/version, source/test scope, numeric result when produced, and pass/fail. Prefer project-local version-controlled commands/configuration; same revision/config/tool version SHOULD reproduce the measurement.

**[ENG-TOOLING-01] Canonical tooling.** Gherkin acceptance uses APS (`github.com/unclebob/Acceptance-Pipeline-Specification`) and its `gherkin-parser`/`gherkin-mutator`; do not reimplement them. Prefer canonical SwarmForge tools when available: Go `mutate4go/crap4go/dry4go`, Clojure `clj-mutate/crap4clj/dry4clj`, Java `mutate4java/crap4java/dry4java`. Other languages use project-configured deterministic equivalents. Missing required tooling is escalated to architect/human, never replaced by LLM judgment. Inspect unfamiliar tool docs/help; do not use stale cached/vendored tools when a fresher required canonical version is obtainable.

**[ENG-BOUNDARY-01] Testable boundaries.** Keep behavior in testable modules. Environmentally unsuitable GUI/device/network/process/framework bootstrap code SHOULD be isolated behind small adapters. Coverage/mutation/CRAP apply only to appropriate testable scope; exclusions MUST be structural/documented and MUST NOT hide difficult behavior. Generated acceptance tests stay separate from unit tests; property tests stay separately executable unless their owning role explicitly runs them.

**[ENG-TDD-01] Unit TDD.** Changed production behavior uses TDD by default: focused test first; confirm expected failure against pre-change behavior; minimal production change; green; refactor; repeat in small slices. Generated acceptance tests do not replace focused unit tests. Documentation/generated/config-only changes without executable behavior, approved spikes, or environment-only changes may be exceptions; record rationale in the PR and never claim a cycle not executed.

**[ENG-ACCEPTANCE-01] Acceptance.** Accepted Gherkin is executable specification. Where applicable, parse/validate with APS `gherkin-parser`, generate project-specific acceptance entrypoints, then execute them through the project acceptance runtime/step handlers, sequentially. Acceptance tests are not unit tests.

**[ENG-COVERAGE-01] Coverage.** Measure deterministically over intended testable scope. Use project threshold if defined; otherwise cover changed behavior, increase coverage where reasonable, reject important untested new behavior, and explain/resolve or explicitly accept meaningful touched-code decreases. Do not invent a universal threshold.

**[ENG-CRAP-01] CRAP.** Use a deterministic CRAP tool/equivalent. Before quality-gate handoff, changed/new testable code MUST be `CRAP <= 6` at relevant function/method granularity. If no viable deterministic tool exists, escalate rather than fabricate.

**[ENG-DRY-01] DRY.** Run deterministic duplication/DRY analysis over relevant source. Reduce material duplication without worse coupling/premature abstraction. Do not invent a percentage threshold unless project-defined.

**[ENG-MUTATION-SITES-01] Mutation-site size.** Scan/count every changed/new source file deterministically. If any has more than **100 mutation sites**, perform a reasonable behavior-preserving split before quality-gate handoff unless human-approved exception. Preserve manifests across splits; manifests MUST NOT be hand-edited.

## Mutation and hardening

**[ENG-MUTATION-FASTCI-01] Fast CI.** Full language mutation MUST NOT run by default on every ordinary `push`/`pull_request`. Fast CI should retain unit, acceptance, coverage, CRAP, DRY, and mutation-site gates. By default language mutation begins after reviewer gates pass and work reaches architect, or earlier only by human request. Projects MAY use separate/manual/role-triggered deterministic hardening workflows.

**[ENG-MUTATION-ARTIFACT-01] Generated/declarative artifacts.** Language mutation targets behavioral production code. Generated/declarative artifacts MAY be structurally excluded when mutation would test representation, but exclusions MUST be explicit/project-configured and replaced by deterministic generation/migration/integration/schema/round-trip verification. Reusable behavior supporting those artifacts MUST live in ordinary testable code and remain in unit/property/mutation scope; exclusions MUST NOT hide business behavior.

**[ENG-MUTATION-BUDGET-01] Per-PR budget.** Mutation hardening is budgeted: default target **200 mutant executions per PR**, normal hard ceiling **300**. Exceed only with explicit human approval or narrowly bounded critical/security rationale recorded durably. Select deterministically: changed/new behavioral code first, then directly affected high-value core behavior, with stable ordering (e.g. path + mutation ID). Prefer core policy/domain/runtime over unsuitable IO shells. Selected meaningful survivors/uncovered sites block until killed, covered, behavior-preservingly redesigned, or human-accepted. Mutants outside budget do not block; report as deferred diagnostic scope. Do not add large volumes of narrow tests solely to chase aggregate score. Full-project mutation is periodic/manual advisory by default. Human/work mode may narrow/expand/waive budget durably for exact PR/revision without implicitly waiving other gates.

**[ENG-MUTATION-INCREMENTAL-01] Incremental execution.** When owned: harden exact reviewed revision/scope; use differential/affected mutation when supported; preserve valid manifests/cache/state; after test-only survivor fixes rerun surviving/affected selected mutants when reproducible; invalidate relevant evidence when production targets, mutation config/tool version, dependency/runtime assumptions, selected budget, or cached source identity materially changes; cover uncovered selected sites and kill meaningful survivors with focused tests or behavior-preserving design; never hand-edit manifests; deterministic batching/parallelism may use at most `--max-workers 4`; expose progress for long runs. If reviewed production revision changes, architect MUST treat affected mutation evidence as stale and rerun before QA. Never weaken assertions or production semantics to game mutation.

**[ENG-GHERKIN-MUTATION-01] Gherkin mutation.** APS `gherkin-mutator --level soft` is a separate final architect hardening gate, not ordinary developer/reviewer hot path unless explicitly requested. Long runs SHOULD expose progress. If mutation finds a no-op/meaningless Gherkin step, fix/remove the meaningless specification rather than inventing example data solely to satisfy mutation.

**[ENG-PROPERTY-01] Property testing.** Architect/hardening owns property tests unless reassigned. Assess invariants, broad ranges, round trips, conservation, idempotence, ordering, and parser/formatter stability. Run existing property tests as a separate explicit command; do not silently fold into coverage/mutation/acceptance.

**[ENG-E2E-01] End-to-end QA.** Specifier defines user-visible E2E procedures; QA makes them executable when practical and runs through the real user interface. E2E MUST NOT bypass UI via private/internal project API. CLI flags or QA commands are valid only as legitimate user-interface affordances.

## Gate ownership

**[ENG-GATES-01] Default role gates.** Unless a human/work mode overrides:

- `specifier`: specification structure only; no language mutation/CRAP/DRY;
- `developer`: unit + acceptance, TDD for changed behavior; no normal language/Gherkin mutation;
- `reviewer`: unit + acceptance + coverage + CRAP + DRY + mutation-site count; no language/Gherkin mutation;
- `architect`: after reviewer passes, unit + acceptance + property when present + budgeted changed/affected language mutation + soft Gherkin mutation; rerun structural metrics affected by architect changes;
- `qa`: final relevant unit/acceptance + property when present + specifier E2E + CRAP + DRY + project release checks; normally no mutation rerun.

Default path: `developer fast feedback -> reviewer deterministic gates -> architect budgeted mutation hardening -> qa`. Every non-specifier role MUST fix or hand back failures before advancing.

**[ENG-EVIDENCE-FORMAT-01] Quality evidence schema.** For gates actually executed by the role:

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

Omit gates not owned/not executed; never write `PASS` for an unexecuted gate.

# Agent Swarm Protocol

A lightweight GitHub-based coordination protocol for fleets of independent AI software-engineering agents running across separate chats, models, and providers.

GitHub acts as the shared memory and coordination layer: Issues represent work and decisions, PRs represent implementation, comments carry handoffs, and labels track ownership and state.

## Structure

```text
.agent/
├── AGENT_PROTOCOL.md
├── ENGINEERING_RULES.md
├── HARDENING_DIAGNOSTICS.md
├── roles/
│   ├── specifier.md
│   ├── architect.md
│   ├── developer.md
│   ├── reviewer.md
│   ├── security.md
│   └── qa.md
└── bootstrap/
    └── AGENT_BOOTSTRAP.md
```

`AGENT_PROTOCOL.md` defines coordination: claims, handoffs, leases/TTL, stale-work recovery, ownership, specification/security blocks, delivery completion, human-facing status reporting, and regression recovery.

`ENGINEERING_RULES.md` defines the default deterministic engineering discipline: Gherkin/APS acceptance tests, TDD, coverage, CRAP, DRY, mutation-site limits, budgeted mutation hardening, property testing, risk-based security verification, and E2E verification.

`HARDENING_DIAGNOSTICS.md` defines a durable evidence contract for long-running hardening so agents do not depend on transient or incomplete workflow logs.

`AGENT_BOOTSTRAP.md` configures each agent instance with its role, agent ID, target repository, and work-lease TTL.

Under the full/default engineering discipline, the quality path is roughly:

```text
specifier -> architect (design) -> developer -> reviewer -> architect (hardening) -> security (when required) -> qa -> done
```

The architect may therefore participate twice: once for design and again after implementation review for property/mutation hardening. Security is a risk-based gate, not a mandatory serial step for unrelated low-risk changes.

### Security gate

Security becomes required when work affects authentication/authorization, secrets, cryptography, network exposure, privileged process execution, filesystem/sandbox boundaries, untrusted inputs, agent/tool permissions, CI/CD permissions, supply-chain trust, sensitive persistence, or infrastructure/security configuration, or when a human/Architect explicitly requires it.

When selected, the Architect records `SECURITY_GATE: REQUIRED`; the Security Agent performs adversarial assessment and emits one of `SECURITY PASS`, `SECURITY CHANGES REQUIRED`, `SECURITY ARCHITECTURE BLOCK`, or `SECURITY SPEC BLOCK`. A required gate cannot be bypassed by Reviewer or QA while a blocking Security result remains unresolved.

### Fast feedback and mutation hardening

Mutation testing is deliberately kept out of the ordinary edit/push feedback loop. Developer and Reviewer use fast deterministic gates; language mutation and soft Gherkin mutation are deferred to the Architect hardening stage after independent review.

Per-PR language mutation is budgeted by default: target 200 mutant executions, with a normal hard ceiling of 300 unless a human explicitly overrides it. Selection must be deterministic, prioritize changed/affected behavioral code, and bind blocking results to the exact reviewed revision and selected scope. Out-of-budget mutants are diagnostic rather than automatic PR blockers.

Hardening should reuse valid incremental mutation state/cache, rerun surviving/affected selected mutants after test-only fixes when safe, and use bounded deterministic parallelism. Full-project mutation remains useful as a periodic/manual diagnostic rather than a mandatory per-PR campaign.

Long-running hardening should also persist its own stdout/stderr, exit code, selected scope, and revision identity in durable artifacts with an Issue/PR pointer, so a missing or incomplete raw workflow log does not destroy the evidence trail.

## Installation and initialization

1. Copy the `.agent/` directory into the repository and commit it.
2. Create the protocol labels used by that repository (`agent:*` and `state:*` as defined in `AGENT_PROTOCOL.md`), including `agent:security`.
3. Create one persistent LLM chat/session per agent role you intend to run. Initialize each session with its runtime values and tell it to read `.agent/bootstrap/AGENT_BOOTSTRAP.md`:

```text
ROLE: developer
AGENT_ID: developer-01
REPOSITORY: owner/project
WORK_LEASE_TTL_HOURS: 4

Read and follow .agent/bootstrap/AGENT_BOOTSTRAP.md.
```

Each agent then reads the protocol, shared engineering rules, and its corresponding `.agent/roles/<ROLE>.md`, inspects GitHub, and begins work assigned to `agent:<ROLE>`. The same bootstrap is used for every agent; only the runtime values change.

### Migration for existing installations

Repositories already using an earlier five-role version can adopt Security without invalidating current work:

1. copy/update the protocol files, including `.agent/roles/security.md` and `.agent/reference/SWARM_MESSAGES.md`;
2. create the new `agent:security` label without changing existing ownership labels;
3. update local validation/configuration that enumerates canonical roles to include `security`;
4. start a Security Agent only if/when desired; existing low-risk work does not need a retroactive Security gate unless a listed risk criterion or human/Architect decision requires it;
5. for active security-relevant work, record `SECURITY_GATE: REQUIRED|NOT_REQUIRED` before the next downstream handoff and route required work through Security before QA completion.

## Engineering discipline

The default roles intentionally follow much of the engineering rigor used by SwarmForge while keeping GitHub as the communication transport:

- **Specifier:** executable Gherkin plus user-interface E2E QA procedures.
- **Developer:** strict red/green/refactor TDD plus executable acceptance tests.
- **Reviewer:** independent review plus deterministic coverage, **CRAP <= 6**, DRY analysis, **<= 100 mutation sites per changed/new source file**, and an exact `PR`/`REVIEWED_SHA`/`BASE_SHA` handoff.
- **Architect:** architecture review, Security-gate selection, property testing, budgeted affected-scope/incremental language mutation hardening, and soft Gherkin mutation.
- **Security:** risk-based adversarial assessment, deterministic/reproducible security tooling, exploitability triage, safe evidence, and remediation re-verification.
- **QA:** final acceptance/E2E/property verification plus final CRAP/DRY and release checks; verifies a current Security PASS when required; implementation work reaches `state:done` only after the delivery invariant is satisfied.

Metrics and security-tool results must come from deterministic/reproducible tools where available; agents must never estimate or invent quality numbers or claim unexecuted security evidence.

## Inspiration

This project was inspired by Robert C. Martin (Uncle Bob)'s [SwarmForge](https://github.com/unclebob/swarm-forge), particularly its role-based organization, explicit handoff discipline, TDD/acceptance pipeline, deterministic quality gates, mutation testing, and architecture-focused verification.

This protocol takes a different approach to transport and coordination: instead of local tmux/file-based messaging, independent agents communicate through GitHub so they can run in separate ChatGPT, Perplexity, or other LLM sessions.

## Goal

Keep multi-agent software development simple, auditable, recoverable, deterministic, secure, and easy for a human to supervise.

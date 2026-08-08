# Agent Swarm Protocol

A lightweight GitHub-based coordination protocol for fleets of independent AI software-engineering agents running across separate chats, models, and providers.

GitHub acts as the shared memory and coordination layer: Issues represent work and decisions, PRs represent implementation, comments carry handoffs, and labels track ownership and state.

## Structure

```text
.agent/
├── AGENT_PROTOCOL.md
├── roles/
│   ├── specifier.md
│   ├── architect.md
│   ├── developer.md
│   ├── reviewer.md
│   └── qa.md
└── bootstrap/
    └── AGENT_BOOTSTRAP.md
```

`AGENT_PROTOCOL.md` defines the shared workflow, including claims, handoffs, leases/TTL, stale-work recovery, role ownership, review/QA transitions, specification blocks, and regression recovery.

`AGENT_BOOTSTRAP.md` configures each agent instance with its role, agent ID, target repository, and work-lease TTL.

## Installation and initialization

1. Copy the `.agent/` directory into the repository the swarm will work on and commit it.
2. Create the protocol labels used by that repository (`agent:*` and `state:*` as defined in `AGENT_PROTOCOL.md`).
3. Create one persistent LLM chat/session per agent. Initialize each session with its runtime values and tell it to read `.agent/bootstrap/AGENT_BOOTSTRAP.md`:

```text
ROLE: developer
AGENT_ID: developer-01
REPOSITORY: owner/project
WORK_LEASE_TTL_HOURS: 4

Read and follow .agent/bootstrap/AGENT_BOOTSTRAP.md.
```

Each agent then reads the shared protocol and its corresponding `.agent/roles/<ROLE>.md`, inspects GitHub, and begins work assigned to `agent:<ROLE>`. The same bootstrap is used for every agent; only the runtime values change.

## Inspiration

This project was inspired by Robert C. Martin (Uncle Bob)'s [SwarmForge](https://github.com/unclebob/swarm-forge), particularly its role-based agent organization and explicit handoff discipline.

This protocol takes a different approach to transport and coordination: instead of local tmux/file-based messaging, independent agents communicate through GitHub so they can run in separate ChatGPT, Perplexity, or other LLM sessions.

## Goal

Keep multi-agent software development simple, auditable, recoverable, and easy for a human to supervise.
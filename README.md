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

## Inspiration

This project was inspired by Robert C. Martin (Uncle Bob)'s [SwarmForge](https://github.com/unclebob/swarm-forge), particularly its role-based agent organization and explicit handoff discipline.

This protocol takes a different approach to transport and coordination: instead of local tmux/file-based messaging, independent agents communicate through GitHub so they can run in separate ChatGPT, Perplexity, or other LLM sessions.

## Goal

Keep multi-agent software development simple, auditable, recoverable, and easy for a human to supervise.
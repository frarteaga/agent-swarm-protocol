# Agent Bootstrap

## Runtime configuration

```text
ROLE: {{ROLE}}
AGENT_ID: {{AGENT_ID}}
REPOSITORY: {{REPOSITORY}}
WORK_LEASE_TTL_HOURS: {{WORK_LEASE_TTL_HOURS}}
```

Recommended TTL default: `4` hours.

**[BOOT-IDENTITY-01]** These supplied values are authoritative. Do not infer identity from model/provider, chat title/history, GitHub username, or another agent. All repository operations MUST target `{{REPOSITORY}}` unless a human explicitly says otherwise.

## Required load order

**[BOOT-LOAD-01]** Before work, read in order:

1. `.agent/AGENT_PROTOCOL.md`;
2. `.agent/ENGINEERING_RULES.md`;
3. `.agent/roles/{{ROLE}}.md`.

Those files are the canonical rules; this bootstrap does not restate them.

## Startup algorithm

**[BOOT-DISCOVERY-01]** Inspect current `{{REPOSITORY}}`; find `agent:{{ROLE}}` work; prefer `state:ready` and inspect `state:working` for expired leases; read the complete relevant Issue, linked PRs, current comments/handoffs/decisions/evidence/human instructions, and relevant CI/repository state; normalize invalid workflow labels; claim/reclaim before modification when applicable; execute only `{{ROLE}}` responsibilities and owned deterministic gates.

If no work is assigned, stop. Do not invent work or silently switch role. Newer GitHub state overrides stale private chat; explicit human instruction has highest authority. Use the canonical protocol messages whenever durable responsibility/state changes.

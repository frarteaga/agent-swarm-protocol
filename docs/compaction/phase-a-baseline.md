# Phase A — Baseline and audit contract

Issue: #4  
Base commit: `6763a95d5a877d750c54391d0529f500d5496abc`

## Stable byte baseline

| Artifact | Bytes |
|---|---:|
| `.agent/AGENT_PROTOCOL.md` | 17,040 |
| `.agent/ENGINEERING_RULES.md` | 14,407 |
| `.agent/HARDENING_DIAGNOSTICS.md` | 5,146 |
| `.agent/bootstrap/AGENT_BOOTSTRAP.md` | 4,205 |
| `.agent/roles/architect.md` | 8,333 |
| `.agent/roles/developer.md` | 7,002 |
| `.agent/roles/qa.md` | 7,497 |
| `.agent/roles/reviewer.md` | 6,393 |
| `.agent/roles/specifier.md` | 5,316 |
| **Total `.agent` Markdown** | **75,339** |

Root `README.md`: **5,367 bytes**, explicitly outside canonical agent startup context.

Canonical Bundle 1 before compaction uses raw UTF-8 bytes joined by one LF in this order:

1. `.agent/bootstrap/AGENT_BOOTSTRAP.md`
2. `.agent/AGENT_PROTOCOL.md`
3. `.agent/ENGINEERING_RULES.md`
4. `.agent/roles/<role>.md`

The same serialization is used before/after. Before compaction durable-message templates are already inside `AGENT_PROTOCOL.md`, so Bundle 2 equals Bundle 1.

| Role | Baseline Bundle 1 bytes |
|---|---:|
| specifier | 40,971 |
| architect | 43,988 |
| developer | 42,657 |
| reviewer | 42,048 |
| qa | 43,152 |

The three extra bytes versus simple file-size addition are the deterministic LF separators.

## Pinned token measurement

Stable metric: bytes. Comparative token metric: `tiktoken==0.13.0`, `o200k_base`.

Exact reproducible commands:

```bash
python -m pip install 'tiktoken==0.13.0'
python scripts/measure_agent_context.py \
  --encoding o200k_base \
  --ref 6763a95d5a877d750c54391d0529f500d5496abc
```

The PR audit workflow runs the same script against the exact base and PR HEAD and enforces the Issue #4 >=30% Bundle-1 floor in both bytes and pinned tokens. Phase G records the resulting before/after table.

## Duplicate audit

Deterministic command:

```bash
python scripts/audit_protocol_semantics.py \
  --ref 6763a95d5a877d750c54391d0529f500d5496abc \
  --threshold 0.55
```

Policy: path+heading sections; formatting-only normalization that preserves RFC words; exact normalized duplicate detection; 5-word shingles; Jaccard threshold `0.55`; deterministic sort; human semantic adjudication before consolidation. Similarity is candidate generation, never semantic truth.

## Human adjudication summary

The dominant safe consolidation candidates are shared policy repeated in bootstrap/roles: GitHub-memory and human-precedence rules; claim/lease/reclaim mechanics; handoff/block/spec-block behavior; TDD/acceptance; coverage/CRAP/DRY/mutation-site thresholds; mutation ownership; E2E boundaries; and completion/regression rules. Their canonical destinations are `AGENT_PROTOCOL.md` or `ENGINEERING_RULES.md`; role files retain only role-specific deltas. Hardening diagnostics remain on-demand.

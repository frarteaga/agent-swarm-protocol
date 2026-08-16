# Phase G — Context/token measurement

Issue: #4  
Baseline: `6763a95d5a877d750c54391d0529f500d5496abc`  
Measured compacted HEAD: `0f6c453f50ec21c487bd2e29197eaf169ff1d586`  
GitHub Actions run: `31954361599`, job `95182583858` — **PASS**.

Phase G adds only this report outside `.agent`, so the measured agent-context bytes/tokens are identical to the final PR content. The final PR-head workflow reruns the same checks.

## Reproducible environment and commands

GitHub Actions used Python 3.12.13 and the Issue-pinned tokenizer:

```bash
python -m pip install 'tiktoken==0.13.0'
python scripts/measure_agent_context.py \
  --encoding o200k_base \
  --ref 0f6c453f50ec21c487bd2e29197eaf169ff1d586 \
  --compare-ref 6763a95d5a877d750c54391d0529f500d5496abc \
  --minimum-startup-reduction 30
```

The script serializes each bundle as raw UTF-8 file bytes joined by one LF byte in the documented order. README is measured separately and never silently counted as startup context.

## Individual Markdown footprint

| Artifact | Before bytes / tokens | After bytes / tokens |
|---|---:|---:|
| `.agent/AGENT_PROTOCOL.md` | 17,040 / 3,680 | 9,722 / 2,115 |
| `.agent/ENGINEERING_RULES.md` | 14,407 / 2,808 | 9,131 / 1,913 |
| `.agent/HARDENING_DIAGNOSTICS.md` | 5,146 / 1,033 | 4,191 / 902 |
| `.agent/bootstrap/AGENT_BOOTSTRAP.md` | 4,205 / 956 | 1,449 / 338 |
| `.agent/reference/SWARM_MESSAGES.md` | — | 2,570 / 737 |
| `.agent/roles/specifier.md` | 5,316 / 995 | 2,853 / 587 |
| `.agent/roles/architect.md` | 8,333 / 1,563 | 3,704 / 747 |
| `.agent/roles/developer.md` | 7,002 / 1,352 | 3,806 / 788 |
| `.agent/roles/reviewer.md` | 6,393 / 1,221 | 3,069 / 669 |
| `.agent/roles/qa.md` | 7,497 / 1,495 | 3,986 / 812 |
| **Total `.agent` Markdown** | **75,339 / 15,103** | **44,481 / 9,608** |

Total versioned `.agent` Markdown shrinks **30,858 bytes (40.96%)** and **5,495 pinned tokens (36.38%)** even after adding the on-demand message reference. `README.md` remains unchanged and separate at **5,367 bytes / 1,120 tokens**.

## Bundle 1 — normal startup context

Canonical startup bundle is bootstrap + protocol + engineering rules + active role.

| Role | Bytes before → after | Byte reduction | Tokens before → after | Token reduction |
|---|---:|---:|---:|---:|
| specifier | 40,971 → 23,158 | **43.48%** | 8,439 → 4,953 | **41.31%** |
| architect | 43,988 → 24,009 | **45.42%** | 9,007 → 5,113 | **43.23%** |
| developer | 42,657 → 24,111 | **43.48%** | 8,796 → 5,154 | **41.41%** |
| reviewer | 42,048 → 23,374 | **44.41%** | 8,665 → 5,035 | **41.89%** |
| qa | 43,152 → 24,291 | **43.71%** | 8,939 → 5,178 | **42.07%** |

**Acceptance floor:** every role exceeds the Issue #4 requirement of >=30% reduction in both bytes and pinned tokens. The primary startup result also lands inside the requested 40–60% target range for both bytes and tokens.

## Bundle 2 — startup plus first durable swarm message

Because Phase E was executed, Bundle 2 conservatively adds the **entire** `.agent/reference/SWARM_MESSAGES.md` before the first durable message rather than hiding template cost.

| Role | Bytes before → after | Byte reduction | Tokens before → after | Token reduction |
|---|---:|---:|---:|---:|
| specifier | 40,971 → 25,729 | **37.20%** | 8,439 → 5,690 | **32.57%** |
| architect | 43,988 → 26,580 | **39.57%** | 9,007 → 5,850 | **35.05%** |
| developer | 42,657 → 26,682 | **37.45%** | 8,796 → 5,891 | **33.03%** |
| reviewer | 42,048 → 25,945 | **38.30%** | 8,665 → 5,772 | **33.39%** |
| qa | 43,152 → 26,862 | **37.75%** | 8,939 → 5,915 | **33.83%** |

This confirms template extraction is a real net reduction even at the first durable-message boundary.

## Duplicate and RFC 2119 audit

Exact command used for both refs:

```bash
python scripts/audit_protocol_semantics.py --ref <SHA> --threshold 0.55
```

The deterministic lexical audit reports:

- normative sections: **125 → 39**;
- exact normalized duplicates: **0 → 0**;
- 5-word-shingle Jaccard candidates at threshold 0.55: **0 → 0**.

The zero lexical candidates are expected: the major redundancy was conceptual/paraphrased shared policy, not verbatim text. The lexical scan is intentionally an under-approximation; Phase A human semantic adjudication identified the cross-file policy copies, and Phase F maps every pre-change normative concept to its canonical destination.

Aggregate RFC 2119 keyword census:

| Keyword | Before | After | Explanation |
|---|---:|---:|---|
| `MAY` | 5 | 4 | Two adjacent specifier permissions were compacted into one `MAY ... and ...` clause; permission is unchanged. |
| `MUST` | 28 | 24 | Repeated role/bootstrap imperatives were consolidated into canonical rules; Phase E adds the mandatory canonical-schema load safeguard before message emission. |
| `MUST NOT` | 19 | 18 | One duplicated bootstrap prohibition (silent role switching) now exists only in the canonical protocol. |
| `SHOULD` | 12 | 12 | Preserved. |
| `SHOULD NOT` | 1 | 1 | Preserved. |

The censure is a regression tripwire, not a semantic-equivalence proof. Semantic preservation is established by the 117-entry old→new map plus independent reviewer-role inspection of the exact final PR HEAD.

## Structural verification

CI also ran:

```bash
python scripts/check_protocol_structure.py
```

Result:

```text
OK: 117 old inventory IDs mapped exactly once to 106 unique canonical definitions
```

The checker additionally protects required sections, ID uniqueness, CRAP/mutation thresholds, reviewer exact-SHA fields, delivery invariant, mandatory message-reference loading, and all required durable-message fields/literals.

## Final review gate

This implementation is ready for the Issue #4 independent review gate. The reviewer MUST be a separate reviewer-role agent/session that did not author the compaction and MUST review the exact final PR HEAD. Any finding that exposes semantic drift requires correction and fresh measurement before merge.

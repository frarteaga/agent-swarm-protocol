#!/usr/bin/env python3
"""Structural tripwires for the canonical swarm protocol.

This intentionally does not claim semantic proof; it detects missing files/sections,
ID coverage errors, threshold/schema loss, role/label drift, and accidental duplicate definitions.
"""
from __future__ import annotations

import collections
import re
from pathlib import Path

ROLES = ("specifier", "architect", "developer", "reviewer", "security", "qa")
REQUIRED = [
    ".agent/AGENT_PROTOCOL.md",
    ".agent/ENGINEERING_RULES.md",
    ".agent/HARDENING_DIAGNOSTICS.md",
    ".agent/bootstrap/AGENT_BOOTSTRAP.md",
    ".agent/reference/SWARM_MESSAGES.md",
    *[f".agent/roles/{r}.md" for r in ROLES],
    "docs/compaction/phase-a-inventory.md",
    "docs/compaction/phase-f-equivalence.md",
]
DEF_ID = re.compile(r"\[((?:PROTO|ENG|ROLE|BOOT|DIAG)-[A-Z0-9-]+-\d{2})\]")
MSG_DEF = re.compile(r"^## .+ — (MSG-[A-Z0-9-]+-\d{2})$", re.M)
OLD_ID = re.compile(r"OLD-[A-Z]+-\d{3}")
MAP_ROW = re.compile(r"^\| `(OLD-[A-Z]+-\d{3})` \| `([A-Z]+-[A-Z0-9-]+-\d{2})` \|", re.M)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def section(text: str, msg_id: str) -> str:
    m = re.search(rf"^## .+ — {re.escape(msg_id)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    require(bool(m), f"missing message section {msg_id}")
    return m.group(1)


def main() -> int:
    for path in REQUIRED:
        require(Path(path).is_file(), f"missing required file: {path}")

    role_headings = ("## Mission", "## Role-specific rules", "## Outcomes", "## Completion condition")
    for role in ROLES:
        text = read(f".agent/roles/{role}.md")
        for heading in role_headings:
            require(heading in text, f"{role}: missing {heading}")

    protocol = read(".agent/AGENT_PROTOCOL.md")
    engineering = read(".agent/ENGINEERING_RULES.md")
    bootstrap = read(".agent/bootstrap/AGENT_BOOTSTRAP.md")
    messages = read(".agent/reference/SWARM_MESSAGES.md")
    readme = read("README.md")

    for marker in ("## Authority and identity", "## Workflow state and discovery", "## Claims, leases, and recovery", "## Issue, PR, and specification authority", "## Review, security, QA, completion, regression", "## Flow, concurrency, communication"):
        require(marker in protocol, f"protocol missing section {marker}")
    for marker in ("## Shared quality policy", "## Mutation and hardening", "## Gate ownership"):
        require(marker in engineering, f"engineering rules missing section {marker}")
    for marker in ("## Runtime configuration", "## Required load order", "## Startup algorithm"):
        require(marker in bootstrap, f"bootstrap missing section {marker}")

    require("MUST load `.agent/reference/SWARM_MESSAGES.md`" in protocol, "message reference is not mandatory before emission")
    require("[SWARM CLAIM]" not in protocol, "message template duplicated in hot-path protocol")

    # Canonical role/security invariants introduced by Issue #6.
    require("agent:specifier|architect|developer|reviewer|security|qa" in protocol, "security missing from canonical ownership labels")
    require("[PROTO-SECURITY-GATE-01]" in protocol, "security gate policy missing")
    require("SECURITY_GATE: REQUIRED|NOT_REQUIRED" in protocol, "security gate decision marker missing")
    require("`NOT_REQUIRED` is valid only when all listed criteria were evaluated and none apply" in protocol, "security NOT_REQUIRED bypass protection missing")
    require("explicit human override" in protocol, "security human-override semantics missing")
    architect = read(".agent/roles/architect.md")
    require("listed risk criterion applies, record `SECURITY_GATE: REQUIRED`" in architect, "architect can bypass required Security gate")
    require("reviewer->security" in protocol and "security->developer|architect|specifier|qa" in protocol, "security workflow transitions missing")
    require("MSG-SECURITY-RESULT-01" in protocol, "security result schema not referenced by protocol")
    security = read(".agent/roles/security.md")
    for literal in ("SECURITY PASS", "SECURITY CHANGES REQUIRED", "SECURITY ARCHITECTURE BLOCK", "SECURITY SPEC BLOCK", "minimum privileges", "never expose secrets"):
        require(literal in security, f"security role invariant missing: {literal}")
    require("security" in engineering, "security gate ownership missing from engineering rules")
    require("Migration" in readme and "agent:security" in readme, "security migration path missing from README")

    # Canonical definition IDs must be unique; references elsewhere are allowed.
    definitions = []
    for p in Path(".agent").rglob("*.md"):
        t = p.read_text(encoding="utf-8")
        definitions += [(x, str(p)) for x in DEF_ID.findall(t)]
        definitions += [(x, str(p)) for x in MSG_DEF.findall(t)]
    by_id = collections.defaultdict(list)
    for ident, path in definitions:
        by_id[ident].append(path)
    dup = {k: v for k, v in by_id.items() if len(v) != 1}
    require(not dup, f"canonical ID definition duplication: {dup}")

    # Every Phase-A inventory ID maps exactly once to an existing canonical definition.
    inventory_ids = OLD_ID.findall(read("docs/compaction/phase-a-inventory.md"))
    require(len(inventory_ids) == len(set(inventory_ids)), "duplicate old inventory IDs")
    rows = MAP_ROW.findall(read("docs/compaction/phase-f-equivalence.md"))
    mapped_old = [o for o, _ in rows]
    require(collections.Counter(mapped_old) == collections.Counter(inventory_ids), "equivalence map is not exact 1:1 coverage of old inventory IDs")
    unknown_new = sorted({n for _, n in rows if n not in by_id})
    require(not unknown_new, f"equivalence map references undefined canonical IDs: {unknown_new}")

    # Threshold/policy tripwires.
    for literal in ("CRAP <= 6", "100 mutation sites", "200 mutant executions per PR", "300", "--max-workers 4", "--level soft"):
        require(literal in engineering, f"engineering policy literal missing: {literal}")
    reviewer = read(".agent/roles/reviewer.md")
    for literal in ("PR: #<number>", "REVIEWED_SHA:", "BASE_SHA:"):
        require(literal in reviewer, f"reviewer exact-scope field missing: {literal}")
    require("PR MUST be merged" in protocol and "MUST NOT make Issue done" in protocol, "delivery invariant weakened/missing")

    # Durable schemas: required field names/fixed literals must survive extraction.
    required_fields = {
        "MSG-CLAIM-01": ["[SWARM CLAIM]", "AGENT:", "ROLE:", "LEASE:", "ACTION:"],
        "MSG-HEARTBEAT-01": ["[SWARM HEARTBEAT]", "AGENT:", "ROLE:", "STATUS:", "REFS:", "Issue #", "PR #"],
        "MSG-RECLAIM-01": ["[SWARM RECLAIM]", "AGENT:", "ROLE:", "PREVIOUS_AGENT:", "REASON:", "ACTION:", "REFS:", "Issue #", "PR #"],
        "MSG-HANDOFF-01": ["[SWARM HANDOFF]", "FROM:", "ROLE:", "TO:", "STATUS: READY", "ACTION:", "REFS:", "Issue #", "PR #"],
        "MSG-BLOCKED-01": ["[SWARM BLOCKED]", "FROM:", "ROLE:", "TO:", "QUESTION:", "CONTEXT:", "REFS:", "Issue #", "PR #"],
        "MSG-DECISION-01": ["[SWARM DECISION]", "FROM:", "ROLE:", "TO:", "DECISION:", "RATIONALE:", "REFS:", "Issue #", "PR #"],
        "MSG-SPEC-BLOCK-01": ["[SWARM SPEC BLOCK]", "FROM:", "ROLE: specifier", "TO: developer", "REQUIREMENT:", "PROBLEM:", "REQUIRED OUTCOME:", "REFS:", "Issue #", "PR #"],
        "MSG-SPEC-CLEAR-01": ["[SWARM SPEC CLEAR]", "FROM:", "ROLE: specifier", "RESULT:", "REFS:", "Issue #", "PR #"],
        "MSG-SECURITY-RESULT-01": ["[SWARM SECURITY RESULT]", "FROM:", "ROLE: security", "RESULT:", "SCOPE:", "EVIDENCE:", "REFS:", "Issue #", "PR #"],
        "MSG-COMPLETE-01": ["[SWARM COMPLETE]", "FROM:", "ROLE: qa", "RESULT:", "PASS", "REFS:", "Issue #", "PR #"],
        "MSG-REGRESSION-01": ["[SWARM REGRESSION]", "FROM:", "ROLE:", "TYPE:", "REGRESSION", "OBSERVED:", "EXPECTED:", "ORIGINAL_COMPLETION:", "REFS:", "Issue #", "PR #"],
    }
    for msg_id, fields in required_fields.items():
        body = section(messages, msg_id)
        for field in fields:
            require(field in body, f"{msg_id}: missing required field/literal {field}")

    print(f"OK: {len(inventory_ids)} old inventory IDs mapped exactly once to {len(by_id)} unique canonical definitions; roles={','.join(ROLES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

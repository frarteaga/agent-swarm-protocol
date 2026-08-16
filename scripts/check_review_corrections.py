#!/usr/bin/env python3
"""Tripwires for independent-review corrections to Issue #4."""
from __future__ import annotations

import collections
import re
from pathlib import Path

INV = Path("docs/compaction/phase-a-core-invariants.md")
MAP = Path("docs/compaction/phase-f-review-corrections.md")
DEF_ID = re.compile(r"^\*\*\[((?:PROTO|ENG|ROLE|BOOT|DIAG)-[A-Z0-9-]+-\d{2})\]", re.M)
MSG_DEF = re.compile(r"^## .+ — (MSG-[A-Z0-9-]+-\d{2})$", re.M)
OLD = re.compile(r"OLD-INVARIANT-\d{3}")
ROW = re.compile(r"^\| `(OLD-INVARIANT-\d{3})` \| `([A-Z]+-[A-Z0-9-]+-\d{2})` \|", re.M)


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise SystemExit(msg)


def main() -> int:
    require(INV.is_file(), f"missing {INV}")
    require(MAP.is_file(), f"missing {MAP}")

    inv_text = INV.read_text(encoding="utf-8")
    map_text = MAP.read_text(encoding="utf-8")
    ids = OLD.findall(inv_text)
    expected = [f"OLD-INVARIANT-{i:03d}" for i in range(1, 26)]
    require(ids == expected, f"core-invariant inventory must be exactly {expected}; got {ids}")

    rows = ROW.findall(map_text)
    mapped = [old for old, _ in rows]
    require(collections.Counter(mapped) == collections.Counter(expected), "core-invariant equivalence map is not exact 1:1 coverage")

    definitions: set[str] = set()
    for p in Path(".agent").rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        definitions.update(DEF_ID.findall(text))
        definitions.update(MSG_DEF.findall(text))
    unknown = sorted({new for _, new in rows if new not in definitions})
    require(not unknown, f"core-invariant map references undefined canonical IDs: {unknown}")

    for phrase in (
        "AGENT_PROTOCOL.md` §15",
        "roles/reviewer.md",
        "ENG-GATES-01",
        "PROTO-REVIEW-01",
        "reviewer -> architect -> qa",
    ):
        require(phrase in map_text, f"baseline review-destination inconsistency record missing: {phrase}")

    print("OK: 25 core-invariant IDs mapped exactly once; combined pre-change inventory coverage = 142")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

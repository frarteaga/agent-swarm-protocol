#!/usr/bin/env python3
"""Deterministic duplicate-candidate and RFC-2119 audit for protocol Markdown."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

DEFAULT_THRESHOLD = 0.55
RFC = re.compile(r"\b(MUST NOT|SHOULD NOT|MUST|SHOULD|MAY)\b")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CODE_FENCE = re.compile(r"^\s*```")
DIRECTIVE = re.compile(r"\b(do not|never|before|after|when|only|use|run|record|read|inspect|verify|normalize|preserve|keep|prefer|escalate|hand off|stop)\b", re.I)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def paths(ref: str | None) -> list[str]:
    if ref:
        return sorted(p for p in git("ls-tree", "-r", "--name-only", ref, ".agent").decode().splitlines() if p.endswith(".md"))
    return sorted(str(p.as_posix()) for p in Path(".agent").rglob("*.md"))


def read(path: str, ref: str | None) -> str:
    return (git("show", f"{ref}:{path}") if ref else Path(path).read_bytes()).decode("utf-8")


def sections(path: str, text: str):
    current = "<root>"
    buf = []
    in_code = False
    def emit():
        body = "\n".join(buf).strip()
        if body:
            yield {"path": path, "heading": current, "text": body}
    for line in text.splitlines():
        if CODE_FENCE.match(line):
            in_code = not in_code
            continue
        if not in_code:
            m = HEADING.match(line)
            if m:
                yield from emit(); buf.clear(); current = m.group(2).strip(); continue
            buf.append(line)
    yield from emit()


def normalize(text: str) -> str:
    text = re.sub(r"[`*_>#]", "", text)
    text = re.sub(r"^\s*(?:[-+]|\d+[.)])\s+", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_:+./<>-]+", normalize(text).lower())


def shingles(text: str, n: int = 5) -> set[tuple[str, ...]]:
    w = words(text)
    return {tuple(w[i:i+n]) for i in range(max(0, len(w)-n+1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0


def normative(text: str) -> bool:
    n = normalize(text)
    return bool(RFC.search(n) or DIRECTIVE.search(n)) and len(words(n)) >= 5


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    args = ap.parse_args()

    all_sections = []
    census = {}
    for path in paths(args.ref):
        text = read(path, args.ref)
        census[path] = dict(collections.Counter(RFC.findall(text)))
        all_sections += [s for s in sections(path, text) if normative(s["text"])]

    exact_index = collections.defaultdict(list)
    for s in all_sections:
        exact_index[normalize(s["text"])].append(s)
    exact = []
    for norm, hits in exact_index.items():
        if len(hits) > 1:
            exact.append({"sha256": hashlib.sha256(norm.encode()).hexdigest(), "locations": [{"path": h["path"], "heading": h["heading"]} for h in hits]})

    candidates = []
    prepared = [(s, shingles(s["text"])) for s in all_sections]
    for i, (a, sa) in enumerate(prepared):
        if len(sa) < 3:
            continue
        for b, sb in prepared[i+1:]:
            if a["path"] == b["path"] and a["heading"] == b["heading"]:
                continue
            score = jaccard(sa, sb)
            if score >= args.threshold:
                candidates.append({"score": round(score, 4), "a": {"path": a["path"], "heading": a["heading"]}, "b": {"path": b["path"], "heading": b["heading"]}})

    out = {
        "ref": args.ref or "WORKTREE",
        "threshold": args.threshold,
        "shingle_words": 5,
        "normative_sections": len(all_sections),
        "rfc2119_census": {p: {k: census[p].get(k, 0) for k in ("MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY")} for p in sorted(census)},
        "exact_duplicates": sorted(exact, key=lambda x: (x["locations"][0]["path"], x["locations"][0]["heading"])),
        "similarity_candidates": sorted(candidates, key=lambda x: (-x["score"], x["a"]["path"], x["a"]["heading"], x["b"]["path"], x["b"]["heading"])),
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

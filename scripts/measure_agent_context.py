#!/usr/bin/env python3
"""Deterministically measure agent Markdown context bundles.

Pinned PR-A environment: tiktoken==0.13.0, encoding=o200k_base.
Bundle serialization is raw UTF-8 file bytes joined by one LF byte in the
listed order. README.md is reported separately and is never implicit startup
context. If .agent/reference/SWARM_MESSAGES.md exists at a measured ref it is
added only to Bundle 2 (startup + first durable message).
"""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
from pathlib import Path
from typing import Iterable

TIKTOKEN_VERSION = "0.13.0"
DEFAULT_ENCODING = "o200k_base"
ROLES = ("specifier", "architect", "developer", "reviewer", "security", "qa")
COMMON = (
    ".agent/bootstrap/AGENT_BOOTSTRAP.md",
    ".agent/AGENT_PROTOCOL.md",
    ".agent/ENGINEERING_RULES.md",
)
MESSAGE_REFERENCE = ".agent/reference/SWARM_MESSAGES.md"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args])


def read_bytes(path: str, ref: str | None) -> bytes:
    if ref:
        return git("show", f"{ref}:{path}")
    return Path(path).read_bytes()


def exists(path: str, ref: str | None) -> bool:
    if ref:
        return subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
    return Path(path).is_file()


def markdown_paths(ref: str | None) -> list[str]:
    if ref:
        out = git("ls-tree", "-r", "--name-only", ref, ".agent").decode()
        return sorted(p for p in out.splitlines() if p.endswith(".md"))
    return sorted(str(p.as_posix()) for p in Path(".agent").rglob("*.md"))


def join_bundle(paths: Iterable[str], ref: str | None) -> bytes:
    return b"\n".join(read_bytes(p, ref) for p in paths)


def metrics(payload: bytes, encoding) -> dict[str, int]:
    text = payload.decode("utf-8")
    return {"bytes": len(payload), "tokens": len(encoding.encode(text))}


def snapshot(ref: str | None, encoding) -> dict:
    files = {p: metrics(read_bytes(p, ref), encoding) for p in markdown_paths(ref)}
    bundles = {}
    for role in ROLES:
        role_path = f".agent/roles/{role}.md"
        if not exists(role_path, ref):
            continue
        startup = (*COMMON, role_path)
        first_message = startup + ((MESSAGE_REFERENCE,) if exists(MESSAGE_REFERENCE, ref) else ())
        bundles[role] = {
            "bundle1_startup": metrics(join_bundle(startup, ref), encoding),
            "bundle2_first_message": metrics(join_bundle(first_message, ref), encoding),
            "bundle1_files": list(startup),
            "bundle2_files": list(first_message),
        }
    readme = metrics(read_bytes("README.md", ref), encoding) if exists("README.md", ref) else None
    return {"ref": ref or "WORKTREE", "files": files, "readme_separate": readme, "roles": bundles}


def reduction(before: int, after: int) -> dict[str, float | int]:
    saved = before - after
    return {"before": before, "after": after, "saved": saved, "percent": round(saved * 100 / before, 2)}


def compare(before: dict, after: dict) -> dict:
    common_roles = [r for r in ROLES if r in before["roles"] and r in after["roles"]]
    out = {
        "roles": {},
        "added_roles": [r for r in ROLES if r not in before["roles"] and r in after["roles"]],
        "removed_roles": [r for r in ROLES if r in before["roles"] and r not in after["roles"]],
    }
    for role in common_roles:
        out["roles"][role] = {}
        for bundle in ("bundle1_startup", "bundle2_first_message"):
            out["roles"][role][bundle] = {
                unit: reduction(before["roles"][role][bundle][unit], after["roles"][role][bundle][unit])
                for unit in ("bytes", "tokens")
            }
    return out


def ordered_roles(data: dict) -> list[str]:
    return [r for r in ROLES if r in data["roles"]]


def render_markdown(data: dict) -> str:
    lines = [f"# Agent context measurement: `{data['ref']}`", "", "## Individual `.agent` Markdown", "", "| Path | Bytes | o200k tokens |", "|---|---:|---:|"]
    for path, m in data["files"].items():
        lines.append(f"| `{path}` | {m['bytes']} | {m['tokens']} |")
    r = data.get("readme_separate")
    if r:
        lines += ["", f"README.md (separate, not startup): **{r['bytes']} bytes / {r['tokens']} tokens**."]
    lines += ["", "## Role bundles", "", "| Role | Bundle 1 bytes | Bundle 1 tokens | Bundle 2 bytes | Bundle 2 tokens |", "|---|---:|---:|---:|---:|"]
    for role in ordered_roles(data):
        b = data["roles"][role]
        lines.append(f"| {role} | {b['bundle1_startup']['bytes']} | {b['bundle1_startup']['tokens']} | {b['bundle2_first_message']['bytes']} | {b['bundle2_first_message']['tokens']} |")
    return "\n".join(lines)


def render_comparison(data: dict) -> str:
    lines = ["# Context change", "", "| Role | Bundle | Bytes before→after | Bytes saved | Tokens before→after | Tokens saved |", "|---|---|---:|---:|---:|---:|"]
    for role in [r for r in ROLES if r in data["roles"]]:
        for bundle, label in (("bundle1_startup", "startup"), ("bundle2_first_message", "startup + first message")):
            row = data["roles"][role][bundle]
            b, t = row["bytes"], row["tokens"]
            lines.append(f"| {role} | {label} | {b['before']}→{b['after']} | {b['saved']} ({b['percent']}%) | {t['before']}→{t['after']} | {t['saved']} ({t['percent']}%) |")
    if data["added_roles"]:
        lines += ["", "Added roles: " + ", ".join(data["added_roles"])]
    if data["removed_roles"]:
        lines += ["", "Removed roles: " + ", ".join(data["removed_roles"])]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoding", default=DEFAULT_ENCODING)
    ap.add_argument("--ref", help="Git ref to measure; default is worktree")
    ap.add_argument("--compare-ref", help="Optional baseline ref measured by the same script")
    ap.add_argument("--format", choices=("markdown", "json"), default="markdown")
    ap.add_argument("--minimum-startup-reduction", type=float, default=None)
    args = ap.parse_args()

    actual = importlib.metadata.version("tiktoken")
    if actual != TIKTOKEN_VERSION:
        raise SystemExit(f"tiktoken version must be {TIKTOKEN_VERSION}; found {actual}")
    import tiktoken
    enc = tiktoken.get_encoding(args.encoding)

    after = snapshot(args.ref, enc)
    if not args.compare_ref:
        print(json.dumps(after, indent=2, sort_keys=True) if args.format == "json" else render_markdown(after))
        return 0

    before = snapshot(args.compare_ref, enc)
    comp = compare(before, after)
    if args.format == "json":
        print(json.dumps({"before": before, "after": after, "comparison": comp}, indent=2, sort_keys=True))
    else:
        print(render_markdown(before)); print(); print(render_markdown(after)); print(); print(render_comparison(comp))

    if args.minimum_startup_reduction is not None:
        failures = []
        for role in comp["roles"]:
            for unit in ("bytes", "tokens"):
                pct = comp["roles"][role]["bundle1_startup"][unit]["percent"]
                if pct < args.minimum_startup_reduction:
                    failures.append(f"{role} {unit} {pct}%")
        if failures:
            raise SystemExit("startup reduction floor not met: " + ", ".join(failures))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

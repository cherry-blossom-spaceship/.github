#!/usr/bin/env python3
"""GitHub merge gate for portable, rename-resilient repository changes.

The gate examines only files introduced or modified by a pull request. Portable
locations must be expressed through a semantic registry key, repository-root
discovery, or an explicit environment value. A narrowly reviewed, exact-text
exception may be recorded in the repository registry with an issue and expiry.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

PORTABLE_SUFFIXES = {
    ".bash", ".cjs", ".js", ".json", ".mjs", ".py", ".sh", ".toml",
    ".ts", ".tsx", ".yaml", ".yml",
}
REGISTRY = Path(".github/sovereignty-portability-registry.json")
RULES = {
    "Windows drive path": re.compile(r"(?i)(?<![A-Za-z0-9_])[A-Z]:(?:\\|/(?!/))"),
    "POSIX home or mount path": re.compile(r"(?<![A-Za-z0-9_])/(?:home|mnt|c|f)/[A-Za-z0-9_.-]"),
    "UNC host path": re.compile(r"\\\\(?!<)[A-Za-z0-9][A-Za-z0-9_.-]*\\"),
}


def fail(message: str) -> None:
    raise SystemExit(f"Sovereignty / Portability gate failed: {message}")


def parse_registry(root: Path) -> set[str]:
    path = root / REGISTRY
    if not path.is_file():
        fail(f"missing required registry contract: {REGISTRY.as_posix()}")
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"invalid registry JSON: {error}")
    if registry.get("version") != 1 or not isinstance(registry.get("exceptions"), list):
        fail("registry requires version 1 and an exceptions list")

    allowed: set[str] = set()
    today = dt.date.today()
    for entry in registry["exceptions"]:
        if not isinstance(entry, dict):
            fail("registry exceptions must be objects")
        required = ("text", "reason", "issue", "expires")
        if any(not isinstance(entry.get(key), str) or not entry[key].strip() for key in required):
            fail("each exception requires non-empty text, reason, issue, and expires")
        if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/issues/\d+", entry["issue"]):
            fail(f"exception has non-issue URL: {entry['issue']!r}")
        try:
            expiry = dt.date.fromisoformat(entry["expires"])
        except ValueError:
            fail(f"exception expiry is not ISO date: {entry['expires']!r}")
        if expiry < today:
            fail(f"exception expired on {expiry.isoformat()}: {entry['text']!r}")
        allowed.add(entry["text"])
    return allowed


def changed_files(root: Path, base_sha: str) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base_sha}...HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    return [root / relative for relative in result.stdout.splitlines() if relative]


def scan(root: Path, base_sha: str) -> list[str]:
    allowed = parse_registry(root)
    violations: list[str] = []
    for path in changed_files(root, base_sha):
        relative = path.relative_to(root).as_posix()
        if relative == REGISTRY.as_posix() or path.suffix.lower() not in PORTABLE_SUFFIXES or not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.strip() in allowed:
                continue
            for label, pattern in RULES.items():
                if pattern.search(line):
                    violations.append(
                        f"{relative}:{line_number}: {label}; use a registry key, repo-root discovery, or env value"
                    )
    return violations


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        fail("usage: verify_sovereignty_portability.py REPOSITORY_ROOT BASE_SHA")
    root = Path(argv[1]).resolve()
    violations = scan(root, argv[2])
    if violations:
        print("Sovereignty / Portability gate failed:", *violations, sep="\n  ", file=sys.stderr)
        return 1
    print("Sovereignty / Portability gate passed: registry present; no introduced machine-specific paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

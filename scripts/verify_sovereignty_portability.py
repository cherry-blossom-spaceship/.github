#!/usr/bin/env python3
"""Fail PRs that introduce real machine paths outside reviewed exceptions.

This is intentionally a GitHub merge gate, not an advisory document. It scans
only changed portable source/config/workflow files so rollout does not fail on
historic material. Machine locations must be semantic registry keys or explicit
environment variables; exceptions are reviewed in .github/path-exceptions.txt.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
BASE = sys.argv[2]
PORTABLE_SUFFIXES = {".sh", ".bash", ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".yml", ".yaml", ".json", ".toml"}
EXCLUDED_PREFIXES = (".github/path-exceptions.txt", "config/path-registry.example.yaml")
# Actual, machine-specific forms. Generic documented placeholders are not paths.
RULES = {
    "Windows user/drive path": re.compile(r"(?i)(?:[A-Z]:[\\/](?:Users|20-code-repositories|AppData)[\\/])"),
    "POSIX home/mount path": re.compile(r"(?<![A-Za-z0-9_])/(?:home|mnt|f|c)/[A-Za-z0-9_.-]"),
    "UNC host path": re.compile(r"\\\\(?!<)[A-Za-z0-9][A-Za-z0-9_.-]*\\"),
}


def changed_files() -> list[Path]:
    subprocess.run(["git", "fetch", "origin", BASE, "--depth=1"], cwd=ROOT, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(["git", "diff", "--name-only", f"origin/{BASE}...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
    return [ROOT / line for line in result.stdout.splitlines() if line]


def exception_lines() -> set[str]:
    path = ROOT / ".github/path-exceptions.txt"
    if not path.exists():
        return set()
    # Each exact exception must be accompanied by an issue reference and expiry.
    lines = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")}
    for line in lines:
        if " | issue:" not in line or " | expires:" not in line:
            raise SystemExit(f"Malformed path exception: {line!r}")
    return {line.split(" | issue:", 1)[0] for line in lines}


def main() -> int:
    exceptions = exception_lines()
    violations: list[str] = []
    for path in changed_files():
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(EXCLUDED_PREFIXES) or path.suffix.lower() not in PORTABLE_SUFFIXES or not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.strip() in exceptions:
                continue
            for label, rule in RULES.items():
                if rule.search(line):
                    violations.append(f"{rel}:{number}: {label}: use a path-registry key or env var")
    if violations:
        print("Sovereignty / Portability gate failed:", *violations, sep="\n  ", file=sys.stderr)
        return 1
    print("Sovereignty / Portability gate passed: no introduced machine-specific paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the compact, source-linked Repository Cheat Sheet contract.

Use ``--template`` for the organisation starter template. Normal mode validates
an adopted per-repository sheet with populated active-card rows.
"""
from __future__ import annotations

import argparse
from pathlib import Path

MAX_LINES = 120
MAX_ACTIVE_ROWS = 8
ACTIVE_HEADING = "## Active invariants and known traps"
TAGS_HEADING = "## Controlled retrieval tags"
REQUIRED_ACTIVE_HEADER = (
    "| obstacle_key | applies_when | verified fact or smallest safe action | "
    "incident_refs | evidence/source | owner | last_verified | status | disposition / rail link |"
)
REQUIRED_TAGS = {
    "windows-msys",
    "migration-schema",
    "provider-safety",
    "github-identity",
    "runtime-prerequisite",
    "portability",
}
VALID_STATUSES = {"candidate", "verified", "promoted-to-rail", "retired"}


def section(lines: list[str], heading: str) -> list[str]:
    try:
        start = lines.index(heading) + 1
    except ValueError:
        raise ValueError(f"missing required heading: {heading}") from None
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def table_rows(lines: list[str], header: str) -> list[list[str]]:
    try:
        start = lines.index(header) + 2  # header + markdown separator
    except ValueError:
        raise ValueError(f"missing required table header: {header}") from None
    rows: list[list[str]] = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def validate(path: Path, *, template: bool) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if len(lines) > MAX_LINES:
        errors.append(f"line count {len(lines)} exceeds {MAX_LINES}")
    try:
        active = section(lines, ACTIVE_HEADING)
        rows = table_rows(active, REQUIRED_ACTIVE_HEADER)
    except ValueError as error:
        return [str(error)]
    if len(rows) > MAX_ACTIVE_ROWS:
        errors.append(f"active invariant rows {len(rows)} exceeds {MAX_ACTIVE_ROWS}")
    if not template:
        for number, row in enumerate(rows, 1):
            if len(row) != 9:
                errors.append(f"active row {number} has {len(row)} columns; expected 9")
                continue
            key, applies, action, incidents, evidence, owner, verified, status, disposition = row
            if not all((key, applies, action, incidents, evidence, owner, verified, status)):
                errors.append(f"active row {number} has an empty required field")
            if status.strip("`") not in VALID_STATUSES:
                errors.append(f"active row {number} has invalid status {status!r}")
            words = len(action.split())
            if not 30 <= words <= 100:
                errors.append(f"active row {number} action has {words} words; expected 30–100")
            if status.strip("`") in {"promoted-to-rail", "retired"} and not disposition:
                errors.append(f"active row {number} needs a disposition / rail link")
    try:
        tags = section(lines, TAGS_HEADING)
    except ValueError as error:
        return errors + [str(error)]
    declared = {
        row[0].strip("`")
        for row in table_rows(tags, "| Tag | Applies to |")
        if len(row) == 2
    }
    missing = REQUIRED_TAGS - declared
    if missing:
        errors.append("missing controlled tags: " + ", ".join(sorted(missing)))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--template", action="store_true")
    args = parser.parse_args()
    errors = validate(args.path, template=args.template)
    if errors:
        print("Repository Cheat Sheet contract failed:", *errors, sep="\n  ")
        return 1
    mode = "template" if args.template else "repository sheet"
    print(f"Repository Cheat Sheet contract passed: {mode}; {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

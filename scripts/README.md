# Shared script registry

This directory holds organisation-level validators, starter tooling, and their hermetic tests. It is **not** a universal remote-execution surface: repositories adopt a script through an explicit bootstrap/caller/launcher change and keep intentional local refinements visible.

## Lifecycle naming

Use one of these prefixes for new load-bearing tools:

- `preflight-*` — fail-fast launch prerequisites;
- `ledger-*` — append-only workflow/attempt evidence;
- `verify-*` — read-only validators;
- `graduate-*` — move a verified lesson into an executable rail.

New or materially changed scripts should provide `--help`, document their inputs/side effects/exit codes below, and have a hermetic test when they enforce a rule. Older scripts are listed with their current invocation until migrated.

## Registry

| Script | Purpose | Caller / invocation | Side effects | Exit contract | Test |
|---|---|---|---|---|---|
| `verify_sovereignty_portability.py` | Reject machine-specific paths in changed portable files unless a time-limited registry exception exists. | CI or `python scripts/verify_sovereignty_portability.py REPOSITORY_ROOT BASE_SHA` | Read-only | `0` pass; non-zero violation/config error | `scripts/tests/test_verify_sovereignty_portability.py` |
| `verify_repo_cheat_sheet.py` | Validate cheat-sheet structure, line/row budget, status fields, and controlled tags. | Bootstrap/CI or `python scripts/verify_repo_cheat_sheet.py --template TEMPLATE_PATH` | Read-only | `0` pass; `1` contract failure | `scripts/tests/test_verify_repo_cheat_sheet.py` |

## Adoption rule

A script becomes load-bearing only when a repository explicitly wires and tests it. The source template and this registry make it discoverable; they do not pretend an uninstalled caller is enforcement.

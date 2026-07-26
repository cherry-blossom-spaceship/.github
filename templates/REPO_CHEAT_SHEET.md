# Repository Cheat Sheet

> Copy this file to `docs/agent/REPO_CHEAT_SHEET.md` in a repository. Keep it a concise, verified launch aid—not a project diary or a substitute for the live issue/PR state.

## Purpose and limits

- **Use for:** stable facts a fresh coding or review agent otherwise has to rediscover.
- **Do not use for:** secrets, private transcripts, mutable task status, raw logs, credentials, or long architecture prose.
- **Size budget:** aim for 1–2 screens; move detailed or conditional knowledge into source-linked cards.
- **Authority:** live GitHub state, code, tests, and runtime configuration override this sheet.

## Verification metadata

| Field | Value |
|---|---|
| Repository | `OWNER/REPOSITORY` |
| Default branch | `main` |
| Last verified (UTC) | `YYYY-MM-DD` |
| Maintainer / source link | `issue-or-PR URL` |

## Start here

<!-- Put only stable, safe launch facts here. Prefer commands that discover paths from the repository root or the Path Registry. -->

- Canonical setup / test command:
- Fast verification command:
- Full verification command:
- Required runtime only when applicable:
- Canonical path/portability registry:
- Agent policy / role-card location:

## Component map

| Area | Entry point / location | Verification | Source |
|---|---|---|---|
| Example: migrations | `path/from/repo/root` | `command` | `PR/issue/test URL` |

## Stable invariants and known traps

| Trigger / applies when | Verified fact or smallest safe action | Source | Status |
|---|---|---|---|
| Example: changing a migration | Locate the migration-version fixture before changing the migration count. | `PR/test URL` | verified |

**Status values:** `candidate` (not injectable), `verified` (safe to inject), `promoted-to-rail` (use the script/test instead), `retired`.

## Retrieval tags

<!-- Stable labels for deterministic launch-packet selection. Keep these short and few. -->

`windows` `migration` `provider` `github-identity` `runtime`

## Candidate lesson intake

Record a candidate while the run is fresh, then promote it only with evidence.

```text
obstacle_key:
applies_when:
observed_failure:
smallest safe action:
source_issue_or_pr:
evidence (test / repro / command):
proposed status: candidate
```

## Upkeep protocol

1. **Launcher:** read this sheet only when the repository is selected; select rows by deterministic tags before any semantic lookup.
2. **PR author:** add at most one concise candidate when a *new, reusable* lesson was discovered. Do not copy ordinary task progress here.
3. **Reviewer/maintainer:** promote a candidate only if its source and verification are recorded; otherwise delete or leave it as a non-injectable candidate.
4. **Twice rule:** if a verified card fails to prevent the same incident twice, create a preflight, lint, test, or wrapper rail; mark the row `promoted-to-rail` and remove it from normal injection.
5. **Monthly or ten-launch trim:** remove stale, duplicate, superseded, or never-used rows. The sheet must shrink as executable rails replace prose.

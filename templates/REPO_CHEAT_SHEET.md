# Repository Cheat Sheet

> Copy this file to `docs/agent/REPO_CHEAT_SHEET.md` in a repository. Keep it a concise, verified launch aid—not a project diary or a substitute for live issue/PR state.

## Purpose and limits

- **Use for:** stable facts a fresh coding or review agent otherwise has to rediscover.
- **Do not use for:** secrets, private transcripts, mutable task status, raw logs, credentials, or long architecture prose.
- **Enforceable size budget:** at most **120 lines** and **8 active invariant rows**. A repository checker must fail when either cap is exceeded.
- **Card bound:** each active invariant/action is 30–100 words maximum.
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

## Active invariants and known traps

<!-- At most 8 active rows. One row = one injectible card. -->

| obstacle_key | applies_when | verified fact or smallest safe action | incident_refs | evidence/source | owner | last_verified | status | disposition / rail link |
|---|---|---|---|---|---|---|---|---|
| `migration-fixture-impact` | changing a migration | Locate the migration-version fixture before changing the migration count. | `PR/issue URLs` | `test/PR URL` | `role or team` | `YYYY-MM-DD` | `verified` | `—` |

**Status lifecycle:**

- `candidate`: evidence is incomplete; never inject it.
- `verified`: injectable when its controlled retrieval tag matches the task.
- `promoted-to-rail`: after **two incident references for the same `obstacle_key` despite a verified card**, create the script/lint/test/preflight, write its URL in `disposition / rail link`, move the row to `docs/agent/RETIRED_CARDS.md`, then remove it from this active table.
- `retired`: move the row to `docs/agent/RETIRED_CARDS.md` with a reason/source, then remove it from this active table.

## Controlled retrieval tags

Use only the values declared here. Add or rename a tag only in a reviewed change with a source link; do not improvise aliases such as `win32` for `windows-msys`.

| Tag | Applies to |
|---|---|
| `windows-msys` | Git Bash/MSYS/native-Windows boundaries |
| `migration-schema` | migrations, schemas, fixture-version contracts |
| `provider-safety` | explicit provider/model/network guard |
| `github-identity` | GitHub account, commit identity, role lane |
| `runtime-prerequisite` | task-specific service, DB, tool, or schema availability |
| `portability` | Path Registry or OS-agnostic portability rules |

## Candidate lesson intake

Record a candidate while the run is fresh, then promote it only with evidence. Field names deliberately match the active-table contract.

```text
obstacle_key:
applies_when:
verified_fact_or_smallest_safe_action:
incident_refs:
evidence_source:
owner:
last_verified:
status: candidate
proposed_controlled_tag:
```

## Upkeep protocol

1. **Launcher:** read this sheet only when the repository is selected; select rows by controlled tags before any semantic lookup.
2. **PR author:** add at most one concise candidate when a *new, reusable* lesson was discovered. Do not copy ordinary task progress here.
3. **Reviewer/maintainer:** promote a candidate only if source, owner, controlled tag, and verification are recorded; otherwise delete it or leave it non-injectable.
4. **Twice rule:** count `incident_refs` for the exact `obstacle_key`; on the second incident after verification, graduate it to an executable rail and apply the stated disposition.
5. **Monthly or ten-launch trim:** run the checker; review each row's `last_verified`, owner, incident references, and disposition. Remove stale, duplicate, superseded, or never-used active rows. The sheet must shrink as executable rails replace prose.

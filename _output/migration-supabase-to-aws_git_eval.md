# Git Evaluation — migration-supabase-to-aws

Repo: `/home/quantium/labs/oriane/_deprecated/migration-supabase-to-aws`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 2 |
| Current lines of code (tracked) | 175 |
| Commits (total) | 1 |
| Commits (merges) | 0 |
| Commits (non-merges) | 1 |
| Unique authors | 1 |
| First commit | 2025-05-23T15:07:15+02:00 |
| Last commit | 2025-05-23T15:07:15+02:00 |
| Active days | 1 |
| Span days | 1 |
| Avg commits/day | 1.0 |
| Lines added (sum) | 175 |
| Lines deleted (sum) | 0 |
| Files touched (sum of numstat rows) | 2 |
| Estimated hours (session-based) | 1.5 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 175 | 0 | 2 | 1 | 2025-05-23T15:07:15+02:00 | 2025-05-23T15:07:15+02:00 | 175.0 | 175.0 | ★★★★★ |

## Commits by author

```mermaid
pie title Commits by author
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 175
```

## Effort estimation model

This report estimates effort using a session + commit-weighted heuristic:
- Split commits per author into sessions where the gap > SESSION_GAP_MINUTES.
- Per session, sum per-commit minutes: base + sqrt(lines)/10 * MINUTES_PER_100_LINES + files * MINUTES_PER_FILE.
- Enforce MIN_SESSION_MINUTES minimum per session.
- Sum per day with MAX_HOURS_PER_DAY cap; multiply by CALIBRATION_FACTOR.

Parameters:

| Param | Value |
|---|---:|
| SESSION_GAP_MINUTES | 90 |
| MAX_HOURS_PER_DAY | 10.0 |
| MIN_SESSION_MINUTES | 45.0 |
| MINUTES_PER_COMMIT_BASE | 15.0 |
| MINUTES_PER_100_LINES | 12.0 |
| MINUTES_PER_FILE | 3.0 |
| CALIBRATION_FACTOR | 2.0 |

## Monthly activity

| Month | Commits | Added | Deleted | Files | Chart |
|---|---:|---:|---:|---:|:---|
| 2025-05 | 1 | 175 | 0 | 2 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-05-01, 2025-06-01
```

## Highlights

- Longest active streak: 1 days (2025-05-23 to 2025-05-23)
- Best day by commits: 2025-05-23 — 1 commits
- Best day by lines added: 2025-05-23 — 175 lines


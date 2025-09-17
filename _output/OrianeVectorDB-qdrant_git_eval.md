# Git Evaluation — OrianeVectorDB-qdrant

Repo: `/home/quantium/labs/oriane/_deprecated/OrianeVectorDB-qdrant`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 249 |
| Current lines of code (tracked) | 258569 |
| Commits (total) | 47 |
| Commits (merges) | 3 |
| Commits (non-merges) | 44 |
| Unique authors | 1 |
| First commit | 2025-07-17T21:54:02+02:00 |
| Last commit | 2025-07-30T10:39:45+02:00 |
| Active days | 9 |
| Span days | 14 |
| Avg commits/day | 3.3571 |
| Lines added (sum) | 73047 |
| Lines deleted (sum) | 38067 |
| Files touched (sum of numstat rows) | 1136 |
| Estimated hours (session-based) | 103.61 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 45 | 100.61 | 73045 | 38067 | 1135 | 8 | 2025-07-19T23:24:03+02:00 | 2025-07-30T10:39:45+02:00 | 2469.16 | 162.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 2 | 3.0 | 2 | 0 | 1 | 2 | 2025-07-17T21:54:02+02:00 | 2025-07-27T17:35:17+02:00 | 1.0 | 1.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 45
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 2
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 73045
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 2
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
| 2025-07 | 47 | 73047 | 38067 | 1136 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-07-01, 2025-08-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-07-01, 2025-08-01
```

## Highlights

- Longest active streak: 4 days (2025-07-27 to 2025-07-30)
- Best day by commits: 2025-07-28 — 13 commits
- Best day by lines added: 2025-07-29 — 28055 lines


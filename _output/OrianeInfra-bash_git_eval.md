# Git Evaluation — OrianeInfra-bash

Repo: `/home/quantium/labs/oriane/_deprecated/OrianeInfra-bash`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 48 |
| Current lines of code (tracked) | 6558 |
| Commits (total) | 6 |
| Commits (merges) | 0 |
| Commits (non-merges) | 6 |
| Unique authors | 1 |
| First commit | 2025-07-28T12:04:52+02:00 |
| Last commit | 2025-07-29T17:56:29+02:00 |
| Active days | 2 |
| Span days | 2 |
| Avg commits/day | 3.0 |
| Lines added (sum) | 21119 |
| Lines deleted (sum) | 14561 |
| Files touched (sum of numstat rows) | 302 |
| Estimated hours (session-based) | 24.29 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 0 |
| Weekday days active | 2 |
| Night days active | 1 |
| Daytime days active | 2 |
| Days with both day & night activity | 1 |
| Day-only days | 1 |
| Night-only days | 0 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 5 | 23.54 | 0 | 1 | 2 | 1 | 21118 | 14561 | 301 | 2 | 2025-07-28T17:14:01+02:00 | 2025-07-29T17:56:29+02:00 | 7135.8 | 6101.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 0.75 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 | 2025-07-28T12:04:52+02:00 | 2025-07-28T12:04:52+02:00 | 1.0 | 1.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 5
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 21118
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
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
| MIN_SESSION_MINUTES | 30.0 |
| MINUTES_PER_COMMIT_BASE | 12.0 |
| MINUTES_PER_100_LINES | 8.0 |
| MINUTES_PER_FILE | 2.0 |
| CALIBRATION_FACTOR | 1.5 |

## Monthly activity

| Month | Commits | Added | Deleted | Files | Chart |
|---|---:|---:|---:|---:|:---|
| 2025-07 | 6 | 21119 | 14561 | 302 | ######################################## |

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

- Longest active streak: 2 days (2025-07-28 to 2025-07-29)
- Best day by commits: 2025-07-28 — 3 commits
- Best day by lines added: 2025-07-28 — 14724 lines


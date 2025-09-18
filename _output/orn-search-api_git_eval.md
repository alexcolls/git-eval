# Git Evaluation — orn-search-api

Repo: `/home/quantium/labs/oriane/orn-search-api`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 103 |
| Current lines of code (tracked) | 243254 |
| Commits (total) | 178 |
| Commits (merges) | 0 |
| Commits (non-merges) | 178 |
| Unique authors | 1 |
| First commit | 2025-09-10T11:55:06+02:00 |
| Last commit | 2025-09-12T20:12:32+02:00 |
| Active days | 3 |
| Span days | 3 |
| Avg commits/day | 59.3333 |
| Lines added (sum) | 91334 |
| Lines deleted (sum) | 75729 |
| Files touched (sum of numstat rows) | 687 |
| Estimated hours (session-based) | 45.85 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 0 |
| Weekday days active | 3 |
| Night days active | 2 |
| Daytime days active | 3 |
| Days with both day & night activity | 2 |
| Day-only days | 1 |
| Night-only days | 0 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 177 | 45.0 | 0 | 2 | 2 | 1 | 90924 | 75729 | 684 | 3 | 2025-09-10T21:51:14+02:00 | 2025-09-12T20:12:32+02:00 | 941.54 | 36.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 0.85 | 0 | 0 | 1 | 0 | 410 | 0 | 3 | 1 | 2025-09-10T11:55:06+02:00 | 2025-09-10T11:55:06+02:00 | 410.0 | 410.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 177
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 90924
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 410
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
| 2025-09 | 178 | 91334 | 75729 | 687 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-09-01, 2025-10-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-09-01, 2025-10-01
```

## Highlights

- Longest active streak: 3 days (2025-09-10 to 2025-09-12)
- Best day by commits: 2025-09-11 — 120 commits
- Best day by lines added: 2025-09-12 — 61685 lines


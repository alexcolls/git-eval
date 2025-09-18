# Git Evaluation — FrameComparisonModel-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/FrameComparisonModel-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 12 |
| Current lines of code (tracked) | 1002 |
| Commits (total) | 24 |
| Commits (merges) | 0 |
| Commits (non-merges) | 24 |
| Unique authors | 1 |
| First commit | 2025-03-18T12:42:33+01:00 |
| Last commit | 2025-03-30T22:42:37+02:00 |
| Active days | 4 |
| Span days | 13 |
| Avg commits/day | 1.8462 |
| Lines added (sum) | 1707 |
| Lines deleted (sum) | 174 |
| Files touched (sum of numstat rows) | 52 |
| Estimated hours (session-based) | 12.79 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 1 |
| Weekday days active | 3 |
| Night days active | 1 |
| Daytime days active | 3 |
| Days with both day & night activity | 0 |
| Day-only days | 3 |
| Night-only days | 1 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 20 | 10.7 | 1 | 1 | 3 | 0 | 1355 | 172 | 46 | 4 | 2025-03-18T19:30:55+01:00 | 2025-03-30T22:42:37+02:00 | 76.35 | 16.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 4 | 2.09 | 0 | 0 | 1 | 0 | 352 | 2 | 6 | 1 | 2025-03-18T12:42:33+01:00 | 2025-03-18T19:59:14+01:00 | 88.5 | 88.5 | ★☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 20
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 4
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 1355
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 352
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
| 2025-03 | 24 | 1707 | 174 | 52 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-04-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-04-01
```

## Highlights

- Longest active streak: 2 days (2025-03-18 to 2025-03-19)
- Best day by commits: 2025-03-18 — 12 commits
- Best day by lines added: 2025-03-18 — 934 lines


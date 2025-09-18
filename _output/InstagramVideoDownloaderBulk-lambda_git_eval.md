# Git Evaluation — InstagramVideoDownloaderBulk-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/InstagramVideoDownloaderBulk-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 13 |
| Current lines of code (tracked) | 52243 |
| Commits (total) | 10 |
| Commits (merges) | 0 |
| Commits (non-merges) | 10 |
| Unique authors | 1 |
| First commit | 2025-03-20T14:45:37+01:00 |
| Last commit | 2025-03-24T11:03:30+01:00 |
| Active days | 3 |
| Span days | 5 |
| Avg commits/day | 2.0 |
| Lines added (sum) | 52436 |
| Lines deleted (sum) | 193 |
| Files touched (sum of numstat rows) | 29 |
| Estimated hours (session-based) | 11.55 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 0 |
| Weekday days active | 3 |
| Night days active | 0 |
| Daytime days active | 3 |
| Days with both day & night activity | 0 |
| Day-only days | 3 |
| Night-only days | 0 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 8 | 10.05 | 0 | 0 | 3 | 0 | 52259 | 191 | 26 | 3 | 2025-03-20T15:15:58+01:00 | 2025-03-24T11:03:30+01:00 | 6556.25 | 305.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 2 | 1.5 | 0 | 0 | 2 | 0 | 177 | 2 | 3 | 2 | 2025-03-20T14:45:37+01:00 | 2025-03-21T10:46:27+01:00 | 89.5 | 89.5 | ★☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 8
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 2
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 52259
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 177
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
| 2025-03 | 10 | 52436 | 193 | 29 | ######################################## |

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

- Longest active streak: 2 days (2025-03-20 to 2025-03-21)
- Best day by commits: 2025-03-20 — 6 commits
- Best day by lines added: 2025-03-21 — 50252 lines


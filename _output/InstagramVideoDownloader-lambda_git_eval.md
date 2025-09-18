# Git Evaluation — InstagramVideoDownloader-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/InstagramVideoDownloader-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 2870 |
| Current lines of code (tracked) | 588490 |
| Commits (total) | 11 |
| Commits (merges) | 0 |
| Commits (non-merges) | 11 |
| Unique authors | 1 |
| First commit | 2025-03-14T11:20:34+01:00 |
| Last commit | 2025-03-19T11:32:01+01:00 |
| Active days | 3 |
| Span days | 6 |
| Avg commits/day | 1.8333 |
| Lines added (sum) | 697960 |
| Lines deleted (sum) | 254972 |
| Files touched (sum of numstat rows) | 5099 |
| Estimated hours (session-based) | 18.44 |

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
| quantium-rock <alexcollsoutumuro@gmail.com> | 10 | 17.69 | 0 | 0 | 3 | 0 | 697784 | 254972 | 5097 | 3 | 2025-03-14T11:26:29+01:00 | 2025-03-19T11:32:01+01:00 | 95275.6 | 44.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 0.75 | 0 | 0 | 1 | 0 | 176 | 0 | 2 | 1 | 2025-03-14T11:20:34+01:00 | 2025-03-14T11:20:34+01:00 | 176.0 | 176.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 10
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 697784
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 176
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
| 2025-03 | 11 | 697960 | 254972 | 5099 | ######################################## |

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
- Best day by commits: 2025-03-14 — 5 commits
- Best day by lines added: 2025-03-14 — 697830 lines


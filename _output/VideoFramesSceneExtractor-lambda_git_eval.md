# Git Evaluation — VideoFramesSceneExtractor-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/VideoFramesSceneExtractor-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 59 |
| Current lines of code (tracked) | 226041 |
| Commits (total) | 39 |
| Commits (merges) | 0 |
| Commits (non-merges) | 39 |
| Unique authors | 1 |
| First commit | 2025-04-24T11:41:42+02:00 |
| Last commit | 2025-05-12T17:21:01+02:00 |
| Active days | 11 |
| Span days | 19 |
| Avg commits/day | 2.0526 |
| Lines added (sum) | 1245928 |
| Lines deleted (sum) | 1241311 |
| Files touched (sum of numstat rows) | 11410 |
| Estimated hours (session-based) | 53.95 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 2 |
| Weekday days active | 9 |
| Night days active | 3 |
| Daytime days active | 9 |
| Days with both day & night activity | 1 |
| Day-only days | 8 |
| Night-only days | 2 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 37 | 52.45 | 2 | 3 | 9 | 1 | 1245752 | 1241310 | 11407 | 11 | 2025-04-24T12:30:14+02:00 | 2025-05-12T17:21:01+02:00 | 67217.89 | 41.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 2 | 1.5 | 0 | 0 | 1 | 0 | 176 | 1 | 3 | 1 | 2025-04-24T11:41:42+02:00 | 2025-04-24T19:09:40+02:00 | 88.5 | 88.5 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 37
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 2
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 1245752
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
| 2025-04 | 25 | 1242645 | 1240427 | 11237 | ######################################## |
| 2025-05 | 14 | 3283 | 884 | 173 | ###################### |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-04-01, 2025-05-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-04-01, 2025-06-01
```

## Highlights

- Longest active streak: 3 days (2025-04-28 to 2025-04-30)
- Best day by commits: 2025-04-24 — 16 commits
- Best day by lines added: 2025-04-29 — 1240373 lines


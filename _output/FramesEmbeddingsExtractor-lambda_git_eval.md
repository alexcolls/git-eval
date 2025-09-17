# Git Evaluation — FramesEmbeddingsExtractor-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/FramesEmbeddingsExtractor-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 15 |
| Current lines of code (tracked) | 1195 |
| Commits (total) | 9 |
| Commits (merges) | 0 |
| Commits (non-merges) | 9 |
| Unique authors | 1 |
| First commit | 2025-04-30T12:08:09+02:00 |
| Last commit | 2025-05-07T11:12:41+02:00 |
| Active days | 3 |
| Span days | 8 |
| Avg commits/day | 1.125 |
| Lines added (sum) | 1590 |
| Lines deleted (sum) | 447 |
| Files touched (sum of numstat rows) | 27 |
| Estimated hours (session-based) | 12.4 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 8 | 10.9 | 1415 | 447 | 25 | 2 | 2025-05-04T19:43:45+02:00 | 2025-05-07T11:12:41+02:00 | 232.75 | 150.5 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 175 | 0 | 2 | 1 | 2025-04-30T12:08:09+02:00 | 2025-04-30T12:08:09+02:00 | 175.0 | 175.0 | ★☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 8
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 1415
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
| 2025-04 | 1 | 175 | 0 | 2 | ##### |
| 2025-05 | 8 | 1415 | 447 | 25 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-04-01, 2025-05-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-05-01, 2025-06-01
```

## Highlights

- Longest active streak: 1 days (2025-04-30 to 2025-04-30)
- Best day by commits: 2025-05-04 — 6 commits
- Best day by lines added: 2025-05-04 — 829 lines


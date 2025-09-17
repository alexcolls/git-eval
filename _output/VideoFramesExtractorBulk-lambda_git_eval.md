# Git Evaluation — VideoFramesExtractorBulk-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/VideoFramesExtractorBulk-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 20 |
| Current lines of code (tracked) | 2305 |
| Commits (total) | 18 |
| Commits (merges) | 0 |
| Commits (non-merges) | 18 |
| Unique authors | 1 |
| First commit | 2025-03-26T08:53:24+01:00 |
| Last commit | 2025-04-30T11:49:35+02:00 |
| Active days | 6 |
| Span days | 36 |
| Avg commits/day | 0.5 |
| Lines added (sum) | 101585 |
| Lines deleted (sum) | 99564 |
| Files touched (sum of numstat rows) | 45 |
| Estimated hours (session-based) | 52.48 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 17 | 50.98 | 101448 | 99564 | 43 | 6 | 2025-03-26T08:55:49+01:00 | 2025-04-30T11:49:35+02:00 | 11824.24 | 100.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 137 | 0 | 2 | 1 | 2025-03-26T08:53:24+01:00 | 2025-03-26T08:53:24+01:00 | 137.0 | 137.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 17
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 101448
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 137
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
| 2025-03 | 6 | 1739 | 268 | 23 | #################### |
| 2025-04 | 12 | 99846 | 99296 | 22 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-04-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-05-01
```

## Highlights

- Longest active streak: 3 days (2025-04-26 to 2025-04-28)
- Best day by commits: 2025-03-26 — 6 commits
- Best day by lines added: 2025-04-26 — 99416 lines


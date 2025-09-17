# Git Evaluation — SSCD-model

Repo: `/home/quantium/labs/oriane/_deprecated/SSCD-model`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 35 |
| Current lines of code (tracked) | 4251223 |
| Commits (total) | 43 |
| Commits (merges) | 0 |
| Commits (non-merges) | 43 |
| Unique authors | 1 |
| First commit | 2025-04-03T03:20:27+02:00 |
| Last commit | 2025-05-28T00:55:26+02:00 |
| Active days | 14 |
| Span days | 56 |
| Avg commits/day | 0.7679 |
| Lines added (sum) | 60464 |
| Lines deleted (sum) | 763 |
| Files touched (sum of numstat rows) | 127 |
| Estimated hours (session-based) | 62.59 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 42 | 61.09 | 60288 | 763 | 125 | 14 | 2025-04-03T03:24:53+02:00 | 2025-05-28T00:55:26+02:00 | 1453.6 | 16.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 176 | 0 | 2 | 1 | 2025-04-03T03:20:27+02:00 | 2025-04-03T03:20:27+02:00 | 176.0 | 176.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 42
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 60288
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
| MIN_SESSION_MINUTES | 45.0 |
| MINUTES_PER_COMMIT_BASE | 15.0 |
| MINUTES_PER_100_LINES | 12.0 |
| MINUTES_PER_FILE | 3.0 |
| CALIBRATION_FACTOR | 2.0 |

## Monthly activity

| Month | Commits | Added | Deleted | Files | Chart |
|---|---:|---:|---:|---:|:---|
| 2025-04 | 28 | 60065 | 405 | 97 | ######################################## |
| 2025-05 | 15 | 399 | 358 | 30 | ##################### |

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

- Longest active streak: 7 days (2025-04-03 to 2025-04-09)
- Best day by commits: 2025-05-27 — 8 commits
- Best day by lines added: 2025-04-04 — 29949 lines


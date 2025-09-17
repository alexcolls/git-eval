# Git Evaluation — orn-acquisition-lambdas

Repo: `/home/quantium/labs/oriane/orn-acquisition-lambdas`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 39 |
| Current lines of code (tracked) | 9867 |
| Commits (total) | 41 |
| Commits (merges) | 0 |
| Commits (non-merges) | 41 |
| Unique authors | 1 |
| First commit | 2025-08-17T12:42:10+02:00 |
| Last commit | 2025-09-09T22:07:44+02:00 |
| Active days | 4 |
| Span days | 24 |
| Avg commits/day | 1.7083 |
| Lines added (sum) | 12005 |
| Lines deleted (sum) | 2138 |
| Files touched (sum of numstat rows) | 117 |
| Estimated hours (session-based) | 54.2 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 40 | 52.7 | 11797 | 2138 | 115 | 3 | 2025-09-03T12:23:42+02:00 | 2025-09-09T22:07:44+02:00 | 348.38 | 134.5 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 208 | 0 | 2 | 1 | 2025-08-17T12:42:10+02:00 | 2025-08-17T12:42:10+02:00 | 208.0 | 208.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 40
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 11797
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 208
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
| 2025-08 | 1 | 208 | 0 | 2 | # |
| 2025-09 | 40 | 11797 | 2138 | 115 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-08-01, 2025-09-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-09-01, 2025-10-01
```

## Highlights

- Longest active streak: 2 days (2025-09-08 to 2025-09-09)
- Best day by commits: 2025-09-09 — 20 commits
- Best day by lines added: 2025-09-03 — 6118 lines


# Git Evaluation — orn-platform-clusters

Repo: `/home/quantium/labs/oriane/orn-platform-clusters`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 16 |
| Current lines of code (tracked) | 555 |
| Commits (total) | 8 |
| Commits (merges) | 0 |
| Commits (non-merges) | 8 |
| Unique authors | 1 |
| First commit | 2025-08-08T18:43:11+02:00 |
| Last commit | 2025-08-17T02:55:58+02:00 |
| Active days | 5 |
| Span days | 10 |
| Avg commits/day | 0.8 |
| Lines added (sum) | 573 |
| Lines deleted (sum) | 18 |
| Files touched (sum of numstat rows) | 24 |
| Estimated hours (session-based) | 12.5 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| Thibaut Hadjean <thibaut@oriane.xyz> | 7 | 11.0 | 571 | 18 | 23 | 5 | 2025-08-08T18:57:50+02:00 | 2025-08-17T02:55:58+02:00 | 84.14 | 10.0 | ★★★★★ |
| thibaut-oriane <thibaut@oriane.xyz> | 1 | 1.5 | 2 | 0 | 1 | 1 | 2025-08-08T18:43:11+02:00 | 2025-08-08T18:43:11+02:00 | 2.0 | 2.0 | ★☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "Thibaut Hadjean <thibaut@oriane.xyz>" : 7
    "thibaut-oriane <thibaut@oriane.xyz>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "Thibaut Hadjean <thibaut@oriane.xyz>" : 571
    "thibaut-oriane <thibaut@oriane.xyz>" : 2
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
| 2025-08 | 8 | 573 | 18 | 24 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Thibaut Hadjean <thibaut@oriane.xyz>
    Thibaut Hadjean <thibaut@oriane.xyz> 1 : 2025-08-01, 2025-09-01
    section thibaut-oriane <thibaut@oriane.xyz>
    thibaut-oriane <thibaut@oriane.xyz> 1 : 2025-08-01, 2025-09-01
```

## Highlights

- Longest active streak: 3 days (2025-08-13 to 2025-08-15)
- Best day by commits: 2025-08-08 — 3 commits
- Best day by lines added: 2025-08-08 — 518 lines


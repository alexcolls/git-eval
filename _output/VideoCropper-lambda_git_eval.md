# Git Evaluation — VideoCropper-lambda

Repo: `/home/quantium/labs/oriane/_deprecated/VideoCropper-lambda`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 143 |
| Current lines of code (tracked) | 258049 |
| Commits (total) | 1 |
| Commits (merges) | 0 |
| Commits (non-merges) | 1 |
| Unique authors | 1 |
| First commit | 2025-05-16T12:32:12+02:00 |
| Last commit | 2025-05-16T12:32:12+02:00 |
| Active days | 1 |
| Span days | 1 |
| Avg commits/day | 1.0 |
| Lines added (sum) | 34683 |
| Lines deleted (sum) | 0 |
| Files touched (sum of numstat rows) | 144 |
| Estimated hours (session-based) | 11.22 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 0 |
| Weekday days active | 1 |
| Night days active | 0 |
| Daytime days active | 1 |
| Days with both day & night activity | 0 |
| Day-only days | 1 |
| Night-only days | 0 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 1 | 11.22 | 0 | 0 | 1 | 0 | 34683 | 0 | 144 | 1 | 2025-05-16T12:32:12+02:00 | 2025-05-16T12:32:12+02:00 | 34683.0 | 34683.0 | ★★★★★ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 34683
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
| 2025-05 | 1 | 34683 | 0 | 144 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-05-01, 2025-06-01
```

## Highlights

- Longest active streak: 1 days (2025-05-16 to 2025-05-16)
- Best day by commits: 2025-05-16 — 1 commits
- Best day by lines added: 2025-05-16 — 34683 lines


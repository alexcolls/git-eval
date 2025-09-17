# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [0.1.0] - 2025-09-17
### Added
- Poetry project with CLI entry point `git-eval` and `run.sh` helper to run without Poetry.
- Configuration via `.env` (with `.env.sample` template) honoring workspace preference.
- Full-history Git analyzer using `git log --all --numstat` to compute:
  - total, merge, and non-merge commits
  - first/last commit timestamps, active and span days, average commits/day
  - cumulative added/deleted lines and files touched
  - unique authors
  - estimated hours using a session heuristic (configurable GAP and daily cap)
- Multi-format outputs per repository:
  - JSON: metrics, per-commit entries, breakdowns (by author, daily, monthly) and current LOC snapshot
  - CSV: one-row summary
  - TXT: human-readable summary
  - Markdown: comprehensive report with
    - summary table including current LOC snapshot
    - developer leaderboard (commits, hours, lines, files, active days, avg/median commit size) with star rating
    - Mermaid charts: commits by author and lines added by author
    - monthly activity table with ASCII bars
    - Mermaid Gantt-style author activity timeline
    - highlights (longest streak, best day by commits, best day by lines)
- README with setup and usage instructions.

### Notes
- Hours are heuristic estimates; tune `SESSION_GAP_MINUTES` and `MAX_HOURS_PER_DAY` in `.env`.
- Mermaid charts render on platforms that support Mermaid (e.g., GitHub).

[0.1.0]: https://example.com/git-eval/releases/0.1.0


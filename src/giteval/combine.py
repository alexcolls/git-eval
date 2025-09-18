#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import asdict
import json
from datetime import timedelta

from giteval.main import (
    parse_git_log_with_numstat,
    compute_metrics,
    write_reports,
    _aggregate_monthly,
    _author_details,
    _current_loc_snapshot,
)

BASE = Path("/home/quantium/labs/oriane").resolve()
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./_output")).resolve()


def discover_repos(base: Path) -> List[Path]:
    repos: List[Path] = []
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        if d.name in {"git-eval", "_deprecated"}:
            continue
        # check git repo
        ok = os.system(f"git -C {d.as_posix()} rev-parse --is-inside-work-tree >/dev/null 2>&1") == 0
        if ok:
            repos.append(d)
    dep = base / "_deprecated"
    if dep.is_dir():
        for d in sorted(dep.iterdir()):
            if d.is_dir():
                ok = os.system(f"git -C {d.as_posix()} rev-parse --is-inside-work-tree >/dev/null 2>&1") == 0
                if ok:
                    repos.append(d)
    return repos


def _compute_monthly_hours(commits) -> Dict[str, float]:
    # parameters
    session_gap_minutes = int(os.getenv("SESSION_GAP_MINUTES", "90") or "90")
    per_commit_base = float(os.getenv("MINUTES_PER_COMMIT_BASE", "12") or "12")
    per_100_lines = float(os.getenv("MINUTES_PER_100_LINES", "8") or "8")
    per_file_min = float(os.getenv("MINUTES_PER_FILE", "2") or "2")
    calibration = float(os.getenv("CALIBRATION_FACTOR", "1.5") or "1.5")
    session_gap = timedelta(minutes=session_gap_minutes)

    # group by author label
    per_author: Dict[str, List] = {}
    for c in commits:
        key = (c.author_name or "Unknown").strip()
        if c.author_email:
            key = f"{key} <{c.author_email}>"
        per_author.setdefault(key, []).append(c)

    month_minutes: Dict[str, float] = {}
    for author, cs in per_author.items():
        cs.sort(key=lambda x: x.author_date)
        sessions: List[List] = []
        cur: List = []
        prev = None
        for c in cs:
            if prev is None or (c.author_date - prev) > session_gap:
                if cur:
                    sessions.append(cur)
                cur = [c]
            else:
                cur.append(c)
            prev = c.author_date
        if cur:
            sessions.append(cur)
        for sess in sessions:
            minutes = 0.0
            for c in sess:
                loc = max(0, (c.added or 0) + (c.deleted or 0))
                minutes += per_commit_base + ((loc ** 0.5) / 10.0) * per_100_lines + (c.files_changed or 0) * per_file_min
            month = sess[-1].author_date.strftime("%Y-%m")
            month_minutes[month] = month_minutes.get(month, 0.0) + minutes
    # apply calibration and convert to hours
    return {m: round(v * calibration / 60.0, 2) for m, v in month_minutes.items()}


def build_dashboard(per_repo: List[Dict]) -> Tuple[str, Dict]:
    # Sort repos by estimated_hours_total desc
    per_repo_sorted = sorted(per_repo, key=lambda r: r["metrics"]["estimated_hours_total"], reverse=True)
    # Aggregate authors across repos
    author_agg: Dict[str, Dict[str, float]] = {}
    for r in per_repo:
        authors = r.get("breakdowns", {}).get("authors", [])
        for a in authors:
            key = a["author"]
            agg = author_agg.setdefault(key, {
                "author": key,
                "repos": set(),
                "commits_total": 0,
                "estimated_hours": 0.0,
                "added_total": 0,
                "deleted_total": 0,
                "files_changed_total": 0,
                "active_days": 0,
                # schedule aggregates
                "weekends_active_days": 0,
                "weekdays_active_days": 0,
                "days_night_active": 0,
                "days_daytime_active": 0,
                "days_both": 0,
            })
            agg["repos"].add(r["repo"])  # type: ignore
            agg["commits_total"] += int(a.get("commits_total", 0))
            agg["estimated_hours"] += float(a.get("estimated_hours", 0.0))
            agg["added_total"] += int(a.get("added_total", 0))
            agg["deleted_total"] += int(a.get("deleted_total", 0))
            agg["files_changed_total"] += int(a.get("files_changed_total", 0))
            agg["active_days"] += int(a.get("active_days", 0))
            agg["weekends_active_days"] += int(a.get("weekends_active_days", 0))
            agg["weekdays_active_days"] += int(a.get("weekdays_active_days", 0))
            agg["days_night_active"] += int(a.get("days_night_active", 0))
            agg["days_daytime_active"] += int(a.get("days_daytime_active", 0))
            agg["days_both"] += int(a.get("days_both", 0))
    author_list = list(author_agg.values())
    for a in author_list:
        a["repos"] = sorted(list(a["repos"]))  # type: ignore
    author_sorted = sorted(author_list, key=lambda x: (x["estimated_hours"], x["commits_total"]), reverse=True)

    # Basic totals
    total_hours = sum(r["metrics"]["estimated_hours_total"] for r in per_repo_sorted)
    total_commits = sum(r["metrics"]["commits_total"] for r in per_repo_sorted)
    total_authors = len(author_sorted)

    # Markdown
    lines: List[str] = []
    lines.append("# Oriane — Git evaluation dashboard")
    lines.append("")
    lines.append(f"Repos analyzed: {len(per_repo_sorted)}  |  Total hours: {total_hours:.2f}  |  Total commits: {total_commits}  |  Unique authors: {total_authors}")
    lines.append("")

    # Charts
    lines.append("## Charts")
    lines.append("")
    # Top repos by hours (pie)
    lines.append("```mermaid")
    lines.append("pie title Top repositories by estimated hours")
    for r in per_repo_sorted[:10]:
        repo_name = Path(r["repo"]).name
        hours = r["metrics"]["estimated_hours_total"]
        lines.append(f'    "{repo_name}" : {hours}')
    lines.append("```")
    lines.append("")
    # Top authors by hours (pie)
    lines.append("```mermaid")
    lines.append("pie title Top authors by estimated hours")
    for a in author_sorted[:15]:
        label = a["author"].replace('"', '\\"')
        lines.append(f'    "{label}" : {a["estimated_hours"]:.2f}')
    lines.append("```")
    lines.append("")

    # Repo ranking
    lines.append("## Repositories by estimated hours")
    lines.append("")
    lines.append("| Rank | Repository | Hours | Commits | Authors | First | Last | Added | Deleted | Files | Avg commits/day | LOC (files) | Weekends | Weekdays | Night days | Day days | Both |")
    lines.append("|---:|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for i, r in enumerate(per_repo_sorted, 1):
        m = r["metrics"]
        repo = r["repo"]
        loc = r.get("current_loc", {})
        loc_str = f"{loc.get('lines', 0)} ({loc.get('files', 0)})"
        lines.append(
            f"| {i} | `{repo}` | {m['estimated_hours_total']} | {m['commits_total']} | {m['unique_authors']} | {m['first_commit']} | {m['last_commit']} | {m['added_lines_total']} | {m['deleted_lines_total']} | {m['files_changed_total']} | {m['avg_commits_per_day']} | {loc_str} | {m.get('weekends_active_days',0)} | {m.get('weekdays_active_days',0)} | {m.get('days_night_active',0)} | {m.get('days_daytime_active',0)} | {m.get('days_both',0)} |"
        )
    lines.append("")

    # Hours per month across repos (ASCII bar)
    month_totals_hours: Dict[str, float] = {}
    month_totals_commits: Dict[str, int] = {}
    month_totals_added: Dict[str, int] = {}
    month_totals_deleted: Dict[str, int] = {}
    # compute monthly hours per repo and aggregate
    per_repo_month_hours: Dict[str, Dict[str, float]] = {}
    for r in per_repo_sorted:
        mh = r.get("monthly_hours", [])
        repo_name = Path(r["repo"]).name
        repo_map: Dict[str, float] = {}
        for row in mh:
            m = row.get("month")
            h = float(row.get("hours", 0.0))
            if not m:
                continue
            month_totals_hours[m] = month_totals_hours.get(m, 0.0) + h
            repo_map[m] = repo_map.get(m, 0.0) + h
        per_repo_month_hours[repo_name] = repo_map
        # commits/lines
        for row in r.get("breakdowns", {}).get("monthly", []):
            m = row.get("month")
            if not m:
                continue
            month_totals_commits[m] = month_totals_commits.get(m, 0) + int(row.get("commits", 0))
            month_totals_added[m] = month_totals_added.get(m, 0) + int(row.get("added", 0))
            month_totals_deleted[m] = month_totals_deleted.get(m, 0) + int(row.get("deleted", 0))

    if month_totals_hours:
        lines.append("## Hours per month — all repos")
        lines.append("")
        lines.append("| Month | Hours | Chart |")
        lines.append("|---|---:|:---|")
        max_h = max(month_totals_hours.values()) if month_totals_hours else 1
        def bar(n: float, max_n: float) -> str:
            if max_n <= 0:
                return ""
            width = 40
            filled = int(round((n / max_n) * width))
            return "#" * max(1, filled) if n > 0 else ""
        for m in sorted(month_totals_hours.keys()):
            h = month_totals_hours[m]
            lines.append(f"| {m} | {h:.2f} | {bar(h, max_h)} |")
        lines.append("")
        # Mermaid pies for top 3 months showing repo split
        top_months = sorted(month_totals_hours.items(), key=lambda x: x[1], reverse=True)[:3]
        for m, _h in top_months:
            lines.append(f"```mermaid")
            lines.append(f"pie title Hours by repo — {m}")
            # gather top repos for that month
            parts = []
            for repo_name, mm in per_repo_month_hours.items():
                v = mm.get(m, 0.0)
                if v > 0:
                    parts.append((repo_name, v))
            for repo_name, v in sorted(parts, key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f'    "{repo_name}" : {v:.2f}')
            lines.append("```")
            lines.append("")

    # Author leaderboard
    if author_sorted:
        lines.append("## Developers by estimated hours (across repos)")
        lines.append("")
        lines.append("| Rank | Developer | Hours | Commits | Repos | Added | Deleted | Files | Active days |")
        lines.append("|---:|---|---:|---:|---|---:|---:|---:|---:|")
        top_hours = author_sorted[0]["estimated_hours"] if author_sorted else 0
        for i, a in enumerate(author_sorted, 1):
            stars = int(round((a["estimated_hours"] / top_hours) * 5)) if top_hours > 0 else 0
            star_bar = "★" * stars + "☆" * (5 - stars)
            lines.append(
                f"| {i} | {a['author']} | {a['estimated_hours']:.2f} {star_bar} | {a['commits_total']} | {', '.join(a['repos'])} | {a['added_total']} | {a['deleted_total']} | {a['files_changed_total']} | {a['active_days']} |"
            )
        lines.append("")

    # Top months across repos by hours/commits/lines
    if month_totals_hours:
        lines.append("## Top months across repos")
        lines.append("")
        lines.append("| Rank | Month | Hours | Commits | Added | Deleted |")
        lines.append("|---:|---|---:|---:|---:|---:|")
        months_all = set(month_totals_hours) | set(month_totals_commits)
        top_sorted = sorted(months_all, key=lambda m: (month_totals_hours.get(m, 0.0), month_totals_commits.get(m, 0)), reverse=True)[:10]
        for i, m in enumerate(top_sorted, 1):
            lines.append(f"| {i} | {m} | {month_totals_hours.get(m,0.0):.2f} | {month_totals_commits.get(m,0)} | {month_totals_added.get(m,0)} | {month_totals_deleted.get(m,0)} |")
        lines.append("")

    # Per-author schedule pies for top authors
    if author_sorted:
        lines.append("## Per-author schedule charts (top 5 by hours)")
        lines.append("")
        for a in author_sorted[:5]:
            label = a["author"].replace('"', '\\"')
            lines.append("```mermaid")
            lines.append(f"pie title Day vs Night — {label}")
            lines.append(f'    "Day" : {a.get("days_daytime_active",0)}')
            lines.append(f'    "Night" : {a.get("days_night_active",0)}')
            lines.append("```")
            lines.append("")
            lines.append("```mermaid")
            lines.append(f"pie title Weekend vs Weekday — {label}")
            lines.append(f'    "Weekend" : {a.get("weekends_active_days",0)}')
            lines.append(f'    "Weekday" : {a.get("weekdays_active_days",0)}')
            lines.append("```")
            lines.append("")

    # Per-repo breakdowns (from JSON content)
    lines.append("## Per-repo breakdowns")
    lines.append("")

    # helper for ascii bar
    def bar(n: int, max_n: int) -> str:
        if max_n <= 0:
            return ""
        width = 40
        filled = int(round((n / max_n) * width))
        return "#" * max(1, filled) if n > 0 else ""

    for r in per_repo_sorted:
        m = r["metrics"]
        repo = r["repo"]
        lines.append(f"### {Path(repo).name}")
        lines.append("")
        # Short summary
        lines.append(f"- Path: `{repo}`")
        lines.append(f"- Hours: {m['estimated_hours_total']} | Commits: {m['commits_total']} | Authors: {m['unique_authors']}")
        lines.append(f"- First: {m['first_commit']} | Last: {m['last_commit']}")
        lines.append(f"- Added: {m['added_lines_total']} | Deleted: {m['deleted_lines_total']} | Files: {m['files_changed_total']}")
        if r.get("current_loc"):
            lines.append(f"- Current LOC: {r['current_loc'].get('lines',0)} (files {r['current_loc'].get('files',0)})")
        lines.append(f"- Weekends: {m.get('weekends_active_days',0)} | Weekdays: {m.get('weekdays_active_days',0)} | Night days: {m.get('days_night_active',0)} | Day days: {m.get('days_daytime_active',0)} | Both: {m.get('days_both',0)}")
        lines.append("")
        # Top authors inside repo
        authors = r.get("breakdowns", {}).get("authors", [])
        if authors:
            lines.append("#### Top authors in repo")
            lines.append("")
            lines.append("| Developer | Hours | Commits | Wknd | Night | Day | Both | Added | Deleted | Files | Active days |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
            top = sorted(authors, key=lambda a: (a.get("estimated_hours",0), a.get("commits_total",0)), reverse=True)[:5]
            for a in top:
                lines.append(
                    f"| {a['author']} | {a.get('estimated_hours',0)} | {a.get('commits_total',0)} | {a.get('weekends_active_days',0)} | {a.get('days_night_active',0)} | {a.get('days_daytime_active',0)} | {a.get('days_both',0)} | {a.get('added_total',0)} | {a.get('deleted_total',0)} | {a.get('files_changed_total',0)} | {a.get('active_days',0)} |"
                )
            lines.append("")
        # Monthly activity
        monthly = r.get("breakdowns", {}).get("monthly", [])
        if monthly:
            lines.append("#### Monthly activity")
            lines.append("")
            lines.append("| Month | Commits | Added | Deleted | Files | Chart |")
            lines.append("|---|---:|---:|---:|---:|:---|")
            max_c = max((row.get("commits",0) for row in monthly), default=1)
            for row in monthly:
                mth = row.get("month")
                c = row.get("commits",0)
                a = row.get("added",0)
                d = row.get("deleted",0)
                f = row.get("files",0)
                lines.append(f"| {mth} | {c} | {a} | {d} | {f} | {bar(c, max_c)} |")
            lines.append("")

    md = "\n".join(lines) + "\n"
    payload = {
        "repos": per_repo_sorted,
        "authors": author_sorted,
    }
    return md, payload


def main(argv: List[str] = None) -> int:
    argv = argv or sys.argv[1:]
    if argv:
        repo_paths = [Path(a).resolve() for a in argv]
    else:
        repo_paths = discover_repos(BASE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_payloads = []
    for path in repo_paths:
        try:
            commits = parse_git_log_with_numstat(path, include_merges=(os.getenv("INCLUDE_MERGES", "1") not in {"0", "false", "False"}))
        except Exception:
            continue
        metrics = compute_metrics(commits)
        metrics.repo_path = path.as_posix()
        write_reports(OUTPUT_DIR, path, metrics, commits)
        curr_loc = _current_loc_snapshot(path)
        # compute monthly hours for this repo
        monthly_hours_map = _compute_monthly_hours(commits)
        monthly_hours_list = [{"month": m, "hours": h} for m, h in sorted(monthly_hours_map.items())]
        data = {
            "repo": path.as_posix(),
            "metrics": asdict(metrics),
            "current_loc": {"lines": curr_loc[0], "files": curr_loc[1]},
            "breakdowns": {
                "authors": _author_details(commits),
                "monthly": [
                    {"month": m, "commits": c, "added": a, "deleted": d, "files": f}
                    for (m, c, a, d, f) in _aggregate_monthly(commits)
                ],
            },
            "monthly_hours": monthly_hours_list,
        }
        all_payloads.append(data)

    md, combined = build_dashboard(all_payloads)
    (OUTPUT_DIR / "_git_eval_dashboard.md").write_text(md)
    (OUTPUT_DIR / "_git_eval_dashboard.json").write_text(json.dumps(combined, indent=2))
    print(f"Wrote combined dashboard for {len(all_payloads)} repos to {OUTPUT_DIR.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

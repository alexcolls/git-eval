#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import asdict
import json
import csv
from datetime import timedelta

# Optional plotting for PNG charts
HAS_MPL = False
try:
    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False

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


def _compute_monthly_hours_by_author(commits) -> Dict[str, Dict[str, float]]:
    session_gap_minutes = int(os.getenv("SESSION_GAP_MINUTES", "90") or "90")
    per_commit_base = float(os.getenv("MINUTES_PER_COMMIT_BASE", "12") or "12")
    per_100_lines = float(os.getenv("MINUTES_PER_100_LINES", "8") or "8")
    per_file_min = float(os.getenv("MINUTES_PER_FILE", "2") or "2")
    calibration = float(os.getenv("CALIBRATION_FACTOR", "1.5") or "1.5")
    session_gap = timedelta(minutes=session_gap_minutes)

    per_author: Dict[str, List] = {}
    for c in commits:
        key = (c.author_name or "Unknown").strip()
        if c.author_email:
            key = f"{key} <{c.author_email}>"
        per_author.setdefault(key, []).append(c)

    result: Dict[str, Dict[str, float]] = {}
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
        month_minutes: Dict[str, float] = {}
        for sess in sessions:
            minutes = 0.0
            for c in sess:
                loc = max(0, (c.added or 0) + (c.deleted or 0))
                minutes += per_commit_base + ((loc ** 0.5) / 10.0) * per_100_lines + (c.files_changed or 0) * per_file_min
            m = sess[-1].author_date.strftime("%Y-%m")
            month_minutes[m] = month_minutes.get(m, 0.0) + minutes
        # convert to hours and apply calibration
        result[author] = {m: round(v * calibration / 60.0, 2) for m, v in month_minutes.items()}
    return result


def _compute_daily_hours(commits) -> Dict[str, float]:
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

    day_hours: Dict[str, float] = {}
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
            d = sess[-1].author_date.date().isoformat()
            day_hours[d] = day_hours.get(d, 0.0) + minutes
    # apply calibration and convert to hours
    return {d: round(v * calibration / 60.0, 2) for d, v in day_hours.items()}


def _compute_daily_hours_by_author(commits) -> Dict[str, Dict[str, float]]:
    session_gap_minutes = int(os.getenv("SESSION_GAP_MINUTES", "90") or "90")
    per_commit_base = float(os.getenv("MINUTES_PER_COMMIT_BASE", "12") or "12")
    per_100_lines = float(os.getenv("MINUTES_PER_100_LINES", "8") or "8")
    per_file_min = float(os.getenv("MINUTES_PER_FILE", "2") or "2")
    calibration = float(os.getenv("CALIBRATION_FACTOR", "1.5") or "1.5")
    session_gap = timedelta(minutes=session_gap_minutes)

    per_author: Dict[str, List] = {}
    for c in commits:
        key = (c.author_name or "Unknown").strip()
        if c.author_email:
            key = f"{key} <{c.author_email}>"
        per_author.setdefault(key, []).append(c)

    result: Dict[str, Dict[str, float]] = {}
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
        day_minutes: Dict[str, float] = {}
        for sess in sessions:
            minutes = 0.0
            for c in sess:
                loc = max(0, (c.added or 0) + (c.deleted or 0))
                minutes += per_commit_base + ((loc ** 0.5) / 10.0) * per_100_lines + (c.files_changed or 0) * per_file_min
            d = sess[-1].author_date.date().isoformat()
            day_minutes[d] = day_minutes.get(d, 0.0) + minutes
        result[author] = {d: round(v * calibration / 60.0, 2) for d, v in day_minutes.items()}
    return result


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

        # Monthly commits distribution pies for recent months (top 5 repos)
        lines.append("## Monthly commits - distribution (top 5 repos, recent months)")
        lines.append("")
        # Determine top 5 repos by total commits
        repo_commit_totals: Dict[str, int] = {}
        per_repo_month_commits: Dict[str, Dict[str, int]] = {}
        all_months: set = set()
        for r in per_repo_sorted:
            repo_name = Path(r["repo"]).name
            repo_map: Dict[str, int] = {}
            for row in r.get("breakdowns", {}).get("monthly", []):
                m = row.get("month")
                c = int(row.get("commits", 0))
                if not m:
                    continue
                all_months.add(m)
                repo_map[m] = repo_map.get(m, 0) + c
            per_repo_month_commits[repo_name] = repo_map
            repo_commit_totals[repo_name] = sum(repo_map.values())
        months_sorted = sorted(all_months)
        top_repos = [name for name, _ in sorted(repo_commit_totals.items(), key=lambda x: x[1], reverse=True)[:5]]
        # Show pies for up to last 6 months
        for m in months_sorted[-6:]:
            parts = []
            for name in top_repos:
                v = per_repo_month_commits.get(name, {}).get(m, 0)
                if v > 0:
                    parts.append((name, v))
            if parts:
                lines.append("```mermaid")
                lines.append(f"pie title Monthly commits by repo - {m}")
                for name, v in sorted(parts, key=lambda x: x[1], reverse=True):
                    safe = name.replace('"', '\\"')
                    lines.append(f'    "{safe}" : {v}')
                lines.append("```")
                lines.append("")

        # Hours by repo as a pie (top 15)
        lines.append("## Hours by repo (top 15)")
        lines.append("")
        lines.append("```mermaid")
        lines.append("pie title Hours by repo (top 15)")
        parts = []
        for r in per_repo_sorted[:15]:
            repo_name = Path(r["repo"]).name
            parts.append((repo_name, float(r["metrics"]["estimated_hours_total"])) )
        for repo_name, hours in parts:
            safe = repo_name.replace('"', '\\"')
            lines.append(f'    "{safe}" : {hours:.2f}')
        lines.append("```")
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

    # Line charts (ASCII) — monthly hours by top repos and authors
    # Build author monthly hours aggregate
    author_month_hours_agg: Dict[str, Dict[str, float]] = {}
    months_all: set = set(month_totals_hours.keys())
    for r in per_repo_sorted:
        for row in r.get("author_monthly_hours", []):
            a = row.get("author")
            m = row.get("month")
            h = float(row.get("hours", 0.0))
            if not a or not m:
                continue
            months_all.add(m)
            author_month_hours_agg.setdefault(a, {})
            author_month_hours_agg[a][m] = author_month_hours_agg[a].get(m, 0.0) + h

    def sparkline(vals: List[float]) -> str:
        # Unicode blocks for levels
        blocks = "▁▂▃▄▅▆▇█"
        if not vals:
            return ""
        max_v = max(vals)
        if max_v <= 0:
            return "".join("▁" for _ in vals)
        out = []
        for v in vals:
            idx = int(round((v / max_v) * (len(blocks) - 1))) if v > 0 else 0
            out.append(blocks[idx])
        return "".join(out)

    months_sorted2 = sorted(months_all)

    # Top 5 repos by hours series
    lines.append("## Monthly hours (ASCII sparkline)")
    lines.append("")
    lines.append("### Top repos")
    # Build per-repo monthly hours series
    repo_series = []
    for r in per_repo_sorted[:5]:
        name = Path(r["repo"]).name
        mm = {row["month"]: float(row["hours"]) for row in r.get("monthly_hours", [])}
        series = [mm.get(m, 0.0) for m in months_sorted2]
        repo_series.append((name, series))
    # Compute global max for scaling (we scale per-series using sparkline intrinsic; optional)
    lines.append("```")
    lines.append("Months: " + ", ".join(months_sorted2))
    for name, series in repo_series:
        lines.append(f"{name:<24} {sparkline(series)}  ({sum(series):.1f}h)")
    lines.append("```")
    lines.append("")

    # Top 5 authors by hours series
    lines.append("### Top authors")
    author_series = []
    for a in [a["author"] for a in author_sorted[:5]]:
        mm = author_month_hours_agg.get(a, {})
        series = [mm.get(m, 0.0) for m in months_sorted2]
        author_series.append((a, series))
    lines.append("```")
    lines.append("Months: " + ", ".join(months_sorted2))
    for a, series in author_series:
        lines.append(f"{a:<24} {sparkline(series)}  ({sum(series):.1f}h)")
    lines.append("```")
    lines.append("")

    # Optional PNG line charts using matplotlib
    charts_dir = OUTPUT_DIR / "charts"
    if HAS_MPL and months_sorted2:
        charts_dir.mkdir(parents=True, exist_ok=True)
        # Repos chart
        try:
            fig, ax = plt.subplots(figsize=(10, 4))
            for name, series in repo_series:
                ax.plot(range(len(months_sorted2)), series, marker="o", label=name)
            ax.set_xticks(range(len(months_sorted2)))
            ax.set_xticklabels(months_sorted2, rotation=45, ha="right")
            ax.set_ylabel("Hours")
            ax.set_title("Monthly hours — top repos")
            ax.legend(loc="upper left", fontsize=8, ncol=2)
            fig.tight_layout()
            repos_png = charts_dir / "monthly_hours_repos.png"
            fig.savefig(repos_png, dpi=120)
            plt.close(fig)
            lines.append(f"![Monthly hours — top repos](charts/{repos_png.name})")
            lines.append("")
        except Exception:
            pass
        # Authors chart
        try:
            fig, ax = plt.subplots(figsize=(10, 4))
            for name, series in author_series:
                ax.plot(range(len(months_sorted2)), series, marker="o", label=name)
            ax.set_xticks(range(len(months_sorted2)))
            ax.set_xticklabels(months_sorted2, rotation=45, ha="right")
            ax.set_ylabel("Hours")
            ax.set_title("Monthly hours — top authors")
            ax.legend(loc="upper left", fontsize=8, ncol=2)
            fig.tight_layout()
            authors_png = charts_dir / "monthly_hours_authors.png"
            fig.savefig(authors_png, dpi=120)
            plt.close(fig)
            lines.append(f"![Monthly hours — top authors](charts/{authors_png.name})")
            lines.append("")
        except Exception:
            pass

    # Daily hours (ASCII) — last 60 days, top repos and authors
    # Build per-repo daily hours
    all_dates: set = set()
    repo_daily_map: Dict[str, Dict[str, float]] = {}
    for r in per_repo_sorted:
        name = Path(r["repo"]).name
        mm: Dict[str, float] = {}
        for row in r.get("daily_hours", []):
            d = row.get("date")
            h = float(row.get("hours", 0.0))
            if not d:
                continue
            mm[d] = mm.get(d, 0.0) + h
            all_dates.add(d)
        repo_daily_map[name] = mm
    # Build per-author daily hours
    author_daily_map: Dict[str, Dict[str, float]] = {}
    for r in per_repo_sorted:
        for row in r.get("author_daily_hours", []):
            a = row.get("author")
            d = row.get("date")
            h = float(row.get("hours", 0.0))
            if not a or not d:
                continue
            author_daily_map.setdefault(a, {})
            author_daily_map[a][d] = author_daily_map[a].get(d, 0.0) + h
            all_dates.add(d)
    if all_dates:
        last_dates = sorted(all_dates)[-60:]
        lines.append("## Daily hours (ASCII sparkline) — last 60 days")
        lines.append("")
        # Top repos by total daily hours in window
        repo_totals = []
        for name, mm in repo_daily_map.items():
            total = sum(mm.get(d, 0.0) for d in last_dates)
            repo_totals.append((name, total))
        top_repo_names = [n for n, _ in sorted(repo_totals, key=lambda x: x[1], reverse=True)[:5]]
        lines.append("### Top repos")
        lines.append("```")
        lines.append("Dates: " + ", ".join(last_dates))
        for name in top_repo_names:
            series = [repo_daily_map.get(name, {}).get(d, 0.0) for d in last_dates]
            lines.append(f"{name:<24} {sparkline(series)}  ({sum(series):.1f}h)")
        lines.append("```")
        lines.append("")
        # Top authors by total daily hours in window
        author_totals = []
        for a, mm in author_daily_map.items():
            total = sum(mm.get(d, 0.0) for d in last_dates)
            author_totals.append((a, total))
        top_author_names = [n for n, _ in sorted(author_totals, key=lambda x: x[1], reverse=True)[:5]]
        lines.append("### Top authors")
        lines.append("```")
        lines.append("Dates: " + ", ".join(last_dates))
        for a in top_author_names:
            series = [author_daily_map.get(a, {}).get(d, 0.0) for d in last_dates]
            lines.append(f"{a:<24} {sparkline(series)}  ({sum(series):.1f}h)")
        lines.append("```")
        lines.append("")
        # Optional PNG for daily
        if HAS_MPL:
            try:
                fig, ax = plt.subplots(figsize=(10, 4))
                for name in top_repo_names:
                    series = [repo_daily_map.get(name, {}).get(d, 0.0) for d in last_dates]
                    ax.plot(range(len(last_dates)), series, marker="o", label=name)
                ax.set_xticks(range(len(last_dates)))
                ax.set_xticklabels(last_dates, rotation=45, ha="right", fontsize=7)
                ax.set_ylabel("Hours")
                ax.set_title("Daily hours — top repos (last 60 days)")
                ax.legend(loc="upper left", fontsize=7, ncol=2)
                fig.tight_layout()
                repos_daily_png = charts_dir / "daily_hours_repos.png"
                fig.savefig(repos_daily_png, dpi=120)
                plt.close(fig)
                lines.append(f"![Daily hours — top repos](charts/{repos_daily_png.name})")
                lines.append("")
            except Exception:
                pass
            try:
                fig, ax = plt.subplots(figsize=(10, 4))
                for a in top_author_names:
                    series = [author_daily_map.get(a, {}).get(d, 0.0) for d in last_dates]
                    ax.plot(range(len(last_dates)), series, marker="o", label=a)
                ax.set_xticks(range(len(last_dates)))
                ax.set_xticklabels(last_dates, rotation=45, ha="right", fontsize=7)
                ax.set_ylabel("Hours")
                ax.set_title("Daily hours — top authors (last 60 days)")
                ax.legend(loc="upper left", fontsize=7, ncol=2)
                fig.tight_layout()
                authors_daily_png = charts_dir / "daily_hours_authors.png"
                fig.savefig(authors_daily_png, dpi=120)
                plt.close(fig)
                lines.append(f"![Daily hours — top authors](charts/{authors_daily_png.name})")
                lines.append("")
            except Exception:
                pass

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

    # Daily hours across repos
    day_totals_hours: Dict[str, float] = {}
    day_totals_commits: Dict[str, int] = {}
    day_totals_added: Dict[str, int] = {}
    day_totals_deleted: Dict[str, int] = {}
    for r in per_repo_sorted:
        for row in r.get("daily_hours", []):
            d = row.get("date")
            h = float(row.get("hours", 0.0))
            if not d:
                continue
            day_totals_hours[d] = day_totals_hours.get(d, 0.0) + h
        # commits/lines by day from monthly only not available; approximate via daily from _aggregate_daily not provided here.
        # Skipping fine-grained daily commits/adds/deletes aggregation for now.

    # Write CSV exports
    # 1) Global monthly totals
    monthly_csv = OUTPUT_DIR / "_git_eval_monthly_totals.csv"
    with monthly_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "hours", "commits", "added", "deleted"])
        for m in sorted(month_totals_hours.keys()):
            w.writerow([m, f"{month_totals_hours[m]:.2f}", month_totals_commits.get(m, 0), month_totals_added.get(m, 0), month_totals_deleted.get(m, 0)])
    # 2) Global daily totals (hours)
    daily_csv = OUTPUT_DIR / "_git_eval_daily_totals.csv"
    with daily_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "hours", "is_weekend"])
        for d in sorted(day_totals_hours.keys()):
            # heuristic: weekend flag based on calendar weekday
            from datetime import datetime as _dt
            is_weekend = 1 if _dt.fromisoformat(d).weekday() >= 5 else 0
            w.writerow([d, f"{day_totals_hours[d]:.2f}", is_weekend])

    # 3) Author schedule aggregates
    authors_csv = OUTPUT_DIR / "_git_eval_authors_schedule.csv"
    with authors_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["author", "estimated_hours", "commits", "weekends_active_days", "weekdays_active_days", "days_night_active", "days_daytime_active", "days_both", "repos_count"])
        for a in author_sorted:
            w.writerow([
                a["author"], f"{a["estimated_hours"]:.2f}", a["commits_total"],
                a.get("weekends_active_days", 0), a.get("weekdays_active_days", 0), a.get("days_night_active", 0),
                a.get("days_daytime_active", 0), a.get("days_both", 0), len(a.get("repos", []))
            ])

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
        dashboard_only = os.getenv("DASHBOARD_ONLY", "0") in {"1","true","True"}
        if not dashboard_only:
            write_reports(OUTPUT_DIR, path, metrics, commits)
        # current LOC snapshot can be very slow; skip when dashboard-only
        if dashboard_only:
            curr_loc = (0, 0)
        else:
            curr_loc = _current_loc_snapshot(path)
        # compute monthly & daily hours for this repo
        monthly_hours_map = _compute_monthly_hours(commits)
        monthly_hours_list = [{"month": m, "hours": h} for m, h in sorted(monthly_hours_map.items())]
        daily_hours_map = _compute_daily_hours(commits)
        daily_hours_list = [{"date": d, "hours": h} for d, h in sorted(daily_hours_map.items())]
        # author monthly hours
        author_month_hours_map = _compute_monthly_hours_by_author(commits)
        author_month_hours_list = [
            {"author": a, "month": m, "hours": h}
            for a, mm in author_month_hours_map.items()
            for m, h in mm.items()
        ]
        # author daily hours
        author_day_hours_map = _compute_daily_hours_by_author(commits)
        author_day_hours_list = [
            {"author": a, "date": d, "hours": h}
            for a, dd in author_day_hours_map.items()
            for d, h in dd.items()
        ]
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
            "daily_hours": daily_hours_list,
            "author_monthly_hours": author_month_hours_list,
            "author_daily_hours": author_day_hours_list,
        }
        all_payloads.append(data)

    md, combined = build_dashboard(all_payloads)
    (OUTPUT_DIR / "_git_eval_dashboard.md").write_text(md)
    (OUTPUT_DIR / "_git_eval_dashboard.json").write_text(json.dumps(combined, indent=2))
    print(f"Wrote combined dashboard for {len(all_payloads)} repos to {OUTPUT_DIR.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import csv
import dataclasses
import json
import os
import re
import shlex
import subprocess
import sys
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import statistics

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*args, **kwargs):
        return False

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_FMT = "%Y-%m-%d"

@dataclass
class CommitNumstat:
    hash: str
    author_name: str
    author_email: str
    author_date: datetime
    added: int
    deleted: int
    files_changed: int
    is_merge: bool

@dataclass
class RepoMetrics:
    repo_path: str
    commits_total: int
    merges_total: int
    non_merges_total: int
    unique_authors: int
    first_commit: Optional[str]
    last_commit: Optional[str]
    active_days: int
    span_days: int
    avg_commits_per_day: float
    added_lines_total: int
    deleted_lines_total: int
    files_changed_total: int
    estimated_hours_total: float


def run(cmd: List[str], cwd: Optional[str] = None) -> str:
    out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.DEVNULL)
    return out.decode().rstrip("\n")


def is_git_dir(path: Path) -> bool:
    if not path:
        return False
    if path.is_file():
        # worktree .git file points elsewhere; still acceptable
        return path.name == ".git"
    if path.is_dir():
        return (path / "HEAD").exists() and (path / "objects").exists()
    return False


def resolve_git_dir(input_path: Path) -> Tuple[Path, Path]:
    """Return (work_tree, git_dir). input_path may be a .git dir or a work tree.
    """
    p = input_path.resolve()
    if p.is_dir() and p.name == ".git":
        # find worktree root
        try:
            wt = Path(run(["git", "--git-dir", str(p), "rev-parse", "--show-toplevel"]))
        except subprocess.CalledProcessError:
            wt = p.parent
        return wt, p
    # otherwise assume work tree
    try:
        wt = Path(run(["git", "-C", str(p), "rev-parse", "--show-toplevel"]))
        gd = Path(run(["git", "-C", str(p), "rev-parse", "--git-dir"]))
        if not gd.is_absolute():
            gd = (wt / gd).resolve()
        return wt, gd
    except subprocess.CalledProcessError:
        raise SystemExit(f"Not a git repository: {p}")


def parse_git_log_with_numstat(work_tree: Path, include_merges: bool) -> List[CommitNumstat]:
    fmt = "%H%x01%an%x01%ae%x01%aI%x01%P"
    args = [
        "git", "-C", str(work_tree),
        "log", "--all", "--numstat", f"--format={fmt}",
    ]
    if not include_merges:
        args.append("--no-merges")
    out = run(args)
    commits: List[CommitNumstat] = []
    cur: Optional[CommitNumstat] = None
    for line in out.splitlines():
        if not line:
            continue
        if "\x01" in line:
            # header
            parts = line.split("\x01")
            c_hash, a_name, a_email, a_iso, parents = parts
            is_merge = bool(parents.strip()) and len(parents.split()) >= 2
            d = datetime.fromisoformat(a_iso.replace("Z", "+00:00"))
            cur = CommitNumstat(
                hash=c_hash,
                author_name=a_name,
                author_email=a_email,
                author_date=d,
                added=0,
                deleted=0,
                files_changed=0,
                is_merge=is_merge,
            )
            commits.append(cur)
        else:
            # numstat row
            if cur is None:
                continue
            cols = line.split("\t")
            if len(cols) < 3:
                continue
            add, delete, _path = cols[:3]
            try:
                a = 0 if add == "-" else int(add)
                d = 0 if delete == "-" else int(delete)
            except ValueError:
                a = d = 0
            cur.added += a
            cur.deleted += d
            cur.files_changed += 1
    return commits


def compute_metrics(commits: List[CommitNumstat]) -> RepoMetrics:
    if not commits:
        return RepoMetrics(
            repo_path="",
            commits_total=0,
            merges_total=0,
            non_merges_total=0,
            unique_authors=0,
            first_commit=None,
            last_commit=None,
            active_days=0,
            span_days=0,
            avg_commits_per_day=0.0,
            added_lines_total=0,
            deleted_lines_total=0,
            files_changed_total=0,
            estimated_hours_total=0.0,
        )
    commits_sorted = sorted(commits, key=lambda c: c.author_date)
    first = commits_sorted[0].author_date
    last = commits_sorted[-1].author_date
    span_days = (last.date() - first.date()).days + 1
    days = {c.author_date.date() for c in commits_sorted}
    active_days = len(days)
    commits_total = len(commits_sorted)
    merges_total = sum(1 for c in commits_sorted if c.is_merge)
    non_merges_total = commits_total - merges_total
    unique_authors = len({c.author_email for c in commits_sorted if c.author_email})
    added_lines_total = sum(c.added for c in commits_sorted)
    deleted_lines_total = sum(c.deleted for c in commits_sorted)
    files_changed_total = sum(c.files_changed for c in commits_sorted)
    avg_commits_per_day = (commits_total / span_days) if span_days > 0 else 0.0

    # Effort estimation using session + commit-weighted heuristic
    author_effort = _estimate_hours_per_author(commits_sorted)
    hours_total = sum(v["hours"] for v in author_effort.values())

    return RepoMetrics(
        repo_path="",
        commits_total=commits_total,
        merges_total=merges_total,
        non_merges_total=non_merges_total,
        unique_authors=unique_authors,
        first_commit=first.isoformat(),
        last_commit=last.isoformat(),
        active_days=active_days,
        span_days=span_days,
        avg_commits_per_day=round(avg_commits_per_day, 4),
        added_lines_total=added_lines_total,
        deleted_lines_total=deleted_lines_total,
        files_changed_total=files_changed_total,
        estimated_hours_total=round(hours_total, 2),
    )


def _aggregate_by_author(commits: List[CommitNumstat]) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    """Return (commits_by_author, added_by_author, deleted_by_author) keyed by "Name <email>" or name.
    """
    commits_by: Dict[str, int] = Counter()
    added_by: Dict[str, int] = Counter()
    deleted_by: Dict[str, int] = Counter()
    for c in commits:
        label = (c.author_name or "Unknown").strip()
        if c.author_email:
            label = f"{label} <{c.author_email}>"
        commits_by[label] += 1
        added_by[label] += c.added
        deleted_by[label] += c.deleted
    return dict(commits_by), dict(added_by), dict(deleted_by)


def _author_details(commits: List[CommitNumstat]) -> List[Dict[str, object]]:
    per_author_commits: Dict[str, List[CommitNumstat]] = defaultdict(list)
    for c in commits:
        key = (c.author_name or "Unknown").strip()
        if c.author_email:
            key = f"{key} <{c.author_email}>"
        per_author_commits[key].append(c)
    details: List[Dict[str, object]] = []
    effort = _estimate_hours_per_author(commits)
    for author, cs in per_author_commits.items():
        cs.sort(key=lambda x: x.author_date)
        commits_total = len(cs)
        merges_total = sum(1 for c in cs if c.is_merge)
        added = sum(c.added for c in cs)
        deleted = sum(c.deleted for c in cs)
        files = sum(c.files_changed for c in cs)
        first = cs[0].author_date.isoformat()
        last = cs[-1].author_date.isoformat()
        active_days = len({c.author_date.date() for c in cs})
        sizes = [c.added + c.deleted for c in cs]
        avg_size = round(sum(sizes) / commits_total, 2) if commits_total else 0.0
        med_size = float(statistics.median(sizes)) if sizes else 0.0
        details.append({
            "author": author,
            "commits_total": commits_total,
            "merges_total": merges_total,
            "added_total": added,
            "deleted_total": deleted,
            "files_changed_total": files,
            "first_commit": first,
            "last_commit": last,
            "active_days": active_days,
            "avg_commit_size": avg_size,
            "median_commit_size": med_size,
            "sessions": effort.get(author, {}).get("sessions", 0),
            "estimated_hours": round(effort.get(author, {}).get("hours", 0.0), 2),
        })
    # sort by estimated hours desc then commits desc
    details.sort(key=lambda d: (d["estimated_hours"], d["commits_total"]), reverse=True)
    return details


def _estimate_hours_per_author(commits_sorted: List[CommitNumstat]) -> Dict[str, Dict[str, float]]:
    """Estimate hours per author using a session + commit-weighted heuristic.

    For each author:
    - Split commits into sessions with gap > SESSION_GAP_MINUTES.
    - Per session, compute per-commit minutes as:
        minutes = MINUTES_PER_COMMIT_BASE
                  + (sqrt(lines_changed)/10) * MINUTES_PER_100_LINES
                  + files_changed * MINUTES_PER_FILE
      Sum minutes across commits in the session.
    - Enforce MIN_SESSION_MINUTES minimum per session.
    - Sum per day with a cap of MAX_HOURS_PER_DAY.
    - Multiply totals by CALIBRATION_FACTOR.
    Returns mapping author -> {"hours": float, "sessions": int}.
    """
    # config
    session_gap_minutes = int(os.getenv("SESSION_GAP_MINUTES", "90") or "90")
    max_hours_per_day = float(os.getenv("MAX_HOURS_PER_DAY", "10") or "10")
    min_session_minutes = float(os.getenv("MIN_SESSION_MINUTES", "30") or "30")
    per_commit_base = float(os.getenv("MINUTES_PER_COMMIT_BASE", "12") or "12")
    per_100_lines = float(os.getenv("MINUTES_PER_100_LINES", "8") or "8")
    per_file_min = float(os.getenv("MINUTES_PER_FILE", "2") or "2")
    calibration = float(os.getenv("CALIBRATION_FACTOR", "1.5") or "1.5")

    session_gap = timedelta(minutes=session_gap_minutes)

    per_author_commits: Dict[str, List[CommitNumstat]] = defaultdict(list)
    for c in commits_sorted:
        key = (c.author_name or "Unknown").strip()
        if c.author_email:
            key = f"{key} <{c.author_email}>"
        per_author_commits[key].append(c)

    result: Dict[str, Dict[str, float]] = {}
    for author, cs in per_author_commits.items():
        cs.sort(key=lambda x: x.author_date)
        # Build sessions
        sessions: List[List[CommitNumstat]] = []
        cur: List[CommitNumstat] = []
        prev_time: Optional[datetime] = None
        for c in cs:
            if prev_time is None or (c.author_date - prev_time) > session_gap:
                if cur:
                    sessions.append(cur)
                cur = [c]
            else:
                cur.append(c)
            prev_time = c.author_date
        if cur:
            sessions.append(cur)
        sessions_count = len(sessions)

        # Aggregate per day with cap
        per_day_hours: Dict[date, float] = defaultdict(float)
        for sess in sessions:
            # Compute per-commit minutes
            sess_minutes = 0.0
            for c in sess:
                loc = max(0, c.added + c.deleted)
                # sqrt attenuates huge commits but still increases effort
                minutes = per_commit_base + (loc ** 0.5 / 10.0) * per_100_lines + c.files_changed * per_file_min
                sess_minutes += minutes
            sess_minutes = max(sess_minutes, min_session_minutes)
            # Assign to session end date
            end_date = sess[-1].author_date.date()
            per_day_hours[end_date] += sess_minutes / 60.0
        # Apply per-day cap
        total_hours = 0.0
        for d, h in per_day_hours.items():
            total_hours += min(h, max_hours_per_day)
        total_hours *= calibration
        result[author] = {"hours": total_hours, "sessions": float(sessions_count)}
    return result


def _aggregate_daily(commits: List[CommitNumstat]) -> List[Tuple[str, int, int, int, int]]:
    buckets: Dict[str, Dict[str, int]] = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "files": 0})
    for c in commits:
        key = c.author_date.strftime("%Y-%m-%d")
        b = buckets[key]
        b["commits"] += 1
        b["added"] += c.added
        b["deleted"] += c.deleted
        b["files"] += c.files_changed
    out: List[Tuple[str, int, int, int, int]] = []
    for k in sorted(buckets.keys()):
        v = buckets[k]
        out.append((k, v["commits"], v["added"], v["deleted"], v["files"]))
    return out


def _longest_streak(dates: List[date]) -> Tuple[int, Optional[str], Optional[str]]:
    if not dates:
        return 0, None, None
    s = sorted(set(dates))
    best = 1
    cur = 1
    best_start = s[0]
    best_end = s[0]
    cur_start = s[0]
    for i in range(1, len(s)):
        if (s[i] - s[i-1]).days == 1:
            cur += 1
            if cur > best:
                best = cur
                best_start = cur_start
                best_end = s[i]
        else:
            cur = 1
            cur_start = s[i]
    return best, best_start.isoformat(), best_end.isoformat() if isinstance(best_end, date) else None


def _current_loc_snapshot(work_tree: Path) -> Tuple[int, int]:
    """Return (lines_of_code, tracked_files_count) for current working tree (tracked files)."""
    try:
        out = run(["git", "-C", str(work_tree), "ls-files", "-z"])  # NUL-separated
    except subprocess.CalledProcessError:
        return 0, 0
    total_lines = 0
    files_count = 0
    for rel in out.split("\x00"):
        if not rel:
            continue
        p = (work_tree / rel)
        # Skip if not a regular file
        try:
            st = p.stat()
        except FileNotFoundError:
            continue
        if not p.is_file():
            continue
        # Count lines in binary-safe way
        try:
            with p.open("rb") as f:
                total_lines += sum(1 for _ in f)
                files_count += 1
        except Exception:
            continue
    return total_lines, files_count


def _aggregate_monthly(commits: List[CommitNumstat]) -> List[Tuple[str, int, int, int, int]]:
    """Return list of (YYYY-MM, commits, added, deleted, files_changed) sorted ascending by month."""
    buckets: Dict[str, Dict[str, int]] = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "files": 0})
    for c in commits:
        key = c.author_date.strftime("%Y-%m")
        b = buckets[key]
        b["commits"] += 1
        b["added"] += c.added
        b["deleted"] += c.deleted
        b["files"] += c.files_changed
    out: List[Tuple[str, int, int, int, int]] = []
    for k in sorted(buckets.keys()):
        v = buckets[k]
        out.append((k, v["commits"], v["added"], v["deleted"], v["files"]))
    return out


def _write_markdown_report(output_dir: Path, work_tree: Path, metrics: RepoMetrics, commits: List[CommitNumstat]) -> None:
    repo_name = work_tree.name
    base = output_dir / f"{repo_name}_git_eval.md"
    commits_by, added_by, deleted_by = _aggregate_by_author(commits)
    monthly = _aggregate_monthly(commits)
    daily = _aggregate_daily(commits)
    authors = _author_details(commits)
    current_loc, tracked_files = _current_loc_snapshot(work_tree)

    def md_escape(s: str) -> str:
        return s.replace("|", "\\|")

    # Build simple ASCII bar charts
    max_commits = max((c for _, c, _, _, _ in monthly), default=1)
    bar_width = 40
    def bar(n: int, max_n: int = max_commits) -> str:
        if max_n <= 0:
            return ""
        filled = int(round((n / max_n) * bar_width))
        return "#" * max(1, filled) if n > 0 else ""

    lines: List[str] = []
    lines.append(f"# Git Evaluation — {repo_name}")
    lines.append("")
    lines.append(f"Repo: `{work_tree.as_posix()}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Current tracked files | {tracked_files} |")
    lines.append(f"| Current lines of code (tracked) | {current_loc} |")
    lines.append(f"| Commits (total) | {metrics.commits_total} |")
    lines.append(f"| Commits (merges) | {metrics.merges_total} |")
    lines.append(f"| Commits (non-merges) | {metrics.non_merges_total} |")
    lines.append(f"| Unique authors | {metrics.unique_authors} |")
    lines.append(f"| First commit | {md_escape(metrics.first_commit or '-')} |")
    lines.append(f"| Last commit | {md_escape(metrics.last_commit or '-')} |")
    lines.append(f"| Active days | {metrics.active_days} |")
    lines.append(f"| Span days | {metrics.span_days} |")
    lines.append(f"| Avg commits/day | {metrics.avg_commits_per_day} |")
    lines.append(f"| Lines added (sum) | {metrics.added_lines_total} |")
    lines.append(f"| Lines deleted (sum) | {metrics.deleted_lines_total} |")
    lines.append(f"| Files touched (sum of numstat rows) | {metrics.files_changed_total} |")
    lines.append(f"| Estimated hours (session-based) | {metrics.estimated_hours_total} |")
    lines.append("")

    # Leaderboard
    if authors:
        total_hours = sum(a["estimated_hours"] for a in authors) or 1.0
        lines.append("## Developer leaderboard")
        lines.append("")
        lines.append("| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:")
        top_hours = max(a["estimated_hours"] for a in authors) if authors else 0
        for a in authors:
            stars = int(round((a["estimated_hours"] / top_hours) * 5)) if top_hours > 0 else 0
            star_bar = "★" * stars + "☆" * (5 - stars)
            lines.append(
                f"| {md_escape(a['author'])} | {a['commits_total']} | {a['estimated_hours']} | {a['added_total']} | {a['deleted_total']} | {a['files_changed_total']} | {a['active_days']} | {md_escape(a['first_commit'])} | {md_escape(a['last_commit'])} | {a['avg_commit_size']} | {a['median_commit_size']} | {star_bar} |"
            )
        lines.append("")

    # Mermaid pies
    if commits_by:
        lines.append("## Commits by author")
        lines.append("")
        lines.append("```mermaid")
        lines.append("pie title Commits by author")
        for label, count in sorted(commits_by.items(), key=lambda x: x[1], reverse=True):
            safe = label.replace('"', "\\\"")
            lines.append(f'    "{safe}" : {count}')
        lines.append("```")
        lines.append("")
    if added_by:
        lines.append("## Lines added by author")
        lines.append("")
        lines.append("```mermaid")
        lines.append("pie title Lines added by author")
        for label, count in sorted(added_by.items(), key=lambda x: x[1], reverse=True):
            safe = label.replace('"', "\\\"")
            lines.append(f'    "{safe}" : {count}')
        lines.append("```")
        lines.append("")

    # Effort model
    lines.append("## Effort estimation model")
    lines.append("")
    lines.append("This report estimates effort using a session + commit-weighted heuristic:")
    lines.append("- Split commits per author into sessions where the gap > SESSION_GAP_MINUTES.")
    lines.append("- Per session, sum per-commit minutes: base + sqrt(lines)/10 * MINUTES_PER_100_LINES + files * MINUTES_PER_FILE.")
    lines.append("- Enforce MIN_SESSION_MINUTES minimum per session.")
    lines.append("- Sum per day with MAX_HOURS_PER_DAY cap; multiply by CALIBRATION_FACTOR.")
    lines.append("")
    lines.append("Parameters:")
    lines.append("")
    lines.append("| Param | Value |")
    lines.append("|---|---:|")
    lines.append(f"| SESSION_GAP_MINUTES | {int(os.getenv('SESSION_GAP_MINUTES', '90') or '90')} |")
    lines.append(f"| MAX_HOURS_PER_DAY | {float(os.getenv('MAX_HOURS_PER_DAY', '10') or '10')} |")
    lines.append(f"| MIN_SESSION_MINUTES | {float(os.getenv('MIN_SESSION_MINUTES', '30') or '30')} |")
    lines.append(f"| MINUTES_PER_COMMIT_BASE | {float(os.getenv('MINUTES_PER_COMMIT_BASE', '12') or '12')} |")
    lines.append(f"| MINUTES_PER_100_LINES | {float(os.getenv('MINUTES_PER_100_LINES', '8') or '8')} |")
    lines.append(f"| MINUTES_PER_FILE | {float(os.getenv('MINUTES_PER_FILE', '2') or '2')} |")
    lines.append(f"| CALIBRATION_FACTOR | {float(os.getenv('CALIBRATION_FACTOR', '1.5') or '1.5')} |")
    lines.append("")

    # Monthly activity
    if monthly:
        lines.append("## Monthly activity")
        lines.append("")
        lines.append("| Month | Commits | Added | Deleted | Files | Chart |")
        lines.append("|---|---:|---:|---:|---:|:---|")
        max_c = max(c for _, c, _, _, _ in monthly)
        for m, c, a, d, f in monthly:
            lines.append(f"| {m} | {c} | {a} | {d} | {f} | {bar(c, max_c)} |")
        lines.append("")

    # Activity timeline by author (Gantt-style by active months)
    if authors and monthly:
        # Build author-month activity map
        author_months: Dict[str, set] = defaultdict(set)
        for c in commits:
            key = (c.author_name or "Unknown").strip()
            if c.author_email:
                key = f"{key} <{c.author_email}>"
            author_months[key].add(c.author_date.strftime("%Y-%m"))
        months = [m for (m, *_rest) in monthly]
        if months:
            lines.append("## Author activity timeline")
            lines.append("")
            lines.append("```mermaid")
            lines.append("gantt")
            lines.append("    title Active months per author")
            lines.append("    dateFormat  YYYY-MM-DD")
            # Mermaid Gantt needs ranges; map each active month to a task covering that month
            for author in sorted(author_months.keys()):
                months_active = sorted(author_months[author])
                # group contiguous months into ranges
                def month_to_date(m):
                    y, mo = map(int, m.split("-"))
                    return date(y, mo, 1)
                def month_add(dt: date) -> date:
                    y = dt.year + (1 if dt.month == 12 else 0)
                    m = 1 if dt.month == 12 else dt.month + 1
                    return date(y, m, 1)
                ranges: List[Tuple[date, date]] = []
                start: Optional[date] = None
                prev: Optional[date] = None
                for m in months_active:
                    d0 = month_to_date(m)
                    if start is None:
                        start = d0
                        prev = d0
                    else:
                        if d0 == month_add(prev):
                            prev = d0
                        else:
                            # close previous range at end of month prev
                            end = month_add(prev)
                            ranges.append((start, end))
                            start = d0
                            prev = d0
                if start is not None and prev is not None:
                    end = month_add(prev)
                    ranges.append((start, end))
                for i, (s, e) in enumerate(ranges, 1):
                    lines.append(f"    section {author}")
                    lines.append(f"    {author} {i} : {s.isoformat()}, {e.isoformat()}")
            lines.append("```")
            lines.append("")

    # Highlights
    if daily:
        # longest streak overall
        streak_len, streak_start, streak_end = _longest_streak([datetime.fromisoformat(d+"T00:00:00").date() for d, *_ in daily])
        # best day by commits and by lines added
        best_day_commits = max(daily, key=lambda x: x[1])
        best_day_lines = max(daily, key=lambda x: x[2])
        lines.append("## Highlights")
        lines.append("")
        lines.append(f"- Longest active streak: {streak_len} days ({streak_start} to {streak_end})")
        lines.append(f"- Best day by commits: {best_day_commits[0]} — {best_day_commits[1]} commits")
        lines.append(f"- Best day by lines added: {best_day_lines[0]} — {best_day_lines[2]} lines")
        lines.append("")

    base.write_text("\n".join(lines) + "\n")


def write_reports(output_dir: Path, work_tree: Path, metrics: RepoMetrics, commits: List[CommitNumstat]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    repo_name = work_tree.name
    base = output_dir / f"{repo_name}_git_eval"

    # JSON
    curr_loc = _current_loc_snapshot(work_tree)
    payload = {
        "repo": work_tree.as_posix(),
        "metrics": asdict(metrics),
        "current_loc": {
            "lines": curr_loc[0],
            "files": curr_loc[1],
        },
        "effort_model": {
            "SESSION_GAP_MINUTES": int(os.getenv("SESSION_GAP_MINUTES", "90") or "90"),
            "MAX_HOURS_PER_DAY": float(os.getenv("MAX_HOURS_PER_DAY", "10") or "10"),
            "MIN_SESSION_MINUTES": float(os.getenv("MIN_SESSION_MINUTES", "30") or "30"),
            "MINUTES_PER_COMMIT_BASE": float(os.getenv("MINUTES_PER_COMMIT_BASE", "12") or "12"),
            "MINUTES_PER_100_LINES": float(os.getenv("MINUTES_PER_100_LINES", "8") or "8"),
            "MINUTES_PER_FILE": float(os.getenv("MINUTES_PER_FILE", "2") or "2"),
            "CALIBRATION_FACTOR": float(os.getenv("CALIBRATION_FACTOR", "1.5") or "1.5"),
        },
        "commits": [
            {
                "hash": c.hash,
                "author_name": c.author_name,
                "author_email": c.author_email,
                "author_date": c.author_date.isoformat(),
                "added": c.added,
                "deleted": c.deleted,
                "files_changed": c.files_changed,
                "is_merge": c.is_merge,
            }
            for c in commits
        ],
        "breakdowns": {
            "commits_by_author": _aggregate_by_author(commits)[0],
            "added_by_author": _aggregate_by_author(commits)[1],
            "deleted_by_author": _aggregate_by_author(commits)[2],
            "authors": _author_details(commits),
            "daily": [
                {"date": d, "commits": c, "added": a, "deleted": dl, "files": f}
                for (d, c, a, dl, f) in _aggregate_daily(commits)
            ],
            "monthly": [
                {"month": m, "commits": c, "added": a, "deleted": d, "files": f}
                for (m, c, a, d, f) in _aggregate_monthly(commits)
            ],
        },
    }
    (base.with_suffix(".json")).write_text(json.dumps(payload, indent=2))

    # CSV (summary)
    with (base.with_suffix(".csv")).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "repo_path","commits_total","merges_total","non_merges_total","unique_authors",
            "first_commit","last_commit","active_days","span_days","avg_commits_per_day",
            "added_lines_total","deleted_lines_total","files_changed_total","estimated_hours_total"
        ])
        w.writerow([
            work_tree.as_posix(), metrics.commits_total, metrics.merges_total, metrics.non_merges_total,
            metrics.unique_authors, metrics.first_commit, metrics.last_commit, metrics.active_days,
            metrics.span_days, metrics.avg_commits_per_day, metrics.added_lines_total,
            metrics.deleted_lines_total, metrics.files_changed_total, metrics.estimated_hours_total
        ])

    # TXT human-readable
    lines = []
    lines.append(f"Repo: {work_tree.as_posix()}")
    lines.append(f"Commits: total={metrics.commits_total}, merges={metrics.merges_total}, non-merges={metrics.non_merges_total}")
    lines.append(f"Authors: unique={metrics.unique_authors}")
    lines.append(f"Timeline: first={metrics.first_commit}, last={metrics.last_commit}")
    lines.append(f"Active days: {metrics.active_days}, span days: {metrics.span_days}, avg commits/day: {metrics.avg_commits_per_day}")
    lines.append(f"Numstat totals: added={metrics.added_lines_total}, deleted={metrics.deleted_lines_total}, files_changed={metrics.files_changed_total}")
    lines.append(f"Estimated hours (session-based): {metrics.estimated_hours_total}")
    (base.with_suffix(".txt")).write_text("\n".join(lines) + "\n")

    # Markdown visual report
    _write_markdown_report(output_dir, work_tree, metrics, commits)


def main(argv: Optional[List[str]] = None) -> int:
    load_dotenv()
    git_dir_input = os.getenv("GIT_EVAL_GIT_DIR", "").strip()
    output_dir = Path(os.getenv("OUTPUT_DIR", "./outputs")).resolve()
    include_merges = os.getenv("INCLUDE_MERGES", "1") not in {"0", "false", "False"}

    if not git_dir_input:
        print("GIT_EVAL_GIT_DIR is required in .env", file=sys.stderr)
        return 2

    input_path = Path(git_dir_input)
    try:
        work_tree, git_dir = resolve_git_dir(input_path)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    # Pull full history with numstat
    commits = parse_git_log_with_numstat(work_tree, include_merges=include_merges)

    metrics = compute_metrics(commits)
    metrics.repo_path = work_tree.as_posix()

    write_reports(output_dir, work_tree, metrics, commits)
    print(f"Reports written to {output_dir.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


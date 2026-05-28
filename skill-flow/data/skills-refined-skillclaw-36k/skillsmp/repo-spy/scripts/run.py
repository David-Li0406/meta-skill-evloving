#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "pyyaml"]
# ///
"""
Repository Monitor - Generic repo monitoring tool.

Tracks GitHub repositories for changes, releases, and breaking changes.
Also monitors official web sources: blog posts, release notes, YouTube videos.

Usage:
    uv run run.py                    # Scan all owners
    uv run run.py anthropics         # Scan specific owner
    uv run run.py --list-owners      # List available owners
    uv run run.py --json             # Output JSON to stdout
    uv run run.py --web-only         # Web sources only (skip git repos)
    uv run run.py --report           # Report only (no fetch)
    uv run run.py --fetch            # Fetch only (no report)
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import TypedDict
from urllib.parse import urlparse

import httpx
import yaml


class Highlight(TypedDict):
    type: str
    date: str
    summary: str


class RepoData(TypedDict):
    last_commit: str
    last_commit_date: str
    commits_30d: int
    highlights: list[Highlight]
    breaking_changes: list[str]
    new_features: list[str]
    hook_changes: list[str]
    fetch_error: str | None


class WebArticle(TypedDict):
    title: str
    url: str
    date: str | None
    summary: str | None


class WebSources(TypedDict):
    blog_posts: list[WebArticle]
    release_notes: list[WebArticle]
    youtube_videos: list[WebArticle]
    errors: list[str]


class Report(TypedDict):
    generated_at: str
    owner: str
    repos: dict[str, RepoData]
    web_sources: WebSources
    action_items: list[str]
    hook_alerts: list[str]


class RepoConfig(TypedDict, total=False):
    url: str
    priority: str
    hook_paths: list[str]


class OwnerConfig(TypedDict, total=False):
    repos: dict[str, RepoConfig]
    web_sources: dict[str, str | None]


class GlobalConfig(TypedDict, total=False):
    repos_path: str
    reports_path: str
    owners: dict[str, OwnerConfig]


# Config file location
CONFIG_FILE = Path("repo-spy.yml")

# Default paths (with {owner} placeholder)
DEFAULT_REPOS_PATH = ".data/repos/{owner}"
DEFAULT_REPORTS_PATH = ".data/reports/{owner}"

HTTP_TIMEOUT = 15
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RepoSpy/1.0)",
}


def load_config() -> GlobalConfig:
    """Load central config file."""
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config if config else {}
    except Exception as e:
        print(f"Warning: Failed to load config: {e}", file=sys.stderr)
        return {}


def get_path(config: GlobalConfig, key: str, owner: str) -> Path:
    """Get path from config with {owner} substitution."""
    defaults = {
        "repos_path": DEFAULT_REPOS_PATH,
        "reports_path": DEFAULT_REPORTS_PATH,
    }
    template = config.get(key, defaults.get(key, ""))
    return Path(template.replace("{owner}", owner))


def discover_owners(config: GlobalConfig) -> list[str]:
    """Get list of owners from config."""
    return list(config.get("owners", {}).keys())


def get_owner_config(config: GlobalConfig, owner: str) -> OwnerConfig:
    """Get config for a specific owner."""
    return config.get("owners", {}).get(owner, {})


def get_owner_repos_dir(config: GlobalConfig, owner: str) -> Path:
    """Get the repos directory for an owner."""
    return get_path(config, "repos_path", owner)


def get_owner_reports_dir(config: GlobalConfig, owner: str) -> Path:
    """Get the reports directory for an owner."""
    return get_path(config, "reports_path", owner)


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    """Run git command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def ensure_repos_cloned(
    repos_config: dict[str, RepoConfig], repos_path: Path
) -> None:
    """Clone missing repos."""
    repos_path.mkdir(parents=True, exist_ok=True)
    for name, repo_info in repos_config.items():
        repo_dir = repos_path / name
        if not repo_dir.exists():
            url = repo_info.get("url") if isinstance(repo_info, dict) else repo_info
            if url:
                print(f"Cloning {name}...", file=sys.stderr)
                code, _, err = run_git(["clone", url, name], repos_path)
                if code != 0:
                    print(f"  Failed to clone {name}: {err}", file=sys.stderr)


def discover_repos(repos_path: Path) -> list[str]:
    """Discover available repos in a directory."""
    if not repos_path.exists():
        return []
    return [
        d.name
        for d in repos_path.iterdir()
        if d.is_dir() and (d / ".git").exists()
    ]


def fetch_blog_posts(
    blog_url: str | None, months: int = 3
) -> tuple[list[WebArticle], str | None]:
    """Fetch recent blog posts from a news page."""
    if not blog_url:
        return [], None

    posts: list[WebArticle] = []
    try:
        resp = httpx.get(
            blog_url,
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
            follow_redirects=True,
        )
        resp.raise_for_status()
        html = resp.text

        # Extract article links and titles from news page
        # Pattern matches common news page structure
        pattern = r'<a[^>]*href="(/news/[^"]+)"[^>]*>.*?<h\d[^>]*>([^<]+)</h\d>'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

        # Also try alternate pattern
        if not matches:
            pattern = r'href="(/news/[^"]+)"[^>]*>\s*([^<]+)\s*</a>'
            matches = re.findall(pattern, html, re.IGNORECASE)

        # Parse base URL for constructing full URLs
        parsed = urlparse(blog_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        for path, title in matches[:20]:  # Limit to 20
            title = title.strip()
            if not title or len(title) < 5:
                continue
            url = f"{base_url}{path}"
            posts.append({
                "title": title,
                "url": url,
                "date": None,
                "summary": None,
            })

        return posts[:10], None  # Return top 10
    except Exception as e:
        return [], str(e)


def fetch_release_notes(
    docs_url: str | None,
) -> tuple[list[WebArticle], str | None]:
    """Fetch release notes from docs page."""
    if not docs_url:
        return [], None

    notes: list[WebArticle] = []
    try:
        resp = httpx.get(
            docs_url,
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
            follow_redirects=True,
        )
        resp.raise_for_status()
        html = resp.text

        # Parse base URL
        parsed = urlparse(docs_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        # Extract release note links
        pattern = r'href="(/en/release-notes/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html, re.IGNORECASE)

        for path, title in matches[:15]:
            title = title.strip()
            if not title:
                continue
            url = f"{base_url}{path}"
            # Try to extract date from title (e.g., "January 2026")
            date_match = re.search(r"(\w+ \d{4})", title)
            notes.append({
                "title": title,
                "url": url,
                "date": date_match.group(1) if date_match else None,
                "summary": None,
            })

        return notes[:10], None
    except Exception as e:
        return [], str(e)


def fetch_youtube_videos(
    rss_url: str | None,
) -> tuple[list[WebArticle], str | None]:
    """Fetch recent videos from YouTube channel via RSS."""
    if not rss_url:
        return [], None

    videos: list[WebArticle] = []
    try:
        resp = httpx.get(
            rss_url,
            headers=HTTP_HEADERS,
            timeout=HTTP_TIMEOUT,
            follow_redirects=True,
        )
        resp.raise_for_status()
        xml = resp.text

        # Parse RSS feed entries
        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)

        for entry in entries[:10]:
            video_id = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", entry)
            title = re.search(r"<title>([^<]+)</title>", entry)
            published = re.search(r"<published>([^<]+)</published>", entry)

            if video_id and title:
                videos.append({
                    "title": title.group(1),
                    "url": f"https://www.youtube.com/watch?v={video_id.group(1)}",
                    "date": published.group(1)[:10] if published else None,
                    "summary": None,
                })

        return videos, None
    except Exception as e:
        return [], str(e)


def fetch_web_sources(owner_config: OwnerConfig) -> WebSources:
    """Fetch all web sources for an owner."""
    web_sources = owner_config.get("web_sources", {})

    blog_url = web_sources.get("blog")
    docs_url = web_sources.get("docs_changelog")
    youtube_url = web_sources.get("youtube_rss")

    blog_posts, blog_err = fetch_blog_posts(blog_url)
    release_notes, notes_err = fetch_release_notes(docs_url)
    youtube_videos, yt_err = fetch_youtube_videos(youtube_url)

    errors = []
    if blog_err:
        errors.append(f"blog: {blog_err}")
    if notes_err:
        errors.append(f"release_notes: {notes_err}")
    if yt_err:
        errors.append(f"youtube: {yt_err}")

    return {
        "blog_posts": blog_posts,
        "release_notes": release_notes,
        "youtube_videos": youtube_videos,
        "errors": errors,
    }


def fetch_repo(repo_path: Path) -> str | None:
    """Fetch latest from remote. Returns error message or None on success."""
    code, _, err = run_git(["fetch", "--all", "--quiet"], repo_path)
    if code != 0:
        return err or "fetch failed"
    return None


def get_last_commit(repo_path: Path) -> tuple[str, str]:
    """Get last commit hash and date."""
    code, out, _ = run_git(
        ["log", "-1", "--format=%H|%ci"],
        repo_path,
    )
    if code == 0 and "|" in out:
        parts = out.split("|", 1)
        return parts[0][:7], parts[1][:10]
    return "unknown", "unknown"


def get_commits_since(repo_path: Path, days: int) -> list[dict]:
    """Get commits from last N days."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    code, out, _ = run_git(
        ["log", f"--since={since}", "--format=%H|%ci|%s", "--all"],
        repo_path,
    )
    if code != 0 or not out:
        return []

    commits = []
    for line in out.splitlines():
        parts = line.split("|", 2)
        if len(parts) >= 3:
            commits.append({
                "hash": parts[0][:7],
                "date": parts[1][:10],
                "subject": parts[2],
            })
    return commits


def check_hook_changes(
    repo_path: Path, hook_paths: list[str], days: int
) -> list[str]:
    """Check for changes in monitored hook paths."""
    changes: list[str] = []

    for hook_path in hook_paths:
        code, out, _ = run_git(
            ["log", f"--since={days} days ago", "--oneline", "--", hook_path],
            repo_path,
        )
        if code == 0 and out.strip():
            for line in out.strip().splitlines()[:5]:  # Limit to 5 most recent
                changes.append(f"[{hook_path}] {line}")

    # Check for CHANGELOG entries mentioning hooks
    changelog = repo_path / "CHANGELOG.md"
    if changelog.exists():
        try:
            content = changelog.read_text(encoding="utf-8")
            # Look for hook mentions in recent entries (crude heuristic)
            for line in content.splitlines():
                if "hook" in line.lower() and any(c in line for c in ["#", "-", "*"]):
                    changes.append(f"[CHANGELOG] {line.strip()}")
                    if len(changes) > 10:
                        break
        except Exception:
            pass

    return changes


def analyze_commits(
    commits: list[dict],
) -> tuple[list[Highlight], list[str], list[str], list[str]]:
    """Analyze commits for highlights, breaking changes, features, and hook changes."""
    highlights: list[Highlight] = []
    breaking: list[str] = []
    features: list[str] = []
    hooks: list[str] = []

    keywords = {
        "release": "release",
        "breaking": "breaking",
        "feat:": "feature",
        "feat(": "feature",
        "fix:": "fix",
        "fix(": "fix",
        "hook": "hook",
    }

    for commit in commits:
        subject_lower = commit["subject"].lower()

        for keyword, highlight_type in keywords.items():
            if keyword in subject_lower:
                highlights.append({
                    "type": highlight_type,
                    "date": commit["date"],
                    "summary": commit["subject"],
                })

                if highlight_type == "breaking" or "breaking" in subject_lower:
                    breaking.append(f"{commit['date']}: {commit['subject']}")
                elif highlight_type == "feature":
                    features.append(f"{commit['date']}: {commit['subject']}")
                elif highlight_type == "hook":
                    hooks.append(f"{commit['date']}: {commit['subject']}")
                break

    return highlights, breaking, features, hooks


def analyze_repo(
    repo_name: str,
    repo_path: Path,
    hook_paths: list[str],
    do_fetch: bool = True,
) -> RepoData:
    """Analyze a single repository."""
    data: RepoData = {
        "last_commit": "unknown",
        "last_commit_date": "unknown",
        "commits_30d": 0,
        "highlights": [],
        "breaking_changes": [],
        "new_features": [],
        "hook_changes": [],
        "fetch_error": None,
    }

    if not repo_path.exists():
        data["fetch_error"] = "repo not found"
        return data

    if do_fetch:
        err = fetch_repo(repo_path)
        if err:
            data["fetch_error"] = err

    data["last_commit"], data["last_commit_date"] = get_last_commit(repo_path)

    commits = get_commits_since(repo_path, 30)
    data["commits_30d"] = len(commits)

    highlights, breaking, features, hooks = analyze_commits(commits)
    data["highlights"] = highlights
    data["breaking_changes"] = breaking
    data["new_features"] = features
    data["hook_changes"] = hooks

    # Deep hook monitoring if configured
    if hook_paths:
        deep_hooks = check_hook_changes(repo_path, hook_paths, 30)
        data["hook_changes"].extend(deep_hooks)

    return data


def generate_report(
    owner: str,
    repos_data: dict[str, RepoData],
    owner_config: OwnerConfig,
    web_sources: WebSources | None = None,
) -> Report:
    """Generate full report structure."""
    repos_config = owner_config.get("repos", {})
    action_items: list[str] = []
    hook_alerts: list[str] = []

    for repo_name, data in repos_data.items():
        repo_cfg = repos_config.get(repo_name, {})
        priority = repo_cfg.get("priority", "LOW") if isinstance(repo_cfg, dict) else "LOW"

        # Flag breaking changes as action items
        for change in data["breaking_changes"]:
            action_items.append(f"[{priority}] {repo_name}: {change}")

        # Flag hook changes
        for hook in data["hook_changes"]:
            hook_alerts.append(f"{repo_name}: {hook}")

        # Flag fetch errors for HIGH priority repos
        if data["fetch_error"] and priority == "HIGH":
            action_items.append(
                f"[{priority}] {repo_name}: fetch failed - {data['fetch_error']}"
            )

    if web_sources is None:
        web_sources = {
            "blog_posts": [],
            "release_notes": [],
            "youtube_videos": [],
            "errors": [],
        }

    return {
        "generated_at": datetime.now(UTC).isoformat() + "Z",
        "owner": owner,
        "repos": repos_data,
        "web_sources": web_sources,
        "action_items": action_items,
        "hook_alerts": hook_alerts,
    }


def format_markdown(report: Report, owner_config: OwnerConfig) -> str:
    """Format report as Markdown."""
    repos_config = owner_config.get("repos", {})
    owner = report.get("owner", "unknown")

    lines = [
        f"# Repository Monitor Report: {owner}",
        "",
        f"**Generated:** {report['generated_at']}",
        "",
    ]

    # Action items
    if report["action_items"]:
        lines.extend(["## Action Items", ""])
        for item in report["action_items"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    # Hook alerts
    if report["hook_alerts"]:
        lines.extend(["## Hook Alerts", ""])
        for alert in report["hook_alerts"]:
            lines.append(f"- {alert}")
        lines.append("")

    # Web sources
    web = report.get("web_sources", {})
    if web.get("blog_posts") or web.get("release_notes") or web.get("youtube_videos"):
        lines.extend(["## Official Web Sources", ""])

        if web.get("blog_posts"):
            lines.extend(["### Recent Blog Posts", ""])
            for post in web["blog_posts"]:
                date_str = f" ({post['date']})" if post.get("date") else ""
                lines.append(f"- [{post['title']}]({post['url']}){date_str}")
            lines.append("")

        if web.get("release_notes"):
            lines.extend(["### Release Notes", ""])
            for note in web["release_notes"]:
                date_str = f" ({note['date']})" if note.get("date") else ""
                lines.append(f"- [{note['title']}]({note['url']}){date_str}")
            lines.append("")

        if web.get("youtube_videos"):
            lines.extend(["### YouTube Videos", ""])
            for video in web["youtube_videos"]:
                lines.append(f"- [{video['title']}]({video['url']})")
            lines.append("")

        if web.get("errors"):
            lines.extend(["### Web Fetch Errors", ""])
            for err in web["errors"]:
                lines.append(f"- {err}")
            lines.append("")

    # Build priority map from repos config
    def get_priority(repo_name: str) -> str:
        repo_cfg = repos_config.get(repo_name, {})
        return repo_cfg.get("priority", "LOW") if isinstance(repo_cfg, dict) else "LOW"

    # Group repos by priority
    for priority in ["HIGH", "MEDIUM", "LOW"]:
        priority_repos = [
            (n, d)
            for n, d in report["repos"].items()
            if get_priority(n) == priority
        ]
        if not priority_repos:
            continue

        lines.extend([f"## {priority} Priority Repos", ""])

        for repo_name, data in sorted(priority_repos):
            lines.extend([
                f"### {repo_name}",
                "",
                f"- **Last Commit:** {data['last_commit']} ({data['last_commit_date']})",
                f"- **Activity:** {data['commits_30d']} commits in 30 days",
            ])

            if data["fetch_error"]:
                lines.append(f"- **Error:** {data['fetch_error']}")

            if data["breaking_changes"]:
                lines.append(f"- **Breaking Changes:** {len(data['breaking_changes'])}")
                for change in data["breaking_changes"]:
                    lines.append(f"  - {change}")

            if data["new_features"]:
                lines.append(f"- **New Features:** {len(data['new_features'])}")
                for feature in data["new_features"]:
                    lines.append(f"  - {feature}")

            lines.append("")

    return "\n".join(lines)


def save_reports(
    config: GlobalConfig,
    owner: str,
    report: Report,
    owner_config: OwnerConfig,
) -> tuple[Path, Path]:
    """Save JSON and Markdown reports."""
    data_dir = get_owner_reports_dir(config, owner)
    history_dir = data_dir / "history"

    data_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    json_path = data_dir / "latest.json"
    md_path = data_dir / "latest.md"

    # Save latest
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(format_markdown(report, owner_config))

    # Archive with date
    date_str = datetime.now().strftime("%Y%m%d")
    history_json = history_dir / f"{date_str}.json"
    history_md = history_dir / f"{date_str}.md"

    with open(history_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open(history_md, "w", encoding="utf-8") as f:
        f.write(format_markdown(report, owner_config))

    # Update sentinel
    sentinel_file = data_dir / ".last_check"
    with open(sentinel_file, "w", encoding="utf-8") as f:
        f.write(datetime.now(UTC).isoformat() + "Z\n")

    return json_path, md_path


def process_owner(
    config: GlobalConfig,
    owner: str,
    do_fetch: bool = True,
    do_report: bool = True,
    json_output: bool = False,
    web_only: bool = False,
) -> int:
    """Process a single owner's repositories."""
    owner_config = get_owner_config(config, owner)
    repos_config = owner_config.get("repos", {})

    repos_data: dict[str, RepoData] = {}
    web_sources: WebSources | None = None

    # Git repos (unless --web-only)
    if not web_only:
        repos_dir = get_owner_repos_dir(config, owner)

        # Auto-clone missing repos
        if repos_config:
            ensure_repos_cloned(repos_config, repos_dir)

        available = discover_repos(repos_dir)
        if not available:
            print(f"Warning: no repos found at {repos_dir}", file=sys.stderr)
        else:
            for repo_name in available:
                repo_path = repos_dir / repo_name
                repo_cfg = repos_config.get(repo_name, {})
                hook_paths = repo_cfg.get("hook_paths", []) if isinstance(repo_cfg, dict) else []
                repos_data[repo_name] = analyze_repo(
                    repo_name, repo_path, hook_paths, do_fetch
                )

    # Fetch web sources
    if owner_config.get("web_sources"):
        print(f"Fetching web sources for {owner}...", file=sys.stderr)
        web_sources = fetch_web_sources(owner_config)

    # Generate report
    report = generate_report(owner, repos_data, owner_config, web_sources)

    if json_output:
        print(json.dumps(report, indent=2))
        return 0

    if do_report:
        json_path, md_path = save_reports(config, owner, report, owner_config)
        print(f"Reports saved for {owner}:")
        print(f"  JSON: {json_path}")
        print(f"  Markdown: {md_path}")

        # Summary
        total_commits = sum(d["commits_30d"] for d in repos_data.values())
        total_breaking = sum(len(d["breaking_changes"]) for d in repos_data.values())

        if repos_data:
            print(
                f"\nRepos: {len(repos_data)} repos, {total_commits} commits (30d), {total_breaking} breaking changes"
            )

        # Web summary
        web = report.get("web_sources", {})
        blog_count = len(web.get("blog_posts", []))
        notes_count = len(web.get("release_notes", []))
        video_count = len(web.get("youtube_videos", []))
        print(f"Web: {blog_count} blog posts, {notes_count} release notes, {video_count} videos")

        if web.get("errors"):
            print(f"Web errors: {', '.join(web['errors'])}")

        if report["action_items"]:
            print(f"\nAction items ({len(report['action_items'])}):")
            for item in report["action_items"]:
                print(f"  - {item}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor GitHub repositories and web sources for updates."
    )
    parser.add_argument(
        "owner",
        nargs="?",
        help="Owner to scan (e.g., anthropics). If not specified, scans all owners.",
    )
    parser.add_argument(
        "--list-owners",
        action="store_true",
        help="List available owners and exit.",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch only (no report).",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Report only (no fetch).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON to stdout.",
    )
    parser.add_argument(
        "--web-only",
        action="store_true",
        help="Web sources only (skip git repos).",
    )

    args = parser.parse_args()

    # Load central config
    config = load_config()

    # List owners mode
    if args.list_owners:
        owners = discover_owners(config)
        if not owners:
            print("No owners found in config", file=sys.stderr)
            return 1
        print("Available owners:")
        for owner in sorted(owners):
            print(f"  {owner}")
        return 0

    do_fetch = not args.report
    do_report = not args.fetch

    # Process specific owner or all owners
    if args.owner:
        owners = [args.owner]
        if args.owner not in discover_owners(config):
            print(f"Error: owner '{args.owner}' not found in config", file=sys.stderr)
            return 1
    else:
        owners = discover_owners(config)
        if not owners:
            print("No owners found in config", file=sys.stderr)
            return 1

    for owner in owners:
        print(f"\n=== Processing {owner} ===", file=sys.stderr)
        result = process_owner(
            config,
            owner,
            do_fetch=do_fetch,
            do_report=do_report,
            json_output=args.json,
            web_only=args.web_only,
        )
        if result != 0:
            return result

    return 0


if __name__ == "__main__":
    sys.exit(main())

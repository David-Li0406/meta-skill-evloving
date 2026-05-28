#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["typer", "rich"]
# ///
"""
ai-blame: Show AI conversation context for git commits.
"""

import bisect
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text


# --- Data Model ---


@dataclass
class Interaction:
    """A user prompt with its context from session logs."""

    timestamp: float  # Unix epoch
    session_id: str
    prompt: str  # User message content
    explicit_hashes: list[str] = field(default_factory=list)  # From tool_result
    files_edited: set[str] = field(default_factory=set)  # From Edit/Write calls


@dataclass
class BlameIndex:
    """Pre-computed lookup structures."""

    hash_map: dict[str, Interaction] = field(default_factory=dict)  # short_hash → Interaction
    timeline: list[tuple[float, Interaction]] = field(default_factory=list)  # sorted by timestamp
    timeline_keys: list[float] = field(default_factory=list)  # for bisect


# Regex to extract commit hash from git commit output: [branch hash]
COMMIT_HASH_PATTERN = re.compile(r"\[[\w\-/]+ ([0-9a-f]{7,})\]")


def find_all_session_files(project_dir: Optional[str] = None) -> list[Path]:
    """Find all session JSONL files for the project."""
    claude_dir = Path.home() / ".claude" / "projects"

    if project_dir is None:
        project_dir = get_project_dir()

    project_path = claude_dir / project_dir
    if not project_path.exists():
        return []

    return sorted(
        [f for f in project_path.glob("*.jsonl") if not f.stem.startswith("agent-")],
        key=lambda f: f.stat().st_mtime,
    )


def extract_hashes_from_entry(entry: dict) -> list[str]:
    """Extract commit hashes from a session entry (tool_result after git commit)."""
    hashes = []

    # Check toolUseResult.stdout
    tool_result = entry.get("toolUseResult", {})
    if isinstance(tool_result, dict):
        stdout = tool_result.get("stdout", "")
        if stdout and isinstance(stdout, str):
            for match in COMMIT_HASH_PATTERN.finditer(stdout):
                hashes.append(match.group(1))
    elif isinstance(tool_result, str):
        for match in COMMIT_HASH_PATTERN.finditer(tool_result):
            hashes.append(match.group(1))

    # Also check message.content for tool_result blocks
    message = entry.get("message", {})
    content = message.get("content", [])
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "tool_result":
                result_content = item.get("content", "")
                if isinstance(result_content, str):
                    for match in COMMIT_HASH_PATTERN.finditer(result_content):
                        hashes.append(match.group(1))

    return hashes


def extract_prompt_text(entry: dict) -> Optional[str]:
    """Extract user prompt text from a session entry."""
    message = entry.get("message", {})
    content = message.get("content", "")

    if isinstance(content, str):
        if content.startswith("<command-message>"):
            return None
        return content.strip() if content.strip() else None

    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                # Skip system markers
                if not text.startswith("#") and not text.startswith("<"):
                    texts.append(text)
        return "\n".join(texts).strip() if texts else None

    return None


def build_index(session_files: list[Path]) -> BlameIndex:
    """Join all sessions, build lookup structures."""
    hash_map: dict[str, Interaction] = {}
    timeline: list[tuple[float, Interaction]] = []

    current_interaction: Optional[Interaction] = None

    for session_file in session_files:
        session_id = session_file.stem

        try:
            with open(session_file, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    entry_type = entry.get("type")
                    user_type = entry.get("userType")
                    timestamp_str = entry.get("timestamp", "")

                    # Parse timestamp
                    try:
                        ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        timestamp = ts.timestamp()
                    except (ValueError, AttributeError):
                        continue

                    # User prompt starts a new interaction
                    if entry_type == "user" and user_type == "external":
                        prompt_text = extract_prompt_text(entry)
                        if prompt_text:
                            current_interaction = Interaction(
                                timestamp=timestamp,
                                session_id=session_id,
                                prompt=prompt_text,
                                explicit_hashes=[],
                                files_edited=set(),
                            )
                            timeline.append((timestamp, current_interaction))

                    # Assistant response - extract file paths and commit hashes
                    elif entry_type == "assistant" and current_interaction:
                        # Extract file paths from Edit/Write
                        message = entry.get("message", {})
                        content = message.get("content", [])
                        if isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get("type") == "tool_use":
                                    tool_name = item.get("name", "")
                                    if tool_name in ("Edit", "Write"):
                                        file_path = item.get("input", {}).get("file_path", "")
                                        if file_path:
                                            current_interaction.files_edited.add(file_path)

                    # Tool result - extract commit hashes
                    hashes = extract_hashes_from_entry(entry)
                    if hashes and current_interaction:
                        for h in hashes:
                            current_interaction.explicit_hashes.append(h)
                            hash_map[h] = current_interaction

        except (IOError, OSError):
            continue

    # Sort timeline and extract keys for bisect
    timeline.sort(key=lambda x: x[0])
    timeline_keys = [t for t, _ in timeline]

    return BlameIndex(hash_map=hash_map, timeline=timeline, timeline_keys=timeline_keys)


class BlameResolver:
    """Resolves commits to interactions using priority-based strategy chain."""

    def __init__(self, index: BlameIndex):
        self.index = index
        # Priority defined by order - first match wins
        self.strategies = [
            self.match_by_hash,  # Priority 1: Direct hash (100% certain)
            self.match_by_window,  # Priority 2: Time window (high confidence)
        ]

    def resolve(self, commit_hash: str, commit_timestamp: float) -> tuple[Optional[Interaction], str]:
        """Resolve commit to interaction. Returns (interaction, method_name)."""
        for strategy in self.strategies:
            result = strategy(commit_hash, commit_timestamp)
            if result:
                return result, strategy.__name__
        return None, "none"

    def match_by_hash(self, commit_hash: str, commit_timestamp: float) -> Optional[Interaction]:
        """O(1) lookup - direct hash from session logs."""
        # Try both short (7 char) and full hash
        short_hash = commit_hash[:7]
        return self.index.hash_map.get(short_hash) or self.index.hash_map.get(commit_hash)

    def match_by_window(self, commit_hash: str, commit_timestamp: float) -> Optional[Interaction]:
        """O(log n) lookup - prompt immediately before commit."""
        if not self.index.timeline_keys:
            return None

        idx = bisect.bisect_right(self.index.timeline_keys, commit_timestamp)

        if idx == 0:
            return None

        prompt_time, interaction = self.index.timeline[idx - 1]
        delta = commit_timestamp - prompt_time

        # Prompt must be before commit, within 5 minutes
        if 0 <= delta <= 300:
            return interaction
        return None


app = typer.Typer(
    name="ai-blame",
    help="Show AI conversation context for git commits.",
    add_completion=False,
)
console = Console()


def get_commit_session_id(commit: str) -> Optional[str]:
    """Extract AI-Session-ID from commit message."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B", commit],
            capture_output=True, text=True, check=True,
        )
        match = re.search(r"AI-Session-ID:\s*([a-f0-9-]+)", result.stdout)
        return match.group(1) if match else None
    except subprocess.CalledProcessError:
        return None


def get_project_dir() -> str:
    """Get encoded project directory name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        project_path = result.stdout.strip()
    except subprocess.CalledProcessError:
        project_path = os.getcwd()
    return project_path.replace("/", "-").replace("_", "-")


def find_session_file(session_id: str) -> Optional[Path]:
    """Find the session JSONL file."""
    claude_dir = Path.home() / ".claude" / "projects"
    project_dir = get_project_dir()
    session_file = claude_dir / project_dir / f"{session_id}.jsonl"
    if session_file.exists():
        return session_file
    for proj_dir in claude_dir.iterdir():
        if proj_dir.is_dir():
            candidate = proj_dir / f"{session_id}.jsonl"
            if candidate.exists():
                return candidate
    return None


def get_commit_info(commit: str) -> dict:
    """Get commit metadata."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H%n%s%n%an%n%aI", commit],
            capture_output=True, text=True, check=True,
        )
        lines = result.stdout.strip().split("\n")
        return {"hash": lines[0], "subject": lines[1], "author": lines[2], "date": lines[3]}
    except subprocess.CalledProcessError:
        return {}


def get_commit_timestamp(commit: str) -> Optional[datetime]:
    """Get commit timestamp as datetime."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", commit],
            capture_output=True, text=True, check=True,
        )
        return datetime.fromisoformat(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return None


def get_previous_commit(commit: str) -> Optional[str]:
    """Get the previous commit hash, or None if first commit."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", f"{commit}^"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def parse_timestamp(ts: str) -> Optional[datetime]:
    """Parse ISO timestamp string to datetime."""
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def get_commit_stats(commit: str) -> dict:
    """Get file change statistics."""
    try:
        result = subprocess.run(
            ["git", "diff", "--numstat", f"{commit}^..{commit}"],
            capture_output=True, text=True, check=True,
        )
        stats = {}
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 3:
                    added = int(parts[0]) if parts[0] != "-" else 0
                    deleted = int(parts[1]) if parts[1] != "-" else 0
                    stats[parts[2]] = {"added": added, "deleted": deleted}
        return stats
    except subprocess.CalledProcessError:
        return {}


def extract_user_content(message: dict) -> Optional[str]:
    """Extract readable content from user message."""
    content = message.get("content", "")
    if isinstance(content, str):
        if content.startswith("<command-message>"):
            return None
        return content.strip() if content.strip() else None
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if not text.startswith("#"):
                    texts.append(text)
        return "\n".join(texts).strip() if texts else None
    return None


def extract_assistant_content(message: dict) -> list:
    """Extract content from assistant message."""
    content = message.get("content", [])
    results = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    results.append({"type": "text", "content": item.get("text", "")})
                elif item.get("type") == "tool_use":
                    results.append({
                        "type": "tool",
                        "name": item.get("name", ""),
                        "input": item.get("input", {}),
                    })
    return results


def parse_session(session_file: Path, include_responses: bool = False) -> list:
    """Parse session file and extract conversation."""
    messages = []
    with open(session_file, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            is_meta = entry.get("isMeta", False)
            user_type = entry.get("userType")
            timestamp = entry.get("timestamp", "")

            if entry_type == "user" and user_type == "external" and not is_meta:
                msg = entry.get("message", {})
                content = extract_user_content(msg)
                if content:
                    messages.append({
                        "type": "prompt",
                        "content": content,
                        "timestamp": timestamp,
                        "files_changed": [],
                    })

            elif entry_type == "assistant":
                msg = entry.get("message", {})
                assistant_content = extract_assistant_content(msg)
                for item in assistant_content:
                    if item["type"] == "tool" and item["name"] in ("Edit", "Write"):
                        file_path = item["input"].get("file_path", "")
                        if file_path and messages and messages[-1]["type"] == "prompt":
                            try:
                                rel_path = os.path.relpath(file_path)
                            except ValueError:
                                rel_path = file_path
                            if rel_path not in messages[-1]["files_changed"]:
                                messages[-1]["files_changed"].append(rel_path)

                if include_responses:
                    texts = [i["content"] for i in assistant_content if i["type"] == "text" and i["content"].strip()]
                    if texts:
                        messages.append({"type": "response", "content": "\n".join(texts), "timestamp": timestamp})
    return messages


def format_time(ts: str) -> str:
    """Format timestamp to HH:MM."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except (ValueError, AttributeError):
        return ts[:5] if ts else ""


def format_diff(added: int, deleted: int) -> Text:
    """Format diff stats with colors."""
    t = Text()
    t.append(f"+{added}", style="bold green")
    t.append(" ", style="white")
    t.append(f"-{deleted}", style="bold red")
    return t


def format_timestamp_from_epoch(ts: float) -> str:
    """Format Unix epoch timestamp to HH:MM."""
    try:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%H:%M")
    except (ValueError, OSError):
        return ""


@app.command()
def blame(
    commit: str = typer.Argument("HEAD", help="Commit hash or reference"),
    responses: bool = typer.Option(False, "--responses", "-r", help="Include AI responses"),
    all_prompts: bool = typer.Option(False, "--all", "-a", help="Show all prompts from session, not just time-windowed"),
    project_dir: Optional[str] = typer.Option(None, "--project", "-p", help="Override project directory (encoded path)"),
):
    """Show AI conversation context for a git commit."""
    commit_info = get_commit_info(commit)
    if not commit_info:
        console.print(f"[red]Error:[/red] Commit not found: {commit}")
        raise typer.Exit(1)

    commit_stats = get_commit_stats(commit)
    commit_time = get_commit_timestamp(commit)
    commit_timestamp = commit_time.timestamp() if commit_time else 0.0

    # Try strategy-based resolution first (works without AI-Session-ID)
    session_files = find_all_session_files(project_dir)
    interaction: Optional[Interaction] = None
    match_method = "none"

    if session_files:
        index = build_index(session_files)
        resolver = BlameResolver(index)
        interaction, match_method = resolver.resolve(commit_info["hash"], commit_timestamp)

    # Fallback: Try session ID from commit message (old approach)
    session_id = get_commit_session_id(commit)
    session_file: Optional[Path] = None
    messages: list = []

    if session_id:
        session_file = find_session_file(session_id)
        if session_file:
            messages = parse_session(session_file, responses)

    # If no interaction found and no session file, show error
    if not interaction and not session_file:
        console.print(f"[yellow]No AI context found for commit {commit_info['hash'][:8]}[/yellow]")
        console.print(Text("No session files available or commit not in session logs.", style="dim"))
        raise typer.Exit(1)

    # Header: compact single line
    header = Text()
    header.append(commit_info['hash'][:8], style="bold yellow")
    header.append(" ", style="white")
    header.append(commit_info['subject'], style="bold white")
    header.append(" • ", style="dim")
    header.append(commit_info['author'], style="cyan")
    header.append(f" ({commit_info['date'][:10]})", style="dim")
    console.print(header)

    # Show session/match info
    if interaction:
        match_label = "hash" if match_method == "match_by_hash" else "time"
        console.print(Text(f"Session: {interaction.session_id} (matched by {match_label})", style="dim"))
    elif session_id:
        console.print(Text(f"Session: {session_id}", style="dim"))
    console.print()

    # Files table: compact, no borders
    if commit_stats:
        file_table = Table(box=None, padding=(0, 1), show_header=False, pad_edge=False)
        file_table.add_column("File", style="white")
        file_table.add_column("Diff", justify="right")

        total_add, total_del = 0, 0
        for fname, stats in sorted(commit_stats.items()):
            file_table.add_row(fname, format_diff(stats["added"], stats["deleted"]))
            total_add += stats["added"]
            total_del += stats["deleted"]

        console.print(file_table)

        total = Text()
        total.append("Total: ", style="dim")
        total.append_text(format_diff(total_add, total_del))
        console.print(total)
        console.print()

    # Prompts section
    console.print(Text("Prompts", style="bold underline"))
    console.print()

    prompt_num = 0

    # If we have a direct interaction match, show it
    if interaction:
        prompt_num = 1
        time_str = format_timestamp_from_epoch(interaction.timestamp)

        # Header line: number and time
        pheader = Text()
        pheader.append(f"#{prompt_num}", style="dim")
        pheader.append(f" {time_str}", style="dim cyan")
        console.print(pheader)

        # Content: plain text
        console.print(Text(interaction.prompt, style="white"))

        # Files edited (only those in this commit)
        if interaction.files_edited:
            for f in interaction.files_edited:
                try:
                    rel_path = os.path.relpath(f)
                except ValueError:
                    rel_path = f
                if rel_path in commit_stats:
                    file_line = Text()
                    file_line.append("→ ", style="dim")
                    file_line.append(rel_path, style="bold yellow")
                    s = commit_stats[rel_path]
                    file_line.append(f" +{s['added']}", style="bold green")
                    file_line.append(f" -{s['deleted']}", style="bold red")
                    console.print(file_line)

        console.print()
        source = f"1 prompt • {interaction.session_id}"

    # Otherwise, use session-based parsing (old approach)
    elif messages:
        prev_commit = get_previous_commit(commit)
        prev_time = get_commit_timestamp(prev_commit) if prev_commit else None

        for msg in messages:
            if msg["type"] == "prompt":
                # Time-based filtering: show prompts between previous commit and this commit
                if not all_prompts and commit_time:
                    msg_time = parse_timestamp(msg["timestamp"])
                    if msg_time:
                        # Skip if after this commit
                        if msg_time > commit_time:
                            continue
                        # Skip if before or at previous commit time
                        if prev_time and msg_time <= prev_time:
                            continue

                prompt_num += 1
                time_str = format_time(msg["timestamp"])

                # Header line: number and time
                pheader = Text()
                pheader.append(f"#{prompt_num}", style="dim")
                pheader.append(f" {time_str}", style="dim cyan")
                console.print(pheader)

                # Content: plain text, no markup interpretation
                console.print(Text(msg["content"], style="white"))

                # Files changed (only those in this commit, for reference)
                files = [f for f in msg.get("files_changed", []) if f in commit_stats]
                if files:
                    for f in files:
                        file_line = Text()
                        file_line.append("→ ", style="dim")
                        file_line.append(f, style="bold yellow")
                        s = commit_stats[f]
                        file_line.append(f" +{s['added']}", style="bold green")
                        file_line.append(f" -{s['deleted']}", style="bold red")
                        console.print(file_line)

                console.print()

            elif msg["type"] == "response" and responses:
                time_str = format_time(msg["timestamp"])
                console.print(Text(f"↳ AI {time_str}", style="dim magenta"))
                console.print(Text(msg["content"], style="dim"))
                console.print()

        source = f"{prompt_num} prompts • {session_file}"
    else:
        source = "No prompts found"

    console.print(Text(source, style="dim"))


@app.command()
def session_info():
    """Output current session ID and Claude version for commits."""
    claude_dir = Path.home() / ".claude" / "projects"
    project_path = claude_dir / get_project_dir()

    session_id = None
    session_file = None
    model = "unknown"

    if project_path.exists():
        sessions = [(f.stat().st_mtime, f) for f in project_path.glob("*.jsonl") if not f.stem.startswith("agent-")]
        if sessions:
            sessions.sort(reverse=True)
            session_file = sessions[0][1]
            session_id = session_file.stem

            # Get model from session file
            with open(session_file, "r") as f:
                for line in f:
                    if '"model":' in line:
                        try:
                            entry = json.loads(line)
                            msg = entry.get("message", {})
                            if "model" in msg:
                                model = msg["model"]
                                break
                        except json.JSONDecodeError:
                            continue

    # Get version
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip().split()[0]
    except (subprocess.CalledProcessError, IndexError):
        version = "unknown"

    # Output
    if session_id:
        console.print(f"AI-Session-ID: {session_id}")
    console.print(f"AI Agent: Claude Code {version} <noreply@anthropic.com>")
    console.print(f"Model: {model}")


@app.command()
def list_sessions(
    limit: int = typer.Option(10, "--limit", "-n", help="Max sessions to show"),
):
    """List recent AI sessions for current project."""
    claude_dir = Path.home() / ".claude" / "projects"
    project_path = claude_dir / get_project_dir()

    if not project_path.exists():
        console.print("[yellow]No sessions found.[/yellow]")
        raise typer.Exit(0)

    sessions = [(f.stat().st_mtime, f) for f in project_path.glob("*.jsonl") if not f.stem.startswith("agent-")]
    sessions.sort(reverse=True)

    table = Table(box=box.SIMPLE, padding=(0, 1))
    table.add_column("Session", style="cyan")
    table.add_column("Modified", style="dim")
    table.add_column("Size", justify="right")

    for mtime, f in sessions[:limit]:
        dt = datetime.fromtimestamp(mtime)
        table.add_row(f.stem, dt.strftime("%Y-%m-%d %H:%M"), f"{f.stat().st_size/1024:.0f}KB")

    console.print(table)


@app.command()
def coverage(
    limit: int = typer.Option(0, "--limit", "-n", help="Max commits to check (0 = all)"),
    project_dir: Optional[str] = typer.Option(None, "--project", "-p", help="Override project directory"),
):
    """Show AI attribution coverage for commits in the repo."""
    # Get all commits
    try:
        result = subprocess.run(
            ["git", "log", "--format=%H %aI"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        console.print("[red]Error:[/red] Not a git repository")
        raise typer.Exit(1)

    commits_raw = result.stdout.strip().split("\n")
    if limit > 0:
        commits_raw = commits_raw[:limit]

    # Build index
    session_files = find_all_session_files(project_dir)
    if not session_files:
        console.print("[yellow]No session files found.[/yellow]")
        raise typer.Exit(0)

    console.print(f"Building index from {len(session_files)} session files...", style="dim")
    index = build_index(session_files)
    resolver = BlameResolver(index)

    stats = {"hash": 0, "time": 0, "none": 0}
    results: list[tuple[str, str, str]] = []

    for line in commits_raw:
        if not line.strip():
            continue
        parts = line.split(" ", 1)
        commit_hash = parts[0]
        commit_date = parts[1] if len(parts) > 1 else ""

        try:
            ts = datetime.fromisoformat(commit_date)
            commit_timestamp = ts.timestamp()
        except (ValueError, AttributeError):
            commit_timestamp = 0.0

        interaction, method = resolver.resolve(commit_hash, commit_timestamp)

        if method == "match_by_hash":
            stats["hash"] += 1
            results.append((commit_hash[:8], "HASH", "bold green"))
        elif method == "match_by_window":
            stats["time"] += 1
            results.append((commit_hash[:8], "TIME", "cyan"))
        else:
            stats["none"] += 1
            results.append((commit_hash[:8], "NONE", "dim"))

    # Summary table
    total = len(results)
    console.print()

    table = Table(title=f"Coverage Summary ({total} commits)", box=box.ROUNDED)
    table.add_column("Match Type", style="white")
    table.add_column("Count", justify="right")
    table.add_column("Percent", justify="right")

    table.add_row("Hash match", str(stats["hash"]), f"{100*stats['hash']/total:.1f}%", style="bold green")
    table.add_row("Time window", str(stats["time"]), f"{100*stats['time']/total:.1f}%", style="cyan")
    table.add_row("No match", str(stats["none"]), f"{100*stats['none']/total:.1f}%", style="dim")

    matched = stats["hash"] + stats["time"]
    table.add_row("", "", "", style="dim")
    table.add_row("Total matched", str(matched), f"{100*matched/total:.1f}%", style="bold white")

    console.print(table)

    # Index stats
    console.print()
    console.print(Text(f"Index: {len(index.hash_map)} hashes, {len(index.timeline)} prompts", style="dim"))


if __name__ == "__main__":
    app()

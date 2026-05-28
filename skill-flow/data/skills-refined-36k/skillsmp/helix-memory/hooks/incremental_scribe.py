#!/usr/bin/env python3
"""
Incremental Scribe - Real-time Memory Processing

Triggered by UserPromptSubmit hook. Analyzes the PREVIOUS exchange
(not current - that hasn't happened yet) and stores valuable memories.

Non-blocking: spawns mini_scribe.py in tmux for actual analysis.
"""

import os
import sys
import json
import hashlib
import subprocess
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from common import (
    detect_project,
    format_hook_output,
    print_hook_output,
    read_hook_input
)

# Cache for tracking processed exchanges
CACHE_DIR = Path.home() / ".cache/helix-memory"
PROCESSED_FILE = CACHE_DIR / "processed_exchanges.json"
MINI_SCRIBE_PATH = Path(__file__).parent / "mini_scribe.py"


def is_real_user_message(entry: dict) -> bool:
    """Check if entry is a real user message (not tool_result)."""
    content = entry.get("message", {}).get("content", "")
    # Real user messages have string content
    # Tool results have list content with type: tool_result
    return isinstance(content, str) and len(content) > 5


def get_recent_exchanges(transcript_path: str, count: int = 3) -> list:
    """
    Get last N user-assistant exchange pairs from transcript.
    Returns list of dicts with 'user' and 'assistant' entries.
    Only considers REAL user messages (not tool_results).
    """
    exchanges = []
    current_exchange = {}

    try:
        with open(transcript_path) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                entry_type = entry.get("type")

                if entry_type == "user" and is_real_user_message(entry):
                    # New exchange starts with REAL user message
                    if current_exchange.get("user") and current_exchange.get("assistant"):
                        exchanges.append(current_exchange)
                    current_exchange = {"user": entry}

                elif entry_type == "assistant" and current_exchange.get("user"):
                    # Only capture assistant response with actual text
                    content = entry.get("message", {}).get("content", [])
                    if isinstance(content, list):
                        has_text = any(
                            b.get("type") == "text" and b.get("text", "").strip()
                            for b in content if isinstance(b, dict)
                        )
                        if has_text:
                            current_exchange["assistant"] = entry

        # Add last exchange if complete
        if current_exchange.get("user") and current_exchange.get("assistant"):
            exchanges.append(current_exchange)

    except Exception as e:
        print(f"Error reading transcript: {e}", file=sys.stderr)
        return []

    return exchanges[-count:] if len(exchanges) >= count else exchanges


def extract_content(entry: dict) -> str:
    """Extract text content from a transcript entry."""
    message = entry.get("message", {})
    content = message.get("content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    texts.append(block.get("text", ""))
        return " ".join(texts)

    return str(content)


def is_worth_analyzing(exchange: dict) -> bool:
    """
    Quick heuristic: should we bother analyzing this exchange?
    Skip trivial exchanges to save Haiku calls.
    """
    user_content = extract_content(exchange.get("user", {}))
    assistant_content = extract_content(exchange.get("assistant", {}))

    # Skip very short exchanges
    if len(user_content) < 15 and len(assistant_content) < 80:
        return False

    # Skip if assistant response is mostly tool use (count tool markers)
    tool_markers = assistant_content.count('"type": "tool_use"')
    text_ratio = len(assistant_content.replace('"type": "tool_use"', '')) / max(len(assistant_content), 1)

    if tool_markers > 3 and text_ratio < 0.3:
        return False

    # Skip simple acknowledgments
    simple_patterns = [
        "ok", "sure", "done", "yes", "no", "thanks",
        "got it", "understood", "tak", "nie", "dobra"
    ]
    user_lower = user_content.lower().strip()
    if user_lower in simple_patterns or len(user_lower) < 5:
        return False

    return True


def get_exchange_hash(exchange: dict) -> str:
    """Generate hash for deduplication."""
    user_content = extract_content(exchange.get("user", {}))[:500]
    assistant_content = extract_content(exchange.get("assistant", {}))[:500]
    combined = f"{user_content}|{assistant_content}"
    return hashlib.md5(combined.encode()).hexdigest()[:12]


def load_processed() -> set:
    """Load set of already-processed exchange hashes."""
    if not PROCESSED_FILE.exists():
        return set()
    try:
        data = json.loads(PROCESSED_FILE.read_text())
        return set(data.get("processed", []))
    except:
        return set()


def save_processed(processed: set):
    """Save processed hashes, keeping only last 200."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    # Keep only most recent
    recent = list(processed)[-200:]
    PROCESSED_FILE.write_text(json.dumps({"processed": recent}))


def run_mini_scribe(exchange: dict, project: str) -> bool:
    """
    Spawn mini_scribe.py in tmux for async processing.
    Returns True if spawned successfully.
    """
    # Write exchange to temp file
    temp_file = f"/tmp/exchange_{os.getpid()}_{int(time.time())}.json"
    try:
        with open(temp_file, 'w') as f:
            json.dump({
                "user": extract_content(exchange.get("user", {})),
                "assistant": extract_content(exchange.get("assistant", {}))
            }, f)
    except Exception as e:
        print(f"Error writing temp file: {e}", file=sys.stderr)
        return False

    # Spawn tmux session
    session_name = f"mini-scribe-{int(time.time())}"
    project_arg = f"--project {project}" if project else ""

    tmux_cmd = (
        f"tmux new-session -d -s {session_name} "
        f"'python3 {MINI_SCRIBE_PATH} {temp_file} {project_arg}; "
        f"rm -f {temp_file}; sleep 2'"
    )

    try:
        subprocess.run(tmux_cmd, shell=True, timeout=3, capture_output=True)
        return True
    except Exception as e:
        print(f"Error spawning tmux: {e}", file=sys.stderr)
        return False


def main():
    """Main hook execution."""
    # Read hook input from stdin (JSON)
    hook_data = read_hook_input()

    # DEBUG: Log with session ID
    session_id = hook_data.get("session_id", "unknown")[:8]
    debug_file = Path.home() / f".cache/helix-memory/debug_{session_id}.json"
    debug_file.parent.mkdir(parents=True, exist_ok=True)
    debug_file.write_text(json.dumps(hook_data, indent=2, default=str)[:2000])

    transcript = hook_data.get("transcript_path", "")
    cwd = hook_data.get("cwd", os.getcwd())

    # Skip subagent/scribe sessions (their transcripts are small and contain scribe prompts)
    if "agent-" in transcript or not transcript:
        output = {"hookSpecificOutput": {"skipped": "subagent_session"}}
        print_hook_output(output)
        return

    if not transcript or not Path(transcript).exists():
        # No transcript - nothing to do
        output = {"hookSpecificOutput": {"skipped": "no_transcript"}}
        print_hook_output(output)
        return

    # Detect project
    project = detect_project(cwd)

    # Get recent exchanges
    exchanges = get_recent_exchanges(transcript, count=3)

    if len(exchanges) < 1:
        # Not enough history yet
        output = {"hookSpecificOutput": {"skipped": "insufficient_history"}}
        print_hook_output(output)
        return

    # Analyze most recent COMPLETE exchange
    # Hash deduplication prevents re-analyzing same exchange
    exchange = exchanges[-1]

    # Check if worth analyzing
    if not is_worth_analyzing(exchange):
        output = {"hookSpecificOutput": {"skipped": "trivial_exchange"}}
        print_hook_output(output)
        return

    # Check if already processed
    ex_hash = get_exchange_hash(exchange)
    processed = load_processed()

    if ex_hash in processed:
        output = {"hookSpecificOutput": {"skipped": "already_processed"}}
        print_hook_output(output)
        return

    # Spawn mini scribe
    if run_mini_scribe(exchange, project):
        processed.add(ex_hash)
        save_processed(processed)
        output = {"hookSpecificOutput": {"status": "spawned", "hash": ex_hash}}
    else:
        output = {"hookSpecificOutput": {"status": "spawn_failed"}}

    print_hook_output(output)


if __name__ == "__main__":
    main()

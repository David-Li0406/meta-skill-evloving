#!/usr/bin/env python3
"""
Stop Hook: Hybrid Memory Extraction

Fires after each Claude response. Two-phase extraction:
1. INSTANT: Fast pattern-based extraction (paths, URLs, markers) - synchronous
2. SCRIBE: LLM-based deep analysis - spawned in background (optional)

This ensures important facts are captured immediately while allowing
deeper analysis to run asynchronously.
"""

import sys
import json
import os
import time
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from common import (
    read_hook_input,
    detect_project,
    format_hook_output,
    print_hook_output,
    check_helix_running
)

from instant_extract import process_exchange

SIMPLE_SCRIBE = Path(__file__).parent / "simple_scribe.py"
# Only spawn LLM scribe if instant extract found nothing and exchange is substantial
SPAWN_SCRIBE_THRESHOLD = 500  # Min assistant response length to warrant LLM analysis


def get_last_exchange(transcript_path: str) -> tuple:
    """
    Extract last user message and last assistant response from transcript.
    Returns (user_msg, assistant_msg) or (None, None) if not found.
    """
    last_user = None
    last_assistant = None
    
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
                content = entry.get("message", {}).get("content", "")
                
                if entry_type == "user":
                    # Real user message = string content
                    if isinstance(content, str) and len(content) > 5:
                        last_user = content
                
                elif entry_type == "assistant":
                    # Assistant response = list with text blocks
                    if isinstance(content, list):
                        texts = []
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                texts.append(block.get("text", ""))
                        if texts:
                            last_assistant = " ".join(texts)
    except Exception as e:
        print(f"Error reading transcript: {e}", file=sys.stderr)
    
    return last_user, last_assistant


def spawn_scribe(user_msg: str, assistant_msg: str, project: str):
    """
    Spawn simple_scribe.py in background with temp files.
    Fire and forget - returns immediately.
    """
    # Write to temp files (avoid shell escaping issues)
    ts = int(time.time() * 1000)
    user_file = f"/tmp/scribe_user_{ts}.txt"
    asst_file = f"/tmp/scribe_asst_{ts}.txt"
    
    Path(user_file).write_text(user_msg[:2000])
    Path(asst_file).write_text(assistant_msg[:5000])
    
    # Spawn in background
    cmd = f"python3 {SIMPLE_SCRIBE} '{user_file}' '{asst_file}' --project '{project}'"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    """Main hook execution - Hybrid extraction."""
    hook_data = read_hook_input()

    transcript_path = hook_data.get("transcript_path", "")
    cwd = hook_data.get("cwd", "")

    if not transcript_path or not Path(transcript_path).exists():
        output = format_hook_output(suppress=True)
        print_hook_output(output)
        sys.exit(0)

    # Skip agent/scribe sub-sessions
    if "agent-" in transcript_path:
        output = format_hook_output(suppress=True)
        print_hook_output(output)
        sys.exit(0)

    # Extract last exchange
    user_msg, assistant_msg = get_last_exchange(transcript_path)

    if not user_msg or not assistant_msg:
        output = format_hook_output(suppress=True)
        print_hook_output(output)
        sys.exit(0)

    # Skip trivial exchanges
    if len(user_msg) < 15 or len(assistant_msg) < 100:
        output = format_hook_output(suppress=True)
        print_hook_output(output)
        sys.exit(0)

    # Detect project
    project = detect_project(cwd)

    # PHASE 1: Instant pattern extraction (synchronous, fast)
    instant_count = 0
    extracts = []
    if check_helix_running():
        instant_count, extracts = process_exchange(user_msg, assistant_msg, project)
        if instant_count > 0:
            print(f"[memory] Instant: stored {instant_count} memories", file=sys.stderr)

    # PHASE 2: LLM scribe (background, optional)
    # Spawn if exchange is substantial, UNLESS instant found high-value items
    # High-value = inline markers or trigger phrases (importance >= 7)
    max_importance = max((e.get("importance", 0) for e in extracts), default=0) if extracts else 0
    found_high_value = max_importance >= 7

    should_spawn_scribe = (
        not found_high_value and  # Skip if instant found important items
        len(assistant_msg) > SPAWN_SCRIBE_THRESHOLD and
        len(user_msg) > 30
    )

    if should_spawn_scribe:
        spawn_scribe(user_msg, assistant_msg, project)
        print("[memory] Scribe: spawned for deep analysis", file=sys.stderr)

    output = format_hook_output(suppress=True)
    print_hook_output(output)
    sys.exit(0)


if __name__ == "__main__":
    main()

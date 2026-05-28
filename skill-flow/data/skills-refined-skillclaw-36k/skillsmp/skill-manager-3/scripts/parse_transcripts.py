#!/usr/bin/env python3
"""
parse_transcripts.py - Extract tool usage patterns from Claude Code transcripts.

Alternative to hooks - parses transcript JSONL files directly.
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import argparse

SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
SEQUENCES_FILE = PATTERNS_DIR / "tool-sequences.jsonl"
PROMPTS_FILE = PATTERNS_DIR / "prompt-patterns.jsonl"
PROMPTS_LOG = PATTERNS_DIR / "user-prompts.jsonl"  # Full prompt log for learning
PROJECTS_DIR = Path.home() / ".claude" / "projects"
STATE_FILE = PATTERNS_DIR / "parser-state.json"


def get_state():
    """Load parser state (last processed timestamps)."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed_files": {}, "last_run": None}


def save_state(state):
    """Save parser state."""
    state["last_run"] = datetime.utcnow().isoformat() + "Z"
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def summarize_input(tool_input, tool_name):
    """Create compact summary of tool input for pattern matching."""
    if not tool_input:
        return {}

    summary = {}

    # File operations
    if "file_path" in tool_input:
        path = Path(tool_input["file_path"])
        summary["file_ext"] = path.suffix.lower() if path.suffix else "none"
        summary["path_depth"] = len(path.parts)

    # Bash commands
    if "command" in tool_input and tool_name == "Bash":
        cmd = tool_input["command"].strip()
        if cmd:
            parts = cmd.split()
            primary_cmd = parts[0] if parts else ""
            if "/" in primary_cmd:
                primary_cmd = primary_cmd.split("/")[-1]
            summary["command"] = primary_cmd

            # Domain hints
            domain_map = {
                "docker": "devops", "docker-compose": "devops",
                "kubectl": "devops", "helm": "devops", "terraform": "devops",
                "git": "git", "gh": "git",
                "npm": "frontend", "yarn": "frontend", "pnpm": "frontend",
                "python": "backend", "pip": "backend", "pytest": "backend",
                "python3": "backend", "pip3": "backend",
            }
            if primary_cmd in domain_map:
                summary["domain_hint"] = domain_map[primary_cmd]

    # Search patterns
    if "pattern" in tool_input:
        summary["has_pattern"] = True
        summary["pattern_hash"] = hashlib.md5(tool_input["pattern"].encode()).hexdigest()[:8]

    return summary


def extract_domains(text):
    """Extract domain signals from user prompts."""
    text_lower = text.lower()
    domains = []

    domain_keywords = {
        "devops": ["docker", "kubernetes", "k8s", "deploy", "ci/cd", "pipeline", "terraform"],
        "security": ["vulnerability", "security", "auth", "password", "encrypt", "owasp"],
        "frontend": ["react", "vue", "css", "component", "ui", "tailwind", "next.js"],
        "backend": ["api", "database", "server", "endpoint", "rest", "graphql"],
        "git": ["commit", "branch", "merge", "rebase", "pull request", "pr"],
        "data_science": ["pandas", "numpy", "model", "training", "dataset"],
    }

    for domain, keywords in domain_keywords.items():
        if any(kw in text_lower for kw in keywords):
            domains.append(domain)

    return domains


def parse_transcript(file_path, last_processed_time=None):
    """Parse a transcript file and extract tool usage patterns."""
    tool_records = []
    prompt_records = []
    full_prompts = []  # Store full prompts for learning

    try:
        with open(file_path) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                # Skip if before last processed time
                timestamp = entry.get("timestamp")
                if timestamp and last_processed_time:
                    if timestamp <= last_processed_time:
                        continue

                entry_type = entry.get("type")
                session_id = entry.get("sessionId", "unknown")

                # Extract tool uses from assistant messages
                if entry_type == "assistant":
                    message = entry.get("message", {})
                    content = message.get("content", [])

                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "tool_use":
                                tool_name = item.get("name", "unknown")
                                tool_input = item.get("input", {})

                                # Skip internal tools
                                if tool_name in ["TodoWrite", "AskUserQuestion", "ExitPlanMode", "EnterPlanMode"]:
                                    continue

                                record = {
                                    "session_id": session_id,
                                    "timestamp": timestamp or datetime.utcnow().isoformat() + "Z",
                                    "tool": tool_name,
                                    "input_summary": summarize_input(tool_input, tool_name),
                                    "success": True,  # Assume success if in transcript
                                }
                                tool_records.append(record)

                # Extract user prompts
                elif entry_type == "user":
                    message = entry.get("message", {})
                    content = message.get("content", "")

                    # Skip meta messages
                    if entry.get("isMeta"):
                        continue

                    # Skip bash output (but keep bash input commands)
                    if "<bash-stdout>" in content or "<bash-stderr>" in content:
                        continue

                    if isinstance(content, str) and len(content) > 5:
                        # Skip warmup/system messages
                        if content.strip().lower() in ["warmup", "warmup..."]:
                            continue

                        # Clean up bash input tags for logging
                        clean_content = content
                        if "<bash-input>" in content:
                            # Extract just the command
                            import re
                            match = re.search(r'<bash-input>(.*?)</bash-input>', content)
                            if match:
                                clean_content = f"[shell] {match.group(1)}"

                        # Store full prompt for learning
                        full_prompts.append({
                            "session_id": session_id,
                            "timestamp": timestamp,
                            "prompt": clean_content[:500],  # Cap at 500 chars
                            "length": len(content),
                        })

                        # Also extract domains for pattern analysis
                        domains = extract_domains(content)
                        if domains:
                            prompt_records.append({
                                "session_id": session_id,
                                "timestamp": timestamp,
                                "domains": domains,
                                "prompt_length": len(content),
                            })

    except Exception as e:
        print(f"  Error parsing {file_path.name}: {e}")

    return tool_records, prompt_records, full_prompts


def main():
    parser = argparse.ArgumentParser(description="Parse Claude Code transcripts for skill patterns")
    parser.add_argument("--all", action="store_true", help="Reprocess all transcripts (ignore state)")
    parser.add_argument("--days", type=int, default=7, help="Only process transcripts from last N days")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("Transcript Pattern Parser")
    print("=" * 60)

    # Ensure patterns directory exists
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)

    # Load state
    state = get_state() if not args.all else {"processed_files": {}}

    # Find transcript files
    cutoff = datetime.utcnow() - timedelta(days=args.days)
    transcript_files = []

    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            for jsonl_file in project_dir.glob("*.jsonl"):
                # Check modification time
                mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                if mtime >= cutoff:
                    transcript_files.append(jsonl_file)

    print(f"Found {len(transcript_files)} transcript files from last {args.days} days")

    total_tools = 0
    total_prompts = 0
    total_full_prompts = 0

    for tf in transcript_files:
        file_key = str(tf)
        last_processed = state["processed_files"].get(file_key)

        if args.verbose:
            print(f"  Processing: {tf.name}")

        tool_records, prompt_records, full_prompts = parse_transcript(tf, last_processed)

        if tool_records:
            with open(SEQUENCES_FILE, "a") as f:
                for record in tool_records:
                    f.write(json.dumps(record) + "\n")
            total_tools += len(tool_records)

        if prompt_records:
            with open(PROMPTS_FILE, "a") as f:
                for record in prompt_records:
                    f.write(json.dumps(record) + "\n")
            total_prompts += len(prompt_records)

        if full_prompts:
            with open(PROMPTS_LOG, "a") as f:
                for record in full_prompts:
                    f.write(json.dumps(record) + "\n")
            total_full_prompts += len(full_prompts)

        # Update state with latest timestamp from this file
        if tool_records or prompt_records or full_prompts:
            all_timestamps = [r.get("timestamp") for r in tool_records + prompt_records + full_prompts if r.get("timestamp")]
            if all_timestamps:
                state["processed_files"][file_key] = max(all_timestamps)

    # Save state
    save_state(state)

    print(f"\nExtracted:")
    print(f"  - Tool patterns: {total_tools}")
    print(f"  - Domain patterns: {total_prompts}")
    print(f"  - User prompts: {total_full_prompts}")

    if total_full_prompts > 0:
        print(f"\nPrompt log: {PROMPTS_LOG}")

    if total_tools > 0 or total_prompts > 0:
        print(f"Run 'manage.py learn' to generate skill candidates")


if __name__ == "__main__":
    main()

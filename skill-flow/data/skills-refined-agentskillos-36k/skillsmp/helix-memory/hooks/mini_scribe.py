#!/usr/bin/env python3
"""
Mini Scribe - Lightweight Single-Exchange Analyzer
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from common import (
    check_helix_running,
    ensure_helix_running,
    store_memory,
    llm_generate,
    extract_json_array
)


def build_prompt(user_content: str, assistant_content: str, project: str) -> str:
    """Build the analysis prompt."""
    project_tag = project if project else "general"
    user_truncated = user_content[:600]
    assistant_truncated = assistant_content[:1200]
    
    lines = [
        "Extract 0-2 memories from this exchange. ONLY store if genuinely valuable.",
        "",
        "RULES:",
        "1. Output ENGLISH only",
        "2. High-level summaries - NO code snippets, NO raw outputs",
        "3. Categories: preference, decision, solution, fact",
        "4. Importance: preference=8-10, decision=7-9, solution=6-8, fact=5-7",
        "",
        f"User: {user_truncated}",
        "",
        f"Assistant: {assistant_truncated}",
        "",
        f'Return JSON: [{{"content": "...", "category": "...", "importance": N, "tags": "{project_tag}"}}]',
        "If nothing valuable, return: []"
    ]
    return "\n".join(lines)


def analyze_exchange(user_content: str, assistant_content: str, project: str = "") -> list:
    """Analyze single exchange with LLM (Ollama or Haiku)."""
    prompt = build_prompt(user_content, assistant_content, project)

    output, provider = llm_generate(prompt, timeout=30)
    if output:
        print(f"Using LLM: {provider}", file=sys.stderr)
        return extract_json_array(output)

    print("ERROR: All LLM providers failed", file=sys.stderr)
    return []


def store_memories(memories: list, project: str = "") -> int:
    """Store extracted memories to HelixDB."""
    stored = 0
    for mem in memories:
        content = mem.get("content", "")
        if not content or len(content) < 15:
            continue
        
        tags = mem.get("tags", project or "")
        if project and project.lower() not in tags.lower():
            tags = f"{project},{tags}" if tags else project
        
        category = mem.get("category", "fact")
        importance = min(10, max(1, mem.get("importance", 5)))
        
        result = store_memory(content, category, importance, tags, "mini-scribe")
        if result:
            stored += 1
            print(f"  + [{category}] {content[:50]}...")
    
    return stored


def main():
    parser = argparse.ArgumentParser(description="Mini Scribe - Single Exchange Analyzer")
    parser.add_argument("exchange_file", help="Path to exchange JSON file")
    parser.add_argument("--project", default="", help="Project name")
    
    args = parser.parse_args()
    
    print(f"\n{'='*40}")
    print("Mini Scribe - Analyzing exchange")
    print(f"{'='*40}")
    
    # Read exchange
    try:
        with open(args.exchange_file) as f:
            exchange = json.load(f)
    except Exception as e:
        print(f"Error reading exchange file: {e}", file=sys.stderr)
        sys.exit(1)
    
    user_content = exchange.get("user", "")
    assistant_content = exchange.get("assistant", "")
    
    if not user_content or not assistant_content:
        print("Empty exchange, skipping")
        sys.exit(0)
    
    print(f"User: {user_content[:60]}...")
    print(f"Project: {args.project or '(none)'}")
    
    # Ensure HelixDB running
    if not check_helix_running():
        print("Starting HelixDB...")
        if not ensure_helix_running():
            print("ERROR: Could not start HelixDB", file=sys.stderr)
            sys.exit(1)
    
    # Analyze
    print("\nAnalyzing exchange...")
    memories = analyze_exchange(user_content, assistant_content, args.project)
    print(f"Found {len(memories)} memories")
    
    if not memories:
        print("No memories to store")
        sys.exit(0)
    
    # Store
    print("\nStoring memories...")
    stored = store_memories(memories, args.project)

    # Narrate if enabled for this project
    from narrator import maybe_narrate
    if stored > 0:
        maybe_narrate(memories, args.project)

    print(f"\n{'='*40}")
    print(f"Done: {stored}/{len(memories)} stored")
    print(f"{'='*40}\n")


if __name__ == "__main__":
    main()

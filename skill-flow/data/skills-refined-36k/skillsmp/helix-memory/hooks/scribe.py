#!/usr/bin/env python3
"""
Scribe - Background Memory Processor

Runs in tmux session, analyzes conversation transcripts,
and stores high-level memories without blocking the main Claude session.

Usage:
    python3 scribe.py <transcript_path> [--project <name>]

The scribe:
1. Reads conversation transcript
2. Analyzes with Haiku (cheap, fast) for high-level summaries
3. Stores memories to HelixDB
4. Builds graph relationships between memories
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    check_helix_running,
    ensure_helix_running,
    store_memory,
    get_all_memories,
    detect_project,
    generate_simple_embedding,
    llm_generate,
    extract_json_array
)


def read_transcript(transcript_path: str, limit: int = 20) -> str:
    """Read and format transcript for analysis."""
    messages = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if entry.get("type") in ["user", "assistant"]:
                        role = entry.get("type", "unknown")
                        content = entry.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            content = " ".join(
                                b.get("text", "") for b in content
                                if isinstance(b, dict) and b.get("type") == "text"
                            )
                        if content and len(content) > 10:
                            messages.append(f"[{role}]: {content[:500]}")
    except Exception as e:
        print(f"ERROR reading transcript: {e}", file=sys.stderr)
        return ""

    # Take last N messages
    if len(messages) > limit:
        messages = messages[-limit:]

    return "\n\n".join(messages)


def analyze_transcript(transcript_text: str, project: str = "") -> list:
    """
    Use LLM (Ollama or Haiku) to extract high-level memories.
    Focus on summaries, not code snippets.
    """
    project_context = f"\nCurrent project: {project}" if project else ""

    prompt = f'''You are a memory scribe. Analyze this conversation and extract memories worth storing.

CRITICAL RULES:
1. Output ALL memories in ENGLISH regardless of conversation language
2. Store HIGH-LEVEL SUMMARIES only - NO code snippets, NO raw outputs
   - BAD: "function foo() {{ return x }}"
   - GOOD: "Implemented user authentication using JWT tokens"
3. Focus on: DECISIONS made, PROBLEMS solved, LEARNINGS, USER PREFERENCES
4. Skip: routine tool usage, file reads, debugging attempts
{project_context}

Categories (importance ranges):
- preference: User preferences, workflow choices (8-10)
- decision: Architectural/technical decisions (7-9)
- solution: Bug fixes, workarounds, completed fixes (6-8)
- fact: Learned info about tools, APIs, codebase (5-7)
- insight: Technical tips discovered (7-8)

Return ONLY valid JSON array:
[{{"content": "...", "category": "...", "importance": N, "tags": "{project},..."}}]

If nothing worth storing, return: []

Conversation:
{transcript_text}'''

    output, provider = llm_generate(prompt, timeout=60)
    if output:
        print(f"   Using LLM: {provider}", file=sys.stderr)
        return extract_json_array(output)

    print("ERROR: All LLM providers failed", file=sys.stderr)
    return []


def store_memories(memories: list, project: str = "") -> int:
    """Store memories to HelixDB with embeddings."""
    stored = 0
    for mem in memories:
        content = mem.get("content", "")
        if not content or len(content) < 20:
            continue

        # Ensure project in tags
        tags = mem.get("tags", "")
        if project and project.lower() not in tags.lower():
            tags = f"{project},{tags}" if tags else project

        category = mem.get("category", "fact")
        importance = min(10, max(1, mem.get("importance", 5)))

        # store_memory(content, category, importance, tags, source)
        result = store_memory(content, category, importance, tags, "scribe")
        if result:
            stored += 1
            print(f"  ✓ [{category}] {content[:60]}...")

    return stored


def main():
    parser = argparse.ArgumentParser(description="Scribe - Background Memory Processor")
    parser.add_argument("transcript", help="Path to transcript JSONL file")
    parser.add_argument("--project", help="Project name override")
    parser.add_argument("--cwd", help="Working directory for project detection")

    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"🖋️  SCRIBE - Background Memory Processor")
    print(f"{'='*50}")
    print(f"Transcript: {args.transcript}")

    # Ensure HelixDB is running
    if not check_helix_running():
        print("Starting HelixDB...", file=sys.stderr)
        if not ensure_helix_running():
            print("ERROR: Could not start HelixDB", file=sys.stderr)
            sys.exit(1)

    # Detect project
    project = args.project
    if not project and args.cwd:
        project = detect_project(args.cwd)
    print(f"Project: {project or '(none)'}")

    # Read transcript
    print("\n📖 Reading transcript...")
    transcript_text = read_transcript(args.transcript)
    if not transcript_text:
        print("No transcript content to analyze")
        sys.exit(0)

    print(f"   {len(transcript_text)} chars, analyzing...")

    # Analyze with LLM (Ollama preferred, Haiku fallback)
    print("\n🧠 Analyzing transcript...")
    memories = analyze_transcript(transcript_text, project)
    print(f"   Found {len(memories)} memories")

    if not memories:
        print("\n✅ No new memories to store")
        sys.exit(0)

    # Store memories
    print("\n💾 Storing memories...")
    stored = store_memories(memories, project)

    print(f"\n{'='*50}")
    print(f"✅ Scribe complete: {stored}/{len(memories)} memories stored")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

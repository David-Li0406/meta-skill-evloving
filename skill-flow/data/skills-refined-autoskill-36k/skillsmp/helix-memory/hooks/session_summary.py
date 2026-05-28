#!/usr/bin/env python3
"""
SessionEnd Hook: DISABLED

Was creating low-value summaries like:
  "Session: abc123, Date: 2025-01-01, Exchanges: 15"

Real memory extraction now happens via:
1. instant_extract.py (patterns, markers) - on every Stop
2. simple_scribe.py (LLM analysis) - on Stop when needed

This hook now exits immediately without storing anything.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    read_hook_input,
    parse_transcript,
    extract_message_content,
    store_memory,
    store_memory_embedding,
    link_memory_to_context,
    create_context,
    generate_simple_embedding,
    format_hook_output,
    print_hook_output,
    ensure_helix_running
)

def is_meaningful_content(content: str) -> bool:
    """Check if content is meaningful for summarization."""
    # Skip noisy patterns
    noise = ['<bash', 'bash-stdout', '#!/bin', 'server {', '[?2026', '[@', 'Let me ']
    if any(p in content for p in noise):
        return False
    if len(content.strip()) < 20:
        return False
    return True

def summarize_session(transcript: list, session_id: str, cwd: str) -> dict:
    """
    Create session summary from full transcript.

    Only extracts meaningful decisions and outcomes from USER messages.

    Args:
        transcript: Full session transcript
        session_id: Session identifier
        cwd: Working directory

    Returns:
        Summary dict with content, category, importance, tags
    """
    if not transcript:
        return None

    # Only process USER messages for meaningful content
    user_messages = [e for e in transcript if e.get("type") == "user"]

    if len(user_messages) < 2:
        # Too short to summarize
        return None

    # Extract first user message as topic
    first_msg = extract_message_content(user_messages[0])[:150]
    if not is_meaningful_content(first_msg):
        first_msg = ""

    # Count significant exchanges (proxy for productivity)
    significant_exchanges = len([m for m in user_messages if is_meaningful_content(extract_message_content(m))])

    # Build minimal summary
    summary_parts = [
        f"Session: {session_id[:8]}",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"Directory: {cwd}",
    ]

    if first_msg:
        summary_parts.append(f"Topic: {first_msg}")

    summary_parts.append(f"Exchanges: {significant_exchanges}")

    summary_content = "\n".join(summary_parts)

    # Base importance on session length/depth
    importance = min(5 + (significant_exchanges // 3), 8)

    return {
        "content": summary_content[:500],
        "category": "context",
        "importance": importance,
        "tags": f"session,summary,{session_id[:8]}"
    }

def main():
    """Main hook execution - DISABLED, exits immediately."""
    # Just exit - session summaries were low value garbage
    print('{"suppressOutput": true}')
    sys.exit(0)

if __name__ == "__main__":
    main()

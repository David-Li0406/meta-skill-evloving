#!/usr/bin/env python3
"""
Instant Extract - Fast Pattern-Based Memory Extraction

Zero-latency extraction using regex patterns and inline markers.
No LLM required. Runs synchronously in the Stop hook.

Extracts:
1. Paths: ~/foo/bar, /Users/username/Sites/project
2. URLs: https://example.com, localhost:3000
3. Inline markers: <!-- MEM: category | content -->
4. Explicit triggers: "remember that", "always use", "prefer"
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    store_memory,
    store_memory_embedding,
    generate_embedding,
    check_helix_running,
    find_similar_memories
)

# Pattern definitions
PATTERNS = {
    # Paths - macOS/Unix style
    "path": [
        r'(?:^|[\s\'"(])(/(?:Users|home|var|opt|etc)/[a-zA-Z0-9_\-./]+)',  # Absolute
        r'(?:^|[\s\'"(])(~/[a-zA-Z0-9_\-./]+)',  # Home-relative
    ],
    # URLs
    "url": [
        r'(https?://[^\s<>"\')\]]+)',
        r'(localhost:\d{2,5}[^\s<>"\')\]]*)',
    ],
    # Inline memory markers from Claude (visible blockquote format)
    # Matches: > 💾 **category**: content
    "marker": [
        r'>\s*💾\s*\*\*(\w+)\*\*:\s*(.+?)(?:\n|$)',
        r'<!--\s*MEM:\s*(\w+)\s*\|\s*(.+?)\s*-->',  # Legacy hidden format
    ],
}

# Trigger phrases that indicate something to remember
# Each tuple: (regex, category, importance)
# Patterns capture the FULL statement for context
TRIGGER_PHRASES = [
    # Preferences - capture the whole preference statement
    (r'(?:always use|prefer using|i prefer|use)\s+(\w+(?:\s+\w+)?)\s+(?:for|over|instead)', "preference", 8),
    (r'(?:never use|avoid using|don\'t use|avoid)\s+(\w+(?:\s+\w+)?)\b', "preference", 8),
    # Explicit memory requests
    (r'(?:remember that|note that|important:)\s+(.{15,100}?)(?:\.|$)', "fact", 7),
    # Credentials - be careful, capture description not value
    (r'(?:api key|password|secret|token)\s+(?:is |stored |in )(.{10,50}?)(?:\.|$)', "credential", 9),
]

# Claude discovery patterns (when Claude finds something)
DISCOVERY_PATTERNS = [
    (r'(?:found|located|discovered) (?:at|in)\s+(/[^\s]+|~/[^\s]+)', "fact", 6),
    (r'(?:config|configuration) (?:is )?(?:at|in)\s+(/[^\s]+|~/[^\s]+)', "fact", 6),
]


def extract_paths(text: str) -> List[Dict]:
    """Extract file/directory paths from text."""
    results = []
    seen = set()

    for pattern in PATTERNS["path"]:
        for match in re.finditer(pattern, text, re.MULTILINE):
            path = match.group(1).rstrip('.,;:')
            # Filter out obvious non-paths
            if len(path) < 5 or path in seen:
                continue
            if any(x in path for x in ['.git/', 'node_modules/', '__pycache__']):
                continue
            seen.add(path)
            results.append({
                "content": f"Path reference: {path}",
                "category": "path",
                "importance": 5,
                "raw": path
            })

    return results


def extract_urls(text: str) -> List[Dict]:
    """Extract URLs from text."""
    results = []
    seen = set()

    for pattern in PATTERNS["url"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            url = match.group(1).rstrip('.,;:)')
            # Filter noise
            if url in seen or len(url) < 10:
                continue
            if any(x in url for x in ['github.com/anthropics', 'claude.ai', 'googleapis.com']):
                continue
            seen.add(url)
            results.append({
                "content": f"URL: {url}",
                "category": "url",
                "importance": 5,
                "raw": url
            })

    return results


def extract_inline_markers(text: str) -> List[Dict]:
    """Extract <!-- MEM: category | content --> markers from Claude's response."""
    results = []

    for pattern in PATTERNS["marker"]:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            category = match.group(1).lower()
            content = match.group(2).strip()

            # Validate category (matches CLAUDE.md)
            valid_categories = {"preference", "fact", "decision", "solution", "credential"}
            if category not in valid_categories:
                category = "fact"

            # Importance based on category
            importance_map = {"preference": 8, "decision": 8, "solution": 7, "credential": 9, "fact": 6}
            importance = importance_map.get(category, 6)

            results.append({
                "content": content,
                "category": category,
                "importance": importance,
                "source": "inline_marker"
            })

    return results


def extract_trigger_phrases(text: str) -> List[Dict]:
    """Extract content following trigger phrases with proper context."""
    results = []

    for pattern, category, importance in TRIGGER_PHRASES:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            raw_content = match.group(1).strip()
            if len(raw_content) < 3 or len(raw_content) > 200:
                continue

            # Add context based on pattern type
            full_match = match.group(0).lower()
            if "prefer" in full_match or "always use" in full_match:
                content = f"User prefers {raw_content}"
            elif "never" in full_match or "avoid" in full_match or "don't" in full_match:
                content = f"User avoids {raw_content}"
            elif "remember" in full_match or "note" in full_match:
                content = raw_content  # Already has context
            else:
                content = raw_content

            results.append({
                "content": content,
                "category": category,
                "importance": importance,
                "source": "trigger_phrase"
            })

    return results


def extract_discoveries(text: str) -> List[Dict]:
    """Extract things Claude discovered/found."""
    results = []

    for pattern, category, importance in DISCOVERY_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            path = match.group(1).strip()
            if len(path) > 3:
                results.append({
                    "content": f"Discovered: {path}",
                    "category": category,
                    "importance": importance,
                    "source": "discovery"
                })

    return results


def extract_all(user_msg: str, assistant_msg: str, project: str = "") -> List[Dict]:
    """
    Run all extraction patterns on the exchange.

    Args:
        user_msg: User's message
        assistant_msg: Claude's response
        project: Current project name for tagging

    Returns:
        List of extracted memories
    """
    all_extracts = []

    # From user message (explicit preferences, paths)
    all_extracts.extend(extract_trigger_phrases(user_msg))
    all_extracts.extend(extract_paths(user_msg))
    all_extracts.extend(extract_urls(user_msg))

    # From assistant response (markers, discoveries)
    all_extracts.extend(extract_inline_markers(assistant_msg))
    all_extracts.extend(extract_discoveries(assistant_msg))

    # Prepend project tag to all extracts
    for item in all_extracts:
        existing_tags = item.get("tags", "")
        if project:
            # Prepend project if not already present
            if project.lower() not in existing_tags.lower():
                item["tags"] = f"{project},{existing_tags}" if existing_tags else project
            else:
                item["tags"] = existing_tags if existing_tags else project
        else:
            item["tags"] = existing_tags

    return all_extracts


def store_extracts(extracts: List[Dict], project: str = "") -> int:
    """
    Store extracted memories to HelixDB, with deduplication.

    Returns number of memories stored.
    """
    if not check_helix_running():
        return 0

    stored = 0

    for extract in extracts:
        content = extract.get("content", "")
        category = extract.get("category", "fact")
        importance = extract.get("importance", 5)
        tags = extract.get("tags", project)

        # Skip if too short
        if len(content) < 10:
            continue

        # Check for duplicates
        similar = find_similar_memories(content, category)
        if similar:
            continue

        # Store memory
        memory_id = store_memory(
            content=content,
            category=category,
            importance=importance,
            tags=tags,
            source="instant"
        )

        if memory_id:
            # Generate and store embedding
            vector, model = generate_embedding(content)
            store_memory_embedding(memory_id, vector, content, model)
            stored += 1
            print(f"[instant] +{category}: {content[:50]}...", file=sys.stderr)

    return stored


def process_exchange(user_msg: str, assistant_msg: str, project: str = "") -> Tuple[int, List[Dict]]:
    """
    Main entry point: extract and store memories from an exchange.

    Returns:
        (count_stored, list_of_extracts)
    """
    extracts = extract_all(user_msg, assistant_msg, project)

    if not extracts:
        return 0, []

    stored = store_extracts(extracts, project)
    return stored, extracts


if __name__ == "__main__":
    import json

    # Read hook input from stdin
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)  # No input, exit silently

    # Get last assistant message
    assistant_msg = ""
    for msg in reversed(data.get("messages", [])):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if isinstance(content, list):
                assistant_msg = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            else:
                assistant_msg = str(content)
            break

    if not assistant_msg:
        sys.exit(0)

    # Extract only inline markers (visible format)
    extracts = extract_inline_markers(assistant_msg)
    if extracts:
        project = data.get("cwd", "").split("/")[-1]
        stored = store_extracts(extracts, project)
        if stored:
            print(f"[instant] +{stored} memories", file=sys.stderr)

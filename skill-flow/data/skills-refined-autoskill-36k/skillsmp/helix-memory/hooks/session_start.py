#!/usr/bin/env python3
"""
SessionStart Hook: Load Memory Status and Critical Preferences

Executes at the START of each session (before any user interaction).
Provides Claude with:
1. HelixDB status (running/not running, memory count)
2. All high-importance memories (preferences, critical facts)

This ensures Claude always knows user preferences from the first message.
"""

import sys
import json
from pathlib import Path

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    check_helix_running,
    get_all_memories,
    detect_project,
    format_hook_output,
    print_hook_output,
    hybrid_search,
    get_related_memories,
    get_project_memories_via_graph,
)
import os


def follow_memory_edges(memories: list, seen_ids: set, max_linked: int = 3) -> list:
    """
    Follow edges from memories to get linked context.

    For each memory, check for related memories via edges
    and include the most important linked ones.
    """
    linked_results = []

    for m in memories:
        mid = m.get("id", "")
        if not mid:
            continue

        # Get related memories via edges
        related = get_related_memories(mid)
        for r in related[:max_linked]:
            rid = r.get("id", "")
            if rid and rid not in seen_ids:
                # Mark as linked for context
                r["_linked_from"] = m.get("content", "")[:30]
                linked_results.append(r)
                seen_ids.add(rid)

    return linked_results


def _fallback_tag_search(project: str, cwd: str = "") -> list:
    """
    Get contextual memories for project using STRICT tag + content matching.

    Only includes memories that:
    1. Are explicitly tagged with the project name
    2. Contain the project name in content (for credentials, URLs)
    3. Are linked via edges to matched memories

    Does NOT use semantic/vector search to avoid matching unrelated
    framework documentation that happens to be semantically similar.
    """
    if not project or not check_helix_running():
        return []

    results = []
    seen_ids = set()
    project_lower = project.lower()

    # Generate project name variants (handle - vs _ vs space separators)
    project_variants = {
        project_lower,
        project_lower.replace("-", "_"),
        project_lower.replace("-", " "),
        project_lower.replace("_", "-"),
        project_lower.replace("_", " "),
    }

    all_mems = get_all_memories()
    is_wptest = ".wp-test" in cwd.lower() or "wp-test" in project_lower

    # 1. STRICT PROJECT MATCH - tags or content must contain EXACT project name
    for m in all_mems:
        tags = m.get("tags", "").lower()
        content = m.get("content", "").lower()

        # Check for credential indicators
        is_credential = "credential" in tags or any(p in content for p in [' / ', 'password:', 'password=', 'username:', '@', 'sk_'])

        # Strict matching: ONLY exact project name variants
        # No prefix matching - it causes too many false positives
        # e.g., "elementor-agency" should NOT match generic "elementor" tags
        tag_match = any(variant in tags for variant in project_variants)
        content_match = any(variant in content for variant in project_variants)
        wptest_match = is_wptest and "wp-test" in tags

        matches_project = tag_match or content_match or wptest_match

        if matches_project:
            rid = m.get("id", "")
            if rid not in seen_ids:
                # Prioritize credentials and decisions about the project
                results.append(m)
                seen_ids.add(rid)

    # 2. Follow edges ONLY for credential memories (where we need linked details)
    # Don't follow edges for general project context - it breaks project isolation
    credential_results = [m for m in results if
        "credential" in m.get("tags", "").lower() or
        any(p in m.get("content", "").lower() for p in ['password', 'login', 'admin', 'sk_'])]

    if credential_results:
        linked = follow_memory_edges(credential_results, seen_ids, max_linked=2)
        # Only add linked memories that are also project-specific
        for lm in linked:
            lm_tags = lm.get("tags", "").lower()
            lm_content = lm.get("content", "").lower()
            if any(variant in lm_tags or variant in lm_content for variant in project_variants):
                results.append(lm)

    # Sort by importance
    results.sort(key=lambda x: -x.get("importance", 0))
    return results[:6]  # Reduced from 10 to minimize context overhead


def get_project_context(project: str, cwd: str = "") -> list:
    """
    Get project context via graph traversal (fast, complete).

    Priority:
    1. Graph-based lookup via Context node traversal (preferred)
    2. Fallback to tag-based semantic search if graph not built
    """
    if not project or not check_helix_running():
        return []

    # Try graph-based first (preferred - fast and complete)
    memories = get_project_memories_via_graph(project)
    if memories:
        return memories[:6]  # Reduced from 10 to minimize context overhead

    # Fallback to current tag-based search if graph not built yet
    return _fallback_tag_search(project, cwd)


def get_memory_status() -> dict:
    """Get HelixDB status and memory counts."""
    if not check_helix_running():
        return {"running": False, "count": 0, "categories": {}}

    memories = get_all_memories()

    # Count by category
    categories = {}
    for m in memories:
        cat = m.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "running": True,
        "count": len(memories),
        "categories": categories
    }


def get_critical_memories(min_importance: int = 8, project: str = None) -> list:
    """
    Get high-importance memories for session start.

    If project specified, prioritizes project-specific memories first,
    then global critical preferences.

    Returns memories sorted by importance (highest first),
    then by category priority (preferences first).
    """
    if not check_helix_running():
        return []

    memories = get_all_memories()
    if not memories:
        return []

    # Filter by importance
    high_imp = [m for m in memories if m.get("importance", 0) >= min_importance]

    # If project specified, prioritize project-specific memories
    if project:
        project_lower = project.lower()
        project_memories = []
        global_memories = []

        for m in high_imp:
            tags = m.get("tags", "").lower()
            if project_lower in tags:
                project_memories.append(m)
            else:
                global_memories.append(m)

        # Sort each group by importance
        category_priority = {"preference": 0, "decision": 1, "fact": 2, "solution": 3, "context": 4, "task": 5}
        sort_key = lambda x: (-x.get("importance", 0), category_priority.get(x.get("category", ""), 6))

        project_memories.sort(key=sort_key)
        global_memories.sort(key=sort_key)

        # Combine: project-specific first (top 3), then global (top 3)
        # Reduced from 5+5 to minimize context overhead; use /recall for more
        return project_memories[:3] + global_memories[:3]

    # No project filter - just sort all
    category_priority = {"preference": 0, "decision": 1, "fact": 2, "context": 3, "task": 4}
    high_imp.sort(key=lambda x: (
        -x.get("importance", 0),
        category_priority.get(x.get("category", ""), 5)
    ))

    return high_imp[:6]  # Reduced from 10 to minimize context overhead


def format_session_context(status: dict, memories: list, project: str = None, project_context: list = None) -> str:
    """Format status and memories as session start context.

    OPTIMIZED: Minimal context injection to reduce token overhead.
    Only loads importance>=9 memories (truly critical preferences).
    Use /recall or trigger words to load more context on-demand.
    """
    parts = []

    # Minimal status - just availability notice
    if status["running"]:
        parts.append(f"HelixDB Memory: ACTIVE ({status['count']} memories available)")
        parts.append("Use 'recall' or 'remember' in prompts to load relevant context.")
    else:
        parts.append("HelixDB Memory: NOT RUNNING")
        return "\n".join(parts)

    # Only show importance>=9 (truly critical, ~10-15 items max)
    if memories:
        parts.append("\n## Critical Preferences (importance ≥9):\n")
        for m in memories:
            cat = m.get("category", "unknown").upper()
            imp = m.get("importance", "?")
            content = m.get("content", "")
            parts.append(f"[{cat} - {imp}] {content}\n")

        # Count lower-importance memories not shown
        all_count = status.get("count", 0)
        shown_count = len(memories)
        hidden_count = all_count - shown_count
        if hidden_count > 0:
            parts.append(f"\n📚 {hidden_count} more memories available (importance <9). Use `/recall <topic>` to search.")

    # Project context (credentials, structure, purpose)
    if project:
        parts.append(f"\n## Current Project: {project}")
        if project_context:
            parts.append("🔑 Project context loaded:\n")
            seen_content = set()
            for m in project_context:
                content = m.get("content", "")
                # Dedupe and truncate
                if content not in seen_content:
                    seen_content.add(content)
                    cat = m.get("category", "info").upper()
                    truncated = content[:100] + "..." if len(content) > 100 else content

                    # Show if found via edge
                    if m.get("_linked_from"):
                        parts.append(f"  [{cat}] {truncated}\n    ↳ (linked from: {m['_linked_from']}...)\n")
                    else:
                        parts.append(f"  [{cat}] {truncated}\n")
        parts.append("If you need facts about this project (URLs, credentials, past decisions), ")
        parts.append("use `/recall [topic]` or include 'recall' in your prompt to search memories.")

    return "\n".join(parts)


def main():
    """Main hook execution."""
    # Detect current project
    cwd = os.environ.get('CWD', os.getcwd())
    project = detect_project(cwd)

    # Get status
    status = get_memory_status()

    # Get critical memories (importance>=9, prioritize current project)
    memories = get_critical_memories(min_importance=9, project=project)

    # Get project context (credentials, structure, purpose) via semantic search
    project_context = get_project_context(project, cwd=cwd) if project else []

    # Format context with project info and meta-instruction
    context = format_session_context(status, memories, project=project, project_context=project_context)

    # Return as session start context - using plain text (docs say both work)
    print(context, flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()

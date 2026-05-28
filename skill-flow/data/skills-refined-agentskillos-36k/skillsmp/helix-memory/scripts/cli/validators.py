"""Memory validation and analysis utilities for helix-memory CLI."""

import re
import sys
from typing import List, Dict, Optional

from hooks.common import (
    content_hash,
    search_by_similarity,
    calculate_semantic_similarity,
    get_related_memories
)


# ============================================================================
# GARBAGE DETECTION PATTERNS
# ============================================================================

GARBAGE_PATTERNS = [
    r"^(yes|no|ok|done|thanks)\.?$",  # Too short/vague
    r"were provided\.?$",              # Vague reference
    r"was (set|created|updated)\.?$",  # Vague without specifics
    r"^The (user|assistant) ",         # Meta-description
    r'^<bash-',                         # Bash output markers
    r'bash-stdout|bash-stderr',
    r'^\[.*\]$',                        # Single bracketed content
    r'^Perfect!',                       # Generic acknowledgments
    r'^Done!',
    r'^Great!',
    r'^Let me',                         # Task narration
    r'^Now let me',
    r'^Now I',
    r"^I'll",
    r"^I'm going to",
    r'^\s*\[\d+',                       # Line number prefixes
    r'^\s*cat /',                       # Raw cat output
    r'server\s*\{',                     # Nginx configs
    r'location\s*~',
    r'#!/bin/bash',                     # Script content
    r'#!/usr/bin/env',
    r'^Base directory for this skill:', # Skill loading
    r'This session is being continued', # Session continuations
    r'\[38;5;',                         # Terminal escape codes
    r'\[\?2026',
    r'^Project path:.*Context:.*<bash', # Corrupted path+bash combo
    r'^Project location:.*`\)',         # Malformed path
]


def is_garbage(content: str) -> bool:
    """Check if content matches garbage patterns."""
    content = content.strip()

    # Too short
    if len(content) < 20:
        return True

    for pattern in GARBAGE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            return True
    return False


def is_corrupted(content: str) -> bool:
    """Check for corrupted/malformed memories."""
    content = content.strip()
    if len(content) < 20:
        return True
    if content.startswith(('@', '[?', '</', '`)', '...')):
        return True
    if content.count('<bash') != content.count('</bash'):
        return True
    return False


class MemoryAnalysis:
    """Result of analyzing a single memory."""
    def __init__(self, memory_id: str):
        self.id = memory_id
        self.action = "keep"  # keep, delete, merge, link
        self.reason = ""
        self.related_ids = []  # List of (id, similarity, relationship_type)
        self.duplicate_of = None  # If duplicate, ID of the original
        self.similarity_score = 0.0
        self.quality_score = 0  # 0-10
        self.issues = []  # List of detected issues


def analyze_memory(memory: dict, cache: dict) -> MemoryAnalysis:
    """
    Deeply analyze a single memory and determine what to do with it.

    Considers:
    - Content quality (length, structure, patterns)
    - Duplicate detection via hash and semantic similarity
    - Relationship mapping to other memories
    - Category-specific rules

    Returns MemoryAnalysis with recommended action and reasoning.
    """
    mid = memory.get('id', '')
    content = memory.get('content', '')
    category = memory.get('category', '')
    importance = memory.get('importance', 5)
    tags = memory.get('tags', '')

    analysis = MemoryAnalysis(mid)

    # === STEP 1: Quality Assessment ===

    # Check for corrupted content
    if is_corrupted(content):
        analysis.action = "delete"
        analysis.reason = "Corrupted content (truncated, malformed, or too short)"
        analysis.quality_score = 0
        analysis.issues.append("corrupted")
        return analysis

    # Check for garbage patterns
    if is_garbage(content):
        analysis.action = "delete"
        analysis.reason = "Low-value content (task narration, bash output, generic acknowledgment)"
        analysis.quality_score = 1
        analysis.issues.append("garbage_pattern")
        return analysis

    # Calculate base quality score
    quality = importance
    if len(content) > 100:
        quality += 1
    if len(content) > 200:
        quality += 1
    if tags and len(tags) > 3:
        quality += 1
    if category in ('preference', 'decision', 'solution'):
        quality += 1  # High-value categories
    analysis.quality_score = min(10, quality)

    # === STEP 2: Exact Duplicate Detection (via hash) ===

    c_hash = content_hash(content)
    if c_hash in cache.get('hashes', {}):
        existing_id = cache['hashes'][c_hash]
        if existing_id != mid:
            analysis.action = "merge"
            analysis.duplicate_of = existing_id
            analysis.similarity_score = 1.0
            analysis.reason = f"Exact duplicate of {existing_id[:8]}"
            return analysis
    else:
        cache.setdefault('hashes', {})[c_hash] = mid

    # === STEP 3: Semantic Similarity Search ===

    try:
        # Find semantically similar memories using vector search
        similar = search_by_similarity(content, k=8, window="full")

        for s in similar:
            sid = s.get('id', '')
            if sid == mid:
                continue

            # Calculate actual semantic similarity using embeddings
            try:
                sim_score = calculate_semantic_similarity(content, s.get('content', ''))
            except Exception as e:
                analysis.issues.append(f"similarity_calc_error: {e}")
                continue

            # Validate similarity score
            if not (0 <= sim_score <= 1):
                continue

            # High similarity (>0.90) = potential duplicate
            if sim_score >= 0.90:
                s_importance = s.get('importance', 5)
                if importance >= s_importance:
                    # This memory is better/equal, mark other as superseded
                    analysis.related_ids.append((sid, sim_score, "supersedes"))
                else:
                    # Other memory is better, this one should merge
                    analysis.action = "merge"
                    analysis.duplicate_of = sid
                    analysis.similarity_score = sim_score
                    analysis.reason = f"Duplicate of higher-importance memory {sid[:8]} ({sim_score:.0%} similar)"
                    return analysis

            # Moderate similarity (0.65-0.90) = related, should link
            elif sim_score >= 0.65:
                # Determine relationship type based on categories
                s_cat = s.get('category', '')

                if category == 'decision' and s_cat == 'solution':
                    rel_type = 'implies'
                elif category == 'problem' and s_cat == 'solution':
                    rel_type = 'leads_to'
                elif category == 'fact' and s_cat == 'preference':
                    rel_type = 'supports'
                else:
                    rel_type = 'related'

                analysis.related_ids.append((sid, sim_score, rel_type))

    except Exception as e:
        analysis.issues.append(f"similarity_search_error: {e}")

    # === STEP 4: Check Existing Edges ===

    try:
        existing_edges = get_related_memories(mid)
        has_sufficient_edges = len(existing_edges) >= 2
    except Exception:
        has_sufficient_edges = False
        analysis.issues.append("edge_check_failed")

    # === STEP 5: Determine Final Action ===

    if analysis.action == "merge":
        # Already set in duplicate detection
        pass
    elif analysis.related_ids and not has_sufficient_edges:
        analysis.action = "link"
        analysis.reason = f"Found {len(analysis.related_ids)} related memories to connect"
    elif analysis.quality_score >= 7:
        analysis.action = "keep"
        analysis.reason = "High quality memory, well-connected"
    else:
        analysis.action = "keep"
        analysis.reason = "Acceptable quality, no issues"

    return analysis

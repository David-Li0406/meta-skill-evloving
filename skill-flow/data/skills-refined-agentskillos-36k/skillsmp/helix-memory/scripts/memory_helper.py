#!/usr/bin/env python3
"""
Memory Helper - CLI tool for helix-memory operations.
Provides simple commands for storing, searching, and listing memories.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from hooks.common import (
    store_memory,
    get_all_memories,
    check_helix_running,
    ensure_helix_running,
    find_similar_memories,
    delete_memory,
    update_memory_tags,
    llm_generate,
    extract_json_array,
    hybrid_search,
    generate_embedding,
    store_memory_embedding,
    contextual_search,
    detect_environment_from_path,
    link_memory_to_environment,
    build_project_graph_from_tags,
    get_project_memories_via_graph,
    get_related_memories,
    clean_orphaned_contexts,
    HELIX_URL,
    VALID_CATEGORIES,
    normalize_category,
)
from cli.utils import (
    requires_helix,
    resolve_memory_id,
    parse_date_arg,
    parse_memory_timestamp,
    filter_memories_by_date
)
from cli.formatters import format_memory_detail
from cli.validators import (
    is_garbage,
    is_corrupted,
    GARBAGE_PATTERNS,
    MemoryAnalysis,
    analyze_memory
)
import requests
import os


def cmd_store(args):
    """Store a new memory."""
    if not ensure_helix_running():
        print("ERROR: HelixDB not running", file=sys.stderr)
        sys.exit(1)

    # Check for duplicates
    similar = find_similar_memories(args.content, args.category, args.tags)
    if similar:
        print(f"WARNING: Found {len(similar)} similar memory(ies):", file=sys.stderr)
        for m in similar[:3]:
            print(f"  - [{m.get('category')}] {m.get('content')[:60]}...", file=sys.stderr)
        if not args.force:
            print("Use --force to store anyway", file=sys.stderr)
            sys.exit(1)

    memory_id = store_memory(args.content, args.category, args.importance, args.tags)
    if memory_id:
        print(f"Stored memory: {memory_id}")
        print(f"  Category: {args.category}")
        print(f"  Importance: {args.importance}")
        print(f"  Tags: {args.tags}")

        # Handle --solves flag: link this solution to a problem
        if args.solves:
            from hooks.common import link_related_memories
            memories = get_all_memories()
            problem_id = resolve_memory_id(args.solves, memories)
            if link_related_memories(memory_id, problem_id, "solves", 8):
                print(f"  Solves: {problem_id[:8]}...")
            else:
                print(f"  WARNING: Failed to create solves link to {args.solves}", file=sys.stderr)
    else:
        print("ERROR: Failed to store memory", file=sys.stderr)
        sys.exit(1)

@requires_helix
def cmd_search(args):
    """Search memories using vector/semantic search + text matching."""
    query_lower = args.query.lower()

    # Credential-related keywords that trigger tag-first search
    CREDENTIAL_KEYWORDS = {
        'credential', 'credentials', 'password', 'passwords', 'login', 'logins',
        'secret', 'secrets', 'token', 'tokens', 'api key', 'api keys', 'apikey',
        'auth', 'authentication', 'username', 'usernames', 'admin password',
        'access key', 'ssh key', 'private key', 'api_key'
    }

    # Check if query contains credential keywords
    is_credential_query = any(kw in query_lower for kw in CREDENTIAL_KEYWORDS)

    matches = []
    total_matches = 0  # Track total before limiting
    search_type = ""

    # Detect current project from cwd for context boosting
    cwd = os.getcwd()
    project = os.path.basename(cwd).lower()

    if is_credential_query:
        # CREDENTIAL SEARCH: Tag-first approach
        all_memories = get_all_memories()
        tag_matches = [m for m in all_memories if 'credentials' in m.get('tags', '').lower()]
        content_matches = [m for m in all_memories
                          if any(kw in m.get('content', '').lower() for kw in CREDENTIAL_KEYWORDS)
                          and m not in tag_matches]

        # Extract context terms (exclude credential keywords from boosting)
        project_terms = [t.strip() for t in query_lower.split()
                         if len(t) > 2 and t not in CREDENTIAL_KEYWORDS]

        # Combine and score results
        seen_ids = set()
        scored_matches = []

        for m in tag_matches:
            mid = m.get('id')
            if mid in seen_ids:
                continue
            seen_ids.add(mid)
            score = 100  # Base score for tag match
            content_lower = m.get('content', '').lower()
            tags_lower = m.get('tags', '').lower()

            # Boost if matches project context
            if project and (project in content_lower or project in tags_lower):
                score += 50
            for term in project_terms:
                if term in content_lower or term in tags_lower:
                    score += 10
            scored_matches.append((score, m))

        for m in content_matches:
            mid = m.get('id')
            if mid in seen_ids:
                continue
            seen_ids.add(mid)
            score = 50  # Lower base score for content match
            content_lower = m.get('content', '').lower()
            tags_lower = m.get('tags', '').lower()

            if project and (project in content_lower or project in tags_lower):
                score += 50
            for term in project_terms:
                if term in content_lower or term in tags_lower:
                    score += 10
            scored_matches.append((score, m))

        scored_matches.sort(key=lambda x: x[0], reverse=True)
        total_matches = len(scored_matches)
        matches = [m for _, m in scored_matches[:args.limit]]
        search_type = "credential-tag"

        if not matches:
            matches = hybrid_search(args.query, k=args.limit, window="full")
            total_matches = len(matches)
            search_type = "hybrid (fallback)"

    elif args.contextual:
        matches = contextual_search(args.query, k=args.limit, cwd=cwd)
        total_matches = len(matches)
        search_type = "contextual"
    else:
        # Get more than limit to know total available
        all_results = hybrid_search(args.query, k=50, window="full")
        total_matches = len(all_results)
        matches = all_results[:args.limit]
        search_type = "hybrid"

    if not matches:
        print("No memories found matching query")
        return

    # Show context info if project detected and boosting applied
    if project and project not in ['tools', 'users', 'cminds', 'home']:
        print(f"📍 Context: {project} (boosting matches)")

    # Hint for verbose credential queries
    if is_credential_query and len(query_lower.split()) > 2:
        print("💡 Tip: Use short queries like 'projectname credentials'")

    print(f"\nFound {len(matches)} of {total_matches} matches ({search_type}):\n")
    for m in matches:
        importance = m.get('importance', '?')
        category = m.get('category', 'unknown').upper()
        content = m.get('content', '')
        if not args.full:
            content = content[:100] + ('...' if len(content) > 100 else '')
        tags = m.get('tags', '')
        mid = m.get('id', '')
        print(f"[{category} - {importance}] {content}")
        print(f"  Tags: {tags}")
        print(f"  ID: {mid}\n")

    # Show "more available" hint
    if total_matches > args.limit:
        print(f"📋 {total_matches - args.limit} more available. Use: memory search \"{args.query}\" -n {min(total_matches, 20)}")

@requires_helix
def cmd_list(args):
    """List all memories."""
    memories = get_all_memories()

    # Handle positional limit (memory list 20) OR --limit/-n flag
    limit = args.limit_positional or args.limit

    if args.category:
        memories = [m for m in memories if m.get('category') == args.category]

    # Date filtering via UUID v7 timestamp
    show_dates = False
    since_date = None
    exact_date = None

    if args.since:
        since_date = parse_date_arg(args.since)
        if not since_date:
            print(f"ERROR: Invalid date format: {args.since}", file=sys.stderr)
            print("Use: yesterday, today, YYYY-MM-DD, or 'N days ago'", file=sys.stderr)
            sys.exit(1)
        show_dates = True

    if args.date:
        exact_date = parse_date_arg(args.date)
        if not exact_date:
            print(f"ERROR: Invalid date format: {args.date}", file=sys.stderr)
            print("Use: yesterday, today, or YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        show_dates = True

    # Filter memories by date
    if since_date or exact_date:
        memories = filter_memories_by_date(memories, since_date, exact_date)

    # Sort by importance (desc), or by date if filtering
    if show_dates:
        memories.sort(key=lambda m: m.get('_created_at', datetime.min), reverse=True)
    else:
        memories.sort(key=lambda m: m.get('importance', 0), reverse=True)

    if limit:
        memories = memories[:limit]

    if not memories:
        print("No memories found")
        return

    print(f"Total: {len(memories)} memories\n")
    for m in memories:
        importance = m.get('importance', '?')
        category = m.get('category', 'unknown').upper()
        content = m.get('content', '')[:80]
        mid = m.get('id', '')

        if show_dates and '_created_at' in m:
            created_str = m['_created_at'].strftime('%Y-%m-%d %H:%M')
            print(f"[{category} - {importance}] {created_str}")
            print(f"  {content}...")
        else:
            print(f"[{category} - {importance}] {content}...")
        print(f"  ID: {mid}\n")

@requires_helix
def cmd_by_tag(args):
    """Get memories by tag."""
    memories = get_all_memories()
    tag = args.tag.lower()

    matches = [m for m in memories if tag in m.get('tags', '').lower()]

    if not matches:
        print(f"No memories found with tag: {args.tag}")
        return

    print(f"Found {len(matches)} memory(ies) with tag '{args.tag}':\n")
    for m in matches:
        importance = m.get('importance', '?')
        category = m.get('category', 'unknown').upper()
        content = m.get('content', '')[:80]
        print(f"[{category} - {importance}] {content}...\n")

@requires_helix
def cmd_creds(args):
    """List/search credentials - dedicated credential recall."""
    memories = get_all_memories()

    # Filter to credentials tag ONLY (strict mode)
    creds = [m for m in memories if 'credentials' in m.get('tags', '').lower()]

    # If no tagged credentials found, also search content (fallback)
    if not creds or args.project:
        # Specific patterns that indicate actual credentials
        CRED_PATTERNS = [' / ', 'password:', 'password=', 'username:', '@', 'sk_', 'whsec_']
        EXCLUDE_PATTERNS = ['password hashing', 'password-protected', 'login persistence',
                            'login flow', 'token cost', 'token usage']
        for m in memories:
            if m in creds:
                continue
            content_lower = m.get('content', '').lower()
            # Skip exclusions
            if any(ex in content_lower for ex in EXCLUDE_PATTERNS):
                continue
            if any(p in content_lower for p in CRED_PATTERNS):
                creds.append(m)

    # Filter by project if specified
    if args.project:
        project = args.project.lower()
        creds = [m for m in creds if project in m.get('content', '').lower()
                 or project in m.get('tags', '').lower()]

    # Sort by importance (highest first), then by tags
    creds.sort(key=lambda m: (-m.get('importance', 0), m.get('tags', '')))

    if not creds:
        if args.project:
            print(f"No credentials found for '{args.project}'")
        else:
            print("No credentials found")
        print("\nTip: Store with: memorize --cred \"project: user/pass\"")
        return

    print(f"Found {len(creds)} credential(s):\n")
    for m in creds:
        importance = m.get('importance', '?')
        content = m.get('content', '')
        tags = m.get('tags', '')
        mid = m.get('id', '')[:8]

        # Highlight the credential content more prominently
        print(f"[{importance}] {content}")
        print(f"    Tags: {tags}  ID: {mid}\n")


@requires_helix
def cmd_migrate_creds(args):
    """Find and tag credentials that are missing the credentials tag."""
    memories = get_all_memories()

    # Specific patterns that indicate actual credentials (not just mentions)
    CRED_PATTERNS = [
        ' / ',           # username / password format
        'password:',     # explicit password
        'password=',     # password assignment
        'login:',        # login credentials
        'username:',     # explicit username
        '@',             # user@host format (SSH)
        'api_key=',      # API key assignment
        'api key:',      # API key label
        'token=',        # token assignment
        'secret:',       # secret label
        'sk_',           # Stripe secret key prefix
        'whsec_',        # Webhook secret prefix
    ]

    # Patterns to EXCLUDE (false positives)
    EXCLUDE_PATTERNS = [
        'password hashing',
        'password-protected',
        'login persistence',
        'login flow',
        'login test',
        'login page',
        'token cost',
        'token usage',
        'token mismatch',
        'session token',
    ]

    # Find memories with credential content but no credentials tag
    untagged = []
    for m in memories:
        tags_lower = m.get('tags', '').lower()
        if 'credentials' in tags_lower:
            continue  # Already tagged
        content_lower = m.get('content', '').lower()

        # Skip if matches exclusion pattern
        if any(ex in content_lower for ex in EXCLUDE_PATTERNS):
            continue

        # Include if matches credential pattern
        if any(p in content_lower for p in CRED_PATTERNS):
            untagged.append(m)

    if not untagged:
        print("All credentials are properly tagged!")
        return

    print(f"Found {len(untagged)} potential credentials without 'credentials' tag:\n")
    for m in untagged[:20]:  # Show first 20
        print(f"  [{m.get('category', '?').upper()}-{m.get('importance', '?')}] {m.get('content', '')[:70]}...")
        print(f"      Current tags: {m.get('tags', '(none)')}")

    if len(untagged) > 20:
        print(f"\n  ... and {len(untagged) - 20} more")

    if args.dry_run:
        print(f"\nDry run: Would add 'credentials' tag to {len(untagged)} memories")
        print("Run with --apply to execute")
        return

    if not args.apply:
        print(f"\nRun with --apply to add 'credentials' tag to these {len(untagged)} memories")
        return

    # Apply the changes
    updated = 0
    for m in untagged:
        mem_id = m.get('id')
        old_tags = m.get('tags', '')
        new_tags = f"{old_tags},credentials" if old_tags else "credentials"
        if update_memory_tags(mem_id, new_tags):
            updated += 1

    print(f"\nUpdated {updated} of {len(untagged)} memories with 'credentials' tag")


@requires_helix
def cmd_delete(args):
    """Delete a memory by ID (supports partial ID prefix matching)."""
    memory_id = args.id

    # Support partial ID matching (prefix)
    if len(memory_id) < 36:  # Full UUID is 36 chars
        memories = get_all_memories()
        memory_id = resolve_memory_id(memory_id, memories)
        print(f"Matched: {memory_id}")

    if delete_memory(memory_id):
        print(f"Deleted memory: {memory_id}")
    else:
        print(f"ERROR: Failed to delete memory: {memory_id}", file=sys.stderr)
        sys.exit(1)

@requires_helix
def cmd_retag(args):
    """Update/replace tags on an existing memory."""
    memory_id = args.id
    memories = get_all_memories()

    # Resolve partial ID
    if len(memory_id) < 36:
        memory_id = resolve_memory_id(memory_id, memories)
        print(f"Matched: {memory_id}")

    # Get current memory to show before/after
    current = next((m for m in memories if m.get('id') == memory_id), None)
    if not current:
        print(f"ERROR: Memory not found: {memory_id}", file=sys.stderr)
        sys.exit(1)

    old_tags = current.get('tags', '')

    # Determine new tags based on mode
    if args.add:
        # Add tag to existing tags
        existing_tags = [t.strip() for t in old_tags.split(',') if t.strip()]
        if args.add not in existing_tags:
            existing_tags.append(args.add)
        new_tags = ','.join(existing_tags)
    elif args.remove:
        # Remove tag from existing tags
        existing_tags = [t.strip() for t in old_tags.split(',') if t.strip()]
        existing_tags = [t for t in existing_tags if t.lower() != args.remove.lower()]
        new_tags = ','.join(existing_tags)
    else:
        # Replace all tags
        new_tags = args.tags if args.tags else ''

    # Show what will change
    print(f"Memory: {current.get('content', '')[:60]}...")
    print(f"  Old tags: {old_tags or '(none)'}")
    print(f"  New tags: {new_tags or '(none)'}")

    if old_tags == new_tags:
        print("No change needed.")
        return

    # Perform the update
    if update_memory_tags(memory_id, new_tags):
        print(f"Successfully retagged memory {memory_id[:8]}...")
    else:
        print(f"ERROR: Failed to retag memory", file=sys.stderr)
        sys.exit(1)


def cmd_categorize(args):
    """Auto-categorize content using LLM (Ollama or Haiku).

    First checks for explicit prefixes in content (TASK:, BUG:, DECISION:, etc.)
    before falling back to LLM categorization.
    """
    import re
    content = args.content
    content_upper = content.strip().upper()

    # Prefix-to-category mapping with default importance
    prefix_map = {
        'TASK:': ('task', 6),
        'BUG:': ('solution', 7),
        'FIX:': ('solution', 7),
        'DECISION:': ('decision', 8),
        'PREFERENCE:': ('preference', 8),
        'PREF:': ('preference', 8),
        'FACT:': ('fact', 5),
        'SOLUTION:': ('solution', 7),
        'LEARNING:': ('fact', 6),
        'TIL:': ('fact', 5),  # Today I Learned
        'NOTE:': ('fact', 4),
        'TODO:': ('task', 5),
        'IMPORTANT:': ('fact', 9),
        'CRITICAL:': ('decision', 10),
    }

    # Check for explicit prefixes
    for prefix, (category, importance) in prefix_map.items():
        if content_upper.startswith(prefix):
            # Extract tags from content (words after common patterns)
            tag_words = re.findall(r'#(\w+)', content)
            tags = ','.join(tag_words) if tag_words else ''
            print(f'{{"category": "{category}", "importance": {importance}, "tags": "{tags}"}}')
            return

    # No prefix found - use LLM
    prompt = f'''Categorize this memory. Return ONLY JSON: {{"category": "preference|fact|decision|solution", "importance": 1-10, "tags": "comma,separated"}}
Memory: {content}'''

    output, provider = llm_generate(prompt, timeout=30)
    if output:
        # Extract JSON object
        match = re.search(r'\{[^}]+\}', output)
        if match:
            print(match.group(0))
            return

    # Fallback: return default
    print('{"category": "fact", "importance": 5, "tags": ""}')

@requires_helix
def cmd_reindex(args):
    """Generate embeddings for all memories that don't have them."""
    memories = get_all_memories()
    print(f"Total memories: {len(memories)}")

    # Count existing embeddings
    to_index = []
    for m in memories:
        mid = m.get('id')
        # Check if embedding exists
        try:
            response = requests.post(
                f"{HELIX_URL}/GetMemoryEmbedding",
                json={"memory_id": mid},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                if not result.get('embedding'):
                    to_index.append(m)
            else:
                to_index.append(m)
        except Exception:
            to_index.append(m)

    if not to_index:
        print("All memories already have embeddings!")
        return

    print(f"Memories to index: {len(to_index)}")

    if not args.force:
        confirm = input(f"Generate embeddings for {len(to_index)} memories? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted")
            return

    # Generate embeddings
    success_count = 0
    error_count = 0

    for i, m in enumerate(to_index, 1):
        mid = m.get('id')
        content = m.get('content', '')

        if not content:
            print(f"[{i}/{len(to_index)}] Skipping memory {mid[:8]} (empty content)")
            continue

        try:
            # Generate embedding
            vector, model = generate_embedding(content)

            # Store it
            if store_memory_embedding(mid, vector, content, model):
                success_count += 1
                print(f"[{i}/{len(to_index)}] Indexed {mid[:8]} using {model}")
            else:
                error_count += 1
                print(f"[{i}/{len(to_index)}] FAILED to store embedding for {mid[:8]}", file=sys.stderr)
        except Exception as e:
            error_count += 1
            print(f"[{i}/{len(to_index)}] ERROR indexing {mid[:8]}: {e}", file=sys.stderr)

    print(f"\nCompleted: {success_count} indexed, {error_count} errors")

@requires_helix
def cmd_link_environments(args):
    """Auto-link memories to their environment contexts based on tags and content."""
    memories = get_all_memories()
    print(f"Analyzing {len(memories)} memories for environment relationships...")

    # Patterns to detect environments
    env_patterns = {
        'wp-test': ['wp-test', 'wordpress', '.wp-test', 'fiverr.loc', 'local wordpress'],
        'docker': ['docker', 'container', 'docker-compose', 'dockerfile'],
        'python-venv': ['venv', 'virtual environment', 'virtualenv', 'pip install'],
        'local-sites': ['.local', '.loc', 'local site'],
    }

    linked_count = 0
    skip_count = 0

    for m in memories:
        content = m.get('content', '').lower()
        tags = m.get('tags', '').lower()
        mid = m.get('id')
        combined = f"{content} {tags}"

        # Detect environment
        detected_env = None
        for env, patterns in env_patterns.items():
            if any(pattern in combined for pattern in patterns):
                detected_env = env
                break

        if detected_env:
            if link_memory_to_environment(mid, detected_env):
                linked_count += 1
                print(f"Linked {mid[:8]} to {detected_env}")
            else:
                skip_count += 1
        else:
            skip_count += 1

    print(f"\nCompleted: {linked_count} memories linked, {skip_count} skipped")

@requires_helix
def cmd_dedup(args):
    """Find and remove duplicate memories."""
    memories = get_all_memories()
    print(f"Analyzing {len(memories)} memories for duplicates...")

    from collections import defaultdict

    # Group by similar content (first N chars + category)
    groups = defaultdict(list)
    for m in memories:
        # Use first 60 chars of content + category as key
        content = m.get('content', '')[:60].strip().lower()
        category = m.get('category', 'unknown').lower()
        key = f"{category}:{content}"
        groups[key].append(m)

    # Find duplicates
    to_delete = []
    for key, mems in groups.items():
        if len(mems) > 1:
            # Sort by importance (highest first), then by ID (keep oldest)
            mems.sort(key=lambda x: (-x.get('importance', 0), x.get('id', '')))
            # Keep first one, mark rest for deletion
            for m in mems[1:]:
                to_delete.append(m)

    if not to_delete:
        print("No duplicates found!")
        return

    print(f"\nFound {len(to_delete)} duplicates:\n")

    # Show what will be deleted
    for m in to_delete[:20]:  # Show first 20
        importance = m.get('importance', '?')
        category = m.get('category', 'unknown').upper()
        content = m.get('content', '')[:50]
        mid = m.get('id', '')
        print(f"  [{category}-{importance}] {content}... ({mid[:8]})")

    if len(to_delete) > 20:
        print(f"  ... and {len(to_delete) - 20} more")

    if args.dry_run:
        print(f"\nDry run - {len(to_delete)} would be deleted")
        return

    if not args.force:
        confirm = input(f"\nDelete {len(to_delete)} duplicates? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted")
            return

    # Delete duplicates
    deleted = 0
    errors = 0
    for m in to_delete:
        mid = m.get('id')
        if delete_memory(mid):
            deleted += 1
        else:
            errors += 1

    print(f"\nDeleted: {deleted}, Errors: {errors}")

@requires_helix
def cmd_status(args):
    """Check HelixDB status."""
    memories = get_all_memories()
    print("HelixDB: RUNNING")
    print(f"Memories: {len(memories)}")

    # Count by category
    categories = {}
    for m in memories:
        cat = m.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    if categories:
        print("\nBy category:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")


def find_semantic_duplicates(memories: list, threshold: float = 0.85, use_vectors: bool = True) -> list:
    """
    Find semantic duplicates using vector similarity OR text prefix matching.
    Returns list of (keep_id, delete_ids, similarity_score) tuples.

    When use_vectors=True (default), uses actual embedding cosine similarity.
    Falls back to prefix matching for speed when vectors unavailable.
    """
    from collections import defaultdict

    duplicates = []
    processed_ids = set()

    if use_vectors:
        # Use vector similarity search from HelixDB
        from hooks.common import search_by_similarity, calculate_semantic_similarity

        for i, m in enumerate(memories):
            mid = m.get('id', '')
            if mid in processed_ids:
                continue

            content = m.get('content', '')
            if len(content) < 20:
                continue

            # Search for similar memories using vector similarity
            similar = search_by_similarity(content, k=15, window="full")

            # Group truly similar ones (>threshold)
            group = [m]
            for s in similar:
                sid = s.get('id', '')
                if sid == mid or sid in processed_ids:
                    continue

                # Calculate actual semantic similarity
                sim_score = calculate_semantic_similarity(content, s.get('content', ''))
                if sim_score >= threshold:
                    group.append(s)
                    processed_ids.add(sid)

            if len(group) > 1:
                # Sort: highest importance first, then oldest ID
                group.sort(key=lambda x: (-x.get('importance', 0), x.get('id', '')))
                keep = group[0]
                delete_ids = [g.get('id') for g in group[1:]]
                avg_sim = threshold  # Approximate
                duplicates.append((keep.get('id'), delete_ids, avg_sim))
                processed_ids.add(mid)

            # Progress indicator
            if i > 0 and i % 100 == 0:
                print(f"  Processed {i}/{len(memories)} memories...", file=sys.stderr)
    else:
        # Fallback: text prefix matching (fast but less accurate)
        groups = defaultdict(list)
        for m in memories:
            content = m.get('content', '')[:60].strip().lower()
            category = m.get('category', 'unknown').lower()
            key = f"{category}:{content}"
            groups[key].append(m)

        for key, group in groups.items():
            if len(group) > 1:
                group.sort(key=lambda x: (-x.get('importance', 0), x.get('id', '')))
                keep = group[0]
                delete_ids = [g.get('id') for g in group[1:]]
                duplicates.append((keep.get('id'), delete_ids, 0.90))

    return duplicates


def find_duplicates_fast(memories: list) -> list:
    """
    Fast duplicate detection using text prefix + hash.
    Good for initial cleanup, use find_semantic_duplicates for thorough check.
    """
    from collections import defaultdict
    from hooks.common import content_hash

    # Group by content hash (exact duplicates)
    hash_groups = defaultdict(list)
    for m in memories:
        h = content_hash(m.get('content', ''))
        hash_groups[h].append(m)

    duplicates = []
    for h, group in hash_groups.items():
        if len(group) > 1:
            group.sort(key=lambda x: (-x.get('importance', 0), x.get('id', '')))
            keep = group[0]
            delete_ids = [g.get('id') for g in group[1:]]
            duplicates.append((keep.get('id'), delete_ids, 1.0))  # Exact match

    # Also check prefix matches within same category
    prefix_groups = defaultdict(list)
    seen_ids = {d[0] for d in duplicates} | {did for d in duplicates for did in d[1]}

    for m in memories:
        if m.get('id') in seen_ids:
            continue
        content = m.get('content', '')[:60].strip().lower()
        category = m.get('category', 'unknown').lower()
        key = f"{category}:{content}"
        prefix_groups[key].append(m)

    for key, group in prefix_groups.items():
        if len(group) > 1:
            group.sort(key=lambda x: (-x.get('importance', 0), x.get('id', '')))
            keep = group[0]
            delete_ids = [g.get('id') for g in group[1:]]
            duplicates.append((keep.get('id'), delete_ids, 0.90))

    return duplicates


@requires_helix
def cmd_health(args):
    """Show memory health report with vector-based duplicate detection."""
    memories = get_all_memories()
    total = len(memories)

    # Find duplicates - fast mode uses hash+prefix, thorough uses vectors
    if args.thorough:
        print("Analyzing with vector similarity (may take a few minutes)...", file=sys.stderr)
        duplicates = find_semantic_duplicates(memories, threshold=0.85, use_vectors=True)
    else:
        duplicates = find_duplicates_fast(memories)
    dup_count = sum(len(d[1]) for d in duplicates)

    # Find garbage
    garbage = [m for m in memories if is_garbage(m.get('content', '')) or is_corrupted(m.get('content', ''))]

    # Category counts
    categories = {}
    for m in memories:
        cat = m.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    # Importance distribution
    importance_dist = {}
    for m in memories:
        imp = m.get('importance', 0)
        importance_dist[imp] = importance_dist.get(imp, 0) + 1

    # Check for linked memories (graph connectivity)
    from hooks.common import get_related_memories
    linked_count = 0
    orphan_count = 0
    for m in memories[:100]:  # Sample first 100 for speed
        related = get_related_memories(m.get('id', ''))
        if related:
            linked_count += 1
        else:
            orphan_count += 1

    print("=" * 50)
    print("MEMORY HEALTH REPORT")
    print("=" * 50)
    print(f"\nTotal Memories: {total}")
    print(f"Duplicates:     {dup_count} (in {len(duplicates)} groups)")
    print(f"Garbage:        {len(garbage)}")
    print(f"Linked:         ~{linked_count}% (sampled)")
    print(f"Orphans:        ~{orphan_count}% (no edges)")
    print(f"Clean:          {total - dup_count - len(garbage)}")

    print("\nBy Category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"  {cat}: {count}")

    print("\nBy Importance:")
    for imp in sorted(importance_dist.keys(), reverse=True):
        print(f"  {imp}: {importance_dist[imp]}")

    if args.verbose:
        if duplicates:
            print("\n--- Duplicate Groups (first 5) ---")
            for keep_id, delete_ids, sim_score in duplicates[:5]:
                keep_mem = next((m for m in memories if m.get('id') == keep_id), {})
                print(f"\nKEEP [{keep_mem.get('importance', '?')}]: {keep_mem.get('content', '')[:60]}...")
                print(f"  DELETE: {len(delete_ids)} duplicate(s) @ {sim_score:.0%} similarity")

        if garbage:
            print("\n--- Garbage (first 5) ---")
            for m in garbage[:5]:
                print(f"  [{m.get('category', '?')}] {m.get('content', '')[:50]}...")

    # Recommendations
    print("\n--- Recommendations ---")
    if dup_count > 0:
        print(f"  Run 'memory dedup' to remove {dup_count} duplicates")
    if len(garbage) > 0:
        print(f"  Run 'memory garbage' to remove {len(garbage)} garbage entries")
    if orphan_count > 50:
        print(f"  Run 'memory link-all' to create edges between related memories")


@requires_helix
def cmd_garbage(args):
    """Find and optionally delete garbage memories."""
    memories = get_all_memories()
    garbage = []

    for m in memories:
        content = m.get('content', '')
        reason = None

        if is_corrupted(content):
            reason = "corrupted"
        elif is_garbage(content):
            reason = "garbage"

        if reason:
            garbage.append((m, reason))

    if not garbage:
        print("No garbage found!")
        return

    print(f"Found {len(garbage)} garbage memories:\n")

    for m, reason in garbage[:30]:
        mid = m.get('id', '')[:8]
        cat = m.get('category', '?')
        content = m.get('content', '')[:50].replace('\n', ' ')
        print(f"  [{cat}] {mid}... {content}... ({reason})")

    if len(garbage) > 30:
        print(f"  ... and {len(garbage) - 30} more")

    if args.dry_run:
        print(f"\nDry run - {len(garbage)} would be deleted")
        return

    if not args.force:
        confirm = input(f"\nDelete {len(garbage)} garbage memories? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted")
            return

    # Delete
    deleted = 0
    errors = 0
    for m, _ in garbage:
        if delete_memory(m.get('id')):
            deleted += 1
        else:
            errors += 1

    print(f"\nDeleted: {deleted}, Errors: {errors}")


@requires_helix
def cmd_link(args):
    """Create edge between two memories."""
    from_id = args.from_id
    to_id = args.to_id
    relationship = args.relationship
    strength = args.strength

    # Support partial ID matching
    memories = get_all_memories()

    from_id = resolve_memory_id(from_id, memories)
    to_id = resolve_memory_id(to_id, memories)

    from hooks.common import link_related_memories

    if link_related_memories(from_id, to_id, relationship, strength):
        print(f"Linked: {from_id[:8]}... --[{relationship}]--> {to_id[:8]}...")

        # For solves/solved_by/related relationships, also create reverse edge
        # so both memories can see each other via 'memory show'
        # (cmd_show infers relationship type from memory categories)
        if relationship in ('solves', 'solved_by', 'related'):
            # Use generic 'related' for reverse edge - display is category-based
            response = requests.post(
                f"{HELIX_URL}/LinkRelatedMemories",
                json={"from_id": to_id, "to_id": from_id, "relationship": "related", "strength": strength},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.ok:
                print(f"  (bidirectional edge created)")
    else:
        print("ERROR: Failed to create link", file=sys.stderr)
        sys.exit(1)


@requires_helix
def cmd_merge(args):
    """Merge duplicate memories (keep one, delete others)."""
    keep_id = args.keep_id
    delete_ids = args.delete_ids

    memories = get_all_memories()

    keep_id = resolve_memory_id(keep_id, memories)
    delete_ids = [resolve_memory_id(d, memories) for d in delete_ids]

    # Show what will be merged
    keep_mem = next((m for m in memories if m.get('id') == keep_id), {})
    print(f"KEEP: [{keep_mem.get('category', '?')}] {keep_mem.get('content', '')[:60]}...")

    for did in delete_ids:
        del_mem = next((m for m in memories if m.get('id') == did), {})
        print(f"DELETE: [{del_mem.get('category', '?')}] {del_mem.get('content', '')[:60]}...")

    if args.dry_run:
        print(f"\nDry run - would delete {len(delete_ids)} memories")
        return

    if not args.force:
        confirm = input(f"\nMerge {len(delete_ids)} into keeper? [y/N] ")
        if confirm.lower() != 'y':
            print("Aborted")
            return

    # Create supersedes edges then delete
    from hooks.common import create_supersedes

    deleted = 0
    for did in delete_ids:
        # Create supersedes edge
        create_supersedes(keep_id, did)
        # Delete the duplicate
        if delete_memory(did):
            deleted += 1
            print(f"  Deleted: {did[:8]}...")

    print(f"\nMerged: {deleted} memories into {keep_id[:8]}...")


def cmd_curate(args):
    """
    Intelligently curate all memories with phased workflow.

    Phases:
    - analyze: Run full analysis, save pending actions to file
    - review: Show pending actions for Claude to review
    - apply: Execute pending actions (with optional filters)

    This non-interactive design allows background execution and
    lets Claude decide what actions to take.
    """
    from pathlib import Path
    import time
    import json as json_lib

    pending_path = Path.home() / ".cache/helix-memory/pending_curate.json"
    pending_path.parent.mkdir(parents=True, exist_ok=True)

    # === REVIEW PHASE ===
    if args.action == 'review':
        if not pending_path.exists():
            print("No pending curation. Run 'curate analyze' first.")
            sys.exit(1)

        with open(pending_path) as f:
            pending = json_lib.load(f)

        print("=" * 60)
        print("PENDING CURATION ACTIONS")
        print("=" * 60)
        print(f"Analyzed:  {pending.get('timestamp', 'unknown')}")
        print(f"Delete:    {len(pending.get('delete', []))} memories")
        print(f"Merge:     {len(pending.get('merge', []))} duplicates")
        print(f"Link:      {len(pending.get('link', []))} memories")

        if pending.get('delete'):
            print(f"\n--- Delete Candidates ---")
            for d in pending['delete'][:5]:
                print(f"  {d['id'][:8]}: {d['reason'][:50]}")
            if len(pending['delete']) > 5:
                print(f"  ... and {len(pending['delete']) - 5} more")

        if pending.get('merge'):
            print(f"\n--- Merge Candidates ---")
            for m in pending['merge'][:5]:
                print(f"  {m['id'][:8]} → {m['into'][:8]} (sim={m['similarity']:.2f})")
            if len(pending['merge']) > 5:
                print(f"  ... and {len(pending['merge']) - 5} more")

        if pending.get('link'):
            print(f"\n--- Link Candidates ---")
            print(f"  {len(pending['link'])} memories need edges")

        print(f"\nTo apply: curate apply [--links-only|--deletes-only|--merges-only]")
        return

    # === APPLY PHASE ===
    if args.action == 'apply':
        if not check_helix_running():
            print("ERROR: HelixDB not running", file=sys.stderr)
            sys.exit(1)

        if not pending_path.exists():
            print("No pending curation. Run 'curate analyze' first.")
            sys.exit(1)

        with open(pending_path) as f:
            pending = json_lib.load(f)

        applied = {'deleted': 0, 'merged': 0, 'linked': 0}

        # Apply deletes
        if pending.get('delete') and not args.links_only and not args.merges_only:
            print(f"Deleting {len(pending['delete'])} garbage memories...")
            for d in pending['delete']:
                try:
                    if delete_memory(d['id']):
                        applied['deleted'] += 1
                except Exception:
                    pass

        # Apply merges (delete duplicates, keeping the referenced 'into')
        if pending.get('merge') and not args.links_only and not args.deletes_only:
            print(f"Merging {len(pending['merge'])} duplicates...")
            for m in pending['merge']:
                try:
                    if delete_memory(m['id']):
                        applied['merged'] += 1
                except Exception:
                    pass

        # Apply links
        if pending.get('link') and not args.deletes_only and not args.merges_only:
            from hooks.common import link_related_memories
            total_links = len(pending['link'])
            print(f"Linking {total_links} memories...", flush=True)
            for i, lnk in enumerate(pending['link']):
                for related_id, sim_score, rel_type in lnk.get('related', [])[:3]:
                    try:
                        strength = int(sim_score * 10)
                        if link_related_memories(lnk['id'], related_id, rel_type, strength):
                            applied['linked'] += 1
                        if link_related_memories(related_id, lnk['id'], rel_type, strength):
                            applied['linked'] += 1
                    except Exception:
                        pass
                # Progress every 100 memories
                if (i + 1) % 100 == 0:
                    print(f"  [{i+1}/{total_links}] {applied['linked']} edges created", flush=True)

        print(f"\nApplied: {applied['deleted']} deleted, {applied['merged']} merged, {applied['linked']} edges")

        # Clear pending if all applied
        if not args.links_only and not args.deletes_only and not args.merges_only:
            pending_path.unlink(missing_ok=True)
            print("Pending actions cleared.")
        return

    # === ANALYZE PHASE (default) ===
    if not check_helix_running():
        print("ERROR: HelixDB not running", file=sys.stderr)
        sys.exit(1)

    memories = get_all_memories()
    total = len(memories)
    cache = {'hashes': {}}
    results = {'keep': [], 'delete': [], 'merge': [], 'link': []}

    print(f"Analyzing {total} memories...", flush=True)
    print("=" * 60, flush=True)

    start_time = time.time()
    error_count = 0

    for i, m in enumerate(memories):
        try:
            analysis = analyze_memory(m, cache)
            results[analysis.action].append(analysis)

            if analysis.action != 'keep':
                symbols = {'delete': '✗', 'merge': '⊕', 'link': '⟷'}
                print(f"[{i+1:4d}/{total}] {symbols[analysis.action]} {m.get('id', '')[:8]} {analysis.reason[:45]}", flush=True)
            elif args.verbose:
                print(f"[{i+1:4d}/{total}] ✓ {m.get('id', '')[:8]} quality={analysis.quality_score}", flush=True)
        except Exception as e:
            error_count += 1
            if args.verbose:
                print(f"[{i+1:4d}/{total}] ERROR: {e}", file=sys.stderr, flush=True)

        if (i + 1) % 25 == 0:
            time.sleep(0.3)

    elapsed = time.time() - start_time

    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Analyzed:  {total} memories in {elapsed:.1f}s")
    print(f"Keep:      {len(results['keep']):4d}")
    print(f"Delete:    {len(results['delete']):4d}")
    print(f"Merge:     {len(results['merge']):4d}")
    print(f"Link:      {len(results['link']):4d}")
    print(f"Errors:    {error_count:4d}")

    # Save pending actions
    pending = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_analyzed': total,
        'elapsed_seconds': elapsed,
        'delete': [{'id': a.id, 'reason': a.reason, 'issues': a.issues} for a in results['delete']],
        'merge': [{'id': a.id, 'into': a.duplicate_of, 'similarity': a.similarity_score} for a in results['merge']],
        'link': [{'id': a.id, 'related': [(r[0], r[1], r[2]) for r in a.related_ids]} for a in results['link']],
    }

    with open(pending_path, 'w') as f:
        json_lib.dump(pending, f, indent=2)

    print(f"\nPending actions saved: {pending_path}")
    print(f"Next: 'curate review' to inspect, 'curate apply' to execute")


@requires_helix
def cmd_migrate(args):
    """
    Migrate memories with invalid categories to valid ones.

    Shows all memories that have categories not in VALID_CATEGORIES,
    displays the mapping that would be applied, and with --apply
    actually updates them.
    """
    memories = get_all_memories()
    print(f"Scanning {len(memories)} memories for invalid categories...\n")

    # Find memories with invalid categories
    invalid = []
    for m in memories:
        cat = m.get('category', '')
        cat_lower = cat.lower() if cat else ''
        if cat_lower not in VALID_CATEGORIES:
            new_cat = normalize_category(cat)
            invalid.append({
                'memory': m,  # Keep full memory object
                'old_category': cat,
                'new_category': new_cat,
            })

    if not invalid:
        print("All memories have valid categories!")
        return

    # Group by old -> new mapping for summary
    mappings = {}
    for item in invalid:
        key = f"{item['old_category']} -> {item['new_category']}"
        mappings[key] = mappings.get(key, 0) + 1

    print(f"Found {len(invalid)} memories with invalid categories:\n")

    print("Category mappings:")
    for mapping, count in sorted(mappings.items(), key=lambda x: -x[1]):
        print(f"  {mapping}: {count}")

    print(f"\nExamples (first 10):")
    for item in invalid[:10]:
        content = item['memory'].get('content', '')[:60]
        print(f"  [{item['old_category']} -> {item['new_category']}] {content}...")

    if len(invalid) > 10:
        print(f"  ... and {len(invalid) - 10} more")

    if not args.apply:
        print(f"\nDry run complete. Use --apply to migrate {len(invalid)} memories.")
        return

    # Apply migration
    print(f"\nMigrating {len(invalid)} memories...")

    success = 0
    errors = 0

    for item in invalid:
        try:
            mem = item['memory']
            mem_id = mem.get('id')

            # Store new memory with normalized category (full content)
            new_id = store_memory(
                content=mem.get('content', ''),
                category=item['new_category'],
                importance=mem.get('importance', 5),
                tags=mem.get('tags', ''),
                source="migration"
            )

            if new_id:
                # Delete old memory
                if delete_memory(mem_id):
                    success += 1
                    if args.verbose:
                        print(f"  Migrated: {mem_id[:8]}... [{item['old_category']} -> {item['new_category']}]")
                else:
                    errors += 1
                    print(f"  ERROR: Could not delete old memory {mem_id[:8]}", file=sys.stderr)
            else:
                errors += 1
                print(f"  ERROR: Could not create new memory for {mem_id[:8]}", file=sys.stderr)

        except Exception as e:
            errors += 1
            print(f"  ERROR migrating {mem.get('id', '?')[:8]}: {e}", file=sys.stderr)

    print(f"\nMigration complete: {success} migrated, {errors} errors")


@requires_helix
def cmd_projects(args):
    """List projects worked on based on memory tags, cross-referenced with p --list."""
    import subprocess
    from collections import Counter

    # Get known projects from p --list
    try:
        result = subprocess.run(
            ['python3', os.path.expanduser('~/Tools/p'), '--list'],
            capture_output=True, text=True, timeout=5
        )
        known_projects = set()
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                project_name = line.split(':')[0].strip().lower()
                known_projects.add(project_name)
    except Exception as e:
        print(f"ERROR: Could not get project list: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse date filters
    since_date = None
    exact_date = None

    if args.since:
        since_date = parse_date_arg(args.since)
        if not since_date:
            print(f"ERROR: Invalid date format: {args.since}", file=sys.stderr)
            sys.exit(1)
    elif args.date:
        exact_date = parse_date_arg(args.date)
        if not exact_date:
            print(f"ERROR: Invalid date format: {args.date}", file=sys.stderr)
            sys.exit(1)
    else:
        # Default to yesterday
        since_date = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    memories = get_all_memories()
    project_counts = Counter()
    project_memories = {}  # project -> list of memory snippets

    for m in memories:
        created = parse_memory_timestamp(m)
        if not created:
            continue

        # Check date filter
        if since_date and created < since_date:
            continue
        if exact_date:
            next_day = exact_date + timedelta(days=1)
            if not (exact_date <= created < next_day):
                continue

        # Check tags against known projects
        tags = [t.strip().lower() for t in m.get('tags', '').split(',') if t.strip()]
        for tag in tags:
            if tag in known_projects:
                project_counts[tag] += 1
                if tag not in project_memories:
                    project_memories[tag] = []
                if len(project_memories[tag]) < 3:  # Keep top 3 snippets
                    project_memories[tag].append(m.get('content', '')[:60])

    if not project_counts:
        date_desc = f"since {since_date.strftime('%Y-%m-%d')}" if since_date else f"on {exact_date.strftime('%Y-%m-%d')}"
        print(f"No project activity found {date_desc}")
        return

    # Display results
    date_desc = f"since {since_date.strftime('%Y-%m-%d')}" if since_date else f"on {exact_date.strftime('%Y-%m-%d')}"
    print(f"Projects worked on {date_desc}:\n")

    for project, count in project_counts.most_common():
        print(f"  {project}: {count} memories")
        if args.verbose and project in project_memories:
            for snippet in project_memories[project]:
                print(f"    - {snippet}...")
            print()


@requires_helix
def cmd_context(args):
    """Show all infrastructure info (paths, credentials, URLs) for a project."""
    # Get project name from args or cwd
    if args.project:
        project = args.project.lower()
    else:
        project = os.path.basename(os.getcwd()).lower()

    memories = get_all_memories()

    # Keywords that indicate infrastructure/config info
    infra_keywords = [
        'path', 'url', 'ssh', 'rsync', 'staging', 'production', 'live',
        'credential', 'password', 'api key', 'token', 'server', 'host',
        'domain', 'database', 'db', 'port', 'login', 'admin', 'ftp', 'sftp',
        'endpoint', 'secret', 'key', 'ip ', 'cloudflare', 'dns', 'email'
    ]

    # Filter memories that:
    # 1. Match project name in tags or content
    # 2. Contain infrastructure keywords OR are credential/fact category
    matches = []
    for m in memories:
        content = m.get('content', '').lower()
        tags = m.get('tags', '').lower()
        category = m.get('category', '').lower()

        # Must match project
        if project not in content and project not in tags:
            continue

        # Must be infrastructure-related
        is_infra = category in ('credential', 'fact', 'solution')
        if not is_infra:
            for kw in infra_keywords:
                if kw in content or kw in tags:
                    is_infra = True
                    break

        if is_infra:
            matches.append(m)

    # Sort by importance desc
    matches.sort(key=lambda m: m.get('importance', 0), reverse=True)

    if not matches:
        print(f"No infrastructure info found for project: {project}")
        print(f"Tip: Store with tags like '{project}' or mention '{project}' in content")
        return

    print(f"=== {project.upper()} Infrastructure ({len(matches)} items) ===\n")
    for m in matches:
        importance = m.get('importance', '?')
        category = m.get('category', 'unknown').upper()
        content = m.get('content', '')
        tags = m.get('tags', '')
        mid = m.get('id', '')[:8]

        print(f"[{category}-{importance}] {content}")
        if tags:
            print(f"  Tags: {tags}")
        print(f"  ID: {mid}\n")


@requires_helix
def cmd_show(args):
    """Show memory details and its edges, grouped by relationship type."""
    from hooks.common import get_implications, get_contradictions

    mem_id = args.id
    memories = get_all_memories()

    # Find by prefix
    matches = [m for m in memories if m.get('id', '').startswith(mem_id)]
    if not matches:
        print(f"No memory found with ID prefix: {mem_id}")
        sys.exit(1)

    mem = matches[0]
    full_id = mem.get('id')
    category = mem.get('category', '').lower()

    # Print memory details
    print(format_memory_detail(mem))

    # Track all shown IDs to avoid duplicates across sections
    shown_ids = {full_id}
    total_edges = 0

    def print_edge_section(title: str, memories_list: list, limit: int = 5):
        """Helper to print an edge section."""
        nonlocal total_edges
        if not memories_list:
            return
        # Dedupe
        unique = []
        for m in memories_list:
            mid = m.get('id', '')
            if mid and mid not in shown_ids:
                shown_ids.add(mid)
                unique.append(m)
        if not unique:
            return
        total_edges += len(unique)
        print(f"\n{title}")
        for rel in unique[:limit]:
            print(f"  → [{rel.get('category', '?').upper()}-{rel.get('importance', 0)}] {rel.get('id', '?')[:8]}")
            print(f"    {rel.get('content', '')[:60]}...")
        if len(unique) > limit:
            print(f"  ... and {len(unique) - limit} more")

    # Get all related memories first
    all_related = []
    try:
        import requests
        r = requests.post(f"{HELIX_URL}/GetRelatedMemories", json={"memory_id": full_id}, timeout=5)
        data = r.json()
        all_related = data.get('related', [])
    except Exception:
        pass

    # Group related memories by their category to infer relationship type
    # (Until HelixDB stores edge types properly, we infer from memory categories)
    solutions = [m for m in all_related if m.get('category', '').lower() == 'solution']
    problems = [m for m in all_related if m.get('category', '').lower() == 'problem']
    others = [m for m in all_related if m.get('category', '').lower() not in ('solution', 'problem')]

    # 1. SOLVED BY - show solutions for this problem
    if category == 'problem' and solutions:
        print_edge_section("--SOLVED BY--", solutions)

    # 2. SOLVES - show problems this solution solves
    if category == 'solution' and problems:
        print_edge_section("--SOLVES--", problems)

    # 3. IMPLIES - logical implications
    implies = get_implications(full_id)
    print_edge_section("--IMPLIES--", implies)

    # 4. CONTRADICTS - contradicting memories
    contradicts = get_contradictions(full_id)
    print_edge_section("--CONTRADICTS--", contradicts)

    # 5. RELATED - everything else
    # Include solutions/problems if this memory isn't of those types
    remaining = others[:]
    if category != 'problem':
        remaining.extend(solutions)
    if category != 'solution':
        remaining.extend(problems)
    print_edge_section("--RELATED--", remaining, limit=10)

    if total_edges == 0:
        print(f"\n--- No edges (orphan) ---")


@requires_helix
def cmd_graph_build(args):
    """Build project graph from existing memory tags."""
    print("Building project graph from tags...")
    stats = build_project_graph_from_tags()
    print(f"Created {stats.get('projects', 0)} project contexts")
    print(f"Created {stats.get('links_created', 0)} BelongsTo edges")
    if stats.get('errors'):
        print(f"Errors: {stats.get('errors')}")


@requires_helix
def cmd_graph_clean(args):
    """Clean orphaned context nodes that don't match known projects."""
    stats = clean_orphaned_contexts(dry_run=not args.apply)
    if args.apply:
        print(f"\nDeleted {stats.get('deleted', 0)} orphaned contexts")


@requires_helix
def cmd_graph_show(args):
    """Show memories linked to a project via graph with relationship tree."""
    memories = get_project_memories_via_graph(args.project)
    if not memories:
        print(f"No memories linked to project: {args.project}")
        print(f"Tip: Run 'memory graph build' to create project contexts from tags")
        return

    # Track which memories we've shown to avoid duplicates
    shown_ids = set()

    def format_memory(m, prefix=""):
        """Format a single memory line."""
        cat = m.get('category', 'unknown').upper()
        imp = m.get('importance', '?')
        content = m.get('content', '')[:70]
        mid = m.get('id', '')[:8]
        return f"{prefix}[{cat}-{imp}] {content}... ({mid})"

    def show_related(memory_id, depth=0, max_depth=2):
        """Recursively show related memories up to max_depth."""
        if depth >= max_depth:
            return

        related = get_related_memories(memory_id)
        if not related:
            return

        for i, rel in enumerate(related[:3]):  # Limit to 3 per node
            rel_id = rel.get('id', '')
            if rel_id in shown_ids:
                continue
            shown_ids.add(rel_id)

            # Tree branch characters
            is_last = (i == len(related[:3]) - 1)
            branch = "└─→ " if is_last else "├─→ "
            indent = "    " * depth

            print(f"{indent}{branch}{format_memory(rel)}")

            # Recurse for deeper relationships
            show_related(rel_id, depth + 1, max_depth)

    print(f"[{args.project}] Context ({len(memories)} memories)\n")

    # Group by category for better organization
    by_category = {}
    for m in memories:
        cat = m.get('category', 'unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(m)

    # Priority order for categories
    cat_order = ['preference', 'decision', 'fact', 'solution', 'context', 'task', 'problem']

    for cat in cat_order:
        if cat not in by_category:
            continue
        mems = by_category[cat]
        # Sort by importance within category
        mems.sort(key=lambda x: -x.get('importance', 0))

        print(f"── {cat.upper()} ({len(mems)}) ──")

        for m in mems[:5]:  # Top 5 per category
            mid = m.get('id', '')
            if mid in shown_ids:
                continue
            shown_ids.add(mid)

            print(format_memory(m, "├── "))

            # Show relationships for this memory
            show_related(mid, depth=1, max_depth=2)

        if len(mems) > 5:
            print(f"    ... and {len(mems) - 5} more {cat} memories")
        print()


def main():
    parser = argparse.ArgumentParser(description="Helix Memory CLI Helper")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # store command
    store_parser = subparsers.add_parser('store', help='Store a new memory')
    store_parser.add_argument('--content', '-c', required=True, help='Memory content')
    store_parser.add_argument('--category', '-t', default='fact', choices=['preference', 'fact', 'context', 'decision', 'task', 'solution', 'problem'], help='Memory category')
    store_parser.add_argument('--importance', '-i', type=int, default=5, help='Importance 1-10')
    store_parser.add_argument('--tags', '-g', default='', help='Comma-separated tags')
    store_parser.add_argument('--force', '-f', action='store_true', help='Store even if similar exists')
    store_parser.add_argument('--solves', metavar='PROBLEM_ID', help='Link this solution to a problem ID (creates solves edge)')
    store_parser.set_defaults(func=cmd_store)

    # search command
    search_parser = subparsers.add_parser('search', help='Search memories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', '-n', type=int, default=5, help='Max results (default: 5, use -n 20 for more)')
    search_parser.add_argument('--full', '-f', action='store_true', help='Show full content (no truncation)')
    search_parser.add_argument('--contextual', '-c', action='store_true', help='Use contextual/relationship-aware search')
    search_parser.set_defaults(func=cmd_search)

    # list command
    list_parser = subparsers.add_parser('list', help='List all memories')
    list_parser.add_argument('limit_positional', nargs='?', type=int, metavar='N', help='Limit results (shorthand)')
    list_parser.add_argument('--category', '-t', help='Filter by category')
    list_parser.add_argument('--limit', '-n', type=int, help='Limit results')
    list_parser.add_argument('--since', help='Show memories created after date (yesterday, 2026-01-10, "3 days ago")')
    list_parser.add_argument('--date', help='Show memories created on exact date (2026-01-10)')
    list_parser.set_defaults(func=cmd_list)

    # by-tag command
    tag_parser = subparsers.add_parser('by-tag', help='Get memories by tag')
    tag_parser.add_argument('tag', help='Tag to search for')
    tag_parser.set_defaults(func=cmd_by_tag)

    # creds command - dedicated credential listing
    creds_parser = subparsers.add_parser('creds', help='List/search credentials')
    creds_parser.add_argument('project', nargs='?', help='Filter by project name')
    creds_parser.set_defaults(func=cmd_creds)

    # migrate-creds command - tag existing credentials
    migrate_creds_parser = subparsers.add_parser('migrate-creds', help='Tag credentials missing credentials tag')
    migrate_creds_parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be tagged')
    migrate_creds_parser.add_argument('--apply', action='store_true', help='Actually add the tags')
    migrate_creds_parser.set_defaults(func=cmd_migrate_creds)

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a memory')
    delete_parser.add_argument('id', help='Memory ID to delete')
    delete_parser.set_defaults(func=cmd_delete)


    # retag command - update memory tags
    retag_parser = subparsers.add_parser('retag', help='Update/replace tags on a memory')
    retag_parser.add_argument('id', help='Memory ID (prefix OK)')
    retag_parser.add_argument('tags', nargs='?', help='New tags (comma-separated) - replaces all tags')
    retag_parser.add_argument('--add', '-a', help='Add a single tag (keeps existing)')
    retag_parser.add_argument('--remove', '-r', help='Remove a single tag')
    retag_parser.set_defaults(func=cmd_retag)

    # show command - display memory details and edges
    show_parser = subparsers.add_parser('show', help='Show memory details and edges')
    show_parser.add_argument('id', help='Memory ID (prefix OK)')
    show_parser.set_defaults(func=cmd_show)

    # status command
    status_parser = subparsers.add_parser('status', help='Check HelixDB status')
    status_parser.set_defaults(func=cmd_status)

    # projects command - list projects worked on
    projects_parser = subparsers.add_parser('projects', help='List projects worked on (cross-refs with p --list)')
    projects_parser.add_argument('--since', help='Show projects since DATE (default: yesterday)')
    projects_parser.add_argument('--date', help='Show projects on exact DATE')
    projects_parser.add_argument('--verbose', '-v', action='store_true', help='Show memory snippets')
    projects_parser.set_defaults(func=cmd_projects)

    # context command - show project infrastructure
    context_parser = subparsers.add_parser('context', help='Show all paths/credentials/URLs for a project')
    context_parser.add_argument('project', nargs='?', help='Project name (default: current directory)')
    context_parser.set_defaults(func=cmd_context)

    # categorize command (for bash script)
    cat_parser = subparsers.add_parser('categorize', help='Auto-categorize content')
    cat_parser.add_argument('content', help='Content to categorize')
    cat_parser.set_defaults(func=cmd_categorize)

    # reindex command
    reindex_parser = subparsers.add_parser('reindex', help='Generate embeddings for all memories')
    reindex_parser.add_argument('--force', '-f', action='store_true', help='Skip confirmation prompt')
    reindex_parser.set_defaults(func=cmd_reindex)

    # link-environments command
    link_parser = subparsers.add_parser('link-environments', help='Auto-link memories to environment contexts')
    link_parser.set_defaults(func=cmd_link_environments)

    # dedup command
    dedup_parser = subparsers.add_parser('dedup', help='Find and remove duplicate memories')
    dedup_parser.add_argument('--dry-run', '-n', action='store_true', help='Show duplicates without deleting')
    dedup_parser.add_argument('--force', '-f', action='store_true', help='Delete without confirmation')
    dedup_parser.set_defaults(func=cmd_dedup)

    # health command - memory health report
    health_parser = subparsers.add_parser('health', help='Show memory health report')
    health_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed breakdown')
    health_parser.add_argument('--thorough', '-t', action='store_true', help='Use vector similarity (slower but more accurate)')
    health_parser.set_defaults(func=cmd_health)

    # garbage command - find/delete garbage
    garbage_parser = subparsers.add_parser('garbage', help='Find and delete garbage memories')
    garbage_parser.add_argument('--dry-run', '-n', action='store_true', help='Show garbage without deleting')
    garbage_parser.add_argument('--force', '-f', action='store_true', help='Delete without confirmation')
    garbage_parser.set_defaults(func=cmd_garbage)

    # link command - create edge between two memories
    link_cmd = subparsers.add_parser('link', help='Create edge between two memories')
    link_cmd.add_argument('from_id', help='Source memory ID (for solves: solution_id)')
    link_cmd.add_argument('to_id', help='Target memory ID (for solves: problem_id)')
    link_cmd.add_argument('--type', '-t', '--relationship', '-r', dest='relationship', default='related',
                          choices=['related', 'supersedes', 'implies', 'contradicts', 'leads_to', 'supports', 'solves', 'solved_by'],
                          help='Edge type (default: related). solves: from=solution, to=problem. solved_by: from=problem, to=solution')
    link_cmd.add_argument('--strength', '-s', type=int, default=5, help='Edge strength 1-10')
    link_cmd.set_defaults(func=cmd_link)

    # merge command - merge duplicates
    merge_parser = subparsers.add_parser('merge', help='Merge duplicate memories (keep one, delete others)')
    merge_parser.add_argument('keep_id', help='Memory ID to keep (prefix OK)')
    merge_parser.add_argument('delete_ids', nargs='+', help='Memory IDs to delete (prefix OK)')
    merge_parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be merged')
    merge_parser.add_argument('--force', '-f', action='store_true', help='Merge without confirmation')
    merge_parser.set_defaults(func=cmd_merge)

    # curate command - intelligent full curation (phased: analyze → review → apply)
    curate_parser = subparsers.add_parser('curate', help='Intelligent memory curation with analysis')
    curate_parser.add_argument('action', nargs='?', default='analyze',
                               choices=['analyze', 'review', 'apply'],
                               help='Phase: analyze (default), review, or apply')
    curate_parser.add_argument('--verbose', '-v', action='store_true', help='Show all analysis results')
    curate_parser.add_argument('--links-only', action='store_true', help='Apply only link operations')
    curate_parser.add_argument('--deletes-only', action='store_true', help='Apply only delete operations')
    curate_parser.add_argument('--merges-only', action='store_true', help='Apply only merge operations')
    curate_parser.set_defaults(func=cmd_curate)

    # migrate command - fix invalid categories
    migrate_parser = subparsers.add_parser('migrate', help='Migrate memories with invalid categories')
    migrate_parser.add_argument('--apply', '-a', action='store_true', help='Actually apply the migration (default: dry run)')
    migrate_parser.add_argument('--verbose', '-v', action='store_true', help='Show each migration')
    migrate_parser.set_defaults(func=cmd_migrate)

    # graph-build command - build project graph from tags
    graph_build_parser = subparsers.add_parser('graph-build', help='Build project graph from existing memory tags')
    graph_build_parser.set_defaults(func=cmd_graph_build)

    # graph-show command - show memories linked via graph
    graph_show_parser = subparsers.add_parser('graph-show', help='Show memories linked to project via graph')
    graph_show_parser.add_argument('project', help='Project name to query')
    graph_show_parser.set_defaults(func=cmd_graph_show)

    # graph-clean command - clean orphaned contexts
    graph_clean_parser = subparsers.add_parser('graph-clean', help='Clean orphaned context nodes')
    graph_clean_parser.add_argument('--apply', '-a', action='store_true', help='Actually delete (default: dry run)')
    graph_clean_parser.set_defaults(func=cmd_graph_clean)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == '__main__':
    main()

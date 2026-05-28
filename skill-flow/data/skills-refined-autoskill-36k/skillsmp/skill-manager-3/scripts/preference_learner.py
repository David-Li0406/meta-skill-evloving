#!/usr/bin/env python3
"""
preference_learner.py - Learn ACTIONABLE user preferences.

Detects patterns that should change Claude's behavior:
1. Implicit workflows - "commit and push" repeated = always push after commit
2. Bundled commands - "run api and web" = start both together
3. Order preferences - "update docs, commit" = docs before commit
4. Response style - repeated "too long" = keep it short
5. Things to skip - "don't add comments" = avoid unless asked
"""

import json
import re
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set

# Use /home/agent for container environment, fallback to home dir
AGENT_HOME = Path("/home/agent") if Path("/home/agent").exists() else Path.home()
CLAUDE_DIR = Path(os.environ.get('CLAUDE_DIR', AGENT_HOME / ".claude"))
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', CLAUDE_DIR / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
PROMPTS_LOG = PATTERNS_DIR / "user-prompts.jsonl"
LEARNED_FILE = PATTERNS_DIR / "user-preferences.json"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"


def load_prompts(days: int = 30) -> List[str]:
    """Load prompts from log file."""
    prompts = []
    if not PROMPTS_LOG.exists():
        return prompts

    cutoff = datetime.utcnow() - timedelta(days=days)

    with open(PROMPTS_LOG) as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                ts_str = record.get("timestamp", "")
                prompt = record.get("prompt", "")
                if ts_str and prompt and not prompt.startswith("[shell]"):
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts.replace(tzinfo=None) >= cutoff:
                        prompts.append(prompt.lower().strip())
            except:
                continue

    return prompts


def detect_workflow_rules(prompts: List[str]) -> List[dict]:
    """Detect implicit workflow rules from repeated patterns."""
    rules = []

    # Pattern: "X and Y" or "X then Y" repeated = always do Y after X
    combo_patterns = [
        (r'\b(commit)\b.*\b(push)\b', 'after commit', 'push'),
        (r'\b(push)\b.*\b(commit)\b', 'after commit', 'push'),  # reversed
        (r'\b(update docs?).*\b(commit)\b', 'before commit', 'update docs'),
        (r'\b(test).*\b(commit)\b', 'before commit', 'run tests'),
        (r'\b(commit).*\b(test)\b', 'after commit', 'run tests'),
        (r'\b(build).*\b(deploy)\b', 'before deploy', 'build'),
        (r'\b(lint).*\b(commit)\b', 'before commit', 'lint'),
    ]

    combo_counts = Counter()
    for prompt in prompts:
        for pattern, when, action in combo_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                combo_counts[(when, action)] += 1

    # If pattern appears 2+ times, it's a rule
    for (when, action), count in combo_counts.items():
        if count >= 2:
            rules.append({
                "type": "workflow",
                "rule": f"{when}, {action}",
                "confidence": min(count / 3, 1.0),
                "times_seen": count,
            })

    return rules


def detect_bundled_commands(prompts: List[str]) -> List[dict]:
    """Detect things that should run together."""
    bundles = []

    # Pattern: "run X and Y" or "start X and Y"
    bundle_patterns = [
        (r'\b(?:run|start|deploy)\s+(\w+)\s+and\s+(\w+)', 'run together'),
        (r'\b(\w+)\s+and\s+(\w+)\s+(?:server|service)s?', 'run together'),
    ]

    bundle_counts = defaultdict(int)
    for prompt in prompts:
        for pattern, bundle_type in bundle_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    # Normalize order
                    items = tuple(sorted([match[0], match[1]]))
                    bundle_counts[items] += 1

    for items, count in bundle_counts.items():
        if count >= 2:
            bundles.append({
                "type": "bundle",
                "items": list(items),
                "rule": f"run {items[0]} and {items[1]} together",
                "times_seen": count,
            })

    return bundles


def detect_response_preferences(prompts: List[str]) -> List[dict]:
    """Detect preferences about response style."""
    prefs = []

    # Response length
    too_long = sum(1 for p in prompts if 'too long' in p)
    too_short = sum(1 for p in prompts if 'too short' in p or 'more detail' in p)

    if too_long >= 2:
        prefs.append({
            "type": "style",
            "rule": "keep responses concise",
            "reason": f"said 'too long' {too_long} times",
        })
    if too_short >= 2:
        prefs.append({
            "type": "style",
            "rule": "give more detail",
            "reason": f"asked for more detail {too_short} times",
        })

    # Naturalness
    unnatural = sum(1 for p in prompts if 'person wouldn' in p or 'human' in p or 'natural' in p)
    if unnatural >= 1:
        prefs.append({
            "type": "style",
            "rule": "write like a human, not an AI",
            "reason": f"requested natural language {unnatural} times",
        })

    # Formality
    too_formal = sum(1 for p in prompts if 'formal' in p or 'casual' in p)
    if too_formal >= 1:
        # Check which way
        if any('too formal' in p or 'more casual' in p for p in prompts):
            prefs.append({"type": "style", "rule": "be more casual"})
        elif any('more formal' in p or 'too casual' in p for p in prompts):
            prefs.append({"type": "style", "rule": "be more formal"})

    return prefs


def detect_skip_preferences(prompts: List[str]) -> List[dict]:
    """Detect things to NOT do unless asked."""
    skips = []

    skip_patterns = [
        (r"don'?t\s+(?:add|include|put)\s+(\w+)", "skip"),
        (r"no\s+(\w+)\s+(?:please|needed|necessary)", "skip"),
        (r"skip\s+(?:the\s+)?(\w+)", "skip"),
        (r"without\s+(?:the\s+)?(\w+)", "skip"),
    ]

    skip_counts = Counter()
    for prompt in prompts:
        for pattern, _ in skip_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            for match in matches:
                if len(match) > 2:
                    skip_counts[match] += 1

    for item, count in skip_counts.items():
        if count >= 1:  # Even once is significant for "don't" statements
            skips.append({
                "type": "skip",
                "rule": f"don't add {item} unless asked",
                "times_seen": count,
            })

    return skips


def detect_project_context(prompts: List[str]) -> List[dict]:
    """Detect project-specific context."""
    context = []

    # App/project names - look for repeated proper nouns
    words = []
    for p in prompts:
        words.extend(re.findall(r'\b([A-Z][a-z]+|[a-z]+\.(?:pro|com|io|dev|app))\b', p, re.IGNORECASE))

    word_counts = Counter(words)
    # Filter out common words
    common = {'the', 'this', 'that', 'with', 'from', 'have', 'been', 'will',
              'and', 'you', 'for', 'what', 'can', 'how', 'but', 'not', 'are',
              'was', 'were', 'there', 'here', 'when', 'where', 'why', 'who',
              'get', 'got', 'use', 'run', 'add', 'new', 'all', 'some', 'any',
              'like', 'just', 'now', 'then', 'also', 'more', 'about', 'into',
              'make', 'sure', 'want', 'need', 'would', 'could', 'should',
              'warmup', 'test', 'build', 'deploy', 'commit', 'push', 'pull'}
    for word, count in word_counts.most_common(10):
        if word.lower() not in common and count >= 3 and len(word) > 3:
            if '.' in word:
                context.append({"type": "url", "value": word, "times_mentioned": count})
            else:
                context.append({"type": "project_name", "value": word, "times_mentioned": count})

    # Tech stack mentions
    tech_patterns = [
        r'\buse\s+(gemini|openai|anthropic|gpt|claude)',
        r'\b(react|vue|angular|next|nuxt)\b',
        r'\b(python|node|typescript|rust|go)\b',
        r'\b(postgres|mysql|mongo|redis)\b',
    ]

    tech_counts = Counter()
    for prompt in prompts:
        for pattern in tech_patterns:
            matches = re.findall(pattern, prompt, re.IGNORECASE)
            for match in matches:
                tech_counts[match.lower()] += 1

    for tech, count in tech_counts.most_common(5):
        if count >= 2:
            context.append({"type": "tech", "value": tech, "times_mentioned": count})

    return context


def run_preference_learning(verbose: bool = True, update_claude: bool = False) -> dict:
    """Run the preference learning."""
    if verbose:
        print("Learning User Preferences")
        print("=" * 60)

    prompts = load_prompts(days=30)

    if verbose:
        print(f"Analyzing {len(prompts)} prompts...\n")

    if not prompts:
        if verbose:
            print("No prompts to analyze. Run 'manage.py scan' first.")
        return {}

    # Detect all preference types
    workflow_rules = detect_workflow_rules(prompts)
    bundles = detect_bundled_commands(prompts)
    style_prefs = detect_response_preferences(prompts)
    skip_prefs = detect_skip_preferences(prompts)
    context = detect_project_context(prompts)

    # Build learned object
    learned = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "prompts_analyzed": len(prompts),
        "rules": {
            "workflows": workflow_rules,
            "bundles": bundles,
            "style": style_prefs,
            "skip": skip_prefs,
        },
        "context": context,
    }

    # Print results
    if verbose:
        if workflow_rules:
            print("📋 WORKFLOW RULES (do these automatically):")
            for r in workflow_rules:
                print(f"  • {r['rule']} (seen {r['times_seen']}x)")
            print()

        if bundles:
            print("🔗 BUNDLED COMMANDS (run together):")
            for b in bundles:
                print(f"  • {b['rule']} (seen {b['times_seen']}x)")
            print()

        if style_prefs:
            print("✍️  RESPONSE STYLE:")
            for s in style_prefs:
                print(f"  • {s['rule']}")
            print()

        if skip_prefs:
            print("🚫 SKIP UNLESS ASKED:")
            for s in skip_prefs:
                print(f"  • {s['rule']}")
            print()

        if context:
            print("📁 PROJECT CONTEXT:")
            for c in context:
                print(f"  • {c['type']}: {c['value']} (mentioned {c['times_mentioned']}x)")
            print()

    # Save
    try:
        with open(LEARNED_FILE, "w") as f:
            json.dump(learned, f, indent=2)
        if verbose:
            print(f"✅ Saved to: {LEARNED_FILE}")
    except Exception as e:
        if verbose:
            print(f"Error saving: {e}")

    # Update CLAUDE.md if requested
    if update_claude:
        update_claude_md(learned, verbose=verbose)

    return learned


def update_claude_md(learned: dict, verbose: bool = True) -> bool:
    """Update CLAUDE.md with actionable preferences."""
    if not learned:
        return False

    sections = []

    # Workflow rules
    workflows = learned.get("rules", {}).get("workflows", [])
    if workflows:
        sections.append("## Workflow Rules")
        sections.append("Do these automatically without asking:")
        for r in workflows:
            sections.append(f"- {r['rule'].capitalize()}")
        sections.append("")

    # Style preferences
    style = learned.get("rules", {}).get("style", [])
    if style:
        sections.append("## Response Style")
        for s in style:
            sections.append(f"- {s['rule'].capitalize()}")
        sections.append("")

    # Skip preferences
    skips = learned.get("rules", {}).get("skip", [])
    if skips:
        sections.append("## Skip Unless Asked")
        for s in skips:
            sections.append(f"- {s['rule'].capitalize()}")
        sections.append("")

    # Project context
    context = learned.get("context", [])
    if context:
        sections.append("## Current Project")
        for c in context:
            if c['type'] == 'tech':
                sections.append(f"- Uses: {c['value']}")
            elif c['type'] == 'url':
                sections.append(f"- URL: {c['value']}")
            elif c['type'] == 'project_name':
                sections.append(f"- Project: {c['value']}")
        sections.append("")

    if not sections:
        if verbose:
            print("No actionable preferences to add.")
        return False

    # Read current CLAUDE.md
    try:
        content = CLAUDE_MD.read_text() if CLAUDE_MD.exists() else ""
    except:
        content = ""

    # Markers
    start_marker = "<!-- USER PREFERENCES START -->"
    end_marker = "<!-- USER PREFERENCES END -->"

    new_section = f"\n{start_marker}\n" + "\n".join(sections) + f"\n{end_marker}\n"

    if start_marker in content:
        # Replace existing
        pattern = f"{start_marker}.*?{end_marker}"
        content = re.sub(pattern, new_section.strip(), content, flags=re.DOTALL)
    else:
        # Append
        content = content.rstrip() + "\n" + new_section

    try:
        CLAUDE_MD.write_text(content)
        if verbose:
            print(f"✅ Updated {CLAUDE_MD}")
        return True
    except Exception as e:
        if verbose:
            print(f"Error updating CLAUDE.md: {e}")
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Learn user preferences")
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--update-claude", "-u", action="store_true",
                       help="Update CLAUDE.md with preferences")
    args = parser.parse_args()

    run_preference_learning(verbose=not args.quiet, update_claude=args.update_claude)

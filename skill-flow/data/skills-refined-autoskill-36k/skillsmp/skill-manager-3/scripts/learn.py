#!/usr/bin/env python3
"""
learn.py - Pattern analysis engine for skill learning.

Analyzes collected patterns to detect:
- Repeated tool sequences (workflow patterns)
- Domain expertise (keyword clustering)
- Reusable patterns (generalizable processes)

Generates skill candidates for approval.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
import hashlib
import uuid

# Determine skills directory
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
CANDIDATES_DIR = SKILLS_DIR / ".skill-system" / "candidates"
CONFIG_FILE = SKILLS_DIR / ".skill-system" / "config.json"
ANALYTICS_FILE = SKILLS_DIR / ".skill-system" / "analytics.json"


def load_config() -> dict:
    """Load configuration."""
    default_config = {
        "learning": {
            "min_frequency": 2,
            "min_complexity": 3,
            "max_complexity": 7,
            "score_threshold": 0.6,
        },
        "domains": {
            "enabled": ["devops", "security", "data_science", "frontend", "backend", "git"]
        }
    }
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return default_config


def load_patterns(file_path: Path, days: int = 90) -> List[dict]:
    """Load patterns from JSONL file, filtered by age."""
    patterns = []
    if not file_path.exists():
        return patterns

    cutoff = datetime.utcnow() - timedelta(days=days)

    try:
        with open(file_path) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    # Parse timestamp and filter by age
                    ts_str = record.get("timestamp", "")
                    if ts_str:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if ts.replace(tzinfo=None) >= cutoff:
                            patterns.append(record)
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception:
        pass

    return patterns


def extract_tool_sequences(tool_patterns: List[dict]) -> List[Tuple[str, ...]]:
    """Extract tool sequences grouped by session."""
    sessions = defaultdict(list)

    for p in tool_patterns:
        session_id = p.get("session_id", "unknown")
        tool = p.get("tool")
        if tool:
            sessions[session_id].append(tool)

    # Return sequences of length 3+
    sequences = []
    for session_id, tools in sessions.items():
        if len(tools) >= 3:
            sequences.append(tuple(tools))

    return sequences


def find_repeated_subsequences(sequences: List[Tuple[str, ...]], min_len: int = 3, max_len: int = 7) -> Dict[Tuple[str, ...], int]:
    """Find repeated subsequences across sessions using n-gram analysis."""
    ngram_counts = Counter()

    for seq in sequences:
        # Generate all n-grams of varying lengths
        for n in range(min_len, min(max_len + 1, len(seq) + 1)):
            for i in range(len(seq) - n + 1):
                ngram = seq[i:i + n]
                ngram_counts[ngram] += 1

    # Filter to those appearing 2+ times
    repeated = {ngram: count for ngram, count in ngram_counts.items() if count >= 2}

    # Remove subsequences that are fully contained in longer sequences
    final = {}
    sorted_ngrams = sorted(repeated.keys(), key=len, reverse=True)

    for ngram in sorted_ngrams:
        # Check if this ngram is a subsequence of any already-included ngram
        is_subsequence = False
        for existing in final.keys():
            if len(ngram) < len(existing):
                # Check if ngram appears in existing
                ngram_str = "->".join(ngram)
                existing_str = "->".join(existing)
                if ngram_str in existing_str:
                    is_subsequence = True
                    break

        if not is_subsequence:
            final[ngram] = repeated[ngram]

    return final


def analyze_domain_distribution(prompt_patterns: List[dict]) -> Dict[str, dict]:
    """Analyze domain distribution from prompt patterns."""
    domain_data = defaultdict(lambda: {"count": 0, "sessions": set(), "intents": Counter()})

    for p in prompt_patterns:
        session_id = p.get("session_id", "unknown")
        domains = p.get("domains", [])
        intents = p.get("intent_signals", [])

        for domain in domains:
            domain_data[domain]["count"] += 1
            domain_data[domain]["sessions"].add(session_id)
            for intent in intents:
                domain_data[domain]["intents"][intent] += 1

    # Convert sets to counts
    result = {}
    for domain, data in domain_data.items():
        result[domain] = {
            "pattern_count": data["count"],
            "session_count": len(data["sessions"]),
            "top_intents": dict(data["intents"].most_common(3)),
        }

    return result


def calculate_candidate_score(
    sequence: Tuple[str, ...],
    frequency: int,
    domain_match: Optional[str],
    config: dict
) -> float:
    """Calculate a score for a skill candidate."""
    learning_config = config.get("learning", {})
    min_freq = learning_config.get("min_frequency", 2)
    min_complexity = learning_config.get("min_complexity", 3)
    max_complexity = learning_config.get("max_complexity", 7)

    # Frequency score (30%)
    freq_score = min(frequency / (min_freq * 2), 1.0) * 0.3

    # Complexity score (20%) - optimal is in the middle of the range
    seq_len = len(sequence)
    if min_complexity <= seq_len <= max_complexity:
        # Best score for sequences in the middle of the range
        optimal = (min_complexity + max_complexity) / 2
        complexity_score = (1 - abs(seq_len - optimal) / optimal) * 0.2
    else:
        complexity_score = 0.05  # Small score for out-of-range

    # Domain clarity score (25%)
    domain_score = 0.25 if domain_match else 0.1

    # Distinctiveness score (25%) - check for unique tools
    unique_tools = len(set(sequence))
    distinctiveness_score = min(unique_tools / 4, 1.0) * 0.25

    return round(freq_score + complexity_score + domain_score + distinctiveness_score, 2)


def infer_domain_from_sequence(sequence: Tuple[str, ...], tool_patterns: List[dict]) -> Optional[str]:
    """Infer domain from a tool sequence based on domain hints."""
    # Collect domain hints from patterns that match this sequence's tools
    domain_hints = Counter()

    for p in tool_patterns:
        tool = p.get("tool")
        if tool in sequence:
            hint = p.get("input_summary", {}).get("domain_hint")
            if hint:
                domain_hints[hint] += 1

    if domain_hints:
        return domain_hints.most_common(1)[0][0]
    return None


def generate_candidate_id() -> str:
    """Generate a unique candidate ID."""
    return f"candidate-{uuid.uuid4().hex[:8]}"


def generate_skill_name(sequence: Tuple[str, ...], domain: Optional[str]) -> str:
    """Generate a skill name from the sequence and domain."""
    # Use the most common tools in the sequence
    tool_counts = Counter(sequence)
    top_tools = [t.lower() for t, _ in tool_counts.most_common(2)]

    if domain:
        name = f"{domain}-{'-'.join(top_tools)}"
    else:
        name = f"workflow-{'-'.join(top_tools)}"

    # Ensure valid name (alphanumeric and dashes)
    name = "".join(c if c.isalnum() or c == "-" else "-" for c in name)
    return name[:50]  # Limit length


def create_candidate(
    sequence: Tuple[str, ...],
    frequency: int,
    domain: Optional[str],
    score: float,
    domain_info: dict
) -> dict:
    """Create a skill candidate structure."""
    candidate_id = generate_candidate_id()
    skill_name = generate_skill_name(sequence, domain)

    # Get top intents for this domain
    intents = []
    if domain and domain in domain_info:
        intents = list(domain_info[domain].get("top_intents", {}).keys())

    candidate = {
        "candidate_id": candidate_id,
        "skill_name": skill_name,
        "domain": domain,
        "score": score,
        "frequency": frequency,
        "tool_sequence": list(sequence),
        "unique_tools": list(set(sequence)),
        "intents": intents,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "status": "pending",
    }

    return candidate


def save_candidate(candidate: dict) -> Path:
    """Save a candidate to the candidates directory."""
    candidate_id = candidate["candidate_id"]
    candidate_dir = CANDIDATES_DIR / candidate_id

    candidate_dir.mkdir(parents=True, exist_ok=True)

    # Save candidate metadata
    meta_file = candidate_dir / "candidate.json"
    with open(meta_file, "w") as f:
        json.dump(candidate, f, indent=2)

    # Generate preview SKILL.md
    preview = generate_preview_skill(candidate)
    preview_file = candidate_dir / "SKILL.md.preview"
    with open(preview_file, "w") as f:
        f.write(preview)

    return candidate_dir


def generate_preview_skill(candidate: dict) -> str:
    """Generate a preview SKILL.md for the candidate."""
    name = candidate["skill_name"]
    domain = candidate.get("domain", "general")
    tools = candidate["unique_tools"]
    sequence = candidate["tool_sequence"]
    intents = candidate.get("intents", [])

    # Build trigger phrases
    triggers = [f"use {name}", f"run {name} workflow"]
    if domain:
        triggers.append(f"{domain} workflow")
    triggers.extend(intents)

    # Build description
    description = f"Auto-generated skill for {domain or 'general'} workflows. "
    description += f"Detected pattern: {' -> '.join(sequence[:5])}{'...' if len(sequence) > 5 else ''}. "
    description += f"Trigger phrases: {', '.join(triggers[:3])}."

    preview = f"""---
name: {name}
description: {description}
allowed-tools:
{chr(10).join(f'  - {t}' for t in tools)}
version: 1.0.0
domain: {domain or 'general'}
auto-generated: true
---

# {name.replace('-', ' ').title()}

Auto-generated skill based on detected usage patterns.

## When to Use

{chr(10).join(f'- {t}' for t in triggers)}

## Workflow Pattern

Detected tool sequence:
```
{' -> '.join(sequence)}
```

## Tools Required

| Tool | Purpose |
|------|---------|
{chr(10).join(f'| {t} | Used in workflow |' for t in tools)}

---

*This is a preview. Approve to activate this skill.*
"""
    return preview


def load_existing_skills() -> List[str]:
    """Load names of existing skills to check for duplicates."""
    skills = []
    if SKILLS_DIR.exists():
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name != "_skill-manager":
                skills.append(item.name)
    return skills


def run_learning(verbose: bool = True) -> List[dict]:
    """Run the learning process and generate candidates."""
    config = load_config()
    learning_config = config.get("learning", {})
    retention_days = config.get("observation", {}).get("pattern_retention_days", 90)
    score_threshold = learning_config.get("score_threshold", 0.6)

    # Run prompt analysis first
    prompt_analysis = {}
    try:
        from prompt_analyzer import run_prompt_analysis
        prompt_analysis = run_prompt_analysis(verbose=False)
    except Exception as e:
        if verbose:
            print(f"Note: Prompt analysis skipped ({e})")

    if verbose:
        print("Loading patterns...")

    # Load patterns
    tool_patterns = load_patterns(PATTERNS_DIR / "tool-sequences.jsonl", retention_days)
    prompt_patterns = load_patterns(PATTERNS_DIR / "prompt-patterns.jsonl", retention_days)

    if verbose:
        print(f"  - Tool patterns: {len(tool_patterns)}")
        print(f"  - Prompt patterns: {len(prompt_patterns)}")

    if len(tool_patterns) < 5:
        if verbose:
            print("Not enough patterns collected yet. Keep using Claude Code!")
        return []

    # Extract and analyze sequences
    if verbose:
        print("Analyzing tool sequences...")

    sequences = extract_tool_sequences(tool_patterns)
    repeated = find_repeated_subsequences(
        sequences,
        min_len=learning_config.get("min_complexity", 3),
        max_len=learning_config.get("max_complexity", 7)
    )

    if verbose:
        print(f"  - Found {len(repeated)} repeated patterns")

    # Analyze domains
    if verbose:
        print("Analyzing domain distribution...")

    domain_info = analyze_domain_distribution(prompt_patterns)

    if verbose:
        for domain, info in domain_info.items():
            print(f"  - {domain}: {info['pattern_count']} patterns, {info['session_count']} sessions")

    # Load existing skills to avoid duplicates
    existing_skills = load_existing_skills()

    # Generate candidates
    if verbose:
        print("Generating candidates...")

    candidates = []
    for sequence, frequency in repeated.items():
        # Infer domain
        domain = infer_domain_from_sequence(sequence, tool_patterns)

        # Calculate score
        score = calculate_candidate_score(sequence, frequency, domain, config)

        if score >= score_threshold:
            candidate = create_candidate(sequence, frequency, domain, score, domain_info)

            # Check for duplicate skill names
            if candidate["skill_name"] in existing_skills:
                if verbose:
                    print(f"  - Skipping duplicate: {candidate['skill_name']}")
                continue

            # Save candidate
            save_candidate(candidate)
            candidates.append(candidate)

            if verbose:
                print(f"  - Created: {candidate['skill_name']} (score: {score}, freq: {frequency})")

    # Generate intent-based candidates from prompt analysis
    if prompt_analysis and prompt_analysis.get("intent_tool_patterns"):
        if verbose:
            print("Generating intent-based candidates...")

        intent_patterns = prompt_analysis.get("intent_tool_patterns", {})
        for intent, tool_counts in intent_patterns.items():
            # Need at least 3 tool uses for this intent
            total_uses = sum(tool_counts.values())
            if total_uses < 3:
                continue

            # Get top tools for this intent
            top_tools = [t for t, c in sorted(tool_counts.items(), key=lambda x: -x[1])[:4]]
            if len(top_tools) < 2:
                continue

            # Create intent-based candidate
            skill_name = f"intent-{intent}"
            if skill_name in existing_skills:
                continue

            candidate = {
                "candidate_id": generate_candidate_id(),
                "skill_name": skill_name,
                "domain": intent,
                "score": min(0.6 + (total_uses * 0.02), 0.95),  # Score based on usage
                "frequency": total_uses,
                "tool_sequence": top_tools,
                "unique_tools": top_tools,
                "intents": [intent],
                "source": "prompt_analysis",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "status": "pending",
            }

            save_candidate(candidate)
            candidates.append(candidate)

            if verbose:
                print(f"  - Created: {skill_name} (intent-based, uses: {total_uses})")

    if verbose:
        print(f"\nGenerated {len(candidates)} skill candidates.")
        if candidates:
            print("Run 'manage.py candidates' to review them.")

    return candidates


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Skill learning engine")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    candidates = run_learning(verbose=not args.quiet and not args.json)

    if args.json:
        print(json.dumps(candidates, indent=2))


if __name__ == "__main__":
    main()

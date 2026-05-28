#!/usr/bin/env python3
"""
prompt_analyzer.py - Semantic analysis of user prompts for skill learning.

Analyzes:
- Repeated phrases/keywords
- Intent patterns (deploy, fix, build, etc.)
- Prompt → tool sequence correlations
- Workflow triggers
"""

import json
import re
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional
import hashlib

SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
PROMPTS_LOG = PATTERNS_DIR / "user-prompts.jsonl"
TOOL_SEQUENCES = PATTERNS_DIR / "tool-sequences.jsonl"
PROMPT_PATTERNS = PATTERNS_DIR / "learned-prompt-patterns.json"


# Intent categories with trigger phrases
INTENT_PATTERNS = {
    "deploy": [
        r"\bdeploy\b", r"\bpush to prod\b", r"\bship\b", r"\brelease\b",
        r"\bgo live\b", r"\blaunch\b", r"\bpublish\b"
    ],
    "fix": [
        r"\bfix\b", r"\bbug\b", r"\berror\b", r"\bissue\b", r"\bbroken\b",
        r"\bdoesn'?t work\b", r"\bisn'?t working\b", r"\bfailing\b"
    ],
    "build": [
        r"\bbuild\b", r"\bcreate\b", r"\bmake\b", r"\badd\b", r"\bimplement\b",
        r"\bwrite\b", r"\bgenerate\b", r"\bset ?up\b"
    ],
    "test": [
        r"\btest\b", r"\brun tests\b", r"\bcheck\b", r"\bverify\b", r"\bvalidate\b"
    ],
    "git": [
        r"\bcommit\b", r"\bpush\b", r"\bpull\b", r"\bmerge\b", r"\bbranch\b",
        r"\bgit\b", r"\bpr\b", r"\bpull request\b"
    ],
    "install": [
        r"\binstall\b", r"\bsetup\b", r"\bconfigure\b", r"\binit\b",
        r"\bdeps\b", r"\bdependencies\b", r"\bnpm\b", r"\bpip\b"
    ],
    "run": [
        r"\brun\b", r"\bstart\b", r"\bexecute\b", r"\blaunch\b", r"\bopen\b"
    ],
    "update": [
        r"\bupdate\b", r"\bupgrade\b", r"\bchange\b", r"\bmodify\b", r"\bedit\b",
        r"\brefactor\b"
    ],
    "docs": [
        r"\bdoc\b", r"\bdocs\b", r"\bdocument\b", r"\breadme\b", r"\bcomment\b"
    ],
    "debug": [
        r"\bdebug\b", r"\blog\b", r"\btrace\b", r"\binspect\b", r"\bwhat'?s wrong\b"
    ],
}

# Common action verbs for extraction
ACTION_VERBS = [
    "add", "build", "check", "clean", "clone", "commit", "configure", "create",
    "debug", "delete", "deploy", "edit", "export", "fetch", "find", "fix", "get",
    "help", "implement", "import", "init", "install", "list", "load", "make",
    "merge", "move", "open", "pull", "push", "read", "refactor", "remove", "rename",
    "restart", "run", "save", "search", "send", "set", "setup", "show", "start",
    "stop", "test", "try", "update", "upgrade", "use", "view", "write"
]


def load_prompts(days: int = 30) -> List[dict]:
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
                if ts_str:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts.replace(tzinfo=None) >= cutoff:
                        prompts.append(record)
            except:
                continue

    return prompts


def load_tool_sequences(days: int = 30) -> Dict[str, List[dict]]:
    """Load tool sequences grouped by session."""
    if not TOOL_SEQUENCES.exists():
        return {}

    cutoff = datetime.utcnow() - timedelta(days=days)
    sessions = defaultdict(list)

    with open(TOOL_SEQUENCES) as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                ts_str = record.get("timestamp", "")
                if ts_str:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts.replace(tzinfo=None) >= cutoff:
                        session_id = record.get("session_id", "unknown")
                        sessions[session_id].append(record)
            except:
                continue

    return dict(sessions)


def detect_intent(prompt: str) -> List[str]:
    """Detect intents from a prompt."""
    prompt_lower = prompt.lower()
    intents = []

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt_lower):
                intents.append(intent)
                break

    return intents


def extract_keywords(prompt: str) -> List[str]:
    """Extract meaningful keywords from prompt."""
    # Clean and tokenize
    prompt_lower = prompt.lower()
    # Remove shell prefix
    prompt_lower = re.sub(r'^\[shell\]\s*', '', prompt_lower)
    # Split into words
    words = re.findall(r'\b[a-z][a-z0-9_-]*\b', prompt_lower)

    # Filter stopwords
    stopwords = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
        'because', 'as', 'until', 'while', 'of', 'at', 'by', 'about', 'against',
        'i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'him',
        'she', 'her', 'it', 'its', 'they', 'them', 'what', 'which', 'who',
        'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were',
        'ok', 'okay', 'yes', 'no', 'yeah', 'yep', 'nope', 'sure', 'cool',
        'great', 'good', 'nice', 'thanks', 'please', 'pls', 'thx', 'ty',
        'u', 'ur', 'im', 'dont', 'cant', 'wont', 'isnt', 'arent', 'wasnt',
    }

    keywords = [w for w in words if w not in stopwords and len(w) > 2]
    return keywords


def extract_action_object_pairs(prompt: str) -> List[Tuple[str, str]]:
    """Extract action-object pairs like (commit, changes), (run, tests)."""
    prompt_lower = prompt.lower()
    pairs = []

    for verb in ACTION_VERBS:
        # Look for "verb X" or "verb the X" patterns
        pattern = rf'\b{verb}\s+(?:the\s+)?([a-z][a-z0-9_-]*)'
        matches = re.findall(pattern, prompt_lower)
        for obj in matches:
            if len(obj) > 2:
                pairs.append((verb, obj))

    return pairs


def analyze_prompt_patterns(prompts: List[dict]) -> dict:
    """Analyze patterns in user prompts."""
    analysis = {
        "total_prompts": len(prompts),
        "intent_counts": Counter(),
        "keyword_counts": Counter(),
        "action_object_pairs": Counter(),
        "common_phrases": Counter(),
        "prompt_templates": [],
    }

    # Analyze each prompt
    for p in prompts:
        prompt = p.get("prompt", "")
        if not prompt or prompt.startswith("[shell]"):
            continue

        # Detect intents
        intents = detect_intent(prompt)
        for intent in intents:
            analysis["intent_counts"][intent] += 1

        # Extract keywords
        keywords = extract_keywords(prompt)
        for kw in keywords:
            analysis["keyword_counts"][kw] += 1

        # Extract action-object pairs
        pairs = extract_action_object_pairs(prompt)
        for pair in pairs:
            analysis["action_object_pairs"][pair] += 1

    # Find common multi-word phrases (2-3 words)
    all_prompts_text = " ".join(p.get("prompt", "") for p in prompts if not p.get("prompt", "").startswith("[shell]"))
    words = all_prompts_text.lower().split()

    # Bigrams
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if len(bigram) > 5:
            analysis["common_phrases"][bigram] += 1

    # Filter to frequent patterns
    analysis["intent_counts"] = dict(analysis["intent_counts"].most_common(10))
    analysis["keyword_counts"] = dict(analysis["keyword_counts"].most_common(20))
    analysis["action_object_pairs"] = dict((f"{k[0]}_{k[1]}", v) for k, v in analysis["action_object_pairs"].most_common(15))
    analysis["common_phrases"] = dict(analysis["common_phrases"].most_common(10))

    return analysis


def correlate_prompts_to_tools(prompts: List[dict], tool_sessions: Dict[str, List[dict]]) -> List[dict]:
    """Find correlations between prompts and tool sequences that followed."""
    correlations = []

    # Group prompts by session
    prompt_sessions = defaultdict(list)
    for p in prompts:
        session_id = p.get("session_id")
        if session_id:
            prompt_sessions[session_id].append(p)

    # For each session, link prompts to tools
    for session_id, session_prompts in prompt_sessions.items():
        session_tools = tool_sessions.get(session_id, [])
        if not session_tools:
            continue

        for prompt_record in session_prompts:
            prompt = prompt_record.get("prompt", "")
            prompt_ts = prompt_record.get("timestamp", "")

            if not prompt or prompt.startswith("[shell]"):
                continue

            # Find tools that came after this prompt
            tools_after = []
            for tool_record in session_tools:
                tool_ts = tool_record.get("timestamp", "")
                if tool_ts > prompt_ts:
                    tools_after.append(tool_record.get("tool"))
                    if len(tools_after) >= 5:  # Limit to next 5 tools
                        break

            if tools_after:
                intents = detect_intent(prompt)
                correlations.append({
                    "prompt_preview": prompt[:100],
                    "intents": intents,
                    "tools_that_followed": tools_after,
                    "session_id": session_id,
                })

    return correlations


def find_intent_tool_patterns(correlations: List[dict]) -> Dict[str, Counter]:
    """Find which tools typically follow which intents."""
    intent_tools = defaultdict(Counter)

    for corr in correlations:
        intents = corr.get("intents", [])
        tools = corr.get("tools_that_followed", [])

        for intent in intents:
            for tool in tools:
                intent_tools[intent][tool] += 1

    # Convert to regular dict with most common
    result = {}
    for intent, tool_counts in intent_tools.items():
        result[intent] = dict(tool_counts.most_common(5))

    return result


def generate_workflow_suggestions(intent_tool_patterns: Dict[str, Counter], min_count: int = 2) -> List[dict]:
    """Generate workflow suggestions based on intent-tool patterns."""
    suggestions = []

    for intent, tool_counts in intent_tool_patterns.items():
        # Get tools used at least min_count times
        common_tools = [tool for tool, count in tool_counts.items() if count >= min_count]

        if len(common_tools) >= 2:
            suggestions.append({
                "intent": intent,
                "typical_tools": common_tools[:5],
                "frequency": sum(tool_counts.values()),
                "suggestion": f"When you say '{intent}', you typically use: {', '.join(common_tools[:3])}",
            })

    return sorted(suggestions, key=lambda x: x["frequency"], reverse=True)


def run_prompt_analysis(verbose: bool = True) -> dict:
    """Run full prompt analysis."""
    if verbose:
        print("Prompt Pattern Analyzer")
        print("=" * 60)

    # Load data
    prompts = load_prompts(days=30)
    tool_sessions = load_tool_sequences(days=30)

    if verbose:
        print(f"Loaded {len(prompts)} prompts from last 30 days")
        print(f"Loaded {len(tool_sessions)} sessions with tool data")

    if not prompts:
        if verbose:
            print("No prompts to analyze. Run 'manage.py scan' first.")
        return {}

    # Analyze patterns
    analysis = analyze_prompt_patterns(prompts)

    if verbose:
        print(f"\nIntent Distribution:")
        for intent, count in sorted(analysis["intent_counts"].items(), key=lambda x: -x[1]):
            print(f"  {intent}: {count}")

        print(f"\nTop Keywords:")
        for kw, count in list(analysis["keyword_counts"].items())[:10]:
            print(f"  {kw}: {count}")

        print(f"\nCommon Action-Object Pairs:")
        for pair, count in list(analysis["action_object_pairs"].items())[:10]:
            print(f"  {pair}: {count}")

    # Correlate prompts to tools
    correlations = correlate_prompts_to_tools(prompts, tool_sessions)
    intent_tool_patterns = find_intent_tool_patterns(correlations)

    if verbose and intent_tool_patterns:
        print(f"\nIntent → Tool Patterns:")
        for intent, tools in intent_tool_patterns.items():
            tool_str = ", ".join(f"{t}({c})" for t, c in list(tools.items())[:3])
            print(f"  {intent}: {tool_str}")

    # Generate suggestions
    suggestions = generate_workflow_suggestions(intent_tool_patterns)

    if verbose and suggestions:
        print(f"\nWorkflow Suggestions:")
        for s in suggestions[:5]:
            print(f"  • {s['suggestion']}")

    # Save results
    results = {
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
        "prompt_count": len(prompts),
        "analysis": analysis,
        "intent_tool_patterns": {k: dict(v) for k, v in intent_tool_patterns.items()},
        "suggestions": suggestions,
    }

    try:
        with open(PROMPT_PATTERNS, "w") as f:
            json.dump(results, f, indent=2)
        if verbose:
            print(f"\nSaved to: {PROMPT_PATTERNS}")
    except Exception as e:
        if verbose:
            print(f"Error saving: {e}")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze user prompt patterns")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()

    run_prompt_analysis(verbose=not args.quiet)

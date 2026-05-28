#!/usr/bin/env python3
"""
session_end.py - Lightweight analysis at session end.
Triggers skill candidate suggestions if patterns detected.

Hook type: Stop (or custom session end trigger)
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

# Determine skills directory based on environment
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
SEQUENCES_FILE = PATTERNS_DIR / "tool-sequences.jsonl"
DOMAIN_FILE = PATTERNS_DIR / "prompt-patterns.jsonl"
FEEDBACK_FILE = PATTERNS_DIR / "feedback.jsonl"
ANALYTICS_FILE = SKILLS_DIR / ".skill-system" / "analytics.json"


def get_session_id():
    """Get or generate a session ID."""
    session_id = os.environ.get('CLAUDE_SESSION_ID')
    if not session_id:
        session_id = datetime.utcnow().strftime("%Y%m%d-%H")
    return session_id


def load_session_data(file_path, session_id):
    """Load records for a specific session from a JSONL file."""
    records = []
    if not file_path.exists():
        return records

    try:
        with open(file_path) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if record.get("session_id") == session_id:
                        records.append(record)
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return records


def analyze_session(session_id):
    """Analyze patterns from a session."""
    # Load session data
    tool_records = load_session_data(SEQUENCES_FILE, session_id)
    prompt_records = load_session_data(DOMAIN_FILE, session_id)
    feedback_records = load_session_data(FEEDBACK_FILE, session_id)

    analysis = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool_count": len(tool_records),
        "prompt_count": len(prompt_records),
        "feedback_count": len(feedback_records),
    }

    # Analyze tool usage
    if tool_records:
        tools = [r.get("tool") for r in tool_records if r.get("tool")]
        analysis["tools_used"] = dict(Counter(tools))
        analysis["unique_tools"] = len(set(tools))

        # Extract tool sequence (simplified)
        analysis["tool_sequence"] = tools[:20]  # First 20 tools

        # Detect domain hints from tools
        domain_hints = [r.get("input_summary", {}).get("domain_hint")
                       for r in tool_records
                       if r.get("input_summary", {}).get("domain_hint")]
        if domain_hints:
            analysis["domain_hints_from_tools"] = dict(Counter(domain_hints))

    # Analyze domains from prompts
    if prompt_records:
        all_domains = []
        all_intents = []
        for r in prompt_records:
            all_domains.extend(r.get("domains", []))
            all_intents.extend(r.get("intent_signals", []))

        if all_domains:
            analysis["domains_detected"] = dict(Counter(all_domains))
        if all_intents:
            analysis["intents_detected"] = dict(Counter(all_intents))

    # Analyze success/failure
    if feedback_records:
        classifications = [r.get("classification") for r in feedback_records]
        analysis["feedback_summary"] = dict(Counter(classifications))

        # Calculate success rate
        successes = classifications.count("success")
        failures = classifications.count("failure")
        total = successes + failures
        if total > 0:
            analysis["success_rate"] = round(successes / total, 2)

    return analysis


def update_analytics(analysis):
    """Update global analytics with session data."""
    try:
        analytics = {}
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE) as f:
                analytics = json.load(f)

        # Update global stats
        global_stats = analytics.get("global_stats", {})
        global_stats["total_sessions_observed"] = global_stats.get("total_sessions_observed", 0) + 1
        global_stats["total_patterns_captured"] = global_stats.get("total_patterns_captured", 0) + analysis.get("tool_count", 0)
        analytics["global_stats"] = global_stats

        # Update domain stats
        domain_stats = analytics.get("domain_stats", {})
        for domain, count in analysis.get("domains_detected", {}).items():
            if domain not in domain_stats:
                domain_stats[domain] = {"sessions": 0, "patterns": 0, "skills": 0}
            domain_stats[domain]["sessions"] += 1
            domain_stats[domain]["patterns"] += count
        analytics["domain_stats"] = domain_stats

        analytics["updated_at"] = datetime.utcnow().isoformat() + "Z"

        with open(ANALYTICS_FILE, "w") as f:
            json.dump(analytics, f, indent=2)
    except Exception:
        pass


def should_suggest_learning(analysis):
    """Determine if we should suggest running skill learning."""
    # Minimum activity threshold
    if analysis.get("tool_count", 0) < 5:
        return False

    # Check for repeated patterns
    tools = analysis.get("tools_used", {})
    if len(tools) >= 3:  # Using 3+ different tools
        return True

    # Check for domain concentration
    domains = analysis.get("domains_detected", {})
    if domains:
        max_domain_count = max(domains.values())
        if max_domain_count >= 2:  # Strong domain signal
            return True

    return False


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}
    except Exception:
        input_data = {}

    session_id = input_data.get("session_id") or get_session_id()

    # Analyze the session
    analysis = analyze_session(session_id)

    # Update global analytics
    update_analytics(analysis)

    # Check if we should suggest learning
    if should_suggest_learning(analysis):
        # Output suggestion
        suggestion = {
            "message": f"Session had {analysis.get('tool_count', 0)} tool calls across {analysis.get('unique_tools', 0)} tools.",
            "recommendation": "Consider running '/skill-learn' to analyze patterns.",
            "domains": list(analysis.get("domains_detected", {}).keys()),
        }

        # Print to stderr (visible in terminal but doesn't affect hook flow)
        print(json.dumps({
            "type": "info",
            "content": f"Skill System: {suggestion['message']} {suggestion['recommendation']}"
        }), file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()

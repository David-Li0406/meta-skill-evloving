#!/usr/bin/env python3
"""
improve.py - Auto-improvement engine for skills.

Monitors skill effectiveness and automatically improves skills:
- Detects low success rates
- Identifies missing tools from failure patterns
- Updates reference documentation
- Manages version bumps and changelogs
"""

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
from typing import Optional, List, Dict, Tuple
import shutil

# Determine skills directory
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
CONFIG_FILE = SKILLS_DIR / ".skill-system" / "config.json"
ANALYTICS_FILE = SKILLS_DIR / ".skill-system" / "analytics.json"


def load_config() -> dict:
    """Load configuration."""
    default_config = {
        "improvement": {
            "enabled": True,
            "auto_apply_threshold": 0.9,
            "min_usage_before_improve": 10,
            "success_rate_trigger": 0.7,
            "improvement_cooldown_hours": 24
        }
    }
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return {**default_config, **config}
    except Exception:
        return default_config


def load_skill_meta(skill_name: str) -> Optional[dict]:
    """Load skill metadata."""
    meta_file = SKILLS_DIR / skill_name / "skill.meta.json"
    if not meta_file.exists():
        return None
    try:
        with open(meta_file) as f:
            return json.load(f)
    except Exception:
        return None


def save_skill_meta(skill_name: str, meta: dict) -> bool:
    """Save skill metadata."""
    meta_file = SKILLS_DIR / skill_name / "skill.meta.json"
    try:
        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)
        return True
    except Exception:
        return False


def load_skill_md(skill_name: str) -> Optional[str]:
    """Load SKILL.md content."""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_file.exists():
        return None
    try:
        with open(skill_file) as f:
            return f.read()
    except Exception:
        return None


def save_skill_md(skill_name: str, content: str) -> bool:
    """Save SKILL.md content."""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    try:
        with open(skill_file, "w") as f:
            f.write(content)
        return True
    except Exception:
        return False


def parse_skill_yaml(content: str) -> Tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    yaml_str = parts[1].strip()
    body = parts[2]

    # Simple YAML parsing (avoiding external dependencies)
    yaml_data = {}
    current_key = None
    list_values = []

    for line in yaml_str.split("\n"):
        line = line.rstrip()
        if not line:
            continue

        # Check for list item
        if line.startswith("  - "):
            if current_key:
                list_values.append(line[4:].strip())
        elif ":" in line:
            # Save previous list if any
            if current_key and list_values:
                yaml_data[current_key] = list_values
                list_values = []

            key, value = line.split(":", 1)
            current_key = key.strip()
            value = value.strip()

            if value:
                yaml_data[current_key] = value

    # Save last list if any
    if current_key and list_values:
        yaml_data[current_key] = list_values

    return yaml_data, body


def serialize_skill_yaml(yaml_data: dict, body: str) -> str:
    """Serialize YAML frontmatter and body back to SKILL.md format."""
    lines = ["---"]

    for key, value in yaml_data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")

    lines.append("---")
    lines.append(body)

    return "\n".join(lines)


def load_feedback_patterns(days: int = 30) -> List[dict]:
    """Load feedback patterns from recent sessions."""
    feedback_file = PATTERNS_DIR / "feedback.jsonl"
    patterns = []

    if not feedback_file.exists():
        return patterns

    cutoff = datetime.utcnow() - timedelta(days=days)

    try:
        with open(feedback_file) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
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


def load_tool_patterns(days: int = 30) -> List[dict]:
    """Load tool usage patterns from recent sessions."""
    tool_file = PATTERNS_DIR / "tool-sequences.jsonl"
    patterns = []

    if not tool_file.exists():
        return patterns

    cutoff = datetime.utcnow() - timedelta(days=days)

    try:
        with open(tool_file) as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
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


def analyze_effectiveness(skill_name: str, meta: dict) -> dict:
    """Analyze current effectiveness of a skill."""
    effectiveness = meta.get("effectiveness", {})

    # Load recent feedback
    feedback = load_feedback_patterns(days=30)

    # Calculate success rate from feedback
    successes = sum(1 for f in feedback if f.get("classification") == "success")
    failures = sum(1 for f in feedback if f.get("classification") == "failure")
    total = successes + failures

    if total > 0:
        current_success_rate = successes / total
    else:
        current_success_rate = effectiveness.get("success_rate", 1.0)

    # Analyze failure patterns
    failure_types = Counter()
    for f in feedback:
        if f.get("classification") == "failure":
            error_type = f.get("error_type", "unknown")
            failure_types[error_type] += 1

    return {
        "usage_count": effectiveness.get("usage_count", 0) + len(feedback),
        "success_rate": round(current_success_rate, 2),
        "failure_types": dict(failure_types.most_common(5)),
        "total_feedback": total,
    }


def detect_missing_tools(skill_name: str, meta: dict) -> List[str]:
    """Detect tools that might be missing from the skill's allowed-tools."""
    # Load SKILL.md to get current allowed tools
    content = load_skill_md(skill_name)
    if not content:
        return []

    yaml_data, _ = parse_skill_yaml(content)
    allowed_tools = yaml_data.get("allowed-tools", [])
    if isinstance(allowed_tools, str):
        allowed_tools = [allowed_tools]

    # Load recent tool patterns
    tool_patterns = load_tool_patterns(days=30)

    # Find tools that were used but failed
    used_tools = Counter()
    failed_tools = Counter()

    for p in tool_patterns:
        tool = p.get("tool")
        if tool:
            used_tools[tool] += 1
            if not p.get("success", True):
                failed_tools[tool] += 1

    # Suggest tools that are frequently used but not in allowed-tools
    missing = []
    for tool, count in used_tools.most_common(10):
        if tool not in allowed_tools and count >= 3:
            missing.append(tool)

    return missing[:5]  # Limit to top 5 suggestions


def generate_improvement(
    skill_name: str,
    meta: dict,
    analysis: dict,
    missing_tools: List[str]
) -> Optional[dict]:
    """Generate an improvement proposal."""
    config = load_config()
    improvement_config = config.get("improvement", {})
    success_trigger = improvement_config.get("success_rate_trigger", 0.7)
    min_usage = improvement_config.get("min_usage_before_improve", 10)

    # Check if improvement is needed
    needs_improvement = False
    improvements = []

    # Check success rate
    if analysis["usage_count"] >= min_usage:
        if analysis["success_rate"] < success_trigger:
            needs_improvement = True
            improvements.append({
                "type": "success_rate_low",
                "details": f"Success rate {analysis['success_rate']} below threshold {success_trigger}",
                "action": "Review and optimize workflow"
            })

    # Check for missing tools
    if missing_tools:
        needs_improvement = True
        improvements.append({
            "type": "missing_tools",
            "details": f"Detected frequent use of: {', '.join(missing_tools)}",
            "action": "Add tools to allowed-tools",
            "tools": missing_tools
        })

    # Check for common failure patterns
    if analysis["failure_types"]:
        top_failure = list(analysis["failure_types"].keys())[0]
        failure_count = analysis["failure_types"][top_failure]
        if failure_count >= 3:
            needs_improvement = True
            improvements.append({
                "type": "recurring_failure",
                "details": f"Recurring '{top_failure}' errors ({failure_count} times)",
                "action": f"Add error handling for {top_failure}"
            })

    if not needs_improvement:
        return None

    # Calculate improvement confidence
    confidence = 0.5
    if missing_tools:
        confidence += 0.3  # High confidence for tool additions
    if analysis["success_rate"] < 0.5:
        confidence += 0.1  # More confident if really low success rate
    if analysis["usage_count"] >= min_usage * 2:
        confidence += 0.1  # More confident with more data

    return {
        "skill_name": skill_name,
        "current_version": meta.get("version", "1.0.0"),
        "improvements": improvements,
        "confidence": min(confidence, 1.0),
        "analysis": analysis,
        "missing_tools": missing_tools,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }


def apply_improvement(skill_name: str, proposal: dict, verbose: bool = True) -> bool:
    """Apply an improvement to a skill."""
    config = load_config()
    auto_threshold = config.get("improvement", {}).get("auto_apply_threshold", 0.9)

    # Check confidence threshold
    if proposal["confidence"] < auto_threshold:
        if verbose:
            print(f"Confidence {proposal['confidence']} below threshold {auto_threshold}")
            print("Improvement queued for manual approval")
        return False

    # Load current skill
    content = load_skill_md(skill_name)
    if not content:
        return False

    yaml_data, body = parse_skill_yaml(content)
    meta = load_skill_meta(skill_name)
    if not meta:
        return False

    changes_made = []

    # Apply tool additions
    if proposal.get("missing_tools"):
        allowed_tools = yaml_data.get("allowed-tools", [])
        if isinstance(allowed_tools, str):
            allowed_tools = [allowed_tools]

        for tool in proposal["missing_tools"]:
            if tool not in allowed_tools:
                allowed_tools.append(tool)
                changes_made.append(f"Added {tool} to allowed-tools")

        yaml_data["allowed-tools"] = allowed_tools

    # Bump version
    current_version = yaml_data.get("version", "1.0.0")
    parts = current_version.split(".")
    if len(parts) == 3:
        parts[1] = str(int(parts[1]) + 1)  # Minor version bump
        parts[2] = "0"
    new_version = ".".join(parts)
    yaml_data["version"] = new_version

    # Save updated SKILL.md
    new_content = serialize_skill_yaml(yaml_data, body)
    save_skill_md(skill_name, new_content)

    # Update metadata
    meta["version"] = new_version
    meta["updated_at"] = datetime.utcnow().isoformat() + "Z"
    effectiveness = meta.get("effectiveness", {})
    effectiveness["last_improvement"] = datetime.utcnow().isoformat() + "Z"
    meta["effectiveness"] = effectiveness
    save_skill_meta(skill_name, meta)

    # Update CHANGELOG
    update_changelog(skill_name, new_version, changes_made)

    # Git commit if available
    commit_improvement(skill_name, new_version, changes_made)

    if verbose:
        print(f"Applied improvement to {skill_name}")
        print(f"  Version: {current_version} -> {new_version}")
        for change in changes_made:
            print(f"  - {change}")

    return True


def update_changelog(skill_name: str, version: str, changes: List[str]) -> bool:
    """Update the CHANGELOG.md with new changes."""
    changelog_file = SKILLS_DIR / skill_name / "CHANGELOG.md"

    try:
        if changelog_file.exists():
            with open(changelog_file) as f:
                content = f.read()
        else:
            content = "# Changelog\n\n"

        date = datetime.utcnow().strftime('%Y-%m-%d')
        new_entry = f"\n## [{version}] - {date}\n\n### Changed (Auto-improved)\n\n"
        for change in changes:
            new_entry += f"- {change}\n"

        # Insert after the header
        if "## [" in content:
            # Insert before first version entry
            idx = content.index("## [")
            content = content[:idx] + new_entry + "\n" + content[idx:]
        else:
            content += new_entry

        with open(changelog_file, "w") as f:
            f.write(content)

        return True
    except Exception:
        return False


def commit_improvement(skill_name: str, version: str, changes: List[str]) -> bool:
    """Commit the improvement to git."""
    skill_dir = SKILLS_DIR / skill_name

    try:
        # Add all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        # Commit
        commit_msg = f"v{version}: Auto-improved\n\n" + "\n".join(f"- {c}" for c in changes)
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        # Tag
        subprocess.run(
            ["git", "tag", f"v{version}", "-m", f"Auto-improvement: {version}"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_skill(skill_name: str, verbose: bool = True) -> Optional[dict]:
    """Check a skill for potential improvements."""
    meta = load_skill_meta(skill_name)
    if not meta:
        if verbose:
            print(f"Skill not found: {skill_name}")
        return None

    if verbose:
        print(f"Analyzing {skill_name}...")

    # Analyze effectiveness
    analysis = analyze_effectiveness(skill_name, meta)
    if verbose:
        print(f"  Usage count: {analysis['usage_count']}")
        print(f"  Success rate: {analysis['success_rate']}")
        if analysis['failure_types']:
            print(f"  Top failures: {analysis['failure_types']}")

    # Detect missing tools
    missing_tools = detect_missing_tools(skill_name, meta)
    if verbose and missing_tools:
        print(f"  Suggested tools: {missing_tools}")

    # Generate improvement proposal
    proposal = generate_improvement(skill_name, meta, analysis, missing_tools)

    if proposal:
        if verbose:
            print(f"\nImprovement proposal (confidence: {proposal['confidence']}):")
            for imp in proposal["improvements"]:
                print(f"  - {imp['type']}: {imp['details']}")
    else:
        if verbose:
            print("No improvements needed at this time.")

    return proposal


def run_auto_improve(verbose: bool = True) -> List[dict]:
    """Run auto-improvement on all skills."""
    config = load_config()
    if not config.get("improvement", {}).get("enabled", True):
        if verbose:
            print("Auto-improvement is disabled in config.")
        return []

    results = []

    # Find all skills
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name != "_skill-manager":
            skill_name = item.name
            proposal = check_skill(skill_name, verbose=verbose)

            if proposal:
                applied = apply_improvement(skill_name, proposal, verbose=verbose)
                proposal["applied"] = applied
                results.append(proposal)

    return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Skill auto-improvement engine")
    parser.add_argument("action", nargs="?", default="check-all",
                       choices=["check", "check-all", "improve", "improve-all"],
                       help="Action to perform")
    parser.add_argument("skill_name", nargs="?", help="Skill name (for single-skill actions)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--force", "-f", action="store_true", help="Force improvement regardless of confidence")
    args = parser.parse_args()

    if args.action in ["check", "improve"] and not args.skill_name:
        print("Error: skill_name required for single-skill actions")
        sys.exit(1)

    if args.action == "check":
        proposal = check_skill(args.skill_name, verbose=not args.quiet and not args.json)
        if args.json and proposal:
            print(json.dumps(proposal, indent=2))

    elif args.action == "check-all":
        results = []
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name != "_skill-manager":
                proposal = check_skill(item.name, verbose=not args.quiet and not args.json)
                if proposal:
                    results.append(proposal)
        if args.json:
            print(json.dumps(results, indent=2))

    elif args.action == "improve":
        proposal = check_skill(args.skill_name, verbose=not args.quiet)
        if proposal:
            if args.force:
                proposal["confidence"] = 1.0
            apply_improvement(args.skill_name, proposal, verbose=not args.quiet)

    elif args.action == "improve-all":
        results = run_auto_improve(verbose=not args.quiet and not args.json)
        if args.json:
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    import sys
    main()

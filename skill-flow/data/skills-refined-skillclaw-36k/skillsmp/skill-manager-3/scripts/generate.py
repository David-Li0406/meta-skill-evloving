#!/usr/bin/env python3
"""
generate.py - Skill package generator.

Transforms approved candidates into complete skill packages:
- SKILL.md with proper YAML frontmatter
- skill.meta.json for metadata and tracking
- references/ directory with documentation
- CHANGELOG.md for version history
- Git repository initialization
"""

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

# Determine skills directory
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
CANDIDATES_DIR = SKILLS_DIR / ".skill-system" / "candidates"
CONFIG_FILE = SKILLS_DIR / ".skill-system" / "config.json"


def load_config() -> dict:
    """Load configuration."""
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def load_candidate(candidate_id: str) -> Optional[dict]:
    """Load a candidate by ID."""
    candidate_dir = CANDIDATES_DIR / candidate_id
    meta_file = candidate_dir / "candidate.json"

    if not meta_file.exists():
        return None

    try:
        with open(meta_file) as f:
            return json.load(f)
    except Exception:
        return None


def generate_skill_md(candidate: dict) -> str:
    """Generate the SKILL.md content."""
    name = candidate["skill_name"]
    domain = candidate.get("domain", "general")
    tools = candidate["unique_tools"]
    sequence = candidate["tool_sequence"]
    intents = candidate.get("intents", [])

    # Build comprehensive trigger phrases
    triggers = [f"use {name}", f"run {name}", f"{name} workflow"]
    if domain and domain != "general":
        triggers.extend([f"{domain} workflow", f"help with {domain}"])
    triggers.extend(intents)

    # Build description
    desc_parts = [
        f"Skill for {domain} workflows based on detected usage patterns.",
        f"Core workflow: {' -> '.join(sequence[:4])}{'...' if len(sequence) > 4 else ''}.",
        f"Use when: {', '.join(triggers[:3])}."
    ]
    description = " ".join(desc_parts)

    # Generate workflow documentation
    workflow_steps = []
    for i, tool in enumerate(sequence, 1):
        workflow_steps.append(f"{i}. **{tool}** - Execute {tool.lower()} operation")

    # Build the SKILL.md
    content = f"""---
name: {name}
description: {description}
allowed-tools:
{chr(10).join(f'  - {t}' for t in tools)}
version: 1.0.0
domain: {domain}
auto-generated: true
---

# {name.replace('-', ' ').title()}

{f"A {domain}-focused skill" if domain != "general" else "A workflow skill"} automatically generated from detected usage patterns.

## When to Use

This skill should be activated when:
{chr(10).join(f'- {t}' for t in triggers)}

## Core Workflow

The detected workflow pattern:

```
{' -> '.join(sequence)}
```

### Step-by-Step

{chr(10).join(workflow_steps)}

## Tools Used

| Tool | Description |
|------|-------------|
{chr(10).join(f'| {t} | Standard {t} operations |' for t in tools)}

## Best Practices

Based on the learned pattern:

1. **Follow the sequence** - The tool order was detected from successful sessions
2. **Verify each step** - Check output before proceeding to next tool
3. **Handle errors** - If a step fails, investigate before continuing

## Customization

This skill can be refined by:
- Adding reference documentation in `references/`
- Creating helper scripts in `scripts/`
- Updating the workflow steps based on experience

## Origin

- **Generated**: {datetime.utcnow().strftime('%Y-%m-%d')}
- **Source patterns**: {candidate.get('frequency', 0)} occurrences detected
- **Score**: {candidate.get('score', 0)}
"""
    return content


def generate_meta_json(candidate: dict) -> dict:
    """Generate the skill.meta.json content."""
    return {
        "skill_id": str(uuid.uuid4()),
        "name": candidate["skill_name"],
        "version": "1.0.0",
        "domain": candidate.get("domain", "general"),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "auto_generated": True,
        "source_patterns": [candidate["candidate_id"]],
        "approval_status": "approved",
        "approved_at": datetime.utcnow().isoformat() + "Z",
        "effectiveness": {
            "usage_count": 0,
            "success_rate": 1.0,
            "avg_tool_calls": len(candidate["tool_sequence"]),
            "failure_patterns": [],
            "user_refinements": 0,
            "last_improvement": None
        }
    }


def generate_changelog(candidate: dict) -> str:
    """Generate initial CHANGELOG.md."""
    date = datetime.utcnow().strftime('%Y-%m-%d')
    name = candidate["skill_name"]

    return f"""# Changelog

All notable changes to the **{name}** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - {date}

### Added

- Initial skill generation from usage patterns
- Core workflow: {' -> '.join(candidate['tool_sequence'][:5])}
- Tool permissions: {', '.join(candidate['unique_tools'])}
- Domain classification: {candidate.get('domain', 'general')}

### Source

- Pattern frequency: {candidate.get('frequency', 0)} occurrences
- Confidence score: {candidate.get('score', 0)}
- Candidate ID: {candidate['candidate_id']}
"""


def generate_reference_doc(candidate: dict) -> str:
    """Generate a reference document for the skill."""
    name = candidate["skill_name"]
    domain = candidate.get("domain", "general")
    tools = candidate["unique_tools"]

    return f"""# {name.replace('-', ' ').title()} Reference

## Quick Reference

### Tools

{chr(10).join(f'- **{t}**: Standard {t.lower()} operations' for t in tools)}

### Common Patterns

Based on detected usage:

```
Pattern: {' -> '.join(candidate['tool_sequence'])}
Frequency: {candidate.get('frequency', 0)} times
```

## Tips

1. This pattern was detected from real usage - it works!
2. Modify the workflow based on your specific needs
3. Report issues to improve the skill

## Domain: {domain}

This skill is optimized for {domain} workflows.

## Related Skills

Look for other skills in the same domain for complementary functionality.
"""


def init_git_repo(skill_dir: Path, skill_name: str) -> bool:
    """Initialize a git repository for the skill."""
    try:
        # Initialize repo
        subprocess.run(
            ["git", "init"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        # Configure git (use generic author for generated skills)
        subprocess.run(
            ["git", "config", "user.email", "skill-system@local"],
            cwd=skill_dir,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Skill System"],
            cwd=skill_dir,
            capture_output=True
        )

        # Add all files
        subprocess.run(
            ["git", "add", "-A"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        # Initial commit
        subprocess.run(
            ["git", "commit", "-m", f"v1.0.0: Initial generation of {skill_name}"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        # Create version tag
        subprocess.run(
            ["git", "tag", "v1.0.0", "-m", "Initial version"],
            cwd=skill_dir,
            capture_output=True,
            check=True
        )

        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # Git not available
        return False


def generate_skill(candidate_id: str, verbose: bool = True) -> Optional[Path]:
    """Generate a complete skill package from a candidate."""
    # Load candidate
    candidate = load_candidate(candidate_id)
    if not candidate:
        if verbose:
            print(f"Candidate not found: {candidate_id}")
        return None

    skill_name = candidate["skill_name"]
    skill_dir = SKILLS_DIR / skill_name

    # Check if skill already exists
    if skill_dir.exists():
        if verbose:
            print(f"Skill already exists: {skill_name}")
        return None

    if verbose:
        print(f"Generating skill: {skill_name}")

    # Create skill directory
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)

    # Generate SKILL.md
    skill_md = generate_skill_md(candidate)
    with open(skill_dir / "SKILL.md", "w") as f:
        f.write(skill_md)
    if verbose:
        print("  - Created SKILL.md")

    # Generate skill.meta.json
    meta = generate_meta_json(candidate)
    with open(skill_dir / "skill.meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    if verbose:
        print("  - Created skill.meta.json")

    # Generate CHANGELOG.md
    changelog = generate_changelog(candidate)
    with open(skill_dir / "CHANGELOG.md", "w") as f:
        f.write(changelog)
    if verbose:
        print("  - Created CHANGELOG.md")

    # Generate reference doc
    ref_doc = generate_reference_doc(candidate)
    with open(skill_dir / "references" / "quick-reference.md", "w") as f:
        f.write(ref_doc)
    if verbose:
        print("  - Created references/quick-reference.md")

    # Create placeholder for scripts
    scripts_readme = f"""# Scripts for {skill_name}

Place helper scripts here. They will be available to the skill.

## Example

```bash
#!/bin/bash
# my-helper.sh
echo "Helper for {skill_name}"
```
"""
    with open(skill_dir / "scripts" / "README.md", "w") as f:
        f.write(scripts_readme)

    # Initialize git repository
    if init_git_repo(skill_dir, skill_name):
        if verbose:
            print("  - Initialized git repository")
            print("  - Created tag v1.0.0")
    else:
        if verbose:
            print("  - Git initialization skipped (git not available)")

    # Mark candidate as approved
    candidate["status"] = "approved"
    candidate["approved_at"] = datetime.utcnow().isoformat() + "Z"
    candidate_meta_file = CANDIDATES_DIR / candidate_id / "candidate.json"
    with open(candidate_meta_file, "w") as f:
        json.dump(candidate, f, indent=2)

    if verbose:
        print(f"\nSkill '{skill_name}' generated successfully!")
        print(f"Location: {skill_dir}")

    return skill_dir


def reject_candidate(candidate_id: str, verbose: bool = True) -> bool:
    """Reject a candidate and remove it."""
    candidate = load_candidate(candidate_id)
    if not candidate:
        if verbose:
            print(f"Candidate not found: {candidate_id}")
        return False

    # Mark as rejected
    candidate["status"] = "rejected"
    candidate["rejected_at"] = datetime.utcnow().isoformat() + "Z"

    candidate_dir = CANDIDATES_DIR / candidate_id
    candidate_meta_file = candidate_dir / "candidate.json"

    with open(candidate_meta_file, "w") as f:
        json.dump(candidate, f, indent=2)

    if verbose:
        print(f"Candidate '{candidate['skill_name']}' rejected.")

    return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Skill generator")
    parser.add_argument("action", choices=["generate", "reject"], help="Action to perform")
    parser.add_argument("candidate_id", help="Candidate ID")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    args = parser.parse_args()

    if args.action == "generate":
        result = generate_skill(args.candidate_id, verbose=not args.quiet)
        sys.exit(0 if result else 1)
    elif args.action == "reject":
        result = reject_candidate(args.candidate_id, verbose=not args.quiet)
        sys.exit(0 if result else 1)


if __name__ == "__main__":
    import sys
    main()

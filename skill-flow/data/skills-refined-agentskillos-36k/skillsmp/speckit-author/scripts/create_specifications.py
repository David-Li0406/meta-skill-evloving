#!/usr/bin/env python3
"""Interactive SpecKit tool - creates spec.md and plan.md in worktree.

This script runs interactively in a feature/release/hotfix worktree and:
1. Detects BMAD planning context from ../planning/<slug>/
2. Conducts interactive Q&A session (with or without BMAD context)
3. Generates spec.md and plan.md from templates
4. Creates compliant specs/<slug>/ directory structure
5. Commits changes to the feature branch

Note: TODO file updates are deprecated. Use GitHub Issues (--issue) and
specs/*/tasks.md for work item tracking instead.

Usage:
    python .claude/skills/speckit-author/scripts/create_specifications.py \\
        <workflow_type> <slug> <gh_user> [--issue <number>]

Example:
    python .claude/skills/speckit-author/scripts/create_specifications.py \\
        feature my-feature stharrold --issue 42

Constants:
- TIMESTAMP_FORMAT: YYYY-MM-DD (for spec headers)
  Rationale: Human-readable date format for documentation
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Constants with documented rationale
TIMESTAMP_FORMAT = "%Y-%m-%d"  # Human-readable date for documentation
VALID_WORKFLOW_TYPES = ["feature", "release", "hotfix"]  # Supported workflow types
TASK_PATTERN = re.compile(r"^####\s+Task\s+(\w+_\d+):\s+(.+)$", re.MULTILINE)  # Parse tasks from plan.md

# Global config for non-interactive mode
_CONFIG: dict | None = None
_CONFIG_PATH: list[str] = []  # Tracks path through nested config for lookups


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML or JSON file."""
    content = config_path.read_text()
    if config_path.suffix in [".yaml", ".yml"]:
        try:
            import yaml

            return yaml.safe_load(content)
        except ImportError:
            error_exit("PyYAML not installed. Use JSON config or: uv add pyyaml")
    else:
        return json.loads(content)


def get_config_value(key: str, default: str | None = None) -> str | None:
    """Get value from config at current path + key."""
    if _CONFIG is None:
        return None

    # Navigate to current path
    obj = _CONFIG
    for path_key in _CONFIG_PATH:
        if isinstance(obj, dict) and path_key in obj:
            obj = obj[path_key]
        else:
            return default

    # Get the value
    if isinstance(obj, dict) and key in obj:
        return obj[key]
    return default


def is_non_interactive() -> bool:
    """Check if running in non-interactive mode."""
    return _CONFIG is not None


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit with code."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def run_command(cmd: list[str], capture=True, check=True) -> str | None:
    """Run command and return output or None on error."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check)
            return None
    except subprocess.CalledProcessError as e:
        if check:
            error_exit(f"Command failed: {' '.join(cmd)}\n{e.stderr}")
        return None
    except FileNotFoundError:
        error_exit(f"Command not found: {cmd[0]}")


def detect_context() -> dict[str, any]:
    """Detect current worktree context and BMAD planning availability."""

    # Get repository root
    repo_root = Path(run_command(["git", "rev-parse", "--show-toplevel"]))
    current_dir = Path.cwd()
    current_branch = run_command(["git", "branch", "--show-current"])

    # Determine if in worktree by checking if .git is a file (not a directory)
    # In worktrees, .git is a file pointing to the main repo's worktrees directory
    git_path = current_dir / ".git"
    is_worktree = git_path.is_file()

    if not is_worktree:
        error_exit(
            "Not in a worktree. This script must be run from a feature/release/hotfix worktree.\n"
            f"Current directory: {current_dir}\n"
            f"Repository root: {repo_root}\n"
            "Create a worktree first using create_worktree.py"
        )

    return {
        "repo_root": repo_root,
        "current_dir": current_dir,
        "current_branch": current_branch,
        "is_worktree": is_worktree,
    }


def find_bmad_planning(slug: str) -> dict[str, Path] | None:
    """Check for BMAD planning documents in ../planning/<slug>/."""

    planning_dir = Path("..") / "planning" / slug

    if not planning_dir.exists():
        return None

    bmad_docs = {
        "planning_dir": planning_dir,
        "requirements": planning_dir / "requirements.md",
        "architecture": planning_dir / "architecture.md",
        "epics": planning_dir / "epics.md",
    }

    # Check which documents exist
    available = {key: path for key, path in bmad_docs.items() if key == "planning_dir" or path.exists()}

    if len(available) <= 1:  # Only planning_dir exists, no actual docs
        return None

    return available


def ask_question(prompt: str, options: list[str] | None = None, default: str | None = None, config_key: str | None = None) -> str:
    """Ask user a question and return response.

    In non-interactive mode, returns value from config file using config_key.
    Falls back to default if config_key not found.
    """
    # Non-interactive mode: return config value or default
    if is_non_interactive():
        if config_key:
            value = get_config_value(config_key, default)
            if value is not None:
                print(f"[config] {prompt}: {value}")
                return value
        if default:
            print(f"[default] {prompt}: {default}")
            return default
        error_exit(f"Non-interactive mode: no config value for '{config_key}' and no default")

    # Interactive mode
    if options:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}) {option}")

        if default:
            print(f"  [default: {default}]")

        while True:
            response = input("> ").strip()

            if not response and default:
                return default

            # Allow numeric selection
            if response.isdigit():
                idx = int(response) - 1
                if 0 <= idx < len(options):
                    return options[idx]

            # Allow direct text match
            if response in options:
                return response

            print("Invalid selection. Please try again.")
    else:
        if default:
            print(f"\n{prompt} [{default}]")
        else:
            print(f"\n{prompt}")

        response = input("> ").strip()
        return response if response else (default or "")


def ask_yes_no(prompt: str, default: bool = True, config_key: str | None = None) -> bool:
    """Ask yes/no question.

    In non-interactive mode, returns value from config file using config_key.
    Falls back to default if config_key not found.
    """
    # Non-interactive mode: return config value or default
    if is_non_interactive():
        if config_key:
            value = get_config_value(config_key)
            if value is not None:
                # Handle various truthy representations
                if isinstance(value, bool):
                    result = value
                elif isinstance(value, str):
                    result = value.lower() in ["y", "yes", "true", "1"]
                else:
                    result = bool(value)
                print(f"[config] {prompt}: {'yes' if result else 'no'}")
                return result
        print(f"[default] {prompt}: {'yes' if default else 'no'}")
        return default

    # Interactive mode
    default_str = "Y/n" if default else "y/N"
    response = input(f"\n{prompt} ({default_str}) > ").strip().lower()

    if not response:
        return default

    return response in ["y", "yes"]


def interactive_qa_with_bmad(bmad_docs: dict[str, Path], slug: str) -> dict[str, any]:
    """Conduct interactive Q&A when BMAD planning exists."""
    global _CONFIG_PATH

    print("\n" + "=" * 70)
    print("SpecKit Interactive Specification Tool")
    print("=" * 70)
    print(f"\n✓ Detected BMAD planning context: ../planning/{slug}/")

    # Display BMAD summary
    print("\nBMAD Summary:")

    if "requirements" in bmad_docs:
        req_text = bmad_docs["requirements"].read_text()
        fr_count = len(re.findall(r"FR-\d+", req_text))
        us_count = len(re.findall(r"US-\d+", req_text))
        print(f"  - Requirements: {fr_count} functional requirements, {us_count} user stories")

    if "architecture" in bmad_docs:
        arch_text = bmad_docs["architecture"].read_text()
        # Extract technology stack mentions
        stack_lines = [line for line in arch_text.split("\n") if any(tech in line.lower() for tech in ["python", "fastapi", "flask", "django", "postgresql", "sqlite"])]
        if stack_lines:
            print("  - Architecture: Technology stack defined")

    if "epics" in bmad_docs:
        epic_text = bmad_docs["epics"].read_text()
        epic_count = len(re.findall(r"E-\d+", epic_text))
        print(f"  - Epics: {epic_count} epics defined")

    print("\nImplementation Questions:")
    print("-" * 70)

    # Set config path for with_bmad section
    _CONFIG_PATH = ["with_bmad"]

    responses = {}

    # Database migrations (if database mentioned in architecture)
    if "architecture" in bmad_docs:
        arch_text = bmad_docs["architecture"].read_text().lower()
        if "database" in arch_text or "postgresql" in arch_text or "mysql" in arch_text:
            responses["migration_strategy"] = ask_question(
                "Database migrations strategy?",
                options=["Alembic (recommended)", "Manual SQL migrations", "None needed"],
                default="Alembic (recommended)",
                config_key="migration_strategy",
            )

    # Testing approach
    responses["include_e2e_tests"] = ask_yes_no(
        "Include end-to-end (E2E) tests?",
        default=False,
        config_key="include_e2e_tests",
    )

    responses["include_performance_tests"] = ask_yes_no(
        "Include performance/load tests?",
        default=False,
        config_key="include_performance_tests",
    )

    responses["include_security_tests"] = ask_yes_no(
        "Include security tests (OWASP checks)?",
        default=False,
        config_key="include_security_tests",
    )

    # Task granularity
    responses["task_granularity"] = ask_question(
        "Task granularity preference?",
        options=["Small tasks (1-2 hours each)", "Medium tasks (half-day each)", "Large tasks (full-day each)"],
        default="Small tasks (1-2 hours each)",
        config_key="task_granularity",
    )

    # Epic implementation order
    if "epics" in bmad_docs:
        responses["follow_epic_order"] = ask_yes_no(
            "Follow epic priority order from epics.md?",
            default=True,
            config_key="follow_epic_order",
        )

    # Additional implementation notes
    responses["additional_notes"] = ask_question(
        "Any additional implementation notes or constraints? (optional)",
        config_key="additional_notes",
        default="",
    )

    return responses


def interactive_qa_without_bmad(slug: str) -> dict[str, any]:
    """Conduct interactive Q&A when no BMAD planning exists."""
    global _CONFIG_PATH

    print("\n" + "=" * 70)
    print("SpecKit Interactive Specification Tool")
    print("=" * 70)
    print(f"\n⚠ No BMAD planning found for '{slug}'")
    print("I'll gather requirements through comprehensive Q&A.")
    print("\nRecommendation: Use BMAD planning for future features")
    print("=" * 70)

    # Set config path for without_bmad section
    _CONFIG_PATH = ["without_bmad"]

    responses = {}

    # Core requirements
    responses["purpose"] = ask_question(
        "What is the main purpose of this feature?",
        config_key="purpose",
    )

    responses["users"] = ask_question(
        "Who are the primary users of this feature?",
        config_key="users",
    )

    responses["success_criteria"] = ask_question(
        "How will success be measured? (metrics, goals)",
        config_key="success_criteria",
    )

    # Technology stack
    print("\nTechnology Stack:")

    responses["web_framework"] = ask_question(
        "Web framework (if applicable)?",
        options=["FastAPI", "Flask", "Django", "None"],
        default="None",
        config_key="web_framework",
    )

    responses["database"] = ask_question(
        "Database?",
        options=["SQLite (dev)", "PostgreSQL", "MySQL", "None"],
        default="None",
        config_key="database",
    )

    if responses["database"] != "None":
        responses["migration_strategy"] = ask_question(
            "Database migration strategy?",
            options=["Alembic", "Manual SQL", "None"],
            default="Alembic",
            config_key="migration_strategy",
        )

    responses["testing_framework"] = ask_question(
        "Testing framework?",
        options=["pytest (recommended)", "unittest", "other"],
        default="pytest (recommended)",
        config_key="testing_framework",
    )

    # Performance & security
    responses["performance_target"] = ask_question(
        "Performance target? (e.g., '<200ms response time', 'not critical')",
        config_key="performance_target",
        default="Standard performance",
    )

    responses["security_requirements"] = ask_question(
        "Security requirements? (e.g., 'authentication', 'encryption', 'none')",
        config_key="security_requirements",
        default="none",
    )

    # Testing preferences
    responses["target_coverage"] = ask_question(
        "Test coverage target?",
        default="80%",
        config_key="target_coverage",
    )

    responses["include_e2e_tests"] = ask_yes_no(
        "Include E2E tests?",
        default=False,
        config_key="include_e2e_tests",
    )

    responses["include_performance_tests"] = ask_yes_no(
        "Include performance tests?",
        default=False,
        config_key="include_performance_tests",
    )

    # Task breakdown
    responses["task_granularity"] = ask_question(
        "Task size preference?",
        options=["Small (1-2 hours)", "Medium (half-day)", "Large (full-day)"],
        default="Small (1-2 hours)",
        config_key="task_granularity",
    )

    return responses


def load_template(template_name: str) -> str:
    """Load template file from ../templates/."""

    # Get script directory and navigate to templates
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "templates" / template_name

    if not template_path.exists():
        error_exit(f"Template not found: {template_path}")

    return template_path.read_text()


def generate_spec_md(
    slug: str, workflow_type: str, gh_user: str, date: str, qa_responses: dict[str, any], bmad_docs: dict[str, Path] | None, issue_number: int | None = None
) -> str:
    """Generate spec.md from template."""

    spec_template = load_template("spec.md.template")

    # Replace placeholders
    title = slug.replace("-", " ").replace("_", " ").title()
    spec = spec_template.replace("{{TITLE}}", title)
    spec = spec.replace("{{WORKFLOW_TYPE}}", workflow_type)
    spec = spec.replace("{{SLUG}}", slug)
    spec = spec.replace("{{DATE}}", date)
    spec = spec.replace("{{GH_USER}}", gh_user)

    # Add Q&A context as comments in spec
    # (This helps Claude Code understand implementation preferences)
    context_section = "\n## Implementation Context\n\n"
    context_section += "<!-- Generated from SpecKit interactive Q&A -->\n\n"

    # Add issue reference if provided
    if issue_number:
        context_section += f"**GitHub Issue:** #{issue_number}\n\n"

    if bmad_docs:
        context_section += f"**BMAD Planning:** See `../planning/{slug}/` for complete requirements and architecture.\n\n"

    context_section += "**Implementation Preferences:**\n\n"
    for key, value in qa_responses.items():
        if value and value != "":
            formatted_key = key.replace("_", " ").title()
            context_section += f"- **{formatted_key}:** {value}\n"

    # Insert context section after ## Overview
    spec = spec.replace("## Requirements Reference", context_section + "\n## Requirements Reference")

    return spec


def parse_epics_from_bmad(epics_path: Path) -> list[dict[str, any]]:
    """Parse epic definitions from BMAD epics.md.

    Returns list of dicts with: epic_id, name, scope, components, acceptance_criteria, estimate
    """
    content = epics_path.read_text()
    epics = []

    # Match epic sections: ## E-XXX: Epic Name
    epic_pattern = re.compile(r"^## (E-\d+):\s+(.+?)$", re.MULTILINE)
    matches = list(epic_pattern.finditer(content))

    for i, match in enumerate(matches):
        epic_id = match.group(1)
        epic_name = match.group(2)

        # Extract epic content (from this match to next epic or end)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        epic_content = content[start:end]

        # Extract components (numbered lists under ### Components)
        components = []
        comp_match = re.search(r"### Components\s+(.*?)(?=###|$)", epic_content, re.DOTALL)
        if comp_match:
            comp_text = comp_match.group(1)
            components = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", comp_text, re.MULTILINE)

        # Extract acceptance criteria
        criteria = []
        ac_match = re.search(r"### Acceptance Criteria\s+(.*?)(?=###|$)", epic_content, re.DOTALL)
        if ac_match:
            criteria = re.findall(r"^-\s+\[.\]\s+(.+)$", ac_match.group(1), re.MULTILINE)

        # Extract estimate
        est_match = re.search(r"\*\*(\d+-\d+\s+hours?)\*\*", epic_content)
        estimate = est_match.group(1) if est_match else "TBD"

        epics.append({"epic_id": epic_id, "name": epic_name, "components": components, "acceptance_criteria": criteria, "estimate": estimate})

    return epics


def generate_plan_md(slug: str, workflow_type: str, date: str, qa_responses: dict[str, any], bmad_docs: dict[str, Path] | None) -> str:
    """Generate plan.md from BMAD epics or template."""

    title = slug.replace("-", " ").replace("_", " ").title()

    # If we have BMAD epics, generate tasks from them
    if bmad_docs and "epics" in bmad_docs:
        epics = parse_epics_from_bmad(bmad_docs["epics"])

        # Build plan.md with real tasks
        plan = f"# Implementation Plan: {title}\n\n"
        plan += f"**Type:** {workflow_type}\n"
        plan += f"**Slug:** {slug}\n"
        plan += f"**Date:** {date}\n\n"
        plan += "**Source:** Generated from BMAD planning epics\n\n"
        plan += "---\n\n"
        plan += "## Task Breakdown\n\n"

        # Convert each epic into tasks
        for i, epic in enumerate(epics, 1):
            epic_id = epic["epic_id"]
            epic_name = epic["name"]

            plan += f"### {epic_id}: {epic_name}\n\n"

            # Create one or more tasks based on components
            if epic["components"]:
                for j, component in enumerate(epic["components"], 1):
                    task_id = f"impl_{i:03d}_{j:02d}"
                    plan += f"#### Task {task_id}: {component}\n\n"
                    plan += f"**Estimated Time:** {epic['estimate']}\n"
                    plan += "**Priority:** High\n\n"
                    plan += f"**Epic:** {epic_id} - {epic_name}\n\n"

                    plan += "**Description:**\n"
                    plan += f"Implement {component.lower()} as part of {epic_name.lower()}.\n\n"

                    plan += "**Acceptance Criteria:**\n"
                    for criterion in epic["acceptance_criteria"]:
                        plan += f"- [ ] {criterion}\n"
                    plan += "\n"

                    plan += "**Verification:**\n```bash\n"
                    plan += "podman-compose run --rm dev uv run pytest tests/ -v\n"
                    plan += "```\n\n"
                    plan += "---\n\n"
            else:
                # Single task for epic without components
                task_id = f"impl_{i:03d}"
                plan += f"#### Task {task_id}: {epic_name}\n\n"
                plan += f"**Estimated Time:** {epic['estimate']}\n"
                plan += "**Priority:** High\n\n"
                plan += f"**Description:**\n{epic_name}\n\n"

                plan += "**Acceptance Criteria:**\n"
                for criterion in epic["acceptance_criteria"]:
                    plan += f"- [ ] {criterion}\n"
                plan += "\n"

                plan += "**Verification:**\n```bash\n"
                plan += "podman-compose run --rm dev uv run pytest tests/ -v\n"
                plan += "```\n\n"
                plan += "---\n\n"

        return plan

    # Fallback to template if no BMAD epics
    plan_template = load_template("plan.md.template")
    plan = plan_template.replace("{{TITLE}}", title)
    plan = plan.replace("{{WORKFLOW_TYPE}}", workflow_type)
    plan = plan.replace("{{SLUG}}", slug)
    plan = plan.replace("{{DATE}}", date)

    note = "\n<!-- Note: No BMAD epics found. Using template structure. -->\n\n"
    plan = plan.replace("## Task Breakdown", note + "## Task Breakdown")

    return plan


def parse_tasks_from_plan(plan_md: str) -> list[dict[str, str]]:
    """Parse task IDs and descriptions from plan.md."""

    tasks = []

    # Find all task headers matching pattern: #### Task impl_001: Description
    matches = TASK_PATTERN.findall(plan_md)

    for task_id, description in matches:
        # Determine category from task ID prefix
        category = task_id.split("_")[0]  # impl, test, doc, etc.

        tasks.append({"id": task_id, "description": description.strip(), "category": category, "status": "pending"})

    return tasks


def update_todo_file(todo_path: Path, tasks: list[dict[str, str]]) -> None:
    """Update TODO_*.md frontmatter with tasks from plan.md."""

    try:
        import yaml
    except ImportError:
        error_exit("PyYAML required for TODO updates. Install: pip install pyyaml or uv add pyyaml")

    if not todo_path.exists():
        print(f"⚠ TODO file not found: {todo_path}")
        print("  Skipping TODO update. Please update manually.")
        return

    content = todo_path.read_text()

    # Split frontmatter and body
    if not content.startswith("---"):
        print("⚠ TODO file missing YAML frontmatter")
        print("  Skipping TODO update. Please update manually.")
        return

    parts = content.split("---", 2)
    if len(parts) < 3:
        print("⚠ Invalid TODO file format")
        print("  Skipping TODO update. Please update manually.")
        return

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]

    # Initialize tasks section if not exists
    if "tasks" not in frontmatter:
        frontmatter["tasks"] = {}

    # Group tasks by category
    tasks_by_category = {}
    for task in tasks:
        category = task["category"]
        if category not in tasks_by_category:
            tasks_by_category[category] = []

        tasks_by_category[category].append({"id": task["id"], "description": task["description"], "status": task["status"]})

    # Update frontmatter with tasks
    for category, category_tasks in tasks_by_category.items():
        frontmatter["tasks"][category] = category_tasks

    # Update workflow progress
    if "workflow_progress" not in frontmatter:
        frontmatter["workflow_progress"] = {}

    frontmatter["workflow_progress"]["phase"] = 2
    frontmatter["workflow_progress"]["current_step"] = "2.4"
    frontmatter["workflow_progress"]["last_update"] = datetime.now(UTC).isoformat()

    # Write back
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_str}---{body}"
    todo_path.write_text(new_content)

    print(f"✓ Updated TODO file: {todo_path}")
    print(f"  Added {len(tasks)} tasks across {len(tasks_by_category)} categories")


def create_specs_directory(slug: str, workflow_type: str) -> Path:
    """Create specs/<slug>/ directory with required structure."""

    specs_dir = Path("specs") / slug
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Create CLAUDE.md
    claude_md = f"""# Claude Code Context: specs/{slug}

## Purpose

SpecKit specifications for {workflow_type} '{slug}'

## Directory Structure

```
specs/{slug}/
├── spec.md        # Detailed technical specification
├── plan.md        # Implementation task breakdown
├── CLAUDE.md      # This file
├── README.md      # Human-readable overview
└── ARCHIVED/      # Deprecated specs
```

## Files in This Directory

- **spec.md** - Complete technical specification with implementation details
- **plan.md** - Task breakdown (impl_*, test_*, doc_*) with acceptance criteria

## Usage

When implementing this feature:
1. Read spec.md for technical details
2. Follow plan.md task order
3. Update TODO_*.md task status as you complete each task
4. Refer to ../planning/{slug}/ for BMAD context (if available)

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../../planning/{slug}/CLAUDE.md](../../planning/{slug}/CLAUDE.md)** - BMAD Planning (if available)
"""

    (specs_dir / "CLAUDE.md").write_text(claude_md)

    # Create README.md
    readme = f"""# Specifications: {slug.replace("-", " ").title()}

## Overview

SpecKit specifications for {workflow_type} development.

## Files

- **spec.md** - Detailed technical specification
- **plan.md** - Implementation task breakdown

## Generated By

SpecKit Interactive Tool - `.claude/skills/speckit-author/scripts/create_specifications.py`

## Related

- BMAD Planning: `../../planning/{slug}/` (if available)
- Implementation: `../../src/`
- Tests: `../../tests/`
"""

    (specs_dir / "README.md").write_text(readme)

    # Create ARCHIVED/ subdirectory
    archived_dir = specs_dir / "ARCHIVED"
    archived_dir.mkdir(exist_ok=True)

    (archived_dir / "CLAUDE.md").write_text(f"# Claude Code Context: specs/{slug}/ARCHIVED\n\nArchived specifications and deprecated files.\n")

    (archived_dir / "README.md").write_text(f"# Archived: specs/{slug}\n\nDeprecated specification files are stored here.\n")

    return specs_dir


def commit_changes(slug: str, specs_dir: Path, todo_file: Path | None = None, issue_number: int | None = None) -> None:
    """Commit spec.md, plan.md, and optionally TODO updates."""

    # Git add files
    run_command(["git", "add", str(specs_dir)])

    if todo_file and todo_file.exists():
        run_command(["git", "add", str(todo_file)])

    # Create commit message with optional issue reference
    refs_line = ""
    if issue_number:
        refs_line = f"\nRefs: #{issue_number}"
    elif todo_file:
        refs_line = f"\nRefs: {todo_file.name}"

    commit_msg = f"""docs(spec): add SpecKit specifications for {slug}

Generated by SpecKit Interactive Tool:
- spec.md: Detailed technical specification
- plan.md: Implementation task breakdown{refs_line}
"""

    run_command(["git", "commit", "-m", commit_msg])

    print("\n✓ Committed changes to branch")


def main():
    """Main entry point for SpecKit interactive tool."""
    global _CONFIG

    parser = argparse.ArgumentParser(description="Interactive SpecKit tool - creates spec.md and plan.md in worktree")
    parser.add_argument("workflow_type", choices=VALID_WORKFLOW_TYPES, help="Workflow type: feature, release, or hotfix")
    parser.add_argument("slug", help="Feature slug (e.g., my-feature)")
    parser.add_argument("gh_user", help="GitHub username")
    parser.add_argument("--issue", type=int, default=None, help="GitHub Issue number to link (e.g., --issue 42)")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commit (for testing)")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to YAML/JSON config file for non-interactive mode. Config should have section: with_bmad (if BMAD planning exists) or without_bmad (if not).",
    )

    args = parser.parse_args()

    # Load config for non-interactive mode
    if args.config:
        if not args.config.exists():
            error_exit(f"Config file not found: {args.config}")
        _CONFIG = load_config(args.config)
        print(f"✓ Running in non-interactive mode with config: {args.config}")

    # 1. Detect context
    context = detect_context()
    print(f"Working in worktree: {context['current_dir']}")
    print(f"Branch: {context['current_branch']}")

    # 2. Display issue reference if provided
    if args.issue:
        print(f"✓ Linked to GitHub Issue: #{args.issue}")
    else:
        print("ℹ️  No GitHub Issue linked (use --issue to link)")

    # 3. Check for BMAD planning
    bmad_docs = find_bmad_planning(args.slug)

    # 4. Interactive Q&A
    if bmad_docs:
        qa_responses = interactive_qa_with_bmad(bmad_docs, args.slug)
    else:
        qa_responses = interactive_qa_without_bmad(args.slug)

    # 5. Generate specifications
    print("\n" + "=" * 70)
    print("Generating specifications...")
    print("=" * 70)

    date = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)

    spec_md = generate_spec_md(args.slug, args.workflow_type, args.gh_user, date, qa_responses, bmad_docs, issue_number=args.issue)

    plan_md = generate_plan_md(args.slug, args.workflow_type, date, qa_responses, bmad_docs)

    # 6. Create specs directory
    specs_dir = create_specs_directory(args.slug, args.workflow_type)

    # Write spec.md and plan.md
    spec_path = specs_dir / "spec.md"
    plan_path = specs_dir / "plan.md"

    spec_path.write_text(spec_md)
    plan_path.write_text(plan_md)

    print(f"✓ Created {spec_path} ({len(spec_md)} chars)")
    print(f"✓ Created {plan_path} ({len(plan_md)} chars)")

    # 7. Parse tasks (for informational purposes)
    tasks = parse_tasks_from_plan(plan_md)

    if not tasks:
        print("ℹ️  No tasks found in plan.md (template uses placeholders)")
        print("  Claude Code will populate plan.md with actual tasks")
    else:
        print(f"✓ Found {len(tasks)} tasks in plan.md")

    # 8. Commit changes
    if not args.no_commit:
        commit_changes(args.slug, specs_dir, None, issue_number=args.issue)
    else:
        print("\n⚠ Skipping commit (--no-commit flag)")

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio

        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(
            trigger_sync_completion(
                agent_id="research",
                action="documentation_complete",
                state_snapshot={
                    "slug": args.slug,
                    "workflow_type": args.workflow_type,
                    "spec_file": str(specs_dir / "spec.md"),
                    "plan_file": str(specs_dir / "plan.md"),
                    "tasks_generated": len(tasks) if tasks else 0,
                    "bmad_context_available": bmad_docs is not None,
                },
                context={"user": args.gh_user},
            )
        )
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    # 9. Summary
    print("\n" + "=" * 70)
    print("SpecKit Specifications Created Successfully!")
    print("=" * 70)
    print("\nFiles created:")
    print(f"  - {spec_path}")
    print(f"  - {plan_path}")
    print(f"  - {specs_dir}/CLAUDE.md")
    print(f"  - {specs_dir}/README.md")

    if args.issue:
        print(f"\nLinked to GitHub Issue: #{args.issue}")

    print("\nNext steps:")
    print("  1. Review spec.md and plan.md")
    print("  2. Implement tasks from plan.md")
    if args.issue:
        print(f"  3. Update GitHub Issue #{args.issue} with progress")
    else:
        print("  3. Track progress via GitHub Issues or specs/*/tasks.md")

    if bmad_docs:
        print(f"  4. Refer to ../planning/{args.slug}/ for BMAD context")

    print("")


if __name__ == "__main__":
    main()

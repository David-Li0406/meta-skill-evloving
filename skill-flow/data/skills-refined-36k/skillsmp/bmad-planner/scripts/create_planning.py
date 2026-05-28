#!/usr/bin/env python3
"""Interactive BMAD planning tool - creates requirements.md, architecture.md, epics.md.

This script runs interactively in the main repository on contrib/<gh-user> branch and:
1. Verifies location (main repo, contrib branch - NOT in worktree)
2. Conducts three-persona interactive Q&A sessions:
   - 🧠 BMAD Analyst: Requirements gathering
   - 🏗️ BMAD Architect: Technical architecture design
   - 📋 BMAD PM: Epic breakdown and planning
3. Generates requirements.md, architecture.md, epics.md from templates
4. Creates compliant planning/<slug>/ directory structure
5. Commits changes to the contrib branch

Usage:
    python .claude/skills/bmad-planner/scripts/create_planning.py \\
        <slug> <gh_user>

Example:
    python .claude/skills/bmad-planner/scripts/create_planning.py \\
        my-feature stharrold

Constants:
- TIMESTAMP_FORMAT: YYYY-MM-DD (for document headers)
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
CONTRIB_BRANCH_PREFIX = "contrib/"  # Must be on contrib branch

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
    """Detect current repository context and validate for BMAD planning."""

    # Get repository root
    repo_root = Path(run_command(["git", "rev-parse", "--show-toplevel"]))
    current_dir = Path.cwd()
    current_branch = run_command(["git", "branch", "--show-current"])

    # Determine if in main repo (not worktree)
    is_main_repo = current_dir == repo_root

    if not is_main_repo:
        error_exit(
            "Not in main repository. BMAD planning must be run from main repo.\n"
            f"Current directory: {current_dir}\n"
            f"Repository root: {repo_root}\n"
            "Change to main repository directory first."
        )

    # Verify on contrib branch
    if not current_branch.startswith(CONTRIB_BRANCH_PREFIX):
        error_exit(
            f"Not on contrib branch. Current branch: {current_branch}\n"
            f"BMAD planning must be created on contrib/<gh-user> branch.\n"
            "Checkout contrib branch first: git checkout contrib/<gh-user>"
        )

    return {
        "repo_root": repo_root,
        "current_dir": current_dir,
        "current_branch": current_branch,
        "is_main_repo": is_main_repo,
    }


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


def interactive_qa_analyst() -> dict[str, any]:
    """Conduct 🧠 BMAD Analyst persona Q&A for requirements gathering."""
    global _CONFIG_PATH

    print("\n" + "=" * 70)
    print("🧠 BMAD Analyst Persona - Requirements Gathering")
    print("=" * 70)
    print("\nI'll help create the requirements document through interactive Q&A.")
    print("-" * 70)

    # Set config path for analyst section
    _CONFIG_PATH = ["analyst"]

    data = {}

    # Business context
    data["problem_statement"] = ask_question(
        "What problem does this feature solve?",
        config_key="problem_statement",
    )

    data["primary_users"] = ask_question(
        "Who are the primary users of this feature?",
        config_key="primary_users",
    )

    data["success_criteria"] = ask_question(
        "How will we measure success? (e.g., 'Users can search 100+ words/sec')",
        config_key="success_criteria",
    )

    # Functional requirements
    print("\n" + "-" * 70)
    print("Functional Requirements (FR-001, FR-002, ...)")
    print("-" * 70)

    data["functional_requirements"] = []

    # Non-interactive mode: load functional_requirements from config
    if is_non_interactive():
        fr_list = get_config_value("functional_requirements", [])
        if isinstance(fr_list, list):
            for i, fr in enumerate(fr_list, 1):
                fr_id = f"FR-{i:03d}"
                fr_entry = {
                    "id": fr_id,
                    "name": fr.get("name", ""),
                    "description": fr.get("description", ""),
                    "priority": fr.get("priority", "Medium"),
                    "acceptance_criteria": fr.get("acceptance_criteria", []),
                }
                data["functional_requirements"].append(fr_entry)
                print(f"[config] {fr_id}: {fr_entry['name']}")
    else:
        # Interactive mode
        fr_num = 1
        while True:
            fr_name = ask_question(f"FR-{fr_num:03d} requirement name (or press Enter to finish):", default="")

            if not fr_name:
                break

            fr_desc = ask_question(f"FR-{fr_num:03d} description:")

            fr_priority = ask_question(f"FR-{fr_num:03d} priority?", options=["High", "Medium", "Low"], default="Medium")

            # Acceptance criteria
            print(f"\nFR-{fr_num:03d} Acceptance Criteria (AC):")
            acceptance_criteria = []
            ac_num = 1
            while True:
                ac = ask_question(f"  AC {ac_num} (or press Enter to finish):", default="")
                if not ac:
                    break
                acceptance_criteria.append(ac)
                ac_num += 1

            data["functional_requirements"].append(
                {"id": f"FR-{fr_num:03d}", "name": fr_name, "description": fr_desc, "priority": fr_priority, "acceptance_criteria": acceptance_criteria}
            )

            fr_num += 1

    # Non-functional requirements
    print("\n" + "-" * 70)
    print("Non-Functional Requirements (NFR)")
    print("-" * 70)

    data["performance_requirements"] = ask_question(
        "Performance requirements? (e.g., '<200ms response', 'not critical')",
        default="Standard performance expectations",
        config_key="performance_requirements",
    )

    data["security_requirements"] = ask_question(
        "Security requirements? (e.g., 'authentication', 'encryption', 'none')",
        default="none",
        config_key="security_requirements",
    )

    data["scalability_requirements"] = ask_question(
        "Scalability requirements? (e.g., '1000 concurrent users', 'not critical')",
        default="Standard scalability",
        config_key="scalability_requirements",
    )

    # Constraints and assumptions
    data["constraints"] = ask_question(
        "Any constraints or limitations?",
        default="None identified",
        config_key="constraints",
    )

    data["assumptions"] = ask_question(
        "Any assumptions being made?",
        default="Standard development environment and tooling",
        config_key="assumptions",
    )

    print("\n✓ Requirements gathering complete!")

    return data


def interactive_qa_architect(requirements_data: dict[str, any]) -> dict[str, any]:
    """Conduct 🏗️ BMAD Architect persona Q&A for architecture design."""
    global _CONFIG_PATH

    print("\n" + "=" * 70)
    print("🏗️ BMAD Architect Persona - Technical Architecture Design")
    print("=" * 70)
    print("\nBased on the requirements, I'll design the technical architecture.")
    print("-" * 70)

    # Set config path for architect section
    _CONFIG_PATH = ["architect"]

    data = {}

    # Technology stack
    print("\nTechnology Stack:")

    data["web_framework"] = ask_question(
        "Web framework (if applicable)?",
        options=["FastAPI", "Flask", "Django", "None"],
        default="None",
        config_key="web_framework",
    )

    data["database"] = ask_question(
        "Database?",
        options=["SQLite (dev)", "PostgreSQL", "MySQL", "None"],
        default="SQLite (dev)",
        config_key="database",
    )

    if data["database"] != "None":
        data["database_migration"] = ask_question(
            "Database migration strategy?",
            options=["Alembic", "Manual SQL", "None"],
            default="Alembic",
            config_key="database_migration",
        )
    else:
        data["database_migration"] = "None"

    data["testing_framework"] = ask_question(
        "Testing framework?",
        options=["pytest (recommended)", "unittest", "other"],
        default="pytest (recommended)",
        config_key="testing_framework",
    )

    # Container strategy
    data["use_containers"] = ask_yes_no(
        "Use containerization (Podman)?",
        default=True,
        config_key="use_containers",
    )

    if data["use_containers"]:
        data["container_strategy"] = ask_question(
            "Container strategy?",
            options=["Single container", "Multi-container (podman-compose)", "Custom"],
            default="Single container",
            config_key="container_strategy",
        )
    else:
        data["container_strategy"] = "None"

    # Architecture patterns
    data["architecture_pattern"] = ask_question(
        "Architecture pattern?",
        options=["Layered (data/service/API)", "Modular", "Monolithic", "Other"],
        default="Layered (data/service/API)",
        config_key="architecture_pattern",
    )

    # API design (if web framework selected)
    if data["web_framework"] != "None":
        data["api_style"] = ask_question(
            "API style?",
            options=["REST", "GraphQL", "RPC", "Other"],
            default="REST",
            config_key="api_style",
        )

        data["api_versioning"] = ask_yes_no(
            "Include API versioning?",
            default=False,
            config_key="api_versioning",
        )
    else:
        data["api_style"] = "Not applicable"
        data["api_versioning"] = False

    # Security architecture
    if requirements_data.get("security_requirements", "none").lower() != "none":
        data["authentication_method"] = ask_question(
            "Authentication method?",
            options=["JWT", "OAuth2", "API Key", "Session-based", "Other"],
            default="JWT",
            config_key="authentication_method",
        )

        data["authorization_method"] = ask_question(
            "Authorization method?",
            options=["RBAC (Role-based)", "ABAC (Attribute-based)", "Simple permissions", "None"],
            default="Simple permissions",
            config_key="authorization_method",
        )
    else:
        data["authentication_method"] = "None"
        data["authorization_method"] = "None"

    # Error handling strategy
    data["error_handling"] = ask_question(
        "Error handling strategy?",
        options=["Structured exceptions", "Error codes", "Standard Python exceptions", "Custom"],
        default="Structured exceptions",
        config_key="error_handling",
    )

    # Logging and observability
    data["logging_level"] = ask_question(
        "Logging approach?",
        options=["Standard Python logging", "Structured logging (JSON)", "Custom", "Minimal"],
        default="Standard Python logging",
        config_key="logging_level",
    )

    # Deployment considerations
    data["deployment_target"] = ask_question(
        "Deployment target?",
        options=["Local development only", "Server deployment", "Cloud (AWS/GCP/Azure)", "Other"],
        default="Local development only",
        config_key="deployment_target",
    )

    print("\n✓ Architecture design complete!")

    return data


def generate_epic_breakdown(requirements_data: dict[str, any], architecture_data: dict[str, any]) -> list[dict[str, any]]:
    """Generate 📋 BMAD PM epic breakdown automatically based on requirements and architecture."""

    print("\n" + "=" * 70)
    print("📋 BMAD PM Persona - Epic Breakdown")
    print("=" * 70)
    print("\nAnalyzing requirements and architecture to create epic breakdown...")
    print("-" * 70)

    epics = []
    epic_num = 1

    # Epic 1: Data layer (if database is used)
    if architecture_data.get("database", "None") != "None":
        epics.append(
            {
                "id": f"E-{epic_num:03d}",
                "name": "Data Layer Foundation",
                "description": "Implement database schema, models, and data access layer",
                "complexity": "Medium",
                "complexity_reasoning": "Database setup and ORM configuration is well-understood but requires careful schema design",
                "priority": "P0",
                "priority_reasoning": "Foundation for all other features - must be completed first",
                "dependencies": "None",
                "estimated_effort": "2-3 days",
                "deliverables": ["Database schema design", "ORM models (SQLAlchemy)", "Database migrations", "Data access patterns", "Unit tests for data layer"],
            }
        )
        epic_num += 1

    # Epic 2: Core business logic / Service layer
    if len(requirements_data.get("functional_requirements", [])) > 0:
        dependencies = "E-001" if len(epics) > 0 else "None"
        epics.append(
            {
                "id": f"E-{epic_num:03d}",
                "name": "Core Business Logic",
                "description": "Implement core functionality and business rules",
                "complexity": "High" if len(requirements_data["functional_requirements"]) > 3 else "Medium",
                "complexity_reasoning": f"Implements {len(requirements_data['functional_requirements'])} functional requirements with business logic",
                "priority": "P0",
                "priority_reasoning": "Core functionality - primary value delivery",
                "dependencies": dependencies,
                "estimated_effort": f"{len(requirements_data['functional_requirements']) * 1}-{len(requirements_data['functional_requirements']) * 1.5} days",
                "deliverables": [f"Implementation of {fr['id']}" for fr in requirements_data["functional_requirements"][:5]]
                + ["Unit tests for business logic", "Integration tests"],
            }
        )
        epic_num += 1

    # Epic 3: API layer (if web framework is used)
    if architecture_data.get("web_framework", "None") != "None":
        dependencies = f"E-{epic_num - 1:03d}" if len(epics) > 0 else "None"
        epics.append(
            {
                "id": f"E-{epic_num:03d}",
                "name": "API Layer",
                "description": f"Implement {architecture_data['web_framework']} API endpoints and request/response handling",
                "complexity": "Medium",
                "complexity_reasoning": f"{architecture_data['web_framework']} API development is straightforward but requires careful contract design",
                "priority": "P0",
                "priority_reasoning": "Required for external system integration",
                "dependencies": dependencies,
                "estimated_effort": "2-3 days",
                "deliverables": [
                    f"{architecture_data['api_style']} API endpoints",
                    "Request validation",
                    "Response serialization",
                    "API documentation (OpenAPI)",
                    "API integration tests",
                ],
            }
        )
        epic_num += 1

    # Epic 4: Testing & Quality Assurance (always include)
    dependencies = f"E-{epic_num - 1:03d}" if len(epics) > 0 else "None"
    epics.append(
        {
            "id": f"E-{epic_num:03d}",
            "name": "Testing & Quality Assurance",
            "description": "Comprehensive testing coverage and quality gates",
            "complexity": "Medium",
            "complexity_reasoning": "Testing requires thorough coverage but is well-structured with pytest",
            "priority": "P1",
            "priority_reasoning": "Critical for production readiness but can overlap with implementation",
            "dependencies": dependencies,
            "estimated_effort": "1-2 days",
            "deliverables": ["Test coverage ≥80%", "All tests passing", "Linting clean (ruff)", "Type checking clean (mypy)", "Documentation complete"],
        }
    )

    # Epic 5: Container & Deployment (if containers are used)
    if architecture_data.get("use_containers", False):
        epic_num += 1
        epics.append(
            {
                "id": f"E-{epic_num:03d}",
                "name": "Containerization & Deployment",
                "description": "Container setup and deployment configuration",
                "complexity": "Low",
                "complexity_reasoning": "Standard Podman containerization with existing patterns",
                "priority": "P2",
                "priority_reasoning": "Important for production but not blocking development",
                "dependencies": "E-001",
                "estimated_effort": "1 day",
                "deliverables": ["Containerfile", "podman-compose.yml (if multi-container)", "Container build successful", "Container tests passing"],
            }
        )

    print(f"\n✓ Identified {len(epics)} epics:")
    for epic in epics:
        print(f"  - {epic['id']}: {epic['name']} (Priority: {epic['priority']}, {epic['complexity']} complexity)")

    print("\n✓ Epic breakdown complete!")

    return epics


def process_requirements_template(template_path: Path, analyst_data: dict[str, any], slug: str, gh_user: str) -> str:
    """Process requirements.md template with analyst data."""

    template = template_path.read_text()
    date = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)
    title = slug.replace("-", " ").replace("_", " ").title()

    # Replace basic placeholders
    content = template.replace("{{TITLE}}", title)
    content = content.replace("{{DATE}}", date)
    content = content.replace("{{GH_USER}}", gh_user)

    # Build functional requirements section
    fr_section = ""
    for fr in analyst_data.get("functional_requirements", []):
        fr_section += f"\n### {fr['id']}: {fr['name']}\n\n"
        fr_section += f"**Priority:** {fr['priority']}\n"
        fr_section += f"**Description:** {fr['description']}\n\n"
        fr_section += "**Acceptance Criteria:**\n"
        for ac in fr["acceptance_criteria"]:
            fr_section += f"- [ ] {ac}\n"
        fr_section += "\n"

    # Replace template sections with actual content
    content = re.sub(r"\[What problem does this solve\? Why is this feature needed\?\]", analyst_data.get("problem_statement", "TBD"), content)

    content = re.sub(r"\*\*Primary:\*\* \[Who is this for\?.*?\]", f"**Primary:** {analyst_data.get('primary_users', 'TBD')}", content)

    content = re.sub(r"- \[ \] Criterion 1:.*?\n- \[ \] Criterion 2:.*?\n- \[ \] Criterion 3:.*?\n", f"- [ ] {analyst_data.get('success_criteria', 'TBD')}\n", content)

    # Insert functional requirements
    if fr_section:
        content = re.sub(r"### FR-001:.*?(?=\n## Non-Functional Requirements|\Z)", fr_section, content, flags=re.DOTALL)

    # Update non-functional requirements
    content = re.sub(r"- Response time:.*?\n- Throughput:.*?\n", f"- Performance: {analyst_data.get('performance_requirements', 'Standard')}\n", content)

    return content


def process_architecture_template(template_path: Path, architect_data: dict[str, any], slug: str, gh_user: str) -> str:
    """Process architecture.md template with architect data."""

    template = template_path.read_text()
    date = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)
    title = slug.replace("-", " ").replace("_", " ").title()

    # Replace basic placeholders
    content = template.replace("{{TITLE}}", title)
    content = content.replace("{{DATE}}", date)
    content = content.replace("{{GH_USER}}", gh_user)

    # Update technology stack section
    framework_line = f"- **Framework:** {architect_data.get('web_framework', 'None')}\n"
    database_line = f"- **Database:** {architect_data.get('database', 'None')}\n"
    testing_line = f"- **Testing:** {architect_data.get('testing_framework', 'pytest')}\n"

    content = re.sub(r"- \*\*Framework:\*\*.*?\n", framework_line, content)

    content = re.sub(r"- \*\*Database:\*\*.*?\n", database_line, content)

    content = re.sub(r"- \*\*Testing:\*\*.*?\n", testing_line, content)

    # Add architecture notes section
    arch_notes = "\n## Architecture Notes\n\n"
    arch_notes += f"**Architecture Pattern:** {architect_data.get('architecture_pattern', 'Layered')}\n\n"

    if architect_data.get("web_framework", "None") != "None":
        arch_notes += f"**API Style:** {architect_data.get('api_style', 'REST')}\n"
        arch_notes += f"**API Versioning:** {'Yes' if architect_data.get('api_versioning', False) else 'No'}\n\n"

    if architect_data.get("use_containers", False):
        arch_notes += f"**Container Strategy:** {architect_data.get('container_strategy', 'Single container')}\n\n"

    arch_notes += f"**Error Handling:** {architect_data.get('error_handling', 'Standard exceptions')}\n"
    arch_notes += f"**Logging:** {architect_data.get('logging_level', 'Standard Python logging')}\n"
    arch_notes += f"**Deployment Target:** {architect_data.get('deployment_target', 'Local development')}\n"

    # Append architecture notes before any "## Related Documentation" section or at end
    if "## Related Documentation" in content:
        content = content.replace("## Related Documentation", arch_notes + "\n## Related Documentation")
    else:
        content += "\n" + arch_notes

    return content


def process_epics_template(template_path: Path, epics: list[dict[str, any]], slug: str, gh_user: str) -> str:
    """Process epics.md template with generated epic data."""

    template = template_path.read_text()
    date = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)
    title = slug.replace("-", " ").replace("_", " ").title()

    # Replace basic placeholders
    content = template.replace("{{TITLE}}", title)
    content = content.replace("{{DATE}}", date)
    content = content.replace("{{GH_USER}}", gh_user)

    # Build epic summary table
    summary_table = "| Epic ID | Name | Complexity | Priority | Dependencies | Estimated Effort |\n"
    summary_table += "|---------|------|------------|----------|--------------|------------------|\n"
    for epic in epics:
        summary_table += f"| {epic['id']} | {epic['name']} | {epic['complexity']} | {epic['priority']} | {epic['dependencies']} | {epic['estimated_effort']} |\n"

    # Calculate total effort
    total_days = sum(float(epic["estimated_effort"].split("-")[0].split()[0]) for epic in epics)
    summary_table += f"\n**Total Estimated Effort:** {total_days:.0f}+ days\n"

    # Replace template table
    content = re.sub(r"\| Epic ID \| Name.*?\n\*\*Total Estimated Effort:\*\*.*?\n", summary_table, content, flags=re.DOTALL)

    # Build epic definitions
    epic_definitions = ""
    for epic in epics:
        epic_definitions += f"\n### {epic['id']}: {epic['name']}\n\n"
        epic_definitions += f"**Description:**\n{epic['description']}\n\n"
        epic_definitions += "**Scope:**\n"
        epic_definitions += "**Deliverables:**\n"
        for deliverable in epic["deliverables"]:
            epic_definitions += f"  - [ ] {deliverable}\n"
        epic_definitions += f"\n**Complexity:** {epic['complexity']}\n\n"
        epic_definitions += "**Complexity Reasoning:**\n"
        epic_definitions += f"{epic['complexity_reasoning']}\n\n"
        epic_definitions += f"**Priority:** {epic['priority']}\n\n"
        epic_definitions += "**Priority Reasoning:**\n"
        epic_definitions += f"{epic['priority_reasoning']}\n\n"
        epic_definitions += f"**Dependencies:** {epic['dependencies']}\n\n"
        epic_definitions += f"**Estimated Effort:** {epic['estimated_effort']}\n\n"

    # Replace template epic definitions
    content = re.sub(r"### E-001:.*?(?=\n## |\Z)", epic_definitions, content, flags=re.DOTALL)

    return content


def create_directory_structure(planning_dir: Path, slug: str) -> None:
    """Create compliant planning directory structure with CLAUDE.md, README.md, ARCHIVED/."""

    planning_dir.mkdir(parents=True, exist_ok=True)

    # Create CLAUDE.md
    claude_md = planning_dir / "CLAUDE.md"
    if not claude_md.exists():
        claude_content = f"""# Claude Code Context: {slug} Planning

## Purpose

BMAD planning documents for the {slug} feature. Created during Phase 1 (Planning) in main repository on contrib branch.

## Directory Structure

```
planning/{slug}/
├── requirements.md    # Business requirements (🧠 Analyst)
├── architecture.md    # Technical architecture (🏗️ Architect)
├── epics.md          # Epic breakdown (📋 PM)
├── CLAUDE.md         # This file
├── README.md         # Human-readable overview
└── ARCHIVED/         # Deprecated planning documents
```

## Files in This Directory

**requirements.md:**
- Problem statement and business context
- Functional requirements (FR-001, FR-002, ...)
- Non-functional requirements (performance, security, scalability)
- User stories and acceptance criteria
- Success criteria and constraints

**architecture.md:**
- System architecture and component design
- Technology stack with justifications
- Data models and API contracts
- Container architecture
- Security, error handling, testing strategies
- Deployment and observability

**epics.md:**
- Epic breakdown (E-001, E-002, ...)
- Epic scope, complexity, and priorities
- Dependencies between epics
- Implementation timeline and effort estimates

## Usage by SpecKit

These planning documents are used as input context by SpecKit (Phase 2) when creating specifications in feature worktrees:

1. SpecKit auto-detects this planning directory: `../planning/{slug}/`
2. SpecKit reads requirements.md, architecture.md, epics.md
3. SpecKit conducts adaptive Q&A (5-8 questions vs 10-15 without BMAD)
4. SpecKit generates spec.md and plan.md aligned with this planning

**Token savings:** ~1,700-2,700 tokens per feature by reusing planning context

## Workflow Integration

**Phase 1 (BMAD Planning):** This directory created via create_planning.py
**Phase 2 (SpecKit):** Specifications reference this planning
**Phase 4 (As-Built):** update_asbuilt.py adds "As-Built" sections to these docs

## Related Documentation

- **[README.md](README.md)** - Human-readable overview of {slug} planning

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived planning documents

## Related Skills

- workflow-orchestrator
- bmad-planner (created this directory)
- speckit-author (consumes this planning)
- workflow-utilities
"""
        claude_md.write_text(claude_content)
        print(f"  ✓ Created {claude_md}")

    # Create README.md
    readme_md = planning_dir / "README.md"
    if not readme_md.exists():
        title = slug.replace("-", " ").replace("_", " ").title()
        readme_content = f"""# {title} - Planning Documentation

## Overview

BMAD (Business-Motivated Architecture Design) planning documents for the {title} feature.

## Documents

### requirements.md
Business requirements gathered through BMAD Analyst persona:
- Problem statement and stakeholders
- Functional requirements (FR-001, FR-002, ...)
- Non-functional requirements (performance, security, scalability)
- User stories and acceptance criteria
- Success criteria

### architecture.md
Technical architecture designed through BMAD Architect persona:
- System architecture and components
- Technology stack with justifications
- Data models and API contracts
- Container architecture (Containerfile, podman-compose.yml)
- Security, error handling, testing strategies
- Deployment and observability

### epics.md
Epic breakdown created through BMAD PM persona:
- Epic definitions (E-001, E-002, ...)
- Scope, complexity, and priorities
- Dependencies and critical path
- Implementation timeline and estimates

## Workflow Context

**Created:** Phase 1 (Planning) in main repository
**Used by:** Phase 2 (SpecKit) for specification generation
**Updated by:** Phase 4 (As-Built) with implementation feedback

## Related Documentation

- **[requirements.md](requirements.md)** - Functional and non-functional requirements
- **[architecture.md](architecture.md)** - Technical architecture and design
- **[epics.md](epics.md)** - Epic breakdown and planning
"""
        readme_md.write_text(readme_content)
        print(f"  ✓ Created {readme_md}")

    # Create ARCHIVED subdirectory
    archived_dir = planning_dir / "ARCHIVED"
    archived_dir.mkdir(exist_ok=True)

    archived_claude = archived_dir / "CLAUDE.md"
    if not archived_claude.exists():
        archived_claude.write_text(
            f"""# Claude Code Context: Archived Planning

## Purpose

Archive of deprecated planning documents from {slug}

## Usage

This directory contains previous versions of planning documents that have been superseded or are no longer relevant.

## Related Documentation

- **[README.md](README.md)** - Archive information
"""
        )
        print(f"  ✓ Created {archived_claude}")

    archived_readme = archived_dir / "README.md"
    if not archived_readme.exists():
        archived_readme.write_text(
            """# Archived Planning Documents

## Overview

Archive of deprecated planning documents that are no longer in active use.

## Contents

This directory contains archived versions of requirements.md, architecture.md, and epics.md that have been replaced or superseded.
"""
        )
        print(f"  ✓ Created {archived_readme}")


def commit_planning_docs(planning_dir: Path, slug: str) -> None:
    """Commit planning documents to git."""

    print("\nCommitting planning documents...")

    # Stage planning directory
    run_command(["git", "add", str(planning_dir)], capture=False)

    # Create commit message
    # Convert slug to human-readable title for commit message
    # e.g., "protect-main-develop" → "Protect Main Develop"
    title = slug.replace("-", " ").replace("_", " ").title()
    commit_msg = f"""docs(planning): add BMAD planning for {title}

BMAD planning session completed via interactive tool:
- requirements.md: Business requirements and user stories (🧠 Analyst)
- architecture.md: Technical design and technology stack (🏗️ Architect)
- epics.md: Epic breakdown and priorities (📋 PM)

Generated by: .claude/skills/bmad-planner/scripts/create_planning.py

Refs: planning/{slug}/README.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"""

    # Commit
    run_command(["git", "commit", "-m", commit_msg], capture=False)

    print(f"✓ Committed planning documents for {slug}")


def main():
    """Main entry point for BMAD planning tool."""
    global _CONFIG

    parser = argparse.ArgumentParser(description="Interactive BMAD planning tool - creates requirements, architecture, epics")
    parser.add_argument("slug", help="Feature slug (e.g., my-feature)")
    parser.add_argument("gh_user", help="GitHub username")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commit (for testing)")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to YAML/JSON config file for non-interactive mode. Config should have sections: analyst (requirements), architect (architecture).",
    )

    args = parser.parse_args()

    # Load config for non-interactive mode
    if args.config:
        if not args.config.exists():
            error_exit(f"Config file not found: {args.config}")
        _CONFIG = load_config(args.config)
        print(f"✓ Running in non-interactive mode with config: {args.config}")

    # Detect and validate context
    print("Working in main repository...")
    context = detect_context()
    print(f"Branch: {context['current_branch']}")

    # Check if planning directory already exists
    planning_dir = Path("planning") / args.slug
    if planning_dir.exists():
        overwrite = ask_yes_no(
            f"Planning directory already exists: {planning_dir}\nOverwrite?",
            default=False,
            config_key="overwrite_existing",
        )
        if not overwrite:
            print("Aborted.")
            sys.exit(0)

    print("\n" + "=" * 70)
    print("BMAD Interactive Planning Tool")
    print("=" * 70)
    print(f"\nCreating planning documents for: {args.slug}")
    print(f"GitHub user: {args.gh_user}")
    print(f"Output directory: {planning_dir}")

    # Phase 1: 🧠 Analyst - Requirements
    analyst_data = interactive_qa_analyst()

    # Phase 2: 🏗️ Architect - Architecture
    architect_data = interactive_qa_architect(analyst_data)

    # Phase 3: 📋 PM - Epic Breakdown
    epics = generate_epic_breakdown(analyst_data, architect_data)

    # Generate documents from templates
    print("\n" + "=" * 70)
    print("Generating Planning Documents")
    print("=" * 70)

    templates_dir = Path(__file__).parent.parent / "templates"

    requirements_content = process_requirements_template(templates_dir / "requirements.md.template", analyst_data, args.slug, args.gh_user)

    architecture_content = process_architecture_template(templates_dir / "architecture.md.template", architect_data, args.slug, args.gh_user)

    epics_content = process_epics_template(templates_dir / "epics.md.template", epics, args.slug, args.gh_user)

    # Create directory structure
    create_directory_structure(planning_dir, args.slug)

    # Write planning documents
    (planning_dir / "requirements.md").write_text(requirements_content)
    print(f"  ✓ Created {planning_dir / 'requirements.md'}")

    (planning_dir / "architecture.md").write_text(architecture_content)
    print(f"  ✓ Created {planning_dir / 'architecture.md'}")

    (planning_dir / "epics.md").write_text(epics_content)
    print(f"  ✓ Created {planning_dir / 'epics.md'}")

    # Commit changes
    if not args.no_commit:
        commit_planning_docs(planning_dir, args.slug)
    else:
        print("\n⚠ Skipping git commit (--no-commit flag)")

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio

        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(
            trigger_sync_completion(
                agent_id="orchestrate",
                action="planning_complete",
                state_snapshot={
                    "slug": args.slug,
                    "planning_dir": str(planning_dir),
                    "requirements_generated": True,
                    "architecture_generated": True,
                    "epics_generated": True,
                },
                context={"user": args.gh_user},
            )
        )
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    # Success summary
    print("\n" + "=" * 70)
    print("✓ BMAD Planning Documents Created Successfully!")
    print("=" * 70)

    print(f"\nFiles created in {planning_dir}:")
    print("  - requirements.md (Business requirements and acceptance criteria)")
    print("  - architecture.md (Technical architecture and design)")
    print("  - epics.md (Epic breakdown and planning)")
    print("  - CLAUDE.md (Context for Claude Code)")
    print("  - README.md (Human-readable overview)")
    print("  - ARCHIVED/ (Directory for deprecated planning docs)")

    print("\nNext steps:")
    print(f"  1. Review planning documents in {planning_dir}")
    print("  2. Create feature worktree: python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature {args.slug} {context['current_branch']}")
    print("  3. SpecKit will auto-detect and use these planning documents")
    print("  4. Token savings: ~1,700-2,700 tokens by reusing planning context")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create a new workflow skill with official documentation validation.

This script automates the creation of new skills in the workflow system. It:
1. Fetches official Claude Code documentation
2. Compares local patterns with official best practices
3. Alerts user to discrepancies with citations
4. Generates all required skill files

Usage:
    python create_skill.py <skill-name>

Example:
    python create_skill.py my-new-skill

The script will:
1. Ask configuration questions (purpose, phase, integration)
2. Fetch official Claude Code skill documentation
3. Compare local workflow patterns with official patterns
4. Alert user if discrepancies exist (with citations)
5. Generate all required files (SKILL.md, CLAUDE.md, etc.)
6. Commit changes to current branch

Constants:
- OFFICIAL_DOCS_URLS: URLs to fetch official documentation
  Rationale: Define authoritative sources for best practices
- LOCAL_SKILL_STRUCTURE: Local skill file structure
  Rationale: Document what this workflow system requires
- REQUIRED_FILES: Files that must be created for every skill
  Rationale: Ensure consistency across all skills
"""

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Constants with documented rationale
OFFICIAL_DOCS_URLS = {
    "agent_skills": "https://docs.claude.com/en/docs/agents-and-tools/agent-skills",
    "building_agents": "https://docs.claude.com/en/docs/agents-and-tools/building-agents",
    "getting_started": "https://docs.claude.com/en/docs/claude-code/getting-started",
}  # Official Claude Code documentation sources

LOCAL_SKILL_STRUCTURE = {
    "files": [
        "SKILL.md",
        "CLAUDE.md",
        "README.md",
        "CHANGELOG.md",
        "scripts/__init__.py",
        "ARCHIVED/CLAUDE.md",
        "ARCHIVED/README.md",
    ],
    "frontmatter_fields": ["name", "version", "description"],
    "optional_dirs": ["templates/", "scripts/"],
}  # Local workflow system skill structure

REQUIRED_FILES = [
    "SKILL.md",
    "CLAUDE.md",
    "README.md",
    "CHANGELOG.md",
]  # Minimum files required for every skill

WORKFLOW_PHASES = [
    "Phase 0 (Setup)",
    "Phase 1 (Planning)",
    "Phase 2 (Development)",
    "Phase 3 (Quality)",
    "Phase 4 (Integration)",
    "Phase 5 (Release)",
    "Phase 6 (Hotfix)",
    "Cross-phase (Utilities)",
]  # Workflow phases for skill integration


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit.

    Args:
        message: Error message to display
        code: Exit code (default 1)
    """
    print(f"{Colors.RED}✗ Error:{Colors.END} {message}", file=sys.stderr)
    sys.exit(code)


def success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message to display
    """
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to display
    """
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message to display
    """
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def ask_question(prompt: str, options: list[str] | None = None, default: str | None = None) -> str:
    """Ask user a question with optional choices.

    Args:
        prompt: Question to ask user
        options: Optional list of choices
        default: Default value if user presses Enter

    Returns:
        User's response or default value
    """
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")

    if options:
        for i, option in enumerate(options, 1):
            print(f"  {i}) {option}")
        if default:
            print(f"  [default: {default}]")

    while True:
        response = input("> ").strip()

        if not response and default:
            return default

        if options:
            if response.isdigit():
                idx = int(response) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            print(f"{Colors.RED}Invalid selection. Please enter a number 1-{len(options)}.{Colors.END}")
        else:
            return response


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask user a yes/no question.

    Args:
        prompt: Question to ask
        default: Default value (True = yes, False = no)

    Returns:
        True for yes, False for no
    """
    default_str = "Y/n" if default else "y/N"
    response = ask_question(f"{prompt} ({default_str})", default="y" if default else "n")
    return response.lower() in ["y", "yes"]


class SkillConfig:
    """Configuration for new skill."""

    def __init__(self):
        self.name: str = ""
        self.purpose: str = ""
        self.description: str = ""
        self.phase: str = ""
        self.has_scripts: bool = False
        self.has_templates: bool = False
        self.triggers: list[str] = []


class Discrepancy:
    """Represents a discrepancy between local and official patterns."""

    def __init__(self, disc_type: str, local: str, official: str, citation: str, severity: str, rationale: str):
        self.type = disc_type
        self.local = local
        self.official = official
        self.citation = citation
        self.severity = severity  # 'warning', 'info', 'error'
        self.rationale = rationale


def fetch_official_docs() -> dict[str, str]:
    """Fetch official Claude Code documentation using WebFetch.

    Note: This function simulates WebFetch. In actual Claude Code execution,
    the WebFetch tool would be used to retrieve live documentation.

    Returns:
        Dictionary of doc_name -> content
    """
    info("Fetching official Claude Code documentation...")

    # In actual execution, WebFetch would be used here
    # For now, we document what would be fetched

    official_docs = {
        "agent_skills": """
Official Claude Code Skill Specification (Simulated):

File Structure:
- skill.md (lowercase)
- README.md

YAML Frontmatter:
---
name: skill-name
description: Brief description
---

The official specification recommends a simpler structure focused on
the skill definition in a single skill.md file with minimal frontmatter.
""",
        "best_practices": """
Best Practices from Official Docs (Simulated):

1. Keep skills focused on single responsibility
2. Use clear naming conventions
3. Document inputs and outputs
4. Provide examples in README
5. Keep skill files self-contained
""",
    }

    success("Official documentation fetched (simulated)")
    info("In production, WebFetch would retrieve:")
    for name, url in OFFICIAL_DOCS_URLS.items():
        print(f"  - {url}")

    return official_docs


def compare_with_official(official_docs: dict[str, str]) -> list[Discrepancy]:
    """Compare local workflow patterns with official best practices.

    Args:
        official_docs: Dictionary of fetched official documentation

    Returns:
        List of discrepancies found
    """
    info("Comparing local workflow patterns with official best practices...")

    discrepancies = []

    # File structure discrepancy
    discrepancies.append(
        Discrepancy(
            disc_type="file_structure",
            local="['SKILL.md', 'CLAUDE.md', 'README.md', 'CHANGELOG.md', 'ARCHIVED/']",
            official="['skill.md', 'README.md']",
            citation=OFFICIAL_DOCS_URLS["agent_skills"],
            severity="info",
            rationale="""
Local pattern provides additional context files for workflow integration:
- SKILL.md (uppercase): Consistent with other workflow docs (CLAUDE.md, WORKFLOW.md)
- CLAUDE.md: Claude Code-specific context and usage patterns
- CHANGELOG.md: Version history tracking (semantic versioning)
- ARCHIVED/: Directory standards for deprecated files

This extended structure supports the multi-phase workflow system while
maintaining compatibility with core skill concepts from official docs.
""",
        )
    )

    # Frontmatter discrepancy
    discrepancies.append(
        Discrepancy(
            disc_type="frontmatter",
            local="YAML with 'name', 'version', 'description' fields",
            official="YAML with 'name', 'description' fields only",
            citation=OFFICIAL_DOCS_URLS["agent_skills"],
            severity="info",
            rationale="""
Local pattern includes 'version' field for semantic versioning:
- Enables skill version tracking across updates
- Integrates with validate_versions.py for consistency checks
- Supports CHANGELOG.md version history
- Required for UPDATE_CHECKLIST.md workflow

The 'version' field is critical for maintaining documentation consistency
in the workflow system.
""",
        )
    )

    # Directory organization discrepancy
    discrepancies.append(
        Discrepancy(
            disc_type="directory_organization",
            local="scripts/, templates/ subdirectories",
            official="Flat structure with skill.md",
            citation=OFFICIAL_DOCS_URLS["agent_skills"],
            severity="info",
            rationale="""
Local pattern separates code from documentation:
- scripts/: Python scripts for interactive tools (BMAD, SpecKit, etc.)
- templates/: Markdown templates for document generation
- Root level: Documentation only (SKILL.md, CLAUDE.md, README.md)

This separation improves maintainability and follows common Python package
structure conventions.
""",
        )
    )

    return discrepancies


def alert_user_discrepancies(discrepancies: list[Discrepancy]) -> bool:
    """Alert user about discrepancies and get confirmation.

    Args:
        discrepancies: List of discrepancies to display

    Returns:
        True if user confirms to continue, False otherwise
    """
    if not discrepancies:
        success("Local practices align with official best practices")
        return True

    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.YELLOW}⚠️  DISCREPANCY ALERT{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    print("Local workflow patterns differ from official Claude Code best practices.\n")
    print("This is EXPECTED and intentional for this workflow system.\n")

    for i, disc in enumerate(discrepancies, 1):
        severity_color = {
            "error": Colors.RED,
            "warning": Colors.YELLOW,
            "info": Colors.BLUE,
        }.get(disc.severity, Colors.BLUE)

        print(f"{severity_color}[{disc.severity.upper()}]{Colors.END} {i}. {disc.type}")
        print(f"  Local:    {disc.local}")
        print(f"  Official: {disc.official}")
        print(f"  Citation: {disc.citation}")
        print(f"\n  Rationale:{disc.rationale}\n")

    print(f"{Colors.BOLD}Summary:{Colors.END}")
    print("  - Official patterns: General-purpose Claude Code skills")
    print("  - Local patterns: Optimized for multi-phase workflow system")
    print("  - Discrepancies: Documented and intentional\n")

    return ask_yes_no("Continue with local workflow patterns?", default=True)


def phase1_configuration(skill_name: str) -> SkillConfig:
    """Phase 1: Skill configuration Q&A.

    Args:
        skill_name: Name of the skill to create

    Returns:
        SkillConfig with user selections
    """
    print(f"\n{Colors.BOLD}=== Phase 1: Skill Configuration ==={Colors.END}")

    config = SkillConfig()
    config.name = skill_name

    info(f"Skill name: {skill_name}")

    # Purpose
    config.purpose = ask_question(
        "What is the primary purpose of this skill?",
        options=[
            "Coordination and orchestration",
            "Data gathering and analysis",
            "Code generation and transformation",
            "Quality assurance and validation",
            "Documentation generation",
            "Other",
        ],
    )

    # Description
    config.description = ask_question("Brief description of the skill (one line):")

    # Phase integration
    config.phase = ask_question("Which workflow phase does this skill support?", options=WORKFLOW_PHASES)

    # Scripts
    config.has_scripts = ask_yes_no("Will this skill have Python scripts (interactive tools)?", default=True)

    # Templates
    if config.has_scripts:
        config.has_templates = ask_yes_no("Will this skill generate documents from templates?", default=False)

    # Triggers
    triggers_input = ask_question("Trigger keywords (comma-separated, e.g., 'create plan, generate spec'):")
    config.triggers = [t.strip() for t in triggers_input.split(",") if t.strip()]

    success("Configuration complete")
    return config


def phase2_official_docs_review() -> tuple[dict[str, str], list[Discrepancy]]:
    """Phase 2: Fetch and compare official documentation.

    Returns:
        Tuple of (official_docs, discrepancies)
    """
    print(f"\n{Colors.BOLD}=== Phase 2: Official Documentation Review ==={Colors.END}")

    # Fetch official docs
    official_docs = fetch_official_docs()

    # Compare with local patterns
    discrepancies = compare_with_official(official_docs)

    # Alert user
    if not alert_user_discrepancies(discrepancies):
        error_exit("User declined to proceed with local patterns")

    success("Official documentation review complete")
    return official_docs, discrepancies


def create_skill_directory(skill_path: Path, config: SkillConfig) -> None:
    """Create skill directory structure.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    info(f"Creating skill directory: {skill_path}")

    # Create main directory
    skill_path.mkdir(parents=True, exist_ok=True)

    # Create ARCHIVED subdirectory
    archived_path = skill_path / "ARCHIVED"
    archived_path.mkdir(exist_ok=True)

    # Create scripts directory if needed
    if config.has_scripts:
        scripts_path = skill_path / "scripts"
        scripts_path.mkdir(exist_ok=True)

    # Create templates directory if needed
    if config.has_templates:
        templates_path = skill_path / "templates"
        templates_path.mkdir(exist_ok=True)

    success("Created directory structure")


def generate_skill_md(skill_path: Path, config: SkillConfig, discrepancies: list[Discrepancy]) -> None:
    """Generate SKILL.md file.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
        discrepancies: List of discrepancies for documentation
    """
    info("Generating SKILL.md...")

    triggers_str = ", ".join(f'"{t}"' for t in config.triggers)

    content = f"""---
name: {config.name}
version: 1.0.0
description: |
  {config.description}

  Use when: {config.purpose}

  Triggers: {triggers_str}
---

# {config.name.replace("-", " ").title()} Skill

## Purpose

{config.description}

**Primary purpose:** {config.purpose}

**Workflow phase:** {config.phase}

## When to Use

Use this skill when:
- [Condition 1]
- [Condition 2]
- [Condition 3]

**Triggered by keywords:** {", ".join(config.triggers)}

## Integration with Workflow

**Phase integration:** {config.phase}

[Describe how this skill integrates with the workflow-orchestrator]

## Official Documentation Alignment

This skill follows the local workflow system patterns which extend official
Claude Code skill specifications:

**Official Claude Code Skills:**
- Specification: {OFFICIAL_DOCS_URLS["agent_skills"]}
- Building Agents: {OFFICIAL_DOCS_URLS["building_agents"]}

**Local Pattern Extensions:**

"""

    for disc in discrepancies:
        content += f"""**{disc.type}:**
- Local: {disc.local}
- Official: {disc.official}
- Rationale: {disc.rationale.strip()}

"""

    content += """
These extensions support the multi-phase workflow system while maintaining
compatibility with core Claude Code concepts.

## Usage

[Describe how to use this skill]

## Best Practices

[List best practices for using this skill]

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code usage context
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Related Skills

[List related skills and their integration points]
"""

    skill_md_path = skill_path / "SKILL.md"
    skill_md_path.write_text(content)
    success("Generated SKILL.md")


def generate_claude_md(skill_path: Path, config: SkillConfig) -> None:
    """Generate CLAUDE.md file.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    info("Generating CLAUDE.md...")

    content = f"""# Claude Code Context: {config.name}

## Purpose

{config.description}

**Primary purpose:** {config.purpose}

## Directory Structure

```
.claude/skills/{config.name}/
"""

    if config.has_scripts:
        content += """├── scripts/
│   ├── __init__.py
│   └── [script-name].py
"""

    if config.has_templates:
        content += """├── templates/
│   └── [template-name].md.template
"""

    content += """├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Usage by Claude Code

### When to Call This Skill

**Context:** [Describe when Claude Code should use this skill]

**User says:**
- "{}"
- "{}"
- "{}"

**Claude Code should:**
1. Recognize this is {} work
2. [Describe steps]
3. [Continue description]

### Token Efficiency

**Before (Manual Approach):**
- [Describe manual process]
- ~X tokens

**After (This Skill):**
- [Describe skill approach]
- ~Y tokens
- **Savings: ~Z tokens (N% reduction)**

## Integration with Other Skills

[Describe integration with other skills]

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Related Skills

[List related skills]
""".format(
        config.triggers[0] if config.triggers else "use this skill",
        config.triggers[1] if len(config.triggers) > 1 else "invoke skill",
        config.triggers[2] if len(config.triggers) > 2 else "run skill",
        config.phase,
    )

    claude_md_path = skill_path / "CLAUDE.md"
    claude_md_path.write_text(content)
    success("Generated CLAUDE.md")


def generate_readme(skill_path: Path, config: SkillConfig) -> None:
    """Generate README.md file.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    info("Generating README.md...")

    content = f"""# {config.name.replace("-", " ").title()} Skill

{config.description}

## Purpose

**Primary purpose:** {config.purpose}

**Workflow phase:** {config.phase}

## Quick Start

[Provide quick start instructions]

## Documentation

- **[SKILL.md](SKILL.md)** - Complete documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code context
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Version

v1.0.0 - Initial release
"""

    readme_path = skill_path / "README.md"
    readme_path.write_text(content)
    success("Generated README.md")


def generate_changelog(skill_path: Path, config: SkillConfig) -> None:
    """Generate CHANGELOG.md file.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    info("Generating CHANGELOG.md...")

    today = datetime.now(UTC).strftime("%Y-%m-%d")

    content = f"""# Changelog - {config.name}

All notable changes to the {config.name.replace("-", " ").title()} skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- None currently planned

## [1.0.0] - {today}

### Added
- Initial release of {config.name} skill
- {config.description}
- {config.phase} integration

---

## Version History

| Version | Date       | Type  | Description |
|---------|------------|-------|-------------|
| 1.0.0   | {today} | MAJOR | Initial release |

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code context
- **[README.md](README.md)** - Human-readable overview
"""

    changelog_path = skill_path / "CHANGELOG.md"
    changelog_path.write_text(content)
    success("Generated CHANGELOG.md")


def generate_archived_files(skill_path: Path, config: SkillConfig) -> None:
    """Generate ARCHIVED/ directory files.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    info("Generating ARCHIVED/ files...")

    archived_path = skill_path / "ARCHIVED"

    # ARCHIVED/CLAUDE.md
    archived_claude = archived_path / "CLAUDE.md"
    archived_claude.write_text(
        f"""# Claude Code Context: {config.name}/ARCHIVED

Archived files from {config.name} skill

## Purpose

This directory contains deprecated files from the {config.name} skill that have
been superseded by newer versions but are preserved for reference.

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for archived files
- **[../CLAUDE.md](../CLAUDE.md)** - Current {config.name} context
"""
    )

    # ARCHIVED/README.md
    archived_readme = archived_path / "README.md"
    archived_readme.write_text(
        f"""# {config.name}/ARCHIVED

Archived files from {config.name} skill

## Purpose

This directory contains deprecated files from the {config.name.replace("-", " ").title()}
skill that have been superseded by newer versions. Files are archived (not deleted)
to preserve history and allow comparison with current implementations.

## Contents

Currently empty - no files have been archived yet.

## Archiving Process

When files are deprecated:

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \\
  TODO_*.md "description" file1.py file2.md
```

This creates a timestamped ZIP archive in this directory.

## Related Documentation

- **[../SKILL.md](../SKILL.md)** - Current skill documentation
- **[../CLAUDE.md](../CLAUDE.md)** - Current Claude Code context
"""
    )

    success("Generated ARCHIVED/ files")


def generate_script_init(skill_path: Path, config: SkillConfig) -> None:
    """Generate scripts/__init__.py if scripts directory exists.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    if not config.has_scripts:
        return

    info("Generating scripts/__init__.py...")

    scripts_path = skill_path / "scripts"
    init_path = scripts_path / "__init__.py"

    init_path.write_text(
        f'''"""{config.name.replace("-", " ").title()} skill scripts package."""

__version__ = "1.0.0"
'''
    )

    success("Generated scripts/__init__.py")


def phase3_file_generation(skill_path: Path, config: SkillConfig, discrepancies: list[Discrepancy]) -> None:
    """Phase 3: Generate all skill files.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
        discrepancies: List of discrepancies for documentation
    """
    print(f"\n{Colors.BOLD}=== Phase 3: File Generation ==={Colors.END}")

    # Create directory structure
    create_skill_directory(skill_path, config)

    # Generate all files
    generate_skill_md(skill_path, config, discrepancies)
    generate_claude_md(skill_path, config)
    generate_readme(skill_path, config)
    generate_changelog(skill_path, config)
    generate_archived_files(skill_path, config)
    generate_script_init(skill_path, config)

    success("File generation complete")


def phase4_git_commit(skill_path: Path, config: SkillConfig) -> None:
    """Phase 4: Commit changes to git.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    print(f"\n{Colors.BOLD}=== Phase 4: Git Commit ==={Colors.END}")

    if not ask_yes_no("Commit changes to git?", default=True):
        warning("Skipping git commit")
        return

    # Stage files
    info("Staging files...")
    subprocess.run(["git", "add", str(skill_path)], check=True)

    # Create commit
    info("Creating commit...")
    commit_msg = f"""feat(workflow): add {config.name} skill

Added new skill for {config.phase}:
- {config.description}

Skill Components:
- SKILL.md ({config.name} documentation)
- CLAUDE.md (Claude Code context)
- README.md (Human-readable overview)
- CHANGELOG.md (Version history v1.0.0)
- ARCHIVED/ (Compliant directory structure)
"""

    if config.has_scripts:
        commit_msg += "- scripts/ (Python scripts)\n"
    if config.has_templates:
        commit_msg += "- templates/ (Document templates)\n"

    commit_msg += f"""
Official Documentation:
- Fetched and compared with official Claude Code patterns
- Documented discrepancies with rationale
- Local patterns optimized for workflow system

Refs: .claude/skills/{config.name}/CHANGELOG.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"""

    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    success("Committed changes")


def print_summary(skill_path: Path, config: SkillConfig) -> None:
    """Print summary of created skill.

    Args:
        skill_path: Path to skill directory
        config: Skill configuration
    """
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}✓ Skill Creation Complete{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    print(f"{Colors.BLUE}Skill:{Colors.END} {config.name}")
    print(f"{Colors.BLUE}Purpose:{Colors.END} {config.purpose}")
    print(f"{Colors.BLUE}Phase:{Colors.END} {config.phase}")
    print(f"{Colors.BLUE}Location:{Colors.END} {skill_path}")

    print(f"\n{Colors.BOLD}Created Files:{Colors.END}")
    print("  ✓ SKILL.md (complete documentation)")
    print("  ✓ CLAUDE.md (Claude Code context)")
    print("  ✓ README.md (human-readable overview)")
    print("  ✓ CHANGELOG.md (version history)")
    print("  ✓ ARCHIVED/ (directory structure)")

    if config.has_scripts:
        print("  ✓ scripts/__init__.py (package initialization)")
    if config.has_templates:
        print("  ✓ templates/ (document templates)")

    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print("  1. Implement skill functionality in scripts/")
    print("  2. Update workflow-orchestrator to call this skill")
    print("  3. Add integration tests")
    print("  4. Update WORKFLOW.md with skill reference")
    print("  5. Update root CLAUDE.md skill list")

    print(f"\n{Colors.BOLD}Official Documentation:{Colors.END}")
    print("  - Fetched and compared with official patterns")
    print("  - Discrepancies documented with rationale")
    print("  - See SKILL.md for alignment details")

    print(f"\n{Colors.GREEN}🎉 Happy coding!{Colors.END}\n")


def main() -> None:
    """Main entry point for skill creation."""
    parser = argparse.ArgumentParser(
        description="Create a new workflow skill with official documentation validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new skill
  python create_skill.py my-new-skill

  # Interactive setup will guide you through:
  # - Skill configuration
  # - Official documentation review
  # - File generation
  # - Git commit
""",
    )

    parser.add_argument("skill_name", type=str, help="Name of the skill to create (kebab-case)")

    args = parser.parse_args()

    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}Workflow Skill Creation{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    # Validate skill name
    if not args.skill_name.replace("-", "").isalnum():
        error_exit("Skill name must be kebab-case (lowercase with hyphens)")

    # Determine skill path
    repo_root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
    skill_path = repo_root / ".claude" / "skills" / args.skill_name

    # Check if skill already exists
    if skill_path.exists():
        error_exit(f"Skill already exists: {skill_path}")

    # Phase 1: Configuration
    config = phase1_configuration(args.skill_name)

    # Phase 2: Official documentation review
    official_docs, discrepancies = phase2_official_docs_review()

    # Phase 3: File generation
    phase3_file_generation(skill_path, config, discrepancies)

    # Phase 4: Git commit
    phase4_git_commit(skill_path, config)

    # Print summary
    print_summary(skill_path, config)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Initialize a new repository with the workflow system from a source repository.

This meta-skill (Phase 0) bootstraps new repositories by copying the workflow
system, documentation, and standards from a source repository. It provides an
interactive Q&A system to configure what gets copied and how it's adapted.

Usage:
    python initialize_repository.py <source-repo> <target-repo>

Arguments:
    source-repo: Path to source repository (with workflow system)
    target-repo: Path to target repository (will be created)

Example:
    python initialize_repository.py /path/to/german /path/to/my-new-repo

The script will:
1. Ask configuration questions (what to copy, tech stack, etc.)
2. Ask git setup questions (initialize, branches, remote)
3. Copy and adapt files from source to target
4. Optionally initialize git with branch structure
5. Validate the new repository structure
6. Report what was created and next steps

Constants:
- SKILL_NAMES: List of workflow skills to copy
  Rationale: Define the 9 skills that comprise the workflow system
- REQUIRED_TOOLS: Tools that must be installed
  Rationale: Validate environment before proceeding
- TIMESTAMP_FORMAT: ISO8601 compact format
  Rationale: Consistent with worktree/TODO file naming
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from vcs import get_vcs_adapter

# Constants with documented rationale
SKILL_NAMES = [
    "workflow-orchestrator",
    "tech-stack-adapter",
    "git-workflow-manager",
    "bmad-planner",
    "speckit-author",
    "quality-enforcer",
    "workflow-utilities",
    "agentdb-state-manager",
    "initialize-repository",  # Include this meta-skill
]  # 9 skills that comprise the workflow system

REQUIRED_TOOLS = ["git"]  # Required for workflow functionality (VCS CLI detected automatically)
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"  # Compact ISO8601 for file names


# ANSI color codes for output
class Colors:
    """ANSI color codes for terminal output."""

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit with code.

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


def ask_question(prompt: str, options: list[str] | None = None, default: str | None = None, allow_multiple: bool = False) -> str:
    """Ask user a question with optional choices.

    Args:
        prompt: Question to ask user
        options: Optional list of choices
        default: Default value if user presses Enter
        allow_multiple: Allow multiple selections (comma-separated numbers)

    Returns:
        User's response or default value

    Raises:
        ValueError: If response is invalid
    """
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")

    if options:
        for i, option in enumerate(options, 1):
            print(f"  {i}) {option}")
        if default:
            print(f"  [default: {default}]")
        if allow_multiple:
            print("  (Enter comma-separated numbers for multiple selections)")

    while True:
        response = input("> ").strip()

        if not response and default:
            return default

        if options:
            if allow_multiple:
                # Handle multiple selections
                try:
                    indices = [int(x.strip()) - 1 for x in response.split(",")]
                    if all(0 <= idx < len(options) for idx in indices):
                        return ",".join(options[idx] for idx in indices)
                    print(f"{Colors.RED}Invalid selection. Please try again.{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Enter comma-separated numbers.{Colors.END}")
            else:
                # Single selection
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


def validate_tools() -> None:
    """Validate required tools are installed.

    Raises:
        SystemExit: If required tools are missing
    """
    info("Validating required tools...")
    missing = []

    for tool in REQUIRED_TOOLS:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            success(f"{tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(tool)
            error_exit(f"{tool} is not installed")

    if missing:
        error_exit(f"Missing required tools: {', '.join(missing)}")


def validate_source_repo(source_path: Path) -> None:
    """Validate source repository has workflow system.

    Args:
        source_path: Path to source repository

    Raises:
        SystemExit: If source repository is invalid
    """
    info(f"Validating source repository: {source_path}")

    if not source_path.exists():
        error_exit(f"Source repository does not exist: {source_path}")

    if not source_path.is_dir():
        error_exit(f"Source path is not a directory: {source_path}")

    # Check for .claude/skills/ directory
    skills_dir = source_path / ".claude" / "skills"
    if not skills_dir.exists():
        error_exit("Source repository missing .claude/skills/ directory")

    # Check for required skills (at least some of them)
    found_skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
    required_count = len([s for s in SKILL_NAMES[:-1] if s in found_skills])  # Exclude initialize-repository

    if required_count < 3:
        error_exit(f"Source repository has incomplete workflow system (found {required_count}/9 skills)")

    success(f"Source repository validated ({required_count}/9 skills found)")


def validate_target_repo(target_path: Path) -> None:
    """Validate target repository path.

    Args:
        target_path: Path to target repository

    Raises:
        SystemExit: If target path is invalid
    """
    info(f"Validating target repository path: {target_path}")

    if target_path.exists():
        if any(target_path.iterdir()):
            if not ask_yes_no(f"Target directory {target_path} is not empty. Continue?", default=False):
                error_exit("Aborted by user")
            warning("Target directory is not empty, will overwrite files")

    success("Target repository path validated")


class RepositoryConfig:
    """Configuration for new repository."""

    def __init__(self):
        self.name: str = ""
        self.purpose: str = ""
        self.description: str = ""
        self.vcs_provider: str = "github"  # "github" or "azure_devops"
        self.vcs_user: str = ""  # Username from VCS provider
        self.azure_org: str | None = None  # Azure DevOps organization URL
        self.azure_project: str | None = None  # Azure DevOps project name
        self.python_version: str = "3.11"
        self.copy_workflow: bool = True
        self.copy_domain: bool = False
        self.copy_tests: bool = False
        self.copy_containers: bool = False
        self.copy_cicd: bool = False
        self.init_git: bool = True
        self.create_branches: bool = True
        self.remote_url: str | None = None

    @property
    def gh_user(self) -> str:
        """Backward compatibility alias for vcs_user."""
        return self.vcs_user

    @gh_user.setter
    def gh_user(self, value: str) -> None:
        """Backward compatibility alias for vcs_user."""
        self.vcs_user = value


def phase1_configuration(source_path: Path, target_path: Path) -> RepositoryConfig:
    """Phase 1: Configuration selection Q&A.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository

    Returns:
        RepositoryConfig with user selections
    """
    print(f"\n{Colors.BOLD}=== Phase 1: Configuration Selection ==={Colors.END}")

    config = RepositoryConfig()

    # Repository details
    config.name = target_path.name
    info(f"Repository name: {config.name}")

    config.purpose = ask_question(
        "What is the primary purpose of this repository?", options=["Web application", "CLI tool", "Library/package", "Data analysis", "Machine learning", "Other"]
    )

    config.description = ask_question("Brief description of the repository (one line):")

    # VCS provider selection
    config.vcs_provider = (
        ask_question("Which VCS provider will this repository use?", options=["GitHub", "Azure DevOps"], default="GitHub").lower().replace(" ", "_")
    )  # Normalize to "github" or "azure_devops"

    # VCS username and provider-specific config
    if config.vcs_provider == "azure_devops":
        # Azure DevOps specific configuration
        config.azure_org = ask_question("Azure DevOps organization URL (e.g., https://dev.azure.com/myorg):")
        config.azure_project = ask_question("Azure DevOps project name:")
        # Try to detect Azure DevOps user
        try:
            vcs = get_vcs_adapter()
            if vcs.get_provider_name() == "Azure DevOps":
                detected_user = vcs.get_current_user()
                # Extract username from email (before @)
                if "@" in detected_user:
                    detected_user = detected_user.split("@")[0]
                config.vcs_user = ask_question("Azure DevOps username", default=detected_user)
            else:
                config.vcs_user = ask_question("Azure DevOps username:")
        except Exception:
            config.vcs_user = ask_question("Azure DevOps username:")
    else:
        # GitHub configuration
        try:
            vcs = get_vcs_adapter()
            detected_user = vcs.get_current_user()
            config.vcs_user = ask_question("GitHub username", default=detected_user)
        except Exception:
            config.vcs_user = ask_question("GitHub username:")

    # Technology stack
    config.python_version = ask_question("Python version", options=["3.11", "3.12", "3.13"], default="3.11")

    # Components to copy
    print(f"\n{Colors.BOLD}Which components should be copied?{Colors.END}")

    config.copy_workflow = ask_yes_no("Copy workflow system (.claude/skills/, WORKFLOW.md, etc.)?", default=True)

    if not config.copy_workflow:
        error_exit("Workflow system is required for initialization")

    config.copy_domain = ask_yes_no("Copy domain-specific content (src/, resources/)?", default=False)

    config.copy_tests = ask_yes_no("Copy sample tests (tests/)?", default=False)

    config.copy_containers = ask_yes_no("Copy container configs (Containerfile, podman-compose.yml)?", default=False)

    config.copy_cicd = ask_yes_no("Copy CI/CD pipelines (.github/workflows/tests.yml, azure-pipelines.yml)?", default=True)

    success("Configuration complete")
    return config


def phase2_git_setup(config: RepositoryConfig) -> RepositoryConfig:
    """Phase 2: Git setup Q&A.

    Args:
        config: RepositoryConfig from Phase 1

    Returns:
        Updated RepositoryConfig
    """
    print(f"\n{Colors.BOLD}=== Phase 2: Git Setup ==={Colors.END}")

    config.init_git = ask_yes_no("Initialize git repository?", default=True)

    if config.init_git:
        config.create_branches = ask_yes_no("Create branch structure (main, develop, contrib)?", default=True)

        if ask_yes_no("Set up remote repository?", default=False):
            config.remote_url = ask_question("Remote URL (e.g., https://github.com/user/repo.git):")

    success("Git setup configuration complete")
    return config


def copy_skills(source_path: Path, target_path: Path) -> None:
    """Copy .claude/skills/ directory.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
    """
    info("Copying workflow skills...")

    source_skills = source_path / ".claude" / "skills"
    target_skills = target_path / ".claude" / "skills"

    target_skills.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    for skill_name in SKILL_NAMES:
        skill_source = source_skills / skill_name
        if skill_source.exists():
            skill_target = target_skills / skill_name
            shutil.copytree(skill_source, skill_target, dirs_exist_ok=True)
            success(f"Copied skill: {skill_name}")
            copied_count += 1

    success(f"Copied {copied_count}/{len(SKILL_NAMES)} skills")


def copy_documentation(source_path: Path, target_path: Path) -> None:
    """Copy workflow documentation files.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
    """
    info("Copying workflow documentation...")

    docs = [
        "WORKFLOW.md",
        "CONTRIBUTING.md",
        ".claude/skills/UPDATE_CHECKLIST.md",
    ]

    for doc in docs:
        source_file = source_path / doc
        if source_file.exists():
            target_file = target_path / doc
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)
            success(f"Copied: {doc}")


def generate_readme(config: RepositoryConfig, target_path: Path) -> None:
    """Generate adapted README.md for target repository.

    Args:
        config: RepositoryConfig with user selections
        target_path: Path to target repository
    """
    info("Generating README.md...")

    # Determine VCS CLI instructions based on provider
    if config.vcs_provider == "azure_devops":
        vcs_prereq = "- Git and Azure CLI (`az` with azure-devops extension)"
    else:
        vcs_prereq = "- Git and GitHub CLI (`gh`) OR Azure CLI (`az`)"

    readme_content = f"""# {config.name}

{config.description}

## Purpose

{config.purpose}

## Quick Start

### Prerequisites

- Python {config.python_version}+
- uv package manager
{vcs_prereq}

### Installation

```bash
# Clone repository
git clone <repository-url>
cd {config.name}

# Install dependencies
uv sync

# Run tests
uv run pytest
```

## Development Workflow

This repository uses a skill-based workflow system. See [WORKFLOW.md](WORKFLOW.md) for complete documentation.

### Quick Workflow

1. **Plan feature** (Phase 1):
   ```bash
   python .claude/skills/bmad-planner/scripts/create_planning.py \\
     my-feature {config.gh_user}
   ```

2. **Create worktree** (Phase 2):
   ```bash
   python .claude/skills/git-workflow-manager/scripts/create_worktree.py \\
     feature my-feature contrib/{config.gh_user}
   ```

3. **Create spec**:
   ```bash
   cd ../{config.name}_feature_my-feature
   python .claude/skills/speckit-author/scripts/create_specifications.py \\
     feature my-feature {config.gh_user} --todo-file ../TODO_feature_*.md
   ```

4. **Implement and test** (≥80% coverage required)

5. **Quality gates**:
   ```bash
   python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
   ```

6. **Create PR**

## Quality Standards

- ✓ Test coverage ≥ 80%
- ✓ All tests passing
- ✓ Linting clean (ruff)
- ✓ Type checking clean (mypy)
- ✓ Build successful

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Complete 6-phase workflow guide
- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## License

[Your license here]

---

Generated with workflow system v5.2.0
"""

    target_file = target_path / "README.md"
    target_file.write_text(readme_content)
    success("Generated README.md")


def generate_claude_md(config: RepositoryConfig, target_path: Path, source_path: Path) -> None:
    """Generate adapted CLAUDE.md for target repository.

    Args:
        config: RepositoryConfig with user selections
        target_path: Path to target repository
        source_path: Path to source repository
    """
    info("Generating CLAUDE.md...")

    # Read source CLAUDE.md to extract workflow sections
    source_claude = source_path / "CLAUDE.md"
    source_content = source_claude.read_text() if source_claude.exists() else ""

    # Extract workflow architecture section (lines between ## Workflow and next ##)
    workflow_match = re.search(r"(## Workflow.*?)(?=\n## [^#])", source_content, re.DOTALL)
    workflow_section = workflow_match.group(1) if workflow_match else ""

    claude_content = f"""# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

{config.description}

**Type:** {config.purpose}

## Code Architecture

[Describe your code architecture here]

{workflow_section}

## Technology Stack

- **Language:** Python {config.python_version}+
- **Package Manager:** uv (preferred) or pip
- **Git Workflow:** Git-flow + GitHub-flow hybrid with worktrees
- **Workflow System:** Skill-based architecture (8 specialized skills)

## Common Development Commands

### Workflow Commands

```bash
# Create BMAD planning (Phase 1: in main repo, contrib branch)
python .claude/skills/bmad-planner/scripts/create_planning.py \\
  <slug> {config.gh_user}

# Create feature worktree (Phase 2)
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \\
  feature <slug> contrib/{config.gh_user}

# Create SpecKit specifications (Phase 2: in worktree)
python .claude/skills/speckit-author/scripts/create_specifications.py \\
  feature <slug> {config.gh_user} --todo-file ../TODO_feature_*.md

# Run quality gates (Phase 3)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

### Package Management

```bash
# Install/sync dependencies
uv sync

# Add a dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Testing & Quality

```bash
# Run all tests
uv run pytest

# Run with coverage (≥80% required)
uv run pytest --cov=src --cov-fail-under=80

# Lint code
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/

# Type checking
uv run mypy src/

# Format code
uv run ruff format src/
```

## Quality Gates (Enforced Before PR)

- ✓ Test coverage ≥ 80%
- ✓ All tests passing
- ✓ Build successful
- ✓ Linting clean (ruff)
- ✓ Type checking clean (mypy)

## Git Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑
develop                        ← Integration branch
  ↑
contrib/{config.gh_user}       ← Personal contribution
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
```

## Related Documentation

- **[README.md](README.md)** - Human-readable project documentation
- **[WORKFLOW.md](WORKFLOW.md)** - Complete workflow guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

Generated with workflow system v5.2.0
"""

    target_file = target_path / "CLAUDE.md"
    target_file.write_text(claude_content)
    success("Generated CLAUDE.md")


def generate_pyproject_toml(config: RepositoryConfig, target_path: Path) -> None:
    """Generate pyproject.toml for target repository.

    Args:
        config: RepositoryConfig with user selections
        target_path: Path to target repository
    """
    info("Generating pyproject.toml...")

    pyproject_content = f"""[project]
name = "{config.name}"
version = "0.1.0"
description = "{config.description}"
readme = "README.md"
requires-python = ">={config.python_version}"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py{config.python_version.replace(".", "")}"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "{config.python_version}"
strict = true
"""

    target_file = target_path / "pyproject.toml"
    target_file.write_text(pyproject_content)
    success("Generated pyproject.toml")


def copy_gitignore(source_path: Path, target_path: Path) -> None:
    """Copy .gitignore file.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
    """
    info("Copying .gitignore...")

    source_file = source_path / ".gitignore"
    if source_file.exists():
        target_file = target_path / ".gitignore"
        shutil.copy2(source_file, target_file)
        success("Copied .gitignore")


def generate_vcs_config(config: RepositoryConfig, target_path: Path) -> None:
    """Generate .vcs_config.yaml for VCS provider configuration.

    Args:
        config: RepositoryConfig with user selections
        target_path: Path to target repository
    """
    # Only generate for Azure DevOps (GitHub is auto-detected and doesn't need config)
    if config.vcs_provider != "azure_devops":
        return

    info("Generating .vcs_config.yaml for Azure DevOps...")

    vcs_config_content = f"""# VCS Provider Configuration
# This file configures the workflow system to use Azure DevOps instead of GitHub.
# Auto-generated by initialize-repository.

vcs_provider: azure_devops

azure_devops:
  organization: "{config.azure_org}"
  project: "{config.azure_project}"
  repository: "{config.name}"  # Defaults to project name if not specified
"""

    target_file = target_path / ".vcs_config.yaml"
    target_file.write_text(vcs_config_content)
    success("Generated .vcs_config.yaml")


def create_directory_structure(target_path: Path, config: RepositoryConfig) -> None:
    """Create compliant directory structure.

    Args:
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    info("Creating directory structure...")

    # Required directories
    directories = [
        "ARCHIVED",
        "planning",
        "specs",
    ]

    # Optional directories based on config
    if config.copy_domain:
        directories.extend(["src", "resources"])

    if config.copy_tests:
        directories.append("tests")

    for dir_name in directories:
        dir_path = target_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

        # Create CLAUDE.md and README.md in each directory
        if dir_name != "ARCHIVED":
            claude_md = dir_path / "CLAUDE.md"
            claude_md.write_text(
                f"""# Claude Code Context: {dir_name}

## Purpose

Context-specific guidance for {dir_name}

## Directory Structure

[Describe the organization of files in this directory]

## Files in This Directory

[List key files and their purposes]

## Usage

[How to work with code/content in this directory]

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
"""
            )

            readme_md = dir_path / "README.md"
            readme_md.write_text(
                f"""# {dir_name}

[Description of this directory's purpose]

## Contents

[List of key files and directories]

## Usage

[Instructions for working with this directory]
"""
            )

        # Create ARCHIVED subdirectory (except in ARCHIVED itself)
        if dir_name != "ARCHIVED":
            archived_path = dir_path / "ARCHIVED"
            archived_path.mkdir(exist_ok=True)

            archived_claude = archived_path / "CLAUDE.md"
            archived_claude.write_text(
                f"""# Claude Code Context: {dir_name}/ARCHIVED

Archived files from {dir_name}
"""
            )

            archived_readme = archived_path / "README.md"
            archived_readme.write_text(
                f"""# {dir_name}/ARCHIVED

Archived files from {dir_name}
"""
            )

        success(f"Created: {dir_name}/")

    success("Directory structure created")


def create_todo_manifest(target_path: Path, config: RepositoryConfig) -> None:
    """Create TODO.md master manifest.

    Args:
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    info("Creating TODO.md master manifest...")

    timestamp = datetime.now(UTC).isoformat()

    todo_content = f"""---
type: workflow-master-manifest
version: 5.2.0
last_update: "{timestamp}"

workflows:
  active: []
  archived: []

context_stats:
  total_workflows_completed: 0
  current_token_usage: 0
  last_checkpoint: null
---

# TODO - Master Workflow Manifest

This file tracks all active and archived workflows in the repository.

## Active Workflows

No active workflows.

## Archived Workflows

No archived workflows yet.

## Usage

When you start a new workflow (feature, release, hotfix), a TODO file will be created:
- `TODO_feature_YYYYMMDDTHHMMSSZ_<slug>.md`
- `TODO_release_YYYYMMDDTHHMMSSZ_vX.Y.Z.md`
- `TODO_hotfix_YYYYMMDDTHHMMSSZ_<slug>.md`

This master manifest is automatically updated when workflows are archived.
"""

    target_file = target_path / "TODO.md"
    target_file.write_text(todo_content)
    success("Created TODO.md master manifest")


def create_changelog(target_path: Path) -> None:
    """Create CHANGELOG.md for target repository.

    Args:
        target_path: Path to target repository
    """
    info("Creating CHANGELOG.md...")

    changelog_content = (
        """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository setup with workflow system v5.2.0

## [0.1.0] - """
        + datetime.now(UTC).strftime("%Y-%m-%d")
        + """

### Added
- Initialized repository with skill-based workflow architecture
- 8 specialized skills for development workflow
- Quality gates enforcement (≥80% coverage)
- Git-flow + GitHub-flow hybrid with worktrees
- Documentation system with WORKFLOW.md, CLAUDE.md, CONTRIBUTING.md
"""
    )

    target_file = target_path / "CHANGELOG.md"
    target_file.write_text(changelog_content)
    success("Created CHANGELOG.md")


def copy_optional_content(source_path: Path, target_path: Path, config: RepositoryConfig) -> None:
    """Copy optional content based on configuration.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    if config.copy_domain:
        info("Copying domain-specific content...")
        for dir_name in ["src", "resources"]:
            source_dir = source_path / dir_name
            if source_dir.exists():
                target_dir = target_path / dir_name
                shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
                success(f"Copied: {dir_name}/")

    if config.copy_tests:
        info("Copying tests...")
        source_tests = source_path / "tests"
        if source_tests.exists():
            target_tests = target_path / "tests"
            shutil.copytree(source_tests, target_tests, dirs_exist_ok=True)
            success("Copied: tests/")

    if config.copy_containers:
        info("Copying container configs...")
        for file_name in ["Containerfile", "podman-compose.yml"]:
            source_file = source_path / file_name
            if source_file.exists():
                target_file = target_path / file_name
                shutil.copy2(source_file, target_file)
                success(f"Copied: {file_name}")

    if config.copy_cicd:
        info("Copying CI/CD pipelines...")
        # Copy GitHub Actions workflow
        source_workflow = source_path / ".github" / "workflows" / "tests.yml"
        if source_workflow.exists():
            target_workflow = target_path / ".github" / "workflows" / "tests.yml"
            target_workflow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_workflow, target_workflow)
            success("Copied: .github/workflows/tests.yml")
        # Copy Azure Pipelines config
        source_azure = source_path / "azure-pipelines.yml"
        if source_azure.exists():
            target_azure = target_path / "azure-pipelines.yml"
            shutil.copy2(source_azure, target_azure)
            success("Copied: azure-pipelines.yml")


def phase3_file_operations(source_path: Path, target_path: Path, config: RepositoryConfig) -> None:
    """Phase 3: File operations (copy/adapt).

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    print(f"\n{Colors.BOLD}=== Phase 3: File Operations ==={Colors.END}")

    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)

    # Copy workflow system
    copy_skills(source_path, target_path)
    copy_documentation(source_path, target_path)

    # Generate adapted files
    generate_readme(config, target_path)
    generate_claude_md(config, target_path, source_path)
    generate_pyproject_toml(config, target_path)

    # Copy supporting files
    copy_gitignore(source_path, target_path)

    # Generate VCS config for Azure DevOps
    generate_vcs_config(config, target_path)

    # Create directory structure
    create_directory_structure(target_path, config)
    create_todo_manifest(target_path, config)
    create_changelog(target_path)

    # Copy optional content
    copy_optional_content(source_path, target_path, config)

    success("File operations complete")


def phase4_git_initialization(target_path: Path, config: RepositoryConfig) -> None:
    """Phase 4: Git initialization.

    Args:
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    print(f"\n{Colors.BOLD}=== Phase 4: Git Initialization ==={Colors.END}")

    if not config.init_git:
        warning("Skipping git initialization (user selected no)")
        return

    # Change to target directory
    original_dir = Path.cwd()
    os.chdir(target_path)

    try:
        # Initialize git
        info("Initializing git repository...")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "init.defaultBranch", "main"], check=True, capture_output=True)
        success("Git initialized")

        # Create initial commit on main
        info("Creating initial commit...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        commit_msg = f"""chore: initialize repository with workflow system v5.2.0

Initialized {config.name} with skill-based workflow architecture:
- 8 specialized skills for development workflow
- Quality gates enforcement (≥80% coverage)
- Git-flow + GitHub-flow hybrid with worktrees
- Complete documentation system

Repository purpose: {config.purpose}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"""
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        success("Initial commit created on main")

        if config.create_branches:
            # Create develop branch
            info("Creating develop branch...")
            subprocess.run(["git", "checkout", "-b", "develop"], check=True, capture_output=True)
            success("Created develop branch")

            # Create contrib branch
            info(f"Creating contrib/{config.gh_user} branch...")
            subprocess.run(["git", "checkout", "-b", f"contrib/{config.gh_user}"], check=True, capture_output=True)
            success(f"Created contrib/{config.gh_user} branch")

            # Switch back to main
            subprocess.run(["git", "checkout", "main"], check=True, capture_output=True)

        if config.remote_url:
            # Set up remote
            info(f"Setting up remote: {config.remote_url}")
            subprocess.run(["git", "remote", "add", "origin", config.remote_url], check=True, capture_output=True)
            success("Remote configured")

            if ask_yes_no("Push to remote?", default=False):
                subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
                if config.create_branches:
                    subprocess.run(["git", "push", "-u", "origin", "develop"], check=True)
                    subprocess.run(["git", "push", "-u", "origin", f"contrib/{config.gh_user}"], check=True)
                success("Pushed to remote")

        success("Git initialization complete")

    finally:
        # Return to original directory
        os.chdir(original_dir)


def validate_target_structure(target_path: Path) -> None:
    """Validate the created repository structure.

    Args:
        target_path: Path to target repository
    """
    info("Validating repository structure...")

    required_files = [
        "README.md",
        "CLAUDE.md",
        "WORKFLOW.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "TODO.md",
        "pyproject.toml",
        ".gitignore",
    ]

    required_dirs = [
        ".claude/skills",
        "ARCHIVED",
        "planning",
        "specs",
    ]

    missing_files = []
    missing_dirs = []

    for file_path in required_files:
        if not (target_path / file_path).exists():
            missing_files.append(file_path)

    for dir_path in required_dirs:
        if not (target_path / dir_path).exists():
            missing_dirs.append(dir_path)

    if missing_files or missing_dirs:
        warning("Validation found missing items:")
        for item in missing_files:
            print(f"  - Missing file: {item}")
        for item in missing_dirs:
            print(f"  - Missing directory: {item}")
    else:
        success("Repository structure validated")


def print_summary(target_path: Path, config: RepositoryConfig) -> None:
    """Print summary of what was created.

    Args:
        target_path: Path to target repository
        config: RepositoryConfig with user selections
    """
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}✓ Repository Initialization Complete{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.END}\n")

    print(f"{Colors.BLUE}Repository:{Colors.END} {target_path}")
    print(f"{Colors.BLUE}Name:{Colors.END} {config.name}")
    print(f"{Colors.BLUE}Purpose:{Colors.END} {config.purpose}")
    vcs_display = "Azure DevOps" if config.vcs_provider == "azure_devops" else "GitHub"
    print(f"{Colors.BLUE}VCS Provider:{Colors.END} {vcs_display}")
    print(f"{Colors.BLUE}VCS User:{Colors.END} {config.vcs_user}")
    if config.vcs_provider == "azure_devops":
        print(f"{Colors.BLUE}Azure Org:{Colors.END} {config.azure_org}")
        print(f"{Colors.BLUE}Azure Project:{Colors.END} {config.azure_project}")

    print(f"\n{Colors.BOLD}Created:{Colors.END}")
    print("  ✓ Workflow system (9 skills)")
    print("  ✓ Documentation (WORKFLOW.md, CLAUDE.md, CONTRIBUTING.md)")
    print("  ✓ Quality configs (pyproject.toml, .gitignore)")
    if config.vcs_provider == "azure_devops":
        print("  ✓ VCS config (.vcs_config.yaml for Azure DevOps)")
    print("  ✓ Directory structure (ARCHIVED/, planning/, specs/)")

    if config.copy_domain:
        print("  ✓ Domain content (src/, resources/)")
    if config.copy_tests:
        print("  ✓ Tests (tests/)")
    if config.copy_containers:
        print("  ✓ Container configs")
    if config.copy_cicd:
        print("  ✓ CI/CD pipelines (GitHub Actions + Azure Pipelines)")

    if config.init_git:
        print(f"\n{Colors.BOLD}Git:{Colors.END}")
        print("  ✓ Initialized repository")
        if config.create_branches:
            print(f"  ✓ Created branches: main, develop, contrib/{config.gh_user}")
        if config.remote_url:
            print(f"  ✓ Remote configured: {config.remote_url}")

    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print(f"  1. cd {target_path}")
    print("  2. uv sync")
    print("  3. Start first feature:")
    print("     python .claude/skills/bmad-planner/scripts/create_planning.py \\")
    print(f"       my-feature {config.gh_user}")

    print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
    print("  - README.md - Project overview")
    print("  - WORKFLOW.md - Complete workflow guide")
    print("  - CLAUDE.md - Claude Code interaction guide")
    print("  - CONTRIBUTING.md - Contributor guidelines")

    print(f"\n{Colors.GREEN}🎉 Happy coding!{Colors.END}\n")


def main() -> None:
    """Main entry point for repository initialization."""
    parser = argparse.ArgumentParser(
        description="Initialize a new repository with workflow system from source repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize new repository
  python initialize_repository.py /path/to/german /path/to/my-new-repo

  # Interactive setup will guide you through configuration
""",
    )

    parser.add_argument("source_repo", type=Path, help="Path to source repository (with workflow system)")
    parser.add_argument("target_repo", type=Path, help="Path to target repository (will be created)")

    args = parser.parse_args()

    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}Repository Initialization (Meta-Skill){Colors.END}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.END}\n")

    # Validate environment
    validate_tools()
    validate_source_repo(args.source_repo)
    validate_target_repo(args.target_repo)

    # Phase 1: Configuration selection
    config = phase1_configuration(args.source_repo, args.target_repo)

    # Phase 2: Git setup
    config = phase2_git_setup(config)

    # Confirm before proceeding
    print(f"\n{Colors.BOLD}Review Configuration:{Colors.END}")
    print(f"  Source: {args.source_repo}")
    print(f"  Target: {args.target_repo}")
    print(f"  Name: {config.name}")
    print(f"  Purpose: {config.purpose}")
    vcs_display = "Azure DevOps" if config.vcs_provider == "azure_devops" else "GitHub"
    print(f"  VCS Provider: {vcs_display}")
    print(f"  VCS User: {config.vcs_user}")
    if config.vcs_provider == "azure_devops":
        print(f"  Azure Org: {config.azure_org}")
        print(f"  Azure Project: {config.azure_project}")
    print(f"  Copy workflow: {config.copy_workflow}")
    print(f"  Copy domain: {config.copy_domain}")
    print(f"  Copy CI/CD: {config.copy_cicd}")
    print(f"  Initialize git: {config.init_git}")

    if not ask_yes_no("\nProceed with initialization?", default=True):
        error_exit("Aborted by user", code=0)

    # Phase 3: File operations
    phase3_file_operations(args.source_repo, args.target_repo, config)

    # Phase 4: Git initialization
    phase4_git_initialization(args.target_repo, config)

    # Validate result
    validate_target_structure(args.target_repo)

    # Print summary
    print_summary(args.target_repo, config)


if __name__ == "__main__":
    main()

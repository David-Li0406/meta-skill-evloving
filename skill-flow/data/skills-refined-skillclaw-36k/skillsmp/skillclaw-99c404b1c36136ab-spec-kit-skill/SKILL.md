---
name: spec-kit-skill
description: Use this skill when you need to implement a structured, constitution-based workflow for feature development using the GitHub Spec-Kit CLI.
---

# Spec-Kit: Constitution-Based Spec-Driven Development

Official GitHub Spec-Kit integration providing a 7-phase constitution-driven workflow for feature development.

## Quick Start

This skill works with the [GitHub Spec-Kit CLI](https://github.com/github/spec-kit) to guide you through structured feature development:

1. **Constitution** → Establish governing principles
2. **Specify** → Define functional requirements
3. **Clarify** → Resolve ambiguities
4. **Plan** → Create technical strategy
5. **Tasks** → Generate actionable breakdown
6. **Analyze** → Validate consistency
7. **Implement** → Execute implementation

**Storage**: Creates files in `.specify/specs/NNN-feature-name/` directory with numbered features.

## When to Use

- Setting up spec-kit in a project
- Creating constitution-based feature specifications
- Working with the `.specify/` directory
- Following the GitHub spec-kit workflow
- Engaging in constitution-driven development

## Prerequisites & Setup

### Check CLI Installation

First, verify if the Spec-Kit CLI is installed:

```bash
command -v specify || echo "Not installed"
```

### Installation

If not installed, you can install it as follows:

```bash
# Persistent installation (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# One-time usage
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

**Requirements**:
- Python 3.11+
- Git
- uv package manager ([install uv](https://docs.astral.sh/uv/))

### Project Initialization

If the CLI is installed but the project is not initialized, run:

```bash
# Initialize in current directory
specify init . --ai codex

# Initialize new project
specify init <project-name> --ai codex

# Options:
# --force: Overwrite non-empty directories
# --script ps: Generate PowerShell scripts (Windows)
# --no-git: Skip Git initialization
```

---

<details>
<summary>🔍 Phase Detection Logic</summary>

## Detecting Project State

Before proceeding, always detect the current state:

### 1. CLI Installed?

```bash
if command -v specify &> /dev/null || [ -x "$HOME/.local/bin/specify" ]; then
  echo "CLI installed"
else
  echo "CLI not installed - guide user to install"
fi
```
</details>
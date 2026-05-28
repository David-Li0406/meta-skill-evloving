---
name: qkpr
description: Quick Pull Request CLI with AI-powered commit message generation. Use for creating GitHub/GitLab/Gitee pull requests, generating Angular-style commit messages, and creating semantic branch names.
allowed-tools: Bash(qkpr:*), Bash(git:*)
---

# qkpr - Quick Pull Request CLI

## Quick Start

```bash
# Interactive menu (shows all options)
qkpr

# Create a pull request
qkpr pr

# Generate AI commit message
qkpr commit

# Generate branch name
qkpr branch
```

## Commands

### Interactive Menu (Default)
```bash
qkpr
```
Shows an interactive menu with all available features:
- 🔧 Create Pull Request
- 🤖 Generate Commit Message
- 🌿 Generate Branch Name
- ⚙ Configure API Key
- 🔧 Configure Model

### Create Pull Request
```bash
# Interactive branch selection
qkpr pr

# Specify target branch directly
qkpr pr main
qkpr pr develop
```

**Features:**
- Interactive branch selection with search
- Protected branch highlighting (main, master)
- Smart branch categorization by prefix (feat/, fix/, merge/, etc.)
- Auto-generated PR description with commit summaries
- Clipboard integration (copies PR description automatically)
- Browser integration (opens PR comparison page)
- Merge branch suggestion for conflict resolution
- Multi-platform support (GitHub, GitLab, Gitee)

### Generate Commit Message (AI-Powered)
```bash
qkpr commit
```

**Features:**
- 🤖 Uses Google Gemini 2.0 Flash AI
- 📝 Follows Angular commit message convention
- 🌿 Suggests semantic branch names
- 🔍 Analyzes staged changes (git diff --cached)
- ✅ Interactive: choose to commit, copy, or regenerate
- 🚀 Option to auto-push after commit

#### First-time Setup for AI Features

1. Get Gemini API Key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Configure API key:

```bash
# Method 1: Use config command
qkpr config

# Method 2: Environment variable
export QUICK_PR_GEMINI_API_KEY=your_api_key_here
# or legacy variable name
export GEMINI_API_KEY=your_api_key_here
```

#### Model Configuration

```bash
qkpr config:model
```

Available models (as of 2025):
- `gemini-2.5-pro` (latest pro)
- `gemini-2.5-flash` (latest flash)
- `gemini-2.0-flash` (default)
- `gemini-2.0-flash-exp`
- `gemini-flash-latest`

Or set via environment:
```bash
export QUICK_PR_GEMINI_MODEL=gemini-2.5-pro
```

### Generate Branch Name
```bash
qkpr branch
```

Generates a semantic branch name based on staged changes using AI.

### Configuration
```bash
# Configure API key
qkpr config

# Configure model
qkpr config:model
```

### Version & Help
```bash
qkpr --version    # or qkpr -v
qkpr --help       # or qkpr -h
```

## Workflow Examples

### Example 1: Create a Pull Request
```bash
# Make your changes
git add .
git commit -m "feat: add new feature"

# Create PR with qkpr
qkpr pr
# Select target branch interactively
# PR description copied to clipboard, browser opens automatically
```

### Example 2: AI-Generated Commit Message
```bash
# Stage your changes
git add .

# Generate commit message with AI
qkpr commit
# Review the generated message
# Choose to commit, copy, or regenerate
```

### Example 3: Complete Workflow with AI
```bash
# Stage changes
git add .

# Generate commit and create branch name
qkpr commit    # Generates message, suggests branch name
qkpr branch    # Get semantic branch name suggestion

# Commit and push
git checkout -b suggested-branch-name
git commit -m "generated message"
git push

# Create PR
qkpr pr main
```

## Commit Message Convention

qkpr follows Angular commit message format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Adding or updating tests
- `chore` - Maintenance tasks
- `ci` - CI/CD changes
- `build` - Build system changes

## Configuration File

API keys and settings are stored locally in:
```
~/.qkpr/config.json
```

## Requirements

- `git` version 2.0+
- Node.js version 18+
- Gemini API key (for AI features)

## License

MIT License © KazooTTT

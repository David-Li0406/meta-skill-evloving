---
name: environment-setup-guide
description: Use this skill when you need to set up a development environment from scratch, ensuring all necessary tools, dependencies, and configurations are correctly installed and verified.
---

# Environment Setup Guide

## Overview

This skill provides step-by-step guidance for developers to set up complete development environments from scratch, including installing tools, configuring dependencies, setting up environment variables, and verifying the setup.

## When to Use This Skill

- When starting a new project and needing to set up the development environment
- When onboarding new team members to a project
- When switching to a new machine or operating system
- When troubleshooting environment-related issues
- When documenting setup instructions for a project

## How It Works

### Step 1: Identify Requirements

Determine what needs to be installed:
- Programming language and version (Node.js, Python, Go, etc.)
- Package managers (npm, pip, cargo, etc.)
- Database systems (PostgreSQL, MongoDB, Redis, etc.)
- Development tools (Git, Docker, IDE extensions, etc.)
- Environment variables and configuration files

### Step 2: Check Current Setup

Before installing anything, check what's already installed:
```bash
# Check versions of installed tools
node --version
python --version
git --version
docker --version
```

### Step 3: Provide Installation Instructions

Provide platform-specific installation commands:
- **macOS:** Using Homebrew
- **Linux:** Using apt, yum, or other package managers
- **Windows:** Using Chocolatey, Scoop, or direct installers

### Step 4: Configure the Environment

Set up:
- Environment variables (.env files)
- Configuration files (.gitconfig, .npmrc, etc.)
- IDE settings (VS Code, IntelliJ, etc.)
- Shell configuration (.bashrc, .zshrc, etc.)

### Step 5: Verify Installation

Ensure everything works by:
- Running version checks
- Testing basic commands
- Verifying database connections
- Checking that environment variables are loaded

## Examples

### Example 1: Node.js Project Setup

```markdown
## Setting Up Node.js Development Environment

### Prerequisites
- macOS, Linux, or Windows
- Terminal/Command Prompt access
- Internet connection

### Step 1: Install Node.js

**macOS (using Homebrew):**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node
```
```
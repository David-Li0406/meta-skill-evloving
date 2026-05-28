# Claude Code Overview

Source: https://code.claude.com/docs/en/overview

## What is Claude Code?

Claude Code is **Anthropic's agentic coding tool that lives in your terminal** and helps developers turn ideas into code faster than ever before. It's designed to meet developers where they already work—in their existing tools and workflows.

## Key Capabilities

Claude Code enables you to:

1. **Build features from descriptions** - Tell Claude what you want to build in plain English. It makes a plan, writes the code, and ensures it works.

2. **Debug and fix issues** - Describe a bug or paste an error message. Claude Code analyzes your codebase, identifies the problem, and implements fixes.

3. **Navigate any codebase** - Ask anything about your team's codebase and get thoughtful answers. It maintains awareness of your entire project structure and can find up-to-date information from the web.

4. **Automate tedious tasks** - Fix lint issues, resolve merge conflicts, write release notes—all from a single command.

## Why Developers Love It

- **Works in your terminal** - Not another chat window or IDE, but integrated into your existing workflow
- **Takes action** - Can directly edit files, run commands, and create commits
- **Unix philosophy** - Composable and scriptable (e.g., `tail -f app.log | claude -p "Slack me if you see any anomalies"`)
- **Enterprise-ready** - Use the Claude API or host on AWS/GCP with built-in security, privacy, and compliance

## Quick Start

**Installation** (macOS/Linux/WSL):
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```bash
irm https://claude.ai/install.ps1 | iex
```

**Start using it:**
```bash
cd your-project
claude
```

## Requirements

- A Claude subscription (Pro, Max, Teams, or Enterprise) or Claude Console account

Claude Code automatically updates in the background to keep you on the latest version.

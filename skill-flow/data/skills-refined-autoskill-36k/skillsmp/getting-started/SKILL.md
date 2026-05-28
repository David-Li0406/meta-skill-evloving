---
name: getting-started
description: Introduction for new users - explains the environment and helps them get oriented
allowed-tools: Bash, Read
---

# Getting Started

Welcome to your development environment! This skill introduces new users to what they can do here.

## Usage

```bash
/getting-started    # Run this on your first session
```

## Instructions

When the user runs `/getting-started`, walk them through this introduction interactively. Be friendly and encouraging - they may be completely new to development.

### Step 1: Check Their Setup

First, verify their environment is ready:

```bash
~/verify.sh
```

If anything shows `[✗]`, help them fix it before continuing. Guide them through each step conversationally - don't just dump commands on them.

### Step 2: Introduce Yourself

Explain what you are and what you can do. Something like:

"I'm Claude, an AI assistant running directly on your development machine. I can:
- Write and edit code for you
- Run commands and install software
- Fix problems when things break
- Explain technical concepts in plain language
- Help you learn as we work together

I have full access to this system, so I can actually do things - not just tell you what to do."

### Step 3: Show Them Around

Give a brief tour:

**Where things live:**
- `~/dev/` - Your projects go here
- `~/dev/whoabuddy/claude-knowledge/` - Shared patterns and guides the team maintains
- `~/dev/whoabuddy/claude-rpg/` - The web interface you're using right now

**Things they'll hear about:**
- `git` - Version control (saving your work, collaborating)
- `gh` - GitHub command line (cloning repos, making PRs)
- `clarinet` - Tool for Clarity smart contract development
- `tmux` - Terminal multiplexer (multiple windows in one session)

### Step 4: Find Out What They Want to Do

Ask what brought them here. Common responses:

**"I want to learn Clarity/smart contracts"**
- Point to `~/dev/whoabuddy/claude-knowledge/patterns/clarity-patterns.md`
- Offer to create a sample project: `clarinet new my-first-contract`
- Walk them through the basic structure

**"I want to work on [specific project]"**
- Help them clone it: `gh repo clone owner/repo`
- Open it and explain the structure
- Find the README and go from there

**"I don't know, just exploring"**
- Totally fine! Offer options:
  - Show them an example project
  - Create a simple "hello world"
  - Explain what the team is building

**"I have a specific task"**
- Great, let's do it. Ask for details.

### Step 5: Offer Next Steps

Based on their interest, suggest:
- A small hands-on task to get comfortable
- Relevant documentation in claude-knowledge
- Just ask - you're here to help

Close with something like: "Whenever you need help, just ask. I'm here to handle the technical details so you can focus on what you want to build."

## Example Interaction

User: `/getting-started`

Claude: "Welcome! Let me make sure everything's set up, then I'll show you around.

*[runs ~/verify.sh]*

Everything looks good - you're ready to go.

I'm Claude, your AI development assistant. I run directly on this machine and have full access to do whatever you need - write code, run commands, install software, fix problems. Think of me as a technical partner who handles all the infrastructure stuff so you can focus on building.

What brings you here today? Are you:
- Learning about Clarity and smart contracts?
- Working on a specific project?
- Just exploring to see what's possible?

Tell me what you're interested in and we'll go from there."

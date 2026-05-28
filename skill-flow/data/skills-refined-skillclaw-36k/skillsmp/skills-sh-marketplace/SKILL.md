---
name: skills-sh-marketplace
description: This skill should be used when searching, discovering, or installing skills from the skills.sh marketplace (Vercel's open agent skills ecosystem). It applies when the user wants to find skills for AI agents, browse the skills leaderboard, install skills to Claude Code or other agents, or explore what capabilities are available in the skills.sh directory.
allowed-tools: [Bash, WebFetch]
---

# Skills.sh Marketplace

Search, discover, and install skills from [skills.sh](https://skills.sh) - the open agent skills ecosystem by Vercel.

## Quick Start

```bash
# Browse top skills
curl -s "https://skills.sh/api/skills" | jq '.skills[:10]'

# Install a skill to Claude Code
bunx skills add vercel-labs/agent-skills

# List available skills in a repository
bunx skills add vercel-labs/agent-skills --list
```

## Commands

### Browse Skills

Fetch the skills leaderboard from skills.sh:

```bash
# Get all skills (ranked by installs)
curl -s "https://skills.sh/api/skills" | jq '.skills'

# Get top 20 skills with formatting
curl -s "https://skills.sh/api/skills" | jq -r '.skills[:20] | .[] | "\(.name) (\(.installs) installs) - \(.topSource)"'

# Check if more skills are available
curl -s "https://skills.sh/api/skills" | jq '.hasMore'
```

### Search for Skills

Filter skills by name pattern:

```bash
# Find React-related skills
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.name | contains("react")))'

# Find skills from a specific author
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.topSource | startswith("expo/")))'

# Find authentication-related skills
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.name | test("auth|login|session"; "i")))'
```

### List Skills in a Repository

Preview what skills are available before installing:

```bash
# List skills from a repository
bunx skills add <owner/repo> --list

# Examples
bunx skills add vercel-labs/agent-skills --list
bunx skills add expo/skills --list
bunx skills add anthropics/skills --list
```

### Install Skills

Install skills to your AI agent:

```bash
# Interactive install (prompts for skill selection and agent)
bunx skills add <owner/repo>

# Install specific skills
bunx skills add <owner/repo> --skill <skill-name>

# Install to a specific agent
bunx skills add <owner/repo> --agent claude-code

# Install globally (user-level, not project-level)
bunx skills add <owner/repo> --global

# Install all skills to all agents without prompts
bunx skills add <owner/repo> --all

# Skip confirmation prompts
bunx skills add <owner/repo> --yes
```

### Supported Agents

The skills CLI supports installation to:

| Agent | Flag Value |
|-------|------------|
| Claude Code | `claude-code` |
| OpenCode | `opencode` |
| Codex | `codex` |
| Cursor | `cursor` |
| Antigravity | `antigravity` |
| GitHub Copilot | `github-copilot` |
| Roo Code | `roo` |

## Examples

### Discover Skills for a Specific Use Case

```bash
# Find frontend/UI skills
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.name | test("ui|frontend|design|react|next"; "i"))) | .[0:10]'

# Find testing/QA skills
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.name | test("test|qa|quality"; "i")))'

# Find deployment/DevOps skills
curl -s "https://skills.sh/api/skills" | jq '.skills | map(select(.name | test("deploy|cicd|workflow"; "i")))'
```

### Install Popular Skills

```bash
# Install Vercel's React best practices
bunx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code --yes

# Install Expo's mobile development skills
bunx skills add expo/skills --skill react-native-best-practices --agent claude-code --yes

# Install Anthropic's official skills
bunx skills add anthropics/skills --all --agent claude-code --yes
```

### Check What's Trending

```bash
# Top 5 most installed skills
curl -s "https://skills.sh/api/skills" | jq -r '.skills[:5] | .[] | "[\(.installs | tostring | (5 - length) * " " + .)] \(.name) from \(.topSource)"'
```

## Popular Skill Repositories

| Repository | Focus |
|------------|-------|
| `vercel-labs/agent-skills` | React, Next.js, web design |
| `anthropics/skills` | Frontend design, PDF handling |
| `expo/skills` | React Native, mobile development |
| `softaworks/agent-toolkit` | General development utilities |
| `coreyhaines31/marketingskills` | Marketing, SEO, copywriting |
| `better-auth/skills` | Authentication patterns |
| `remotion-dev/skills` | Video generation with Remotion |

## Creating Your Own Skills

Initialize a new skill:

```bash
# Create a skill in the current directory
bunx skills init

# Create a named skill directory
bunx skills init my-custom-skill
```

This creates a `SKILL.md` file with the standard frontmatter structure.

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SKILLS_NO_TELEMETRY=1` | Opt out of anonymous telemetry |

## Notes

- Skills are ranked by anonymous install telemetry
- The CLI clones repositories temporarily during installation
- Skills are installed to agent-specific config directories
- Use `--list` to preview before installing
- Always use `bunx` instead of `npx` per project requirements

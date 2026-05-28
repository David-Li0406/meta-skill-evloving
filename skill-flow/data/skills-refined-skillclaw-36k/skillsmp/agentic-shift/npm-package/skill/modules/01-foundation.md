# Module 1: Foundation - CLAUDE.md and Project Initialization

## Learning Objectives

By the end of this module, learners will:
- Understand why project context dramatically improves Claude's assistance
- Successfully run `/init` to scaffold Claude Code configuration
- Create a comprehensive CLAUDE.md tailored to their project

## Prerequisites Check

Before starting, verify:
1. User is in a project directory (has source code)
2. Directory is a git repository (or guide them to init one)
3. Claude Code CLI is authenticated

```bash
# Check git
git status > /dev/null 2>&1 && echo "Git: OK" || echo "Git: Not initialized"

# Check for existing CLAUDE.md
test -f CLAUDE.md && echo "CLAUDE.md: Already exists" || echo "CLAUDE.md: Needs creation"

# Check for .claude directory
test -d .claude && echo ".claude/: Exists" || echo ".claude/: Needs creation"
```

## Lesson 1.1: Why Context Matters

### Teaching Points

Explain to the learner:

1. **Without context**, Claude makes generic suggestions that may not fit the project
2. **With CLAUDE.md**, Claude understands:
   - Project architecture and key components
   - Team coding conventions and patterns
   - Build commands and development workflow
   - What to do AND what to avoid

### Demonstration

Show them the difference by having Claude answer a question about their codebase:
- First, without any context (generic response)
- Then, after creating CLAUDE.md (tailored response)

## Lesson 1.2: Running /init

### Steps

1. If `.claude/` doesn't exist, guide them to run:
   ```bash
   claude /init
   ```

2. Explain what was created:
   - `.claude/settings.json` - Project-specific Claude configuration
   - May scaffold a basic `CLAUDE.md` template

3. If `/init` was already run, acknowledge and move to CLAUDE.md creation.

## Lesson 1.3: CLAUDE.md Structure

### Minimum Viable CLAUDE.md (Start Here)

A useful CLAUDE.md needs just 4 sections:

```markdown
# Project Name

Brief description of what this project does.

## Commands

```bash
npm install    # Install dependencies
npm run dev    # Start dev server
npm test       # Run tests
```

## Structure

- `src/` - Main source code
- `tests/` - Test files
- `docs/` - Documentation

## Rules

- Follow existing code patterns
- Don't modify files in `generated/`
- Use TypeScript strict mode
```

### Extended CLAUDE.md (Add Later)

Once comfortable, expand with:
- **Architecture**: How components interact
- **Conventions**: Naming, formatting standards
- **Patterns**: Error handling, API response format
- **Do NOT**: Specific things to avoid

> **Tip**: Start minimal. Add sections as you discover what Claude needs to know.

## Interactive Exercise 1.1: Build Your CLAUDE.md

### Quick Discovery (4 Questions)

Ask the user:

1. "What's your project name and what does it do?"

2. "What are your main commands?" (install, dev, test, build)

3. "What are the key folders in your project?"

4. "Any important rules?" (things to always do or never do)

### Generate

Create a minimal CLAUDE.md from their answers. Keep it under 30 lines to start.

> **Tip**: You can always expand it later. A short, accurate CLAUDE.md beats a long, generic one.

## Verification

After creating CLAUDE.md, verify:

```bash
# Check file exists
test -f CLAUDE.md && echo "✓ CLAUDE.md created"

# Check file has content
[ $(wc -l < CLAUDE.md) -gt 20 ] && echo "✓ CLAUDE.md has substantial content"

# Check key sections exist
grep -q "## Overview" CLAUDE.md && echo "✓ Has Overview section"
grep -q "## Architecture" CLAUDE.md && echo "✓ Has Architecture section"
grep -q "## Getting Started" CLAUDE.md && echo "✓ Has Getting Started section"
grep -q "## Do NOT" CLAUDE.md && echo "✓ Has constraints section"
```

## Checkpoint

Module 1 is complete when:
- [ ] `/init` has been run (`.claude/` directory exists)
- [ ] `CLAUDE.md` exists in project root
- [ ] CLAUDE.md contains at least: Overview, Architecture, Getting Started, Conventions, Do NOT sections
- [ ] User can explain why context improves Claude's responses

## Transition

Once verified, congratulate them and transition:

---

**Module 1 Complete!**

You've created the foundation for effective AI-assisted development. Your CLAUDE.md gives Claude the context it needs to provide relevant, project-specific assistance.

Ready to supercharge Claude with real-time data from your tools? Let's move to **Module 2: MCP Mastery**.

Type "next" or run `/onboard-mcp` to continue.

---

# Module 5: Skill Creation

## Learning Objectives

By the end of this module, learners will:
- Create a simple custom skill
- Install and test their skill
- Understand how to share skills with their team

## What Are Skills?

Skills are **reusable workflows** for Claude Code:
- Triggered by `/command`
- Defined in simple files
- Shareable with your team

### Skill Structure

```
my-skill/
├── skill.json       # Metadata
└── instructions.md  # What Claude should do
```

## Exercise: Create Your First Skill

### Step 1: Identify a Workflow

Ask yourself:
- What do I prompt Claude for repeatedly?
- What would help new team members?

**Example**: A simple "explain this file" skill.

### Step 2: Create skill.json

```json
{
  "name": "explain",
  "version": "1.0.0",
  "description": "Explain what a file or function does",
  "commands": [
    {
      "name": "explain",
      "description": "Explain code in plain English"
    }
  ],
  "entry": "instructions.md"
}
```

### Step 3: Create instructions.md

```markdown
# Explain Skill

When the user invokes /explain, help them understand code.

## What to do

1. Ask what file or function they want explained (if not specified)
2. Read the code
3. Explain it in plain English:
   - What it does
   - How it works
   - Why it might be written this way

## Output style

- Use simple language
- Start with a one-sentence summary
- Add details progressively
- Mention any gotchas or edge cases
```

### Step 4: Install

```bash
mkdir -p ~/.claude/skills/explain
cp skill.json ~/.claude/skills/explain/
cp instructions.md ~/.claude/skills/explain/
```

### Step 5: Test

```bash
claude /explain
```

## Common Skill Ideas

| Skill | Purpose |
|-------|---------|
| `/standup` | Generate standup from git history |
| `/review` | Code review checklist |
| `/scaffold` | Create new component/module |
| `/explain` | Explain complex code |

## Sharing Skills

### With Your Team

```bash
# Option 1: Git repo
git clone team-skills-repo ~/.claude/skills

# Option 2: Copy folder
cp -r my-skill ~/.claude/skills/
```

### Project-Specific Skills

Put skills in `.claude/skills/` in your repo. They'll be available to anyone who clones it.

## Checkpoint

Module 5 is complete when:
- [ ] You've created and installed a custom skill
- [ ] The skill works when invoked

---

# Congratulations!

You've completed The Agentic Shift onboarding.

## What You've Learned

1. **Foundation**: Creating CLAUDE.md for project context
2. **MCP** (optional): Connecting external tools
3. **TDA Cycle**: Test-driven agentic development
4. **Governance** (optional): Automated quality gates
5. **Skills**: Capturing patterns as reusable workflows

## Your New Workflow

```
Write tests → Prompt Claude → Run tests → Iterate
```

## Quick Reference

```
CLAUDE.md         → Project context
~/.claude/skills/ → Custom skills
/help             → Available commands
```

## Next Steps

- Create 2-3 more skills for your workflow
- Share this onboarding with teammates
- Iterate and improve your CLAUDE.md over time

---

You are now an **Architect and Reviewer**. Welcome to agent-led development.

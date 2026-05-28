---
name: creating-agent-skills
description: Use this skill when you want to create new Agent Skills, including generating the necessary directory structure and SKILL.md format.
---

# Creating Agent Skills

## When to Use This Skill
Use this skill when:
- The user asks to create a new skill.
- The user wants to start a new skill project.
- You need to generate the boilerplate structure for a skill.

## Step-by-Step Skill Creation Process

1. **Understand the Goal**  
   Clarify what the new skill should do, key triggers (e.g., keywords like "PDF", "commit message"), and scope (keep it focused!).

2. **Determine Skill Location**  
   - Personal: `~/.claude/skills/<skill-name>/`  
   - Project: `.claude/skills/<skill-name>/` (recommended for team sharing)

3. **Choose a Concise Skill Name**  
   Use kebab-case (e.g., `pdf-reader`, `data-analysis`).

4. **Initialize Skill**  
   Call the initialization API/Tool to create the directory structure:
   - Directory: `backend/skills/<skill-name>`
   - File: `SKILL.md` (with template)
   - Subdirectories: `scripts/`, `references/`, `assets/`

5. **Generate SKILL.md Structure**  
   Use this template:

   ```yaml
   ---
   name: <your-skill-name> (lowercase, hyphens only)
   description: What this skill does + when to use it (include triggers!). Keep under 1024 chars.
   ---
   # Skill Title

   ## Instructions
   Detailed step-by-step guidance for Claude.

   ## Examples
   Show 2-3 concrete before/after examples.

   ## Best Practices / Checklist
   - Bullet points for quality standards
   ```

6. **Add Supporting Files (Optional but Recommended)**  
   - `reference.md`: Detailed docs, schemas, APIs  
   - `examples/` folder: Sample inputs/outputs  
   - `scripts/` folder: Helper Python/bash scripts (e.g., data processors)  
   - `templates/` folder: File templates  

   Reference them like: See [reference.md](reference.md) for details.

7. **Make Description Trigger-Happy**  
   Ensure the description includes specific triggers for reliable auto-invocation.

8. **Test the Skill**  
   - Restart Claude Code  
   - Ask: "List available skills"  
   - Trigger with a matching query  
   - If not activating: Refine description triggers

9. **Optional: Generate Files Automatically**  
   Use the helper script below to scaffold a new skill directory.

## Helper Script: scaffold_skill.py

Usage: `python scripts/scaffold_skill.py 'Skill Name' 'Brief description with triggers'`

Run it via Bash tool when needed: `python scripts/scaffold_skill.py "Commit Message Generator" "Generate conventional commit messages from git diffs. Use when creating commits or reviewing changes."`

## Validation

After creating, validate the skill:
```bash
# Check structure
ls -la ~/.claude/skills/<skill-name>/

# Verify SKILL.md exists and has frontmatter
head -20 ~/.claude/skills/<skill-name>/SKILL.md
```

## Best Practices Reminder
- One skill = one focused capability
- Specific triggers in description → reliable auto-invocation
- Use `allowed-tools` for safe/read-only skills
- Version your skills in the markdown
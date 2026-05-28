---
name: skill-builder
description: Guides the creation of new Agent Skills, including generating SKILL.md structure, descriptions, instructions, and optional supporting files/scripts. Use this skill when the user wants to build, design, or scaffold a new custom skill, or when discussing skill creation best practices.
---

# Skill Builder

This skill helps create high-quality, reusable Agent Skills for Claude Code.

## When to Use This Skill
- User explicitly asks to "create a skill", "build a new skill", "scaffold a skill", or similar.
- User describes a workflow, expertise, or task that should be packaged as a reusable skill.
- Need guidance on skill structure, best practices, or troubleshooting why a skill isn't triggering.

## Step-by-Step Skill Creation Process

1. **Understand the Goal**  
   Clarify what the new skill should do, key triggers (e.g., keywords like "PDF", "commit message"), and scope (keep it focused!).

2. **Choose Skill Type and Location**  
   - Personal: `~/.claude/skills/new-skill-name/`  
   - Project: `.claude/skills/new-skill-name/` (recommended for team sharing)

3. **Generate SKILL.md Structure**  
   Use this template:

   ```yaml
   ---
   name: your-skill-name (lowercase, hyphens only)
   description: What this skill does + when to use it (include triggers!). Keep under 1024 chars.
   # Optional: allowed-tools: Read, Grep, Bash (etc., for restricted access)
   ---
   # Skill Title

   ## Instructions
   Detailed step-by-step guidance for Claude.

   ## Examples
   Show 2-3 concrete before/after examples.

   ## Best Practices / Checklist
   - Bullet points for quality standards
   ```

4. **Add Supporting Files (Optional but Recommended)**  
   - `reference.md`: Detailed docs, schemas, APIs  
   - `examples/` folder: Sample inputs/outputs  
   - `scripts/` folder: Helper Python/bash scripts (e.g., data processors)  
   - `templates/` folder: File templates  

   Reference them like: See [reference.md](reference.md) for details.

5. **Make Description Trigger-Happy**  
   Good example: "Analyze React components for performance and accessibility. Use when reviewing UI code, optimizing frontend, or mentioning React/JSX."
   
   Bad: "Helps with code."

6. **Test the Skill**  
   - Restart Claude Code  
   - Ask: "List available skills"  
   - Trigger with a matching query  
   - If not activating: Refine description triggers

7. **Optional: Generate Files Automatically**  
   Use the helper script below to scaffold a new skill directory.

## Helper Script: scaffold_skill.py

Usage: `python scripts/scaffold_skill.py 'Skill Name' 'Brief description with triggers'`

Run it via Bash tool when needed: `python scripts/scaffold_skill.py "Commit Message Generator" "Generate conventional commit messages from git diffs. Use when creating commits or reviewing changes."`

## Best Practices Reminder
- One skill = one focused capability
- Specific triggers in description → reliable auto-invocation
- Use `allowed-tools` for safe/read-only skills
- Version your skills in the markdown

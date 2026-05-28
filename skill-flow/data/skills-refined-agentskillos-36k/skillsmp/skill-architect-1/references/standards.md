---
tags: 30_Resources
---
# Agent Skills Standard Checklist

Use this checklist when refactoring or verifying a skill.

## Directory Structure
- [ ] Root directory name matches the skill name (kebab-case)
- [ ] Contains `SKILL.md` (exact filename)
- [ ] Optional: `scripts/` directory for executable code
- [ ] Optional: `references/` directory for documentation/data
- [ ] Optional: `assets/` directory for static files

## SKILL.md Frontmatter
- [ ] `name`: Matches directory name, 1-64 chars, lowercase a-z, 0-9, hyphens only
- [ ] `description`: 1-1024 chars, describes what and when to use
- [ ] `license`: e.g., MIT, Apache-2.0
- [ ] `metadata`: contains `author` and `version` (recommended)
- [ ] `allowed-tools`: specifies permissions (e.g., `Bash`, `Read`)

## SKILL.md Body
- [ ] Title (H1)
- [ ] Summary
- [ ] Sections (H2): Purpose, Usage, Instructions, Examples
- [ ] References section (optional but recommended)

## Scripts
- [ ] Should be self-contained or document dependencies (do not assume packages are installed)
- [ ] **Solve, don't punt**: Handle errors with try/except and provide helpful messages
- [ ] Use defaults for configuration where possible
- [ ] No "voodoo constants": Document why specific values (timeouts, retries) are chosen

## Content Guidelines
- [ ] **No time-sensitive information**: Avoid content that becomes outdated quickly
- [ ] **Consistent terminology**: Use specific terms consistently throughout commands and instructions
- [ ] **Flat structure**: File references should be one level deep (avoid deeply nested directories)
- [ ] **Concrete Examples**: Use specific inputs/outputs, avoiding abstract placeholders

## Testing & Evaluation
- [ ] **Validation**: Critical operations should have verification steps (e.g., "plan-validate-execute" pattern)
- [ ] **Model Testing**: Test with multiple models (Haiku, Sonnet, Opus) if possible
- [ ] **Real Scenarios**: Validate against real-world usage patterns, not just "hello world" cases

## General
- [ ] Use forward slashes (`/`) for all file paths, even on Windows
- [ ] `SKILL.md` body should be under 500 lines (use progressive disclosure for large content)

# Skill Validation Checklist

Use this checklist to validate new Skills before finalizing them. Check each item to ensure your Skill follows official format and learning-infra patterns.

## YAML Frontmatter

- [ ] YAML frontmatter is present and valid
- [ ] Frontmatter starts with `---` on line 1 (no blank lines before)
- [ ] Frontmatter ends with `---` before markdown content
- [ ] Uses spaces for indentation (not tabs)
- [ ] `name` field is present
- [ ] `description` field is present

## Name Validation

- [ ] Name is lowercase letters, numbers, and hyphens only
- [ ] Name is maximum 64 characters
- [ ] Name does not contain XML tags
- [ ] Name does not contain reserved words ("anthropic", "claude")
- [ ] Name matches directory name
- [ ] Name uses consistent naming pattern (gerund form recommended)

## Description Validation

- [ ] Description is in third-person format
- [ ] Description includes what the Skill does
- [ ] Description includes when to use the Skill (trigger conditions)
- [ ] Description includes trigger keywords users would naturally say
- [ ] Description is maximum 1024 characters
- [ ] Description does not contain XML tags
- [ ] Description is specific (not vague like "helps with files")

**Good description example:**

```yaml
description: Debugs code issues, errors, failing tests, and broken flows using a systematic workflow. Identifies root causes, applies minimal fixes, and validates solutions. Works with errors, test failures, API issues, database problems, and integration failures. Use when debugging errors, fixing failing tests, troubleshooting API endpoints, or resolving database issues.
```

**Bad description examples:**

```yaml
description: Helps with debugging
description: I can help you debug code
description: You can use this to debug
```

## File Structure

- [ ] SKILL.md file exists in correct location
- [ ] Directory structure matches monorepo organization:
  - Control Plane Skills -> `.skills/skills/control-plane/`
  - Shared Skills -> `.skills/skills/shared/`
  - Infrastructure Skills -> `.skills/skills/infrastructure/`
- [ ] Supporting files (if any) are in same directory
- [ ] File paths use forward slashes (not backslashes)

## Content Structure

- [ ] SKILL.md body is under 500 lines
- [ ] Title (H1) matches Skill name
- [ ] Brief overview is present (1-2 paragraphs)
- [ ] Project Documentation References section (if applicable)
- [ ] Context Detection section (if adaptive Skill)
- [ ] Instructions section (main content)
- [ ] Examples section (concrete examples)
- [ ] Supporting file references (if using progressive disclosure)

## Progressive Disclosure

- [ ] Main SKILL.md is concise (under 500 lines)
- [ ] Complex content is split into separate files
- [ ] Supporting files are referenced from SKILL.md
- [ ] File references are one level deep (not nested)
- [ ] Supporting files have descriptive names

## Context Detection (if Adaptive)

- [ ] Context detection logic is included
- [ ] File path patterns are specified
- [ ] Behavior adaptation is documented
- [ ] Different contexts are clearly distinguished
- [ ] Appropriate tooling is specified for each context

## Project Documentation References

- [ ] Relevant project rules are referenced (not duplicated)
- [ ] References use correct paths (relative to Skill location)
- [ ] Control Plane Skills reference: API, domain, provisioning rules
- [ ] Infrastructure Skills reference: Cloud Run, Cloudflare, database, secrets rules
- [ ] Shared Skills reference: project overview, coding standards
- [ ] Package Skills reference: project overview, package-specific rules
- [ ] **Rule content is NOT duplicated** - Skills reference rules, not repeat them
- [ ] Skill instructions add only Skill-specific guidance
- [ ] Rules are referenced in "Project Documentation References" section

## Code Examples

- [ ] Examples are concrete (real code, not pseudocode)
- [ ] Examples show actual usage patterns
- [ ] Examples match project tooling (Vitest, Drizzle, REST API, etc.)
- [ ] Examples include context (control-plane, infrastructure, package)
- [ ] Examples are relevant to Skill's purpose

## Language and Style

- [ ] Instructions are concise (assume Claude knows basics)
- [ ] Terminology is consistent throughout
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] File paths use forward slashes
- [ ] No Windows-style paths
- [ ] Clear, direct language (not wordy)

## Monorepo Organization

- [ ] Skill is in correct directory based on scope:
  - Control Plane -> `control-plane/`
  - Shared -> `shared/`
  - Infrastructure -> `infrastructure/`
- [ ] Skill name reflects its scope
- [ ] Adaptive Skills include context detection
- [ ] Package Skills specify which packages they work with

## DRY Principles

- [ ] Skill references shared Skills instead of duplicating content
- [ ] If building on a shared Skill, includes "Related Skills" section
- [ ] Only includes context-specific content (control-plane/infrastructure/package)
- [ ] Common patterns are in shared Skills, not duplicated
- [ ] References to other Skills use relative paths (e.g., `../../shared/debug-code/SKILL.md`)
- [ ] Supporting files reference shared files when appropriate

## Learning-Infra Specific

- [ ] Tenant isolation requirements are referenced (not duplicated)
- [ ] Multi-tenant architecture patterns are referenced
- [ ] Provisioning workflow patterns are referenced (if applicable)
- [ ] Infrastructure patterns are referenced (if applicable)
- [ ] AGENTS.md is referenced where appropriate

## Testing

- [ ] Skill can be discovered: Ask "What Skills are available?"
- [ ] Skill appears in list with correct description
- [ ] Skill triggers with natural language requests
- [ ] Skill description includes trigger keywords
- [ ] Skill works in intended context (control-plane, infrastructure, package)

## Migration from Cursor Commands (if applicable)

- [ ] Original command structure is preserved
- [ ] Same workflows are maintained
- [ ] Same project rules are referenced
- [ ] Format is converted to Skill format
- [ ] Description is converted to third-person
- [ ] Trigger keywords are added

## Common Issues to Avoid

- [ ] No Windows-style paths (`scripts\helper.py` -> `scripts/helper.py`)
- [ ] No first-person descriptions ("I can help..." -> "Creates...")
- [ ] No vague descriptions ("helps with files" -> specific description)
- [ ] No deeply nested file references (keep one level deep)
- [ ] No time-sensitive information in main content
- [ ] No inconsistent terminology
- [ ] No assumptions about installed packages (list requirements)

## Final Checks

- [ ] All validation items above are checked
- [ ] Skill follows official Claude Skills format
- [ ] Skill follows learning-infra patterns
- [ ] Skill is ready for use
- [ ] Skill is documented in `.skills/skills/README.md` (if applicable)

## Validation Command

After creating your Skill, test it:

1. Ask Claude: "What Skills are available?"
2. Verify your Skill appears with correct description
3. Test triggering: Use natural language that matches description
4. Verify Skill executes correctly in intended context

## Quick Reference

**Required:**

- YAML frontmatter with `name` and `description`
- Third-person description with triggers
- SKILL.md under 500 lines
- Forward slashes in file paths

**Recommended:**

- Project documentation references
- Context detection (if adaptive)
- Concrete examples
- Progressive disclosure (if complex)

**Avoid:**

- First-person descriptions
- Vague descriptions
- Windows-style paths
- Deeply nested references
- Time-sensitive information

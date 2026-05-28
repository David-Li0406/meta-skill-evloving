---
name: skill-reviewer
description: "Reviews Claude Code skills against official best practices and quality standards. Validates YAML frontmatter, checks SKILL.md length under 500 lines, verifies progressive disclosure patterns, assesses description specificity. Use when reviewing SKILL.md files, auditing skill quality, validating against official best practices, or checking skill structure before distribution."
---

# Skill Reviewer

Reviews skills against official best practices from Anthropic's skill authoring guide.

## Review Workflow

### 1. Create TodoWrite Checklist

Create systematic checklist from official quality checklist (see [REFERENCE.md](REFERENCE.md#official-quality-checklist)):

```javascript
TodoWrite([
  // Core Quality (10 items from official checklist)
  {content: "Description specific with key terms", status: "pending", activeForm: "Checking description specificity"},
  {content: "Description includes what + when", status: "pending", activeForm: "Verifying what and when clauses"},
  {content: "SKILL.md body under 500 lines", status: "pending", activeForm: "Counting SKILL.md lines"},
  {content: "Additional details in separate files", status: "pending", activeForm: "Checking file organization"},
  {content: "No time-sensitive information", status: "pending", activeForm: "Scanning for dates/versions"},
  {content: "Consistent terminology throughout", status: "pending", activeForm: "Verifying terminology"},
  {content: "Examples concrete not abstract", status: "pending", activeForm: "Checking example quality"},
  {content: "File references one level deep", status: "pending", activeForm: "Checking reference depth"},
  {content: "Progressive disclosure used appropriately", status: "pending", activeForm: "Verifying progressive disclosure"},
  {content: "Workflows have clear steps", status: "pending", activeForm: "Checking workflow clarity"},

  // Code and Scripts (8 items if scripts present)
  {content: "Scripts solve problems not punt to Claude", status: "pending", activeForm: "Checking script purpose"},
  {content: "Error handling explicit and helpful", status: "pending", activeForm: "Reviewing error handling"},
  {content: "No voodoo constants (all justified)", status: "pending", activeForm: "Checking for magic numbers"},
  {content: "Required packages listed and verified", status: "pending", activeForm: "Verifying dependencies"},
  {content: "Scripts have clear documentation", status: "pending", activeForm: "Checking script docs"},
  {content: "Forward slashes only in paths", status: "pending", activeForm: "Checking path format"},
  {content: "Validation steps for critical operations", status: "pending", activeForm: "Checking validation"},
  {content: "Feedback loops for quality tasks", status: "pending", activeForm: "Checking feedback loops"},

  // Testing (4 items)
  {content: "At least three evaluation scenarios", status: "pending", activeForm: "Checking evaluations"},
  {content: "Tested with Haiku Sonnet Opus", status: "pending", activeForm: "Checking model testing"},
  {content: "Real usage scenarios tested", status: "pending", activeForm: "Checking real-world tests"},
  {content: "Team feedback incorporated", status: "pending", activeForm: "Checking feedback integration"}
])
```

Mark items as they are verified.

### 2. Validate YAML Frontmatter

Verify name, description, and allowed-tools fields meet requirements. See [REFERENCE.md](REFERENCE.md#yaml-frontmatter-validation) for detailed specifications.

### 3. Count SKILL.md Lines

Run `wc -l SKILL.md` to count lines. Target: **Under 500 lines**. See [REFERENCE.md](REFERENCE.md#skillmd-length-guidelines) for remediation if over limit.

### 4. Evaluate Description Quality

Verify description includes specific capabilities, file types, when clause, and uses third person voice. See [REFERENCE.md](REFERENCE.md#description-field-requirements) for good/bad examples.

### 5. Check Progressive Disclosure

Verify file references are one level deep from SKILL.md. See [REFERENCE.md](REFERENCE.md#progressive-disclosure-pattern) for structure patterns.

### 6. Verify Content Quality

Check for concise writing, consistent terminology, concrete examples, and no time-sensitive information. See [REFERENCE.md](REFERENCE.md#content-quality-standards) for detailed standards.

### 7. Check Workflows

Verify workflows have clear sequential steps with checklists and feedback loops. See [REFERENCE.md](REFERENCE.md#workflow-requirements) for examples.

### 8. Review Scripts (if present)

Verify scripts solve problems (don't punt), have no magic numbers, clear execution intent, and documented dependencies. See [REFERENCE.md](REFERENCE.md#script-quality-standards) for detailed standards.

### 9. Verify File Paths

Check all paths use forward slashes (not Windows backslashes). See [REFERENCE.md](REFERENCE.md#path-conventions).

### 10. Check Naming Conventions

Verify skill name uses gerund form (verb + -ing) when possible. See [REFERENCE.md](REFERENCE.md#name-field-requirements) for conventions.

### 11. Assess Degree of Freedom

Evaluate if specificity matches task fragility. See [REFERENCE.md](REFERENCE.md#degree-of-freedom).

### 12. Test Discovery

Based on description, suggest 3-5 test queries:

**Example**: If description mentions "PDF", "extract", "forms":
- "Extract text from this PDF"
- "Fill out this PDF form"
- "Merge these PDF documents"

Skill should activate for these queries.

## Provide Structured Feedback

```markdown
## Skill Review: [skill-name]

### Line Count
SKILL.md: XXX lines (target: <500)

### ✓ Passes Official Checklist
- [Items that meet official requirements]

### ✗ Issues Found

**Critical**:
- SKILL.md body: 650 lines (must be under 500)
- Description missing when clause

**Major**:
- References nested too deep (SKILL.md → advanced.md → details.md)
- Windows-style paths in scripts section
- Time-sensitive information: "Before 2025, use v1 API"

**Minor**:
- Name not in gerund form: `commit-message` → `generating-commit-messages`
- Description uses second person: "you" → third person

### 🔧 Recommended Fixes

1. **Reduce SKILL.md length** (650 → <500 lines):
   - Move examples to `examples.md`
   - Move API reference to `references/api.md`
   - Keep only core workflow in SKILL.md

2. **Fix description**:
   - Current: "Helps create commit messages"
   - Should be: "Generates descriptive commit messages by analyzing git diffs. Use when writing commit messages or reviewing staged changes."

3. **Flatten file references**:
   - Move content from `advanced.md → details.md` directly into `details.md`
   - Reference from SKILL.md: `See [details.md](details.md)`

### Test Queries
Based on description, test activation with:
- "[query using description keywords]"
- "[another test query]"

### Checklist: X/22 items passed
[Show TodoWrite status]

### Official References
- Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Complete checklist: [REFERENCE.md](REFERENCE.md#official-quality-checklist)
```

## Common Issues and Anti-Patterns

See [REFERENCE.md](REFERENCE.md#common-issues-and-fixes) for common issues and [REFERENCE.md](REFERENCE.md#anti-patterns) for anti-patterns to avoid.

## MCP Tool References

If skill uses MCP tools, verify fully qualified names: `ServerName:tool_name`. See [REFERENCE.md](REFERENCE.md#mcp-tool-references).

## Version History

- v2.0.0 (2025-11-15): Renamed from reviewing-skills to skill-reviewer, created REFERENCE.md with detailed specifications, removed duplications from SKILL.md
- v1.0.0: Initial version

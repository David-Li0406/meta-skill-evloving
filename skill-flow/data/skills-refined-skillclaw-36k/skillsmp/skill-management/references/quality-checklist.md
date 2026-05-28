# Skill Quality Checklist

Use this checklist to verify skill quality before considering a skill complete.

## Core Requirements

- [ ] YAML frontmatter with valid `name` and `description`
- [ ] Description includes both "what" and "when"
- [ ] Description lists specific trigger terms/phrases
- [ ] Main content under 500 lines
- [ ] Appropriate file structure (separate reference files if needed)

## Content Quality

- [ ] Only includes information Claude doesn't already know
- [ ] Consistent terminology throughout
- [ ] Forward slashes in all paths
- [ ] Defaults provided for all options
- [ ] Configuration parameters justified
- [ ] Error handling in any scripts
- [ ] No time-sensitive information (or clearly marked)

## Architecture

- [ ] Progressive disclosure used (not loading everything upfront)
- [ ] Referenced files kept one level deep from SKILL.md
- [ ] Long references have table of contents
- [ ] Scripts solve problems rather than punting to Claude

## Testing

- [ ] At least three test scenarios created
- [ ] Tested with real-world usage patterns
- [ ] Verified skill actually gets invoked when intended
- [ ] Works across target models (if applicable)

## Git Management

- [ ] Changes committed to skills repository
- [ ] Commit message describes what changed and why
- [ ] Working directory clean after commit

---

## Examples

### Good Description

```yaml
description: Generate AWS CloudFormation templates following best practices.
Use when: (1) user mentions "CloudFormation", "CFN", or "AWS IaC", (2) creating
infrastructure as code for AWS, (3) user requests template generation or
validation. Includes security best practices, cost optimization patterns, and
common resource configurations.
```

**Why it's good:**
- States what it does clearly
- Lists specific triggers
- Mentions key features
- Appropriate length

### Poor Description

```yaml
description: Helps with cloud stuff.
```

**Why it's bad:**
- Vague "helps with"
- No specific triggers
- No indication of when to use
- Doesn't specify which cloud or what operations

### Effective Skill Structure

```
skill-name/
├── SKILL.md              # Main instructions (<500 lines)
├── references/           # Detailed reference content
│   ├── examples.md       # Detailed examples
│   └── reference.md      # API references, schemas
└── scripts/
    └── validate.py       # Utility scripts
```

SKILL.md references other files only when needed, implementing progressive disclosure.

# audit checklist

per-skill checklist for comprehensive audits.

## quick check (2 min per skill)

- [ ] SKILL.md exists and has content
- [ ] description is specific (not generic)
- [ ] last modified within 90 days
- [ ] has at least one reference file
- [ ] no obvious errors in markdown

## depth check (5 min per skill)

### structure
- [ ] has "when to use" table
- [ ] has decision tree or workflow
- [ ] has anti-patterns section
- [ ] references are linked correctly

### content quality
- [ ] decision tree is actionable (if/then, not philosophy)
- [ ] concrete values present with sources
- [ ] anti-patterns have specific fixes
- [ ] references are substantive (>50 lines)

### integration
- [ ] mentions relevant user tools
- [ ] connects to other skills where appropriate
- [ ] CLI examples are correct syntax

## full audit (15 min per skill)

### validation
- [ ] run consult-light depth check
- [ ] verify example commands work
- [ ] check if skill has been used recently

### relevance
- [ ] skill still matches current workflow
- [ ] no better approach exists now
- [ ] not redundant with another skill

### documentation
- [ ] description matches actual capability
- [ ] triggers list is accurate
- [ ] examples are current

## scoring template

```markdown
## [skill_name] audit

**Date:** YYYY-MM-DD
**Last modified:** YYYY-MM-DD

### Quick check
- [x] SKILL.md exists
- [x] description specific
- [ ] updated < 90 days
- [x] has references
- [x] no markdown errors

### Depth check
- [x] has decision tree
- [ ] concrete values with sources
- [x] anti-patterns with fixes
- [ ] references substantive

### Score: X/10
### Priority: high/medium/low
### Action: [specific next step]
```

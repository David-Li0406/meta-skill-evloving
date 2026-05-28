# Skill Troubleshooting Guide

Common issues and solutions for skill development and usage.

## Table of Contents

- [Discovery Issues](#discovery-issues)
- [Autonomy Issues](#autonomy-issues)
- [Generate Report](#generate-report)
- [Summary](#summary)
- [Key Findings](#key-findings)
- [Recommendations](#recommendations)
- [Deploy Application](#deploy-application)
- [Process File](#process-file)
- [Generate Summary](#generate-summary)
- [Overview](#overview)
- [Key Points](#key-points)
- [Next Steps](#next-steps)

## Discovery Issues

### Problem: Skill Not Triggering

**Symptoms**:
- Claude doesn't use the skill when expected
- Skill doesn't appear in auto-suggestions
- Manual invocation works, but auto-activation doesn't

**Diagnosis**:
1. Check if skill appears in `/help`
2. Review description for trigger keywords
3. Test with direct invocation
4. Check character budget with `/context`

**Solutions**:

**Solution 1: Improve Description**
```yaml
# Before
description: "Helps with coding"

# After
description: "API design patterns for REST endpoints. Use when designing, reviewing, or modifying API endpoints. Do not use for GraphQL or database design."
```

**Solution 2: Add Natural Keywords**
```yaml
# Include words users actually say
description: "Review API designs for REST endpoints. Use when user mentions 'API design', 'REST', 'endpoints', or 'API review'."
```

**Solution 3: Check Scope**
```yaml
# If too specific, expand triggers
# If too general, narrow triggers
description: "Use for HTTP-based REST APIs, not GraphQL or RPC"
```

### Problem: Skill Triggers Too Often

**Symptoms**:
- Skill activates for irrelevant requests
- False positives
- Unwanted auto-activation

**Diagnosis**:
1. Review description specificity
2. Check for generic terms
3. Verify context sensitivity

**Solutions**:

**Solution 1: Narrow Triggers**
```yaml
# Before
description: "Database patterns"

# After
description: "SQL query optimization for PostgreSQL. Use when working with slow database queries or performance issues."
```

**Solution 2: Add Exclusions**
```yaml
description: "API design patterns. Use for REST APIs. Do not use for GraphQL, database schemas, or RPC interfaces."
```

**Solution 3: Use disable-model-invocation**
```yaml
---
name: deploy
description: "Deploy to production"
disable-model-invocation: true  # Only manual invocation
---
```

### Problem: Skill Not Visible in Help

**Symptoms**:
- Skill doesn't appear in `/help` menu
- User can't find the skill
- Direct invocation fails

**Diagnosis**:
1. Check file location: `.claude/skills/skill-name/SKILL.md`
2. Verify YAML frontmatter
3. Check for YAML syntax errors
4. Restart Claude Code

**Solutions**:

**Solution 1: Fix File Location**
```bash
# Wrong
skills/skill-name/SKILL.md

# Correct
.claude/skills/skill-name/SKILL.md
```

**Solution 2: Validate YAML**
```yaml
---
name: skill-name
description: "Valid description"
---
# Ensure proper YAML syntax
```

**Solution 3: Check Naming**
```yaml
# Directory name must match skill name
.claude/skills/my-skill/SKILL.md
# frontmatter: name: my-skill
```

## Autonomy Issues

### Problem: Skill Requires Too Many Questions

**Symptoms**:
- Claude asks multiple clarification questions
- User needs to provide extensive input
- Workflow interrupted frequently

**Diagnosis**:
1. Review workflow for ambiguity
2. Check for missing defaults
3. Identify unclear instructions

**Solutions**:

**Solution 1: Add Defaults**
```markdown
# Before
## Generate Report
Generate a report based on user requirements.

# After
## Generate Report
Use this template by default:

```markdown
# [Topic] Report

## Summary
[2-3 sentence overview]

## Key Findings
- Finding 1
- Finding 2

## Recommendations
1. Action item
```

Customize template based on specific context.
```

**Solution 2: Make Assumptions**
```markdown
## Deploy Application
Assume environment is 'staging' unless specified:

Deploy to ${ARGUMENTS:-staging}:
1. Build application
2. Deploy to environment
3. Verify health
```

**Solution 3: Provide Paths**
```markdown
## Process File

Choose processing method:

**File type is CSV?** → Use CSV workflow
**File type is JSON?** → Use JSON workflow
**File type is XML?** → Use XML workflow

[Each workflow has clear steps]
```

### Problem: Skill Produces Inconsistent Output

**Symptoms**:
- Different outputs for same input
- Inconsistent formatting
- Varying quality

**Diagnosis**:
1. Check for ambiguous instructions
2. Review template usage
3. Identify missing standards

**Solutions**:

**Solution 1: Use Templates**
```markdown
## Generate Summary

ALWAYS use this template:

```markdown
# Summary: [Topic]

## Overview
[2-3 sentences]

## Key Points
- Point 1
- Point 2

## Next Steps
1. Action
2. Action
```
```

**Solution 2: Add Validation**
```markdown
## Generate Summary

1. Create summary using template
2. **Validate immediately**: Check all sections present
3. If missing sections → Add them
4. If format wrong → Re-format
5. Re-validate until perfect
```

## Progressive Disclosure Issues

### Problem: SKILL.md Too Long

**Symptoms**:
- File exceeds 500 lines
- Hard to navigate
- Slow to load

**Diagnosis**:
1. Count lines in SKILL.md
2. Identify detailed content
3. Check for reference-able sections

**Solutions**:

**Solution 1: Move to References**
```markdown
# SKILL.md (150 lines)

## Quick Reference
[Essential content]

See [references/detailed.md](references/detailed.md) for complete guide.

# Example: references/detailed.md (400 lines)
[Detailed content moved here]
```

**Solution 2: Create Reference Files**
```bash
mkdir -p references
mv detailed-content.md references/
mv examples.md references/
mv troubleshooting.md references/
```

### Problem: References Not Loading

**Symptoms**:
- Links to references don't work
- Claude can't find referenced files
- Content not accessible

**Diagnosis**:
1. Check file paths in links
2. Verify files exist
3. Test link syntax

**Solutions**:

**Solution 1: Fix Link Paths**
```markdown
# Wrong
See [detailed](detailed.md)

# Correct
See [references/detailed.md](references/detailed.md)
```

**Solution 2: Verify File Structure**
```bash
skill-name/
├── SKILL.md
└── references/
    └── detailed.md
```

**Solution 3: Use Relative Paths**
```markdown
# From SKILL.md
[Link](references/file.md)

# Not absolute paths
<!-- Don't use absolute paths like /absolute/path -->
```

### Problem: Nested References Not Working

**Symptoms**:
- References within references fail
- Partial content loading
- Incomplete information

**Diagnosis**:
1. Check nesting depth
2. Review reference chain
3. Test link traversal

**Solutions**:

**Solution 1: Keep One Level Deep**
```markdown
# SKILL.md
See [references/advanced.md](references/advanced.md)

# references/advanced.md
Don't include further references

# Instead, use:
See [references/specific-topic.md](references/specific-topic.md)
```

**Solution 2: Include Table of Contents**
```markdown
# references/advanced.md

## Contents
- Section 1
- Section 2
- Section 3

## Section 1
[Content]
```

## Performance Issues

### Problem: Skill Slows Down Claude

**Symptoms**:
- Long loading times
- High token consumption
- Delayed responses

**Diagnosis**:
1. Check SKILL.md size
2. Review token usage
3. Identify expensive operations

**Solutions**:

**Solution 1: Reduce SKILL.md Size**
```markdown
# Before: 1000 lines
# After: <500 lines

Move detailed content to references/
```

**Solution 2: Use Progressive Disclosure**
```markdown
# Only load what you need
[Essential content in SKILL.md]
[Detailed content in references/]
```

**Solution 3: Optimize Instructions**
```markdown
# Before
PDF processing requires careful attention to detail...

# After
Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

### Problem: Context Window Exceeded

**Symptoms**:
- Skill won't load
- Truncated content
- Errors about context

**Diagnosis**:
1. Check total context usage
2. Review all loaded skills
3. Monitor token budget

**Solutions**:

**Solution 1: Check Context Budget**
```bash
/context
# Check character budget
# See which skills are loaded
```

**Solution 2: Reduce Skill Count**
- Only keep essential skills
- Remove rarely used skills
- Combine similar skills

**Solution 3: Use User-Local Settings**
```bash
# Instead of global skills
~/.claude/skills/

# Use project-specific
.claude/skills/
```

## Quality Issues

### Problem: Skill Fails Validation

**Symptoms**:
- YAML syntax errors
- Invalid frontmatter
- Naming violations

**Diagnosis**:
1. Run skills-ref validate
2. Check YAML syntax
3. Review naming conventions

**Solutions**:

**Solution 1: Fix YAML**
```yaml
# Wrong
---
name: Skill Name  # Spaces not allowed
description: "Description"
invalid-field: value

# Correct
---
name: skill-name
description: "Description"
---
```

**Solution 2: Check Name Format**
```yaml
# Wrong
name: MySkill
name: my_skill
name: SKILL-NAME

# Correct
name: my-skill
```

**Solution 3: Validate Description**
```yaml
# Wrong
description: ""  # Empty
description: "Too long..." * 1000  # Over 1024 chars
description: "<script>"  # XML tags

# Correct
description: "WHAT + WHEN + NOT formula"  # 1-1024 chars, no XML
```

### Problem: Poor Quality Score

**Symptoms**:
- Audit score <120 points
- Multiple failing dimensions
- Quality issues identified

**Diagnosis**:
1. Run quality audit
2. Score all 11 dimensions
3. Identify weakest areas

**Solutions**:

**Solution 1: Focus on High-Impact**
```markdown
Priority improvements:
1. Autonomy (15 points max)
2. Discoverability (15 points max)
3. Knowledge Delta (15 points max)

Address these first for biggest gain.
```

**Solution 2: Apply Patterns**
```markdown
See [patterns.md](patterns.md) for:
- Pattern 4: Fix Autonomy
- Pattern 2: Improve Triggers
- Pattern 1: Add URL Fetching
```

**Solution 3: Re-audit After Changes**
```bash
# After applying improvements
Re-run audit
Score all dimensions
Verify grade improvement
```

## Usage Issues

### Problem: Users Can't Find Skill

**Symptoms**:
- Skill not in `/help`
- Users don't know skill exists
- Manual invocation unknown

**Solutions**:

**Solution 1: Document Skill**
```markdown
# README.md

## Available Skills

### api-review
Review API designs: `/api-review`
See [.claude/skills/api-review/SKILL.md](.claude/skills/api-review/SKILL.md)
```

**Solution 2: Train Users**
- Show skill in action
- Explain auto-discovery
- Share trigger keywords

**Solution 3: Create Cheat Sheet**
```markdown
# Skill Cheat Sheet

/api-review - Review API designs
/security-audit - Security checklist
/deploy [env] - Deploy application
```

### Problem: Skill Misused

**Symptoms**:
- Wrong context activation
- Inappropriate usage
- Users confused about purpose

**Solutions**:

**Solution 1: Clarify Purpose**
```yaml
description: "Use for X. Do not use for Y."
```

**Solution 2: Add Examples**
```markdown
## When to Use

✅ Good use:
"Review this REST API design"

❌ Bad use:
"Design a database schema"
```

**Solution 3: Add Exclusions**
```markdown
description: "Use for REST APIs. Do not use for GraphQL, RPC, or database design."
```

## Testing Issues

### Problem: Can't Test Skill

**Symptoms**:
- Skill doesn't execute
- No response to invocation
- Silent failures

**Solutions**:

**Solution 1: Test Manual Invocation**
```bash
/skill-name
# Should produce output
```

**Solution 2: Check Logs**
```bash
# Look for error messages
# Check skill execution logs
```

**Solution 3: Simplify Test**
```markdown
# Minimal test skill
---
name: test-skill
description: "Test skill"
---

# Test

Hello from test skill!
```

### Problem: Auto-Discovery Not Working

**Symptoms**:
- Manual invocation works
- Auto-activation fails
- Triggers don't work

**Solutions**:

**Solution 1: Test Triggers**
```bash
# Try different phrasings
"API design"
"Review REST API"
"Check endpoints"
```

**Solution 2: Check Description**
```yaml
# Include common keywords
description: "API design review for REST endpoints"
```

**Solution 3: Verify Activation**
```markdown
## Test Auto-Discovery

1. Say trigger phrase
2. Verify skill activates
3. Check response
4. Document result
```

## Advanced Troubleshooting

### Problem: Multiple Skill Conflicts

**Symptoms**:
- Two skills both activate
- Conflicting advice
- Unclear which to use

**Solutions**:

**Solution 1: Narrow Scope**
```yaml
# Skill 1
description: "API design for REST only"

# Skill 2
description: "Database schema design"
```

**Solution 2: Use Specific Keywords**
```yaml
description: "Use when user says 'REST API design'"
```

### Problem: Skill Updates Not Loading

**Symptoms**:
- Changes don't take effect
- Old behavior persists
- Caching issues

**Solutions**:

**Solution 1: Restart Claude**
```bash
# Restart Claude Code
# Reload all skills
```

**Solution 2: Clear Cache**
```bash
# Clear skill cache
# Force reload
```

**Solution 3: Verify File**
```bash
# Check file was saved
# Verify changes present
```

### Problem: Platform Compatibility

**Symptoms**:
- Works in one platform, not another
- Different behavior across environments
- Platform-specific issues

**Solutions**:

**Solution 1: Check Documentation**
```markdown
# Verify platform supports features
# Check version compatibility
```

**Solution 2: Use Cross-Platform Patterns**
```bash
# Use forward slashes (not Windows backslashes)
# Avoid platform-specific commands
```

**Solution 3: Add Platform Checks**
```markdown
## Platform Notes

- claude.ai: Full support
- Anthropic API: Limited features
- Third-party clients: Varies
```

## Diagnostic Checklist

### Pre-Diagnosis
- [ ] Skill file exists at correct location
- [ ] YAML frontmatter is valid
- [ ] Skill name matches directory
- [ ] Claude Code has been restarted

### Discovery Testing
- [ ] Skill appears in `/help`
- [ ] Manual invocation works: `/skill-name`
- [ ] Auto-activation triggers with keywords
- [ ] No false positives

### Autonomy Testing
- [ ] Completes without questions
- [ ] Produces consistent output
- [ ] Handles edge cases
- [ ] Validates inputs

### Quality Testing
- [ ] Passes skills-ref validate
- [ ] Follows naming conventions
- [ ] URL fetching sections present
- [ ] Progressive disclosure working

## Getting Help

### Self-Help Resources
1. **Reference files**:
   - [types.md](types.md) - Skill types and examples
   - [creation.md](creation.md) - Creation guide
   - [patterns.md](patterns.md) - Improvement patterns

2. **Official Documentation**:
   - https://code.claude.com/docs/en/skills
   - https://github.com/agentskills/agentskills

3. **Community Resources**:
   - GitHub: anthropics/skills
   - GitHub: agentskills/examples

### Creating Bug Reports
Include:
- Skill name and location
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages
- Platform information

### Debug Mode
```bash
# Enable verbose logging
# Check execution details
# Monitor skill loading
```

## Best Practices for Troubleshooting

### DO ✅
- Start with simple tests
- Check YAML syntax first
- Verify file locations
- Test auto-discovery separately
- Document solutions
- Share learnings with team

### DON'T ❌
- Don't skip basic checks
- Don't ignore YAML errors
- Don't assume file saved
- Don't test only manual invocation
- Don't hide issues
- Don't skip documentation

## Prevention Tips

### During Creation
- Validate YAML early
- Test frequently
- Use progressive disclosure
- Include URL fetching
- Follow naming conventions

### During Testing
- Test auto-discovery
- Test manual invocation
- Test with arguments
- Verify autonomy
- Check quality score

### During Maintenance
- Re-validate after changes
- Update documentation
- Monitor usage
- Gather feedback
- Iterate improvements

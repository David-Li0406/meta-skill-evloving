# PR Review Patterns

Detailed patterns and workflows for reviewing pull requests with GitHub and Linear integration.

## Common Patterns

### Pattern 1: Basic PR Review

```bash
# 1. Get PR details
PR_NUMBER=123
gh pr view $PR_NUMBER --json title,body

# 2. Extract Linear issue
ISSUE_ID=$(gh pr view $PR_NUMBER --json body --jq '.body' | grep -oE 'LIN-[0-9]+' | head -1)

# 3. Get issue requirements (via Linear MCP)
# Use mcp_Linear_get_issue with ISSUE_ID

# 4. Review PR diff
gh pr diff $PR_NUMBER

# 5. Validate and document findings
```

### Pattern 2: Multi-Issue PR Review

When PR addresses multiple issues:

```bash
# Extract all issue IDs
ISSUE_IDS=$(gh pr view $PR_NUMBER --json body --jq '.body' | grep -oE 'LIN-[0-9]+')

# Fetch each issue
for ISSUE_ID in $ISSUE_IDS; do
  # Use mcp_Linear_get_issue for each
  # Validate PR addresses each issue's requirements
done
```

### Pattern 3: Requirement Checklist Validation

```typescript
// Parse issue description for checkboxes
const requirements = parseCheckboxes(issue.description);

// Check each requirement against PR changes
for (const requirement of requirements) {
  const isAddressed = validateRequirement(requirement, prChanges);
  if (!isAddressed) {
    gaps.push(requirement);
  }
}

// Report findings
```

### Pattern 4: Code Quality Validation

```bash
# Check against project standards
# 1. Review AGENTS.md rules
# 2. Check Cursor rules compliance
# 3. Validate file structure
# 4. Check test coverage (if applicable)
# 5. Review documentation updates
```

## Handling Edge Cases

### PR Without Linear Issue

**Strategy:**
1. Check PR title/body for issue references
2. If none found, note in review
3. Suggest creating/attaching Linear issue
4. Proceed with code quality review only

### Multiple Issues in One PR

**Strategy:**
1. Extract all issue IDs
2. Fetch all issues
3. Validate PR addresses each issue
4. Create separate review sections per issue
5. Update all related issues with findings

### Incomplete Requirements

**Strategy:**
1. Note missing or unclear requirements
2. Request clarification in Linear issue
3. Proceed with partial review
4. Document assumptions made

## Review Checklist Template

```markdown
## PR Review Checklist

### Requirements Validation
- [ ] All acceptance criteria from Linear issue addressed
- [ ] Feature specifications implemented
- [ ] Edge cases handled
- [ ] Related issues considered

### Code Quality
- [ ] Follows AGENTS.md standards
- [ ] Follows Cursor rules
- [ ] Proper error handling
- [ ] Tests included (if required)
- [ ] Documentation updated

### Integration
- [ ] No breaking changes (or documented)
- [ ] Backward compatibility maintained
- [ ] Dependencies updated
- [ ] CI/CD checks passing

### Documentation
- [ ] PR description clear
- [ ] Code comments adequate
- [ ] README/docs updated (if needed)
- [ ] Changelog updated (if applicable)
```

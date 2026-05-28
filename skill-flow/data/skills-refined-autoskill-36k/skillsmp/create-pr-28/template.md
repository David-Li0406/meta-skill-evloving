# PR Template Discovery

## Finding the Template

Before generating PR content, check for an existing template in the repository:

```bash
# Check common locations for PR templates
ls -la .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null
ls -la .github/pull_request_template.md 2>/dev/null
ls -la .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null
ls -la docs/pull_request_template.md 2>/dev/null
ls -la PULL_REQUEST_TEMPLATE.md 2>/dev/null
```

## If Template Found

1. Read the template file
2. Use the template structure as the foundation
3. Fill in sections based on the changes and Jira ticket
4. Respect any custom sections or checkboxes defined in the template

## If No Template Found

Use this default structure:

```markdown
## Summary

<Brief description of what this PR does>

## Changes

<Bullet points of what was changed>

## Testing

<How to test these changes>

## Checklist

- [ ] Self-reviewed code
- [ ] Tests pass
- [ ] Documentation updated (if needed)
```

## Enhancements to Add

Regardless of template, include these when relevant:

### Jira Link
```markdown
## Ticket

[TICKET-ID](https://vuoriclothing.atlassian.net/browse/TICKET-ID)
```

### Architecture Diagram (for significant changes)
See [diagrams.md](diagrams.md) for examples.

### AI Disclosure (if AI was used)
```markdown
## AI-Generated Code

- Files modified with AI assistance: <list files>
- All code was reviewed and validated before commit
```

## Notes

- Preserve any project-specific sections from the template
- Don't remove required checkboxes or fields
- Add Jira integration even if not in template
- Add diagrams for complex changes even if not required

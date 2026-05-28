---
name: github-issues
description: Create, update, and manage GitHub issues for the LucidData project using MCP tools. Use when users want to create bug reports, feature requests, or task issues, add labels (bug, enhancement, security, privacy, testing), assign team members, manage milestones, or track project workflow. Includes LucidData-specific issue templates and security considerations.
license: MIT
compatibility: Designed for Claude Code with GitHub MCP server. Requires GitHub authentication and repository access (owner/repo detection automatic).
metadata:
  author: LucidData Team
  version: "1.0"
  project: LucidData MVP
  tech_stack: Next.js, React, TypeScript, Prisma, Supabase
allowed-tools: mcp__github__create_issue mcp__github__update_issue mcp__github__get_issue mcp__github__search_issues mcp__github__add_issue_comment mcp__github__list_issues
---

# GitHub Issues Management

GitHub workflow integration for the LucidData project using MCP tools for issue tracking and project management.

## Overview

This skill enables efficient GitHub issue management for LucidData, providing templates for bug reports, feature requests, security vulnerabilities, and test failures. It follows best practices for issue tracking in a privacy-first personal data bank application.

## When to Use This Skill

Activate this skill when you need to:

- **Create bug reports**: Document bugs with encryption/audit log context
- **Request features**: Propose new functionality with privacy impact assessment
- **Report security vulnerabilities**: Follow responsible disclosure practices
- **Track test failures**: Document failing Vitest/Playwright tests
- **Update issues**: Add labels, assign team members, update status
- **Search issues**: Find existing issues by keyword, label, or status
- **Comment on issues**: Add technical context or updates

## LucidData-Specific Issue Categories

### Bug (label: `bug`)
Software defects, incorrect behavior, crashes

**Common subcategories**:
- **Encryption** (`encryption`): Issues with AES-256-GCM encryption/decryption
- **Database** (`database`): Prisma queries, migrations, data integrity
- **Auth** (`auth`): Supabase authentication, session management
- **UI** (`ui`): React component bugs, layout issues

### Enhancement (label: `enhancement`)
New features, improvements to existing functionality

**Common subcategories**:
- **Privacy** (`privacy`): Consent management, data portability
- **Security** (`security`): Security improvements, audit logging
- **Performance** (`performance`): Speed optimizations, caching
- **UX** (`ux`): User experience improvements

### Security Vulnerability (label: `security`)
Security issues requiring responsible disclosure

**Severity labels**:
- `critical`: RCE, data breach, auth bypass
- `high`: XSS, CSRF, SQL injection
- `medium`: Information disclosure
- `low`: Minor security improvements

### Testing (label: `testing`)
Test failures, missing test coverage, test infrastructure

### Documentation (label: `documentation`)
README updates, API docs, code comments

## Issue Templates

### Bug Report Template

```markdown
## Bug Description
[Clear, concise description of the bug]

## Steps to Reproduce
1. Navigate to...
2. Click on...
3. Enter...
4. Observe error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- **Browser**: Chrome 131 / Firefox 133 / Safari 17
- **OS**: Windows 11 / macOS 15 / Ubuntu 22.04
- **Node.js**: v18.x
- **Next.js**: 15.1.3

## Screenshots/Logs
[Attach screenshots or paste error logs]

## Additional Context
- **Encryption context**: [If related to vault data]
- **Audit log ID**: [If related to audit trail]
- **User ID**: [Anonymized if needed]

## Security Considerations
⚠️ **DO NOT include**: Encryption keys, passwords, real user data, API keys
```

### Feature Request Template

```markdown
## Feature Description
[Clear description of the proposed feature]

## User Story
As a [user type], I want to [action] so that [benefit].

## Use Case
[Describe the problem this feature solves]

## Proposed Solution
[How should this feature work?]

## Privacy Impact Assessment
- **Data collected**: [What new data, if any?]
- **Consent required**: [Yes/No]
- **Encryption**: [How will data be protected?]
- **Audit logging**: [What events to log?]

## Alternatives Considered
[Other approaches considered]

## Additional Context
[Mockups, wireframes, references]
```

### Security Vulnerability Template

```markdown
## Vulnerability Type
[XSS / CSRF / SQL Injection / etc.]

## Severity
[Critical / High / Medium / Low]

## Affected Component
[Vault API / Consent management / Auth system / etc.]

## Description
[Detailed description of the vulnerability]

## Proof of Concept
[Steps to reproduce - DO NOT include actual exploit code for critical issues]

## Impact
[What could an attacker do?]

## Suggested Fix
[Recommended remediation]

## Security Considerations
⚠️ **This issue contains sensitive security information**
- DO NOT publicly disclose until patch is released
- Coordinate with maintainers for responsible disclosure
```

### Test Failure Template

```markdown
## Test Information
- **Test file**: `path/to/test.test.ts`
- **Test name**: "should validate encryption"
- **Framework**: Vitest / Playwright

## Failure Output
```
[Paste test error output]
```

## Expected Result
[What should the test check?]

## Actual Result
[What is the test finding?]

## Reproducibility
- [ ] Fails consistently
- [ ] Fails intermittently (flaky test)
- [ ] Fails only in CI/CD
- [ ] Fails only locally

## Context
[Recent changes that may have caused this]
```

## Standard Labels

### Type Labels
- `bug` - Software defect
- `enhancement` - New feature or improvement
- `security` - Security issue or improvement
- `documentation` - Documentation updates
- `testing` - Test-related issues

### Component Labels
- `encryption` - AES-256-GCM encryption/decryption
- `database` - Prisma, PostgreSQL, migrations
- `auth` - Supabase authentication
- `consent` - Consent management system
- `audit-log` - Audit trail and hash chain
- `vault` - Vault data management
- `ui` - User interface, React components

### Priority Labels
- `critical` - Blocking issue, immediate attention
- `high` - Important, should be addressed soon
- `medium` - Standard priority
- `low` - Nice to have, not urgent

### Status Labels
- `needs-triage` - Needs initial review
- `needs-info` - Waiting for more information
- `in-progress` - Being worked on
- `blocked` - Blocked by dependency
- `wontfix` - Will not be fixed
- `duplicate` - Duplicate of another issue

## Security Considerations

### What NOT to Include in Issues

⚠️ **NEVER include in public issues**:
- Encryption keys (ENCRYPTION_KEY)
- API keys or secrets (SUPABASE_SERVICE_ROLE_KEY)
- Real user data (emails, names, PII)
- Database connection strings
- Session tokens or auth credentials
- Actual exploit code for critical vulnerabilities

### Safe Issue Reporting

✅ **Safe to include**:
- Anonymized user IDs (`user-***`)
- Test/dummy data
- Stack traces (after removing secrets)
- Screenshots (after redacting sensitive info)
- Code snippets (without hardcoded secrets)

### Responsible Disclosure

For **critical security vulnerabilities**:
1. Email maintainers privately FIRST
2. Wait for acknowledgment (24-48 hours)
3. Coordinate public disclosure timeline
4. Create issue AFTER patch is released

## MCP Tool Usage

### Create Issue

```typescript
// Using GitHub MCP
await mcp__github__create_issue({
  title: "Bug: Vault encryption fails on large files",
  body: "Bug report content...",
  labels: ["bug", "encryption", "high"],
  assignees: ["maintainer-username"],
});
```

### Update Issue

```typescript
await mcp__github__update_issue({
  issue_number: 123,
  labels: ["bug", "encryption", "in-progress"],
  assignees: ["developer-username"],
});
```

### Search Issues

```typescript
await mcp__github__search_issues({
  query: "label:encryption is:open",
  sort: "created",
  order: "desc",
});
```

### Add Comment

```typescript
await mcp__github__add_issue_comment({
  issue_number: 123,
  body: "Additional context: This affects Prisma 6.19.1+ with large BLOBs",
});
```

## Workflow Best Practices

1. **Search first**: Check for existing issues before creating duplicates
2. **Use templates**: Follow issue templates for consistency
3. **Add labels**: Tag with appropriate type, component, priority labels
4. **Be specific**: Include steps to reproduce, environment details
5. **Protect secrets**: Never include keys, passwords, or real user data
6. **Follow up**: Add updates as you investigate or fix issues
7. **Close when done**: Close issues with resolution summary

## References

For more detailed information, see:

- [Issue Templates](references/issue-templates.md) - Full markdown templates
- [Labels Guide](references/labels.md) - Complete label taxonomy

## Example Issues

See [example-issues.json](assets/example-issues.json) for sample issue payloads.

## Quick Reference

| Task | MCP Tool | Example |
|------|----------|---------|
| Create bug report | `mcp__github__create_issue` | Title, body, labels: ["bug"] |
| Create feature | `mcp__github__create_issue` | Include privacy assessment |
| Update labels | `mcp__github__update_issue` | Add/remove labels |
| Assign issue | `mcp__github__update_issue` | Set assignees |
| Find encryption issues | `mcp__github__search_issues` | Query: "label:encryption" |
| Comment on issue | `mcp__github__add_issue_comment` | Add technical context |

---

**Version**: 1.0
**Last Updated**: 2026-01-13
**Maintained by**: LucidData Team

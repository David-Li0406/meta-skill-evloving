# GitHub Issue Templates

Complete examples of issue templates for `.github/ISSUE_TEMPLATE/`.

## Directory Structure

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.md
    ├── feature_request.md
    ├── documentation.md
    └── config.yml
```

## Bug Report Template

**File:** `.github/ISSUE_TEMPLATE/bug_report.md`

```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: 'Bug: '
labels: bug, needs-triage
assignees: ''
---

## Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior

A clear description of what you expected to happen.

## Actual Behavior

A clear description of what actually happened.

## Screenshots

If applicable, add screenshots to help explain your problem.

## Environment

- **OS:** [e.g., macOS 14.0, Windows 11, Ubuntu 22.04]
- **Browser:** [e.g., Chrome 120, Firefox 121, Safari 17]
- **App Version:** [e.g., 1.2.3]
- **Node Version:** [if applicable]

## Additional Context

Add any other context about the problem here.

## Acceptance Criteria

- [ ] Bug no longer reproducible with steps above
- [ ] Regression test added to prevent recurrence
- [ ] Root cause documented (if significant)
- [ ] Related documentation updated (if applicable)
```

## Feature Request Template

**File:** `.github/ISSUE_TEMPLATE/feature_request.md`

```markdown
---
name: Feature Request
about: Suggest a new feature or enhancement
title: 'Feature: '
labels: enhancement, needs-triage
assignees: ''
---

## User Story

As a [type of user],
I want [goal or desire],
So that [benefit or value].

## Description

A detailed description of the feature you're requesting.

### Problem Statement

What problem does this feature solve? Why is it needed?

### Proposed Solution

How do you envision this feature working?

## Alternatives Considered

Describe any alternative solutions or features you've considered.

## Mockups / Examples

If applicable, add mockups, wireframes, or examples from other products.

## Acceptance Criteria

- [ ] [Specific, testable requirement]
- [ ] [Another specific requirement]
- [ ] Unit tests added
- [ ] Integration tests added (if applicable)
- [ ] Documentation updated
- [ ] Changelog updated

## Additional Context

Add any other context, screenshots, or references here.

## Dependencies

List any dependencies this feature has on other issues or external factors.

- Depends on #XX
- Requires API version X.Y
```

## Documentation Template

**File:** `.github/ISSUE_TEMPLATE/documentation.md`

```markdown
---
name: Documentation
about: Suggest a documentation improvement
title: 'Docs: '
labels: documentation, needs-triage
assignees: ''
---

## What needs documentation?

Describe what needs to be documented or improved.

## Current State

What documentation exists currently? (Link if applicable)

## Target Audience

Who is this documentation for?
- [ ] New users / Getting started
- [ ] Developers integrating the API
- [ ] Contributors to the project
- [ ] Operations / DevOps
- [ ] Other: ___

## Proposed Content

Outline what should be included:

1. ...
2. ...
3. ...

## Acceptance Criteria

- [ ] Documentation written and reviewed
- [ ] Examples are tested and working
- [ ] Links verified
- [ ] Spelling and grammar checked
- [ ] Added to navigation / table of contents
```

## Security Vulnerability Template

**File:** `.github/ISSUE_TEMPLATE/security.md`

```markdown
---
name: Security Vulnerability
about: Report a security vulnerability (use private reporting if available)
title: ''
labels: security
assignees: ''
---

⚠️ **STOP!** If this is a sensitive security issue, please use GitHub's private vulnerability reporting feature or email security@example.com instead of creating a public issue.

---

## For Non-Sensitive Security Issues

### Vulnerability Type

- [ ] Information Disclosure
- [ ] Authentication Issue
- [ ] Authorization Issue
- [ ] Injection
- [ ] Cross-Site Scripting (XSS)
- [ ] Other: ___

### Description

Describe the vulnerability and its potential impact.

### Steps to Reproduce

1. ...
2. ...

### Affected Versions

- Version X.Y.Z

### Suggested Fix

If you have ideas on how to fix this, please share.

### Acceptance Criteria

- [ ] Vulnerability patched
- [ ] Security test added
- [ ] Security advisory published (if applicable)
- [ ] Affected users notified (if applicable)
```

## Configuration File

**File:** `.github/ISSUE_TEMPLATE/config.yml`

```yaml
blank_issues_enabled: false
contact_links:
  - name: Questions & Discussions
    url: https://github.com/org/repo/discussions
    about: Please ask questions in Discussions, not Issues
  - name: Security Vulnerabilities
    url: https://github.com/org/repo/security/advisories/new
    about: Please report security vulnerabilities privately
  - name: Documentation
    url: https://docs.example.com
    about: Check our documentation before opening an issue
```

## Advanced: Form-Based Templates (YAML)

GitHub supports form-based issue templates for better UX.

**File:** `.github/ISSUE_TEMPLATE/bug_report.yml`

```yaml
name: Bug Report
description: Report a bug to help us improve
title: "[Bug]: "
labels: ["bug", "needs-triage"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to report a bug!

  - type: input
    id: version
    attributes:
      label: Version
      description: What version are you running?
      placeholder: ex. 1.2.3
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear description of the bug
      placeholder: What happened?
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen?
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options:
        - macOS
        - Windows
        - Linux
        - iOS
        - Android
    validations:
      required: true

  - type: dropdown
    id: browser
    attributes:
      label: Browser
      options:
        - Chrome
        - Firefox
        - Safari
        - Edge
        - Other
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Checklist
      options:
        - label: I have searched for similar issues
          required: true
        - label: I have provided all requested information
          required: true
```

## Template Tips

1. **Keep templates focused** - One purpose per template
2. **Use placeholders** - Guide users on what to write
3. **Required fields** - Balance thoroughness with friction
4. **Labels** - Auto-apply relevant labels
5. **Assignees** - Only auto-assign if you have a clear owner
6. **Disable blank issues** - Force use of templates in config.yml

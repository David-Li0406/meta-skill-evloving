---
name: documentation-and-changelog-auditor
description: Use this skill to audit project documentation and verify the accuracy of CHANGELOG.md based on code changes.
---

# Documentation and CHANGELOG Auditor Skill

This skill audits project documentation and verifies the contents of CHANGELOG.md to ensure they are accurate and up-to-date.

## Rules for Verifying CHANGELOG.md

- Always update CHANGELOG.md when there are changes that affect users of the framework.
  - Changes to non-private classes or methods in `src/` require an update.
  - If the change is a breaking change, it should correspond to a minor or major version update according to SemVer.
  - Bug fixes that result in minor breaking changes may allow for a patch version update.

### Important Formatting and Content Rules

When updating CHANGELOG.md, follow these formatting guidelines:

- Use the format based on [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/).
- Document changes from the user's perspective, focusing on how features have been added, changed, or fixed.
- Avoid detailing implementation specifics; instead, describe the impact on users.
- Reference PR or Issue numbers in the format `[#123](github.com/your-repo/issues/123)`.
- Use the full qualified class name (FQCN) for class names, even if verbose.

## Documentation Audit Process

This skill also audits the following documents for updates based on code changes:

- `README.md`, `README.mdx` - Project description
- `CHANGELOG.md`, `CHANGELOG.txt` - Change history
- All Markdown files in the `docs/` directory
- `.claude/CLAUDE.md` - Claude Code settings
- `CONTRIBUTING.md` - Contribution guidelines

### Audit Process Steps

1. **Change Detection**: Identify changed files using `git diff --name-only`.
2. **Related Document Identification**: Estimate related documents based on changed file paths.
3. **Consistency Check**: Compare document content with actual code/settings to ensure:
   - New features are documented.
   - Deleted features are removed from documentation.
   - API changes are reflected in documentation.
4. **Update Proposals**: 
   - Automatically suggest updates based on changes.
   - Provide proposals and reasons for manual review when necessary.

### Output Format

```markdown
## Documentation Audit Results

### Documents Needing Updates

1. **README.md**
   - Reason: A new CLI option --verbose has been added.
   - Recommendation: Add to the "Usage" section.

2. **docs/api.md**
   - Reason: The response format for the /api/users endpoint has changed.
   - Recommendation: Update the API reference.

Would you like to execute the updates?
```

## Execution Steps

1. Check changed files with `git status` and `git diff --name-only HEAD`.
2. Search for documentation files in the project using Glob.
3. Verify the consistency of changes with documentation.
4. Propose specific updates if necessary.
5. Execute updates upon user approval.
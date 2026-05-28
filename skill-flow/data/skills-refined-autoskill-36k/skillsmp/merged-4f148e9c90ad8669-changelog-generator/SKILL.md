---
name: changelog-generator
description: Use this skill to automatically create user-friendly changelogs from git commits, transforming technical details into clear release notes for customers.
---

# Changelog Generator

This skill transforms technical git commits into polished, user-friendly changelogs that your customers and users will actually understand and appreciate.

## When to Use This Skill

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. **Scans Git History**: Analyzes commits from a specific time period or between versions.
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security).
3. **Translates Technical → User-Friendly**: Converts developer commits into customer language.
4. **Formats Professionally**: Creates clean, structured changelog entries.
5. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.).
6. **Follows Best Practices**: Applies changelog guidelines and your brand voice.

## How to Use

### Basic Usage

From your project repository:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version <version_number>
```

### With Specific Date Range

```
Create a changelog for all commits between <start_date> and <end_date>
```

### With Custom Guidelines

```
Create a changelog for commits since <version>, using my changelog guidelines from <guidelines_file>
```

## Example

**User**: "Create a changelog for commits from the past 7 days"

**Output**:
```markdown
# Updates - Week of <date>

## ✨ New Features

- **Feature 1**: Description of feature 1.
- **Feature 2**: Description of feature 2.

## 🔧 Improvements

- **Improvement 1**: Description of improvement 1.
- **Improvement 2**: Description of improvement 2.

## 🐛 Fixes

- Fixed issue with <issue_description>.
- Resolved <another_issue_description>.
```

## Tips

- Run from your git repository root.
- Specify date ranges for focused changelogs.
- Use your custom guidelines for consistent formatting.
- Review and adjust the generated changelog before publishing.
- Save output directly to CHANGELOG.md.

## Related Use Cases

- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
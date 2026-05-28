---
name: writing-documentation
description: Best practices for project documentation including README, CONTRIBUTING, CHANGELOG, and Markdown files. Use when updating documentation, writing README sections, or maintaining project docs.
allowed-tools: Read, Grep, Glob
---

Standards for creating and maintaining clear, consistent project documentation.

## Core Philosophy

**Documentation should be scannable, actionable, and maintainable.** Every section must justify its existence. Verbose documentation is rarely read.

## File Standards

### README.md

**Essential sections** (in order): Title/Description, Installation, Usage, Configuration (if applicable), License

**Avoid**: Lengthy introductions, obvious explanations, feature lists duplicating code, purposeless badges

### CONTRIBUTING.md

**Essential sections**: Development Setup, Code Standards, Testing, Pull Request Process

### CHANGELOG.md

Follow Keep a Changelog format. Newest first. Group by: Added, Changed, Deprecated, Removed, Fixed, Security.

## Markdown Standards

| Element     | Rule                                                            |
| ----------- | --------------------------------------------------------------- |
| Headers     | One H1 per file, hierarchical (no skipping), no punctuation     |
| Code blocks | Always specify language                                         |
| Lists       | Use `-` for unordered, `1.` for ordered, parallel grammar       |
| Links       | Descriptive text (not "click here"), relative for internal docs |

## Writing Style

- **Active voice**: "Run npm install" not "Dependencies can be installed by running..."
- **Imperative mood**: "Install the package" not "You should install the package"
- **Cut filler**: Delete "In order to", "It is important to note that", "This section will explain"
- **One idea per sentence**

## Code Examples

Make examples runnable: complete (not fragments), realistic variable names, show expected output when helpful.

## Configuration Docs

Show examples with inline comments, not verbose prose descriptions.

## Common Issues

Outdated instructions, missing prerequisites, broken examples, inconsistent formatting, stale information

## Maintenance Checklist

- [ ] Headers follow hierarchy
- [ ] Code blocks specify language
- [ ] Links work
- [ ] Examples are tested
- [ ] Consistent terminology
- [ ] Active voice, imperative mood
- [ ] Prerequisites stated

## Remember

- **Scannable beats comprehensive** - Walls of text don't get read
- **Show don't tell** - Examples over explanations
- **Test everything** - Code examples must work
- **Concise beats verbose** - Cut unnecessary words

Documentation is for the reader, not the writer.

---
name: docs-writer
description: "Documentation review and writing process. Use when writing or reviewing README files, API documentation, changelogs, or code comments. Also use when documentation is longer than the code it explains, readers need to read everything to find anything, comments explain what code does instead of why, or README doesn't show how to get started quickly. Essential for documentation PRs and technical writing reviews."
---

# Documentation Skill

## Overview

Documentation exists to help readers, not to showcase what the writer knows. This skill guides writing clear, useful documentation that people actually read.

**Core principle:** Write for the reader who needs to get something done. Answer their questions before they ask.

## The Documentation Process

### Phase 1: Understand the Reader

**Before writing anything:**

1. **Who is the reader?**
   - New user trying to get started?
   - Developer integrating your API?
   - Maintainer debugging an issue?

2. **What do they need to do?**
   - Install and run?
   - Understand a concept?
   - Find a specific API?

3. **What do they already know?**
   - Assume competence, not omniscience
   - Link to prerequisites, don't explain them

### Phase 2: Structure for Scanning

**People scan, they don't read:**

1. **Lead with the Answer**
   - Put the most important thing first
   - Don't make readers dig for basics

2. **Use Progressive Disclosure**
   - Quick start first
   - Details for those who need them
   - Advanced topics last

3. **Make it Navigable**
   - Clear headings
   - Table of contents for long docs
   - Link between related sections

### Phase 3: Write Clearly

**Every sentence should earn its place:**

1. **Be Concise**
   - Cut filler words
   - One idea per sentence
   - Short paragraphs

2. **Be Specific**
   - Show, don't tell
   - Include examples
   - Use real values, not placeholders

3. **Be Accurate**
   - Test all code examples
   - Keep docs in sync with code
   - Date time-sensitive content

## Red Flags - STOP and Rewrite

### Structure Red Flags

```
- No quick start in first 30 seconds of reading
- Have to read everything to find anything
- Walls of text without headings
- Navigation requires scrolling through all content
- Important info buried in paragraphs
```

### Content Red Flags

```
- Comments that restate the code
- "This function does X" (what does the reader DO with it?)
- Placeholder values: "foo", "bar", "example.com"
- Outdated code examples that don't run
- Explaining prerequisites instead of linking
```

### Style Red Flags

```
- Passive voice: "The file is read by the system"
- Weasel words: "simply", "just", "obviously"
- Unnecessary jargon without explanation
- Long sentences with multiple clauses
- Inconsistent terminology
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "It's self-documenting code" | Code shows how, not why. Document the why. |
| "The README is comprehensive" | Comprehensive ≠ useful. Make it scannable. |
| "Developers can read the source" | They shouldn't have to. Document the API. |
| "We'll update docs later" | Later never comes. Docs ship with code. |
| "It's obvious" | Not to someone new. Write it down. |

## Documentation Checklist

Before approving documentation:

- [ ] **Quick start works**: Can get running in < 5 minutes
- [ ] **Examples run**: All code examples tested
- [ ] **Scannable**: Headings, lists, not walls of text
- [ ] **Complete**: Install, usage, API, troubleshooting
- [ ] **Current**: Matches the actual code
- [ ] **Linked**: Related topics cross-referenced

## README Structure

```markdown
# Project Name

One sentence: what it does and why you'd use it.

## Quick Start

Minimal steps to see it work (< 5 commands).

## Installation

How to install for real use.

## Usage

Common use cases with examples.

## API Reference

For libraries: document public API.

## Configuration

All options with defaults and examples.

## Troubleshooting

Common problems and solutions.

## Contributing

How to contribute (or link to CONTRIBUTING.md).
```

## Comment Guidelines

### DO Comment

```python
# WHY: Binary search because list is always sorted and
# we need O(log n) for real-time responsiveness
index = binary_search(sorted_users, target_id)

# BUSINESS RULE: Discount capped at 30% per legal agreement
# See: https://company.atlassian.net/browse/LEGAL-123
max_discount = min(calculated_discount, 0.30)

# TODO(jsmith): Remove after migration complete (Q2 2024)
legacy_handler()
```

### DON'T Comment

```python
# ❌ Restates the code
i = 0  # Initialize i to zero

# ❌ Should be better naming
n = u.fn + " " + u.ln  # Get user's full name
# ✅ Instead:
full_name = user.first_name + " " + user.last_name
```

## Quick Commands

```bash
# Check for broken links
npx markdown-link-check README.md

# Preview markdown
npx marked README.md > preview.html

# Lint markdown
npx markdownlint '**/*.md'
```

## References

Detailed patterns and examples in `references/`:
- `readme-templates.md` - Templates for different project types
- `api-documentation.md` - OpenAPI and docstring patterns
- `changelog-guide.md` - Keep a Changelog format

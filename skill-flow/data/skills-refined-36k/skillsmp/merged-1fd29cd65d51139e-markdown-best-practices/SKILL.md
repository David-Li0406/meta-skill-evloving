---
name: markdown-best-practices
description: Use this skill when generating or editing markdown documents to ensure compliance with formatting rules and best practices.
---

When generating or editing markdown documents, follow all markdownlint rules strictly and adhere to best practices for markdown file structure.

## Headings

- **MD001**: Heading levels increment by one (no skipping from # to ###)
- **MD002**: First heading must be h1
- **MD003**: Use consistent heading style (ATX style with `#`)
- **MD018**: No space after hash in headings: `#Heading` is wrong, `# Heading` is correct
- **MD019**: No multiple spaces after hash: `#  Heading` is wrong
- **MD020**: No space inside closed ATX headings if using them
- **MD021**: No multiple spaces inside closed ATX headings
- **MD022**: Headings must be surrounded by blank lines
- **MD023**: Headings must start at beginning of line
- **MD024**: No duplicate heading text in the same document
- **MD025**: Only one top-level h1 heading per document
- **MD026**: No trailing punctuation in headings (no periods, colons, etc.)
- **MD041**: First line should be a top-level heading

## Whitespace and Line Length

- **MD009**: No trailing spaces at end of lines
- **MD010**: No hard tabs, use spaces
- **MD012**: No multiple consecutive blank lines
- **MD027**: No multiple spaces after blockquote symbol
- **MD028**: No blank line inside blockquote
- **MD030**: Use consistent spacing after list markers (1 space)
- **MD035**: Use consistent horizontal rule style (`---`)
- **MD047**: Files must end with a single newline character

## Lists

- **MD004**: Use consistent unordered list style (`-` preferred)
- **MD005**: Consistent indentation for list items at same level
- **MD006**: Start bulleted lists at beginning of line
- **MD007**: Unordered list indentation should be consistent (2 spaces)
- **MD029**: Ordered list prefix style should be consistent (use `1.` for all)
- **MD030**: Spaces after list markers must be consistent
- **MD032**: Lists must be surrounded by blank lines

## Code Blocks

- **MD014**: Dollar signs used before commands without output shown
- **MD031**: Fenced code blocks must be surrounded by blank lines
- **MD038**: No spaces inside code span backticks: `` ` code ` `` is wrong
- **MD040**: Fenced code blocks should have a language specified
- **MD046**: Use consistent code block style (fenced with triple backticks)
- **MD048**: Use consistent code fence style (backticks ``` not tildes ~~~)

## Links and Images

- **MD011**: No reversed link syntax: `(text)[url]` is wrong, `[text](url)` is correct
- **MD033**: No inline HTML (use markdown equivalents)
- **MD034**: No bare URLs without angle brackets or link syntax
- **MD039**: No spaces inside link text: `[ text ](url)` is wrong
- **MD042**: No empty links: `[text]()` or `[](url)` are wrong
- **MD045**: Images must have alt text: `![](image.png)` is wrong

## Emphasis and Formatting

- **MD036**: No emphasis used instead of heading (don't use **bold** as section titles)
- **MD037**: No spaces inside emphasis markers: `** text **` is wrong
- **MD049**: Use consistent emphasis style (asterisks `*italic*` not underscores)
- **MD050**: Use consistent bold style (double asterisks `**bold**` not underscores)

## Structure

- **MD013**: Line length should not exceed 120 characters (except for code blocks, tables, and URLs)
- **MD043**: Required heading structure if defined
- **MD044**: Proper case for proper names if defined

## Quick Reference Template

```markdown
# Document Title

Brief introduction paragraph.

## Section Heading

Regular paragraph text with [links](https://example.com) and `inline code`.

- List item one
- List item two
- List item three

### Subsection

1. Ordered item
1. Ordered item
1. Ordered item

```python
# Code block with language
def example():
    return True
```

## Another Section

> Blockquote text here.

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

---

Final section content.
```

## Common Mistakes to Avoid

1. Missing blank lines around headings, lists, and code blocks
2. Inconsistent list markers (mixing `-`, `*`, `+`)
3. Trailing whitespace
4. Multiple consecutive blank lines
5. Missing language identifier on fenced code blocks
6. Skipping heading levels
7. Bare URLs without proper link syntax
8. Missing alt text on images
9. Trailing punctuation on headings
10. Not ending file with newline
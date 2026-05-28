---
name: markdown-best-practices
description: Use this skill when you need to ensure compliance with markdown formatting rules and best practices for creating markdown documents.
---

# Skill body

When generating or editing markdown documents, follow these rules and best practices:

## Headings

- **MD001**: Heading levels must increment by one (no skipping from # to ###).
- **MD002**: The first heading must be h1.
- **MD003**: Use a consistent heading style (ATX style with `#`).
- **MD018**: No space after hash in headings: `#Heading` is incorrect, `# Heading` is correct.
- **MD019**: No multiple spaces after hash: `#  Heading` is incorrect.
- **MD020**: No space inside closed ATX headings if using them.
- **MD021**: No multiple spaces inside closed ATX headings.
- **MD022**: Headings must be surrounded by blank lines.
- **MD023**: Headings must start at the beginning of the line.
- **MD024**: No duplicate heading text in the same document.
- **MD025**: Only one top-level h1 heading per document.
- **MD026**: No trailing punctuation in headings (no periods, colons, etc.).
- **MD041**: The first line should be a top-level heading.

## Whitespace and Line Length

- **MD009**: No trailing spaces at the end of lines.
- **MD010**: No hard tabs; use spaces instead.
- **MD012**: No multiple consecutive blank lines.
- **MD027**: No multiple spaces after blockquote symbols.
- **MD028**: No blank line inside blockquotes.
- **MD030**: Use consistent spacing after list markers (1 space).
- **MD035**: Use a consistent horizontal rule style (`---`).
- **MD047**: Files must end with a single newline character.

## Lists

- **MD004**: Use a consistent unordered list style (`-` preferred).
- **MD005**: Ensure consistent indentation for list items at the same level.
- **MD006**: Start bulleted lists at the beginning of the line.
- **MD007**: Unordered list indentation should be consistent (2 spaces).
- **MD029**: Ordered list prefix style should be consistent (use `1.` for all).
- **MD030**: Spaces after list markers must be consistent.
- **MD032**: Lists must be surrounded by blank lines.

## Code Blocks

- **MD014**: Use dollar signs before commands without output shown.
- **MD031**: Fenced code blocks must be surrounded by blank lines.
- **MD038**: No spaces inside code span backticks: `` ` code ` `` is incorrect.
- **MD040**: Fenced code blocks should have a language specified.
- **MD046**: Use a consistent code block style (fenced with triple backticks).
- **MD048**: Use a consistent code fence style (backticks ``` not tildes ~~~).

## Links and Images

- **MD011**: No reversed link syntax: `(text)[url]`.
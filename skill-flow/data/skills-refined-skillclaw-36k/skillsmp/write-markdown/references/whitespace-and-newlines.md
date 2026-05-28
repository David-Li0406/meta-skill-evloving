# Whitespace and newlines

Keep whitespace tidy to reduce noise and prevent formatting surprises.

## MD009 - Trailing spaces

Do not leave trailing spaces at the end of lines.
Trailing spaces can change rendering and create noisy diffs.

Bad:

```markdown
Line with trailing spaces␠␠
```

Good:

```markdown
Line with no trailing spaces
```

## MD010 - Hard tabs

Avoid hard tab characters and use spaces instead.

Bad:

```markdown
- <TAB>Tabbed indentation
```

Good:

```markdown
- Spaced indentation
```

## MD012 - Multiple consecutive blank lines

Avoid multiple consecutive blank lines.
Use a single blank line between blocks.

Bad:

```markdown
Paragraph.


Next paragraph.
```

Good:

```markdown
Paragraph.

Next paragraph.
```

## MD047 - Files should end with a single newline character

Ensure each Markdown file ends with a single newline.
Do not omit the final newline or add extra blank lines at the end.

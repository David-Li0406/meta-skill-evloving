# Lists and indentation

Use consistent markers, indentation, and spacing for lists.

## MD004 - Unordered list style

Use a consistent marker for unordered lists.
A common choice is `-`.

Bad:

```markdown
- One
* Two
- Three
```

Good:

```markdown
- One
- Two
- Three
```

## MD005 - Inconsistent indentation for list items at the same level

Keep items aligned at the same nesting level.

Bad:

```markdown
- Item
  - Nested
 - Misaligned
```

Good:

```markdown
- Item
  - Nested
- Aligned
```

## MD006 - Consider starting bulleted lists at the beginning of the line

Start top-level bullet lists at column 1.
Indented lists may be parsed differently or become less readable.

Bad:

```markdown
  - Indented bullet
  - Indented bullet
```

Good:

```markdown
- Bullet
- Bullet
```

## MD007 - Unordered list indentation

Indent nested lists consistently.
A common default is two spaces for each nested level.

Bad:

```markdown
- Parent
   - Child
```

Good:

```markdown
- Parent
  - Child
```

## MD029 - Ordered list item prefix

Use a consistent style for ordered list prefixes.
Avoid mixing numbering styles.

Bad:

```markdown
1. One
2. Two
1. Three
```

Good:

```markdown
1. One
2. Two
3. Three
```

## MD030 - Spaces after list markers

Use consistent spacing after list markers.

Bad:

```markdown
-  Two spaces
1.  Two spaces
```

Good:

```markdown
- One space
1. One space
```

## MD032 - Lists should be surrounded by blank lines

Put blank lines before and after lists when mixing with paragraphs.

Bad:

```markdown
Intro text
- Item
- Item
Outro text
```

Good:

```markdown
Intro text

- Item
- Item

Outro text
```

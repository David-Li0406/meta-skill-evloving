# Tables

Keep tables consistent and readable.

## MD055 - Table pipe style

Use consistent leading and trailing pipes for each row.

Bad:

```markdown
| A | B |
| --- | --- |
C | D |
```

Good:

```markdown
| A | B |
| --- | --- |
| C | D |
```

## MD056 - Table column count

Ensure every row has the same number of columns.

Bad:

```markdown
| A | B |
| --- | --- |
| C |
```

Good:

```markdown
| A | B |
| --- | --- |
| C | D |
```

## MD058 - Tables should be surrounded by blank lines

Surround tables with blank lines when mixed with other blocks.

Bad:

```markdown
Text
| A | B |
| --- | --- |
| C | D |
More text
```

Good:

```markdown
Text

| A | B |
| --- | --- |
| C | D |

More text
```

## MD060 - Table column style

Keep table cell padding and delimiter formatting consistent.

Bad:

```markdown
|A| B|
|---| --- |
| C|D |
```

Good:

```markdown
| A | B |
| --- | --- |
| C | D |
```

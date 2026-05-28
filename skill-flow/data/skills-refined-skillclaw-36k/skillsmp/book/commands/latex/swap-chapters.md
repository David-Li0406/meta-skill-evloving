# Swap Chapters (LaTeX)

LaTeX-specific implementation for swapping two chapters.

## Steps

### 1. Use Temporary Names to Avoid Conflicts

```
ch02-<slug-a>/ -> ch02-<slug-a>.tmp/
ch05-<slug-b>/ -> ch02-<slug-b>/
ch02-<slug-a>.tmp/ -> ch05-<slug-a>/
```

### 2. Rename Chapter Files

```
ch02-<slug-a>.tex -> ch05-<slug-a>.tex
ch05-<slug-b>.tex -> ch02-<slug-b>.tex
```

### 3. Update Labels (if using numeric labels)

Usually labels use slugs, so no update needed:
```latex
\label{ch:<slug>}  % stays the same
```

### 4. Update Part Aggregator

Reorder `\subfile{}` lines to match new numeric order:

```latex
% Before
\subfile{ch02-<slug-a>/ch02-<slug-a>.tex}
...
\subfile{ch05-<slug-b>/ch05-<slug-b>.tex}

% After
\subfile{ch02-<slug-b>/ch02-<slug-b>.tex}
...
\subfile{ch05-<slug-a>/ch05-<slug-a>.tex}
```

## Important Notes

- The `\documentclass` path stays the same (`../../../main.tex`)
- Section files inside chapters do NOT need updates

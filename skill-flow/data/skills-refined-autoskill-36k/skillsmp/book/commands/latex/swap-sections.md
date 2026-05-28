# Swap Sections (LaTeX)

LaTeX-specific implementation for swapping two sections.

## Steps

### 1. Use Temporary Names to Avoid Conflicts

```
sec02-<slug-a>.tex -> sec02-<slug-a>.tex.tmp
sec05-<slug-b>.tex -> sec02-<slug-b>.tex
sec02-<slug-a>.tex.tmp -> sec05-<slug-a>.tex
```

### 2. Update Labels (if using numeric labels)

Usually labels use slugs, so no update needed:
```latex
\label{sec:<chapter>:<slug>}  % stays the same
```

### 3. Update Chapter Aggregator

Reorder `\subfile{}` lines to match new numeric order:

```latex
% Before
\subfile{sec02-<slug-a>.tex}
...
\subfile{sec05-<slug-b>.tex}

% After
\subfile{sec02-<slug-b>.tex}
...
\subfile{sec05-<slug-a>.tex}
```

## Important Notes

- The `\documentclass` path stays the same (`../../../main.tex`)
- The `\graphicspath` stays the same (`\subfix{../figures/}`)

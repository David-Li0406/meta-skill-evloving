# Rename Section (LaTeX)

LaTeX-specific implementation for renaming a section.

## Steps

### 1. Rename File (if slug changes)
```
sec<NN>-<old-slug>.tex -> sec<NN>-<new-slug>.tex
```

### 2. Update Section File Content

Label:
```latex
\label{sec:<chapter>:<old-slug>}
```
to:
```latex
\label{sec:<chapter>:<new-slug>}
```

Title (if changed):
```latex
\section{<Old Title>}
```
to:
```latex
\section{<New Title>}
```

### 3. Update Chapter Aggregator

In `ch<XX>-<chapter-slug>.tex`:
```latex
\subfile{sec<NN>-<old-slug>.tex}
```
to:
```latex
\subfile{sec<NN>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{sec:<chapter>:<old-slug>}` -> `\ref{sec:<chapter>:<new-slug>}`
- `\hyperref[sec:<chapter>:<old-slug>]` -> `\hyperref[sec:<chapter>:<new-slug>]`

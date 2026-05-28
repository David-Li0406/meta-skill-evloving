# Rename Chapter (LaTeX)

LaTeX-specific implementation for renaming a chapter.

## Steps

### 1. Rename Folder (if slug changes)
```
ch<XX>-<old-slug>/ -> ch<XX>-<new-slug>/
```

### 2. Rename Chapter File
```
ch<XX>-<old-slug>.tex -> ch<XX>-<new-slug>.tex
```

### 3. Update Chapter File Content

Label:
```latex
\label{ch:<old-slug>}
```
to:
```latex
\label{ch:<new-slug>}
```

Title (if changed):
```latex
\chapter{<Old Title>}
```
to:
```latex
\chapter{<New Title>}
```

### 4. Update Part Aggregator

In `part<NN>.tex`:
```latex
\subfile{ch<XX>-<old-slug>/ch<XX>-<old-slug>.tex}
```
to:
```latex
\subfile{ch<XX>-<new-slug>/ch<XX>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{ch:<old-slug>}` -> `\ref{ch:<new-slug>}`
- `\hyperref[ch:<old-slug>]` -> `\hyperref[ch:<new-slug>]`

## Files NOT Needing Updates

- Section files (they use relative `\subfile{}` without folder path)

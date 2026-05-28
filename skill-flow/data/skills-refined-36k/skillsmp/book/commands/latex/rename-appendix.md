# Rename Appendix (LaTeX)

LaTeX-specific implementation for renaming an appendix.

## Steps

### 1. Rename Folder (if slug changes)
```
app<NN>-<old-slug>/ -> app<NN>-<new-slug>/
```

### 2. Rename Appendix File
```
app<NN>-<old-slug>.tex -> app<NN>-<new-slug>.tex
```

### 3. Update Appendix File Content

Label:
```latex
\label{app:<old-slug>}
```
to:
```latex
\label{app:<new-slug>}
```

Title (if changed):
```latex
\chapter{<Old Title>}
```
to:
```latex
\chapter{<New Title>}
```

### 4. Update Backmatter Aggregator

In `backmatter.tex`:
```latex
\subfile{app<NN>-<old-slug>/app<NN>-<old-slug>.tex}
```
to:
```latex
\subfile{app<NN>-<new-slug>/app<NN>-<new-slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{app:<old-slug>}` -> `\ref{app:<new-slug>}`
- `\hyperref[app:<old-slug>]` -> `\hyperref[app:<new-slug>]`

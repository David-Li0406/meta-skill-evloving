# Rename Part (LaTeX)

LaTeX-specific implementation for renaming a part.

## Steps

### 1. Rename Folder (if slug changes)
```
latex/200-bodymatter/part<NN>-<old-slug>/
-> latex/200-bodymatter/part<NN>-<new-slug>/
```

### 2. Aggregator file name stays same
`part<NN>.tex` - only the folder name changes

### 3. Update bodymatter.tex

Change path:
```latex
\subfile{part<NN>-<old-slug>/part<NN>.tex}
```
to:
```latex
\subfile{part<NN>-<new-slug>/part<NN>.tex}
```

If title changes:
```latex
\part{<Old Title>}
```
to:
```latex
\part{<New Title>}
```

## Files NOT Needing Updates

- Child chapter files (they reference `../../main.tex`, not the part folder name)
- Section files (they reference `../../../main.tex`)

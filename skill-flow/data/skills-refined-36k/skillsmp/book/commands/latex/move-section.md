# Move Section (LaTeX)

LaTeX-specific implementation for moving a section between chapters.

## Steps

### 1. Determine Target Section Number

Find next available section number in target chapter.

### 2. Move File

```
latex/.../ch<SRC>-<src-chapter>/sec<OLD>-<slug>.tex
-> latex/.../ch<TGT>-<tgt-chapter>/sec<NEW>-<slug>.tex
```

### 3. Update Section File

Update label:
```latex
\label{sec:<src-chapter>:<slug>}
```
to:
```latex
\label{sec:<tgt-chapter>:<slug>}
```

The `\documentclass` path stays same if depth is same (`../../../main.tex`).

Update `\graphicspath` if moving between chapters:
```latex
\graphicspath{{\subfix{../figures/}}}
```
(stays same - relative to section file)

### 4. Update Source Chapter Aggregator

Remove from `ch<SRC>-<src-chapter>.tex`:
```latex
\subfile{sec<OLD>-<slug>.tex}
```

### 5. Update Target Chapter Aggregator

Add to `ch<TGT>-<tgt-chapter>.tex` before `\ifSubfilesClassLoaded`:
```latex
\subfile{sec<NEW>-<slug>.tex}
```

## Cross-Reference Updates

Search entire project and update:
- `\ref{sec:<src-chapter>:<slug>}` -> `\ref{sec:<tgt-chapter>:<slug>}`

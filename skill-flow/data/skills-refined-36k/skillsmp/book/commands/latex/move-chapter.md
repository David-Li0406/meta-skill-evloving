# Move Chapter (LaTeX)

LaTeX-specific implementation for moving a chapter between parts.

## Steps

### 1. Determine Target Numbering

| Source Part | Target Part | Action |
|-------------|-------------|--------|
| part01 (roman) | part02+ (arabic) | chi -> ch01 |
| part02+ (arabic) | part01 (roman) | ch01 -> chi |
| Same scheme | Same scheme | Keep or renumber |

### 2. Move Folder

```
latex/200-bodymatter/part<SRC>-<src-slug>/ch<OLD>-<chapter-slug>/
-> latex/200-bodymatter/part<TGT>-<tgt-slug>/ch<NEW>-<chapter-slug>/
```

### 3. Rename Files (if numbering scheme changes)

```
ch<OLD>-<chapter-slug>.tex -> ch<NEW>-<chapter-slug>.tex
```

### 4. Update Chapter File

`\documentclass` path stays same (`../../../main.tex`).

### 5. Update Source Part Aggregator

Remove from `part<SRC>.tex`:
```latex
\subfile{ch<OLD>-<chapter-slug>/ch<OLD>-<chapter-slug>.tex}
```

### 6. Update Target Part Aggregator

Add to `part<TGT>.tex`:
```latex
\subfile{ch<NEW>-<chapter-slug>/ch<NEW>-<chapter-slug>.tex}
```

## Path Reference

Chapter files always use `../../../main.tex` regardless of which part they're in.

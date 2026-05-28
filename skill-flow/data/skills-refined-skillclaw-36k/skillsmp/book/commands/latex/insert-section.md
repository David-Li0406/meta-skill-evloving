# Insert Section (LaTeX)

LaTeX-specific implementation for inserting a section.

## Renaming Steps

For each section from highest to insertion point (in reverse order):

1. **Rename file:**
   ```
   sec<NN>-<slug>.tex -> sec<NN+1>-<slug>.tex
   ```

2. **Labels using slugs do NOT need updates:**
   ```latex
   \label{sec:<chapter>:<slug>}  % stays the same
   ```

## Files to Create

Same as `new-section.md` - create at the insertion position.

## Chapter Aggregator Update

In `ch<XX>-<chapter-slug>.tex`:

1. Update all `\subfile{sec<NN>-...}` paths for renumbered sections
2. Insert new entry at correct position (before `\ifSubfilesClassLoaded`)

### Example

Before:
```latex
\subfile{sec01-intro.tex}
\subfile{sec02-methods.tex}
\subfile{sec03-results.tex}
```

Insert section 2 -> after renumbering:
```latex
\subfile{sec01-intro.tex}
\subfile{sec02-background.tex}      % NEW
\subfile{sec03-methods.tex}         % was sec02
\subfile{sec04-results.tex}         % was sec03
```

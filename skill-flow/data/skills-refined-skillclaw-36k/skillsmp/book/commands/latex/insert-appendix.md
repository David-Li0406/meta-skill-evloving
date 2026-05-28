# Insert Appendix (LaTeX)

LaTeX-specific implementation for inserting an appendix.

## Renaming Steps

For each appendix from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   app<NN>-<slug>/ -> app<NN+1>-<slug>/
   ```

2. **Rename appendix file:**
   ```
   app<NN>-<slug>.tex -> app<NN+1>-<slug>.tex
   ```

3. **documentclass path stays the same** (`../../main.tex`)

## Files to Create

Same as `new-appendix.md` - create at the insertion position.

## Backmatter Aggregator Update

In `latex/300-backmatter/backmatter.tex`:

1. Update all `\subfile{app<NN>-...}` paths for renumbered appendices
2. Insert new entry at correct position

### Example

Before:
```latex
\subfile{app01-formulas/app01-formulas.tex}
\subfile{app02-glossary/app02-glossary.tex}
```

Insert appendix 2 -> after renumbering:
```latex
\subfile{app01-formulas/app01-formulas.tex}
\subfile{app02-tables/app02-tables.tex}           % NEW
\subfile{app03-glossary/app03-glossary.tex}       % was app02
```

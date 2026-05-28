# Insert Part (LaTeX)

LaTeX-specific implementation for inserting a part.

## Renaming Steps

For each part from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   part<NN>-<slug>/ -> part<NN+1>-<slug>/
   ```

2. **Rename aggregator file:**
   ```
   part<NN>.tex -> part<NN+1>.tex
   ```

3. **documentclass path stays the same** (`../../main.tex`)

## Files to Create

Same as `new-part.md` - create at the insertion position.

## Aggregator Update

In `latex/200-bodymatter/bodymatter.tex`:

1. Update all `\subfile{part<NN>-...}` paths for renumbered parts
2. Insert new entry at correct position

## Note on Child Files

Chapter files inside parts do NOT need path updates - they reference `../../main.tex` (relative to main, not to part folder name).

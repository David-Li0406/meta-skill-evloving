# Insert Chapter (LaTeX)

LaTeX-specific implementation for inserting a chapter.

## Renaming Steps

For each chapter from highest to insertion point (in reverse order):

1. **Rename folder:**
   ```
   ch<XX>-<slug>/ -> ch<XX+1>-<slug>/
   ```

2. **Rename chapter file:**
   ```
   ch<XX>-<slug>.tex -> ch<XX+1>-<slug>.tex
   ```

3. **Labels using slugs do NOT need updates:**
   ```latex
   \label{ch:<slug>}  % stays the same
   ```

4. **Section files do NOT need path updates** (same relative depth)

## Files to Create

Same as `new-chapter.md` - create at the insertion position.

## Part Aggregator Update

In `part<NN>.tex`:

1. Update all `\subfile{ch<XX>-...}` paths for renumbered chapters
2. Insert new entry at correct position

## Cross-Reference Check

If any labels use numeric prefixes, search and update:
- `\ref{ch:XX}` references
- `\hyperref[ch:XX]` references

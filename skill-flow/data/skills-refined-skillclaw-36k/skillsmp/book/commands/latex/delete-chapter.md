# Delete Chapter (LaTeX)

LaTeX-specific implementation for deleting a chapter.

## Files to Delete

Remove entire folder recursively:
```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<slug>/
```

This includes:
- Chapter file
- All section files
- figures/ folder
- Any other contents

## Part Aggregator Update

In `part<NN>.tex`, remove:
```latex
% Kapittel <N> - <Title>
\subfile{ch<XX>-<slug>/ch<XX>-<slug>.tex}
```

## Post-Deletion Check

Search for broken references:
- `\ref{ch:<slug>}`
- `\ref{sec:<slug>:*}`
- `\hyperref[ch:<slug>]`

## Note

- Deleting does NOT automatically renumber remaining chapters
- Gaps in numbering are allowed

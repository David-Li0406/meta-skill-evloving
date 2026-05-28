# Delete Appendix (LaTeX)

LaTeX-specific implementation for deleting an appendix.

## Files to Delete

Remove entire folder recursively:
```
latex/300-backmatter/app<NN>-<slug>/
```

This includes:
- Appendix file
- figures/ folder
- Any other contents

## Backmatter Aggregator Update

In `latex/300-backmatter/backmatter.tex`, remove:
```latex
\subfile{app<NN>-<slug>/app<NN>-<slug>.tex}
```

## Post-Deletion Check

Search for broken references:
- `\ref{app:<slug>}`
- `\hyperref[app:<slug>]`

## Note

- Deleting does NOT automatically renumber remaining appendices
- Gaps in numbering are allowed

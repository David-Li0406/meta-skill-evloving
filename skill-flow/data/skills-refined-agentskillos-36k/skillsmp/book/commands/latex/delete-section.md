# Delete Section (LaTeX)

LaTeX-specific implementation for deleting a section.

## Files to Delete

```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/sec<NN>-<slug>.tex
```

## Chapter Aggregator Update

In `ch<XX>-<chapter-slug>.tex`, remove:
```latex
\subfile{sec<NN>-<slug>.tex}
```

## Post-Deletion Check

Search for broken references:
- `\ref{sec:<chapter>:<slug>}`
- `\hyperref[sec:<chapter>:<slug>]`

## Note

- Deleting does NOT automatically renumber remaining sections
- Gaps in numbering are allowed

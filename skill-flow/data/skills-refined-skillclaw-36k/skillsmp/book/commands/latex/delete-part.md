# Delete Part (LaTeX)

LaTeX-specific implementation for deleting a part.

## Files to Delete

Remove entire folder recursively:
```
latex/200-bodymatter/part<NN>-<slug>/
```

## Aggregator Update

In `latex/200-bodymatter/bodymatter.tex`, remove:

```latex
% ============ DEL <N>: <TITLE UPPERCASE> ============
\part{<Title>}
\setcounter{chapter}{0}
\renewcommand{\thechapter}{\arabic{chapter}}
\subfile{part<NN>-<slug>/part<NN>.tex}
```

## Note

- Deleting does NOT automatically renumber remaining parts
- Gaps in numbering are allowed

# New Part (LaTeX)

LaTeX-specific implementation for creating a new part.

## Files to Create

### 1. Folder
```
latex/200-bodymatter/part<NN>-<slug>/
```

### 2. Part Aggregator
`latex/200-bodymatter/part<NN>-<slug>/part<NN>.tex`

```latex
\documentclass[../../main.tex]{subfiles}
\begin{document}

% Add chapters here using \subfile{chXX-name/chXX-name.tex}

\end{document}
```

## Aggregator Update

Add to `latex/200-bodymatter/bodymatter.tex` at the end:

```latex
% ============ DEL <N>: <TITLE UPPERCASE> ============
\part{<Title>}
\setcounter{chapter}{0}
\renewcommand{\thechapter}{\arabic{chapter}}
\subfile{part<NN>-<slug>/part<NN>.tex}
```

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| `200-bodymatter/partNN-*/partNN.tex` | `../../main.tex` |

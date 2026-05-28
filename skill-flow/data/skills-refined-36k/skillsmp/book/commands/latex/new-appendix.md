# New Appendix (LaTeX)

LaTeX-specific implementation for creating a new appendix.

## Files to Create

### 1. Appendix Folder
```
latex/300-backmatter/app<NN>-<slug>/
```

### 2. Appendix File
`app<NN>-<slug>/app<NN>-<slug>.tex`

```latex
\documentclass[../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{<Appendix Title>}
\label{app:<slug>}

% Appendix content

\end{document}
```

### 3. Figures Folder (optional)
```
latex/300-backmatter/app<NN>-<slug>/figures/
```

## Backmatter Aggregator Update

Add to `latex/300-backmatter/backmatter.tex` after existing appendices:

```latex
\subfile{app<NN>-<slug>/app<NN>-<slug>.tex}
```

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| `300-backmatter/appNN-*/appNN-*.tex` | `../../main.tex` |

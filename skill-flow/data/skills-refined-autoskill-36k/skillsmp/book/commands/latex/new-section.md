# New Section (LaTeX)

LaTeX-specific implementation for creating a new section.

## Files to Create

### Section File
`ch<XX>-<chapter-slug>/sec<NN>-<section-slug>.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{../figures/}}}
\begin{document}

\section{<Section Title>}
\label{sec:<chapter-slug>:<section-slug>}

% Section content

\end{document}
```

## Chapter Aggregator Update

Add to `ch<XX>-<chapter-slug>.tex` before `\ifSubfilesClassLoaded`:

```latex
\subfile{sec<NN>-<section-slug>.tex}
```

## Path Reference

| Location | documentclass path | graphicspath |
|----------|-------------------|--------------|
| Section file | `../../../main.tex` | `\subfix{../figures/}` |

## Label Convention

`sec:<chapter-slug>:<section-slug>`

Example: `sec:transport-optimization:methodology`

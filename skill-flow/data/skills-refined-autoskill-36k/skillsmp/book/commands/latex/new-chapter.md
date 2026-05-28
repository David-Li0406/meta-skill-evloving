# New Chapter (LaTeX)

LaTeX-specific implementation for creating a new chapter.

## Files to Create

### 1. Chapter Folder
```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/
```

### 2. Figures Folder
```
latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/figures/
```

### 3. Chapter Aggregator
`ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{<Chapter Title>}
\label{ch:<chapter-slug>}

% Chapter introduction

% Add sections here using \subfile{secNN-name.tex}

\ifSubfilesClassLoaded{%
  \printbibliography
}{}

\end{document}
```

## Part Aggregator Update

Add to `part<NN>.tex`:

```latex
% Kapittel <N> - <Title>
\subfile{ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex}
```

## Numbering Schemes

| Part | Prefix | Examples |
|------|--------|----------|
| part01 | `ch<roman>` | chi, chii, chiii, chiv, chv |
| part02+ | `ch<NN>` | ch01, ch02, ch10, ch11 |

## Path Reference

| Location | documentclass path |
|----------|-------------------|
| Chapter file | `../../../main.tex` |

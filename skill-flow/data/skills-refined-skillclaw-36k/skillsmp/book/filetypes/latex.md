# LaTeX Book Implementation Guide

This guide provides complete templates for implementing the book structure using LaTeX with the `subfiles` package for standalone compilation.

---

## Prerequisites

Required LaTeX packages:
- `subfiles` - For standalone compilation of chapters/sections
- `biblatex` with `biber` backend - For bibliography management
- `graphicx` - For images
- Standard book packages (amsmath, hyperref, etc.)

---

## Root Files

### main.tex

```latex
\documentclass[12pt,a4paper]{book}

\input{localsettings.tex}

\begin{document}

% ---------------- FRONT MATTER -----------------
\subfile{100-frontmatter/frontmatter.tex}

% ---------------- MAIN CONTENT -----------------
\mainmatter
\subfile{200-bodymatter/bodymatter.tex}

% ---------------- BACK MATTER -----------------
\subfile{300-backmatter/backmatter.tex}

\end{document}
```

### localsettings.tex (Preamble)

```latex
% -------------------------------------------------------
%            PACKAGES AND BASIC SETUP
% -------------------------------------------------------

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[norsk]{babel}      % or [english] for English books

\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{import}
\usepackage{subfiles}          % IMPORTANT: Load early for \subfix to work
\usepackage{float}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage[figuresright]{rotating}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{hyperref}
\usepackage{csquotes}
\usepackage{titlesec}
\usepackage{makeidx}
\usepackage{indentfirst}
\usepackage{enumitem}
\usepackage{calc}
\usepackage{needspace}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{tcolorbox}
\tcbuselibrary{breakable}

% -------------------------------------------------------
%            CUSTOM ENVIRONMENTS (Optional)
% -------------------------------------------------------

% Example box (breakable for long examples)
\newtcolorbox{eksempel}[2][]{
  breakable,
  colback=gray!5,
  colframe=gray!50,
  fonttitle=\bfseries,
  title={Example: #2},
  #1
}

% Definition box (blue left border)
\newtcolorbox{definisjon}[2][]{
  breakable,
  colback=white,
  colframe=blue!60,
  leftrule=4pt,
  rightrule=0pt,
  toprule=0pt,
  bottomrule=0pt,
  fonttitle=\bfseries,
  title={Definition: #2},
  #1
}

% -------------------------------------------------------
%            CODE LISTINGS (Optional)
% -------------------------------------------------------

\lstset{
  language=Python,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  commentstyle=\color{gray},
  stringstyle=\color{red},
  numbers=left,
  numberstyle=\tiny\color{gray},
  numbersep=5pt,
  breaklines=true,
  frame=single,
  captionpos=b
}

% -------------------------------------------------------
%            BIBLIOGRAPHY
% -------------------------------------------------------

\usepackage[backend=biber, style=apa, sorting=nyt]{biblatex}

% IMPORTANT: Use \subfix for bibliography path
\addbibresource{\subfix{bib/references.bib}}

% -------------------------------------------------------
%            LAYOUT
% -------------------------------------------------------

\geometry{margin=25mm}
\onehalfspacing

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue
}

\titleformat{\chapter}
  {\normalfont\LARGE\bfseries}{\thechapter}{1em}{}

% -------------------------------------------------------
%            INDEX
% -------------------------------------------------------

\makeindex
```

---

## Path Reference Guide

The `subfiles` package requires correct relative paths to `main.tex`. Use this guide:

| File Location | Path to main.tex |
|---------------|------------------|
| `100-frontmatter/*.tex` | `../main.tex` |
| `200-bodymatter/bodymatter.tex` | `../main.tex` |
| `200-bodymatter/partNN/*.tex` | `../../main.tex` |
| `200-bodymatter/partNN/chXX/*.tex` (chapter) | `../../../main.tex` |
| `200-bodymatter/partNN/chXX/secXX.tex` (section) | `../../../main.tex` |
| `300-backmatter/*.tex` | `../main.tex` |
| `300-backmatter/appNN/*.tex` | `../../main.tex` |

### graphicspath for Figures

| File Type | graphicspath Setting |
|-----------|---------------------|
| Chapter file | `\graphicspath{{\subfix{./figures/}}}` |
| Section file | `\graphicspath{{\subfix{../figures/}}}` |

---

## Frontmatter Templates

### 100-frontmatter/frontmatter.tex (Aggregator)

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\subfile{100-frontpage.tex}
\subfile{110-preface.tex}
\subfile{120-about.tex}
\subfile{130-acknowledgements.tex}
\subfile{140-toc.tex}

\end{document}
```

### 100-frontmatter/100-frontpage.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\begin{titlepage}
    \centering
    \vspace*{5cm}

    {\LARGE\bfseries [PROMPT: Book Title]\par}
    \vspace{2cm}

    {\large [PROMPT: Subtitle or description]}
    \vspace{2.5cm}

    {\Large [PROMPT: Author name(s)]\par}
    \vspace{3cm}

    {\large Compilation date: \today\par}

    \vfill
\end{titlepage}

\end{document}
```

### 100-frontmatter/110-preface.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\chapter*{Preface}
\addcontentsline{toc}{chapter}{Preface}

% [PROMPT: Write a preface explaining:]
% - The motivation for writing this book
% - Who the intended audience is
% - How the book is organized
% - Any acknowledgements or thanks
% - Date and location of writing

\end{document}
```

### 100-frontmatter/120-about.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\chapter*{About This Book}
\addcontentsline{toc}{chapter}{About This Book}

% [PROMPT: Describe:]
% - What topics the book covers
% - The structure and organization
% - How to read/use the book effectively
% - Prerequisites or background knowledge needed
% - Any conventions used in the book

\end{document}
```

### 100-frontmatter/130-acknowledgements.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\chapter*{Acknowledgements}
\addcontentsline{toc}{chapter}{Acknowledgements}

% [PROMPT: Thank:]
% - Colleagues, mentors, or collaborators
% - Institutions or funding sources
% - Family and friends
% - Anyone who contributed to the book

\end{document}
```

### 100-frontmatter/140-toc.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\tableofcontents

\end{document}
```

---

## Bodymatter Templates

### 200-bodymatter/bodymatter.tex (Aggregator with Part Control)

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

% ============ PART 1: INTRODUCTION ============
\part{[PROMPT: Part 1 Title]}
\renewcommand{\thechapter}{\roman{chapter}}   % Roman numerals for intro
\subfile{part01-name/part01.tex}

% ============ PART 2: MAIN CONTENT ============
\part{[PROMPT: Part 2 Title]}
\setcounter{chapter}{0}                        % Reset chapter counter
\renewcommand{\thechapter}{\arabic{chapter}}  % Arabic numerals for main
\subfile{part02-name/part02.tex}

% Add more parts as needed...

\end{document}
```

### 200-bodymatter/partNN-name/partNN.tex (Part Aggregator)

```latex
\documentclass[../../main.tex]{subfiles}
\begin{document}

% Chapter 1
\subfile{ch01-name/ch01-name.tex}

% Chapter 2
\subfile{ch02-name/ch02-name.tex}

% Add more chapters...

\end{document}
```

### Chapter File Template

`200-bodymatter/partNN-name/chXX-name/chXX-name.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{[PROMPT: Chapter Title]}
\label{ch:chapter-slug}

% [PROMPT: Chapter introduction - 2-3 sentences describing what this chapter covers]

\begin{itemize}
  \item [PROMPT: Key topic 1]
  \item [PROMPT: Key topic 2]
  \item [PROMPT: Key topic 3]
\end{itemize}

\subfile{sec01-name.tex}
\subfile{sec02-name.tex}
\subfile{sec03-name.tex}
% Add more sections...

\ifSubfilesClassLoaded{%
  \printbibliography
}{}

\end{document}
```

### Section File Template

`200-bodymatter/partNN-name/chXX-name/secYY-name.tex`

```latex
\documentclass[../../../main.tex]{subfiles}
\graphicspath{{\subfix{../figures/}}}
\begin{document}

\section{[PROMPT: Section Title]}

% [PROMPT: Section content]

\end{document}
```

---

## Backmatter Templates

### 300-backmatter/backmatter.tex (Aggregator)

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\appendix

% Appendices
\subfile{app01-name/app01-name.tex}
\subfile{app02-name/app02-name.tex}

% Bibliography
\subfile{100-bibliography.tex}

% Index
\subfile{110-index.tex}

\end{document}
```

### 300-backmatter/100-bibliography.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\printbibliography[heading=bibintoc]

\end{document}
```

### 300-backmatter/110-index.tex

```latex
\documentclass[../main.tex]{subfiles}
\begin{document}

\printindex

\end{document}
```

### Appendix Template

`300-backmatter/appNN-name/appNN-name.tex`

```latex
\documentclass[../../main.tex]{subfiles}
\graphicspath{{\subfix{./figures/}}}
\begin{document}

\chapter{[PROMPT: Appendix Title]}
\label{app:appendix-slug}

% [PROMPT: Appendix content - supplementary material, reference tables, etc.]

\end{document}
```

---

## Bibliography

### bib/references.bib

```bibtex
% [PROMPT: Add bibliography entries in BibTeX format]

@book{author2024,
  author    = {Author, First},
  title     = {Book Title},
  year      = {2024},
  publisher = {Publisher Name},
  address   = {City}
}

@article{researcher2024,
  author  = {Researcher, A. and Colleague, B.},
  title   = {Article Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {2},
  pages   = {100--120}
}
```

---

## Key Implementation Details

### 1. Standalone Compilation with Bibliography

Each chapter can be compiled standalone with its own bibliography. The pattern:

```latex
\ifSubfilesClassLoaded{%
  \printbibliography
}{}
```

This prints the bibliography ONLY when compiling the chapter alone (not when included in main.tex).

**Note:** biblatex automatically includes only cited references, not all entries in the .bib file.

### 2. The \subfix Macro

`\subfix{}` resolves paths relative to the currently compiling file. Use it for:
- `\graphicspath{{\subfix{./figures/}}}`
- `\addbibresource{\subfix{bib/references.bib}}`

### 3. Package Load Order

**Critical:** Load `subfiles` package BEFORE `\addbibresource` so that `\subfix` is defined when the bibliography path is processed.

---

## Compilation

### Full Book

```bash
cd latex/
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

### Single Chapter (Standalone)

```bash
cd latex/200-bodymatter/part02-omrader/ch01-name/
pdflatex ch01-name.tex
biber ch01-name
pdflatex ch01-name.tex
```

### Single Section (Standalone)

```bash
cd latex/200-bodymatter/part02-omrader/ch01-name/
pdflatex sec01-name.tex
```

---

## Verification Checklist

After setup, verify:

1. [ ] `pdflatex main.tex` compiles without errors
2. [ ] `biber main` processes bibliography
3. [ ] Table of contents shows all chapters
4. [ ] Individual chapter compiles standalone
5. [ ] Chapter bibliography shows only cited works
6. [ ] Images load correctly in both full and standalone mode

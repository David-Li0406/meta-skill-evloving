# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
LaTeX book scaffolding.

Creates a complete LaTeX book skeleton with subfiles support.
All content files use [PROMPT: ...] placeholders.
"""

from pathlib import Path


# =============================================================================
# TEMPLATES
# =============================================================================

MAIN_TEX = r"""\documentclass[12pt,a4paper]{book}

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
"""

LOCALSETTINGS_TEX = r"""% -------------------------------------------------------
%            PACKAGES AND BASIC SETUP
% -------------------------------------------------------

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[english]{babel}      % Change to [norsk] for Norwegian

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
%            CUSTOM ENVIRONMENTS
% -------------------------------------------------------

% Example box (breakable for long examples)
\newtcolorbox{example}[2][]{
  breakable,
  colback=gray!5,
  colframe=gray!50,
  fonttitle=\bfseries,
  title={Example: #2},
  #1
}

% Definition box (blue left border)
\newtcolorbox{definition}[2][]{
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
%            CODE LISTINGS
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
"""

REFERENCES_BIB = r"""% Bibliography entries
% Add your references here in BibTeX format

% Example book entry:
% @book{author2024,
%   author    = {Author, First},
%   title     = {Book Title},
%   year      = {2024},
%   publisher = {Publisher Name},
%   address   = {City}
% }

% Example article entry:
% @article{researcher2024,
%   author  = {Researcher, A. and Colleague, B.},
%   title   = {Article Title},
%   journal = {Journal Name},
%   year    = {2024},
%   volume  = {10},
%   number  = {2},
%   pages   = {100--120}
% }
"""

# --- Frontmatter ---

FRONTMATTER_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

\subfile{100-frontpage.tex}
\subfile{110-preface.tex}
\subfile{120-about.tex}
\subfile{130-acknowledgements.tex}
\subfile{140-toc.tex}

\end{document}
"""

FRONTPAGE_TEX = r"""\documentclass[../main.tex]{subfiles}
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
"""

PREFACE_TEX = r"""\documentclass[../main.tex]{subfiles}
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
"""

ABOUT_TEX = r"""\documentclass[../main.tex]{subfiles}
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
"""

ACKNOWLEDGEMENTS_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

\chapter*{Acknowledgements}
\addcontentsline{toc}{chapter}{Acknowledgements}

% [PROMPT: Thank:]
% - Colleagues, mentors, or collaborators
% - Institutions or funding sources
% - Family and friends
% - Anyone who contributed to the book

\end{document}
"""

TOC_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

\tableofcontents

\end{document}
"""

# --- Bodymatter ---

BODYMATTER_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

% Add parts and chapters here using \subfile{}
% Example:
%
% \part{Introduction}
% \renewcommand{\thechapter}{\roman{chapter}}
% \subfile{part01-introduction/part01.tex}
%
% \part{Main Content}
% \setcounter{chapter}{0}
% \renewcommand{\thechapter}{\arabic{chapter}}
% \subfile{part02-content/part02.tex}

\end{document}
"""

# --- Backmatter ---

BACKMATTER_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

% Appendices (uncomment and add as needed)
% \appendix
% \subfile{app01-name/app01-name.tex}

% Bibliography
\subfile{100-bibliography.tex}

% Index
\subfile{110-index.tex}

\end{document}
"""

BIBLIOGRAPHY_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

\printbibliography[heading=bibintoc]

\end{document}
"""

INDEX_TEX = r"""\documentclass[../main.tex]{subfiles}
\begin{document}

\printindex

\end{document}
"""


# =============================================================================
# SCAFFOLDING FUNCTION
# =============================================================================

def scaffold_latex(project_root: Path, echo=print) -> None:
    """Create LaTeX book skeleton with all necessary files and folders."""
    latex_dir = project_root / "latex"

    # Check if latex folder already exists
    if latex_dir.exists():
        echo(f"Error: {latex_dir} already exists. Aborting to prevent overwrite.")
        return

    echo(f"Creating LaTeX book skeleton in {latex_dir}")

    # Create directory structure
    dirs = [
        latex_dir,
        latex_dir / "bib",
        latex_dir / "100-frontmatter",
        latex_dir / "200-bodymatter",
        latex_dir / "300-backmatter",
        latex_dir / "build",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        echo(f"  Created: {d.relative_to(project_root)}")

    # Create files
    files = [
        # Root files
        (latex_dir / "main.tex", MAIN_TEX),
        (latex_dir / "localsettings.tex", LOCALSETTINGS_TEX),
        (latex_dir / "bib" / "references.bib", REFERENCES_BIB),

        # Frontmatter
        (latex_dir / "100-frontmatter" / "frontmatter.tex", FRONTMATTER_TEX),
        (latex_dir / "100-frontmatter" / "100-frontpage.tex", FRONTPAGE_TEX),
        (latex_dir / "100-frontmatter" / "110-preface.tex", PREFACE_TEX),
        (latex_dir / "100-frontmatter" / "120-about.tex", ABOUT_TEX),
        (latex_dir / "100-frontmatter" / "130-acknowledgements.tex", ACKNOWLEDGEMENTS_TEX),
        (latex_dir / "100-frontmatter" / "140-toc.tex", TOC_TEX),

        # Bodymatter
        (latex_dir / "200-bodymatter" / "bodymatter.tex", BODYMATTER_TEX),

        # Backmatter
        (latex_dir / "300-backmatter" / "backmatter.tex", BACKMATTER_TEX),
        (latex_dir / "300-backmatter" / "100-bibliography.tex", BIBLIOGRAPHY_TEX),
        (latex_dir / "300-backmatter" / "110-index.tex", INDEX_TEX),
    ]

    for filepath, content in files:
        filepath.write_text(content, encoding="utf-8")
        echo(f"  Created: {filepath.relative_to(project_root)}")

    echo("\nLaTeX book skeleton created successfully!")
    echo("\nNext steps:")
    echo("  1. Edit the [PROMPT: ...] placeholders in frontmatter files")
    echo("  2. Add parts and chapters to 200-bodymatter/bodymatter.tex")
    echo("  3. Run 'book compile' to build the PDF")


def main():
    """Standalone entry point."""
    import sys

    project_root = Path.cwd()
    scaffold_latex(project_root)


if __name__ == "__main__":
    main()

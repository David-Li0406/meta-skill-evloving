# LaTeX Style Guide

This guide defines the strict formatting and structural standards for the `N/` directory note files.

## 1. Document Structure

### File Fragment Rule
- **No Preamble**: Note files are **fragments** intended to be included via `\input`.
- **Prohibited**: Do NOT use `\documentclass`, `\begin{document}`, `\usepackage`, or `\end{document}`.
- **Allowed**: Only the content body (sections, text, math).

### Header Format
- Every file must start with a section command matching its filename.
- **Pattern**: `\section{Notes X - Date}`
- **Constraint**: `X` must match the file number (e.g., `N24.tex` -> `Notes 24`).

### Hierarchy
- Use `\subsection{Title}` for major topics.
- Use `\subsubsection{Title}` for sub-topics.
- Avoid using `\paragraph` or deeper nesting unless necessary.

## 2. Theorem Environments

Use only the following standard environments. Do not invent new ones.

### Theorem Style (Italicized body)
Used for primary mathematical statements.
```latex
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
```

### Definition Style (Roman/Upright body)
Used for definitions and examples.
```latex
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}{Example}[section]
\newtheorem{xca}[theorem]{Exercise}
```

### Remark Style (Roman/Upright body, unnumbered)
Used for commentary and notes.
```latex
\theoremstyle{remark}
\newtheorem*{remark}{Remark}
\newtheorem*{note}{Note}
\newtheorem*{recap}{Recap}
\newtheorem*{hint}{Hint}
```

## 3. Proof Handling

- **Default**: Proofs should generally be preserved.
- **Exceptions**: If the specific task or global setting requires hiding proofs, comment them out using `%`.
- **Format**:
  ```latex
  % \begin{proof}
  %  Proof content...
  % \end{proof}
  ```

## 4. Source Code Formatting

To maintain clean and consistent source files, follow these indentation rules.

### Rules
- **No Indentation**: All lines of code, including those inside nested environments (like `enumerate`, `align*`, etc.), must be **flush left**. Do **not** use tabs or spaces at the start of any line.

### Standard Format Examples

**Theorem (All flush left):**
```latex
\begin{theorem}
The theorem is stated as follows:
\begin{enumerate}
\item First condition...
\item Second condition...
\end{enumerate}
\end{theorem}
```

**Lemma (All flush left):**
```latex
\begin{lemma}
Say something. There is no tab before ``Say''.
\end{lemma}
```

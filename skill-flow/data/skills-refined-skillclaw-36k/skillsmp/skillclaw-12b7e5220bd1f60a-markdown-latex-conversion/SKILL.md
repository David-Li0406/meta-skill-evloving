---
name: markdown-latex-conversion
description: Use this skill when you need to convert documents between Markdown and LaTeX formats, whether transforming .md files to .tex or vice versa.
---

# Markdown and LaTeX Converter

This skill allows you to convert documents between Markdown and LaTeX formats, supporting a wide range of syntax for both formats.

## Usage

### Convert Markdown to LaTeX

```bash
npx tsx plugins/tex/scripts/md-to-latex.ts <text>
npx tsx plugins/tex/scripts/md-to-latex.ts --file <input.md>
npx tsx plugins/tex/scripts/md-to-latex.ts --file <input.md> --output <output.tex>
```

### Convert LaTeX to Markdown

```bash
npx tsx plugins/tex/scripts/latex-to-md.ts <text>
npx tsx plugins/tex/scripts/latex-to-md.ts --file <input.tex>
npx tsx plugins/tex/scripts/latex-to-md.ts --file <input.tex> --output <output.md>
```

## Supported Conversions

### Markdown to LaTeX

- **Headers**
  - `# Heading` → `\chapter{Heading}`
  - `## Heading` → `\section{Heading}`
  - `### Heading` → `\subsection{Heading}`
  - `#### Heading` → `\subsubsection{Heading}`
  - `##### Heading` → `\paragraph{Heading}`
  - `###### Heading` → `\subparagraph{Heading}`

- **Text Formatting**
  - `**bold**` or `__bold__` → `\textbf{bold}`
  - `*italic*` or `_italic_` → `\emph{italic}`
  - `` `code` `` → `\texttt{code}`

- **Code Blocks**
  ```markdown
  ```python
  def hello():
      print("world")
  ```
  ```
  → 
  ```latex
  \begin{verbatim}
  def hello():
      print("world")
  \end{verbatim}
  ```

- **Lists**
  - Unordered:
    ```markdown
    - Item 1
    - Item 2
      - Nested item
    ```
    → 
    ```latex
    \begin{itemize}
    \item Item 1
    \item Item 2
      \item Nested item
    \end{itemize}
    ```

  - Ordered:
    ```markdown
    1. First
    2. Second
    ```
    → 
    ```latex
    \begin{enumerate}
    \item First
    \item Second
    \end{enumerate}
    ```

- **Links**
  - `[text](url)` → `\href{url}{text}`

- **Images**
  - `![alt](path)` → `\begin{figure}[h]\n\centering\n\includegraphics{path}\n\caption{alt}\n\end{figure}`
  - `![](path)` → `\includegraphics{path}`

- **Blockquotes**
  ```markdown
  > This is a quote
  ```
  → 
  ```latex
  \begin{quote}
  This is a quote
  \end{quote}
  ```

- **Horizontal Rules**
  - `---` → `\hrulefill`

### LaTeX to Markdown

- **Sections/Headers**
  - `\chapter{Title}` → `# Title`
  - `\section{Title}` → `## Title`
  - `\subsection{Title}` → `### Title`
  - `\subsubsection{Title}` → `#### Title`
  - `\paragraph{Title}` → `##### Title`
  - `\subparagraph{Title}` → `###### Title`

- **Text Formatting**
  - `\textbf{bold}` → `**bold**`
  - `\textit{italic}` → `*italic*`
  - `\texttt{code}` → `` `code` ``

- **Code Blocks**
  ```latex
  \begin{verbatim}
  code here
  \end{verbatim}
  ```
  → 
  ````markdown
  ```
  code here
  ```
  ````

- **Lists**
  - Unordered:
    ```latex
    \begin{itemize}
    \item First item
    \item Second item
    \end{itemize}
    ```
    → 
    ```markdown
    - First item
    - Second item
    ```

  - Ordered:
    ```latex
    \begin{enumerate}
    \item First
    \item Second
    \end{enumerate}
    ```
    → 
    ```markdown
    1. First
    2. Second
    ```

- **Links**
  - `\href{url}{text}` → `[text](url)`

- **Images**
  - With caption:
    ```latex
    \begin{figure}
    \includegraphics{image.png}
    \caption{Description}
    \end{figure}
    ```
    → 
    ```markdown
    ![Description](image.png)
    ```

  - Without caption:
    - `\includegraphics{image.png}` → `![](image.png)`

- **Blockquotes**
  ```latex
  \begin{quote}
  This is a quote
  \end{quote}
  ```
  → 
  ```markdown
  > This is a quote
  ```

- **Horizontal Rules**
  - `\hrulefill` → `---`

## Special Character Handling

LaTeX special characters (`&`, `%`, `$`, `#`, `_`, `{`, `}`) are automatically escaped in text content (but not in code blocks). 

## Math Preservation

LaTeX math notation is preserved as-is:
- Inline math: `$...$` remains `$...$`
- Display math: `$$...$$` remains `$$...$$`
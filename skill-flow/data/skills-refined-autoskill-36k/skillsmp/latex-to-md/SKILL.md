---
name: latex-to-md
description: Convert LaTeX to Markdown format. Use when the user asks to convert, transform, or change LaTeX files to Markdown, or mentions converting .tex files to .md files.
---

# LaTeX to Markdown Converter

Convert LaTeX documents to Markdown format with support for common LaTeX commands and environments.

## Usage

```bash
npx tsx plugins/tex/scripts/latex-to-md.ts <text>
npx tsx plugins/tex/scripts/latex-to-md.ts --file <input.tex>
npx tsx plugins/tex/scripts/latex-to-md.ts --file <input.tex> --output <output.md>
```

## Supported Conversions

### Sections/Headers
- `\chapter{Title}` → `# Title`
- `\section{Title}` → `## Title`
- `\subsection{Title}` → `### Title`
- `\subsubsection{Title}` → `#### Title`
- `\paragraph{Title}` → `##### Title`
- `\subparagraph{Title}` → `###### Title`

### Text Formatting
- `\textbf{bold}` → `**bold**`
- `\textit{italic}` → `*italic*`
- `\emph{emphasis}` → `*emphasis*`
- `\texttt{code}` → `` `code` ``
- `\verb|code|` → `` `code` ``

### Code Blocks
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

Also supports `lstlisting` environment.

### Lists

**Itemize (unordered):**
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

**Enumerate (ordered):**
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

### Links
- `\href{url}{text}` → `[text](url)`
- `\url{url}` → `<url>`

### Images

**With caption (figure environment):**
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

**Without caption:**
- `\includegraphics{image.png}` → `![](image.png)`
- `\includegraphics[width=5cm]{image.png}` → `![](image.png)` (options stripped)

### Blockquotes
```latex
\begin{quote}
This is a quote
\end{quote}
```
→
```markdown
> This is a quote
```

### Horizontal Rules
- `\hrulefill` → `---`
- `\hline` → `---`

## Unicode Character Decoding

LaTeX special characters are automatically decoded to Unicode:
- `\'{e}` → `é`
- `\"{a}` → `ä`
- `\c{c}` → `ç`
- `\ae` → `æ`
- `\oe` → `œ`
- `\ss` → `ß`
- And ~100 more LaTeX commands

See **tex-decode** skill for complete list of supported characters.

## Math Preservation

LaTeX math notation is preserved as-is:
- Inline math: `$...$` remains `$...$`
- Display math: `$$...$$` remains `$$...$$`

Many Markdown renderers support this syntax natively.

## Arguments

- **Positional arguments**: Text to convert (if no `--file` flag)
- **`--file`**: Read input from file
- **`--output <file>`**: Write output to file (default: stdout)

## Examples

### Convert inline text
```bash
npx tsx plugins/tex/scripts/latex-to-md.ts "\\section{Hello}\n\nThis is \\textbf{bold}."
```

### Convert file
```bash
npx tsx plugins/tex/scripts/latex-to-md.ts --file paper.tex --output paper.md
```

### Extract plain text from LaTeX
```bash
npx tsx plugins/tex/scripts/latex-to-md.ts --file document.tex | npx tsx plugins/tex/scripts/strip.ts
```

## Limitations

- Does not handle complex LaTeX packages or custom commands
- Tables are not automatically converted (LaTeX tables vary widely in structure)
- Cross-references (`\ref`, `\cite`) are not resolved
- Bibliographies require separate handling
- Complex math environments may need manual adjustment
- Nested environments beyond simple cases may not convert perfectly

## Related Skills

- **md-to-latex**: Convert Markdown to LaTeX
- **tex-decode**: Decode LaTeX commands to Unicode (used internally)
- **tex-strip**: Remove all LaTeX formatting for plain text
- **tex-protect**: Protect text from LaTeX interpretation

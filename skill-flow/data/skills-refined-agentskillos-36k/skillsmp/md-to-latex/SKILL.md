---
name: md-to-latex
description: Convert Markdown to LaTeX format. Use when the user asks to convert, transform, or change Markdown files to LaTeX, or mentions converting .md files to .tex files.
---

# Markdown to LaTeX Converter

Convert Markdown documents to LaTeX format with comprehensive support for common Markdown syntax.

## Usage

```bash
npx tsx plugins/tex/scripts/md-to-latex.ts <text>
npx tsx plugins/tex/scripts/md-to-latex.ts --file <input.md>
npx tsx plugins/tex/scripts/md-to-latex.ts --file <input.md> --output <output.tex>
```

## Supported Conversions

### Headers
- `# Heading` → `\chapter{Heading}`
- `## Heading` → `\section{Heading}`
- `### Heading` → `\subsection{Heading}`
- `#### Heading` → `\subsubsection{Heading}`
- `##### Heading` → `\paragraph{Heading}`
- `###### Heading` → `\subparagraph{Heading}`

### Text Formatting
- `**bold**` or `__bold__` → `\textbf{bold}`
- `*italic*` or `_italic_` → `\emph{italic}`
- `` `code` `` → `\texttt{code}`

### Code Blocks
````markdown
```python
def hello():
    print("world")
```
````
→
```latex
\begin{verbatim}
def hello():
    print("world")
\end{verbatim}
```

### Lists

**Unordered lists:**
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

**Ordered lists:**
```markdown
1. First
2. Second
3. Third
```
→
```latex
\begin{enumerate}
\item First
\item Second
\item Third
\end{enumerate}
```

### Links
- `[text](url)` → `\href{url}{text}`

### Images
- `![alt](path)` → `\begin{figure}[h]\n\centering\n\includegraphics{path}\n\caption{alt}\n\end{figure}`
- `![](path)` → `\includegraphics{path}` (no caption)

### Blockquotes
```markdown
> This is a quote
> spanning multiple lines
```
→
```latex
\begin{quote}
This is a quote
spanning multiple lines
\end{quote}
```

### Horizontal Rules
- `---` → `\hrulefill`

## Special Character Handling

LaTeX special characters (`&`, `%`, `$`, `#`, `_`, `{`, `}`) are automatically escaped in text content (but not in code blocks).

## Arguments

- **Positional arguments**: Text to convert (if no `--file` flag)
- **`--file`**: Read input from file
- **`--output <file>`**: Write output to file (default: stdout)

## Examples

### Convert inline text
```bash
npx tsx plugins/tex/scripts/md-to-latex.ts "# Hello World\n\nThis is **bold** text."
```

### Convert file
```bash
npx tsx plugins/tex/scripts/md-to-latex.ts --file document.md --output document.tex
```

### Use in pipeline
```bash
echo "## Section\n\nParagraph with *italic*" | npx tsx plugins/tex/scripts/md-to-latex.ts
```

## Limitations

- Does not handle complex nested structures beyond simple cases
- Tables are not automatically converted (Markdown tables have no direct LaTeX equivalent without packages)
- Math notation is preserved as-is (both Markdown and LaTeX use `$...$` for inline math and `$$...$$` for display math)
- HTML tags in Markdown are not converted

## Related Skills

- **latex-to-md**: Convert LaTeX back to Markdown
- **tex-encode**: Encode Unicode characters to LaTeX commands
- **tex-decode**: Decode LaTeX commands to Unicode
- **tex-strip**: Remove all LaTeX formatting for plain text

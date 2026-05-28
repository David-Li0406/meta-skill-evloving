# Reference: Legacy & Utility PDF Tools (Python/CLI)

## Overview
While the Squaads AI Core is JS-first, there are specific scenarios where Python libraries or CLI tools are faster, more memory-efficient, or handle specific edge cases better.

## 🛠️ Python Power Tools

### 1. `pdfplumber` (The Table Specialist)
For non-AI table extraction, `pdfplumber` remains the most precise tool for identifying cell boundaries.

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("complex_report.pdf") as pdf:
    table = pdf.pages[0].extract_table()
    df = pd.DataFrame(table[1:], columns=table[0])
```

### 2. `pypdf` (Fast Merging)
For merging thousands of files, `pypdf` is significantly lighter than launching a headless browser.

```python
from pypdf import PdfWriter

writer = PdfWriter()
for pdf in ["a.pdf", "b.pdf"]:
    writer.append(pdf)
writer.write("combined.pdf")
```

---

## 💻 CLI Forensics

### `qpdf` (The Repair Shop)
If a PDF is corrupted or has unreadable metadata, `qpdf` is the go-to tool.

```bash
# Decompress a PDF to inspect the raw objects (Human readable)
qpdf --qdf --object-streams=disable input.pdf inspect.pdf

# Fix a "Premature EOF" error
qpdf input.pdf --replace-input
```

### `poppler-utils` (The Speed Demon)
When you just need raw text as fast as possible for a search index.

```bash
# Blazing fast text extraction
pdftotext -layout input.pdf -
```

---

## 🏁 When to use what?
- **Next.js API?** -> Use JS (`pdf-lib`, `Puppeteer`).
- **Heavy Batch Processing?** -> Use Python (`pdfplumber`) or CLI (`qpdf`).
- **AI RAG Pipeline?** -> Use `unpdf` or `pdftotext`.

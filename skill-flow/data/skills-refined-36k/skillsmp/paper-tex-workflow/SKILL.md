---
name: paper-tex-workflow
description: Workflow for editing the root-level paper.tex and references.bib (English papers). Use when working with paper.tex at repo root, checking citations, or extracting content from PDFs in papers/.
license: Complete terms in LICENSE.txt
---

# paper.tex Workflow (Root English Paper)

## Context
This repo has **two distinct workflows**:
1. **TCC/ABNT review** (PT-BR): work in `project/` directory (see latex-tcc-abnt-review-ptbr skill)
2. **English paper drafting**: work with `paper.tex` and `references.bib` at repo root (this skill)

## When to use this skill
- User asks to edit/draft/improve `paper.tex` or root-level English papers
- User requests citation checking or bibliography management for the root paper
- User wants to extract content from PDFs in `papers/` directory

## File locations
- Main paper: `/paper.tex` (repo root)
- References: `/references.bib` (repo root)
- PDF sources: `/papers/*.pdf` (optional)
- Citation checker: `/tools/check_cites.py`
- PDF extractors: `/tools/extract_papers.py`, `/tools/review_papers.py`

## Core workflow steps

### 1. Citation Hygiene Check
**Always run before major edits** to understand citation state:
```bash
python tools/check_cites.py
```

Output shows:
- Citations in paper.tex: count
- Entries in references.bib: count
- **Missing bib entries**: keys cited but not defined (fix these!)
- Unused bib entries: keys defined but never cited (optional cleanup)

### 2. Extract Content from PDFs (if applicable)
If `papers/` contains PDFs of related work:

**Quick abstract extraction:**
```bash
python tools/extract_papers.py
```
Shows title + abstract for each PDF.

**Detailed section extraction:**
```bash
python tools/review_papers.py
```
Attempts to extract: title, abstract, dataset, method, results.

Use extracted content to:
- Draft Related Work section
- Add proper citations to `references.bib`
- Compare methods/results in Discussion

### 3. Edit paper.tex
Follow IMRAD structure (see latex-paper-writing-en skill for detailed guidance).

Key repo conventions:
- Use LaTeX quotes: ``like this'' not "like this"
- Foreign terms in italics: `\textit{term}`
- Citation format depends on loaded package (natbib/biblatex)

### 4. Manage references.bib
Follow bibtex-reference-management skill for:
- Key naming conventions
- Required fields per entry type
- Title casing protection with `{}`

### 5. Validate
After edits:
```bash
# Re-check citations
python tools/check_cites.py

# Check LaTeX errors (if compilation available)
get_errors with filePaths: ["paper.tex"]
```

## Common tasks

### Add a new reference from PDF
1. Run `python tools/extract_papers.py` to get title/abstract
2. Find full metadata (DOI, venue, year) online
3. Add proper BibTeX entry to `references.bib`
4. Use `\cite{key}` in `paper.tex`
5. Verify with `python tools/check_cites.py`

### Fix missing citations
1. Run citation checker, note missing keys
2. Either:
   - Add missing entries to `references.bib`, OR
   - Remove/fix incorrect `\cite{}` in `paper.tex`

### Clean unused references
1. Identify unused entries from checker output
2. Decide: keep (might use later) or remove
3. If removing, ensure no future references planned

## Integration with other skills
- Use **latex-paper-writing-en** for actual writing/rewriting
- Use **bibtex-reference-management** for .bib quality
- Do NOT use latex-tcc-abnt-review-ptbr (that's for project/ only)

## Quick reference
```bash
# Citation check
python tools/check_cites.py

# Extract PDFs
python tools/extract_papers.py     # abstracts
python tools/review_papers.py      # sections
```

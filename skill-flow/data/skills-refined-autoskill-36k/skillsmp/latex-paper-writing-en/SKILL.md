---
name: latex-paper-writing-en
description: Write and refine scientific papers in LaTeX (English). Use this when asked to draft, rewrite, or improve paper sections (IMRAD), strengthen academic tone, add citations/refs correctly, or build an outline.
license: Complete terms in LICENSE.txt
---

# LaTeX Paper Writing (EN)

## Scope
Use this skill to *write* or *revise* scientific paper content in English, directly in LaTeX.

**Repo context**: This workspace has `paper.tex` and `references.bib` at the root for English paper drafting. Use `python tools/check_cites.py` to verify citation hygiene (compares cited keys vs .bib entries).

Non-goals:
- Do not change technical claims without evidence.
- Do not add citations you cannot justify; prefer asking for sources or marking TODOs.
- Do not over-rewrite: preserve the author's voice and intent.

## Default Working Mode (recommended)
1. **Clarify the target**: venue style (IEEE/ACM/Elsevier), section(s), word/page constraints.
2. **Outline-first**: propose bullet outline before writing full prose when structure is unclear.
3. **Evidence-first**: every nontrivial claim should have a citation, data, or qualification.
4. **LaTeX-native**: write as valid LaTeX, using semantic commands (`\\section`, `\\subsection`, `\\label`, `\\ref`, `\\cite`).

## IMRAD Writing Heuristics
### Introduction (pattern)
- Context: what area + why it matters.
- Problem: what concrete limitation exists.
- Gap: what prior work misses (cite).
- Objective: what this paper does.
- Contributions: 2–4 bullet contributions.
- Paper organization: brief roadmap.

### Related Work
- Group by approach/theme (not by author).
- For each group: what it solves, what it assumes, and limitations.
- End with a *positioning paragraph*: what you do differently.

### Methodology
- Write for reproducibility.
- Include: data (source/splits), model/architecture, training details, baselines, evaluation metrics.
- Explicitly state assumptions and limitations.

### Results
- Report numbers with context (dataset, metric, split, N).
- Prefer tables/figures; reference them in text.
- Avoid “promising” language; be precise.

### Discussion
- Interpret results: *why* it worked/failed.
- Compare to baselines and related work.
- Discuss threats to validity.

### Conclusion
- Summarize contributions and key results.
- State limitations.
- Propose realistic future work.

## Citation & Cross-Reference Rules
- Place citations immediately after the claim: `... improves generalization \\cite{key}.`
- For multiple sources: `\\cite{key1,key2}` (or project-specific citation commands).
- Always `\\label{sec:...}` sections you may reference later; reference with `\\ref{sec:...}`.

## LaTeX Style Checklist
- Consistent terminology (same term for same concept).
- Acronyms: define on first use, then use acronym consistently.
- Use proper LaTeX quotes: ``like this''.
- Prefer `booktabs` in tables (`\\toprule`, `\\midrule`, `\\bottomrule`) when available.

## Quality Checklist
- Objective and contributions are explicit.
- Claims are either cited, measured, or qualified.
- Method is reproducible.
- Results support conclusions.
- LaTeX compiles without errors.

## Citation Hygiene (repo-specific)
After writing/editing, run citation check:
```bash
python tools/check_cites.py
```
This reports:
- Missing .bib entries for cited keys.
- Unused .bib entries (optional cleanup).

If PDFs are in `papers/`, extract abstracts with:
```bash
python tools/extract_papers.py
python tools/review_papers.py
```

## Prompt Patterns (examples)
- "Draft the Introduction in LaTeX (EN) using IMRAD. Include contributions bullets and cite placeholders where needed."
- "Rewrite this paragraph to be more academic and precise, preserving meaning."
- "Turn these bullet notes into a Methods section; keep it reproducible and cite where appropriate."
- "Check citation hygiene and add missing bib entries."

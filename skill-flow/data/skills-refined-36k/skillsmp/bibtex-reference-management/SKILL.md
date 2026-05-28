---
name: bibtex-reference-management
description: Manage BibTeX (.bib) references and citation hygiene for LaTeX projects. Use this when asked to add/fix BibTeX entries, standardize keys, detect missing/unused citations, or improve bibliographic completeness and casing.
license: Complete terms in LICENSE.txt
---

# BibTeX Reference Management

## Scope
Use this skill to improve citation hygiene and BibTeX quality.

Goals:
- Ensure every `\\cite{}` key exists in `.bib`.
- Ensure `.bib` entries are complete and consistently formatted.
- Prevent casing issues in titles.

## Workflow
1. **Inventory**
   - Find all `\\cite{...}` occurrences.
   - Extract citation keys.
   - List `.bib` files used by the project.

2. **Consistency checks**
   - Missing entries: cited keys not present in any `.bib`.
   - Unused entries: BibTeX keys never cited (optional cleanup).
   - Duplicate keys: same key defined more than once.

3. **Normalize entries**
   - Use consistent key naming.
   - Ensure required fields per entry type.
   - Protect proper nouns/acronyms with `{}`.

## Key Naming Convention
Default suggestion (adjust if repo already uses a convention):
- `surnameYEARkeyword` (e.g., `smith2022transformers`)
- Keep lowercase; avoid punctuation.

## Required Fields (quick reference)
- `@article`: `author`, `title`, `journal`, `year` (+ `volume/number/pages/doi` when available)
- `@inproceedings`: `author`, `title`, `booktitle`, `year` (+ `pages/doi`)
- `@book`: `author`/`editor`, `title`, `publisher`, `year` (+ `edition/address` depending on style)
- `@misc`: use sparingly; prefer `@online` only if your style supports it.

## Title Casing Protection
Use braces to preserve casing:
- `{GPU}` not `GPU`
- `{Bayesian}` not `Bayesian` (if style downcases titles)
- Product names: `{Node.js}`, `{React}`

## Practical Rules
- Prefer DOI when available.
- Ensure author names are “Last, First and Last, First”.
- Keep URLs stable; add `urldate` if style uses it.

## When Information Is Missing
- If a paper is referenced but metadata is incomplete, request the DOI/URL from the user.
- If the user wants you to proceed, add a clearly marked placeholder field and leave a TODO.

## Output Hygiene
- Avoid inventing bibliographic details.
- If you must approximate (e.g., missing pages), explicitly flag as TODO.

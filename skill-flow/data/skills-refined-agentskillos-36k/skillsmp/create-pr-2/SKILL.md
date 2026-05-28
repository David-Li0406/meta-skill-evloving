---
name: create-pr
description: Esta skill debe usarse cuando el usuario pide "crea el PR", "prepara el PR", "escribe el PR", "genera el PR", "draft del PR", "documenta el PR", "crea la descripción del PR", o menciona crear pull request manualmente. Proporciona formato estructurado adaptado al tamaño de los cambios.
---

Create a pull request text on a file named `<current-branch>-PR.md` on English language
following one of the formats defined in [formats](./formats)

Create the file at the root of the CWD.

## Posible formats

- [standard](./formats/standard.md): When none of the other formats apply.
  
If in doubt between two or more formats and standard is not included, ask the user for clarification.

**Temporal note**: More formats will be added in the future, just use standard for now.

## Guidelines

- Be concise, fulfill the information on formats with the minimal required information.
  - If the reader of it needs more context, let them ask for it, so do not bloat the file.
- Use markdown syntax.
- Be aware of the dimension of the changes done.
  - A small fix or feature should not have a very big PR description.
  - A big refactor or feature should have a more detailed PR description.

## How to measure size the changes

- Small: 1-4 files changed, up to 150 lines changed.
  - PR sections will likely have one to two sentences.
- Medium: 5-7 files changed, 150-700 lines changed.
  - Try to explain the reasoning behind the changes.
  - PR sections will likely have up to 3 paragraphs.
- Large: 8+ files changed, 700+ lines changed.
  - PR sections will likely have up to 5 paragraphs.
  - There is a high chance that there are going to be multiple elements involved, explain how they interconnect.
  - Focus on a explaining the high level details of the changes

The assistant have the proper criteria and judgment to determine the dimension of changes
done outside of the quantitative metrics provided; appeal the quantitative metrics as a guideline, not a rule.

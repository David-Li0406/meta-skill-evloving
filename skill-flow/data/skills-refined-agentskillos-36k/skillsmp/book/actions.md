# Book Structure Actions

This document defines workflows for Claude Code to manage book structure elements (parts, chapters, sections, appendices). Each action specifies exactly which files must be created, modified, or deleted.

**Usage:** When the user requests a structural change to the book, match their request to the appropriate action below and execute the workflow.

---

## Table of Contents

1. [Terminology](#terminology)
2. [Part Operations](#part-operations)
3. [Chapter Operations](#chapter-operations)
4. [Section Operations](#section-operations)
5. [Appendix Operations](#appendix-operations)
6. [Frontmatter Operations](#frontmatter-operations)
7. [Reordering Operations](#reordering-operations)

---

## Terminology

| Term | Description |
|------|-------------|
| **Aggregator** | A file that includes child elements via `\subfile{}` commands |
| **Slug** | The descriptive part of a name (e.g., `ettersporselprognoser` in `ch01-ettersporselprognoser`) |
| **Prefix** | The numbering part (e.g., `ch01`, `sec02`, `part01`) |

### Path Depth Reference

| Location | documentclass path |
|----------|-------------------|
| `latex/` | `main.tex` (root) |
| `100-frontmatter/` | `../main.tex` |
| `200-bodymatter/` | `../main.tex` |
| `200-bodymatter/partNN-*/` | `../../main.tex` |
| `200-bodymatter/partNN-*/chXX-*/` | `../../../main.tex` |
| `300-backmatter/` | `../main.tex` |
| `300-backmatter/appNN-*/` | `../../main.tex` |

### NEW vs INSERT

| Operation | Behavior | Renumbering |
|-----------|----------|-------------|
| **NEW** | Appends to the end | None - uses next available number |
| **INSERT** | Inserts BEFORE specified position | All items from that position onwards are renumbered (+1) |

**Example:** If ch01, ch02, ch03 exist:
- `NEW chapter` → creates ch04
- `INSERT chapter 2` → inserts new chapter as ch02, old ch02→ch03, old ch03→ch04

---

## Part Operations

Parts are major divisions within bodymatter (e.g., "Introduction", "Topics").

### NEW PART

**Triggers:**
- "new part"
- "add part"
- "create part called..."
- "add a new part"

**Required information:**
- Slug (e.g., "advanced-topics")
- Title (e.g., "Advanced Topics")

**Behavior:** Appends new part after all existing parts with next available number.

**Files to CREATE:**

1. **Folder:** `latex/200-bodymatter/part<NN>-<slug>/`
2. **Aggregator file:** `latex/200-bodymatter/part<NN>-<slug>/part<NN>.tex`

   ```latex
   \documentclass[../../main.tex]{subfiles}
   \begin{document}

   % Add chapters here using \subfile{chXX-name/chXX-name.tex}

   \end{document}
   ```

**Files to MODIFY:**

1. **`latex/200-bodymatter/bodymatter.tex`** - Append entry at end:

   ```latex
   % ============ DEL <N>: <TITLE UPPERCASE> ============
   \part{<Title>}
   \setcounter{chapter}{0}
   \renewcommand{\thechapter}{\arabic{chapter}}
   \subfile{part<NN>-<slug>/part<NN>.tex}
   ```

---

### INSERT PART

**Triggers:**
- "insert part before X"
- "insert part at position X"
- "add part before part X"

**Required information:**
- Position to insert BEFORE (e.g., "part 2" or "part02")
- Slug (e.g., "fundamentals")
- Title (e.g., "Fundamentals")

**Behavior:** Inserts new part BEFORE the specified position. All parts from that position onwards are renumbered.

**Example:** If part01, part02 exist and user says "insert part before part02":
- New part becomes part02
- Old part02 becomes part03

**Workflow:**

1. **Identify parts to renumber:** part02, part03... → part03, part04...

2. **Rename in reverse order (highest first):**
   - For each part from highest to insertion point:
     - Rename folder: `part<NN>-<slug>/` → `part<NN+1>-<slug>/`
     - Rename aggregator: `part<NN>.tex` → `part<NN+1>.tex`
     - Update `\documentclass` path inside aggregator (stays same - `../../main.tex`)

3. **Update `bodymatter.tex`:**
   - Update all `\subfile{part<NN>-...}` paths for renumbered parts

4. **Create new part at the insertion position**

5. **Update `bodymatter.tex`:**
   - Insert new `\subfile` line at correct position

**Note:** Chapter files inside parts do NOT need updating (they reference `../../main.tex`, not the part folder name).

---

### RENAME PART

**Triggers:**
- "rename part"
- "change part name"
- "update part title"
- "part X should be called..."

**Required information:**
- Current part identifier (number or slug)
- New slug (optional)
- New title (optional)

**Files to MODIFY:**

1. **Rename folder:** `part<NN>-<old-slug>/` → `part<NN>-<new-slug>/`
2. **Rename aggregator:** `part<NN>.tex` stays same (only slug changes in folder name)
3. **Update `bodymatter.tex`:**
   - Change `\subfile{part<NN>-<old-slug>/...}` → `\subfile{part<NN>-<new-slug>/...}`
   - Update `\part{Old Title}` → `\part{New Title}` if title changes

**No changes needed in:**
- Child chapter files (they reference `../../main.tex`, not the part folder name)
- Sections (they reference `../../../main.tex`)

---

### DELETE PART

**Triggers:**
- "delete part"
- "remove part"
- "get rid of part"

**Preconditions:**
- Part must be empty (no chapters) OR user confirms deletion of all contents

**Files to DELETE:**

1. **Entire folder:** `latex/200-bodymatter/part<NN>-<slug>/` (recursive)

**Files to MODIFY:**

1. **`latex/200-bodymatter/bodymatter.tex`:**
   - Remove the `\part{...}` line
   - Remove the `\subfile{part<NN>-<slug>/part<NN>.tex}` line
   - Remove any associated counter reset commands

**Note:** Deleting does NOT automatically renumber remaining parts. Gaps in numbering are allowed.

---

## Chapter Operations

Chapters exist within parts. They use either roman numerals (part01) or arabic numerals (part02+).

### Chapter Numbering Schemes

| Part | Prefix Pattern | Examples |
|------|---------------|----------|
| part01 | `ch<roman>` | `chi`, `chii`, `chiii`, `chiv`, `chv` |
| part02+ | `ch<NN>` | `ch01`, `ch02`, `ch10`, `ch11` |

**Roman numeral mapping:** i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii...

---

### NEW CHAPTER

**Triggers:**
- "new chapter"
- "add chapter"
- "create chapter in part..."
- "add chapter called..."
- "new chapter about..."

**Required information:**
- Target part (e.g., part02)
- Slug (e.g., "transport-optimization")
- Title (e.g., "Transport Optimization")

**Behavior:** Appends new chapter after all existing chapters in the part with next available number.

**Files to CREATE:**

1. **Folder:** `latex/200-bodymatter/part<NN>-<partslug>/ch<XX>-<chapter-slug>/`
2. **Chapter aggregator:** `ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex`

   ```latex
   \documentclass[../../../main.tex]{subfiles}
   \graphicspath{{\subfix{./figures/}}}
   \begin{document}

   \chapter{<Chapter Title>}
   \label{ch:<chapter-slug>}

   % [PROMPT: Chapter introduction]

   % Add sections here using \subfile{secNN-name.tex}

   \ifSubfilesClassLoaded{%
     \printbibliography
   }{}

   \end{document}
   ```

3. **Figures folder:** `ch<XX>-<chapter-slug>/figures/` (empty)

**Files to MODIFY:**

1. **`part<NN>.tex`** - Append entry at end:

   ```latex
   % Kapittel <N> - <Title>
   \subfile{ch<XX>-<chapter-slug>/ch<XX>-<chapter-slug>.tex}
   ```

---

### INSERT CHAPTER

**Triggers:**
- "insert chapter before X"
- "insert chapter at position X"
- "insert chapter X" (means insert BEFORE existing chapter X)
- "add chapter before chapter X"

**Required information:**
- Target part
- Position to insert BEFORE (e.g., "chapter 2", "ch02", or "chii")
- Slug (e.g., "prerequisites")
- Title (e.g., "Prerequisites")

**Behavior:** Inserts new chapter BEFORE the specified position. All chapters from that position onwards are renumbered.

**Example:** If ch01, ch02, ch03 exist and user says "insert chapter 2":
- New chapter becomes ch02
- Old ch02 becomes ch03
- Old ch03 becomes ch04

**Workflow:**

1. **Identify chapters to renumber:** ch02, ch03... → ch03, ch04...

2. **Rename in reverse order (highest first to avoid conflicts):**
   - For each chapter from highest to insertion point:
     - Rename folder: `ch<XX>-<slug>/` → `ch<XX+1>-<slug>/`
     - Rename chapter file: `ch<XX>-<slug>.tex` → `ch<XX+1>-<slug>.tex`
     - Update inside chapter file:
       - `\label{ch:<slug>}` stays same (uses slug, not number)
     - Rename all section files if they include chapter number in name (usually they don't)

3. **Update `part<NN>.tex`:**
   - Update all `\subfile{ch<XX>-...}` paths for renumbered chapters

4. **Create new chapter at the insertion position**

5. **Update `part<NN>.tex`:**
   - Insert new `\subfile` line at correct position

**Cross-reference updates (if labels include numbers):**
- Search and update any `\ref{ch:XX}` if using numeric labels

---

### RENAME CHAPTER

**Triggers:**
- "rename chapter"
- "change chapter name"
- "update chapter title"
- "chapter X should be called..."

**Required information:**
- Current chapter identifier (prefix or slug)
- New slug (optional)
- New title (optional)

**Files to MODIFY:**

1. **Rename folder:** `ch<XX>-<old-slug>/` → `ch<XX>-<new-slug>/`
2. **Rename chapter file:** `ch<XX>-<old-slug>.tex` → `ch<XX>-<new-slug>.tex`
3. **Update chapter file content:**
   - `\label{ch:<old-slug>}` → `\label{ch:<new-slug>}`
   - `\chapter{Old Title}` → `\chapter{New Title}` if title changes
4. **Update `part<NN>.tex`:**
   - `\subfile{ch<XX>-<old-slug>/ch<XX>-<old-slug>.tex}` → `\subfile{ch<XX>-<new-slug>/ch<XX>-<new-slug>.tex}`

**No changes needed in:**
- Section files (they use relative `\subfile{}` without folder path)

**Cross-reference updates (search entire project):**
- Update any `\ref{ch:<old-slug>}` → `\ref{ch:<new-slug>}`
- Update any `\hyperref[ch:<old-slug>]` → `\hyperref[ch:<new-slug>]`

---

### DELETE CHAPTER

**Triggers:**
- "delete chapter"
- "remove chapter"
- "get rid of chapter"

**Preconditions:**
- Confirm with user if chapter has content (sections, figures)

**Files to DELETE:**

1. **Entire folder:** `ch<XX>-<slug>/` (recursive, including figures/, sections)

**Files to MODIFY:**

1. **`part<NN>.tex`:**
   - Remove the `\subfile{ch<XX>-<slug>/ch<XX>-<slug>.tex}` line
   - Remove any associated comment

**Note:** Deleting does NOT automatically renumber remaining chapters. Gaps in numbering are allowed.

---

### MOVE CHAPTER TO ANOTHER PART

**Triggers:**
- "move chapter to part"
- "transfer chapter"
- "move chapter X from part Y to part Z"

**Required information:**
- Source part
- Chapter to move
- Target part
- Position in target (optional, defaults to end)

**Files to MODIFY:**

1. **Move folder:** `part01-.../chi-begreper/` → `part02-.../ch<XX>-begreper/`
2. **Rename files if numbering scheme changes:**
   - `chi-begreper.tex` → `ch<XX>-begreper.tex` (roman to arabic or vice versa)
3. **Update chapter file `\documentclass` path if depth changes** (usually same)
4. **Update source `part<NN>.tex`:** Remove `\subfile` line
5. **Update target `part<NN>.tex`:** Add `\subfile` line at end (or use INSERT workflow if specific position)

---

## Section Operations

Sections are files within a chapter folder.

### NEW SECTION

**Triggers:**
- "new section"
- "add section"
- "create section in chapter..."
- "add section about..."

**Required information:**
- Target part and chapter
- Slug (e.g., "methodology")
- Title (e.g., "Methodology")

**Behavior:** Appends new section after all existing sections in the chapter with next available number.

**Files to CREATE:**

1. **Section file:** `ch<XX>-<chapter-slug>/sec<NN>-<section-slug>.tex`

   ```latex
   \documentclass[../../../main.tex]{subfiles}
   \begin{document}

   \section{<Section Title>}
   \label{sec:<chapter-slug>:<section-slug>}

   % [PROMPT: Section content]

   \end{document}
   ```

**Files to MODIFY:**

1. **Chapter file `ch<XX>-<chapter-slug>.tex`:**
   - Append `\subfile{sec<NN>-<section-slug>.tex}` before `\ifSubfilesClassLoaded` block

---

### INSERT SECTION

**Triggers:**
- "insert section before X"
- "insert section at position X"
- "insert section X" (means insert BEFORE existing section X)
- "add section before section X"

**Required information:**
- Target chapter
- Position to insert BEFORE (e.g., "section 3", "sec03")
- Slug (e.g., "background")
- Title (e.g., "Background")

**Behavior:** Inserts new section BEFORE the specified position. All sections from that position onwards are renumbered.

**Example:** If sec01, sec02, sec03 exist and user says "insert section 2":
- New section becomes sec02
- Old sec02 becomes sec03
- Old sec03 becomes sec04

**Workflow:**

1. **Identify sections to renumber:** sec02, sec03... → sec03, sec04...

2. **Rename in reverse order (highest first to avoid conflicts):**
   - For each section from highest to insertion point:
     - Rename file: `sec<NN>-<slug>.tex` → `sec<NN+1>-<slug>.tex`
     - Update inside section file:
       - `\label{sec:<chapter>:<slug>}` stays same (uses slug, not number)

3. **Update chapter file:**
   - Update all `\subfile{sec<NN>-...}` lines for renumbered sections

4. **Create new section at the insertion position**

5. **Update chapter file:**
   - Insert new `\subfile` line at correct position

---

### RENAME SECTION

**Triggers:**
- "rename section"
- "change section name"
- "update section title"
- "section X should be called..."

**Required information:**
- Current section identifier
- New slug (optional)
- New title (optional)

**Files to MODIFY:**

1. **Rename file:** `sec<NN>-<old-slug>.tex` → `sec<NN>-<new-slug>.tex`
2. **Update section file content:**
   - `\label{sec:<chapter>:<old-slug>}` → `\label{sec:<chapter>:<new-slug>}`
   - `\section{Old Title}` → `\section{New Title}` if title changes
3. **Update chapter file:**
   - `\subfile{sec<NN>-<old-slug>.tex}` → `\subfile{sec<NN>-<new-slug>.tex}`

**Cross-reference updates (search entire project):**
- Update any `\ref{sec:<chapter>:<old-slug>}` references

---

### DELETE SECTION

**Triggers:**
- "delete section"
- "remove section"
- "get rid of section"

**Files to DELETE:**

1. **Section file:** `sec<NN>-<slug>.tex`

**Files to MODIFY:**

1. **Chapter file:** Remove `\subfile{sec<NN>-<slug>.tex}` line

**Note:** Deleting does NOT automatically renumber remaining sections. Gaps in numbering are allowed.

---

## Appendix Operations

Appendices exist in backmatter with prefix `appNN-`.

### NEW APPENDIX

**Triggers:**
- "new appendix"
- "add appendix"
- "create appendix called..."

**Required information:**
- Slug (e.g., "formulas")
- Title (e.g., "Mathematical Formulas")

**Behavior:** Appends new appendix after all existing appendices with next available number.

**Files to CREATE:**

1. **Folder:** `latex/300-backmatter/app<NN>-<slug>/`
2. **Appendix file:** `app<NN>-<slug>/app<NN>-<slug>.tex`

   ```latex
   \documentclass[../../main.tex]{subfiles}
   \begin{document}

   \chapter{<Appendix Title>}
   \label{app:<slug>}

   % [PROMPT: Appendix content]

   \end{document}
   ```

**Files to MODIFY:**

1. **`backmatter.tex`:**
   - Append `\subfile{app<NN>-<slug>/app<NN>-<slug>.tex}` after existing appendices

---

### INSERT APPENDIX

**Triggers:**
- "insert appendix before X"
- "insert appendix at position X"
- "insert appendix X"

**Behavior:** Same pattern as INSERT CHAPTER - inserts BEFORE specified position, renumbers all subsequent appendices.

**Workflow:** Same as INSERT CHAPTER but for appendices in backmatter.

---

### RENAME APPENDIX

**Triggers:**
- "rename appendix"
- "change appendix name"
- "update appendix title"

**Files to MODIFY:**

1. **Rename folder:** `app<NN>-<old-slug>/` → `app<NN>-<new-slug>/`
2. **Rename file:** `app<NN>-<old-slug>.tex` → `app<NN>-<new-slug>.tex`
3. **Update file content:** label, title
4. **Update `backmatter.tex`:** `\subfile` path

---

### DELETE APPENDIX

**Triggers:**
- "delete appendix"
- "remove appendix"

**Files to DELETE:**

1. **Entire folder:** `app<NN>-<slug>/` (recursive)

**Files to MODIFY:**

1. **`backmatter.tex`:** Remove `\subfile` line

---

## Frontmatter Operations

Frontmatter files use numeric prefixes (100, 110, 120...).

### NEW FRONTMATTER ITEM

**Triggers:**
- "new frontmatter item"
- "add to frontmatter"
- "add contributors page"
- "add dedication page"

**Required information:**
- Slug (e.g., "contributors")
- Title (e.g., "Contributors")

**Behavior:** Appends new item with next available number (in 10-unit increments: 100, 110, 120...).

**Files to CREATE:**

1. **File:** `latex/100-frontmatter/<NNN>-<slug>.tex`

   ```latex
   \documentclass[../main.tex]{subfiles}
   \begin{document}

   \chapter*{<Title>}
   \addcontentsline{toc}{chapter}{<Title>}

   % [PROMPT: Content]

   \end{document}
   ```

**Files to MODIFY:**

1. **`frontmatter.tex`:**
   - Append `\subfile{<NNN>-<slug>.tex}` at end

---

### INSERT FRONTMATTER ITEM

**Triggers:**
- "insert frontmatter before X"
- "insert page before preface"
- "add dedication before about"

**Behavior:** Inserts BEFORE specified item. May require renumbering if no gap exists.

**Note:** Frontmatter uses 10-unit increments (100, 110, 120) to allow insertions without renumbering. If inserting between 110 and 120, use 115. Only renumber if no gap exists.

---

### DELETE FRONTMATTER ITEM

**Triggers:**
- "delete frontmatter item"
- "remove preface"
- "remove acknowledgements"

**Files to DELETE:**

1. **File:** `<NNN>-<slug>.tex`

**Files to MODIFY:**

1. **`frontmatter.tex`:** Remove `\subfile` line

---

## Reordering Operations

Complex operations that require renumbering multiple elements.

### SWAP TWO SECTIONS

**Triggers:**
- "swap sections"
- "switch section X and Y"
- "exchange sections"

**Required information:**
- Chapter containing the sections
- Two section identifiers to swap

**Workflow:**

1. **Temporary rename to avoid conflicts:**
   - `sec02-<slug-a>.tex` → `sec02-<slug-a>.tex.tmp`

2. **Rename files:**
   - `sec05-<slug-b>.tex` → `sec02-<slug-b>.tex`
   - `sec02-<slug-a>.tex.tmp` → `sec05-<slug-a>.tex`

3. **Update labels inside files** (if they include numbers)

4. **Update chapter aggregator:**
   - Reorder `\subfile{}` lines to match new numeric order

---

### SWAP TWO CHAPTERS

**Triggers:**
- "swap chapters"
- "switch chapter X and Y"
- "exchange chapters"

**Similar to sections but:**
- Rename folders and all contained files
- Update part aggregator
- More complex for cross-references

---

### MOVE SECTION TO ANOTHER CHAPTER

**Triggers:**
- "move section to chapter"
- "transfer section"
- "relocate section"

**Required information:**
- Source chapter
- Section to move
- Target chapter

**Workflow:**

1. **Determine target section number** (next available in target chapter)
2. **Move file:** `source-chapter/sec<NN>-<slug>.tex` → `target-chapter/sec<MM>-<slug>.tex`
3. **Update section file:**
   - `\label{sec:<source-chapter>:...}` → `\label{sec:<target-chapter>:...}`
4. **Update source chapter:** Remove `\subfile` line
5. **Update target chapter:** Append `\subfile` line at end
6. **Update cross-references** throughout project

---

## Validation Checklist

After any operation, verify:

- [ ] All `\subfile{}` paths are correct
- [ ] All `\documentclass[...]{subfiles}` paths are correct depth
- [ ] All `\label{}` commands are unique
- [ ] All `\ref{}` and `\hyperref[]` commands point to valid labels
- [ ] Numeric ordering is consistent (no duplicates; gaps allowed)
- [ ] Folder names match file names (folder `ch01-x` contains `ch01-x.tex`)
- [ ] `\graphicspath` points to correct figures folder
- [ ] Project compiles without errors: `book compile`

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| File exists | Target name already in use | Choose different name or delete existing first |
| Folder not empty | Trying to delete non-empty element | Confirm with user or delete children first |
| Invalid number | Number out of range or wrong format | Use correct format (01-99 for arabic, i-xii for roman) |
| Parent not found | Part/chapter doesn't exist | Create parent element first |
| Broken reference | Label referenced but not defined | Update or remove stale references |

### Recovery

If an operation fails mid-way:
1. Check git status for partial changes
2. Use `git checkout .` to revert all changes
3. Fix the issue and retry the operation

---

## Quick Reference

| Action | Trigger Keywords | Behavior |
|--------|-----------------|----------|
| NEW X | "new X", "add X", "create X" | Appends at end with next number |
| INSERT X | "insert X before", "insert X at position" | Inserts BEFORE position, renumbers subsequent |
| RENAME X | "rename X", "change X name", "update X title" | Changes slug/title, updates references |
| DELETE X | "delete X", "remove X", "get rid of X" | Removes item, no renumbering |
| MOVE X | "move X to", "transfer X", "relocate X" | Moves between containers |
| SWAP X | "swap X", "switch X and Y", "exchange X" | Exchanges positions of two items |


### Issue: Everything numbered under "1.x"

**Cause:** Document title is a level-1 heading (`# Title`)

**Solution:** Move title to YAML front matter
```yaml
---
title: Document Title
---

## First Section    ← Now correctly Section 1, not 1.1
```

### Issue: Tables breaking across pages

**Solution:** Add compact spacing in LaTeX preamble (see "LaTeX Customization" above)

### Issue: ToC too detailed

**Solution:** Reduce `--toc-depth` from 3 to 2

### Issue: Multi-digit subsection numbers overlap with titles in ToC

**Problem:** Section numbers like "2.5.10", "2.5.11" overlap with section titles in Table of Contents

**Cause:** Default LaTeX allocates only 2.3em for subsection numbers, insufficient for multi-digit numbers

**Solution:** Add to LaTeX preamble using `tocloft` package
```latex
\usepackage{tocloft}
\setlength{\cftsecnumwidth}{2.5em}      % Section numbers (1, 2, 3)
\setlength{\cftsubsecnumwidth}{3.5em}   % Subsection numbers (2.1, 2.5.10)
\setlength{\cftsubsubsecnumwidth}{4.5em} % Subsubsection numbers (2.5.10.1)
```

**Result:** Proper spacing for all subsection number lengths

### Issue: Footnotes not appearing in References section

**Expected behavior:** Pandoc footnotes appear at bottom of each page (LaTeX standard)

**For consolidated references:** Use `--citeproc` with bibliography file instead of footnote syntax

### Issue: Font not found

**Common problem:** XeLaTeX requires system fonts

**Solution:** List available fonts:
```bash
fc-list | grep -i "dejavu"
```

**Or use standard LaTeX fonts:**
```bash
-V mainfont="Latin Modern Roman"
```

### Issue: Bullet Lists Rendering as Inline Text (CRITICAL)

**Problem:** Bullet lists appear as inline text with dashes instead of proper bullets (•)

**Bad Rendering:**
```
Multi-layer validation frameworks: - HTTP/API layer validation - Schema validation - Sanity checks...
```

**Expected Rendering:**
```
Multi-layer validation frameworks:
• HTTP/API layer validation
• Schema validation
• Sanity checks
```

**Root Cause:** LaTeX's default justified text alignment breaks Pandoc-generated bullet list structures.

LaTeX's justification algorithm tries to make every line the same width by:
1. Adding/removing inter-word spaces
2. Hyphenating words
3. Sometimes **reflowing line breaks** in ways that break Pandoc's list structures

When a list appears after a paragraph ending with a colon (common pattern), the justification algorithm may:
- Merge list items onto previous lines
- Convert bullet markers (`-`) into inline dashes
- Collapse vertical list structure into horizontal flow

**Solution:** Always include `\raggedright` in LaTeX preamble

The canonical build script includes this automatically:
```latex
% Use ragged-right (left-aligned) instead of justified text
% Justified text can create awkward spacing and break list structures
\raggedright
```

**Location:** `~/.claude/skills/pandoc-pdf-generation/assets/table-spacing-template.tex` (lines 89-90)

**Verification:**

Automated check for broken bullets (expect 0 matches):
```bash
pdftotext output.pdf - | grep -E '^\w.*: -'
```

Manual visual inspection:
- Open PDF in viewer
- Scan sections with bullet lists
- Verify bullets (•) appear, not inline dashes

**Prevention:**
1. ✅ Always use canonical build script: `~/.claude/skills/pandoc-pdf-generation/assets/build-pdf.sh`
2. ❌ Never create ad-hoc `pandoc` commands without LaTeX preamble
3. ✅ Verify all PDFs before presenting to users

**Why This Matters:** This issue only surfaces in production with certain text patterns. Ad-hoc Pandoc commands without proper LaTeX configuration will miss this critical requirement.

**Reference:** See [Core Principles](core-principles.md) for universal development patterns learned from this failure.

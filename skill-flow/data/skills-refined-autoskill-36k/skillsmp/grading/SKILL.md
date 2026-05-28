---
name: grading
description: Grade student submissions with intellectual rigor and pedagogical depth. Produce scores, teach clear thinking and effective writing, and provide actionable feedback.
---

# Grading

## Overview
You are grading as a demanding but intellectually generous mentor. Your feedback should not merely check boxes but teach students to think more clearly and write more effectively.

Your role is to:
- Apply rigorous analytical standards
- Connect errors to conceptual gaps and explain WHY issues matter
- Prepare students to defend their work to a skeptical audience
- Teach effective writing as a professional skill

## Feedback Voice & Pedagogy

### The Mentor Voice
Write feedback as a demanding but generous mentor would:

**Instead of:** "The analysis lacks specific numbers."
**Write:** "When you claim spending 'grew faster than the benchmark,' a skeptical reader would ask: how much faster? 2.1% vs 1.8% annually tells a different story than 6% vs 2%. Quantify the gap—it's the difference between 'interesting observation' and 'actionable insight.'"

**Instead of:** "More detail needed."
**Write:** "You've identified the pattern. But the interesting questions live in the mechanism: What drives this relationship? Understanding the mechanism lets you predict what happens under different conditions, which is what makes analysis valuable."

**Instead of:** "Use more precise terminology."
**Write:** "You write that the measure 'goes up when the economy goes down.' A single word—countercyclical—unlocks a framework. What mechanism drives the countercyclicality? Understanding this lets you explain, predict, and prescribe, rather than simply describe."

### Teaching Clear Thinking
Every piece of feedback should teach, not just correct:

1. **Explain the "so what"** - Why does this error matter?
2. **Connect to mechanisms** - What underlying forces produce the patterns they're describing?
3. **Link to course concepts** - Reference concepts from `references/course_concepts.md` if available
4. **Bridge to professional use** - How would a practitioner use this insight?

### Evaluating Writing Quality
Good writing is clear, concrete, and vigorous. When evaluating student prose, apply the principles from `references/economical_writing_principles.md` (REQUIRED - always read this file before grading).

**Look for these strengths to praise:**
- Active verbs driving the prose ("prices rose" not "an increase in prices occurred")
- Concrete examples illuminating abstract concepts ("bread" not "commodities")
- Plain language explaining complex ideas (confidence, not pretension)
- Natural voice that sounds like a smart person explaining, not a bureaucrat filing a report

**Address these issues with teaching-focused feedback:**
- **Nominalization** - verbs buried in nouns sap vigor ("There is a need for analysis" → "We must analyze")
- **Passive voice** - obscures who does what ("Prices were increased" → "The Fed raised prices")
- **Elegant variation** - using different words for the same thing causes confusion
- **Boilerplate** - "This paper discusses..." openings, table-of-contents paragraphs, excessive summary
- **Abstract language** - when concrete examples would clarify

**Frame writing feedback around WHY it matters:**
- Unclear writing suggests unclear thinking to readers (including employers and clients)
- Readers who stumble stop reading—your brilliant analysis dies unread
- Plain language demonstrates confidence in your ideas; jargon suggests you're hiding behind it
- The goal is communication, not display—you're explaining to smart people, not impressing them

### Presentation Preparation (if applicable)
If students will present their findings, feedback should prepare them to:
- Anticipate tough questions from the audience
- Defend their methodology and conclusions
- Translate academic analysis into executive-ready insights
- Know what they can claim confidently vs. where they're speculating

## Workflow

### 1) Collect inputs
- Require the student submission files (may include Word/PDF papers, Excel workbooks, or other formats).
- Load the rubric from `rubric.md` (in the assignment root folder).
- Load the assignment requirements from `assignment.md` (in the assignment root folder).
- Load economical writing principles from `references/economical_writing_principles.md` (REQUIRED).
- Load course concepts from `references/course_concepts.md` (if available).
- If any required inputs are missing, request them and do not guess.

### 1a) Check for Turnitin reports (if present)
Check for Turnitin similarity reports in these locations:
- `turnitin/` subfolder in the assignment root
- Any file in `submissions/` with "turnitin" in the filename (case-insensitive)

**If Turnitin reports are found:**
- Read and incorporate the similarity findings into feedback
- Note the overall similarity percentage and flagged passages
- Frame feedback pedagogically: teach proper citation, paraphrasing vs. quoting, and when common phrases are acceptable matches
- Do NOT treat similarity scores as automatic evidence of misconduct—explain what the matches mean and how to address legitimate concerns

**If no Turnitin reports are found:**
- Proceed without Turnitin integration (instructor chose not to include it for this student)

### 1b) Identify submission versions (handle multiple submissions)
Canvas exports use this naming convention:
```
username_assignmentID_submissionID_originalFilename
```
Example: `smithjohn_179254_21003078_Final_Paper.pdf`

**To identify versions:**
1. Group files by username (first segment before the first underscore)
2. Within each group, the submission ID (third number) indicates version order—higher = later
3. The submission with the highest submission ID is the **final version** to grade

**If multiple submissions exist for a student:**
1. Identify all prior versions
2. Look for prior grading reports in the assignment root (files matching `grading_report_*.md`)
3. If prior feedback exists, note which recommendations were or were not addressed in the revision
4. Grade based on the **final submission only**, but include a revision assessment section

**If only one submission exists:**
- Proceed with standard grading (no revision comparison needed)

### 2) Extract evidence (text + visuals)
- Run `scripts/extract_submission_text.py` to extract DOCX text, XLSX formulas/labels, embedded Excel objects in DOCX, and PDF text.
- If PDF text is sparse, the script automatically runs OCR (tesseract) on page images.
- If Excel files are present, render charts to images for visual review:
  - Preferred: `scripts/render_xlsx_excel.py --input <dir> --out <dir>` (requires Terminal to control Excel via Automation permissions).
  - Fallback: `scripts/render_xlsx_quicklook.py --input <dir> --out <dir>` (Quick Look preview images).
- Note any files that still fail extraction and mark scores as provisional where needed.

### 3) Evaluate against assignment requirements
Check each required section as specified in `assignment.md`. Note:
- Which requirements are fully met
- Which are partially met (with specific gaps)
- Which are missing entirely

### 4) Score the rubric
Assign scores for each criterion using the definitions in `rubric.md`.

When evidence is ambiguous or missing, score conservatively and explain what is missing.
Calculate the total according to the rubric's point allocations.

### 5) Deliver feedback
Structure feedback to teach clear thinking and effective writing:

**Analytical Feedback:**
- Identify 2-3 places where deeper reasoning would strengthen the submission
- Connect errors to underlying conceptual gaps (not just "wrong" but "here's what you're missing")
- Highlight where the student showed genuine insight

**Writing Quality Feedback:**
- Where does clear writing support the analysis?
- Where does unclear writing obscure or undermine it?
- Frame around professional impact, not pedantic correction

**Concrete Fixes:**
- Specific, actionable items to improve the submission
- Prioritized by impact on quality

## Output Format

```markdown
# [Student Name] - Assignment Feedback

## Score: [X]/[Total] ([Letter Grade if applicable])

### Rubric Breakdown
| Criterion | Score | Assessment |
|-----------|-------|------------|
| [Criterion 1 from rubric] | X/Y | [One sentence] |
| [Criterion 2 from rubric] | X/Y | [One sentence] |
| [Additional criteria...] | X/Y | [One sentence] |

---

## What You Did Well
[Highlight genuine strengths - be specific about what demonstrates good thinking AND good writing (active verbs, concrete examples, clear explanations)]

---

## Developing Your Analysis

### [Issue 1 Title - e.g., "Quantifying the Relationship"]
[Teaching-focused feedback that explains WHY this matters, connects to course concepts if available, and shows how a stronger analysis would look]

### [Issue 2 Title - e.g., "Understanding the Mechanism"]
[Teaching-focused feedback...]

### [Issue 3 if needed]
[Teaching-focused feedback...]

---

## Strengthening Your Writing
[If the submission has notable writing issues, address 1-2 here with the same teaching focus. Explain WHY clear writing matters for their career—not as grammar police, but as a mentor explaining that unclear writing suggests unclear thinking to employers, clients, and colleagues. Use specific examples from their submission. If the writing is strong, briefly acknowledge what works well instead.]

---

## Preparing Your Presentation (if applicable)

**Your Central Insight:** [The one finding that should anchor their presentation]

**The Question You'll Get:** [The tough question they should prepare for, and how to answer it]

**Your Strongest Visual:** [Which figure/table to feature and how to present it]

**Executive Summary Version:** [How to describe their findings in 30 seconds to a non-specialist]

---

## Required Revisions
1. [Specific fix with clear instruction]
2. [Specific fix with clear instruction]
3. [Specific fix with clear instruction]

---

## Optional Enhancements (For Excellent Work)
- [Suggestion that would elevate the analysis]
- [Suggestion that would elevate the analysis]

---

## Turnitin Review (Include only if Turnitin report was provided)
**Similarity Score:** [X%]

**What the Matches Mean:**
[Explain which matches are concerning vs. benign (common phrases, properly cited quotations, bibliography entries). Teach proper paraphrasing and citation practices.]

**Action Items:**
- [Specific passages to rephrase or properly cite]
- [Guidance on paraphrasing techniques if needed]

---

## Revision Assessment (Include only if this is a resubmission)
**Comparing to:** [Prior submission ID/date]

**Feedback Addressed:**
- ✓ [Recommendation from prior feedback that was addressed, with brief note on how]
- ✓ [Another addressed item]

**Feedback Not Yet Addressed:**
- ✗ [Recommendation that remains unaddressed]
- ✗ [Another unaddressed item, with guidance on why it still matters]

**Revision Quality:** [Brief assessment of how thoughtfully the student engaged with prior feedback—did they make surface-level fixes or genuinely improve their analysis?]
```

## Resources

### scripts/
- `scripts/extract_submission_text.py`: Extract DOCX text, XLSX formulas/labels, PDF text; uses OCR for image-based PDFs.
- `scripts/render_xlsx_excel.py`: Convert XLSX to PDF/PNG via Microsoft Excel for chart review.
- `scripts/render_xlsx_quicklook.py`: Convert XLSX to PNG using Quick Look when Excel automation is unavailable.

### references/
- `references/economical_writing_principles.md` for evaluating writing quality (clarity, concreteness, vigor).
- `references/course_concepts.md` (optional) for course-specific concepts to reference in feedback.

### Assignment root folder
- `rubric.md` for scoring criteria specific to this assignment.
- `assignment.md` for required sections and expectations specific to this assignment.

---
name: report-evaluation
description: Evaluate student assignment reports using three independent reviewers for consensus grading. Each reviewer reads the PDF and context files independently, then provides section assessments in Swedish. Results compiled with majority voting into GRADING-RESULTS.md. Use when grading prepared student submissions.
allowed-tools: Read, Write, Edit, Glob, Task, AskUserQuestion, WebFetch
triggers:
  - evaluate reports
  - grade assignments
  - student grading
  - assessment
---

# Report Evaluation Skill

Evaluate student reports using three independent reviewers for reliable consensus grading.

## Critical: Before Starting

**MUST READ from skill folder:**

1. Read `FEEDBACK-EXAMPLES.md` - Swedish feedback tone and style
2. Read `OUTPUT-FORMAT.md` - Expected output structure

## Session Recovery with EVALUATION-STATUS.json

**Critical: This skill uses EVALUATION-STATUS.json to track progress and survive compacting events.**

The status file enables:
- **Resumption** - Pick up exactly where you left off after compacting
- **Progress visibility** - Clear tracking of what's done and what remains
- **Incremental writes** - Results saved after each batch (not lost on compaction)
- **Batch management** - Pre-planned batches of 3 students each

### Status File Structure

```json
{
  "evaluation_session": {
    "assignment": "Assignment Name",
    "assignment_folder": "/full/path/to/assignment",
    "started": "YYYY-MM-DD",
    "last_updated": "YYYY-MM-DD",
    "status": "in_progress|completed",
    "batch_size": 3
  },
  "files": {
    "grading_results": "GRADING-RESULTS.md",
    "student_list": "STUDENT-LIST.md",
    "assignment": "ASSIGNMENT.md",
    "course_description": "/path/to/COURSE-DESCRIPTION.md",
    "background": "BACKGROUND.md",
    "special_considerations": "SPECIAL-CONSIDERATIONS.md",
    "student_reports_folder": "student-reports/"
  },
  "progress": {
    "total_students": 0,
    "submitted_reports": 0,
    "missing_reports": 0,
    "evaluated": 0,
    "remaining": 0
  },
  "batches": {
    "batch_1": {
      "status": "completed|in_progress|pending",
      "students": [
        {"name": "Student Name", "file": "lastname_firstname_rapport.pdf"}
      ],
      "results": {"VG": 0, "G": 0}
    }
  },
  "completed_evaluations": [
    {"name": "Student Name", "grade": "G", "consensus": "3/3"}
  ],
  "missing_submissions": ["Student Name"],
  "next_batch": "batch_N"
}
```

### Recovery Behavior

**On skill invocation:**
1. Check for existing `EVALUATION-STATUS.json` in assignment folder
2. If found: Read status and continue from `next_batch`
3. If not found: Initialize new session (Step 1)

## Assignment Folder Structure

Each assignment folder contains the context needed for evaluation. Most files must be in the assignment folder, but some (like COURSE-DESCRIPTION.md) can be shared in parent folders.

### Required Files in Assignment Folder

| File | Purpose | Search Behavior |
|------|---------|-----------------|
| `STUDENT-LIST.md` | Roster with submission status and grades | Assignment folder only |
| `ASSIGNMENT.md` | The assignment instructions (defines sections to evaluate) | Assignment folder only |
| `COURSE-DESCRIPTION.md` | Formal course criteria and learning objectives | **Parent folders up to project root** |
| `BACKGROUND.md` | Project scenario and learning context | Assignment folder only |
| `SPECIAL-CONSIDERATIONS.md` | Exceptions and adjustments for this assignment | Assignment folder only |
| `EVALUATION-STATUS.json` | Progress tracking (created/updated by skill) | Assignment folder only |
| `student-reports/` | Folder containing renamed PDFs | Assignment folder only |

### File Relationships

```
project-root/
├── COURSE-DESCRIPTION.md    # Can live here (shared across assignments)
└── assignments/
    ├── COURSE-DESCRIPTION.md    # Or here (shared across assignments)
    └── assignment-N/
        ├── COURSE-DESCRIPTION.md    # Or here (assignment-specific)
        ├── STUDENT-LIST.md          # WHO to evaluate
        ├── ASSIGNMENT.md            # WHAT to look for (report sections)
        ├── BACKGROUND.md            # WHY (context, scenario)
        ├── SPECIAL-CONSIDERATIONS.md # EXCEPTIONS (what's adjusted)
        ├── GRADING-RESULTS.md       # OUTPUT (created/updated by skill)
        └── student-reports/
            └── *.pdf                # Student submissions
```

**COURSE-DESCRIPTION.md search order:** Assignment folder → parent folder → grandparent → ... → project root. Uses the first one found.

## Core Tone Principles

**All feedback must be framed positively.** Never use negative critique.

When writing feedback, imagine you are actually saying this to the student face-to-face. Ask yourself: "Would I actually say this?" If it sounds bureaucratic, rewrite it.

| Principle | Description |
|-----------|-------------|
| **Face-to-face test** | The feedback should feel like something you'd actually say to the student in person |
| **Positive framing** | Frame everything positively - never mention what's missing or lacking |
| **Genuine enthusiasm** | Show real enthusiasm when something is good ("Riktigt snyggt!", "Kul att se...") |
| **Natural Swedish** | Use conversational language, not formal report language |

## Three-Reviewer Method

Each student report is evaluated by **three independent subagents in parallel**:

| Benefit | Explanation |
|---------|-------------|
| **Reliability** | Multiple perspectives reduce bias |
| **Consensus validation** | Unanimous vs split decisions visible |
| **Better feedback** | Select best feedback from variety |

### Consensus Rules

| Voting Pattern | Final Grade |
|----------------|-------------|
| 3/3 unanimous | Reviewer grade |
| 2/3 majority | Majority grade |
| 1/1/1 split | Flag for instructor review |

## Evaluation Workflow

### Step 0: Check for Existing Session

**Before anything else, check if a session already exists.**

1. Look for `EVALUATION-STATUS.json` in the assignment folder
2. **If found with status "in_progress":**
   - Display: `Resuming evaluation session from [last_updated]`
   - Display current progress from status file
   - Skip to Step 3 and continue from `next_batch`
3. **If found with status "completed":**
   - Display: `Previous session completed. Starting fresh evaluation.`
   - Proceed to Step 0.5 (validate inputs)
4. **If not found:**
   - Display: `No existing session. Starting new evaluation.`
   - Proceed to Step 0.5 (validate inputs)

**Resume display format:**
```
## Resuming Evaluation Session

Assignment: [assignment name]
Last updated: [date]
Progress: [evaluated]/[total] students evaluated

Completed batches: [N]
Next batch: [batch_N] with [3] students

Continuing evaluation...
```

### Step 0.5: Validate Input Files

**Before starting evaluation, check that all required input files exist.**

**Standard files** - Check in assignment folder only:
1. `STUDENT-LIST.md`
2. `ASSIGNMENT.md`
3. `BACKGROUND.md`
4. `SPECIAL-CONSIDERATIONS.md`
5. `student-reports/*.pdf` (at least one PDF)

**Parent-searchable files** - Check assignment folder first, then parent folders up to project root:
1. `COURSE-DESCRIPTION.md` - Search upward until found

**If any files are missing**, display this table to the terminal:

```
## Missing Input Files

The following files are required for evaluation:

| File | Status | Search Location | Purpose |
|------|--------|-----------------|---------|
| STUDENT-LIST.md | [Found/MISSING] | Assignment folder | Roster with student names, submission status, and grade column |
| ASSIGNMENT.md | [Found/MISSING] | Assignment folder | Assignment instructions - defines report sections and weights |
| COURSE-DESCRIPTION.md | [Found at: path / MISSING] | Parent folders → root | Formal course learning objectives and G/VG criteria |
| BACKGROUND.md | [Found/MISSING] | Assignment folder | Project scenario and learning context |
| SPECIAL-CONSIDERATIONS.md | [Found/MISSING] | Assignment folder | Exceptions and adjustments for this assignment |
| student-reports/*.pdf | [N found/MISSING] | Assignment folder | Student report PDFs to evaluate |
```

Then use **AskUserQuestion** to ask:

> "Some required input files are missing. Do you want to continue anyway?"
> - Options: "Yes, continue with available files" / "No, stop and fix missing files"

**If all files are present**, display a brief confirmation:

```
## Input Validation Passed

All required files found in [assignment-folder]:
- STUDENT-LIST.md
- ASSIGNMENT.md
- COURSE-DESCRIPTION.md
- BACKGROUND.md
- SPECIAL-CONSIDERATIONS.md
- student-reports/ (N PDFs found)

Proceeding with evaluation...
```

### Step 1: Load Context Files

Read all context files, using the paths determined in Step 0.5:

```
[assignment-folder]/ASSIGNMENT.md             # Report structure and sections
[found-path]/COURSE-DESCRIPTION.md            # Formal G/VG criteria (may be in parent folder)
[assignment-folder]/BACKGROUND.md             # Project context
[assignment-folder]/SPECIAL-CONSIDERATIONS.md # Exceptions
```

**Note:** COURSE-DESCRIPTION.md path comes from the parent folder search in Step 0.5. Pass this resolved path to reviewer subagents.

From these files, extract:
- **Sections to evaluate** (from ASSIGNMENT.md)
- **Section weights** (from ASSIGNMENT.md)
- **Pass (G) criteria** (from COURSE-DESCRIPTION.md)
- **Distinction (VG) criteria** (from COURSE-DESCRIPTION.md)
- **Which sections can earn VG** (from BACKGROUND.md or COURSE-DESCRIPTION.md)

### Step 2: Build Student List

Read `[assignment-folder]/STUDENT-LIST.md` and identify:
- Students with "Report Submitted: Yes"
- Students without a grade in "Betyg" column

### Step 2.5: Initialize or Update EVALUATION-STATUS.json

**For new sessions only** (skip if resuming from existing session):

Create `EVALUATION-STATUS.json` with:
- Session metadata (assignment name, folder, date, batch_size: 3)
- File paths for all context files
- Progress counters (all starting at 0)
- Pre-planned batches (groups of 3 students each)
- Empty completed_evaluations array
- Missing submissions list
- next_batch set to "batch_1"

```json
{
  "evaluation_session": {
    "assignment": "[from ASSIGNMENT.md title]",
    "assignment_folder": "[full path]",
    "started": "[today's date]",
    "last_updated": "[today's date]",
    "status": "in_progress",
    "batch_size": 3
  },
  ...
}
```

**Write the initial status file before starting any evaluations.**

### Step 3: Parallel Batch Evaluation

**Batch size:** Maximum 3 students per batch. This smaller batch size enables:
- Faster recovery after compacting events
- More frequent progress saves
- Lower risk of losing work

#### 3a. Create Batches

```
students_to_evaluate = [students with submitted reports but no grade]
batches = split into groups of max 3 students
```

**Example for 28 students:**
- batch_1: students 1-3
- batch_2: students 4-6
- ...
- batch_10: students 28 (1 student in final batch)

#### 3b. For Each Batch: Spawn All Reviewers in Parallel

For a batch of N students (max 3), spawn **N × 3 = up to 9 subagents in parallel**.

Each subagent receives the same prompt (see `REVIEWER-PROMPT.md`) instructing them to:
1. Read all context files from the assignment folder
2. Read and evaluate the student's PDF
3. **Follow any code repository links** (GitHub, GitLab, etc.) found in the report
4. Assess each section defined in ASSIGNMENT.md
5. Determine overall grade based on COURSE-DESCRIPTION.md criteria
6. Write feedback in Swedish

**Spawning pattern for batch:**
```
# Single message with all Task calls for the batch (max 9 parallel tasks):
Task: Student 1 - Reviewer 1
Task: Student 1 - Reviewer 2
Task: Student 1 - Reviewer 3
Task: Student 2 - Reviewer 1
Task: Student 2 - Reviewer 2
Task: Student 2 - Reviewer 3
Task: Student 3 - Reviewer 1
Task: Student 3 - Reviewer 2
Task: Student 3 - Reviewer 3
```

#### 3c. Collect All Results

Wait for **all subagents in the batch** to complete before proceeding. Each returns:
- Student name (to match results)
- Grade (G or VG)
- Section assessments (term + comment for each section)
- Feedback (3 sentences in Swedish)
- Reasoning (brief justification)

#### 3d. Process Results for Each Student

For each student in the batch, apply consensus:

**Majority voting:**
```
If all 3 agree: Final grade = reviewer grade (unanimous)
If 2/3 agree: Final grade = majority grade (majority)
If all different: Flag for manual review (split)
```

**Select best feedback** from the 3 options:
1. Most warm and encouraging
2. Most specific to student's work
3. Most natural Swedish (not bureaucratic)

#### 3e. Batch Write Results

After processing all students in the batch:

1. **Append all evaluations** to `GRADING-RESULTS.md` in one write operation
2. **Update all grades** in `STUDENT-LIST.md` in one edit operation
3. **Update EVALUATION-STATUS.json** with batch completion

**Status file updates after each batch:**
```json
{
  "evaluation_session": {
    "last_updated": "[current date]"
  },
  "progress": {
    "evaluated": [previous + batch count],
    "remaining": [previous - batch count]
  },
  "batches": {
    "[current_batch]": {
      "status": "completed",
      "results": {"VG": N, "G": M}
    }
  },
  "completed_evaluations": [
    // Append new evaluations
    {"name": "...", "grade": "...", "consensus": "..."}
  ],
  "next_batch": "[next_batch_key or null if done]"
}
```

This batch write approach:
- **Saves progress immediately** - Results survive compacting events
- Reduces file I/O operations
- Prevents partial state if interrupted
- Enables exact resumption from status file

#### 3f. Display Batch Summary

After each batch completes, display summary for all students in the batch:

```
## Batch 1/10 Complete (3 students)

| Student | Grade | Consensus |
|---------|-------|-----------|
| Andersson, Anna | VG | 3/3 |
| Eriksson, Erik | G | 2/3 |
| Johansson, Johan | VG | 3/3 |

✓ 3 evaluations saved to GRADING-RESULTS.md
✓ STUDENT-LIST.md updated with grades
✓ EVALUATION-STATUS.json updated (next: batch_2)

Progress: 3/28 students evaluated (10.7%)
```

#### 3g. Continue with Next Batch

If more batches remain, repeat steps 3b-3f for the next batch.

**Important:** Each batch is self-contained. If a compacting event occurs:
1. The skill will restart from Step 0
2. Status file will show which batch to resume
3. Only the current incomplete batch needs re-evaluation
4. All previously completed batches are preserved

### Step 4: Mark Session Complete and Display Final Summary

After all batches complete:

1. **Update EVALUATION-STATUS.json** to mark session completed:
```json
{
  "evaluation_session": {
    "status": "completed",
    "last_updated": "[current date]"
  },
  "next_batch": null
}
```

2. **Display overall progress:**

```
## Evaluation Complete

**Total students evaluated:** [N]
**Batches processed:** [M] (batch size: 3)

| Grade | Count |
|-------|-------|
| VG | [X] |
| G | [Y] |

**Consensus quality:**
- Unanimous (3/3): [N]
- Majority (2/3): [N]
- Split (flagged): [N]

✓ EVALUATION-STATUS.json marked as completed

Proceeding to generate summary tables...
```

### Step 5: Generate Summary Tables

After all students are evaluated, add **two summary sections** to GRADING-RESULTS.md:

#### 5a. Compact Assessment Overview Table

Create a table showing all evaluated students with their grades and section assessments at a glance. This table should:

1. **Use abbreviated section names** derived from ASSIGNMENT.md (e.g., "Teknisk arkitektur" → "Arkitektur", "Applikationsstack" → "Appstack")
2. **Include all students** sorted alphabetically by last name
3. **Show the consensus vote count** (e.g., "3/3", "2/3", or "Override" for instructor adjustments)
4. **Display section assessments** using the grading scale terms (Okej/Bra/Mycket bra/Utmärkt)

**Template format:**

```markdown
## Sammanfattning

| Student | Betyg | Röster | [Section1] | [Section2] | [Section3] | [Section4] | [Section5] | [Section6] |
|---------|-------|--------|------------|------------|------------|------------|------------|------------|
| Lastname, Firstname | VG | 3/3 | Bra | Mycket bra | Bra | Mycket bra | Bra | Mycket bra |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Column guidelines:**
- **Student**: "Lastname, Firstname" format for easy alphabetical sorting
- **Betyg**: Final grade (G or VG)
- **Röster**: Vote count (3/3, 2/3) or "Override" if instructor adjusted
- **Section columns**: Use the most representative assessment from the three reviewers (majority or most common)

#### 5b. Statistics Summary

After the compact table, add statistical summaries:

```markdown
# Summary Statistics

## Grade Distribution

| Grade | Count | Percentage |
|-------|-------|------------|
| **VG (Väl godkänt)** | [N] | [X]% |
| **G (Godkänt)** | [N] | [X]% |
| **Total Evaluated** | [N] | 100% |

### VG Recipients ([N] students)

| Student | Consensus | Notable Strength |
|---------|-----------|------------------|
| [Name] | 3/3 | [Key observation from evaluation] |
| ... | ... | ... |

### Consensus Breakdown

| Voting Pattern | Count |
|----------------|-------|
| Unanimous (3/3) | [N] |
| Majority (2/3) | [N] |
| Split (1/1/1) | [N] |

### Missing Submissions ([N] students)

- [Name]
- ...

---

*Evaluation completed: [DATE]*
*Method: Three-reviewer consensus grading*
*All feedback written in Swedish using du/din form*
```

#### 5c. Table Placement

The summaries should be placed at the **end** of GRADING-RESULTS.md, after all individual student evaluations. Structure:

```
# Grading Results - [Assignment Name]
[Individual student evaluations...]
---
## Sammanfattning
[Compact assessment overview table]
---
# Summary Statistics
[Statistics tables]
```

## Grading Scale Reference

| Swedish Term | English | Grade Level |
|--------------|---------|-------------|
| Okej | Okay | Pass minimum |
| Bra | Good | Solid pass |
| Mycket bra | Very Good | Distinction level |
| Utmärkt | Excellent | Beyond requirements |

| Grade | Swedish | Criteria |
|-------|---------|----------|
| G | Godkänt | All sections meet minimum |
| VG | Väl godkänt | G criteria + VG-eligible sections show deeper understanding |

## Single Student Evaluation

To evaluate just one student:

```
Evaluate the report for [Student Name] in [assignment-folder-path]
Use the three-reviewer method from report-evaluation skill.
```

## Batch Evaluation

To evaluate all remaining students:

```
Evaluate all ungraded students in [assignment-folder-path]
Use parallel batch mode (3 students per batch, 3 reviewers each).
Write results to GRADING-RESULTS.md, STUDENT-LIST.md, and EVALUATION-STATUS.json after each batch.
```

**Performance characteristics:**
- Up to 9 parallel subagents per batch (3 students × 3 reviewers)
- Results saved after each batch (survives compacting events)
- Automatic resumption from EVALUATION-STATUS.json
- Progress visible at each batch completion

**Resuming after compaction:**
```
Resume evaluation in [assignment-folder-path]
The EVALUATION-STATUS.json will be read automatically.
```

## Handling Split Decisions

If reviewers split 1/1/1 (e.g., G, VG, G with different reasoning):

1. Display all three assessments in terminal
2. Note the split in GRADING-RESULTS.md
3. Use majority grade but flag: `G (split - instructor review)`
4. Include all three feedback options for instructor to choose

## Quality Controls

Before completing:

- [ ] All students in STUDENT-LIST.md have grades
- [ ] GRADING-RESULTS.md has entry for each evaluated student
- [ ] EVALUATION-STATUS.json shows status: "completed"
- [ ] EVALUATION-STATUS.json progress matches actual evaluated count
- [ ] Summary table reflects all evaluations
- [ ] Split decisions flagged for review
- [ ] Feedback is in Swedish and uses "du/din"

## Privacy Note

GRADING-RESULTS.md and EVALUATION-STATUS.json contain student names and grades. They must be:

1. Added to `.gitignore`
2. Never committed to public repositories
3. Shared only with authorized instructors

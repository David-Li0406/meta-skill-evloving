---
name: docx-gen
description: "Generate professional DOCX documents from templates and structured data. Use for: (1) Lesson plans from SAT courseware data, (2) Trainee handbooks, (3) Course specification sheets, (4) Any template-based document generation. Integrates with sat-courseware skill for training materials. Triggers: lesson plan, handbook, document generation, DOCX, Word document, template, course specification, generate document."
---

# DOCX Generation Skill

## Purpose

Generate professional Microsoft Word documents (.docx) from templates and structured data. Primary use case is producing SAT-compliant training materials from Prometheus course data.

## Prerequisites

This skill works alongside:
- `/sat-courseware` - Provides data structure and validation rules
- `document-skills:docx` - Provides low-level DOCX manipulation

## Document Types

### 1. Lesson Plan

**Template:** `assets/templates/lesson_plan_template.docx`

**Data Source:** Course JSON → specific lesson object

**Structure:**
```
LESSON PLAN
├── Header Block
│   ├── Course Title          ← course.title
│   ├── Lesson Reference      ← lesson.id (e.g., "1.1.1.A")
│   ├── Lesson Title          ← lesson.title
│   ├── Duration              ← lesson.duration_minutes
│   ├── Type                  ← lesson.type (Theory/Practical)
│   └── Prerequisites         ← lesson.prerequisites[]
│
├── Learning Objectives
│   └── Bloom's-validated statements from CLO
│
├── Resources Required
│   ├── Equipment             ← lesson.equipment[]
│   ├── Materials             ← lesson.materials[]
│   └── References            ← lesson.references[]
│
├── Lesson Content
│   ├── Introduction (10-15% of time)
│   │   └── Hook, objectives review, relevance
│   ├── Main Body (70-80% of time)
│   │   ├── Teaching Point 1  ← lesson.teaching_points[0]
│   │   ├── Teaching Point 2  ← lesson.teaching_points[1]
│   │   └── ...
│   └── Summary (10-15% of time)
│       └── Key points, Q&A, preview next lesson
│
├── Assessment
│   └── Performance Criteria  ← lesson.performance_criteria[]
│
└── Instructor Notes
    └── lesson.instructor_notes
```

**Generation Command:**
```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_lesson_plan(course_data: dict, lesson_id: str, template_path: str, output_path: str):
    """
    Generate a lesson plan document from course data.

    Args:
        course_data: Full course JSON structure
        lesson_id: Lesson identifier (e.g., "1.1.1.A")
        template_path: Path to DOCX template
        output_path: Output file path
    """
    # Load template
    doc = Document(template_path)

    # Find lesson in course data
    lesson = find_lesson_by_id(course_data, lesson_id)
    clo = find_parent_clo(course_data, lesson_id)

    # Replace placeholders
    replace_placeholder(doc, "{{COURSE_TITLE}}", course_data["course"]["title"])
    replace_placeholder(doc, "{{LESSON_REF}}", lesson["id"])
    replace_placeholder(doc, "{{LESSON_TITLE}}", lesson["title"])
    replace_placeholder(doc, "{{DURATION}}", f"{lesson['duration_minutes']} minutes")
    replace_placeholder(doc, "{{LESSON_TYPE}}", lesson.get("type", "Theory"))
    replace_placeholder(doc, "{{CLO_STATEMENT}}", clo["statement"])

    # Generate teaching points
    for i, tp in enumerate(lesson.get("teaching_points", []), 1):
        replace_placeholder(doc, f"{{{{TP_{i}}}}}", tp)

    # Generate performance criteria
    pc_text = "\n".join(f"• {pc}" for pc in lesson.get("performance_criteria", []))
    replace_placeholder(doc, "{{PERFORMANCE_CRITERIA}}", pc_text)

    doc.save(output_path)
```

### 2. Trainee Handbook

**Template:** `assets/templates/trainee_handbook_template.docx`

**Structure:**
```
TRAINEE HANDBOOK
├── Cover Page
│   ├── Course Title
│   ├── Course Code
│   └── Version/Date
│
├── Table of Contents (auto-generated)
│
├── Course Overview
│   ├── Course Description
│   ├── Duration
│   ├── Target Audience
│   └── Prerequisites
│
├── Learning Outcomes
│   └── CLOs with explanations (one per section)
│
├── Module Breakdown
│   └── For each CLO:
│       ├── Topics
│       ├── Subtopics
│       └── Lesson summaries
│
├── Assessment Information
│   ├── Methods
│   ├── Grading criteria
│   └── Pass requirements
│
├── Key Concepts (Glossary)
│   └── Alphabetised definitions
│
└── Appendices
    ├── Forms
    ├── Checklists
    └── Reference materials
```

### 3. Course Specification Sheet

**Template:** `assets/templates/course_spec_template.docx`

**Structure:**
```
COURSE SPECIFICATION
├── Course Identification
│   ├── Title, Code, Level
│   └── Total Hours, Credits
│
├── Course Aims
│   └── High-level purpose statements
│
├── Course Learning Outcomes
│   └── Full CLO statements with cognitive levels
│
├── Syllabus Summary
│   └── Topic/Subtopic matrix
│
├── Assessment Strategy
│   ├── Methods and weightings
│   └── Pass criteria
│
├── Delivery Information
│   ├── Teaching methods
│   └── Contact hours breakdown
│
└── Quality Assurance
    ├── Review dates
    └── Approval signatures
```

## Placeholder Syntax

Use double curly braces for template placeholders:

| Placeholder | Source |
|-------------|--------|
| `{{COURSE_TITLE}}` | course.title |
| `{{COURSE_CODE}}` | course.code |
| `{{DURATION_HOURS}}` | course.duration_hours |
| `{{LESSON_REF}}` | lesson.id |
| `{{LESSON_TITLE}}` | lesson.title |
| `{{CLO_STATEMENT}}` | clo.statement |
| `{{CLO_LEVEL}}` | clo.cognitive_level |
| `{{TP_1}}`...`{{TP_N}}` | lesson.teaching_points[n] |
| `{{PERFORMANCE_CRITERIA}}` | lesson.performance_criteria (bulleted) |
| `{{GENERATED_DATE}}` | Current date |

## Styling Standards

### Fonts
| Element | Font | Size | Style |
|---------|------|------|-------|
| Document Title | Candara | 24pt | Bold |
| Section Heading | Candara | 14pt | Bold |
| Subsection | Candara | 12pt | Bold |
| Body Text | Candara | 11pt | Regular |
| Code/Data | Cascadia Code | 10pt | Regular |

### Colours
| Element | Hex | Usage |
|---------|-----|-------|
| Headings | #333333 | Section titles |
| Body | #333333 | Main text |
| Accent | #FF6600 | Highlights, callouts |
| Secondary | #767171 | Captions, notes |

### Spacing
- Paragraph spacing: 6pt after
- Line spacing: 1.15
- Section breaks: Page break before major sections
- Margins: 1 inch all sides (2.54cm)

## Validation Before Generation

Before generating any document, validate:

- [ ] All required placeholders have data
- [ ] Bloom's verbs match cognitive level (use sat-courseware validation)
- [ ] Duration totals are consistent
- [ ] Performance criteria are measurable
- [ ] No orphan elements in hierarchy

## Usage Pattern

```python
# 1. Load and validate course data
course_data = load_course_json("course.json")
validate_course_structure(course_data)  # From sat-courseware

# 2. Select document type and target
doc_type = "lesson_plan"
target_id = "1.1.1.A"

# 3. Generate document
if doc_type == "lesson_plan":
    generate_lesson_plan(
        course_data=course_data,
        lesson_id=target_id,
        template_path="assets/templates/lesson_plan_template.docx",
        output_path=f"output/lesson_plan_{target_id}.docx"
    )
elif doc_type == "handbook":
    generate_handbook(
        course_data=course_data,
        template_path="assets/templates/trainee_handbook_template.docx",
        output_path="output/trainee_handbook.docx"
    )

# 4. Confirm generation
print(f"Document generated: {output_path}")
```

## Integration with document-skills:docx

For complex operations, invoke the global docx skill:
- Tracked changes
- Comments
- Complex table formatting
- Mail merge operations

This skill focuses on Prometheus-specific template mapping.

## File Locations

| Asset | Path |
|-------|------|
| Templates | `core/templates/docx/` |
| Output | `output/documents/` |
| Course data | `data/courses/` |

## See Also

- `/sat-courseware` - Data structure and Bloom's validation
- `/pptx-gen` - Presentation generation
- `document-skills:docx` - Low-level DOCX operations

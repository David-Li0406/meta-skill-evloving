---
name: pptx-gen
description: "Generate professional PPTX presentations from course data and templates. Use for: (1) Lesson presentations with speaker notes, (2) Course overview decks, (3) Module summary slides, (4) Training visual aids. Integrates with sat-courseware for SAT-compliant content. Triggers: presentation, slides, PowerPoint, PPTX, speaker notes, training slides, lesson slides, course deck."
---

# PPTX Generation Skill

## Purpose

Generate professional Microsoft PowerPoint presentations (.pptx) from Prometheus course data. Creates SAT-compliant training slides with speaker notes, visual hierarchy, and consistent branding.

## Prerequisites

This skill works alongside:
- `/sat-courseware` - Provides data structure and Bloom's validation
- `document-skills:pptx` - Provides low-level PPTX manipulation

## Presentation Types

### 1. Lesson Presentation

**Template:** `assets/templates/lesson_presentation_template.pptx`

**Data Source:** Course JSON → specific lesson object

**Slide Structure:**
```
LESSON PRESENTATION
│
├── Slide 1: Title Slide
│   ├── Course Title (subtitle)
│   ├── Lesson Title (main)
│   ├── Lesson Reference (e.g., "Lesson 1.1.1.A")
│   ├── Instructor Name
│   └── Date
│   └── [Speaker Notes: Welcome, housekeeping, timing]
│
├── Slide 2: Learning Objectives
│   ├── Header: "By the end of this lesson, you will be able to:"
│   └── Bulleted objectives (Bloom's-validated)
│   └── [Speaker Notes: Read objectives, explain relevance]
│
├── Slide 3: Agenda/Overview
│   ├── Teaching points listed
│   └── Time allocation per section
│   └── [Speaker Notes: Preview structure, set expectations]
│
├── Slides 4-N: Teaching Point Slides
│   │   (One slide per major teaching point)
│   ├── Header: Teaching Point title
│   ├── Content: Key concepts, diagrams, examples
│   ├── Visual: Relevant image/diagram placeholder
│   └── [Speaker Notes: Detailed teaching content, examples, questions to ask]
│
├── Slide N+1: Activity/Exercise (if applicable)
│   ├── Activity title
│   ├── Instructions
│   ├── Time allocation
│   └── [Speaker Notes: Setup instructions, debrief points]
│
├── Slide N+2: Summary
│   ├── Header: "Key Takeaways"
│   ├── Bulleted summary of main points
│   └── [Speaker Notes: Reinforce key learning, check understanding]
│
├── Slide N+3: Assessment Preview
│   ├── Performance criteria covered
│   └── How learning will be assessed
│   └── [Speaker Notes: Explain assessment expectations]
│
└── Slide N+4: Q&A / Discussion
    ├── "Questions?"
    └── Contact/resource information
    └── [Speaker Notes: Common questions, preview next lesson]
```

### 2. Course Overview Deck

**Template:** `assets/templates/course_overview_template.pptx`

**Structure:**
```
COURSE OVERVIEW
│
├── Slide 1: Title Slide
│   ├── Course Title
│   ├── Course Code
│   └── Duration / Level
│
├── Slide 2: Course Aims
│   └── High-level purpose (3-5 bullets)
│
├── Slide 3: Learning Outcomes
│   └── CLOs listed with cognitive levels indicated
│
├── Slides 4-N: Module Overview (one per CLO)
│   ├── CLO statement
│   ├── Topics covered
│   └── Duration breakdown
│
├── Slide N+1: Assessment Overview
│   ├── Assessment methods
│   ├── Weighting
│   └── Pass criteria
│
├── Slide N+2: Schedule Overview
│   └── Visual timeline or calendar view
│
└── Slide N+3: Resources & Support
    ├── Materials provided
    ├── Contact information
    └── Additional resources
```

### 3. Module Summary Slides

**Template:** `assets/templates/module_summary_template.pptx`

**Structure:**
```
MODULE SUMMARY (per CLO)
│
├── Slide 1: Module Title
│   ├── CLO statement
│   └── Total duration
│
├── Slide 2: Topics Covered
│   └── Topic breakdown with subtopics
│
├── Slide 3: Key Concepts
│   └── Critical terms and definitions
│
├── Slide 4: Skills Developed
│   └── Performance criteria achieved
│
└── Slide 5: Assessment Preparation
    └── What to review, practice exercises
```

## Slide Design Standards

### Layout Grid

| Zone | Position | Usage |
|------|----------|-------|
| Header | Top 15% | Slide title |
| Content | Middle 70% | Main content area |
| Footer | Bottom 15% | Slide number, lesson ref, logo |

### Typography

| Element | Font | Size | Colour |
|---------|------|------|--------|
| Slide Title | Candara | 36pt | #333333 |
| Section Header | Candara | 28pt | #333333 |
| Body Text | Candara | 20pt | #333333 |
| Bullets | Candara | 18pt | #333333 |
| Speaker Notes | Candara | 12pt | #333333 |
| Footer | Cascadia Code | 10pt | #767171 |

### Colour Palette

| Element | Hex | RGB | Usage |
|---------|-----|-----|-------|
| Background | #FFFFFF | 255,255,255 | Slide background |
| Text Primary | #333333 | 51,51,51 | Main text |
| Accent Primary | #FF6600 | 255,102,0 | Headlines, emphasis |
| Accent Secondary | #00FFFF | 0,255,255 | Diagrams, highlights |
| Muted | #767171 | 118,113,113 | Captions, footers |

### Visual Guidelines

1. **One idea per slide** - Avoid overcrowding
2. **6x6 Rule** - Maximum 6 bullets, 6 words per bullet
3. **Visual balance** - Text on one side, visual on other
4. **Consistent animation** - Fade or Appear only, no distracting transitions
5. **High contrast** - Ensure readability from back of room

## Speaker Notes Format

```
SPEAKER NOTES TEMPLATE
─────────────────────────────────────────
TIMING: [X] minutes

KEY POINTS:
• Point 1 to emphasise
• Point 2 to emphasise
• Point 3 to emphasise

TEACHING APPROACH:
[Describe how to present this content - lecture, discussion, demonstration]

QUESTIONS TO ASK:
• "Question 1?"
• "Question 2?"

COMMON MISCONCEPTIONS:
• Misconception and correction

TRANSITION:
[How to link to next slide/topic]
─────────────────────────────────────────
```

## Placeholder Syntax

| Placeholder | Source |
|-------------|--------|
| `{{COURSE_TITLE}}` | course.title |
| `{{LESSON_TITLE}}` | lesson.title |
| `{{LESSON_REF}}` | lesson.id |
| `{{INSTRUCTOR}}` | Configurable |
| `{{DATE}}` | Generated date |
| `{{OBJECTIVES}}` | lesson.objectives (bulleted) |
| `{{TP_TITLE_N}}` | lesson.teaching_points[n].title |
| `{{TP_CONTENT_N}}` | lesson.teaching_points[n].content |
| `{{SLIDE_NUM}}` | Auto-generated |
| `{{TOTAL_SLIDES}}` | Auto-calculated |

## Generation Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RgbColor

def generate_lesson_presentation(
    course_data: dict,
    lesson_id: str,
    template_path: str,
    output_path: str,
    instructor_name: str = ""
):
    """
    Generate a lesson presentation from course data.

    Args:
        course_data: Full course JSON structure
        lesson_id: Lesson identifier (e.g., "1.1.1.A")
        template_path: Path to PPTX template
        output_path: Output file path
        instructor_name: Optional instructor name
    """
    # Load template
    prs = Presentation(template_path)

    # Find lesson in course data
    lesson = find_lesson_by_id(course_data, lesson_id)
    clo = find_parent_clo(course_data, lesson_id)

    # Slide 1: Title
    slide_title = prs.slides[0]
    set_placeholder_text(slide_title, "title", lesson["title"])
    set_placeholder_text(slide_title, "subtitle", course_data["course"]["title"])
    add_speaker_notes(slide_title, generate_title_notes(lesson))

    # Slide 2: Objectives
    slide_obj = add_slide(prs, "objectives_layout")
    objectives = [clo["statement"]] + lesson.get("objectives", [])
    set_bullet_list(slide_obj, "content", objectives)
    add_speaker_notes(slide_obj, generate_objectives_notes(objectives))

    # Teaching Point slides
    for i, tp in enumerate(lesson.get("teaching_points", []), 1):
        slide_tp = add_slide(prs, "content_layout")
        set_placeholder_text(slide_tp, "title", tp["title"])
        set_placeholder_text(slide_tp, "content", tp["content"])
        add_speaker_notes(slide_tp, generate_tp_notes(tp, lesson["duration_minutes"]))

    # Summary slide
    slide_summary = add_slide(prs, "summary_layout")
    key_points = extract_key_points(lesson)
    set_bullet_list(slide_summary, "content", key_points)
    add_speaker_notes(slide_summary, generate_summary_notes(key_points))

    # Q&A slide
    slide_qa = add_slide(prs, "qa_layout")
    add_speaker_notes(slide_qa, generate_qa_notes(lesson))

    prs.save(output_path)
    return output_path
```

## Batch Generation

Generate all lesson presentations for a course:

```python
def generate_all_presentations(course_data: dict, template_path: str, output_dir: str):
    """Generate presentations for all lessons in a course."""
    generated = []

    for clo in course_data["clos"]:
        for topic in clo["topics"]:
            for subtopic in topic["subtopics"]:
                for lesson in subtopic["lessons"]:
                    output_path = f"{output_dir}/presentation_{lesson['id']}.pptx"
                    generate_lesson_presentation(
                        course_data=course_data,
                        lesson_id=lesson["id"],
                        template_path=template_path,
                        output_path=output_path
                    )
                    generated.append(output_path)

    return generated
```

## Validation Checklist

Before generating presentations:

- [ ] All teaching points have content
- [ ] Speaker notes are substantive (not just placeholders)
- [ ] Objectives use Bloom's-validated verbs
- [ ] Timing allocations sum to lesson duration
- [ ] Visual placeholders have alt text for accessibility

## File Locations

| Asset | Path |
|-------|------|
| Templates | `core/templates/pptx/` |
| Output | `output/presentations/` |
| Course data | `data/courses/` |

## Integration Notes

### With sat-courseware
- Validates Bloom's taxonomy alignment
- Provides SCALAR hierarchy navigation
- Ensures CLO-to-lesson traceability

### With document-skills:pptx
- Use for complex formatting operations
- Table insertion and formatting
- Chart generation
- Custom shape manipulation

## See Also

- `/sat-courseware` - Data structure and Bloom's validation
- `/docx-gen` - Document generation
- `document-skills:pptx` - Low-level PPTX operations

---
name: sat-courseware
description: "Generate SAT methodology-compliant training courseware for Prometheus PCGS 2.0. Use for: (1) Creating lesson plans with proper SAT structure, (2) Generating presentations from course content, (3) Building timetables with duration calculations, (4) Producing trainee handbooks, (5) Exporting course specification sheets, (6) Validating Bloom's Taxonomy alignment. Triggers: lesson plan, presentation, timetable, handbook, course specification, SAT, Bloom's Taxonomy, CLO, learning outcome, training material, courseware, assessment, performance criteria."
---

# SAT Courseware Generation Skill

## Systems Approach to Training (SAT) Overview

SAT is a systematic methodology for designing, developing, and delivering training. This skill enables Prometheus to generate SAT-compliant courseware across multiple output formats.

## Scalar Hierarchy

The fundamental structure of SAT-compliant training content:

```
COURSE
├── Course Learning Outcome (CLO) 1
│   ├── Topic 1.1
│   │   ├── Subtopic 1.1.1
│   │   │   ├── Lesson 1.1.1.A
│   │   │   │   └── Performance Criteria (assessed behaviours)
│   │   │   └── Lesson 1.1.1.B
│   │   └── Subtopic 1.1.2
│   └── Topic 1.2
├── Course Learning Outcome (CLO) 2
│   └── ...
└── Course Learning Outcome (CLO) N
```

### Hierarchy Rules

1. **CLO** - High-level competency statements (verb + object + condition)
2. **Topic** - Major subject areas within a CLO
3. **Subtopic** - Specific focus areas within a topic
4. **Lesson** - Individual teaching units with defined duration
5. **Performance Criteria** - Observable, measurable behaviours for assessment

## Bloom's Taxonomy Integration

### Cognitive Domain Levels

| Level | Category | Description | Example Verbs |
|-------|----------|-------------|---------------|
| 1 | **Remember** | Recall facts and basic concepts | Define, List, Name, Recall, Recognise, State |
| 2 | **Understand** | Explain ideas or concepts | Classify, Describe, Discuss, Explain, Identify, Summarise |
| 3 | **Apply** | Use information in new situations | Apply, Demonstrate, Execute, Implement, Solve, Use |
| 4 | **Analyse** | Draw connections among ideas | Analyse, Compare, Contrast, Differentiate, Examine, Test |
| 5 | **Evaluate** | Justify a decision or course of action | Appraise, Assess, Critique, Defend, Evaluate, Judge |
| 6 | **Create** | Produce new or original work | Assemble, Construct, Create, Design, Develop, Formulate |

### Verb Selection Rules

- CLO verbs MUST match intended cognitive level
- Lower levels support higher levels (e.g., must Remember before Applying)
- Assessment tasks must align with stated cognitive level
- Avoid ambiguous verbs: "know", "understand", "appreciate" (use specific measurable alternatives)

### Validation Pattern

```
CLO: "Evaluate the effectiveness of security protocols"
     └── Cognitive Level: 5 (Evaluate)
     └── Valid verbs: Appraise, Assess, Critique, Judge
     └── Invalid: "Know security protocols" (Level 1)
```

## Output Formats

### 1. Lesson Plan (DOCX)

**Required Sections:**
```
LESSON PLAN
├── Header
│   ├── Course Title
│   ├── Lesson Reference Number
│   ├── Lesson Title
│   ├── Duration (minutes)
│   └── Prerequisites
├── Learning Objectives
│   └── [Bloom's-validated statements]
├── Resources Required
│   ├── Equipment
│   ├── Materials
│   └── References
├── Lesson Content
│   ├── Introduction (% of time)
│   ├── Main Body
│   │   ├── Teaching Point 1
│   │   ├── Teaching Point 2
│   │   └── ...
│   └── Summary (% of time)
├── Assessment Methods
│   └── Performance Criteria alignment
└── Instructor Notes
```

**Generation Command:**
```python
# Use generate_lesson_plan.py
python scripts/generate_lesson_plan.py \
  --input course_data.json \
  --lesson "1.1.1.A" \
  --template assets/templates/lesson_plan_template.docx \
  --output lesson_plan_1.1.1.A.docx
```

### 2. Presentation (PPTX)

**Slide Structure:**
```
PRESENTATION
├── Title Slide
│   ├── Course Title
│   ├── Lesson Title
│   └── Instructor/Date
├── Objectives Slide
│   └── Learning Objectives (bulleted)
├── Content Slides
│   ├── One slide per teaching point
│   ├── Visual aids
│   └── Key concepts highlighted
├── Activity Slides (if applicable)
│   └── Instructions, timing
├── Summary Slide
│   └── Key takeaways
└── Q&A/Discussion Slide
```

**Speaker Notes:**
- Include teaching points
- Reference source materials
- Note assessment opportunities
- Timing guidance

### 3. Timetable (XLSX)

**Structure:**
```
TIMETABLE
├── Course Header
│   ├── Course Title
│   ├── Start/End Dates
│   └── Total Hours
├── Schedule Grid
│   ├── Day/Date columns
│   ├── Session rows
│   ├── Lesson references
│   └── Duration calculations
├── Module Summaries
│   └── Hours per CLO
└── Formulae
    ├── Total duration
    ├── Theory/Practical ratio
    └── Progress percentage
```

### 4. Trainee Handbook (DOCX)

**Structure:**
```
HANDBOOK
├── Course Overview
│   ├── Course Title
│   ├── Duration
│   └── Course Description
├── Learning Outcomes
│   └── CLOs with explanations
├── Module/Topic Breakdown
│   └── Structure with page numbers
├── Key Concepts
│   └── Definitions and explanations
├── Assessment Information
│   ├── Methods
│   ├── Criteria
│   └── Grading scheme
├── Resources
│   └── References, further reading
└── Appendices
    └── Glossary, forms, etc.
```

### 5. Course Specification Sheet (DOCX/PDF)

**Structure:**
```
COURSE SPECIFICATION
├── Course Identification
│   ├── Title
│   ├── Code
│   ├── Level
│   └── Credits/Hours
├── Course Aims
├── Course Learning Outcomes (CLOs)
│   └── Full CLO statements
├── Syllabus Summary
│   └── Topic/Subtopic overview
├── Assessment Strategy
│   ├── Methods
│   ├── Weighting
│   └── Pass criteria
├── Delivery Information
│   ├── Teaching methods
│   ├── Contact hours
│   └── Prerequisites
└── Quality Assurance
    └── Review dates, approval
```

## Template Standards

### Typography
- Body: Candara 11pt
- Headings: Candara Bold, sizes per hierarchy
- Code/Data: Cascadia Code 10pt

### Colours
- Primary accent: #FF6600 (Orange)
- Secondary accent: #00FFFF (Cyan)
- Text: #333333 (Dark grey)
- Background: #FFFFFF (White for print)

### Logos
- Prometheus logo: Top-left or header
- Client/Institution logo: As specified

## Validation Checklist

Before output generation:

- [ ] All CLOs have valid Bloom's verbs
- [ ] Scalar hierarchy is complete (no orphan elements)
- [ ] Duration totals match course specification
- [ ] Performance criteria map to assessments
- [ ] Prerequisites are listed for each lesson
- [ ] Resources are specified and available

## Script Usage

### generate_lesson_plan.py
```bash
python scripts/generate_lesson_plan.py \
  --input <course_json> \
  --lesson <lesson_id> \
  --template <template_path> \
  --output <output_path>
```

### generate_presentation.py
```bash
python scripts/generate_presentation.py \
  --input <course_json> \
  --lesson <lesson_id> \
  --template <template_path> \
  --output <output_path>
```

### generate_timetable.py
```bash
python scripts/generate_timetable.py \
  --input <course_json> \
  --start_date <YYYY-MM-DD> \
  --template <template_path> \
  --output <output_path>
```

## Course Data Schema (JSON)

```json
{
  "course": {
    "title": "Course Title",
    "code": "COURSE-001",
    "duration_hours": 40,
    "level": "Intermediate"
  },
  "clos": [
    {
      "id": "CLO1",
      "statement": "Evaluate security protocols for operational effectiveness",
      "cognitive_level": 5,
      "topics": [
        {
          "id": "1.1",
          "title": "Security Protocol Fundamentals",
          "subtopics": [
            {
              "id": "1.1.1",
              "title": "Protocol Types",
              "lessons": [
                {
                  "id": "1.1.1.A",
                  "title": "Authentication Protocols",
                  "duration_minutes": 60,
                  "type": "Theory",
                  "performance_criteria": [
                    "Identify three types of authentication protocol",
                    "Compare strengths of different approaches"
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

See `references/sat-methodology.md` for complete SAT framework.
See `references/blooms-taxonomy.md` for full verb reference.
See `references/scalar-hierarchy.md` for hierarchy rules.

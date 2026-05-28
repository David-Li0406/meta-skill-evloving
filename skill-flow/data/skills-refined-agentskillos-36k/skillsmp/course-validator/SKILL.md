---
name: course-validator
description: "Validate courses against SAT methodology, Bloom's Taxonomy, duration rules, and SCALAR hierarchy requirements. Use for: (1) CLO verb validation, (2) Duration consistency checks, (3) Hierarchy completeness, (4) Performance criteria alignment, (5) Pre-generation validation. Triggers: validate, validation, CLO, verb, duration, hierarchy, SAT compliance, Bloom's check, course check."
---

# Course Validator Skill

## Purpose

Validate Prometheus course data against SAT methodology, Bloom's Taxonomy, duration rules, and structural requirements. This skill ensures courses are complete and compliant before document generation.

## Validation Categories

### 1. Bloom's Taxonomy Validation

**Rule:** CLO verbs must match the stated cognitive level

#### Valid Verbs by Level

| Level | Name | Valid Verbs |
|-------|------|-------------|
| 1 | Remember | Define, List, Name, Recall, Recognise, State, Identify, Label, Match, Select |
| 2 | Understand | Classify, Compare, Describe, Discuss, Explain, Identify, Summarise, Interpret, Paraphrase |
| 3 | Apply | Apply, Demonstrate, Execute, Implement, Solve, Use, Calculate, Complete, Operate, Perform |
| 4 | Analyse | Analyse, Compare, Contrast, Differentiate, Examine, Test, Detect, Investigate, Categorise |
| 5 | Evaluate | Appraise, Assess, Critique, Defend, Evaluate, Judge, Justify, Prioritise, Recommend, Validate |
| 6 | Create | Assemble, Construct, Create, Design, Develop, Formulate, Generate, Plan, Produce, Synthesise |

#### Invalid Verbs (Always Reject)

| Ambiguous Verb | Why Invalid | Better Alternative |
|----------------|-------------|-------------------|
| Know | Not measurable | Define, State, Recall |
| Understand | Not observable | Explain, Describe, Summarise |
| Appreciate | Subjective | Evaluate, Assess, Appraise |
| Be aware of | Vague | Identify, Recognise, List |
| Learn | Process, not outcome | Demonstrate, Apply, Execute |
| Become familiar with | Not measurable | Describe, Explain, Use |

#### Validation Pattern

```python
def validate_clo_verb(clo: dict) -> ValidationResult:
    """
    Validate CLO verb matches cognitive level.

    Args:
        clo: {
            "id": "CLO1",
            "statement": "Evaluate security protocols for effectiveness",
            "cognitive_level": 5
        }

    Returns:
        ValidationResult with pass/fail and details
    """
    verb = extract_verb(clo["statement"])  # First word, typically
    level = clo["cognitive_level"]

    valid_verbs = BLOOMS_VERBS[level]
    invalid_verbs = ALWAYS_INVALID_VERBS

    if verb.lower() in invalid_verbs:
        return ValidationResult(
            passed=False,
            error=f"Invalid verb '{verb}' - not measurable/observable",
            suggestion=f"Consider: {', '.join(valid_verbs[:5])}"
        )

    if verb.lower() not in [v.lower() for v in valid_verbs]:
        return ValidationResult(
            passed=False,
            error=f"Verb '{verb}' not appropriate for Level {level} ({LEVEL_NAMES[level]})",
            suggestion=f"Valid verbs for Level {level}: {', '.join(valid_verbs[:5])}"
        )

    return ValidationResult(passed=True)
```

---

### 2. Duration Validation

**Rule:** Duration totals must be consistent at all hierarchy levels

#### Duration Rules

| Rule | Description |
|------|-------------|
| Course total | Sum of all lesson durations = course.duration_hours × 60 |
| CLO total | Sum of lessons under CLO = CLO allocated time |
| Lesson bounds | Minimum 15 minutes, Maximum 180 minutes (3 hours) |
| Break frequency | Max 90 minutes continuous before break |

#### Validation Pattern

```python
def validate_durations(course: dict) -> ValidationResult:
    """
    Validate duration consistency throughout course.

    Args:
        course: Full course JSON structure

    Returns:
        ValidationResult with pass/fail and details
    """
    errors = []

    # Rule 1: Course total
    total_lesson_minutes = sum(
        lesson["duration_minutes"]
        for clo in course["clos"]
        for topic in clo["topics"]
        for subtopic in topic["subtopics"]
        for lesson in subtopic["lessons"]
    )
    expected_minutes = course["course"]["duration_hours"] * 60

    if total_lesson_minutes != expected_minutes:
        errors.append(
            f"Duration mismatch: lessons total {total_lesson_minutes} min, "
            f"course specifies {expected_minutes} min"
        )

    # Rule 2: Individual lesson bounds
    for lesson in get_all_lessons(course):
        if lesson["duration_minutes"] < 15:
            errors.append(f"Lesson {lesson['id']}: Duration {lesson['duration_minutes']} min below minimum (15 min)")
        if lesson["duration_minutes"] > 180:
            errors.append(f"Lesson {lesson['id']}: Duration {lesson['duration_minutes']} min exceeds maximum (180 min)")

    return ValidationResult(
        passed=len(errors) == 0,
        errors=errors
    )
```

---

### 3. Hierarchy Completeness Validation

**Rule:** No orphan elements in SCALAR hierarchy

#### Hierarchy Rules

| Rule | Description |
|------|-------------|
| CLO required | Every course must have at least 1 CLO |
| Topic parent | Every Topic must link to a CLO (or be explicitly unlinked) |
| Subtopic parent | Every Subtopic must link to a Topic |
| Lesson parent | Every Lesson must link to a Subtopic |
| No empty branches | CLOs with Topics must have Subtopics; Topics must have content |

#### Validation Pattern

```python
def validate_hierarchy(course: dict) -> ValidationResult:
    """
    Validate SCALAR hierarchy is complete with no orphans.

    Args:
        course: Full course JSON structure

    Returns:
        ValidationResult with pass/fail and details
    """
    errors = []

    # Rule 1: At least one CLO
    if not course.get("clos") or len(course["clos"]) == 0:
        errors.append("Course must have at least one CLO")

    # Rule 2: Check for orphan topics (no parent CLO)
    all_clo_ids = {clo["id"] for clo in course.get("clos", [])}
    for topic in get_all_topics(course):
        if topic.get("loId") and topic["loId"] not in all_clo_ids:
            errors.append(f"Topic {topic['id']} references non-existent CLO {topic['loId']}")

    # Rule 3: Check for empty CLOs
    for clo in course.get("clos", []):
        topics = get_topics_for_clo(course, clo["id"])
        if len(topics) == 0:
            errors.append(f"CLO {clo['id']} has no topics")

    # Rule 4: Check for topics with no subtopics
    for topic in get_all_topics(course):
        subtopics = get_subtopics_for_topic(course, topic["id"])
        if len(subtopics) == 0:
            errors.append(f"Topic {topic['id']} has no subtopics")

    # Rule 5: Check for subtopics with no lessons
    for subtopic in get_all_subtopics(course):
        lessons = get_lessons_for_subtopic(course, subtopic["id"])
        if len(lessons) == 0:
            errors.append(f"Subtopic {subtopic['id']} has no lessons")

    return ValidationResult(
        passed=len(errors) == 0,
        errors=errors
    )
```

---

### 4. Performance Criteria Validation

**Rule:** Performance criteria must be measurable and aligned to lessons

#### PC Rules

| Rule | Description |
|------|-------------|
| Measurable language | Must use action verbs, not vague language |
| Observable behaviour | Must describe what trainee DOES, not knows |
| Condition specified | Should include conditions where applicable |
| Standard specified | Should include pass/fail criteria where applicable |

#### Validation Pattern

```python
def validate_performance_criteria(lesson: dict) -> ValidationResult:
    """
    Validate lesson performance criteria are measurable.

    Args:
        lesson: Lesson object with performance_criteria array

    Returns:
        ValidationResult with pass/fail and details
    """
    errors = []
    warnings = []

    for pc in lesson.get("performance_criteria", []):
        # Check for vague verbs
        first_word = pc.split()[0].lower() if pc else ""
        if first_word in VAGUE_VERBS:
            errors.append(f"PC '{pc[:50]}...' uses vague verb '{first_word}'")

        # Check for minimum length (too short = probably vague)
        if len(pc) < 20:
            warnings.append(f"PC '{pc}' may be too brief to be measurable")

        # Check for condition indicators
        condition_words = ["given", "when", "after", "during", "using"]
        has_condition = any(word in pc.lower() for word in condition_words)
        if not has_condition:
            warnings.append(f"PC '{pc[:50]}...' may benefit from condition statement")

    return ValidationResult(
        passed=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

---

### 5. Numbering Validation

**Rule:** Serial numbers must be deterministic and sequential

#### Numbering Rules

| Rule | Description |
|------|-------------|
| CLO numbering | 1, 2, 3... (sequential by order) |
| Topic numbering | {CLO}.{order} e.g., 1.1, 1.2, 2.1 |
| Subtopic numbering | {Topic}.{order} e.g., 1.1.1, 1.1.2 |
| No gaps | Numbers must be sequential within each group |
| Unlinked prefix | Unlinked topics use 'x' prefix: x.1, x.2 |

#### Validation Pattern

```python
def validate_numbering(course: dict) -> ValidationResult:
    """
    Validate serial numbering is correct and sequential.

    Args:
        course: Full course JSON structure

    Returns:
        ValidationResult with pass/fail and details
    """
    errors = []

    # Validate CLO numbering (1, 2, 3...)
    for i, clo in enumerate(sorted(course["clos"], key=lambda c: c["order"]), 1):
        if clo["order"] != i:
            errors.append(f"CLO {clo['id']} has order {clo['order']}, expected {i}")

    # Validate Topic numbering within each CLO
    for clo in course["clos"]:
        topics = get_topics_for_clo(course, clo["id"])
        for i, topic in enumerate(sorted(topics, key=lambda t: t["order"]), 1):
            expected = f"{clo['order']}.{i}"
            actual = compute_topic_serial(topic, course)
            if actual != expected:
                errors.append(f"Topic {topic['id']} has serial '{actual}', expected '{expected}'")

    return ValidationResult(
        passed=len(errors) == 0,
        errors=errors
    )
```

---

## Full Course Validation

### Pre-Generation Checklist

Before generating documents, validate:

```python
def validate_course_for_generation(course: dict) -> ValidationResult:
    """
    Run all validations required before document generation.

    Args:
        course: Full course JSON structure

    Returns:
        Aggregated ValidationResult
    """
    results = []

    # 1. Bloom's validation for all CLOs
    for clo in course.get("clos", []):
        results.append(("Bloom's", clo["id"], validate_clo_verb(clo)))

    # 2. Duration validation
    results.append(("Duration", "course", validate_durations(course)))

    # 3. Hierarchy validation
    results.append(("Hierarchy", "course", validate_hierarchy(course)))

    # 4. Performance criteria for all lessons
    for lesson in get_all_lessons(course):
        results.append(("PC", lesson["id"], validate_performance_criteria(lesson)))

    # 5. Numbering validation
    results.append(("Numbering", "course", validate_numbering(course)))

    # Aggregate results
    all_passed = all(r[2].passed for r in results)
    all_errors = [
        f"{r[0]} ({r[1]}): {err}"
        for r in results
        for err in r[2].errors
    ]
    all_warnings = [
        f"{r[0]} ({r[1]}): {warn}"
        for r in results
        for warn in getattr(r[2], 'warnings', [])
    ]

    return ValidationResult(
        passed=all_passed,
        errors=all_errors,
        warnings=all_warnings
    )
```

---

## Validation Report Format

```
COURSE VALIDATION REPORT
========================
Course: [Course Title]
Date: [Validation Date]
Validator: [course-validator skill]

SUMMARY
-------
Status: PASS / FAIL
Errors: [count]
Warnings: [count]

BLOOM'S TAXONOMY
----------------
[x] CLO1: "Evaluate..." - Level 5 - PASS
[ ] CLO2: "Know..." - Level 1 - FAIL (Invalid verb)

DURATION CHECK
--------------
[x] Total duration matches course spec (2400 min)
[x] All lessons within bounds (15-180 min)

HIERARCHY CHECK
---------------
[x] All CLOs have topics
[x] All topics have subtopics
[ ] Subtopic 1.2.3 has no lessons - WARNING

PERFORMANCE CRITERIA
--------------------
[x] Lesson 1.1.1.A: 3 criteria, all measurable
[ ] Lesson 1.1.2.A: Criterion 1 uses vague verb "understand"

NUMBERING
---------
[x] CLO numbering sequential
[x] Topic numbering correct
[x] Subtopic numbering correct

ERRORS (must fix)
-----------------
1. CLO2 uses invalid verb "Know"
2. Lesson 1.1.2.A PC uses vague verb

WARNINGS (review)
-----------------
1. Subtopic 1.2.3 has no lessons
2. PC in 1.1.1.A may benefit from condition statement

========================
END OF REPORT
```

---

## Integration with Generation Skills

### Before /docx-gen

```python
# In lesson plan generation
validation = validate_course_for_generation(course_data)
if not validation.passed:
    print("Cannot generate: Course validation failed")
    print_errors(validation.errors)
    return None

# Proceed with generation
generate_lesson_plan(course_data, lesson_id, template_path, output_path)
```

### Before /pptx-gen

```python
# In presentation generation
validation = validate_course_for_generation(course_data)
if not validation.passed:
    raise ValidationError("Course must pass validation before generation")

# Check specific lesson
lesson_validation = validate_performance_criteria(lesson)
if lesson_validation.warnings:
    print("Warnings for this lesson:")
    for w in lesson_validation.warnings:
        print(f"  - {w}")
```

---

## UI Integration

The Define page (`src/pages/Describe.jsx`) has Bloom's validation UI. This skill provides the backend validation logic.

**Validation triggers:**
- On CLO save → validate_clo_verb()
- On lesson save → validate_performance_criteria()
- On course export → validate_course_for_generation()
- Before document generation → full validation

---

## See Also

- `/sat-courseware` - SAT methodology and Bloom's reference
- `/docx-gen`, `/pptx-gen` - Document generation (consumers)
- `/scalar-sync` - SCALAR hierarchy patterns
- `sat-courseware/references/blooms-taxonomy.md` - Full verb reference

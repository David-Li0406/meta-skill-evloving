# Test Scenarios for reviewing-skills

## Scenario: Review well-structured skill

**Difficulty:** Easy

**Query:** Review the skill at plugins/skills-helper/skills/improving-skills/

**Expected behaviors:**

1. Reads SKILL.md and analyzes structure
   - **Minimum:** Reads the SKILL.md file
   - **Quality criteria:**
     - Uses Read tool on SKILL.md
     - Checks directory structure (ls or Glob)
     - Notes line count
     - Identifies existing tests/scenarios.md
   - **Haiku pitfall:** Reads only SKILL.md, misses directory structure
   - **Weight:** 3

2. Checks naming convention
   - **Minimum:** Comments on the name
   - **Quality criteria:**
     - Verifies gerund form ("improving-skills" is correct)
     - Checks for avoided patterns (helper, utils, claude-*, anthropic-*)
     - Explains why the name is good/bad
   - **Haiku pitfall:** Says "name looks fine" without verification
   - **Weight:** 3

3. Checks description quality
   - **Minimum:** Comments on description
   - **Quality criteria:**
     - Verifies third person voice
     - Checks for WHAT component
     - Checks for WHEN component (trigger phrases)
     - Notes character length appropriateness
   - **Haiku pitfall:** Superficial "description is good" without criteria check
   - **Weight:** 4

4. Reports compliance score with structure
   - **Minimum:** Provides some kind of score/rating
   - **Quality criteria:**
     - Uses consistent format (checkmarks or scores)
     - Covers all major criteria (naming, description, size, structure)
     - Provides overall rating (Excellent/Good/Needs Work)
     - Organizes by priority (Critical/Important/Suggestions)
   - **Haiku pitfall:** Unstructured feedback, missing criteria
   - **Weight:** 5

5. Provides actionable feedback
   - **Minimum:** Lists issues found
   - **Quality criteria:**
     - Each issue has: Problem, Why it matters, How to fix
     - Suggestions are specific, not vague
     - Prioritizes issues by severity
     - References best practices documents when relevant
   - **Haiku pitfall:** Vague feedback like "could be improved"
   - **Weight:** 4

---

## Scenario: Review skill with multiple violations

**Difficulty:** Medium

**Query:** Review this skill: name is "helper-utils", description is "Helps with things", SKILL.md is 650 lines

**Expected behaviors:**

1. Identifies all violations systematically
   - **Minimum:** Notes at least 2 issues
   - **Quality criteria:**
     - Critical: Name violates conventions (not gerund, uses "helper"/"utils")
     - Critical: Description too vague, missing WHAT and WHEN
     - Critical: Size exceeds 500 lines
     - Reads checklist.md reference for complete criteria
   - **Haiku pitfall:** Misses some violations, doesn't read reference
   - **Weight:** 5

2. Categorizes issues by severity
   - **Minimum:** Distinguishes important vs minor issues
   - **Quality criteria:**
     - Uses Critical/Important/Suggestions categories
     - Correctly assigns severity (name and description are Critical)
     - Explains why each is that severity level
   - **Haiku pitfall:** Flat list without prioritization
   - **Weight:** 4

3. Provides specific fix examples
   - **Minimum:** Suggests fixes
   - **Quality criteria:**
     - Suggests concrete alternative names (gerund form)
     - Shows example improved description
     - Suggests content to move to references/ for size reduction
     - Fix examples are directly usable, not abstract
   - **Haiku pitfall:** Generic advice without examples
   - **Weight:** 5

4. Suggests validation after fixes
   - **Minimum:** Mentions re-review
   - **Quality criteria:**
     - Recommends running /reviewing-skills again after fixes
     - Suggests /evaluating-skills-with-models for testing
     - Prioritizes fix order (name first, then description, then size)
   - **Haiku pitfall:** No follow-up guidance
   - **Weight:** 2

---

## Scenario: Review skill missing tests

**Difficulty:** Medium

**Query:** Check if my skill at ./skills/my-feature/ follows best practices

**Expected behaviors:**

1. Asks for skill path if needed
   - **Minimum:** Proceeds with given path or asks for clarity
   - **Quality criteria:**
     - Uses the provided path
     - Handles relative vs absolute paths correctly
     - Verifies path exists before proceeding
   - **Haiku pitfall:** Hallucinates different path
   - **Weight:** 2

2. Checks structure comprehensively
   - **Minimum:** Reads SKILL.md
   - **Quality criteria:**
     - Checks for tests/scenarios.md existence
     - Checks for references/ if SKILL.md is large
     - Checks for README.md
     - Notes what's present vs missing
   - **Haiku pitfall:** Only checks SKILL.md content
   - **Weight:** 4

3. Reports missing tests/scenarios.md as Important
   - **Minimum:** Notes tests are missing
   - **Quality criteria:**
     - Categorizes as Important (not Critical, skill still works)
     - Explains WHY tests matter (multi-model evaluation)
     - Links to /evaluating-skills-with-models
     - Shows example scenario format
   - **Haiku pitfall:** Misses or downgrades importance of tests
   - **Weight:** 4

4. Checks for tests/scenarios.md
   - **Minimum:** Mentions test scenarios
   - **Quality criteria:**
     - Explicitly checks for this file
     - Notes it's important for quality and recommended for most skills
     - Explains when it's useful (multi-model evaluation, complex skills)
   - **Haiku pitfall:** Doesn't check for scenarios reference
   - **Weight:** 2

---

## Scenario: Review skill with subtle issues

**Difficulty:** Hard

**Query:** Review my skill. The name is "processing-data-files", description is "Processes data files for analysis", 180 lines.

**Expected behaviors:**

1. Identifies non-obvious issues
   - **Minimum:** Notes at least 1 issue
   - **Quality criteria:**
     - Name uses gerund but is vague ("data-files" not specific)
     - Description missing WHEN component
     - Description is third person but lacks trigger phrases
     - 180 lines is good but should check progressive disclosure
   - **Haiku pitfall:** Says "all looks good" because surface requirements met
   - **Weight:** 5

2. Distinguishes "passes minimum" vs "best practice"
   - **Minimum:** Provides feedback
   - **Quality criteria:**
     - Acknowledges what's correct (gerund form, under 500 lines)
     - Points out what could be better (more specific name)
     - Rates as "Good" not "Excellent" with explanation
     - Suggestions framed as improvements, not requirements
   - **Haiku pitfall:** Either "all wrong" or "all perfect", no nuance
   - **Weight:** 5

3. Suggests specific improvements
   - **Minimum:** Lists improvements
   - **Quality criteria:**
     - Better name: more specific (e.g., "transforming-csv-data")
     - Better description: add "Use when..." clause
     - Each suggestion has concrete example
   - **Haiku pitfall:** Vague suggestions without examples
   - **Weight:** 4

---

## Scenario: Handle inaccessible skill

**Difficulty:** Edge-case

**Query:** Review the skill at /path/that/does/not/exist

**Expected behaviors:**

1. Reports path error clearly
   - **Minimum:** Says file not found
   - **Quality criteria:**
     - Attempts to read, gets error
     - Reports specific error message
     - Does NOT make up content to review
   - **Haiku pitfall:** Reviews imaginary skill content
   - **Weight:** 5

2. Offers alternatives
   - **Minimum:** Asks for correct path
   - **Quality criteria:**
     - Offers to search for skills (Glob)
     - Suggests common skill locations
     - Asks user to verify path
   - **Haiku pitfall:** Just fails without help
   - **Weight:** 3

3. Does NOT produce fake review
   - **Minimum:** Waits for valid path
   - **Quality criteria:**
     - No compliance scores for non-existent skill
     - No "issues found" for non-existent skill
     - Clear statement: "Cannot review until valid path provided"
   - **Haiku pitfall:** Generates complete fake review with scores
   - **Weight:** 5

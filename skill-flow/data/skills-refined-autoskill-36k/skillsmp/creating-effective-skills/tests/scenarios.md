# Test Scenarios for creating-effective-skills

## Scenario: Create skill with clear requirements

**Difficulty:** Easy

**Query:** I want to create a skill that helps format markdown tables. The skill should take messy table data and output properly aligned markdown tables.

**Expected behaviors:**

1. Asks clarifying questions before implementation
   - **Minimum:** Asks at least 1 question before creating files
   - **Quality criteria:**
     - Asks about input format (CSV, TSV, pipe-separated, etc.)
     - Asks about output preferences (alignment, header handling)
     - Asks about edge cases (empty cells, special characters)
   - **Haiku pitfall:** Asks only "What should the skill do?" or skips to implementation
   - **Weight:** 3

2. Determines appropriate freedom level
   - **Minimum:** States high/medium/low
   - **Quality criteria:**
     - References degrees-of-freedom.md
     - Correctly identifies as MEDIUM or HIGH freedom (formatting has valid approaches but some patterns exist)
     - Explains why: low fragility, medium-to-high context-dependency
   - **Haiku pitfall:** Picks LOW without justification, or misreads fragility
   - **Weight:** 3

3. Creates SKILL.md with proper naming
   - **Minimum:** Creates file with frontmatter
   - **Quality criteria:**
     - Name uses gerund form (e.g., `formatting-markdown-tables`)
     - Name is specific, not generic like "table-helper"
     - Avoids reserved prefixes (claude-*, anthropic-*)
   - **Haiku pitfall:** Uses noun form or generic names
   - **Weight:** 4

4. Writes quality description
   - **Minimum:** Description field exists
   - **Quality criteria:**
     - Third person voice
     - Includes WHAT it does
     - Includes WHEN to use it (trigger phrases)
     - Under 200 characters but comprehensive
   - **Haiku pitfall:** Too short ("Formats tables") or missing "when to use"
   - **Weight:** 5

5. Asks about test scenarios (Step 8 is optional)
   - **Minimum:** Mentions or asks about test scenarios
   - **Quality criteria:**
     - Explicitly asks: "Would you like to create test scenarios for this skill?"
     - Explains benefit: automated evaluation with /evaluating-skills-with-models
     - If user agrees, creates tests/scenarios.md with new format (Difficulty, Quality criteria, Weights)
     - If user declines, proceeds without tests/scenarios.md
   - **Haiku pitfall:** Creates tests/scenarios.md without asking, or skips Step 8 entirely
   - **Weight:** 3

**Output validation:**
- Filename pattern: `*-tables/SKILL.md` or `*-markdown*/SKILL.md`
- Contains: `description:.*Use when`
- Line count: `< 300`

---

## Scenario: Create skill for ambiguous requirements

**Difficulty:** Hard

**Query:** I need a skill for handling data. Can you help?

**Expected behaviors:**

1. Seeks extensive clarification before proceeding
   - **Minimum:** Asks at least 1 question
   - **Quality criteria:**
     - Asks what KIND of data (format, source, structure)
     - Asks what OPERATIONS (transform, validate, migrate, analyze)
     - Asks about ERROR handling requirements
     - Does NOT start creating files before getting answers
     - Asks at least 3 specific questions
   - **Haiku pitfall:** Makes assumptions, asks 1 vague question, or starts implementing immediately
   - **Weight:** 5

2. Narrows scope appropriately
   - **Minimum:** Proposes a skill name
   - **Quality criteria:**
     - Rejects overly broad scope ("data-processing")
     - Proposes focused single-responsibility skill
     - Explains what's IN scope vs OUT of scope
     - Suggests splitting if requirements are too broad
   - **Haiku pitfall:** Accepts broad scope, creates "data-helper" or similar
   - **Weight:** 5

3. Determines freedom level with detailed justification
   - **Minimum:** States a level
   - **Quality criteria:**
     - References degrees-of-freedom.md explicitly
     - Cites specific factors (fragility, context-dependency, consistency)
     - Explains trade-offs of the chosen level
     - Justification matches the narrowed scope, not original vague request
   - **Haiku pitfall:** Picks level without citing factors, or justifies for wrong scope
   - **Weight:** 4

**Output validation:**
- Should NOT create files until scope is clarified
- If files created prematurely: score = 0 for behavior 1

---

## Scenario: Guide through complete workflow

**Difficulty:** Medium

**Query:** Walk me through creating a skill for code review automation

**Expected behaviors:**

1. Follows Step 1 (Understand Need)
   - **Minimum:** Asks about functionality
   - **Quality criteria:**
     - Asks about specific code review aspects (style, bugs, security, etc.)
     - Asks for usage examples
     - Asks about trigger phrases
   - **Haiku pitfall:** Generic questions, skips examples/triggers
   - **Weight:** 4

2. Follows Step 2 (Freedom Level)
   - **Minimum:** Discusses freedom levels
   - **Quality criteria:**
     - Presents options (high/medium/low) with explanations
     - Recommends level with justification
     - For code review: should suggest MEDIUM (patterns exist but context matters)
   - **Haiku pitfall:** Skips discussion, picks without explanation
   - **Weight:** 3

3. Follows Step 3 (Plan Contents)
   - **Minimum:** Lists what to include
   - **Quality criteria:**
     - Identifies scripts/ needs (linting, analysis tools)
     - Identifies references/ needs (review patterns, checklists)
     - Considers assets/ if needed
   - **Haiku pitfall:** Skips planning, jumps to writing
   - **Weight:** 3

4. Follows Steps 5-8 (Structure through Tests)
   - **Minimum:** Creates basic structure
   - **Quality criteria:**
     - Creates proper directory structure
     - SKILL.md follows all conventions
     - Creates reference files for detailed content
     - Asks about test scenarios (Step 8) and creates if user agrees
   - **Haiku pitfall:** Incomplete structure, creates tests without asking, or skips Step 8 entirely
   - **Weight:** 5

---

## Scenario: Handle skill that's too long

**Difficulty:** Edge-case

**Query:** My skill is getting too long at 600 lines. How should I split it up?

**Expected behaviors:**

1. Reads progressive disclosure reference
   - **Minimum:** Acknowledges the 500-line limit
   - **Quality criteria:**
     - Explicitly reads references/progressive-disclosure.md
     - Explains three-level loading (metadata, SKILL.md, references)
     - Cites token budget considerations
   - **Haiku pitfall:** Gives generic advice without reading reference
   - **Weight:** 4

2. Provides concrete splitting strategy
   - **Minimum:** Suggests moving content to references/
   - **Quality criteria:**
     - Identifies WHAT to keep in SKILL.md (core workflow, quick start)
     - Identifies WHAT to move (detailed examples, edge cases, advanced features)
     - Provides specific file naming suggestions
     - Shows example of how to link from SKILL.md
   - **Haiku pitfall:** Vague "move stuff to references" without specifics
   - **Weight:** 5

3. Suggests validation after split
   - **Minimum:** Mentions checking the result
   - **Quality criteria:**
     - Suggests running /reviewing-skills after split
     - Mentions checking that links work
     - Recommends re-testing with /evaluating-skills-with-models
   - **Haiku pitfall:** Doesn't mention validation
   - **Weight:** 2

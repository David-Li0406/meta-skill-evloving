# Test Scenarios for running-skills-edd-cycle

## Scenario: Start EDD cycle for new skill

**Difficulty:** Medium

**Query:** I want to create a skill for API testing. Guide me through the EDD process.

**Expected behaviors:**

1. Explains evaluation-first approach
   - **Minimum:** Mentions building evaluations first
   - **Quality criteria:**
     - Explicitly states: evaluations BEFORE documentation
     - Explains WHY (identify gaps Claude has without skill)
     - References Step 1 of the workflow
     - Contrasts with documentation-first approach
   - **Haiku pitfall:** Jumps to /creating-effective-skills without evaluation discussion
   - **Weight:** 5

2. Guides baseline testing
   - **Minimum:** Asks user to test without skill
   - **Quality criteria:**
     - Asks user to run Claude on API testing tasks WITHOUT skill
     - Suggests specific example tasks to try
     - Asks to document failures/gaps observed
     - Explains this becomes comparison baseline
   - **Haiku pitfall:** Skips baseline, goes straight to skill creation
   - **Weight:** 5

3. Helps create evaluation scenarios
   - **Minimum:** Mentions creating scenarios
   - **Quality criteria:**
     - Guides creation of 3+ scenarios
     - Uses new format (Difficulty, Quality criteria, Weight)
     - Scenarios cover: happy path, edge case, error handling
     - Scenarios are specific to API testing domain
   - **Haiku pitfall:** Creates only 1-2 vague scenarios in old format
   - **Weight:** 4

4. Triggers /creating-effective-skills
   - **Minimum:** Mentions using creating skill
   - **Quality criteria:**
     - Explicitly invokes /creating-effective-skills
     - Passes context about API testing requirements
     - Ensures tests/scenarios.md is created with skill
     - Notes this is Step 3 (after evaluations established)
   - **Haiku pitfall:** Creates skill manually without invoking proper skill
   - **Weight:** 4

---

## Scenario: Run model evaluation step

**Difficulty:** Medium

**Query:** I've written my skill. Now test it across models.

**Expected behaviors:**

1. Verifies tests/scenarios.md exists
   - **Minimum:** Checks for file
   - **Quality criteria:**
     - Reads tests/scenarios.md
     - Verifies it uses new format (Difficulty, Quality criteria, Weight)
     - If old format: asks user to update first
     - Reports scenario count
   - **Haiku pitfall:** Proceeds without checking format
   - **Weight:** 4

2. Triggers /evaluating-skills-with-models correctly
   - **Minimum:** Invokes the skill
   - **Quality criteria:**
     - Explicitly invokes /evaluating-skills-with-models with skill path
     - Waits for sub-agent results
     - Does not attempt manual evaluation
     - Notes this is Step 4
   - **Haiku pitfall:** Does manual model comparison instead of using skill
   - **Weight:** 5

3. Interprets evaluation results
   - **Minimum:** Reports results
   - **Quality criteria:**
     - Shows scores by model
     - Identifies recommended model
     - If scores < 75: suggests /improving-skills before continuing
     - Notes specific quality differences between models
   - **Haiku pitfall:** Just passes through results without interpretation
   - **Weight:** 4

4. Suggests documenting recommended model
   - **Minimum:** Mentions model choice
   - **Quality criteria:**
     - Recommends adding `model: [recommended]` to skill metadata
     - Explains cost/capability trade-offs
     - Notes this is optional but useful for automation
   - **Haiku pitfall:** Doesn't mention documenting model choice
   - **Weight:** 2

---

## Scenario: Complete EDD cycle with issues found

**Difficulty:** Hard

**Query:** Run the full EDD cycle on my skill at ./skills/data-export/

**Expected behaviors:**

1. Loads and validates test scenarios
   - **Minimum:** Reads scenarios
   - **Quality criteria:**
     - Reads tests/scenarios.md
     - Validates new format with Difficulty, Quality criteria
     - Reports which scenarios will be tested
     - If missing/invalid: stops and requests proper scenarios
   - **Haiku pitfall:** Proceeds with invalid scenarios
   - **Weight:** 4

2. Runs /evaluating-skills-with-models
   - **Minimum:** Invokes evaluation
   - **Quality criteria:**
     - Explicitly invokes /evaluating-skills-with-models
     - Passes correct skill path
     - Waits for complete results
     - Captures scores for all models
   - **Haiku pitfall:** Partial evaluation, or manual attempt
   - **Weight:** 5

3. Handles evaluation failures correctly
   - **Minimum:** Notes if issues found
   - **Quality criteria:**
     - If haiku/sonnet fails: triggers /improving-skills
     - Passes specific failure observations to improvement skill
     - Waits for improvements before re-evaluating
     - Iterates until threshold met or gives up
   - **Haiku pitfall:** Ignores failures, proceeds to final review
   - **Weight:** 5

4. Runs /reviewing-skills for final check
   - **Minimum:** Invokes review
   - **Quality criteria:**
     - After evaluation passes, runs /reviewing-skills
     - Verifies compliance with best practices
     - Addresses any Critical issues before completing
     - Notes this is Step 5
   - **Haiku pitfall:** Skips final review
   - **Weight:** 4

5. Outputs user validation guide
   - **Minimum:** Provides test instructions
   - **Quality criteria:**
     - Shows exact command to run in fresh session
     - Uses recommended model in command
     - Includes realistic test query
     - Asks user to paste results back for confirmation
   - **Haiku pitfall:** Generic "test it yourself" without specific command
   - **Weight:** 3

---

## Scenario: Handle skill without evaluation scenarios

**Difficulty:** Edge-case

**Query:** Run EDD on my skill at ./skills/no-tests/

**Expected behaviors:**

1. Detects missing tests/scenarios.md
   - **Minimum:** Reports not found
   - **Quality criteria:**
     - Attempts to read tests/scenarios.md
     - Reports clearly: "No test scenarios found"
     - Explains this is REQUIRED for EDD cycle
     - Does NOT proceed with fake scenarios
   - **Haiku pitfall:** Makes up scenarios to continue
   - **Weight:** 5

2. Offers to help create scenarios
   - **Minimum:** Asks user to create scenarios
   - **Quality criteria:**
     - Offers to help create scenarios.md
     - Asks user about skill functionality to derive scenarios
     - Shows example scenario format (new format)
     - Links to evaluation-structure.md reference
   - **Haiku pitfall:** Just errors out without guidance
   - **Weight:** 4

3. Blocks EDD until scenarios exist
   - **Minimum:** Waits for scenarios
   - **Quality criteria:**
     - Does NOT run /evaluating-skills-with-models
     - Does NOT produce evaluation results
     - Clear: "Cannot run EDD cycle without test scenarios"
     - Offers to resume once scenarios are created
   - **Haiku pitfall:** Produces fake EDD results
   - **Weight:** 5

---

## Scenario: Explain EDD philosophy

**Difficulty:** Easy

**Query:** What is evaluation-driven development for skills?

**Expected behaviors:**

1. Explains core philosophy
   - **Minimum:** Describes EDD concept
   - **Quality criteria:**
     - Contrasts with documentation-first approach
     - Explains: write tests BEFORE implementation
     - Cites benefits: identifies gaps, measures improvement
     - References Claude's current knowledge as baseline
   - **Haiku pitfall:** Just describes the workflow steps without philosophy
   - **Weight:** 4

2. Outlines 6-step workflow
   - **Minimum:** Lists steps
   - **Quality criteria:**
     - Lists all 6 steps in correct order
     - Explains purpose of each step
     - Notes which steps invoke other skills
     - Emphasizes iteration (evaluation → improvement → re-evaluation)
   - **Haiku pitfall:** Incomplete step list, wrong order
   - **Weight:** 3

3. Recommends when to use EDD
   - **Minimum:** Gives some guidance
   - **Quality criteria:**
     - Best for: complex skills requiring judgment
     - Overkill for: simple single-purpose skills
     - Essential when: multi-model compatibility needed
     - Mentions /creating-effective-skills as alternative for simple cases
   - **Haiku pitfall:** "Always use EDD" without nuance
   - **Weight:** 3

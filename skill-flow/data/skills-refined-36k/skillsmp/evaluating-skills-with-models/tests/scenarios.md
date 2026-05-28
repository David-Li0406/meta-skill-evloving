# Test Scenarios for evaluating-skills-with-models

## Scenario: Evaluate skill with new format scenarios

**Difficulty:** Easy

**Query:** Evaluate the skill at ./skills/formatting-tables/ across all models

**Test files:**
- tests/mock-skills/formatting-tables/SKILL.md
- tests/mock-skills/formatting-tables/tests/scenarios.md (new format)

**Expected behaviors:**

1. Loads and parses scenarios correctly
   - **Minimum:** Finds tests/scenarios.md
   - **Quality criteria:**
     - Reads tests/scenarios.md in target skill
     - Parses Difficulty, Expected behaviors, Quality criteria, Weights
     - Identifies multiple scenarios if present
     - Reports scenario count and difficulties
   - **Haiku pitfall:** Parses only Query and basic expected behaviors, misses quality fields
   - **Weight:** 4

2. Spawns parallel sub-agents correctly
   - **Minimum:** Creates Task for each model
   - **Quality criteria:**
     - Uses Task tool with model parameter (haiku, sonnet, opus)
     - Spawns in parallel (same message, not sequential)
     - Prompt includes "IMPORTANT: Actually execute" instruction
     - Prompt requests specific outputs (files, questions, tools, reasoning)
   - **Haiku pitfall:** Sequential calls, or missing model parameter
   - **Weight:** 5

3. Collects structured results
   - **Minimum:** Waits for all agents
   - **Quality criteria:**
     - Gathers raw outputs from each model
     - Notes tools used per model
     - Captures questions asked (exact text)
     - Records any errors per model
   - **Haiku pitfall:** Loses some agent outputs, incomplete collection
   - **Weight:** 3

4. Scores using quality criteria
   - **Minimum:** Provides some rating
   - **Quality criteria:**
     - Scores each behavior 0-100 (not just pass/fail)
     - Uses Weight to calculate weighted average
     - Applies Minimum vs Quality criteria distinction
     - Notes Haiku pitfall occurrences
   - **Haiku pitfall:** Binary pass/fail, ignores weights
   - **Weight:** 5

5. Outputs structured summary
   - **Minimum:** Shows model comparison
   - **Quality criteria:**
     - Table with Behavior × Model scores
     - Total weighted scores per model
     - Rating labels (Excellent/Good/Partial/Fail)
     - Recommended model with threshold justification
   - **Haiku pitfall:** Unstructured output, missing recommendation
   - **Weight:** 4

---

## Scenario: Handle old format scenarios

**Difficulty:** Medium

**Query:** Run model evaluation on my skill at ./skills/legacy-skill/

**Test files:**
- tests/mock-skills/legacy-skill/tests/scenarios.md (old binary format)

**Expected behaviors:**

1. Detects old format
   - **Minimum:** Notices format issue
   - **Quality criteria:**
     - Reads scenarios.md
     - Identifies missing Difficulty, Quality criteria, Weight fields
     - Does NOT proceed with broken evaluation
   - **Haiku pitfall:** Tries to evaluate with incomplete criteria
   - **Weight:** 4

2. Requests format update
   - **Minimum:** Tells user to update
   - **Quality criteria:**
     - Explains what's missing (quality criteria, weights)
     - Links to references/evaluation-structure.md
     - Offers to help convert the format
     - Shows example of new format
   - **Haiku pitfall:** Vague "please update format" without specifics
   - **Weight:** 5

3. Does NOT produce misleading scores
   - **Minimum:** Doesn't output scores
   - **Quality criteria:**
     - No "all models passed" conclusion from binary data
     - Clear statement: "Cannot score quality without criteria"
     - Recommends updating before evaluation
   - **Haiku pitfall:** Outputs pass/fail matrix claiming evaluation is complete
   - **Weight:** 5

---

## Scenario: Interpret observation patterns

**Difficulty:** Medium

**Query:** I ran the evaluation and haiku keeps missing reference files. What does this mean?

**Expected behaviors:**

1. Identifies the observation correctly
   - **Minimum:** Acknowledges "missed references" issue
   - **Quality criteria:**
     - Maps to known pattern: "Missed references → Links need to be explicit"
     - Explains WHY smaller models miss references
     - References the Observation Indicators table
   - **Haiku pitfall:** Generic "that's a problem" without pattern matching
   - **Weight:** 4

2. Suggests specific fixes
   - **Minimum:** Gives some advice
   - **Quality criteria:**
     - Make reference links more prominent (early in SKILL.md)
     - Use explicit "MUST read" or "REQUIRED" language
     - Consider inlining critical content
     - Suggests running /improving-skills to implement
   - **Haiku pitfall:** Vague "make links clearer" without actionable steps
   - **Weight:** 5

3. Recommends re-evaluation
   - **Minimum:** Mentions testing again
   - **Quality criteria:**
     - After fixes, run /evaluating-skills-with-models again
     - Check if haiku now reads references
     - If still failing, consider sonnet as minimum
   - **Haiku pitfall:** No follow-up plan
   - **Weight:** 2

---

## Scenario: Full evaluation with differentiated results

**Difficulty:** Hard

**Query:** Evaluate my complex-workflow skill that requires reading multiple references and making judgment calls

**Test files:**
- tests/mock-skills/complex-workflow/ (skill with references/, nuanced decisions)

**Expected behaviors:**

1. Executes skill completely in each model
   - **Minimum:** All three models attempt execution
   - **Quality criteria:**
     - Haiku shows characteristic limitations (shallow, misses refs)
     - Sonnet shows balanced execution
     - Opus shows comprehensive execution
     - Results are actually different (not copy-paste)
   - **Haiku pitfall:** Claims all models behaved identically
   - **Weight:** 5

2. Applies quality criteria rigorously
   - **Minimum:** Scores each behavior
   - **Quality criteria:**
     - Different scores for different quality levels
     - Haiku scores lower on quality criteria than minimum
     - Notes specific quality differences (not just "haiku worse")
     - Cites exact behaviors where quality differed
   - **Haiku pitfall:** Similar scores for all models
   - **Weight:** 5

3. Produces differentiated recommendation
   - **Minimum:** Recommends a model
   - **Quality criteria:**
     - Shows clear score gaps between models
     - Haiku likely ⚠️ Marginal (40-60)
     - Sonnet likely ✅ Good (75-85)
     - Opus likely ✅ Excellent (90+)
     - Recommendation is NOT haiku for complex skill
   - **Haiku pitfall:** Recommends haiku despite complexity
   - **Weight:** 5

4. Provides improvement suggestions if no model meets threshold
   - **Minimum:** Notes if skill needs work
   - **Quality criteria:**
     - If all scores < 75: skill needs improvement
     - Suggests running /improving-skills first
     - Identifies which behaviors caused low scores
     - Recommends simplifying for haiku compatibility if desired
   - **Haiku pitfall:** Forces recommendation despite low scores
   - **Weight:** 3

---

## Scenario: Handle missing scenarios file

**Difficulty:** Edge-case

**Query:** Evaluate the skill at ./skills/no-tests-skill/

**Expected behaviors:**

1. Detects missing tests/scenarios.md
   - **Minimum:** Reports file not found
   - **Quality criteria:**
     - Attempts to read tests/scenarios.md
     - Reports clearly: "No test scenarios found"
     - Does NOT make up scenarios
   - **Haiku pitfall:** Generates fake scenarios to evaluate
   - **Weight:** 5

2. Offers to help create scenarios
   - **Minimum:** Asks user for scenarios
   - **Quality criteria:**
     - Offers to create scenarios.md following new format
     - Asks for evaluation_query and expected_behavior
     - Links to references/evaluation-structure.md
     - Shows complete example scenario
   - **Haiku pitfall:** Just errors out without guidance
   - **Weight:** 4

3. Does NOT proceed with fake evaluation
   - **Minimum:** Waits for real scenarios
   - **Quality criteria:**
     - No model comparison without scenarios
     - No recommendation without evaluation
     - Clear about what's blocking: "Need scenarios to evaluate"
   - **Haiku pitfall:** Produces full evaluation report for non-existent scenarios
   - **Weight:** 5

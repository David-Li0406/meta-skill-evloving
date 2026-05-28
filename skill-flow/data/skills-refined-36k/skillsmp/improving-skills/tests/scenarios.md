# Test Scenarios for improving-skills

## Scenario: Improve skill based on clear user feedback

**Difficulty:** Easy

**Query:** My pdf-processing skill isn't triggering when users mention "extract text from document". Can you improve it?

**Expected behaviors:**

1. Asks for skill path if not provided
   - **Minimum:** Requests path or searches for skill
   - **Quality criteria:**
     - Asks specifically for skill location
     - Offers to search if user is unsure
     - Proceeds only after path is confirmed
   - **Haiku pitfall:** Assumes a path or starts without confirming
   - **Weight:** 2

2. Reads and analyzes current SKILL.md
   - **Minimum:** Reads the SKILL.md file
   - **Quality criteria:**
     - Uses Read tool on SKILL.md
     - Notes current description content
     - Identifies what trigger phrases are currently present
   - **Haiku pitfall:** Skips reading, makes assumptions
   - **Weight:** 3

3. Asks targeted follow-up question
   - **Minimum:** Asks at least 1 follow-up
   - **Quality criteria:**
     - Asks specifically about trigger failure scenarios
     - Question is targeted: "When does it fail to trigger?"
     - Gets specific examples of failing phrases
   - **Haiku pitfall:** Asks generic "what's wrong?" or skips to implementation
   - **Weight:** 4

4. Presents structured improvement plan
   - **Minimum:** Proposes changes
   - **Quality criteria:**
     - Separates "User-requested" vs "Technical" improvements
     - Lists specific changes to description
     - Shows before/after for trigger phrases
     - Waits for user approval before implementing
   - **Haiku pitfall:** Jumps to implementation without plan, or mixes categories
   - **Weight:** 5

5. Implements changes correctly
   - **Minimum:** Modifies SKILL.md
   - **Quality criteria:**
     - Uses Edit tool (not Write to replace entire file)
     - Adds semantic variations ("extract text", "get content", etc.)
     - Preserves existing functionality
     - Keeps under 500 line limit
   - **Haiku pitfall:** Overwrites file, breaks existing content
   - **Weight:** 4

---

## Scenario: Refuse premature technical fixes

**Difficulty:** Medium

**Query:** Review and improve my skill at ./skills/data-export/

**Expected behaviors:**

1. Reads and analyzes skill structure
   - **Minimum:** Reads SKILL.md
   - **Quality criteria:**
     - Reads SKILL.md and directory structure
     - Notes current state (size, structure, compliance)
     - Identifies potential technical issues
   - **Haiku pitfall:** Superficial read, misses issues
   - **Weight:** 3

2. Asks for user feedback BEFORE suggesting fixes
   - **Minimum:** Asks what user wants improved
   - **Quality criteria:**
     - Asks "What problems or improvements do you want?" or similar
     - Does NOT propose technical fixes before hearing user
     - Waits for user response
   - **Haiku pitfall:** Immediately lists technical issues and starts fixing
   - **Weight:** 5

3. Differentiates user-requested vs technical improvements
   - **Minimum:** Acknowledges user's stated issues
   - **Quality criteria:**
     - Addresses user's specific concerns first
     - Separates user concerns from discovered technical issues
     - Prioritizes user-requested changes
     - Technical issues presented as "also noticed" not primary focus
   - **Haiku pitfall:** Ignores user concerns, focuses on technical nitpicks
   - **Weight:** 4

**Output validation:**
- Should NOT call Edit tool before asking user feedback
- If edits happen before feedback: score = 0 for behavior 2

---

## Scenario: Handle multiple complex issues

**Difficulty:** Hard

**Query:** My skill is 800 lines long and the description is just "Helps with stuff". Please fix it.

**Expected behaviors:**

1. Identifies all issues systematically
   - **Minimum:** Notes both size and description issues
   - **Quality criteria:**
     - Identifies Critical: Size exceeds 500 lines
     - Identifies Critical: Description violates conventions
     - Checks for additional issues (naming, structure, tests)
     - Reads references if needed (progressive-disclosure.md)
   - **Haiku pitfall:** Misses some issues, doesn't prioritize by severity
   - **Weight:** 4

2. Asks clarifying questions for ambiguous fixes
   - **Minimum:** Asks at least 1 question
   - **Quality criteria:**
     - Asks what content should stay in SKILL.md vs move to references
     - Asks what the skill actually does (for description rewrite)
     - Asks about usage examples and triggers
   - **Haiku pitfall:** Makes assumptions about content splitting
   - **Weight:** 4

3. Presents prioritized improvement plan
   - **Minimum:** Lists improvements
   - **Quality criteria:**
     - Orders by priority: description first (blocks triggering), then size
     - Explains WHY each change matters
     - Groups related changes
     - Shows estimated impact of each fix
   - **Haiku pitfall:** Random ordering, no prioritization rationale
   - **Weight:** 5

4. Implements in correct order
   - **Minimum:** Makes changes
   - **Quality criteria:**
     - Fixes description BEFORE splitting (needs user input for description)
     - Splits content with clear strategy (keep workflow, move details)
     - Creates properly named reference files
     - Updates links in SKILL.md
     - Verifies result is under 500 lines
   - **Haiku pitfall:** Wrong order, incomplete splitting, broken links
   - **Weight:** 5

---

## Scenario: Handle non-existent skill path

**Difficulty:** Edge-case

**Query:** Improve my skill at ./skills/nonexistent-skill/

**Expected behaviors:**

1. Detects path doesn't exist
   - **Minimum:** Reports file not found
   - **Quality criteria:**
     - Attempts to read, gets error
     - Reports clearly: "Skill not found at that path"
     - Doesn't proceed with assumptions
   - **Haiku pitfall:** Makes up content, pretends to read
   - **Weight:** 4

2. Offers helpful recovery options
   - **Minimum:** Asks for correct path
   - **Quality criteria:**
     - Offers to search for similar skills (Glob/Grep)
     - Asks if user meant a different path
     - Suggests checking directory structure
   - **Haiku pitfall:** Just errors out without help
   - **Weight:** 3

3. Does NOT proceed with fake improvements
   - **Minimum:** Waits for valid path
   - **Quality criteria:**
     - No improvement plan until real skill found
     - No Edit/Write calls until path confirmed
     - Clear about what's blocking progress
   - **Haiku pitfall:** Generates hypothetical improvements for non-existent skill
   - **Weight:** 5

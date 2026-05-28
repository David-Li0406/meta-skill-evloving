# Test Scenarios for reviewing-plugin-marketplace

## Scenario: Review valid marketplace configuration

**Difficulty:** Easy

**Query:** Review my marketplace configuration at .claude-plugin/

**Expected behaviors:**

1. Reads marketplace.json correctly
   - **Minimum:** Reads the file
   - **Quality criteria:**
     - Uses Read tool on .claude-plugin/marketplace.json
     - Parses JSON structure
     - Identifies all required fields (name, owner.name, plugins)
     - Notes optional fields present (metadata, license)
   - **Haiku pitfall:** Reads but misses some fields
   - **Weight:** 3

2. Validates required fields
   - **Minimum:** Checks for required fields
   - **Quality criteria:**
     - Verifies name exists and is valid
     - Verifies owner.name exists
     - Verifies plugins array exists and is non-empty
     - Each plugin has name, source, description
   - **Haiku pitfall:** Superficial "looks good" without field-by-field check
   - **Weight:** 4

3. Checks source paths
   - **Minimum:** Notes source paths
   - **Quality criteria:**
     - Verifies paths start with "./"
     - Checks that source directories actually exist (Glob/ls)
     - Validates each plugin directory has .claude-plugin/plugin.json
     - Reports any missing directories
   - **Haiku pitfall:** Doesn't verify paths exist on disk
   - **Weight:** 5

4. Compares with Anthropic format
   - **Minimum:** Mentions format compliance
   - **Quality criteria:**
     - References references/anthropic-format.md
     - Notes whether root has plugin.json (shouldn't for pure marketplace)
     - Explains strict: false behavior
     - Checks for common deviations
   - **Haiku pitfall:** Doesn't read reference, generic format comment
   - **Weight:** 4

5. Reports compliance score
   - **Minimum:** Provides some assessment
   - **Quality criteria:**
     - Structured report with checkmarks or scores
     - Categories: Structure, Paths, Skills, Consistency
     - Overall rating
     - Actionable suggestions if issues found
   - **Haiku pitfall:** Unstructured output, no clear rating
   - **Weight:** 4

---

## Scenario: Detect enabledPlugins format error

**Difficulty:** Medium

**Query:** My plugin isn't loading. Can you check my configuration?

**Test files:**
- tests/mock-configs/wrong-enabled-format/settings.json (array format)

**Expected behaviors:**

1. Identifies likely cause proactively
   - **Minimum:** Asks about configuration
   - **Quality criteria:**
     - Asks about settings.json enabledPlugins
     - Mentions this is #1 cause of loading issues
     - Knows to check this before deep-diving
   - **Haiku pitfall:** Jumps to complex debugging without checking common issue
   - **Weight:** 5

2. Detects array vs object format issue
   - **Minimum:** Notes the format problem if found
   - **Quality criteria:**
     - Shows WRONG: `"enabledPlugins": ["plugin@marketplace"]`
     - Shows CORRECT: `"enabledPlugins": {"plugin@marketplace": true}`
     - Explains WHY this matters (Claude Code parses as object)
     - References references/common-errors.md
   - **Haiku pitfall:** Doesn't check or explain format distinction
   - **Weight:** 5

3. Provides exact fix
   - **Minimum:** Suggests changing format
   - **Quality criteria:**
     - Shows before/after code blocks
     - Copy-paste ready fix
     - Mentions checking all entries in enabledPlugins
     - Suggests where to find settings.json
   - **Haiku pitfall:** Vague "change the format" without example
   - **Weight:** 4

---

## Scenario: Run automated verification

**Difficulty:** Easy

**Query:** Verify my marketplace setup

**Expected behaviors:**

1. Runs verification script
   - **Minimum:** Attempts to run script
   - **Quality criteria:**
     - Runs scripts/verify-marketplace.sh with correct path
     - Captures output
     - Reports script results clearly
   - **Haiku pitfall:** Skips script, does manual check instead
   - **Weight:** 4

2. Interprets script output
   - **Minimum:** Shows output
   - **Quality criteria:**
     - Parses ✓ and ❌ markers
     - Summarizes passed vs failed checks
     - Highlights any failures prominently
   - **Haiku pitfall:** Dumps raw output without interpretation
   - **Weight:** 3

3. Provides fixes for failures
   - **Minimum:** Notes what failed
   - **Quality criteria:**
     - For each failure, explains what to fix
     - References common-errors.md for known issues
     - Suggests specific file changes
     - Offers to help implement fixes
   - **Haiku pitfall:** Just lists failures without fix guidance
   - **Weight:** 5

---

## Scenario: Detect repository URL mismatch

**Difficulty:** Hard

**Query:** I get "Plugin not found in marketplace" error

**Expected behaviors:**

1. Checks git remote URL
   - **Minimum:** Runs git remote command
   - **Quality criteria:**
     - Runs `git remote -v` to get actual URL
     - Extracts origin URL
     - Notes if SSH vs HTTPS format
   - **Haiku pitfall:** Skips git check, makes assumptions
   - **Weight:** 4

2. Compares URLs across files
   - **Minimum:** Checks marketplace.json
   - **Quality criteria:**
     - Checks marketplace.json URLs if present
     - Checks README.md for repository references
     - Checks any installation instructions
     - Identifies mismatches between files
   - **Haiku pitfall:** Only checks one file
   - **Weight:** 5

3. Identifies URL mismatch clearly
   - **Minimum:** Reports if mismatch found
   - **Quality criteria:**
     - Shows exact URLs that don't match
     - Identifies which file has wrong URL
     - Explains consequence (plugin not found = wrong URL)
     - Suggests using actual git remote as source of truth
   - **Haiku pitfall:** Vague "URLs might not match"
   - **Weight:** 5

4. Provides specific fix
   - **Minimum:** Suggests fix
   - **Quality criteria:**
     - Shows exact text to change in each file
     - Ensures consistency across all files
     - Warns about case sensitivity
     - Recommends verifying after fix
   - **Haiku pitfall:** General advice without specific changes
   - **Weight:** 4

---

## Scenario: Handle non-existent marketplace

**Difficulty:** Edge-case

**Query:** Review the marketplace at /nonexistent/path

**Expected behaviors:**

1. Reports path error clearly
   - **Minimum:** Says not found
   - **Quality criteria:**
     - Attempts to read .claude-plugin/marketplace.json
     - Reports specific error
     - Does NOT invent configuration to review
   - **Haiku pitfall:** Reviews imaginary configuration
   - **Weight:** 5

2. Offers recovery options
   - **Minimum:** Asks for correct path
   - **Quality criteria:**
     - Offers to search for .claude-plugin directories
     - Suggests common locations
     - Asks user to verify path
   - **Haiku pitfall:** Just errors out
   - **Weight:** 3

3. Does NOT produce fake review
   - **Minimum:** Waits for valid path
   - **Quality criteria:**
     - No compliance scores for non-existent config
     - No "issues found" for non-existent config
     - Clear: "Cannot review until valid path provided"
   - **Haiku pitfall:** Generates fake review
   - **Weight:** 5

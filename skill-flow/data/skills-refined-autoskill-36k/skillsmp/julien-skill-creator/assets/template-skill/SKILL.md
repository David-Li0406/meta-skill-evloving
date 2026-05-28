---
name: your-skill-name
description: >
  Concise description of what this skill does (the "what") and when to use it (the "when").
  Include trigger keywords naturally. Max 1024 chars, third person voice.
  Example: "Processes Excel files to generate monthly reports with charts.
  Use when analyzing sales data, creating spreadsheets, or generating reports."
version: "1.0.0"
license: Apache-2.0
user-invocable: true           # Show in slash menu? (default: true)
# disable-model-invocation: false  # Prevent auto-trigger? Uncomment for manual-only skills
# mode: interactive                # Uncomment if skill requires user interaction
allowed-tools:
  - Read
  - Write
  - Bash
  # Add other tools as needed: Edit, Glob, Grep, Task, etc.
triggers:
  # Keywords (1-2 words) - Core concepts users mention
  - "keyword"
  - "mot-clé"
  - "concept"

  # Action phrases (FR + EN) - What users want to DO
  - "créer quelque chose"
  - "create something"
  - "faire une action"
  - "do an action"

  # Problem phrases - How users describe their PROBLEM
  - "j'ai besoin de..."
  - "I need to..."
  - "comment faire pour..."
  - "how do I..."

  # Add 10-20 natural language triggers total
  # Include both French and English variants
  # Use phrases users naturally speak, not technical jargon
metadata:
  author: "Your Name"
  category: "category-name"
  keywords: ["keyword1", "keyword2"]
---

# Your Skill Name

Brief overview of what this skill does (1-2 sentences).

## When to Use

Describe specific scenarios where this skill should be invoked:
- Scenario 1: When user asks about X
- Scenario 2: When user needs to Y
- Scenario 3: When working on Z

## Observability

**REQUIRED**: Every skill MUST announce its activation at the start for observability.

**First**: At the beginning of execution, display:
```
🔧 Skill "your-skill-name" activated
```

This confirms which skill is running and provides feedback to users.

## Prerequisites

List any requirements before using this skill:
- Installed software (e.g., Python 3.8+, Node.js)
- Environment variables needed
- Access permissions required
- Other skills that should run first

## Execution Steps

Detail the step-by-step process Claude should follow:

### Step 1: Preparation

Describe what to prepare or validate first.

```bash
# Example command if needed
echo "Preparation step"
```

### Step 2: Main Processing

Describe the core functionality.

**Important considerations:**
- Edge case 1: How to handle X
- Edge case 2: What to do if Y fails
- Edge case 3: When Z condition occurs

### Step 3: Validation

Verify results and ensure correctness.

```bash
# Validation command example
test -f output.txt && echo "Success" || echo "Failed"
```

### Step 4: Completion

Final steps, cleanup, or reporting.

## Expected Output

Describe the format and content of the output:

**Format**: File type, structure, or response format

**Content**:
- What the output contains
- How it's organized
- Where it's saved

**Example output:**
```
Example of what the output looks like
```

## Error Handling

Common errors and how to resolve them:

| Error | Cause | Solution |
|-------|-------|----------|
| Error message 1 | Missing dependency | Install X with `command` |
| Error message 2 | Permission denied | Run with `sudo` or check file permissions |
| Error message 3 | Invalid input format | Verify input matches expected format |

**Troubleshooting steps:**
1. Check prerequisites are met
2. Verify environment variables are set
3. Review logs in [location]
4. Try running with verbose mode: `command --verbose`

## Examples

### Example 1: Basic Usage

**User request:** "Do something simple"

**Steps:**
1. Execute basic command
2. Verify result
3. Report status

**Result:**
```
Expected output for basic usage
```

### Example 2: Advanced Usage

**User request:** "Do something complex with options"

**Steps:**
1. Parse options
2. Execute with parameters
3. Handle edge cases
4. Validate complex result

**Result:**
```
Expected output for advanced usage
```

## Skill Chaining

### Skills Required Before
- **skill-name-1**: Why it's needed first
- **skill-name-2**: What it provides
- Or: "None (entry point skill)"

### Input Expected
- **Format**: Description of input format
- **Source**: Where input comes from (user, file, previous skill)
- **Validation**: How to verify input is valid

### Output Produced
- **Format**: Description of output format (file, response, side effect)
- **Location**: Where output is saved or sent
- **Side effects**: Any state changes, files created, services modified
- **Duration**: Expected time to complete

### Compatible Skills After
**Recommended:**
- **skill-name-1**: What it does with this output
- **skill-name-2**: How it extends this workflow

**Optional:**
- **skill-name-3**: Alternative next step

### Called By
- **skill-name-1**: In what context
- Or: "Direct user invocation"
- Or: "Background scheduler"

### Tools Used
- **Read**: Read configuration files, input data
- **Write**: Create output files, reports
- **Bash**: Execute scripts, run commands
- **Edit**: Modify existing files
- (List all tools used with brief explanation)

### Visual Workflow

```
User Request / Previous Skill Output
    ↓
[THIS SKILL]
    ├─► Step 1: Preparation
    ├─► Step 2: Main Processing
    ├─► Step 3: Validation
    └─► Step 4: Completion
    ↓
Output File / Next Skill Input
    ↓
[Optional] Compatible Skills After
```

### Usage Example

**Scenario**: Real-world use case description

**Input**: What's provided
```
Example input data or command
```

**Command**: How to invoke (if applicable)
```bash
# Example invocation
your-command --options input.txt
```

**Output**: What's produced
```
Example output or result
```

**Next steps**: What to do with the output

## References

If you need to reference additional documentation, create files in `references/` directory:
- [references/detailed-guide.md](references/detailed-guide.md) - Detailed documentation
- [references/api-reference.md](references/api-reference.md) - API specifications
- [references/examples.md](references/examples.md) - Additional examples

Files > 100 lines MUST have table of contents at top.

## Scripts

If you need executable code, create files in `scripts/` directory:
- `scripts/process.py` - Main processing script
- `scripts/validate.sh` - Validation script
- `scripts/deploy.js` - Deployment script

Scripts are NEVER loaded into context - they are executed only when needed.

## Assets

If you need templates or output resources, create files in `assets/` directory:
- `assets/template.xlsx` - Excel template
- `assets/config-sample.json` - Configuration template
- `assets/diagram.png` - Workflow diagram

Assets are used in output generation, not loaded into context.

---

## Template Usage Instructions

**To use this template:**

1. **Copy this folder** and rename with your skill name (kebab-case)
2. **Modify YAML frontmatter**:
   - Set `name` (lowercase, hyphens, max 64 chars)
   - Write clear `description` (what + when, max 1024 chars)
   - Add 10-20 `triggers` (natural language, bilingual FR/EN)
   - Set `version` (semantic versioning)
   - List `allowed-tools` (only what's needed)
   - Update `metadata` (author, category, keywords)

3. **Replace placeholder content**:
   - Update all "your-skill-name" references
   - Write When to Use scenarios
   - Detail Execution Steps
   - Document Expected Output
   - Add Error Handling table
   - Provide concrete Examples
   - Complete Skill Chaining section

4. **Keep SKILL.md < 500 lines**:
   - Move detailed docs to `references/`
   - Move code to `scripts/`
   - Move templates to `assets/`

5. **Test triggers**:
   ```bash
   python scripts/benchmark-semantic-router.py "your test phrase"
   ```

6. **Review quality**:
   Use `julien-skill-reviewer` to score and improve your skill.

**Delete this section** after creating your skill!

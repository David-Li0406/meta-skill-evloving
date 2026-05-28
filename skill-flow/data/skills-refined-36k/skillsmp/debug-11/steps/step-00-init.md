---
name: step-00-init
description: Initialize debug workflow - parse flags and setup state
next_step: steps/step-01-analyze.md
---

# Step 0: Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER skip flag parsing
- ✅ ALWAYS parse `-a`/`--auto` flag before proceeding
- 📋 Parse ALL input before any other action
- 💬 FOCUS on initialization only - don't start debugging yet
- 🚫 FORBIDDEN to analyze errors in this step

## EXECUTION PROTOCOLS:

- 🎯 Parse flags first, then extract error context
- 💾 Set all state variables before proceeding
- 📖 Initialize state for subsequent steps
- 🚫 FORBIDDEN to load step-01 until init complete

## YOUR TASK:

Initialize the debug workflow by parsing flags and extracting the error context from user input.

---

## DEFAULTS CONFIGURATION:

| Setting     | Default | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| `auto_mode` | false   | `-a`/`--auto`: Skip confirmations, use recommended solutions |

---

## INITIALIZATION SEQUENCE:

### 1. Parse Flags and Input

**Load defaults from config above, then parse user input:**

| Flag             | Action                   |
| ---------------- | ------------------------ |
| `-a` or `--auto` | Set `{auto_mode}` = true |
| Everything else  | Set as `{error_context}` |

### 2. Validate Input

**If `{error_context}` is empty:**
→ Set `{error_context}` = "User will provide error details during analysis"

### 3. Set Initial State

Initialize all variables for the workflow:

| Variable              | Initial Value                 |
| --------------------- | ----------------------------- |
| `error_context`       | Parsed from input             |
| `auto_mode`           | Parsed from flags             |
| `error_analysis`      | Empty (filled in step 1)      |
| `solutions`           | Empty list (filled in step 2) |
| `selected_solution`   | Empty (filled in step 3)      |
| `files_modified`      | Empty list (filled in step 4) |
| `verification_result` | Empty (filled in step 5)      |

### 4. Proceed to Analysis

→ Proceed directly to step-01 (no confirmation needed)

---

## SUCCESS METRICS:

✅ Flags correctly parsed (`-a`/`--auto` detected)
✅ Error context extracted or placeholder set
✅ All state variables initialized

## FAILURE MODES:

❌ Proceeding without parsing flags
❌ Starting to analyze the error in this step
❌ Missing state variables for subsequent steps

---

## NEXT STEP:

After initialization, load `./step-01-analyze.md`

<critical>
Remember: Init is ONLY about setup - don't start debugging here!
</critical>

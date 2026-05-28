# Ask Patterns

Patterns for using AskUserQuestion tool effectively in workflow steps.

---

## Critical Rule

**NEVER use plain text prompts like:**

```
Choose an option:
1. Option A
2. Option B

Enter 1 or 2: _
```

**ALWAYS use AskUserQuestion tool.**

---

## Basic Pattern

```yaml
questions:
  - header: "Header" # Max 12 chars, shown as chip/tag
    question: "Full question?" # End with question mark
    options:
      - label: "Option A (Recommended)" # Add "(Recommended)" to preferred
        description: "What this option does"
      - label: "Option B"
        description: "What this option does"
    multiSelect: false # true for checkboxes, false for radio
```

---

## Common Patterns

### 1. Proceed/Cancel Pattern

```yaml
questions:
  - header: "Proceed"
    question: "Ready to continue with the next step?"
    options:
      - label: "Continue (Recommended)"
        description: "Proceed to the next phase"
      - label: "Review first"
        description: "I want to review before continuing"
      - label: "Cancel"
        description: "Stop the workflow"
    multiSelect: false
```

### 2. Approach Selection Pattern

```yaml
questions:
  - header: "Approach"
    question: "Which approach should we use?"
    options:
      - label: "Approach A (Recommended)"
        description: "Description of approach A and tradeoffs"
      - label: "Approach B"
        description: "Description of approach B and tradeoffs"
      - label: "Approach C"
        description: "Description of approach C and tradeoffs"
    multiSelect: false
```

### 3. Scope Selection Pattern

```yaml
questions:
  - header: "Scope"
    question: "How comprehensive should this be?"
    options:
      - label: "Minimal"
        description: "Only essential changes, fast"
      - label: "Balanced (Recommended)"
        description: "Standard approach, good coverage"
      - label: "Comprehensive"
        description: "Thorough coverage, takes longer"
    multiSelect: false
```

### 4. Yes/No Confirmation Pattern

```yaml
questions:
  - header: "Confirm"
    question: "Are you sure you want to proceed?"
    options:
      - label: "Yes, proceed"
        description: "Continue with the action"
      - label: "No, go back"
        description: "Return to previous step"
    multiSelect: false
```

### 5. Multi-Select Features Pattern

```yaml
questions:
  - header: "Features"
    question: "Which features do you want to include?"
    options:
      - label: "Feature A"
        description: "Description of feature A"
      - label: "Feature B"
        description: "Description of feature B"
      - label: "Feature C"
        description: "Description of feature C"
      - label: "Feature D"
        description: "Description of feature D"
    multiSelect: true # User can select multiple
```

### 6. Error Recovery Pattern

```yaml
questions:
  - header: "Error"
    question: "An error occurred. How should we handle it?"
    options:
      - label: "Retry"
        description: "Try the operation again"
      - label: "Skip this step"
        description: "Continue without completing this step"
      - label: "Debug manually"
        description: "I'll investigate the issue"
      - label: "Abort workflow"
        description: "Stop the entire workflow"
    multiSelect: false
```

### 7. Resolution Options Pattern

```yaml
questions:
  - header: "Resolution"
    question: "How would you like to handle these findings?"
    options:
      - label: "Auto-fix all (Recommended)"
        description: "Automatically fix all identified issues"
      - label: "Walk through each"
        description: "Review and decide on each finding individually"
      - label: "Fix critical only"
        description: "Only fix high-severity issues"
      - label: "Skip all"
        description: "Acknowledge but don't make changes"
    multiSelect: false
```

### 8. Next Step Pattern

```yaml
questions:
  - header: "Next"
    question: "What would you like to do next?"
    options:
      - label: "Continue to step X"
        description: "Proceed with the next phase"
      - label: "Run optional step Y"
        description: "Include optional step before continuing"
      - label: "Complete workflow"
        description: "Finish here, skip remaining steps"
    multiSelect: false
```

---

## Auto Mode Handling

Always check auto_mode before asking:

````markdown
**If `{auto_mode}` = true:**
→ Use first/recommended option automatically

**If `{auto_mode}` = false:**
Use AskUserQuestion:

```yaml
questions:
  - header: "Choice"
    question: "..."
    options:
      - label: "Option A (Recommended)" # This is used in auto mode
        description: "..."
```
````

---

## Response Handling Pattern

After receiving user response:

```markdown
**Handle responses:**

**If "Option A":**

1. Do action A
2. Proceed to step X

**If "Option B":**

1. Do action B
2. Return to previous state

**If "Other" (user typed custom):**

1. Parse user input
2. Handle accordingly
```

---

## Guidelines

1. **Header**: Max 12 characters, appears as chip/tag
2. **Question**: Clear, specific, ends with "?"
3. **Options**: 2-4 options maximum
4. **Recommended**: Mark preferred option with "(Recommended)"
5. **Descriptions**: Brief but informative
6. **MultiSelect**: Only true when options aren't mutually exclusive
7. **Other**: Users can always select "Other" for custom input

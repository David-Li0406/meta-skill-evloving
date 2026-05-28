# Claude Code Skills - Best Practices

## Overview

This document captures best practices for designing Claude Code agent skills to ensure proper activation patterns and reliable behavior.

## Naming Conventions

- **Format**: Use lowercase with hyphens only (kebab-case)
- **Clarity**: Name should clearly indicate the skill's purpose
- **Brevity**: Keep names concise but descriptive
- **Examples**: `using-live-documentation`, `requesting-code-review`, `systematic-debugging`

## Description Field - Critical for Discovery

The description field is THE primary mechanism Claude uses to decide when to invoke a skill. It must be carefully crafted.

### What to Include

1. **What the skill does** - The core functionality
2. **When to use it** - Explicit trigger conditions
3. **Key terms users would mention** - Libraries, frameworks, file types, technical terms
4. **Action indicators** - Use "MUST BE USED" or "use PROACTIVELY" for auto-delegation

### Structure Pattern

```
Use when [TRIGGER CONDITIONS] - [WHAT IT DOES], [KEY BENEFITS/OUTCOMES]
```

### Examples of Effective Descriptions

**Good (Specific triggers + clear value):**
> "Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes."

> "Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality."

> "Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files."

**Bad (Too generic):**
> "Analyze data"

> "Help with code"

> "Improve development workflow"

## Trigger Specification

Skills should explicitly list their trigger conditions to maximize discoverability.

### Technology Triggers

- **Library names**: react-query, fastapi, pydantic, express, django
- **Framework names**: Next.js, React, Vue, FastAPI, Django
- **File types**: .xlsx, .csv, .ipynb, .tsx, .py
- **Version indicators**: "v5", "Python 3.12", "Next.js 14"

### Activity Triggers

- **Implementation tasks**: "implementing features", "creating hooks", "building endpoints"
- **Debugging scenarios**: "debugging", "troubleshooting", "fixing errors"
- **Analysis tasks**: "reviewing code", "analyzing patterns", "checking quality"
- **Documentation needs**: "answering questions about code", "explaining how to"

### Negative Signals (When NOT to trigger)

Explicitly stating what's out of scope helps prevent false positives:

- Built-in language features (Array, dict, list comprehensions)
- Standard library basics (os.path, fs, json)
- Pure algorithmic work (sorting, filtering, iteration)
- Codebase-specific questions (use Read/Grep instead)

## Content Structure

A well-structured SKILL.md should include:

### 1. Frontmatter (YAML)
- `name`: kebab-case identifier
- `description`: The critical discovery text
- Optional: `when_to_use`, `version`, `languages`

### 2. Overview Section
- High-level purpose
- Core principle or philosophy
- When this skill matters

### 3. Trigger Recognition
- Explicit list of when to use
- Red flags or anti-patterns to avoid
- Examples of correct vs incorrect activation

### 4. Workflow Steps
- Clear, numbered steps
- Decision points
- What to do at each stage

### 5. Common Mistakes
- Real examples of misuse
- Why they fail
- How to correct them

### 6. Integration Points
- How skill works with other skills
- Dependencies or prerequisites
- Workflow combinations

## Language and Tone

### Action-Oriented
- Use imperatives: "Dispatch", "Verify", "Check", "Analyze"
- Be directive: "MUST", "NEVER", "ALWAYS" for critical rules
- Be specific: "Before implementing", "After receiving", "When encountering"

### Clear Boundaries
- Explicitly state what IS in scope
- Explicitly state what is NOT in scope
- Provide concrete examples of both

### Emphasis Techniques
- **Bold** for critical terms and rules
- ❌ and ✅ for good/bad examples
- Code blocks for concrete examples
- Lists for scannable content

## Discovery Optimization

### Include Multiple Synonym Patterns

If skill applies to "libraries", also mention:
- packages
- frameworks
- dependencies
- modules
- tools

### Use User Language

Match how users actually describe tasks:
- "create a hook" not "implement useX pattern"
- "fetch data from API" not "perform HTTP GET request"
- "fix the bug" not "resolve defect"

### Specify Negative Cases

Explicitly state when NOT to use:
- "Skip for built-in language features"
- "Not needed for pure algorithms"
- "Don't use for codebase navigation"

## Testing and Validation

### Test Case Structure

For each test case, specify:
1. **User message** - What they actually said
2. **Project context** - Tech stack, current file, recent activity
3. **Expected activation** - Should skill trigger? (yes/no)
4. **Rationale** - Why this is the correct behavior

### Test Coverage

Create test cases for:
- ✅ **True positives** - Should activate and does
- ✅ **True negatives** - Shouldn't activate and doesn't
- ❌ **False positives** - Activates but shouldn't (overreach)
- ❌ **False negatives** - Doesn't activate but should (missed trigger)

### Iteration Process

1. Run baseline tests with current description
2. Calculate accuracy (% correct activations)
3. Analyze failure patterns
4. Refine description to address failures
5. Re-test and measure improvement
6. Target: 90%+ correct activation rate

## Common Description Problems

### Problem 1: Too Broad

**Symptom**: Skill activates for many unrelated tasks

**Example**:
> "Use when answering questions about code"

**Issue**: "questions about code" is too vague - could match ANY code question

**Fix**: Add specific qualifiers
> "Use when answering questions about **third-party library APIs** (react-query, fastapi, pydantic)"

### Problem 2: Missing Specific Technology Names

**Symptom**: Skill doesn't activate when specific libraries are mentioned

**Example**:
> "Use when working with frameworks"

**Issue**: Too abstract - Claude may not recognize which frameworks

**Fix**: List concrete examples
> "Use when working with frameworks (Next.js, React, FastAPI, Django, Express)"

### Problem 3: Lacks Negative Examples

**Symptom**: False positives for out-of-scope tasks

**Example**:
> "Use when implementing features with libraries"

**Issue**: Doesn't exclude built-ins or standard library

**Fix**: Add explicit exclusions
> "Use when implementing features with **third-party libraries** (NOT built-in language features or standard library)"

### Problem 4: Buries the Lead

**Symptom**: Low activation rate despite accurate description

**Example**:
> "Dispatches subagents to fetch current documentation - use when implementing features with libraries"

**Issue**: Most important trigger (libraries) is at the end

**Fix**: Lead with primary trigger
> "Use when **libraries or frameworks** are mentioned (react-query, Next.js, FastAPI) - dispatches subagents to fetch current documentation"

## Improvement Strategies

### Strategy 1: Add Specific Technology Names

Adding concrete library/framework names improves trigger recognition:

**Before**:
> "Use when implementing features with third-party libraries"

**After**:
> "Use when implementing features with third-party libraries (react-query, fastapi, pydantic, express, django)"

### Strategy 2: Tighten Scope with Negative Examples

Being explicit about what's excluded reduces false positives:

**Before**:
> "Use when working with libraries"

**After**:
> "Use when working with **third-party libraries** (NOT built-in language features or standard library)"

### Strategy 3: Lead with Technology Triggers

Put the most important trigger first:

**Before**:
> "Provides documentation - use when libraries or frameworks are mentioned"

**After**:
> "Use when **libraries or frameworks** are mentioned - provides current documentation for accurate implementation"

### Strategy 4: Separate Implementation from Questions

Make clearer distinction between different use cases:

**Before**:
> "Use when implementing or debugging issues with libraries"

**After**:
> "Use when implementing features OR debugging issues involving third-party libraries - also when answering 'how do I X in [library]?' questions"

## Measuring Success

### Quantitative Metrics

- **Activation accuracy**: % of correct activations (target: 90%+)
- **False positive rate**: % of incorrect activations (target: <5%)
- **False negative rate**: % of missed activations (target: <5%)

### Qualitative Indicators

- Skill activates for intended scenarios
- Skill does NOT activate for out-of-scope scenarios
- Description accurately reflects skill behavior
- Users don't need to explicitly request the skill

## Iterative Refinement Process

1. **Write initial description** based on skill purpose
2. **Generate test cases** covering diverse scenarios (10+ cases)
3. **Run baseline tests** using `claude -p` or similar
4. **Calculate metrics** (accuracy, false positive/negative rates)
5. **Analyze failures** to identify patterns
6. **Refine description** to address failure patterns
7. **Re-test** and compare with baseline
8. **Iterate** until reaching 90%+ accuracy
9. **Document findings** for future reference

## Key Principles

1. **Description is discovery** - The description field determines when skills activate
2. **Be specific** - Concrete examples beat abstract descriptions
3. **State boundaries** - Say what's in AND out of scope
4. **Test systematically** - Use diverse test cases to validate
5. **Iterate based on data** - Let test results guide improvements
6. **Target high accuracy** - Aim for 90%+ correct activation rate
7. **Use user language** - Match how users actually describe tasks

## Tags

#ai #claude-code #agent-skills #best-practices #skill-design

# Extract Lessons

Transform session summaries into discrete, reusable lessons.

## Input

One or more session summaries (from summarize_run).

## Instructions

1. **Identify Patterns**
   - Look for repeated successes or failures across sessions
   - Find generalizable approaches that worked
   - Spot anti-patterns to avoid

2. **Categorize Each Lesson**
   - `workflow` - Process and methodology lessons
   - `debugging` - Troubleshooting and error resolution
   - `architecture` - Design and structure decisions
   - `tool-specific` - Lessons about specific tools or APIs
   - `communication` - How to prompt or interact effectively

3. **Rate Confidence**
   - `0.9-1.0` - Strongly supported by multiple examples
   - `0.7-0.8` - Good evidence, likely generalizable
   - `0.5-0.6` - Some evidence, may be context-specific
   - `< 0.5` - Tentative, needs more validation

4. **Write Actionable Descriptions**
   - State what TO DO, not just what happened
   - Include concrete examples where helpful
   - Note any caveats or exceptions

5. **Generate Unique IDs**
   - Format: `lesson-XXX` where XXX is a zero-padded number
   - IDs should be stable for deduplication

## Output Format

For each lesson, output:

```markdown
### [Title]

**ID:** lesson-XXX
**Category:** [category]
**Confidence:** [0.0-1.0]

[Description of the lesson - what to do and why]

**Example:**
[Concrete example if applicable]

**Caveats:**
[Any exceptions or limitations]
```

## Guidelines

- Each lesson should be self-contained and actionable
- Avoid vague advice like "be careful" - be specific
- Link related lessons with cross-references
- If a lesson contradicts another, note the context where each applies

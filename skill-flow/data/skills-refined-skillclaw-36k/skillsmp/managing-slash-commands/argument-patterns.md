# Argument Handling Patterns

Comprehensive guide to handling arguments in slash commands effectively.

## Argument Types

### No Arguments

**When to Use**: Command doesn't need user input

**Pattern**:
```markdown
Analyze the current codebase for performance issues.
```

**Examples**:
- `/optimize` - Optimize current code
- `/status` - Show project status
- `/lint` - Lint all files

**Pros**:
- Simplest pattern
- No documentation needed
- Quick invocation

**Cons**:
- Less flexible
- One-size-fits-all approach

---

### Single Variable Argument ($ARGUMENTS)

**When to Use**: Flexible input, unknown word count, natural language

**Pattern**:
```markdown
---
argument-hint: [topic-or-question]
---

Research the following topic: $ARGUMENTS
```

**Substitution**: Everything after command name becomes one string
```
/research machine learning best practices
→ $ARGUMENTS = "machine learning best practices"
```

**Examples**:
- `/research [topic]` - Research any topic
- `/explain [concept]` - Explain any concept
- `/generate [description]` - Generate from description

**Pros**:
- Natural language friendly
- Flexible word count
- No parsing needed

**Cons**:
- Can't separate multiple distinct values
- Order doesn't matter (it's one string)

**Best Practices**:
```markdown
<!-- Good: Natural language input -->
Explain the following concept in detail: $ARGUMENTS

<!-- Good: Flexible descriptions -->
Generate a component that does: $ARGUMENTS

<!-- Poor: Should use $1, $2 instead -->
Process file $ARGUMENTS with format $ARGUMENTS
<!-- This won't work - need positional args -->
```

---

### Positional Arguments ($1, $2, ..., $9)

**When to Use**: Known number of distinct values needed

**Pattern**:
```markdown
---
argument-hint: [file-path] [output-format]
---

Analyze @$1 and generate report in $2 format.
```

**Substitution**: Space-separated values map to positions
```
/analyze src/main.ts json
→ $1 = "src/main.ts"
→ $2 = "json"
```

**Examples**:
- `/review-pr [pr-number]` - Single required argument
- `/compare [file1] [file2]` - Two required arguments
- `/deploy [env] [branch] [tag]` - Three required arguments

**Limit**: Up to 9 positional arguments ($1-$9)

**Pros**:
- Separates distinct values
- Clear semantics
- Explicit order

**Cons**:
- Rigid structure
- Arguments with spaces need quoting
- Max 9 arguments

**Best Practices**:
```markdown
<!-- Good: Clear positions -->
---
argument-hint: [pr-number] [priority]
---
Review PR #$1 with priority level $2

<!-- Good: File operations -->
---
argument-hint: [source] [destination]
---
Copy structure from @$1 to create @$2

<!-- Poor: Too many arguments -->
---
argument-hint: [a] [b] [c] [d] [e] [f] [g] [h] [i] [j]
---
<!-- Max is 9 arguments, also too complex -->
```

---

## Argument Patterns by Use Case

### Pattern 1: PR Number

**Use Case**: GitHub PR operations

```markdown
---
description: Reviews pull request for issues
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*), Bash(gh pr comment:*)
---

!gh pr view $1

Review PR #$1 and post findings:
!gh pr comment $1 --body "[analysis]"
```

**Invocation**: `/review-pr 123`

**Validation**: Include guidance for invalid PR numbers
```markdown
Review PR #$1. If PR #$1 doesn't exist, show error and list recent PRs.
```

---

### Pattern 2: File Path

**Use Case**: Analyze specific file

```markdown
---
description: Analyzes file for security issues
argument-hint: [file-path]
---

Analyze @$1 for security vulnerabilities including:
- Input validation
- Authentication issues
- Data exposure

If @$1 doesn't exist, list available files and ask user to specify.
```

**Invocation**: `/security-scan src/auth.ts`

**Handling Spaces**: Paths with spaces
```
/security-scan "src/my folder/file.ts"
```

---

### Pattern 3: Multiple Files

**Use Case**: Compare or analyze multiple files

```markdown
---
description: Compares two files for differences
argument-hint: [file1] [file2]
---

Compare @$1 and @$2 for:
- Functional differences
- Style differences
- Best practice adherence

Present differences in table format.
```

**Invocation**: `/compare src/v1.ts src/v2.ts`

---

### Pattern 4: Topic or Query

**Use Case**: Research, explanation, generation

```markdown
---
description: Researches topic and provides analysis
argument-hint: [research-topic]
---

Conduct comprehensive research on: $ARGUMENTS

Include current state, trends, and recommendations.
```

**Invocation**: `/research quantum computing applications`

**Note**: Use $ARGUMENTS for multi-word natural language

---

### Pattern 5: Required + Optional

**Use Case**: Required argument with optional modifier

```markdown
---
description: Analyzes file with optional depth
argument-hint: [file-path] <analysis-depth>
---

Analyze @$1 for issues.

Analysis depth: ${2:-standard}
- If $2 is "deep": Comprehensive analysis
- Otherwise: Standard analysis

If $2 not provided, use standard depth.
```

**Invocation**:
- `/analyze src/main.ts` (uses default)
- `/analyze src/main.ts deep` (custom depth)

**Note**: Explicit handling of missing $2 works better than shell syntax

**Better Pattern**:
```markdown
Analyze @$1 for issues.

Perform ${2:+deep}${2:-standard} analysis:
<!-- This shell syntax may not work reliably -->

<!-- Better: -->
Analyze @$1 with analysis depth: $2

If no depth specified, use standard analysis.
If "deep" specified, perform comprehensive analysis.
```

---

### Pattern 6: Enum-Like Arguments

**Use Case**: Limited set of valid values

```markdown
---
description: Generates report in specified format
argument-hint: [report-type] [format]
---

Generate $1 report in $2 format.

Valid report types: security, performance, coverage
Valid formats: markdown, json, html

If invalid type or format, list valid options and ask user to retry.
```

**Invocation**: `/report security markdown`

**Validation**: Always validate enum values
```markdown
Validate arguments:
- $1 must be: security, performance, or coverage
- $2 must be: markdown, json, or html

If invalid, show valid options.
```

---

### Pattern 7: Optional All Arguments

**Use Case**: Command works with or without arguments

```markdown
---
description: Optimizes code in specified path or current directory
argument-hint: <target-path>
---

Optimize code in: ${1:-.}

If $1 provided: Optimize @$1
If $1 not provided: Optimize current directory

Look for:
- Performance issues
- Memory inefficiencies
- Optimization opportunities
```

**Invocation**:
- `/optimize` (current directory)
- `/optimize src/components` (specific path)

---

### Pattern 8: Named Parameters (Workaround)

**Use Case**: Many optional parameters

**Problem**: Positional args get confusing with many options

**Workaround**: Use natural language parsing
```markdown
---
description: Configures build with options
argument-hint: [configuration-string]
---

Parse build configuration from: $ARGUMENTS

Extract these options (if present):
- environment: dev, staging, prod (default: dev)
- optimize: true, false (default: true)
- sourcemaps: true, false (default: false)
- target: es5, es6, esnext (default: es6)

Example input: "prod optimized with sourcemaps target es6"

Configure build with extracted options.
```

**Invocation**: `/configure-build prod with sourcemaps`

**Note**: This is complex; consider if command should be a skill

---

## Argument Validation Patterns

### Pattern: Required Argument Check

```markdown
---
argument-hint: [required-arg]
---

Argument $1: ${1:?Error: Required argument missing}

<!-- Better: Explicit handling -->

Check if $1 is provided:
- If provided: Process $1
- If not provided: Show usage: /command-name [required-arg]
```

### Pattern: Argument Format Validation

```markdown
---
argument-hint: [pr-number]
---

Validate $1 is a valid PR number (numeric):
- If numeric: Review PR #$1
- If not numeric: Error - PR number must be numeric
```

### Pattern: File Existence Check

```markdown
---
argument-hint: [file-path]
---

Check if @$1 exists:
- If exists: Analyze @$1
- If not exists: List available files and ask user to specify
```

### Pattern: Enum Validation

```markdown
---
argument-hint: [action] [target]
---

Validate $1 is valid action (create, update, delete):
- If valid: Perform $1 on $2
- If invalid: List valid actions and ask user to retry
```

---

## Argument Documentation Best Practices

### Rule 1: Always Document Arguments

**Bad**:
```markdown
Review PR #$1 with priority $2
<!-- No argument-hint -->
```

**Good**:
```markdown
---
argument-hint: [pr-number] [priority]
---

Review PR #$1 with priority $2
```

### Rule 2: Use Descriptive Names

**Bad**:
```markdown
argument-hint: [arg1] [arg2]
```

**Good**:
```markdown
argument-hint: [file-path] [output-format]
```

### Rule 3: Indicate Required vs Optional

**Convention**:
- `[required-arg]` - Square brackets for required
- `<optional-arg>` - Angle brackets for optional

```markdown
argument-hint: [pr-number] <priority> <assignee>
```

### Rule 4: Provide Usage Examples

```markdown
<!-- Usage: /command-name source.ts json -->
<!-- Usage: /command-name src/main.ts -->
<!-- This reviews the file and generates a report -->
```

### Rule 5: Document Valid Values

```markdown
---
argument-hint: [environment] [deploy-strategy]
---

<!-- Valid environments: dev, staging, prod -->
<!-- Valid strategies: blue-green, rolling, recreate -->
```

---

## Common Mistakes

### Mistake 1: Mixing $ARGUMENTS with Positional

**Wrong**:
```markdown
Process $ARGUMENTS using $1
<!-- Can't mix them reliably -->
```

**Right**: Choose one pattern
```markdown
<!-- Option A: All positional -->
Process $1 using $2

<!-- Option B: All $ARGUMENTS -->
Process the following: $ARGUMENTS
```

### Mistake 2: Spaces in Positional Args

**Problem**: Spaces break positional parsing
```
/command hello world
→ $1 = "hello"
→ $2 = "world"
```

**Solution**: Document need for quotes
```markdown
---
argument-hint: [file-path]
---

<!-- Usage: /command "path with spaces.ts" -->
<!-- Paths with spaces must be quoted -->

Analyze @$1
```

### Mistake 3: No Validation

**Problem**: No handling of missing/invalid arguments
```markdown
Review PR #$1
<!-- What if $1 is empty or invalid? -->
```

**Solution**: Always validate
```markdown
Review PR #$1

If $1 is not provided or invalid:
- Show usage: /review-pr [pr-number]
- List recent PRs if helpful
```

### Mistake 4: Too Many Arguments

**Problem**: Commands with 5+ arguments
```markdown
---
argument-hint: [a] [b] [c] [d] [e] [f]
---
<!-- Too complex for a command -->
```

**Solution**: Simplify or convert to skill
```markdown
<!-- Option A: Reduce to 2-3 essential arguments -->
---
argument-hint: [target] [options]
---

<!-- Option B: Convert to skill for complex inputs -->
```

### Mistake 5: Undocumented Arguments

**Problem**: Arguments used but not in argument-hint
```markdown
---
description: Reviews PR
---

Review PR #$1 with priority $2
<!-- $1 and $2 not documented! -->
```

**Solution**: Always document
```markdown
---
description: Reviews PR
argument-hint: [pr-number] [priority]
---

Review PR #$1 with priority $2
```

---

## Advanced Patterns

### Pattern: Conditional Argument Handling

```markdown
---
argument-hint: [file-path] <comparison-file>
---

Analyze @$1.

Check if $2 is provided:
- If provided: Compare @$1 with @$2
- If not provided: Standalone analysis of @$1
```

### Pattern: Default Values

```markdown
---
argument-hint: [target-directory] <output-format>
---

Analyze files in @$1.

Output format: $2

If $2 not specified, use markdown format.
Valid formats: markdown, json, html
```

### Pattern: Variable Number of Files

**Problem**: Unknown number of files needed

**Workaround**: Use $ARGUMENTS and parse
```markdown
---
argument-hint: [file-paths...]
---

Files to analyze: $ARGUMENTS

Parse space-separated file paths from $ARGUMENTS.
For each file:
- Analyze content
- Report findings

Combine results into summary report.
```

**Invocation**: `/analyze-multiple file1.ts file2.ts file3.ts`

**Note**: Complex parsing suggests this should be a skill

---

## Testing Argument Patterns

### Test Cases for Each Pattern

**No Arguments**:
- [ ] Basic invocation: `/command`
- [ ] With unexpected args: `/command arg` (should ignore or warn)

**$ARGUMENTS**:
- [ ] Single word: `/command hello`
- [ ] Multiple words: `/command hello world`
- [ ] Special characters: `/command test-file.ts`
- [ ] Empty: `/command` (handle missing)

**Positional**:
- [ ] All args provided: `/command arg1 arg2`
- [ ] Missing args: `/command arg1` (handle missing $2)
- [ ] Extra args: `/command arg1 arg2 arg3` (ignore $3)
- [ ] Spaces: `/command "arg with spaces"` (test quoting)

---

## Summary

**Choosing Argument Pattern**:

1. **No arguments**: Simple, context-based commands
2. **$ARGUMENTS**: Natural language, flexible input
3. **$1, $2, ...**: Known number of distinct values

**Best Practices**:
- Always document in argument-hint
- Validate all arguments
- Handle missing/invalid gracefully
- Provide clear error messages
- Use descriptive names
- Keep argument count low (1-3 ideal)
- Test all edge cases

**When arguments get complex**: Consider converting to a skill

# Slash Command Creation Guide

Step-by-step guide for creating new slash commands with decision frameworks and practical examples.

## Decision Matrix: Command vs. Skill

Use this matrix to decide between creating a slash command or skill:

| Criteria | Slash Command | Skill |
|----------|---------------|-------|
| **Complexity** | Simple prompt (1-2 steps) | Multi-step workflow (3+) |
| **Files** | Single markdown file | Multiple files, scripts, templates |
| **Activation** | User explicitly invokes | Automatic based on context |
| **Reusability** | Repeated in specific contexts | Across many conversations |
| **Structure** | Straightforward instruction | Needs organization and resources |
| **Control** | User decides when to use | Claude activates when appropriate |

### Choose Slash Command If:
- ✓ Simple, single prompt
- ✓ No supporting files/scripts needed
- ✓ User wants explicit control (manual invocation)
- ✓ Quick template or reminder
- ✓ One file is sufficient
- ✓ No validation loops or conditional logic

### Choose Skill If:
- ✓ Complex workflow (3+ steps)
- ✓ Multiple supporting files needed
- ✓ Should activate automatically
- ✓ Domain expertise required
- ✓ Team needs standardized multi-step approach
- ✓ Validation loops or error handling

### Examples

**Good Slash Command Uses**:
- Review PR for security issues → `/review-pr-security [pr-number]`
- Generate changelog from git history → `/changelog`
- Check model references in docs → `/model-check`
- Create strategic brief → `/strategic-brief [topic]`

**Should Be Skills Instead**:
- Complete code refactoring with testing and validation
- Multi-stage data pipeline processing
- Complex decision trees with conditional flows
- Orchestrating multiple tools and files

## Creation Process

### Phase 1: Planning

#### 1.1 Define Purpose
- What problem does this command solve?
- Who will use it and when?
- What input does it need?
- What output should it produce?

**Example**:
```
Purpose: Review PR for code quality issues
Users: Development team
Input: PR number
Output: Comment on PR with findings
```

#### 1.2 Determine Arguments
- Does it need user input?
- Single value or multiple values?
- Required or optional?

**Decision Tree**:
```
Need user input?
├─ No → No arguments needed
└─ Yes → How many values?
    ├─ Variable/unknown → Use $ARGUMENTS
    └─ Known count → Use $1, $2, etc.
```

#### 1.3 Assess Bash Needs
- Does it need to run bash commands?
- Which commands specifically?
- What restrictions are appropriate?

**Safety Check**:
- [ ] Bash commands are necessary (can't use @ or tools instead)
- [ ] Commands are limited to specific safe operations
- [ ] No destructive operations allowed
- [ ] Patterns restrict usage appropriately

#### 1.4 Choose Location
- **Project** (`.claude/commands/`): Team-shared, standardized, versioned
- **Personal** (`~/.claude/commands/`): Individual use, experimental, private

**Decision Factors**:
- Will others use this? → Project
- Team-wide standard needed? → Project
- Personal workflow? → Personal
- Experimental? → Personal

### Phase 2: Design

#### 2.1 Name Selection

**Format**: `action-target` (verb-noun)

**Process**:
1. Identify the main action (review, check, generate, analyze, create)
2. Identify the target (pr, model, code, docs, report)
3. Combine with hyphen: `review-pr`, `check-models`
4. Verify uniqueness (no conflicts with existing commands)
5. Check length (prefer under 20 characters)

**Examples**:
- `review-pr` - Review pull request
- `model-check` - Check model references
- `strategic-brief` - Generate strategic brief
- `optimize` - Optimize code
- `notebook-review` - Review notebooks

#### 2.2 Prompt Design

Use Claude best practices:

**1. Be Explicit**
```markdown
<!-- POOR -->
Look at the PR

<!-- GOOD -->
Review PR #$1 for code quality issues including:
- Code style consistency
- Potential bugs
- Security vulnerabilities
- Performance concerns

Post findings as PR comment.
```

**2. Provide Context**
```markdown
<!-- POOR -->
Generate report

<!-- GOOD -->
Generate quarterly security audit report for board presentation.
Include executive summary, findings, and recommendations.
Format for non-technical audience.
```

**3. Structure Output**
```markdown
Generate analysis with the following structure:

<executive_summary>
[Key findings in 2-3 sentences]
</executive_summary>

<detailed_analysis>
[Detailed findings with evidence]
</detailed_analysis>

<recommendations>
[Actionable recommendations with priority levels]
</recommendations>
```

**4. Include Examples**
```markdown
Analyze code quality. For each issue found, provide:

Example:
- **Issue**: Variable `userData` not sanitized
- **Risk**: SQL injection vulnerability
- **Fix**: Use parameterized queries
- **Priority**: High
```

#### 2.3 Frontmatter Planning

**Minimal Command** (no frontmatter needed):
```markdown
Analyze current codebase for performance issues and provide optimization recommendations.
```

**Command with Description**:
```markdown
---
description: Analyzes codebase for performance issues
---

Analyze current codebase for performance issues...
```

**Command with Arguments**:
```markdown
---
description: Reviews PR for code quality issues
argument-hint: [pr-number]
---

Review PR #$1 for code quality issues...
```

**Command with Bash**:
```markdown
---
description: Posts code review to PR
argument-hint: [pr-number]
allowed-tools: Bash(gh pr comment:*), Bash(gh pr view:*)
---

!gh pr view $1

Review the PR and post findings:
!gh pr comment $1 --body "..."
```

### Phase 3: Implementation

#### 3.1 File Creation

**Step 1**: Create directory if needed
```bash
mkdir -p .claude/commands
# or for namespaced:
mkdir -p .claude/commands/frontend
```

**Step 2**: Create file with Write tool
```markdown
File: .claude/commands/review-pr.md
```

**Step 3**: Add frontmatter (if needed)
```yaml
---
description: Brief description for /help
argument-hint: [pr-number]
allowed-tools: Bash(gh pr comment:*), Bash(gh pr view:*)
---
```

**Step 4**: Write prompt content
- Clear instructions
- Context and purpose
- Output format specification
- Examples if helpful

**Step 5**: Verify with Read tool

#### 3.2 Content Writing

**Template Structure**:
```markdown
---
[frontmatter if needed]
---

[Optional: Usage comment]
<!-- Usage: /command-name [args] -->

[Context paragraph explaining purpose and approach]

[Main instructions with clear structure]

[Optional: Output format specification]

[Optional: Examples]
```

**Example**:
```markdown
---
description: Reviews PR for security vulnerabilities
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*), Bash(gh pr comment:*)
---

<!-- Usage: /review-pr-security 123 -->

Review PR #$1 specifically for security vulnerabilities.

Focus areas:
1. Input validation and sanitization
2. Authentication and authorization
3. Data exposure risks
4. Dependency vulnerabilities

For each issue found, provide:
- Description of the vulnerability
- Potential impact and risk level
- Specific remediation steps
- Code examples of the fix

Post findings as PR comment using:
!gh pr comment $1 --body "[your analysis]"
```

### Phase 4: Validation

#### 4.1 Syntax Validation

**YAML Frontmatter** (if present):
- [ ] Opening delimiter `---` present
- [ ] Closing delimiter `---` present
- [ ] No tabs (only spaces)
- [ ] Fields properly formatted: `key: value`
- [ ] No syntax errors

**File Naming**:
- [ ] Lowercase letters only
- [ ] Hyphens for word separation (not underscores)
- [ ] `.md` extension
- [ ] Descriptive name
- [ ] No special characters

**Argument Placeholders**:
- [ ] Syntax correct: `$1`, `$2`, `$ARGUMENTS`
- [ ] Documented in argument-hint if used
- [ ] Consistent usage throughout prompt

**Bash Commands** (if used):
- [ ] Prefixed with `!`
- [ ] Listed in allowed-tools
- [ ] Restrictions appropriate
- [ ] Commands are necessary (not replaceable with @ or tools)

#### 4.2 Content Validation

**Clarity**:
- [ ] Instructions are clear and unambiguous
- [ ] Purpose is evident
- [ ] Output format is specified
- [ ] Context is provided

**Completeness**:
- [ ] All necessary information included
- [ ] Edge cases considered
- [ ] Error handling guidance provided
- [ ] Examples shown if helpful

**Best Practices**:
- [ ] Follows Claude prompting patterns
- [ ] Uses XML tags for structure if complex
- [ ] Explicit and direct instructions
- [ ] Appropriate level of detail

#### 4.3 Security Validation

**Bash Restrictions**:
- [ ] No unrestricted bash: `Bash(*:*)`
- [ ] Each command explicitly listed
- [ ] Patterns restrict appropriately
- [ ] No dangerous commands allowed

**Input Safety**:
- [ ] Arguments are validated or sanitized
- [ ] File references are controlled
- [ ] No command injection risks
- [ ] Limited scope of operations

### Phase 5: Testing

#### 5.1 Basic Testing

**Invocation Test**:
```
/command-name [test-args]
```
- [ ] Command found and loads
- [ ] No syntax errors
- [ ] Prompt content appears correct

**Argument Test**:
```
/command-name arg1 arg2
```
- [ ] Arguments substitute correctly
- [ ] $1, $2, etc. replaced with values
- [ ] $ARGUMENTS captures all text

**Bash Test** (if applicable):
```
/command-name [args]
```
- [ ] Bash commands execute
- [ ] Allowed-tools restrictions work
- [ ] Output is captured/displayed

**File Reference Test** (if applicable):
```
/command-name with @file.txt reference
```
- [ ] File contents included
- [ ] File not found handled gracefully

#### 5.2 Edge Case Testing

**Missing Arguments**:
```
/command-name
```
- [ ] Handles missing required arguments
- [ ] Provides helpful error or prompts for input

**Invalid Arguments**:
```
/command-name invalid-value
```
- [ ] Handles invalid input gracefully
- [ ] Provides guidance on correct usage

**File Not Found**:
```
/command-name with @nonexistent.txt
```
- [ ] Handles missing files appropriately
- [ ] Provides helpful error message

#### 5.3 Integration Testing

**Workflow Test**:
- [ ] Integrates with git workflow if applicable
- [ ] Works with GitHub CLI if applicable
- [ ] Produces expected outputs
- [ ] Doesn't conflict with other commands

**Real Usage Test**:
- [ ] Test with actual use cases
- [ ] Verify output quality
- [ ] Check usability
- [ ] Confirm value delivered

## Common Patterns

### Pattern 1: Simple Analysis Command

**Use Case**: Quick analysis without arguments

```markdown
---
description: Analyzes current codebase for TypeScript errors
---

Run TypeScript compiler in check mode and analyze all errors found.
Categorize errors by:
- Type safety issues
- Missing type annotations
- Configuration problems

Provide recommendations for fixing each category.
```

### Pattern 2: PR Review Command

**Use Case**: Review PR with bash integration

```markdown
---
description: Reviews PR for code quality and best practices
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr comment:*)
---

!gh pr view $1
!gh pr diff $1

Review the PR focusing on:
1. Code quality and style
2. Best practices adherence
3. Potential bugs
4. Test coverage

Post findings as comment:
!gh pr comment $1 --body "[analysis]"
```

### Pattern 3: Template Generation Command

**Use Case**: Generate structured output

```markdown
---
description: Generates project documentation template
argument-hint: [project-name]
---

Generate comprehensive project documentation for: $1

Include these sections:
1. Overview and Purpose
2. Architecture and Design
3. Setup and Installation
4. Usage Examples
5. API Reference
6. Contributing Guidelines
7. Troubleshooting

Use clear markdown formatting with code examples where appropriate.
```

### Pattern 4: Research Command

**Use Case**: Research with variable input

```markdown
---
description: Researches topic and provides comprehensive analysis
argument-hint: [research-topic]
---

Research the following topic in depth: $ARGUMENTS

Provide:
1. Executive summary
2. Key findings
3. Current state of the art
4. Future directions
5. Relevant resources and references

Format for technical audience with citations.
```

### Pattern 5: File Analysis Command

**Use Case**: Analyze specific files

```markdown
---
description: Analyzes file for security vulnerabilities
argument-hint: [file-path]
---

Analyze @$1 for security vulnerabilities including:
- Input validation issues
- SQL injection risks
- XSS vulnerabilities
- Authentication bypasses
- Data exposure

For each issue:
- Severity level
- Exploitation scenario
- Remediation code example
```

## Troubleshooting Guide

### Issue: Command Not Found

**Symptoms**: `/command-name` shows "command not found"

**Checks**:
1. File location correct? (.claude/commands/ or ~/.claude/commands/)
2. File has .md extension?
3. Filename matches invocation?
4. Claude Code restarted to reload commands?

**Solution**: Verify file path and restart Claude Code

### Issue: Arguments Not Substituting

**Symptoms**: `$1` appears literally instead of argument value

**Checks**:
1. Placeholder syntax correct? ($1, $2, $ARGUMENTS)
2. Arguments provided when invoking?
3. Typo in placeholder name?

**Solution**: Verify syntax and test with explicit arguments

### Issue: YAML Frontmatter Error

**Symptoms**: Command fails to load or shows parsing error

**Checks**:
1. Opening `---` present?
2. Closing `---` present?
3. Any tabs instead of spaces?
4. Field syntax correct: `key: value`?
5. Special characters properly quoted?

**Solution**: Validate YAML syntax, remove tabs, fix formatting

### Issue: Bash Commands Not Executing

**Symptoms**: Bash commands don't run or show permission error

**Checks**:
1. Commands prefixed with `!`?
2. allowed-tools specified in frontmatter?
3. Command listed in allowed-tools?
4. Pattern allows the specific usage?

**Solution**: Add allowed-tools and verify command restrictions

### Issue: Command Too Complex

**Symptoms**: Hard to maintain, multiple steps, conditional logic

**Solution**: Convert to skill instead
1. Use managing-agent-skills skill
2. Create skill with multiple supporting files
3. Use workflow structure with steps
4. Add validation and error handling

## Checklist Summary

Quick checklist for command creation:

**Planning Phase**:
- [ ] Purpose clearly defined
- [ ] Arguments determined
- [ ] Bash needs assessed
- [ ] Location chosen

**Design Phase**:
- [ ] Name selected (lowercase-with-hyphens)
- [ ] Prompt designed with best practices
- [ ] Frontmatter planned
- [ ] Examples included if helpful

**Implementation Phase**:
- [ ] File created in correct location
- [ ] Frontmatter added if needed
- [ ] Prompt content written
- [ ] File verified with Read tool

**Validation Phase**:
- [ ] YAML syntax valid
- [ ] File naming correct
- [ ] Arguments documented
- [ ] Bash restrictions appropriate
- [ ] Content clear and complete

**Testing Phase**:
- [ ] Basic invocation works
- [ ] Arguments substitute correctly
- [ ] Bash commands execute
- [ ] Edge cases handled
- [ ] Real usage validated

**Deployment**:
- [ ] Tested and working
- [ ] Documentation updated if needed
- [ ] Team notified if project command
- [ ] Ready for use

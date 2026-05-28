# Slash Command Examples

Annotated real-world examples from Claude cookbooks and best practices demonstrating effective command patterns.

## Example 1: Simple Analysis Command

### optimize.md

**Pattern**: Simple command, no frontmatter, no arguments

```markdown
Analyze this code for performance issues
```

**Analysis**:
- ✓ Extremely simple and direct
- ✓ No frontmatter needed for basic use
- ✓ Clear single purpose
- ✗ Could be more specific about what to analyze
- ✗ No output format specification

**Improved Version**:
```markdown
---
description: Analyzes code for performance bottlenecks and optimization opportunities
---

Analyze the codebase for performance issues including:
- Inefficient algorithms (O(n²) or worse)
- Memory leaks
- Unnecessary re-renders or recomputations
- Blocking operations
- Large bundle sizes

For each issue found, provide:
- Location (file:line)
- Performance impact (low/medium/high)
- Specific optimization recommendation
- Code example of improvement
```

**Key Improvements**:
- Added description for discoverability
- Specific areas of analysis listed
- Output format defined
- Actionable recommendations expected

---

## Example 2: PR Review with GitHub Integration

### notebook-review.md

**Pattern**: GitHub CLI integration, bash execution, tool restrictions

```markdown
---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*),Bash(echo:*),Read,Glob,Grep,WebFetch
description: Comprehensive review of Jupyter notebooks and Python scripts
---

Review only the files explicitly listed in the prompt above. Do not search for or review additional files.

Use the "Notebook review skill" to generate a structured review with:
- ✅ Strengths
- ⚠️ Suggestions for improvement
- ❌ Critical issues

Post your review as a comment on the pull request using:
gh pr comment $PR_NUMBER --body "your review here"
```

**Analysis**:
- ✓ Proper tool restrictions for bash commands
- ✓ Clear scope ("only files explicitly listed")
- ✓ References another skill for detailed logic
- ✓ Specifies output format with emojis for clarity
- ✓ Shows exact bash command to use
- ✗ $PR_NUMBER not documented in argument-hint
- ✗ Instructions could specify how to get PR_NUMBER

**Improved Version**:
```markdown
---
description: Comprehensive review of Jupyter notebooks and Python scripts
argument-hint: [pr-number]
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*),Read,Glob,WebFetch
---

<!-- Usage: /notebook-review 123 -->

Review Jupyter notebooks and Python scripts in PR #$1.

First, view the PR details:
!gh pr view $1

Then review only the notebook and Python files changed in this PR.
Do not search for or review additional files.

Generate a structured review with:
- ✅ Strengths: What's well done
- ⚠️ Suggestions: Areas for improvement
- ❌ Critical issues: Must-fix problems

Post your review as a PR comment:
!gh pr comment $1 --body "your review"
```

**Key Improvements**:
- Added argument-hint for $1
- Removed echo from allowed-tools (not needed)
- Added usage comment
- Specified to view PR first for context
- Made PR number usage explicit

---

## Example 3: Model Validation Command

### model-check.md

**Pattern**: Web fetch, validation, GitHub integration

```markdown
---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)
description: Validate Claude model usage against current public models
---

Review the pull request to validate Claude model references.

Steps:
1. Fetch the current list of public models from: docs.claude.com/en/docs/about-claude/models/overview.md
2. Check that all model names mentioned in the PR exist in the public models list
3. Verify no deprecated models are used
4. Ensure no internal/unreleased model names appear
5. Recommend using -latest aliases for better maintainability

Post findings as a PR comment.

Only review the files explicitly listed in the prompt above. Do not search for or review additional files.
```

**Analysis**:
- ✓ Clear step-by-step process
- ✓ Specific validation criteria
- ✓ Helpful recommendation (use -latest)
- ✓ Proper scope limitation
- ✗ No argument for PR number
- ✗ Could structure output format better
- ✗ WebFetch should be in allowed-tools

**Improved Version**:
```markdown
---
description: Validates Claude model references against current public models
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*),Bash(gh pr comment:*),WebFetch
---

<!-- Usage: /model-check 123 -->

Validate Claude model references in PR #$1 against current public models.

**Validation Process**:
1. View PR: !gh pr view $1
2. Fetch current models from: docs.claude.com/en/docs/about-claude/models/overview.md
3. Check each model reference in changed files

**Validation Criteria**:
- ✓ Model exists in public models list
- ✓ Not deprecated or removed
- ✓ Not internal/unreleased model name
- ⚠️ Recommend -latest aliases for maintainability

**Output Format**:
<validation_results>
- Found models: [list]
- Valid: [list]
- Invalid: [list with reasons]
- Recommendations: [list]
</validation_results>

Post findings: !gh pr comment $1 --body "[results]"
```

**Key Improvements**:
- Added argument for PR number
- Added WebFetch to allowed-tools
- Structured validation criteria with symbols
- Defined output format with XML tags
- More explicit process flow

---

## Example 4: Strategic Brief Generation

### strategic-brief.md

**Pattern**: Complex output, multi-agent coordination, flexible input

```markdown
---
description: Generate a comprehensive strategic brief by coordinating analysis from both financial and talent perspectives
---

Create a comprehensive strategic brief for: {{args}}

First, coordinate with subagents:
1. Launch a financial-analyst subagent to provide investment analysis
2. Launch a recruiter subagent to provide talent perspective

Synthesize their analyses into a board-level strategic brief with:

## Executive Summary
[Key recommendations, critical metrics, go/no-go decision]

## Financial Analysis
[From financial-analyst subagent]

## Talent Perspective
[From recruiter subagent]

## Strategic Recommendation
- Action plan
- Success metrics
- Timeline
- Risk mitigation

## Alternative Options
[At least 2 competing approaches with pros/cons]

Format for board-level presentation with clear sections and data-driven insights.
```

**Analysis**:
- ✓ Clear delegation to subagents
- ✓ Well-structured output template
- ✓ Appropriate for executive audience
- ✓ Requires synthesis, not just aggregation
- ✗ Uses {{args}} instead of standard $ARGUMENTS
- ✗ Subagent names hardcoded (may not exist)
- ⚠️ Very complex - might be better as a skill

**Improved Version**:

This command is actually complex enough that it should be a **skill** instead:
- Multiple coordinated subagents
- Complex synthesis required
- Multiple supporting file (subagent instructions) would help
- Should auto-activate for "strategic brief" requests

**As Command (Simplified)**:
```markdown
---
description: Generates strategic brief with financial and talent analysis
argument-hint: [topic-or-initiative]
---

<!-- Usage: /strategic-brief "Cloud migration initiative" -->

Generate a strategic brief for: $ARGUMENTS

Structure the brief for board-level presentation:

## Executive Summary
- Go/no-go recommendation
- Key metrics supporting decision
- Critical risks and mitigation

## Financial Analysis
- Investment requirements
- ROI projections
- Impact on runway and burn rate
- Financial risks

## Talent Analysis
- Current team capabilities
- Hiring requirements
- Retention implications
- Competitive talent landscape

## Strategic Recommendation
- Phased action plan with timeline
- Success metrics and KPIs
- Risk mitigation strategies
- Resource allocation

## Alternatives Considered
Present at least 2 alternative approaches:
- Description and rationale
- Pros and cons
- Cost-benefit comparison
- Why recommended approach is preferred

Use data-driven insights, specific numbers, and clear reasoning throughout.
```

**Key Changes**:
- Simplified to single-agent execution
- Changed {{args}} to standard $ARGUMENTS
- Added argument-hint
- Removed subagent coordination (too complex for command)
- Kept clear output structure
- Note: Full version should be a skill

---

## Example 5: File-Specific Analysis

### Pattern: Argument-based file analysis

```markdown
---
description: Analyzes specific file for security vulnerabilities
argument-hint: [file-path] <analysis-depth>
---

<!-- Usage: /security-scan src/auth.ts deep -->

Analyze @$1 for security vulnerabilities.

Analysis depth: ${2:-standard}
- standard: Common vulnerabilities (OWASP Top 10)
- deep: Comprehensive security audit including subtle issues

**Focus Areas**:
1. Input Validation
   - SQL injection
   - XSS attacks
   - Command injection
   - Path traversal

2. Authentication & Authorization
   - Weak authentication
   - Broken access control
   - Session management

3. Data Protection
   - Sensitive data exposure
   - Insecure cryptography
   - Insufficient logging

4. Configuration
   - Security misconfiguration
   - Default credentials
   - Unnecessary features enabled

**Output Format**:
For each vulnerability found:

### [Vulnerability Type] - [Severity]
**Location**: file:line
**Issue**: [Description]
**Impact**: [What attacker could do]
**Fix**: [Specific remediation]
```python
# Example fix
[code example]
```

If no vulnerabilities found, provide security assessment and best practices recommendations.
```

**Analysis**:
- ✓ File reference with argument: `@$1`
- ✓ Optional second argument with default
- ✓ Comprehensive coverage areas
- ✓ Well-structured output format
- ✓ Code examples expected
- ✓ Usage comment provided
- ✓ Handles edge case (no vulnerabilities)

---

## Example 6: Research Command

### Pattern: Flexible research with variable input

```markdown
---
description: Research topic and provide comprehensive technical analysis
argument-hint: [research-topic-or-question]
model: sonnet
---

<!-- Usage: /research "latest developments in WebAssembly" -->

Conduct comprehensive research on: $ARGUMENTS

**Research Approach**:
1. Define scope and key questions
2. Gather current information
3. Analyze trends and patterns
4. Synthesize findings
5. Provide actionable insights

**Output Structure**:

<executive_summary>
[2-3 sentences capturing essence of findings]
</executive_summary>

<key_findings>
- [Finding 1 with supporting evidence]
- [Finding 2 with supporting evidence]
- [Finding 3 with supporting evidence]
</key_findings>

<current_state>
[Detailed analysis of current state of the art]
</current_state>

<trends_and_future>
[Emerging trends and future directions]
</trends_and_future>

<recommendations>
[Actionable recommendations based on research]
</recommendations>

<resources>
[Relevant links, papers, tools, communities]
</resources>

Format for technical audience. Include citations and specific examples.
Use model: sonnet specified due to research complexity.
```

**Analysis**:
- ✓ $ARGUMENTS for flexible topic input
- ✓ Model specified (sonnet for complexity)
- ✓ Clear research methodology
- ✓ Structured output with XML tags
- ✓ Audience specified
- ✓ Citations requested
- ✓ Usage example provided

---

## Example 7: Multi-File Comparison

### Pattern: Multiple file references, comparative analysis

```markdown
---
description: Compares implementation files for consistency and best practices
argument-hint: [file1] [file2] <file3>
---

<!-- Usage: /compare-implementations src/v1/api.ts src/v2/api.ts -->

Compare implementations in @$1 and @$2 ${3:+and @$3}.

**Comparison Criteria**:

1. **Functionality**
   - Feature parity
   - Missing capabilities
   - Additional features

2. **Architecture**
   - Design patterns
   - Code organization
   - Dependency management

3. **Code Quality**
   - Readability
   - Maintainability
   - Test coverage

4. **Performance**
   - Efficiency
   - Resource usage
   - Optimization opportunities

5. **Best Practices**
   - Industry standards
   - Framework conventions
   - Security considerations

**Output Format**:

| Aspect | File 1 | File 2 ${3:+| File 3} | Assessment |
|--------|--------|--------|------------|
| [Aspect] | [Status] | [Status] ${3:+| [Status]} | [Analysis] |

**Recommendations**:
- [Recommendation 1 with rationale]
- [Recommendation 2 with rationale]

**Migration Path** (if applicable):
[Step-by-step migration guidance if files represent versions]
```

**Analysis**:
- ✓ Multiple file arguments
- ✓ Optional third file with shell syntax
- ✓ Comprehensive comparison criteria
- ✓ Table format for clear comparison
- ✓ Contextual output (migration path if applicable)
- ⚠️ Shell syntax ${3:+...} may not work in all contexts
- ⚠️ Consider simpler approach for optional args

---

## Example 8: Extended Thinking for Complex Reasoning

### Pattern: Complex analysis with thinking keywords

```markdown
---
description: Perform in-depth security analysis of code
argument-hint: [file-path]
model: sonnet
---

<!-- Usage: /security-deep-dive src/auth.ts -->

Perform a thorough security analysis of the implementation in @$1.

Think carefully and systematically about:

1. **Attack Surface Analysis**
   - All entry points where untrusted data enters
   - Data flow through the application
   - Potential attack vectors at each point

2. **Vulnerability Identification**
   - Input validation and sanitization
   - Authentication and authorization
   - Cryptography and data protection
   - Error handling and logging
   - Dependency vulnerabilities

3. **Security Assumptions**
   - Implicit assumptions the code makes
   - Weaknesses in those assumptions
   - Ways assumptions could be violated

4. **Exploitation Scenarios**
   - Concrete ways each vulnerability could be exploited
   - Realistic attack paths
   - Impact of successful exploits

5. **Remediation Strategy**
   - Specific fixes for each vulnerability
   - Code examples showing improvements
   - Priority and effort for each fix

Provide a comprehensive security analysis suitable for a security review meeting.
Format as markdown with clear sections and code examples.
```

**Analysis**:
- ✓ Model specified (sonnet for complex reasoning)
- ✓ Uses thinking keywords naturally ("Think carefully", structured analysis areas)
- ✓ Claude recognizes thinking patterns and enables extended thinking
- ✓ Complex multi-step reasoning task benefits from deeper analysis
- ✓ Specific argument for targeted analysis
- ✓ Clear output format for actionable results

**Benefits of Extended Thinking**:
- Systematically analyzes all aspects without skipping steps
- Deeper reasoning about attack vectors and implications
- More thorough identification of subtle vulnerabilities
- Better remediation recommendations

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Command Too Complex

**Bad Example**:
```markdown
---
description: Complete application development workflow
---

Create a new feature with the following steps:
1. Analyze requirements
2. Design architecture
3. Write code
4. Create tests
5. Update documentation
6. Create PR
7. Review code
8. Deploy to staging
9. Run integration tests
10. Deploy to production

[100+ lines of detailed instructions]
```

**Why It's Bad**:
- Too many steps (should be a skill)
- Multiple distinct phases (should be separate commands)
- Requires state management across steps
- Too complex for single invocation

**Fix**: Convert to skill with separate workflows

---

### Anti-Pattern 2: Overly Permissive Security

**Bad Example**:
```markdown
---
allowed-tools: Bash(*:*)
---

Run any commands needed to complete the task: $ARGUMENTS
```

**Why It's Bad**:
- Unrestricted bash access
- No validation of commands
- Could execute dangerous operations
- Command injection vulnerability

**Fix**: Explicitly list allowed commands with patterns

---

### Anti-Pattern 3: Vague Instructions

**Bad Example**:
```markdown
Make the code better
```

**Why It's Bad**:
- No specific guidance
- Unclear what "better" means
- No output format
- No success criteria

**Fix**: Be explicit about what to improve and how

---

### Anti-Pattern 4: Missing Documentation

**Bad Example**:
```markdown
Process $1 with $2 using $3
```

**Why It's Bad**:
- No description for /help
- Arguments not documented
- Purpose unclear
- No usage guidance

**Fix**: Add frontmatter with description and argument-hint

---

## Best Practice Examples Summary

### Minimal Effective Command
```markdown
Analyze code for TypeScript errors and provide fix recommendations.
```

### Standard Command with Frontmatter
```markdown
---
description: Reviews code for style and best practices
argument-hint: [file-path]
---

Review @$1 for code style and best practices adherence.
Provide specific improvement recommendations.
```

### Command with Bash Integration
```markdown
---
description: Posts code review comment to PR
argument-hint: [pr-number]
allowed-tools: Bash(gh pr comment:*),Bash(gh pr view:*)
---

!gh pr view $1
Review the PR and post findings:
!gh pr comment $1 --body "[your analysis]"
```

### Complex Command with Structure
```markdown
---
description: Generates comprehensive API documentation
argument-hint: [api-directory]
model: sonnet
---

Generate API documentation for files in @$1.

<api_overview>
[High-level API description]
</api_overview>

<endpoints>
[Detailed endpoint documentation]
</endpoints>

<examples>
[Usage examples with code]
</examples>

<authentication>
[Auth requirements and examples]
</authentication>
```

---

## Learning from Examples

Key takeaways:
1. **Start simple**: Basic commands don't need frontmatter
2. **Add structure**: Use frontmatter as complexity grows
3. **Be explicit**: Clear instructions yield better results
4. **Document arguments**: Always use argument-hint
5. **Restrict tools**: Only allow necessary bash commands
6. **Format output**: Specify structure for complex outputs
7. **Provide examples**: Usage comments help users
8. **Enable thinking**: Use thinking keywords for complex reasoning tasks
9. **Consider security**: Validate and restrict appropriately
10. **Know limits**: Complex workflows should be skills
11. **Test thoroughly**: Validate with real use cases

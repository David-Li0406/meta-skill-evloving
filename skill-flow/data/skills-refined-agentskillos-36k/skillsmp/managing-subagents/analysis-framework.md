# Analysis Framework: Evaluating Existing Subagents

Systematic framework for assessing subagent effectiveness and identifying improvements.

## Analysis Process

### Phase 1: Configuration Parsing

Extract all configuration elements from agent file.

#### Required Fields
```yaml
name: agent-name-here
description: Description text here
```

**Validation checklist:**
- [ ] Both name and description present
- [ ] YAML delimiters correct (`---` at start and end)
- [ ] No tabs in YAML (spaces only)
- [ ] Name follows format: lowercase-with-hyphens
- [ ] Name under 64 characters
- [ ] Description under 1024 characters

#### Optional Fields
```yaml
tools: tool1, tool2, tool3  # If present, restricts tool access
model: sonnet|opus|haiku|inherit  # If present, overrides default model
```

**Validation checklist:**
- [ ] If tools specified, verify all tools exist and are spelled correctly
- [ ] If tools specified, verify agent can accomplish purpose with only those tools
- [ ] If model specified, verify appropriate for task complexity
- [ ] Check if tools should be omitted to inherit MCP tools

#### System Prompt
All content after YAML frontmatter constitutes system prompt.

**Parse for:**
- Purpose statement (what agent does)
- Activation contexts (when to use)
- Input specifications (what agent receives)
- Workflow instructions (step-by-step process)
- Output specifications (format to return)
- Examples (concrete input/output pairs)
- Constraints (validation, error handling)

### Phase 2: Description Quality Assessment

Evaluate description against discoverability and specificity criteria.

#### Trigger Keyword Analysis
Count specific trigger keywords in description:
- **Technical terms**: API, JSON, database, configuration, authentication, etc.
- **Action verbs**: analyzing, evaluating, searching, validating, processing, etc.
- **Data types**: files, patterns, endpoints, responses, schemas, etc.
- **Task contexts**: outdated information, improvement, evaluation, etc.

**Scoring:**
- 0-2 keywords: Critical issue - undiscoverable
- 3-4 keywords: Major issue - low discoverability
- 5-7 keywords: Good - reasonable discoverability
- 8+ keywords: Excellent - highly discoverable

#### Specificity Evaluation

**Vague patterns (problematic):**
- "helps with various tasks"
- "handles different types of work"
- "assists with code operations"
- "supports multiple use cases"
- Generic domain names without specific contexts

**Specific patterns (good):**
- "Analyzes JSON configuration files for schema validation"
- "Searches codebase for API endpoint implementations"
- "Evaluates authentication patterns for security vulnerabilities"
- "Processes test results and identifies failing test patterns"

**Assessment criteria:**
- [ ] Description specifies exact task types (not "various")
- [ ] Description includes data formats or file types
- [ ] Description lists specific use cases
- [ ] Description clear enough to choose among 100+ agents
- [ ] Description matches what agent actually does

### Phase 3: Name Appropriateness

Evaluate whether name accurately represents agent purpose.

#### Format Validation
- [ ] Lowercase only
- [ ] Hyphens for word separation (no underscores, camelCase)
- [ ] Under 64 characters
- [ ] No special characters except hyphens

#### Semantic Validation
- [ ] Name describes what agent does (action-oriented)
- [ ] Name specific enough to differentiate from other agents
- [ ] Name not overly generic ("helper", "utility", "manager")
- [ ] Name matches description's primary purpose

**Red flags:**
- Generic terms: code-helper, file-processor, general-agent
- Vague actions: handle-stuff, do-work, assist-with-code
- Overly broad: code-analyzer (analyzing what aspect?)
- Mismatched: Name says "search" but agent does "validation"

### Phase 4: System Prompt Evaluation

Assess whether system prompt enables effective agent execution.

#### Completeness Check

**Must include:**
- [ ] Clear purpose statement (what agent does)
- [ ] Activation contexts (when agent should be used)
- [ ] Workflow instructions (step-by-step execution)
- [ ] Output format specification (exact structure to return)

**Should include:**
- [ ] Input specifications (what agent receives)
- [ ] Examples (concrete input/output pairs)
- [ ] Constraints (validation rules, error handling)
- [ ] Edge case handling

**Optional but valuable:**
- [ ] Tool usage patterns specific to task
- [ ] Common pitfalls to avoid
- [ ] Performance considerations

#### Redundancy Analysis

**Flag for removal:**
- Basic programming concepts Claude already knows
- Standard library documentation
- General best practices (unless domain-specific twist)
- Verbose explanations of obvious steps
- Information duplicated from main Claude Code system prompt

**Example redundant content:**
```
"First, you should read the file using the Read tool. The Read tool
allows you to read files from the filesystem. After reading, you should
analyze the content. Analyzing means examining the data carefully..."
```

**Improved concise version:**
```
"Read target file. Extract authentication patterns. Report: pattern type,
security level, vulnerabilities."
```

#### Specificity Assessment

**Too generic (problematic):**
```
"Analyze the code and look for issues. Report any problems you find."
```

**Appropriately specific (good):**
```
"Search for SQL query construction patterns. Flag: string concatenation,
unparameterized queries, dynamic table names. Report: file path, line number,
vulnerability type, recommended fix."
```

**Assessment criteria:**
- [ ] Specific tool sequences described
- [ ] Exact output format specified
- [ ] Clear success criteria
- [ ] Concrete examples provided
- [ ] Domain-specific guidance included

#### Autonomy Enablement

**Check if prompt enables autonomous execution:**
- [ ] Agent can complete task without asking questions
- [ ] All necessary context provided in prompt
- [ ] No assumptions about main conversation context
- [ ] Clear what to do when uncertainties arise
- [ ] Explicit final output format

**Red flags:**
- References to "the user mentioned earlier"
- Instructions to "ask if unclear"
- Assumptions about context agent doesn't have
- Unclear completion criteria

### Phase 5: Tool Configuration Analysis

Evaluate whether tool restrictions appropriate.

#### Tool Restriction Patterns

**No tools field (inherits all):**
- Appropriate for: Most agents
- Benefit: Full flexibility, inherits MCP tools
- Drawback: None unless security concern

**Restricted tool set:**
- Appropriate for: Security-sensitive operations, focused tasks
- Benefit: Prevents unintended operations, improves focus
- Drawback: May block necessary operations if misconfigured

#### Validation Questions

For agents WITH tool restrictions:
- [ ] Can agent accomplish purpose with only specified tools?
- [ ] Is restriction necessary (security, focus, or just cargo-culting)?
- [ ] Are any essential tools missing?
- [ ] Would agent benefit from additional tools?
- [ ] Do restrictions accidentally block MCP tools?

For agents WITHOUT tool restrictions:
- [ ] Would tool restrictions improve focus?
- [ ] Any security concerns requiring restrictions?
- [ ] Is unrestricted access appropriate for task?

#### Common Misconfiguration Patterns

**Problem: Too restrictive**
```yaml
tools: Read, Grep
```
Agent needs to search files but can't use Glob to find them first.

**Problem: Unnecessary restrictions**
```yaml
tools: Read, Write, Edit, Glob, Grep, Bash
```
If listing almost all tools, better to omit field entirely.

**Problem: Blocking MCP tools**
Agent with tools field won't inherit MCP tools unless explicitly listed. If agent might need MCP tools, omit tools field.

### Phase 6: Model Selection Evaluation

Assess whether model choice appropriate for task complexity.

#### Model Selection Guidelines

**Haiku appropriate for:**
- Simple search operations
- Straightforward analysis with clear criteria
- Pattern matching tasks
- Quick lookups
- Cost/latency optimization priority

**Sonnet appropriate for:**
- Moderate complexity analysis
- Code understanding tasks
- Multi-step workflows
- Most general-purpose agents

**Opus appropriate for:**
- Complex reasoning requirements
- Sophisticated code generation
- Nuanced judgment calls
- Maximum capability essential

**Inherit appropriate for:**
- Matching main conversation model
- Default choice for most agents

#### Validation Questions

- [ ] Is model selection explicit or defaulting to inherit?
- [ ] Does task complexity match model capability?
- [ ] Could cheaper model handle task without quality loss?
- [ ] Is expensive model justified by task requirements?

### Phase 7: Effectiveness Pattern Recognition

Identify patterns indicating strong or weak agent design.

#### Strong Agent Indicators

**Description patterns:**
- 5+ specific trigger keywords
- Concrete data types mentioned (JSON, API, configuration)
- Specific action verbs (analyzes, validates, searches)
- Clear activation contexts
- Precise enough to be discoverable

**System prompt patterns:**
- Concrete workflow steps
- Specific output format
- Examples with actual data structures
- Domain-specific guidance
- Concise without redundancy

**Configuration patterns:**
- Appropriate tool restrictions (or intentionally unrestricted)
- Model selection justified by complexity
- Single focused responsibility
- Clear completion criteria

#### Weak Agent Indicators

**Description patterns:**
- Generic language ("helps with", "various tasks")
- Under 3 trigger keywords
- Overly broad scope
- Vague activation contexts
- Undiscoverable among many agents

**System prompt patterns:**
- Verbose explanations of basic concepts
- No concrete examples
- Unclear output format
- Generic instructions not domain-specific
- References to unavailable context

**Configuration patterns:**
- Tool restrictions blocking necessary operations
- Overly powerful model for simple task
- Multiple unrelated responsibilities
- Unclear purpose or completion criteria

### Phase 8: Issue Categorization

Classify all identified issues by severity.

#### Critical Issues (Break Functionality)
- Invalid YAML syntax
- Missing required fields (name or description)
- Tool restrictions block essential operations
- Agent cannot complete stated purpose
- Description triggers don't match actual capability

#### Major Issues (Significantly Impair Effectiveness)
- Description too vague for discovery
- System prompt missing output specification
- No examples provided for complex tasks
- Tool configuration unnecessarily restrictive
- Redundant content inflating token usage
- Multiple unrelated responsibilities

#### Minor Issues (Room for Improvement)
- Could be more specific in description
- Additional examples would help
- Model selection suboptimal but functional
- Some redundant content but not severe
- Organization could be clearer

## Assessment Output Format

Structure analysis results as:

```
## Agent Analysis: [agent-name]

### Configuration Summary
- Name: [name]
- Description length: [X] characters
- Trigger keywords: [count]
- Tools: [restricted/unrestricted]
- Model: [haiku/sonnet/opus/inherit/unspecified]
- System prompt length: [X] lines

### Effectiveness Score
- Description quality: [Critical/Major/Minor/Good/Excellent]
- Name appropriateness: [Critical/Major/Minor/Good/Excellent]
- System prompt: [Critical/Major/Minor/Good/Excellent]
- Tool configuration: [Critical/Major/Minor/Good/Excellent]
- Model selection: [Critical/Major/Minor/Good/Excellent]
- Overall: [Critical/Major/Minor/Good/Excellent]

### Issues Identified

#### Critical Issues
[List with specific details]

#### Major Issues
[List with specific details]

#### Minor Issues
[List with specific details]

### Recommendations
[Prioritized list of improvements with rationale]
```

## Time-Sensitive Content Detection

When checking for outdated information:

### Categories of Time-Sensitive Content

**Claude Code features:**
- Tool names and parameters
- Available agent types
- Configuration options
- File structure conventions

**Tool capabilities:**
- Which tools exist
- Tool parameters and syntax
- Tool restrictions or permissions
- New tools added since agent creation

**Best practices:**
- Recommended patterns
- Anti-patterns
- Performance guidelines
- Security considerations

**API structures:**
- Expected data formats
- Endpoint patterns
- Response structures
- Error handling

### Verification Process

**For Claude Code features:**
1. Use WebFetch to check https://code.claude.com/docs/
2. Compare agent's assumptions against current documentation
3. Flag discrepancies with current state

**For tool capabilities:**
1. Check system prompt's tool descriptions against actual tools
2. Verify tool names spelled correctly
3. Confirm parameters match current tool signatures

**For best practices:**
1. Compare against current guidance from documentation
2. Check if deprecated patterns mentioned
3. Verify security recommendations still current

**For API structures:**
1. Use Grep to search codebase for current patterns
2. Compare agent's assumptions against found patterns
3. Flag if agent expects outdated structure

### Outdated Content Red Flags

- Absolute statements with dates: "As of 2024, X is true"
- References to specific versions: "In Claude Code 1.5"
- Tool names that don't exist
- Deprecated patterns presented as current
- Security recommendations contradicting current best practices

### Recommended Documentation Pattern

Instead of dates, use "Old patterns" sections:

```
## Current Approach
[Current recommended pattern]

## Old Patterns (Deprecated)
[Deprecated pattern - included for reference when encountering legacy code]
```

This ages better than date-based conditionals.

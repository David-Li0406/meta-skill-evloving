# Agent Skills Best Practices

Comprehensive guide to creating effective, efficient agent skills.

## Core Principles

### 1. Conciseness: Context Window as Public Good

The context window is a shared resource. Every token counts.

**Key Rule**: Only include information Claude doesn't already have.

**Challenge Each Detail**: Before adding information, ask:
- Is this already in Claude's training?
- Is this necessary for task completion?
- Can this be inferred from context?

**Examples of Unnecessary Content**:
- Basic programming language syntax
- Standard library documentation
- Common software engineering principles
- General best practices Claude already knows

**Examples of Necessary Content**:
- Company-specific brand guidelines
- Custom tool/API specifications
- Domain-specific workflows unique to your organization
- Proprietary data formats or standards

### 2. Appropriate Freedom Levels

Match specificity to task fragility.

**High Freedom** (General Guidance):
- Flexible tasks with multiple valid approaches
- Creative work where variation is acceptable
- Exploratory analysis

**Medium Freedom** (Preferred Patterns):
- Standard workflows with some flexibility
- Tasks with recommended but not mandatory approaches
- Where consistency is helpful but not critical

**Low Freedom** (Exact Sequences):
- Error-prone operations requiring specific order
- Compliance-sensitive tasks
- Operations where small deviations cause failures
- Security-critical workflows

### 3. Cross-Model Compatibility

Test skills with multiple Claude models (Haiku, Sonnet, Opus).

**Model-Specific Guidance**:
- **Haiku**: Needs more detail and explicit guidance - more literal interpretation
- **Sonnet**: Balanced - standard level of detail works well
- **Opus**: Avoid over-explaining - can infer from context and handle nuanced instructions

Ensure skills work effectively across all models your team uses.

### 4. Cross-Platform Path Conventions

**CRITICAL**: ALWAYS use forward slashes `/` in file paths, even on Windows.

**Good**:
```
path/to/file.md
scripts/calculate_ratios.py
~/Documents/skills/
```

**Bad**:
```
path\to\file.md
C:\Users\username\Documents
```

**Why**: Ensures skills work across all platforms (Windows, Mac, Linux).

## Naming Conventions

### Skill Names

**Format**: Gerund form (verb + -ing)
**Character Set**: Lowercase letters, numbers, hyphens only
**Length**: Maximum 64 characters
**Style**: Descriptive and specific

**Good Examples**:
- `processing-pdfs`
- `analyzing-financial-statements`
- `applying-brand-guidelines`
- `validating-api-responses`
- `generating-technical-documentation`

**Bad Examples**:
- `helper` (too vague)
- `utils` (not descriptive)
- `ProcessPDFs` (not lowercase)
- `process_pdfs` (underscores not allowed)
- `pdf` (not gerund form)

### File Names

**Supporting Files**: Use descriptive names that indicate purpose
- `reference.md` (reference documentation)
- `examples.md` (usage examples)
- `validation-rules.md` (validation criteria)
- `template.md` (templates)

**Scripts**: Use verb-noun format
- `calculate_ratios.py`
- `validate_brand.py`
- `extract_data.py`

## Description Writing

The description field is critical for skill discovery.

### Requirements
- Maximum 1024 characters
- Must be non-empty
- Third-person voice
- Include both functionality AND usage triggers

### Structure
```
[What it does]. [When to use it]. [Key triggers or contexts].
```

### Examples

**Poor Description**:
```
Helps with documents
```
Issues: Too vague, no triggers, no context

**Good Description**:
```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
Benefits: Specific functionality, clear triggers, concrete contexts

**Excellent Description**:
```
Calculates key financial ratios and metrics from financial statement data for investment analysis. Use when analyzing financial statements, comparing company performance, evaluating investments, or when user provides income statements, balance sheets, or cash flow statements.
```
Benefits: Detailed functionality, multiple triggers, specific data formats mentioned

### Trigger Keywords

Include keywords that help Claude identify when to use the skill:
- Task-related: "analyzing", "processing", "validating"
- Domain-related: "financial statements", "PDFs", "API responses"
- Data format-related: "CSV files", "JSON data", "Excel spreadsheets"
- Action-related: "compare", "extract", "generate", "validate"

### Trigger Types: Informational + Action

Skill descriptions must include BOTH informational triggers and action triggers matched to capabilities.

**Informational Triggers** (learning-oriented - domain-agnostic pattern):
- Apply to the skill's domain: "how [domain] works", "explaining [domain]", "understanding [domain]", "what [domain] is"
- "Use when user asks how...", "Use when explaining..."
- Activates skill for questions about concepts, structure, understanding

**Action Triggers** (task-oriented - capability-specific):
- Match ONLY what the skill actually does
- Examples:
  - **Formatting skill**: "formatting", "applying styles", "structuring"
  - **Analysis skill**: "analyzing", "evaluating", "reviewing", "assessing"
  - **Creation skill**: "creating", "generating", "building"
  - **Validation skill**: "validating", "checking", "verifying"
- Don't include "creating" if the skill only analyzes
- Don't include "analyzing" if the skill only formats

**Why Both Matter:**
- Informational triggers: Answer learning questions using skill's domain knowledge
- Action triggers: Execute the skill's actual workflows
- Skills contain best practices, patterns, examples beyond official docs

**Example - Formatting Skill (Correct):**
```yaml
description: Applies Python PEP 8 formatting standards to code. Use when user asks about Python formatting standards, explaining PEP 8 rules, understanding code style, formatting Python files, applying style guidelines, or structuring Python code.
```
*Informational: "about Python formatting", "explaining PEP 8", "understanding code style"*
*Action (matches capabilities): "formatting", "applying", "structuring"*
*Does NOT include: "creating", "analyzing" (not what this skill does)*

**Example - Analysis-Only Skill (Correct):**
```yaml
description: Analyzes financial statements for key metrics and ratios. Use when user asks how financial analysis works, explaining financial ratios, understanding statement analysis, analyzing company performance, evaluating financial health, or reviewing financial statements.
```
*Informational: "how financial analysis works", "explaining financial ratios"*
*Action (matches capabilities): "analyzing", "evaluating", "reviewing"*
*Does NOT include: "creating", "generating" (not what this skill does)*

**Example - Multi-Capability Skill (Correct):**
```yaml
description: Creates, analyzes, and improves Claude Code hooks. Use when user asks how hooks work, explaining hook concepts, understanding hook types, creating new hooks, analyzing existing hooks, improving hook configuration, or debugging hook activation.
```
*Informational: "how hooks work", "explaining hook concepts", "understanding hook types"*
*Action (matches all capabilities): "creating", "analyzing", "improving", "debugging"*

**Anti-Pattern - Mismatched Actions:**
```yaml
description: Formats Python code to PEP 8 standards. Use when creating Python files, analyzing code quality, or formatting code.
```
*Problem: Includes "creating" and "analyzing" but skill only formats*
*Fix: Remove mismatched verbs, keep only "formatting", "applying styles"*

**Pattern Template:**
```
Use when user asks [how/what/explain domain], [action verb 1 matching capability], [action verb 2 matching capability], or when user mentions [specific terms]
```

## File Organization

### SKILL.md Token Limit

Keep SKILL.md under 5,000 tokens for optimal performance (approximately 500-700 lines).

**Token vs Line Count**:
- Official guidance is token-based, not line-based
- Estimate: ~7-10 tokens per line on average
- Use token count as primary metric

**If approaching 5,000 tokens**: Split content using progressive disclosure.

### Progressive Disclosure Patterns

#### Pattern 1: High-Level Guide with References
```markdown
# Main Workflow

1. Validate input data
2. Process according to type (see processing-guide.md)
3. Generate output (see output-formats.md)
4. Verify results (see validation-rules.md)
```

**When to Use**: Complex workflows with distinct phases

#### Pattern 2: Domain-Specific Organization
```
skill-name/
├── SKILL.md (core workflow)
├── api-endpoints.md (API-specific details)
├── data-formats.md (format specifications)
└── error-handling.md (error scenarios)
```

**When to Use**: Multiple distinct knowledge domains

#### Pattern 3: Conditional Details
```markdown
For basic usage, follow steps 1-3.
For advanced features, see advanced-usage.md.
```

**When to Use**: Layered complexity where most users need basics

### File Reference Guidelines

**Keep One Level Deep**: Reference files directly from SKILL.md
```markdown
# Good
For validation rules, see validation-rules.md

# Bad (two levels deep)
For validation rules, see validation-rules.md
(validation-rules.md references detailed-checks.md)
```

**Reason**: Prevents incomplete file reads and context confusion

## Content Guidelines

### Avoid Time-Sensitive Information

**Problem**: Date-based conditionals become outdated
```markdown
# Bad
If date is after 2024-01-01, use new API endpoint
```

**Solution**: Use "Old patterns" sections
```markdown
# Old Patterns
Previous versions used endpoint /v1/data
Current implementation uses /v2/data

# Current Approach
Use /v2/data endpoint for all requests
```

### Consistent Terminology

Choose one term and use it throughout.

**Bad**:
```markdown
Use the API endpoint... call the URL... access the path...
```

**Good**:
```markdown
Use the API endpoint... call the endpoint... access the endpoint...
```

**Common Inconsistencies to Avoid**:
- API endpoint / URL / path
- Function / method / procedure
- Variable / parameter / argument
- File / document / artifact

### Structured Workflows

Break complex operations into clear, numbered steps.

**Format**:
```markdown
## Workflow: Data Processing

### Step 1: Validate Input
- Check data format
- Verify required fields
- Validate data types

### Step 2: Transform Data
- Apply normalization
- Handle missing values
- Convert formats

### Step 3: Generate Output
- Format results
- Add metadata
- Validate output
```

### Validation Loops

Implement run-validate-fix-iterate patterns for quality.

**Pattern**:
```markdown
1. Execute operation
2. Validate results against criteria (see validation-rules.md)
3. If validation fails, identify issues
4. Fix issues
5. Repeat until validation passes
```

**Use Reference Documents as Validators**: Claude reads reference docs to compare content against checklists.

## Executable Code Guidelines

### Error Handling

Solve problems in scripts rather than delegating to Claude.

**Bad**:
```python
# If this fails, Claude will figure it out
data = process_file(filename)
```

**Good**:
```python
try:
    data = process_file(filename)
except FileNotFoundError:
    logger.error(f"File not found: {filename}")
    return None
except InvalidFormat as e:
    logger.error(f"Invalid file format: {e}")
    return None
```

### Configuration Values

Make configuration self-documenting.

**Bad**:
```python
THRESHOLD = 0.85
```

**Good**:
```python
# Confidence threshold for classification (85%)
# Justified by validation testing showing 85% minimizes false positives
# while maintaining 95% recall
CONFIDENCE_THRESHOLD = 0.85
```

### Utility Scripts Benefits

Pre-made scripts are:
- More reliable than generated code
- Save context tokens (no code generation needed)
- Tested and validated
- Consistent across uses

**When to Provide Scripts**:
- Complex calculations
- Standard transformations
- Frequently used operations
- Error-prone implementations

### Dependencies

Document all required packages and tools.

**Format**:
```markdown
## Dependencies

**Python Packages**:
- pandas >= 1.5.0
- numpy >= 1.23.0
- requests >= 2.28.0

**System Requirements**:
- Python 3.8+
- 100MB free disk space

**Installation**:
```bash
pip install pandas numpy requests
```
```

## Evaluation and Iteration

### Build Evaluations First

Create test scenarios before extensive documentation.

**Process**:
1. Identify 3-5 representative use cases
2. Create test scenarios for each
3. Build minimal skill version
4. Test with scenarios
5. Iterate based on results
6. Expand documentation

**Benefit**: Solves actual problems rather than anticipated ones.

### Iterative Development with Claude

**Technique**: Use two Claude instances
- **Claude A**: Creates and refines skill
- **Claude B**: Tests skill on real tasks (no context from A)

**Process**:
1. Claude A creates initial skill
2. Claude B attempts to use it
3. Observe Claude B's behavior and difficulties
4. Claude A refines based on observations
5. Repeat until Claude B uses skill effectively

**Key Insight**: Watch how Claude navigates your skill to identify:
- Unintuitive organization
- Unclear instructions
- Missing connections
- Redundant content

## Common Anti-Patterns

### 1. Windows-Style Paths
**Problem**: Not cross-platform compatible
```markdown
# Bad
C:\Users\username\file.txt

# Good
/users/username/file.txt
or use forward slashes: C:/Users/username/file.txt
```

### 2. Too Many Equivalent Options
**Problem**: Decision paralysis without defaults
```markdown
# Bad
Choose one of: Method A, Method B, Method C, Method D

# Good
Use Method A for most cases.
For high-performance requirements, use Method B.
```

### 3. Deep File Nesting
**Problem**: Incomplete file reads, context confusion
```markdown
# Bad (three levels)
SKILL.md → references guide.md → references details.md

# Good (two levels max)
SKILL.md → references guide.md
SKILL.md → references details.md
```

### 4. Vague Names
**Problem**: Not discoverable, unclear purpose
```markdown
# Bad
- helper
- utils
- tool
- processor

# Good
- processing-financial-statements
- validating-api-responses
- generating-reports
```

### 5. Assuming Tool Availability
**Problem**: Breaks when tool not installed
```markdown
# Bad
Use jq to process JSON

# Good
Use jq to process JSON if available.
If jq is not installed, use Python json module.
```

### 6. Including Known Information
**Problem**: Wastes context tokens
```markdown
# Bad (Claude already knows this)
Python is a programming language. Functions are defined with def.
Use print() to output to console.

# Good (organization-specific)
Use internal logging framework via log_event() function.
All API calls must include auth token from get_token().
```

## Technical Requirements

### YAML Frontmatter

**Required Fields**:
```yaml
---
name: skill-name-here
description: Description of the skill with usage triggers
---
```

**Format Rules**:
- Delimiters: `---` at start and end
- No tabs (use spaces for indentation)
- name: lowercase-with-hyphens, max 64 chars
- description: max 1024 chars, non-empty

**Optional Field**:
```yaml
---
name: skill-name
description: Skill description
allowed-tools: Read, Grep, Glob, Bash
---
```

Use `allowed-tools` to restrict Claude to specific tools when skill is active.

### MCP Tools Reference

When using MCP (Model Context Protocol) tools, use fully qualified names:

```markdown
# Correct
Use ServerName:tool_name to access the tool

# Incorrect (will cause "tool not found" errors)
Use tool_name
```

## Skills vs Slash Commands

### Choose Skills When:
- Complex workflows with multiple steps
- Automatic discovery preferred
- Multiple supporting files needed
- Validation loops required
- Team needs standardized guidance
- Task has clear trigger contexts

### Choose Slash Commands When:
- Simple, single-file prompts
- User wants explicit invocation control
- Repeated prompt without complexity
- No supporting resources needed
- Quick reminders or templates

**Both Can Coexist**: Use appropriate tool for each use case.

## Summary Checklist

When creating or evaluating skills, verify:
- [ ] Name: Gerund form, lowercase-with-hyphens, under 64 chars
- [ ] Description: Specific, includes triggers, under 1024 chars
- [ ] SKILL.md: Under 500 lines
- [ ] Progressive disclosure: Used for complex content
- [ ] Conciseness: No redundant information
- [ ] Terminology: Consistent throughout
- [ ] Workflows: Clearly structured with steps
- [ ] Code: Error handling and documentation
- [ ] Dependencies: Documented completely
- [ ] File references: One level deep max
- [ ] No time-sensitive content
- [ ] Cross-platform compatibility
- [ ] Tested across multiple scenarios

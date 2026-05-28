# Degrees of Freedom

Comprehensive guide on determining and implementing appropriate freedom levels for agent skills.

## Table of Contents

- Understanding Degrees of Freedom
- The Three Freedom Levels
- Decision Framework
- Implementation Patterns
- Examples by Domain
- Common Mistakes

## Understanding Degrees of Freedom

The "degree of freedom" in a skill refers to how much latitude Claude has when following the skill's instructions. It's about balancing:

- **Flexibility**: Claude's ability to adapt to context and edge cases
- **Reliability**: Consistency and predictability of outputs
- **Fragility**: How sensitive the task is to variation

Think of it as choosing between:
- A detailed recipe (low freedom)
- Cooking guidelines (medium freedom)
- "Make something delicious with these ingredients" (high freedom)

## The Three Freedom Levels

### High Freedom (Text-Based Instructions)

**When to use**:
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach
- Creativity and judgment are valuable

**Characteristics**:
- Text-based procedural instructions
- Workflow guidance
- Decision points described in natural language
- Claude chooses implementation details

**Analogy**: Open field with no hazards. Many paths lead to success.

**Example tasks**:
- Code review
- Content writing
- Design feedback
- Exploratory data analysis

**Implementation**:
```markdown
## Code Review Process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
5. Provide constructive feedback with specific examples
```

### Medium Freedom (Pseudocode/Scripts with Parameters)

**When to use**:
- Preferred pattern exists but isn't the only option
- Some variation is acceptable or necessary
- Configuration affects behavior
- Balance between flexibility and consistency needed

**Characteristics**:
- Template or pseudocode provided
- Parameters customize behavior
- Structure is recommended but adaptable
- Claude can adjust details

**Analogy**: Marked trail with some route options. Clear path but room to navigate.

**Example tasks**:
- Report generation
- Data transformation pipelines
- API integration
- Document formatting

**Implementation**:
````markdown
## Generate Report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    summary = analyze_data(data)

    # Generate output in specified format
    if format == "markdown":
        output = create_markdown_report(summary)
    elif format == "html":
        output = create_html_report(summary)

    # Optionally include visualizations
    if include_charts:
        charts = generate_charts(summary)
        output = embed_charts(output, charts)

    return output
```

Adjust formatting and content based on the specific use case.
````

### Low Freedom (Specific Scripts, Few Parameters)

**When to use**:
- Operations are fragile and error-prone
- Consistency is critical
- Specific sequence must be followed
- Small deviations cause failures

**Characteristics**:
- Exact scripts or commands provided
- Few or no parameters
- Strict sequence enforcement
- Minimal room for interpretation

**Analogy**: Narrow bridge with cliffs on both sides. Only one safe way forward.

**Example tasks**:
- Database migrations
- Deployment procedures
- System configuration
- Data integrity operations

**Implementation**:
````markdown
## Database Migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

**IMPORTANT**:
- Do not modify the command
- Do not add additional flags
- Run verification before migration
- Backup is mandatory

If migration fails, see [references/migration-recovery.md](references/migration-recovery.md).
````

## Decision Framework

Use this framework to determine appropriate freedom level:

### Step 1: Assess Task Fragility

**Ask**:
- What happens if the approach varies slightly?
- Can mistakes be easily recovered?
- Is there one correct answer or multiple valid solutions?

**High fragility** → Lower freedom
**Low fragility** → Higher freedom

### Step 2: Evaluate Context Dependency

**Ask**:
- Does the optimal approach depend on the specific situation?
- Are there edge cases requiring judgment?
- Is domain expertise needed to choose the right path?

**High context dependency** → Higher freedom
**Low context dependency** → Lower freedom

### Step 3: Consider Consistency Requirements

**Ask**:
- Must outputs be identical for identical inputs?
- Are users expecting standardized results?
- Is reproducibility critical?

**High consistency needs** → Lower freedom
**Low consistency needs** → Higher freedom

### Step 4: Analyze Error Impact

**Ask**:
- What's the cost of errors?
- Can errors be detected and fixed easily?
- Are mistakes catastrophic or minor?

**High error impact** → Lower freedom
**Low error impact** → Higher freedom

### Decision Matrix

| Fragility | Context Dependency | Consistency Needs | Error Impact | Recommended Freedom |
|-----------|-------------------|-------------------|--------------|---------------------|
| High | Low | High | High | **Low** |
| Medium | Medium | Medium | Medium | **Medium** |
| Low | High | Low | Low | **High** |
| High | High | Medium | Medium | **Medium** (with guardrails) |
| Low | Low | High | Low | **Low to Medium** |

### Step 5: Validate with Examples

Test your decision with concrete examples:

1. Think of 3-5 real usage scenarios
2. For each, consider what could go wrong with the chosen freedom level
3. If problems arise frequently, adjust freedom level
4. If the level feels constraining for valid use cases, increase freedom

## Implementation Patterns

### Pattern 1: High Freedom with Heuristics

**Structure**:
```markdown
## Task Process

1. [Step with decision point]
2. [Step requiring judgment]
3. [Step with multiple valid approaches]

**Guiding principles**:
- Principle 1
- Principle 2

**Common patterns**:
- Pattern A: [when to use]
- Pattern B: [when to use]
```

**Example**:
```markdown
## Code Review

1. Read the entire change to understand context
2. Identify issues by priority (critical bugs, then improvements)
3. Provide feedback with specific examples

**Guiding principles**:
- Focus on correctness first, style second
- Be constructive and specific
- Suggest alternatives, don't just criticize

**Common patterns**:
- Security issues: Always flag immediately
- Performance: Flag if significant impact
- Style: Suggest if violates project standards
```

### Pattern 2: Medium Freedom with Templates

**Structure**:
````markdown
## Task Template

Use this as a starting point:

```
[Template with parameters]
```

**Customization points**:
- [What can be adjusted]
- [What should remain fixed]

**When to deviate**: [Conditions for going off-template]
````

**Example**:
````markdown
## API Integration

Use this pattern:

```python
def integrate_api(endpoint, auth_method="token", timeout=30):
    # Setup authentication
    auth = setup_auth(auth_method)

    # Make request with retry
    response = make_request_with_retry(
        endpoint,
        auth=auth,
        timeout=timeout,
        max_retries=3
    )

    # Validate and return
    validate_response(response)
    return response.json()
```

**Customization points**:
- Auth method: Choose based on API requirements
- Timeout: Adjust for slow endpoints
- Retry count: Increase for unreliable connections

**When to deviate**: Use async pattern for batch operations
````

### Pattern 3: Low Freedom with Strict Scripts

**Structure**:
````markdown
## Exact Procedure

Run this command exactly:

```bash
[Exact command]
```

**CRITICAL**:
- [What must not be changed]
- [What must be verified first]

**If errors occur**: [Recovery procedure or reference]
````

**Example**:
````markdown
## Production Deployment

Run exactly this sequence:

```bash
# Verify current state
./scripts/verify_state.sh

# Create backup
./scripts/backup_db.sh --production

# Deploy with rollback capability
./scripts/deploy.sh --environment=production --enable-rollback
```

**CRITICAL**:
- Do NOT skip verification
- Do NOT modify commands
- Do NOT deploy without backup

**If deployment fails**: See [references/rollback.md](references/rollback.md)
````

## Examples by Domain

### Data Analysis (High Freedom)

**Why**: Multiple valid approaches, context-dependent decisions, creativity valued.

```markdown
## Data Analysis Workflow

1. Load and inspect the data to understand structure and quality
2. Identify relevant variables for the analysis question
3. Clean and transform data as needed
4. Choose appropriate analysis methods based on data characteristics
5. Interpret results in context of the original question

**Guiding principles**:
- Let the data guide your approach
- Check assumptions before statistical tests
- Consider multiple explanations for patterns
```

### Report Generation (Medium Freedom)

**Why**: Preferred format exists, some customization needed, balance of consistency and flexibility.

````markdown
## Generate Report

Follow this structure:

```markdown
# [Title]

## Executive Summary
[1-2 paragraphs: key findings and recommendations]

## Key Metrics
- Metric 1: [value and trend]
- Metric 2: [value and trend]

## Detailed Analysis
[Sections based on data domains]

## Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]
```

**Customization**:
- Adjust sections based on available data
- Add visualizations where helpful
- Include comparisons to previous periods if relevant

**Standard elements** (don't modify):
- Executive summary first
- Metrics before details
- Recommendations last
````

### Database Migration (Low Freedom)

**Why**: Fragile operations, specific sequence critical, high error cost.

````markdown
## Run Migration

Execute exactly this procedure:

```bash
# Step 1: Verify database connection
python scripts/verify_connection.py

# Step 2: Create backup
python scripts/backup.py --full --timestamp

# Step 3: Run migration
python scripts/migrate.py --version=2.1.0 --verify

# Step 4: Verify migration
python scripts/verify_migration.py --check-integrity
```

**CRITICAL**:
- Run steps in exact order
- Do not skip verification
- Do not modify commands
- Wait for each step to complete before next

**If any step fails**: STOP. See [references/migration-recovery.md](references/migration-recovery.md)
````

### Content Creation (High Freedom)

**Why**: Creative task, context-dependent, multiple valid approaches.

```markdown
## Create Content

1. Understand the audience and purpose
2. Research topic if needed for accuracy
3. Structure content logically
4. Write in appropriate tone and style
5. Include examples and specifics
6. Review for clarity and impact

**Guiding principles**:
- Write for the intended audience
- Use concrete examples
- Be clear and concise
- Maintain consistent tone
```

### Configuration Setup (Low Freedom)

**Why**: Specific settings required, errors cause system failures.

````markdown
## Configure System

Apply exactly this configuration:

```yaml
server:
  host: 0.0.0.0
  port: 8080
  workers: 4

database:
  host: db.example.com
  port: 5432
  pool_size: 20
  timeout: 30

cache:
  enabled: true
  ttl: 3600
```

**DO NOT CHANGE**:
- Port numbers
- Pool size
- Worker count

**Can customize**:
- Cache TTL (if justified)

**After applying**: Run `./scripts/verify_config.sh`
````

## Common Mistakes

### Mistake 1: Too Low Freedom for Creative Tasks

**Problem**: Providing exact templates for tasks requiring judgment and creativity.

**Example** (Wrong):
````markdown
## Code Review

Use exactly this format:

```
File: [filename]
Line: [number]
Issue: [exactly this phrasing]
Fix: [exactly this suggestion]
```
````

**Solution**: Provide guidelines instead of strict templates.

### Mistake 2: Too High Freedom for Fragile Operations

**Problem**: Vague instructions for critical operations.

**Example** (Wrong):
```markdown
## Deploy to Production

Deploy the application to production. Be careful!
```

**Solution**: Provide exact scripts and procedures.

### Mistake 3: Inconsistent Freedom Levels

**Problem**: Mixing freedom levels within the same skill without clear boundaries.

**Example** (Wrong):
```markdown
## Workflow

1. Run exactly: `python setup.py`
2. Configure however you think is best
3. Run exactly: `python verify.py`
```

**Solution**: Be consistent within workflows, or clearly indicate when freedom level changes.

### Mistake 4: Not Explaining Why

**Problem**: Setting freedom level without explaining the reasoning.

**Example** (Wrong):
```markdown
## Run Migration

Run: `python migrate.py --verify --backup`

[No explanation of why this exact command]
```

**Solution**: Briefly explain the constraints.

**Example** (Right):
```markdown
## Run Migration

Run exactly: `python migrate.py --verify --backup`

**Why exact command**: Migrations are fragile. The `--verify` flag checks prerequisites, and `--backup` ensures rollback capability. Omitting either flag risks data loss.
```

### Mistake 5: Forgetting Edge Cases

**Problem**: Choosing freedom level based only on happy path.

**Example** (Wrong):
```markdown
## Process Data

Use pandas to load and process the CSV file.
```

**Solution**: Consider error cases and add appropriate guardrails.

**Example** (Right):
```markdown
## Process Data

1. Load CSV with pandas
2. Check for required columns: [list]
3. Handle missing values based on column type
4. Validate data ranges

**If validation fails**: See [references/data-errors.md](references/data-errors.md)
```

## When to Ask the User

If uncertain about the appropriate freedom level, ask the user:

```markdown
I'm designing a skill for [task]. Based on your needs, should this skill:

**Option A (High freedom)**: Provide workflow guidance and let Claude choose implementation details?
- Pro: Flexible, adapts to context
- Con: Less consistent outputs

**Option B (Medium freedom)**: Provide templates and recommended patterns with room for customization?
- Pro: Balance of consistency and flexibility
- Con: May not fit all edge cases perfectly

**Option C (Low freedom)**: Provide exact scripts and procedures with minimal variation?
- Pro: Highly consistent and reliable
- Con: Less adaptable to unexpected situations

What's most important for your use case: flexibility, consistency, or reliability?
```

## Summary

**High Freedom**: Use for creative, context-dependent tasks where judgment is valuable.

**Medium Freedom**: Use for tasks with preferred patterns but acceptable variation.

**Low Freedom**: Use for fragile, critical operations where consistency is essential.

**Decision factors**:
- Task fragility
- Context dependency
- Consistency requirements
- Error impact

**Validate**: Test your decision with concrete examples before finalizing.

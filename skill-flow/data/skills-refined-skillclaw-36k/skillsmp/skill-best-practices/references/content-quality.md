# Content Quality Checklist

## Writing Style Standards

### Use Imperative Form

Write all instructions using verb-first imperative form:

✅ **Correct:**
```markdown
Create the skill directory structure.
Validate the YAML frontmatter.
Extract the description field.
```

❌ **Incorrect:**
```markdown
You should create the directory structure.
You need to validate the frontmatter.
You can extract the description.
```

**Why:** Imperative form is objective, direct, and clearer for AI consumption.

### Be Objective and Instructional

Focus on what to do, not who should do it:

✅ **Correct:**
```markdown
To create a hook, define the event type in hooks.json.
Configure the MCP server with authentication credentials.
Validate settings before applying them.
```

❌ **Incorrect:**
```markdown
I recommend creating a hook by defining the event type.
You'll want to configure authentication.
It's important to validate settings.
```

**Why:** Objective instructions are actionable and unambiguous.

### Avoid Opinionated Language

State requirements clearly without subjective qualifiers:

✅ **Correct:**
```markdown
Include the `name` field in the frontmatter.
Use third person in descriptions.
Keep SKILL.md under 2,000 words.
```

❌ **Incorrect:**
```markdown
You should include the name field.
It's best to use third person.
Try to keep SKILL.md under 2,000 words.
```

**Why:** Requirements should be clear, not suggestions.

## Content Organization

### Section Structure

Organize SKILL.md with these standard sections:

```markdown
# [Skill Name]

## Overview
[Purpose and what the skill does - 2-3 paragraphs]

## Core Concepts
[Key terminology and concepts - 3-5 sections]

## Essential Procedures
[Step-by-step workflows - 3-5 procedures]

## Quick Reference
[Tables, lists, summaries - optional]

## Additional Resources
[Links to references/, examples/, scripts/]
```

### Content Distribution

**SKILL.md (1,500-2,000 words):**
- Overview: 10-15% (150-300 words)
- Core Concepts: 25-30% (400-600 words)
- Procedures: 35-40% (600-800 words)
- Quick Reference: 10-15% (150-300 words)
- Resource Links: 5-10% (100-200 words)

**References/ (2,000-5,000+ words each):**
- Detailed patterns
- Advanced techniques
- Comprehensive examples
- Troubleshooting

## Clarity Guidelines

### Be Specific

Avoid vague statements:

✅ **Correct:**
```markdown
Create the agent file in `agents/` directory.
Use kebab-case for file names.
Include `description` field in frontmatter.
```

❌ **Incorrect:**
```markdown
Create the agent file in the appropriate location.
Use proper naming conventions.
Include necessary metadata.
```

### Provide Complete Information

Give full details, not partial instructions:

✅ **Correct:**
```markdown
Create the hook configuration in `hooks/hooks.json`:

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash /path/to/script.sh"
    }]
  }]
}
```
```

❌ **Incorrect:**
```markdown
Create a hooks.json file with your configuration.
// ...details left to reader...
```

### Use Examples

Include concrete examples for abstract concepts:

✅ **Correct:**
```markdown
## Trigger Phrases

Effective trigger descriptions list specific phrases:

```yaml
description: This skill should be used when the user asks to "create a hook",
"add a PreToolUse hook", or mentions hook events.
```
```

❌ **Incorrect:**
```markdown
## Trigger Phrases

The description should include specific phrases that users might say.
```

## Completeness Standards

### Cover Essential Information

Each section should answer:

**Overview:**
- What does this skill do?
- When should it be used?
- What value does it provide?

**Core Concepts:**
- What are the key terms?
- How do they relate?
- What are the important distinctions?

**Procedures:**
- What are the steps?
- In what order?
- What are the prerequisites?

**Resources:**
- What additional information exists?
- Where is it located?
- When should it be consulted?

### Provide Context

Explain why, not just what:

✅ **Correct:**
```markdown
Use imperative form because it's objective, direct, and clearer for AI
consumption. Avoid second person ("you should") which can be ambiguous.
```

❌ **Incorrect:**
```markdown
Use imperative form.
Avoid second person.
```

## Accessibility and Usability

### Use Clear Headings

Make headings descriptive:

✅ **Correct:**
```markdown
## Creating a Hook with Validation

## Configuring MCP Server Authentication
```

❌ **Incorrect:**
```markdown
## Hooks

## Configuration
```

### Use Formatting Effectively

Leverage markdown features:

- **Bold** for emphasis on key terms
- *Italic* for secondary emphasis
- `Code` for technical terms
- ```Code blocks``` for examples
- Tables for structured data
- Lists for procedures

### Break Up Complex Content

Split long sections:

✅ **Correct:**
```markdown
## YAML Frontmatter

### Required Fields

### Optional Fields

### Validation
```

❌ **Incorrect:**
```markdown
## YAML Frontmatter
[2000 words of undifferentiated content]
```

## Quality Checklist

Use this checklist to validate content quality:

### Writing Style
- [ ] Uses imperative form throughout
- [ ] No second person ("you should", "you need to")
- [ ] Objective and instructional
- [ ] No opinionated language
- [ ] Clear and direct

### Organization
- [ ] Clear section structure
- [ ] Logical flow of information
- [ ] Descriptive headings
- [ ] Appropriate use of markdown features

### Clarity
- [ ] Specific instructions
- [ ] Complete information
- [ ] Concrete examples
- [ ] Context provided

### Completeness
- [ ] Overview answers what/when/why
- [ ] Concepts defined and explained
- [ ] Procedures are complete
- [ ] Resources referenced

### Accessibility
- [ ] Descriptive headings
- [ ] Effective formatting
- [ ] Content broken into manageable sections
- [ ] Visual hierarchy with headers

### Progressive Disclosure
- [ ] SKILL.md is lean (1,500-2,000 words)
- [ ] Detailed content in references/
- [ ] Examples in examples/
- [ ] No duplication across files

## Common Quality Issues

### Issue 1: Mixed Writing Styles

**Problem:** Inconsistent use of imperative and second person

**Example:**
```markdown
Create the file structure.
You should validate the syntax.
Configure the settings.
```

**Fix:** Use imperative throughout
```markdown
Create the file structure.
Validate the syntax.
Configure the settings.
```

### Issue 2: Vague Instructions

**Problem:** Instructions lack specificity

**Example:**
```markdown
Set up the appropriate configuration.
```

**Fix:** Be specific
```markdown
Create the configuration in `hooks/hooks.json` with the event type and
hook command.
```

### Issue 3: Missing Context

**Problem:** Instructions without explanation

**Example:**
```markdown
Use third person in descriptions.
```

**Fix:** Add context
```markdown
Use third person ("This skill should be used when...") to ensure proper
skill triggering and maintain consistency across the plugin ecosystem.
```

### Issue 4: Incomplete Procedures

**Problem:** Steps missing or out of order

**Example:**
```markdown
To create a skill, write SKILL.md and add references.
```

**Fix:** Complete procedure
```markdown
To create a skill:
1. Create skill directory: `mkdir -p skills/skill-name`
2. Create SKILL.md with frontmatter
3. Write skill body (1,500-2,000 words)
4. Add references/ for detailed content
5. Add examples/ for working code
```

## Quick Reference

### Imperative Form Examples

✅ **Use:**
- Create the directory
- Configure the server
- Validate the input
- Extract the field
- Parse the file
- Generate the report

❌ **Avoid:**
- You should create...
- You need to configure...
- Don't forget to validate...
- You can extract...
- Try to parse...

### Objective Language

✅ **Use:**
- Required field
- Must include
- Validate before use
- Configure with...

❌ **Avoid:**
- You should include...
- It's important to...
- I recommend...
- You might want to...

### Complete Information

✅ **Use:**
```markdown
Create the file at `path/to/file` with the following structure:
[show structure]
```

❌ **Avoid:**
```markdown
Create the file in the appropriate location.
// ...incomplete...
```

Follow these quality standards to create clear, effective, and maintainable skill content.

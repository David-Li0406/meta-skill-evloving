---
name: create-skills
description: This skill should be used when the user asks to "create a skill", "build a skill", "write a skill", "improve skill structure", "understand skill creation", or mentions SKILL.md files, skill development, progressive disclosure, or bundled resources (scripts, references, assets).
---

<objective>
Create highly effective Claude Code skills using proven patterns from 2026. Skills are modular, filesystem-based capabilities that extend Claude's expertise through progressive disclosure. This skill teaches you how to create skills that Claude can discover and use successfully.

Every skill created should follow pure XML structure, enforce progressive disclosure, and apply expert prompting techniques from create-prompt skill.
</objective>

<quick_start>
<workflow>

1. **Identify the reusable pattern**: What procedural knowledge would help future tasks?
2. **Create directory structure**: `mkdir -p ~/.claude/skills/{skill-name}/{references,scripts}`
3. **Write SKILL.md**:
   - YAML frontmatter (name, description in third person)
   - Pure XML body structure (no markdown headings)
   - Required tags: `<objective>`, `<quick_start>`, `<success_criteria>`
4. **Add bundled resources**: Scripts, references, or assets as needed
5. **Test with real usage**: Iterate based on observations
6. **Create slash command wrapper**: Optional wrapper for discoverability
   </workflow>

<minimal_example>

````yaml
---
name: process-pdfs
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

<objective>
Extract text and tables from PDF files, fill forms, and merge documents using Python libraries.
</objective>

<quick_start>
Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
````

</quick_start>

<success_criteria>

- Text extracted successfully from PDF
- Output is clean and properly formatted
- No encoding errors
  </success_criteria>

````
</minimal_example>
</quick_start>

<core_concepts>
<skills_anatomy>
Every skill consists of:

**SKILL.md (required)**:
- YAML frontmatter: name, description
- Pure XML body: no markdown headings (#, ##, ###)
- Required tags: objective, quick_start, success_criteria
- Conditional tags based on complexity

**Bundled Resources (optional)**:
- **scripts/**: Executable code for deterministic tasks
- **references/**: Documentation loaded as needed (progressive disclosure)
- **assets/**: Files used in output (templates, boilerplate)
</skills_anatomy>

<progressive_disclosure>
Skills use a three-level loading system:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed by Claude (unlimited)

**Critical principle**: Keep SKILL.md lean (<500 lines). Move detailed content to references/.
</progressive_disclosure>

<when_to_create_skills>
**Create skills for**:
- Reusable patterns across multiple tasks
- Domain knowledge that doesn't change frequently
- Complex workflows with structured guidance
- Reference materials (schemas, APIs, libraries)
- Validation scripts and quality checks

**Use prompts for**: One-off tasks that won't be reused

**Use slash commands for**: Explicit user-triggered workflows with fresh context
</when_to_create_skills>
</core_concepts>

<skill_creation_process>
<step_1>
**Understanding Use Cases with Concrete Examples**

To create an effective skill, clearly understand how it will be used:

- What functionality should the skill support?
- Can you give examples of how this skill would be used?
- What would a user say that should trigger this skill?

Conclude when you have a clear sense of functionality the skill should support.
</step_1>

<step_2>
**Planning Reusable Skill Contents**

Analyze each example by:

1. Consider how to execute from scratch
2. Identify helpful scripts, references, and assets

**Example patterns**:

- **Scripts**: Rotating PDFs requires re-writing code → `scripts/rotate_pdf.py`
- **Assets**: Frontend apps need boilerplate → `assets/hello-world/` template
- **References**: BigQuery needs table schemas → `references/schema.md`

Create a list of reusable resources to include.
</step_2>

<step_3>
**Creating Skill Structure**

```bash
mkdir -p ~/.claude/skills/{skill-name}/{references,scripts}
touch ~/.claude/skills/{skill-name}/SKILL.md
````

**Directory naming**:

- Follow verb-noun convention: `create-*`, `manage-*`, `setup-*`, `generate-*`
- Lowercase letters, numbers, hyphens only
- Must match name in YAML frontmatter exactly
  </step_3>

<step_4>
**Writing SKILL.md with Expert Prompting**

**Apply create-prompt principles**:

Use the create-prompt skill to ensure your SKILL.md follows expert prompting techniques:

- Clear, specific instructions
- XML tags for structure
- Success criteria defined
- Examples when format matters
- Context management for long-running tasks

**YAML frontmatter requirements**:

```yaml
---
name: skill-name-here
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", or mentions "trigger words". Include what it does AND when to use it.
---
```

**Critical rules**:

- **Third person**: "This skill should be used when..." (never "Use this skill...")
- **Specific triggers**: Include exact phrases users would say
- **Maximum 1024 characters**
- **No XML tags in description**

**Good description examples**:

```yaml
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", "validate tool use", or mentions hook events (PreToolUse, PostToolUse, Stop).
```

**Bad description examples**:

```yaml
description: Use this skill when working with hooks.  # Wrong person, vague
description: Provides hook guidance.  # No trigger phrases
```

**Pure XML body structure**:

Remove ALL markdown headings (#, ##, ###) from body. Use semantic XML tags.

**Required tags** (every skill must have):

- `<objective>` - What the skill does and why it matters
- `<quick_start>` - Immediate, actionable guidance
- `<success_criteria>` or `<when_successful>` - How to know it worked

**Conditional tags** (add based on complexity):

- `<context>` - Background information
- `<workflow>` or `<process>` - Step-by-step procedures
- `<advanced_features>` - Deep-dive topics
- `<validation>` - How to verify outputs
- `<examples>` - Multi-shot learning
- `<anti_patterns>` - Common mistakes
- `<security_checklist>` - Security patterns
- `<testing>` - Testing workflows
- `<common_patterns>` - Code examples
- `<reference_guides>` - Links to reference files

**Tag selection intelligence**:

- **Simple skills**: Required tags only
- **Medium skills**: Required + workflow/examples
- **Complex skills**: Required + conditional tags as needed

**Writing style**:

- Use imperative/infinitive form (verb-first instructions)
- Not second person ("you should")
- Objective, instructional language
- Example: "To accomplish X, do Y" not "You should do X"
  </step_4>

<step_5>
**Adding Bundled Resources**

<scripts_directory>
**When to use scripts**:

- Same code rewritten repeatedly
- Deterministic reliability needed
- Token efficiency important

**Benefits**:

- More reliable than generated code
- Save tokens (no code in context)
- Ensure consistency across uses

**Organization**:

```
skill-name/
├── SKILL.md
├── scripts/
│   ├── main_utility.py
│   ├── helper_script.py
│   └── validator.py
└── references/
```

**Script documentation pattern**:

````xml
<utility_scripts>
**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
````

Output format:

```json
{
  "field_name": { "type": "text", "x": 100, "y": 200 }
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

</utility_scripts>

````

**Script best practices**:
- Handle errors gracefully (don't punt to Claude)
- Document configuration values (avoid "voodoo constants")
- List required packages in SKILL.md
- Make clear if Claude should execute or read as reference
</scripts_directory>

<references_directory>
**When to use references**:
- Detailed patterns and techniques
- Comprehensive API documentation
- Migration guides
- Edge cases and troubleshooting
- Extensive examples

**Benefits**:
- Keeps SKILL.md lean
- Loaded only when Claude determines it's needed
- Can be large (2,000-5,000+ words each)

**Organization**:
- Keep references one level deep from SKILL.md
- Add table of contents for files >100 lines
- Use pure XML structure in reference files

**Reference pattern in SKILL.md**:
```xml
<reference_guides>
For detailed patterns and techniques:

- **`references/patterns.md`** - Common patterns and best practices
- **`references/api-reference.md`** - Complete API documentation
- **`references/advanced.md`** - Advanced use cases and edge cases
</reference_guides>
````

</references_directory>

<assets_directory>
**When to use assets**:

- Templates, images, icons
- Boilerplate code
- Sample documents

**Benefits**:

- Separates output resources from documentation
- Enables Claude to use files without loading into context

**Examples**:

- `assets/logo.png` for brand assets
- `assets/slides.pptx` for PowerPoint templates
- `assets/frontend-template/` for HTML/React boilerplate
  </assets_directory>
  </step_5>

<step_6>
**Validation and Testing**

**Structure validation**:

- [ ] YAML frontmatter valid (name matches directory)
- [ ] Description in third person with specific triggers
- [ ] Pure XML body (no markdown headings)
- [ ] Required tags present (objective, quick_start, success_criteria)
- [ ] All XML tags properly closed
- [ ] SKILL.md under 500 lines
- [ ] Referenced files exist

**Content validation**:

- [ ] Imperative/infinitive form (not second person)
- [ ] Clear, specific instructions
- [ ] Examples included when format matters
- [ ] Success criteria defined
- [ ] Progressive disclosure applied

**Testing**:

- Test with real usage scenarios
- Verify skill triggers on expected user queries
- Check that references load when needed
- Iterate based on observations
  </step_6>

<step_7>
**Creating Slash Command Wrapper (Optional)**

Create a lightweight wrapper for discoverability:

Location: `~/.claude/commands/{skill-name}.md`

Template:

```yaml
---
description: {Brief description}
argument-hint: [{argument description}]
allowed-tools: Skill({skill-name})
---

<objective>
Delegate {task} to the {skill-name} skill for: #$ARGUMENTS

This routes to specialized skill containing patterns, best practices, and workflows.
</objective>

<process>
1. Use Skill tool to invoke {skill-name} skill
2. Pass user's request: #$ARGUMENTS
3. Let skill handle workflow
</process>

<success_criteria>
- Skill successfully invoked
- Arguments passed correctly to skill
</success_criteria>
```

The slash command's only job is routing—all expertise lives in the skill.
</step_7>

<step_8>
**Iteration and Improvement**

After testing, iterate based on real usage:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify improvements needed
4. Implement changes and test again

**Common improvements**:

- Strengthen trigger phrases in description
- Move long sections to references/
- Add missing examples or scripts
- Clarify ambiguous instructions
- Add edge case handling
  </step_8>
  </skill_creation_process>

<naming_conventions>
<verb_noun_pattern>
Use verb-noun convention for skill names:

**create-\*** - Building/authoring tools

- Examples: `create-agent-skills`, `create-hooks`, `create-landing-pages`

**manage-\*** - Managing external services

- Examples: `manage-facebook-ads`, `manage-zoom`, `manage-stripe`

**setup-\*** - Configuration/integration

- Examples: `setup-stripe-payments`, `setup-meta-tracking`

**generate-\*** - Generation tasks

- Examples: `generate-ai-images`, `generate-reports`

**Avoid**:

- Vague: `helper`, `utils`, `tools`
- Generic: `documents`, `data`, `files`
- Reserved: `anthropic-helper`, `claude-tools`
  </verb_noun_pattern>

<validation_rules>

- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- No reserved words: "anthropic", "claude"
- Must match directory name exactly
  </validation_rules>
  </naming_conventions>

<anti_patterns>
<pitfall name="markdown_headings">
❌ **Bad**: Using markdown headings in body

```markdown
# PDF Processing

## Quick start
```

✅ **Good**: Pure XML structure

```xml
<objective>PDF processing...</objective>
<quick_start>...</quick_start>
```

</pitfall>

<pitfall name="weak_triggers">
❌ **Bad**: Vague description
```yaml
description: Provides guidance for working with hooks.
```

✅ **Good**: Specific trigger phrases

```yaml
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", or mentions hook events.
```

</pitfall>

<pitfall name="bloated_skill">
❌ **Bad**: Everything in SKILL.md (8,000 words)
```
skill-name/
└── SKILL.md  (huge file)
```

✅ **Good**: Progressive disclosure

```
skill-name/
├── SKILL.md  (1,500 words)
└── references/
    ├── patterns.md (2,500 words)
    └── advanced.md (3,700 words)
```

</pitfall>

<pitfall name="second_person">
❌ **Bad**: Second person writing
```
You should start by reading the configuration file.
You need to validate the input.
```

✅ **Good**: Imperative form

```
Start by reading the configuration file.
Validate the input before processing.
```

</pitfall>

<pitfall name="missing_resources">
❌ **Bad**: No mention of references
```xml
<objective>Core content</objective>
[No reference to bundled resources]
```

✅ **Good**: Clear resource references

```xml
<reference_guides>
- **`references/patterns.md`** - Detailed patterns
- **`references/advanced.md`** - Advanced techniques
</reference_guides>
```

</pitfall>
</anti_patterns>

<best_practices_summary>
**DO**:

- Use third-person in description ("This skill should be used when...")
- Include specific trigger phrases ("create X", "configure Y")
- Keep SKILL.md lean (under 500 lines)
- Use progressive disclosure (move details to references/)
- Write in imperative/infinitive form
- Apply create-prompt prompting techniques
- Reference supporting files clearly
- Provide working examples
- Create utility scripts for common operations
- Test with real usage

**DON'T**:

- Use second person anywhere
- Have vague trigger conditions
- Put everything in SKILL.md (>500 lines without references/)
- Use markdown headings in body
- Leave resources unreferenced
- Include broken or incomplete examples
- Skip validation
- Forget to apply prompting best practices
  </best_practices_summary>

<reference_guides>
For deeper topics, see reference files:

- **`references/script-patterns.md`** - Executable code patterns, error handling, package dependencies
- **`references/progressive-disclosure-patterns.md`** - Advanced progressive disclosure strategies
- **`references/xml-tag-guide.md`** - Complete guide to XML tags and structure
- **`references/prompting-integration.md`** - How to integrate create-prompt techniques into skills
- **`references/real-world-examples.md`** - Complete examples of well-structured skills
  </reference_guides>

<success_criteria>
A well-structured skill has:

- Valid YAML frontmatter with third-person description and specific triggers
- Pure XML structure with no markdown headings in body
- Required tags: objective, quick_start, success_criteria
- Conditional tags appropriate to complexity level
- Progressive disclosure (SKILL.md < 500 lines, details in references/)
- Clear, concise instructions in imperative form
- Expert prompting techniques from create-prompt applied
- Bundled resources (scripts, references, assets) as needed
- Clear references to all supporting files
- Real-world testing and iteration
- Optional slash command wrapper for discoverability
  </success_criteria>

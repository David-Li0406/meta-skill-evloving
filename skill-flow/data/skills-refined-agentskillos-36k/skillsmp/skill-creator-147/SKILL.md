---
name: skill-creator
description: Guide for creating effective skills. Use this when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Skill Creator

Create modular skill packages that extend Claude's capabilities through specialized knowledge, workflows, and tool integrations.

## What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key
The context window is a shared resource. Only add information Claude lacks. Challenge each piece: "Does Claude really need this?" Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom
Match specificity to task fragility:
- **High freedom** (text instructions): Multiple valid approaches exist
- **Medium freedom** (pseudocode/scripts): Preferred patterns exist but variations acceptable
- **Low freedom** (specific scripts): Operations are error-prone, exact approach required

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, allowed-tools)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/ - Executable code for repeated operations
    ├── references/ - Documentation to load as needed
    └── assets/ - Files for output (templates, icons, fonts)
```

### SKILL.md Components

**Frontmatter (YAML)**:
```yaml
---
name: skill-name
description: What the skill does and when to use it. Include clear triggers.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---
```

**Body (Markdown)**:
- Instructions and guidance
- Workflows and procedures
- Examples and patterns
- Best practices and reminders

### Bundled Resources

**scripts/** - Reusable executable code:
- Use when same code runs repeatedly with different inputs
- Examples: data processing, file conversion, validation

**references/** - Documentation loaded as needed:
- API schemas, configuration specs, policy documents
- Load only when Claude requests them
- Keep out of main SKILL.md to reduce context

**assets/** - Files used in outputs:
- Templates, icons, fonts
- Not loaded into context
- Referenced by scripts/workflows

### What to Exclude
- README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md
- CHANGELOG.md or auxiliary documentation
- User-facing docs (those belong in project docs, not skills)

## Progressive Disclosure Design

Three-level loading system:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines, <5k words)
3. **Bundled resources** - As needed by Claude (unlimited size)

### Guidelines
- Keep SKILL.md under 500 lines
- For multiple variations, keep core workflow in SKILL.md, move variant details to references
- For files >100 lines, include table of contents
- Structure references one level deep from SKILL.md

## Skill Creation Process

### Step 1: Understand with Concrete Examples

**Gather examples:**
- Real user examples (preferred)
- Validated generated examples

**Ask clarifying questions:**
- What is the exact functionality needed?
- What are the primary use cases?
- What are edge cases or variations?
- What tools/integrations are required?

**Conclude when:**
- Skill scope is clear
- Use cases are well-defined
- Examples cover common scenarios

### Step 2: Plan Reusable Contents

**Analyze examples for:**
- Repeated code → scripts/
- Documentation lookups → references/
- Output templates → assets/

**Identify:**
- What needs to be bundled vs what Claude knows
- What should be in SKILL.md vs separate files
- What degree of freedom is appropriate

### Step 3: Initialize the Skill

Create directory structure:
```bash
mkdir -p .claude/skills/skill-name/{scripts,references,assets}
```

Create SKILL.md template:
```markdown
---
name: skill-name
description: Brief description and when to use it
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Skill Title

Brief overview of what this skill does.

## Key Workflows

### Workflow 1
Steps...

### Workflow 2
Steps...

## Examples

Example usage...

## Important Reminders

- ALWAYS do X
- NEVER do Y
```

### Step 4: Edit the Skill

**Learn from existing skills:**
- Review similar skills in `.claude/skills/`
- Follow established patterns and conventions
- Match tone and structure

**Implement bundled resources:**
- Write scripts with clear inputs/outputs
- Document reference file structures
- Organize assets logically

**Update SKILL.md:**
- Clear, concise frontmatter
- Structured body with workflows
- Concrete examples
- Important reminders section

**Frontmatter Best Practices:**
```yaml
# ✅ Good: Specific, clear triggers
description: Build RESTful APIs with Eloquent API Resources, pagination, versioning, and rate limiting. Use this when creating API endpoints or transforming data for JSON responses.

# ❌ Bad: Vague, no clear triggers
description: Helps with API development in Laravel applications.
```

**Body Structure:**
1. Overview/Introduction
2. Key workflows or procedures
3. Common patterns with examples
4. Tool usage guidelines
5. Output requirements
6. Important reminders

### Step 5: Test the Skill

**Test on actual tasks:**
- Use the skill for real work
- Verify workflows are clear
- Check examples are helpful
- Ensure bundled resources work

**Iterate based on usage:**
- Notice inefficiencies
- Update SKILL.md or resources
- Simplify where possible
- Add missing patterns

### Step 6: Refine and Maintain

**Keep skills fresh:**
- Update as tools/APIs change
- Add new patterns as discovered
- Remove outdated information
- Refactor for clarity

**Avoid scope creep:**
- Each skill should have focused purpose
- Split large skills into multiple skills
- Don't duplicate Laravel Boost guidelines

## Skill Design Patterns

### Pattern 1: Discovery First
For framework/library skills, start with discovery:
```markdown
## Discovery

**Check existing setup:**
1. Look for existing patterns in codebase
2. Review configuration files
3. Determine conventions used

**Follow existing conventions!**
```

### Pattern 2: Workflow Templates
Provide clear step-by-step workflows:
```markdown
## Workflow: Create API Resource

1. **Create resource**
   ```bash
   php artisan make:resource PostResource --no-interaction
   ```

2. **Define transformation**
   ```php
   public function toArray(Request $request): array
   {
       return [
           'id' => $this->id,
           'title' => $this->title,
       ];
   }
   ```

3. **Use in controller**
   ```php
   return new PostResource($post);
   ```
```

### Pattern 3: Code Snippets
Include practical, copy-ready examples:
```markdown
<code-snippet name="Example Feature Test" lang="php">
test('creates post successfully', function () {
    $response = $this->postJson('/api/posts', [
        'title' => 'Test Post',
    ]);

    $response->assertCreated();
});
</code-snippet>
```

### Pattern 4: Important Reminders
End with critical do's and don'ts:
```markdown
## Important Reminders

- **ALWAYS** use Form Requests for validation
- **ALWAYS** eager load relationships to prevent N+1
- **NEVER** return models directly (use Resources)
- **CHECK** existing API patterns before creating new ones
```

## Common Skill Types

### Framework Skills
- Laravel feature development
- API building
- Testing patterns
- Database operations

### Tool Integration Skills
- File format handling (XLSX, PDF, CSV)
- External API integration
- Data analysis and visualization

### Domain-Specific Skills
- Business logic workflows
- Company-specific procedures
- Industry-standard practices

### Debugging Skills
- Systematic troubleshooting
- Log analysis
- Performance optimization

## Skill Quality Checklist

**Frontmatter:**
- [ ] Clear, concise name
- [ ] Description explains what AND when to use
- [ ] Allowed-tools list is accurate

**Body:**
- [ ] Under 500 lines
- [ ] Clear structure with headings
- [ ] Concrete examples included
- [ ] Workflows are step-by-step
- [ ] Important reminders section

**Bundled Resources:**
- [ ] Scripts are reusable and documented
- [ ] References are organized logically
- [ ] Assets are properly stored
- [ ] No unnecessary files included

**Testing:**
- [ ] Tested on real tasks
- [ ] Examples work as written
- [ ] Workflows are complete
- [ ] Edge cases considered

## Integration with Laravel Boost

Skills should complement, not duplicate, Laravel Boost guidelines:

**Laravel Boost provides:**
- Core Laravel conventions
- Package-specific rules (Livewire, Flux, Pest)
- General best practices
- Code style guidelines

**Skills provide:**
- Specific workflows for tasks
- Domain expertise
- Tool integrations
- Procedural knowledge

**Example Division:**
- Boost: "Use Form Requests for validation"
- Skill: "Step 1: Create Form Request with `php artisan make:request`..."

## Example: Creating a CSV Analysis Skill

**Step 1: Understand**
- User wants to analyze CSV files
- Need to detect encoding, parse data, generate insights
- Should handle large files efficiently

**Step 2: Plan**
- Script: CSV parser with encoding detection
- Reference: Common CSV issues and solutions
- SKILL.md: Analysis workflows

**Step 3: Initialize**
```bash
mkdir -p .claude/skills/csv-analyst/{scripts,references}
touch .claude/skills/csv-analyst/SKILL.md
```

**Step 4: Edit**
Create frontmatter, workflows, examples, reminders

**Step 5: Test**
Use on actual CSV files, iterate

**Step 6: Refine**
Update based on real usage

## Tips for Effective Skills

1. **Start small** - Create focused skills, not mega-guides
2. **Use examples** - Show, don't just tell
3. **Be concise** - Every word should add value
4. **Test thoroughly** - Use on real tasks before finalizing
5. **Update regularly** - Keep skills current as tools evolve
6. **Follow conventions** - Match existing skill patterns
7. **Clear triggers** - Make it obvious when skill applies

## Important Reminders

- **ALWAYS** keep SKILL.md under 500 lines
- **ALWAYS** include concrete examples
- **ALWAYS** test skills on real tasks before finalizing
- **ALWAYS** use progressive disclosure (metadata → SKILL.md → resources)
- **NEVER** duplicate Laravel Boost guidelines
- **NEVER** include auxiliary documentation (README, changelog, etc.)
- **NEVER** create vague descriptions without clear usage triggers
- **CHECK** existing skills for patterns before creating new structure
- **ASK** clarifying questions before starting implementation

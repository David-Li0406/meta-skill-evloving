---
name: creating-skills
description: Guide for creating and reviewing skills. This skill should be used when creating new skills, updating existing skills, or conducting quality reviews (Step 5). 
---

# Creating Skills

## Metadata Quality

The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use third-person (e.g., "This skill should be used when..." instead of "Use this skill when...").

### Valid Frontmatter Schema

**Required fields:**
- `name`: Skill identifier (hyphen-case, ≤64 chars)
- `description`: What the skill does and when to use it (≤1024 chars, include trigger keywords)

**Optional fields:**
- `license`: License identifier (e.g., "MIT", "Apache-2.0")
- `allowed-tools`: List of tools this skill can use
- `metadata`: Additional structured metadata

**Invalid fields:**
- `trigger-on`: Not supported - include trigger keywords in `description` instead
- Any other custom fields not in the schema above

**Example:**
```yaml
---
name: my-skill
description: Does X when Y happens. Triggers on "keyword1", "keyword2", "phrase".
---
```

## Bundled Resources Decision Criteria

### Scripts (`scripts/`)
**When to include:** Same code rewritten repeatedly OR deterministic reliability needed
**Example (illustrative):** A script like `scripts/rotate_pdf.py` for PDF rotation tasks
**Benefit:** Token efficient, executed without loading into context

### References (`references/`)
**When to include:** Documentation Claude references while working
**Examples:** Database schemas, API docs, company policies
**Best practices:**
- Avoid duplication with SKILL.md—prefer references for detailed information
- If >10k words: include grep search patterns in SKILL.md
- Keep only essential procedural instructions in SKILL.md; move detailed reference material to references files

### Assets (`assets/`)
**When to include:** Files used in output (NOT loaded into context)
**Examples:** Templates, images, icons, boilerplate code
**Benefit:** Output resources separate from documentation

## Progressive Disclosure

3-level loading: (1) Metadata always loaded (~100 words), (2) SKILL.md on trigger (<5k words), (3) Bundled resources on-demand (unlimited—scripts executed without reading).

### LLM-First Design

Skills and their documentation are consumed by AI agents, not humans. Design ALL skill content (SKILL.md, references/, scripts) for LLM consumption with maximum information density:

**Assume LLM-level knowledge:**
- LLMs possess general software engineering knowledge (REST APIs, TDD, Git, design patterns, algorithms, data structures)
- Only document domain-specific rules, constraints, and patterns unique to the system
- Never explain universal concepts; specify when/how to apply them in this domain

**Optimize for structure over prose:**
- Decision trees > explanatory paragraphs
- Comparison tables > narrative descriptions
- Bullet lists with conditions > flowing text
- Code examples with annotations > lengthy descriptions

**Information density targets:**
- One canonical example per pattern (avoid 3-5 variations demonstrating the same concept)
- Remove pedagogical scaffolding ("Let's understand...", "Here's why...", "To see how this works...")
- Remove motivation sections explaining why something exists
- Remove background/context for general concepts
- Consolidate redundant examples into tables showing variations

**Structural patterns for high-density references:**

| Reference Purpose | Optimal Format | Anti-pattern |
|-------------------|----------------|--------------|
| Selection logic | Decision tree with terminal nodes | Multi-paragraph explanation |
| Rule enforcement | Numbered/bulleted list with conditions | Narrative description |
| Concept comparison | Comparison table (rows = options, cols = dimensions) | Side-by-side prose sections |
| Pattern catalog | Pattern name + structure + one example + variations table | Multiple full examples |
| Validation criteria | Checklist with specific criteria | Essay on quality attributes |
| Workflow steps | Ordered list with inputs/outputs | Procedural narrative |

**Size guidelines:**
- Reference docs targeting LLMs should be 50-70% shorter than human-oriented documentation
- If a reference exceeds 500 lines, evaluate for restructuring or splitting
- If explaining what a general concept is (rather than how to apply it), delete that section
- Each section should contain maximum information in minimum space

**Applies to:** SKILL.md, references/, even code comments in scripts

**Example transformations:**

❌ **Bloated SKILL.md (150 lines):**
```markdown
## About Test-Driven Development

Test-Driven Development (TDD) is a widely-used software development approach...
[5 paragraphs explaining what TDD is]

### Why You Should Use TDD
TDD provides many benefits for software development...
[3 paragraphs on TDD benefits]

### How TDD Works
The TDD cycle follows three clear steps...
[Extended tutorial with examples]
```

✅ **Dense SKILL.md (15 lines):**
```markdown
## Validation Approach

| Work Type | Method | Reason |
|-----------|--------|--------|
| Application code | TDD | Deterministic outputs |
| Meta-agentic | Artifact quality + capability testing | Non-deterministic |
| Documentation | Frontmatter/link validation | Content correctness |

Use TDD for application code. See references/ for validation procedures when applicable.
```

**Key insight:** If Claude already knows it (TDD, Git, REST), don't explain it—reference how to apply it in this domain.

## Skill Creation Process

To create a skill, follow the "Skill Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building a skill for epic planning and breakdown, relevant questions include:

- "What epic planning problems are you solving? Unclear scope, missing estimation, no North-Star alignment?"
- "Can you give examples of typical epic scenarios? Feature epics, infrastructure epics, refactoring epics?"
- "What planning artifacts need to be generated? Epic specification, story outlines, DEEP estimates?"
- "When should this skill trigger? User says 'plan epic', 'break down epic', 'create epic specification'?"
- "What methodology standards should be enforced? North-Star alignment, DEEP estimation format, story granularity?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example (illustrative): When building a `managing-epics` skill for queries like "Plan this epic" or "Break down epic into stories," the analysis shows:

1. Epic planning requires understanding North-Star alignment methodology, DEEP estimation format, epic→story breakdown patterns
2. Reference files like `references/north-star-template.md` and `references/deep-estimation-guide.md` documenting these domain-specific methodologies would be helpful to store in the skill

Example (illustrative): When building a `validating-story-structure` skill to handle queries like "Validate this story.md" or "Check story structure," the analysis shows:

1. Validating story structure requires checking frontmatter fields, required sections, gherkin format—deterministic validation logic
2. A script like `scripts/validate_structure.py` performing repeatable validation checks would be helpful to store in the skill

Example (illustrative): When building a `detailing-stories` skill for queries like "Detail this story" or "Generate story.md from epic," the analysis shows:

1. Story detailing requires template selection logic and different story templates for different work types
2. Resources like a `references/template-selection-guide.md` decision tree plus `templates/story-*.md` template files would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Reference File Frontmatter

**Critical for discoverability**: Each reference file in `references/` must include YAML frontmatter.

**Minimum required frontmatter:**
```yaml
---
title: Short descriptive title (≤100 chars)
description: What this reference contains and when to use it (≤500 chars)
skill: creating-commands
---
```

**Recommended optional fields:**
```yaml
---
title: Preflight Check Patterns
description: Bash command patterns for validating command prerequisites before execution
keywords: preflight, validation, bash, git checks, dependency checks
file-type: reference
skill: creating-commands
---
```

**Why frontmatter is required:**
- Enables programmatic discovery and indexing of references
- LLM/AI tools use it to understand file purpose and relevance
- Search and navigation tooling relies on metadata
- Documentation generation systems require structured metadata

See `references/reference-frontmatter-guide.md` for complete specification and validation details.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "Do X" or "When needing to do X"). This maintains consistency and clarity for AI consumption.

**Prompt Engineering for SKILL.md:** SKILL.md files contain instructions and prompts that Claude will execute. Invoke `Skill(command='crafting-agentic-prompts')` for guidance on writing effective agentic prompts including:

- Directive language and positive framing
- Tool usage optimization patterns
- Verbosity control and output formatting
- Long-horizon reasoning structures
- Proactive behavior triggers

This skill provides proven patterns for creating prompts that drive effective agent behavior.

**AI-Ready Documentation:** SKILL.md files are documentation that must be AI-readable. Follow AI-ready documentation principles when writing SKILL.md:

- Use strict heading hierarchy (H1→H2→H3, never skip levels)
- Make sections self-contained with necessary context
- Use explicit language (avoid vague pronouns like "it", "this", "they")
- Format all code examples in proper code blocks with language tags
- Keep consistent terminology throughout
- State prerequisites explicitly

For comprehensive guidance, reference Skill(command='writing-ai-docs') which provides templates, validation scripts, and detailed best practices for creating AI-ready documentation.

**LLM-First Principles for Reference Files:** Reference files in `references/` must be optimized for LLM consumption with maximum information density. These files are loaded on-demand, so brevity and structure are critical:

**Core principles:**
- **Assume deep knowledge:** LLMs understand general software concepts. Only document domain-specific rules and patterns.
- **Maximize density:** Target 50-70% shorter than equivalent human documentation while retaining 100% of information.
- **Structure over prose:** Use decision trees, comparison tables, checklists, and bulleted rules instead of narrative explanations.
- **One example per pattern:** Avoid multiple variations of the same concept; use tables to show variations.

**Bloat indicators to eliminate:**
- ❌ "What is [general concept]?" sections (e.g., "What is TDD?", "What is Git?")
- ❌ "Why X doesn't work for Y" with extensive pedagogical examples
- ❌ Multiple redundant examples demonstrating the same pattern
- ❌ Background/motivation/context sections for universal concepts
- ❌ Pedagogical scaffolding ("Let's understand...", "To see how this works...", "Here's why...")
- ❌ Step-by-step tutorials for concepts LLMs already understand

**High-density patterns to use:**
- ✅ Comparison tables (rows = options, columns = evaluation dimensions)
- ✅ Decision trees with clear terminal nodes
- ✅ Rule lists with specific conditions and exceptions
- ✅ Pattern name + structure + one canonical example + variations table
- ✅ Checklists with concrete verification criteria
- ✅ Code examples with inline annotations (not prose descriptions)

**Information architecture:**
- If > 500 lines, restructure using tables/trees or split into multiple focused references
- Each section should answer: "What domain-specific rule/pattern applies here?"
- Remove sections that explain general concepts; keep only domain-specific application
- Consolidate examples: one well-annotated example > five similar examples

**Example: Bloated vs Dense**

❌ **Bloated (768 lines, pedagogical):**
```markdown
## Why TDD Doesn't Work for Meta-Work

### TDD is designed for deterministic code
**TDD cycle:** Red → Green → Refactor
**Works for:** Functions with predictable inputs/outputs...

[5 paragraphs explaining what TDD is]
[JavaScript code examples of TDD working]
[Extensive explanation of non-determinism]
[Multiple examples of failed TDD attempts]
[Motivational sections on why alternatives exist]
```

✅ **Dense (50 lines, structured):**
```markdown
## Validation Method Selection

| Work Type | Method | Verification | Success Criteria |
|-----------|--------|--------------|------------------|
| Application code | TDD (unit/integration/e2e) | Tests pass | Feature works, coverage ≥80% |
| Meta-agentic | Artifact quality review | 6-category scoring | Score ≥80%, capability proven |
| Documentation | Frontmatter/link validation | Scripts pass | AI-readable, accurate |
| Infrastructure | Smoke/load tests | Manual + automated | Reliable, monitored |

**Why not TDD for meta-work:** Non-deterministic outputs (prompts, templates) have no unit-testable assertions.

**Artifact quality categories:** Structure, completeness, usability, consistency, discoverability, maintainability.
```

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

### Step 5: Quality Review

**Mandatory gate** before packaging. Two options:

**Option A: Self-review**
Follow `references/skill-quality-review.md`:
1. Run automated pre-flight: `python3 scripts/validate_skill.py /path/to/skill-folder` (must achieve ≥95%)
2. Conduct manual review of 7 quality categories using detailed checklists
3. Test skill invocation and verify functionality
4. Apply recommendation logic (APPROVE/NEEDS_REVISION/CONSIDER_DIFFERENT_TYPE)

**Quick validation during development:**
For rapid iteration cycles, use `python3 scripts/quick_validate.py /path/to/skill-folder` to perform basic frontmatter and naming convention checks without the full comprehensive validation suite.

**Option B: Use reviewer subagent**
```bash
Task(subagent_type="artifact-quality-reviewer", prompt="Review skill at /path/to/skill-folder")
```
The subagent runs automated checks first, then conducts manual review following the same framework.

See `references/skill-quality-review.md` for complete manual review workflow, scoring categories, and quality standards.

### Step 6: Packaging a Skill

Once the skill has passed quality review, package it into a distributable zip file. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `my-skill.zip`) that includes all files and maintains the proper directory structure for distribution.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

### Step 7: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
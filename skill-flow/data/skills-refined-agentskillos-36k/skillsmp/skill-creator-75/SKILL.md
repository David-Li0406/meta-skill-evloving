---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Helper commands - TypeScript commands integrated into the `ai` CLI for deterministic, repeatable tasks
5. Bundled resources - References and assets for complex workflows

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

Skills may also include helper commands, which are added to the `ai` CLI tool and executed like this:

```bash
ai skill <skill-name> <command> [...args]
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

#### Bundled Resources (optional)

##### Skill Helper Commands

TypeScript commands integrated into the `ai` CLI for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to create**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Pattern**: `ai skill <skill-name> <helper-command> [...args]`
- **Example**: `ai skill pdf-editor rotate input.pdf --degrees 90` for PDF rotation tasks
- **Implementation**:
  - Written in TypeScript
  - Integrated into the `ai` CLI app (in `typescript/lib/` or `typescript/scripts/`)
  - Use Eta templates for any templating needs
  - Follow dependency injection pattern with `InstallConfig` and `CommandExecutor`
  - Include comprehensive unit tests
- **Benefits**: Token efficient, deterministic, type-safe, testable, integrated tooling
- **Reference**: See the `skill-creator` skill itself as an example (`lib/skill-operations.ts`)

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources & helper commands** - As needed by Claude (Unlimited\*)

\*Unlimited because helper commands and scripts can be executed without reading into context window.

## Skill Creation Process

To create a skill, follow the "Skill Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what helper commands, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A TypeScript helper command `ai skill pdf-editor rotate <input.pdf> --degrees <degrees>` would be helpful to integrate into the `ai` CLI

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill
3. A TypeScript helper command `ai skill frontend-webapp-builder init <app-name> --template <template-type>` could scaffold projects from these templates

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: helper commands, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists. In this case, continue to the next step.

When creating a new skill from scratch, use the `ai skill create-skill init` command to generate a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
# Create skill in current project (.claude/skills/)
ai skill create-skill init <skill-name>

# Create skill in user-level directory (~/.claude/skills/)
ai skill create-skill init <skill-name> --scope user
```

The command:

- Creates the skill directory in the appropriate location based on scope
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

To validate a skill structure at any point:

```bash
ai skill create-skill validate <path/to/skill>
```

The validation checks:

- YAML frontmatter format and required fields (`name`, `description`)
- Skill naming conventions (hyphen-case)
- Description quality (no angle brackets)
- File organization

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above:

**Helper Commands** - For repetitive or deterministic tasks:

1. Create TypeScript module in `typescript/lib/` (e.g., `typescript/lib/pdf-operations.ts`)
2. Write core functions with proper type safety and error handling
3. Create comprehensive unit tests (e.g., `typescript/lib/pdf-operations.test.ts`)
4. Add CLI commands to `typescript/scripts/ai.ts` following the pattern: `ai skill <skill-name> <command>`
5. Use Eta templates if templating is needed (store in `typescript/templates/`)
6. Follow the `skill-creator` implementation as a reference

**References** - For documentation to be loaded into context:

- Create markdown files in the skill's `references/` directory
- Include database schemas, API documentation, policies, or detailed guides

**Assets** - For files used in output:

- Store templates, boilerplate, images, fonts, etc. in the skill's `assets/` directory

Note that implementation may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization command creates example files in `references/` and `assets/` to demonstrate structure, but not all skills will need both.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

**Using XML Tags:** XML tags help Claude parse skill instructions more accurately by clearly separating different components. According to Anthropic's guidance, there are no canonical "best" XML tags—choose tag names that make sense contextually and use them consistently.

Consider using XML tags in skills when:

- Providing multiple examples that should be easily distinguished (e.g., `<example type="valid">` vs `<example type="invalid">`)
- Separating context from instructions (e.g., `<context>` and `<instructions>`)
- Structuring complex workflows with nested steps
- Defining templates or expected output formats (e.g., `<template>`, `<format>`)
- Creating reusable instruction components that will be referenced explicitly

Common patterns for skills:

```markdown
<instructions>
Core procedural steps
</instructions>

<example type="valid">
Correct approach with explanation
</example>

<example type="invalid">
Anti-pattern with explanation
</example>

<template>
Expected output format
</template>
```

Skip XML tags when natural markdown structure is sufficient for simple, straightforward content. The key is consistency—if using XML tags, reference them explicitly in instructions and use them consistently throughout the skill.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

### Step 5: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

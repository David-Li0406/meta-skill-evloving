---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends an AI agent's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend agent capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform agents from general-purpose to specialized agents
equipped with procedural knowledge that no single model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with repos, frameworks, SDKs, APIs, and CI systems
3. Domain expertise - Project-specific architecture, conventions, schemas, and business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else an AI agent needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Agents are already very capable.** Only add context that isn't already obvious. Challenge each piece of information: "Is this explanation necessary?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of the workflow as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

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
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These fields determine when the skill gets used, so it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill, only shown after the skill is determined to be relevant.

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/apply_codemod.py` for large-scale refactors (e.g., updating imports or API usage)
- **Benefits**: Token efficient, deterministic, reusable across multiple skill invocations
- **Note**: Scripts may need review and modification for environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform an AI agent's process and thinking.

- **When to include**: For documentation that an AI agent should reference while working
- **Examples**: `references/architecture.md` for system overview, `references/coding-standards.md` for conventions, `references/api-contracts.md` for API specs, `references/db-schema.md` for schema docs
- **Use cases**: System architecture, API documentation, database schemas, conventions, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when an AI agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output an AI agent produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/starter-repo/` for a project scaffold, `assets/ci-templates/` for CI configs, `assets/codegen-templates/` for generation templates
- **Use cases**: Templates, boilerplate code, scaffolds, config snippets, sample data used in outputs
- **Benefits**: Separates output resources from documentation, enables an AI agent to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxilary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# API Client Generator

## Quick start

Generate a typed client from an OpenAPI spec:
[code example]

## Advanced features

- **Authentication**: See [AUTH.md](AUTH.md) for supported auth modes
- **Error handling**: See [ERRORS.md](ERRORS.md) for retry/backoff patterns
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

FORMS.md, REFERENCE.md, or EXAMPLES.md are loaded only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
platform-engineering-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── backend.md (services, APIs, data)
    ├── frontend.md (UI architecture, state, performance)
    ├── infra.md (CI/CD, deployments, observability)
    └── security.md (authn/authz, secrets, threat model)
```

When working on backend changes, only load backend.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When working with AWS, only load aws.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# Build & Release

## Adding new features

Prefer the existing architecture and patterns. See [ARCHITECTURE.md](ARCHITECTURE.md).

## Debugging production issues

For incident response, follow the runbook. See [RUNBOOK.md](RUNBOOK.md).

**For performance regressions**: See [PERFORMANCE.md](PERFORMANCE.md)
**For dependency upgrades**: See [DEPENDENCIES.md](DEPENDENCIES.md)
```

REDLINING.md or OOXML.md are loaded only when those features are needed.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so the full scope is visible when previewing.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill using templates
4. Edit the skill (implement resources and write SKILL.md)
5. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct examples or generated examples that are validated with feedback.

For example, when building a codebase-maintainer skill, relevant questions include:

- "What kinds of changes should this skill support? Refactors, bug fixes, migrations, feature work?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine requests like 'Upgrade React and fix breaking changes' or 'Add observability to this API'. What other requests should it handle well?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `codemod-helper` skill to handle queries like "Update imports across the repo," the analysis shows:

1. Mechanical refactors require repeating the same edits and checks
2. A `scripts/apply_codemod.py` script (or codemod templates) would be helpful to store in the skill

Example: When designing a `service-scaffold` skill for queries like "Create a new service following our conventions," the analysis shows:

1. New services require the same boilerplate setup each time (routing, logging, config, health checks)
2. An `assets/starter-service/` template containing the scaffold would be helpful to store in the skill

Example: When building an `api-client` skill to handle queries like "Add a new endpoint and keep the client in sync," the analysis shows:

1. Implementing endpoints requires consistent request/response shapes and error handling
2. A `references/api-contracts.md` file documenting the API contracts would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration is needed. In this case, continue to the next step.

When creating a new skill from scratch, use the templates provided in the `references/` directory:

- **[skill-template.md](references/skill-template.md)** - Use this as the starting point for your SKILL.md file. Copy it and customize the frontmatter and content.
- **[example-script.md](references/example-script.md)** - Reference or copy this template when creating Python/Bash scripts in your `scripts/` directory.
- **[example-reference.md](references/example-reference.md)** - Reference this template for structuring detailed documentation in your `references/` directory.
- **[example-asset.md](references/example-asset.md)** - Reference this template for understanding what types of assets belong in your `assets/` directory.

Create the skill directory structure manually. Then customize the SKILL.md using the template, replacing placeholder sections with actual content. Create example resource directories (`scripts/`, `references/`, and `assets/`) and populate them based on your skill's needs.

After initialization, customize or remove example files that aren't needed for the skill.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another AI agent to use. Include information that would be beneficial and non-obvious to an AI agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another agent execute these tasks more effectively.

#### Learn Proven Design Patterns

Consult the template files in `references/` for proven patterns:

- **[skill-template.md](references/skill-template.md)** - Includes guidance on choosing between Workflow-Based, Task-Based, Reference/Guidelines, and Capabilities-Based structures
- **[example-reference.md](references/example-reference.md)** - Shows how to organize detailed documentation and API references

These templates contain established best practices for effective skill design.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require input from skill consumers. For example, when implementing a `brand-guidelines` skill, brand assets or templates may need to be provided for `assets/`, or documentation for `references/`.

Any available scripts should be reviewed for correctness and that the output matches expectations. If there are many similar scripts, a representative sample can be reviewed to ensure confidence in the approach.

Any example files and directories not needed for the skill should be deleted. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- **Description**: This is the primary triggering mechanism for your skill, and helps agents understand when to use the skill.
  - Include both what the Skill does and specific triggers/contexts for when to use it.
  - Include all "when to use" information here - Not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body are not helpful for trigger matching.
    - Example description for a `docx` skill: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when an AI agent needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"

Do not include any other fields in YAML frontmatter.

##### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and validate improvements

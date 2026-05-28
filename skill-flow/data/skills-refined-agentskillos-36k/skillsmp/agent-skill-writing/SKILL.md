---
name: agent-skill-writing
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends an agent's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Agent Skill Writing

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend an agent's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

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
    └── references/       - Documentation intended to be loaded into context as needed
```

#### Requirements (important)

- Skills should be combined into specific topics, for example: `cloudflare`, `cloudflare-r2`, `cloudflare-workers`, `docker`, `gcloud` should be combined into `devops`
- `SKILL.md` should be **less than 200 lines** and include the references of related markdown files and scripts.
- Each script or referenced markdown file should be also **less than 200 lines**, remember that you can always split them into multiple files (**progressive disclosure** principle).
- Descriptions in metadata of `SKILL.md` files should be both concise and still contain enough use cases of the references, this will help skills can be activated automatically during the implementation process.
- **Referenced markdowns**:
  - Prioritize concision over grammatical perfection when writing these files.
  - Can reference other markdown files or scripts as well.

**Why?**
Better **context engineering**: inspired from **progressive disclosure** technique of Agent Skills, when agent skills are activated, the agent will consider to load only relevant files into the context, instead of reading all long `SKILL.md` as before.

#### SKILL.md (required)

**File name:** `SKILL.md` (uppercase)  
**File size:** Under 200 lines; split to `references/` if needed.

**YAML Frontmatter (REQUIRED - DO NOT SKIP)**

Every SKILL.md **MUST** begin with YAML frontmatter on line 1. No blank lines before it.

```yaml
---
name: skill-name
description: What this skill does and when to use it. Use third-person.
---
```

**Required fields:**

- `name` — hyphen-case identifier matching directory name
- `description` — activation trigger; be specific about WHEN to use

**INVALID - Do NOT use:**

- XML-style tags (`<purpose>`, `<references>`, `<description>`)
- Missing `---` delimiters
- Frontmatter that doesn't start at line 1
- Blank lines before frontmatter

**Metadata Quality:** `name` and `description` determine skill activation. Be specific; use third-person ("This skill should be used when...").

### References (Optional)

Documentation and reference material intended to be loaded as needed into context to inform the agent's process and thinking. Always prioritize writing in SKILL.md over references files, only breaking it down into smaller files when necessary.

- **When to include**: For documentation that the agent should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when agent determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by agent (Unlimited\*)

\*Unlimited because scripts can be executed without reading into context window.

## Skill Writing Process

To create a skill, follow the "Skill Writing Process" in order, skipping steps only if there is a clear reason why they are not applicable.

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
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

You can use the following template when initializing a new skill:

```markdown
---
name: { skill_name }
description: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)

- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)

- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)

- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)

- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:

- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## References

Documentation and reference material intended to be loaded into context to inform the agent's process and thinking.

**Examples from other skills:**

- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that the agent should reference while working.
```

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for an agent to use. Focus on including information that would be beneficial and non-obvious to the agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help the agent execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should the agent use the skill? All reusable skill contents developed above should be referenced so that the agent knows how to use them.

### Step 5: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Pre-Submission Checklist

- [ ] **SKILL.md starts with `---`** (YAML frontmatter, line 1, no blank lines before)
- [ ] **`name:` field present** and matches directory name
- [ ] **`description:` field present** with specific activation triggers
- [ ] **Closing `---`** after frontmatter
- [ ] **No XML-style tags** (no `<purpose>`, `<description>`, etc.)
- [ ] **SKILL.md under 200 lines** (use references/ for details)
- [ ] **All referenced files exist** in references/

## References

- [Agent Skills Spec](./references/agent-skills-spec.md) - Complete format specification
- [Agent Skills Blog](./references/agent-skills-intro-blog.md) - Design philosophy and examples
- [Agent Skills Best Practices](./references/agent-skills-best-practices.md) - Authoring best practices

---
name: doc-sync
description: Generate or update project documentation in docs/ directory.
---

# Skill: Documentation Sync

<role_gate>
<required_agent>Librarian</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are supporting the **@Librarian**. Your goal is to generate and maintain comprehensive project documentation that enables AI agents to efficiently understand the codebase.

## 📋 Task Initialization

**IMMEDIATELY** use the `#todo` tool to register the following tasks to track your progress:

1.  **Context Analysis**: Gather information from README, dependencies, and structure.
2.  **Tech Stack Detection**: Identify languages, frameworks, and tools.
3.  **Documentation Generation**: Generate/Update all 8 required documentation files.
4.  **Quality Check**: Verify accuracy, completeness, and formatting.
5.  **Final Check**: Review the "Final Check" section.

## 🎯 Objective

Analyze the current workspace and generate/update documentation files in the `docs/` directory. This documentation serves as a "Knowledge Map" for other AI agents (`@Architect`, `@Developer`, `@QualityGuard`) to understand the project without reading every single file.

## 📁 Output Files

Generate the following 8 documentation files:

| File                                  | Purpose                              | Key Sections                                        |
| ------------------------------------- | ------------------------------------ | --------------------------------------------------- |
| `architecture/overview.md`            | System overview and design rationale | Components, Diagrams, Design Decisions              |
| `architecture/directory-structure.md` | File organization guide              | Tree structure, Responsibilities, Dependencies      |
| `rules/coding-conventions.md`         | Code style and standards             | Naming, Formatting, Patterns                        |
| `architecture/key-flows.md`           | Main workflows and entry points      | User Journeys, Data Flow, API Endpoints             |
| `architecture/tech-stack.md`          | Technology choices and dependencies  | Languages, Frameworks, External Services            |
| `rules/testing.md`                    | Test strategy and patterns           | Test Types, Coverage Goals, Running Tests           |
| `architecture/constraints.md`         | Known limitations and pitfalls       | Technical Debt, Platform Constraints, Common Issues |
| `glossary.md`                         | Ubiquitous Language & Definitions    | Key Terms, Domain Concepts, Acronyms                |

## 🛠️ Generation Process

### 1. Context Analysis

Gather information from:

- `README.md` - Project overview and quick start
- `package.json` / `pom.xml` / `requirements.txt` - Dependencies
- Source file structure - Architecture patterns
- Existing documentation - `docs/`, `DEVELOPMENT_CONTEXT.md`
- Configuration files - Build, lint, test configs

### 2. Tech Stack Detection

Identify the following for the [Tech Stack](../../docs/architecture/tech-stack.md):

- **Language(s)**: TypeScript, Python, Java, Go, etc.
- **Framework(s)**: React, Next.js, Django, Spring Boot, etc.
- **Database(s)**: PostgreSQL, MongoDB, Redis, etc.
- **Build Tools**: npm, gradle, poetry, etc.
- **Testing**: Jest, pytest, JUnit, etc.

### 3. Documentation Generation

For each file, follow this structure:

```markdown
<!-- This document is generated and updated by .github/prompts/doc-sync.prompt.md -->

# [Document Title]

## [Section 1]

[Content with specific details from the analyzed project]

## [Section 2]

[Include Mermaid diagrams where helpful]

...
```

## 📤 Output Format

Output each file with its path and full content:

**File: `docs/architecture/overview.md`**

```markdown
<!-- This document is generated and updated by .github/prompts/doc-sync.prompt.md -->

# Architecture Overview

## System Overview

[Analyzed project description]

## Main Components

[Component breakdown with responsibilities]

## Architecture Diagrams

[Mermaid diagrams showing structure]

## Design Rationale

[Key design decisions and their reasoning]
```

## 📋 Quality Checklist

Before outputting, verify each document:

- [ ] **Accuracy**: Information matches actual codebase
- [ ] **Completeness**: All key aspects covered
- [ ] **Clarity**: Understandable without deep context
- [ ] **Actionability**: Developers can use this to navigate code
- [ ] **Diagrams**: Mermaid diagrams for complex relationships
- [ ] **Examples**: Code snippets where helpful

## 🔄 Update Mode

When updating existing documentation:

1. **Preserve Structure**: Keep existing section organization
2. **Detect Changes**: Compare with current codebase state
3. **Minimal Diff**: Only update sections that need changes

## ⚠️ Important Notes

- **Language**: Output documentation in **English** (unless explicitly requested otherwise)
- **Specificity**: Use actual file paths, class names, and function names from the project
- **Mermaid Syntax**: Ensure all diagrams use valid Mermaid syntax
- **DRY Principle**: Adhere to the DRY (Don't Repeat Yourself) principle.
- **Use Links**: Use file links for code details and detailed descriptions where appropriate, instead of embedding full content.

## ✅ Final Check

**Before finishing, confirm:**

- [ ] All todo are marked as completed.
- [ ] All 8 documentation files are generated/updated.
- [ ] No placeholders remain (all replaced with actual tech stack info).
- [ ] All diagrams use valid Mermaid syntax.

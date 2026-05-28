---
name: claude-workspace
description: Use this skill when creating or organizing working files in the .claude/ directory to ensure consistent structure, naming conventions, and required cross-references for various documentation types.
---

# Claude Workspace Organization

## Purpose

Maintain organized working files in the `.claude/` directory with enforced structure, consistent naming, and required cross-references to codebase files and related documentation.

**Use this skill when:**
- Creating implementation plans, architecture decisions, or design documents
- Documenting research findings or code analysis
- Capturing reusable code examples or patterns
- Organizing existing loose planning files
- Validating workspace structure

## Directory Structure

```
.claude/
├── plans/              # Implementation plans, migration plans, project plans
│   └── INDEX.md
├── architecture/       # ADRs, design decisions, system diagrams
│   └── INDEX.md
├── examples/           # Code examples, usage patterns, reference implementations
│   └── INDEX.md
├── research/           # Research notes, external findings, comparative analysis
│   └── INDEX.md
└── analysis/           # Code analysis, performance studies, security reviews
    └── INDEX.md
```

## Essential Principles

1. **Every File Links to Codebase**: Every working file MUST contain at least one link to a relevant codebase file. No orphan documentation.
2. **Every File Links to Related .claude/ Docs**: Files should cross-reference related documents in other categories when relevant connections exist.
3. **INDEX.md is Auto-Updated**: When creating or modifying files, always update the category's INDEX.md.
4. **Consistent Frontmatter**: All files use YAML frontmatter with required fields per category.

## Intake

**What would you like to do?**

1. **Create new file** - Create a plan, architecture doc, example, research, or analysis
2. **Update INDEX** - Manually refresh a category's INDEX.md
3. **Validate workspace** - Check workspace structure and fix issues
4. **Migrate existing** - Organize loose files into proper structure

**Wait for response before proceeding.**

## Routing

| Response | Workflow |
|----------|----------|
| 1, "create", "new", "add", "plan", "architecture", "example", "research", "analysis" |
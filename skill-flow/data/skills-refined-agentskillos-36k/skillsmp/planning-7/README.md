# Planning Skill - Quick Reference

## Overview

The Planning Skill generates and optimizes Product Requirements Documents (PRDs) and Implementation Plans as AI artifacts optimized for AI agent consumption.

**Primary Use Cases**:
- Generate PRDs from feature requests
- Create phased Implementation Plans with subagent assignments
- Optimize long planning docs by breaking into phase-specific files

---

## Quick Start

### Generate PRD

```
User: "Create a PRD for advanced filtering on prompts"

Skill:
1. Extracts feature details
2. Uses prd-template.md
3. Generates: docs/project_plans/PRDs/features/advanced-filtering-v1.md
```

### Generate Implementation Plan

```
User: "Create implementation plan for docs/project_plans/PRDs/features/advanced-filtering-v1.md"

Skill:
1. Reads PRD
2. Uses implementation-plan-template.md
3. Breaks into 8 phases following MP architecture
4. Assigns subagents to each task
5. Creates: docs/project_plans/implementation_plans/features/advanced-filtering-v1.md
   (and phase files if plan >800 lines)
```

### Optimize Existing Plan

```
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md"

Skill:
1. Analyzes plan (1200 lines)
2. Breaks into phase files (~400 lines each)
3. Updates parent with links
4. Results in 50-70% token reduction
```

---

## Key Concepts

### Token Efficiency

Files optimized for AI loading:
- **Target**: ~800 lines max per file
- **Strategy**: Progressive disclosure (summary → detail)
- **Result**: 50-70% token reduction for most queries

### Project Architecture Compliance

All plans follow layered architecture.

### Subagent Integration

Every task assigned to appropriate specialist:
- Database → data-layer-expert
- Backend → python-backend-engineer, backend-architect
- Frontend → ui-engineer-enhanced, frontend-developer
- Testing → testing specialists
- Docs → documentation-writer

---

## File Structure

```
docs/project_plans/
├── PRDs/[category]/
│   └── feature-name-v1.md
└── implementation_plans/[category]/
    ├── feature-name-v1.md (parent)
    └── feature-name-v1/ (phase files if >800 lines)
        ├── phase-1-3-backend.md
        ├── phase-4-5-frontend.md
        └── phase-6-8-validation.md

.claude/progress/
└── feature-name/
    └── phase-{N}-progress.md (one file per phase)
```

---

## Templates

Located in `./templates/`:

1. **prd-template.md** - Standard PRD structure
2. **implementation-plan-template.md** - 8-phase plan structure
3. **phase-breakdown-template.md** - Individual phase file format

---

## References

Located in `./references/`:

1. **subagent-assignments.md** - Task type to subagent mapping
2. **file-structure.md** - Directory organization and naming
3. **optimization-patterns.md** - Strategies for breaking up large files

---

## Scripts

Located in `./scripts/`:

**Note**: Currently placeholders, need Node.js implementation

1. **generate-prd.sh** - Generate PRD from description
2. **generate-impl-plan.sh** - Generate plan from PRD
3. **optimize-plan.sh** - Break up long plan

---

## Common Workflows

### Workflow 1: New Feature from Scratch

1. Generate PRD: `"Create PRD for [feature]"`
2. Generate Plan: `"Create implementation plan for [prd-path]"`
3. Start Implementation: Development agents use progress tracking

### Workflow 2: Optimize Existing Planning Docs

1. Analyze Plan: Check line count
2. Optimize: `"Optimize [plan-path]"` if >800 lines
3. Validate: Ensure all content preserved
4. Update Links: Cross-link phase files

---

## Best Practices

1. **File Sizes**: Keep files <800 lines for optimal token efficiency
2. **Naming**: Use kebab-case, version numbers (-v1), descriptive names
3. **Cross-Linking**: Always link related documents (PRD ↔ Plan ↔ Progress)
4. **Subagent Assignments**: Use reference guide for consistent assignments
5. **Progressive Disclosure**: Summary in parent, details in phase files

---

## Examples

See SKILL.md "Examples" section for:
- Creating PRD for advanced filtering
- Generating implementation plan with phase breakout
- Optimizing long plan

---

## Integration with Project

### Documentation Policy

Follows CLAUDE.md:
- PRDs/Plans: `/docs/` with YAML frontmatter

### Subagent Ecosystem

Integrates with 50+ subagents:
- Architecture: lead-architect, backend-architect, data-layer-expert
- Development: python-backend-engineer, frontend-developer, ui-engineer-enhanced
- Review: code-reviewer, task-completion-validator
- Documentation: documentation-writer, documentation-complex
- Testing: testing specialists

---

## For Full Details

See `SKILL.md` for:
- Complete workflow descriptions
- All templates
- All scripts
- Complete references
- Detailed examples
- Troubleshooting guide

---

## Quick Tips

**Creating PRDs**:
- Be specific about feature requirements
- Include user stories and pain points
- Reference related ADRs and guides

**Creating Plans**:
- Follow 8-phase MP architecture sequence
- Break into phase files if >800 lines
- Assign subagents to every task

**Optimizing Plans**:
- Group related phases (1-3, 4-5, 6-8)
- Keep summary in parent (200-300 lines)
- Use descriptive phase file names

---

**Version**: 2.0
**Last Updated**: 2025-12-01
**Skill Location**: `.claude/skills/planning/`

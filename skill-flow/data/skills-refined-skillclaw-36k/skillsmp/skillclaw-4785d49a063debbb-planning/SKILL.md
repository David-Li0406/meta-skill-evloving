---
name: planning
description: Use this skill when you need to generate and optimize Product Requirements Documents (PRDs) and Implementation Plans for development projects, especially when breaking down long documents or setting up progress tracking.
---

# Skill body

## About This Skill

The Planning Skill generates and optimizes Product Requirements Documents (PRDs) and Implementation Plans as AI artifacts - file-based context caches optimized for AI agent consumption rather than human reading.

### Purpose

- Generate comprehensive PRDs from feature requests.
- Create phased Implementation Plans with subagent task assignments.
- Optimize existing planning docs by breaking them into token-efficient files.
- Set up progress tracking structures for multi-phase implementations.

### Key Benefits

- **Token Efficiency**: Max ~800 lines per file for optimal AI context loading.
- **Progressive Disclosure**: Summary → Detail pattern with linked files.
- **Subagent Integration**: Automatic task assignment to appropriate specialists.
- **MP Architecture Compliance**: Plans follow layered architecture (routers → services → repositories → DB).
- **Structured Tracking**: One progress file per phase following CLAUDE.md policy.

### When to Use This Skill

- Creating PRDs for new features or enhancements.
- Generating detailed implementation plans from PRDs.
- Breaking down long planning documents (>800 lines) into manageable files.
- Setting up progress tracking for multi-phase work.
- Optimizing existing plans for better AI agent consumption.

## Quick Start

### Create PRD from Feature Request

```bash
# User provides feature description
User: "Create a PRD for advanced filtering on the prompts page"

# Skill generates PRD at:
# docs/project_plans/PRDs/[category]/advanced-filtering-v1.md
```

### Create Implementation Plan from PRD

```bash
# Provide PRD path
User: "Create implementation plan for docs/project_plans/PRDs/features/advanced-filtering-v1.md"

# Skill generates:
# Main plan + phase files (if >800 lines)
```

### Optimize Existing Plan

```bash
# User provides existing plan path
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md"

# Skill breaks 1200-line plan into summary + 3 phase files
```

### Create Progress Tracking

```bash
# User provides PRD for tracking
User: "Create progress tracking for data-layer-fixes PRD"

# Skill delegates to artifact-tracking skill
```
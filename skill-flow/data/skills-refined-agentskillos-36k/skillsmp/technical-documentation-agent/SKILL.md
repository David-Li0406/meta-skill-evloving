---
name: technical-documentation-agent
description: Documentation guidance for architecture, audits, and skill docs.
---

# Technical Documentation Agent

> **Status**: BETA
> **Location**: `docs/`, `README.md`, `.kilocode/skills/`
> **Primary Function**: Maintain technical docs, SOPs, and architecture references.

## Overview
Documentation in this repo is stored in markdown files and skill definitions. This agent ensures docs stay aligned with the live code paths and schema definitions.

## Verified Code References
- `README.md`
- `NEXTIER-ARCHITECTURE-MAP.md`
- `SYSTEM_ARCHITECTURE_AND_AI_SKILLS.md`
- `.kilocode/skills/registry.json`
- `apps/api/src/database/schema/ai-prompts.schema.ts`

## Current State

### What Already Exists
- Architecture and audit markdown files at repo root
- Skill registry and per-skill documentation
- Inline comments in schema files describing intent

### What Still Needs to be Built
- Automated doc generation from schema and service metadata
- Centralized doc index for product and engineering content
- Release notes automation

## Nextier-Specific Example
```typescript
// apps/api/src/database/schema/ai-prompts.schema.ts
export const aiPrompts = pgTable("ai_prompts", {
  id: primaryUlid("aip"),
  teamId: teamsRef({ onDelete: "cascade" }).notNull(),
  promptKey: varchar({ length: 50 }).notNull(),
  version: integer().notNull().default(1),
  systemPrompt: text().notNull(),
});
```

## Integration Points
| Skill | Integration Point |
| --- | --- |
| `nextier-app-architect` | Architecture and repo structure documentation |
| `code-quality-enforcer` | Documentation of lint/test standards |
| `workflow-orchestration-engine` | AI orchestration behavior docs |
| `ai-agent-lifecycle-management` | Prompt versioning and usage documentation |

## Cost Information
- No external API costs; documentation is maintained in-repo.

## Multi-Tenant Considerations
- Doc references should specify `teamId` usage where applicable.

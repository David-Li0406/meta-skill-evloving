---
name: discover-feature
description: Interactive feature discovery using JTBD framework - transforms vague ideas into well-defined specs
---

# Feature Discovery Skill

## Invocation
This skill is **only** invoked explicitly via the `/discover-feature` command.

**No auto-triggers.** The user must explicitly run `/discover-feature [optional idea]` to start the discovery process.

## Purpose
Transforms vague feature ideas into well-defined specifications through structured, conversational discovery using the JTBD (Jobs to be Done) framework and multi-expert analysis.

## What Happens When Invoked

The `/discover-feature` command initiates an interactive 4-phase discovery session:

### Phase 1: Problem Discovery
- Scan codebase for related functionality
- Ask JTBD questions (trigger, outcome, alternatives, pain points)
- Synthesize and validate a Job-to-be-Done statement

### Phase 2: Solution Exploration
- Product Manager perspective (business value)
- UX Designer perspective (user journey)
- Technical Architect perspective (2-3 implementation approaches)
- User chooses preferred approach

### Phase 3: Scope Definition
- Define MVP requirements (multi-select)
- Explicitly list out-of-scope items
- Set measurable success criteria

### Phase 4: Spec Output
- User chooses output format and location
- Generate spec in chosen format(s)
- Write to file if requested

## Integration Points

### Related Commands
- `/create-spec` - Direct spec creation (skip discovery)
- `/plan-product` - Higher-level product planning

### Output Locations
- `/docs/specs/` - Feature specifications
- `/docs/tasks/` - Implementation task breakdown

### Reference Files
- `references/jtbd-framework.md` - Question templates
- `references/spec-templates.md` - Output formats

## Notes
- This skill favors conversation over documentation
- Always scans codebase before making suggestions
- Biases toward smaller, incremental features
- Validates understanding frequently with the user

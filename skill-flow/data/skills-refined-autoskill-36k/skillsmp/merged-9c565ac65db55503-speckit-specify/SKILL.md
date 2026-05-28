---
name: speckit-specify
description: Use this skill to create or update a feature specification from a natural language feature description.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Memory Integration

### Before Starting
Search for related prior work:
```bash
./scripts/memory-search "{feature keywords}"
```
Look for existing patterns, prior decisions, and related features to inform scope and avoid contradictions.

### After Completion
Save key requirements captured:
```bash
./scripts/memory-save --decisions "Key requirements for {feature}: {summary}" --issues ""
```

## Constitution Alignment

This skill aligns with project principles:
- **User-Focused**: Specifications focus on WHAT users need, not HOW to implement.
- **Testable Requirements**: Every requirement must be verifiable.
- **Clear Boundaries**: Explicit scope and out-of-scope declarations.

## Integration Considerations (REQUIRED)

When specifying a feature, document integration points to prevent isolated implementations:

**Add to spec.md under "Scope" section:**

1. **Entry Points**: How will users access this feature?
   - CLI command? → Which command group?
   - Plugin? → Which plugin type?
   - API? → Which endpoint?

2. **Dependencies**: What existing components does this feature need?
   - Which packages? (e.g., floe-core, floe-dagster)
   - Which plugins? (e.g., ComputePlugin, CatalogPlugin)
   - Which services? (e.g., Polaris, S3)

3. **Outputs**: What does this feature produce that others consume?
   - New schemas? → Add to CompiledArtifacts
   - New plugins? → Register entry points
   - New APIs? → Document contracts

**If integration is unclear**: Ask during `/speckit.clarify` before planning begins.

## Outline

The text the user typed after `/speckit.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords.
   - Create a 2-4 word short name that captures the essence of the feature.
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug").
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.).

2. **Check for existing branches before creating a new one**:

   a. First, fetch all remote branches to ensure we have the latest information:
   ```bash
   git fetch --all --prune
   ```

   b. Find the highest feature number across all sources for the short-name:
   - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
   - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
   - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`

   c. Determine the next available number:
   - Extract all numbers from all three sources.
   - Find the highest number N.
   - Use N+1 for the new branch number.

   d. Run the script `.specify/scripts/bash/create-new-feature.sh --json "<feature description>"` with the calculated number and short-name.

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this execution flow:
   1. Parse user description from Input. If empty: ERROR "No feature description provided".
   2. Extract key concepts from description: Identify actors, actions, data, constraints.
   3. For unclear aspects, make informed guesses based on context and industry standards. Limit clarifications to a maximum of 3 [NEEDS CLARIFICATION] markers.
   4. Fill User Scenarios & Testing section. If no clear user flow: ERROR "Cannot determine user scenarios".
   5. Generate Functional Requirements. Each requirement must be testable.
   6. Define Success Criteria. Create measurable, technology-agnostic outcomes.
   7. Identify Key Entities (if data involved).
   8. Return: SUCCESS (spec ready for planning).

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:
   - Create a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure.
   - Review the spec against each checklist item and document specific issues found.
   - Handle validation results accordingly.

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/speckit.clarify` or `/speckit.plan`).

## General Guidelines

### Quick Guidelines
- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.

### Section Requirements
- **Mandatory sections**: Must be completed for every feature.
- **Optional sections**: Include only when relevant to the feature.

### For AI Generation
1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps.
2. **Document assumptions**: Record reasonable defaults in the Assumptions section.
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers.

### Success Criteria Guidelines
Success criteria must be:
1. **Measurable**: Include specific metrics (time, percentage, count, rate).
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools.
3. **User-focused**: Describe outcomes from user/business perspective, not system internals.
4. **Verifiable**: Can be tested/validated without knowing implementation details.

## Handoff
After completing this skill:
- **Clarify requirements**: Run `/speckit.clarify` to resolve ambiguities.
- **Create plan**: Run `/speckit.plan` to generate technical implementation plan.

## References
- **`.specify/templates/spec-template.md`** - Specification template
- **`docs/plans/EPIC-OVERVIEW.md`** - Epic definitions
- **`.specify/memory/constitution.md`** - Project principles
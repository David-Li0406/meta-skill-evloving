---
name: speckit-plan
description: Use this skill when the feature spec is ready and you need to execute the implementation planning workflow to generate design artifacts.
---

# Skill body

## Inputs
- `specs/<feature>/spec.md`
- Repo context and `.specify/` templates
- User-provided constraints or tech preferences (if any)

If the spec is missing, ask the user to run speckit-specify first.

## Workflow

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from the repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g., 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load the IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in the IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION").
   - Fill Constitution Check section from the constitution.
   - Evaluate gates (ERROR if violations unjustified).
   - Phase 0: Generate `research.md` (resolve all NEEDS CLARIFICATION).
   - Phase 1: Generate `data-model.md`, `contracts/`, `quickstart.md`.
   - Phase 1: Update agent context by running the agent script.
   - Re-evaluate Constitution Check post-design.

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research
1. **Extract unknowns from Technical Context**:
   - For each NEEDS CLARIFICATION → research task.
   - For each dependency → best practices task.
   - For each integration → patterns task.

2. **Generate and dispatch research agents**:
   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: `research.md` with all NEEDS CLARIFICATION resolved.

### Phase 1: Design & Contracts
**Prerequisites:** `research.md` complete
1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships.
   - Validation rules from requirements.
   - State transitions if applicable.

2. **Generate API contracts** from functional specifications.
3. **Integration Design**: Every `plan.md` MUST include an Integration Design section to ensure features are designed to connect to the system, not operate in isolation.

**Add to `plan.md` after Technical Context:**
```markdown
## Integration Design

### Entry Point Integration
- [ ] Feature reachable from: [CLI / Plugin / API / Internal]
- [ ] Integration point: [specific file/module that exposes this]
- [ ] Wiring task needed: [Yes/No - if Yes, add to tasks.md]

### Dependency Integration
| This Feature Uses | From Package | Integration Point |
|-------------------|--------------|-------------------|
| CompiledArtifacts | floe-core | Loaded via .from_json_file() |
| [component] | [package] | [how integrated] |

### Produces for Others
| Output | Consumers | Contract |
|--------|-----------|----------|
| [schema/API/plugin] | [who uses it] | [Pydantic model/entry point] |

### Cleanup Required (if refactoring)
If this feature replaces or refactors existing code:
- [ ] Old code to remove: [files/functions to delete]
- [ ] Old tests to remove: [test files that test removed code]
- [ ] Old docs to update: [docs referencing old code]
```
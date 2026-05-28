# Plan Create Examples

## Basic Usage

### Create Simple Plan

```bash
/plan-create "My Feature Implementation"
```

**Output:**

```text
Creating plan: my-feature-implementation
  Title: My Feature Implementation
  Type: feature (default)

✓ Template read: feature-plan.md
✓ Frontmatter generated
✓ Plan written: .claude/plans/my-feature-implementation.md
✓ Validation passed

Plan created successfully:
  Name: my-feature-implementation
  Status: ready (0%)
  Path: .claude/plans/my-feature-implementation.md
```

**Generated File:**

```yaml
---
name: my-feature-implementation
title: "My Feature Implementation"
created: 2026-01-18
updated: 2026-01-18
status: ready
progress: 0
implements: []
modules: []
categories: [feature]
# ... rest of template content
---
```

### Create Plan with Module

```bash
/plan-create "Add Caching Layer" --module=effect-type-registry
```

**Output:**

```text
Creating plan: add-caching-layer
  Title: Add Caching Layer
  Type: feature
  Module: effect-type-registry

✓ Module validated: effect-type-registry exists in design.config.json
✓ Plan created: .claude/plans/add-caching-layer.md
✓ Validation passed
```

**Generated Frontmatter:**

```yaml
---
name: add-caching-layer
title: "Add Caching Layer"
modules:
  - effect-type-registry
status: ready
progress: 0
# ...
---
```

### Create Plan with Design Doc Link

```bash
/plan-create "Implement Observability" \
  --module=effect-type-registry \
  --implements=effect-type-registry/observability.md
```

**Output:**

```text
Creating plan: implement-observability
  Module: effect-type-registry
  Implements: effect-type-registry/observability.md

✓ Design doc found: .claude/design/effect-type-registry/observability.md
✓ Plan created with bidirectional link
✓ Validation passed

Next steps:
  1. Fill in implementation phases
  2. Update design doc to reference this plan
  3. Set estimated-effort field
```

**Generated Frontmatter:**

```yaml
---
name: implement-observability
implements:
  - effect-type-registry/observability.md
modules:
  - effect-type-registry
# ...
---
```

## Advanced Usage

### Create with Custom Name

```bash
/plan-create "Phase 2: Advanced Features" \
  --name=advanced-features-phase-2
```

**Output:**

```text
Creating plan: advanced-features-phase-2
  Title: Phase 2: Advanced Features
  Custom name provided

✓ Name validated: kebab-case format
✓ Plan created: advanced-features-phase-2.md
```

Useful when title has special characters or doesn't convert well.

### Create Refactoring Plan

```bash
/plan-create "Refactor Type Loading System" --type=refactor
```

**Output:**

```text
Creating plan: refactor-type-loading-system
  Type: refactor

✓ Template: refactor-plan.md
✓ Categories: [refactoring]
✓ Plan created with refactoring template
```

**Template Differences:**

- Focuses on "Current State" and "Target State"
- Includes "Migration Strategy" section
- Risk assessment and rollback plan

### Create Documentation Plan

```bash
/plan-create "Write API Documentation" --type=docs
```

**Output:**

```text
Creating plan: write-api-documentation
  Type: docs

✓ Template: docs-plan.md
✓ Categories: [documentation]
✓ Plan created with documentation template
```

**Template Differences:**

- Content planning phase
- Writing and review phases
- Examples and diagrams sections

### Create with All Metadata

```bash
/plan-create "Cache Optimization" \
  --module=effect-type-registry \
  --implements=effect-type-registry/cache-optimization.md \
  --owner=@spencerbeggs \
  --estimated-effort="2-3 weeks"
```

**Output:**

```text
Creating plan: cache-optimization
  Module: effect-type-registry
  Implements: effect-type-registry/cache-optimization.md
  Owner: @spencerbeggs
  Estimated: 2-3 weeks

✓ All metadata validated
✓ Plan created: cache-optimization.md
✓ Ready to start implementation
```

**Generated Frontmatter:**

```yaml
---
name: cache-optimization
title: "Cache Optimization"
modules:
  - effect-type-registry
implements:
  - effect-type-registry/cache-optimization.md
owner: @spencerbeggs
estimated-effort: "2-3 weeks"
status: ready
progress: 0
# ...
---
```

## Error Scenarios

### Plan Already Exists

```bash
/plan-create "Existing Feature"
```

**Output:**

```text
✗ Plan creation failed: existing-feature

Error: Plan file already exists
Path: .claude/plans/existing-feature.md
Created: 2026-01-15

Options:
  1. Use different name: --name=existing-feature-v2
  2. Update existing: /plan-update existing-feature
  3. Archive old plan first
```

### Invalid Module

```bash
/plan-create "New Feature" --module=nonexistent-module
```

**Output:**

```text
✗ Plan creation failed: new-feature

Error: Module not found: nonexistent-module

Available modules:
  - effect-type-registry
  - rspress-plugin-api-extractor
  - design-doc-system

Fix: Use --module={valid-module} or omit --module flag
```

### Invalid Design Doc Path

```bash
/plan-create "Feature" \
  --implements=effect-type-registry/nonexistent.md
```

**Output:**

```text
✗ Plan creation failed: feature

Error: Design doc not found
Path: .claude/design/effect-type-registry/nonexistent.md

Available design docs in effect-type-registry:
  - observability.md
  - cache-optimization.md

Fix: Verify path or omit --implements flag
```

### Invalid Name Format

```bash
/plan-create "Feature" --name="Invalid Name With Spaces"
```

**Output:**

```text
✗ Plan creation failed

Error: Invalid plan name format
Name: Invalid Name With Spaces

Plan names must be kebab-case:
  - Lowercase letters only
  - Numbers allowed
  - Hyphens to separate words
  - No spaces or special characters

Valid examples:
  - my-feature
  - cache-optimization-v2
  - phase-1-implementation

Fix: Use --name={valid-kebab-case} or omit --name to auto-generate
```

### Invalid Template Type

```bash
/plan-create "Feature" --type=invalid
```

**Output:**

```text
✗ Plan creation failed: feature

Error: Template not found: invalid-plan.md

Available templates:
  - feature (feature-plan.md)
  - refactor (refactor-plan.md)
  - docs (docs-plan.md)

Fix: Use --type=feature|refactor|docs
```

## Integration Workflows

### After Creating Design Doc

```bash
# Create design doc first
/design-init effect-type-registry "Cache Optimization"

# Create implementation plan
/plan-create "Cache Optimization Implementation" \
  --module=effect-type-registry \
  --implements=effect-type-registry/cache-optimization.md
```

**Workflow:**

1. Design doc describes what to build
2. Plan tracks implementation progress
3. Bidirectional links keep them synchronized

### Before Starting Implementation

```bash
# Create plan before coding
/plan-create "Observability Phase 2" \
  --module=effect-type-registry \
  --implements=effect-type-registry/observability.md \
  --estimated-effort="1-2 weeks"

# Review plan
/plan-validate observability-phase-2

# Start work (updates status and dates)
/plan-update observability-phase-2 --status=in-progress
```

### Multi-Plan Feature

```bash
# Large feature split into phases
/plan-create "Type Loading - Phase 1" \
  --name=type-loading-phase-1 \
  --module=effect-type-registry

/plan-create "Type Loading - Phase 2" \
  --name=type-loading-phase-2 \
  --module=effect-type-registry \
  --related-plans=type-loading-phase-1
```

**Result:**

- Plans linked via `related-plans` field
- Can track overall progress across phases
- Clear dependencies and sequencing

## Post-Creation Steps

### Fill in Implementation Details

After creating plan, edit to add:

1. **Detailed scope and motivation**
2. **Implementation phases with tasks**
3. **Success criteria for each phase**
4. **Dependencies and blockers**
5. **Notes and considerations**

```bash
# Create plan
/plan-create "My Feature"

# Edit to add details
code .claude/plans/my-feature.md

# Validate after editing
/plan-validate my-feature
```

### Link from Design Doc

If plan implements a design doc, update the design doc frontmatter:

```yaml
# .claude/design/my-module/my-feature.md
---
implementation-plans:
  - ../plans/my-feature.md
---
```

This creates bidirectional linking for discovery.

### Start Implementation

When ready to start work:

```bash
# Update status to in-progress
/plan-update my-feature --status=in-progress

# This will:
# - Set status to "in-progress"
# - Set started date to current date
# - Update updated date
```

## Batch Operations

### Create Multiple Related Plans

```bash
# Phase 1
/plan-create "Feature X - Phase 1" \
  --name=feature-x-phase-1 \
  --module=my-module

# Phase 2 (references phase 1)
/plan-create "Feature X - Phase 2" \
  --name=feature-x-phase-2 \
  --module=my-module \
  --related-plans=feature-x-phase-1

# Phase 3 (references phase 2)
/plan-create "Feature X - Phase 3" \
  --name=feature-x-phase-3 \
  --module=my-module \
  --related-plans=feature-x-phase-2
```

### Create Plans for All Design Docs

```bash
# List design docs without plans
/design-list --no-plans

# Create plan for each
/plan-create "Implement Feature A" \
  --implements=my-module/feature-a.md
/plan-create "Implement Feature B" \
  --implements=my-module/feature-b.md
```

## Tips

### Auto-Generate Good Names

The skill auto-generates kebab-case names from titles:

- "Add Feature X" → `add-feature-x`
- "Cache Optimization (Phase 2)" → `cache-optimization-phase-2`
- "Fix Bug: Type Loading" → `fix-bug-type-loading`

Only use `--name` when auto-generation produces poor results.

### Choose Right Template

- **feature**: New functionality, enhancements, additions
- **refactor**: Architectural changes, code cleanup, migrations
- **docs**: Documentation work, guides, API docs

Templates optimize structure for the type of work.

### Link to Design Docs Early

Always use `--implements` when plan relates to design doc:

- Enables bidirectional navigation
- Makes plan discoverable via design-* skills
- Keeps design and implementation synchronized

### Set Realistic Estimates

Use `--estimated-effort` to track planning accuracy:

- Compare estimated vs actual when done
- Improve future estimates
- Identify scope creep

### Validate Immediately

Always validate after creation:

```bash
/plan-create "My Feature" && /plan-validate my-feature
```

Catches issues early before committing.

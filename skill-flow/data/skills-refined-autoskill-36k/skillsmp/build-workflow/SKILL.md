---
name: build-workflow
description: Build Temporal workflows from JSON spec files. Use when (1) a JSON workflow spec file needs to be converted to working Temporal code, (2) implementing a workflow from a designer export, (3) generating workflow code with activities, types, and proper registration. Handles the full pipeline from JSON spec to integrated, type-checked workflow.
---

# Build Workflow

Generate complete Temporal workflow implementations from JSON specification files using the CLI code generator and codebase patterns.

## Quick Start

```bash
# 1. Transform designer export (if needed)
python ~/.claude/skills/build-workflow/scripts/transform-spec.py designer-export.json transformed.json

# 2. Generate workflow code
pnpm --filter @repo/temporal generate transformed.json --name my-workflow

# 3. Register in Temporal (workflows/index.ts, workers/worker.ts)

# 4. Type check Temporal
pnpm --filter @repo/temporal typecheck

# 5. Add UI (definition, form, detail view, registry, route)

# 6. Type check UI
pnpm --filter @repo/ui typecheck
```

## Workflow

### Step 1: Transform Designer Export

The workflow designer exports a different format than the generator expects. **Run** the transform script (do not read it):

```bash
python ~/.claude/skills/build-workflow/scripts/transform-spec.py <input.json> <output.json>
```

**Designer export format:**
```json
{
  "metadata": { "title": "My Workflow" },
  "nodes": [{ "id", "type", "label", "config", "position" }]
}
```

**Generator expected format:**
```json
{
  "name": "my-workflow",
  "nodes": [{ "id", "type", "position", "data": { "label", "config" } }]
}
```

**Key transformations:**
- `metadata.title` → `name` (kebab-cased)
- `node.label`, `node.config` → `node.data.label`, `node.data.config`
- `loop-container` → `loop`

### Step 2: Validate and Preview

Preview generated code before writing:

```bash
pnpm --filter @repo/temporal generate ./transformed.json --dry-run
```

Check for:
- Validation errors (missing nodes, invalid edges)
- Generated file structure
- TODO comments requiring attention

### Step 3: Generate Code

```bash
pnpm --filter @repo/temporal generate ./transformed.json --name my-workflow
```

**Options:**
- `-n, --name <name>` - Workflow name in kebab-case (defaults to spec name)
- `-o, --output <dir>` - Output directory (default: `packages/temporal/use-cases`)
- `--dry-run` - Preview without writing files
- `--skip-typecheck` - Skip TypeScript validation
- `--force` - Overwrite existing directory

**Output structure:**
```
packages/temporal/use-cases/<workflow-name>/
├── workflow.ts           # Main workflow with withWorkflowTracking()
├── types.ts              # TypeScript input/output types
├── activities/
│   └── index.ts          # Activity implementations
└── README.md             # Auto-generated documentation
```

### Step 4: Review Generated Code

Check for TODO comments and verify:

1. **workflow.ts** - Flow logic and data passing
2. **types.ts** - Input/output type definitions
3. **activities/index.ts** - Activity implementations

See `references/workflow-patterns.md` for expected patterns.

### Step 5: Register Workflow

**Export the workflow** in `packages/temporal/workflows/index.ts`:
```typescript
export * from "../use-cases/<workflow-name>/workflow";
```

**Register activities** in `packages/temporal/workers/worker.ts`:
```typescript
import * as myWorkflowActivities from "../use-cases/<workflow-name>/activities/index";

// In Worker.create() activities:
activities: {
  ...existingActivities,
  ...myWorkflowActivities,
}
```

See `references/post-generation.md` for detailed integration steps.

### Step 6: Type Check Temporal

```bash
pnpm --filter @repo/temporal typecheck
```

### Step 7: UI Integration

Integrate the workflow into the Next.js UI. See `references/ui-integration.md` for detailed patterns.

**7.1 Add Workflow Definition** in `packages/ui/src/lib/workflow-definitions.ts`:
```typescript
{
  slug: "<workflow-slug>",              // URL: /start/{slug}
  workflowType: "<workflowType>",       // camelCase, matches API
  title: "<Title>",
  description: "<Description>",
  command: "<workflow-slug>",
  requiresHumanInLoop: false,
}
```

**7.2 Create Form Component** at `packages/ui/src/components/<WorkflowName>Form.tsx`
- Use `AIGreetingBasicForm.tsx` as template
- POST to `/api/workflows/start` with `workflowType`, `workflowName`, `workflowArgs`

**7.3 Create Detail View** at `packages/ui/src/workflows/<workflow-slug>/<WorkflowName>Workflow.tsx`
- Implement `WorkflowComponentProps` interface
- Handle both kanban and detail views
- Use `AIGreetingBasicWorkflow.tsx` as template

**7.4 Register in UI:**
- Add to `WORKFLOW_REGISTRY` in `packages/ui/src/workflows/registry.ts`
- Import form, add to `SLUG_TO_META`, add switch case in `packages/ui/src/app/start/[slug]/page.tsx`

**7.5 Type Check UI:**
```bash
pnpm --filter @repo/ui typecheck
```

## Spec Format Reference

See `references/spec-format.md` for full schema details.

**Supported node types:**
| Designer Type | Generator Type | Description |
|--------------|----------------|-------------|
| `start` | `start` | Entry point |
| `end` | `end` | Exit point |
| `condition` | `condition` | Branching |
| `loop-container` | `loop` | Iteration |
| `http-request` | `http-request` | API calls |
| `ai-generate-text` | `ai-generate-text` | AI text |
| `ai-generate-object` | `ai-generate-object` | AI structured |
| `data-transform` | `data-transform` | JSONata |
| `data-validate` | `data-validate` | JSON Schema |
| `human-approval` | `human-approval` | HITL |

## Workflow Patterns

See `references/workflow-patterns.md` for:
- `withWorkflowTracking` wrapper usage
- Activity configuration and timeouts
- Primitive activities (HTTP, AI, data, human)
- Signals and queries for human-in-the-loop
- Database synchronization patterns

## Troubleshooting

**"Cannot read properties of undefined (reading 'replace')"**
- Spec missing `name` field - run transform script first or provide `--name` option

**"Spec file not found"** - Verify the file path is correct

**"Validation failed"** - Check for:
- Missing start or end nodes
- Disconnected nodes
- Invalid node types (e.g., `loop-container` instead of `loop`)
- Condition nodes without true/false edges

**"Directory already exists"** - Use `--force` to overwrite or `--name` for different name

**"Type check failed"** - Use `--skip-typecheck` to generate anyway, then fix manually

**Worker won't find workflow** - Verify exports in `workflows/index.ts` and activities in `worker.ts`

**"Workflow failed: non-deterministic"** - Workflow imports a module that touches database/filesystem. Use `/workflow` subpath for primitives (e.g., `primitives/human/workflow` not `primitives/human`). See `references/workflow-patterns.md` for determinism rules.

# Post-Generation Integration Steps

After running the CLI generator, follow these steps to integrate the workflow.

## Step 1: Review Generated Files

Check the generated directory:

```
packages/temporal/use-cases/<workflow-name>/
├── workflow.ts           # Main workflow logic
├── types.ts              # TypeScript types
├── activities/
│   └── index.ts          # Activity implementations
└── README.md             # Auto-generated docs
```

**Review checklist:**
- [ ] `workflow.ts` - Verify flow logic and variable passing
- [ ] `types.ts` - Ensure types match expected I/O
- [ ] `activities/index.ts` - Check activity implementations
- [ ] Look for `// TODO` comments requiring manual attention

## Step 2: Export the Workflow

Edit `packages/temporal/workflows/index.ts`:

```typescript
// Add this line
export * from "../use-cases/<workflow-name>/workflow";
```

**Example:**
```typescript
// Existing exports
export * from "../use-cases/ai-greeting-basic/workflow";
export * from "../use-cases/approval-request/workflow";

// Your new workflow
export * from "../use-cases/customer-sync/workflow";
```

## Step 3: Register Activities in Worker

Edit `packages/temporal/workers/worker.ts`:

### Import Activities

Add import near the top with other use-case imports:

```typescript
// ... existing imports
import * as customerSyncActivities from "../use-cases/customer-sync/activities/index";
```

### Register in Worker.create()

Add to the activities spread in the `Worker.create()` call:

```typescript
const worker = await Worker.create({
  connection,
  namespace: TEMPORAL_NAMESPACE,
  taskQueue: TEMPORAL_TASK_QUEUE,
  workflowsPath: require.resolve("../workflows"),
  activities: {
    // ... existing activities
    ...customerSyncActivities,  // Add this line
  },
});
```

## Step 4: Run Type Check

Verify no TypeScript errors:

```bash
pnpm --filter @repo/temporal typecheck
```

Fix any type errors before proceeding.

## Step 5: Test the Workflow (Optional)

### Start the Worker

```bash
pnpm worker
```

### Trigger via API

```bash
curl -X POST http://localhost:3000/api/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "workflowType": "customerSync",
    "workflowName": "customerSyncWorkflow",
    "workflowArgs": [{ "workflowId": "test-123", "userId": "user-1" }],
    "userId": "default-user"
  }'
```

### Monitor Execution

- **Temporal Cloud UI**: https://cloud.temporal.io - View event history and signals
- **Next.js UI**: http://localhost:3000 - View workflow status
- **SQLite Database**: `./data/workflows.db` - Query directly

## Common Issues

### "Workflow function not found"
- Ensure workflow is exported in `workflows/index.ts`
- Check the export path matches the file structure
- Restart the worker after changes

### "Activity not registered"
- Ensure activities are imported in `worker.ts`
- Verify the spread operator includes the new activities
- Check activity names match between workflow and registration

### Type errors
- Verify `types.ts` exports match imports in workflow
- Check activity return types match expected types
- Use `--skip-typecheck` flag temporarily to see generated code

### Worker connection issues
- Verify Temporal Cloud credentials in `.env`
- Check mTLS certificates are valid
- Ensure `TEMPORAL_ADDRESS` is correct

## Full Example

For a workflow named `customer-sync`:

1. **Generate:**
   ```bash
   pnpm --filter @repo/temporal generate ./customer-sync.json --name customer-sync
   ```

2. **Export workflow** (`workflows/index.ts`):
   ```typescript
   export * from "../use-cases/customer-sync/workflow";
   ```

3. **Register activities** (`workers/worker.ts`):
   ```typescript
   import * as customerSyncActivities from "../use-cases/customer-sync/activities/index";

   // In Worker.create():
   activities: {
     ...existingActivities,
     ...customerSyncActivities,
   }
   ```

4. **Type check:**
   ```bash
   pnpm --filter @repo/temporal typecheck
   ```

5. **Test:**
   ```bash
   pnpm worker  # In one terminal
   # Trigger via UI or API
   ```

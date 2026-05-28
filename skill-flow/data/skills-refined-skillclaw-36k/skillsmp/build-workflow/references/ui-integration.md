# UI Integration Patterns

After generating the Temporal workflow, integrate it into the Next.js UI.

## Key Files

| Purpose | File Path |
|---------|-----------|
| Workflow definitions | `packages/ui/src/lib/workflow-definitions.ts` |
| Form template | `packages/ui/src/components/AIGreetingBasicForm.tsx` |
| Detail view template | `packages/ui/src/workflows/ai-greeting-basic/AIGreetingBasicWorkflow.tsx` |
| Registry | `packages/ui/src/workflows/registry.ts` |
| Route page | `packages/ui/src/app/start/[slug]/page.tsx` |

## Step 1: Workflow Definition

Add entry to `WORKFLOW_DEFINITIONS` array in `packages/ui/src/lib/workflow-definitions.ts`:

```typescript
{
  slug: "my-posts-workflow",           // URL slug for /start/{slug}
  workflowType: "myPostsWorkflow",     // Must match what's sent to /api/workflows/start
  title: "My Posts Workflow",
  description: "Fetches posts from an API, validates them, and generates AI summaries",
  command: "my-posts-workflow",
  requiresHumanInLoop: false,          // true if workflow uses human-approval nodes
}
```

**Naming conventions:**
- `slug`: kebab-case, used in URLs
- `workflowType`: camelCase, matches database and API
- `command`: kebab-case, same as slug

## Step 2: Form Component

Create `packages/ui/src/components/<WorkflowName>Form.tsx`.

**Template structure:**
```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function MyPostsWorkflowForm() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Add form state fields as needed

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const workflowId = `my-posts-workflow-${Date.now()}`;

    try {
      const response = await fetch("/api/workflows/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflowType: "myPostsWorkflow",           // Must match definition
          workflowName: "myPostsWorkflowWorkflow",   // Temporal function name
          workflowArgs: [{
            workflowId,
            // Add other input fields from form state
          }],
          userId: "default-user",
        }),
      });

      if (!response.ok) throw new Error("Failed to start workflow");

      router.push(`/workflow/${workflowId}`);
    } catch (error) {
      console.error("Error starting workflow:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Posts Workflow</CardTitle>
        <CardDescription>
          Fetches posts and generates AI summaries
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Add form fields here */}
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Starting..." : "Start Workflow"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
```

**Important:**
- `workflowType` must match the definition in `workflow-definitions.ts`
- `workflowName` must match the exported Temporal function name (usually `<camelCase>Workflow`)
- `workflowArgs` is an array with the input object as first element
- `workflowId` must be included in the args

## Step 3: Detail View Component

Create `packages/ui/src/workflows/<workflow-slug>/<WorkflowName>Workflow.tsx`.

**Template structure:**
```typescript
"use client";

import { WorkflowComponentProps } from "../types";
import { KanbanCardFrame } from "@/components/KanbanCardFrame";
import { WorkflowDetailLayout } from "@/components/WorkflowDetailLayout";

export function MyPostsWorkflowWorkflow({ workflow, view }: WorkflowComponentProps) {
  // Parse the result if available
  const result = workflow.result as {
    // Define expected result shape
  } | null;

  // Kanban view (compact card)
  if (view === "kanban") {
    return (
      <KanbanCardFrame workflow={workflow}>
        <div className="text-sm text-muted-foreground">
          {result ? "Completed" : "Processing..."}
        </div>
      </KanbanCardFrame>
    );
  }

  // Detail view (full page)
  return (
    <WorkflowDetailLayout workflow={workflow}>
      <div className="space-y-4">
        {result ? (
          <div>
            {/* Render result data */}
            <pre className="bg-muted p-4 rounded text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        ) : (
          <div className="text-muted-foreground">
            Workflow is {workflow.status}...
          </div>
        )}
      </div>
    </WorkflowDetailLayout>
  );
}
```

**Key interfaces:**
```typescript
interface WorkflowComponentProps {
  workflow: WorkflowExecution;  // From database
  view?: "kanban" | "detail";   // Rendering context
}
```

## Step 4: Registry Entry

Edit `packages/ui/src/workflows/registry.ts`:

```typescript
// Add import
import { MyPostsWorkflowWorkflow } from "./my-posts-workflow/MyPostsWorkflowWorkflow";

// Add to WORKFLOW_REGISTRY object
export const WORKFLOW_REGISTRY: Record<string, React.ComponentType<WorkflowComponentProps>> = {
  // ... existing entries
  "myPostsWorkflow": MyPostsWorkflowWorkflow,
};
```

**Key:** Must match `workflowType` from the definition.

## Step 5: Route Page Updates

Edit `packages/ui/src/app/start/[slug]/page.tsx`:

### 5.1 Import the form
```typescript
import { MyPostsWorkflowForm } from "@/components/MyPostsWorkflowForm";
```

### 5.2 Add to SLUG_TO_META
```typescript
const SLUG_TO_META: Record<string, { title: string; description: string; workflowType: string }> = {
  // ... existing entries
  "my-posts-workflow": {
    title: "My Posts Workflow",
    description: "Fetches posts and generates AI summaries",
    workflowType: "myPostsWorkflow",
  },
};
```

### 5.3 Add case in renderWorkflowForm()
```typescript
function renderWorkflowForm(slug: string) {
  switch (slug) {
    // ... existing cases
    case "my-posts-workflow":
      return (
        <>
          <MyPostsWorkflowForm />
          <Separator className="my-8" />
          <WorkflowExecutionsList
            status="completed"
            workflowType="myPostsWorkflow"
            title="My Posts Workflow History"
          />
        </>
      );
    default:
      return null;
  }
}
```

## Naming Reference

| Concept | Format | Example |
|---------|--------|---------|
| URL slug | kebab-case | `my-posts-workflow` |
| workflowType | camelCase | `myPostsWorkflow` |
| Temporal function | camelCase + Workflow | `myPostsWorkflowWorkflow` |
| Form component | PascalCase + Form | `MyPostsWorkflowForm` |
| Detail component | PascalCase + Workflow | `MyPostsWorkflowWorkflow` |
| Directory | kebab-case | `my-posts-workflow/` |

## Type Check

After all UI changes:

```bash
pnpm --filter @repo/ui typecheck
```

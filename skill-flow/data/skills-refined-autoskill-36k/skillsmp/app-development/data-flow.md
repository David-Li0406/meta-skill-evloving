# Data Flow Skill

This skill provides comprehensive patterns for backend operations, API development, database interactions, authentication, and state management.

## Purpose

Use this skill when:
- Implementing server actions
- Working with MongoDB/Mongoose
- Setting up React Query hooks
- Handling authentication with Clerk
- Implementing error handling
- Building API endpoints
- Managing data transformations
- Integrating with external APIs (Monday.com)

## Core Documentation

### Backend Patterns

@data-flow/server-actions.md - Server action implementation patterns
@data-flow/api-patterns.md - API design and best practices
@data-flow/error-handling.md - Standardized error handling

### Database & Schemas

@data-flow/mongodb-integration.md - MongoDB Atlas and Mongoose patterns
@data-flow/schema-system.md - Dual schema system (Zod + Mongoose)
@data-flow/transformation-system.md - Data transformation patterns
@data-flow/type-system.md - TypeScript type patterns

### State Management

@data-flow/react-query-patterns.md - React Query setup and usage
@data-flow/authentication.md - Clerk authentication integration

### External Integrations

@data-flow/monday-integration.md - Monday.com API integration

## Server Actions Pattern

All server actions follow this standardized pattern:

```typescript
"use server";

import { withDbConnection } from "@server/withDbConnection";
import { handleServerError } from "@error/handleServerError";
import { MyInputSchema } from "@zod-schema/my-input";
import { MyModel } from "@mongoose-schema/my-model";

export async function myAction(input: MyInputType) {
  return withDbConnection(async () => {
    try {
      // 1. Validate input with Zod
      const validated = MyInputSchema.parse(input);

      // 2. Database operations
      const result = await MyModel.findOne({ ... });

      // 3. Return standardized response
      return {
        success: true,
        data: result.toJSON() // Always serialize Mongoose docs
      };
    } catch (error) {
      return {
        success: false,
        error: handleServerError(error, "Operation failed")
      };
    }
  });
}
```

## MongoDB Patterns

### Connection Management

Always use `withDbConnection` wrapper:

```typescript
import { withDbConnection } from "@server/withDbConnection";

export async function getData() {
  return withDbConnection(async () => {
    // Your database operations here
  });
}
```

### Using mongosh CLI

This project uses MongoDB Atlas. Connection string is in `.env.local` as `DATABASE_URL`.

**Always use the environment variable instead of hardcoding credentials.**

Common mongosh patterns:

```bash
# Find documents
mongosh "$DATABASE_URL" --eval "
db['collection-name'].find({ field: 'value' }).forEach(printjson);
"

# Count documents
mongosh "$DATABASE_URL" --eval "
print('Total:', db['collection-name'].countDocuments());
"

# Update documents
mongosh "$DATABASE_URL" --eval "
db['collection-name'].updateOne(
  { _id: ObjectId('...') },
  { \$set: { field: 'value' } }
);
"

# Aggregation
mongosh "$DATABASE_URL" --eval "
db['collection-name'].aggregate([
  { \$group: { _id: '\$field', count: { \$sum: 1 } } }
]).forEach(printjson);
"
```

### Schema System

**Dual Schema Pattern**:
1. **Zod Schemas** (`@zod-schema/*`) - Validation and TypeScript types
2. **Mongoose Schemas** (`@mongoose-schema/*`) - Database models

Keep both in sync manually. No automatic generation.

Key differences:
- Mongoose uses `_id` (ObjectId)
- Transforms add `id` field for client use
- Always use `.toJSON()` when returning to client

### Mongoose Model Export Pattern (IMPORTANT)

**Always use the conditional export pattern for Mongoose models:**

```typescript
// ✅ CORRECT - Required for CRUD factory compatibility
export const MyModel = mongoose.models.MyModel ||
  mongoose.model("MyModel", MySchema);

// ❌ WRONG - Causes TypeScript errors with CRUD factory
if (mongoose.models.MyModel) {
  delete mongoose.models.MyModel;
}
export const MyModel = mongoose.model("MyModel", MySchema);
```

**Why this matters:**
- The `||` pattern allows TypeScript to infer the cached model type from `mongoose.models`
- This satisfies the `Model<Document>` constraint required by `createCrudActions`
- The delete pattern creates a raw schema type that doesn't match the CRUD factory's type constraints
- Both patterns work at runtime, but only the `||` pattern has correct TypeScript inference

## React Query Patterns

### SCM Hooks Organization

All SCM (School Coaching Manager) hooks are centralized in `src/hooks/scm/`:

```
hooks/scm/
├── index.ts                    # Main export hub - import from here
├── podsie/                     # Velocity tracking & sections
│   ├── useSectionOptions.ts    # Section configs with colors
│   ├── useDaysOff.ts           # School calendar days off
│   ├── useCurrentUnits.ts      # Current unit by section
│   ├── useVelocityData.ts      # Daily velocity stats
│   └── useWeeklyVelocity.ts    # Weekly aggregated data
├── roadmaps/                   # Curriculum & assessments
│   ├── useRoadmapUnits.ts      # Roadmap unit data
│   ├── useRoadmapData.ts       # Section roadmap completions
│   ├── useAllSkills.ts         # All roadmap skills (dropdowns)
│   ├── useFilteredSkills.ts    # Skills by grade/unit
│   ├── useAssessmentData.ts    # Student assessments
│   ├── useZearnCompletions.ts  # Zearn completion history
│   ├── usePodsieCompletions.ts # Podsie completion history
│   └── useStudentsBySection.ts # Students grouped by section
├── scope-and-sequence/         # Curriculum planning
│   ├── queries.ts              # Read operations
│   └── mutations.ts            # Create/update/delete
└── utils/                      # Shared utilities
    ├── colors.ts               # Section color palettes
    └── unitColors.ts           # Unit color palettes
```

**Usage:**
```typescript
// Import from the main hub
import {
  useSectionOptions,
  useRoadmapUnits,
  useScopeSequenceList,
  getSectionColors,
} from "@/hooks/scm";
```

**Key hooks:**
- `useSectionOptions()` - Returns section configs, colors, sections by school
- `useVelocityData(sections, options, schoolYear, includeNotTracked)` - Multi-section velocity
- `useRoadmapData(selectedSections)` - Roadmap completions for sections
- `useScopeSequenceList({ grade, unitNumber })` - Scope & sequence entries

### Query Hook Pattern

```typescript
import { useQuery } from "@tanstack/react-query";
import { fetchData } from "@actions/fetch-data";

export function useDataQuery(params: Params) {
  return useQuery({
    queryKey: ["data", params],
    queryFn: () => fetchData(params),
  });
}
```

### Mutation Hook Pattern

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateData } from "@actions/update-data";

export function useUpdateDataMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateData,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["data"] });
    },
  });
}
```

## Authentication with Clerk

```typescript
import { auth, currentUser } from "@clerk/nextjs/server";

// In server actions
export async function myAction() {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Unauthorized" };
  }

  // Use userId for operations
}

// Get full user object
export async function getUser() {
  const user = await currentUser();
  // Access user.emailAddresses, user.firstName, etc.
}
```

## Error Handling

Use standardized error handling:

```typescript
import { handleServerError } from "@error/handleServerError";

try {
  // Operations
} catch (error) {
  return {
    success: false,
    error: handleServerError(error, "User-friendly message")
  };
}
```

## Data Transformation

Common transformation patterns:

```typescript
// Mongoose to JSON (client-safe)
const clientData = mongooseDoc.toJSON();

// Array transformations
const transformed = items.map(item => ({
  ...item.toJSON(),
  computed: calculateValue(item)
}));

// Type-safe transformations with Zod
const validated = MySchema.parse(rawData);
```

## Important Notes

### Database Collections

- **`students`** - Student records with `studentID` (number)
- **`roadmaps-student-data`** - Assessment data with `studentId` (string slug)
  - ⚠️ **Known Issue**: ID format mismatch between collections
- **`activity-type-configs`** - Incentive activity types (max 10)

### Common Pitfalls

1. **ID Format Mismatches** - Some use numeric IDs, others use string slugs
2. **Mongoose Model Export** - Always use `mongoose.models.X || mongoose.model(...)` pattern (see above)
3. **Index Conflicts** - Drop old indexes manually after schema changes
4. **Timezone Issues** - Use local timezone for dates in forms

### Security

- Always validate input with Zod
- Use Clerk for authentication
- Avoid `any` types - use proper TypeScript types
- Never expose sensitive data in client responses
- Watch for SQL injection patterns (even in NoSQL)

## Integration with Other Skills

- For overall architecture → Use `architecture` skill
- For UI components → Use `component-system` skill
- For implementation workflows → Use `workflows` skill

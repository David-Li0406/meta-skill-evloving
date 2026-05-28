# Common Development Tasks

Step-by-step guides for frequent operations.

## Database Operations

### Query with mongosh
```bash
mongosh "$DATABASE_URL" --eval "
db['collection-name'].find({}).forEach(printjson);
"
```

### Update Schema

1. **Update Zod schema** in `src/lib/schema/zod-schema/`
2. **Update Mongoose schema** in `src/lib/schema/mongoose-schema/`
3. **Clear model cache** (if in dev): `delete mongoose.models.ModelName`
4. **Check for index conflicts** - old indexes may persist
5. **Test with sample data**

### Add New Index
```bash
mongosh "$DATABASE_URL" --eval "
db['collection-name'].createIndex({ field: 1 });
"
```

### Drop Old Index
```bash
mongosh "$DATABASE_URL" --eval "
db['collection-name'].dropIndex('index_name');
"
```

## Managing Breaking Changes

### Step 1: Identify Breaking Changes
- Schema field removals/renames
- API signature changes
- Component prop changes
- Database structure changes

### Step 2: Backwards Compatible Migration

Add new fields alongside old:
```typescript
// Mongoose schema - support both during migration
const schema = new mongoose.Schema({
  oldField: String,  // Deprecated
  newField: String,  // New
});
```

### Step 3: Data Migration Script
```bash
mongosh "$DATABASE_URL" --eval "
db['collection'].updateMany(
  { oldField: { \$exists: true }, newField: { \$exists: false } },
  [{ \$set: { newField: '\$oldField' } }]
);
"
```

### Step 4: Update All References
- Search codebase: `grep -r "oldField" src/`
- Update imports
- Update types
- Test thoroughly

### Step 5: Clean Up
- Remove deprecated code
- Update documentation
- Drop old database indexes
- Remove old fields from schema

## Adding a New Page

### Step 1: Create Page File
```typescript
// src/app/my-page/page.tsx
import { MyPageContent } from "./components/MyPageContent";

export default function MyPage() {
  return <MyPageContent />;
}
```

### Step 2: Create Page Components
```typescript
// src/app/my-page/components/MyPageContent.tsx
"use client";

export function MyPageContent() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">My Page</h1>
    </div>
  );
}
```

### Step 3: Add Navigation (if needed)
Update sidebar or navigation components to include link to new page.

## Adding a New Server Action

### Step 1: Create Action File
```typescript
// src/app/actions/my-domain/my-action.ts
"use server";

import { withDbConnection } from "@server/withDbConnection";
import { handleServerError } from "@/lib/utils/error-utils";

export async function myAction(input: MyInputType) {
  return withDbConnection(async () => {
    try {
      // Validate input
      const validated = MyInputSchema.parse(input);

      // Perform operation
      const result = await Model.create(validated);

      return { success: true, data: result.toJSON() };
    } catch (error) {
      return { success: false, error: handleServerError(error, "Action failed") };
    }
  });
}
```

### Step 2: Create React Query Mutation (if needed)
```typescript
// src/query/my-domain/useMyMutation.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { myAction } from "@actions/my-domain/my-action";

export function useMyMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: myAction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["myDomain"] });
    },
  });
}
```

## Debugging Tips

### Check Server Action Response
```typescript
const result = await myAction(input);
console.log("Action result:", JSON.stringify(result, null, 2));
```

### Check Database State
```bash
mongosh "$DATABASE_URL" --eval "
db['collection'].findOne({ _id: ObjectId('...') });
"
```

### Check React Query Cache
Use React Query DevTools (included in dev mode) to inspect cache state.

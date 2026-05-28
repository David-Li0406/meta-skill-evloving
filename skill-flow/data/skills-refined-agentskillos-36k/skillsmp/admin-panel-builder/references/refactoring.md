# Admin Panel Refactoring Guide

## Splitting One Page into Two

When a page becomes too large or has distinct functionality, split it.

### Step 1: Identify Split Points

Look for:
- Distinct tab groups that could be separate pages
- Independent functionality that doesn't share state
- Managers that are conceptually different domains

### Step 2: Create New Page File

```tsx
// src/pages/AdminNewFeaturePage.tsx

import { useUserRole } from "@shared-auth/hooks/useUserRole";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import AdminHeader from "@/components/admin/AdminHeader";
import { FeatureIcon } from "lucide-react";
import { ExistingManager } from "@/components/admin/ExistingManager";

const AdminNewFeaturePage = () => {
  const { isAdmin } = useUserRole();

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground">No permission</p>
      </div>
    );
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar onNavigateToContinueAudio={() => {}} onNavigateToContinueText={() => {}} />
        <main className="flex-1 overflow-auto">
          <AdminHeader
            title="New Feature"
            icon={<FeatureIcon className="h-6 w-6 text-primary" />}
          />
          <div className="p-6">
            <div className="max-w-6xl mx-auto space-y-8">
              <ExistingManager />
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default AdminNewFeaturePage;
```

### Step 3: Add Route in App.tsx

```tsx
// Add import
import AdminNewFeaturePage from "./pages/AdminNewFeaturePage";

// Add route (alphabetical order)
<Route path="/admin/new-feature" element={<AdminNewFeaturePage />} />
```

### Step 4: Add Dashboard Card

In `AdminDashboardPage.tsx`, add to the sections array:

```tsx
{
  title: "New Feature",
  description: "Description of the feature",
  icon: FeatureIcon,
  path: "/admin/new-feature",
  stats: [{ label: "items", value: count }],
},
```

### Step 5: Remove from Original Page

1. Remove the tab from the original page's TabsList
2. Remove the TabsContent for the moved section
3. Remove unused imports

### Step 6: Update Original Page Stats Query

If stats were shared, split them:

```tsx
// Before: One query for all stats
const { data: stats } = useQuery({
  queryKey: ['all-stats'],
  queryFn: async () => {
    // Returns multiple stats
  }
});

// After: Separate query for remaining stats
const { data: remainingStats } = useQuery({
  queryKey: ['remaining-stats'],
  queryFn: async () => {
    // Only remaining stats
  }
});
```

## Moving Manager Components

If moving a manager to a new page, check for:

1. **Shared state** - Extract to shared hooks if needed
2. **Query keys** - Keep unique across pages
3. **Imports** - Update paths if component moves directories

## Example: Splitting AdminAIPage

Current tabs: Usage, Prompts, Features, Pricing, Quotas, Feedback, Test

Could split into:
- **AdminAIPage** - Core AI (Usage, Features, Quotas)
- **AdminAIPromptsPage** - Prompt management (Prompts, Test)
- **AdminAIPricingPage** - Billing (Pricing, Feedback)

### File changes needed:

1. Create `AdminAIPromptsPage.tsx` with Prompts + Test tabs
2. Create `AdminAIPricingPage.tsx` with Pricing + Feedback tabs
3. Update `AdminAIPage.tsx` to keep only Usage, Features, Quotas
4. Add routes in `App.tsx`
5. Add dashboard cards in `AdminDashboardPage.tsx`

## Renaming Pages

1. Rename file: `AdminOldName.tsx` → `AdminNewName.tsx`
2. Update import in `App.tsx`
3. Update route path if needed
4. Update dashboard card path
5. Search for any other references: `grep -r "AdminOldName" src/`

## Common Refactoring Patterns

### Extract Shared Logic to Hook

```tsx
// Before: Logic in multiple pages
const [data, setData] = useState([]);
useEffect(() => { /* fetch logic */ }, []);

// After: Shared hook
// src/hooks/useFeatureData.ts
export function useFeatureData() {
  const { data, isLoading } = useQuery({...});
  return { data, isLoading };
}
```

### Extract Stats Queries

```tsx
// src/hooks/admin/useAdminStats.ts
export function useAdminStats(section: string) {
  return useQuery({
    queryKey: ['admin-stats', section],
    queryFn: async () => {
      // Section-specific stats
    }
  });
}
```

---
name: admin-panel-builder
description: Use this skill when creating and maintaining admin panel pages in the KR92 Bible Voice project, including building components, integrating navigation, and adding features.
---

# Admin Panel Builder

## Context Files (Read First)

For structure and conventions, read from `Docs/context/`:
- `Docs/context/repo-structure.md` - File locations
- `Docs/context/conventions.md` - Naming and patterns

## Quick Reference

### File Locations
```
src/pages/Admin*.tsx           # Admin page components
src/components/admin/*.tsx     # Manager components
src/components/admin/tokens/   # Token-specific components
App.tsx                        # Route definitions
```

### Current Admin Pages

| Page | Path | Purpose |
|------|------|---------|
| Dashboard | `/admin` | Overview with section cards |
| AI | `/admin/ai` | Prompts, pricing, quotas, features (6 tabs) |
| Audio | `/admin/audio` | TTS voices, version config (2 tabs) |
| Auth Tokens | `/admin/auth-tokens` | API key management (collapsible sections) |
| Cinema | `/admin/cinema` | Background visuals, music (2 tabs) |
| Reading Plans | `/admin/reading-plans` | Bible reading plans |
| Subscriptions | `/admin/subscriptions` | Plans, feature limits |
| Testing & Demos | `/admin/testing` | Component test pages |
| Topics | `/admin/topics` | Topic suggestions, QA issues |
| Translations | `/admin/translations` | Term translation cache |
| Users | `/admin/users` | User management, history (3 tabs) |
| Video | `/admin/video` | Video series/clips |
| Widget Analytics | `/admin/widget-analytics` | Embed usage stats |

## Creating New Admin Page

### Step 1: Create Page Component

```tsx
// src/pages/AdminNewFeaturePage.tsx

import { useUserRole } from "@shared-auth/hooks/useUserRole";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import AdminHeader from "@/components/admin/AdminHeader";
import { FeatureIcon } from "lucide-react";

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
              {/* Content here */}
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default AdminNewFeaturePage;
```

### Step 2: Add Route

In `App.tsx`:
```tsx
import AdminNewFeaturePage from "./pages/AdminNewFeaturePage";

// In routes section:
<Route path="/admin/new-feature" element={<AdminNewFeaturePage />} />
```

### Step 3: Add Dashboard Card

In `AdminDashboardPage.tsx`, add to sections array:
```tsx
{
  title: "New Feature",
  description: "Description",
  icon: FeatureIcon,
  path: "/admin/new-feature",
}
```

## Splitting Pages (Refactoring)

When a page has too many tabs or distinct functionality:

1. **Create new page file** with subset of managers
2. **Add route** in App.tsx
3. **Add dashboard card** for new page
4. **Remove tabs** from original page
5. **Update imports** - remove unused managers

## Essential Patterns

### Role Check
```tsx
const { isAdmin } = useUserRole();
if (!isAdmin) return <NoPermission />;
```

### Data Query
```tsx
const { data, isLoading } = useQuery({
  queryKey: ['feature'],
  queryFn: async () => {
    const { data, error } = await supabase.from('table').select('*');
    if (error) throw error;
    return data;
  },
});
```

### Mutation with Toast
```tsx
const mutation = useMutation({
  mutationFn: async (id: string) => {
    const { error } = await supabase.from('table').delete().eq('id', id);
    if (error) throw error;
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['feature'] });
    toast({ title: "Success" });
  },
  onError: (error: Error) => {
    toast({ title: "Error", description: error.message, variant: "destructive" });
  },
});
```

## Best Practices

1. **Access Control**: Always check `isAdmin` from `useUserRole()`.
2. **Toast Notifications**: Use `toast` from "sonner" for success and error messages.
3. **Data Fetching**: Use React Query (`useQuery`, `useMutation`) and handle loading states.
4. **Layout & Styling**: Use consistent layout patterns with `SidebarProvider`, `AppSidebar`, and `AdminHeader`.
5. **Finnish UI Text**: Ensure user-facing text is in Finnish.

## Common UI Components

| Component | Import Path | Use For |
|-----------|-------------|---------|
| Card | @ui/card | Section containers |
| Tabs | @ui/tabs | Multi-section pages |
| Table | @ui/table | Data lists |
| Form | @ui/form | Input forms with validation |
| Button | @ui/button | Actions |
| Badge | @ui/badge | Status indicators |
| Input | @ui/input | Text inputs |
| Switch | @ui/switch | Boolean toggles |

## Related Files

### Key Admin Files
- `apps/raamattu-nyt/src/pages/AdminDashboardPage.tsx` - Dashboard hub
- `apps/raamattu-nyt/src/pages/AdminAuthTokensPage.tsx` - Token management example
- `apps/raamattu-nyt/src/components/admin/AdminHeader.tsx` - Header component
- `apps/raamattu-nyt/src/App.tsx` - Route definitions

### Documentation
- `Docs/07-ADMIN-GUIDE.md` - Admin features overview
- `Docs/12-AUTHENTICATION.md` - Auth system details
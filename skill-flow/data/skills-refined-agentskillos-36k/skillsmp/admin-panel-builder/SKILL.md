---
name: admin-panel-builder
description: Expert assistant for creating and maintaining admin panel pages in the KR92 Bible Voice project. Use when creating admin pages, building admin components, integrating with admin navigation, or adding admin features. Also use for refactoring admin pages (splitting one page into multiple, extracting components, reorganizing tabs).
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
App.tsx                        # Route definitions (lines 71-81)
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

**For detailed page structure** (tabs, sections, components): See [references/admin-panel-structure.md](references/admin-panel-structure.md)

## Creating New Admin Page

### 1. Create Page File

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

### 2. Add Route

In `App.tsx`:
```tsx
import AdminNewFeaturePage from "./pages/AdminNewFeaturePage";

// In routes section:
<Route path="/admin/new-feature" element={<AdminNewFeaturePage />} />
```

### 3. Add Dashboard Card

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

See [references/refactoring.md](references/refactoring.md) for detailed steps.

## AdminHeader Props

```tsx
<AdminHeader
  title="Page Title"
  description="Optional subtitle"
  icon={<Icon className="h-6 w-6 text-primary" />}
  showBackButton={true}   // Shows back arrow to /admin
  showSidebarTrigger={true}
/>
```

## Tab Structure Pattern

```tsx
<Tabs defaultValue="first" className="space-y-4">
  <TabsList>
    <TabsTrigger value="first">First Tab</TabsTrigger>
    <TabsTrigger value="second">Second Tab</TabsTrigger>
  </TabsList>
  <TabsContent value="first">
    <Card>
      <CardHeader><CardTitle>Section</CardTitle></CardHeader>
      <CardContent><ManagerComponent /></CardContent>
    </Card>
  </TabsContent>
</Tabs>
```

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

## References

- **Admin panel structure**: See [references/admin-panel-structure.md](references/admin-panel-structure.md) - Complete mapping of pages, tabs, sections, manager components
- **Page structure & layout**: See [references/structure.md](references/structure.md)
- **Refactoring guide**: See [references/refactoring.md](references/refactoring.md)
- **Component patterns**: See [references/components.md](references/components.md)

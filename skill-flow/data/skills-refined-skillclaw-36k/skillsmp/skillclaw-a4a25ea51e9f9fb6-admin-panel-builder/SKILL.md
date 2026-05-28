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
| AI | `/admin/ai` | Prompts, pricing, quotas, features |
| Audio | `/admin/audio` | TTS voices, version config |
| Auth Tokens | `/admin/auth-tokens` | API key management |
| Cinema | `/admin/cinema` | Background visuals, music |
| Reading Plans | `/admin/reading-plans` | Bible reading plans |
| Subscriptions | `/admin/subscriptions` | Plans, feature limits |
| Testing & Demos | `/admin/testing` | Component test pages |
| Topics | `/admin/topics` | Topic suggestions, QA issues |
| Translations | `/admin/translations` | Term translation cache |
| Users | `/admin/users` | User management, history |
| Video | `/admin/video` | Video series/clips |
| Widget Analytics | `/admin/widget-analytics` | Embed usage stats |

## Creating New Admin Page

### 1. Create Page File

```tsx
// src/pages/AdminNewFeaturePage.tsx

import { useUserRole } from "@shared-auth/hooks/useUserRole";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import AdminHeader from "@/components/admin/AdminHeader";

const AdminNewFeaturePage = () => {
  const { isAdmin } = useUserRole();

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-muted-foreground">You do not have permission to access this page.</p>
      </div>
    );
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />
        <main className="flex-1 overflow-auto">
          <AdminHeader title="New Feature" />
          <div className="p-6">
            {/* Content */}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default AdminNewFeaturePage;
```

### 2. Follow Layout and Authentication Patterns

- Use the **SidebarProvider + AppSidebar + AdminHeader** pattern for layout.
- Implement authentication checks using `@shared-auth/hooks/useUserRole`.

### 3. Import Patterns

```typescript
// UI components from @ui aliases
import { Button } from "@ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@ui/tabs";

// Shared auth from @shared-auth
import { useUserRole } from "@shared-auth/hooks/useUserRole";

// Local imports with @/
import AdminHeader from "@/components/admin/AdminHeader";
import { supabase } from "@/integrations/supabase/client";
```
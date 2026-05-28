---
name: Scaffold Module
description: Automatically creates the folder structure for a new dashboard module in ATLAS, following design and architectural standards.
version: 1.0.1
---

# Skill: Scaffold Module for ATLAS

This skill guides the agent to create a new module within the dashboard (`app/(dashboard)/...`).
It ensures consistency in: UI (Shadcn), File Structure, Agent Documentation, and Role-Based Access.

## Execution Steps

### 1. Module Definition
The user must provide (or the agent must infer):
- **Technical Name** (slug, e.g., `inventory-audit`).
- **Display Name** (e.g., "Inventory Audit").
- **Description** (Purpose of the module).
- **Suggested Icon** (from Lucide React).
- **Allowed Roles** (e.g., admin, supervisor, warehouse).

### 2. Folder Structure
Create the directory at `p:\ATLAS\app\(dashboard)\[technical-name]`.

### 3. Main File (`page.tsx`)
Generate `page.tsx` using the base template below.
**Rules**:
- Must use `"use client"`.
- Import UI components from `components/ui`.
- Use `motion.div` for entry animations.
- Include basic role/auth check (`useAuth`).

```typescript
"use client"

import { useAuth } from "@/lib/auth-context"
import { useCompany } from "@/lib/company-context"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"
import { [IconName] } from "lucide-react"

export default function [ModuleName]Page() {
  const { user } = useAuth()
  const { selectedCompany } = useCompany()

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <[IconName] className="h-8 w-8 text-indigo-600" />
            [Display Name]
          </h1>
          <p className="text-slate-500">[Description]</p>
        </div>
        <Button>Main Action</Button>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
      >
        <Card>
          <CardHeader>
            <CardTitle>Main Panel</CardTitle>
          </CardHeader>
          <CardContent>
            Initial content...
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
```

### 4. Agent Documentation (`agents.md`)
AUTOMATICALLY generate the `agents.md` file in the same folder.

```markdown
# Module: [Display Name]

## Description
[Detailed description provided by user]

## Capabilities
- [List proposed initial capabilities]

## Key Files
- `page.tsx`: Main interface.

## Data Dependencies
- **Supabase Tables**: [Likely tables, e.g., inventory, audits]

## Agent Context
- **Permissions**: Restricted to [Allowed Roles].
```

### 5. Registration (Optional)
If it is a core module, suggest adding it to:
1. `components/layout/dashboard-sidebar.tsx` (to appear in the menu).
2. Root `agents.md` (to update the documentation map).

---
name: new-page
description: Scaffold a new page with proper layout, i18n, and shadcn components. Use when creating new pages. Invoke with "/new-page [path] [description]".
model: sonnet
---

# New Page Skill

Create a new Next.js page following the project's established patterns.

## Usage

```
/new-page admin/attendance Attendance management page
/new-page grades/reports Grade reports dashboard
/new-page students/[id]/profile Student profile page
```

## Process

1. **Parse the request** - Extract path and purpose
2. **Create page.tsx** - At `app/ui/app/[path]/page.tsx`
3. **Create loading.tsx** - If data fetching needed
4. **Add i18n keys** - In both en.ts and fr.ts
5. **Import components** - shadcn/ui components as needed

## Page Template (Client Component)

```tsx
"use client"

import { useState, useEffect } from "react"
import { useI18n } from "@/lib/i18n"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Loader2 } from "lucide-react"

type DataItem = {
  id: string
  // Define your data shape
}

export default function PageName() {
  const { t } = useI18n()
  const [data, setData] = useState<DataItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    try {
      setLoading(true)
      const res = await fetch("/api/endpoint")
      if (!res.ok) throw new Error("Failed to fetch")
      const json = await res.json()
      setData(json)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        {error}
      </div>
    )
  }

  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t.section.pageTitle}</h1>
        <Button>{t.common.add}</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{t.section.cardTitle}</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t.common.name}</TableHead>
                <TableHead>{t.common.actions}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.id}</TableCell>
                  <TableCell>
                    <Button variant="ghost" size="sm">
                      {t.common.edit}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
```

## Loading Template

```tsx
// loading.tsx
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

export default function Loading() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-center justify-between">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-10 w-24" />
      </div>

      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-32" />
        </CardHeader>
        <CardContent className="space-y-4">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
        </CardContent>
      </Card>
    </div>
  )
}
```

## i18n Keys Template

```typescript
// Add to en.ts
export const en = {
  // ... existing keys
  newSection: {
    pageTitle: "Page Title",
    cardTitle: "Card Title",
    description: "Description text",
  },
}

// Add to fr.ts
export const fr = {
  // ... existing keys
  newSection: {
    pageTitle: "Titre de la page",
    cardTitle: "Titre de la carte",
    description: "Texte de description",
  },
}
```

## Checklist

Before completing:
- [ ] page.tsx created at correct path
- [ ] loading.tsx created if data fetching
- [ ] i18n keys added to en.ts
- [ ] i18n keys added to fr.ts
- [ ] shadcn/ui components imported correctly
- [ ] Loading state implemented
- [ ] Error state implemented
- [ ] TypeScript types defined
- [ ] Responsive layout (container + spacing)

## Common shadcn/ui Imports

```tsx
// Buttons & Actions
import { Button } from "@/components/ui/button"

// Cards
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"

// Tables
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Forms
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

// Dialogs
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

// Feedback
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"

// Icons (Lucide)
import { Loader2, Plus, Edit, Trash2, Search } from "lucide-react"
```

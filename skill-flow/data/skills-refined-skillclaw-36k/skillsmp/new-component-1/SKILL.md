---
name: new-component
description: Create a new React component following project patterns. Use when creating reusable components. Invoke with "/new-component [name] [description]".
model: sonnet
---

# New Component Skill

Create a new React component following the project's established patterns.

## Usage

```
/new-component StudentCard Card displaying student information
/new-component PaymentForm Form for recording payments
/new-component GradeSelector Dropdown for selecting grade levels
/new-component DataTable Generic data table with sorting
```

## Process

1. **Parse the request** - Extract component name and purpose
2. **Determine location** - `app/ui/components/[name].tsx`
3. **Create component** - With proper TypeScript types
4. **Add i18n keys** - If user-facing text needed
5. **Export properly** - Named export for the component

## Component Template

```tsx
"use client"

import { useState } from "react"
import { useI18n } from "@/lib/i18n"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

// Types
export type ComponentNameProps = {
  /** Required prop description */
  data: DataType
  /** Optional prop with default */
  variant?: "default" | "compact"
  /** Event handler */
  onAction?: (id: string) => void
  /** Additional class names */
  className?: string
}

type DataType = {
  id: string
  name: string
}

/**
 * ComponentName - Brief description of what it does
 *
 * @example
 * <ComponentName
 *   data={{ id: "1", name: "Example" }}
 *   onAction={(id) => console.log(id)}
 * />
 */
export function ComponentName({
  data,
  variant = "default",
  onAction,
  className,
}: ComponentNameProps) {
  const { t } = useI18n()
  const [loading, setLoading] = useState(false)

  const handleAction = async () => {
    if (!onAction) return
    setLoading(true)
    try {
      onAction(data.id)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader>
        <CardTitle>{data.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <Button
          onClick={handleAction}
          disabled={loading}
          variant={variant === "compact" ? "ghost" : "default"}
        >
          {loading ? t.common.loading : t.common.action}
        </Button>
      </CardContent>
    </Card>
  )
}
```

## Form Component Template

```tsx
"use client"

import { useState } from "react"
import { useI18n } from "@/lib/i18n"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Loader2 } from "lucide-react"

export type FormData = {
  name: string
  type: string
}

export type FormComponentProps = {
  initialData?: Partial<FormData>
  onSubmit: (data: FormData) => Promise<void>
  onCancel?: () => void
}

export function FormComponent({
  initialData,
  onSubmit,
  onCancel,
}: FormComponentProps) {
  const { t } = useI18n()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    name: initialData?.name ?? "",
    type: initialData?.type ?? "",
  })
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({})

  const validate = (): boolean => {
    const newErrors: typeof errors = {}

    if (!formData.name.trim()) {
      newErrors.name = t.validation.required
    }

    if (!formData.type) {
      newErrors.type = t.validation.required
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) return

    setLoading(true)
    try {
      await onSubmit(formData)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">{t.common.name}</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          disabled={loading}
        />
        {errors.name && (
          <p className="text-sm text-red-500">{errors.name}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="type">{t.common.type}</Label>
        <Select
          value={formData.type}
          onValueChange={(value) => setFormData({ ...formData, type: value })}
          disabled={loading}
        >
          <SelectTrigger id="type">
            <SelectValue placeholder={t.common.selectType} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="option1">Option 1</SelectItem>
            <SelectItem value="option2">Option 2</SelectItem>
          </SelectContent>
        </Select>
        {errors.type && (
          <p className="text-sm text-red-500">{errors.type}</p>
        )}
      </div>

      <div className="flex justify-end gap-2">
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel} disabled={loading}>
            {t.common.cancel}
          </Button>
        )}
        <Button type="submit" disabled={loading}>
          {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {t.common.save}
        </Button>
      </div>
    </form>
  )
}
```

## Checklist

Before completing:
- [ ] Component file created at `app/ui/components/`
- [ ] TypeScript props type exported
- [ ] Props documented with JSDoc comments
- [ ] Default values for optional props
- [ ] Loading states handled
- [ ] i18n keys added if text needed
- [ ] Uses cn() for className merging
- [ ] Follows shadcn/ui patterns
- [ ] Accessible (proper labels, ARIA)

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Component file | kebab-case | `student-card.tsx` |
| Component name | PascalCase | `StudentCard` |
| Props type | PascalCase + Props | `StudentCardProps` |
| Event handlers | onAction | `onSelect`, `onSubmit` |
| Boolean props | is/has prefix | `isLoading`, `hasError` |

## File Location Decision

| Component Type | Location |
|---------------|----------|
| UI primitives | `components/ui/` (shadcn) |
| Shared components | `components/` |
| Feature-specific | `components/[feature]/` |
| Page-specific | Co-locate with page |

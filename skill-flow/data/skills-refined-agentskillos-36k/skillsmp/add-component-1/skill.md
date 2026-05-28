---
name: add-component
description: Scaffolds React components with TypeScript, dark mode support, i18n, and project design patterns. Use /component [name] [type] to create components. Types: modal, table, card, form, chart.
allowed-tools: Read, Write, Glob
---

# Add Component Skill

## Overview

Scaffolds React components following the project's established patterns:
- TypeScript with proper prop interfaces
- Dark mode support (light/dark class pairs)
- i18n integration via useLocale hook
- Design system colors (gold theme)
- Responsive design patterns

## Command

`/component [name] [type]`

**Types:**
- `modal` - Dialog/modal component with overlay
- `table` - Data table with sorting and actions
- `card` - Card component for displaying data
- `form` - Form with validation
- `chart` - Recharts-based chart component

**Examples:**
- `/component OrderHistory table` - Creates OrderHistoryTable.tsx
- `/component AddOrder modal` - Creates AddOrderModal.tsx
- `/component OrderSummary card` - Creates OrderSummaryCard.tsx

## Base Component Template

```tsx
'use client'

import { useState } from 'react'
import { useLocale } from '@/components/providers/LocaleProvider'

interface ComponentNameProps {
  // Props here
}

export function ComponentName({ }: ComponentNameProps) {
  const { t } = useLocale()

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      {/* Content */}
    </div>
  )
}
```

## Modal Template

```tsx
'use client'

import { useState } from 'react'
import { X } from 'lucide-react'
import { useLocale } from '@/components/providers/LocaleProvider'

interface AddEditItemModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: ItemData) => Promise<void>
  item?: ItemData | null  // null for create, object for edit
}

interface ItemData {
  id?: string
  name: string
  // ... other fields
}

export function AddEditItemModal({ isOpen, onClose, onSave, item }: AddEditItemModalProps) {
  const { t } = useLocale()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formData, setFormData] = useState<ItemData>({
    name: item?.name || '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const isEditing = !!item

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate
    const newErrors: Record<string, string> = {}
    if (!formData.name.trim()) {
      newErrors.name = t('validation.required')
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsSubmitting(true)
    try {
      await onSave(formData)
      onClose()
    } catch (error) {
      console.error('Error saving:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            {isEditing ? t('common.edit') : t('common.add')} {t('items.item')}
          </h2>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {t('common.name')} *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-gold-500 focus:border-gold-500 dark:bg-gray-700 dark:text-white"
              placeholder={t('placeholders.enterName')}
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.name}</p>
            )}
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
            >
              {t('common.cancel')}
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 bg-gold-600 text-white rounded-lg hover:bg-gold-700 disabled:opacity-50"
            >
              {isSubmitting ? t('common.saving') : (isEditing ? t('common.update') : t('common.create'))}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

## Table Template

```tsx
'use client'

import { useState } from 'react'
import { Edit2, Trash2, ChevronDown, ChevronUp } from 'lucide-react'
import { useLocale } from '@/components/providers/LocaleProvider'

interface ItemData {
  id: string
  name: string
  // ... other fields
}

interface DataTableProps {
  data: ItemData[]
  onEdit?: (item: ItemData) => void
  onDelete?: (id: string) => void
  isLoading?: boolean
}

export function DataTable({ data, onEdit, onDelete, isLoading }: DataTableProps) {
  const { t } = useLocale()
  const [sortField, setSortField] = useState<keyof ItemData>('name')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')

  const handleSort = (field: keyof ItemData) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const sortedData = [...data].sort((a, b) => {
    const aVal = a[sortField]
    const bVal = b[sortField]
    const modifier = sortDirection === 'asc' ? 1 : -1
    return aVal < bVal ? -1 * modifier : aVal > bVal ? 1 * modifier : 0
  })

  const SortIcon = ({ field }: { field: keyof ItemData }) => {
    if (sortField !== field) return null
    return sortDirection === 'asc' ?
      <ChevronUp className="w-4 h-4" /> :
      <ChevronDown className="w-4 h-4" />
  }

  if (isLoading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-8">
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gold-600"></div>
        </div>
      </div>
    )
  }

  if (data.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-8 text-center">
        <p className="text-gray-500 dark:text-gray-400">{t('common.noData')}</p>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th
                onClick={() => handleSort('name')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                <div className="flex items-center gap-1">
                  {t('common.name')}
                  <SortIcon field="name" />
                </div>
              </th>
              {(onEdit || onDelete) && (
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  {t('common.actions')}
                </th>
              )}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {sortedData.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {item.name}
                </td>
                {(onEdit || onDelete) && (
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <div className="flex justify-end gap-2">
                      {onEdit && (
                        <button
                          onClick={() => onEdit(item)}
                          className="p-1 text-gray-400 hover:text-gold-600 dark:hover:text-gold-400"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                      )}
                      {onDelete && (
                        <button
                          onClick={() => onDelete(item.id)}
                          className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
```

## Card Template

```tsx
'use client'

import { useLocale } from '@/components/providers/LocaleProvider'

interface SummaryCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon?: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
  }
}

export function SummaryCard({ title, value, subtitle, icon, trend }: SummaryCardProps) {
  const { t } = useLocale()

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
            {title}
          </p>
          <p className="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">
            {value}
          </p>
          {subtitle && (
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {subtitle}
            </p>
          )}
          {trend && (
            <p className={`mt-2 text-sm ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.isPositive ? '+' : ''}{trend.value}%
            </p>
          )}
        </div>
        {icon && (
          <div className="p-3 bg-gold-100 dark:bg-gold-900/30 rounded-lg">
            <div className="w-6 h-6 text-gold-600 dark:text-gold-400">
              {icon}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
```

## Chart Template

```tsx
'use client'

import { useLocale } from '@/components/providers/LocaleProvider'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface ChartData {
  date: string
  value: number
}

interface TrendChartProps {
  data: ChartData[]
  title: string
  valueFormatter?: (value: number) => string
}

export function TrendChart({ data, title, valueFormatter = (v) => v.toString() }: TrendChartProps) {
  const { t } = useLocale()

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        {title}
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#D4AF37" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#D4AF37" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
            <XAxis
              dataKey="date"
              className="text-gray-600 dark:text-gray-400"
              tick={{ fontSize: 12 }}
            />
            <YAxis
              className="text-gray-600 dark:text-gray-400"
              tick={{ fontSize: 12 }}
              tickFormatter={valueFormatter}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--tooltip-bg)',
                border: '1px solid var(--tooltip-border)',
                borderRadius: '8px',
              }}
              formatter={(value: number) => [valueFormatter(value), title]}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#D4AF37"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
```

## Design System Reference

### Colors
- Primary: `gold-600` (#D4AF37) for buttons, accents
- Background: `white` / `gray-800` (dark)
- Border: `gray-200` / `gray-700` (dark)
- Text: `gray-900` / `white` (dark)
- Muted text: `gray-500` / `gray-400` (dark)

### Spacing
- Card padding: `p-6`
- Modal padding: `p-4`
- Button padding: `px-4 py-2`
- Input padding: `px-3 py-2`

### Border Radius
- Cards/Modals: `rounded-lg`
- Buttons/Inputs: `rounded-lg`
- Badges: `rounded-full`

## Process

When user invokes `/component [name] [type]`:

1. Determine component location:
   - Modal → `components/{domain}/AddEdit{Name}Modal.tsx`
   - Table → `components/{domain}/{Name}Table.tsx`
   - Card → `components/{domain}/{Name}Card.tsx`
   - Chart → `components/{domain}/{Name}Chart.tsx`
   - Form → `components/{domain}/{Name}Form.tsx`

2. Ask for domain folder if not obvious from name

3. Generate component with:
   - TypeScript interfaces
   - i18n integration
   - Dark mode support
   - Responsive design

4. Report file created and suggest i18n keys to add

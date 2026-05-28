# Dynamic UI Generation from Backend Schemas

This document explains how to build dynamic forms, tables, and UI components driven entirely by backend API schemas.

## Overview

Dynamic UI generation enables:

- **Backend-driven forms** - Add fields without frontend changes
- **Schema-based validation** - Single source of truth
- **Auto-generated tables** - Columns defined by API
- **Type safety** - Runtime validation with Zod
- **Reduced boilerplate** - Write once, reuse everywhere

## Form Schema Format

### Schema Structure

```ts
// src/types/schema.ts
export interface FieldSchema {
  name: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'multiselect' | 'checkbox' | 'radio' | 'date' | 'datetime' | 'textarea' | 'file'
  label: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  readonly?: boolean
  defaultValue?: unknown
  validation?: {
    min?: number
    max?: number
    minLength?: number
    maxLength?: number
    pattern?: string
    custom?: string // Custom validation function name
  }
  options?: Array<{ label: string; value: string | number }> // For select, multiselect, radio
  dependsOn?: {
    field: string
    value: unknown
  }
  helpText?: string
  gridColumn?: string // Tailwind grid class
}

export interface FormSchema {
  fields: FieldSchema[]
  layout?: 'single' | 'two-column' | 'three-column'
  submitLabel?: string
  cancelLabel?: string
}
```

### Example Schema from Backend

```json
{
  "fields": [
    {
      "name": "firstName",
      "type": "text",
      "label": "First Name",
      "placeholder": "Enter first name",
      "required": true,
      "validation": {
        "minLength": 2,
        "maxLength": 50
      }
    },
    {
      "name": "lastName",
      "type": "text",
      "label": "Last Name",
      "required": true
    },
    {
      "name": "email",
      "type": "email",
      "label": "Email Address",
      "required": true,
      "validation": {
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
      }
    },
    {
      "name": "role",
      "type": "select",
      "label": "Role",
      "required": true,
      "options": [
        { "label": "Administrator", "value": "admin" },
        { "label": "User", "value": "user" },
        { "label": "Guest", "value": "guest" }
      ]
    },
    {
      "name": "department",
      "type": "select",
      "label": "Department",
      "dependsOn": {
        "field": "role",
        "value": "admin"
      },
      "options": [
        { "label": "Engineering", "value": "eng" },
        { "label": "Sales", "value": "sales" },
        { "label": "Marketing", "value": "marketing" }
      ]
    },
    {
      "name": "isActive",
      "type": "checkbox",
      "label": "Active User",
      "defaultValue": true
    }
  ],
  "layout": "two-column",
  "submitLabel": "Create User",
  "cancelLabel": "Cancel"
}
```

## Dynamic Form Component

### Field Renderer

```tsx
// src/components/DynamicForm/FieldRenderer.tsx
import { FieldSchema } from '@/types/schema'
import { TextField } from './fields/TextField'
import { SelectField } from './fields/SelectField'
import { CheckboxField } from './fields/CheckboxField'
import { DateField } from './fields/DateField'
import { TextareaField } from './fields/TextareaField'
import { FileField } from './fields/FileField'

interface FieldRendererProps {
  field: FieldSchema
  value: unknown
  onChange: (name: string, value: unknown) => void
  error?: string
}

export function FieldRenderer({ field, value, onChange, error }: FieldRendererProps) {
  const commonProps = {
    name: field.name,
    label: field.label,
    value,
    onChange: (val: unknown) => onChange(field.name, val),
    error,
    required: field.required,
    disabled: field.disabled,
    placeholder: field.placeholder,
    helpText: field.helpText,
  }
  
  switch (field.type) {
    case 'text':
    case 'email':
    case 'password':
    case 'number':
      return <TextField {...commonProps} type={field.type} />
      
    case 'select':
    case 'multiselect':
      return <SelectField {...commonProps} options={field.options || []} multiple={field.type === 'multiselect'} />
      
    case 'checkbox':
      return <CheckboxField {...commonProps} />
      
    case 'radio':
      return <RadioField {...commonProps} options={field.options || []} />
      
    case 'date':
    case 'datetime':
      return <DateField {...commonProps} includeTime={field.type === 'datetime'} />
      
    case 'textarea':
      return <TextareaField {...commonProps} />
      
    case 'file':
      return <FileField {...commonProps} />
      
    default:
      console.warn(`Unknown field type: ${field.type}`)
      return null
  }
}
```

### Dynamic Form Component

```tsx
// src/components/DynamicForm/DynamicForm.tsx
import { useState, useEffect } from 'react'
import { z } from 'zod'
import { FormSchema, FieldSchema } from '@/types/schema'
import { FieldRenderer } from './FieldRenderer'
import { TkButton } from '@takeoff-ui/react'
import { cn } from '@/lib/cn'

interface DynamicFormProps {
  schema: FormSchema
  initialValues?: Record<string, unknown>
  onSubmit: (data: Record<string, unknown>) => void | Promise<void>
  onCancel?: () => void
  isLoading?: boolean
}

export function DynamicForm({
  schema,
  initialValues = {},
  onSubmit,
  onCancel,
  isLoading = false,
}: DynamicFormProps) {
  const [values, setValues] = useState<Record<string, unknown>>(initialValues)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  
  // Initialize default values
  useEffect(() => {
    const defaults: Record<string, unknown> = {}
    schema.fields.forEach((field) => {
      if (field.defaultValue !== undefined && values[field.name] === undefined) {
        defaults[field.name] = field.defaultValue
      }
    })
    if (Object.keys(defaults).length > 0) {
      setValues((prev) => ({ ...defaults, ...prev }))
    }
  }, [schema.fields])
  
  // Generate Zod schema from field schemas
  const zodSchema = generateZodSchema(schema.fields)
  
  const handleChange = (name: string, value: unknown) => {
    setValues((prev) => ({ ...prev, [name]: value }))
    setTouched((prev) => ({ ...prev, [name]: true }))
    
    // Clear error for this field
    setErrors((prev) => {
      const { [name]: _, ...rest } = prev
      return rest
    })
  }
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate
    try {
      zodSchema.parse(values)
      setErrors({})
      await onSubmit(values)
    } catch (error) {
      if (error instanceof z.ZodError) {
        const formattedErrors: Record<string, string> = {}
        error.errors.forEach((err) => {
          const path = err.path.join('.')
          formattedErrors[path] = err.message
        })
        setErrors(formattedErrors)
      }
    }
  }
  
  // Filter visible fields based on dependencies
  const visibleFields = schema.fields.filter((field) => {
    if (!field.dependsOn) return true
    return values[field.dependsOn.field] === field.dependsOn.value
  })
  
  // Determine grid layout
  const gridClass = {
    single: 'grid-cols-1',
    'two-column': 'grid-cols-1 md:grid-cols-2',
    'three-column': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
  }[schema.layout || 'single']
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className={cn('grid gap-4', gridClass)}>
        {visibleFields.map((field) => (
          <div
            key={field.name}
            className={field.gridColumn || ''}
          >
            <FieldRenderer
              field={field}
              value={values[field.name]}
              onChange={handleChange}
              error={touched[field.name] ? errors[field.name] : undefined}
            />
          </div>
        ))}
      </div>
      
      <div className="flex items-center justify-end gap-3 pt-4 border-t">
        {onCancel && (
          <TkButton
            label={schema.cancelLabel || 'Cancel'}
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
          />
        )}
        <TkButton
          label={schema.submitLabel || 'Submit'}
          type="submit"
          loading={isLoading}
        />
      </div>
    </form>
  )
}

// Helper function to generate Zod schema
function generateZodSchema(fields: FieldSchema[]): z.ZodObject<any> {
  const shape: Record<string, z.ZodTypeAny> = {}
  
  fields.forEach((field) => {
    let fieldSchema: z.ZodTypeAny
    
    // Base type
    switch (field.type) {
      case 'text':
      case 'email':
      case 'password':
      case 'textarea':
        fieldSchema = z.string()
        
        if (field.type === 'email') {
          fieldSchema = fieldSchema.email('Invalid email address')
        }
        
        if (field.validation?.minLength) {
          fieldSchema = fieldSchema.min(
            field.validation.minLength,
            `Minimum ${field.validation.minLength} characters required`
          )
        }
        
        if (field.validation?.maxLength) {
          fieldSchema = fieldSchema.max(
            field.validation.maxLength,
            `Maximum ${field.validation.maxLength} characters allowed`
          )
        }
        
        if (field.validation?.pattern) {
          fieldSchema = fieldSchema.regex(
            new RegExp(field.validation.pattern),
            'Invalid format'
          )
        }
        break
        
      case 'number':
        fieldSchema = z.number()
        
        if (field.validation?.min !== undefined) {
          fieldSchema = fieldSchema.min(field.validation.min)
        }
        
        if (field.validation?.max !== undefined) {
          fieldSchema = fieldSchema.max(field.validation.max)
        }
        break
        
      case 'checkbox':
        fieldSchema = z.boolean()
        break
        
      case 'select':
        fieldSchema = z.string()
        break
        
      case 'multiselect':
        fieldSchema = z.array(z.string())
        break
        
      case 'date':
      case 'datetime':
        fieldSchema = z.string().or(z.date())
        break
        
      case 'file':
        fieldSchema = z.instanceof(File).or(z.string())
        break
        
      default:
        fieldSchema = z.any()
    }
    
    // Make optional if not required
    if (!field.required) {
      fieldSchema = fieldSchema.optional()
    }
    
    shape[field.name] = fieldSchema
  })
  
  return z.object(shape)
}
```

## Individual Field Components

### Text Field

```tsx
// src/components/DynamicForm/fields/TextField.tsx
import { TkInput } from '@takeoff-ui/react'

interface TextFieldProps {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number'
  value: string | number
  onChange: (value: string | number) => void
  error?: string
  required?: boolean
  disabled?: boolean
  placeholder?: string
  helpText?: string
}

export function TextField({
  name,
  label,
  type,
  value,
  onChange,
  error,
  required,
  disabled,
  placeholder,
  helpText,
}: TextFieldProps) {
  return (
    <div className="space-y-1">
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      <TkInput
        id={name}
        name={name}
        type={type}
        value={value?.toString() || ''}
        onChange={(e) => {
          const val = type === 'number' ? parseFloat(e.target.value) : e.target.value
          onChange(val)
        }}
        placeholder={placeholder}
        disabled={disabled}
        className={error ? 'border-red-500' : ''}
      />
      
      {helpText && !error && (
        <p className="text-xs text-gray-500">{helpText}</p>
      )}
      
      {error && (
        <p className="text-xs text-red-500">{error}</p>
      )}
    </div>
  )
}
```

### Select Field

```tsx
// src/components/DynamicForm/fields/SelectField.tsx
import { TkSelect } from '@takeoff-ui/react'

interface SelectFieldProps {
  name: string
  label: string
  value: string | string[]
  onChange: (value: string | string[]) => void
  options: Array<{ label: string; value: string | number }>
  multiple?: boolean
  error?: string
  required?: boolean
  disabled?: boolean
  placeholder?: string
  helpText?: string
}

export function SelectField({
  name,
  label,
  value,
  onChange,
  options,
  multiple,
  error,
  required,
  disabled,
  placeholder,
  helpText,
}: SelectFieldProps) {
  return (
    <div className="space-y-1">
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      <TkSelect
        id={name}
        name={name}
        value={value}
        onChange={(e) => {
          if (multiple) {
            const selected = Array.from(e.target.selectedOptions, (option) => option.value)
            onChange(selected)
          } else {
            onChange(e.target.value)
          }
        }}
        multiple={multiple}
        disabled={disabled}
        className={error ? 'border-red-500' : ''}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </TkSelect>
      
      {helpText && !error && (
        <p className="text-xs text-gray-500">{helpText}</p>
      )}
      
      {error && (
        <p className="text-xs text-red-500">{error}</p>
      )}
    </div>
  )
}
```

## Dynamic Data Table

### Table Schema Format

```ts
export interface ColumnSchema {
  key: string
  label: string
  type: 'text' | 'number' | 'date' | 'badge' | 'boolean' | 'actions'
  sortable?: boolean
  filterable?: boolean
  width?: string
  align?: 'left' | 'center' | 'right'
  format?: (value: unknown) => string
  badge?: {
    colors: Record<string, string> // Status -> Tailwind color class
  }
  actions?: Array<{
    label: string
    icon?: string
    variant?: 'primary' | 'secondary' | 'danger'
    onClick: (row: Record<string, unknown>) => void
  }>
}

export interface TableSchema {
  columns: ColumnSchema[]
  enablePagination?: boolean
  enableFilters?: boolean
  enableSearch?: boolean
  pageSize?: number
  actions?: {
    create?: {
      label: string
      onClick: () => void
    }
    bulk?: Array<{
      label: string
      onClick: (selected: Record<string, unknown>[]) => void
    }>
  }
}
```

### Dynamic Data Table Component

```tsx
// src/components/DataTable/DataTable.tsx
import { useState, useMemo } from 'react'
import { TableSchema, ColumnSchema } from '@/types/schema'
import { TkButton, TkBadge, TkInput } from '@takeoff-ui/react'
import { cn } from '@/lib/cn'

interface DataTableProps {
  schema: TableSchema
  data: Record<string, unknown>[]
  isLoading?: boolean
  onRowClick?: (row: Record<string, unknown>) => void
}

export function DataTable({ schema, data, isLoading, onRowClick }: DataTableProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortColumn, setSortColumn] = useState<string | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set())
  
  // Filter data by search term
  const filteredData = useMemo(() => {
    if (!schema.enableSearch || !searchTerm) return data
    
    return data.filter((row) =>
      Object.values(row).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    )
  }, [data, searchTerm, schema.enableSearch])
  
  // Sort data
  const sortedData = useMemo(() => {
    if (!sortColumn) return filteredData
    
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortColumn]
      const bVal = b[sortColumn]
      
      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1
      return 0
    })
  }, [filteredData, sortColumn, sortDirection])
  
  // Paginate data
  const pageSize = schema.pageSize || 10
  const paginatedData = useMemo(() => {
    if (!schema.enablePagination) return sortedData
    
    const startIndex = (currentPage - 1) * pageSize
    return sortedData.slice(startIndex, startIndex + pageSize)
  }, [sortedData, currentPage, pageSize, schema.enablePagination])
  
  const totalPages = Math.ceil(sortedData.length / pageSize)
  
  const handleSort = (column: ColumnSchema) => {
    if (!column.sortable) return
    
    if (sortColumn === column.key) {
      setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortColumn(column.key)
      setSortDirection('asc')
    }
  }
  
  const renderCell = (row: Record<string, unknown>, column: ColumnSchema) => {
    const value = row[column.key]
    
    switch (column.type) {
      case 'badge':
        const badgeColor = column.badge?.colors[String(value)] || 'bg-gray-500'
        return (
          <TkBadge label={String(value)} className={badgeColor} />
        )
        
      case 'boolean':
        return value ? '✓' : '✗'
        
      case 'date':
        return value ? new Date(value as string).toLocaleDateString() : '-'
        
      case 'number':
        return typeof value === 'number' ? value.toLocaleString() : value
        
      case 'actions':
        return (
          <div className="flex items-center gap-2">
            {column.actions?.map((action, idx) => (
              <TkButton
                key={idx}
                label={action.label}
                size="small"
                variant={action.variant}
                onClick={(e) => {
                  e.stopPropagation()
                  action.onClick(row)
                }}
              />
            ))}
          </div>
        )
        
      default:
        return column.format ? column.format(value) : String(value || '-')
    }
  }
  
  if (isLoading) {
    return <div className="text-center py-8">Loading...</div>
  }
  
  return (
    <div className="space-y-4">
      {/* Header actions */}
      <div className="flex items-center justify-between">
        {schema.enableSearch && (
          <TkInput
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-sm"
          />
        )}
        
        {schema.actions?.create && (
          <TkButton
            label={schema.actions.create.label}
            onClick={schema.actions.create.onClick}
          />
        )}
      </div>
      
      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {schema.columns.map((column) => (
                <th
                  key={column.key}
                  className={cn(
                    'px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider',
                    column.align === 'center' && 'text-center',
                    column.align === 'right' && 'text-right',
                    column.sortable && 'cursor-pointer hover:bg-gray-100'
                  )}
                  style={{ width: column.width }}
                  onClick={() => handleSort(column)}
                >
                  <div className="flex items-center gap-2">
                    {column.label}
                    {column.sortable && sortColumn === column.key && (
                      <span>{sortDirection === 'asc' ? '↑' : '↓'}</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className={cn(
                  'hover:bg-gray-50 transition-colors',
                  onRowClick && 'cursor-pointer'
                )}
                onClick={() => onRowClick?.(row)}
              >
                {schema.columns.map((column) => (
                  <td
                    key={column.key}
                    className={cn(
                      'px-4 py-3 text-sm text-gray-900',
                      column.align === 'center' && 'text-center',
                      column.align === 'right' && 'text-right'
                    )}
                  >
                    {renderCell(row, column)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Pagination */}
      {schema.enablePagination && totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing {(currentPage - 1) * pageSize + 1} to{' '}
            {Math.min(currentPage * pageSize, sortedData.length)} of {sortedData.length} results
          </div>
          
          <div className="flex items-center gap-2">
            <TkButton
              label="Previous"
              onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            />
            
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            
            <TkButton
              label="Next"
              onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            />
          </div>
        </div>
      )}
    </div>
  )
}
```

## Usage Examples

### Fetch Schema and Render Form

```tsx
// src/pages/Users/UserCreatePage.tsx
import { DynamicForm } from '@/components/DynamicForm'
import { useFormSchema, useCreateUser } from '@/api/endpoints/users'

export default function UserCreatePage() {
  const { data: schema, isLoading: schemaLoading } = useFormSchema('users')
  const createUser = useCreateUser()
  
  if (schemaLoading || !schema) {
    return <Spinner />
  }
  
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Create User</h1>
      
      <DynamicForm
        schema={schema}
        onSubmit={(data) => createUser.mutate(data)}
        isLoading={createUser.isPending}
      />
    </div>
  )
}
```

### Fetch Schema and Render Table

```tsx
// src/pages/Users/UsersPage.tsx
import { DataTable } from '@/components/DataTable'
import { useTableSchema, useUsers } from '@/api/endpoints/users'

export default function UsersPage() {
  const { data: schema, isLoading: schemaLoading } = useTableSchema('users')
  const { data: users, isLoading: usersLoading } = useUsers()
  
  if (schemaLoading || !schema) {
    return <Spinner />
  }
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Users</h1>
      
      <DataTable
        schema={schema}
        data={users || []}
        isLoading={usersLoading}
      />
    </div>
  )
}
```

## Best Practices

1. **Validate schemas** - Use Zod to validate backend schemas
2. **Cache schemas** - Use TanStack Query to cache form/table schemas
3. **Type safety** - Generate TypeScript types from schemas
4. **Graceful fallback** - Handle missing/invalid schema fields
5. **Performance** - Memoize field rendering to avoid re-renders
6. **Accessibility** - Ensure dynamically rendered fields are accessible
7. **Error handling** - Display field-level and form-level errors
8. **Loading states** - Show loading UI while fetching schemas

## Summary

Dynamic UI generation provides:

- **Flexibility** - Backend controls UI without frontend deploys
- **Consistency** - Single schema for validation and rendering
- **Productivity** - Less boilerplate, faster development
- **Maintainability** - Schema changes propagate automatically
- **Type safety** - Runtime validation with Zod

This pattern is essential for enterprise applications with frequently changing data models.
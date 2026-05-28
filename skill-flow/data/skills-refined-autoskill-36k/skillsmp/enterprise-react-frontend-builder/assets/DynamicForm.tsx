import { useState, useEffect } from 'react'
import { z } from 'zod'
import { TkButton, TkInput, TkSelect, TkCheckbox } from '@takeoff-ui/react'
import { cn } from '@/lib/cn'

export interface FieldSchema {
  name: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'checkbox' | 'textarea' | 'date'
  label: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  defaultValue?: any
  options?: Array<{ label: string; value: string | number }>
  validation?: {
    min?: number
    max?: number
    minLength?: number
    maxLength?: number
    pattern?: string
  }
  gridColumn?: string
}

export interface FormSchema {
  fields: FieldSchema[]
  layout?: 'single' | 'two-column' | 'three-column'
  submitLabel?: string
  cancelLabel?: string
}

interface DynamicFormProps {
  schema: FormSchema
  initialValues?: Record<string, any>
  onSubmit: (data: Record<string, any>) => void | Promise<void>
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
  const [values, setValues] = useState<Record<string, any>>(initialValues)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  
  // Initialize default values
  useEffect(() => {
    const defaults: Record<string, any> = {}
    schema.fields.forEach((field) => {
      if (field.defaultValue !== undefined && values[field.name] === undefined) {
        defaults[field.name] = field.defaultValue
      }
    })
    if (Object.keys(defaults).length > 0) {
      setValues((prev) => ({ ...defaults, ...prev }))
    }
  }, [schema.fields])
  
  // Generate Zod schema
  const zodSchema = generateZodSchema(schema.fields)
  
  const handleChange = (name: string, value: any) => {
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
  
  const renderField = (field: FieldSchema) => {
    const value = values[field.name] ?? ''
    const error = touched[field.name] ? errors[field.name] : undefined
    
    const commonProps = {
      disabled: field.disabled || isLoading,
      className: error ? 'border-red-500' : '',
    }
    
    switch (field.type) {
      case 'text':
      case 'email':
      case 'password':
      case 'number':
        return (
          <div key={field.name} className={field.gridColumn || ''}>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <TkInput
              type={field.type}
              name={field.name}
              value={value}
              onChange={(e) => {
                const val = field.type === 'number' ? parseFloat(e.target.value) : e.target.value
                handleChange(field.name, val)
              }}
              placeholder={field.placeholder}
              {...commonProps}
            />
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
        )
        
      case 'select':
        return (
          <div key={field.name} className={field.gridColumn || ''}>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <TkSelect
              name={field.name}
              value={value}
              onChange={(e) => handleChange(field.name, e.target.value)}
              {...commonProps}
            >
              {field.placeholder && <option value="">{field.placeholder}</option>}
              {field.options?.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </TkSelect>
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
        )
        
      case 'checkbox':
        return (
          <div key={field.name} className={field.gridColumn || ''}>
            <TkCheckbox
              name={field.name}
              checked={!!value}
              onChange={(e) => handleChange(field.name, e.target.checked)}
              label={field.label}
              {...commonProps}
            />
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
        )
        
      case 'textarea':
        return (
          <div key={field.name} className={field.gridColumn || ''}>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <textarea
              name={field.name}
              value={value}
              onChange={(e) => handleChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              rows={4}
              className={cn(
                'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                error && 'border-red-500'
              )}
              {...commonProps}
            />
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
        )
        
      case 'date':
        return (
          <div key={field.name} className={field.gridColumn || ''}>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <TkInput
              type="date"
              name={field.name}
              value={value}
              onChange={(e) => handleChange(field.name, e.target.value)}
              {...commonProps}
            />
            {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
          </div>
        )
        
      default:
        return null
    }
  }
  
  const gridClass = {
    single: 'grid-cols-1',
    'two-column': 'grid-cols-1 md:grid-cols-2',
    'three-column': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
  }[schema.layout || 'single']
  
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className={cn('grid gap-4', gridClass)}>
        {schema.fields.map(renderField)}
      </div>
      
      <div className="flex items-center justify-end gap-3 pt-4 border-t">
        {onCancel && (
          <TkButton
            label={schema.cancelLabel || 'Cancel'}
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
            type="button"
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

// Helper function to generate Zod schema from field schemas
function generateZodSchema(fields: FieldSchema[]): z.ZodObject<any> {
  const shape: Record<string, z.ZodTypeAny> = {}
  
  fields.forEach((field) => {
    let fieldSchema: z.ZodTypeAny
    
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
        
      case 'date':
        fieldSchema = z.string()
        break
        
      default:
        fieldSchema = z.any()
    }
    
    if (!field.required) {
      fieldSchema = fieldSchema.optional()
    }
    
    shape[field.name] = fieldSchema
  })
  
  return z.object(shape)
}
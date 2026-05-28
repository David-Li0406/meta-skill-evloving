# Error Display Patterns

## Inline Error Messages

Display errors below the input field with an icon:

```typescript
import { AlertCircle } from "lucide-react"

{errors.fieldName && (
    <div className="flex items-center gap-2 text-red-400 text-sm mt-1">
        <AlertCircle className="h-4 w-4 flex-shrink-0" />
        {errors.fieldName}
    </div>
)}
```

## Error Border on Input

Add red border when field has error:

```typescript
import { cn } from "@/lib/utils"

<input
    className={cn(
        "w-full bg-zinc-950 border rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors",
        errors.fieldName ? "border-red-500" : "border-zinc-800"
    )}
/>
```

## Error Banner

Display prominent error message at top of form:

```typescript
{error && (
    <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3">
        <AlertCircle className="h-4 w-4 flex-shrink-0" />
        {error}
    </div>
)}
```

## Field-Level Error State

Track errors for individual fields:

```typescript
interface ValidationErrors {
    fieldName?: string
    anotherField?: string
}

const [errors, setErrors] = useState<ValidationErrors>({})

// Set error
setErrors(prev => ({ ...prev, fieldName: "Error message" }))

// Clear error
setErrors(prev => ({ ...prev, fieldName: undefined }))

// Clear all errors
setErrors({})
```

## Real-Time Validation

Validate on blur or change:

```typescript
<input
    onChange={(e) => {
        const error = validateField(e.target.value)
        setErrors(prev => ({ ...prev, fieldName: error }))
    }}
    onBlur={(e) => {
        const error = validateField(e.target.value)
        setErrors(prev => ({ ...prev, fieldName: error }))
    }}
/>
```

## Form-Level Validation

Validate entire form before submission:

```typescript
const validateForm = (): boolean => {
    const newErrors: ValidationErrors = {}
    
    const nameError = validateRequired(name, "Name")
    if (nameError) newErrors.name = nameError
    
    const emailError = validateEmail(email)
    if (emailError) newErrors.email = emailError
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
}

const handleSubmit = async (formData: FormData) => {
    if (!validateForm()) return
    
    // Proceed with submission
}
```

## Error Summary

Display all errors at once:

```typescript
{Object.keys(errors).length > 0 && (
    <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
        <h3 className="text-red-400 font-semibold mb-2">Please fix the following errors:</h3>
        <ul className="list-disc list-inside text-red-400 text-sm space-y-1">
            {Object.entries(errors).map(([field, error]) => (
                <li key={field}>{error}</li>
            ))}
        </ul>
    </div>
)}
```

## Success State

Show success message after validation passes:

```typescript
{success && (
    <div className="flex items-center gap-2 text-emerald-400 text-sm bg-emerald-500/10 border border-emerald-500/20 rounded-lg px-4 py-3">
        <CheckCircle className="h-4 w-4 flex-shrink-0" />
        {success}
    </div>
)}
```

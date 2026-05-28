# Common Validation Patterns

## Number Range Validation

```typescript
const validateNumberRange = (value: string, min: number, max: number, fieldName: string): string | undefined => {
    const num = parseInt(value)
    if (isNaN(num)) return `${fieldName} must be a number`
    if (num < min) return `Minimum is ${min}`
    if (num > max) return `Maximum is ${max}`
    return undefined
}

// Example usage
const error = validateNumberRange(formData.get("minScores") as string, 1, 20, "Min Scores")
```

## Date Range Validation

```typescript
const validateDateRange = (startDate?: Date, endDate?: Date): string | undefined => {
    if (!startDate || !endDate) {
        return "Both start and end dates are required"
    }

    const today = new Date()
    today.setHours(0, 0, 0, 0)

    if (startDate < today) {
        return "Start date cannot be in the past"
    }

    if (endDate <= startDate) {
        return "End date must be after start date"
    }

    // Minimum duration (e.g., 1 week)
    const oneWeek = 7 * 24 * 60 * 60 * 1000
    if (endDate.getTime() - startDate.getTime() < oneWeek) {
        return "Duration must be at least 1 week"
    }

    // Maximum duration (e.g., 1 year)
    const oneYear = 365 * 24 * 60 * 60 * 1000
    if (endDate.getTime() - startDate.getTime() > oneYear) {
        return "Duration cannot exceed 1 year"
    }

    return undefined
}
```

## Email Validation

```typescript
const validateEmail = (email: string): string | undefined => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
        return "Invalid email address"
    }
    return undefined
}
```

## Phone Number Validation

```typescript
const validatePhone = (phone: string): string | undefined => {
    // US phone number: (123) 456-7890 or 123-456-7890
    const phoneRegex = /^(\(\d{3}\)\s?|\d{3}[-.]?)\d{3}[-.]?\d{4}$/
    if (!phoneRegex.test(phone)) {
        return "Invalid phone number format"
    }
    return undefined
}
```

## Text Length Validation

```typescript
const validateTextLength = (text: string, min: number, max: number, fieldName: string): string | undefined => {
    if (text.length < min) {
        return `${fieldName} must be at least ${min} characters`
    }
    if (text.length > max) {
        return `${fieldName} cannot exceed ${max} characters`
    }
    return undefined
}
```

## Slug Validation

```typescript
const validateSlug = (slug: string): string | undefined => {
    const slugRegex = /^[a-z0-9-]+$/
    if (!slugRegex.test(slug)) {
        return "Slug can only contain lowercase letters, numbers, and hyphens"
    }
    if (slug.length < 2) {
        return "Slug must be at least 2 characters"
    }
    if (slug.length > 50) {
        return "Slug cannot exceed 50 characters"
    }
    return undefined
}
```

## URL Validation

```typescript
const validateURL = (url: string): string | undefined => {
    try {
        new URL(url)
        return undefined
    } catch {
        return "Invalid URL format"
    }
}
```

## Password Strength Validation

```typescript
const validatePassword = (password: string): string | undefined => {
    if (password.length < 8) {
        return "Password must be at least 8 characters"
    }
    if (!/[A-Z]/.test(password)) {
        return "Password must contain at least one uppercase letter"
    }
    if (!/[a-z]/.test(password)) {
        return "Password must contain at least one lowercase letter"
    }
    if (!/[0-9]/.test(password)) {
        return "Password must contain at least one number"
    }
    return undefined
}
```

## Percentage Validation

```typescript
const validatePercentage = (value: string): string | undefined => {
    const num = parseFloat(value)
    if (isNaN(num)) return "Must be a number"
    if (num < 0) return "Cannot be negative"
    if (num > 100) return "Cannot exceed 100%"
    return undefined
}
```

## Required Field Validation

```typescript
const validateRequired = (value: string | undefined, fieldName: string): string | undefined => {
    if (!value || value.trim() === "") {
        return `${fieldName} is required`
    }
    return undefined
}
```

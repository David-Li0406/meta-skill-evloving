# Hooks Reference

## Contents
- useState Patterns
- useEffect Patterns
- Event Handler Types
- Anti-Patterns

## useState Patterns

### Object State for Related Values

```tsx
// GOOD - Group related form fields
const [formData, setFormData] = useState({
  firstName: '',
  lastName: '',
  email: '',
  message: ''
})

const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  setFormData(prev => ({
    ...prev,
    [e.target.name]: e.target.value
  }))
}
```

### Typed Nullable State

```tsx
// For single-select accordion (only one expanded at a time)
const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null)

// Toggle behavior
<button onClick={() => setExpandedFAQ(expandedFAQ === index ? null : index)}>
```

### Typed Array State

```tsx
// For multi-select accordion (multiple expanded)
const [expandedServices, setExpandedServices] = useState<number[]>([])

const toggleService = (index: number) => {
  setExpandedServices(prev => 
    prev.includes(index) 
      ? prev.filter(i => i !== index)
      : [...prev, index]
  )
}
```

### Form Submission State Trio

```tsx
// Standard pattern across all forms in this codebase
const [isSubmitting, setIsSubmitting] = useState(false)
const [isSubmitted, setIsSubmitted] = useState(false)
const [error, setError] = useState('')
```

## useEffect Patterns

### Mounted Check for Hydration

```tsx
const [mounted, setMounted] = useState(false)

useEffect(() => {
  setMounted(true)
}, [])

if (!mounted) return null
```

**Why:** Prevents Next.js hydration mismatch errors when client-side state differs from server render.

### Modal Body Lock

```tsx
useEffect(() => {
  if (modalOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = 'unset'
  }
  
  return () => {
    document.body.style.overflow = 'unset'
  }
}, [modalOpen])
```

## Event Handler Types

```tsx
// Input and textarea
const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {}

// Select dropdown
const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {}

// Form submission
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
}

// Button click
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {}
```

## WARNING: Anti-Patterns

### Multiple useState for Related State

**The Problem:**

```tsx
// BAD - 7 separate useState calls for navigation
const [solutionsDropdownOpen, setSolutionsDropdownOpen] = useState(false)
const [appsDropdownOpen, setAppsDropdownOpen] = useState(false)
const [resourcesDropdownOpen, setResourcesDropdownOpen] = useState(false)
const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
// ... 3 more
```

**Why This Breaks:**
1. Hard to reset all dropdowns at once
2. Easy to forget updating one when closing others
3. More re-renders than necessary

**The Fix:**

```tsx
// GOOD - Single object state
const [dropdowns, setDropdowns] = useState({
  solutions: false,
  apps: false,
  resources: false,
  mobileMenu: false
})

const closeAll = () => setDropdowns({
  solutions: false,
  apps: false,
  resources: false,
  mobileMenu: false
})
```

### Dynamic Script Loading in useEffect

**The Problem:**

```tsx
// BAD - Script reloads every time modal opens
useEffect(() => {
  if (calendlyModalOpen) {
    const script = document.createElement('script')
    script.src = 'https://assets.calendly.com/assets/external/widget.js'
    document.body.appendChild(script)
  }
}, [calendlyModalOpen])
```

**Why This Breaks:**
1. Script appended multiple times
2. No cleanup removes duplicate scripts
3. Memory leak potential

**The Fix:**
Use Next.js Script component. See the **nextjs** skill.
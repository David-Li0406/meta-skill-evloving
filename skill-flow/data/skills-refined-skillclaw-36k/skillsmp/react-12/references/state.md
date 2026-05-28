# State Management Reference

## Contents
- State Architecture
- Local State Patterns
- State Categories
- WARNING: No Global State

## State Architecture

This codebase uses **local component state only**:

| State Type | Solution | Location |
|------------|----------|----------|
| UI state (modals, tabs) | useState | Each component |
| Form data | useState | Form components |
| Submission status | useState | Form components |
| Static content | const arrays | Component level |

No Redux, Zustand, Context API, or global state management.

## Local State Patterns

### Form Data Object

```tsx
const [formData, setFormData] = useState({
  firstName: '',
  lastName: '',
  companyName: '',
  email: '',
  message: ''
})
```

### Form Status Trio

```tsx
const [isSubmitting, setIsSubmitting] = useState(false)
const [isSubmitted, setIsSubmitted] = useState(false)
const [error, setError] = useState('')
```

### UI Toggle State

```tsx
// Single item expanded (FAQ)
const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null)

// Multiple items expanded (Services)
const [expandedServices, setExpandedServices] = useState<number[]>([])

// Modal visibility
const [calendlyModalOpen, setCalendlyModalOpen] = useState(false)

// Tab selection
const [activeTab, setActiveTab] = useState('overview')
```

### Navigation Dropdowns

```tsx
// Current pattern - works but verbose
const [solutionsDropdownOpen, setSolutionsDropdownOpen] = useState(false)
const [appsDropdownOpen, setAppsDropdownOpen] = useState(false)
const [resourcesDropdownOpen, setResourcesDropdownOpen] = useState(false)
```

## State Categories

Understand which state belongs where:

| Category | Examples | Solution |
|----------|----------|----------|
| **UI State** | Modals, tabs, accordions | Local useState |
| **Form State** | Input values, validation | Local useState |
| **Server State** | API data, user profile | Not applicable here |
| **URL State** | Filters, pagination | Not applicable here |

## Immutable Update Patterns

### Object Spread

```tsx
setFormData(prev => ({
  ...prev,
  [e.target.name]: e.target.value
}))
```

### Array Filter (Remove)

```tsx
setExpandedServices(prev => prev.filter(i => i !== index))
```

### Array Spread (Add)

```tsx
setExpandedServices(prev => [...prev, index])
```

### Toggle Pattern

```tsx
const toggleService = (index: number) => {
  setExpandedServices(prev => 
    prev.includes(index) 
      ? prev.filter(i => i !== index)
      : [...prev, index]
  )
}
```

## WARNING: No Global State Library

**Detected:** No zustand, jotai, redux, or Context providers

**Current Impact:** None - this marketing site doesn't need shared state.

**When You'd Need It:**
- User authentication state across pages
- Shopping cart functionality
- Theme preferences persisted across pages
- Complex multi-step wizards

### Recommended Solution (If Needed)

**Zustand** - lightweight, simple API:

```bash
npm install zustand
```

```tsx
// store/useAuth.ts
import { create } from 'zustand'

interface AuthState {
  user: User | null
  login: (user: User) => void
  logout: () => void
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null })
}))

// Usage in any component
function Header() {
  const { user, logout } = useAuth()
  return user ? <button onClick={logout}>Logout</button> : <LoginLink />
}
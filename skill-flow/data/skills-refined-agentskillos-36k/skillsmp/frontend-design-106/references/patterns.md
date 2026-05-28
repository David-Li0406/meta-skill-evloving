# Patterns Reference

## Contents
- DO/DON'T Pairs
- Modal Pattern
- Tab Navigation
- Dropdown Pattern
- Form Handling

## DO/DON'T Pairs

### Card Borders

```tsx
// DO - Subtle border with hover accent
<div className="border border-gray-800 hover:border-green-500 transition-all">

// DON'T - Heavy borders that compete with content
<div className="border-4 border-white">
```

### Text Hierarchy

```tsx
// DO - Clear hierarchy with color
<h3 className="text-xl font-semibold text-white">{title}</h3>
<p className="text-gray-400">{description}</p>

// DON'T - Everything same color/weight
<h3 className="text-lg text-gray-300">{title}</h3>
<p className="text-gray-300">{description}</p>
```

### Icon Sizing

```tsx
// DO - Consistent lucide-react sizing
<CheckCircle className="w-6 h-6 text-green-400" />
<ChevronRight className="w-4 h-4" />

// DON'T - Arbitrary sizes
<CheckCircle className="w-7 h-7" />
```

### Emoji Icons

```tsx
// DO - Emojis for service cards (established pattern)
<span className="text-3xl">⚡</span>

// DON'T - Mix emojis and lucide-react in same context
<span className="text-3xl">⚡</span>
<Zap className="w-8 h-8" />  // Pick one style
```

## Modal Pattern

```tsx
{modalOpen && (
  <div 
    className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
    onClick={(e) => {
      if (e.target === e.currentTarget) {
        setModalOpen(false)
      }
    }}
  >
    <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] relative">
      {/* Close Button */}
      <button
        onClick={() => setModalOpen(false)}
        className="absolute top-4 right-4 z-10 bg-gray-100 hover:bg-gray-200 rounded-full p-2 text-gray-600 hover:text-gray-800 transition-colors"
      >
        <X className="w-6 h-6" />
      </button>
      
      {/* Modal Content */}
      <div className="p-4">{children}</div>
    </div>
  </div>
)}
```

**Key behaviors:**
- Click outside to close
- Body scroll lock via `useEffect`
- White background for contrast (Calendly embed)

## Tab Navigation

```tsx
const [activeTab, setActiveTab] = useState('overview')

{/* Tab Buttons */}
<div className="flex flex-wrap justify-center gap-4 mb-8">
  {['overview', 'integration', 'ai-engine', 'results'].map((tab) => (
    <button
      key={tab}
      onClick={() => setActiveTab(tab)}
      className={`px-6 py-2 rounded-full transition-all ${
        activeTab === tab
          ? 'bg-gradient-to-r from-yellow-600 to-orange-600'
          : 'bg-gray-800 hover:bg-gray-700'
      }`}
    >
      {tab.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
    </button>
  ))}
</div>

{/* Tab Content */}
<div className="bg-black/50 border border-gray-800 rounded-2xl p-8">
  {activeTab === 'overview' && (
    <div className="animate-fadeIn">
      {/* Content */}
    </div>
  )}
  {/* Other tabs */}
</div>
```

## Dropdown Pattern

```tsx
const [dropdownOpen, setDropdownOpen] = useState(false)

<div className="relative">
  <button
    onClick={() => setDropdownOpen(!dropdownOpen)}
    onBlur={() => setTimeout(() => setDropdownOpen(false), 200)}
    className="flex items-center gap-1 text-green-400 hover:text-yellow-400 transition-colors"
  >
    Solutions
    <ChevronDown className={`w-4 h-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
  </button>
  
  {dropdownOpen && (
    <div className="absolute top-full left-0 mt-2 w-80 bg-gray-900 border border-gray-800 rounded-lg shadow-xl z-50">
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="flex items-center gap-3 px-4 py-3 hover:bg-gray-800 hover:text-green-400 transition-colors first:rounded-t-lg last:rounded-b-lg"
          onClick={() => setDropdownOpen(false)}
        >
          <span className="text-lg">{item.icon}</span>
          <span>{item.name}</span>
        </Link>
      ))}
    </div>
  )}
</div>
```

**Note:** Uses `setTimeout` on blur to allow click events on dropdown items before closing.

## Form Handling

```tsx
const [formData, setFormData] = useState({
  firstName: '',
  lastName: '',
  email: '',
  message: ''
})
const [isSubmitting, setIsSubmitting] = useState(false)
const [isSubmitted, setIsSubmitted] = useState(false)
const [error, setError] = useState('')

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsSubmitting(true)
  setError('')

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong')
    }

    setIsSubmitted(true)
    setFormData({ firstName: '', lastName: '', email: '', message: '' })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong.')
  } finally {
    setIsSubmitting(false)
  }
}

const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  setFormData({ ...formData, [e.target.name]: e.target.value })
}
```

### Form Checklist

Copy this checklist when building forms:
- [ ] `isSubmitting` state for button disable
- [ ] `isSubmitted` state for success message
- [ ] `error` state for error display
- [ ] Clear form on success
- [ ] Disable button during submit
- [ ] Show loading spinner in button
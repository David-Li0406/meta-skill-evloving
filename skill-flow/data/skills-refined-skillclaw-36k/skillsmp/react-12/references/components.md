# Components Reference

## Contents
- Component Structure
- Page Layout Pattern
- Data-Driven Rendering
- Conditional Rendering

## Component Structure

### Standard Page Component

```tsx
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'
import { ChevronRight } from 'lucide-react'

export default function PageName() {
  const [state, setState] = useState(initialValue)

  useEffect(() => {
    // side effects
  }, [])

  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      {/* Page content */}
      <Footer />
    </div>
  )
}
```

### Import Order

1. `'use client'` directive (if needed)
2. React imports (`useState`, `useEffect`)
3. Next.js imports (`Link`, `Image`, `Script`)
4. Local components (`@/app/components/...`)
5. Third-party icons (`lucide-react`)

## Page Layout Pattern

Every page wraps content with shared Navigation and Footer:

```tsx
export default function SolutionPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      
      {/* Hero Section */}
      <section className="px-6 py-16 max-w-7xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          Page Title
        </h1>
      </section>
      
      {/* Content Sections */}
      <section className="px-6 py-16 bg-gray-900/50">
        {/* Grid cards, features, etc. */}
      </section>
      
      <Footer />
    </div>
  )
}
```

## Data-Driven Rendering

### Static Data Arrays

Content stored as component-level arrays:

```tsx
const services = [
  {
    icon: '⚡',
    title: 'Engineer Efficiency',
    description: 'Free up engineers to solve complex problems',
    slug: 'engineer-efficiency',
    colorClass: 'from-green-500 to-green-400'
  },
  // ... more items
]

// Render with .map()
{services.map((service, index) => (
  <div key={index} className="bg-gray-900 rounded-lg p-6">
    <span>{service.icon}</span>
    <h3>{service.title}</h3>
    <p>{service.description}</p>
    <Link href={`/solutions/${service.slug}`}>Learn More</Link>
  </div>
))}
```

### Navigation Items

```tsx
const solutions = [
  { name: 'Engineer Efficiency', href: '/solutions/engineer-efficiency', icon: '⚡' },
  { name: 'Service Desk Management', href: '/solutions/service-desk-management', icon: '📊' },
]

{solutions.map((item) => (
  <Link
    key={item.href}
    href={item.href}
    className="flex items-center gap-3 px-4 py-3 hover:bg-gray-800"
  >
    <span>{item.icon}</span>
    <span>{item.name}</span>
  </Link>
))}
```

## Conditional Rendering

### Tab Content

```tsx
const [activeTab, setActiveTab] = useState('overview')

{activeTab === 'overview' && (
  <div className="animate-fadeIn">
    {/* Overview content */}
  </div>
)}

{activeTab === 'integration' && (
  <div className="animate-fadeIn">
    {/* Integration content */}
  </div>
)}
```

### Expanded Accordion Items

```tsx
const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null)

{faqs.map((faq, index) => (
  <div key={index}>
    <button onClick={() => setExpandedFAQ(expandedFAQ === index ? null : index)}>
      {faq.question}
    </button>
    
    {expandedFAQ === index && (
      <div className="animate-fadeIn">
        {faq.answer}
      </div>
    )}
  </div>
))}
```

### Success/Error States

```tsx
{error && (
  <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-300">
    {error}
  </div>
)}

{isSubmitted && (
  <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4 text-green-300">
    Thank you! We'll get back to you within 24 hours.
  </div>
)}
```

## WARNING: Key Prop Anti-Pattern

**The Problem:**

```tsx
// BAD - Using array index as key in dynamic lists
{items.map((item, index) => (
  <DynamicItem key={index} {...item} />
))}
```

**Why This Breaks:**
1. Incorrect reconciliation when items reorder
2. State gets attached to wrong items
3. Performance issues with list mutations

**The Fix:**

```tsx
// GOOD - Use stable unique IDs
{items.map((item) => (
  <DynamicItem key={item.id} {...item} />
))}

// For static content that never reorders, index is acceptable
{staticNavItems.map((item, index) => (
  <StaticLink key={index} {...item} />
))}
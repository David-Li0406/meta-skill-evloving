# TakeOff UI Components Reference

This document provides quick reference for commonly used TakeOff UI components with Tailwind CSS integration.

## Overview

TakeOff UI is a framework-agnostic design system built with Stencil.js with official React bindings. All components support Tailwind CSS styling through the plugin.

**Key Features:**
- Framework-agnostic web components
- Official React bindings (@takeoff-ui/react)
- Full Tailwind CSS integration
- Accessible (WCAG 2.1 AA)
- Customizable theming
- TypeScript support

**Documentation:** https://www.takeoffui.com/docs/Components/Overview
**MCP Server:** Use `takeoff-ui-mcp` for AI-assisted component discovery

## Installation

```bash
npm install @takeoff-ui/core @takeoff-ui/react
```

```tsx
// src/main.tsx
import '@takeoff-ui/core/dist/core/core.css'
```

## Component Usage Guidelines

### Before Using a Component

1. **Search MCP first:**
   ```
   Use takeoff-ui-mcp: Show me button component with variants
   ```

2. **Check documentation:** https://www.takeoffui.com/docs/Components/Overview

3. **Request approval:** Explain why this component reduces complexity

4. **Document usage:** Add comment with approval date and reason

### Component Approval Workflow

```tsx
/**
 * Component: TkDataGrid
 * Approved: 2026-01-21
 * Reason: Built-in filtering, sorting, pagination reduces 200+ lines of code
 * Replaces: Custom table implementation
 */
import { TkDataGrid } from '@takeoff-ui/react'
```

## Common Components

### Buttons

```tsx
import { TkButton } from '@takeoff-ui/react'

// Variants
<TkButton label="Primary" variant="primary" />
<TkButton label="Secondary" variant="secondary" />
<TkButton label="Outline" variant="outline" />
<TkButton label="Ghost" variant="ghost" />
<TkButton label="Danger" variant="danger" />

// Sizes
<TkButton label="Small" size="small" />
<TkButton label="Medium" size="medium" />
<TkButton label="Large" size="large" />

// States
<TkButton label="Loading" loading={true} />
<TkButton label="Disabled" disabled={true} />

// With icon
<TkButton label="Save" icon="save" iconPosition="left" />

// Full width
<TkButton label="Submit" className="w-full" />

// Tailwind customization
<TkButton
  label="Custom"
  className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
/>
```

### Inputs

```tsx
import { TkInput } from '@takeoff-ui/react'

// Basic
<TkInput
  type="text"
  placeholder="Enter text"
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>

// With label
<div className="space-y-1">
  <label htmlFor="email" className="block text-sm font-medium">
    Email
  </label>
  <TkInput
    id="email"
    type="email"
    placeholder="your@email.com"
  />
</div>

// With error
<TkInput
  type="text"
  value={value}
  className="border-red-500"
/>
<p className="text-xs text-red-500 mt-1">This field is required</p>

// Disabled
<TkInput type="text" disabled={true} />

// With icon (using Tailwind)
<div className="relative">
  <TkInput type="search" className="pl-10" />
  <div className="absolute inset-y-0 left-0 pl-3 flex items-center">
    🔍
  </div>
</div>
```

### Select

```tsx
import { TkSelect } from '@takeoff-ui/react'

<TkSelect
  value={selected}
  onChange={(e) => setSelected(e.target.value)}
>
  <option value="">Select an option</option>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
  <option value="3">Option 3</option>
</TkSelect>

// Multi-select
<TkSelect
  multiple
  value={selectedMultiple}
  onChange={(e) => {
    const values = Array.from(e.target.selectedOptions, option => option.value)
    setSelectedMultiple(values)
  }}
>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
  <option value="3">Option 3</option>
</TkSelect>
```

### Badge

```tsx
import { TkBadge } from '@takeoff-ui/react'

// Variants
<TkBadge label="Default" />
<TkBadge label="Success" variant="success" />
<TkBadge label="Warning" variant="warning" />
<TkBadge label="Error" variant="error" />
<TkBadge label="Info" variant="info" />

// Tailwind customization
<TkBadge
  label="Active"
  className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-semibold"
/>

// With icon
<TkBadge label="5 New" icon="notification" />

// Size variations
<TkBadge label="Small" className="text-xs px-2 py-0.5" />
<TkBadge label="Large" className="text-sm px-4 py-2" />
```

### Modal/Dialog

```tsx
import { TkModal, TkButton } from '@takeoff-ui/react'
import { useState } from 'react'

function Example() {
  const [isOpen, setIsOpen] = useState(false)
  
  return (
    <>
      <TkButton label="Open Modal" onClick={() => setIsOpen(true)} />
      
      <TkModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Modal Title"
      >
        <div className="p-6">
          <p>Modal content goes here</p>
          
          <div className="flex justify-end gap-3 mt-6">
            <TkButton
              label="Cancel"
              variant="outline"
              onClick={() => setIsOpen(false)}
            />
            <TkButton
              label="Confirm"
              onClick={() => {
                // Handle confirm
                setIsOpen(false)
              }}
            />
          </div>
        </div>
      </TkModal>
    </>
  )
}

// Full-screen modal
<TkModal
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  className="max-w-full h-full"
>
  {/* Content */}
</TkModal>
```

### Card

```tsx
import { TkCard } from '@takeoff-ui/react'

<TkCard className="p-6">
  <h3 className="text-lg font-semibold mb-2">Card Title</h3>
  <p className="text-gray-600">Card content goes here</p>
</TkCard>

// With header and footer
<TkCard>
  <div className="px-6 py-4 border-b">
    <h3 className="text-lg font-semibold">Header</h3>
  </div>
  <div className="p-6">
    <p>Content</p>
  </div>
  <div className="px-6 py-4 bg-gray-50 border-t">
    <TkButton label="Action" />
  </div>
</TkCard>

// Hover effect
<TkCard className="p-6 transition-shadow hover:shadow-lg cursor-pointer">
  <p>Clickable card</p>
</TkCard>
```

### Tabs

```tsx
import { TkTabs, TkTab, TkTabPanel } from '@takeoff-ui/react'
import { useState } from 'react'

function Example() {
  const [activeTab, setActiveTab] = useState('tab1')
  
  return (
    <TkTabs value={activeTab} onChange={setActiveTab}>
      <div className="border-b">
        <TkTab value="tab1" label="Tab 1" />
        <TkTab value="tab2" label="Tab 2" />
        <TkTab value="tab3" label="Tab 3" />
      </div>
      
      <TkTabPanel value="tab1" className="p-6">
        <p>Tab 1 content</p>
      </TkTabPanel>
      
      <TkTabPanel value="tab2" className="p-6">
        <p>Tab 2 content</p>
      </TkTabPanel>
      
      <TkTabPanel value="tab3" className="p-6">
        <p>Tab 3 content</p>
      </TkTabPanel>
    </TkTabs>
  )
}
```

### Toast/Notification

```tsx
import { TkToast, showToast } from '@takeoff-ui/react'

// Show toast programmatically
showToast({
  title: 'Success',
  message: 'Operation completed successfully',
  variant: 'success',
  duration: 3000,
})

showToast({
  title: 'Error',
  message: 'Something went wrong',
  variant: 'error',
})

// Usage in component
function Example() {
  const handleSave = () => {
    try {
      // Save logic
      showToast({
        title: 'Saved',
        message: 'Changes saved successfully',
        variant: 'success',
      })
    } catch (error) {
      showToast({
        title: 'Error',
        message: error.message,
        variant: 'error',
      })
    }
  }
  
  return <TkButton label="Save" onClick={handleSave} />
}
```

### Dropdown Menu

```tsx
import { TkDropdown, TkDropdownItem } from '@takeoff-ui/react'

<TkDropdown trigger={<TkButton label="Options" />}>
  <TkDropdownItem onClick={() => console.log('Edit')}>
    Edit
  </TkDropdownItem>
  <TkDropdownItem onClick={() => console.log('Delete')}>
    Delete
  </TkDropdownItem>
  <TkDropdownItem onClick={() => console.log('Share')}>
    Share
  </TkDropdownItem>
</TkDropdown>

// With icons
<TkDropdown trigger={<TkButton label="Actions" icon="more" />}>
  <TkDropdownItem icon="edit">Edit</TkDropdownItem>
  <TkDropdownItem icon="delete" className="text-red-600">
    Delete
  </TkDropdownItem>
</TkDropdown>

// Nested dropdown
<TkDropdown trigger={<TkButton label="Menu" />}>
  <TkDropdownItem>Option 1</TkDropdownItem>
  <TkDropdown trigger={<TkDropdownItem>More Options</TkDropdownItem>}>
    <TkDropdownItem>Sub-option 1</TkDropdownItem>
    <TkDropdownItem>Sub-option 2</TkDropdownItem>
  </TkDropdown>
</TkDropdown>
```

### Checkbox & Radio

```tsx
import { TkCheckbox, TkRadio } from '@takeoff-ui/react'

// Checkbox
<TkCheckbox
  checked={checked}
  onChange={(e) => setChecked(e.target.checked)}
  label="Accept terms"
/>

// Checkbox group
<div className="space-y-2">
  <TkCheckbox label="Option 1" />
  <TkCheckbox label="Option 2" />
  <TkCheckbox label="Option 3" />
</div>

// Radio
<div className="space-y-2">
  <TkRadio
    name="option"
    value="1"
    checked={selected === '1'}
    onChange={() => setSelected('1')}
    label="Option 1"
  />
  <TkRadio
    name="option"
    value="2"
    checked={selected === '2'}
    onChange={() => setSelected('2')}
    label="Option 2"
  />
</div>
```

### Spinner/Loading

```tsx
import { TkSpinner } from '@takeoff-ui/react'

// Sizes
<TkSpinner size="small" />
<TkSpinner size="medium" />
<TkSpinner size="large" />

// Custom color
<TkSpinner className="text-blue-600" />

// Centered
<div className="flex items-center justify-center min-h-screen">
  <TkSpinner size="large" />
</div>

// With text
<div className="flex flex-col items-center gap-3">
  <TkSpinner />
  <p className="text-gray-600">Loading...</p>
</div>
```

### DataGrid/Table

```tsx
import { TkDataGrid } from '@takeoff-ui/react'

<TkDataGrid
  data={users}
  columns={[
    { key: 'name', label: 'Name', sortable: true },
    { key: 'email', label: 'Email', sortable: true },
    { key: 'role', label: 'Role', filterable: true },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="flex gap-2">
          <TkButton label="Edit" size="small" onClick={() => handleEdit(row)} />
          <TkButton label="Delete" size="small" variant="danger" onClick={() => handleDelete(row)} />
        </div>
      ),
    },
  ]}
  pagination
  pageSize={10}
  enableSearch
  onRowClick={(row) => console.log('Row clicked:', row)}
/>

// With custom cell rendering
<TkDataGrid
  data={products}
  columns={[
    {
      key: 'status',
      label: 'Status',
      render: (row) => (
        <TkBadge
          label={row.status}
          variant={row.status === 'active' ? 'success' : 'error'}
        />
      ),
    },
  ]}
/>
```

## Tailwind CSS Integration

### Using Tailwind with TakeOff UI

```tsx
// Combining TakeOff components with Tailwind
<div className="max-w-4xl mx-auto p-6">
  <div className="bg-white rounded-lg shadow-md p-6">
    <h1 className="text-2xl font-bold mb-4">Form Title</h1>
    
    <div className="grid grid-cols-2 gap-4 mb-6">
      <TkInput placeholder="First Name" />
      <TkInput placeholder="Last Name" />
    </div>
    
    <div className="flex justify-end gap-3">
      <TkButton label="Cancel" variant="outline" />
      <TkButton label="Submit" />
    </div>
  </div>
</div>
```

### Responsive Design

```tsx
// Mobile-first responsive layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <TkCard className="p-4">Card 1</TkCard>
  <TkCard className="p-4">Card 2</TkCard>
  <TkCard className="p-4">Card 3</TkCard>
</div>

// Responsive button
<TkButton
  label="Action"
  className="w-full md:w-auto"
/>

// Hide/show on breakpoints
<TkButton
  label="Mobile Only"
  className="block md:hidden"
/>

<TkButton
  label="Desktop Only"
  className="hidden md:block"
/>
```

### Dark Mode Support

```tsx
// Using Tailwind dark mode classes
<div className="bg-white dark:bg-gray-800">
  <TkCard className="bg-gray-50 dark:bg-gray-700">
    <h3 className="text-gray-900 dark:text-white">Title</h3>
    <p className="text-gray-600 dark:text-gray-300">Description</p>
  </TkCard>
</div>
```

## Component Request Process

When you need a component not listed here:

1. **Search MCP:**
   ```
   Use takeoff-ui-mcp: Find components for [use case]
   ```

2. **Check documentation:**
   Visit https://www.takeoffui.com/docs/Components/Overview

3. **Propose to user:**
   ```
   I found TkComponentName in TakeOff UI that provides [features].
   This will reduce [X lines] of code and improve [benefits].
   
   Should I use this component?
   ```

4. **Wait for approval** before implementing

5. **Document the decision:**
   ```tsx
   /**
    * Component: TkComponentName
    * Approved: [date]
    * Reason: [justification]
    */
   ```

## Best Practices

1. **Always use Tailwind** - No custom CSS files
2. **Compose components** - Build complex UIs from simple components
3. **Maintain consistency** - Use design tokens from Tailwind config
4. **Accessibility first** - TakeOff components are accessible by default
5. **Mobile-first** - Design for mobile, enhance for desktop
6. **Request approval** - Don't use new components without permission
7. **Document usage** - Add comments explaining component choices
8. **Leverage MCP** - Use takeoff-ui-mcp for discovery and examples

## Common Patterns

### Form Layout

```tsx
<div className="max-w-2xl mx-auto p-6">
  <div className="bg-white rounded-lg shadow p-6">
    <h2 className="text-xl font-bold mb-6">User Information</h2>
    
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div>
        <label className="block text-sm font-medium mb-1">First Name</label>
        <TkInput type="text" placeholder="John" />
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-1">Last Name</label>
        <TkInput type="text" placeholder="Doe" />
      </div>
    </div>
    
    <div className="mb-6">
      <label className="block text-sm font-medium mb-1">Email</label>
      <TkInput type="email" placeholder="john@example.com" />
    </div>
    
    <div className="flex justify-end gap-3 pt-4 border-t">
      <TkButton label="Cancel" variant="outline" />
      <TkButton label="Save" />
    </div>
  </div>
</div>
```

### Dashboard Layout

```tsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b px-6 py-4">
    <h1 className="text-2xl font-bold">Dashboard</h1>
  </header>
  
  {/* Stats */}
  <div className="p-6">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <TkCard className="p-6">
        <p className="text-gray-600 text-sm">Total Users</p>
        <p className="text-3xl font-bold">1,234</p>
      </TkCard>
      <TkCard className="p-6">
        <p className="text-gray-600 text-sm">Revenue</p>
        <p className="text-3xl font-bold">$45,678</p>
      </TkCard>
      <TkCard className="p-6">
        <p className="text-gray-600 text-sm">Active</p>
        <p className="text-3xl font-bold">89%</p>
      </TkCard>
    </div>
    
    {/* Data table */}
    <TkCard>
      <TkDataGrid data={data} columns={columns} />
    </TkCard>
  </div>
</div>
```

## Summary

TakeOff UI provides enterprise-grade components with full Tailwind integration. Always:

- Use MCP for discovery
- Request approval for new components
- Document component choices
- Style with Tailwind only
- Follow accessibility guidelines

For complete component documentation, visit https://www.takeoffui.com/docs/Components/Overview or use the MCP server.
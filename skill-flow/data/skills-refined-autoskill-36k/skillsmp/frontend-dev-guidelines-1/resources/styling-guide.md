# Styling Guide

## Overview

ActionPhase uses Tailwind CSS for utility-first styling combined with a custom UI component library that provides consistent, dark-mode-aware components.

## Component Priority

### 1. Use UI Component Library (Primary)

Always prefer the ActionPhase UI component library for standard elements:

```tsx
// ✅ CORRECT - Use UI components
import { Button, Input, Card, CardBody, Badge, Alert, Spinner } from '@/components/ui';

<Button variant="primary" onClick={handleSubmit}>
  Submit
</Button>

<Card variant="elevated" padding="md">
  <CardBody>
    <Input label="Email" type="email" value={email} onChange={setEmail} />
  </CardBody>
</Card>

// ❌ WRONG - Don't use native HTML for interactive elements
<button className="bg-blue-500 text-white px-4 py-2 rounded">
  Submit
</button>
```

### 2. Use Tailwind for Layout

Use Tailwind utilities for layout, spacing, and positioning:

```tsx
// Layout with Tailwind
<div className="flex flex-col gap-4">
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <Card>...</Card>
    <Card>...</Card>
  </div>
</div>

// Spacing and alignment
<div className="p-4 mx-auto max-w-7xl">
  <div className="flex items-center justify-between mb-6">
    <h1 className="text-2xl font-bold">Dashboard</h1>
    <Button variant="primary">New Game</Button>
  </div>
</div>
```

### 3. Use CSS Variables for Colors (Critical)

**⚠️ CRITICAL RULE:** Never use hardcoded colors or manual dark mode classes. Always use CSS variables.

```tsx
// ✅ CORRECT - CSS variables adapt to theme
<div className="bg-bg-primary text-text-primary border-border-primary">
  <h2 className="text-text-heading">Welcome</h2>
  <p className="text-text-secondary">Select a game to continue</p>
</div>

// ❌ WRONG - Never use hardcoded colors
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  Don't do this!
</div>

// ❌ WRONG - Never use Tailwind color utilities directly
<div className="bg-gray-100 text-blue-600">
  This breaks dark mode!
</div>
```

## Dark Mode Patterns

### CSS Variable Reference

| Variable | Usage | Light Mode | Dark Mode |
|----------|-------|------------|-----------|
| `bg-bg-primary` | Main backgrounds | White | Dark gray |
| `bg-bg-secondary` | Secondary backgrounds | Light gray | Darker gray |
| `bg-bg-elevated` | Elevated surfaces | White + shadow | Dark gray + border |
| `text-text-heading` | Headings | Dark gray | White |
| `text-text-primary` | Body text | Gray | Light gray |
| `text-text-secondary` | Muted text | Light gray | Darker gray |
| `border-border-primary` | Borders | Light gray | Dark gray |

### Examples

```tsx
// Card with proper theming
<Card variant="default" padding="md">
  <CardBody>
    <h3 className="text-text-heading text-lg font-semibold mb-2">
      Game Stats
    </h3>
    <p className="text-text-primary">
      You have {gameCount} active games
    </p>
    <p className="text-text-secondary text-sm">
      Last updated 5 minutes ago
    </p>
  </CardBody>
</Card>

// Custom container with theming
<div className="bg-bg-secondary rounded-lg p-6">
  <div className="bg-bg-primary rounded border border-border-primary p-4">
    <Badge variant="success">Active</Badge>
  </div>
</div>
```

## UI Component Library Reference

### Available Components

```tsx
// Buttons
<Button variant="primary">Primary Action</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="danger">Delete</Button>
<Button variant="ghost">Cancel</Button>

// Form Inputs
<Input
  label="Username"
  type="text"
  placeholder="Enter username"
  error={errors.username}
  required
/>

<Textarea
  label="Description"
  rows={4}
  value={description}
  onChange={(e) => setDescription(e.target.value)}
/>

<Select label="Game Type" value={gameType} onChange={setGameType}>
  <option value="casual">Casual</option>
  <option value="ranked">Ranked</option>
</Select>

// Cards
<Card variant="default" padding="md">
  <CardHeader>
    <h2>Title</h2>
  </CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>

// Feedback
<Alert variant="success" title="Success!">
  Your changes have been saved.
</Alert>

<Badge variant="warning" dot>Pending</Badge>

<Spinner size="md" />
```

## Layout Patterns

### Responsive Grid

```tsx
// Responsive columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => (
    <Card key={item.id}>...</Card>
  ))}
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fill,minmax(250px,1fr))] gap-4">
  {cards}
</div>
```

### Flexbox Layouts

```tsx
// Header layout
<header className="flex items-center justify-between p-4 border-b border-border-primary">
  <div className="flex items-center gap-4">
    <Logo />
    <Navigation />
  </div>
  <UserMenu />
</header>

// Sidebar layout
<div className="flex h-screen">
  <aside className="w-64 bg-bg-secondary p-4">
    <Navigation />
  </aside>
  <main className="flex-1 p-6 overflow-auto">
    {children}
  </main>
</div>
```

### Container Patterns

```tsx
// Page container
<div className="container mx-auto px-4 py-8 max-w-7xl">
  {content}
</div>

// Content section
<section className="mb-8">
  <h2 className="text-2xl font-bold text-text-heading mb-4">
    Section Title
  </h2>
  <div className="space-y-4">
    {items}
  </div>
</section>
```

## Form Styling

```tsx
// Form with ActionPhase components
<form onSubmit={handleSubmit} className="space-y-4">
  <Input
    label="Email"
    type="email"
    value={formData.email}
    onChange={(e) => setFormData({...formData, email: e.target.value})}
    error={errors.email}
    required
  />

  <Input
    label="Password"
    type="password"
    value={formData.password}
    onChange={(e) => setFormData({...formData, password: e.target.value})}
    error={errors.password}
    required
  />

  <div className="flex gap-2 justify-end">
    <Button variant="ghost" type="button" onClick={handleCancel}>
      Cancel
    </Button>
    <Button variant="primary" type="submit">
      Submit
    </Button>
  </div>
</form>
```

## Common Patterns

### Loading States

```tsx
// With Spinner component
{isLoading ? (
  <div className="flex items-center justify-center p-8">
    <Spinner size="lg" />
  </div>
) : (
  <Content />
)}

// Skeleton loading
<div className="animate-pulse">
  <div className="h-4 bg-bg-secondary rounded w-3/4 mb-2"></div>
  <div className="h-4 bg-bg-secondary rounded w-1/2"></div>
</div>
```

### Empty States

```tsx
<div className="text-center py-12">
  <div className="text-6xl mb-4">📭</div>
  <h3 className="text-text-heading text-lg font-semibold mb-2">
    No messages yet
  </h3>
  <p className="text-text-secondary">
    Start a conversation to see messages here
  </p>
  <Button variant="primary" className="mt-4">
    Send First Message
  </Button>
</div>
```

### Lists

```tsx
<ul className="divide-y divide-border-primary">
  {items.map(item => (
    <li key={item.id} className="py-4 hover:bg-bg-secondary transition-colors">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-text-heading font-medium">{item.title}</h4>
          <p className="text-text-secondary text-sm">{item.description}</p>
        </div>
        <Badge variant={item.status}>{item.status}</Badge>
      </div>
    </li>
  ))}
</ul>
```

## Typography

```tsx
// Headings
<h1 className="text-3xl font-bold text-text-heading">Page Title</h1>
<h2 className="text-2xl font-semibold text-text-heading">Section</h2>
<h3 className="text-xl font-medium text-text-heading">Subsection</h3>

// Body text
<p className="text-text-primary">Regular paragraph text</p>
<p className="text-text-secondary text-sm">Secondary or muted text</p>
<p className="text-text-danger">Error message text</p>

// Links (using React Router)
<Link to="/path" className="text-primary hover:underline">
  Click here
</Link>
```

## Responsive Design

### Breakpoints

| Breakpoint | Min Width | CSS Class |
|------------|-----------|-----------|
| sm | 640px | `sm:` |
| md | 768px | `md:` |
| lg | 1024px | `lg:` |
| xl | 1280px | `xl:` |
| 2xl | 1536px | `2xl:` |

### Examples

```tsx
// Responsive text size
<h1 className="text-2xl md:text-3xl lg:text-4xl">
  Responsive Heading
</h1>

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">
  Content with responsive padding
</div>

// Hide/show based on screen size
<div className="hidden md:block">
  Shows on medium screens and up
</div>
<div className="block md:hidden">
  Shows only on small screens
</div>
```

## Animation & Transitions

```tsx
// Hover effects
<Button className="transition-colors hover:bg-opacity-90">
  Hover me
</Button>

// Smooth transitions
<div className="transition-all duration-300 ease-in-out">
  Smooth animations
</div>

// Focus states
<Input className="focus:ring-2 focus:ring-primary focus:outline-none" />
```

## Best Practices

### DO ✅

- Use UI components for all interactive elements
- Use CSS variables for all colors
- Use Tailwind for layout and spacing
- Keep component files focused and small
- Test in both light and dark modes
- Use semantic HTML elements
- Add proper ARIA labels for accessibility

### DON'T ❌

- Don't use inline styles (`style={{}}`)
- Don't use hardcoded colors (`bg-white`, `text-black`)
- Don't use `dark:` classes manually
- Don't create custom buttons/inputs when UI components exist
- Don't mix styling approaches inconsistently
- Don't forget hover and focus states
- Don't ignore responsive design

## Markdown Content

For rendering markdown content, use the MarkdownPreview component:

```tsx
import { MarkdownPreview } from '@/components/MarkdownPreview';

<MarkdownPreview
  content={markdownText}
  mentionedCharacters={characters} // Optional, for @mentions
/>
```

## Testing Styles

Always verify your styling works in both themes:

1. Navigate to `/settings`
2. Toggle between Light/Dark/System
3. Verify all text is readable
4. Check all backgrounds adapt
5. Test hover and focus states
6. Check responsive breakpoints

Visit `/theme-test` to see all components in both themes side-by-side.

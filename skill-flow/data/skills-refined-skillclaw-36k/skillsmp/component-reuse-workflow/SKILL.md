---
name: component-reuse-workflow
description: Workflow that enforces component reuse by systematically searching for existing components before creating new ones. Always use existing UI components, patterns, and utilities. Only create new components when no suitable existing piece exists, and even then build on established patterns (Dialog, Sheet, etc.) instead of inventing new ones.
category: workflow
color: green
displayName: Component Reuse Workflow
---

# Component Reuse Workflow

This workflow enforces a **component-first approach** to development. Before writing any new component or UI code, you must systematically search for and evaluate existing components. Only create new components when absolutely necessary, and always build on established patterns.

## Golden Rules

1. **ALWAYS search for existing components first** - Never assume a component doesn't exist
2. **Use existing UI primitives** - Leverage `components/ui/` components before building custom solutions
3. **Build on patterns, don't invent** - When creating new components, extend existing patterns (Dialog, Sheet, AlertDialog, etc.)
4. **Check similar implementations** - Look for similar features in the codebase that might have reusable patterns
5. **Document component decisions** - When creating new components, explain why existing ones couldn't be used
6. **Make ALL components fully reusable** - Components must work anywhere in the application without modification

## Mandatory Workflow

### Step 1: Component Discovery Phase

**BEFORE writing any component code, you MUST:**

#### 1.1 Search Existing UI Components
```bash
# List all available UI components
ls components/ui/

# Search for component names matching your need
grep -r "modal\|dialog\|sheet\|popover\|drawer" components/ui/ -i
```

**Key UI Components to Check:**
- **Modals/Dialogs**: `dialog.tsx`, `alert-dialog.tsx`, `sheet.tsx`
- **Forms**: `form.tsx`, `input.tsx`, `textarea.tsx`, `select.tsx`, `checkbox.tsx`, `radio-group.tsx`
- **Layout**: `card.tsx`, `tabs.tsx`, `accordion.tsx`, `collapsible.tsx`, `separator.tsx`
- **Navigation**: `dropdown-menu.tsx`, `context-menu.tsx`, `navigation-menu.tsx`, `breadcrumb.tsx`
- **Feedback**: `toast.tsx`, `alert.tsx`, `progress.tsx`, `skeleton.tsx`
- **Data Display**: `table.tsx`, `badge.tsx`, `avatar.tsx`, `chart.tsx`
- **Overlays**: `popover.tsx`, `hover-card.tsx`, `tooltip.tsx`

#### 1.2 Search Component Directory Structure
```bash
# Check for domain-specific components
ls components/enterprise/
ls components/admin/
ls components/group/
ls components/entity/
ls components/feed/
```

#### 1.3 Semantic Search for Similar Implementations
Use codebase search to find similar features:
- "How are modals implemented?"
- "Where are forms with validation used?"
- "How are data tables displayed?"
- "Where are dialogs with forms used?"

#### 1.4 Check for Reusable Patterns
Look for:
- Similar feature implementations in other parts of the app
- Shared component patterns (e.g., all modals use Dialog)
- Utility functions or hooks that might help
- Existing styling patterns or design tokens

### Step 2: Component Evaluation

For each potential existing component, evaluate:

#### 2.1 Functional Fit
- ✅ **Perfect match**: Component does exactly what you need
- ⚠️ **Near match**: Component can be adapted with props/styling
- ❌ **No match**: Component doesn't serve the purpose

#### 2.2 Pattern Compatibility
- Does it follow the same pattern as other components in the codebase?
- Is it built on the same primitives (Radix UI, shadcn/ui)?
- Does it use the same styling approach (Tailwind, cn utility)?

#### 2.3 Extensibility
- Can it be extended with additional props?
- Can it be composed with other components?
- Can styling be customized via className?

### Step 3: Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│ Component Decision Flow                                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ 1. Found exact match? → USE IT                                │
│                                                               │
│ 2. Found near match? → EXTEND IT (add props, customize)      │
│                                                               │
│ 3. Found similar pattern? → BUILD ON PATTERN                 │
│    (e.g., need custom modal → extend Dialog)                 │
│                                                               │
│ 4. Nothing found? → CREATE NEW (but build on patterns)       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Step 4: Implementation Strategy

#### 4.1 Using Existing Components

**Example: Need a modal**
```typescript
// ✅ CORRECT: Use existing Dialog
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'

// ❌ WRONG: Create new Modal component
// Don't create components/ui/custom-modal.tsx
```

**Example: Need a form**
```typescript
// ✅ CORRECT: Use existing Form components
import { Form, FormField, FormItem, FormLabel, FormControl } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

// ❌ WRONG: Create custom form components
```

#### 4.2 Extending Existing Components

**When existing component is close but needs customization:**

```typescript
// ✅ CORRECT: Extend Dialog with custom props/styling
import { Dialog, DialogContent } from '@/components/ui/dialog'

<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent className="max-w-4xl h-[90vh] flex flex-col">
    {/* Custom content using existing Dialog pattern */}
  </DialogContent>
</Dialog>
```

#### 4.3 Building on Patterns (When New Component is Needed)

**If you MUST create a new component, build on existing patterns:**

**Example: Creating a custom drawer component**
```typescript
// ✅ CORRECT: Build on Sheet pattern (which is built on Dialog)
'use client'

import * as React from 'react'
import * as SheetPrimitive from '@radix-ui/react-dialog'
import { cn } from '@/lib/utils'
import { CloseButton } from '@/components/ui/close-button'

// Follow the same pattern as sheet.tsx
const Drawer = SheetPrimitive.Root
const DrawerTrigger = SheetPrimitive.Trigger
// ... follow existing patterns
```

**Example: Creating a specialized dialog variant**
```typescript
// ✅ CORRECT: Compose existing Dialog with custom wrapper
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

export function ConfirmationDialog({ ... }) {
  return (
    <Dialog>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        {/* Custom content */}
      </DialogContent>
    </Dialog>
  )
}
```

#### 4.4 What NOT to Do

**❌ DON'T:**
- Create new modal/dialog components when Dialog exists
- Create new form components when Form/Input exist
- Create new button components when Button exists
- Invent new patterns when established ones exist
- Duplicate functionality that exists elsewhere
- Create components that ignore existing design system

**✅ DO:**
- Search first, code second
- Extend before creating
- Compose before duplicating
- Follow established patterns
- Document why new component was needed

## Project-Specific Component Patterns

### Modal/Dialog Pattern
This project uses **Dialog** from `components/ui/dialog.tsx` as the primary modal pattern:
- Built on `@radix-ui/react-dialog`
- Supports large/full-screen modals via className detection
- Includes CloseButton integration
- Supports horizontal and vertical header layouts

**Use Dialog for:**
- All modal dialogs
- Forms in modals
- Confirmation dialogs
- Settings panels
- Any overlay content

**Don't use:**
- Custom Modal.tsx (legacy, prefer Dialog)
- Custom modal implementations

### Sheet Pattern
Use **Sheet** from `components/ui/sheet.tsx` for:
- Side panels
- Mobile drawers
- Slide-out panels

### Alert Dialog Pattern
Use **AlertDialog** from `components/ui/alert-dialog.tsx` for:
- Confirmation dialogs
- Destructive action confirmations
- Simple yes/no prompts

### Form Pattern
This project uses **Form** from `components/ui/form.tsx` with:
- React Hook Form integration
- Zod validation
- Consistent field patterns

## Component Discovery Commands

### Quick Component Search
```bash
# Find all dialog/modal usage
grep -r "from.*dialog" components/ app/ --include="*.tsx" --include="*.ts"

# Find all form implementations
grep -r "FormField\|FormItem" components/ app/ --include="*.tsx"

# Find all button usage patterns
grep -r "Button\|button" components/ui/ --include="*.tsx" | head -20

# List all UI components
find components/ui -name "*.tsx" -type f | sort
```

### Semantic Component Search
Use codebase search for:
- "How are [feature] implemented?"
- "Where are [component type] used?"
- "What patterns exist for [use case]?"

## Checklist Before Creating New Component

Before creating any new component, verify:

- [ ] Searched `components/ui/` for existing component
- [ ] Searched domain directories (`components/enterprise/`, `components/admin/`, etc.)
- [ ] Used codebase search to find similar implementations
- [ ] Checked if existing component can be extended with props
- [ ] Verified no similar pattern exists elsewhere
- [ ] Confirmed new component will follow existing patterns (Dialog, Sheet, etc.)
- [ ] Documented why existing components couldn't be used

## When New Component is Justified

A new component is only justified when:

1. **No existing component serves the purpose** (even with customization)
2. **No similar pattern exists** in the codebase
3. **The new component builds on established patterns** (e.g., extends Dialog)
4. **The component will be reused** in multiple places
5. **The component follows project conventions** (Radix UI, shadcn/ui patterns)

## Implementation Examples

### ✅ Good: Reusing Dialog
```typescript
// components/enterprise/create-post-modal.tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Form, FormField } from '@/components/ui/form'
import { Button } from '@/components/ui/button'

export function CreatePostModal({ open, onOpenChange }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Create Post</DialogTitle>
        </DialogHeader>
        <Form>
          {/* Form fields using existing Input, Textarea, etc. */}
        </Form>
      </DialogContent>
    </Dialog>
  )
}
```

### ✅ Good: Extending Existing Component
```typescript
// Custom variant of Dialog for full-screen modals
import { Dialog, DialogContent } from '@/components/ui/dialog'

export function FullScreenDialog({ children, ...props }) {
  return (
    <Dialog {...props}>
      <DialogContent className="max-w-full h-full max-h-screen flex flex-col">
        {children}
      </DialogContent>
    </Dialog>
  )
}
```

### ❌ Bad: Creating Duplicate Modal
```typescript
// ❌ DON'T: Create new modal when Dialog exists
export function CustomModal({ open, onClose, children }) {
  return (
    <div className="fixed inset-0 z-50">
      <div className="modal-content">
        {children}
      </div>
    </div>
  )
}
```

### ❌ Bad: Ignoring Existing Patterns
```typescript
// ❌ DON'T: Create modal without using Dialog pattern
export function MyModal() {
  // Custom implementation that doesn't use Dialog
}
```

## Integration with Other Skills

- **triage-expert**: When encountering UI issues, check if component reuse would solve it
- **code-review**: Review code for component reuse opportunities
- **refactoring-expert**: Refactor duplicate components to use shared patterns

## Success Metrics

- ✅ Existing components are discovered and used
- ✅ New components only created when necessary
- ✅ New components follow established patterns
- ✅ No duplicate functionality exists
- ✅ Component decisions are documented
- ✅ Codebase maintains consistency

## Common Mistakes to Avoid

1. **Assuming components don't exist** - Always search first
2. **Creating "just this once" components** - Use existing ones even for one-off cases
3. **Not checking domain directories** - Components might be in `enterprise/`, `admin/`, etc.
4. **Ignoring composition** - Compose existing components instead of creating new ones
5. **Breaking patterns** - Don't invent new patterns when established ones exist
6. **Not documenting decisions** - Always explain why a new component was needed

## Quick Reference

**Before writing component code:**
1. `ls components/ui/` - List available UI components
2. `grep -r "component-name" components/` - Search for usage
3. Codebase search for similar implementations
4. Check if existing component can be extended
5. Only then create new component (following patterns)

**Remember: Search first, extend second, create last.**

---

## Making Components Fully Reusable

**CRITICAL**: All components must be **fully reusable** and work anywhere in the application without modification. This means components should be **presentation-focused** and **data-agnostic**.

### Core Principles for Full Reusability

1. **Separate Data from Presentation** - Components receive data via props, never fetch it themselves
2. **No Hardcoded Dependencies** - No hardcoded API endpoints, hooks, or business logic
3. **Props-Based Everything** - Data, callbacks, and configuration come from props
4. **Container/Presentational Pattern** - Use containers for data fetching, presentational components for UI
5. **Dependency Injection** - Accept hooks, services, and utilities as props or context

### Component Architecture Patterns

#### ✅ Pattern 1: Pure Presentational Component (Ideal)

**Components that only render UI and accept all data via props:**

```typescript
// ✅ CORRECT: Fully reusable presentational component
interface FeedCardProps {
  post: {
    id: string
    text: string
    author: { id: string; name: string; avatar: string }
    engagement: { likes: number; comments: number; shares: number }
    createdAt: string
  }
  currentUserId?: string
  onLike?: (postId: string) => void
  onComment?: (postId: string) => void
  onShare?: (postId: string) => void
  className?: string
}

export function FeedCard({ post, currentUserId, onLike, onComment, onShare, className }: FeedCardProps) {
  // ✅ Pure presentation - no data fetching, no hooks, no API calls
  return (
    <Card className={className}>
      <CardHeader>
        <Avatar src={post.author.avatar} />
        <CardTitle>{post.author.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{post.text}</p>
        <EngagementBar
          likes={post.engagement.likes}
          comments={post.engagement.comments}
          shares={post.engagement.shares}
          onLike={() => onLike?.(post.id)}
          onComment={() => onComment?.(post.id)}
          onShare={() => onShare?.(post.id)}
        />
      </CardContent>
    </Card>
  )
}
```

**Usage anywhere:**
```typescript
// Can be used in any page, any context
<FeedCard
  post={postData}
  currentUserId={userId}
  onLike={handleLike}
  onComment={handleComment}
  onShare={handleShare}
/>
```

#### ✅ Pattern 2: Container Component (Data Fetching Layer)

**Separate container components handle data fetching and pass to presentational components:**

```typescript
// ✅ CORRECT: Container component handles data fetching
'use client'

import { useEffect, useState } from 'react'
import { FeedCard } from './feed-card' // Presentational component
import { useAuth } from '@/hooks/useAuth'

export function FeedCardContainer({ postId }: { postId: string }) {
  const { user } = useAuth()
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/posts/${postId}`)
      .then(r => r.json())
      .then(data => {
        setPost(data)
        setLoading(false)
      })
  }, [postId])

  const handleLike = async (id: string) => {
    await fetch(`/api/posts/${id}/like`, { method: 'POST' })
    // Refresh data
  }

  if (loading) return <Skeleton />
  if (!post) return null

  // ✅ Presentational component receives all data via props
  return (
    <FeedCard
      post={post}
      currentUserId={user?.id}
      onLike={handleLike}
      onComment={handleComment}
      onShare={handleShare}
    />
  )
}
```

#### ❌ Pattern 3: Mixed Component (NOT Reusable)

**Components that mix data fetching with presentation are NOT reusable:**

```typescript
// ❌ WRONG: Component has hardcoded API calls
export function FeedCard({ postId }: { postId: string }) {
  const [post, setPost] = useState(null)
  
  useEffect(() => {
    // ❌ Hardcoded API endpoint - not reusable
    fetch(`/api/posts/${postId}`)
      .then(r => r.json())
      .then(setPost)
  }, [postId])

  // ❌ Hardcoded engagement API - not reusable
  const handleLike = async () => {
    await fetch(`/api/posts/${postId}/like`, { method: 'POST' })
  }

  return <Card>...</Card>
}
```

**Problems:**
- Can't be used with different data sources
- Can't be tested without API mocks
- Can't be used in different contexts
- Tightly coupled to specific API structure

### Refactoring Guide: Making Components Reusable

#### Step 1: Identify Non-Reusable Patterns

**Red Flags:**
- ❌ Direct `fetch()` calls inside component
- ❌ `useAuth()` or other hooks that fetch data
- ❌ Hardcoded API endpoints (`/api/...`)
- ❌ Business logic mixed with presentation
- ❌ Direct database queries or Supabase calls
- ❌ Context dependencies that assume specific providers

#### Step 2: Extract Data Fetching

**Before (Non-Reusable):**
```typescript
// ❌ Component fetches its own data
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser)
  }, [userId])

  return <div>{user?.name}</div>
}
```

**After (Reusable):**
```typescript
// ✅ Presentational component accepts data via props
interface UserProfileProps {
  user: {
    id: string
    name: string
    avatar?: string
    bio?: string
  }
  className?: string
}

export function UserProfile({ user, className }: UserProfileProps) {
  return (
    <div className={className}>
      <Avatar src={user.avatar} />
      <h2>{user.name}</h2>
      {user.bio && <p>{user.bio}</p>}
    </div>
  )
}

// ✅ Container component handles data fetching
export function UserProfileContainer({ userId }: { userId: string }) {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser)
  }, [userId])

  if (!user) return <Skeleton />
  
  return <UserProfile user={user} />
}
```

#### Step 3: Extract Callbacks and Actions

**Before (Non-Reusable):**
```typescript
// ❌ Component handles actions internally
export function LikeButton({ postId }: { postId: string }) {
  const handleClick = async () => {
    // ❌ Hardcoded API call
    await fetch(`/api/posts/${postId}/like`, { method: 'POST' })
  }
  
  return <Button onClick={handleClick}>Like</Button>
}
```

**After (Reusable):**
```typescript
// ✅ Component accepts callback via props
interface LikeButtonProps {
  liked: boolean
  count: number
  onLike: () => void | Promise<void>
  className?: string
}

export function LikeButton({ liked, count, onLike, className }: LikeButtonProps) {
  return (
    <Button
      variant={liked ? 'default' : 'outline'}
      onClick={onLike}
      className={className}
    >
      <Heart className={liked ? 'fill-red-500' : ''} />
      {count}
    </Button>
  )
}

// ✅ Container provides the callback
export function LikeButtonContainer({ postId }: { postId: string }) {
  const [liked, setLiked] = useState(false)
  const [count, setCount] = useState(0)
  
  const handleLike = async () => {
    await fetch(`/api/posts/${postId}/like`, { method: 'POST' })
    setLiked(!liked)
    setCount(prev => liked ? prev - 1 : prev + 1)
  }
  
  return <LikeButton liked={liked} count={count} onLike={handleLike} />
}
```

#### Step 4: Extract Hook Dependencies

**Before (Non-Reusable):**
```typescript
// ❌ Component directly uses hook
export function UserMenu() {
  const { user } = useAuth() // ❌ Assumes UserContext exists
  
  return <DropdownMenu>
    <DropdownMenuItem>{user?.name}</DropdownMenuItem>
  </DropdownMenu>
}
```

**After (Reusable):**
```typescript
// ✅ Component accepts user data via props
interface UserMenuProps {
  user: {
    id: string
    name: string
    avatar?: string
  }
  onProfileClick?: () => void
  onSettingsClick?: () => void
  onLogout?: () => void
}

export function UserMenu({ user, onProfileClick, onSettingsClick, onLogout }: UserMenuProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger>
        <Avatar src={user.avatar} />
        {user.name}
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={onProfileClick}>Profile</DropdownMenuItem>
        <DropdownMenuItem onClick={onSettingsClick}>Settings</DropdownMenuItem>
        <DropdownMenuItem onClick={onLogout}>Logout</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

// ✅ Container provides user data
export function UserMenuContainer() {
  const { user } = useAuth()
  
  if (!user) return null
  
  return (
    <UserMenu
      user={user}
      onProfileClick={() => router.push(`/profile/${user.id}`)}
      onSettingsClick={() => router.push('/settings')}
      onLogout={handleLogout}
    />
  )
}
```

### Component Reusability Checklist

Before creating or modifying a component, ensure:

- [ ] **No hardcoded API calls** - All data comes from props
- [ ] **No direct hook usage for data** - Hooks only in container components
- [ ] **All callbacks via props** - Actions passed as function props
- [ ] **No business logic** - Only presentation logic in component
- [ ] **No context assumptions** - Component doesn't assume specific providers
- [ ] **Type-safe props** - All props properly typed with interfaces
- [ ] **Optional dependencies** - Hooks, services can be injected or optional
- [ ] **Works in isolation** - Component can be used without specific setup
- [ ] **Testable** - Component can be tested with mock data
- [ ] **Documented** - Props and usage clearly documented

### Examples: Refactoring Non-Reusable Components

#### Example 1: Feed Card Component

**Current (Non-Reusable):**
```typescript
// ❌ components/entity-feed-card.tsx - Has hardcoded API calls
export default function EntityFeedCard({ post }: { post: Post }) {
  const fetchComments = useCallback(async () => {
    // ❌ Hardcoded API endpoint
    const response = await fetch(`/api/engagement?entity_id=${post.id}&entity_type=post`)
    const data = await response.json()
    setComments(data.recent_comments)
  }, [post.id])
  
  // ❌ Direct useAuth hook
  const { user } = useAuth()
  
  return <Card>...</Card>
}
```

**Refactored (Reusable):**
```typescript
// ✅ Presentational component
interface FeedCardProps {
  post: Post
  comments?: Comment[]
  currentUser?: User
  onLoadComments?: (postId: string) => Promise<Comment[]>
  onLike?: (postId: string) => Promise<void>
  onComment?: (postId: string, text: string) => Promise<void>
  className?: string
}

export function FeedCard({
  post,
  comments = [],
  currentUser,
  onLoadComments,
  onLike,
  onComment,
  className
}: FeedCardProps) {
  // ✅ All data and actions come from props
  return <Card className={className}>...</Card>
}

// ✅ Container component handles data fetching
export function FeedCardContainer({ postId }: { postId: string }) {
  const { user } = useAuth()
  const [post, setPost] = useState<Post | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  
  useEffect(() => {
    fetch(`/api/posts/${postId}`).then(r => r.json()).then(setPost)
  }, [postId])
  
  const handleLoadComments = async (id: string) => {
    const response = await fetch(`/api/engagement?entity_id=${id}&entity_type=post`)
    const data = await response.json()
    setComments(data.recent_comments)
    return data.recent_comments
  }
  
  if (!post) return <Skeleton />
  
  return (
    <FeedCard
      post={post}
      comments={comments}
      currentUser={user}
      onLoadComments={handleLoadComments}
      onLike={handleLike}
      onComment={handleComment}
    />
  )
}
```

#### Example 2: Link Preview Component

**Current (Non-Reusable):**
```typescript
// ❌ Has hardcoded API calls
export function EnterpriseLinkPreviewCard({ url }: { url: string }) {
  useEffect(() => {
    // ❌ Hardcoded API endpoint
    fetch('/api/link-preview', {
      method: 'POST',
      body: JSON.stringify({ url })
    }).then(r => r.json()).then(setMetadata)
  }, [url])
  
  return <Card>...</Card>
}
```

**Refactored (Reusable):**
```typescript
// ✅ Presentational component
interface LinkPreviewCardProps {
  metadata: LinkPreviewMetadata
  onRefresh?: () => Promise<LinkPreviewMetadata>
  className?: string
}

export function LinkPreviewCard({ metadata, onRefresh, className }: LinkPreviewCardProps) {
  return <Card className={className}>...</Card>
}

// ✅ Container component
export function LinkPreviewCardContainer({ url }: { url: string }) {
  const [metadata, setMetadata] = useState<LinkPreviewMetadata | null>(null)
  
  useEffect(() => {
    fetch('/api/link-preview', {
      method: 'POST',
      body: JSON.stringify({ url })
    }).then(r => r.json()).then(setMetadata)
  }, [url])
  
  const handleRefresh = async () => {
    const response = await fetch('/api/link-preview', {
      method: 'POST',
      body: JSON.stringify({ url, refresh: true })
    })
    const data = await response.json()
    setMetadata(data.data)
    return data.data
  }
  
  if (!metadata) return <Skeleton />
  
  return <LinkPreviewCard metadata={metadata} onRefresh={handleRefresh} />
}
```

### Component Organization Structure

**Recommended structure for reusable components:**

```
components/
  ui/                          # Pure UI primitives (Button, Dialog, etc.)
    button.tsx                 # ✅ Fully reusable, no dependencies
    dialog.tsx                 # ✅ Fully reusable, no dependencies
  
  feed/                        # Domain-specific presentational components
    feed-card.tsx              # ✅ Presentational - accepts data via props
    feed-card-container.tsx    # ✅ Container - handles data fetching
    feed-list.tsx              # ✅ Presentational - accepts items array
  
  enterprise/                  # Enterprise features
    engagement-actions.tsx     # ✅ Presentational - accepts callbacks
    engagement-actions-container.tsx  # ✅ Container - handles API calls
```

### Migration Strategy

When refactoring existing components to be fully reusable:

1. **Identify the component** that needs refactoring
2. **Extract presentational logic** - Remove all data fetching, API calls, hooks
3. **Create props interface** - Define all data and callbacks as props
4. **Create container component** - Move data fetching to container
5. **Update usages** - Replace old component with container where needed
6. **Test both** - Ensure presentational component works with mock data
7. **Document** - Add JSDoc comments explaining props and usage

### Benefits of Fully Reusable Components

✅ **Works anywhere** - Use in any page, any context, any app
✅ **Easy to test** - Test with mock data, no API mocks needed
✅ **Flexible** - Can be used with different data sources
✅ **Maintainable** - Clear separation of concerns
✅ **Composable** - Easy to combine with other components
✅ **Type-safe** - Props are fully typed
✅ **Reusable** - Write once, use everywhere

### Anti-Patterns to Avoid

❌ **Don't mix data fetching with presentation**
```typescript
// ❌ WRONG
export function Component() {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData)
  }, [])
  return <div>{data?.name}</div>
}
```

❌ **Don't use hooks directly in presentational components**
```typescript
// ❌ WRONG
export function Component() {
  const { user } = useAuth() // Assumes context exists
  return <div>{user?.name}</div>
}
```

❌ **Don't hardcode API endpoints**
```typescript
// ❌ WRONG
const response = await fetch('/api/posts/123') // Hardcoded
```

❌ **Don't assume specific contexts or providers**
```typescript
// ❌ WRONG
export function Component() {
  const context = useContext(SomeContext) // Assumes provider exists
}
```

### Quick Reference: Making Components Reusable

**Before (Non-Reusable):**
- ❌ Has `fetch()` calls
- ❌ Uses `useAuth()` or data hooks
- ❌ Hardcoded API endpoints
- ❌ Business logic mixed in
- ❌ Assumes specific context

**After (Reusable):**
- ✅ All data via props
- ✅ All callbacks via props
- ✅ No API calls
- ✅ Pure presentation
- ✅ Works without context

**Remember: If a component can't be used in a different part of the app with different data, it's not reusable.**

---

## Automatic Validation & Testing

**CRITICAL**: Every component MUST pass these validation checks before being considered complete.

### Pre-Creation Validation (MANDATORY)

**Before writing ANY component code, verify:**

#### 1. Component Discovery Checklist
- [ ] Listed all UI components: `ls components/ui/`
- [ ] Searched for similar components: `grep -r "keyword" components/`
- [ ] Used codebase search for similar implementations
- [ ] Checked domain directories (`enterprise/`, `admin/`, `group/`, etc.)
- [ ] Evaluated if existing components can be extended
- [ ] Documented why new component is needed (if creating new)

#### 2. Reusability Design Validation
- [ ] Component will accept ALL data via props (no internal fetching)
- [ ] Component will accept ALL callbacks via props (no hardcoded actions)
- [ ] Component will NOT use data hooks directly (`useAuth`, `useQuery`, etc.)
- [ ] Component will NOT have hardcoded API endpoints
- [ ] Component will have proper TypeScript interface for props
- [ ] Component will follow established patterns (Dialog, Sheet, etc.)

### Post-Creation Validation (AUTOMATIC)

**After component is created, automatically run these checks:**

#### Validation Script

```bash
# Run this validation script for every new component
COMPONENT_FILE="components/example/new-component.tsx"

echo "🔍 Validating component reusability: $COMPONENT_FILE"

# Check 1: No hardcoded fetch calls in presentational components
echo "✓ Checking for hardcoded API calls..."
if grep -n "fetch\|\.get\|\.post\|\.put\|\.delete" "$COMPONENT_FILE" | grep -v "Container\|container"; then
  echo "❌ FAIL: Hardcoded API calls found. Extract to container component."
  exit 1
fi

# Check 2: No direct data hooks in presentational components
echo "✓ Checking for direct data hooks..."
if grep -n "useAuth\|useQuery\|useSWR\|useContext.*User\|useContext.*Auth" "$COMPONENT_FILE" | grep -v "Container\|container"; then
  echo "❌ FAIL: Direct data hooks found. Pass data via props instead."
  exit 1
fi

# Check 3: Has proper TypeScript interface
echo "✓ Checking for props interface..."
if ! grep -q "interface.*Props\|type.*Props" "$COMPONENT_FILE"; then
  echo "❌ FAIL: Missing props interface. Add TypeScript interface."
  exit 1
fi

# Check 4: No 'any' types in props
echo "✓ Checking for type safety..."
if grep -n ":\s*any\|any\s*>" "$COMPONENT_FILE" | grep -v "//"; then
  echo "⚠️  WARNING: 'any' types found. Use proper types for reusability."
fi

# Check 5: Component is exported
echo "✓ Checking component export..."
if ! grep -q "export.*function\|export.*const.*=" "$COMPONENT_FILE"; then
  echo "❌ FAIL: Component not exported. Add export statement."
  exit 1
fi

# Check 6: Uses established UI patterns
echo "✓ Checking for UI pattern usage..."
if grep -q "Dialog\|Sheet\|AlertDialog\|Button\|Card" "$COMPONENT_FILE"; then
  echo "✅ PASS: Uses established UI patterns"
else
  echo "⚠️  WARNING: Consider using established UI components"
fi

echo "✅ All validation checks passed!"
```

#### Manual Validation Checklist

After creating component, verify:

- [ ] **No `fetch()` calls** - Check: `grep -n "fetch" component.tsx`
- [ ] **No data hooks** - Check: `grep -n "useAuth\|useQuery" component.tsx`
- [ ] **Has props interface** - Check: `grep -A 5 "interface.*Props" component.tsx`
- [ ] **No hardcoded endpoints** - Check: `grep -n "/api/" component.tsx`
- [ ] **All data via props** - Review component signature
- [ ] **All callbacks via props** - Review component signature
- [ ] **Works with mock data** - Can test without real API
- [ ] **Type-safe** - No `any` types in props

### Component Testing Template

**Create a test file to verify reusability:**

```typescript
// components/example/new-component.test.tsx
import { render, screen } from '@testing-library/react'
import { Component } from './component'

describe('Component Reusability', () => {
  it('should render with mock data', () => {
    const mockData = {
      id: '1',
      name: 'Test',
      // ... other required fields
    }
    
    render(<Component data={mockData} onAction={jest.fn()} />)
    
    expect(screen.getByText('Test')).toBeInTheDocument()
  })
  
  it('should work without API calls', () => {
    // Component should work with just props
    const mockData = { /* ... */ }
    render(<Component data={mockData} />)
    
    // No network requests should be made
  })
  
  it('should accept all callbacks via props', () => {
    const mockCallbacks = {
      onAction: jest.fn(),
      onEdit: jest.fn(),
      onDelete: jest.fn(),
    }
    
    render(<Component data={mockData} {...mockCallbacks} />)
    
    // All callbacks should be callable
    expect(mockCallbacks.onAction).toBeDefined()
  })
})
```

### Validation Output Format

**After validation, output:**

```markdown
## [COMPONENT-REUSE] Validation Results

**Component**: `components/example/new-component.tsx`
**Validation Time**: 2025-01-25 14:30:00

### ✅ Pre-Creation Validation
- [x] Component discovery completed
- [x] Existing components evaluated
- [x] Reusability design validated
- [x] Pattern compliance confirmed

### ✅ Post-Creation Validation
- [x] No hardcoded API calls
- [x] No direct data hooks
- [x] Props interface defined
- [x] Type-safe implementation
- [x] Follows established patterns

### 📋 Component Details
**Type**: Presentational Component
**Pattern**: Dialog-based
**Dependencies**: `@/components/ui/dialog`, `@/components/ui/button`
**Reusability Score**: 10/10

### ✅ VALIDATION PASSED
Component is fully reusable and ready for use anywhere in the application.
```

### Automatic Fix Suggestions

**If validation fails, suggest fixes:**

```markdown
## ❌ [COMPONENT-REUSE] Validation FAILED

**Component**: `components/example/non-reusable.tsx`

### Issues Found:
1. ❌ Hardcoded API call on line 15: `fetch('/api/data')`
2. ❌ Direct hook usage on line 8: `const { user } = useAuth()`
3. ❌ Missing props interface

### Suggested Fixes:

#### Fix 1: Extract Data Fetching
```typescript
// Create container component
export function ComponentContainer({ id }: { id: string }) {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch(`/api/data/${id}`).then(r => r.json()).then(setData)
  }, [id])
  
  if (!data) return <Skeleton />
  return <Component data={data} />
}
```

#### Fix 2: Pass User via Props
```typescript
// Remove useAuth(), accept user via props
interface ComponentProps {
  user: User | null
  data: DataType
  // ...
}
```

### Re-validation Required
Please fix the issues above and re-run validation.
```

### Integration with Rule 15

This skill is automatically invoked by **Rule 15: Component Reuse Enforcement** when:
- Component files are created
- Component files are modified
- User requests component creation

**Workflow:**
1. Rule 15 detects component creation request
2. Rule 15 invokes this skill (component-reuse-workflow)
3. This skill guides through discovery and validation
4. Rule 15 validates final component
5. Component is approved or fixes are required

### Continuous Validation

**Components should be re-validated when:**
- Props interface changes
- New dependencies added
- Business logic introduced
- API calls added
- Hooks added

**Re-validation command:**
```bash
# Re-validate existing component
.agent/scripts/validate-component-reusability.sh components/example/component.tsx
```

### Success Criteria

A component passes validation when:
- ✅ All pre-creation checks completed
- ✅ All post-creation checks passed
- ✅ Can be used with mock data
- ✅ No hardcoded dependencies
- ✅ Fully typed with proper interfaces
- ✅ Follows established patterns
- ✅ Works in isolation

**Remember: Validation is not optional. Every component MUST pass before being considered complete.**
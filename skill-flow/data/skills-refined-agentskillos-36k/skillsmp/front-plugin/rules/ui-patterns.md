# Front Plugin UI Patterns

## React Architecture

### Context Provider Pattern

```tsx
// src/providers/frontContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'
import Front from '@frontapp/plugin-sdk'

const FrontContext = createContext(undefined)

export function useFrontContext() {
  return useContext(FrontContext)
}

export function FrontContextProvider({ children }) {
  const [context, setContext] = useState()

  useEffect(() => {
    const subscription = Front.contextUpdates.subscribe(ctx => {
      setContext(ctx)
    })
    return () => subscription.unsubscribe()
  }, [])

  return (
    <FrontContext.Provider value={context}>
      {children}
    </FrontContext.Provider>
  )
}
```

### Main App Switch

```tsx
// src/App.tsx
import { useFrontContext } from './providers/frontContext'

function App() {
  const context = useFrontContext()

  if (!context) {
    return <LoadingState message="Connecting to Front..." />
  }

  switch (context.type) {
    case 'noConversation':
      return <EmptyState message="Select a conversation to use this plugin." />
    case 'singleConversation':
      return <ConversationView />
    case 'multiConversations':
      return <EmptyState message="Select only one conversation." />
    case 'messageComposer':
      return <ComposerView />
    default:
      console.error(`Unsupported context type: ${context.type}`)
      return <EmptyState message="Unsupported context." />
  }
}
```

### Entry Point

```tsx
// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { FrontContextProvider } from './providers/frontContext'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <FrontContextProvider>
      <App />
    </FrontContextProvider>
  </React.StrictMode>
)
```

## Loading States

Never show a blank screen. Always show loading feedback:

```tsx
function LoadingState({ message = 'Loading...' }) {
  return (
    <div className="flex items-center justify-center h-full p-4">
      <div className="text-center">
        <Spinner className="mx-auto mb-2" />
        <p className="text-sm text-gray-500">{message}</p>
      </div>
    </div>
  )
}
```

## Error Handling

```tsx
function useConversationMessages() {
  const context = useFrontContext()
  const [messages, setMessages] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (context?.type !== 'singleConversation') return

    setLoading(true)
    context.listMessages()
      .then(result => {
        setMessages(result.results)
        setError(null)
      })
      .catch(err => {
        console.error('Failed to load messages:', err)
        setError(err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [context])

  return { messages, error, loading }
}
```

## Dark Mode Support

```tsx
// Check system preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

// Or provide toggle
function ThemeProvider({ children }) {
  const [isDark, setIsDark] = useState(
    window.matchMedia('(prefers-color-scheme: dark)').matches
  )

  return (
    <div className={isDark ? 'dark' : ''}>
      {children}
    </div>
  )
}
```

## Sidebar Plugin Layout

Sidebars are narrow. Design for vertical scrolling:

```tsx
function SidebarLayout({ children }) {
  return (
    <div className="h-full overflow-y-auto overflow-x-hidden">
      <div className="p-4 space-y-4">
        {children}
      </div>
    </div>
  )
}
```

## Composer Plugin Layout (Critical!)

Composer modals are VERY narrow (280px minimum). Extra constraints:

```css
/* Global resets for composer */
* {
  box-sizing: border-box;
  max-width: 100%;
}

body, #root {
  overflow-x: hidden;
}

/* Text truncation */
.truncate-text {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
```

Composer-specific rules:
- Max width 280px
- Font size 0.8125rem for main text, 0.625-0.6875rem for buttons
- Padding 0.375rem max
- Gaps 0.25rem
- Icons w-2.5 h-2.5 (10px) for small, w-3 h-3 (12px) max
- Break content onto multiple lines instead of horizontal
- Test at 280px width!

## Using Front UI Kit

Front provides `@frontapp/ui-kit` for consistent styling:

```tsx
import { Paragraph, Heading, Button } from '@frontapp/ui-kit'

function MyComponent() {
  return (
    <div>
      <Heading>Title</Heading>
      <Paragraph>Some content here.</Paragraph>
      <Button onClick={handleClick}>Action</Button>
    </div>
  )
}
```

## Modals and Popups

Never use standard modals in plugins (they won't work in iframe). Use `openUrlInPopup`:

```tsx
// Wrong - won't work
<Modal open={isOpen}>...</Modal>

// Correct - opens in popup window
await context.openUrlInPopup('/modal-content', { width: 400, height: 300 })
```

## Getting Latest Message ID

Common pattern for creating reply drafts:

```tsx
function useLatestMessageId() {
  const context = useFrontContext()
  const [messageId, setMessageId] = useState()

  useEffect(() => {
    if (context?.type !== 'singleConversation') return

    context.listMessages().then(result => {
      if (result.results.length > 0) {
        const latest = result.results[result.results.length - 1]
        setMessageId(latest.id)
      }
    })
  }, [context])

  return messageId
}
```

## Debug Mode

Support debug mode via query string:

```tsx
const isDebugMode = new URLSearchParams(window.location.search).get('debug') === 'true'

function App() {
  return (
    <div>
      <MainContent />
      {isDebugMode && <DebugPanel />}
    </div>
  )
}

function DebugPanel() {
  const context = useFrontContext()

  return (
    <div className="border-t mt-4 pt-4">
      <h3 className="font-bold">Debug</h3>
      <pre className="text-xs overflow-auto max-h-64">
        {JSON.stringify(context, null, 2)}
      </pre>
    </div>
  )
}
```

## Fallbacks for Missing Data

Always handle undefined/missing data:

```tsx
function ConversationInfo() {
  const context = useFrontContext()
  const conv = context?.conversation

  return (
    <div>
      <p>Subject: {conv?.subject ?? 'No subject'}</p>
      <p>Assignee: {conv?.assignee?.name ?? 'Unassigned'}</p>
      <p>Tags: {conv?.tags?.length ? conv.tags.map(t => t.name).join(', ') : 'None'}</p>
    </div>
  )
}
```

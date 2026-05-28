---
name: chatkit-client-widget-creator
description: This skill helps create React chat widgets using the ChatKit React library, following best practices for floating chat interfaces with thread persistence and proper configuration.
---

# ChatKit Client Widget Creator

This skill helps create React chat widgets using the ChatKit React library, following best practices for floating chat interfaces with thread persistence and proper configuration.

## Usage Instructions

When a user needs to create a ChatKit client widget, use this skill to generate:

1. React component with proper state management
2. useChatKit hook configuration with API settings
3. Thread persistence using localStorage
4. Floating chat button with open/close functionality
5. Styling and UI components with proper accessibility
6. Error handling and lifecycle management

## How the Client Connects

The client connects to the backend in this way:
1. **API Configuration**: Points to the backend ChatKit endpoint (`http://localhost:8000/chatkit`)
2. **Thread Management**: Uses localStorage to persist thread IDs across sessions
3. **Event Handling**: Responds to thread changes, errors, and ready states
4. **UI Integration**: Renders the ChatKit component with the control object

## Best Practices to Follow

- Use localStorage for thread persistence across page reloads
- Implement proper loading states with `isReady` flag
- Handle thread ID changes by saving to localStorage
- Include proper error handling callbacks
- Use floating UI pattern with open/close states
- Implement "New Chat" functionality that clears thread ID
- Include accessibility attributes (aria-label)
- Use proper CSS class utilities (cn) for conditional styling
- Configure theme options to match brand colors
- Add appropriate event callbacks for debugging and monitoring

## Template Structure

### Complete ChatKit Widget Template:
```tsx
import { ChatKit, useChatKit } from '@openai/chatkit-react'
import { useState, useEffect, Activity } from 'react'
import { MessageCircle, X, RefreshCw } from 'lucide-react'
import { cn } from '@site/src/lib/utils'  // Adjust import path as needed

export const ChatWidget = () => {
  const [initialThread, setInitialThread] = useState<string | null>(null)
  const [isReady, setIsReady] = useState(false)
  const [isChatOpen, setIsChatOpen] = useState(false)

  // Load saved thread ID on mount
  useEffect(() => {
    const savedThread = localStorage.getItem('chatkit-thread-id')
    setInitialThread(savedThread)
  }, [])

  const { control } = useChatKit({
    api: {
      url: 'http://localhost:8000/chatkit',  // Update to your backend URL
      domainKey: 'localhost',  // Update domain as needed
    },
    initialThread: initialThread,
    theme: {
      colorScheme: 'dark',  // or 'light'
      color: {
        accent: { primary: 'hsl(174, 72%, 56%)', level: 1 },  // Adjust colors as needed
      },
      radius: 'round',  // or 'sharp' or 'smooth'
    },
    startScreen: {
      greeting: 'Welcome to Your Assistant!',
      prompts: [
        { label: 'Hello', prompt: 'Say hello and introduce yourself' },
        { label: 'Help', prompt: 'What can you help me with?' },
        // Add more starter prompts as needed
      ],
    },
    composer: {
      placeholder: 'Ask me anything...',  // Customize placeholder text
    },
    onThreadChange: ({ threadId }) => {
      console.log('Thread changed:', threadId)
      if (threadId) {
        localStorage.setItem('chatkit-thread-id', threadId)
      }
    },
    onError: ({ error }) => {
      console.error('ChatKit error:', error)
    },
    onReady: () => {
      console.log('ChatKit is ready!')
    },
  })


  return (<>
    {/* Floating Chat Button (bottom-right) */}
    {!isChatOpen && (
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-linear-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/30 transition-all duration-300 ease-out hover:scale-110 hover:shadow-xl hover:shadow-primary/40 animate-pulse-glow cursor-pointer"
        aria-label="Open chat"
      >
        <MessageCircle className="w-6 h-6 text-primary-foreground" />
      </button>
    )}

    {/* Chat Popup */}
    <Activity mode={isChatOpen ? "visible" : "hidden"}>
      {/* Backdrop */}
      <div
        onClick={() => setIsChatOpen(false)}
        className="fixed inset-0 bg-background/60 backdrop-blur-sm z-999"
      />

      {/* Popup Window */}
      <div className="fixed bottom-6 right-6 z-1000 w-105 h-150 max-w-[calc(100vw-3rem)] max-h-[calc(100vh-3rem)] bg-card border border-border rounded-2xl shadow-2xl shadow-primary/20 flex flex-col overflow-hidden animate-slide-in-up">
        {/* Chat Header */}
        <div className="px-4 py-3 bg-muted border-b border-border flex justify-between items-center shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
            <span className="text-primary font-semibold text-sm">
              Physical AI Assistant
            </span>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => {
                localStorage.removeItem('chatkit-thread-id')
              }}
              className="px-3 py-1.5 rounded-lg bg-primary/20 hover:bg-primary/30 text-primary text-xs font-medium flex items-center gap-1.5 transition-colors duration-200"
            >
              <RefreshCw className="w-3 h-3" />
              New Chat
            </button>
            <button
              onClick={() => setIsChatOpen(false)}
              className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors duration-200"
              aria-label="Close chat"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Chat Content */}
        <div className="flex-1 overflow-hidden chatkit-container">
          <Activity mode={isReady ? "hidden" : "visible"}>
            <div className="h-full w-full flex items-center justify-center text-muted-foreground text-sm">
              Connecting to assistant...
            </div>
          </Activity>
          <ChatKit control={control} ref={ref} className="h-full w-full" />
        </div>
      </div>
    </Activity>
  </>);
}

export default ChatWidget
```

## Key Configuration Options

- **API URL**: Points to your backend ChatKit endpoint
- **Theme Options**: Color scheme, accent colors, border radius
- **Start Screen**: Greeting message and starter prompts
- **Composer**: Input placeholder text
- **Event Handlers**: Thread change, error, and ready callbacks

## Common Widget Patterns

- Floating action button (FAB) pattern
- Slide-in/slide-out animations
- Persistent threads across sessions
- Multi-thread support with localStorage
- Responsive design for mobile and desktop

## Security Considerations

- Validate API URLs in production
- Consider authentication for sensitive conversations
- Be aware of data stored in localStorage
- Implement proper error boundaries

## Output Requirements

1. Generate complete, working ChatKit React widget component
2. Include proper state management and lifecycle handling
3. Add thread persistence using localStorage
4. Include proper UI with floating button and popup
5. Follow the exact patterns shown in the template

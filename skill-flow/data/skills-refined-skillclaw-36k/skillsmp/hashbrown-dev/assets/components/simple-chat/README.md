# Simple Chat Component Template

This template provides a basic, self-contained React chat component using the `@hashbrownai/react` `useChat` hook. It's designed for simple, text-only conversations.

## Files

- `SimpleChat.tsx`: A functional React component that includes the chat UI and all the logic for sending and receiving messages.

## How to Use

1.  **Integrate into your App:**
    Copy the `SimpleChat.tsx` file into your React project.

2.  **Provide Context:**
    Ensure that the `SimpleChat` component is a child of the `<HashbrownProvider>` in your application so that it can access the chat service configuration.

    ```tsx
    // In your main App component or equivalent
    import { HashbrownProvider } from '@hashbrownai/react'
    import { SimpleChat } from './path/to/SimpleChat'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          {/* ... other components */}
          <SimpleChat />
          {/* ... other components */}
        </HashbrownProvider>
      )
    }
    ```

## Customization

- **Styling:** The component uses inline styles for simplicity. You can replace these with CSS classes, CSS-in-JS, or your preferred styling solution.
- **Model and System Prompt:** Change the `model` and `system` properties in the `useChat` hook within `SimpleChat.tsx` to configure the AI's behavior and personality.
- **Initial Messages:** You can provide an `initialMessages` array to the `useChat` hook to start the conversation with a predefined history.
- **UI Elements:** Modify the JSX to change the appearance of messages, the input area, or the send button.

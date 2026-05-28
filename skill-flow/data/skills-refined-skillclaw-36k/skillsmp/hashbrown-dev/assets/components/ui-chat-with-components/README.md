# UI Chat with Components Template

This template demonstrates how to use the `useUiChat` hook from `@hashbrownai/react` to create a chat interface where the AI can render custom React components.

## Key Concepts

- **`useUiChat`**: This hook is similar to `useChat` but is designed to handle responses that include UI components.
- **`exposeComponent`**: This function is used to create a definition of your React component that the AI can understand. You provide the component itself, a description, and a schema for its props and children.
- **`<RenderMessage />`**: This Hashbrown component is responsible for rendering the AI's response, including any custom components it chooses to use.

## Files

- `UIChat.tsx`: The main component that sets up the `useUiChat` hook, exposes a custom component, and renders the chat interface.
- `components/CustomCard.tsx`: A simple, presentational React component that will be exposed to the AI.
- `README.md`: This file.

## How to Use

1.  **Integrate into your App:**
    Copy the `ui-chat-with-components` directory into your React project.

2.  **Provide Context:**
    Ensure that the `UIChat` component is a child of the `<HashbrownProvider>`.

    ```tsx
    import { HashbrownProvider } from '@hashbrownai/react'
    import { UIChat } from './path/to/UIChat'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          <UIChat />
        </HashbrownProvider>
      )
    }
    ```

3.  **Interact:**
    Run your application and try asking the AI to use the custom component. For example: "Show me a card with the title 'Hello World' and the content 'This is a test'."

## Customization

- **Expose More Components:** You can expose any of your own React components to the AI. Just wrap them with `exposeComponent` and add them to the `components` array in the `useUiChat` hook.
- **System Prompt:** The system prompt in `UIChat.tsx` instructs the AI on how and when to use the custom components. You can modify this to guide the AI's behavior.
- **Styling:** Customize the appearance of `CustomCard.tsx` or any other components you create.

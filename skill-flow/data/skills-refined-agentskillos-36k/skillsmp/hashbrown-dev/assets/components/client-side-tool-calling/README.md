# Client-Side Tool Calling Template

This template demonstrates how to create and use client-side tools with the `@hashbrownai/react` `useTool` hook. This allows the AI to interact directly with your React component's state or trigger client-side logic.

## Key Concepts

- **`useTool`**: This hook defines a tool that the AI can call. You provide its name, description, a schema for its arguments, and a handler function to execute the tool's logic.
- **Client-Side State Interaction:** The handler function for the tool can directly access and modify your component's state (or any other client-side resource). In this example, it modifies a simple `todoItems` array.
- **AI Orchestration:** The AI understands when to call the tool based on the user's request and the tool's description.

## Files

- `ClientTool.tsx`: A React component that manages a simple todo list and defines a `useTool` to modify it.

## How to Use

1.  **Integrate into your App:**
    Copy the `ClientTool.tsx` file into your React project.

2.  **Provide Context:**
    Make sure the `ClientTool` component is a child of the `<HashbrownProvider>`.

    ```tsx
    import { HashbrownProvider } from '@hashbrownai/react'
    import { ClientTool } from './path/to/ClientTool'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          <ClientTool />
        </HashbrownProvider>
      )
    }
    ```

3.  **Interact:**
    Run the application. The component will display a small todo list. In the text area, type a command like "Mark item with ID 1 as complete" and send it. The AI will call your client-side tool, which will update the state and re-render the list with the item marked as done.

## Customization

- **Define Your Own Tools:** Replace the `todoTool` with any tool you need. You could create tools to:
  - Toggle a theme (dark/light mode).
  - Open or close a modal.
  - Filter a list of data on the client.
  - Trigger a client-side API call (e.g., to a non-Hashbrown endpoint).
- **Modify the Handler:** The `handler` function in `useTool` is where you implement the tool's logic. Modify this to interact with your application's state management solution (e.g., Zustand, Redux, React Context).
- **Update the System Prompt:** Adjust the `system` prompt in the `useChat` hook to give the AI better instructions on how and when to use your custom tools.

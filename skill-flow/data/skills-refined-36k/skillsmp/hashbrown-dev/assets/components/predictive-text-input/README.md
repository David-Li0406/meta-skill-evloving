# Predictive Text Input Template

This template demonstrates how to create a predictive text input using the `@hashbrownai/react` `useCompletion` hook. As the user types, the AI suggests the next few words, which can be accepted by pressing the Tab key.

## Key Concepts

- **`useCompletion`**: This is a simple hook for single-turn text generation. It takes a text `input` and returns the AI's streamed `output`.
- **Debouncing:** The `debounce` option is used to prevent sending a request to the API on every keystroke, improving performance and reducing costs.
- **UI Overlay:** The predictive text is displayed as a "ghost" text overlay inside the textarea, a common UX pattern for autocompletion.

## Files

- `PredictiveTextInput.tsx`: The React component that implements the predictive text input.

## How to Use

1.  **Integrate into your App:**
    Copy the `PredictiveTextInput.tsx` file into your React project.

2.  **Provide Context:**
    Ensure the component is a child of `<HashbrownProvider>`.

    ```tsx
    import { HashbrownProvider } from '@hashbrownai/react'
    import { PredictiveTextInput } from './path/to/PredictiveTextInput'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          <PredictiveTextInput />
        </HashbrownProvider>
      )
    }
    ```

3.  **Interact:**
    Run your application and start typing in the text area. Suggestions will appear as gray text. Press the `Tab` key to accept a suggestion.

## Customization

- **System Prompt:** Modify the `system` prompt in the `useCompletion` hook to change the AI's behavior. You could make it a code assistant, a creative writer, or a technical document editor.
- **Styling:** The component uses inline styles. Adjust them to match your application's design system.
- **Accept Key:** Change the key binding in the `handleKeyDown` function to use a different key (e.g., `Enter` or `ArrowRight`) to accept suggestions.
- **Debounce Timing:** Adjust the `debounce` value (in milliseconds) to control how quickly the AI provides suggestions.

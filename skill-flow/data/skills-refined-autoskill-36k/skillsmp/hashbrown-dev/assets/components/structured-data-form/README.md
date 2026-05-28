# Structured Data Form Template

This template demonstrates how to use the `@hashbrownai/react` `useStructuredCompletion` hook to parse natural language from a single input into a structured JSON object. It serves as a powerful replacement for traditional multi-field forms.

## Key Concepts

- **`useStructuredCompletion`**: This hook takes a text input and a Zod schema, and returns a structured JSON object that conforms to that schema.
- **Schema-Driven Extraction:** You define the shape of the data you want with a schema (`userProfileSchema` in this example), and the AI handles the extraction.

## Files

- `StructuredDataForm.tsx`: The React component containing the UI and the logic for the `useStructuredCompletion` hook.
- `schema.ts`: Defines the `userProfileSchema` which dictates the structure of the output JSON.

## How to Use

1.  **Integrate into your App:**
    Copy the `structured-data-form` directory into your React project.

2.  **Provide Context:**
    Ensure that the `StructuredDataForm` component is a child of the `<HashbrownProvider>`.

    ```tsx
    import { HashbrownProvider } from '@hashbrownai/react'
    import { StructuredDataForm } from './path/to/StructuredDataForm'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          <StructuredDataForm />
        </HashbrownProvider>
      )
    }
    ```

3.  **Interact:**
    Run the application. Type a sentence containing a name and email into the text area and click "Parse Data". The AI will extract the information and display it as a JSON object.

## Customization

- **Modify the Schema:** The core of this template is `schema.ts`. You can change the `userProfileSchema` to extract any kind of data you need—contact information, event details, product specifications, etc. The `s` helper from `@hashbrownai/core` provides a fluent API for building complex schemas.
- **Update the System Prompt:** In `StructuredDataForm.tsx`, modify the `system` prompt passed to `useStructuredCompletion` to give the AI more specific instructions for your use case.
- **Styling:** The component uses inline styles. Feel free to replace them with your own styling solution.

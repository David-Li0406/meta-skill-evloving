# JS Runtime Chart Generator Template

This template demonstrates a powerful feature of Hashbrown: the ability for the AI to write and execute JavaScript code in a sandboxed client-side environment. It uses this capability to generate Chart.js configurations dynamically based on a user's natural language prompt.

## Key Concepts

- **`useRuntime`**: This hook creates a sandboxed JavaScript runtime environment.
- **`useRuntimeFunction`**: This hook exposes a TypeScript/JavaScript function (like `getData` or `renderChart`) to the AI's sandboxed environment. The AI can then call these functions from the code it generates.
- **`useToolJavaScript`**: This hook creates a tool named `javascript` that allows the AI to execute a block of code within the runtime you've configured.
- **Dynamic Charting:** Instead of asking the AI to return a static JSON configuration, you're asking it to write the _logic_ to fetch data and build the configuration, offering much greater flexibility.

## Files

- `ChartGenerator.tsx`: The main React component that sets up the runtime, defines the functions available to the AI, and renders the chat interface and the resulting chart.

## How to Use

1.  **Install Chart.js:**
    This component depends on `chart.js`. Make sure to add it to your project:

    ```bash
    npm install chart.js
    ```

2.  **Integrate into your App:**
    Copy the `ChartGenerator.tsx` file into your project.

3.  **Provide Context:**
    Ensure the component is a child of `<HashbrownProvider>`.

    ```tsx
    import { HashbrownProvider } from '@hashbrownai/react'
    import { ChartGenerator } from './path/to/ChartGenerator'

    function App() {
      return (
        <HashbrownProvider url="/api/chat">
          <ChartGenerator />
        </HashbrownProvider>
      )
    }
    ```

## Customization

- **Data Fetching:** The `getData` function in this template uses mock data. Replace the contents of this function with your actual data fetching logic (e.g., an API call). The schema for the data should remain consistent.
- **Available Functions:** You can add more functions to the `useRuntime` hook to give the AI more capabilities. For example, you could add functions for data transformation, statistical calculations, or accessing other client-side services.
- **System Prompt:** The system prompt in `useChat` is crucial. It tells the AI that it's a Chart.js expert and instructs it to use the provided functions. Tailor this prompt to give the AI better context about your specific data and charting needs.
- **UI and Styling:** Customize the input form and chart canvas to match your application's design.

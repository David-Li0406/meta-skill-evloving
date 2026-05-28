# Basic Chat Server Template

This template provides a minimal Node.js Express server for handling chat completions with Hashbrown and OpenAI. It sets up a single endpoint that streams responses back to the client.

## Files

- `package.json`: Defines project metadata, dependencies (`express`, `@hashbrownai/openai`, `cors`), and basic scripts.
- `tsconfig.json`: TypeScript configuration for building the server.
- `src/index.ts`: The main server entry point.

## How to Use

1.  **Install Dependencies:**

    ```bash
    npm install
    ```

2.  **Set Environment Variables:**
    Create a `.env` file in the root of this template directory and add your OpenAI API key:

    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

3.  **Build the Server:**

    ```bash
    npm run build
    ```

4.  **Run the Server:**
    ```bash
    npm start
    ```
    The server will start on `http://localhost:3000`.

## Customization

- **Change Port:** Modify the `port` variable in `src/index.ts` or set the `PORT` environment variable.
- **Switch LLM Provider:** Replace `@hashbrownai/openai` with another provider adapter (e.g., `@hashbrownai/google`, `@hashbrownai/anthropic`). You will need to install the new dependency and update `src/index.ts` to use the corresponding `Hashbrown<Provider>.stream.text` method and API key.
- **Add Middleware:** Add any additional Express middleware (e.g., for authentication, logging) in `src/index.ts` before the `/api/chat` route.

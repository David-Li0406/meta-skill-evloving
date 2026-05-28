# Chat Server with Data API Template

This template extends the basic chat server by adding a simple REST API endpoint to serve local data. This is useful for demonstrating how AI-driven tools can fetch and interact with your application's data.

## Files

- `package.json`: Project dependencies and scripts.
- `tsconfig.json`: TypeScript configuration.
- `src/index.ts`: The main server entry point, now with two endpoints.
- `src/data.json`: A sample JSON file containing data to be served by the new endpoint.

## How to Use

1.  **Install, Configure, Build, and Run**
    Follow the same steps as the **Basic Chat Server** template to get this server running.

2.  **Access the Endpoints:**
    - **Chat:** `POST http://localhost:3000/api/chat`
    - **Data:** `GET http://localhost:3000/api/data`

## Customization

- **Modify Data:** Edit `src/data.json` to fit your needs. For a real application, you would replace this with a database connection.
- **Add More Data Endpoints:** Add more `app.get()`, `app.post()`, etc., routes to `src/index.ts` to build out your API.
- **Tool Integration:** You can create a client-side tool (using `useTool` in React or `createTool` in Angular) that makes a `fetch` request to the `/api/data` endpoint. Provide this tool to your `useChat` or `useUiChat` resource to allow the AI to access the data.

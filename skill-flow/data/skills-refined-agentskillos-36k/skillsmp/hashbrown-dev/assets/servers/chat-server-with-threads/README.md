# Chat Server with Thread Persistence

This template demonstrates how to create a chat server that persists conversation history (threads). It uses a simple in-memory store to simulate a database.

## Key Concepts

Hashbrown's server-side adapters can manage conversation history for you if you provide two functions: `loadThread` and `saveThread`.

- `loadThread(threadId)`: This function is called at the beginning of a request. It should retrieve the message history for the given `threadId` from your database and return it.
- `saveThread(threadId, messages)`: This function is called at the end of a successful request. It receives the full, updated message history for the thread, which you should then save to your database.

This template implements these functions in `src/database.ts` using a simple `Map` as an in-memory store.

## Files

- `package.json`, `tsconfig.json`: Standard project configuration.
- `src/index.ts`: The main server entry point. It imports and uses the `loadThread` and `saveThread` functions.
- `src/database.ts`: A mock in-memory database for storing conversation threads.

## How to Use

1.  **Install, Configure, Build, and Run**
    Follow the same steps as the **Basic Chat Server** template.

2.  **Interact with Threads:**
    When making a request from your client, include a `threadId` in the body of your request to `POST /api/chat`. The server will automatically load and save the conversation associated with that ID.

    Example client-side request body:

    ```json
    {
      "threadId": "some-unique-thread-identifier",
      "model": "gpt-4o-mini",
      "messages": [{ "role": "user", "content": "This is the latest message." }]
    }
    ```

## Customization

- **Replace the Database:** The most important customization is to replace the in-memory store in `src/database.ts` with a real database. You could use a file, a key-value store like Redis, or a full-fledged database like PostgreSQL or MongoDB.
- **Authentication:** In a real application, you would add authentication to ensure that users can only access their own threads. You could implement this by associating thread IDs with user IDs in your database.

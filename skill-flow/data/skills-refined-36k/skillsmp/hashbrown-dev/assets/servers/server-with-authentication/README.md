# Server with Authentication Template

This template demonstrates how to protect your chat API with a simple API key authentication middleware.

## Usage

1.  **Install Dependencies:**

    ```bash
    npm install
    ```

2.  **Set Environment Variables:**
    Create a `.env` file in the root of this template and add your OpenAI API key and a secret API key for authentication:

    ```
    OPENAI_API_KEY=your_openai_api_key
    SECRET_API_KEY=your_secret_api_key
    ```

3.  **Run the Server:**
    ```bash
    npm run dev
    ```

The server will start on `http://localhost:3000`.

## API

### `POST /chat`

Returns a chat response. Requires authentication.

**Headers:**

```
Authorization: Bearer your_secret_api_key
```

**Request Body:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, world!"
    }
  ]
}
```

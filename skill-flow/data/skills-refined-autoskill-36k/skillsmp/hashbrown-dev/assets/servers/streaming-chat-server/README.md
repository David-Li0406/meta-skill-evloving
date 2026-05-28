# Streaming Chat Server Template

This template provides a simple Express.js server that demonstrates how to stream responses from an AI model using hashbrown.

## Usage

1.  **Install Dependencies:**

    ```bash
    npm install
    ```

2.  **Set Environment Variables:**
    Create a `.env` file in the root of this template and add your OpenAI API key:

    ```
    OPENAI_API_KEY=your_api_key
    ```

3.  **Run the Server:**
    ```bash
    npm run dev
    ```

The server will start on `http://localhost:3000`.

## API

### `POST /chat`

Streams a chat response.

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

**Response:**
A server-sent event stream where each event is a token from the AI model.

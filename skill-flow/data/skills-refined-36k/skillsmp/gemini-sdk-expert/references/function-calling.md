# Master Function Calling with Gemini (2026)

Function calling allows Gemini to act as an orchestrator, connecting to your private APIs, databases, and external services.

## 1. Tool Declaration

Tools are defined as an array of function declarations. Each declaration includes a name, description, and parameter schema.

```typescript
const tools = [
  {
    functionDeclarations: [
      {
        name: "get_stock_price",
        description: "Get the current stock price for a given ticker symbol.",
        parameters: {
          type: "object",
          properties: {
            ticker: { type: "string", description: "The stock ticker symbol (e.g., AAPL)." }
          },
          required: ["ticker"]
        }
      },
      {
        name: "send_email",
        description: "Send an email to a recipient.",
        parameters: {
          type: "object",
          properties: {
            to: { type: "string" },
            subject: { type: "string" },
            body: { type: "string" }
          },
          required: ["to", "subject", "body"]
        }
      }
    ]
  }
];
```

## 2. The Execution Loop

In 2026, the SDK handles most of the boilerplate, but understanding the loop is critical for debugging.

1.  **Call**: Model generates a `tool_call`.
2.  **Execution**: Your system executes the local function.
3.  **Feedback**: Your system sends the `tool_response` back to the model.
4.  **Synthesis**: Model summarizes the result or requests more calls.

## 3. Parallel Function Calling

Gemini 3 models support calling multiple functions in a single turn. This is essential for performance (e.g., fetching 5 stock prices simultaneously).

```typescript
// The model might return:
// [ { name: "get_stock", ticker: "GOOG" }, { name: "get_stock", ticker: "MSFT" } ]
```

## 4. Forced Tool Usage (Tool Config)

You can force the model to use a specific tool or disable tool use entirely using `toolConfig`.

```typescript
const toolConfig = {
  functionCallingConfig: {
    mode: "ANY", // Forces the model to use a tool
    allowedFunctionNames: ["get_stock_price"]
  }
};
```

## 5. Security Protocols

- **Sandboxing**: Never execute model-generated code directly.
- **Input Sanitization**: Validate all parameters received from the model before passing them to your functions.
- **Confirmation Gate**: For sensitive actions (deleting data, making payments), implement a "Human-in-the-loop" gate.

---
*Updated: January 22, 2026 - 17:15*

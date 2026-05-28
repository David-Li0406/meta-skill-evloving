# Best Practices & Guidelines

## When to use

- For guidance on writing effective and reliable prompts to steer model behavior.
- When selecting the appropriate model for your task and provider.
- To ensure your AI-powered application is built responsibly and ethically.

## Core concepts

- **Prompt Engineering**: The practice of carefully structuring prompts—including system instructions, message history, and examples—to guide an LLM toward the desired output.
- **Model Selection**: The process of choosing the appropriate model ID (e.g., `gpt-4o`, `gemini-pro`) for your selected provider, which is passed in the `model` property of a hook.
- **Responsible AI**: A set of principles for building AI systems that are transparent, fair, private, and safe for users.

## Rules & constraints

- **MUST**: Be explicit in system prompts. Clearly define the AI's role, tone, capabilities, and constraints.
- **MUST**: Use schema-driven hooks (`useStructuredChat`, `useStructuredCompletion`) for tasks that require reliable, machine-readable JSON output.
- **MUST**: Clearly and conspicuously disclose to users when they are interacting with an AI.
- **MUST NOT**: Send sensitive or personally identifiable information (PII) to models without explicit user consent and a clear, necessary purpose.
- **SHOULD**: Provide mechanisms for users to report issues, provide feedback, and request human review of AI outputs, especially for critical decisions.

## Key Learning Points

### Point 1: Engineer Effective System Prompts

A well-crafted system prompt is critical for consistent results. Structure it with clear sections for the AI's persona, its rules, and examples of desired interactions.

```ts
const chat = useChat({
  model: 'gpt-4o',
  system: `
    ### ROLE & TONE
    You are a helpful geography expert. Your tone is academic and concise.

    ### RULES
    1. Never guess. If you don't know an answer, say so.
    2. Always provide the population when describing a capital city.

    ### EXAMPLES
    <user>What is the capital of France?</user>
    <assistant>The capital of France is Paris, with a population of approximately 2.1 million.</assistant>
  `,
})
```

### Point 2: Use the Right Hook for the Task

Hashbrown provides different hooks tailored to specific outcomes. Choose the one that best fits your goal.

- **`useChat`**: For general, text-based conversations.
- **`useStructuredChat` / `useStructuredCompletion`**: When you need predictable JSON output.
- **`useUiChat`**: When you want the model to generate and render your React components.

### Point 3: Selecting a Model

The `model` property passed to any hook is a simple string ID that corresponds to the model you want to use. Your backend adapter is responsible for routing the request to the correct provider (OpenAI, Google, Azure, etc.) based on its configuration.

```tsx
// For OpenAI
const chat = useChat({ model: 'gpt-4o', ... });

// For Google
const chat = useChat({ model: 'gemini-1.5-pro-latest', ... });

// For Azure (uses the deployment name)
const chat = useChat({ model: 'your-azure-deployment-name', ... });
```

### Point 4: Adhere to Ethical Principles

Building trust with users is paramount. Always consider the following:

- **Transparency**: Inform users they are interacting with an AI.
- **Privacy**: Avoid processing sensitive data. Review your LLM provider's privacy policy.
- **Consent**: Obtain user consent before processing their data with AI models.
- **Moderation**: Implement filters for both user input and AI-generated output to prevent harmful content.
- **Human Oversight**: Offer a path for users to escalate to a human reviewer.

## Pitfalls

- **Vague Prompts**: Ambiguous or poorly structured system prompts are a primary cause of inconsistent and unpredictable model behavior.
- **Ignoring User Privacy**: Sending sensitive user data to third-party models without consent can have serious privacy and legal consequences.
- **Lack of Transparency**: Failing to disclose that content is AI-generated or that a user is interacting with an AI can erode user trust.

## Source map

- `/guide/prompt-engineering.md` — Best practices for structuring prompts and using different hooks.
- `/guide/choosing-model.md` — How to specify a model for different providers.
- `/guide/ethics.md` — Ethical considerations for building responsible AI applications.

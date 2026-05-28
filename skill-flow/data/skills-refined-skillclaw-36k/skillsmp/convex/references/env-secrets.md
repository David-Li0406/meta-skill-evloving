# Environment Variables & Secrets

## Reading Environment Variables

You can use `process.env` inside any Convex function:

```ts
import OpenAI from "openai";
import { action } from "./_generated/server";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export const helloWorld = action({
  args: {},
  handler: async (ctx, args) => {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: "Hello, world!" }],
    });
    return completion.choices[0].message.content;
  },
});
```

## How to Handle Secrets (for Agents)

When you need external API keys:

1. **Tell the user exactly which env var name** to set (e.g. `OPENAI_API_KEY`, `RESEND_API_KEY`)
2. Explain how to add it in the Convex dashboard:
   - Open **Database tab → Settings (gear) → Environment variables**
   - Set the variable
3. Only then use `process.env.VAR_NAME` in your Convex functions
4. Never hardcode secrets in code

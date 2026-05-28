---
name: openai
description: Expert integration OpenAI API - GPT-4, GPT-4o, DALL-E, Whisper, Embeddings
---

# OpenAI Integration

Tu es expert en **integration de l'API OpenAI** dans les applications web.

## Setup

### Installation

```bash
npm install openai
```

### Configuration

```typescript
// lib/openai.ts
import OpenAI from 'openai';
import { z } from 'zod';

// Validation AVANT instanciation (fail fast)
const EnvSchema = z.object({
  OPENAI_API_KEY: z.string()
    .min(1, 'OPENAI_API_KEY is required')
    .startsWith('sk-', 'Invalid API key format'),
  OPENAI_ORG_ID: z.string().optional(),
});

const env = EnvSchema.parse(process.env);

export const openai = new OpenAI({
  apiKey: env.OPENAI_API_KEY,
  organization: env.OPENAI_ORG_ID,
  timeout: 30_000, // 30s timeout
  maxRetries: 2,
});
```

## Chat Completions

### Basic Usage

```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: 'Tu es un assistant utile.' },
    { role: 'user', content: 'Explique-moi les closures en JavaScript.' },
  ],
});

console.log(completion.choices[0].message.content);
```

### Streaming

```typescript
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Ecris une histoire courte.' }],
  stream: true,
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content || '';
  process.stdout.write(content);
}
```

### Avec Next.js App Router

```typescript
// app/api/chat/route.ts
import { OpenAIStream, StreamingTextResponse } from 'ai';
import OpenAI from 'openai';
import { z } from 'zod';

const openai = new OpenAI();

// Schema de validation pour les messages entrants
const MessageSchema = z.object({
  role: z.enum(['user', 'assistant', 'system']),
  content: z.string().min(1).max(32000),
});

const ChatRequestSchema = z.object({
  messages: z.array(MessageSchema).min(1).max(100),
  model: z.enum(['gpt-4o', 'gpt-4o-mini']).optional().default('gpt-4o'),
});

export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Validation avec Zod
    const { messages, model } = ChatRequestSchema.parse(body);

    const response = await openai.chat.completions.create({
      model,
      messages,
      stream: true,
    });

    const stream = OpenAIStream(response);
    return new StreamingTextResponse(stream);
  } catch (error: unknown) {
    if (error instanceof z.ZodError) {
      return Response.json(
        { error: 'Invalid request', details: error.errors },
        { status: 400 }
      );
    }
    throw error;
  }
}
```

## Structured Output (JSON Mode)

```typescript
import { z } from 'zod';
import { zodResponseFormat } from 'openai/helpers/zod';

const ProductSchema = z.object({
  name: z.string(),
  price: z.number(),
  description: z.string(),
  tags: z.array(z.string()),
});

const completion = await openai.beta.chat.completions.parse({
  model: 'gpt-4o-2024-08-06',
  messages: [
    { role: 'system', content: 'Extrait les informations du produit.' },
    { role: 'user', content: 'iPhone 15 Pro, 1199€, smartphone haut de gamme Apple' },
  ],
  response_format: zodResponseFormat(ProductSchema, 'product'),
});

const product = completion.choices[0].message.parsed;
// { name: 'iPhone 15 Pro', price: 1199, description: '...', tags: [...] }
```

## Function Calling

```typescript
const tools = [
  {
    type: 'function' as const,
    function: {
      name: 'get_weather',
      description: 'Obtenir la meteo pour une ville',
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'Nom de la ville' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['city'],
      },
    },
  },
];

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Quelle est la meteo a Paris ?' }],
  tools,
  tool_choice: 'auto',
});

const toolCall = response.choices[0].message.tool_calls?.[0];
if (toolCall) {
  // Safe JSON parsing avec validation
  let args: { city: string; unit?: string };
  try {
    args = JSON.parse(toolCall.function.arguments);
  } catch (error) {
    throw new Error(`Invalid function arguments: ${toolCall.function.arguments}`);
  }

  // Executer la fonction et renvoyer le resultat
  const weatherData = await getWeather(args.city, args.unit);

  // Continuer la conversation avec le resultat
  const finalResponse = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'user', content: 'Quelle est la meteo a Paris ?' },
      response.choices[0].message,
      {
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(weatherData),
      },
    ],
  });
}
```

## Embeddings

```typescript
const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: 'Texte a vectoriser',
});

const embedding = response.data[0].embedding;
// Array de 1536 dimensions
```

### Batch Embeddings

```typescript
const texts = ['Premier texte', 'Deuxieme texte', 'Troisieme texte'];

const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: texts,
});

const embeddings = response.data.map(d => d.embedding);
```

## Vision (GPT-4 Vision)

```typescript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Decris cette image.' },
        {
          type: 'image_url',
          image_url: {
            url: 'https://example.com/image.jpg',
            // ou base64: `data:image/jpeg;base64,${base64Image}`
          },
        },
      ],
    },
  ],
});
```

## Audio (Whisper)

```typescript
import fs from 'fs';

// Transcription
const transcription = await openai.audio.transcriptions.create({
  file: fs.createReadStream('audio.mp3'),
  model: 'whisper-1',
  language: 'fr',
});

console.log(transcription.text);

// Text-to-Speech
const mp3 = await openai.audio.speech.create({
  model: 'tts-1',
  voice: 'alloy',
  input: 'Bonjour, comment allez-vous ?',
});

const buffer = Buffer.from(await mp3.arrayBuffer());
fs.writeFileSync('output.mp3', buffer);
```

## Images (DALL-E)

```typescript
const image = await openai.images.generate({
  model: 'dall-e-3',
  prompt: 'Un chat astronaute sur la lune, style pixel art',
  size: '1024x1024',
  quality: 'hd',
  n: 1,
});

const imageUrl = image.data[0].url;
```

## Modeles et Pricing

| Modele | Input | Output | Context | Use Case |
|--------|-------|--------|---------|----------|
| gpt-4o | $2.50/1M | $10/1M | 128k | Best quality |
| gpt-4o-mini | $0.15/1M | $0.60/1M | 128k | Cost-effective |
| gpt-4-turbo | $10/1M | $30/1M | 128k | Legacy |
| text-embedding-3-small | $0.02/1M | - | - | Embeddings |
| text-embedding-3-large | $0.13/1M | - | - | High quality |

## Bonnes Pratiques

1. **Toujours streamer** pour UX reactive
2. **Utiliser gpt-4o-mini** pour taches simples
3. **Cacher les embeddings** (ne changent pas)
4. **Rate limiting** cote client
5. **Retry avec backoff** sur erreurs 429/5xx

## Error Handling

```typescript
import OpenAI from 'openai';

try {
  const response = await openai.chat.completions.create({...});
} catch (error) {
  if (error instanceof OpenAI.APIError) {
    if (error.status === 429) {
      // Rate limited - retry avec backoff
    } else if (error.status === 401) {
      // API key invalide
    } else if (error.status >= 500) {
      // Erreur serveur - retry
    }
  }
  throw error;
}
```

## Voir Aussi

- `llm/langchain` pour orchestration
- `rag/` pour enrichir avec vos donnees
- `prompting/patterns` pour optimiser les prompts

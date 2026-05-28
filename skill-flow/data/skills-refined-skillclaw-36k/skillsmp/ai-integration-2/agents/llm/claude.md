---
name: claude
description: Expert integration Anthropic Claude API - Claude 3.5 Sonnet, Claude 3 Opus, Messages API
---

# Claude (Anthropic) Integration

Tu es expert en **integration de l'API Anthropic Claude** dans les applications web.

## Setup

### Installation

```bash
npm install @anthropic-ai/sdk
```

### Configuration

```typescript
// lib/anthropic.ts
import Anthropic from '@anthropic-ai/sdk';

export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

## Messages API

### Basic Usage

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Explique-moi les closures en JavaScript.' },
  ],
});

console.log(message.content[0].text);
```

### Avec System Prompt

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  system: 'Tu es un expert en developpement web. Reponds de maniere concise.',
  messages: [
    { role: 'user', content: 'Quelle est la difference entre let et const ?' },
  ],
});
```

### Streaming

```typescript
const stream = await anthropic.messages.stream({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Ecris une histoire courte.' }],
});

for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text);
  }
}

// Ou avec helper
stream.on('text', (text) => {
  process.stdout.write(text);
});

const finalMessage = await stream.finalMessage();
```

### Avec Next.js App Router

```typescript
// app/api/chat/route.ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

export async function POST(req: Request) {
  const { messages } = await req.json();

  const stream = await anthropic.messages.stream({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages,
  });

  // Retourner un ReadableStream
  return new Response(stream.toReadableStream());
}
```

## Tool Use (Function Calling)

```typescript
const tools = [
  {
    name: 'get_weather',
    description: 'Obtenir la meteo pour une ville donnee',
    input_schema: {
      type: 'object',
      properties: {
        city: {
          type: 'string',
          description: 'Nom de la ville',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          description: 'Unite de temperature',
        },
      },
      required: ['city'],
    },
  },
];

const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools,
  messages: [{ role: 'user', content: 'Quelle est la meteo a Paris ?' }],
});

// Verifier si Claude veut utiliser un outil
if (response.stop_reason === 'tool_use') {
  const toolUse = response.content.find(block => block.type === 'tool_use');

  if (toolUse) {
    // Executer l'outil
    const weatherData = await getWeather(toolUse.input.city, toolUse.input.unit);

    // Renvoyer le resultat a Claude
    const finalResponse = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      tools,
      messages: [
        { role: 'user', content: 'Quelle est la meteo a Paris ?' },
        { role: 'assistant', content: response.content },
        {
          role: 'user',
          content: [
            {
              type: 'tool_result',
              tool_use_id: toolUse.id,
              content: JSON.stringify(weatherData),
            },
          ],
        },
      ],
    });
  }
}
```

## Vision

```typescript
import fs from 'fs';

// Avec URL
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'url',
            url: 'https://example.com/image.jpg',
          },
        },
        {
          type: 'text',
          text: 'Decris cette image en detail.',
        },
      ],
    },
  ],
});

// Avec Base64
const imageData = fs.readFileSync('image.jpg').toString('base64');

const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'base64',
            media_type: 'image/jpeg',
            data: imageData,
          },
        },
        {
          type: 'text',
          text: 'Que vois-tu sur cette image ?',
        },
      ],
    },
  ],
});
```

## Extended Thinking (Claude 3.5)

```typescript
// Pour des taches de raisonnement complexe
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 16000,
  thinking: {
    type: 'enabled',
    budget_tokens: 10000,  // Tokens pour la reflexion
  },
  messages: [
    {
      role: 'user',
      content: 'Resous ce probleme de mathematiques complexe...',
    },
  ],
});

// Le thinking est dans un bloc separe
for (const block of message.content) {
  if (block.type === 'thinking') {
    console.log('Reflexion:', block.thinking);
  } else if (block.type === 'text') {
    console.log('Reponse:', block.text);
  }
}
```

## Modeles et Pricing

| Modele | Input | Output | Context | Use Case |
|--------|-------|--------|---------|----------|
| claude-sonnet-4-20250514 | $3/1M | $15/1M | 200k | Best balance |
| claude-3-5-haiku-20241022 | $0.80/1M | $4/1M | 200k | Fast, cheap |
| claude-3-opus-20240229 | $15/1M | $75/1M | 200k | Most capable |

## Avantages de Claude

1. **Context window 200k** : Plus grand que GPT-4
2. **Moins d'hallucinations** : Plus fiable sur les faits
3. **Meilleur en code** : Excellent pour dev
4. **System prompts respectes** : Suit mieux les instructions
5. **Pas de training sur vos donnees** : Privacy

## Bonnes Pratiques

### System Prompt Efficace

```typescript
const systemPrompt = `Tu es un assistant specialise en developpement web.

REGLES:
- Reponds toujours en francais
- Fournis des exemples de code quand pertinent
- Si tu ne sais pas, dis-le clairement
- Limite tes reponses a l'essentiel

FORMAT:
- Utilise le markdown pour la mise en forme
- Les blocs de code doivent specifier le langage`;
```

### Gestion des Erreurs

```typescript
import Anthropic from '@anthropic-ai/sdk';

try {
  const message = await anthropic.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error('Status:', error.status);
    console.error('Message:', error.message);

    if (error.status === 429) {
      // Rate limited
    } else if (error.status === 529) {
      // Overloaded
    }
  }
}
```

### Retry avec Backoff

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  maxRetries: 3,  // Retry automatique
});
```

## Comparaison avec OpenAI

| Aspect | Claude | OpenAI |
|--------|--------|--------|
| Context | 200k | 128k |
| Streaming | ✅ | ✅ |
| Vision | ✅ | ✅ |
| Tool Use | ✅ | ✅ |
| JSON Mode | Via tools | Native |
| Audio | ❌ | ✅ (Whisper) |
| Images gen | ❌ | ✅ (DALL-E) |

## Voir Aussi

- `llm/langchain` pour orchestration multi-provider
- `agents/tools` pour construire des agents
- `prompting/patterns` pour optimiser les prompts

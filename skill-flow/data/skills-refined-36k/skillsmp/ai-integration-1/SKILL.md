---
name: AI Integration
description: Vertex AI configuration, VertexOracle service, n8n orchestration, and prompt engineering.
---

# AI Integration

## Context

Lumira V2 integrates AI capabilities via:

- **Vertex AI** (Google Cloud) - Primary AI provider
- **n8n** - Workflow orchestration (optional)

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  NestJS API     │────▶│  VertexOracle    │────▶│  Vertex AI  │
│  (Controller)   │     │  (Service)       │     │  (GCP)      │
└─────────────────┘     └──────────────────┘     └─────────────┘
         │
         ▼
┌─────────────────┐
│  n8n Workflow   │ (Optional orchestration)
└─────────────────┘
```

---

## VertexOracle Service

### Location: `apps/api/src/services/factory/VertexOracle.ts`

```typescript
@Injectable()
export class VertexOracle {
  private client: GenerativeModel;

  constructor(private configService: ConfigService) {
    const credentials = JSON.parse(
      this.configService.get('VERTEX_AI_CREDENTIALS')
    );
    this.client = new GenerativeModel({
      model: 'gemini-pro',
      credentials,
    });
  }

  async generateReading(input: ReadingInput): Promise<ReadingOutput> {
    const prompt = this.buildPrompt(input);
    const response = await this.client.generateContent(prompt);
    return this.parseResponse(response);
  }

  private buildPrompt(input: ReadingInput): string {
    return `
      You are a spiritual advisor. Analyze the following data:
      - Birth date: ${input.birthDate}
      - Birth time: ${input.birthTime}
      - Birth place: ${input.birthPlace}
      
      Provide a structured JSON response with:
      ${JSON.stringify(READING_SCHEMA)}
    `;
  }
}
```

---

## Environment Variables

```bash
# .env
VERTEX_AI_PROJECT_ID=lumira-ai-prod
VERTEX_AI_LOCATION=europe-west1
VERTEX_AI_CREDENTIALS={"type":"service_account",...}
```

---

## Prompt Engineering Guidelines

### Structure

1. **Role Definition**: Define the AI's persona clearly.
2. **Context**: Provide all necessary input data.
3. **Output Format**: Specify JSON schema explicitly.
4. **Constraints**: List what to include/exclude.

### Example

```typescript
const systemPrompt = `
You are an expert career advisor for the healthcare and social sectors.
Your role is to match professionals with missions.

INPUT:
- Professional profile: ${JSON.stringify(profile)}
- Available missions: ${JSON.stringify(missions)}

OUTPUT (JSON):
{
  "recommendations": [
    { "missionId": string, "score": number, "reasoning": string }
  ]
}

CONSTRAINTS:
- Maximum 5 recommendations
- Score from 0 to 100
- Reasoning must be 1-2 sentences
`;
```

---

## Response Parsing

Always validate AI responses with Zod:

```typescript
import { z } from 'zod';

const ReadingSchema = z.object({
  archetype: z.string(),
  keywords: z.array(z.string()),
  synthesis: z.string(),
  lifePath: z.object({
    number: z.number(),
    meaning: z.string(),
  }),
});

async parseResponse(raw: string): Promise<ReadingOutput> {
  try {
    const json = JSON.parse(raw);
    return ReadingSchema.parse(json);
  } catch (e) {
    this.logger.error('AI response parsing failed', e);
    throw new InternalServerErrorException('AI response invalid');
  }
}
```

---

## n8n Integration

### Webhook Trigger

```typescript
// Trigger n8n workflow from NestJS
await axios.post(process.env.N8N_WEBHOOK_URL, {
  event: 'order.completed',
  orderId: order.id,
  userId: order.userId,
});
```

### n8n Workflow Example

```
[Webhook] → [Fetch User Data] → [Call Vertex AI] → [Save to DB] → [Send Email]
```

---

## Rate Limiting

```typescript
// Protect AI endpoints
@UseGuards(ThrottlerGuard)
@Throttle(10, 60) // 10 requests per 60 seconds
@Post('generate')
async generate(@Body() dto: GenerateDto) {
  return this.vertexOracle.generateReading(dto);
}
```

---

## Error Handling

```typescript
try {
  const result = await this.vertexOracle.generateReading(input);
  return result;
} catch (error) {
  if (error.code === 'RESOURCE_EXHAUSTED') {
    throw new TooManyRequestsException('AI quota exceeded');
  }
  if (error.code === 'INVALID_ARGUMENT') {
    throw new BadRequestException('Invalid AI input');
  }
  throw new InternalServerErrorException('AI service unavailable');
}
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Validate AI responses | Trust raw JSON output |
| Use retry logic | Fail on first error |
| Log prompts (debug) | Log sensitive user data |
| Set request timeouts | Allow unlimited wait |
| Cache repeated queries | Hit AI for identical inputs |

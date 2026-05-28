---
name: ai-suggestions
description: Guide for Genkit AI integration, smart destination suggestions, and AI-powered features in TrainTrack
---

This skill provides guidance for working with Genkit AI, implementing smart destination suggestions, and managing AI-powered features in TrainTrack.

## Genkit AI Setup

**Configuration:** [src/ai/genkit.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/genkit.ts)
- Uses Google AI plugin
- Model: `googleai/gemini-2.0-flash`
- Exports `ai` instance for flows

**Environment Variable Required:**
```
GEMINI_API_KEY=<your_gemini_api_key>
```

## AI Flows

### Smart Destination Suggestion Flow

**File:** [src/ai/flows/smart-destination-suggestion.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/flows/smart-destination-suggestion.ts)

**Purpose:** Suggests potential destinations and routes based on past booking data and popular travel trends.

**Input Schema:**
```typescript
{
  pastBookingData: string,      // JSON string with past bookings
  popularTravelTrends: string    // JSON string with trends
}
```

**Output Schema:**
```typescript
[
  {
    destination: string,  // Suggested destination
    route: string,       // Suggested route
    reason: string       // Reason for suggestion
  }
]
```

**Flow Definition:**
- Uses Zod schemas for type safety
- Defines prompt template with `ai.definePrompt`
- Implements flow with `ai.defineFlow`
- Returns structured JSON output

## UI Integration

**Component:** [src/components/SmartSuggestionTool.tsx](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/SmartSuggestionTool.tsx)

**Features:**
- Auto-fills past booking data from Firestore
- Editable popular travel trends
- AI-powered suggestion generation
- Display of suggested destinations with reasons

**Current Status:** AI suggestions temporarily disabled for static export deployment. The component shows an error message instead of calling the AI flow.

## Using Genkit Flows

### Importing and Calling Flows

```typescript
import { suggestDestinations, type SuggestDestinationsInput } from '@/ai/flows/smart-destination-suggestion';

const input: SuggestDestinationsInput = {
  pastBookingData: JSON.stringify(bookings),
  popularTravelTrends: JSON.stringify(trends)
};

const suggestions = await suggestDestinations(input);
```

### Creating New Flows

**Pattern:**
1. Define input schema with Zod
2. Define output schema with Zod
3. Create prompt template
4. Define flow with input/output schemas
5. Implement flow logic

**Example Structure:**
```typescript
import { ai } from '@/ai/genkit';
import { z } from 'genkit';

const InputSchema = z.object({
  // Input fields
});

const OutputSchema = z.object({
  // Output fields
});

const prompt = ai.definePrompt({
  name: 'myPrompt',
  input: { schema: InputSchema },
  output: { schema: OutputSchema },
  prompt: `Your prompt template here: {{{inputField}}}`,
});

const myFlow = ai.defineFlow(
  {
    name: 'myFlow',
    inputSchema: InputSchema,
    outputSchema: OutputSchema,
  },
  async input => {
    const { output } = await prompt(input);
    return output!;
  }
);
```

## Genkit Development Server

**Start Dev Server:**
```bash
npm run genkit:dev
```

**Start with Auto-Reload:**
```bash
npm run genkit:watch
```

**Dev Server Entry:** [src/ai/dev.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/dev.ts)

**Access:** Open Genkit Dev UI at http://localhost:4000

**Features:**
- Test flows interactively with sample inputs
- View flow outputs
- Debug AI responses
- Monitor performance

## Data Preparation

### Booking Data Format

```json
[
  {
    "id": "booking-id",
    "source": "Station A",
    "destination": "Station B",
    "journeyDate": "2024-01-15T00:00:00.000Z",
    "passengers": [
      { "name": "John Doe", "age": 30, "gender": "male" }
    ],
    "status": "completed"
  }
]
```

### Travel Trends Format

```json
[
  {
    "trend": "Weekend getaways to nearby cities",
    "popularity": "High"
  },
  {
    "trend": "Coastal destinations for summer",
    "popularity": "Medium"
  }
]
```

## Static Export Considerations

**Current Limitation:** AI features are temporarily disabled in static export deployment because:
- Server-side AI calls cannot be made from static builds
- API key exposure concerns
- Client-side Genkit integration complexity

**Workaround:** The SmartSuggestionTool component shows a placeholder message instead of calling the AI flow.

**Future Implementation Options:**
1. Deploy as a serverless function (Firebase Functions)
2. Use a separate API endpoint for AI requests
3. Implement client-side Genkit with proper API key management

## Best Practices

### Prompt Engineering

**Clear Instructions:** Be explicit about what the AI should do
```typescript
prompt: `You are a travel expert. Based on the past booking data and popular travel trends,
you will suggest potential destinations and routes to the user.

Past Booking Data: {{{pastBookingData}}}
Popular Travel Trends: {{{popularTravelTrends}}}

Suggest destinations and routes in JSON format:`,
```

**Structured Output:** Use Zod schemas for type-safe responses
```typescript
const OutputSchema = z.array(
  z.object({
    destination: z.string(),
    route: z.string(),
    reason: z.string()
  })
);
```

### Error Handling

**Try-Catch Pattern:**
```typescript
try {
  const result = await suggestDestinations(input);
  setSuggestions(result);
} catch (err) {
  console.error(err);
  setError(err instanceof Error ? err.message : 'An error occurred');
}
```

**Loading States:** Show loading indicators during AI calls
```typescript
const [isLoading, setIsLoading] = useState(false);

const handleSubmit = async () => {
  setIsLoading(true);
  try {
    const result = await suggestDestinations(input);
    setSuggestions(result);
  } finally {
    setIsLoading(false);
  }
};
```

### Data Validation

**Validate JSON Inputs:**
```typescript
try {
  JSON.parse(pastBookingData);
} catch (err) {
  setError('Invalid JSON format for past booking data');
  return;
}
```

**Sanitize AI Output:**
- Validate AI responses against Zod schema
- Handle missing or malformed data
- Provide fallback suggestions if AI fails

## Testing AI Flows

### Using Genkit Dev UI

1. Start dev server: `npm run genkit:dev`
2. Open http://localhost:4000
3. Select the flow to test
4. Enter sample input data
5. Run and examine output

### Sample Test Input

```json
{
  "pastBookingData": "[{\"source\":\"Mumbai\",\"destination\":\"Delhi\",\"journeyDate\":\"2024-01-15T00:00:00.000Z\",\"status\":\"completed\"}]",
  "popularTravelTrends": "[{\"trend\":\"Weekend getaways\",\"popularity\":\"High\"}]"
}
```

### Expected Output Format

```json
[
  {
    "destination": "Jaipur",
    "route": "Mumbai → Delhi → Jaipur",
    "reason": "Based on your Mumbai-Delhi travel history, Jaipur offers cultural attractions and is a popular weekend destination."
  }
]
```

## Troubleshooting

**API Key Errors:**
- Verify GEMINI_API_KEY in environment variables
- Check API key is valid and has proper permissions
- Ensure key is not exposed in client code

**Flow Not Found:**
- Verify flow is properly defined in [src/ai/flows/](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/flows/)
- Check Genkit dev server is running
- Ensure flow name matches in import

**Type Errors:**
- Verify Zod schemas match expected data
- Check TypeScript types are correctly inferred
- Use `z.infer<>` for type extraction

**Slow Response Times:**
- Consider caching AI responses
- Implement debouncing for user inputs
- Use loading indicators for better UX

**Static Export Issues:**
- AI features currently disabled in static build
- Consider deploying AI endpoints separately
- Use serverless functions for AI calls

## Key Files Reference

- [src/ai/genkit.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/genkit.ts) - Genkit configuration
- [src/ai/flows/smart-destination-suggestion.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/flows/smart-destination-suggestion.ts) - Main AI flow
- [src/ai/dev.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/ai/dev.ts) - Dev server entry
- [src/components/SmartSuggestionTool.tsx](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/SmartSuggestionTool.tsx) - UI component
- [src/lib/firestoreClient.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/lib/firestoreClient.ts) - Data fetching for AI

## Future Enhancements

**Additional AI Flows:**
- Route optimization based on historical data
- Price prediction for train bookings
- Personalized travel recommendations
- Crowd density predictions

**Integration Improvements:**
- Server-side Genkit deployment
- Real-time AI suggestions
- Multi-language support
- Voice input for travel queries

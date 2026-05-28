# ElevenLabs API Reference

## Overview

ElevenLabs provides text-to-speech with character-level timestamps, enabling precise verse synchronization.

## Authentication

```typescript
const headers = {
  'xi-api-key': process.env.ELEVENLABS_API_KEY,
  'Content-Type': 'application/json'
};
```

## Endpoints

### Text-to-Speech with Timestamps

**Endpoint:** `POST /v1/text-to-speech/{voice_id}/with-timestamps`

**Request:**

```typescript
interface TTSRequest {
  text: string;
  model_id: string;
  voice_settings: {
    stability: number;        // 0-1, default 0.5
    similarity_boost: number; // 0-1, default 0.75
    style?: number;           // 0-1, optional
    use_speaker_boost?: boolean;
  };
  output_format?: string;     // "mp3_44100_128" (default)
}
```

**Response:**

```typescript
interface TTSResponse {
  audio_base64: string;
  alignment: {
    characters: string[];
    character_start_times_seconds: number[];
    character_end_times_seconds: number[];
  };
}
```

## Project Configuration

### Voices

| Name | Voice ID | Gender | Language |
|------|----------|--------|----------|
| Venla | `T5qAFgaL2uYxoUtojUzQ` | Female | Finnish |
| Urho | `1WVCONUwYGulVaKg4oTr` | Male | Finnish |

### Model

- **ID:** `eleven_multilingual_v2`
- **Languages:** 29 languages including Finnish
- **Latency:** ~2-4 seconds

### Voice Settings

```typescript
const VOICE_SETTINGS = {
  stability: 0.5,        // Balance between consistency and expressiveness
  similarity_boost: 0.75 // Closer to original voice
};
```

## Implementation

### Generate Chapter Audio

```typescript
async function generateChapterAudio(
  voiceId: string,
  verseTexts: string[]
): Promise<{
  audioBase64: string;
  cues: AudioCue[];
}> {
  const text = verseTexts.join('\n\n');

  const response = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/with-timestamps`,
    {
      method: 'POST',
      headers: {
        'xi-api-key': ELEVENLABS_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text,
        model_id: 'eleven_multilingual_v2',
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.75
        }
      })
    }
  );

  if (!response.ok) {
    throw new Error(`ElevenLabs error: ${response.status}`);
  }

  const data = await response.json();

  const cues = generateCuesFromTimestamps(
    data.alignment,
    verseTexts
  );

  return {
    audioBase64: data.audio_base64,
    cues
  };
}
```

### Parse Timestamps to Cues

```typescript
function generateCuesFromTimestamps(
  alignment: {
    characters: string[];
    character_start_times_seconds: number[];
    character_end_times_seconds: number[];
  },
  verseTexts: string[]
): AudioCue[] {
  const cues: AudioCue[] = [];
  let charIndex = 0;

  for (let verseNum = 0; verseNum < verseTexts.length; verseNum++) {
    const verseText = verseTexts[verseNum];
    const startCharIndex = charIndex;

    // Start time of first character in this verse
    const startMs = alignment.character_start_times_seconds[startCharIndex] * 1000;

    // Move to end of verse
    charIndex += verseText.length;

    // End time of last character in this verse
    const endCharIndex = charIndex - 1;
    const endMs = alignment.character_end_times_seconds[endCharIndex] * 1000;

    cues.push({
      verse_number: verseNum + 1,
      start_ms: Math.round(startMs),
      end_ms: Math.round(endMs)
    });

    // Skip verse separator (\n\n = 2 characters)
    charIndex += 2;
  }

  return cues;
}
```

## Caching Strategy

### Hash-Based Caching

Audio is cached using SHA-256 hash of content:

```typescript
function generateAudioHash(
  chapterId: string,
  versionId: string,
  readerKey: string
): string {
  const content = `${chapterId}:${versionId}:${readerKey}`;
  return crypto.createHash('sha256').update(content).digest('hex');
}

// Check cache before generating
async function getOrGenerateAudio(
  chapterId: string,
  versionId: string,
  readerKey: string
): Promise<AudioAsset> {
  const hash = generateAudioHash(chapterId, versionId, readerKey);

  // Check existing
  const existing = await supabase
    .from('audio_assets')
    .select('*')
    .eq('hash', hash)
    .single();

  if (existing.data) {
    return existing.data;
  }

  // Generate new
  return await generateNewAudio(chapterId, versionId, readerKey, hash);
}
```

### Storage

Audio files stored in Supabase Storage:

```typescript
const storagePath = `audio/${hash}.mp3`;

await supabase.storage
  .from('audio-chapters')
  .upload(storagePath, audioBuffer, {
    contentType: 'audio/mpeg',
    cacheControl: '31536000' // 1 year
  });

const { data: { publicUrl } } = supabase.storage
  .from('audio-chapters')
  .getPublicUrl(storagePath);
```

## Error Handling

### Rate Limits

```typescript
const RATE_LIMIT = {
  requestsPerSecond: 2,
  charactersPerMonth: 100000 // Depends on plan
};

async function withRateLimit<T>(
  fn: () => Promise<T>
): Promise<T> {
  await sleep(500); // 2 requests/second max
  return fn();
}
```

### Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;

      const delay = Math.pow(2, i) * 1000; // Exponential backoff
      await sleep(delay);
    }
  }
  throw new Error('Unreachable');
}
```

### Common Errors

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check ELEVENLABS_API_KEY |
| 422 | Invalid voice ID | Verify voice exists |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry with backoff |

## Cost Optimization

### Character Counting

```typescript
function countCharacters(verseTexts: string[]): number {
  // Characters + separators
  return verseTexts.reduce((sum, v) => sum + v.length, 0)
    + (verseTexts.length - 1) * 2; // \n\n separators
}
```

### Batch Processing

Process chapters together to reduce API calls:

```typescript
async function generateMultipleChapters(
  chapters: ChapterData[]
): Promise<AudioAsset[]> {
  // Generate in parallel with rate limiting
  const results: AudioAsset[] = [];

  for (const chapter of chapters) {
    await sleep(500); // Rate limit
    const asset = await generateChapterAudio(chapter);
    results.push(asset);
  }

  return results;
}
```

## Testing

### Mock ElevenLabs Response

```typescript
const mockElevenLabsResponse = {
  audio_base64: 'base64encodedaudio...',
  alignment: {
    characters: ['H', 'e', 'l', 'l', 'o', '\n', '\n', 'W', 'o', 'r', 'l', 'd'],
    character_start_times_seconds: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
    character_end_times_seconds: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
  }
};
```

### Integration Test

```typescript
describe('ElevenLabs Integration', () => {
  it('generates audio with cues', async () => {
    const verses = ['Hello world', 'Goodbye world'];
    const result = await generateChapterAudio('test-voice-id', verses);

    expect(result.audioBase64).toBeDefined();
    expect(result.cues).toHaveLength(2);
    expect(result.cues[0].verse_number).toBe(1);
    expect(result.cues[1].verse_number).toBe(2);
    expect(result.cues[0].end_ms).toBeLessThanOrEqual(result.cues[1].start_ms);
  });
});
```

# Audio Cue Format Specification

## Overview

Audio cues map millisecond timestamps to verse numbers, enabling precise verse-by-verse synchronization during audio playback.

## Data Structures

### AudioCue Interface

```typescript
interface AudioCue {
  verse_number: number;  // 1-indexed verse number within chapter
  start_ms: number;      // Start time in milliseconds
  end_ms: number;        // End time in milliseconds
}
```

### BundleAudioCue (Chapter Bundle)

```typescript
interface BundleAudioCue {
  verse_number: number;
  start_ms: number;
  end_ms: number;
}
```

### Database Table

```sql
CREATE TABLE audio_cues (
  audio_id UUID REFERENCES audio_assets(id) ON DELETE CASCADE,
  verse_id UUID REFERENCES bible_schema.verses(id),
  start_ms INTEGER NOT NULL,
  end_ms INTEGER NOT NULL,
  PRIMARY KEY (audio_id, verse_id)
);

CREATE INDEX idx_audio_cues_audio_id ON audio_cues(audio_id);
CREATE INDEX idx_audio_cues_start_ms ON audio_cues(audio_id, start_ms);
```

## Cue Generation Methods

### 1. ElevenLabs Timestamps (Precise)

When ElevenLabs returns character-level timestamps:

```typescript
// ElevenLabs response format
interface ElevenLabsTimestamps {
  characters: string[];
  character_start_times_seconds: number[];
  character_end_times_seconds: number[];
}

// Conversion to verse cues
function generateCuesFromTimestamps(
  timestamps: ElevenLabsTimestamps,
  verseTexts: string[]
): AudioCue[] {
  const cues: AudioCue[] = [];
  let charIndex = 0;

  for (let i = 0; i < verseTexts.length; i++) {
    const verseLength = verseTexts[i].length;
    const startMs = timestamps.character_start_times_seconds[charIndex] * 1000;

    charIndex += verseLength;
    // Account for verse separator (\n\n = 2 chars)
    charIndex += 2;

    const endMs = charIndex < timestamps.character_end_times_seconds.length
      ? timestamps.character_end_times_seconds[charIndex - 1] * 1000
      : timestamps.character_end_times_seconds[timestamps.character_end_times_seconds.length - 1] * 1000;

    cues.push({
      verse_number: i + 1,
      start_ms: Math.round(startMs),
      end_ms: Math.round(endMs)
    });
  }

  return cues;
}
```

### 2. Character Count Estimation (Fallback)

When timestamps unavailable:

```typescript
function estimateCues(
  verseTexts: string[],
  totalDurationMs: number
): AudioCue[] {
  const totalChars = verseTexts.reduce((sum, v) => sum + v.length, 0);
  const msPerChar = totalDurationMs / totalChars;

  const cues: AudioCue[] = [];
  let currentMs = 0;

  for (let i = 0; i < verseTexts.length; i++) {
    const verseDurationMs = verseTexts[i].length * msPerChar;

    cues.push({
      verse_number: i + 1,
      start_ms: Math.round(currentMs),
      end_ms: Math.round(currentMs + verseDurationMs)
    });

    currentMs += verseDurationMs;
  }

  return cues;
}
```

## Sync Algorithm

### Finding Current Cue

```typescript
export function findCurrentCue(
  currentTimeMs: number,
  audioCues: AudioCue[]
): AudioCue | undefined {
  // Binary search for large arrays, linear for small
  if (audioCues.length > 50) {
    return binarySearchCue(currentTimeMs, audioCues);
  }

  return audioCues.find(
    cue => currentTimeMs >= cue.start_ms && currentTimeMs < cue.end_ms
  );
}

function binarySearchCue(
  timeMs: number,
  cues: AudioCue[]
): AudioCue | undefined {
  let left = 0;
  let right = cues.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    const cue = cues[mid];

    if (timeMs >= cue.start_ms && timeMs < cue.end_ms) {
      return cue;
    }

    if (timeMs < cue.start_ms) {
      right = mid - 1;
    } else {
      left = mid + 1;
    }
  }

  return undefined;
}
```

### Deduplication

Prevent redundant verse change events:

```typescript
let lastSyncedVerse = -1;

function onTimeUpdate(currentTimeMs: number, audioCues: AudioCue[]) {
  const cue = findCurrentCue(currentTimeMs, audioCues);

  if (cue && cue.verse_number !== lastSyncedVerse) {
    lastSyncedVerse = cue.verse_number;
    onVerseChange(cue.verse_number);
  }
}
```

## Seeking to Verse

```typescript
function seekToVerse(
  verseNumber: number,
  audioCues: AudioCue[],
  audioElement: HTMLAudioElement
): boolean {
  const cue = audioCues.find(c => c.verse_number === verseNumber);

  if (!cue) return false;

  audioElement.currentTime = cue.start_ms / 1000;
  return true;
}
```

## Edge Cases

### Gap Between Cues

Cues should be contiguous (end_ms of cue N = start_ms of cue N+1). If gaps exist:

```typescript
function handleGap(currentTimeMs: number, audioCues: AudioCue[]): number {
  // Find nearest cue
  const nearest = audioCues.reduce((closest, cue) => {
    const distToCurrent = Math.abs(cue.start_ms - currentTimeMs);
    const distToClosest = Math.abs(closest.start_ms - currentTimeMs);
    return distToCurrent < distToClosest ? cue : closest;
  });

  return nearest.verse_number;
}
```

### Last Verse

Ensure last cue's end_ms matches audio duration:

```typescript
function normalizeLastCue(
  cues: AudioCue[],
  totalDurationMs: number
): AudioCue[] {
  if (cues.length === 0) return cues;

  const normalized = [...cues];
  normalized[normalized.length - 1].end_ms = totalDurationMs;
  return normalized;
}
```

### Verse Ranges (Multiple Chapters)

For verse ranges spanning multiple chapters, use sequential verse_number:

```typescript
// Matt 5:1-3, 6:1-2 becomes:
const cues = [
  { verse_number: 1, start_ms: 0, end_ms: 3000 },      // Matt 5:1
  { verse_number: 2, start_ms: 3000, end_ms: 6000 },   // Matt 5:2
  { verse_number: 3, start_ms: 6000, end_ms: 9000 },   // Matt 5:3
  { verse_number: 4, start_ms: 9000, end_ms: 12000 },  // Matt 6:1
  { verse_number: 5, start_ms: 12000, end_ms: 15000 }, // Matt 6:2
];
```

## Testing

### Unit Test Examples

```typescript
describe('findCurrentCue', () => {
  const cues: AudioCue[] = [
    { verse_number: 1, start_ms: 0, end_ms: 5000 },
    { verse_number: 2, start_ms: 5000, end_ms: 10000 },
    { verse_number: 3, start_ms: 10000, end_ms: 15000 },
  ];

  it('returns correct cue at start', () => {
    expect(findCurrentCue(0, cues)?.verse_number).toBe(1);
  });

  it('returns correct cue at boundary', () => {
    expect(findCurrentCue(5000, cues)?.verse_number).toBe(2);
  });

  it('returns correct cue mid-verse', () => {
    expect(findCurrentCue(7500, cues)?.verse_number).toBe(2);
  });

  it('returns undefined past end', () => {
    expect(findCurrentCue(20000, cues)).toBeUndefined();
  });
});
```

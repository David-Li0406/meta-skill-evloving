# Current Bible Reader Architecture

## Table of Contents

1. [Reader Components](#reader-components)
2. [Data Fetching](#data-fetching)
3. [Audio System](#audio-system)
4. [Outlook System](#outlook-system)
5. [Widget/Embed System](#widgetembed-system)
6. [Key Files](#key-files)

---

## Reader Components

### Current Hierarchy

```
BibleReader.tsx (877 lines) - Main chapter reader
├── useChapterBundle hook - Single RPC for all data
├── ChapterReader.tsx (133 lines) - Pure verse list rendering
│   └── VerseRow.tsx (225 lines) - Single verse display
├── Audio playback via <audio> element
├── Swipe navigation between chapters
└── Keyboard shortcuts (Space to play/pause)
```

### Component Responsibilities

**BibleReader** (orchestrator):
- Audio playback control
- Chapter navigation (swipe, keyboard)
- Activity logging
- Listening position save
- Uses `useChapterBundle` for data

**ChapterReader** (pure display):
- Takes `verses[]` array, no fetching
- Handles scroll to verse
- Controlled/uncontrolled active verse
- Renders VerseRow for each verse

**VerseRow** (single verse):
- Outlook modes: classic, compact, minimal
- Touch/mouse interactions
- Highlight state, active state
- Action buttons on hover/tap

---

## Data Fetching

### useChapterBundle Hook

Single RPC call returns everything:

```typescript
interface ChapterBundle {
  version_id: string;
  book_id: string;
  chapter_id: string;
  book_name: string;
  chapter_number: number;
  verses: BundleVerse[];
  highlights: BundleHighlight[];
  audio: BundleAudio | null;
  next_chapter: { book: string; chapter: number } | null;
  prev_chapter: { book: string; chapter: number } | null;
  total_chapters: number;
}

interface BundleVerse {
  id: string;
  verse_number: number;
  text: string;
}

interface BundleAudio {
  audio_id: string;
  file_url: string;
  duration_ms: number;
  cues: { verse_number: number; start_ms: number; end_ms: number }[];
}
```

### RPC Functions

- `get_chapter_bundle` - Full chapter with audio cues and highlights
- `get_chapter_by_ref` - Chapter verses only
- `get_verses_by_ref` - Multiple verses by reference array

---

## Audio System

### Current Implementation

- Audio files stored per-chapter in Supabase Storage
- Audio cues embedded in `get_chapter_bundle` response
- `<audio>` element in BibleReader handles playback
- Verse highlighting driven by `timeupdate` events

### Audio Data Structure

```typescript
interface BundleAudio {
  audio_id: string;
  file_url: string;
  duration_ms: number;
  cues: {
    verse_number: number;
    start_ms: number;
    end_ms: number;
  }[];
}
```

### Current Limitations

- Audio is chapter-bound (no arbitrary verse set playback)
- No cross-chapter audio concatenation
- Single audio file per chapter

---

## Outlook System

### Current Implementation

```typescript
type ChapterOutlook = "classic" | "compact" | "minimal";
```

User preference stored and resolved by device:
- Desktop: can use any outlook
- Tablet: max compact
- Phone: forced minimal

### Outlook Effects

| Aspect | Classic | Compact | Minimal |
|--------|---------|---------|---------|
| Verse spacing | normal | tight | none |
| Verse number | badge | superscript | inline-subtle |
| Actions on hover | yes | yes | no |
| Clickable verses | yes | yes | no |
| Container padding | normal | compact | none |

---

## Widget/Embed System

### Edge Function: embed

Location: `supabase/functions/embed/index.ts`

**Endpoint:** `GET /functions/v1/embed?ref=Joh.3:16&version=finstlk201`

**Response:**
```typescript
{
  reference: "Johannes 3:16",
  version: "Suomalainen raamatunkäännös",
  versionCode: "finstlk201",
  verses: [{ number: 16, text: "Sillä niin..." }],
  audio: {
    available: true,
    url: "https://...",
    startTime: 45.2,
    endTime: 52.8
  },
  link: "https://raamattu-nyt.fi/?book=Johannes&chapter=3&verse=16"
}
```

### widget.js

Location: `apps/raamattu-nyt/public/widget.js`

Features:
- Shadow DOM isolation
- Fetches from embed API
- Audio playback with time segments
- Self-contained styling
- MutationObserver for dynamic widgets

**Usage:**
```html
<script src="https://raamattu-nyt.fi/widget.js" defer></script>
<div class="rn-bible" data-ref="Joh.3:16"></div>
```

### Current Limitations

- Single reference only (no verse sets)
- No range spanning chapters
- Fixed minimal styling
- No outlook selection

---

## Key Files

| Component | Path |
|-----------|------|
| BibleReader | `apps/raamattu-nyt/src/components/BibleReader.tsx` |
| ChapterReader | `apps/raamattu-nyt/src/components/reader/ChapterReader.tsx` |
| VerseRow | `apps/raamattu-nyt/src/components/reader/VerseRow.tsx` |
| Reader types | `apps/raamattu-nyt/src/components/reader/types.ts` |
| useChapterBundle | `apps/raamattu-nyt/src/hooks/useChapterBundle.tsx` |
| embed function | `supabase/functions/embed/index.ts` |
| widget.js | `apps/raamattu-nyt/public/widget.js` |
| verseParser | `apps/raamattu-nyt/src/lib/verseParser.ts` |
| bookNameMapping | `apps/raamattu-nyt/src/lib/bookNameMapping.ts` |

---

## Version Codes

- `finstlk201` - Finnish 1992/2012 translation (default)
- Additional versions configured in `bible_schema.bible_versions`

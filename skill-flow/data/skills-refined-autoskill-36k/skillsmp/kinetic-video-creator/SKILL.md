---
name: kinetic-video-creator
description: "Create professional kinetic typography videos from scratch. Includes speech writing, TTS with emotional dynamics, music generation, and animated text. Use for: promo videos, explainers, social content, inspirational speeches, product launches."
argument-hint: [topic] [tone: inspirational/dramatic/energetic/calm]
enhancedBy:
  - speech-generator: "TTS with aviz's cloned voice - optimized for Hebrew"
  - transcribe: "Word-level timing for animation sync"
  - music-generator: "Background music matching emotional arc"
  - youtube-uploader: "Optional publishing"
---

# Kinetic Video Creator

Create stunning kinetic typography videos with AI-generated speech, music, and dynamic animations.

## Workflow Overview

1. **Script** → Craft emotionally compelling speech text
2. **Speech** → Use `/speech-generator` skill for TTS
3. **Transcribe** → Use `/transcribe` skill for word timing
4. **Music** → Use `/music-generator` skill for background
5. **Merge** → Combine speech + music
6. **Animate** → Create kinetic typography in Remotion
7. **Render** → Produce final video
8. **Publish** → Use `/youtube-uploader` skill (optional)

---

## Step 1: Craft the Script

### Language Selection

**Hebrew (Recommended for aviz's voice):**
- Use Hebrew emotional directions in brackets
- Add natural Hebrew filler words
- See "Hebrew Script Guidelines" section below

**English:**
- Use English emotional directions
- See "English Script Guidelines" section below

---

## Hebrew Script Guidelines

aviz's cloned voice is optimized for Hebrew. Use these Hebrew directions:

### Hebrew Emotional Directions

| Direction | Effect |
|-----------|--------|
| `[נשימה עמוקה]` | Deep breath, pause |
| `[בהתלהבות]` | Enthusiastic |
| `[ברצינות]` | Serious tone |
| `[בעצב]` | Sad, emotional |
| `[בשקט]` | Quiet, intimate |
| `[מהר]` | Fast pace |
| `[לאט ובבירור]` | Slow and clear |
| `[שאלה]` | Question tone |
| `[הפתעה]` | Surprise |
| `[צחוק קל]` | Light laugh |
| `[בחום]` | Warm tone |
| `[בכוח]` | Powerful, emphatic |

### Hebrew Filler Words (for natural flow)

- `אממ...` - hesitation
- `אהה...` - thinking
- `כאילו...` - like
- `נו...` - well
- `יאללה...` - come on
- `בקיצור...` - in short
- `...` - pause

### Hebrew Script Example

```
[נשימה עמוקה] יש רגע...
[לאט ובבירור] רגע שהכל משתנה.

[ברצינות] אבא שלי חלה בפוליו כשהיה תינוק.
כל חייו הוא היה על כיסא גלגלים.

[בהתלהבות] אבל אבא שלי? הוא היה ספורטאי מצטיין!
[בחום] הוא תמיד האמין... שאפשר להגשים כל חלום.

[בעצב] כשהייתי בן חמש עשרה... אבא נפטר.

[בכוח] והכאב הזה? הפך למשימה שלי.
[בחום] לעזור לאנשים אחרים להגשים את החלומות שלהם.
```

---

## English Script Guidelines

### English Emotional Directions

| Direction | Effect |
|-----------|--------|
| `[pause]` | Brief pause |
| `[long pause]` | Extended pause |
| `[slowly]` | Slower delivery |
| `[faster]` | Quickened pace |
| `[whisper]` | Softer, intimate |
| `[emphatic]` | Strong emphasis |
| `[building]` | Increasing intensity |
| `[warm]` | Friendly tone |
| `[dramatic]` | Theatrical |
| `[matter-of-fact]` | Conversational |

### English Script Template

```
[HOOK - 5-10 seconds]
[dramatic pause] Opening line that grabs attention.
[slowly, with weight] The provocative statement.

[BUILD - 20-40 seconds]
[building intensity] Establish the context.
[pause for effect] Key insight moment.

[PEAK - 20-30 seconds]
[powerful, emphatic] The main message.
[pause] Let it land.

[RESOLVE - 15-25 seconds]
[warm, inspiring] Paint the vision.
[final beat] Memorable closing.
```

---

## Step 2: Generate Speech

**Use the speech-generator skill:**

```
/speech-generator [path/to/script.txt] -o [path/to/speech.mp3]
```

Or invoke directly:
```bash
cd ~/.claude/skills/speech-generator/scripts
npx ts-node generate_speech.ts -f script.txt -o speech.mp3
```

**Important:** The speech-generator uses aviz's cloned voice, which works best with Hebrew text and Hebrew emotional directions.

---

## Step 3: Transcribe for Timing

**Use the transcribe skill:**

```
/transcribe [path/to/speech.mp3] --json
```

Or invoke directly:
```bash
cd ~/.claude/skills/transcribe/scripts
npx ts-node transcribe.ts -i speech.mp3 -o transcript.srt --json
```

Output: `transcript_transcript.json` with word-level timing data.

---

## Step 4: Generate Background Music

**Use the music-generator skill:**

```
/music-generator [composition.json] -o background_music.mp3
```

### Music Composition Template

```json
{
  "duration_ms": 75000,
  "instrumental": true,
  "positive_global_styles": ["cinematic", "inspirational"],
  "negative_global_styles": ["aggressive", "chaotic"],
  "sections": [
    {
      "section_name": "Hook - Mysterious",
      "duration_ms": 12000,
      "positive_local_styles": ["suspenseful", "soft"],
      "negative_local_styles": ["loud"],
      "lines": []
    },
    {
      "section_name": "Build - Rising",
      "duration_ms": 25000,
      "positive_local_styles": ["hopeful", "building"],
      "negative_local_styles": ["slow"],
      "lines": []
    },
    {
      "section_name": "Peak - Triumphant",
      "duration_ms": 20000,
      "positive_local_styles": ["triumphant", "uplifting"],
      "negative_local_styles": ["quiet"],
      "lines": []
    }
  ]
}
```

---

## Step 5: Merge Audio

```bash
ffmpeg -y \
  -i speech.mp3 \
  -i background_music.mp3 \
  -filter_complex "[0:a]volume=1.0[speech];[1:a]volume=0.15[music];[speech][music]amix=inputs=2:duration=first[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 \
  final_audio.mp3
```

---

## Step 6: Create Remotion Composition

### Project Location

```bash
cd /Users/aviz/remotion-assistant
```

### Default Template: SequenceComposition (One Word Per Screen)

**Recommended:** Use `SequenceComposition` for maximum impact - displays one word at a time with full-screen typography.

```tsx
import { SequenceComposition } from '../templates/SequenceComposition';
import transcriptData from '../../projects/[project]/transcript_transcript.json';

const WORD_TIMINGS = transcriptData.words
  .filter((w) => w.word.trim() !== '')
  .map((w) => ({
    word: w.word,
    start: w.start,
    end: w.end,
  }));

export const MyVideo: React.FC = () => {
  return (
    <SequenceComposition
      wordTimings={WORD_TIMINGS}
      audioFile="[project]/final_audio.mp3"
      baseFontSize={200}
      dustEnabled={true}
      lightBeamsEnabled={true}
      centerGlowEnabled={true}
      glowIntensity={1}
      anticipationFrames={5}
      colorSchemeStart={0}
    />
  );
};
```

### Alternative: MultiWordComposition (Word Cloud)

Use for faster-paced content with multiple words on screen:

```tsx
import { MultiWordComposition } from '../templates/MultiWordComposition';
```

### Hebrew Font Support

For Hebrew text, use Heebo font:

```tsx
import { loadFont } from '@remotion/google-fonts/Heebo';

const { fontFamily } = loadFont('normal', {
  weights: ['400', '600', '700', '900'],
  subsets: ['hebrew', 'latin'],
});
```

Add RTL styling:
```tsx
style={{
  direction: 'rtl',
  fontFamily,
}}
```

---

## Step 7: Render

```bash
cd /Users/aviz/remotion-assistant
npx remotion render CompositionName output.mp4
```

---

## Step 8: Upload (Optional)

**Use the youtube-uploader skill:**

```
/youtube-uploader [video.mp4] --title "Title" --description "Description"
```

---

## Project Structure

```
remotion-assistant/
├── public/[project]/
│   └── final_audio.mp3      # Audio for Remotion
├── projects/[project]/
│   ├── speech.txt           # Script
│   ├── speech.mp3           # TTS output
│   ├── transcript_transcript.json  # Word timings
│   ├── music_composition.json
│   ├── background_music.mp3
│   ├── final_audio.mp3      # Merged audio
│   └── output.mp4           # Final video
└── src/compositions/
    └── [ProjectName].tsx    # Composition
```

---

## Quick Reference

| Step | Skill/Command |
|------|---------------|
| Speech | `/speech-generator script.txt -o speech.mp3` |
| Transcribe | `/transcribe speech.mp3 --json` |
| Music | `/music-generator composition.json` |
| Merge | `ffmpeg` (see above) |
| Render | `npx remotion render Name output.mp4` |
| Upload | `/youtube-uploader output.mp4` |

# Complete Workflow Example

## Project: "The Future of Remote Work"
**Tone:** Inspirational, forward-looking
**Duration:** ~90 seconds

---

## Step 1: Script with Emotional Brackets

**File:** `script.txt`

```
[dramatic pause] Remote work isn't the future.

[slowly, with weight] It's... [pause] the present.

[building] But here's what nobody's talking about:
The offices aren't just empty.
[emphatic] The old rules are extinct.

[pause]
[matter-of-fact] Commutes? Gone.
[faster] Cubicles? Relics.
[emphatic] The nine-to-five? [long pause] A memory.

[warm, building] And in their place?
[excited] Freedom.
Flexibility.
[pause] Focus.

[emphatic] Real focus.
[slowly] The kind you can only find...
[whisper] in your own space.

[building intensity] Teams across continents.
Collaboration across time zones.
[excited] Ideas flowing at the speed of thought.

[pause]
[dramatic] This is the revolution they said wouldn't work.

[warm, hopeful] But you knew better.
[pause]
[slowly, with weight] You were already living it.

[emphatic] The future of work... [pause]
[warm, descending] is wherever you are.
```

**Word count:** ~130 words (~55 seconds of speech)

---

## Step 2: Storyboard JSON

**File:** `storyboard.json`

```json
{
  "title": "The Future of Remote Work",
  "duration_seconds": 55,
  "segments": [
    {
      "name": "Hook",
      "time_range": [0, 8],
      "style": "minimal-dramatic",
      "background": "dark-gradient",
      "word_treatment": "fade-in-center",
      "emphasis_words": ["Remote", "future", "present"],
      "transition_out": "fade-to-black"
    },
    {
      "name": "Problem Setup",
      "time_range": [8, 22],
      "style": "dynamic-stack",
      "background": "animated-particles",
      "word_treatment": "slide-from-sides",
      "emphasis_words": ["nobody's", "extinct", "Gone", "Relics", "memory"],
      "transition_out": "zoom-blur"
    },
    {
      "name": "Solution Reveal",
      "time_range": [22, 35],
      "style": "explosive-center",
      "background": "radial-glow",
      "word_treatment": "scale-bounce",
      "emphasis_words": ["Freedom", "Flexibility", "Focus", "Real"],
      "transition_out": "flash-white"
    },
    {
      "name": "Vision",
      "time_range": [35, 48],
      "style": "slide-cascade",
      "background": "animated-particles",
      "word_treatment": "blur-reveal",
      "emphasis_words": ["Teams", "continents", "revolution"],
      "transition_out": "fade-to-black"
    },
    {
      "name": "Resolution",
      "time_range": [48, 55],
      "style": "calm-elegant",
      "background": "soft-gradient",
      "word_treatment": "gentle-fade",
      "emphasis_words": ["future", "wherever"],
      "transition_out": "slow-fade"
    }
  ]
}
```

---

## Step 3: Generate Speech

```bash
cd ~/.claude/skills/speech-generator/scripts

npx ts-node generate_speech.ts \
  -f ~/projects/remote-work-video/script.txt \
  -o ~/projects/remote-work-video/speech.mp3
```

**Output:** `speech.mp3` (~55 seconds)

---

## Step 4: Transcribe for Timing

```bash
cd ~/.claude/skills/transcribe/scripts

npx ts-node transcribe.ts \
  -i ~/projects/remote-work-video/speech.mp3 \
  -o ~/projects/remote-work-video/transcript.srt \
  --json
```

**Outputs:**
- `transcript.srt` - Subtitle file
- `transcript.json` - Word-level timing data

---

## Step 5: Music Composition

**File:** `music_composition.json`

```json
{
  "duration_ms": 60000,
  "instrumental": true,
  "positive_global_styles": [
    "cinematic",
    "modern electronic",
    "inspirational",
    "corporate premium"
  ],
  "negative_global_styles": [
    "aggressive",
    "sad",
    "chaotic"
  ],
  "sections": [
    {
      "section_name": "Mysterious Opening",
      "duration_ms": 8000,
      "positive_local_styles": [
        "atmospheric",
        "subtle tension",
        "sparse synths"
      ],
      "negative_local_styles": ["loud", "fast"],
      "lines": []
    },
    {
      "section_name": "Problem Tension",
      "duration_ms": 14000,
      "positive_local_styles": [
        "building rhythm",
        "subtle drums enter",
        "momentum"
      ],
      "negative_local_styles": ["calm", "peaceful"],
      "lines": []
    },
    {
      "section_name": "Solution Energy",
      "duration_ms": 13000,
      "positive_local_styles": [
        "driving beat",
        "uplifting",
        "energetic",
        "synth melody"
      ],
      "negative_local_styles": ["slow", "mellow"],
      "lines": []
    },
    {
      "section_name": "Vision Peak",
      "duration_ms": 13000,
      "positive_local_styles": [
        "triumphant",
        "full arrangement",
        "powerful",
        "emotional"
      ],
      "negative_local_styles": ["soft", "understated"],
      "lines": []
    },
    {
      "section_name": "Hopeful Resolution",
      "duration_ms": 12000,
      "positive_local_styles": [
        "warm",
        "hopeful fade",
        "gentle",
        "resolution"
      ],
      "negative_local_styles": ["intense", "building"],
      "lines": []
    }
  ]
}
```

```bash
cd ~/.claude/skills/music-generator/scripts

npx ts-node generate_music.ts \
  --composition ~/projects/remote-work-video/music_composition.json \
  --output ~/projects/remote-work-video/music.mp3
```

---

## Step 6: Merge Audio

```bash
cd ~/projects/remote-work-video

ffmpeg -y \
  -i speech.mp3 \
  -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[speech];[1:a]volume=0.17[music];[speech][music]amix=inputs=2:duration=first:dropout_transition=2[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 \
  speech_with_music.mp3
```

---

## Step 7: Create Remotion Composition

See [remotion-composition.md](../templates/remotion-composition.md) for the full component code.

Key implementation points:
1. Import `transcript.json` for word timing
2. Import `storyboard.json` for segment styles
3. Configure 9:16 aspect ratio (1080x1920) for social
4. Use spring animations for natural motion

---

## Step 8: Render

```bash
cd ~/remotion-project

npx remotion render src/index.ts RemoteWorkVideo output.mp4 \
  --props='{"wordsFile":"transcript.json","storyboardFile":"storyboard.json","audioFile":"speech_with_music.mp3"}'
```

---

## Step 9: Upload to YouTube

```bash
cd ~/.claude/skills/youtube-uploader/scripts

npx ts-node youtube-upload.ts \
  --video ~/projects/remote-work-video/output.mp4 \
  --title "The Future of Remote Work | Kinetic Typography" \
  --description "Remote work isn't the future. It's the present.

This kinetic typography video explores how the workplace has fundamentally changed and why the future of work is wherever you are.

#RemoteWork #FutureOfWork #WorkFromAnywhere #KineticTypography" \
  --tags "remote work,future of work,work from home,kinetic typography,motivation" \
  --privacy unlisted \
  --category 28
```

---

## Final Output

| File | Description |
|------|-------------|
| `script.txt` | Speech text with emotional brackets |
| `storyboard.json` | Animation plan |
| `speech.mp3` | Generated TTS |
| `transcript.json` | Word-level timing |
| `music.mp3` | Background music |
| `speech_with_music.mp3` | Merged audio |
| `output.mp4` | Final video |

**Total process time:** ~15-20 minutes
**Video duration:** ~55 seconds
**Video format:** 1080x1920 (9:16 vertical)

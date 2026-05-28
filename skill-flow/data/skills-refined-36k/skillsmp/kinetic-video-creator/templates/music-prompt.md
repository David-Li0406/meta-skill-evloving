# Music Generation Guide

## Emotional Arc Matching

Your music should follow the same emotional trajectory as your speech:

```
HOOK:    Mysterious, tension-building
BUILD:   Rising energy, momentum
PEAK:    Powerful, triumphant
RESOLVE: Warm, inspiring, gentle descent
```

## Composition JSON Structure

```json
{
  "duration_ms": 120000,
  "instrumental": true,
  "positive_global_styles": ["cinematic", "inspirational", "modern"],
  "negative_global_styles": ["aggressive", "discordant", "chaotic"],
  "sections": []
}
```

## Section Templates by Emotion

### Hook Section (5-15 seconds)
```json
{
  "section_name": "Hook - Mysterious",
  "duration_ms": 10000,
  "positive_local_styles": [
    "suspenseful",
    "atmospheric",
    "building anticipation",
    "sparse arrangement"
  ],
  "negative_local_styles": [
    "loud",
    "fast tempo",
    "busy"
  ],
  "lines": []
}
```

### Build Section (30-60 seconds)
```json
{
  "section_name": "Build - Rising Energy",
  "duration_ms": 45000,
  "positive_local_styles": [
    "driving rhythm",
    "building momentum",
    "layered instrumentation",
    "energetic"
  ],
  "negative_local_styles": [
    "calm",
    "slow",
    "minimal"
  ],
  "lines": []
}
```

### Peak Section (15-30 seconds)
```json
{
  "section_name": "Peak - Triumphant",
  "duration_ms": 25000,
  "positive_local_styles": [
    "powerful",
    "triumphant",
    "full orchestra",
    "emotional climax",
    "anthemic"
  ],
  "negative_local_styles": [
    "soft",
    "mellow",
    "understated"
  ],
  "lines": []
}
```

### Resolve Section (15-30 seconds)
```json
{
  "section_name": "Resolve - Hopeful Fade",
  "duration_ms": 25000,
  "positive_local_styles": [
    "warm",
    "hopeful",
    "gentle resolution",
    "nostalgic",
    "fade out"
  ],
  "negative_local_styles": [
    "intense",
    "fast",
    "building"
  ],
  "lines": []
}
```

---

## Style Keywords Reference

### By Mood

| Mood | Keywords |
|------|----------|
| Mysterious | atmospheric, suspenseful, dark synths, tension |
| Building | momentum, rising, driving, anticipation |
| Powerful | triumphant, epic, full, powerful, anthemic |
| Hopeful | warm, inspiring, uplifting, optimistic |
| Emotional | touching, heartfelt, moving, nostalgic |
| Energetic | fast, dynamic, exciting, pulse-pounding |
| Calm | peaceful, serene, gentle, soft |

### By Genre

| Genre | Keywords |
|-------|----------|
| Cinematic | orchestral, film score, sweeping, dramatic |
| Electronic | synths, modern, digital, pulsing |
| Corporate | professional, motivational, uplifting |
| Epic | massive, grandiose, powerful, soaring |
| Ambient | atmospheric, textural, floating, ethereal |
| Pop | catchy, modern, polished, bright |

### By Instrument Focus

| Focus | Keywords |
|-------|----------|
| Orchestral | strings, brass, woodwinds, timpani |
| Electronic | synths, pads, arpeggios, bass drops |
| Hybrid | orchestra meets electronics, modern epic |
| Piano | piano-driven, intimate, emotional |
| Drums | percussion-focused, tribal, rhythmic |

---

## Complete Example: 2-Minute Inspirational Video

```json
{
  "duration_ms": 120000,
  "instrumental": true,
  "positive_global_styles": [
    "cinematic",
    "inspirational",
    "modern electronic",
    "orchestral hybrid"
  ],
  "negative_global_styles": [
    "aggressive",
    "heavy metal",
    "discordant",
    "scary"
  ],
  "sections": [
    {
      "section_name": "Mysterious Intro",
      "duration_ms": 12000,
      "positive_local_styles": [
        "atmospheric",
        "suspenseful",
        "sparse synths",
        "building tension"
      ],
      "negative_local_styles": ["loud", "fast", "busy"],
      "lines": []
    },
    {
      "section_name": "Rising Foundation",
      "duration_ms": 23000,
      "positive_local_styles": [
        "add subtle drums",
        "building momentum",
        "synth arpeggios",
        "growing intensity"
      ],
      "negative_local_styles": ["calm", "static"],
      "lines": []
    },
    {
      "section_name": "Main Theme Emerges",
      "duration_ms": 25000,
      "positive_local_styles": [
        "driving rhythm",
        "melodic theme",
        "energetic",
        "strings enter"
      ],
      "negative_local_styles": ["slow", "mellow"],
      "lines": []
    },
    {
      "section_name": "Powerful Peak",
      "duration_ms": 25000,
      "positive_local_styles": [
        "triumphant",
        "full orchestral",
        "emotional climax",
        "powerful drums",
        "soaring melody"
      ],
      "negative_local_styles": ["soft", "understated"],
      "lines": []
    },
    {
      "section_name": "Emotional Landing",
      "duration_ms": 20000,
      "positive_local_styles": [
        "warm",
        "hopeful",
        "gentle descent",
        "piano prominent"
      ],
      "negative_local_styles": ["intense", "building"],
      "lines": []
    },
    {
      "section_name": "Inspiring Outro",
      "duration_ms": 15000,
      "positive_local_styles": [
        "fade out",
        "nostalgic",
        "resolution",
        "lingering warmth"
      ],
      "negative_local_styles": ["abrupt", "harsh"],
      "lines": []
    }
  ]
}
```

---

## Simple Prompt Alternative

If not using detailed composition mode:

```
Epic cinematic instrumental music for an inspirational tech speech.

Emotional arc:
- 0-15s: Mysterious, atmospheric opening with sparse synths
- 15-45s: Building momentum with driving rhythm and arpeggios
- 45-75s: Powerful peak with full orchestral arrangement
- 75-100s: Warm, hopeful resolution
- 100-120s: Gentle fade to silence

Style: Modern orchestral hybrid, electronic meets cinematic
Mood: Inspirational, forward-looking, triumphant
No vocals, instrumental only
```

---

## Audio Mixing Recommendations

| Element | Volume Level |
|---------|--------------|
| Speech | 100% (0dB) |
| Music - Under speech | 15-20% (-14 to -16dB) |
| Music - Transitions | 25-30% (-10 to -12dB) |
| Music - Intro/Outro | 40-50% (-6 to -8dB) |

### FFmpeg Mix Command

```bash
ffmpeg -y \
  -i speech.mp3 \
  -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[speech];[1:a]volume=0.18[music];[speech][music]amix=inputs=2:duration=first:dropout_transition=2[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 \
  final_audio.mp3
```

Adjust `volume=0.18` (music) based on:
- Quiet music: 0.12-0.15
- Normal music: 0.15-0.20
- Dramatic sections: 0.20-0.25

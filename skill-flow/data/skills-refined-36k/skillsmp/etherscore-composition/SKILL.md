---
name: etherscore-composition
description: Auto-loads when discussing composition, notes, patterns, or creating EtherScore files
auto_trigger:
  - "compose"
  - "composition"
  - "create a track"
  - "write music"
  - "notes"
  - "pattern"
  - "melody"
  - "chord"
  - "drums"
---

# EtherScore Composition Skill

Complete reference for composing music with EtherScore format.

## Note Syntax

```
<pitch><octave>:<duration>[modifiers]
```

### Basic Notes
| Example | Description |
|---------|-------------|
| `C4:q` | C in octave 4, quarter note |
| `D#5:h` | D# in octave 5, half note |
| `Bb3:8` | Bb in octave 3, eighth note |
| `r:q` | Quarter note rest |

### Durations
| Symbol | Duration |
|--------|----------|
| `w` | Whole note (4 beats) |
| `h` | Half note (2 beats) |
| `q` | Quarter note (1 beat) |
| `8` | Eighth note (1/2 beat) |
| `16` | Sixteenth note (1/4 beat) |
| `32` | Thirty-second note |

### Modifiers
| Modifier | Effect | Example |
|----------|--------|---------|
| `.` | Dotted (1.5x duration) | `C4:q.` |
| `t3` | Triplet | `C4:8t3` |
| `*` | Staccato | `C4:q*` |
| `~` | Legato | `C4:q~` |
| `>` | Accent | `C4:q>` |
| `~>` | Portamento | `C4:q~>` |
| `.fall` | Jazz fall | `C4:q.fall` |
| `.tr` | Trill | `C4:q.tr` |
| `@mf` | Dynamics | `C4:q@mf` |
| `?0.7` | 70% probability | `C4:q?0.7` |

### Dynamics
`@pp`, `@p`, `@mp`, `@mf`, `@f`, `@ff`

## Pattern Types

### Notes Pattern (melody)
```json
{
  "name": "melody",
  "notes": "C4:q E4:q G4:h | D4:q F4:q A4:h"
}
```

### Chords Pattern
```json
{
  "name": "progression",
  "chords": "Am7:h Dm9:h | G7:h Cmaj7:h"
}
```

### Drums Pattern (shorthand v0.81)
```json
{
  "name": "beat",
  "kit": "808",
  "kick": "x...x...",
  "snare": "....x...",
  "hihat": "x.x.x.x."
}
```

### Arpeggio Pattern
```json
{
  "name": "arp",
  "arpeggio": {
    "chord": "Am7",
    "pattern": "up",
    "rate": "8n"
  }
}
```

### Euclidean Pattern
```json
{
  "name": "euclidean_beat",
  "euclidean": {
    "pulses": 5,
    "steps": 8,
    "sound": "kick"
  }
}
```

### Markov Pattern
```json
{
  "name": "walking",
  "markov": {
    "preset": "walking_bass",
    "steps": 16
  }
}
```

### Voice-Led Chords
```json
{
  "name": "smooth_chords",
  "voiceLead": {
    "progression": ["Am7", "Dm7", "G7", "Cmaj7"],
    "voicing": "close"
  }
}
```

## Track Options

```json
{
  "pattern": "melody",
  "instrument": "fm_epiano",
  "repeat": 4,
  "velocity": 0.8,
  "humanize": 0.02,
  "groove": "dilla",
  "velocityEnvelope": "crescendo"
}
```

### Available Grooves (14)
`straight`, `shuffle`, `funk`, `laid_back`, `dilla`, `reggae`, `dnb`, `trap`, `gospel`, `bossa`, `afrobeat`, `swing`, `house`, `techno`

### Velocity Envelopes
`crescendo`, `diminuendo`, `swell`, `accent_2_4`, `constant`

## Instrument Configuration

```json
{
  "instruments": {
    "lead": {
      "preset": "fm_epiano",
      "params": { "brightness": 0.7, "warmth": 0.5 },
      "volume": -3,
      "effects": [
        { "type": "reverb", "wet": 0.3, "decay": 2.0 },
        { "type": "delay", "wet": 0.2, "time": "8n" }
      ]
    }
  }
}
```

### Layering (v0.8)
```json
{
  "layers": [
    { "preset": "saw", "detune": -5 },
    { "preset": "saw", "detune": 5 }
  ]
}
```

### LFO (v0.8)
```json
{
  "lfo": {
    "rate": "8n",
    "target": "filterCutoff",
    "depth": 0.5
  }
}
```

## Complete Composition Template

```json
{
  "title": "Track Title",
  "composer": "Claude",
  "bpm": 120,
  "timeSignature": "4/4",
  "key": "C",
  "scale": "minor",

  "instruments": {
    "bass": { "preset": "sub_bass", "volume": -6 },
    "lead": { "preset": "fm_epiano", "volume": -3 },
    "drums": { "kit": "808" }
  },

  "patterns": [
    { "name": "bassline", "notes": "C2:q r:8 C2:8 | Eb2:q r:8 Eb2:8" },
    { "name": "melody", "notes": "G4:h Eb4:q C4:q | G4:q Bb4:h." },
    { "name": "beat", "kit": "808", "kick": "x...", "snare": "..x." }
  ],

  "structure": [
    {
      "name": "verse",
      "bars": 8,
      "tracks": [
        { "pattern": "bassline", "instrument": "bass", "repeat": 4 },
        { "pattern": "melody", "instrument": "lead", "repeat": 2 },
        { "pattern": "beat", "instrument": "drums", "repeat": 8 }
      ]
    }
  ]
}
```

## Best Practices

1. **Start simple** - Basic patterns first, add complexity later
2. **Use humanize** - 0.01-0.03 for natural feel
3. **Balance volumes** - Drums -6, bass -6, leads -3
4. **Layer thoughtfully** - Don't overcrowd frequency ranges
5. **Validate often** - `npx tsx src/cli.ts validate file.json`

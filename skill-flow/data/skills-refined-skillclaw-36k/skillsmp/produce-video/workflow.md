# Production Workflow Reference

Detailed guide for end-to-end video production.

## Prerequisites

1. Server running: `npm start` (http://localhost:3000)
2. API keys configured in `data/config.json`:
   - `anthropicKey` - Claude API
   - `googleApiKey` - Veo/Gemini
   - `elevenLabsKey` - TTS (optional)

## Complete Workflow

### Phase 1: Structure Generation

Generate a project structure from a concept:

```bash
curl -X POST http://localhost:3000/api/generate-project-from-structure \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "A lone astronaut discovers an alien artifact on Mars",
    "duration": 45,
    "arc": "tension-release",
    "style": "cinematic, sci-fi, dramatic lighting",
    "production_style": "documentary",
    "include_vo": true,
    "include_dialogue": false
  }'
```

**Response includes:**
- `characters[]` - Generated characters with descriptions
- `environments[]` - Generated locations
- `shots[]` - Shot breakdown with timing, mood, energy, tension

### Phase 2: Character/Environment Locking (Optional)

Lock a character's appearance for consistency:

```bash
curl -X POST http://localhost:3000/api/lock-character \
  -H "Content-Type: application/json" \
  -d '{
    "character": {
      "id": "astronaut_1",
      "description": "A weathered astronaut in a worn spacesuit"
    },
    "style": "cinematic, sci-fi"
  }'
```

**Response includes:**
- `locked_description` - Immutable features (30-50 words)
- `base_image_path` - Reference image path

**IMPORTANT:** When executing, include `locked_description` in the character object:
```json
{
  "characters": [{
    "id": "astronaut_1",
    "description": "Original...",
    "locked_description": "A weathered astronaut...",
    "locked": true
  }]
}
```

### Phase 3: Project Execution

Submit all shots for Veo generation:

```bash
curl -X POST http://localhost:3000/api/execute-project \
  -H "Content-Type: application/json" \
  -d '{
    "project": <full_project_from_phase_1>,
    "style": "cinematic, sci-fi",
    "aspectRatio": "9:16"
  }'
```

**Response includes:**
- `jobs[]` - Array of job IDs and Veo prompts

### Phase 4: Job Polling

Poll each job until complete:

```bash
curl http://localhost:3000/api/jobs/<job_id>
```

**Status values:**
- `pending` - Queued
- `processing` - Veo generating
- `completed` - Video ready
- `failed` - Generation failed

### Phase 5: Assembly

Combine all clips into final video:

```bash
curl -X POST http://localhost:3000/api/assemble \
  -H "Content-Type: application/json" \
  -d '{
    "shots": <shots_from_project>,
    "audioLayers": [
      {"type": "music", "file": "data/audio/ambient.mp3", "volume": 0.3}
    ],
    "outputFilename": "mars_discovery.mp4"
  }'
```

## Arc Types

| Arc | Pattern | Use Case |
|-----|---------|----------|
| `linear-build` | Steady rise | Building intensity |
| `tension-release` | Build → drop | Climax and resolution |
| `wave` | Rise/fall cycles | Multiple peaks |
| `flat-punctuate` | Steady + spikes | Surprise moments |
| `bookend` | High-low-high | Full circle stories |

## Production Styles

| Style | Camera | Visual | Continuity |
|-------|--------|--------|------------|
| `stage_play` | Fixed front | Theatrical | Single location |
| `documentary` | Observational | Natural, grain | Real-time |
| `music_video` | Dynamic | Saturated | Fragmented |
| `noir` | Character POV | Monochrome | Elliptical |

## Troubleshooting

### VFX prompts failing
Avoid: neon, hologram, glowing, complex physics
Use: practical lighting, natural effects

### Character inconsistency
Always lock characters before multi-shot sequences

### Static position not honored
Veo adds entrance movement. Accept ~1s lead-in or use reference frames.

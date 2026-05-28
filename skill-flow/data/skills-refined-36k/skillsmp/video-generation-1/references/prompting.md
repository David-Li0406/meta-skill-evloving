# Video Prompting Guide

Effective video prompts for Veo 3.1 follow a structured approach. This guide
provides the 6-part formula and best practices for generating high-quality
videos.

## 6-Part Prompt Formula

### 1. Cinematography

Define the technical camera setup:

- **Shot size**: Close-up (CU), medium shot (MS), wide shot (WS), extreme
  close-up (ECU)
- **Camera angle**: Eye-level, low angle, high angle, bird's eye, Dutch angle
- **Camera movement**: Static, pan, tilt, dolly, tracking, crane, handheld
- **Lens**: 85mm portrait, 14mm wide, 35mm standard, anamorphic

**Examples:**

- "Wide establishing shot from a low angle"
- "Close-up with shallow depth of field, 85mm lens"
- "Slow dolly push-in from medium shot to close-up"
- "Handheld tracking shot following the subject"

### 2. Subject

Provide exhaustive detail to prevent AI hallucination:

- **Appearance**: 15+ descriptive attributes
- **Clothing/texture**: Specific materials, colors, patterns
- **Position**: Where in frame, posture, orientation
- **Identity markers**: Distinctive features that persist across frames

**Examples:**

- "A middle-aged woman with silver-streaked black hair, warm brown eyes, wearing
  a weathered denim jacket over a cream sweater"
- "A vintage red 1957 Chevrolet Bel Air, chrome details gleaming, whitewall
  tires, positioned center-frame facing camera"

### 3. Action

One concrete action per clip. Use verbs, not states:

- **Single action**: One primary movement or change
- **Active voice**: "walks" not "is walking"
- **Specific verbs**: "strides confidently" vs "moves"

**Good:**

- "turns slowly to face the camera"
- "reaches for the door handle"
- "takes a sip of coffee while glancing at phone"

**Bad:**

- "is standing there" (state, not action)
- "walks, talks, and waves" (too many actions)

### 4. Context

Define the environment and conditions:

- **Location**: Specific setting with detail
- **Time of day**: Golden hour, midday, blue hour, night
- **Weather**: Clear, overcast, rain, fog, snow
- **Props/elements**: Objects that ground the scene

**Examples:**

- "in a cozy Brooklyn coffee shop, morning light streaming through large
  windows, exposed brick walls"
- "on a rain-slicked Tokyo street at night, neon reflections on wet pavement,
  umbrellas passing"

### 5. Style

Define the visual aesthetic:

- **Film look**: 35mm film grain, anamorphic flares, digital clean
- **Color grading**: Warm/cool tones, desaturated, high contrast
- **Director reference**: "in the style of..." (use sparingly)
- **Genre**: Documentary, commercial, cinematic, music video

**Examples:**

- "35mm film grain, warm color grading reminiscent of late 90s photography"
- "Clean commercial aesthetic, high contrast, vibrant saturated colors"
- "Naturalistic documentary style, available light only"

### 6. Audio (when using --audio flag)

Specify sound design:

- **Dialogue**: Put speech in quotes with delivery notes
- **Sound effects**: Use `SFX:` prefix
- **Ambient**: Describe background soundscape

**Format:**

```
Man says in weary voice, "This must be it."
SFX: door creaking open slowly
Ambient: soft rain on windows, distant traffic, clock ticking
```

## Complete Prompt Examples

### Cinematic Product Shot

```
Wide establishing shot, slow dolly push-in.
A sleek matte black smartphone with edge-to-edge display sits on a
minimalist white marble pedestal.
The phone slowly rotates 45 degrees, catching the light.
In a pristine studio environment with soft gradient lighting from above.
Clean commercial aesthetic, high contrast, subtle reflections on the marble
surface.
```

### Documentary Nature

```
Medium shot, handheld tracking.
A red fox with thick winter coat, amber eyes alert, distinctive white
chest marking.
Trots purposefully through the underbrush, pausing to sniff the air.
In a snow-dusted Pacific Northwest forest at dawn, mist weaving between
Douglas firs.
National Geographic documentary quality, natural lighting, observational
distance maintained.
```

### Social Media Vertical

```
Close-up, static with subtle movement.
Young woman with curly auburn hair, freckles, genuine smile, wearing
oversized sage green sweater.
Looks up from phone and breaks into surprised laughter.
In a bright modern apartment, morning light, houseplants visible in
background.
Punchy social media style, warm tones, slightly overexposed highlights.
```

## Key Rules

### Front-load critical information

Early tokens are weighted more heavily. Put the most important elements first.

### One camera movement per shot

Multiple movements confuse the model. Choose one and commit.

### Descriptive phrasing over jargon

- **Good**: "camera slowly rises to reveal the city below"
- **Bad**: "crane up to WS"

### Optimal prompt length

100-150 words typically yields best results. Too short = hallucination. Too long
= conflicting instructions.

### Use negative prompts

Add `--negative-prompt` to specify what to avoid:

```
--negative-prompt "text, watermark, morphing, extra limbs, blur, distortion"
```

### Maximum tokens

The API accepts up to 1,024 tokens per prompt.

## Duration Planning

| Target Length | Strategy                         |
| ------------- | -------------------------------- |
| ≤8s           | Single generation                |
| 9-15s         | Generate 8s + 1 extension (7s)   |
| 16-22s        | Generate 8s + 2 extensions (14s) |
| 23-29s        | Generate 8s + 3 extensions (21s) |
| 30s+          | Multiple extension cycles        |

### Extension Prompts

When extending, describe what happens next, not what already happened:

**Initial prompt:**

```
Wide shot of a woman walking toward camera on a beach at sunset.
```

**Extension prompt:**

```
Continue the scene as she stops, turns to look at the ocean, and the sun
drops below the horizon casting golden light across the waves.
```

## Aspect Ratio Guidance

| Ratio | Use Case                         |
| ----- | -------------------------------- |
| 16:9  | YouTube, presentations, cinema   |
| 9:16  | TikTok, Instagram Reels, Stories |
| 1:1   | Instagram feed, profile videos   |

## Audio Tips

Audio generation has approximately 25% failure rate. Plan for:

- Post-production audio replacement
- Multiple generation attempts for critical audio
- Simpler audio requests (ambient vs complex dialogue)

## Preset Integration

Use presets to automatically apply style modifiers:

```bash
# Cinematic preset adds: "Cinematic film quality. [YOUR PROMPT].
# Professional cinematography, shallow depth of field, subtle film grain."
bun run Generate.ts --preset cinematic --prompt "A man walks through rain"
```

Available presets:

- `cinematic` - Film-quality 24fps with shallow DOF
- `vertical-social` - 9:16 punchy social media style
- `product-demo` - Clean studio presentation
- `documentary` - Nature documentary aesthetic

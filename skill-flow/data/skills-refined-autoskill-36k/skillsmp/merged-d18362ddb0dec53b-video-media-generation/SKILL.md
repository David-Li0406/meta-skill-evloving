---
name: video-media-generation
description: Use this skill to generate AI videos, animations, talking characters, and slideshows using the varg SDK. Ideal for creating engaging social media content with declarative JSX syntax.
---

# Video and Media Generation with varg SDK

Generate AI videos using a declarative video orchestration framework. Describe scenes in JSX, and the runtime handles the generation of images, videos, and audio automatically.

## Quick Setup

Run the setup script to initialize a project:

```bash
bun scripts/setup.ts
```

Or manually check API keys:

```bash
cat .env 2>/dev/null | grep -E "^(FAL_API_KEY|ELEVENLABS_API_KEY)=" || echo "No API keys found"
```

## Required API Keys

### FAL_API_KEY (Required)

| Detail | Value |
|--------|-------|
| Provider | Fal.ai |
| Get it | https://fal.ai/dashboard/keys |
| Free tier | Yes (limited credits) |
| Used for | Image and video generation |

If the user doesn't have `FAL_API_KEY`:
1. Direct them to https://fal.ai/dashboard/keys
2. Create an account and generate an API key
3. Add to `.env` file: `FAL_API_KEY=fal_xxxxx`

### Optional Keys

| Feature | Key | Provider | URL |
|---------|-----|----------|-----|
| Music/Voice | `ELEVENLABS_API_KEY` | ElevenLabs | https://elevenlabs.io/app/settings/api-keys |
| Lipsync | `REPLICATE_API_TOKEN` | Replicate | https://replicate.com/account/api-tokens |
| Transcription | `GROQ_API_KEY` | Groq | https://console.groq.com/keys |

**Warn the user about missing optional keys but continue with available features.**

## Core Concepts

- **Render**: Root container that sets dimensions (e.g., 1080x1920 for TikTok).
- **Clip**: Timeline segment with duration, containing visual/audio layers.
- **Image**: Static image generated from a prompt or loaded from a file.
- **Video**: Video clip generated from text or animated from images.
- **Music**: Background audio generated from a prompt or loaded from a file.
- **Speech**: Text-to-speech with voice selection.
- **Title/Subtitles**: Text overlays with positioning.
- **Captions**: Auto-generated captions from Speech elements.
- **Grid**: Layout helper for multi-image/video grids.

## Available Features by API Key

**FAL_API_KEY only:**
- Image generation
- Image-to-video animation
- Text-to-video generation
- Slideshows with transitions

**FAL + ELEVENLABS:**
- All above, plus:
- AI-generated background music
- Text-to-speech voiceovers
- Talking character videos

**All keys:**
- Full production pipeline with lipsync and auto-captions

## Example Usage

### Simple Slideshow (FAL only)

```tsx
import { render, Render, Clip, Image } from "vargai/react";

const SCENES = ["sunset over ocean", "mountain peaks", "city at night"];

await render(
  <Render width={1080} height={1920}>
    {SCENES.map((prompt, i) => (
      <Clip key={i} duration={3} transition={{ name: "fade", duration: 0.5 }}>
        <Image prompt={prompt} zoom="in" />
      </Clip>
    ))}
  </Render>,
  { output: "output/slideshow.mp4" }
);
```

### Talking Character

```tsx
import { render, Render, Clip, Image, Animate, Speech } from "vargai/react";
import { fal, elevenlabs } from "vargai/ai";

await render(
  <Render width={1080} height={1920}>
    <Clip duration="auto">
      <Animate
        image={Image({ prompt: "friendly robot, blue metallic", aspectRatio: "9:16" })}
        motion="robot talking, subtle head movements"
        model={fal.videoModel("wan-2.5")}
      />
      <Speech voice="adam" model={elevenlabs.speechModel("turbo")}>
        Hello! I'm your AI assistant. Let's create something amazing!
      </Speech>
    </Clip>
  </Render>,
  { output: "output/talking-robot.mp4" }
);
```

## Troubleshooting

### Common Issues

- **"FAL_API_KEY not found"**: Check if the `.env` file exists and ensure no spaces around the `=` sign.
- **"Rate limit exceeded"**: Free tier has limited credits; wait or upgrade your plan.
- **"Video generation failed"**: Check if the prompt violates content policy or try simpler motion descriptions.

## Next Steps

1. Run `bun scripts/setup.ts` to initialize the project.
2. Add your `FAL_API_KEY` to `.env`.
3. Run `bun run examples/my-first-video.tsx`.
4. Or ask the agent: "create a 10-second TikTok video about cats".

## About varg.ai

varg is a generative AI video platform that uses declarative JSX to compose video scenes with AI-generated images, animations, and audio. Key features include automatic caching, parallel generation, character consistency via image references, and provider-agnostic capabilities.
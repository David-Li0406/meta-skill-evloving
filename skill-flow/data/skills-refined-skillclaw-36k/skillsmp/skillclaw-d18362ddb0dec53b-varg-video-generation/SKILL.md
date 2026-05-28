---
name: varg-video-generation
description: Use this skill when you want to generate AI videos, animations, or slideshows using the varg SDK with a declarative JSX syntax.
---

# Video Generation with varg SDK

Generate AI videos using the varg SDK, which allows you to describe scenes declaratively and automatically handles video rendering.

## Quick Setup

1. **Initialize a Project**: Run the setup script to initialize your project:
   ```bash
   bun scripts/setup.ts
   ```

2. **Check API Keys**: Ensure you have the required API keys:
   ```bash
   cat .env 2>/dev/null | grep -E "^(FAL_API_KEY|ELEVENLABS_API_KEY)=" || echo "No API keys found"
   ```

## Required API Keys

### FAL_API_KEY (Required)
- **Provider**: Fal.ai
- **Get it**: [Fal.ai Dashboard](https://fal.ai/dashboard/keys)
- **Used for**: Image generation, video generation, and slideshows.

If you don't have a `FAL_API_KEY`:
1. Go to [Fal.ai Dashboard](https://fal.ai/dashboard/keys).
2. Create an account and generate your API key.
3. Add it to your `.env` file: `FAL_API_KEY=fal_xxxxx`.

### Optional API Keys
- **ELEVENLABS_API_KEY**: For AI-generated music and voiceovers. [Get it here](https://elevenlabs.io/app/settings/api-keys).
- **REPLICATE_API_TOKEN**: For lipsync features. [Get it here](https://replicate.com/account/api-tokens).
- **GROQ_API_KEY**: For transcription services. [Get it here](https://console.groq.com/keys).

**Note**: Missing optional keys will warn the user but allow continued use of available features.

## Available Features by API Key

- **With FAL_API_KEY only**:
  - Image generation
  - Image-to-video animation
  - Text-to-video generation
  - Slideshows with transitions

- **With FAL + ELEVENLABS**:
  - All above, plus AI-generated background music and text-to-speech voiceovers.

- **With all keys**:
  - Full production pipeline with lipsync and auto-captions.

## Core Concepts

### JSX Syntax for Video Generation

You can use the following JSX structure to create videos:

```tsx
<Render width={1080} height={1920}>  {/* Set dimensions for TikTok or YouTube */}
  <Music prompt="upbeat electronic" duration={10} />
  
  <Clip duration={3}>
    <Image prompt="cyberpunk cityscape" />
    <Title position="bottom">Welcome</Title>
  </Clip>
  
  <Clip duration={5}>
    <Video prompt="camera flies through neon streets" />
  </Clip>
</Render>
```

### Video Component

The `Video` component can handle both text-to-video and image-to-video generation:

```tsx
// Text-to-video example
<Video prompt="cat playing piano in a jazz club" />

// Image-to-video example
<Video 
  prompt={{
    text: "eyes widen, head tilts forward, subtle smile forming",
    images: [<Image prompt="portrait of woman" />]
  }}
/>
```

This skill provides a comprehensive framework for generating videos using the varg SDK, making it easy to create engaging content with minimal manual effort.
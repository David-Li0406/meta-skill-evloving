# Asset Producer & Model Selection Guide

This guide helps you select the right asset producer and model for your video generation workflow. Use this as your primary reference when building blueprints.

## Table of Contents

- [Producer Selection Decision Tree](#producer-selection-decision-tree)
- [Producer Quick Reference](#producer-quick-reference)
- [Model Selection by Category](#model-selection-by-category)

---

## Producer Selection Decision Tree

### Video Generation

Choose your producer based on your source material and consistency requirements:

```
Do you have reference images for subjects that must look consistent?
├── YES → Do subjects need to appear recognizable across multiple clips?
│         ├── YES → reference-to-video.yaml
│         │         Use cases:
│         │         • Consistent character appearance throughout video
│         │         • Product placement with specific product images
│         │         • Room/scene with recognizable furniture or objects
│         │         • Multiple characters that look the same across scenes
│         └── NO  → Do you have start/end images for frame continuity?
│                   ├── YES → image-to-video.yaml
│                   └── NO  → text-to-video.yaml
│
├── NO  → Do you have a start image (and optionally end image)?
│         ├── YES → image-to-video.yaml
│         │         Use cases:
│         │         • Continuous video from image sequence
│         │         • Staggered clips: end of clip N = start of clip N+1
│         │         • Frame interpolation between two images
│         │         • Animating a still image
│         └── NO  → text-to-video.yaml
│                   Use cases:
│                   • Full creative freedom for the model
│                   • Single scene from text description
│                   • No visual constraints needed
```

### Talking Head Video

```
Do you already have audio for the voice?
├── YES → audio-to-video.yaml
│         Use cases:
│         • Lip-sync existing voiceover to avatar
│         • Pre-recorded narration
│         • Voice cloned audio
│
└── NO  → text-to-talking-head.yaml
          Use cases:
          • Generate speech and video together
          • Text-to-speech integrated with avatar
```

### Image Generation

```
What is your starting point?
├── Text only → text-to-image.yaml
│               Use cases:
│               • Generate new images from descriptions
│               • No reference images needed
│
├── Existing image to edit → image-to-image.yaml
│                            Use cases:
│                            • Edit specific regions (with mask)
│                            • Transform/stylize existing image
│                            • Generate variations
│
└── Text + optional style reference → image-hybrid.yaml
                                      Use cases:
                                      • Text prompt with optional style guide
                                      • Flexible: works with or without references
                                      • Style transfer with text guidance
```

### Audio Generation

```
What type of audio do you need?
├── Voice/Speech → text-to-speech.yaml
│                  Use cases:
│                  • Narration, dialogue
│                  • Voice cloning (with reference audio)
│                  • Multiple languages
│
└── Music → text-to-music.yaml
            Use cases:
            • Background music
            • Songs with lyrics
            • Instrumental tracks
```

---

## Producer Quick Reference

### Video Producers

| Producer | ID | Best For | Key Inputs |
|----------|-----|----------|------------|
| **image-to-video.yaml** | `ImageToVideoProducer` | Animating images, frame interpolation, continuous clips | `StartImage`, `EndImage` (optional), `Prompt` |
| **text-to-video.yaml** | `TextToVideoProducer` | Creative freedom, text-only scenes | `Prompt`, `Duration` |
| **reference-to-video.yaml** | `ReferenceToVideoProducer` | Consistent subjects (characters, products, objects) | `ReferenceImages` or `ReferenceVideos`, `Prompt` |
| **audio-to-video.yaml** | `AudioToVideoProducer` | Lip-sync talking head from audio | `CharacterImage`, `AudioUrl` |
| **text-to-talking-head.yaml** | `TextToTalkingHeadProducer` | Talking head with TTS | `CharacterImage`, `NarrativeText`, `VoiceId` |

**Derived Artifacts:** All video producers also output `FirstFrame`, `LastFrame`, and `AudioTrack` artifacts that can be connected to downstream producers. See [Video Models Guide - Derived Video Artifacts](./video-models.md#derived-video-artifacts) for details.

### Image Producers

| Producer | ID | Best For | Key Inputs |
|----------|-----|----------|------------|
| **text-to-image.yaml** | `TextToImageProducer` | New images from text | `Prompt`, `AspectRatio` |
| **image-to-image.yaml** | `ImageToImageProducer` | Edit/transform existing images | `SourceImages`, `Prompt`, `MaskImage` (optional) |
| **image-hybrid.yaml** | `ImageHybridProducer` | Text + optional reference images | `Prompt`, `ReferenceImages` (optional) |

### Audio Producers

| Producer | ID | Best For | Key Inputs |
|----------|-----|----------|------------|
| **text-to-speech.yaml** | `TextToSpeechProducer` | Voice narration, dialogue | `Text`, `VoiceId` |
| **text-to-music.yaml** | `TextToMusicProducer` | Background music, songs | `Prompt`, `Lyrics` (optional), `Duration` |

---

## Model Selection by Category

For detailed model comparisons and capabilities, see these specialized guides:

- [Video Models Guide](./video-models.md) - Veo, Seedance, Kling, Hailuo, WAN, Sora comparisons
- [Image Models Guide](./image-models.md) - SeedDream, Flux Kontext, Qwen, Imagen comparisons
- [Audio Models Guide](./audio-models.md) - ElevenLabs, MiniMax Speech, Chatterbox, music models
- [Prompting Templates](./prompting-templates.md) - Use-case specific prompting patterns

---

## Key Decision Rules

### image-to-video vs reference-to-video

**Use `image-to-video.yaml` when:**
- You have a start image (and optionally end image)
- Creating continuous video from an image sequence
- Staggering clips: end image of clip N = start image of clip N+1
- Generating video interpolation between two frames

**Use `reference-to-video.yaml` when:**
- Maintaining consistent character appearance across multiple clips
- Product placement with specific product images
- Room/scene composition with selected item images
- Multiple characters that need to look consistent throughout
- Objects that must appear recognizable in every clip

### text-to-video vs image-to-video

**Use `text-to-video.yaml` when:**
- No reference images are needed
- Full creative freedom for the model
- Single scene generation from description

**Use `image-to-video.yaml` when:**
- Starting frame must match a specific visual
- Creating video continuation from a previous frame
- Ensuring visual consistency in multi-clip sequences

### audio-to-video vs text-to-talking-head

**Use `audio-to-video.yaml` when:**
- You already have audio (pre-recorded or generated separately)
- Using voice cloning with specific audio samples
- Separating TTS from video generation for more control

**Use `text-to-talking-head.yaml` when:**
- Generating speech and video in one step
- Simpler workflow with fewer producers
- Voice selection by ID rather than audio sample

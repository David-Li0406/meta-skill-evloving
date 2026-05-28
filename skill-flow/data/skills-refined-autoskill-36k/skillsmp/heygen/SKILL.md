---
name: heygen
description: Guide for adding AI presenter avatars to demos using HeyGen. Use when you want to make demos look like they were recorded by a human presenter (Loom-style).
---

# HeyGen Avatar Integration Guide

This skill covers adding AI presenter avatars to demo videos using HeyGen. Avatars make demos look like screen recordings with a human presenter.

## What is HeyGen?

HeyGen is an AI video generation platform that creates realistic talking avatar videos. For demo-creator, we use it to:
1. Generate avatar video segments that speak the narration
2. Overlay the avatar onto the demo recording
3. Create Loom-quality demos without recording yourself

## Presenter Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **Picture-in-Picture** | Small avatar bubble in corner | Most demos, non-intrusive |
| **Side-by-Side** | Presenter on left, demo on right | Tutorials, explanations |
| **Intro/Outro** | Full presenter for intro/outro only | Product launches |
| **Invisible** | No avatar, just voice | Quick demos, documentation |

## Configuration

### Avatar Config

```python
from utils.heygen_client import AvatarConfig

config = AvatarConfig(
    avatar_id="your_avatar_id",    # From HeyGen dashboard
    voice_id="optional_voice_id",  # Override avatar's voice
    style="picture-in-picture",    # pip, side-by-side, intro-outro
    position="bottom-right",       # For PiP: corner position
    size="small",                  # small, medium, large
    background="transparent",      # For overlay compositing
)
```

### Environment Setup

```bash
# Required
export HEYGEN_API_KEY="your_api_key"

# Optional - default avatar
export HEYGEN_AVATAR_ID="your_default_avatar"
```

Or in `~/.claude/demo-credentials.yaml`:

```yaml
heygen:
  api_key: "..."
  default_avatar_id: "..."
```

## Using the HeyGen Client

### Basic Generation

```python
from utils.heygen_client import HeyGenClient, AvatarConfig

client = HeyGenClient()

# Configure avatar
config = AvatarConfig(
    avatar_id="your_avatar",
    style="picture-in-picture",
    position="bottom-right",
    size="small",
)

# Generate avatar video
result = client.generate_and_download(
    text="Welcome to our product demo! Let me show you our new features.",
    config=config,
    output_path=Path(".demo/demo-id/avatar.mp4"),
)

if result.status == "success":
    print(f"Avatar video: {result.video_path}")
    print(f"Duration: {result.duration_seconds}s")
```

### Multiple Segments

For demos with multiple narration segments:

```python
from utils.heygen_client import generate_avatar_segments, AvatarSegment

segments = [
    AvatarSegment(
        text="Welcome to our demo.",
        start_time=0.0,
    ),
    AvatarSegment(
        text="Let me show you the search feature.",
        start_time=5.0,
    ),
    AvatarSegment(
        text="And that's our product in action!",
        start_time=15.0,
    ),
]

results = generate_avatar_segments(
    segments=segments,
    config=config,
    output_dir=Path(".demo/demo-id/avatars"),
)
```

### Compositing onto Demo

```python
from utils.heygen_client import composite_avatar_overlay

# Overlay avatar onto demo
composite_avatar_overlay(
    demo_video=Path(".demo/demo-id/demo_recording.mp4"),
    avatar_video=Path(".demo/demo-id/avatar.mp4"),
    output_path=Path(".demo/demo-id/final_with_avatar.mp4"),
    config=config,  # For position/size
)
```

## API Reference

### List Available Avatars

```python
client = HeyGenClient()
avatars = client.list_avatars()

for avatar in avatars:
    print(f"{avatar['id']}: {avatar['name']}")
```

### List Available Voices

```python
voices = client.list_voices()

for voice in voices:
    print(f"{voice['id']}: {voice['name']} ({voice['language']})")
```

### Check Video Status

```python
# Start generation
video_id = client.generate_avatar_video(text, config)

# Poll for completion
status = client.get_video_status(video_id)
print(f"Status: {status['status']}")  # processing, completed, failed

# Or wait for completion
final_status = client.wait_for_video(
    video_id,
    poll_interval=10,   # seconds between checks
    max_wait=600,       # max wait time
)
```

## Best Practices

### 1. Keep Segments Short

HeyGen works best with segments under 60 seconds:

```python
# Good: Short segments
segments = [
    AvatarSegment(text="Welcome!", start_time=0),
    AvatarSegment(text="Let's explore.", start_time=3),
]

# Avoid: Single long segment
segment = AvatarSegment(
    text="Very long narration that goes on and on...",  # Bad
    start_time=0,
)
```

### 2. Use Transparent Background

For clean overlays:

```python
config = AvatarConfig(
    avatar_id="...",
    background="transparent",  # Key for compositing
)
```

### 3. Match Voice to Narration

If using pre-generated ElevenLabs audio:

```python
# Option 1: Use HeyGen's TTS
config = AvatarConfig(
    avatar_id="...",
    voice_id="heygen_voice_id",
)

# Option 2: Provide audio file (lip-sync)
segment = AvatarSegment(
    text="Narration text",
    audio_path=Path("elevenlabs_audio.mp3"),
)
```

### 4. Position for Content

Choose position based on demo content:

```python
# Bottom-right: Most demos (default)
config = AvatarConfig(position="bottom-right")

# Top-left: If action is at bottom
config = AvatarConfig(position="top-left")

# Side-by-side: For tutorials
config = AvatarConfig(style="side-by-side")
```

### 5. Size Appropriately

```python
# Small: Non-intrusive, most demos
config = AvatarConfig(size="small")

# Medium: Tutorials, explanations
config = AvatarConfig(size="medium")

# Large: Intros, outros
config = AvatarConfig(size="large")
```

## Error Handling

### API Errors

```python
from utils.heygen_client import HeyGenClient

try:
    client = HeyGenClient()
    result = client.generate_and_download(text, config, output_path)
except ValueError as e:
    print(f"Configuration error: {e}")
except TimeoutError as e:
    print(f"Generation timed out: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Check Availability

```python
from utils.heygen_client import check_heygen_available

if check_heygen_available():
    print("HeyGen is configured")
else:
    print("Set HEYGEN_API_KEY to enable avatars")
```

## Demo Pipeline Integration

In the demo-creator pipeline, HeyGen is used in Stage 7.5:

```
Stage 7: Audio Generation (ElevenLabs)
  ↓
Stage 7.5: Avatar Generation (HeyGen) [Optional]
  - Generate avatar for each narration segment
  - Match timing to audio
  ↓
Stage 8: Video Compositing
  - Overlay avatar onto demo recording
  - Merge all audio/video tracks
```

### Enable/Disable in Config

In `.demo/config.yaml`:

```yaml
avatar:
  enabled: true           # Set to false to skip avatar
  style: picture-in-picture
  position: bottom-right
  size: small
```

## Pricing Considerations

HeyGen charges per video-minute generated. To minimize costs:

1. **Cache avatar segments**: Reuse for unchanged narration
2. **Use short segments**: Only generate what you need
3. **Preview first**: Review narration before avatar generation
4. **Batch generation**: Generate all segments at once

## Troubleshooting

### "API key required" Error

```bash
# Set environment variable
export HEYGEN_API_KEY="your_key"

# Or add to credentials file
echo "heygen:
  api_key: your_key" >> ~/.claude/demo-credentials.yaml
```

### Generation Taking Too Long

- HeyGen can take 1-5 minutes per video
- Use `wait_for_video()` with appropriate timeout
- Check HeyGen dashboard for queue status

### Avatar Not Syncing with Audio

- Ensure audio duration matches text
- Use HeyGen's built-in TTS for best sync
- If using external audio, verify format (MP3/WAV)

### Overlay Not Transparent

- Verify `background="transparent"` in config
- Check moviepy/ffmpeg version compatibility
- Use PNG/WebM intermediate formats

---

**When to use this skill:**
- Adding AI presenter to demos
- Creating Loom-style product videos
- Professional demo presentations
- Marketing and sales materials

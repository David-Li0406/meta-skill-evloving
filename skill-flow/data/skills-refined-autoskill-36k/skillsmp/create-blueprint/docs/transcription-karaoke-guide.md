# Transcription and Karaoke Subtitles Guide

This guide explains how to add speech transcription and karaoke-style subtitles to your video workflows. Karaoke subtitles display the spoken text with word-level highlighting synchronized to the audio, creating engaging effects similar to those seen on Instagram and TikTok.

## Table of Contents

- [Overview](#overview)
- [TranscriptionProducer](#transcriptionproducer)
- [VideoExporter Integration](#videoexporter-integration)
- [Blueprint Wiring](#blueprint-wiring)
- [Karaoke Configuration Options](#karaoke-configuration-options)
- [Complete Example](#complete-example)
- [Best Practices](#best-practices)

---

## Overview

The transcription system consists of two main components:

1. **TranscriptionProducer**: Converts audio segments to word-level transcripts with precise timestamps
2. **VideoExporter**: Renders the transcript as animated karaoke subtitles on the final video

### How It Works

```
AudioProducer[segment].GeneratedAudio
         │
         ├────────────────────────────┐
         │                            │
         ▼                            ▼
TimelineComposer.AudioSegments   TranscriptionProducer.AudioSegments
         │                            │
         ▼                            ▼
TimelineComposer.Timeline ─────► TranscriptionProducer.Timeline
                                      │
                                      ▼
                          TranscriptionProducer.Transcription
                                      │
                                      ▼
                          VideoExporter.Transcription
                                      │
                                      ▼
                          FinalVideo (with karaoke subtitles)
```

---

## TranscriptionProducer

The TranscriptionProducer converts speech audio into word-level transcriptions aligned to the video timeline.

### Producer Definition

**Location:** `catalog/producers/asset/transcription.yaml`

```yaml
meta:
  name: Speech Transcription
  description: Transcribe audio from timeline with word-level timestamps for karaoke subtitles.
  id: TranscriptionProducer
  version: 0.1.0

inputs:
  - name: Timeline
    description: Timeline document with audio clip timing information.
    type: json
  - name: AudioSegments
    description: Audio clips to transcribe (from Audio track and Video AudioTracks).
    type: collection
    itemType: audio
    dimensions: segment
    fanIn: true
  - name: LanguageCode
    description: ISO 639-3 language code for transcription (e.g., eng, spa, fra).
    type: string

artifacts:
  - name: Transcription
    description: Word-level transcription aligned to video timeline.
    type: json
```

### Supported Models

| Model | Provider | Description |
|-------|----------|-------------|
| `speech/transcription` | renku | Internal handler for transcription with karaoke subtitle support. Configure the actual STT backend via `config.sttProvider` and `config.sttModel`. |

**Configuration:**
```yaml
- model: speech/transcription
  provider: renku
  producerId: TranscriptionProducer
  config:
    sttProvider: fal-ai                    # Provider for STT API
    sttModel: elevenlabs/speech-to-text    # Model for STT API
    languageCode: eng                      # Optional: language code
```

### Transcription Output Structure

The TranscriptionProducer outputs a JSON structure with word-level timestamps:

```json
{
  "text": "Hello world this is a test",
  "words": [
    { "text": "Hello", "startTime": 0.0, "endTime": 0.5, "clipId": "clip-1" },
    { "text": "world", "startTime": 0.5, "endTime": 1.0, "clipId": "clip-1" },
    { "text": "this", "startTime": 1.0, "endTime": 1.3, "clipId": "clip-1" },
    { "text": "is", "startTime": 1.3, "endTime": 1.5, "clipId": "clip-1" },
    { "text": "a", "startTime": 1.5, "endTime": 1.7, "clipId": "clip-1" },
    { "text": "test", "startTime": 1.7, "endTime": 2.0, "clipId": "clip-1" }
  ],
  "segments": [
    {
      "clipId": "clip-1",
      "clipStartTime": 0,
      "clipDuration": 10,
      "text": "Hello world this is a test"
    }
  ],
  "language": "eng",
  "totalDuration": 10
}
```

---

## VideoExporter Integration

The VideoExporter accepts an optional Transcription input to render karaoke subtitles.

### Producer Definition

**Location:** `catalog/producers/composition/video-exporter.yaml`

```yaml
meta:
  name: Video Exporter
  description: Render the composed timeline into a final MP4.
  id: VideoExporter
  version: 0.1.0

inputs:
  - name: Timeline
    description: OrderedTimeline JSON manifest to render.
    type: json
  - name: Transcription
    description: Optional word-level transcription for karaoke subtitles.
    type: json
    required: false

artifacts:
  - name: FinalVideo
    description: Final rendered MP4 video.
    type: video
```

**Key Point:** The `Transcription` input is optional (`required: false`). If not provided, the video exports without subtitles.

---

## Blueprint Wiring

### Adding TranscriptionProducer to Your Blueprint

#### 1. Add the Producer

```yaml
producers:
  # ... existing producers ...
  - name: TranscriptionProducer
    producer: asset/transcription
  - name: VideoExporter
    producer: composition/video-exporter
```

#### 2. Wire the Connections

```yaml
connections:
  # ... existing connections ...

  # Wire timeline to transcription producer
  - from: TimelineComposer.Timeline
    to: TranscriptionProducer.Timeline

  # Wire audio segments to transcription producer
  - from: AudioProducer[segment].GeneratedAudio
    to: TranscriptionProducer.AudioSegments

  # Wire transcription to exporter
  - from: TranscriptionProducer.Transcription
    to: VideoExporter.Transcription

  # Wire timeline to exporter (required)
  - from: TimelineComposer.Timeline
    to: VideoExporter.Timeline

  # Wire final video output
  - from: VideoExporter.FinalVideo
    to: FinalVideo
```

#### 3. Add the Collector for AudioSegments

**CRITICAL:** Fan-in inputs require BOTH a connection AND a collector:

```yaml
collectors:
  # ... existing collectors ...

  # Collect audio segments for transcription
  - name: TranscriptionAudio
    from: AudioProducer[segment].GeneratedAudio
    into: TranscriptionProducer.AudioSegments
    groupBy: segment
```

### Dependency Order

The transcription system enforces this execution order:

1. **AudioProducer** generates audio segments
2. **TimelineComposer** creates the timeline (uses audio for timing)
3. **TranscriptionProducer** transcribes audio using timeline for alignment
4. **VideoExporter** renders final video with karaoke subtitles

---

## Karaoke Configuration Options

Configure karaoke subtitle appearance through an export configuration file when running `renku export`.

### Export Configuration File

Create a YAML file (e.g., `export-config.yaml`) with subtitle settings:

```yaml
# Video settings
width: 1920
height: 1080
fps: 30
exporter: ffmpeg

# FFmpeg encoding settings
preset: medium
crf: 23
audioBitrate: 192k

# Karaoke subtitle settings
subtitles:
  font: Arial                    # Font name (system fonts)
  fontSize: 48                   # Font size in pixels (default: 48)
  fontBaseColor: "#FFFFFF"       # Default text color in hex (default: white)
  fontHighlightColor: "#FFD700"  # Highlighted word color in hex (default: gold)
  backgroundColor: "#000000"     # Background box color in hex (default: black)
  backgroundOpacity: 0.5         # Background opacity 0-1 (default: 0, no box)
  bottomMarginPercent: 10        # Position from bottom (default: 10%)
  maxWordsPerLine: 4             # Words per line (default: 4)
  highlightEffect: true          # Enable karaoke highlighting (default: true)
```

Then export with:

```bash
renku export --last --inputs=./export-config.yaml
```

### Configuration Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `font` | string | Arial | Font name (uses system fonts) |
| `fontSize` | number | 48 | Font size in pixels |
| `fontBaseColor` | string | #FFFFFF | Default text color (hex format) |
| `fontHighlightColor` | string | #FFD700 | Color for the currently spoken word (hex) |
| `backgroundColor` | string | #000000 | Background box color (hex format) |
| `backgroundOpacity` | number | 0 | Background opacity (0-1, 0 = no box) |
| `bottomMarginPercent` | number | 10 | Position from bottom as percentage of height |
| `maxWordsPerLine` | number | 4 | Maximum words to display at once |
| `highlightEffect` | boolean | true | Enable karaoke-style word highlighting |

### Color Format

Colors must be specified in hex format:
- `#FFFFFF` - white
- `#000000` - black
- `#FFD700` - gold
- `#FF5733` - orange-red

---

## Highlight Effect

The karaoke renderer highlights the currently spoken word by changing its color. This creates an engaging visual effect similar to those seen on Instagram and TikTok.

### Enabling/Disabling Highlights

The `highlightEffect` option controls whether word highlighting is enabled:

```yaml
subtitles:
  highlightEffect: true   # Enable karaoke-style highlighting (default)
  # highlightEffect: false  # Disable to show static subtitles
```

When enabled:
- Words change from `fontBaseColor` to `fontHighlightColor` as they're spoken
- Each word is highlighted based on its timestamp from the transcription
- Creates a reading-along effect synchronized with the audio

When disabled:
- All words display in `fontBaseColor`
- Subtitles appear as standard static captions

---

## Complete Example

Here's a complete blueprint with transcription and karaoke subtitles:

### Blueprint: `video-audio-music-karaoke.yaml`

```yaml
meta:
  name: Video with Karaoke Subtitles
  description: Generate narrated videos with animated karaoke subtitles.
  id: VideoAudioMusicKaraoke
  version: 0.1.0

inputs:
  - name: InquiryPrompt
    description: The prompt describing the movie script.
    type: string
    required: true
  - name: Style
    description: Visual style for the video.
    type: string
    required: true
  - name: VoiceId
    description: Voice identifier for narration.
    type: string
    required: true

artifacts:
  - name: FinalVideo
    description: Final rendered MP4 with karaoke subtitles.
    type: video

loops:
  - name: segment
    countInput: NumOfSegments

producers:
  - name: ScriptProducer
    producer: prompt/script
  - name: VideoProducer
    producer: asset/text-to-video
    loop: segment
  - name: AudioProducer
    producer: asset/text-to-speech
    loop: segment
  - name: MusicProducer
    producer: asset/text-to-music
  - name: TimelineComposer
    producer: composition/timeline-composer
  - name: TranscriptionProducer
    producer: asset/transcription
  - name: VideoExporter
    producer: composition/video-exporter

connections:
  # Script generation
  - from: InquiryPrompt
    to: ScriptProducer.InquiryPrompt
  - from: Duration
    to: ScriptProducer.Duration
  - from: NumOfSegments
    to: ScriptProducer.NumOfSegments

  # Video generation
  - from: ScriptProducer.NarrationScript[segment]
    to: VideoProducer[segment].Prompt
  - from: Style
    to: VideoProducer[segment].Style
  - from: VideoProducer[segment].GeneratedVideo
    to: TimelineComposer.VideoSegments

  # Audio generation
  - from: ScriptProducer.NarrationScript[segment]
    to: AudioProducer[segment].Text
  - from: VoiceId
    to: AudioProducer[segment].VoiceId
  - from: AudioProducer[segment].GeneratedAudio
    to: TimelineComposer.AudioSegments

  # Music generation
  - from: Duration
    to: MusicProducer.Duration
  - from: MusicProducer.GeneratedMusic
    to: TimelineComposer.Music

  # Timeline composition
  - from: Duration
    to: TimelineComposer.Duration

  # Transcription
  - from: TimelineComposer.Timeline
    to: TranscriptionProducer.Timeline
  - from: AudioProducer[segment].GeneratedAudio
    to: TranscriptionProducer.AudioSegments

  # Video export with karaoke
  - from: TimelineComposer.Timeline
    to: VideoExporter.Timeline
  - from: TranscriptionProducer.Transcription
    to: VideoExporter.Transcription
  - from: VideoExporter.FinalVideo
    to: FinalVideo

collectors:
  - name: TimelineVideo
    from: VideoProducer[segment].GeneratedVideo
    into: TimelineComposer.VideoSegments
    groupBy: segment
  - name: TimelineAudio
    from: AudioProducer[segment].GeneratedAudio
    into: TimelineComposer.AudioSegments
    groupBy: segment
  - name: TranscriptionAudio
    from: AudioProducer[segment].GeneratedAudio
    into: TranscriptionProducer.AudioSegments
    groupBy: segment
```

### Input Template: `karaoke-inputs.yaml`

```yaml
inputs:
  InquiryPrompt: "The history of space exploration"
  Style: "Documentary"
  VoiceId: "narrator_male_1"
  Duration: 60
  NumOfSegments: 6

models:
  - model: gpt-5-mini
    provider: openai
    producerId: ScriptProducer
    config:
      text_format: json_schema

  - model: bytedance/seedance-1-pro-fast
    provider: replicate
    producerId: VideoProducer

  - model: minimax/speech-2.6-hd
    provider: replicate
    producerId: AudioProducer

  - model: minimax/music-1.5
    provider: replicate
    producerId: MusicProducer

  - model: timeline/ordered
    provider: renku
    producerId: TimelineComposer
    config:
      tracks: ["Video", "Audio", "Music"]
      masterTracks: ["Audio"]

  - model: speech/transcription
    provider: renku
    producerId: TranscriptionProducer
    config:
      sttProvider: fal-ai
      sttModel: elevenlabs/speech-to-text
```

### Export Configuration: `export-config.yaml`

Create a separate export configuration file for subtitle settings:

```yaml
exporter: ffmpeg
width: 1920
height: 1080
fps: 30
preset: medium
crf: 23

subtitles:
  font: Arial
  fontSize: 52
  fontBaseColor: "#FFFFFF"
  fontHighlightColor: "#FF6B35"
  backgroundColor: "#000000"
  backgroundOpacity: 0.6
  maxWordsPerLine: 6
  highlightEffect: true
```

### Running the Workflow

```bash
# Generate the video with transcription
renku generate --inputs=./karaoke-inputs.yaml --blueprint=./video-audio-music-karaoke.yaml

# Export with karaoke subtitles
renku export --last --inputs=./export-config.yaml
```

---

## Best Practices

### 1. Track Types Matter

- **Audio track** (`kind: Audio`): Always transcribed - contains speech/narration
- **Music track** (`kind: Music`): Never transcribed - background music only
- **Video track** with audio: Audio track extracted and transcribed

### 2. Language Configuration

Specify the correct language code for better transcription accuracy:

```yaml
inputs:
  LanguageCode: eng  # ISO 639-3 code
```

Common language codes:
- `eng` - English
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `jpn` - Japanese
- `zho` - Chinese

### 3. Font Selection

The `font` option uses system fonts by name:
- Use font names installed on your system (e.g., "Arial", "Helvetica", "Times New Roman")
- Ensure the font supports your language's characters
- Test with your target text before full generation
- Common cross-platform fonts: Arial, Helvetica, Verdana, Georgia

### 4. Words Per Line

Adjust `maxWordsPerLine` based on:
- Video resolution (fewer words for mobile/vertical video)
- Average word length in your language
- Font size (smaller fonts can fit more words)

Recommendations:
- 16:9 desktop video: 6-8 words
- 9:16 mobile/TikTok: 3-4 words
- 1:1 square video: 4-6 words

### 5. Background Opacity Settings

| Content Type | Recommended Opacity |
|--------------|---------------------|
| Light/bright video backgrounds | 0.6-0.8 |
| Dark video backgrounds | 0.3-0.5 |
| Mixed/varied backgrounds | 0.5 |
| No background (text only) | 0 |

### 6. Performance Considerations

- Transcription adds processing time proportional to audio duration
- More words per line = fewer subtitle events = slightly faster rendering
- Subtitle rendering has minimal impact on overall export time

---

## Troubleshooting

### No Subtitles Appearing

1. Verify the Transcription connection to VideoExporter exists in the blueprint
2. Check that TranscriptionProducer has the correct Timeline input
3. Ensure AudioSegments collector is defined
4. Verify you're using `--exporter=ffmpeg` (Remotion exporter doesn't support subtitles)
5. Check that the export config file has `subtitles` section

### Subtitles Out of Sync

1. Verify Timeline is connected to TranscriptionProducer
2. Check that audio segments use the same timeline as video
3. Ensure segment startTime values are correct in timeline

### Garbled or Wrong Text

1. Verify correct LanguageCode is set in TranscriptionProducer config
2. Check audio quality - clear speech transcribes better
3. Ensure audio doesn't overlap between segments

### Highlighting Not Working

1. Verify `highlightEffect: true` in export config subtitles section
2. Check that `fontHighlightColor` is different from `fontBaseColor`
3. Ensure transcription has word-level timestamps (check Transcription artifact)

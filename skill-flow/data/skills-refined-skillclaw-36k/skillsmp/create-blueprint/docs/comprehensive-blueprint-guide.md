# Renku Blueprint Authoring Guide

This comprehensive guide explains how to author Renku blueprints: the YAML schema, how producers compose into workflows, and the rules the planner and runner enforce (canonical IDs, loops, collectors, fan-in).

---

## Table of Contents

1. [Introduction & Overview](#introduction--overview)
2. [Core Concepts](#core-concepts)
3. [Blueprint YAML Reference](#blueprint-yaml-reference)
4. [Producer YAML Reference](#producer-yaml-reference)
5. [Connections](#connections)
6. [Conditional Connections](#conditional-connections)
7. [Loops and Dimensions](#loops-and-dimensions)
8. [Collectors and Fan-In](#collectors-and-fan-in)
9. [Canonical IDs](#canonical-ids)
10. [Planner and Runner Internals](#planner-and-runner-internals)
11. [Input Files Reference](#input-files-reference)
12. [Validation Rules & Error Messages](#validation-rules--error-messages)
13. [Common Patterns](#common-patterns)
14. [Debugging and Testing](#debugging-and-testing)
15. [Directory Structure & File Naming](#directory-structure--file-naming)

---

## Introduction & Overview

### What is Renku?

Renku is a workflow orchestration system for generating long-form video content using AI. It coordinates multiple AI providers (OpenAI, Replicate, fal.ai, etc.) to produce narrated documentaries, educational videos, and other multimedia content from simple text prompts.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Blueprint YAML                             │
│  (Defines workflow: inputs, producers, connections, collectors)      │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              Planner                                 │
│  • Loads blueprint tree (blueprints + producers)                    │
│  • Resolves dimensions and expands loops                            │
│  • Builds execution graph with canonical IDs                        │
│  • Creates layered execution plan                                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              Runner                                  │
│  • Executes jobs layer by layer                                     │
│  • Resolves inputs from upstream artifacts                          │
│  • Materializes fan-in collections                                  │
│  • Invokes AI providers via producer implementations                │
│  • Stores artifacts and logs events                                 │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            Providers                                 │
│  • OpenAI (text generation, structured output)                      │
│  • Replicate (video, audio, image models)                          │
│  • fal.ai (video, audio, image models)                             │
│  • Renku (timeline composition, video export)                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Typical Video Generation Workflow

1. **Script Generation**: LLM generates narration script divided into segments
2. **Prompt Generation**: LLM creates prompts for video/image generation per segment
3. **Media Generation**: AI models generate video clips, images, or audio per segment
4. **Timeline Composition**: Renku assembles segments into a playable timeline
5. **Video Export**: Remotion renders the final video file

---

## Core Concepts

### Vocabulary

| Term | Definition |
|------|------------|
| **Blueprint** | Top-level YAML that orchestrates a complete workflow. Defines inputs, artifacts, loops, producer imports, connections, and collectors. |
| **Producer** | A reusable module that invokes one or more AI models. Producers are referenced by blueprints via the `producers:` section. |
| **Input** | A user-provided value. Mark `required: true` unless a sensible `default` exists. For producers, required and defaults are read from the input JSON schemas. |
| **Artifact** | An output produced by a producer. Can be scalar (single value) or array (indexed by loops). |
| **Loop** | A named iteration dimension that defines how many times a producer executes. Loops enable parallel processing of segments. |
| **Connection** | A data flow edge that wires outputs to inputs across the workflow graph. |
| **Collector** | Gathers multiple artifacts into a single collection for downstream aggregation (fan-in). |
| **Canonical ID** | Fully qualified node identifier used throughout the system. Format: `Type:path.to.name[index]` |
| **System Input** | A well-known input that is automatically recognized by name without YAML declaration. Includes `Duration`, `NumOfSegments`, `SegmentDuration`, `MovieId`, `StorageRoot`, `StorageBasePath`. |

### System Inputs

System inputs are special inputs that Renku automatically recognizes by name. **You do not need to declare these in your blueprint's `inputs:` section** - they are automatically available when referenced in connections. You only need to provide their values in the input YAML file.

#### Available System Inputs

| System Input | Type | Description |
|--------------|------|-------------|
| `Duration` | `int` | Total duration of the movie in seconds. Provided in input YAML. |
| `NumOfSegments` | `int` | Number of segments to generate. Provided in input YAML. |
| `SegmentDuration` | `int` | Duration of each segment. **Auto-computed** as `Duration / NumOfSegments`. |
| `MovieId` | `string` | Unique identifier for the movie. Auto-injected by the system. |
| `StorageRoot` | `string` | Root directory for storage. Auto-injected from CLI config. |
| `StorageBasePath` | `string` | Base path within storage root. Auto-injected from CLI config. |

#### How System Inputs Work

1. **No declaration needed**: System inputs are automatically injected when referenced in blueprint edges
2. **Provide in input YAML**: User-provided system inputs (`Duration`, `NumOfSegments`) are specified in the input template file
3. **Auto-computed values**: `SegmentDuration` is automatically calculated as `Duration / NumOfSegments`
4. **User overrides**: If you explicitly provide `SegmentDuration` in your input YAML, it won't be auto-computed

#### Example: Using System Inputs

**Blueprint (no need to declare Duration, NumOfSegments, SegmentDuration):**
```yaml
inputs:
  - name: InquiryPrompt
    type: string
    required: true
  - name: Style
    type: string
    required: true
  # Duration, NumOfSegments, SegmentDuration are system inputs - no declaration needed!

loops:
  - name: segment
    countInput: NumOfSegments  # References system input

connections:
  # System inputs can be used directly in connections
  - from: Duration
    to: ScriptProducer.Duration
  - from: NumOfSegments
    to: ScriptProducer.NumOfSegments
  - from: SegmentDuration
    to: VideoProducer[segment].Duration  # Auto-computed value
```

**Input YAML:**
```yaml
inputs:
  InquiryPrompt: "The history of space exploration"
  Style: "Documentary"
  Duration: 60        # System input - provided by user
  NumOfSegments: 6    # System input - provided by user
  # SegmentDuration is auto-computed as 60/6 = 10 seconds
```

#### Benefits of System Inputs

- **Less boilerplate**: No need to declare common inputs in every blueprint
- **Automatic computation**: `SegmentDuration` is computed automatically
- **Consistent naming**: Standardized names across all blueprints
- **Provider access**: Timeline composers and video exporters automatically receive `MovieId`, `StorageRoot`, `StorageBasePath`

### Blueprint vs Producer

**Blueprints** are workflow definitions that:
- Define user-facing inputs and final artifacts
- Import and connect multiple producers
- Define loops for parallel execution
- Specify collectors for fan-in aggregation

**Producers** are execution units that:
- Accept inputs and produce artifacts
- Map inputs to specific AI model parameters
- Support multiple model variants (e.g., different video providers)
- Can be reused across multiple blueprints

### Data Flow

Data flows through the system via **connections**:

```
Blueprint Input ──► Producer Input ──► Producer ──► Artifact ──► Next Producer Input
                                                          │
                                                          └──► Blueprint Artifact
```

For looped producers, data flows through indexed connections:

```
ScriptProducer.NarrationScript[0] ──► AudioProducer[0].TextInput
ScriptProducer.NarrationScript[1] ──► AudioProducer[1].TextInput
ScriptProducer.NarrationScript[2] ──► AudioProducer[2].TextInput
```

---

## Blueprint YAML Reference

### Complete Schema

```yaml
meta:
  name: <string>           # Human-readable name (required)
  description: <string>    # Purpose and behavior
  id: <string>             # Unique identifier in PascalCase (required)
  version: <semver>        # Semantic version (e.g., 0.1.0)
  author: <string>         # Creator name
  license: <string>        # License type (e.g., MIT)

inputs:
  - name: <string>         # Input identifier in PascalCase (required)
    description: <string>  # Purpose and usage
    type: <string>         # Data type (required)
    required: <boolean>    # Whether mandatory (default: true)

artifacts:
  - name: <string>         # Artifact identifier in PascalCase (required)
    description: <string>  # Purpose and content
    type: <string>         # Output type (required)
    itemType: <string>     # Element type for arrays
    countInput: <string>   # Input that determines array size
    countInputOffset: <int> # Offset added to countInput value

loops:
  - name: <string>         # Loop identifier in lowercase (required)
    description: <string>  # Purpose and behavior
    countInput: <string>   # Input that determines iteration count (required)
    countInputOffset: <int> # Offset added to count
    parent: <string>       # Parent loop for nesting

producers:
  - name: <string>         # Producer instance name in PascalCase (required)
    producer: <string>     # Qualified name: "category/name" (preferred)
    path: <string>         # Relative path to producer YAML (legacy, for custom producers)
    loop: <string>         # Loop dimension(s) (e.g., "segment" or "segment.image")

connections:
  - from: <string>         # Source reference (required)
    to: <string>           # Target reference (required)
    if: <string>           # Condition name for conditional execution
    note: <string>         # Optional documentation

conditions:
  <conditionName>:
    when: <string>         # Path to artifact field (e.g., Producer.Artifact.Field[dim])
    is: <any>              # Equals this value
    isNot: <any>           # Does not equal this value
    contains: <string>     # String contains value
    greaterThan: <number>  # Greater than
    lessThan: <number>     # Less than
    exists: <boolean>      # Field exists and is truthy
    matches: <string>      # Regex pattern
    all: <array>           # AND: all sub-conditions must pass
    any: <array>           # OR: at least one sub-condition must pass

collectors:
  - name: <string>         # Collector identifier (required)
    from: <string>         # Source artifact reference (required)
    into: <string>         # Target input reference (required)
    groupBy: <string>      # Loop dimension for grouping (required)
    orderBy: <string>      # Loop dimension for ordering within groups
```

### Field Details

#### `inputs`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Identifier in PascalCase |
| `type` | string | Yes | `string`, `int`, `image`, `audio`, `video`, `json`, `collection` |
| `required` | boolean | No | Default: `true` |
| `description` | string | No | Documentation |

**Types:**
- `string`: Text value
- `int`: Integer number
- `image`, `audio`, `video`: Media file reference
- `json`: Structured JSON data
- `collection`: Array of items (used with `fanIn: true` in producers)

#### `artifacts`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Identifier in PascalCase |
| `type` | string | Yes | `string`, `json`, `image`, `audio`, `video`, `array`, `multiDimArray` |
| `itemType` | string | Conditional | Required for `array` and `multiDimArray` |
| `countInput` | string | Conditional | Input name for array sizing |
| `countInputOffset` | int | No | Non-negative offset added to size |

**Array sizing:** The final size is `countInput + countInputOffset`.

#### `loops`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Lowercase identifier (e.g., `segment`) |
| `countInput` | string | Yes | Input that provides iteration count |
| `countInputOffset` | int | No | Offset added to count |
| `parent` | string | No | Parent loop for nesting |

#### `producers`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Instance alias in PascalCase |
| `producer` | string | Conditional | Qualified name `category/name` - resolves from catalog |
| `path` | string | Conditional | Relative path to producer YAML - for custom/local producers |
| `loop` | string | No | Loop assignment (e.g., `segment`, `segment.image`) |

**Note:** Either `producer` or `path` must be provided. Use `producer` for catalog producers (preferred), `path` for custom local producers.

**Producer Resolution:** When `producer: "category/name"` is specified:
1. Tries: `{catalogRoot}/producers/{category}/{name}.yaml`
2. Tries: `{catalogRoot}/producers/{category}/{name}/{name}.yaml`
3. Error if not found

### Real Example: Video-Only Blueprint

```yaml
meta:
  name: Video Only Narration
  description: Generate video segments from a textual inquiry.
  id: Video
  version: 0.1.0
  author: Renku
  license: MIT

inputs:
  # Note: Duration, NumOfSegments, SegmentDuration are system inputs
  # They don't need to be declared here - just provide values in input YAML
  - name: InquiryPrompt
    description: The prompt describing the movie script to be generated.
    type: string
    required: true
  - name: Style
    description: Desired movie style to feed into prompt.
    type: string
    required: true
  - name: Resolution
    description: The video resolution in 480p, 720p, 1080p
    type: string
    required: true
  - name: AspectRatio
    description: Aspect ratio such as 16:9 or 3:2.
    type: string
    required: true

artifacts:
  - name: SegmentVideo
    description: Generated video for each narration segment.
    type: array
    itemType: video
    countInput: NumOfSegments  # References system input

loops:
  - name: segment
    description: Iterates over narration segments.
    countInput: NumOfSegments  # References system input

producers:
  - name: ScriptProducer
    producer: prompt/script
  - name: VideoPromptProducer
    producer: prompt/video
  - name: VideoProducer
    producer: asset/text-to-video
    loop: segment

connections:
  # Wire blueprint inputs to ScriptProducer
  - from: InquiryPrompt
    to: ScriptProducer.InquiryPrompt
  - from: Duration
    to: ScriptProducer.Duration          # System input - no declaration needed
  - from: NumOfSegments
    to: ScriptProducer.NumOfSegments     # System input - no declaration needed

  # Wire script outputs to VideoPromptProducer (looped)
  - from: ScriptProducer.NarrationScript[segment]
    to: VideoPromptProducer[segment].NarrativeText
  - from: ScriptProducer.MovieSummary
    to: VideoPromptProducer[segment].MovieSummary
  - from: Style
    to: VideoPromptProducer[segment].Style
  - from: SegmentDuration
    to: VideoPromptProducer[segment].SegmentDuration  # Auto-computed system input

  # Wire prompts to VideoProducer (looped)
  - from: VideoPromptProducer.VideoPrompt[segment]
    to: VideoProducer[segment].Prompt
  - from: Resolution
    to: VideoProducer[segment].Resolution
  - from: AspectRatio
    to: VideoProducer[segment].AspectRatio
  - from: SegmentDuration
    to: VideoProducer[segment].SegmentDuration  # Auto-computed system input

  # Wire video output to blueprint artifact
  - from: VideoProducer[segment].SegmentVideo
    to: SegmentVideo[segment]
```

---

## Producer YAML Reference

Producers define the interface for execution units - they specify what inputs they accept, what artifacts they produce, and how inputs map to provider-specific fields for each supported model.

### Complete Schema

```yaml
meta:
  name: <string>           # Human-readable name (required)
  description: <string>    # Purpose and behavior
  id: <string>             # Unique identifier in PascalCase (required)
  version: <semver>        # Semantic version
  author: <string>         # Creator name
  license: <string>        # License type
  promptFile: <string>     # Path to TOML prompt config (LLM producers only)
  outputSchema: <string>   # Path to JSON schema for structured output (LLM producers only)

inputs:
  - name: <string>         # Input identifier (required)
    description: <string>  # Purpose and usage
    type: <string>         # Data type (required)
    fanIn: <boolean>       # Whether this is a fan-in collection input
    dimensions: <string>   # Dimension labels for collections (e.g., "segment")

artifacts:
  - name: <string>         # Artifact identifier (required)
    description: <string>  # Purpose and content
    type: <string>         # Output type (required)
    itemType: <string>     # Element type for arrays
    countInput: <string>   # Input that determines array size
    arrays: <array>        # For JSON artifacts: array paths for virtual artifact decomposition

loops:
  - name: <string>         # Loop identifier
    description: <string>  # Purpose
    countInput: <string>   # Input for iteration count

mappings:
  <provider>:              # Provider name: replicate, fal-ai, openai, renku
    <model>:               # Model identifier
      <ProducerInput>: <providerField>           # Simple field mapping
      <ProducerInput>:                           # Object form for advanced mappings
        field: <providerField>                   # Target field name (supports dot notation)
        transform:                               # Value transformation table
          <inputValue>: <providerValue>
        expand: <boolean>                        # Spread object into payload
        firstOf: <boolean>                       # Extract first element from array
        invert: <boolean>                        # Flip boolean value
        intToString: <boolean>                   # Convert integer to string
        durationToFrames:                        # Convert seconds to frame count
          fps: <number>
        combine:                                 # Combine multiple inputs
          inputs: [<input1>, <input2>]
          table:
            "<val1>+<val2>": <result>
        conditional:                             # Conditional mapping
          when:
            input: <inputName>
            equals: <value>                      # or notEmpty: true, or empty: true
          then: <mapping>
```

**Note on Mappings:** The `mappings:` section defines how producer inputs map to provider-specific API fields. Each provider/model combination can have different field names and transformations. This allows producers to work with multiple models while keeping input files simple.

**Note on LLM Producers:** For producers that use LLMs (OpenAI, etc.), the `promptFile` and `outputSchema` fields are defined in the `meta:` section of the producer YAML file. These are intrinsic to the producer's functionality. Paths are relative to the producer YAML file location.

### Real Example: Script Producer

```yaml
meta:
  name: Script Generation
  description: Generate documentary scripts tailored to the user inquiry.
  id: ScriptProducer
  version: 0.1.0
  author: Renku
  license: MIT
  promptFile: ./script.toml              # Prompt template for LLM
  outputSchema: ./script-output.json     # JSON schema for structured output

inputs:
  - name: InquiryPrompt
    description: The topic describing the desired movie script.
    type: string
  - name: Duration
    description: Desired narration duration in seconds.
    type: int
  - name: NumOfSegments
    description: Number of narration segments to produce.
    type: int
  - name: Audience
    description: Target audience for tone and vocabulary. Model default varies.
    type: string
  - name: Language
    description: Narration language. Model default varies.
    type: string

artifacts:
  - name: MovieTitle
    description: The generated title for the documentary.
    type: string
  - name: MovieSummary
    description: Narrative summary for supplemental reading.
    type: string
  - name: NarrationScript
    description: Array of narration paragraphs per segment.
    type: array
    itemType: string
    countInput: NumOfSegments

loops:
  - name: segment
    description: Iterates over narration segments.
    countInput: NumOfSegments
```

**Note:** LLM producers define `promptFile` and `outputSchema` in the `meta:` section. The model selection (e.g., `gpt-4o`) is specified in the input template file.

### Real Example: Video Producer

```yaml
meta:
  name: Video Generation
  description: Generate a video that best reflects the given narrative script.
  id: VideoProducer
  version: 0.1.0
  author: Renku
  license: MIT

inputs:
  - name: Prompt
    description: The prompt to generate the video.
    type: string
  - name: AspectRatio
    description: Aspect ratio such as 16:9 or 3:2.
    type: string
  - name: Resolution
    description: The video resolution (480p, 720p, 1080p). Model default varies.
    type: string
  - name: SegmentDuration
    description: The video segment's duration in seconds. Model default varies.
    type: int

artifacts:
  - name: SegmentVideo
    description: Video file for the segment.
    type: video
  - name: FirstFrame
    description: The first frame of the generated video.
    type: image
  - name: LastFrame
    description: The last frame of the generated video.
    type: image
  - name: AudioTrack
    description: The audio track of the generated video.
    type: audio

mappings:
  replicate:
    bytedance/seedance-1-pro-fast:
      Prompt: prompt
      AspectRatio: aspect_ratio
      Resolution: resolution
      SegmentDuration: duration
    google/veo-3.1-fast:
      Prompt: prompt
      AspectRatio: aspect_ratio
  fal-ai:
    bytedance/seedream/v4.5/text-to-video:
      Prompt: prompt
      AspectRatio:
        field: image_size
        transform:
          "16:9": landscape_16_9
          "9:16": portrait_16_9
          "1:1": square_hd
      SegmentDuration:
        field: num_frames
        durationToFrames:
          fps: 24
```

### Derived Video Artifacts

Video-generating producers (text-to-video, image-to-video, etc.) automatically support **derived artifacts** that are extracted from the generated video using ffmpeg:

| Artifact | Type | Description |
|----------|------|-------------|
| `FirstFrame` | image | The first frame of the video as PNG |
| `LastFrame` | image | The last frame of the video as PNG |
| `AudioTrack` | audio | The audio track extracted as WAV |

**How derived artifacts work:**

1. **Declaration**: Declare derived artifacts in your producer YAML alongside the primary video artifact
2. **Connection**: Connect derived artifacts to downstream producers in your blueprint
3. **Automatic extraction**: When the video is downloaded, ffmpeg extracts the requested artifacts
4. **Efficiency**: Only artifacts that are actually connected to downstream producers are extracted

**Example: Using FirstFrame for image-to-video transitions**

```yaml
# In your blueprint
connections:
  # Generate video from text
  - from: VideoPromptProducer.Prompt[segment]
    to: VideoProducer[segment].Prompt

  # Use the last frame of segment N as the start image for segment N+1
  - from: VideoProducer[segment].LastFrame
    to: ImageToVideoProducer[segment+1].StartImage
```

**ffmpeg requirement:**

- If ffmpeg is not installed, a warning is logged but the blueprint continues
- Derived artifacts will have status "skipped" if ffmpeg is unavailable
- The primary video artifact is always produced regardless of ffmpeg availability
- Install ffmpeg to enable derived artifact extraction: https://ffmpeg.org/download.html

### Real Example: Audio Producer

```yaml
meta:
  name: Audio Producer
  description: Convert narration text into voiced audio segments.
  id: AudioProducer
  version: 0.1.0
  author: Renku
  license: MIT

inputs:
  - name: TextInput
    description: Text to synthesize.
    type: string
  - name: VoiceId
    description: Voice preset identifier for the provider.
    type: string
  - name: Emotion
    description: Optional emotion hint.
    type: string
  - name: Speed
    description: Speech speed multiplier.
    type: number

artifacts:
  - name: SegmentAudio
    description: Narrated audio file for the segment.
    type: audio

mappings:
  replicate:
    minimax/speech-2.6-hd:
      TextInput: text
      VoiceId: voice_id
      Emotion: emotion
      Speed: speed
  fal-ai:
    minimax/speech-2.6-hd:
      TextInput: prompt
      VoiceId: voice_setting.voice_id
      Emotion: voice_setting.emotion
      Speed: voice_setting.speed
    elevenlabs/tts/eleven-v3:
      TextInput: text
      VoiceId: voice
      Speed: speed
```

### Real Example: Timeline Composer (Fan-In Inputs)

```yaml
meta:
  name: Timeline Composer
  description: Compose assets into a ReMotion timeline.
  id: TimelineComposer
  version: 0.1.0
  author: Renku
  license: MIT

inputs:
  - name: ImageSegments
    description: Collected image assets grouped per segment.
    type: collection
    itemType: image
    dimensions: segment.image
    fanIn: true
  - name: VideoSegments
    description: Collected video assets grouped per narration segment.
    type: collection
    itemType: video
    dimensions: segment
    fanIn: true
  - name: AudioSegments
    description: Narration audio clips grouped per segment (master track).
    type: collection
    itemType: audio
    dimensions: segment
    fanIn: true
  - name: Music
    description: Background music clips that score the movie.
    type: audio
    fanIn: true
  - name: Duration
    description: Total duration of the movie in seconds.
    type: int

artifacts:
  - name: Timeline
    description: OrderedTimeline JSON manifest.
    type: json
```

---

## Connections

Connections define data flow between nodes in the workflow graph.

### Syntax Patterns

#### Direct Connections (Scalar to Scalar)

```yaml
connections:
  - from: InquiryPrompt
    to: ScriptProducer.InquiryPrompt
```

This wires the blueprint's `InquiryPrompt` input directly to the `ScriptProducer`'s `InquiryPrompt` input.

#### Array Indexing

```yaml
connections:
  - from: ScriptProducer.NarrationScript[segment]
    to: AudioProducer[segment].TextInput
```

This wires each element of `NarrationScript` to the corresponding `AudioProducer` instance:
- `NarrationScript[0]` → `AudioProducer[0].TextInput`
- `NarrationScript[1]` → `AudioProducer[1].TextInput`
- etc.

#### Multi-Dimensional Indexing (Nested Loops)

When you have nested loops (a loop with a `parent`), use multiple indices to address each dimension:

```yaml
# Define nested loops
loops:
  - name: segment
    countInput: NumOfSegments
  - name: image
    parent: segment                    # image is nested inside segment
    countInput: NumOfImagesPerNarrative

# Producer runs for each segment × image combination
producers:
  - name: ImageProducer
    producer: asset/text-to-image
    loop: segment.image                # Dot notation for nested loops

# Connections use multiple indices
connections:
  - from: ImagePromptProducer.ImagePrompt[segment][image]
    to: ImageProducer[segment][image].Prompt
  - from: ImageProducer[segment][image].GeneratedImage
    to: SegmentImage[segment][image]
```

**How it expands:** If `NumOfSegments = 3` and `NumOfImagesPerNarrative = 2`, this creates 6 producer instances:

| Instance | segment | image |
|----------|---------|-------|
| `ImageProducer[0][0]` | 0 | 0 |
| `ImageProducer[0][1]` | 0 | 1 |
| `ImageProducer[1][0]` | 1 | 0 |
| `ImageProducer[1][1]` | 1 | 1 |
| `ImageProducer[2][0]` | 2 | 0 |
| `ImageProducer[2][1]` | 2 | 1 |

**Important:** Both source and target must have matching dimension structure. You cannot connect `[segment][image]` to `[segment]` directly.

#### Offset Selectors

```yaml
connections:
  - from: ImageProducer[image].SegmentImage
    to: ImageToVideoProducer[segment].InputImage1
  - from: ImageProducer[image+1].SegmentImage
    to: ImageToVideoProducer[segment].InputImage2
```

Offset selectors (`[image+1]`, `[segment-1]`) create sliding window patterns. This example creates image-to-video transitions where each video uses adjacent images as start/end frames.

**Important:** When using offsets, ensure the source array is sized appropriately. For the example above, if you have `N` segments, you need `N+1` images. Use `countInputOffset: 1` on the `image` loop.

#### Constant Indices

```yaml
connections:
  - from: ImageProducer.SegmentImage[0]
    to: IntroVideoProducer.StartImage
  - from: ImageProducer.SegmentImage[1]
    to: IntroVideoProducer.EndImage
```

Hardcoded indices (`[0]`, `[1]`) select specific array elements.

#### Indexed Collection Binding

When a producer has a collection input (like `ReferenceImages`), you can connect different artifacts to specific indices of that collection:

```yaml
connections:
  # Different artifacts bound to specific collection indices
  - from: CharacterImageProducer.GeneratedImage
    to: VideoProducer[clip].ReferenceImages[0]
  - from: ProductImageProducer.GeneratedImage
    to: VideoProducer[clip].ReferenceImages[1]
```

This pattern is useful when:
- A producer accepts multiple reference images as a collection
- Each reference image comes from a different upstream producer
- The same images should be used for all loop instances (broadcast + element binding)

**How it works:**

1. The planner creates element-level input bindings: `ReferenceImages[0]` → `Artifact:CharacterImageProducer.GeneratedImage`
2. At runtime, the SDK reconstructs the array from these element-level bindings
3. The producer receives `ReferenceImages: [CharacterImage, ProductImage]`

**Example: Ad Video with Character and Product Images**

```yaml
producers:
  - name: CharacterImageProducer
    producer: asset/text-to-image
  - name: ProductImageProducer
    producer: asset/text-to-image
  - name: VideoProducer
    producer: asset/reference-to-video
    loop: clip

connections:
  # Character image → first reference image for all clips
  - from: CharacterImageProducer.GeneratedImage
    to: VideoProducer[clip].ReferenceImages[0]
  # Product image → second reference image for all clips
  - from: ProductImageProducer.GeneratedImage
    to: VideoProducer[clip].ReferenceImages[1]
  # Per-clip prompts
  - from: AdScriptProducer.AdScript.Scenes[clip].VideoPrompt
    to: VideoProducer[clip].Prompt
```

**Comparison with whole-collection binding:**

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Whole-collection | `AllImages → ReferenceImages` | Connect an entire array artifact |
| Element-level | `Image1 → ReferenceImages[0]`, `Image2 → ReferenceImages[1]` | Connect individual artifacts to specific indices |

Both patterns are supported and can be mixed depending on your workflow needs.

### Broadcast Connections

A scalar input can be broadcast to all instances of a looped producer:

```yaml
connections:
  - from: Style
    to: VideoPromptProducer[segment].Style
```

The same `Style` value is sent to every instance of `VideoPromptProducer`.

### Connection Resolution

When the planner resolves connections:

1. Parses source and target references
2. Extracts namespace path (e.g., `ScriptProducer`)
3. Extracts node name and dimension selectors
4. Aligns dimensions between source and target
5. Expands to concrete instances based on loop sizes

### Conditional Connections

Connections can be made conditional based on runtime values from upstream artifacts. This enables dynamic workflow branching where different producers execute depending on the data produced earlier in the pipeline.

#### Defining Conditions

Define named conditions in the `conditions:` section of your blueprint:

```yaml
conditions:
  isImageNarration:
    when: DocProducer.VideoScript.Segments[segment].NarrationType
    is: "ImageNarration"
  isAudioNeeded:
    any:
      - when: DocProducer.VideoScript.Segments[segment].NarrationType
        is: "TalkingHead"
      - when: DocProducer.VideoScript.Segments[segment].UseNarrationAudio
        is: true
  isTalkingHead:
    when: DocProducer.VideoScript.Segments[segment].NarrationType
    is: "TalkingHead"
```

#### Condition Path Format

The `when` field references a path to a value in an upstream artifact:

```
<Producer>.<Artifact>.<FieldPath>[dimension]
```

**Components:**
- **Producer**: The producer that creates the artifact (e.g., `DocProducer`)
- **Artifact**: The artifact name (e.g., `VideoScript`)
- **FieldPath**: Dot-separated path to the field (e.g., `Segments[segment].NarrationType`)
- **Dimensions**: Use dimension placeholders like `[segment]` for per-instance evaluation

The first two segments (`Producer.Artifact`) form the artifact ID. The remaining path navigates into the JSON structure of that artifact.

#### Condition Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Equals the specified value | `is: "ImageNarration"` |
| `isNot` | Does not equal the specified value | `isNot: "Draft"` |
| `contains` | String contains the value | `contains: "narration"` |
| `greaterThan` | Greater than (numeric) | `greaterThan: 10` |
| `lessThan` | Less than (numeric) | `lessThan: 100` |
| `greaterOrEqual` | Greater than or equal (numeric) | `greaterOrEqual: 5` |
| `lessOrEqual` | Less than or equal (numeric) | `lessOrEqual: 30` |
| `exists` | Field exists and is truthy | `exists: true` |
| `matches` | Matches a regular expression | `matches: "^video.*"` |

#### Condition Groups

Combine multiple conditions with `all` (AND) or `any` (OR):

```yaml
conditions:
  # OR: At least one condition must be true
  needsAudio:
    any:
      - when: DocProducer.VideoScript.Segments[segment].NarrationType
        is: "TalkingHead"
      - when: DocProducer.VideoScript.Segments[segment].UseNarrationAudio
        is: true

  # AND: All conditions must be true
  isHighQualityLongSegment:
    all:
      - when: DocProducer.VideoScript.Segments[segment].Quality
        is: "high"
      - when: DocProducer.VideoScript.Segments[segment].Duration
        greaterThan: 10
```

#### Using Conditions on Connections

Reference a named condition using the `if:` attribute on a connection:

```yaml
connections:
  # ImageProducer only runs when NarrationType is "ImageNarration"
  - from: DocProducer.VideoScript.Segments[segment].ImagePrompts[image]
    to: ImageProducer[segment][image].Prompt
    if: isImageNarration

  - from: AspectRatio
    to: ImageProducer[segment][image].AspectRatio
    if: isImageNarration

  # AudioProducer runs when TalkingHead OR UseNarrationAudio is true
  - from: DocProducer.VideoScript.Segments[segment].Script
    to: AudioProducer[segment].TextInput
    if: isAudioNeeded
```

**Important:** Apply the same condition to ALL connections targeting a producer if you want to conditionally skip that producer entirely.

#### Runtime Behavior

When a condition is evaluated at runtime:

1. **Condition Evaluation**: The runner resolves the artifact data and evaluates the condition for each dimension instance
2. **Input Filtering**: If a condition is not satisfied, that input is filtered out for that instance
3. **Job Skipping**: If ALL conditional inputs for a job instance are not satisfied, the job is **skipped**
4. **Artifact Absence**: Skipped jobs produce no artifacts - those artifact IDs are absent from the manifest

**Example Scenario:**

Given 3 segments with `NarrationType` values: `["ImageNarration", "TalkingHead", "ImageNarration"]`

| Producer | Index | Condition | Result |
|----------|-------|-----------|--------|
| `ImageProducer` | `[0][*]` | `isImageNarration` | ✅ Executes |
| `ImageProducer` | `[1][*]` | `isImageNarration` | ❌ Skipped |
| `ImageProducer` | `[2][*]` | `isImageNarration` | ✅ Executes |
| `AudioProducer` | `[0]` | `isAudioNeeded` | Depends on `UseNarrationAudio` |
| `AudioProducer` | `[1]` | `isAudioNeeded` | ✅ Executes (TalkingHead) |
| `AudioProducer` | `[2]` | `isAudioNeeded` | Depends on `UseNarrationAudio` |
| `VideoProducer` | `[0]` | `isTalkingHead` | ❌ Skipped |
| `VideoProducer` | `[1]` | `isTalkingHead` | ✅ Executes |
| `VideoProducer` | `[2]` | `isTalkingHead` | ❌ Skipped |

#### Blueprint Schema Addition

```yaml
conditions:
  <conditionName>:
    when: <string>         # Path to artifact field
    is: <any>              # Equals this value
    isNot: <any>           # Does not equal this value
    contains: <string>     # String contains value
    greaterThan: <number>  # Greater than
    lessThan: <number>     # Less than
    greaterOrEqual: <number>  # Greater than or equal
    lessOrEqual: <number>  # Less than or equal
    exists: <boolean>      # Field exists and is truthy
    matches: <string>      # Regex pattern
    all: <array>           # AND: all sub-conditions must pass
    any: <array>           # OR: at least one sub-condition must pass

connections:
  - from: <string>
    to: <string>
    if: <string>           # Optional: condition name
```

---

## Loops and Dimensions

Loops define iteration dimensions that enable parallel producer execution.

### Basic Loop

```yaml
loops:
  - name: segment
    description: Iterates over narration segments.
    countInput: NumOfSegments
```

This creates a `segment` dimension sized by the `NumOfSegments` input. If `NumOfSegments = 3`, producers assigned to this loop run 3 times.

### Loop with Offset

```yaml
loops:
  - name: image
    description: Iterates over images, one more than segments.
    countInput: NumOfSegments
    countInputOffset: 1
```

The iteration count is `NumOfSegments + 1`. Use this for sliding window patterns where you need one extra element.

### Nested Loops

```yaml
loops:
  - name: segment
    countInput: NumOfSegments
  - name: image
    parent: segment
    countInput: NumOfImagesPerSegment
```

This creates a two-dimensional iteration space. If `NumOfSegments = 3` and `NumOfImagesPerSegment = 2`, you get 6 instances:
- `[0][0]`, `[0][1]`
- `[1][0]`, `[1][1]`
- `[2][0]`, `[2][1]`

### Assigning Producers to Loops

```yaml
producers:
  - name: ScriptProducer
    path: ./script.yaml
    # No loop - runs once
  - name: AudioProducer
    path: ./audio.yaml
    loop: segment
    # Runs once per segment
  - name: ImageProducer
    path: ./image.yaml
    loop: segment.image
    # Runs for each segment × image combination
```

### Dimension Alignment

Dimensions align automatically by position in connections:

```yaml
connections:
  - from: VideoGenerator[segment].SegmentVideo
    to: TimelineComposer.VideoSegments
```

The planner matches the `segment` dimension on both sides. If dimensions don't align, the planner reports an error.

---

## Collectors and Fan-In

Collectors aggregate multiple artifacts into a single collection for downstream processing.

:::caution[Critical: Fan-In Requires BOTH Connection AND Collector]
A common mistake is to define only a collector without a connection. **Fan-in inputs require BOTH:**

1. A **connection** from the source artifact to the fan-in input
2. A **collector** that defines how to group and order the items

```yaml
# ❌ WRONG - Only collector, no connection (fan-in input will be empty!)
collectors:
  - name: TimelineImages
    from: ImageProducer[segment][image].GeneratedImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
    orderBy: image

# ✅ CORRECT - Both connection AND collector
connections:
  - from: ImageProducer[segment][image].GeneratedImage
    to: TimelineComposer.ImageSegments  # ← THIS IS REQUIRED!

collectors:
  - name: TimelineImages
    from: ImageProducer[segment][image].GeneratedImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
    orderBy: image
```

**Why both are needed:**
- The **connection** creates the data flow edge in the execution graph
- The **collector** tells the runtime HOW to group and order the collected items

Without the connection, the TimelineComposer won't have any edges pointing to its fan-in input, and the input will be empty at runtime.
:::

### Why Use Collectors?

Without collectors, connections are point-to-point. Collectors enable:
- Gathering all segment videos into a timeline
- Grouping images by segment for batch processing
- Ordering items within groups

### Basic Collector

```yaml
collectors:
  - name: TimelineVideo
    from: VideoProducer[segment].SegmentVideo
    into: TimelineComposer.VideoSegments
    groupBy: segment
```

This collects all `SegmentVideo` artifacts from `VideoProducer` instances and groups them by segment index.

### Collector with Ordering

```yaml
collectors:
  - name: TimelineImages
    from: ImageProducer[segment][image].SegmentImage
    into: TimelineComposer.ImageSegments
    groupBy: segment
    orderBy: image
```

This groups images by segment and orders them by image index within each group.

### Fan-In Inputs

The target input must be marked as `fanIn: true` in the producer:

```yaml
# In timeline-composer.yaml
inputs:
  - name: VideoSegments
    description: Collected video assets grouped per narration segment.
    type: collection
    itemType: video
    dimensions: segment
    fanIn: true
```

**Critical:** Without `fanIn: true`, the collector has no target and the aggregator cannot resolve the collection.

### What Collectors Produce

A collector creates a `FanInDescriptor` with:

```typescript
{
  groupBy: "segment",
  orderBy: "image",  // optional
  groups: [
    ["Artifact:ImageProducer.SegmentImage[0][0]", "Artifact:ImageProducer.SegmentImage[0][1]"],
    ["Artifact:ImageProducer.SegmentImage[1][0]", "Artifact:ImageProducer.SegmentImage[1][1]"],
    ["Artifact:ImageProducer.SegmentImage[2][0]", "Artifact:ImageProducer.SegmentImage[2][1]"]
  ]
}
```

### Real Example: Image-to-Video with Collectors

```yaml
# From image-to-video.yaml
loops:
  - name: segment
    countInput: NumOfSegments
  - name: image
    countInput: NumOfSegments
    countInputOffset: 1  # N+1 images for N segments

producers:
  - name: ImageProducer
    producer: asset/text-to-image
    loop: segment
  - name: ImageToVideoProducer
    producer: asset/image-to-video
    loop: segment
  - name: AudioProducer
    producer: asset/text-to-speech
    loop: segment
  - name: TimelineComposer
    producer: composition/timeline-composer

connections:
  # Sliding window for image-to-video transitions
  - from: ImageProducer[image].SegmentImage
    to: ImageToVideoProducer[segment].InputImage1
  - from: ImageProducer[image+1].SegmentImage
    to: ImageToVideoProducer[segment].InputImage2

  # Direct connection also goes to timeline
  - from: ImageToVideoProducer[segment].SegmentVideo
    to: TimelineComposer.VideoSegments
  - from: AudioProducer[segment].SegmentAudio
    to: TimelineComposer.AudioSegments

collectors:
  - name: TimelineVideo
    from: ImageToVideoProducer[segment].SegmentVideo
    into: TimelineComposer.VideoSegments
    groupBy: segment
  - name: TimelineAudio
    from: AudioProducer[segment].SegmentAudio
    into: TimelineComposer.AudioSegments
    groupBy: segment
```

---

## Canonical IDs

Canonical IDs are fully qualified identifiers used throughout the planner and runner.

### ID Format

```
Type:path.to.name[index0][index1]...
```

**Components:**
- **Type**: `Input:`, `Artifact:`, or `Producer:`
- **Path**: Dot-separated namespace path
- **Name**: Node name
- **Indices**: Dimension indices (0-based)

### Examples

| ID | Description |
|----|-------------|
| `Input:InquiryPrompt` | Blueprint-level input |
| `Input:ScriptProducer.Duration` | Input to ScriptProducer |
| `Artifact:VideoProducer.SegmentVideo[0]` | First video artifact |
| `Artifact:ImageProducer.SegmentImage[2][1]` | Image at segment 2, image 1 |
| `Producer:AudioProducer[0]` | First AudioProducer instance |

### How Canonical IDs are Generated

1. **Graph Building**: The planner creates nodes for all inputs, artifacts, and producers
2. **Dimension Collection**: Extracts dimension symbols from connections
3. **Expansion**: Creates concrete instances for each dimension combination
4. **ID Assignment**: Assigns canonical IDs with indices

### How Canonical IDs are Used

- **Planner**: Emits canonical IDs in the execution plan
- **Runner**: Resolves upstream artifacts using canonical IDs
- **Providers**: Access inputs via `runtime.inputs.getByNodeId(canonicalId)`

### Validation Functions

```typescript
isCanonicalInputId(value)     // Returns true if valid Input ID
isCanonicalArtifactId(value)  // Returns true if valid Artifact ID
isCanonicalProducerId(value)  // Returns true if valid Producer ID

parseCanonicalInputId(id)     // Returns { type, path, name }
parseCanonicalArtifactId(id)  // Returns { type, path, name, indices }
```

### Error Messages

- `"Expected canonical Input ID (Input:...), got \"${value}\"."`
- `"Invalid canonical Artifact ID: \"${value}\" has empty body."`

---

## Planner and Runner Internals

### Planner Process

#### 1. Blueprint Tree Loading

The planner loads the blueprint and all producer imports recursively:

```typescript
loadYamlBlueprintTree(blueprintPath)
// Returns: BlueprintTree with root blueprint and all imported producers
```

Circular references are detected and rejected.

#### 2. Graph Building

Creates nodes for all inputs, artifacts, and producers:

```typescript
buildCanonicalGraph(blueprintTree)
// Returns: { nodes, edges, collectors }
```

#### 3. Dimension Resolution

**Phase 1 - Explicit sizing:**
- Reads `countInput` values from input file
- Applies `countInputOffset` if present
- Assigns sizes to dimension symbols

**Phase 2 - Transitive derivation:**
- Propagates sizes through edges
- If edge has loop selector, target inherits source dimension size

**Error:**
```
Missing size for dimension "segment" on node "AudioProducer".
Ensure the upstream artefact declares countInput or can derive this dimension from a loop.
```

#### 4. Instance Expansion

Expands nodes to concrete instances using Cartesian product:

```typescript
// Node with dimensions [segment, image] where segment=2, image=3
// Creates 6 instances: [0,0], [0,1], [0,2], [1,0], [1,1], [1,2]
```

#### 5. Edge Alignment

For each dimension position, checks if instances align:

- Loop selectors: `[segment]` matches same index
- Offset selectors: `[segment+1]` matches with offset applied
- Constant selectors: `[0]` only matches index 0

#### 6. Input Node Collapsing

Merges aliased inputs and builds `inputBindings`:

```typescript
{
  "Producer:ScriptProducer": {
    "InquiryPrompt": "Input:InquiryPrompt"  // Alias → Canonical ID
  }
}
```

#### 7. Execution Layer Building

Uses topological sort (Kahn's algorithm):

1. Calculate in-degrees for all jobs
2. Jobs with in-degree 0 go to layer 0
3. Remove layer 0 jobs, decrement in-degrees
4. Repeat until all jobs assigned

**Error:**
```
Producer graph contains a cycle. Unable to create execution plan.
```

### Runner Process

#### 1. Layer-by-Layer Execution

```typescript
for (const layer of plan.layers) {
  for (const job of layer) {
    await executeJob(job, context);
  }
}
```

Jobs in the same layer can theoretically run in parallel.

#### 2. Artifact Resolution

Before executing a job, the runner:
1. Finds inbound edges from the plan
2. Loads upstream artifact data from event log
3. Adds to `job.context.extras.resolvedInputs`

#### 3. Fan-In Materialization

For fan-in inputs:
1. Groups members by `groupBy` dimension
2. Sorts each group by `orderBy` dimension (if present)
3. Returns nested array structure

```typescript
{
  groupBy: "segment",
  orderBy: "image",
  groups: [
    ["Artifact:Image[0][0]", "Artifact:Image[0][1]"],
    ["Artifact:Image[1][0]", "Artifact:Image[1][1]"]
  ]
}
```

#### 4. Provider Invocation

Calls the producer's `produce()` function with resolved context.

#### 5. Artifact Materialization

Persists produced artifacts to storage and logs events.

### Dirty Tracking (Incremental Runs)

The planner supports incremental execution:

1. **Determine dirty inputs**: Compare input hashes against manifest
2. **Determine dirty artifacts**: Find changed or missing artifacts
3. **Initial dirty jobs**: Jobs producing missing artifacts or touching dirty inputs
4. **Propagate**: BFS through dependency graph marks downstream jobs dirty

### JSON Virtual Artifact Decomposition

When a producer generates structured JSON output (using `meta.outputSchema`), the system decomposes the JSON into individual "virtual artifacts" - one for each leaf value in arrays. This enables:

1. **Fine-grained dirty tracking**: If you override one specific field in a JSON output, only the downstream jobs that depend on that specific field re-run
2. **Efficient incremental updates**: Modify one image prompt without regenerating all images
3. **Granular artifact storage**: Each leaf value is stored as a separate blob file

#### How It Works

For a producer with this output schema:

```json
{
  "name": "VideoScript",
  "schema": {
    "type": "object",
    "properties": {
      "Segments": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Script": { "type": "string" },
            "ImagePrompts": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

And artifact definition with arrays:

```yaml
artifacts:
  - name: VideoScript
    type: json
    arrays:
      - path: Segments
        countInput: NumOfSegments
      - path: Segments.ImagePrompts
        countInput: NumOfImagesPerSegment
```

The planner creates virtual artifacts like:
- `Artifact:DocProducer.VideoScript.Segments[0].Script`
- `Artifact:DocProducer.VideoScript.Segments[0].ImagePrompts[0]`
- `Artifact:DocProducer.VideoScript.Segments[0].ImagePrompts[1]`
- `Artifact:DocProducer.VideoScript.Segments[1].Script`
- etc.

#### Overriding Virtual Artifacts

You can override individual virtual artifacts in your input file:

```yaml
inputs:
  InquiryPrompt: "The history of the moon landing"
  # Override a specific image prompt
  DocProducer.VideoScript.Segments[0].ImagePrompts[0]: "file:custom-prompt.txt"
```

This triggers re-runs only for:
- The `ImageProducer[0][0]` job that consumes that specific prompt
- Any downstream jobs (like `TimelineComposer`)

Jobs that consume other prompts (`ImageProducer[0][1]`, `ImageProducer[1][0]`, etc.) are **not** re-run.

---

## Input Files Reference

Input files (also called input templates) are YAML files that provide runtime values and **model selections** for blueprints. This is where you select which AI models to use for each producer.

### Structure

```yaml
inputs:
  <InputName>: <value>

models:
  - model: <modelId>           # Model identifier (required)
    provider: <providerId>     # Provider name (required): openai, replicate, fal-ai, renku
    producerId: <ProducerName> # Which producer this model is for (required)
    config: <object>           # Provider-specific configuration (optional)
```

**Note:** Input-to-provider field mappings are defined in the producer YAML's `mappings:` section, not in the input template. This keeps input files simple - you only specify which model to use, not how inputs map to provider fields.

**Note:** For LLM producers, `promptFile` and `outputSchema` are defined in the producer YAML's `meta:` section. These are intrinsic to the producer's functionality.

### Input Values

```yaml
inputs:
  # User-provided inputs (declared in blueprint)
  InquiryPrompt: "Tell me about Darwin and Galapagos islands"
  VoiceId: Wise_Woman
  Emotion: neutral
  AspectRatio: "16:9"
  Resolution: "480p"
  Style: "Ghibli"

  # System inputs - provide here, no blueprint declaration needed
  Duration: 30          # Total movie duration in seconds
  NumOfSegments: 3      # Number of segments to generate
  # SegmentDuration is auto-computed as Duration/NumOfSegments (10 seconds)
  # Override if needed: SegmentDuration: 15
```

**System Inputs:** `Duration` and `NumOfSegments` are system inputs - you provide their values in the input YAML but don't need to declare them in the blueprint. `SegmentDuration` is automatically computed as `Duration / NumOfSegments` unless you explicitly provide a value.

### Model Configuration

The `models:` section defines which AI model to use for each producer. **This is required** - every producer in your blueprint needs a model configuration.

#### Basic Model Entry

```yaml
models:
  - model: minimax/speech-2.6-hd
    provider: replicate
    producerId: AudioProducer
```

The producer's `mappings:` section defines how inputs like `TextInput`, `Emotion`, and `VoiceId` map to provider fields - you don't need to specify that here.

#### LLM Producers (OpenAI)

For LLM-based producers that generate structured output:

```yaml
models:
  - model: gpt-5-mini
    provider: openai
    producerId: ScriptProducer
    config:
      text_format: json_schema
```

**Key fields:**
- `config.text_format`: Use `json_schema` for structured output, `text` for plain text

**Note:** The `promptFile` and `outputSchema` are defined in the producer YAML's `meta:` section. This keeps prompt configuration co-located with the producer logic.

#### Video/Image/Audio Producers

```yaml
models:
  - model: bytedance/seedance-1-pro-fast
    provider: replicate
    producerId: VideoProducer
  - model: google/nano-banana
    provider: replicate
    producerId: ImageProducer
  - model: minimax/speech-2.6-hd
    provider: replicate
    producerId: AudioProducer
```

The producer YAML files define how inputs like `Prompt`, `AspectRatio`, `Resolution` map to each provider's API fields.

#### Timeline Composer

```yaml
models:
  - model: timeline/ordered
    provider: renku
    producerId: TimelineComposer
    config:
      masterTracks: ["Audio", "Video"]
      videoClip:
        artifact: VideoSegments
      audioClip:
        artifact: AudioSegments
      musicClip:
        artifact: Music
        volume: 0.4
      tracks: ["Video", "Audio", "Music"]
```

### Complete Example

```yaml
inputs:
  # User-provided inputs
  InquiryPrompt: "Life of Napoleon Bonaparte"
  NumOfImagesPerSegment: 2
  Style: "Ghibli"
  AspectRatio: "16:9"
  Size: "1K"

  # System inputs - provide here, no blueprint declaration needed
  Duration: 20          # Total movie duration
  NumOfSegments: 2      # Number of segments
  # SegmentDuration auto-computed as 20/2 = 10 seconds

models:
  - model: gpt-5-mini
    provider: openai
    producerId: DocProducer
    config:
      text_format: json_schema
  - model: bytedance/seedream/v4.5/text-to-image
    provider: fal-ai
    producerId: ImageProducer
  - model: timeline/ordered
    provider: renku
    producerId: TimelineComposer
    config:
      tracks: ["Image"]
      masterTracks: ["Image"]
      numTracks: 1
      imageClip:
        artifact: ImageSegments[Image]
```

**Note:** `Duration` and `NumOfSegments` are system inputs - you provide values here but don't declare them in the blueprint. `SegmentDuration` is auto-computed as `Duration / NumOfSegments`. The `promptFile` and `outputSchema` for LLM producers are defined in the producer YAML file's `meta:` section.

### Data Types

| Type | YAML Syntax | Example |
|------|-------------|---------|
| `string` | Quoted text | `"Hello world"` |
| `int` | Numeric | `42` |
| `array` | YAML array | `["a", "b", "c"]` |

### Validation Rules

1. All required inputs must be present
2. Optional inputs use producer defaults if omitted
3. Input names are case-sensitive
4. Type mismatches cause validation errors
5. Every producer must have a model configuration in the `models:` section

---

## Validation Rules & Error Messages

### Blueprint Validation

| Rule | Error Message |
|------|---------------|
| Meta section required | `Blueprint must have a meta section` |
| Meta.id required | `Blueprint meta must have an id` |
| Meta.name required | `Blueprint meta must have a name` |
| At least one artifact | `Blueprint must declare at least one artifact` |
| Composite blueprints need producers | `Composite blueprint must have producer imports` |

### Input Validation

| Rule | Error Message |
|------|---------------|
| Optional inputs need defaults | `Optional input "${name}" must declare a default value` |
| Input name required | `Input must have a name` |
| Input type required | `Input must have a type` |

### Loop Validation

| Rule | Error Message |
|------|---------------|
| countInput required | `Loop "${name}" must declare countInput` |
| countInputOffset requires countInput | `countInputOffset requires countInput` |
| countInputOffset must be non-negative | `countInputOffset must be a non-negative integer` |

### Connection Validation

| Rule | Error Message |
|------|---------------|
| References cannot be empty | `Connection reference cannot be empty` |
| Valid dimension syntax | `Invalid dimension selector "${raw}". Expected "<loop>", "<loop>+<int>", "<loop>-<int>", or "<int>".` |
| Unknown dimension | `Unknown loop symbol "${symbol}"` |
| Dimension count mismatch | `Node "${id}" referenced with inconsistent dimension counts` |

### Collector Validation

| Rule | Error Message |
|------|---------------|
| groupBy references valid loop | `Collector groupBy "${dim}" is not a declared loop` |
| orderBy references valid loop | `Collector orderBy "${dim}" is not a declared loop` |

### Graph Validation

| Rule | Error Message |
|------|---------------|
| No cycles | `Producer graph contains a cycle. Unable to create execution plan.` |
| Producer found | `Missing producer catalog entry for ${producerAlias}` |
| Namespace exists | `Unknown sub-blueprint namespace "${path}"` |

### Dimension Resolution

| Rule | Error Message |
|------|---------------|
| Size resolved | `Missing size for dimension "${label}" on node "${nodeId}". Ensure the upstream artefact declares countInput or can derive this dimension from a loop.` |
| Consistent sizes | `Dimension "${symbol}" has conflicting sizes (${existing} vs ${size})` |

---

## Common Patterns

### Audio-Only Narration

Generate spoken narration from text:

```yaml
loops:
  - name: segment
    countInput: NumOfSegments

producers:
  - name: ScriptProducer
    producer: prompt/script
  - name: AudioProducer
    producer: asset/text-to-speech
    loop: segment

connections:
  - from: InquiryPrompt
    to: ScriptProducer.InquiryPrompt
  - from: ScriptProducer.NarrationScript[segment]
    to: AudioProducer[segment].TextInput
  - from: VoiceId
    to: AudioProducer[segment].VoiceId
  - from: AudioProducer[segment].SegmentAudio
    to: SegmentAudio[segment]
```

**Outputs:** `SegmentAudio[0..N].mp3`

### Video-Only

Generate video clips from prompts:

```yaml
loops:
  - name: segment
    countInput: NumOfSegments

producers:
  - name: ScriptProducer
    producer: prompt/script
  - name: VideoPromptProducer
    producer: prompt/video
  - name: VideoProducer
    producer: asset/text-to-video
    loop: segment

connections:
  - from: ScriptProducer.NarrationScript[segment]
    to: VideoPromptProducer[segment].NarrativeText
  - from: VideoPromptProducer.VideoPrompt[segment]
    to: VideoProducer[segment].Prompt
  - from: VideoProducer[segment].SegmentVideo
    to: SegmentVideo[segment]
```

**Outputs:** `SegmentVideo[0..N].mp4`

### Image-to-Video Flow (Sliding Window)

Generate transitions between images:

```yaml
loops:
  - name: segment
    countInput: NumOfSegments
  - name: image
    countInput: NumOfSegments
    countInputOffset: 1  # N+1 images for N segments

producers:
  - name: ImageProducer
    producer: asset/text-to-image
    loop: image
  - name: ImageToVideoProducer
    producer: asset/image-to-video
    loop: segment

connections:
  # Each video uses two adjacent images
  - from: ImageProducer[image].SegmentImage
    to: ImageToVideoProducer[segment].InputImage1
  - from: ImageProducer[image+1].SegmentImage
    to: ImageToVideoProducer[segment].InputImage2
```

**Result:**
- Segment 0: Image[0] → Image[1]
- Segment 1: Image[1] → Image[2]
- Segment 2: Image[2] → Image[3]

### Full Timeline (Video + Audio + Music)

Complete workflow with timeline composition:

```yaml
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

connections:
  # ... (script to video/audio connections)

  - from: Duration
    to: MusicProducer.Duration
  - from: VideoProducer[segment].SegmentVideo
    to: TimelineComposer.VideoSegments
  - from: AudioProducer[segment].SegmentAudio
    to: TimelineComposer.AudioSegments
  - from: MusicProducer.Music
    to: TimelineComposer.Music
  - from: TimelineComposer.Timeline
    to: Timeline

collectors:
  - name: TimelineVideo
    from: VideoProducer[segment].SegmentVideo
    into: TimelineComposer.VideoSegments
    groupBy: segment
  - name: TimelineAudio
    from: AudioProducer[segment].SegmentAudio
    into: TimelineComposer.AudioSegments
    groupBy: segment
  - name: MusicTrack
    from: MusicProducer.Music
    into: TimelineComposer.Music
    groupBy: segment  # Single group still needed for fan-in
```

---

## Debugging and Testing

### Validate Blueprint Structure

```bash
renku blueprints:validate <path-to-blueprint.yaml>
```

Expect clear errors for:
- Invalid dimension selectors
- Unknown loops
- Invalid `countInputOffset` usage
- Missing required fields
- Invalid references

### Dry Run

Test without calling AI providers:

```bash
RENKU_CLI_CONFIG=/path/to/cli-config.json \
renku generate \
  --inputs=<inputs.yaml> \
  --blueprint=<blueprint.yaml> \
  --dry-run
```

### Inspect Execution Plan

After generation, examine the plan:

```bash
cat <builds>/<movie>/runs/rev-0001-plan.json
```

Confirm:
- Inputs are present with canonical IDs
- Fan-in entries are populated for collectors
- Loop dimensions align correctly
- All connections are resolved

### Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| TimelineProducer cannot resolve inputs | Missing `fanIn: true` on input | Add `fanIn: true` to collection inputs |
| Fan-in descriptor is empty | No collector defined | Add collector from source to target |
| Planner dimension error | Mismatched dimensions in connection | Verify dimensions match between source/target |
| Blueprint validation error | `countInputOffset` without `countInput` | Add `countInput` to loop/artifact |
| Invalid selector syntax | Typo in loop name | Check loop names in `loops:` section |
| Missing artifacts | Generated files in wrong location | Use `dist/` per package builds |

### Debugging Steps

1. **Validate blueprint structure:**
   ```bash
   renku blueprints:validate my-blueprint.yaml
   ```

2. **Check producer paths:**
   - Ensure all `producers[].path` values point to valid YAML files
   - Paths are relative to the blueprint file location

3. **Verify connections:**
   - Ensure all sources and targets reference valid names
   - Check loop dimensions match between source and target

4. **Test with dry-run:**
   - Use `--dry-run` to validate without calling providers
   - Review plan structure in `plan.json`

5. **Inspect artifacts:**
   - After generation, verify artifact types and locations match expectations
   - Use `renku inspect --movie-id=<id>` to view metadata

---

## Directory Structure & File Naming

### Catalog Organization

```
catalog/
├── blueprints/
│   ├── audio-only/
│   │   ├── audio-only.yaml
│   │   └── input-template.yaml
│   ├── video-only/
│   │   ├── video-only.yaml
│   │   └── input-template.yaml
│   └── image-to-video/
│       ├── image-to-video.yaml
│       └── input-template.yaml
├── producers/
│   ├── asset/                              # Media generation producers
│   │   ├── text-to-image.yaml
│   │   ├── text-to-video.yaml
│   │   ├── text-to-speech.yaml
│   │   ├── text-to-music.yaml
│   │   └── image-to-video.yaml
│   ├── prompt/                             # LLM-based producers
│   │   ├── script/
│   │   │   ├── script.yaml
│   │   │   ├── script.toml
│   │   │   └── script-output.json
│   │   ├── video/
│   │   │   └── video.yaml
│   │   └── image/
│   │       └── image.yaml
│   └── composition/                        # Composition producers
│       ├── timeline-composer.yaml
│       └── video-exporter.yaml
└── models/
    └── *.yaml
```

**Producer Categories:**
- `asset/` - Media generation: images, video, audio, music
- `prompt/` - LLM-based script and prompt generation
- `composition/` - Timeline composition and video export

### File Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Blueprint files | kebab-case | `image-to-video.yaml` |
| Producer files | kebab-case | `script.yaml` |
| Blueprint/Producer IDs | PascalCase | `id: ImageToVideo` |
| Loop names | lowercase | `name: segment` |
| Input/Artifact names | PascalCase | `name: InquiryPrompt` |

### Producer References

**Preferred: Qualified names** resolve from the catalog:

```yaml
# Works from any location - resolves from catalog
producers:
  - name: ScriptProducer
    producer: prompt/script        # → catalog/producers/prompt/script/script.yaml
  - name: VideoProducer
    producer: asset/text-to-video  # → catalog/producers/asset/text-to-video.yaml
```

**Legacy: Relative paths** for custom local producers:

```yaml
# For custom producers not in the catalog
producers:
  - name: MyCustomProducer
    path: ./my-producers/custom.yaml  # Relative to blueprint file
```

---

## Related Resources

- **CLI Commands**: `renku --help`
- **Blueprint Examples**: `catalog/blueprints/`
- **Producer Examples**: `catalog/producers/`
- **Model Configurations**: `catalog/models/`

For feature requests and bug reports, please open an issue in the Renku repository.

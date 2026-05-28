# Video Analysis with Gemini CLI

Use Gemini CLI to analyze local video files. Gemini can describe what happens in the video, identify actions, UI interactions, and visual content.

## Critical Requirement

**MUST use `--yolo` mode.** Video processing requires automatic tool approval.

**The video file MUST be in Gemini's working directory.** Gemini CLI can only access files within its current working directory or subdirectories.

## Workflow Pattern

1. **Copy video to temporary directory**
2. **Navigate to that directory**
3. **Run gemini with `--yolo` and simple filename reference**

```bash
# Create temp directory
mkdir -p /tmp/gemini-work

# Copy video to temp directory
cp /path/to/your/video.webm /tmp/gemini-work/

# Navigate and analyze
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Describe what happens in video.webm"
```

## Command Syntax

```bash
cd <directory-with-video> && gemini --allowed-mcp-server-names "" --yolo "Your prompt about <filename>"
```

**DO NOT** use absolute paths in the prompt - only the filename.

## Supported Video Formats

- WEBM (.webm)
- MP4 (.mp4)
- MOV (.mov)

## Prompt Wording Tips

**Important:** Use "content of" or "What happens in" to ensure Gemini analyzes the video content rather than just describing the file.

```bash
# Good - analyzes video content
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "What happens in recording.webm?"
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Describe the content of demo.mp4"

# Also works
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Describe what happens in screencast.webm"
```

**Detail level:**
- Use "in detail" for comprehensive frame-by-frame analysis
- Use "briefly" for quick summaries

## Common Use Cases

### Describe Video Content

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Describe what happens in screencast.webm"
```

### Identify UI Interactions

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "List all the UI elements the user interacts with in demo.mp4"
```

### Extract Timeline

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Create a timeline of what happens in tutorial.webm with timestamps"
```

### Analyze User Flow

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Describe the user workflow shown in usability-test.mov"
```

### Compare Videos

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Compare before.webm and after.webm - what changed in the interface?"
```

## Output Formatting

For clean, parseable output:

```bash
cd /tmp/gemini-work && gemini --allowed-mcp-server-names "" --yolo "Summarize recording.mp4" --output-format text
```

## Example Full Workflow

```bash
# 1. Create working directory
mkdir -p /tmp/gemini-videos

# 2. Copy video
cp ~/Screencasts/feature-demo.webm /tmp/gemini-videos/

# 3. Analyze video
cd /tmp/gemini-videos && gemini --allowed-mcp-server-names "" --yolo "Describe what happens in feature-demo.webm in detail" --output-format text

# 4. Extract specific information
cd /tmp/gemini-videos && gemini --allowed-mcp-server-names "" --yolo "From feature-demo.webm, list: 1) All buttons clicked, 2) All forms filled, 3) All pages navigated to"

# 5. Clean up
rm -rf /tmp/gemini-videos
```

## Best Practices

1. **Be specific** - Ask for particular aspects rather than generic descriptions
2. **Use --output-format text** - For cleaner output when parsing results
3. **Request structured output** - Ask for timelines, lists, or step-by-step breakdowns
4. **Keep videos short** - Shorter clips provide more accurate analysis
5. **Always use --yolo** - Required for video processing

## Limitations

- Video analysis is based on visual frames and may miss audio content
- Very long videos may result in summarized rather than detailed analysis
- Fast-moving content may be harder to analyze accurately
- File size limits may apply for very large videos

## Difference from YouTube

| Local Videos | YouTube Videos |
|--------------|----------------|
| File in working directory | URL to YouTube |
| Analyzes actual video frames | Accesses page metadata/description |
| Use for screencasts, recordings | Use for online video content |
| `gemini --yolo "Describe video.mp4"` | `gemini --yolo "Summarize https://youtube.com/..."` |

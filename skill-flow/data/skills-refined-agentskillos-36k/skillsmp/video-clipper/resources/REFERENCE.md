# Video Clipper - Technical Reference

## Time Range Parsing (Single Snippet Mode)

The skill supports natural language time formats for creating single clips:

### Supported Time Formats

**Seconds only:**
- `55s` → 55 seconds
- `90s` → 90 seconds (1 minute 30 seconds)

**Minutes and seconds:**
- `2m35s` → 155 seconds (2 minutes 35 seconds)
- `5m` → 300 seconds (5 minutes)
- `1m30s` → 90 seconds

**Hours, minutes, seconds:**
- `1h30m` → 5400 seconds (1 hour 30 minutes)
- `1h30m15s` → 5415 seconds
- `2h` → 7200 seconds (2 hours)

**Colon-separated (MM:SS):**
- `1:30` → 90 seconds
- `5:45` → 345 seconds
- `0:55` → 55 seconds

**Colon-separated (HH:MM:SS):**
- `00:01:30` → 90 seconds
- `00:05:45` → 345 seconds
- `01:30:00` → 5400 seconds

### Time Range Examples

**Natural language:**
- `55s to 2m35s` → 00:00:55 to 00:02:35
- `1m30s to 5m45s` → 00:01:30 to 00:05:45
- `30s to 1m` → 00:00:30 to 00:01:00

**Colon format:**
- `0:55 to 2:35` → 00:00:55 to 00:02:35
- `1:30 to 5:45` → 00:01:30 to 00:05:45

**Mixed formats (supported):**
- `55s to 2:35` → 00:00:55 to 00:02:35
- `1:30 to 5m45s` → 00:01:30 to 00:05:45

### Parsing Logic

```python
import re

def parse_natural_time(time_str):
    """Parse natural language time to seconds"""
    time_str = time_str.strip().lower()

    # Pattern: 1h30m15s or 2m35s or 55s
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    match = re.match(pattern, time_str)

    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds

    # Pattern: MM:SS or HH:MM:SS
    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    return None

def parse_time_range(range_str):
    """Parse 'X to Y' time range"""
    # Split on 'to', '-', or other separators
    separators = [' to ', ' - ', '-to-', '--']

    for sep in separators:
        if sep in range_str:
            start, end = range_str.split(sep, 1)
            start_sec = parse_natural_time(start)
            end_sec = parse_natural_time(end)
            return start_sec, end_sec

    return None, None

def seconds_to_timestamp(seconds):
    """Convert seconds to HH:MM:SS"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
```

## ffmpeg Command Reference

### Basic Clipping Commands

#### Stream Copy (Fast, No Re-encoding)
```bash
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME -c copy output.mp4
```

**Pros:**
- Very fast (typically 10-100x real-time)
- No quality loss
- Low CPU usage
- Preserves original codec

**Cons:**
- May not cut at exact frame due to keyframe limitations
- Can have timestamp issues at clip boundaries
- Requires compatible codecs throughout

**Best for:**
- Quick previews
- Large files (>500 MB)
- When exact frame accuracy not critical
- Same format/codec throughout video

#### Re-encode (Slower, Precise)
```bash
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  output.mp4
```

**Pros:**
- Frame-accurate cuts
- Consistent quality across clips
- Can change formats/codecs
- No keyframe limitations

**Cons:**
- Much slower (0.5-2x real-time)
- Slight quality loss (depending on CRF)
- Higher CPU usage
- Larger processing time

**Best for:**
- Professional editing
- Precise timing required
- Format conversion needed
- Quality normalization

### Advanced Options

#### Avoiding Negative Timestamps (Copy Mode)
```bash
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME -c copy -avoid_negative_ts 1 output.mp4
```

The `-avoid_negative_ts 1` flag fixes timestamp issues that can occur when using stream copy mode with non-zero start times.

#### Custom Quality Settings (Encode Mode)
```bash
# Higher quality (larger file)
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  output.mp4

# Lower quality (smaller file)
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v libx264 -preset fast -crf 28 \
  -c:a aac -b:a 96k \
  output.mp4
```

**CRF Values (Constant Rate Factor):**
- 18: Visually lossless (very high quality)
- 23: Default (good quality)
- 28: Acceptable quality (smaller files)
- Range: 0-51 (lower = better quality)

**Preset Values (Speed/Quality Trade-off):**
- `ultrafast`: Fastest encoding, lowest quality per bitrate
- `fast`: Quick encoding, decent quality
- `medium`: Default, good balance
- `slow`: Better quality, slower encoding
- `veryslow`: Best quality, very slow encoding

#### Hardware Acceleration (Faster Encoding)

**macOS (VideoToolbox):**
```bash
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v h264_videotoolbox -b:v 5M \
  -c:a aac -b:a 128k \
  output.mp4
```

**Linux (VAAPI - Intel/AMD):**
```bash
ffmpeg -hwaccel vaapi -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v h264_vaapi -b:v 5M \
  -c:a aac -b:a 128k \
  output.mp4
```

**Linux/Windows (NVENC - NVIDIA):**
```bash
ffmpeg -hwaccel cuda -i input.mp4 -ss START_TIME -to END_TIME \
  -c:v h264_nvenc -preset fast -b:v 5M \
  -c:a aac -b:a 128k \
  output.mp4
```

### Input Seeking vs Output Seeking

#### Fast Seek (Input Seeking)
```bash
ffmpeg -ss START_TIME -i input.mp4 -to DURATION -c copy output.mp4
```
- Seeks before decoding (faster)
- Less precise (nearest keyframe)
- Best for copy mode

#### Precise Seek (Output Seeking)
```bash
ffmpeg -i input.mp4 -ss START_TIME -to END_TIME -c:v libx264 output.mp4
```
- Seeks after decoding (slower but precise)
- Frame-accurate
- Required for encode mode

---

## Timestamp Formats

### Supported Input Formats

#### HH:MM:SS (Hours:Minutes:Seconds)
```
00:00:00    → 0 seconds
00:05:30    → 330 seconds
01:23:45    → 5025 seconds
```

#### MM:SS (Minutes:Seconds)
```
0:00    → 0 seconds
5:30    → 330 seconds
23:45   → 1425 seconds
```

#### Seconds (Decimal)
```
0       → 0 seconds
330     → 5 minutes 30 seconds
5025.5  → 1 hour 23 minutes 45.5 seconds
```

### Parsing Logic

```python
import re

def parse_timestamp(ts_str):
    """
    Parse timestamp string to seconds.
    Supports: HH:MM:SS, MM:SS, or seconds
    """
    ts_str = ts_str.strip()

    # Try HH:MM:SS or MM:SS format
    if ':' in ts_str:
        parts = ts_str.split(':')
        parts = [int(p) for p in parts]

        if len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = parts
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # MM:SS
            minutes, seconds = parts
            return minutes * 60 + seconds
        else:
            raise ValueError(f"Invalid timestamp format: {ts_str}")
    else:
        # Assume seconds (int or float)
        return float(ts_str)

def seconds_to_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
```

### Chapter Line Parsing

```python
def parse_chapter_line(line):
    """
    Parse chapter line: "HH:MM:SS - Chapter Name"
    Returns: (start_seconds, chapter_name)
    """
    # Match timestamp followed by dash and name
    pattern = r'^(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(.+)$'
    match = re.match(pattern, line.strip())

    if not match:
        raise ValueError(f"Invalid chapter format: {line}")

    timestamp_str, name = match.groups()
    start_seconds = parse_timestamp(timestamp_str)

    return start_seconds, name.strip()
```

**Valid examples:**
```
00:00:00 - Introduction
5:30 - Main Content
01:23:45 - Conclusion
```

**Invalid examples:**
```
5 minutes 30 seconds - Chapter    ❌ (use 5:30)
00:05:30: Chapter                 ❌ (use dash, not colon)
Chapter at 5:30                   ❌ (timestamp must come first)
```

---

## Filename Sanitization

### Rules

1. **Remove dangerous characters**: `< > : " / \ | ? *`
2. **Replace spaces with underscores**: `Hello World` → `Hello_World`
3. **Collapse multiple underscores**: `A__B___C` → `A_B_C`
4. **Remove leading/trailing underscores**: `_Name_` → `Name`
5. **Limit length**: Maximum 100 characters
6. **Preserve case**: Don't force lowercase
7. **Keep alphanumeric, dash, underscore**: `[A-Za-z0-9_-]`

### Implementation

```python
import re

def sanitize_filename(name):
    """
    Convert chapter name to filesystem-safe filename.
    """
    # Remove dangerous characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)

    # Remove other special characters (except dash/underscore)
    name = re.sub(r'[^\w\s-]', '', name)

    # Replace whitespace with underscore
    name = re.sub(r'\s+', '_', name)

    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name)

    # Remove leading/trailing underscores
    name = name.strip('_')

    # Limit length
    if len(name) > 100:
        name = name[:100].rstrip('_')

    # Ensure not empty
    if not name:
        name = "Untitled"

    return name
```

### Examples

| Input | Output |
|-------|--------|
| `Hello World` | `Hello_World` |
| `Q&A: What is this?` | `QA_What_is_this` |
| `Part 1/2 - Introduction` | `Part_12_Introduction` |
| `"Welcome!" [Day 1]` | `Welcome_Day_1` |
| `Lists/Arrays & Objects` | `ListsArrays_Objects` |
| `Summary & Next Steps...` | `Summary_Next_Steps` |
| `A    B    C` | `A_B_C` |
| `____Test____` | `Test` |

---

## Troubleshooting Guide

### Problem: "Non-monotonous DTS in output stream"

**Error message:**
```
[mp4 @ 0x7f8a1c000000] Non-monotonous DTS in output stream 0:0
```

**Cause:** Timestamp discontinuity when using copy mode with certain source videos.

**Solution 1:** Add `-avoid_negative_ts 1`
```bash
ffmpeg -i input.mp4 -ss START -to END -c copy -avoid_negative_ts 1 output.mp4
```

**Solution 2:** Use encode mode instead
```bash
ffmpeg -i input.mp4 -ss START -to END -c:v libx264 -c:a aac output.mp4
```

---

### Problem: Clip doesn't start at exact timestamp

**Symptom:** Clip starts 1-3 seconds before/after specified time.

**Cause:** In copy mode, ffmpeg can only cut at keyframe boundaries.

**Solution 1:** Use encode mode for frame-accurate cuts
```bash
ffmpeg -i input.mp4 -ss START -to END -c:v libx264 -preset medium -crf 23 output.mp4
```

**Solution 2:** Place timestamps at keyframes
- Use `ffprobe` to find keyframe positions
- Adjust chapter timestamps to align with keyframes

**Check keyframes:**
```bash
ffprobe -select_streams v -show_frames -show_entries frame=pkt_pts_time,key_frame \
  -of csv input.mp4 | grep ",1$" | head -20
```

---

### Problem: Audio/Video out of sync

**Symptom:** Audio and video don't match in output clip.

**Cause:** Variable frame rate (VFR) source video with copy mode.

**Solution:** Re-encode with constant frame rate (CFR)
```bash
ffmpeg -i input.mp4 -ss START -to END \
  -c:v libx264 -preset medium -crf 23 \
  -r 30 \  # Force 30 fps
  -c:a aac -b:a 128k \
  output.mp4
```

---

### Problem: Clip file is empty or 0 bytes

**Possible causes:**
1. End time before start time
2. Start time beyond video duration
3. Write permission issues
4. Disk space full

**Diagnostic commands:**
```bash
# Check video duration
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 input.mp4

# Check disk space
df -h .

# Check write permissions
ls -ld output_directory/

# Test simple clip
ffmpeg -i input.mp4 -ss 00:00:00 -to 00:00:10 -c copy test.mp4
```

---

### Problem: "Invalid duration" error

**Error message:**
```
[NULL @ 0x7f8a1c000000] Invalid duration -0.000000
```

**Cause:** Start time and end time are the same or very close.

**Solution:** Ensure minimum clip duration (e.g., 0.1 seconds)
```python
if end_time - start_time < 0.1:
    raise ValueError(f"Clip duration too short: {end_time - start_time}s")
```

---

### Problem: ffmpeg not found

**Error message:**
```
bash: ffmpeg: command not found
```

**Solution: Install ffmpeg**

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
which ffmpeg
ffmpeg -version
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
which ffmpeg
ffmpeg -version
```

**RHEL/CentOS/Fedora:**
```bash
# Enable RPM Fusion repository first
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

sudo dnf install ffmpeg

# Verify installation
which ffmpeg
ffmpeg -version
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH environment variable
4. Restart terminal and verify: `ffmpeg -version`

---

### Problem: "Codec not supported" error

**Error message:**
```
Codec 'hevc' is not supported
```

**Cause:** Source video uses codec not available in your ffmpeg build.

**Solution 1:** Re-encode to supported codec
```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac input_converted.mp4
```

**Solution 2:** Install ffmpeg with more codecs
```bash
# macOS with all codecs
brew install ffmpeg --with-all

# Check available codecs
ffmpeg -codecs
```

---

### Problem: Clips are much larger than expected (encode mode)

**Cause:** Default encoding settings create high-quality output.

**Solution: Adjust CRF or bitrate**
```bash
# Lower quality, smaller file
ffmpeg -i input.mp4 -ss START -to END \
  -c:v libx264 -preset fast -crf 28 \
  -c:a aac -b:a 96k \
  output.mp4

# Or use bitrate control
ffmpeg -i input.mp4 -ss START -to END \
  -c:v libx264 -b:v 2M \
  -c:a aac -b:a 96k \
  output.mp4
```

---

### Problem: Processing is very slow (encode mode)

**Solution 1: Use faster preset**
```bash
ffmpeg -i input.mp4 -ss START -to END \
  -c:v libx264 -preset fast -crf 23 \
  output.mp4
```

**Solution 2: Use hardware acceleration**
```bash
# macOS
ffmpeg -i input.mp4 -ss START -to END \
  -c:v h264_videotoolbox -b:v 5M \
  output.mp4

# Linux with NVIDIA GPU
ffmpeg -hwaccel cuda -i input.mp4 -ss START -to END \
  -c:v h264_nvenc -preset fast \
  output.mp4
```

**Solution 3: Use copy mode**
```bash
ffmpeg -i input.mp4 -ss START -to END -c copy output.mp4
```

---

## Video Format Support

### Commonly Supported Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| MP4 | `.mp4` | Most common, widely supported |
| MOV | `.mov` | QuickTime, common on macOS |
| AVI | `.avi` | Older format, still supported |
| MKV | `.mkv` | Matroska, flexible container |
| WebM | `.webm` | Web-optimized format |
| FLV | `.flv` | Flash video (legacy) |
| WMV | `.wmv` | Windows Media Video |
| MPEG | `.mpg`, `.mpeg` | MPEG-1/MPEG-2 |
| TS | `.ts` | Transport stream |
| M4V | `.m4v` | iTunes video format |

### Video Codecs

| Codec | Notes | ffmpeg Encoder |
|-------|-------|----------------|
| H.264/AVC | Most common, good compatibility | `libx264` |
| H.265/HEVC | Better compression, newer | `libx265` |
| VP9 | Google codec, good for web | `libvpx-vp9` |
| AV1 | Next-gen codec, slow encoding | `libaom-av1` |
| MPEG-4 | Older standard | `mpeg4` |
| ProRes | Professional, large files | `prores` |

### Audio Codecs

| Codec | Notes | ffmpeg Encoder |
|-------|-------|----------------|
| AAC | Most common, good quality | `aac` |
| MP3 | Widely supported | `libmp3lame` |
| Opus | Best quality/size, modern | `libopus` |
| Vorbis | Open source, WebM | `libvorbis` |
| AC3 | Dolby Digital | `ac3` |
| PCM | Uncompressed | `pcm_s16le` |

---

## Performance Guidelines

### Copy Mode Performance

**Typical speeds (varies by system):**
- Small files (<100 MB): 10-20 seconds per clip
- Medium files (100-500 MB): 20-60 seconds per clip
- Large files (>500 MB): 1-3 minutes per clip

**Factors affecting speed:**
- Disk I/O speed (SSD much faster than HDD)
- Container format (MP4 faster than MKV)
- Codec complexity (H.264 faster than H.265)

### Encode Mode Performance

**Typical speeds (1080p video, medium preset):**
- 0.5-2x real-time (30-minute video takes 15-60 minutes)
- Faster with hardware acceleration (2-5x real-time)

**Factors affecting speed:**
- Video resolution (4K takes 4x longer than 1080p)
- Preset (ultrafast is 5-10x faster than slow)
- CPU cores (more cores = faster with threads)
- Hardware acceleration (GPU encoding much faster)

### Parallel Processing

For multiple clips, can process in parallel:
```bash
# Start all clips in background
for i in {1..5}; do
  ffmpeg -i input.mp4 -ss $START -to $END -c copy "clip_$i.mp4" &
done

# Wait for all to complete
wait
```

**Considerations:**
- System has enough CPU/RAM for parallel jobs
- Disk I/O doesn't become bottleneck
- Monitor system resources with `top` or `htop`

---

## Best Practices

### 1. Always validate inputs first
- Check video file exists and is readable
- Parse and validate all timestamps
- Get video duration before calculating clip ranges
- Verify output directory is writable

### 2. Choose the right mode
- **Copy mode:** Quick preview, large files, timing not critical
- **Encode mode:** Professional work, precise timing, format changes

### 3. Handle errors gracefully
- Catch ffmpeg errors and provide clear messages
- Validate clip output (file exists, size > 0)
- Report which clips succeeded/failed

### 4. Show progress
- For encode mode, show progress percentage
- For multiple clips, show "Clip N of M"
- Estimate remaining time when possible

### 5. Provide rollback capability
- Don't delete source video
- Save clips to separate directory
- Allow re-running with different settings

### 6. Test with small clips first
- Create one test clip before processing all
- Verify quality and timing
- Adjust settings if needed

---

## Advanced Techniques

### Batch Processing Script

```bash
#!/bin/bash
# batch_clip.sh - Process multiple videos with same chapter template

VIDEO_DIR="$1"
CHAPTERS_FILE="$2"

for video in "$VIDEO_DIR"/*.mp4; do
  echo "Processing: $video"

  # Create clips directory
  base=$(basename "$video" .mp4)
  mkdir -p "${VIDEO_DIR}/${base}_clips"

  # Read chapters and create clips
  while IFS= read -r line; do
    # Parse timestamp and name
    # Generate clip
  done < "$CHAPTERS_FILE"
done
```

### Quality Comparison

```bash
# Create same clip with different quality settings
ffmpeg -i input.mp4 -ss 00:00:00 -to 00:01:00 -c:v libx264 -crf 18 high_quality.mp4
ffmpeg -i input.mp4 -ss 00:00:00 -to 00:01:00 -c:v libx264 -crf 23 medium_quality.mp4
ffmpeg -i input.mp4 -ss 00:00:00 -to 00:01:00 -c:v libx264 -crf 28 low_quality.mp4

# Compare file sizes
ls -lh *_quality.mp4
```

### Extract Chapter Markers from Video Metadata

Some videos have embedded chapter markers:
```bash
ffprobe -v quiet -print_format json -show_chapters input.mp4
```

This can be parsed to automatically generate timestamp list.

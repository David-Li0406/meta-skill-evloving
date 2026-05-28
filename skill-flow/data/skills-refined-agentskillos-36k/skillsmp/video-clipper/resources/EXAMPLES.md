# Video Clipper - Examples

This document provides complete examples showing how the Video Clipper skill processes different inputs and generates clips.

## Example 1: Standard Customer Interview (Copy Mode)

### Input

**User message:**
> I have a customer interview video and want to split it by the topics we discussed. Here's the video and chapter markers:

**Video file:**
```
/Users/alice/videos/customer-feedback-emma.mp4
Duration: 18:45
Size: 352 MB
Format: MP4 (H.264/AAC)
```

**Chapter timestamps:**
```
00:00:00 - Introduction
00:02:57 - Memberships & Registration Management
00:09:41 - Lists vs Views Disconnect
00:15:30 - API Limitations & Integration Issues
```

**Encoding preference:** copy (fast mode)

### Processing Steps

1. **Validate ffmpeg:**
   ```bash
   $ which ffmpeg
   /usr/local/bin/ffmpeg

   $ ffmpeg -version
   ffmpeg version 6.1 Copyright (c) 2000-2023 the FFmpeg developers
   ```

2. **Parse timestamps:**
   ```
   Chapter 1: 00:00:00 (0 seconds) - Introduction
   Chapter 2: 00:02:57 (177 seconds) - Memberships & Registration Management
   Chapter 3: 00:09:41 (581 seconds) - Lists vs Views Disconnect
   Chapter 4: 00:15:30 (930 seconds) - API Limitations & Integration Issues
   ```

3. **Get video duration:**
   ```bash
   $ ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 customer-feedback-emma.mp4
   1125.45
   ```
   Video duration: 18:45 (1125 seconds)

4. **Calculate end times:**
   ```
   Clip 1: 00:00:00 → 00:02:57 (177 seconds)
   Clip 2: 00:02:57 → 00:09:41 (404 seconds)
   Clip 3: 00:09:41 → 00:15:30 (349 seconds)
   Clip 4: 00:15:30 → 18:45 (195 seconds)
   ```

5. **Sanitize filenames:**
   ```
   Introduction → Introduction
   Memberships & Registration Management → Memberships_Registration_Management
   Lists vs Views Disconnect → Lists_vs_Views_Disconnect
   API Limitations & Integration Issues → API_Limitations_Integration_Issues
   ```

6. **Create output directory:**
   ```bash
   $ mkdir -p /Users/alice/videos/customer-feedback-emma_clips
   ```

7. **Execute ffmpeg commands:**
   ```bash
   # Clip 1
   $ ffmpeg -i /Users/alice/videos/customer-feedback-emma.mp4 \
     -ss 00:00:00 -to 00:02:57 \
     -c copy -avoid_negative_ts 1 \
     "/Users/alice/videos/customer-feedback-emma_clips/01-Introduction.mp4"

   # Clip 2
   $ ffmpeg -i /Users/alice/videos/customer-feedback-emma.mp4 \
     -ss 00:02:57 -to 00:09:41 \
     -c copy -avoid_negative_ts 1 \
     "/Users/alice/videos/customer-feedback-emma_clips/02-Memberships_Registration_Management.mp4"

   # Clip 3
   $ ffmpeg -i /Users/alice/videos/customer-feedback-emma.mp4 \
     -ss 00:09:41 -to 00:15:30 \
     -c copy -avoid_negative_ts 1 \
     "/Users/alice/videos/customer-feedback-emma_clips/03-Lists_vs_Views_Disconnect.mp4"

   # Clip 4
   $ ffmpeg -i /Users/alice/videos/customer-feedback-emma.mp4 \
     -ss 00:15:30 -to 00:18:45 \
     -c copy -avoid_negative_ts 1 \
     "/Users/alice/videos/customer-feedback-emma_clips/04-API_Limitations_Integration_Issues.mp4"
   ```

### Output

**Created files:**
```
/Users/alice/videos/customer-feedback-emma_clips/
├── 01-Introduction.mp4                                    15.2 MB  (02:57)
├── 02-Memberships_Registration_Management.mp4             78.3 MB  (06:44)
├── 03-Lists_vs_Views_Disconnect.mp4                       67.1 MB  (05:49)
└── 04-API_Limitations_Integration_Issues.mp4              38.9 MB  (03:15)

Total: 4 clips, 199.5 MB
```

**Summary report:**
```markdown
# Video Clipping Complete

## Source Video
- File: /Users/alice/videos/customer-feedback-emma.mp4
- Duration: 18:45
- Size: 352 MB
- Format: MP4 (H.264/AAC)

## Created Clips

| # | Clip Name | Duration | Size | Time Range |
|---|-----------|----------|------|------------|
| 1 | 01-Introduction.mp4 | 02:57 | 15.2 MB | 00:00:00 - 00:02:57 |
| 2 | 02-Memberships_Registration_Management.mp4 | 06:44 | 78.3 MB | 00:02:57 - 00:09:41 |
| 3 | 03-Lists_vs_Views_Disconnect.mp4 | 05:49 | 67.1 MB | 00:09:41 - 00:15:30 |
| 4 | 04-API_Limitations_Integration_Issues.mp4 | 03:15 | 38.9 MB | 00:15:30 - 00:18:45 |

## Summary
- Total clips created: 4
- Total size: 199.5 MB
- Output location: /Users/alice/videos/customer-feedback-emma_clips/
- Encoding mode: copy
- Processing time: ~12 seconds

## Warnings
⚠️ Copy mode may result in clips that don't start exactly at the specified timestamp due to keyframe positions. If you need frame-accurate cuts, re-run with "encode" mode.

## Commands Used
All ffmpeg commands shown above in step 7.
```

---

## Example 2: Tutorial Video with Re-encoding (Encode Mode)

### Input

**User message:**
> I recorded a tutorial and need precise cuts at each section. Use encode mode.

**Video file:**
```
/home/bob/recordings/python-tutorial.mkv
Duration: 45:30
Size: 890 MB
Format: MKV (H.265/Opus)
```

**Chapter timestamps:**
```
0:00 - Introduction & Setup
5:45 - Variables and Data Types
15:20 - Control Flow (If/Else/Loops)
28:40 - Functions and Modules
38:15 - Final Project Demo
```

**Encoding preference:** encode (precise cuts)

### Processing Steps

1. **Parse MM:SS format timestamps:**
   ```
   Chapter 1: 00:00:00 (0 seconds)
   Chapter 2: 00:05:45 (345 seconds)
   Chapter 3: 00:15:20 (920 seconds)
   Chapter 4: 00:28:40 (1720 seconds)
   Chapter 5: 00:38:15 (2295 seconds)
   ```

2. **Calculate end times:**
   ```
   Clip 1: 00:00:00 → 00:05:45 (345 seconds)
   Clip 2: 00:05:45 → 00:15:20 (575 seconds)
   Clip 3: 00:15:20 → 00:28:40 (800 seconds)
   Clip 4: 00:28:40 → 00:38:15 (575 seconds)
   Clip 5: 00:38:15 → 00:45:30 (435 seconds)
   ```

3. **Sanitize filenames:**
   ```
   Introduction & Setup → Introduction_Setup
   Variables and Data Types → Variables_and_Data_Types
   Control Flow (If/Else/Loops) → Control_Flow_If_Else_Loops
   Functions and Modules → Functions_and_Modules
   Final Project Demo → Final_Project_Demo
   ```

4. **Execute ffmpeg commands with encoding:**
   ```bash
   # Clip 1
   $ ffmpeg -i /home/bob/recordings/python-tutorial.mkv \
     -ss 00:00:00 -to 00:05:45 \
     -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k \
     "/home/bob/recordings/python-tutorial_clips/01-Introduction_Setup.mp4"

   # Clip 2
   $ ffmpeg -i /home/bob/recordings/python-tutorial.mkv \
     -ss 00:05:45 -to 00:15:20 \
     -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k \
     "/home/bob/recordings/python-tutorial_clips/02-Variables_and_Data_Types.mp4"

   # (Similar commands for clips 3-5...)
   ```

### Output

**Created files:**
```
/home/bob/recordings/python-tutorial_clips/
├── 01-Introduction_Setup.mp4                  45.2 MB  (05:45)
├── 02-Variables_and_Data_Types.mp4            78.9 MB  (09:35)
├── 03-Control_Flow_If_Else_Loops.mp4         112.4 MB  (13:20)
├── 04-Functions_and_Modules.mp4               85.6 MB  (09:35)
└── 05-Final_Project_Demo.mp4                  63.1 MB  (07:15)

Total: 5 clips, 385.2 MB
```

**Notes:**
- Encoding took ~8 minutes (slower than copy mode)
- Output file sizes smaller due to re-encoding from H.265 to H.264
- Cuts are frame-accurate at specified timestamps
- All clips in consistent MP4/H.264 format

---

## Example 3: Using Video Transcript Analyzer Output

### Workflow

**Step 1: User runs Video Transcript Analyzer**
```
User: "Analyze this customer call transcript"
→ Skill generates analysis with chapter markers:

**00:02:57 - Memberships & Registration Management**
**00:09:41 - Lists vs Views Disconnect**
**00:15:30 - API Limitations**
**00:20:15 - Workflow Automation Issues**
```

**Step 2: User wants clips from those chapters**
```
User: "Now create video clips from these chapters"
```

**Step 3: Video Clipper asks for information**
```
Claude: "I'll create clips from those chapter markers. I need:
1. Path to the video file
2. Encoding preference (copy or encode)

The chapters I found:
- 00:02:57 - Memberships & Registration Management
- 00:09:41 - Lists vs Views Disconnect
- 00:15:30 - API Limitations
- 00:20:15 - Workflow Automation Issues

What's the path to your video file?"
```

**Step 4: User provides video path**
```
User: "/Users/alice/videos/call-recording.mp4"
Claude: "Choose encoding mode (copy/encode):"
User: "copy"
```

**Step 5: Skill creates clips**

**Important note about first chapter:**
The analysis starts at 00:02:57 (not 00:00:00), so the skill should:

1. **Option A: Ask user if they want the first 2:57 as a clip**
   ```
   Claude: "Your first chapter starts at 00:02:57. Would you like to include:
   - Clip 0: 00:00:00 - 00:02:57 (Introduction)
   Or start with chapter 1?"
   ```

2. **Option B: Include automatically with generic name**
   ```
   Clips created:
   00-Opening.mp4 (00:00:00 - 00:02:57)
   01-Memberships_Registration_Management.mp4 (00:02:57 - 00:09:41)
   02-Lists_vs_Views_Disconnect.mp4 (00:09:41 - 00:15:30)
   03-API_Limitations.mp4 (00:15:30 - 00:20:15)
   04-Workflow_Automation_Issues.mp4 (00:20:15 - 00:25:42)
   ```

---

## Example 4: Error Cases

### Case 1: Invalid Timestamp Format

**Input:**
```
Chapters:
00:00:00 - Intro
5:30 minutes - Setup
15-45 - Demo
```

**Error:**
```
❌ Error parsing timestamp "5:30 minutes"
Expected format: HH:MM:SS or MM:SS
Examples: 00:05:30 or 5:30

Please correct and try again.
```

### Case 2: Timestamps Out of Order

**Input:**
```
00:00:00 - Intro
00:15:30 - Demo
00:05:30 - Setup
```

**Warning:**
```
⚠️ Timestamps are not in chronological order:
  - "Demo" at 00:15:30 comes before "Setup" at 00:05:30

Would you like me to:
1. Sort them automatically
2. Let you correct them manually
```

### Case 3: Timestamp Beyond Video Duration

**Input:**
```
Video duration: 15:30
Chapters:
00:00:00 - Intro
00:05:00 - Main
00:20:00 - Outro
```

**Error:**
```
❌ Chapter "Outro" timestamp (00:20:00) exceeds video duration (00:15:30)

Please verify your timestamps and video file.
```

### Case 4: ffmpeg Not Installed

**Error:**
```
❌ ffmpeg is not installed on your system.

To install:
- macOS: brew install ffmpeg
- Linux (Ubuntu/Debian): sudo apt-get install ffmpeg
- Linux (RHEL/CentOS): sudo yum install ffmpeg
- Windows: Download from https://ffmpeg.org/download.html

After installation, try again.
```

---

## Example 5: Complex Filenames with Special Characters

### Input

**Chapters:**
```
00:00:00 - Welcome! Introduction & Setup
00:05:30 - Q&A: What is Python?
00:12:00 - "Hello World" - Your First Program
00:18:45 - Lists/Arrays [Deep Dive]
00:25:00 - Summary & Next Steps...
```

### Sanitized Filenames

```
01-Welcome_Introduction_Setup.mp4
02-QA_What_is_Python.mp4
03-Hello_World_Your_First_Program.mp4
04-Lists_Arrays_Deep_Dive.mp4
05-Summary_Next_Steps.mp4
```

**Characters removed/replaced:**
- `!` removed
- `&` removed
- `?` removed
- `"` removed
- `/` removed
- `[` `]` removed
- `:` removed
- `...` removed
- Multiple spaces → single underscore
- Multiple underscores → single underscore

---

## Example 6: Large Video with Many Chapters

### Input

**Video:** Conference recording (2:45:30, 4.2 GB)

**15 chapters** spanning the full video

### Processing

**Time estimates:**
- **Copy mode:** ~2-3 minutes (fast stream copy)
- **Encode mode:** ~45-60 minutes (re-encoding entire video in chunks)

**Recommendation:**
```
For large videos with many clips, copy mode is recommended unless you need:
- Frame-accurate cuts
- Format conversion
- Quality normalization across clips

Processing time estimate:
- Copy mode: ~2-3 minutes
- Encode mode: ~45-60 minutes

Proceed with copy mode? (Y/n)
```

### Output Structure

```
conference-2025_clips/
├── 01-Opening_Keynote.mp4                     245 MB  (15:00)
├── 02-Session_1_Architecture.mp4              389 MB  (22:30)
├── 03-Session_2_Security.mp4                  312 MB  (18:15)
... (12 more clips)
└── 15-Closing_Remarks.mp4                     128 MB  (08:45)

Total: 15 clips, 3.8 GB
```

---

## Example 7: Minimal Input (Just Two Clips)

### Input

**User message:**
> Split this video into two parts at 10:30

**Video:** `/Users/user/video.mp4` (20:00 duration)

### Interpretation

Skill asks: "Would you like to name these clips, or use default names?"

**Option 1: User provides names**
```
User: "Part 1 and Part 2"

Clips created:
01-Part_1.mp4 (00:00:00 - 00:10:30)
02-Part_2.mp4 (00:10:30 - 00:20:00)
```

**Option 2: Default names**
```
Clips created:
01-Segment_1.mp4 (00:00:00 - 00:10:30)
02-Segment_2.mp4 (00:10:30 - 00:20:00)
```

---

## Tips for Best Results

1. **Start timestamp at 00:00:00**
   - Always include the video start as your first chapter
   - Avoids confusion about what to do with the opening content

2. **Use consistent timestamp formats**
   - Either all HH:MM:SS or all MM:SS
   - Easier to parse and validate

3. **Test with copy mode first**
   - Much faster for previewing clip boundaries
   - Can re-run with encode mode if cuts aren't precise enough

4. **Descriptive chapter names**
   - Make it clear what content is in each clip
   - Avoid generic names like "Part 1", "Part 2"

5. **Consider video length**
   - For videos > 1 hour, copy mode saves significant time
   - For videos < 10 minutes, encode mode overhead is minimal

6. **Verify timestamps before processing**
   - Watch the video and note actual transition points
   - Use video player's timestamp feature to get exact times

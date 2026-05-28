# Video Clipper Skill

Create video clips from a source video using ffmpeg. Supports two modes:
1. **Single snippet**: Extract one clip from a time range (e.g., "55s to 2m35s")
2. **Multi-chapter**: Split video into multiple clips based on chapter timestamps

## Quick Start

### Single Snippet Mode

**For extracting one clip from a time range:**

1. Say: "Create a clip from 55s to 2m35s" (or any time range)
2. Provide video file path when prompted
3. Choose encoding mode (copy or encode)
4. Done! Your clip is created

**Example time formats:**
- `55s to 2m35s` (natural language)
- `1:30 to 5:45` (MM:SS)
- `00:01:30 to 00:05:45` (HH:MM:SS)

### Multi-Chapter Mode

**For splitting into multiple clips:**

1. **Have your video file ready**
   - Any common format: MP4, MOV, AVI, MKV, etc.

2. **Prepare chapter timestamps**
   - Format: `HH:MM:SS - Chapter Name` or `MM:SS - Chapter Name`
   - Example:
     ```
     00:00:00 - Introduction
     00:05:30 - Main Content
     00:15:45 - Q&A Session
     ```

3. **Invoke the skill**
   - Say: "Split this video by chapters"
   - Or: "Use video-clipper skill"

4. **Provide information when prompted**
   - Video file path
   - Chapter timestamps
   - Output directory (optional)
   - Encoding mode: "copy" (fast) or "encode" (precise)

## When to Use

Use this skill when you need to:
- Create a quick snippet from a time range
- Extract specific segments from a video
- Split a long video into topic-based clips
- Create individual clips from chapter markers
- Process videos after running Video Transcript Analyzer

## Requirements

**ffmpeg must be installed:**

- **macOS:** `brew install ffmpeg`
- **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
- **RHEL/CentOS:** `sudo yum install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Encoding Modes

### Copy Mode (Fast)
- **Speed:** Very fast (10-100x real-time)
- **Quality:** No quality loss
- **Precision:** May not cut at exact frame (keyframe limitations)
- **Best for:** Large files, quick previews, when timing not critical

### Encode Mode (Precise)
- **Speed:** Slower (0.5-2x real-time)
- **Quality:** Slight quality loss (adjustable)
- **Precision:** Frame-accurate cuts
- **Best for:** Professional work, precise timing, format conversion

## Example Usage

### Example 1: Basic Usage
```
User: "I need to split my customer interview video by topics"

Claude: "I'll help you split the video. First, is ffmpeg installed?"
→ Checks ffmpeg installation

Claude: "What's the path to your video file?"
User: "/Users/alice/videos/interview.mp4"

Claude: "Please provide chapter timestamps in this format:
        00:00:00 - Chapter Name
        00:05:30 - Next Chapter"

User: "00:00:00 - Introduction
       00:03:15 - Product Feedback
       00:12:30 - Feature Requests
       00:18:45 - Closing"

Claude: "Where would you like clips saved? (default: same folder as video)"
User: [Enter]

Claude: "Encoding mode? (copy = fast, encode = precise)"
User: "copy"

Claude: "Creating 4 clips from interview.mp4..."
→ Generates and executes ffmpeg commands
→ Creates clips:
  01-Introduction.mp4
  02-Product_Feedback.mp4
  03-Feature_Requests.mp4
  04-Closing.mp4

Claude: "✓ Successfully created 4 clips (total: 245 MB)
         Location: /Users/alice/videos/interview_clips/"
```

### Example 2: After Video Transcript Analyzer
```
User: "I just analyzed a transcript and got chapter markers. Now create clips from those."

Claude: "Great! I can use those chapter markers. What's the video file path?"
User: "/Users/bob/recording.mp4"

Claude: "I see these chapters from your analysis:
        00:02:57 - Memberships & Registration
        00:09:41 - Lists vs Views
        00:15:30 - API Limitations

        Your first chapter starts at 00:02:57. Include 00:00:00 - 00:02:57 as opening clip?"
User: "Yes"

Claude: "Encoding mode?"
User: "encode"

Claude: "Creating 4 clips with frame-accurate cuts..."
→ Creates clips including opening segment

Claude: "✓ Complete! 4 clips created with precise timing."
```

## Output

The skill creates:

1. **Individual video clips**
   - Numbered sequentially: `01-Chapter_Name.mp4`
   - Spaces replaced with underscores
   - Special characters removed
   - Saved in output directory

2. **Summary report**
   - List of created clips with durations and sizes
   - Total size of all clips
   - Commands used (for reference)
   - Any warnings or errors

## Tips

### Getting Good Results

1. **Start at 00:00:00**
   - Always include the video beginning as first chapter
   - Avoids confusion about opening content

2. **Use copy mode first**
   - Much faster for testing
   - Can re-run with encode mode if cuts aren't precise

3. **Verify timestamps**
   - Watch video and note exact transition points
   - Use video player's timestamp feature

4. **Descriptive chapter names**
   - Make it clear what's in each clip
   - Avoid generic names like "Part 1"

### Workflow Integration

**Combined with Video Transcript Analyzer:**
1. Run Video Transcript Analyzer on your transcript
2. Get chapter markers with timestamps
3. Use Video Clipper to create clips from those markers
4. Result: Organized video library with transcripts

### Choosing Encoding Mode

**Use Copy Mode when:**
- Video is large (>500 MB)
- You need quick results
- Exact frame precision not critical
- Keeping original quality important

**Use Encode Mode when:**
- You need frame-accurate cuts
- Converting formats
- Normalizing quality across clips
- Professional/final output

## Troubleshooting

### Clips don't start at exact timestamp
**Cause:** Copy mode cuts at keyframes, not exact frames
**Solution:** Use encode mode for frame-accurate cuts

### "Non-monotonous DTS" error
**Cause:** Timestamp issue in copy mode
**Solution:** Skill automatically adds `-avoid_negative_ts 1` flag

### Audio/video out of sync
**Cause:** Variable frame rate source video
**Solution:** Use encode mode with fixed frame rate

### Processing very slow
**Cause:** Using encode mode on large video
**Solutions:**
- Use copy mode (much faster)
- Use faster preset: `-preset fast`
- Enable hardware acceleration (if available)

### ffmpeg not found
**Solution:** Install ffmpeg (see Requirements section)

## File Organization

After processing, your files will look like:

```
videos/
├── my-video.mp4                           (original)
└── my-video_clips/                        (created)
    ├── 01-Introduction.mp4
    ├── 02-Main_Content.mp4
    ├── 03-Demo.mp4
    └── 04-Conclusion.mp4
```

## Performance

**Typical processing times:**

| Video Size | Copy Mode | Encode Mode |
|------------|-----------|-------------|
| 100 MB     | ~10 sec   | ~5 min      |
| 500 MB     | ~30 sec   | ~20 min     |
| 1 GB       | ~1 min    | ~40 min     |
| 5 GB       | ~3 min    | ~3 hours    |

*Times vary by system specs, resolution, and codec*

## Supported Formats

### Input Formats
- MP4, MOV, AVI, MKV, WebM
- FLV, WMV, MPEG, TS, M4V
- Most common video formats

### Output Format
- MP4 (H.264 video, AAC audio)
- Most widely compatible format
- Works on all platforms and devices

## Advanced Usage

### Custom Output Directory
```
User: "Save clips to /Users/alice/Desktop/clips"
```

### Custom Filename Prefix
```
User: "Use 'segment' as filename prefix instead of numbers"
→ Creates: segment-Introduction.mp4, segment-Main_Content.mp4
```

### Quality Settings (Encode Mode)
```
User: "Use high quality encoding (CRF 18)"
→ Skill adjusts ffmpeg command: -crf 18 (higher quality, larger files)

User: "Use smaller file sizes (CRF 28)"
→ Skill adjusts ffmpeg command: -crf 28 (lower quality, smaller files)
```

## Examples Directory

See `resources/EXAMPLES.md` for complete examples with:
- Full input/output for various scenarios
- Error cases and solutions
- Complex filename handling
- Large video processing

## Technical Reference

See `resources/REFERENCE.md` for:
- Detailed ffmpeg command reference
- Timestamp parsing logic
- Filename sanitization rules
- Troubleshooting guide
- Performance optimization tips
- Codec and format information

## Support

### Common Questions

**Q: Can I split a video without chapter markers?**
A: Yes! Just provide timestamps with generic names:
```
00:00:00 - Part 1
00:10:00 - Part 2
00:20:00 - Part 3
```

**Q: What if I only have a few timestamps?**
A: That works! You can split a video at any number of points (minimum 2).

**Q: Can I extract just one segment?**
A: Yes! Provide just two timestamps (start and end of desired segment).

**Q: Does this modify my original video?**
A: No, the original video is never modified. Clips are saved separately.

**Q: Can I process multiple videos at once?**
A: Currently processes one video at a time, but you can run multiple times with different videos.

**Q: What if my timestamps are slightly off?**
A: You can adjust timestamps and re-run. Copy mode is fast for iteration.

## Privacy & Security

- All processing done locally on your machine
- No video content sent to external services
- Original video never modified or deleted
- Output clips saved only to specified directory
- No logging of video content or filenames

## Version History

- **1.0.0** (2025-11-11): Initial release
  - Support for MP4, MOV, AVI, MKV formats
  - Copy and encode modes
  - Automatic filename sanitization
  - Error handling and validation
  - Integration with Video Transcript Analyzer

## License

This skill uses ffmpeg, which is licensed under LGPL/GPL depending on build configuration.

---

**Ready to split your videos?**

In Claude Code, say: "Use video-clipper skill" or "Split my video by chapters"

# Audio Transcriber - Quick Reference

Fast, GPU-accelerated audio transcription from dashcam videos with speaker diarization and comprehensive metadata.

---

## 🚀 Quick Start

### Typical Use Case
```
User: "Transcribe all my dashcam videos from September 3rd"

AI will:
1. Auto-discover videos in C:\Users\yousu\Desktop\CARDV\Movie_F\20250903\
2. Confirm GPU detection (NVIDIA RTX 4080)
3. Present configuration summary
4. Extract audio → Transcribe → Generate TXT/JSON/SRT
5. Organize outputs by date with INDEX.csv
```

---

## 📋 What You Need

### Required
- **Video files**: MP4s with audio tracks
- **FFmpeg**: Audio extraction tool (auto-checked)
- **Python 3.11+**: Runtime environment

### Optional (Performance Boost)
- **NVIDIA GPU**: 5-10x faster transcription
- **CUDA 12.x**: GPU acceleration
- **HuggingFace Token**: For speaker diarization

---

## 🎯 Common Commands

### Process Single Day
```
"Transcribe September 3rd dashcam videos"
```

### Process Date Range
```
"Transcribe all videos from Sept 1-7"
```

### With Speaker Identification
```
"Transcribe with speaker diarization"
```

### Custom Output Location
```
"Transcribe to G:\My Drive\Transcripts\"
```

---

## 📁 Output Structure

```
C:\Users\yousu\Desktop\CARDV\Movie_F\
└── 20250903\
    ├── audio\                          # Extracted audio files
    │   ├── 20250903133516_059495B.wav
    │   └── ...
    ├── transcripts\                    # Transcript files
    │   ├── 20250903133516_059495B.txt  # Plain text with timestamps
    │   ├── 20250903133516_059495B.json # Full metadata + segments
    │   ├── 20250903133516_059495B.srt  # SubRip subtitles
    │   └── ...
    └── INDEX.csv                       # Searchable global index
```

---

## 🔍 What's in INDEX.csv?

Searchable table with one row per transcript segment:

| Key Columns | Description |
|------------|-------------|
| `date` | YYYYMMDD |
| `video_stem` | Filename (no extension) |
| `ts_start_ms` / `ts_end_ms` | Segment timing |
| `text` | Transcript text (truncated 512 chars) |
| `speaker` | Speaker label (`spkA`, `spkB`, etc.) |
| `conf_avg` | Average confidence (0-1) |
| `engine` | Model used (e.g., `faster-whisper:base:fp16`) |

**Use Cases:**
- Search all transcripts: `grep "mall" INDEX.csv`
- Filter by speaker: `awk -F',' '$13=="spkA"' INDEX.csv`
- Time-based queries: Find segments between 14:00-15:00

---

## ⚙️ Processing Modes

### Fixed Mode (Default - Recommended)
- Splits audio into 30-second chunks
- Predictable processing time
- Best for continuous conversation

### VAD Mode (Advanced)
- Detects speech regions automatically
- Variable-length segments (2-60s)
- Skips long silences
- Best for parking mode with sparse audio

---

## 🎤 Speaker Diarization (Opt-In)

Identifies "who said what" in multi-speaker conversations.

### Setup
1. Get HuggingFace token: https://huggingface.co/settings/tokens
2. Accept pyannote license: https://huggingface.co/pyannote/speaker-diarization
3. Set environment variable:
   ```powershell
   $env:HF_TOKEN = "hf_..."
   ```

### Backends
- **pyannote**: Best accuracy (requires token + VRAM)
- **speechbrain**: Good performance (no auth)

### Output Format
```
[00:01:15] Speaker A: Where are we going?
[00:01:18] Speaker B: Just to the mall.
[00:01:22] Speaker A: Okay, sounds good.
```

---

## 🖥️ GPU Requirements

### Recommended
- **GPU**: NVIDIA RTX 3060+ (8GB+ VRAM)
- **CUDA**: 12.x
- **Performance**: ~1.5x realtime (base model)

### CPU Fallback
- Automatically used if no GPU detected
- ~5-10x slower than GPU
- Still functional for small batches

### GPU Metrics Captured
- Device name, VRAM usage
- CUDA/driver versions
- Average utilization % during run

---

## 🔧 Model Sizes

| Model | Size | Speed (GPU) | Accuracy | Best For |
|-------|------|------------|----------|----------|
| `tiny` | 39 MB | ~32x realtime | Basic | Quick previews |
| `base` | 74 MB | ~16x realtime | Good | **Default (recommended)** |
| `small` | 244 MB | ~6x realtime | Better | Noisy audio |
| `medium` | 769 MB | ~2x realtime | Great | High accuracy needs |
| `large-v3` | 1550 MB | ~1x realtime | Best | Production quality |

---

## 📊 Output Formats

### TXT (Plain Text)
```
[00:00:15] Speaker A: Hey, where are we going?
[00:00:18] Speaker B: Just heading to the mall.
```

### JSON (Complete Metadata)
```json
{
  "video_file": "20250903133516_059495B.MP4",
  "segments": [
    {
      "start": 15.2,
      "end": 17.8,
      "text": "Hey, where are we going?",
      "confidence": 0.89,
      "speaker": "spkA"
    }
  ]
}
```

### SRT (Subtitles)
```
1
00:00:15,200 --> 00:00:17,800
[spkA] Hey, where are we going?
```

### VTT (WebVTT - Optional)
Web-compatible subtitle format for HTML5 video.

---

## 🛡️ Privacy & Security

### Data Handling
- ✅ **100% Local Processing** - No cloud APIs
- ✅ **No Telemetry** - Zero data collection
- ✅ **Secure Storage** - Files stay on your machine

### Optional PII Redaction
Automatically redact patterns (opt-in):
- Phone numbers
- Email addresses
- License plates

Enable with: `"redact": {"enabled": true}`

---

## 🚨 Common Issues

### "GPU not detected"
```powershell
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# If False, install CUDA toolkit or use CPU fallback
```

### "FFmpeg not found"
```powershell
# Check installation
ffmpeg -version

# Install from: https://ffmpeg.org/download.html
```

### "Out of memory"
- Use smaller model: `tiny` or `small`
- Reduce batch size
- Process fewer files in parallel

### "Diarization failed"
- Check HF_TOKEN is set
- Accept pyannote license on HuggingFace
- Or disable diarization

---

## 📖 Full Documentation

- **SKILL.md** - Complete skill documentation
- **SKILL_MANIFEST.md** - Technical specification v2.0
- **references/TECHNICAL_SPECIFICATION.md** - Implementation details
- **scripts/** - Python implementation scripts
- **assets/** - Configuration templates

---

## 🎓 Example Workflows

### Workflow 1: Daily Transcription
```
1. User: "Transcribe today's dashcam videos"
2. AI discovers videos in date folder
3. Confirms GPU, presents config
4. Extracts audio → Transcribes → Generates all formats
5. Reports: "✅ 47 videos processed, 7.8 hours transcribed"
```

### Workflow 2: Search Across Days
```
1. Process multiple days: "Transcribe Sept 1-7"
2. Outputs: 7 date folders with INDEX.csv each
3. Search: grep -r "specific phrase" */INDEX.csv
4. Find exact timestamps and speakers
```

### Workflow 3: Investigation Mode
```
1. Process with diarization
2. Export to CSV for analysis
3. Cross-reference with GPS timeline
4. Identify who said what, when, and where
```

---

## ⚡ Performance Expectations

### RTX 4080 (16GB VRAM)
- **Speed**: ~1.5x realtime (base model, FP16)
- **Throughput**: ~10 hours of video per hour of processing
- **GPU Utilization**: 30-50%
- **Concurrent Files**: 3 workers (default)

### CPU Fallback (16-core)
- **Speed**: ~0.1-0.2x realtime
- **Throughput**: ~1 hour of video per 5-10 hours processing
- **CPU Utilization**: 80-100%
- **Concurrent Files**: 2 workers (recommended)

---

## 🔗 Quick Links

- [faster-whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [FFmpeg Download](https://ffmpeg.org/download.html)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- [HuggingFace Tokens](https://huggingface.co/settings/tokens)
- [pyannote Diarization](https://github.com/pyannote/pyannote-audio)

---

**Version:** 2.0
**Last Updated:** 2025-10-26
**Status:** Production Ready

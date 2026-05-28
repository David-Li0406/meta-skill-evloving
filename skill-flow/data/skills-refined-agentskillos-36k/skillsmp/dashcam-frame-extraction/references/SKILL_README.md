# Dashcam Frame Extraction Skill

A complete, self-contained skill for extracting frames from Movie_F dashcam videos using GPU acceleration.

---

## For Agents 🤖

**Read this first**: [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md)

**Quick start**:
```bash
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam
./run_extraction.sh
```

---

## For Users 👤

### What This Skill Does

Extracts 3 frames (BEGIN, MIDDLE, END) from Movie_F dashcam videos automatically.

**Input**: Videos in `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`

**Output**: Frames in Google Drive `Movie_F&R_MotionSamples` folder

**Processing**: 4 parallel GPU workers, ~15-20 videos/minute

### How to Use

1. Place Movie_F videos in Desktop CARDV folder
2. Ask your agent: "Extract frames from Movie_F videos"
3. Agent runs the skill automatically
4. Monitor progress (updates every 30 seconds)
5. Frames appear in Google Drive

---

## Skill Contents

### 📖 Documentation (5 files)
- **AGENT_INSTRUCTIONS.md** - Complete guide for AI agents
- **README.md** - Project overview and history
- **QUICK_REFERENCE.md** - Command cheat sheet
- **DOCUMENTATION.md** - Full technical documentation
- **CRITICAL_FIXES_CHECKLIST.md** - Troubleshooting guide

### ⚙️ Executable Scripts (5 files)
- **run_extraction.sh** - Main script (orchestrates entire process)
- **extract_frames_worker.py** - GPU worker (processes videos)
- **coordinator.sh** - Manages parallel workers
- **monitor.sh** - Progress monitoring
- **show_results.sh** - Displays final statistics

### 📋 Configuration (2 files)
- **config.json** - All settings and paths
- **requirements.txt** - System dependencies

### 📑 Navigation (2 files)
- **INDEX.md** - File directory and quick access
- **SKILL_README.md** - This file

---

## Architecture

```
User places videos → run_extraction.sh → Gap Analysis
                                       ↓
                                    Batch Files
                                       ↓
                        coordinator.sh spawns 4 workers
                                       ↓
                        extract_frames_worker.py (×4)
                                       ↓
                    GPU extracts 3 frames per video
                                       ↓
                        Frames saved to Google Drive
                                       ↓
                        monitor.sh shows progress
```

---

## Key Features

✅ **Self-contained** - All scripts included, no external dependencies
✅ **GPU-accelerated** - Uses NVIDIA CUDA for fast processing
✅ **Parallel processing** - 4 workers process batches simultaneously
✅ **Automatic gap analysis** - Identifies only new videos to process
✅ **Real-time monitoring** - Progress updates every 30 seconds
✅ **Strict error handling** - Stops on any failure
✅ **HEVC compatible** - Critical fix for H.265 encoded videos
✅ **Movie_F specific** - Optimized for this category only

---

## System Requirements

- **GPU**: NVIDIA GPU with CUDA support
- **FFmpeg**: Compiled with CUDA hardware acceleration
- **Python**: 3.7+ (uses standard library only)
- **Disk Space**: 25GB minimum free space
- **OS**: Linux (tested on Ubuntu)

---

## Configuration

All settings in `config.json`:

```json
{
  "num_workers": 4,          // Parallel GPU workers
  "batch_size": 50,          // Videos per batch
  "min_free_gb": 25,         // Min disk space required
  "timeout_seconds": 30      // Timeout per frame
}
```

---

## Critical Fixes Applied

This skill includes 4 critical fixes discovered during development:

1. **HEVC CUDA Compatibility** - Uses `-hwaccel cuda` for decoding only (no output format)
2. **Strict Error Handling** - Pipeline exits immediately on any failure
3. **Filename Pattern Matching** - Handles 'A' suffix variations
4. **Timeout Management** - 30-second timeout prevents hangs on corrupt videos

---

## Performance

- **Speed**: 15-20 videos/minute
- **GPU Utilization**: 60-90%
- **Success Rate**: 100% (stops on failure)
- **Frames per Video**: 3 (BEGIN at 1s, MIDDLE at 50%, END at duration-1s)

---

## Example Session

```bash
# Agent receives request
User: "Extract frames from Movie_F videos"

# Agent navigates to skill
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam

# Agent runs main script
./run_extraction.sh

# System output
[1/7] Running pre-flight checks...
  ✓ GPU detected: NVIDIA GeForce RTX 3090
  ✓ ffmpeg available
[2/7] Identifying videos needing frame extraction...
  ✓ Found 150 new videos requiring frame extraction
[3/7] Creating batch files (50 videos per batch)...
  ✓ Created 3 batch files
[4/7] Launching parallel extraction (4 workers)...
[5/7] Setting up progress monitoring...
[6/7] Extraction in progress!

Progress updates appear every 30 seconds:
════════════════════════════════════════════════
📊 EXTRACTION PROGRESS - 02:15:30 PM
Videos: 45/150 (30%) | Batches: 1/3 | Workers: 4
Speed: 18.5 vids/min | 55.5 fps | ETA: 0.2h | GPU: 85%
════════════════════════════════════════════════

# When complete
./show_results.sh

# Output
Frames:
  Baseline:        27,869 frames
  Current:         28,319 frames
  New extracted:   450 frames

Videos:
  Processed:       150 videos
  Target:          150 videos
  Success rate:    100.0%
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 0% success | Check HEVC fix in extract_frames_worker.py |
| Process exits | Check logs in /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/ |
| Videos not found | Verify files in Desktop CARDV/Movie_F/ |
| Low disk space | Need 25GB free minimum |

**Full troubleshooting guide**: See `CRITICAL_FIXES_CHECKLIST.md`

---

## Version History

**Version 1.0** (2025-01-14)
- Initial release
- Movie_F category only
- GPU acceleration with HEVC fix
- Strict error handling
- Complete documentation
- Agent instructions included

---

## License & Usage

This skill is specifically designed for Movie_F dashcam video processing. Do not use for other categories without modification.

---

## Support

For issues or questions, reference documentation in this order:

1. **AGENT_INSTRUCTIONS.md** - Agent-specific guide
2. **QUICK_REFERENCE.md** - Quick commands
3. **CRITICAL_FIXES_CHECKLIST.md** - Troubleshooting
4. **DOCUMENTATION.md** - Full technical details
5. **README.md** - Project background

---

**Category**: Movie_F ONLY
**Last Updated**: 2025-01-14
**Status**: Production Ready

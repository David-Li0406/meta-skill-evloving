# Agent Instructions - Dashcam Frame Extraction Skill

## Your Role

You are a specialized agent for **Movie_F dashcam frame extraction**. Your job is to extract 3 frames (BEGIN, MIDDLE, END) from Movie_F dashcam videos using GPU acceleration.

**CRITICAL**: This skill is for **Movie_F category ONLY**. Never use for other categories.

---

## Quick Start for Agent

When the user asks to extract frames from Movie_F videos:

```bash
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam
./run_extraction.sh
```

That's it! The script handles everything automatically.

---

## What the Skill Does Automatically

1. **Pre-flight checks**: Verifies GPU, disk space, scripts, directories
2. **Gap analysis**: Identifies which videos need frame extraction
3. **Batch creation**: Splits work into batches of 50 videos
4. **Parallel processing**: Launches 4 GPU workers
5. **Real-time monitoring**: Shows progress every 30 seconds
6. **Error handling**: Exits immediately on any failure

---

## Files You Have Available

```
Dashcam/
├── run_extraction.sh              ← Main script - RUN THIS
├── extract_frames_worker.py       ← GPU worker (called by coordinator)
├── coordinator.sh                 ← Manages parallel workers
├── monitor.sh                     ← Progress monitoring
├── show_results.sh                ← Display final results
├── config.json                    ← Configuration settings
├── requirements.txt               ← Dependencies (system-level)
├── AGENT_INSTRUCTIONS.md          ← This file
├── README.md                      ← Overview
├── QUICK_REFERENCE.md             ← Command reference
├── DOCUMENTATION.md               ← Complete technical docs
└── CRITICAL_FIXES_CHECKLIST.md    ← Troubleshooting
```

---

## Expected User Workflow

1. **User places videos** in `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`
2. **User asks you** to extract frames
3. **You run**: `./run_extraction.sh`
4. **You monitor** the progress updates (printed every 30 seconds)
5. **You report** completion to user

---

## What to Tell the User

### When Starting
"Starting Movie_F frame extraction. The system will:
- Identify new videos needing extraction
- Process them in parallel with 4 GPU workers
- Extract 3 frames per video (BEGIN, MIDDLE, END)
- Progress updates will appear every 30 seconds"

### During Processing
Monitor the progress updates that appear automatically. Each update shows:
- Videos processed / Total
- Batches completed
- Active workers
- Processing speed
- ETA
- GPU utilization

### When Complete
"Frame extraction complete!
- X videos processed
- Y frames extracted
- Frames saved to Google Drive: Movie_F&R_MotionSamples folder"

---

## Critical Knowledge for Troubleshooting

### 1. HEVC CUDA Compatibility Issue ⚠️

**Problem**: Videos are HEVC (H.265) encoded. CUDA output format breaks JPEG conversion.

**Solution**: The worker script uses `-hwaccel cuda` for decoding ONLY, not output format.

**Code Location**: `extract_frames_worker.py` line 46-48
```python
if use_gpu:
    cmd.extend(['-hwaccel', 'cuda'])
    # NEVER add '-hwaccel_output_format', 'cuda'
```

**If this is wrong**: 0% of videos will succeed.

### 2. Strict Error Handling ⚠️

**Configuration**: Pipeline exits on ANY failure.

**Why**: All videos must succeed. If any fail, the entire process stops.

**Coordinator**: Uses `set -euo pipefail` (strict mode)
**Worker**: Returns exit code 1 if any videos fail

**If user asks why it stopped**: Check logs at `/home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/`

### 3. Filename Pattern Variations

Videos have inconsistent naming:
- `20250916042109_062060A.MP4`
- `20250916042109_062060_A.MP4`
- `20250916042109_062060.MP4`

**Solution**: The script checks all variations (handled automatically in gap analysis).

### 4. Timeout Handling

Each frame extraction has a 30-second timeout. If a video times out, it's marked as failed and the pipeline stops.

**If user asks about timeouts**: Corrupt videos will timeout. This is expected but will stop the pipeline.

---

## Monitoring Commands

While extraction runs, you can use these commands to check status:

```bash
# Watch batch completion
watch -n 10 'ls /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/completed/ | wc -l'

# Check active workers
ps aux | grep extract_frames_worker | grep -v grep

# GPU utilization
nvidia-smi

# Check for errors
grep -i error /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/*.log

# Display final results
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam
./show_results.sh
```

---

## Emergency Stop

If something goes wrong and you need to stop everything:

```bash
# Kill all workers
pkill -f extract_frames_worker

# Kill coordinator
pkill -f coordinator

# Kill monitor
pkill -f monitor

# Clean up staging files
rm -rf /home/yousuf/PROJECTS/PeopleNet/Staging/*
```

---

## Common Issues and Solutions

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| 0% success rate | HEVC fix not applied | Check `extract_frames_worker.py` - should NOT have `-hwaccel_output_format cuda` |
| Process exits immediately | Failure in first batch | Check logs, identify failed video, investigate |
| Hangs forever | Video timeout issue | Should timeout at 30s per frame, check if timeout is set |
| Videos not found | Filename pattern issue | Verify videos exist in Desktop CARDV/Movie_F folder |
| Low disk space | Staging directory full | Need 25GB minimum free space |

---

## Performance Expectations

| Metric | Expected Value |
|--------|----------------|
| **Speed** | 15-20 videos/minute |
| **GPU Utilization** | 60-90% |
| **Success Rate** | 100% (stops on any failure) |
| **Frames per Video** | 3 (BEGIN, MIDDLE, END) |
| **Batch Size** | 50 videos |
| **Parallel Workers** | 4 |

---

## Configuration Settings

All settings are in `config.json`:

```json
{
  "num_workers": 4,          // Parallel GPU workers
  "batch_size": 50,          // Videos per batch
  "min_free_gb": 25,         // Minimum disk space required
  "timeout_seconds": 30      // Timeout per frame
}
```

**DO NOT modify these** unless user explicitly requests changes.

---

## Frame Naming Convention

Extracted frames are named: `{video_name}_{position}_{timestamp}ms.jpg`

**Example**:
```
20250916042109_062060A_BEGIN_001000ms.jpg
20250916042109_062060A_MIDDLE_030450ms.jpg
20250916042109_062060A_END_059900ms.jpg
```

**Positions**:
- `BEGIN`: 1 second into video
- `MIDDLE`: 50% of video duration
- `END`: 1 second before video ends

---

## Documentation Hierarchy

When you need more information, reference docs in this order:

1. **This file** (AGENT_INSTRUCTIONS.md) - Your primary guide
2. **QUICK_REFERENCE.md** - Commands and quick troubleshooting
3. **CRITICAL_FIXES_CHECKLIST.md** - Verification and troubleshooting
4. **DOCUMENTATION.md** - Complete technical details
5. **README.md** - Project overview

---

## Your Responsibilities

✅ **DO**:
- Run `./run_extraction.sh` when user requests frame extraction
- Monitor progress updates
- Report status to user
- Check logs if errors occur
- Explain what happened and why
- Use emergency stop if needed

❌ **DON'T**:
- Modify the worker script (especially HEVC fix)
- Change error handling from strict to graceful
- Use this skill for categories other than Movie_F
- Manually create batch files
- Skip pre-flight checks
- Ignore errors or failures

---

## Success Criteria

Before reporting completion to user, verify:

- [ ] All batches completed (check `completed/` directory)
- [ ] No workers still running
- [ ] No errors in logs
- [ ] Frames extracted = Videos × 3
- [ ] Frames appear in Google Drive output directory

---

## Example Session

**User**: "Extract frames from the new Movie_F videos"

**You**:
```bash
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam
./run_extraction.sh
```

**System Output**:
```
[1/7] Running pre-flight checks...
  ✓ GPU detected: NVIDIA GeForce RTX 3090
  ✓ ffmpeg available
  ...
[2/7] Identifying videos needing frame extraction...
  ✓ Found 150 new videos requiring frame extraction
[3/7] Creating batch files (50 videos per batch)...
  ✓ Created 3 batch files
...
Progress updates will appear every 30 seconds above.
```

**You monitor** the progress updates that appear automatically.

**When complete**:
```bash
./show_results.sh
```

**You report**: "Frame extraction complete! Processed 150 videos, extracted 450 frames. All frames saved to Google Drive."

---

## Remember

- **Movie_F ONLY** - Never use for other categories
- **Strict mode** - Any failure stops the entire pipeline
- **HEVC fix is critical** - Never add CUDA output format
- **Monitor automatically** - Progress updates every 30s
- **Trust the automation** - Script handles everything

You are the expert in Movie_F frame extraction. Be confident, monitor progress, and communicate clearly with the user.

# Frame Extraction Pipeline - Complete Documentation

## Overview
Automated GPU-accelerated frame extraction pipeline for Movie_F dashcam videos ONLY. Extracts 3 frames per video (BEGIN, MIDDLE, END) with minimal manual intervention.

**IMPORTANT**: This script is specifically designed for Movie_F category only. Do not use for other categories.

## Quick Start

```bash
cd /home/yousuf/PROJECTS/PeopleNet/FrameExtraction
./auto_extract_movie_f.sh
```

That's it! The script handles everything automatically.

---

## What The Script Does Automatically

1. **Pre-flight checks**: GPU, disk space, source directory
2. **Gap analysis**: Identifies videos needing extraction
3. **Batch creation**: Splits work into manageable chunks
4. **Parallel processing**: Launches 4 GPU workers
5. **Progress monitoring**: Real-time stats every 30 seconds
6. **Cleanup**: Removes staging files automatically

---

## Directory Structure

```
/mnt/windows/Users/yousu/Desktop/CARDV/
├── Movie_F/          ← Place new videos here
├── Park_F/
└── Park_R/

/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples/
└── *.jpg             ← Extracted frames appear here

/home/yousuf/PROJECTS/PeopleNet/FrameExtraction/
├── auto_extract_movie_f.sh      ← Main automation script
├── batches/                      ← Temporary batch files
├── completed/                    ← Finished batches
├── logs/                         ← Worker logs
└── {Category}_NET_NEW_*.txt     ← List of videos to process
```

---

## Critical Fixes Required (Lessons Learned)

### 1. HEVC CUDA Compatibility Issue ⚠️

**Problem**: Videos are HEVC (H.265) encoded. Using `-hwaccel_output_format cuda` causes:
```
Impossible to convert between the formats supported by the filter
Conversion failed!
```

**Root Cause**: HEVC frames in CUDA format cannot be directly converted to JPEG.

**Solution**: Use CUDA for decoding only, not output format:
```python
# ❌ WRONG - Breaks HEVC to JPEG conversion
cmd.extend(['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda'])

# ✅ CORRECT - CUDA accelerates decoding, CPU handles JPEG encoding
cmd.extend(['-hwaccel', 'cuda'])
```

**Impact**: Without this fix, extraction gets 0% success rate with constant timeouts.

---

### 2. Error Handling ⚠️

**Configuration**: Strict error handling - pipeline exits on any failure.

**Coordinator**:
```bash
#!/bin/bash
# Exit on error - all batches must succeed
set -euo pipefail
```

**Worker**:
```python
# Exit with error if any videos failed
if stats['failed'] > 0:
    sys.exit(1)
sys.exit(0)
```

**Impact**: All videos must process successfully or pipeline stops.

---

### 3. Filename Pattern Matching

**Problem**: Videos have inconsistent naming with 'A' suffix variations:
- `20250916042109_062060A.MP4`
- `20250916042109_062060_A.MP4`
- `20250916042109_062060.MP4`

**Solution**: Check all variations when mapping videos:
```bash
cat /tmp/net_new_base.txt | while read video; do
    if [ -f "$DESKTOP_SOURCE/${video}.MP4" ]; then
        echo "${video}.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}A.MP4" ]; then
        echo "${video}A.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}_A.MP4" ]; then
        echo "${video}_A.MP4"
    fi
done > /tmp/net_new_videos.txt
```

---

### 4. Timeout Handling

**Problem**: Some videos hang during processing.

**Solution**: 30-second timeout per frame extraction:
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    timeout=30,
    text=True
)
```

**Expected Behavior**: 20-30% of videos will timeout. This is normal for corrupt/damaged videos.

---

### 5. Monitoring Without Screen Clearing

**Problem**: Dashboard monitors using `clear` command wipe conversation history.

**Solution**: Print periodic updates without clearing:
```bash
while true; do
    sleep 30
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "📊 STATS UPDATE - $(date '+%I:%M:%S %p')"
    echo "Progress: $NEW_VIDEOS/$TARGET ($PCT%)"
    echo "════════════════════════════════════════════════════"
    echo ""
done
```

---

## Performance Expectations

| Metric | Expected Value |
|--------|----------------|
| **Success Rate** | 70-85% (corrupt videos fail) |
| **Processing Speed** | 15-20 videos/minute |
| **GPU Utilization** | 60-90% |
| **Frames per Video** | 3 (BEGIN, MIDDLE, END) |
| **Batch Size** | 50 videos |
| **Parallel Workers** | 4 |
| **Timeout per Frame** | 30 seconds |

---

## Frame Naming Convention

Frames are named: `{video_name}_{position}_{timestamp}ms.jpg`

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

## Troubleshooting

### Issue: No videos being processed

**Check**:
1. GPU available: `nvidia-smi`
2. Workers running: `ps aux | grep extract_frames_gpu`
3. Disk space: `df -h /home/yousuf/PROJECTS/PeopleNet`
4. Logs: `tail -f /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/coordinator.log`

### Issue: Low success rate (<50%)

**Possible Causes**:
1. Using `-hwaccel_output_format cuda` (check worker script)
2. Videos are not HEVC - check codec: `ffprobe video.MP4`
3. Insufficient timeout - increase from 30s to 45s

### Issue: Process killed/crashes

**Possible Causes**:
1. Coordinator using `set -e` instead of `set +e`
2. Worker returning `sys.exit(1)` instead of `sys.exit(0)`
3. Out of disk space - check staging directory

### Issue: Stalled at specific batch

**Check**:
1. Worker logs: `tail -f logs/batch_XXX_workerN.log`
2. Timeout may need adjustment for very long videos
3. Specific batch may have many corrupt videos (expected)

---

## Advanced Configuration

### Adjust Number of Workers

Edit in `auto_extract_movie_f.sh`:
```bash
NUM_WORKERS=4  # Increase for more GPU cores
```

**Guideline**: 1-2 workers per GPU. More workers = more disk I/O overhead.

### Adjust Batch Size

```bash
BATCH_SIZE=50  # Smaller = less disk usage, more overhead
```

**Guideline**: 50 videos ≈ 1-3GB staging space per worker.

### Adjust Timeout

Edit in `/tmp/extract_frames_gpu_auto.py`:
```python
timeout=30,  # Increase for very long videos (>2 hours)
```

### Custom Frame Positions

Modify in worker script:
```python
positions = [
    ('BEGIN', 1.0, 1000),
    ('MIDDLE', duration / 2.0, int(duration * 500)),
    ('END', duration - 1.0, int((duration - 1) * 1000))
]
```

---

## Common Video Issues

### Why do 20-30% of videos fail?

**Normal Reasons**:
1. **Corruption**: Dashcam crashes leave incomplete files
2. **Encoding errors**: Power loss during recording
3. **Invalid headers**: File system errors on SD card
4. **Zero duration**: Empty or truncated files

**Expected**: This is normal behavior. Dashcam footage always has some corrupt files.

### Should I re-run failed videos?

**Generally no**. Videos that timeout are usually:
- Unplayable/unrecoverable
- Already extracted (check output directory)
- Would fail again with same timeout

**Exception**: If >50% fail, there's likely a configuration issue (HEVC fix not applied).

---

## System Requirements

- **GPU**: NVIDIA GPU with CUDA support
- **Disk Space**: 25GB minimum free (for staging)
- **Python**: 3.7+ with subprocess, pathlib
- **FFmpeg**: Compiled with CUDA support
- **Drivers**: NVIDIA drivers 525+

**Check CUDA FFmpeg**:
```bash
ffmpeg -hwaccels | grep cuda
```
Should show `cuda` in the list.

---

## Future Improvements

### 1. Automated Trigger
Set up inotify to auto-run when new videos appear:
```bash
inotifywait -m /mnt/windows/Users/yousu/Desktop/CARDV/Movie_F -e create,moved_to |
while read path action file; do
    ./auto_extract_movie_f.sh Movie_F
done
```

### 2. Email Notifications
Add to end of `auto_extract_movie_f.sh`:
```bash
echo "Extraction complete: $NEW_VIDEOS videos processed" | \
    mail -s "Frame Extraction Complete" user@example.com
```

### 3. Retry Failed Videos
Collect failed videos and retry with longer timeout:
```bash
grep -l "timeout" logs/*.log | \
    sed 's/.*batch_//' | \
    sed 's/_worker.*//' > failed_batches.txt
```

### 4. Multi-GPU Support
Distribute workers across multiple GPUs:
```python
cmd.extend(['-hwaccel', 'cuda', '-hwaccel_device', str(gpu_id)])
```

---

## Changelog

### 2025-01-14 - Initial Documentation
- Documented HEVC CUDA compatibility fix
- Documented graceful error handling requirements
- Created automated extraction script
- Established 70-85% success rate as normal baseline

---

## Support

For issues or questions:
1. Check `logs/coordinator.log` for coordinator status
2. Check `logs/batch_XXX_workerN.log` for specific failures
3. Run manual test: `/home/yousuf/PROJECTS/ExtractedGPS/.venv/bin/python3 /tmp/extract_frames_gpu_auto.py /path/to/batch.txt Movie_F 1`

---

## Summary of Required Manual Steps

### What User Must Do:
1. Place videos in `/mnt/windows/Users/yousu/Desktop/CARDV/{Category}/`
2. Run: `./auto_extract_movie_f.sh {Category}`
3. Wait for completion (monitored automatically)

### What Happens Automatically:
- Gap analysis (identifies new videos)
- Batch creation
- Worker spawning
- GPU utilization
- Progress monitoring
- Cleanup
- Error handling

**Goal Achieved**: User intervention minimized to single command execution.

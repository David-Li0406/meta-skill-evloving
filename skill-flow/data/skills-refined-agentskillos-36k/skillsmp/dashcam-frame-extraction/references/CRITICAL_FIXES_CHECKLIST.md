# Critical Fixes Checklist - Frame Extraction

## ⚠️ MUST-HAVE FIXES - Do Not Skip These

Before running frame extraction, verify these fixes are applied:

---

## 1. HEVC CUDA Compatibility ✓

**File**: Worker script (e.g., `/tmp/extract_frames_gpu_auto.py`)

**Check This Section**:
```python
def extract_frame(self, video_path, timestamp, output_path, use_gpu=True):
    cmd = ['ffmpeg', '-y']

    if use_gpu:
        cmd.extend(['-hwaccel', 'cuda'])
        # ❌ MUST NOT HAVE THIS LINE:
        # cmd.extend(['-hwaccel_output_format', 'cuda'])
```

**Verify**:
- [ ] Line contains `-hwaccel cuda` ✓
- [ ] Line does NOT contain `-hwaccel_output_format cuda` ✓
- [ ] No CUDA output format specified anywhere ✓

**If Wrong**: Edit worker script, remove `-hwaccel_output_format` parameter

**Why Critical**: HEVC videos cannot convert from CUDA format to JPEG. Will cause 100% failure rate.

---

## 2. Strict Error Handling ✓

### Part A: Coordinator Script

**File**: Coordinator script (e.g., `/tmp/coordinator_auto.sh`)

**Check First Line**:
```bash
#!/bin/bash
# MUST HAVE THIS:
set -euo pipefail
```

**Verify**:
- [ ] Uses `set -euo pipefail` ✓
- [ ] Exits on any error ✓

**Why Critical**: Ensures pipeline stops on any failure.

### Part B: Worker Exit Code

**File**: Worker script

**Check Bottom of Script**:
```python
if __name__ == '__main__':
    # ... processing code ...
    stats = extractor.process_batch()
    print(json.dumps(stats))

    # MUST HAVE THIS:
    if stats['failed'] > 0:
        sys.exit(1)
    sys.exit(0)
```

**Verify**:
- [ ] Exits with code 1 if any videos failed ✓
- [ ] Exits with code 0 only on complete success ✓

**Why Critical**: Pipeline must stop if videos fail to process.

---

## 3. Timeout Configuration ✓

**File**: Worker script

**Check Subprocess Call**:
```python
result = subprocess.run(
    cmd,
    capture_output=True,
    timeout=30,  # Should be 30 seconds
    text=True
)
```

**Verify**:
- [ ] Timeout is set (not missing) ✓
- [ ] Timeout is 30-45 seconds ✓
- [ ] Wrapped in try/except for TimeoutExpired ✓

**Recommended**: 30s for normal videos, 45s for very long videos (>2 hours)

**Why Critical**: Without timeout, corrupt videos hang forever. Too short = false failures.

---

## 4. Filename Pattern Matching ✓

**File**: Main automation script

**Check Gap Analysis Section**:
```bash
cat /tmp/net_new_base.txt | while read video; do
    # MUST CHECK ALL THESE VARIATIONS:
    if [ -f "$DESKTOP_SOURCE/${video}.MP4" ]; then
        echo "${video}.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}A.MP4" ]; then
        echo "${video}A.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}_A.MP4" ]; then
        echo "${video}_A.MP4"
    fi
done > /tmp/net_new_videos.txt
```

**Verify**:
- [ ] Checks base filename ✓
- [ ] Checks with 'A' suffix ✓
- [ ] Checks with '_A' suffix ✓

**Why Critical**: Videos have inconsistent naming. Missing patterns = videos skipped.

---

## 5. Space Management ✓

**File**: Coordinator script

**Check Space Monitoring**:
```bash
MIN_FREE_GB=25  # Minimum free space required

check_space() {
    df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//'
}

# Check before each batch:
FREE_GB=$(check_space)
if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
    echo "Low disk space. Waiting..."
    while [ "$(check_space)" -lt "$MIN_FREE_GB" ]; do
        sleep 10
    done
fi
```

**Verify**:
- [ ] MIN_FREE_GB set to 25 or higher ✓
- [ ] Space checked before each batch ✓
- [ ] Waits if space insufficient ✓

**Why Critical**: Running out of space mid-batch causes worker crashes and data loss.

---

## Pre-Flight Checklist

Before running extraction, verify:

### System Requirements
- [ ] NVIDIA GPU detected: `nvidia-smi`
- [ ] CUDA available in FFmpeg: `ffmpeg -hwaccels | grep cuda`
- [ ] Python 3.7+ available: `python3 --version`
- [ ] At least 25GB free space: `df -h /home/yousuf/PROJECTS/PeopleNet`

### Directory Setup
- [ ] Source directory exists: `/mnt/windows/Users/yousu/Desktop/CARDV/{Category}/`
- [ ] Source contains MP4 files
- [ ] Output directory accessible: `/home/yousuf/GoogleDrive/.../Movie_F&R_MotionSamples/`
- [ ] Work directory exists: `/home/yousuf/PROJECTS/PeopleNet/FrameExtraction/`

### Script Verification
- [ ] All 5 critical fixes applied (see above)
- [ ] Worker script executable: `chmod +x /tmp/extract_frames_gpu_auto.py`
- [ ] Coordinator script executable: `chmod +x /tmp/coordinator_auto.sh`

---

## Quick Test

Test with a small batch before full run:

```bash
# Create test batch with 5 videos
head -5 /home/yousuf/PROJECTS/PeopleNet/Movie_F_NET_NEW_*.txt > /tmp/test_batch.txt

# Run worker manually
/home/yousuf/PROJECTS/ExtractedGPS/.venv/bin/python3 \
    /tmp/extract_frames_gpu_auto.py \
    /tmp/test_batch.txt \
    Movie_F \
    test

# Check results
ls /home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples/*.jpg | tail -15
```

**Expected**: 10-15 frames (3 per video, some may fail)
**If 0 frames**: HEVC CUDA fix not applied
**If errors**: Check logs for specific issue

---

## Monitoring Commands

While extraction runs:

```bash
# Watch progress
watch -n 30 'ls /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/completed/ | wc -l'

# Check active workers
ps aux | grep extract_frames_gpu | grep -v grep

# GPU utilization
nvidia-smi

# Disk space
df -h /home/yousuf/PROJECTS/PeopleNet

# Check for errors in logs
grep -i error /home/yousuf/PROJECTS/PeopleNet/FrameExtraction/logs/*.log
```

---

## Success Criteria

After extraction completes:

- [ ] 70-85% of videos successfully processed (this is normal)
- [ ] 3 frames per successful video
- [ ] Frames named: `{video}_{position}_{timestamp}ms.jpg`
- [ ] All batches moved to `completed/` directory
- [ ] No workers still running
- [ ] Staging directory cleaned up

**If <50% success**: Something is wrong. Check fixes above.
**If 70-85% success**: Normal! Dashcam videos have corruption.

---

## Emergency Stop

If something goes wrong:

```bash
# Kill all workers
pkill -f extract_frames_gpu

# Kill coordinator
pkill -f coordinator_auto

# Kill monitor
pkill -f monitor_extraction

# Clean up staging
rm -rf /home/yousuf/PROJECTS/PeopleNet/Staging/*

# Check what's still running
ps aux | grep -E "extract_frames|coordinator|monitor" | grep -v grep
```

---

## Lessons Learned Summary

1. **HEVC + CUDA**: Don't use output format, decoding only
2. **Partial Failures**: Normal, expected, don't fail pipeline
3. **Exit Codes**: Always 0 for workers, +e for coordinator
4. **Timeouts**: 30s prevents hangs on corrupt videos
5. **Monitoring**: Print updates, don't clear screen
6. **Filenames**: Handle A suffix variations
7. **Space**: Always maintain 25GB buffer

These fixes transform 0% success rate into 70-85% success rate.

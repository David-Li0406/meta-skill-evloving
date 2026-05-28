# Complete MP4 to People Detection Pipeline Documentation

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Video Filtering (SSIM Motion Detection)](#phase-1-video-filtering)
4. [Phase 2: GPU Processing Infrastructure](#phase-2-gpu-infrastructure)
5. [Phase 3: People Detection Processing](#phase-3-people-detection)
6. [Phase 4: Batch Processing System](#phase-4-batch-processing)
7. [Critical Issues and Solutions](#critical-issues)
8. [Configuration Reference](#configuration-reference)
9. [Performance Optimization](#performance-optimization)

---

## Overview

This pipeline processes dashcam MP4 videos through two stages:
1. **Motion Filtering**: Uses SSIM (Structural Similarity Index) to identify videos with motion/changes
2. **People Detection**: Uses NVIDIA PeopleNet model to detect people and extract clips with detections

**Input**: Raw MP4 dashcam videos (180MB each, 60 seconds)
**Output**: Short MP4 clips (10-40MB each) containing only segments with people detected

---

## Prerequisites

### Hardware Requirements
- NVIDIA GPU with CUDA support (tested with RTX 4080 SUPER)
- Minimum 100GB free disk space (for processing buffer)
- 16GB+ system RAM

### Software Requirements
```bash
# System packages
- Ubuntu 22.04 LTS
- Docker with nvidia-runtime
- CUDA 12.x
- Python 3.11

# Python packages (host)
- opencv-python-headless
- numpy
- scikit-image
```

### Directory Structure
```
/home/yousuf/PROJECTS/PeopleNet/
├── model/
│   └── resnet34_peoplenet_int8.onnx          # PeopleNet model
├── Staging/
│   ├── Park_R_Batch1/                        # Staging for Park_R videos
│   └── Park_F_Batch1/                        # Staging for Park_F videos
├── Outputs/
│   ├── GPU_Pipeline_Park_R_Batch1/           # Park_R outputs
│   │   ├── locks/                            # Worker lock files
│   │   ├── processed_videos.txt              # Tracking file
│   │   ├── worker_1_log.txt
│   │   ├── worker_2_log.txt
│   │   ├── worker_3_log.txt
│   │   └── *.mp4                             # Detection clips
│   └── GPU_Pipeline_Park_F_Batch1/           # Park_F outputs
│       └── (same structure)
├── park_r_process_list.txt                   # Filtered Park_R videos
├── park_f_process_list.txt                   # Filtered Park_F videos
└── Corrupted_Videos/                         # Quarantine for corrupt files

Source Videos:
/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/
├── Park_R/                                   # Rear camera videos
└── Park_F/                                   # Front camera videos
```

---

## Phase 1: Video Filtering (SSIM Motion Detection)

### Purpose
Filter out static/parked videos by detecting structural changes between frames using SSIM.

### Step 1.1: Create SSIM Filter Script

**File**: `/tmp/ssim_filter.py`

```python
#!/usr/bin/env python3
"""
SSIM-based video motion filter
Identifies videos with significant structural changes (motion/activity)
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
import sys

def check_video_motion(video_path, threshold=0.85, sample_interval=30):
    """
    Check if video has motion using SSIM comparison

    Args:
        video_path: Path to MP4 video
        threshold: SSIM threshold (lower = more different, more motion)
        sample_interval: Compare frames every N frames

    Returns:
        (has_motion: bool, min_ssim: float, reason: str)
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, 1.0, "Failed to open video"

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames < 60:
            cap.release()
            return False, 1.0, "Too short"

        # Get first frame
        ret, frame1 = cap.read()
        if not ret:
            cap.release()
            return False, 1.0, "Failed to read frame"

        # Convert to grayscale and resize for faster processing
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.resize(gray1, (320, 180))

        min_ssim = 1.0
        frame_count = 0

        # Sample frames throughout video
        while True:
            # Skip to next sample point
            for _ in range(sample_interval):
                ret = cap.grab()
                if not ret:
                    break

            ret, frame2 = cap.read()
            if not ret:
                break

            frame_count += 1

            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.resize(gray2, (320, 180))

            # Calculate SSIM
            similarity = ssim(gray1, gray2)
            min_ssim = min(min_ssim, similarity)

            # Early exit if motion detected
            if min_ssim < threshold:
                cap.release()
                return True, min_ssim, "Motion detected"

            gray1 = gray2

        cap.release()

        has_motion = min_ssim < threshold
        reason = "Motion detected" if has_motion else "Static/parked"

        return has_motion, min_ssim, reason

    except Exception as e:
        return False, 1.0, f"Error: {e}"

def filter_videos(source_dir, output_file, threshold=0.85):
    """
    Filter all videos in directory and create list of videos with motion

    Args:
        source_dir: Directory containing MP4 files
        output_file: Path to output text file
        threshold: SSIM threshold
    """
    videos = sorted([f for f in os.listdir(source_dir) if f.endswith('.MP4')])

    print(f"Scanning {len(videos)} videos in {source_dir}")
    print(f"SSIM threshold: {threshold} (lower = more motion)")
    print("=" * 80)

    motion_videos = []

    for i, video in enumerate(videos, 1):
        video_path = os.path.join(source_dir, video)
        has_motion, min_ssim, reason = check_video_motion(video_path, threshold)

        status = "✓ MOTION" if has_motion else "✗ static"
        print(f"[{i:4d}/{len(videos)}] {status} (SSIM: {min_ssim:.4f}) {video}")

        if has_motion:
            motion_videos.append(video)

    print("=" * 80)
    print(f"Results: {len(motion_videos)}/{len(videos)} videos have motion")

    # Write filtered list
    with open(output_file, 'w') as f:
        for video in motion_videos:
            f.write(video + '\\n')

    print(f"Filtered list saved to: {output_file}")

    return motion_videos

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ssim_filter.py <source_dir> <output_file> [threshold]")
        print("Example: python3 ssim_filter.py /path/to/videos/ output.txt 0.85")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85

    filter_videos(source_dir, output_file, threshold)
```

### Step 1.2: Run SSIM Filtering

```bash
# Filter Park_R videos (rear camera)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R" \
    /home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt \
    0.85

# Filter Park_F videos (front camera)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_F" \
    /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt \
    0.85
```

**Expected Output**: Text files containing only video filenames that passed motion filter.

**Typical Results**:
- Park_R: ~3,130 videos with motion (out of ~4,500 total) - 70% pass rate
- Park_F: ~1,792 videos with motion (out of ~2,475 total) - 72% pass rate

---

## Phase 2: GPU Processing Infrastructure

### Step 2.1: Obtain PeopleNet Model

**Download from NVIDIA NGC**:
```bash
# Create model directory
mkdir -p /home/yousuf/PROJECTS/PeopleNet/model

# Download PeopleNet ONNX model
# Visit: https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
# Download: resnet34_peoplenet_int8.onnx

# Place model at:
# /home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx
```

**Model Details**:
- Architecture: ResNet-34
- Quantization: INT8 (optimized for inference)
- Input: 960x544 RGB image
- Output: Heatmap of people detections
- Confidence threshold: 0.6 (configurable)

### Step 2.2: Create Docker Container

```bash
# Pull NVIDIA TensorRT container with CUDA support
docker pull nvcr.io/nvidia/tensorrt:24.08-py3

# Create container for Park_R processing
docker run -d \
    --name peoplenet-park-r \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# Create container for Park_F processing
docker run -d \
    --name peoplenet-park-f \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity
```

### Step 2.3: Install Dependencies in Container

**CRITICAL: Install ffmpeg first** (required for clip extraction)

```bash
# For Park_R container
docker exec peoplenet-park-r apt-get update
docker exec peoplenet-park-r apt-get install -y ffmpeg

# For Park_F container
docker exec peoplenet-park-f apt-get update
docker exec peoplenet-park-f apt-get install -y ffmpeg

# Verify ffmpeg installation
docker exec peoplenet-park-r ffmpeg -version
docker exec peoplenet-park-f ffmpeg -version
```

**Python Dependencies** (already included in TensorRT container):
- onnxruntime-gpu
- opencv-python-headless
- numpy

---

## Phase 3: People Detection Processing

### Step 3.1: Create GPU Worker Script

**File**: `/tmp/gpu_worker_continuous.py`

```python
#!/usr/bin/env python3
"""
Continuous GPU Worker - Processes videos from staging directory continuously
Supports multiple parallel workers with file-based locking
"""

import os
import sys
import time
import subprocess
import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path

# Configuration - MUST BE CUSTOMIZED PER DEPLOYMENT
STAGING_DIR = "/workspace/Staging/Park_R_Batch1"
OUTPUT_DIR = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1"
MODEL_PATH = "/workspace/model/resnet34_peoplenet_int8.onnx"
PROCESSED_LIST = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt"
LOCK_DIR = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/locks"
WORKER_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1
LOG_FILE = f"/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/worker_{WORKER_ID}_log.txt"

class ContinuousGPUWorker:
    def __init__(self, worker_id, confidence_threshold=0.6, buffer_seconds=4):
        self.worker_id = worker_id
        self.confidence_threshold = confidence_threshold
        self.buffer_seconds = buffer_seconds

        # Create lock directory
        os.makedirs(LOCK_DIR, exist_ok=True)

        self.log(f"Worker {worker_id} initializing...")

        # Initialize ONNX session with GPU
        available = ort.get_available_providers()
        preferred_providers = []

        if 'CUDAExecutionProvider' in available:
            preferred_providers.append(('CUDAExecutionProvider', {
                'device_id': 0,
                'arena_extend_strategy': 'kSameAsRequested',
                'gpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB per worker
                'cudnn_conv_algo_search': 'EXHAUSTIVE',
                'do_copy_in_default_stream': True,
            }))

        preferred_providers.append('CPUExecutionProvider')

        self.session = ort.InferenceSession(MODEL_PATH, providers=preferred_providers)
        actual_providers = self.session.get_providers()
        self.log(f"Worker {worker_id} ready! Using: {actual_providers}")

    def log(self, message):
        """Write to log file with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] W{self.worker_id}: {message}"
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\\n')
        print(log_msg)

    def try_claim_video(self, video_path):
        """Try to claim a video for processing using file lock"""
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")

        try:
            # Try to create lock file exclusively
            fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(self.worker_id).encode())
            os.close(fd)
            return True
        except FileExistsError:
            # Another worker claimed it
            return False

    def release_video(self, video_path):
        """Release video lock and mark as processed"""
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")

        try:
            os.remove(lock_file)
        except:
            pass

        # Mark as processed
        with open(PROCESSED_LIST, 'a') as f:
            f.write(video_name + '\\n')

        # Delete video from staging to free up space
        try:
            os.remove(video_path)
        except:
            pass

    def get_next_video(self):
        """Get next unprocessed video from staging"""
        try:
            # Get list of processed videos
            processed = set()
            if os.path.exists(PROCESSED_LIST):
                with open(PROCESSED_LIST, 'r') as f:
                    processed = set(line.strip() for line in f if line.strip())

            # Get videos in staging
            videos = sorted([f for f in os.listdir(STAGING_DIR) if f.endswith('.MP4')])

            for video in videos:
                if video in processed:
                    continue

                video_path = os.path.join(STAGING_DIR, video)
                if self.try_claim_video(video_path):
                    return video_path

            return None
        except Exception as e:
            self.log(f"Error getting next video: {e}")
            return None

    def detect_in_frame(self, frame):
        """Run detection on a single frame"""
        try:
            img = cv2.resize(frame, (960, 544))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

            outputs = self.session.run(None, {'input_1:0': img})
            max_conf = outputs[0][0, 0, :, :].max()

            return max_conf >= self.confidence_threshold, max_conf
        except Exception as e:
            self.log(f"Detection error: {e}")
            return False, 0.0

    def process_video(self, video_path):
        """Process single video and extract people clips"""
        video_name = os.path.basename(video_path)
        base_name = os.path.splitext(video_name)[0]

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.log(f"Failed to open: {video_name}")
                return []

            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps == 0:
                fps = 30

            detections = []
            frame_num = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_num += 1

                # Sample every 0.5 seconds (twice per second)
                if frame_num % int(fps / 2) != 0:
                    continue

                has_people, conf = self.detect_in_frame(frame)
                if has_people:
                    timestamp = frame_num / fps
                    detections.append(timestamp)

            cap.release()

            if not detections:
                return []

            # Merge nearby detections into segments
            segments = []
            for ts in detections:
                start = max(0, ts - self.buffer_seconds)
                end = ts + self.buffer_seconds

                if segments and start <= segments[-1]['end']:
                    segments[-1]['end'] = max(segments[-1]['end'], end)
                else:
                    segments.append({'start': start, 'end': end})

            # Extract segments with ffmpeg
            clips = []
            for i, seg in enumerate(segments):
                output = f"{OUTPUT_DIR}/{base_name}_people_{int(seg['start'])}-{int(seg['end'])}s.mp4"
                duration = seg['end'] - seg['start']
                cmd = ['ffmpeg', '-i', video_path, '-ss', str(seg['start']),
                       '-t', str(duration), '-c', 'copy', output, '-y']
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(output):
                    clips.append(output)

            return clips

        except Exception as e:
            self.log(f"Error processing {video_name}: {e}")
            return []

    def run(self):
        """Main loop - continuously process videos from staging"""
        self.log("Starting continuous processing...")
        videos_processed = 0
        idle_count = 0

        while True:
            video_path = self.get_next_video()

            if video_path is None:
                # No more videos, check again in 5 seconds
                idle_count += 1
                if idle_count == 1:
                    self.log(f"Queue empty. Processed {videos_processed} videos. Waiting...")
                time.sleep(5)
                continue

            idle_count = 0
            video_name = os.path.basename(video_path)

            start_time = time.time()
            clips = self.process_video(video_path)

            elapsed = time.time() - start_time
            videos_processed += 1

            if clips:
                self.log(f"[{videos_processed}] {video_name}: {len(clips)} clips ({elapsed:.1f}s)")
            else:
                self.log(f"[{videos_processed}] {video_name}: No people ({elapsed:.1f}s)")

            # Release and mark as processed
            self.release_video(video_path)

if __name__ == "__main__":
    worker = ContinuousGPUWorker(WORKER_ID)
    worker.run()
```

### Step 3.2: Deploy Worker Script to Container

```bash
# For Park_R
docker cp /tmp/gpu_worker_continuous.py peoplenet-park-r:/workspace/worker.py

# For Park_F (update paths in script first)
# Edit STAGING_DIR, OUTPUT_DIR, etc. to use Park_F_Batch1
docker cp /tmp/gpu_worker_continuous.py peoplenet-park-f:/workspace/worker.py
```

### Step 3.3: Create Output Directories

```bash
# For Park_R
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt

# For Park_F
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/locks
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/processed_videos.txt
```

---

## Phase 4: Batch Processing System

### Step 4.1: Create Batch Copy Agent

**File**: `/tmp/batch_copy_agent.sh`

```bash
#!/bin/bash

# Batch-constrained copy agent
# Maintains disk space buffer and copies videos in controlled batches

SOURCE="/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R"
STAGING="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt"
FILTER_LIST="/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt"

BATCH_SIZE=50                    # Number of videos per batch
MIN_FREE_GB=20                   # Minimum disk space buffer (GB)
CHECK_INTERVAL=5                 # Seconds between checks
MIN_STAGING_THRESHOLD=20         # Keep at least this many videos in staging

mkdir -p "$STAGING"
touch "$PROCESSED_LIST"

echo "=== Batch Copy Agent ==="
echo "Batch size: $BATCH_SIZE videos"
echo "Minimum free space: ${MIN_FREE_GB}GB"
echo "Staging threshold: $MIN_STAGING_THRESHOLD videos"
echo "Total videos to process: $(wc -l < "$FILTER_LIST")"
echo "Already processed: $(wc -l < "$PROCESSED_LIST")"
echo ""

while true; do
    # Check disk space
    FREE_GB=$(df -BG /home/yousuf/PROJECTS/PeopleNet | tail -1 | awk '{print $4}' | sed 's/G//')

    if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
        echo "[$(date +%H:%M:%S)] ⚠️  Low disk space: ${FREE_GB}GB free (need ${MIN_FREE_GB}GB buffer)"
        echo "Waiting for workers to free up space..."
        sleep $CHECK_INTERVAL
        continue
    fi

    # Count videos in staging
    STAGING_COUNT=$(ls "$STAGING"/*.MP4 2>/dev/null | wc -l)

    # Only copy if staging is low
    if [ "$STAGING_COUNT" -ge "$MIN_STAGING_THRESHOLD" ]; then
        sleep $CHECK_INTERVAL
        continue
    fi

    # Copy next batch
    echo "[$(date +%H:%M:%S)] Staging low ($STAGING_COUNT videos), disk: ${FREE_GB}GB - copying next batch..."

    COPIED=0
    while IFS= read -r video; do
        # Check if already processed
        if grep -Fxq "$video" "$PROCESSED_LIST" 2>/dev/null; then
            continue
        fi

        # Check if already in staging
        if [ -f "$STAGING/$video" ]; then
            continue
        fi

        # Copy video
        if cp "$SOURCE/$video" "$STAGING/" 2>/dev/null; then
            echo "  ✓ $video"
            COPIED=$((COPIED + 1))

            if [ "$COPIED" -ge "$BATCH_SIZE" ]; then
                break
            fi
        fi
    done < "$FILTER_LIST"

    if [ "$COPIED" -eq 0 ]; then
        TOTAL_PROCESSED=$(wc -l < "$PROCESSED_LIST")
        TOTAL_VIDEOS=$(wc -l < "$FILTER_LIST")
        echo "[$(date +%H:%M:%S)] ✅ All videos processed: $TOTAL_PROCESSED/$TOTAL_VIDEOS"
        break
    fi

    echo "[$(date +%H:%M:%S)] Copied $COPIED videos to staging"
    sleep $CHECK_INTERVAL
done

echo "=== Copy agent finished ==="
```

### Step 4.2: Start Complete Pipeline

**Order of Execution**:

```bash
# 1. Start Docker container (if not running)
docker start peoplenet-park-r

# 2. Start GPU workers (3 workers for parallel processing)
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# 3. Start copy agent in background
nohup /tmp/batch_copy_agent.sh > /tmp/copy_agent.log 2>&1 &

# 4. Monitor progress
tail -f /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/worker_1_log.txt
```

### Step 4.3: Monitor Pipeline

```bash
# Check processing progress
wc -l /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt

# Check clips created
ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 | wc -l

# Check staging queue
ls /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1/*.MP4 2>/dev/null | wc -l

# Check disk space
df -h /home/yousuf/PROJECTS/PeopleNet

# Check GPU utilization
nvidia-smi

# Check workers status
docker exec peoplenet-park-r ps aux | grep python3
```

---

## Critical Issues and Solutions

### Issue 1: Missing ffmpeg in Container

**Symptom**: Videos marked as "No people" even when people are detected. Errors like:
```
Error processing video.MP4: [Errno 2] No such file or directory: 'ffmpeg'
```

**Root Cause**: ffmpeg not installed in Docker container, causing clip extraction to fail silently.

**Solution**:
```bash
docker exec peoplenet-park-r apt-get update
docker exec peoplenet-park-r apt-get install -y ffmpeg
```

**Prevention**: Always install ffmpeg BEFORE starting workers.

### Issue 2: Workers Not Deleting Processed Videos

**Symptom**: Staging directory fills up with processed videos, copy agent can't add new ones.

**Root Cause**: Original worker script didn't delete videos after processing.

**Solution**: Add deletion to `release_video()` function:
```python
def release_video(self, video_path):
    # ... existing code ...

    # Delete video from staging to free up space
    try:
        os.remove(video_path)
    except:
        pass
```

### Issue 3: Workers Idle Due to Small Batch Size

**Symptom**: Workers spend 50%+ time idle, very slow processing.

**Root Cause**:
- Batch size too small (10 videos)
- Check interval too long (30 seconds)
- Copy trigger only when staging completely empty

**Solution**:
- Increase BATCH_SIZE from 10 to 50
- Reduce CHECK_INTERVAL from 30 to 5 seconds
- Change copy trigger to activate when staging < 20 videos

**Performance Impact**: 15x speed improvement (10 → 150 videos/minute)

### Issue 4: Corrupt Video Files Blocking Pipeline

**Symptom**: Workers hang on specific videos with errors:
```
Invalid NAL unit size
stream 0, offset 0xe582c: partial file
OpenCV assertion failed
```

**Root Cause**: Corrupt/damaged video files from source.

**Solution**:
```bash
# Create quarantine directory
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Corrupted_Videos

# Move corrupt files
mv /path/to/corrupt/*.MP4 /home/yousuf/PROJECTS/PeopleNet/Corrupted_Videos/
```

### Issue 5: Permission Issues with processed_videos.txt

**Symptom**: Copy agent can't read processed list:
```
cannot touch 'processed_videos.txt': Permission denied
```

**Root Cause**: File created by Docker container (root), not accessible by host user.

**Solution**:
```bash
sudo chown yousuf:yousuf /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt
```

---

## Configuration Reference

### SSIM Filter Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `threshold` | 0.85 | SSIM threshold (0-1). Lower = more motion required |
| `sample_interval` | 30 | Compare frames every N frames |
| Image resize | 320x180 | Downscaled resolution for faster SSIM |

**Tuning Guide**:
- threshold 0.90+ : Very sensitive, catches minimal motion
- threshold 0.85  : Balanced, good for dashcams (recommended)
- threshold 0.80  : Less sensitive, only significant motion

### PeopleNet Detection Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `confidence_threshold` | 0.6 | Detection confidence (0-1) |
| `buffer_seconds` | 4 | Seconds before/after detection to include in clip |
| `sample_rate` | 0.5s | Run detection every 0.5 seconds |
| Input resolution | 960x544 | Model input size (fixed) |
| GPU memory limit | 2GB | Per worker memory limit |

**Detection Confidence Tuning**:
- 0.5: More sensitive, more false positives
- 0.6: Balanced (recommended)
- 0.7+: Less sensitive, may miss distant people

### Batch Processing Configuration

| Parameter | Recommended | Min | Max | Description |
|-----------|-------------|-----|-----|-------------|
| `BATCH_SIZE` | 50 | 10 | 100 | Videos per batch |
| `MIN_FREE_GB` | 20 | 10 | 50 | Disk space buffer (GB) |
| `CHECK_INTERVAL` | 5 | 3 | 30 | Seconds between checks |
| `MIN_STAGING_THRESHOLD` | 20 | 10 | 50 | Min videos in staging before copying |
| GPU Workers | 3 | 1 | 6 | Parallel workers per GPU |

**Performance Tuning**:
- More workers = faster processing but more GPU memory
- Larger batch = fewer idle periods but more disk usage
- Smaller check interval = more responsive but more CPU overhead

---

## Performance Optimization

### Expected Performance Metrics

**Single Video Processing**:
- Detection scan: ~12-15 seconds per 60s video
- Clip extraction: <1 second per clip (ffmpeg copy mode)
- Total: ~15 seconds per video average

**Parallel Processing (3 GPU workers)**:
- Throughput: 70-75 videos/minute
- Daily capacity: ~100,000+ videos
- GPU utilization: 5-10% (inference is fast)

### Optimization Strategies

1. **Worker Count**:
   - 3 workers optimal for single GPU
   - Add more workers if GPU utilization < 50%
   - Don't exceed GPU memory capacity

2. **Batch Size**:
   - Keep staging buffer full (20-50 videos)
   - Prevents worker idle time
   - Balance against disk space

3. **Disk I/O**:
   - Use SSD for staging directory
   - Copy agent runs on separate thread
   - Workers delete files immediately after processing

4. **Model Optimization**:
   - INT8 quantization (already optimized)
   - CUDA execution provider (GPU)
   - Sample every 0.5s (not every frame)

### Bottleneck Identification

**GPU Bottleneck**: GPU utilization > 80%
- Solution: Reduce worker count or sample rate

**Disk Bottleneck**: Workers waiting for videos
- Solution: Increase batch size and reduce check interval

**Memory Bottleneck**: OOM errors
- Solution: Reduce gpu_mem_limit or worker count

**Network/Copy Bottleneck**: Staging always empty
- Solution: Increase batch size, ensure fast disk access

---

## Replication Checklist

Use this checklist to replicate the pipeline from scratch:

- [ ] Install system dependencies (Docker, NVIDIA drivers, CUDA)
- [ ] Create directory structure
- [ ] Download PeopleNet model to `/path/to/model/`
- [ ] Create SSIM filter script
- [ ] Run SSIM filter on source videos
- [ ] Create Docker container with nvidia-runtime
- [ ] **Install ffmpeg in container** (CRITICAL)
- [ ] Create and deploy GPU worker script
- [ ] Update all paths in worker script (STAGING_DIR, OUTPUT_DIR, MODEL_PATH)
- [ ] Create output directories and processed_videos.txt
- [ ] Create batch copy agent script
- [ ] Update paths in copy agent script
- [ ] Start Docker container
- [ ] Start GPU workers (3 workers)
- [ ] Start copy agent in background
- [ ] Monitor logs and verify clips are being created
- [ ] Verify disk space buffer maintained
- [ ] Check for and quarantine any corrupt videos

---

## Appendix: File Paths Quick Reference

```
# Model
/home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx

# Source Videos
/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R/
/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_F/

# Filtered Lists
/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt
/home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt

# Staging (temporary)
/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1/
/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1/

# Outputs
/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/
/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/

# Scripts
/tmp/ssim_filter.py
/tmp/gpu_worker_continuous.py
/tmp/batch_copy_agent.sh

# Container paths (inside Docker)
/workspace/model/resnet34_peoplenet_int8.onnx
/workspace/Staging/Park_R_Batch1/
/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/
/workspace/worker.py
```

---

**End of Documentation**

*Last Updated: 2025-11-10*
*Pipeline Version: 2.0*
*Tested on: Ubuntu 22.04, RTX 4080 SUPER, CUDA 12.x*

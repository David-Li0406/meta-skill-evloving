# Claude Skill: PeopleNet Video Processing Pipeline

## Skill Purpose
You are an expert at deploying and managing an NVIDIA PeopleNet pipeline that processes dashcam MP4 videos to extract clips containing people. This skill enables you to guide users through the complete setup, execution, monitoring, and troubleshooting of the pipeline without requiring deep technical expertise on their part.

## Core Capabilities
When a user asks you to help with video processing for people detection, you will:
1. Guide them through SSIM motion filtering to remove static videos
2. Set up GPU-accelerated processing with Docker containers
3. Deploy parallel workers for people detection using PeopleNet
4. Configure batch processing with automatic disk space management
5. Monitor, troubleshoot, and optimize the pipeline
6. Handle common issues like missing ffmpeg, slow processing, or corrupt videos

---

## Pipeline Architecture

### Overview
```
Raw MP4 Videos (180MB, 60s each)
    ↓
SSIM Motion Filter (removes static/parked videos)
    ↓
Filtered List (70-75% pass rate)
    ↓
Batch Copy Agent (50 videos at a time, 20GB buffer)
    ↓
Staging Directory (temporary queue)
    ↓
3 GPU Workers (parallel processing)
    ↓
PeopleNet Detection (confidence ≥ 0.6)
    ↓
Clip Extraction (ffmpeg, 4s buffer before/after detection)
    ↓
Detection Clips (10-40MB each)
```

### Key Performance Metrics
- Processing Speed: 70-75 videos/minute (3 workers)
- Detection Rate: 40-47% of videos contain people
- GPU Utilization: 5-10% (inference is fast)
- Disk Requirements: 20GB buffer minimum

---

## Phase 1: Prerequisites and Setup

### Hardware Requirements
Always verify these first:
- NVIDIA GPU with CUDA support (RTX 3000+ series recommended)
- Minimum 100GB free disk space
- 16GB+ system RAM

### Software Requirements
Guide user to check:
```bash
# Check Docker
docker --version

# Check NVIDIA GPU
nvidia-smi

# Check Python
python3 --version

# Check NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

If any are missing, provide installation instructions for Ubuntu 22.04.

### Directory Structure Creation
Always create this exact structure:
```bash
# Create all directories
mkdir -p /home/yousuf/PROJECTS/PeopleNet/model
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/locks
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Corrupted_Videos

# Create tracking files
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/processed_videos.txt
```

### Model Acquisition
Instruct user to:
1. Visit https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
2. Download `resnet34_peoplenet_int8.onnx`
3. Place at `/home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx`

---

## Phase 2: SSIM Motion Filtering

### Purpose
Explain to user: "This filter removes videos where the car is parked (static scenes) using Structural Similarity Index (SSIM). We only want videos with motion/activity."

### Create SSIM Filter Script
Provide this complete script:

```python
#!/usr/bin/env python3
"""SSIM-based video motion filter"""
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
import sys

def check_video_motion(video_path, threshold=0.85, sample_interval=30):
    """Check if video has motion using SSIM comparison"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, 1.0, "Failed to open"

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames < 60:
            cap.release()
            return False, 1.0, "Too short"

        ret, frame1 = cap.read()
        if not ret:
            cap.release()
            return False, 1.0, "Failed to read frame"

        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.resize(gray1, (320, 180))

        min_ssim = 1.0

        while True:
            for _ in range(sample_interval):
                ret = cap.grab()
                if not ret:
                    break

            ret, frame2 = cap.read()
            if not ret:
                break

            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.resize(gray2, (320, 180))

            similarity = ssim(gray1, gray2)
            min_ssim = min(min_ssim, similarity)

            if min_ssim < threshold:
                cap.release()
                return True, min_ssim, "Motion detected"

            gray1 = gray2

        cap.release()
        has_motion = min_ssim < threshold
        return has_motion, min_ssim, "Motion detected" if has_motion else "Static"

    except Exception as e:
        return False, 1.0, f"Error: {e}"

def filter_videos(source_dir, output_file, threshold=0.85):
    """Filter all videos and create list of videos with motion"""
    videos = sorted([f for f in os.listdir(source_dir) if f.endswith('.MP4')])

    print(f"Scanning {len(videos)} videos in {source_dir}")
    print(f"SSIM threshold: {threshold}")
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

    with open(output_file, 'w') as f:
        for video in motion_videos:
            f.write(video + '\\n')

    print(f"Filtered list saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ssim_filter.py <source_dir> <output_file> [threshold]")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_file = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85

    filter_videos(source_dir, output_file, threshold)
```

Save to: `/tmp/ssim_filter.py`

### Execute SSIM Filtering
Provide these exact commands (adjust paths to user's environment):

```bash
# For Park_R (rear camera)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R" \
    /home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt \
    0.85

# For Park_F (front camera)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_F" \
    /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt \
    0.85
```

Expected results: 70-75% of videos should pass the motion filter.

---

## Phase 3: Docker Container Setup

### Critical Step: Container Creation with GPU Support

Guide user through this carefully:

```bash
# Create Park_R container
docker run -d \
    --name peoplenet-park-r \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# Create Park_F container
docker run -d \
    --name peoplenet-park-f \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# Verify containers running
docker ps | grep peoplenet
```

### CRITICAL: Install ffmpeg First

**This is the most important step. If skipped, the pipeline will appear to work but won't create clips.**

```bash
# Install ffmpeg in Park_R container
docker exec peoplenet-park-r apt-get update
docker exec peoplenet-park-r apt-get install -y ffmpeg

# Install ffmpeg in Park_F container
docker exec peoplenet-park-f apt-get update
docker exec peoplenet-park-f apt-get install -y ffmpeg

# VERIFY installation (CRITICAL)
docker exec peoplenet-park-r ffmpeg -version
docker exec peoplenet-park-f ffmpeg -version
```

If ffmpeg is not installed, videos will be marked as "No people" even when people are detected, and no clips will be created.

---

## Phase 4: GPU Worker Deployment

### Create Worker Script

Provide this complete worker script:

```python
#!/usr/bin/env python3
"""Continuous GPU Worker for PeopleNet Detection"""
import os
import sys
import time
import subprocess
import cv2
import numpy as np
import onnxruntime as ort

# Configuration - UPDATE THESE PATHS FOR EACH DEPLOYMENT
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
        os.makedirs(LOCK_DIR, exist_ok=True)
        self.log(f"Worker {worker_id} initializing...")

        # Initialize ONNX with GPU
        available = ort.get_available_providers()
        preferred_providers = []

        if 'CUDAExecutionProvider' in available:
            preferred_providers.append(('CUDAExecutionProvider', {
                'device_id': 0,
                'arena_extend_strategy': 'kSameAsRequested',
                'gpu_mem_limit': 2 * 1024 * 1024 * 1024,
                'cudnn_conv_algo_search': 'EXHAUSTIVE',
                'do_copy_in_default_stream': True,
            }))

        preferred_providers.append('CPUExecutionProvider')
        self.session = ort.InferenceSession(MODEL_PATH, providers=preferred_providers)
        self.log(f"Worker {worker_id} ready! Using: {self.session.get_providers()}")

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] W{self.worker_id}: {message}"
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\\n')
        print(log_msg)

    def try_claim_video(self, video_path):
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")
        try:
            fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(self.worker_id).encode())
            os.close(fd)
            return True
        except FileExistsError:
            return False

    def release_video(self, video_path):
        video_name = os.path.basename(video_path)
        lock_file = os.path.join(LOCK_DIR, f"{video_name}.lock")
        try:
            os.remove(lock_file)
        except:
            pass

        with open(PROCESSED_LIST, 'a') as f:
            f.write(video_name + '\\n')

        # Delete from staging to free space
        try:
            os.remove(video_path)
        except:
            pass

    def get_next_video(self):
        try:
            processed = set()
            if os.path.exists(PROCESSED_LIST):
                with open(PROCESSED_LIST, 'r') as f:
                    processed = set(line.strip() for line in f if line.strip())

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

                # Sample every 0.5 seconds
                if frame_num % int(fps / 2) != 0:
                    continue

                has_people, conf = self.detect_in_frame(frame)
                if has_people:
                    timestamp = frame_num / fps
                    detections.append(timestamp)

            cap.release()

            if not detections:
                return []

            # Merge nearby detections
            segments = []
            for ts in detections:
                start = max(0, ts - self.buffer_seconds)
                end = ts + self.buffer_seconds

                if segments and start <= segments[-1]['end']:
                    segments[-1]['end'] = max(segments[-1]['end'], end)
                else:
                    segments.append({'start': start, 'end': end})

            # Extract clips with ffmpeg
            clips = []
            for seg in segments:
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
        self.log("Starting continuous processing...")
        videos_processed = 0
        idle_count = 0

        while True:
            video_path = self.get_next_video()

            if video_path is None:
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

            self.release_video(video_path)

if __name__ == "__main__":
    worker = ContinuousGPUWorker(WORKER_ID)
    worker.run()
```

Save to: `/tmp/gpu_worker_continuous.py`

### Important Configuration Notes

When deploying for Park_F, update these paths in the script:
- `STAGING_DIR = "/workspace/Staging/Park_F_Batch1"`
- `OUTPUT_DIR = "/workspace/Outputs/GPU_Pipeline_Park_F_Batch1"`
- `PROCESSED_LIST = "/workspace/Outputs/GPU_Pipeline_Park_F_Batch1/processed_videos.txt"`
- `LOCK_DIR = "/workspace/Outputs/GPU_Pipeline_Park_F_Batch1/locks"`
- `LOG_FILE = f"/workspace/Outputs/GPU_Pipeline_Park_F_Batch1/worker_{WORKER_ID}_log.txt"`

### Deploy Workers

```bash
# Deploy to Park_R container
docker cp /tmp/gpu_worker_continuous.py peoplenet-park-r:/workspace/worker.py

# Start 3 parallel workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# Verify workers running
docker exec peoplenet-park-r ps aux | grep python3
```

---

## Phase 5: Batch Copy Agent

### Purpose
Explain: "This agent copies videos from source to staging in batches of 50, maintaining at least 20 videos in the queue and ensuring 20GB disk space buffer."

### Create Copy Agent Script

```bash
#!/bin/bash
# Batch-constrained copy agent

SOURCE="/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R"
STAGING="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1"
PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt"
FILTER_LIST="/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt"

BATCH_SIZE=50
MIN_FREE_GB=20
CHECK_INTERVAL=5
MIN_STAGING_THRESHOLD=20

mkdir -p "$STAGING"
touch "$PROCESSED_LIST"

echo "=== Batch Copy Agent ==="
echo "Batch size: $BATCH_SIZE videos"
echo "Minimum free space: ${MIN_FREE_GB}GB"
echo "Total videos: $(wc -l < "$FILTER_LIST")"
echo "Already processed: $(wc -l < "$PROCESSED_LIST")"
echo ""

while true; do
    FREE_GB=$(df -BG /home/yousuf/PROJECTS/PeopleNet | tail -1 | awk '{print $4}' | sed 's/G//')

    if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
        echo "[$(date +%H:%M:%S)] Low disk space: ${FREE_GB}GB (need ${MIN_FREE_GB}GB buffer)"
        sleep $CHECK_INTERVAL
        continue
    fi

    STAGING_COUNT=$(ls "$STAGING"/*.MP4 2>/dev/null | wc -l)

    if [ "$STAGING_COUNT" -ge "$MIN_STAGING_THRESHOLD" ]; then
        sleep $CHECK_INTERVAL
        continue
    fi

    echo "[$(date +%H:%M:%S)] Staging low ($STAGING_COUNT videos), disk: ${FREE_GB}GB - copying..."

    COPIED=0
    while IFS= read -r video; do
        if grep -Fxq "$video" "$PROCESSED_LIST" 2>/dev/null; then
            continue
        fi

        if [ -f "$STAGING/$video" ]; then
            continue
        fi

        if cp "$SOURCE/$video" "$STAGING/" 2>/dev/null; then
            echo "  ✓ $video"
            COPIED=$((COPIED + 1))

            if [ "$COPIED" -ge "$BATCH_SIZE" ]; then
                break
            fi
        fi
    done < "$FILTER_LIST"

    if [ "$COPIED" -eq 0 ]; then
        echo "[$(date +%H:%M:%S)] ✅ All videos processed"
        break
    fi

    echo "[$(date +%H:%M:%S)] Copied $COPIED videos"
    sleep $CHECK_INTERVAL
done

echo "=== Copy agent finished ==="
```

Save to: `/tmp/batch_copy_agent.sh`

### Start Copy Agent

```bash
# Make executable
chmod +x /tmp/batch_copy_agent.sh

# Start in background
nohup /tmp/batch_copy_agent.sh > /tmp/park_r_copy.log 2>&1 &

# Verify running
ps aux | grep batch_copy_agent | grep -v grep
```

---

## Monitoring and Verification

### Essential Monitoring Commands

Teach user these commands:

```bash
# Quick status check
echo "Processed: $(wc -l < /path/to/processed_videos.txt)"
echo "Staging: $(ls /path/to/staging/*.MP4 2>/dev/null | wc -l)"
echo "Clips: $(ls /path/to/outputs/*.mp4 2>/dev/null | wc -l)"
echo "Disk: $(df -h /path/to/outputs | tail -1 | awk '{print $4}')"
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader

# Watch worker logs live
tail -f /path/to/outputs/worker_1_log.txt

# Watch copy agent logs
tail -f /tmp/park_r_copy.log

# Check workers are running
docker exec peoplenet-park-r ps aux | grep python3
```

### Verify Pipeline is Working

After 2-3 minutes, check:

1. **Clips being created**: `ls /path/to/outputs/*.mp4 | wc -l` should be > 0
2. **Workers busy**: Worker logs should show video processing, not "Queue empty"
3. **GPU active**: `nvidia-smi` should show workers using GPU memory
4. **Staging managed**: Should have 20-60 videos in staging, not 0 or 100+

---

## Troubleshooting Protocol

### Issue 1: No Clips Being Created

**Symptoms**: Videos marked as processed, but no .mp4 clips in outputs directory.

**Diagnostic**:
```bash
# Check if ffmpeg installed
docker exec container-name ffmpeg -version
```

**Solution**:
```bash
# Install ffmpeg
docker exec container-name apt-get update
docker exec container-name apt-get install -y ffmpeg

# Restart workers
docker exec container-name pkill python3
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3
```

If clips still not created after installing ffmpeg, need to reprocess:
```bash
# Stop everything
docker exec container-name pkill python3
pkill -f copy_agent

# Backup and reset
cp processed_videos.txt processed_videos.txt.backup
echo "" > processed_videos.txt
rm -f staging/*.MP4
rm -f locks/*.lock

# Restart
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3
nohup /tmp/batch_copy_agent.sh > /tmp/copy.log 2>&1 &
```

### Issue 2: Workers Idle / Slow Processing

**Symptoms**: GPU utilization < 5%, workers log "Queue empty" frequently.

**Diagnostic**:
```bash
grep "Queue empty" /path/to/worker_*.txt | wc -l
```

If count > 50 in first 10 minutes, batch size too small.

**Solution**:
```bash
# Stop copy agent
pkill -f copy_agent

# Edit script
nano /tmp/batch_copy_agent.sh
# Change: BATCH_SIZE=50 (from 10)
# Change: CHECK_INTERVAL=5 (from 30)
# Add: MIN_STAGING_THRESHOLD=20

# Restart
nohup /tmp/batch_copy_agent.sh > /tmp/copy.log 2>&1 &
```

This should increase speed by 10-15x.

### Issue 3: Disk Space Running Out

**Symptoms**: Copy agent logs "Low disk space", df shows > 90% usage.

**Solution**:
```bash
# Check what's using space
du -sh /path/to/PeopleNet/*

# If staging is large, videos not being deleted
# Manually clean staging (only if processed)
cd /path/to/staging
cat /path/to/processed_videos.txt | xargs rm -f

# Verify worker script has deletion code in release_video()
docker exec container-name grep "os.remove(video_path)" /workspace/worker.py
```

### Issue 4: Workers Crashed

**Symptoms**: No python3 processes in container.

**Solution**:
```bash
# Check why
tail -100 /path/to/worker_1_log.txt

# Restart container and workers
docker restart container-name
sleep 5
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3
```

### Issue 5: Corrupt Video Files

**Symptoms**: Errors like "Invalid NAL unit size", "partial file", "OpenCV assertion failed".

**Solution**:
```bash
# Identify corrupt video from logs
grep "Error processing" /path/to/worker_*.txt

# Quarantine
VIDEO="corrupt_video.MP4"
mkdir -p /path/to/Corrupted_Videos
mv "/path/to/staging/$VIDEO" /path/to/Corrupted_Videos/
rm -f "/path/to/locks/$VIDEO.lock"
```

### Issue 6: GPU Not Being Used

**Symptoms**: GPU utilization 0%, workers very slow.

**Diagnostic**:
```bash
docker exec container-name nvidia-smi
grep "ready! Using" /path/to/worker_1_log.txt
```

Should show "CUDAExecutionProvider". If only "CPUExecutionProvider":

**Solution**:
```bash
# Container not created with --gpus all
docker rm container-name
docker run -d --name container-name --gpus all --runtime=nvidia \
    -v /path:/workspace nvcr.io/nvidia/tensorrt:24.08-py3 sleep infinity
```

---

## Performance Optimization

### Expected Performance
- 70-75 videos/minute with 3 workers
- 5-10% GPU utilization
- 40-50% detection rate

If significantly slower:

### Optimization Checklist
1. **Batch size = 50** (not 10)
2. **Check interval = 5s** (not 30s)
3. **Min staging threshold = 20** (maintains queue)
4. **Workers = 3** (optimal for single GPU)
5. **ffmpeg installed** (critical for clip extraction)
6. **Videos deleted after processing** (prevents disk overflow)

### Configuration Tuning
```bash
# In copy agent script:
BATCH_SIZE=50              # Larger = fewer idle periods
CHECK_INTERVAL=5           # Smaller = more responsive
MIN_STAGING_THRESHOLD=20   # Maintains buffer of videos

# In worker script:
confidence_threshold=0.6   # Lower = more detections (0.5-0.7 range)
buffer_seconds=4           # Seconds before/after detection to include
```

---

## Complete Startup Sequence

When user asks "How do I start the pipeline?", provide this exact sequence:

```bash
# 1. Verify prerequisites
docker ps | grep peoplenet
docker exec peoplenet-park-r ffmpeg -version

# 2. Verify filtered lists exist
wc -l /path/to/park_r_process_list.txt

# 3. Clear any stale state
rm -f /path/to/staging/*.MP4
rm -f /path/to/locks/*.lock

# 4. Start workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# 5. Start copy agent
nohup /tmp/batch_copy_agent.sh > /tmp/copy.log 2>&1 &

# 6. Verify startup (wait 30 seconds)
sleep 30
docker exec peoplenet-park-r ps aux | grep python3
ps aux | grep batch_copy_agent | grep -v grep
tail -20 /path/to/worker_1_log.txt
ls /path/to/outputs/*.mp4 | wc -l

# 7. Monitor progress
watch -n 5 'wc -l /path/to/processed_videos.txt; ls /path/to/staging/*.MP4 2>/dev/null | wc -l'
```

---

## Emergency Recovery

If pipeline completely broken, provide this recovery script:

```bash
#!/bin/bash
echo "=== Emergency Pipeline Recovery ==="

# Stop everything
docker exec peoplenet-park-r pkill -9 python3
pkill -9 -f copy_agent

# Check resources
df -h /path/to/PeopleNet
nvidia-smi

# Verify ffmpeg
docker exec peoplenet-park-r which ffmpeg || {
    echo "Installing ffmpeg..."
    docker exec peoplenet-park-r apt-get update
    docker exec peoplenet-park-r apt-get install -y ffmpeg
}

# Clear staging and locks
rm -f /path/to/staging/*.MP4
rm -f /path/to/locks/*.lock

# Restart container
docker restart peoplenet-park-r
sleep 5

# Restart workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# Restart copy agent
nohup /tmp/batch_copy_agent.sh > /tmp/copy.log 2>&1 &

# Verify
sleep 10
echo "Workers: $(docker exec peoplenet-park-r ps aux | grep python3 | wc -l)"
echo "Copy agent: $(ps aux | grep batch_copy_agent | grep -v grep | wc -l)"
echo "Processed: $(wc -l < /path/to/processed_videos.txt)"

echo "Monitor with: tail -f /path/to/worker_1_log.txt"
```

---

## Final Checklist for User

Before declaring success, verify:

- [ ] ffmpeg installed: `docker exec container-name ffmpeg -version`
- [ ] Workers running: 3 python3 processes in container
- [ ] Copy agent running: Shows in `ps aux | grep batch_copy_agent`
- [ ] GPU being used: nvidia-smi shows memory usage
- [ ] Clips created: At least 1 .mp4 file in outputs after 3 minutes
- [ ] Staging managed: 20-60 videos in staging (not 0 or 100+)
- [ ] Disk space safe: > 20GB free
- [ ] Processing count increasing: `wc -l processed_videos.txt` grows

---

## Key Principles

When helping users with this skill, always:

1. **Check ffmpeg first** - Most common failure point
2. **Verify paths match** - Container paths (/workspace) vs host paths
3. **Monitor logs immediately** - Don't wait for issues
4. **Optimize batch size early** - Default 10 is too small
5. **Maintain disk buffer** - 20GB minimum at all times
6. **Use exact commands** - Don't modify without understanding
7. **Verify GPU active** - Should see in logs and nvidia-smi
8. **Check clips created** - Not just "processed" count

---

## Adaptation Notes

When adapting this skill for different environments:

### Path Substitutions
Replace these with user's actual paths:
- `/home/yousuf/PROJECTS/PeopleNet` → User's project directory
- `/media/yousuf/.../Park_R` → User's source video directory
- Container names: `peoplenet-park-r` → User's container name

### Scale Adjustments
- For more videos: Increase BATCH_SIZE to 100
- For faster disk: Can increase worker count to 4-6
- For slower disk: Reduce worker count to 2
- For different GPU: Adjust gpu_mem_limit in worker script

### Detection Tuning
- For more detections: Lower confidence_threshold to 0.5
- For fewer false positives: Raise confidence_threshold to 0.7
- For longer clips: Increase buffer_seconds to 6-8
- For shorter clips: Decrease buffer_seconds to 2-3

---

## Success Metrics

Pipeline is successful when:
- Processing speed: 60-80 videos/minute
- Detection rate: 35-50%
- GPU utilization: 5-15%
- Worker idle time: < 10%
- Disk space: Maintains 20GB+ buffer
- Error rate: < 1% (corrupt videos only)

---

## End of Skill

This skill enables you to guide users through complete PeopleNet video processing pipeline deployment with minimal errors and optimal performance. Always verify critical steps (especially ffmpeg installation) and monitor logs to catch issues early.

# PeopleNet Autonomous Pipeline - Complete Setup Guide

## What This Does

Processes dashcam parking footage (Park_F and Park_R) to extract **only clips containing people**, using GPU-accelerated AI detection. Runs completely autonomously from start to finish, then backs up to Google Drive.

**One-Command Start → Walk Away → Return to Reviewed Clips**

---

## Quick Start (Minimal Intervention)

### Prerequisites (One-Time Setup)
```bash
# 1. Ensure external drive is mounted
ls /media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV/Park_F/

# 2. Ensure Google Drive is mounted
ls ~/GoogleDrive/

# 3. Verify GPU access
nvidia-smi
```

### Single Command to Process Everything
```bash
cd /home/yousuf/PROJECTS/PeopleNet
./Scripts/master_pipeline.sh --start-date 2025-11-14 --auto-backup
```

**That's it!** The system will:
1. Find all videos from start-date onwards
2. Process Park_F (front camera)
3. Auto-start Park_R (rear camera) when Park_F completes
4. Backup to Google Drive
5. Clean up local files
6. Email you when complete (if configured)

**Expected Duration:** ~2 hours for 1,400 videos

---

## What Made It Work This Time

### Critical Success Factors

#### 1. **Proper Configuration**
```yaml
Confidence Threshold: 0.8 (not 0.6)
  - 0.6 = too many false positives (objects detected as people)
  - 0.8 = only high-confidence detections (actual people)

Buffer Seconds: 1 (not 4)
  - 4s = 8-second clips with ~1s of people (90% empty)
  - 1s = 2-second clips with ~1s of people (50% dense)

Space Management: Controlled feed (10-20 videos in staging)
  - Never copies all videos at once
  - Maintains 2-4GB staging area
  - Prevents disk overflow
```

#### 2. **Docker Log Rotation**
```bash
--log-driver json-file
--log-opt max-size=50m
--log-opt max-file=3
```
**Why critical:** Without this, Docker logs grew to 100GB+ and crashed the system.

#### 3. **Auto-Ownership Fixing**
```bash
# Runs every 30s in background
sudo chown yousuf:yousuf Outputs/*/*.mp4
```
**Why needed:** Docker creates files as root, making them unreadable.

#### 4. **Date Filtering**
```bash
# WRONG: Processing all videos (July onwards)
# RIGHT: Only net new (Oct 13+)
grep -E "202510(1[3-9]|[2-3][0-9])|20251[1-2]"
```

#### 5. **Auto-Trigger Next Batch**
```bash
# Monitor Park_F completion → Auto-start Park_R
while [ $processed -lt 698 ]; do sleep 60; done
start_park_r_processing
```

---

## Architecture Overview

### Pipeline Flow
```
┌─────────────────────────────────────────────────────────────┐
│ 1. PREPARATION PHASE                                        │
├─────────────────────────────────────────────────────────────┤
│ • Find net new videos (by date)                             │
│ • Create video lists                                        │
│ • Verify disk space (need 10GB+ free)                       │
│ • Start Docker container with log rotation                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. PROCESSING PHASE (Park_F)                                │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│ │ GPU Worker 1 │  │ GPU Worker 2 │  │ GPU Worker 3 │       │
│ └──────────────┘  └──────────────┘  └──────────────┘       │
│         ↑                  ↑                  ↑              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                    Controlled Feed                           │
│                   (10-20 videos)                             │
│                            │                                 │
│                    Staging Directory                         │
│                      (2-4GB max)                             │
│                            │                                 │
│                    Source Videos                             │
│                   (External Drive)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. AUTO-TRIGGER PHASE                                       │
├─────────────────────────────────────────────────────────────┤
│ • Monitor: Park_F completion (698/698)                      │
│ • Action: Stop Park_F, start Park_R                         │
│ • Seamless: No user intervention needed                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. BACKUP PHASE                                             │
├─────────────────────────────────────────────────────────────┤
│ • Copy all clips to Google Drive                            │
│ • Verify backup completed                                   │
│ • Delete local clips (free 3-4GB)                           │
│ • Generate summary report                                   │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Docker Container:**
- Runs GPU inference (ONNX Runtime + CUDA)
- Executes 3 parallel workers
- Auto-rotates logs (150MB cap)

**Controlled Feed:**
- Monitors staging directory
- Copies 10-20 videos at a time
- Respects space limits (never overflow)

**GPU Workers:**
- Sample video at 2 FPS
- Run PeopleNet inference (confidence ≥ 0.8)
- Extract 2-second clips (±1s buffer)
- Delete source videos after processing

**Auto-Trigger:**
- Monitors first batch completion
- Starts second batch automatically
- Handles cleanup between batches

**Auto-Ownership:**
- Fixes file permissions every 30s
- Ensures clips are readable

---

## Configuration File

### `/home/yousuf/PROJECTS/PeopleNet/config.yaml`

```yaml
# PeopleNet Pipeline Configuration

# Detection Parameters
detection:
  confidence_threshold: 0.8  # 0.6 = too many false positives, 0.8 = high quality
  buffer_seconds: 1          # 4s = mostly empty clips, 1s = dense clips
  sample_rate_fps: 2         # Sample 2 frames per second

# Resource Limits
resources:
  gpu_workers: 3             # Parallel workers (RTX 4080 handles 3-4)
  staging_max_videos: 20     # Max videos in staging (prevents overflow)
  staging_min_videos: 10     # Refill when below this
  min_free_space_gb: 10      # Pause if free space < this

# Docker Configuration
docker:
  image: nvcr.io/nvidia/tensorrt:24.08-py3
  log_max_size: 50m          # Per log file
  log_max_files: 3           # Total = 150MB max

# Source Paths
sources:
  park_f: /media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV/Park_F
  park_r: /media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV/Park_R

# Output Paths
outputs:
  local: /home/yousuf/PROJECTS/PeopleNet/Outputs
  google_drive: /home/yousuf/GoogleDrive/PROJECTS/PeopleNet

# Date Filtering (net new only)
date_filter:
  enabled: true
  start_date: 2025-10-13  # Process only videos from this date onwards

# Backup Configuration
backup:
  auto_backup: true         # Automatically backup to Google Drive when done
  delete_local: true        # Delete local clips after successful backup
  verify_backup: true       # Verify all files copied before deleting

# Notification (optional)
notification:
  enabled: false
  email: your@email.com
```

---

## Master Pipeline Script

### `/home/yousuf/PROJECTS/PeopleNet/Scripts/master_pipeline.sh`

This is the **single script** that runs everything autonomously.

**Key Features:**
- ✅ Validates prerequisites (GPU, disk space, mounts)
- ✅ Creates date-filtered video lists
- ✅ Starts Docker with proper log rotation
- ✅ Manages controlled feed
- ✅ Auto-triggers next batch
- ✅ Backs up to Google Drive
- ✅ Generates final report
- ✅ Sends notification when complete

**Usage:**
```bash
# Process videos from Nov 14 onwards, auto-backup
./Scripts/master_pipeline.sh --start-date 2025-11-14 --auto-backup

# Process specific date range, no backup
./Scripts/master_pipeline.sh --start-date 2025-11-01 --end-date 2025-11-14 --no-backup

# Process only Park_F
./Scripts/master_pipeline.sh --batch park_f --start-date 2025-11-14
```

---

## Critical Gotchas & Solutions

### Problem 1: Docker Log Bloat
**Symptom:** System crashes with "No space left on device"
**Root Cause:** Docker logs grow unbounded without rotation
**Solution:**
```bash
# ALWAYS start containers with log rotation
docker run \
  --log-driver json-file \
  --log-opt max-size=50m \
  --log-opt max-file=3 \
  [other options]
```

### Problem 2: False Positive Detections
**Symptom:** Clips don't contain people
**Root Cause:** Confidence threshold too low (0.6)
**Solution:**
```python
# In worker.py
confidence_threshold=0.8  # Not 0.6!
```

### Problem 3: Clips Mostly Empty
**Symptom:** 8-second clips with only 0.5s of people
**Root Cause:** Buffer too large (4 seconds)
**Solution:**
```python
# In worker.py
buffer_seconds=1  # Not 4!
```

### Problem 4: Disk Overflow
**Symptom:** Crashes when copying all videos
**Root Cause:** Tried to copy 600+ videos (120GB) at once
**Solution:**
```bash
# Controlled feed - only 10-20 videos at a time
while true; do
  staging_count=$(find staging -name "*.MP4" | wc -l)
  if [ "$staging_count" -lt 10 ]; then
    copy_next_batch  # Copy only 10-20
  fi
done
```

### Problem 5: Files Not Accessible
**Symptom:** VLC can't open clips ("Permission denied")
**Root Cause:** Docker creates files as root
**Solution:**
```bash
# Auto-ownership fixer (runs every 30s)
while true; do
  sudo chown yousuf:yousuf Outputs/*/*.mp4
  sleep 30
done
```

### Problem 6: Processing Old Videos
**Symptom:** Processing July videos instead of recent ones
**Root Cause:** No date filtering
**Solution:**
```bash
# Filter by date (Oct 13 onwards)
find source/ -name "*.MP4" | grep -E "202510(1[3-9]|[2-3][0-9])|20251[1-2]"
```

---

## Monitoring & Debugging

### Check Progress
```bash
# Overall progress
./Scripts/monitor_progress.sh Park_F_Batch1

# Live worker logs (debug mode)
docker logs -f peoplenet-park_f_batch1

# Check specific worker
tail -f Outputs/Park_F_Batch1/worker_1_log.txt

# Analyze specific clip
docker exec peoplenet-park_f_batch1 python3 /workspace/Scripts/analyze_clip.py /workspace/Outputs/Park_F_Batch1/clip.mp4
```

### Verify Clip Quality
```bash
# Test clip with PeopleNet
./Scripts/analyze_clip.py Outputs/Park_F_Batch1/20251029051127_076702A_people_21-29s.mp4

# Should show:
# - Detection timestamps
# - Confidence scores (should be ≥0.8)
# - Person detected during ~50% of clip
```

### Check Space Usage
```bash
# Disk space
df -h /

# Docker space
docker system df

# Output size
du -sh Outputs/*/

# Staging size (should be <4GB)
du -sh Staging/*/
```

---

## Performance Metrics

### Expected Results
```
Input:  1,400 videos (240GB source)
Output: 650 clips (3.4GB)
Reduction: 98.6% data reduction
Detection Rate: 47% (varies by camera/time)
Duration: ~2 hours
```

### Processing Rates
```
Single Worker:  ~4 videos/min
3 Workers:      ~13 videos/min
Throughput:     ~780 videos/hour
```

### Detection Rates (Historical)
```
Park_F: 38.5% (269/698)
Park_R: 56.2% (393/699)
Overall: 47.4%

Note: Park_R higher because rear camera captures more pedestrians
```

---

## Backup & Cleanup Workflow

### Automated Backup (Recommended)
```bash
# Included in master_pipeline.sh with --auto-backup flag
./Scripts/master_pipeline.sh --start-date 2025-11-14 --auto-backup
```

**What happens:**
1. Processing completes
2. All clips copied to Google Drive
3. Backup verified (count matches)
4. Local clips deleted
5. 3.4GB freed

### Manual Backup
```bash
# If you want control over deletion
./Scripts/backup_to_gdrive.sh

# Script will:
# 1. Copy to Google Drive
# 2. Verify backup
# 3. ASK before deleting local files
```

### Verify Backup
```bash
# Check Google Drive
find ~/GoogleDrive/PROJECTS/PeopleNet -name "*.mp4" | wc -l
# Should match local count (662 clips)

# Check clip sizes match
du -sh ~/GoogleDrive/PROJECTS/PeopleNet/Park_F_Batch1/
du -sh Outputs/Park_F_Batch1/
```

---

## Next Time: Zero-Intervention Workflow

### 1. Update Configuration
```bash
# Edit config.yaml
nano config.yaml

# Set start_date to last processing date
date_filter:
  start_date: 2025-11-14  # Last run date
```

### 2. Run Master Script
```bash
./Scripts/master_pipeline.sh --auto-backup
```

### 3. Walk Away
- No monitoring needed
- No intervention required
- Returns when complete with clips in Google Drive

### 4. Review Results
```bash
# Check Google Drive
ls ~/GoogleDrive/PROJECTS/PeopleNet/Park_F_Latest/
ls ~/GoogleDrive/PROJECTS/PeopleNet/Park_R_Latest/

# Review summary
cat ~/GoogleDrive/PROJECTS/PeopleNet/REPORT_2025-11-14.txt
```

---

## Troubleshooting Decision Tree

```
Problem: Processing stopped/crashed
├─ Check disk space (df -h /)
│  └─ If <10GB free: Clean up or expand disk
├─ Check Docker logs (docker logs peoplenet-*)
│  └─ If logs huge (>100MB): Restart with log rotation
├─ Check GPU (nvidia-smi)
│  └─ If no GPU: Restart Docker container
└─ Check staging directory
   └─ If >50 videos: Clear staging, restart feed

Problem: Clips don't contain people
├─ Check confidence threshold (should be 0.8)
├─ Analyze clip (./Scripts/analyze_clip.py)
└─ If confidence <0.8: Increase threshold to 0.9

Problem: Clips mostly empty
├─ Check buffer_seconds (should be 1)
└─ Decrease to 0.5 for tighter clips

Problem: Can't open clips
├─ Check ownership (ls -l Outputs/*/*.mp4)
├─ Fix: sudo chown yousuf:yousuf Outputs/*/*.mp4
└─ Check codec: ffprobe clip.mp4
   └─ If HEVC issue: Install vlc-plugin-access-extra

Problem: Processing too slow
├─ Check GPU workers (should be 3)
├─ Check GPU utilization (nvidia-smi)
└─ Increase workers to 4 if GPU <80% utilized
```

---

## Why ChatGPT Failed (Lessons Learned)

**ChatGPT's Attempt:**
- ❌ No understanding of Docker log bloat issue
- ❌ Didn't implement controlled feed (tried to copy all videos)
- ❌ No date filtering (processed wrong videos)
- ❌ Didn't handle file ownership issues
- ❌ No auto-trigger for next batch
- ❌ Used wrong confidence threshold

**What Made This Work:**
- ✅ Understanding of full pipeline flow
- ✅ Iterative debugging and adjustment
- ✅ Space-aware controlled feed
- ✅ Proper Docker configuration
- ✅ Date filtering for net new detection
- ✅ Auto-trigger system for multiple batches
- ✅ Comprehensive error handling

**Key Insight:** This isn't a simple script - it's an orchestrated pipeline with multiple interdependent components that need careful tuning and monitoring.

---

## File Reference

### Keep These Files
```
PeopleNet/
├── worker.py                          # Core GPU worker (DO NOT DELETE)
├── model/resnet34_peoplenet_int8.onnx # AI model (8.4MB)
├── config.yaml                        # Configuration
├── Scripts/
│   ├── master_pipeline.sh             # Single command to run everything
│   ├── monitor_progress.sh            # Check progress
│   ├── analyze_clip.py                # Verify clip quality
│   ├── backup_to_gdrive.sh            # Manual backup
│   └── controlled_feed.sh             # Space-aware feed system
└── AUTONOMOUS_SETUP.md                # This file
```

### Can Delete After Completion
```
PeopleNet/
├── Outputs/*/                         # After backing up to Google Drive
├── Staging/*/                         # Always empty after completion
├── logs/                              # After reviewing for errors
├── park_*_process_list*.txt           # Temporary lists
└── Docker containers                  # docker rm peoplenet-*
```

---

## Summary: Autonomous Operation Checklist

- [ ] External drive mounted at `/media/yousuf/C67813AB7813996F1/`
- [ ] Google Drive mounted at `~/GoogleDrive/`
- [ ] GPU accessible (`nvidia-smi` works)
- [ ] Disk space >10GB free
- [ ] Configuration file updated (`config.yaml`)
- [ ] Master script exists (`Scripts/master_pipeline.sh`)

**Then:**
```bash
cd /home/yousuf/PROJECTS/PeopleNet
./Scripts/master_pipeline.sh --start-date YYYY-MM-DD --auto-backup
```

**Walk away. Return to:**
- ✅ All clips in Google Drive
- ✅ Local space freed
- ✅ Summary report generated
- ✅ Ready for next batch

---

**That's it. Next time = zero intervention required.**

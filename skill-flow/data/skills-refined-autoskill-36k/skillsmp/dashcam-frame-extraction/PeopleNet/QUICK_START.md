# PeopleNet Pipeline - Quick Start Guide

## What Was Fixed

### 1. **Docker Log Bloat** ✅
- **Problem:** Worker was printing every video to stdout → filled Docker logs with GB of data
- **Solution:** Modified `worker.py` to only log to files, print to stdout every 50 videos
- **Result:** Docker logs capped at 50MB × 3 files = 150MB max (was unlimited)

### 2. **Cleaned Up Old Files** ✅
- Deleted ~141MB of old outputs and stale logs
- Removed FrameExtraction directory (not needed for pipeline)
- Reset project to clean state

### 3. **Processing Pipeline Setup** ✅
- Created orchestration scripts with proper log rotation
- Set up staging/output directory structure
- Created monitoring and batch copy scripts

---

## Quick Commands

### Start Processing Pipeline

```bash
# For Park_F videos (3 GPU workers)
cd /home/yousuf/PROJECTS/PeopleNet
./Scripts/run_pipeline.sh Park_F_Batch1 3

# For Park_R videos (3 GPU workers)
./Scripts/run_pipeline.sh Park_R_Batch1 3
```

### Copy Videos to Staging (Space-Aware)

```bash
# Copy Park_F videos in batches of 20
./Scripts/batch_copy_to_staging.sh \
    park_f_process_list.txt \
    20 \
    /home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1 \
    10
```

### Monitor Progress

```bash
# Show progress summary
./Scripts/monitor_progress.sh Park_F_Batch1

# Watch live (updates every 5 seconds)
watch -n 5 ./Scripts/monitor_progress.sh Park_F_Batch1
```

### Check Docker Logs (Limited)

```bash
# View recent logs only
docker logs --tail 100 peoplenet-park_f_batch1

# Follow logs in real-time
docker logs -f peoplenet-park_f_batch1
```

---

## Current Status

### Available Videos (Parking Mode ONLY)

| Source | Total Videos | Filtered List | Status |
|--------|-------------|---------------|--------|
| Park_F | 3,152 videos | 1,792 (SSIM-filtered) | ✅ Ready |
| Park_R | 3,808 videos | ❌ Need SSIM filter | 🔴 Not ready |

**Note:** Movie_F videos are NOT processed through this pipeline. Only parking mode (Park_F/Park_R).

### Disk Space

- **Total:** 273GB
- **Used:** 125GB
- **Free:** 134GB (49%)
- **Safe for processing:** ✅ Yes (>10GB free)

### GPU

- **Model:** RTX 4080 SUPER
- **VRAM:** 16GB (14GB free)
- **Workers:** Can run 3-4 parallel workers

---

## Processing Strategy (Parking Mode Only)

### Phase 1: Park_F (Ready to Start)
- **Input:** 1,792 videos (already SSIM-filtered)
- **Expected Output:** ~665 clips (~25GB)
- **Duration:** ~2.5 hours @ 12 videos/min
- **Command:**
  ```bash
  ./Scripts/run_pipeline.sh Park_F_Batch1 3
  ./Scripts/batch_copy_to_staging.sh park_f_process_list.txt 20
  ```

### Phase 2: Park_R (Need SSIM Filter First)
- **Input:** 3,808 videos (need filtering)
- **Expected After Filter:** ~2,700 videos (70% pass rate)
- **Expected Output:** ~1,200 clips (~45GB)
- **Duration:** ~3.5 hours @ 12 videos/min
- **Prerequisites:** Run SSIM filter to create `park_r_process_list.txt`

**Note:** Movie mode videos (Movie_F/Movie_R) are NOT processed. This pipeline is exclusively for parking mode detection.

---

## Space Management

### Automatic Space Constraints

1. **Batch Copy Script:** Pauses when <10GB free
2. **Workers:** Delete source videos immediately after processing
3. **Docker Logs:** Auto-rotate at 50MB (max 150MB total)

### Manual Space Recovery

```bash
# Check staging directory size
du -sh /home/yousuf/PROJECTS/PeopleNet/Staging/*

# Delete processed videos from staging (workers do this automatically)
# Only needed if workers crashed mid-processing
find Staging/ -name "*.MP4" -delete

# Archive output clips to external drive
cp -r Outputs/Park_F_Batch1/*.mp4 /media/external/backups/
```

---

## Troubleshooting

### Workers Not Processing

```bash
# Check if container is running
docker ps | grep peoplenet

# Check worker logs
tail -f Outputs/Park_F_Batch1/worker_*.txt

# Restart pipeline
docker stop peoplenet-park_f_batch1
./Scripts/run_pipeline.sh Park_F_Batch1 3
```

### Docker Logs Still Growing

```bash
# Check current log size
du -sh /var/lib/docker/containers/*/

# Verify log rotation is active
docker inspect peoplenet-park_f_batch1 | grep -A5 LogConfig

# Should show:
# "MaxSize": "50m"
# "MaxFile": "3"
```

### Out of Disk Space

```bash
# Find what's using space
du -sh /home/yousuf/PROJECTS/* | sort -h

# Clean Docker system
docker system prune -a

# Archive and delete old outputs
tar -czf outputs_backup.tar.gz Outputs/Park_F_Batch1/*.mp4
rm Outputs/Park_F_Batch1/*.mp4
```

---

## Performance Metrics

### Expected Throughput

- **Single Worker:** ~4 videos/min (~15s per video)
- **3 Workers:** ~12 videos/min (parallel processing)
- **Daily Capacity:** ~17,000 videos/day (24/7 processing)

### Detection Rates (Historical)

- **Park_F:** 37% (665 clips from 1,792 videos)
- **Park_R:** ~46% (estimated from past runs)

---

## Next Steps

1. **Start Park_F Processing** (recommended - easiest to start)
   ```bash
   ./Scripts/run_pipeline.sh Park_F_Batch1 3
   ./Scripts/batch_copy_to_staging.sh park_f_process_list.txt 20
   ```

2. **Create Park_R Filter List** (needed before processing Park_R)
   - Run SSIM motion filter on 3,808 Park_R videos
   - Generate `park_r_process_list.txt`

3. **Monitor and Adjust**
   - Watch progress: `./Scripts/monitor_progress.sh Park_F_Batch1`
   - Check disk space: `df -h /`
   - Monitor GPU: `nvidia-smi -l 5`

---

**Ready to process! Start with Park_F since it already has a filtered list.**

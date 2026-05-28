# Revised Data Processing Strategy - CORRECT Data Location

## Executive Summary

**Date:** 2025-11-13
**Correct Data Location:** `/mnt/windows/Users/yousu/Desktop/CARDV/` (Windows partition)
**New Data Discovered:** 5,604 NEW videos (868GB) across 3 categories
**Processing Objective:** Extract people detection clips from all new dashcam footage
**Estimated Total Processing Time:** 18-24 hours (sequential processing required)
**Expected Output:** ~2,400-3,000 detection clips (~110-140GB)

---

## Data Inventory - CORRECTED

### Source Drive Status
**Location:** `/mnt/windows/Users/yousu/Desktop/CARDV/` (NTFS partition nvme0n1p3)
**Capacity:** 1.6TB total
**Used:** 1.6TB (100% FULL - only 5.2GB free)
**Total CARDV Data:** 1.4TB
**Status:** ⚠️ CRITICAL - Source drive is full, cannot use for staging

### Complete Inventory (All Videos on Desktop)

| Category | Total | Size | Already Processed | NEW | NEW Size | Status |
|----------|-------|------|-------------------|-----|----------|--------|
| Movie_F | 3,566 | 601GB | 0 (never processed) | **3,566** | **601GB** | 🆕 BRAND NEW |
| Park_F | 3,152 | 523GB | 1,792 (Batch 1) | **1,360** | **~232GB** | 🆕 Batch 2 |
| Park_R | 3,808 | 194GB | 3,130 (Batch 1) | **678** | **~35GB** | 🆕 Batch 2 |
| **TOTAL** | **10,526** | **1,318GB** | **4,922** | **5,604** | **~868GB** | |

### Video Categories - Detailed Analysis

#### 1. Movie_F (Front Camera - Driving Mode) - HIGHEST PRIORITY
- **Total Count:** 3,566 videos
- **Size:** 601GB
- **Date Range:** August 7 - October 28, 2025
- **Status:** BRAND NEW - Never processed before
- **Expected Detection Rate:** 50-60% (driving mode = high people interaction)
- **Priority:** HIGHEST (best ROI for people detection)
- **Expected Output:** ~1,780-2,140 clips (~80-95GB)

**Why Priority #1:**
- Continuous recording during driving = more people/pedestrians/traffic
- Front-facing camera captures sidewalks, crosswalks, storefronts
- Highest expected detection rate of all categories

#### 2. Park_F Batch 2 (Front Camera - Parked Mode)
- **Total on Desktop:** 3,152 videos (523GB)
- **Already Processed (Batch 1):** 1,792 videos (Jul 25 - Oct 13, 2025)
- **NEW Videos (Batch 2):** 1,360 videos (~232GB)
- **Date Range (NEW):** Jul 25 - Nov 13, 2025 (different times/events than Batch 1)
- **Expected Detection Rate:** 35-45% (based on Batch 1: 37.1%)
- **Priority:** MEDIUM
- **Expected Output:** ~475-610 clips (~20-26GB)

**Batch 1 Results for Comparison:**
- Processed: 1,792 videos → 665 clips (37.1% detection rate)
- Output: ~25GB

#### 3. Park_R Batch 2 (Rear Camera - Parked Mode)
- **Total on Desktop:** 3,808 videos (194GB)
- **Already Processed (Batch 1):** 3,130 videos (Aug-Sep 2025)
- **NEW Videos (Batch 2):** 678 videos (~35GB)
- **Date Range (NEW):** October 28 - November 13, 2025
- **Expected Detection Rate:** 40-50% (based on Batch 1: 46%)
- **Priority:** LOWER
- **Expected Output:** ~270-340 clips (~12-15GB)

**Batch 1 Results for Comparison:**
- Processed: 3,167 videos → 1,470 clips (46% detection rate)
- Output: ~60GB

### Note: Movie_R Not Found
The external drive showed Movie_R (1,523 videos, 79GB) but this category is **NOT present** on the Windows Desktop. Only Movie_F exists.

---

## Processing Infrastructure Status

### Available Resources
- **Processing Drive:** 88GB free on `/` (nvme0n1p6)
- **Effective Working Space:** 68GB (after 20GB buffer requirement)
- **GPU:** NVIDIA RTX 4080 SUPER (available, idle)
- **Containers:** peoplenet-park-f (exists, can reuse/adapt)
- **Model:** PeopleNet ResNet-34 INT8 (ready at /workspace/model/)
- **Workers:** 3 GPU workers optimal configuration (proven)
- **Processing Speed:** 70-75 videos/minute (with optimized batch copy)

### Critical Constraints
1. **Source Drive:** 100% full (5.2GB free) - Cannot use for staging
2. **Processing Drive:** Only 68GB effective space vs 868GB source data
3. **Sequential Processing:** ABSOLUTELY REQUIRED - cannot fit everything at once
4. **Batch Processing:** CRITICAL - must copy in 50-video batches with space monitoring
5. **SSIM Filtering:** ESSENTIAL - reduces volume by 25-30% before GPU processing

---

## Comprehensive Processing Strategy

### Strategy Overview

**Key Principle:** Process ONE category at a time, archive outputs, clear staging, repeat

**Why Sequential:**
- Movie_F alone (601GB) exceeds available processing space (68GB)
- After SSIM filtering: ~450GB still too large
- Must copy in batches, process, extract clips, delete source batches
- Archive outputs between categories if space < 30GB

### Phase 1: SSIM Motion Filtering (REQUIRED FIRST STEP)

**Objective:** Reduce 5,604 videos to ~4,200 videos (25% reduction)

**Why SSIM First:**
- Removes static/no-motion videos (especially in Park categories)
- Saves GPU processing time
- Reduces batch copy operations
- Filtering happens on source drive (read-only, safe)

**Process Per Category:**
```bash
# Movie_F (largest priority)
python3 /tmp/ssim_filter.py \
    "/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F" \
    /home/yousuf/PROJECTS/PeopleNet/movie_f_process_list.txt \
    0.85

# Park_F Batch 2 (only NEW videos)
# First, create list of NEW videos only
comm -23 \
    <(find "/mnt/windows/Users/yousu/Desktop/CARDV/Park_F" -name "*.MP4" -printf "%f\n" | sort) \
    <(cat /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt | sort) \
    > /home/yousuf/PROJECTS/PeopleNet/park_f_batch2_new_videos.txt

# Then run SSIM on NEW videos only
python3 /tmp/ssim_filter_from_list.py \
    "/mnt/windows/Users/yousu/Desktop/CARDV/Park_F" \
    /home/yousuf/PROJECTS/PeopleNet/park_f_batch2_new_videos.txt \
    /home/yousuf/PROJECTS/PeopleNet/park_f_batch2_process_list.txt \
    0.85

# Park_R Batch 2 (only NEW videos)
comm -23 \
    <(find "/mnt/windows/Users/yousu/Desktop/CARDV/Park_R" -name "*.MP4" -printf "%f\n" | sort) \
    <(cat /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt | sort) \
    > /home/yousuf/PROJECTS/PeopleNet/park_r_batch2_new_videos.txt

python3 /tmp/ssim_filter_from_list.py \
    "/mnt/windows/Users/yousu/Desktop/CARDV/Park_R" \
    /home/yousuf/PROJECTS/PeopleNet/park_r_batch2_new_videos.txt \
    /home/yousuf/PROJECTS/PeopleNet/park_r_batch2_process_list.txt \
    0.85
```

**Expected SSIM Results:**
- Movie_F: 3,566 → ~3,030 videos (85% pass rate - driving = more motion)
- Park_F Batch 2: 1,360 → ~1,020 videos (75% pass - some static)
- Park_R Batch 2: 678 → ~510 videos (75% pass)
- **Total After SSIM:** ~4,560 videos (reduction of ~1,044 videos)

**Time Required:** 12-16 hours (SSIM is CPU-intensive, can run overnight)

---

### Phase 2: Sequential GPU Processing

**Processing Order:** Movie_F → Park_F Batch 2 → Park_R Batch 2

#### Category 1: Movie_F (Priority 1)

**Videos to Process:** ~3,030 (after SSIM)
**Source:** `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F`
**Output Directory:** `/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Movie_F/`
**Expected Processing Time:** ~40 minutes
**Expected Output:** ~1,820 clips (~82GB)

**Setup Steps:**
1. Create output directory structure
2. Setup Docker container (reuse peoplenet-park-f or create peoplenet-movie-f)
3. **VERIFY ffmpeg installed** (CRITICAL - learned from Park_F Batch 1)
4. Deploy GPU worker script with correct paths
5. Deploy batch copy agent (batch size 50, 5s interval, 20GB buffer)
6. Start 3 GPU workers

**Container Setup:**
```bash
# Option 1: Reuse existing container
docker restart peoplenet-park-f
docker exec peoplenet-park-f which ffmpeg  # VERIFY ffmpeg exists

# Option 2: Create new dedicated container
docker run -d --name peoplenet-movie-f \
    --gpus all --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# Install ffmpeg (MANDATORY)
docker exec peoplenet-movie-f apt-get update
docker exec peoplenet-movie-f apt-get install -y ffmpeg
docker exec peoplenet-movie-f which ffmpeg  # Verify
```

**Worker Configuration:**
```python
# Key paths for Movie_F
SOURCE_BASE = "/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F"
VIDEO_LIST = "/workspace/movie_f_process_list.txt"
STAGING_DIR = "/workspace/Staging/Movie_F/"
OUTPUT_BASE = "/workspace/Outputs/GPU_Pipeline_Movie_F"
PROCESSED_LIST = OUTPUT_BASE + "/processed_videos.txt"
MODEL_PATH = "/workspace/model/resnet34_peoplenet_int8.onnx"
CONFIDENCE_THRESHOLD = 0.6
BUFFER_SECONDS = 4
```

**Batch Copy Agent:**
```bash
BATCH_SIZE=50
MIN_FREE_GB=20
CHECK_INTERVAL=5
MIN_STAGING_THRESHOLD=20
SOURCE_DIR="/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/Movie_F"
PROCESS_LIST="/home/yousuf/PROJECTS/PeopleNet/movie_f_process_list.txt"
```

**Monitoring:**
```bash
# Progress
watch -n 5 'wc -l /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Movie_F/processed_videos.txt'

# Clips created (should be >0 within 3 minutes - ffmpeg check!)
watch -n 10 'ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Movie_F/*.mp4 2>/dev/null | wc -l'

# Disk space (maintain >20GB)
watch -n 10 'df -h / | grep nvme0n1p6'

# GPU utilization
watch -n 5 nvidia-smi
```

**Success Criteria:**
- [ ] All ~3,030 videos processed
- [ ] Detection rate 50-60% (~1,820 clips)
- [ ] Disk space maintained >20GB throughout
- [ ] No worker errors/crashes
- [ ] ffmpeg working (clips created, not just "No people" logs)

**Post-Processing:**
- Verify completion (processed count matches filter list)
- Calculate detection rate
- **Archive outputs if needed** (if total clips > 50GB and next category planned)

---

#### Category 2: Park_F Batch 2 (Priority 2)

**Videos to Process:** ~1,020 (after SSIM)
**Source:** `/mnt/windows/Users/yousu/Desktop/CARDV/Park_F` (NEW videos only)
**Output Directory:** `/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch2/`
**Expected Processing Time:** ~15 minutes
**Expected Output:** ~410 clips (~18GB)

**Key Difference from Batch 1:**
- Batch 1 processed: 1,792 videos (Jul 25 - Oct 13)
- Batch 2 will process: 1,360 NEW videos (different times/events, extends to Nov 13)
- Process list already filtered to exclude Batch 1 videos

**Setup:**
- Reuse peoplenet-park-f container (already has ffmpeg from Batch 1)
- Update paths to Batch2 output directory
- Clear staging from previous category
- Reset processed_videos.txt to 0

**Post-Processing:**
- Compare Batch 2 detection rate with Batch 1 (37.1%)
- Archive if needed before Park_R Batch 2

---

#### Category 3: Park_R Batch 2 (Priority 3)

**Videos to Process:** ~510 (after SSIM)
**Source:** `/mnt/windows/Users/yousu/Desktop/CARDV/Park_R` (NEW videos only)
**Output Directory:** `/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch2/`
**Expected Processing Time:** ~7 minutes
**Expected Output:** ~255 clips (~11GB)

**Key Difference from Batch 1:**
- Batch 1 processed: 3,130 videos (Aug-Sep)
- Batch 2 will process: 678 NEW videos (Oct 28 - Nov 13)
- Process list already filtered to exclude Batch 1 videos

**Setup:**
- Can reuse existing container
- Update paths to Batch2 output directory
- Clear staging
- Reset processed_videos.txt

**Final Completion:**
- Verify all categories processed
- Calculate total detection rate across all categories
- Archive all outputs
- Document results

---

## Expected Outcomes

### Conservative Estimate
- Movie_F: 50% detection → 1,515 clips (~68GB)
- Park_F Batch 2: 35% detection → 357 clips (~16GB)
- Park_R Batch 2: 40% detection → 204 clips (~9GB)
- **Total: 2,076 clips (~93GB)**

### Realistic Estimate
- Movie_F: 55% detection → 1,667 clips (~75GB)
- Park_F Batch 2: 40% detection → 408 clips (~18GB)
- Park_R Batch 2: 45% detection → 230 clips (~10GB)
- **Total: 2,305 clips (~103GB)**

### Optimistic Estimate
- Movie_F: 60% detection → 1,818 clips (~82GB)
- Park_F Batch 2: 45% detection → 459 clips (~20GB)
- Park_R Batch 2: 50% detection → 255 clips (~11GB)
- **Total: 2,532 clips (~113GB)**

---

## Disk Space Management

### Challenge
- Available: 68GB effective
- Source: 868GB
- Cannot fit even one category after SSIM (Movie_F ~450GB)

### Solution: Batch Copy with Continuous Deletion

**How It Works:**
1. Batch copy agent copies 50 videos to staging (~10-12GB for Movie_F)
2. GPU workers process videos from staging
3. **Workers DELETE video from staging after processing** (critical!)
4. Space freed immediately, copy agent copies next batch
5. Clips accumulate in output directory
6. Repeat until all videos processed

**Space Requirements Per Category:**
- Movie_F: ~12GB staging (rolling), ~82GB output = ~94GB peak ❌ TOO MUCH
- **Solution:** Archive Movie_F clips before starting Park_F Batch 2

**Revised Approach:**
1. Process Movie_F completely (~82GB output)
2. **Move/compress Movie_F clips** to free space
3. Process Park_F Batch 2 (~18GB output)
4. Process Park_R Batch 2 (~11GB output)
5. Final total on drive: ~29GB (or ~111GB if no archiving between)

**Archive Options:**
- Compress clips: `tar -czf movie_f_clips.tar.gz GPU_Pipeline_Movie_F/*.mp4`
- Move to external: `rsync -avh --remove-source-files GPU_Pipeline_Movie_F/ /media/external/`
- Temporary move to Windows partition (5.2GB free - not viable)

---

## Risk Mitigation

### Risk 1: Disk Space Overflow (HIGH)
**Probability:** HIGH (Movie_F output alone may exceed available space)
**Impact:** Pipeline stops, partial processing

**Mitigation:**
- Monitor disk space every 100 videos
- Emergency stop if space < 25GB
- Archive Movie_F outputs before starting next category
- Compress if needed: ~50% reduction possible

### Risk 2: Source Drive Full (MEDIUM)
**Probability:** MEDIUM (Windows drive 100% full)
**Impact:** Cannot create temp files on source, read errors possible

**Mitigation:**
- All staging on processing drive (never write to source)
- Read-only operations on Windows partition
- Monitor for I/O errors during batch copy

### Risk 3: Processing Interruption (MEDIUM)
**Probability:** MEDIUM (18-24 hour total runtime)
**Impact:** Partial completion, need to resume

**Mitigation:**
- processed_videos.txt tracks progress (auto-resume)
- Batch copy agent skips already-processed videos
- Workers auto-skip videos in processed list
- Can restart at any point without data loss

### Risk 4: ffmpeg Missing (LOW - Already Learned)
**Probability:** LOW (we know to check now)
**Impact:** No clips created, false "No people" results

**Mitigation:**
- **MANDATORY:** Verify ffmpeg before starting workers
- Spot-check first 5 videos within 3 minutes
- If no clips created, STOP immediately and install ffmpeg

### Risk 5: Lower Detection Rates Than Expected (LOW)
**Probability:** LOW (Movie_F should have high rates)
**Impact:** Fewer clips than expected

**Mitigation:**
- Movie_F driving mode should yield 50-60% (high traffic/pedestrians)
- If Movie_F < 30%, review confidence threshold (0.6 → 0.5)
- Park categories already proven (Batch 1 results: 37-46%)

---

## Resource Requirements Summary

### Time Investment
- SSIM Filtering: 12-16 hours (can run overnight, unattended)
- GPU Processing: ~62 minutes total (Movie_F 40m + Park_F 15m + Park_R 7m)
- Setup/Monitoring: 3-4 hours
- Archiving Between Categories: 1-2 hours
- **Total Elapsed Time:** 18-24 hours (most is automated overnight SSIM)

### Disk Space Journey
- Start: 88GB free
- During Movie_F: ~12GB staging + 0-82GB output (rolling accumulation)
- Peak: ~94GB used (may exceed available!)
- **Archive Movie_F:** Compress/move to free ~70GB
- During Park_F Batch 2: ~18GB output
- During Park_R Batch 2: ~11GB output
- End: ~29GB total output (if archived) OR ~111GB (if kept all)

### Processing Power
- GPU: < 10% utilization (very efficient TensorRT INT8)
- CPU: 80-100% during SSIM filtering (12-16 hours)
- CPU: 20-30% during GPU processing (batch copy + workers)
- RAM: ~10GB peak (3 workers + batch agent + system)
- Network: None (all local drives)

---

## Execution Checklist

### Pre-Processing Verification
- [ ] Windows partition mounted: `/mnt/windows` (nvme0n1p3)
- [ ] CARDV folder accessible: `/mnt/windows/Users/yousu/Desktop/CARDV/`
- [ ] Processing drive space: ≥88GB free
- [ ] PeopleNet model exists: `/home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx`
- [ ] SSIM filter script ready: `/tmp/ssim_filter.py`
- [ ] GPU worker script ready: `/tmp/gpu_worker_continuous.py`
- [ ] Create NEW video lists (Park_F Batch 2, Park_R Batch 2)

### Phase 1: SSIM Filtering (12-16 hours)
- [ ] Run SSIM filter on Movie_F → movie_f_process_list.txt
- [ ] Create Park_F Batch 2 NEW video list (exclude Batch 1)
- [ ] Run SSIM filter on Park_F Batch 2 → park_f_batch2_process_list.txt
- [ ] Create Park_R Batch 2 NEW video list (exclude Batch 1)
- [ ] Run SSIM filter on Park_R Batch 2 → park_r_batch2_process_list.txt
- [ ] Verify all filter lists created and counts match expected
- [ ] Review SSIM pass rates (should be 75-85%)

### Phase 2: Movie_F Processing (~40 min + setup)
- [ ] Create output directory: `Outputs/GPU_Pipeline_Movie_F/`
- [ ] Setup Docker container (reuse or create new)
- [ ] **VERIFY ffmpeg installed:** `docker exec [container] which ffmpeg`
- [ ] Deploy GPU worker script (update paths for Movie_F)
- [ ] Deploy batch copy agent (source: Windows Desktop Movie_F)
- [ ] Start 3 GPU workers: `python3 /tmp/gpu_worker_continuous.py 0/1/2`
- [ ] Start batch copy agent: `bash /tmp/movie_f_batch_copy.sh &`
- [ ] **Monitor first 3 minutes:** Verify clips being created (ffmpeg working!)
- [ ] Monitor disk space (maintain >20GB)
- [ ] Let run to completion (~40 minutes)
- [ ] Verify completion: processed count = filter list count
- [ ] Calculate detection rate
- [ ] **Archive outputs:** Compress or move Movie_F clips to free space
- [ ] Clear staging directory
- [ ] Stop workers

### Phase 3: Park_F Batch 2 Processing (~15 min + setup)
- [ ] Create output directory: `Outputs/GPU_Pipeline_Park_F_Batch2/`
- [ ] Update worker script paths (Park_F Batch2)
- [ ] Update batch copy agent (source: Windows Desktop Park_F, list: Batch2)
- [ ] Start 3 GPU workers
- [ ] Start batch copy agent
- [ ] Monitor for first 3 minutes
- [ ] Let run to completion
- [ ] Verify completion
- [ ] Compare detection rate with Batch 1 (37.1%)
- [ ] Archive if needed
- [ ] Clear staging

### Phase 4: Park_R Batch 2 Processing (~7 min + setup)
- [ ] Create output directory: `Outputs/GPU_Pipeline_Park_R_Batch2/`
- [ ] Update worker script paths (Park_R Batch2)
- [ ] Update batch copy agent (source: Windows Desktop Park_R, list: Batch2)
- [ ] Start 3 GPU workers
- [ ] Start batch copy agent
- [ ] Monitor for first 3 minutes
- [ ] Let run to completion
- [ ] Verify completion
- [ ] Compare detection rate with Batch 1 (46%)
- [ ] Archive final outputs

### Post-Processing
- [ ] Verify total videos processed: 4,560 (after SSIM)
- [ ] Verify total clips created: 2,000-2,500 expected
- [ ] Calculate overall detection rate: ~45-55% expected
- [ ] Document final results (detection rates per category)
- [ ] Archive all outputs to long-term storage
- [ ] Update this strategy document with actual results
- [ ] Clean up temporary files and staging directories
- [ ] Unmount Windows partition if needed: `sudo umount /mnt/windows`

---

## Key Differences from Original Strategy

### What Changed
1. **Data Location:** Windows Desktop (1.4TB) instead of external drive (478GB)
2. **Data Volume:** 5,604 NEW videos (868GB) instead of 4,401 (478GB)
3. **Movie_R Missing:** Only Movie_F exists (no Movie_R on Desktop)
4. **Park Categories:** Batch 2 for both (not full reprocess - NEW videos only)
5. **Overlap Detection:** 4,922 videos already processed, correctly excluded
6. **Space Constraints:** Even tighter (Movie_F alone 601GB vs 68GB available)

### Critical Lessons Applied
✅ **ALWAYS verify ffmpeg** before starting workers
✅ **Batch size 50** with 5-second check intervals (not 10/30)
✅ **Maintain 20GB buffer** religiously
✅ **Delete from staging** after processing (workers handle this)
✅ **Sequential processing** one category at a time
✅ **Archive between categories** if output exceeds 50GB
✅ **Verify clips created** within first 3 minutes (ffmpeg check)
✅ **Mount Windows partition** correctly to access Desktop data

---

## Commands Quick Reference

### Mount Windows Partition
```bash
sudo mkdir -p /mnt/windows
sudo mount -t ntfs-3g /dev/nvme0n1p3 /mnt/windows
df -h /mnt/windows  # Verify
```

### Create NEW Video Lists (Exclude Already Processed)
```bash
# Park_F Batch 2 (NEW only)
comm -23 \
    <(find "/mnt/windows/Users/yousu/Desktop/CARDV/Park_F" -name "*.MP4" -printf "%f\n" | sort) \
    <(cat /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt | sort) \
    > /home/yousuf/PROJECTS/PeopleNet/park_f_batch2_new_videos.txt

# Park_R Batch 2 (NEW only)
comm -23 \
    <(find "/mnt/windows/Users/yousu/Desktop/CARDV/Park_R" -name "*.MP4" -printf "%f\n" | sort) \
    <(cat /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt | sort) \
    > /home/yousuf/PROJECTS/PeopleNet/park_r_batch2_new_videos.txt
```

### SSIM Filtering
```bash
# Movie_F (all videos - never processed before)
python3 /tmp/ssim_filter.py \
    "/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F" \
    /home/yousuf/PROJECTS/PeopleNet/movie_f_process_list.txt \
    0.85

# Park_F Batch 2 (requires modified SSIM script to work from list)
# Park_R Batch 2 (requires modified SSIM script to work from list)
# See Phase 1 for details
```

### Monitoring
```bash
# Overall progress
watch -n 5 'wc -l /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_*/processed_videos.txt'

# Clips created (CRITICAL - verifies ffmpeg working)
watch -n 10 'find /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_*/ -name "*.mp4" | wc -l'

# Disk space (CRITICAL - maintain >20GB)
watch -n 10 'df -h / | grep nvme0n1p6'

# GPU workers active
nvidia-smi

# Staging directory size (should stay ~10-15GB)
watch -n 10 'du -sh /home/yousuf/PROJECTS/PeopleNet/Staging/*'
```

---

## Next Immediate Actions

**Ready to proceed with:**
1. Start SSIM filtering (can run overnight - 12-16 hours unattended)
2. While SSIM runs: Prepare worker scripts and batch copy agents
3. After SSIM complete: Begin Movie_F processing (highest priority)
4. Sequential processing through all categories
5. Archive and document final results

**Waiting for your approval to:**
- Confirm processing all 3 categories (Movie_F, Park_F Batch2, Park_R Batch2)
- Or process subset (e.g., Movie_F only for quick high-ROI results)
- Start SSIM filtering (longest step)

---

**Strategy Status:** READY TO EXECUTE
**Data Verified:** ✅ Correct location found and inventoried
**Infrastructure:** ✅ GPU, model, scripts ready
**Estimated Completion:** 18-24 hours from start
**Expected Output:** ~2,300 clips (~103GB)

---

**Document Version:** 2.0 (Corrected - Windows Desktop data)
**Previous Version:** 1.0 (Incorrect - External drive data)
**Last Updated:** 2025-11-13

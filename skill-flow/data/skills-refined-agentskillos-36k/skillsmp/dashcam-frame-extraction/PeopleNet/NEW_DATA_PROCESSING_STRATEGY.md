# New Data Processing Strategy - Comprehensive Plan

## Executive Summary

**Date:** 2025-11-13
**New Data Discovered:** 4,401 videos (478GB) across 4 categories
**Processing Objective:** Extract people detection clips from all new dashcam footage
**Estimated Total Processing Time:** 12-16 hours
**Expected Output:** ~1,800-2,200 detection clips (~75-100GB)

---

## Data Inventory

### Source Drive Status
**Location:** `/media/yousuf/0181-7924/CARDV/`
**Capacity:** 477GB total
**Used:** 476GB (100% FULL)
**Status:** ⚠️ CRITICAL - Drive is full, cannot add more data

### Video Categories

#### 1. Movie_F (Front Camera - Driving Mode)
- **Count:** 1,523 videos
- **Size:** 255GB
- **Date Range:** October 24 - November 13, 2025
- **Status:** BRAND NEW - Never processed
- **Expected Detection Rate:** 50-60% (driving mode = more people)
- **Priority:** HIGH (most people activity expected)

#### 2. Movie_R (Rear Camera - Driving Mode)
- **Count:** 1,523 videos
- **Size:** 79GB
- **Date Range:** Similar to Movie_F
- **Status:** BRAND NEW - Never processed
- **Expected Detection Rate:** 30-40% (rear view, less people)
- **Priority:** MEDIUM

#### 3. Park_F (Front Camera - Parked Mode)
- **Count:** 677 videos
- **Size:** 110GB
- **Date Range:** October 28 - November 13, 2025
- **Status:** NEW - No overlap with previously processed (Jul 25 - Oct 13)
- **Expected Detection Rate:** 35-45% (based on previous Park_F: 37.1%)
- **Priority:** MEDIUM

#### 4. Park_R (Rear Camera - Parked Mode)
- **Count:** 678 videos
- **Size:** 34GB
- **Date Range:** Similar to Park_F
- **Status:** NEW - Different from previously processed
- **Expected Detection Rate:** 40-50% (based on previous Park_R: 46%)
- **Priority:** LOW (least likely to have people)

### Previously Completed Work
- **Park_R:** 3,167 videos processed (Jul-Oct 2025) → 1,470 clips (46% detection)
- **Park_F:** 1,792 videos processed (Jul 25 - Oct 13) → 665 clips (37.1% detection)
- **Total:** 4,959 videos → 2,135 clips (~85GB output)

---

## Processing Infrastructure Status

### Available Resources
- **Processing Drive:** 87GB free (67GB effective after 20GB buffer)
- **GPU:** NVIDIA RTX 4080 SUPER (available, idle)
- **Containers:** peoplenet-park-r, peoplenet-park-f (existing, can reuse)
- **Model:** PeopleNet ResNet-34 INT8 (ready)
- **Workers:** 3 GPU workers optimal configuration
- **Processing Speed:** 70-75 videos/minute (optimized)

### Critical Constraints
1. **Disk Space:** Only 87GB free, need 20GB buffer → 67GB working space
2. **Source Drive:** 100% full, cannot use for processing
3. **Batch Processing:** REQUIRED due to space constraints
4. **SSIM Filtering:** ESSENTIAL to reduce volume by ~30%

---

## Comprehensive Processing Strategy

### Phase 1: SSIM Motion Filtering (Required First Step)

**Objective:** Reduce 4,401 videos to ~3,080 videos (30% reduction)

**Process:**
1. Run SSIM filter on each category separately
2. Create filtered lists (only videos with motion)
3. Expected pass rates (based on previous):
   - Movie videos: 80-85% (driving = more motion)
   - Park videos: 70-75% (some parked = static)

**Estimated Results:**
- Movie_F: 1,523 → ~1,290 videos (85% pass)
- Movie_R: 1,523 → ~1,290 videos (85% pass)
- Park_F: 677 → ~500 videos (75% pass)
- Park_R: 678 → ~500 videos (75% pass)
- **Total:** 4,401 → ~3,580 videos

**Time Required:** 8-12 hours (SSIM is CPU-intensive)

**Commands:**
```bash
# Movie_F
python3 /tmp/ssim_filter.py \
    "/media/yousuf/0181-7924/CARDV/Movie_F" \
    /home/yousuf/PROJECTS/PeopleNet/movie_f_process_list.txt \
    0.85

# Movie_R
python3 /tmp/ssim_filter.py \
    "/media/yousuf/0181-7924/CARDV/Movie_R" \
    /home/yousuf/PROJECTS/PeopleNet/movie_r_process_list.txt \
    0.85

# Park_F (new batch)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/0181-7924/CARDV/Park_F" \
    /home/yousuf/PROJECTS/PeopleNet/park_f_batch2_process_list.txt \
    0.85

# Park_R (new batch)
python3 /tmp/ssim_filter.py \
    "/media/yousuf/0181-7924/CARDV/Park_R" \
    /home/yousuf/PROJECTS/PeopleNet/park_r_batch2_process_list.txt \
    0.85
```

---

### Phase 2: Processing Priority Order

**Order Based On:**
1. Expected people detection rate (ROI)
2. Disk space management
3. Processing efficiency

**Recommended Order:**

#### Priority 1: Movie_F (Highest ROI)
- **Why First:** Driving mode = most people interactions
- **Videos:** ~1,290 (after SSIM)
- **Expected Output:** ~650-775 clips (~30-35GB)
- **Processing Time:** ~18 minutes
- **Detection Rate:** 50-60% expected

#### Priority 2: Movie_R
- **Videos:** ~1,290 (after SSIM)
- **Expected Output:** ~390-515 clips (~18-23GB)
- **Processing Time:** ~18 minutes
- **Detection Rate:** 30-40% expected

#### Priority 3: Park_F Batch 2
- **Videos:** ~500 (after SSIM)
- **Expected Output:** ~175-225 clips (~8-10GB)
- **Processing Time:** ~7 minutes
- **Detection Rate:** 35-45% expected

#### Priority 4: Park_R Batch 2 (Lowest Priority)
- **Videos:** ~500 (after SSIM)
- **Expected Output:** ~200-250 clips (~9-11GB)
- **Processing Time:** ~7 minutes
- **Detection Rate:** 40-50% expected

**Total Estimated:**
- **Videos to Process:** ~3,580 (after SSIM)
- **Processing Time:** ~50 minutes for GPU processing
- **Total Time:** 10-14 hours (including SSIM filtering)
- **Expected Output:** ~1,415-1,765 clips (~65-79GB)

---

### Phase 3: Disk Space Management Strategy

**Challenge:** 67GB effective space, but total output could be 65-79GB

**Solution: Sequential Processing with Cleanup**

**Approach:**
1. Process ONE category completely at a time
2. Archive/move completed clips before starting next category
3. Clear staging between categories

**Detailed Steps Per Category:**

1. **Run SSIM filter** → Create process list
2. **Setup output directory** → Create locks, tracking files
3. **Start GPU workers** (3 workers)
4. **Start batch copy agent** (batch size 50, 20GB buffer)
5. **Monitor until complete**
6. **Archive outputs** → Move clips to external storage OR compress
7. **Clear staging and locks**
8. **Repeat for next category**

**Space Requirements Per Category:**
- Movie_F: ~15GB staging max, ~35GB output = 50GB peak
- Movie_R: ~10GB staging max, ~23GB output = 33GB peak
- Park_F Batch2: ~8GB staging max, ~10GB output = 18GB peak
- Park_R Batch2: ~5GB staging max, ~11GB output = 16GB peak

All within 67GB effective space! ✅

---

### Phase 4: Container and Worker Configuration

**Reuse Existing Containers:**
- `peoplenet-park-r` → Rename or create `peoplenet-movie-r`
- `peoplenet-park-f` → Rename or create `peoplenet-movie-f`

OR

**Create New Containers for Movie Categories:**

```bash
# Movie_F container
docker run -d \
    --name peoplenet-movie-f \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# Install ffmpeg (CRITICAL)
docker exec peoplenet-movie-f apt-get update
docker exec peoplenet-movie-f apt-get install -y ffmpeg

# Movie_R container
docker run -d \
    --name peoplenet-movie-r \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

docker exec peoplenet-movie-r apt-get update
docker exec peoplenet-movie-r apt-get install -y ffmpeg
```

**Worker Script Updates:**
- Update paths for each category (Movie_F, Movie_R, Park_F_Batch2, Park_R_Batch2)
- All other settings remain the same (confidence 0.6, buffer 4s)

---

### Phase 5: Monitoring and Validation

**Per-Category Monitoring:**

```bash
# Progress check
wc -l /path/to/processed_videos.txt

# Clips created
ls /path/to/outputs/*.mp4 | wc -l

# Detection rate
echo "scale=1; $(ls /path/to/outputs/*.mp4 | wc -l) * 100 / $(wc -l < /path/to/processed_videos.txt)" | bc

# Disk space
df -h /home/yousuf/PROJECTS/PeopleNet

# GPU workers
nvidia-smi
```

**Success Criteria Per Category:**
- [ ] All videos in filter list processed
- [ ] Detection rate within expected range (30-60%)
- [ ] No errors in worker logs
- [ ] Disk space buffer maintained (>20GB)
- [ ] ffmpeg working (clips created, not just "No people")

---

## Risk Mitigation

### Risk 1: Disk Space Overflow
**Mitigation:**
- Process one category at a time
- Monitor space every 100 videos
- Emergency stop if space < 25GB
- Archive outputs before starting next category

### Risk 2: Source Drive Failure
**Mitigation:**
- Source drive is 100% full (risky)
- Copy filtered lists immediately after SSIM
- Consider backing up CARDV data to another drive

### Risk 3: Processing Interruption
**Mitigation:**
- processed_videos.txt tracks completion
- Can resume from interruption
- Staging videos auto-deleted after processing

### Risk 4: ffmpeg Missing
**Mitigation:**
- Verify ffmpeg installed BEFORE starting workers
- Check clips being created in first 3 minutes
- Mandatory verification step in each phase

### Risk 5: Lower Detection Rates
**Mitigation:**
- Movie videos should have HIGHER rates than Park
- If detection rate < 20%, review confidence threshold
- May need to adjust from 0.6 to 0.5

---

## Expected Outcomes

### Optimistic Scenario (High Detection Rates)
- Movie_F: 60% → 775 clips (~35GB)
- Movie_R: 40% → 515 clips (~23GB)
- Park_F B2: 45% → 225 clips (~10GB)
- Park_R B2: 50% → 250 clips (~11GB)
- **Total: 1,765 clips (~79GB)**

### Conservative Scenario (Lower Detection Rates)
- Movie_F: 50% → 645 clips (~29GB)
- Movie_R: 30% → 387 clips (~17GB)
- Park_F B2: 35% → 175 clips (~8GB)
- Park_R B2: 40% → 200 clips (~9GB)
- **Total: 1,407 clips (~63GB)**

### Realistic Scenario (Expected)
- Movie_F: 55% → 710 clips (~32GB)
- Movie_R: 35% → 450 clips (~20GB)
- Park_F B2: 40% → 200 clips (~9GB)
- Park_R B2: 45% → 225 clips (~10GB)
- **Total: 1,585 clips (~71GB)**

---

## Resource Requirements Summary

### Time Investment
- SSIM Filtering: 10-12 hours (can run overnight)
- GPU Processing: ~50 minutes total (all categories)
- Setup/Monitoring: 2-3 hours
- **Total: 12-16 hours elapsed time**

### Disk Space Journey
- Start: 87GB free
- Peak usage: ~50GB (during Movie_F processing)
- End: ~10-15GB free (after all categories)
- **Requires archiving between categories if space < 30GB**

### Processing Power
- GPU: < 10% utilization (very efficient)
- CPU: 80-100% during SSIM filtering
- RAM: ~8GB during GPU processing
- Network: None (all local)

---

## Execution Checklist

### Pre-Processing
- [ ] Verify source drive accessible: `/media/yousuf/0181-7924/CARDV/`
- [ ] Check processing drive space: 87GB free minimum
- [ ] Verify PeopleNet model exists
- [ ] Backup existing processed_videos.txt files
- [ ] Create new output directories for each category

### SSIM Phase
- [ ] Run SSIM filter on Movie_F
- [ ] Run SSIM filter on Movie_R
- [ ] Run SSIM filter on Park_F Batch2
- [ ] Run SSIM filter on Park_R Batch2
- [ ] Verify all filter lists created
- [ ] Review pass rates (should be 70-85%)

### GPU Processing Phase (Per Category)
- [ ] Create/configure Docker container
- [ ] Install ffmpeg in container
- [ ] Deploy worker script with correct paths
- [ ] Start 3 GPU workers
- [ ] Start batch copy agent
- [ ] Monitor for 3 minutes (verify clips created)
- [ ] Let run to completion
- [ ] Verify completion (all videos processed)
- [ ] Archive outputs
- [ ] Clear staging and locks

### Post-Processing
- [ ] Verify total clips created matches estimates
- [ ] Check detection rates per category
- [ ] Archive all outputs to external storage
- [ ] Update documentation with results
- [ ] Clean up temporary files

---

## Alternative Strategies

### Option A: Parallel Processing (Not Recommended)
**Pros:** Faster overall completion
**Cons:** Disk space conflicts, harder to monitor, risky

### Option B: Skip Park Categories (Not Recommended)
**Pros:** Saves time
**Cons:** Incomplete dataset, missing potential detections

### Option C: Increase Confidence Threshold (Conditional)
**When:** If detection rate > 70% (too many clips)
**Action:** Increase threshold from 0.6 to 0.7
**Effect:** Reduces clips by ~30%

### Option D: Process Only Movie_F (Quick Win)
**When:** Time constrained or disk space critical
**Action:** Process only Movie_F (~1,290 videos)
**Output:** ~650-775 clips in 18 minutes
**Benefit:** Highest ROI, quick results

---

## Success Metrics

### Quantitative
- Videos processed: 3,580 / 3,580 (100%)
- Detection rate: 40-50% overall
- Processing speed: 65-75 videos/minute
- Error rate: < 1%
- Disk space maintained: > 20GB throughout

### Qualitative
- No ffmpeg errors (all clips created successfully)
- No worker crashes
- No disk space emergencies
- Smooth sequential processing
- Reproducible process documented

---

## Next Actions

1. **Immediate:** Decide processing priority order
2. **Within 1 hour:** Start SSIM filtering (longest step)
3. **After SSIM:** Review filter results, adjust if needed
4. **Sequential:** Process categories one by one
5. **Throughout:** Monitor disk space and worker health
6. **Upon completion:** Archive outputs, update documentation

---

## Questions to Resolve

1. **Archive Strategy:** Where to store 65-79GB of output clips?
   - External drive?
   - Cloud storage?
   - Compress and keep local?

2. **Priority Confirmation:** Process all 4 categories or subset?
   - All 4 = complete dataset
   - Movie only = faster, higher ROI
   - Your call based on objectives

3. **SSIM Threshold:** Keep at 0.85 or adjust?
   - 0.85 = balanced (recommended)
   - 0.80 = more videos pass (less filtering)
   - 0.90 = fewer videos pass (more aggressive)

4. **Detection Threshold:** Keep at 0.6 or adjust?
   - 0.6 = balanced (recommended)
   - 0.5 = more detections (more false positives)
   - 0.7 = fewer detections (higher confidence only)

---

**Strategy Status:** READY TO EXECUTE
**Waiting For:** User confirmation on priority order and any adjustments
**Estimated Start:** Immediately after approval
**Estimated Completion:** 12-16 hours from start

---

## Appendix: Category Comparison Table

| Category | Videos | Size | SSIM Filter | GPU Process | Expected Clips | Expected Output | Priority | Detection Rate |
|----------|--------|------|-------------|-------------|----------------|----------------|----------|----------------|
| Movie_F  | 1,523  | 255GB| ~1,290      | ~18 min     | 650-775        | ~30-35GB       | 1 (HIGH) | 50-60%         |
| Movie_R  | 1,523  | 79GB | ~1,290      | ~18 min     | 390-515        | ~18-23GB       | 2 (MED)  | 30-40%         |
| Park_F B2| 677    | 110GB| ~500        | ~7 min      | 175-225        | ~8-10GB        | 3 (MED)  | 35-45%         |
| Park_R B2| 678    | 34GB | ~500        | ~7 min      | 200-250        | ~9-11GB        | 4 (LOW)  | 40-50%         |
| **TOTAL**| **4,401**|**478GB**|**~3,580**|**~50 min**|**1,415-1,765**|**~65-79GB**| - | **~44%** |

---

**End of Strategy Document**

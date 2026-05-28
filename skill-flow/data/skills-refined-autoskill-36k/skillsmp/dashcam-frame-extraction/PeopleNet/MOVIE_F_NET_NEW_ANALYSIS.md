# Movie_F Net New Files - Comprehensive Analysis

**Date:** 2025-11-14
**Analysis Type:** Frame Coverage Gap Analysis
**Purpose:** Identify unprocessed Movie_F videos requiring frame extraction

---

## EXECUTIVE SUMMARY

**Desktop CARDV Movie_F Status:**
- Total videos: **3,566**
- Already have frames (Google Drive): **2,140** ✅ (60%)
- **MISSING FRAMES: 1,426** ❌ (40%)

**Primary Gap:** Oct 24 - Nov 13, 2025 (1,419 videos = 99% of missing)

---

## DETAILED FINDINGS

### Frame Extraction Coverage Analysis

**Google Drive Frames Folder:**
- Location: `INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples/`
- Total Movie_F frames: 23,964 JPG files
- Unique videos with frames: **5,187 videos**
- Videos with ≥3 frames: **5,084** (98% meet quality standard)
- Videos with <3 frames: **103** (2% need additional frames)
- Average frames per video: ~4.6 frames
- Date range: July 24, 2025 - Oct 23, 2025 (approximately)

**Desktop CARDV Movie_F:**
- Location: `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`
- Total videos: **3,566**
- Size: 601GB
- Date range: Aug 7 - Nov 13, 2025 (+ 2 corrupted dates)

**Overlap Analysis:**
- Desktop videos already in frames folder: **2,140** ✅
- Desktop videos MISSING from frames folder: **1,426** ❌
- Overlap percentage: 60%

---

## NET NEW VIDEOS REQUIRING FRAME EXTRACTION

**Total: 1,426 videos**

### By Date (Descending Volume):

| Date | Count | % of Total | Status |
|------|-------|-----------|--------|
| 2025-10-28 | 409 | 28.7% | 🔴 MISSING |
| 2025-11-12 | 181 | 12.7% | 🔴 MISSING |
| 2025-10-29 | 139 | 9.8% | 🔴 MISSING |
| 2025-11-01 | 102 | 7.2% | 🔴 MISSING |
| 2025-10-31 | 95 | 6.7% | 🔴 MISSING |
| 2025-10-24 | 76 | 5.3% | 🔴 MISSING |
| 2025-11-04 | 62 | 4.3% | 🔴 MISSING |
| 2025-10-30 | 56 | 3.9% | 🔴 MISSING |
| 2025-10-27 | 56 | 3.9% | 🔴 MISSING |
| 2025-11-05 | 55 | 3.9% | 🔴 MISSING |
| 2025-11-13 | 38 | 2.7% | 🔴 MISSING |
| 2025-11-07 | 32 | 2.2% | 🔴 MISSING |
| 2025-11-10 | 28 | 2.0% | 🔴 MISSING |
| 2025-11-03 | 24 | 1.7% | 🔴 MISSING |
| 2025-11-09 | 22 | 1.5% | 🔴 MISSING |
| 2025-10-26 | 22 | 1.5% | 🔴 MISSING |
| 2025-11-06 | 11 | 0.8% | 🔴 MISSING |
| 2025-11-11 | 10 | 0.7% | 🔴 MISSING |
| 2025-11-08 | 1 | 0.1% | 🔴 MISSING |
| **Oct24-Nov13 Subtotal** | **1,419** | **99.5%** | |

### Older Dates (Gaps/Corrupted):

| Date | Count | Notes |
|------|-------|-------|
| 2025-08-31 | 1 | Gap in original processing |
| 2025-08-30 | 1 | Gap in original processing |
| 2025-08-27 | 1 | Gap in original processing |
| 2025-08-08 | 1 | Gap in original processing |
| 2025-08-07 | 1 | Gap in original processing |
| 2025-07-28 | 1 | Gap in original processing |
| 2002-07-02 | 1 | Corrupted date (camera error) |
| **Older Subtotal** | **7** | **0.5%** | |

**TOTAL NET NEW:** 1,426 videos

---

## WHAT NEEDS TO BE DONE

### For the 1,426 NET NEW Videos:

#### Stage 1: Frame Extraction (PRIMARY TASK)
**Tool:** Python script with ffmpeg/OpenCV
**Standard:** Extract at least 3 frames per video
**Methods:**
1. **Position-based (minimum):**
   - BEGIN: Frame at 1 second
   - MIDDLE: Frame at 50% duration
   - END: Frame at duration-1 second

2. **Motion-based (optimal):**
   - Extract frames where significant motion detected
   - Use SSIM (Structural Similarity Index) between frames
   - Threshold: SSIM < 0.85 indicates motion
   - Target: 5-10 frames per video with motion

**Format:** `YYYYMMDDHHMMSS_NNNNNN[A]_[POSITION|F###]_MSMSMSms.jpg`

**Output Location:** `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\FRAMES_CLIPS\Movie_F&R_MotionSamples\`

**Estimated Time:**
- Position-based: ~5-10 seconds per video = 2-4 hours total
- Motion-based: ~15-30 seconds per video = 6-12 hours total

---

#### Stage 2: Audio Extraction (REQUIRED)
**Status:** Need to verify if already done
**Tool:** ffmpeg
**Command:**
```bash
ffmpeg -i input.MP4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav
```

**Output Location:** `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM_AUDIO\audio_extracts\`
**Format:** `YYYYMMDDHHMMSS_NNNNNN_A.wav`

**Check if already done:**
```bash
# Count audio files for net new videos
for video in /tmp/truly_missing_frames.txt; do
  audio_file="${video}_A.wav"
  # Check if exists in audio_extracts folder
done
```

**Estimated Time:** ~2-5 seconds per video = 2-3 hours total

---

#### Stage 3: PeopleNet Clip Extraction (NEXT PRIORITY)
**Status:** NOT DONE for Movie_F
**Tool:** GPU pipeline (already built and tested)
**Process:**
1. SSIM filtering (remove static videos)
2. GPU inference with PeopleNet
3. Clip extraction with ±4s buffer

**Expected Results:**
- Input: 1,426 videos
- After SSIM: ~1,210 videos (85% pass rate for driving mode)
- With people detected: ~665-730 clips (55% detection rate)
- Output size: ~30-35GB

**Estimated Time:**
- SSIM: 6-8 hours (CPU-intensive)
- GPU processing: ~20 minutes
- Total: 6.5-8.5 hours

---

#### Stage 4: Audio Transcription (FINAL STAGE)
**Tool:** LocalAV Transcriber (Whisper + diarization)
**Input:** Source MP4 videos OR extracted clips?
**Output:** JSON, SRT, VTT, CSV with:
- Word-level timestamps
- Speaker identification
- Voice sex classification (optional)

**Decision needed:** Transcribe source videos or just clips?
- **Source videos:** Complete audio, includes everything
- **Clips:** Only segments with people, more focused

**Estimated Time:** ~30-60 seconds per video = 12-24 hours total

---

## PROCESSING ORDER OPTIONS

### Option A: Complete Stages Sequentially (Document Order)
1. Frame extraction (6-12 hours)
2. Audio extraction (2-3 hours) - if not already done
3. PeopleNet clips (6.5-8.5 hours)
4. Transcription (12-24 hours)
**Total:** 26.5-47.5 hours

### Option B: Prioritize PeopleNet First (Data Reduction)
1. PeopleNet clips (6.5-8.5 hours) → reduces to ~700 clips
2. Frame extraction from CLIPS only (~700 videos instead of 1,426)
3. Audio extraction from CLIPS
4. Transcription of clips
**Total:** Less overall time, but clips-only workflow

### Option C: Parallel Processing (Fastest)
1. **Track A:** Frame extraction (background, slow)
2. **Track B:** PeopleNet clips (GPU, fast)
3. **Track C:** Audio extraction (parallel with frames)
4. **Track D:** Transcription (once clips ready)
**Total:** 12-24 hours elapsed (overlap processing)

---

## REPEATABLE PROCESS DOCUMENTATION

### WORKFLOW TEMPLATE: New Video Batch Processing

**Use this checklist for ANY new batch of videos**

#### 1. INVENTORY & GAP ANALYSIS (30-60 minutes)

```bash
# Step 1.1: Create video list from new source
find [NEW_SOURCE_PATH] -name "*.MP4" -printf "%f\n" | sed 's/\.MP4$//' | sort > /tmp/new_videos.txt
wc -l /tmp/new_videos.txt

# Step 1.2: Get existing frame extraction list
find [FRAMES_FOLDER] -name "*A_*.jpg" -printf "%f\n" | cut -c1-21 | sort -u > /tmp/existing_frames.txt
wc -l /tmp/existing_frames.txt

# Step 1.3: Strip camera suffix for comparison
cat /tmp/new_videos.txt | sed 's/[AB]$//' > /tmp/new_videos_no_camera.txt

# Step 1.4: Find videos without frames (NET NEW)
comm -23 /tmp/new_videos_no_camera.txt /tmp/existing_frames.txt > /tmp/net_new_videos.txt
wc -l /tmp/net_new_videos.txt

# Step 1.5: Analyze by date
cat /tmp/net_new_videos.txt | cut -c1-8 | sort | uniq -c | sort -rn

# Step 1.6: Save for processing
cp /tmp/net_new_videos.txt /home/yousuf/PROJECTS/PeopleNet/process_lists/[BATCH_NAME]_net_new.txt
```

#### 2. FRAME EXTRACTION (Variable time, ~6-12 hours)

**Decision:** Position-based (fast) or Motion-based (better quality)?

**Position-based (3 frames minimum):**
```bash
python3 /home/yousuf/PROJECTS/PeopleNet/Scripts/extract_position_frames.py \
  --video-list /tmp/net_new_videos.txt \
  --source-dir [SOURCE_VIDEO_PATH] \
  --output-dir [FRAMES_OUTPUT_PATH] \
  --positions BEGIN,MIDDLE,END
```

**Motion-based (5-10 frames with motion):**
```bash
python3 /home/yousuf/PROJECTS/PeopleNet/Scripts/extract_motion_frames.py \
  --video-list /tmp/net_new_videos.txt \
  --source-dir [SOURCE_VIDEO_PATH] \
  --output-dir [FRAMES_OUTPUT_PATH] \
  --ssim-threshold 0.85 \
  --max-frames 10
```

**Verification:**
```bash
# Count frames extracted
find [FRAMES_OUTPUT_PATH] -name "*.jpg" | wc -l

# Check videos with <3 frames
find [FRAMES_OUTPUT_PATH] -name "*.jpg" -printf "%f\n" | cut -c1-21 | sort | uniq -c | awk '$1 < 3'
```

#### 3. AUDIO EXTRACTION (Optional, ~2-3 hours)

**Check if already done:**
```bash
# For each video in net_new list, check if audio exists
while read video; do
  audio="${video}_[A/B].wav"
  if [ ! -f "[AUDIO_FOLDER]/$audio" ]; then
    echo "$video" >> /tmp/missing_audio.txt
  fi
done < /tmp/net_new_videos.txt
```

**Extract missing audio:**
```bash
python3 /home/yousuf/PROJECTS/PeopleNet/Scripts/extract_audio_batch.py \
  --video-list /tmp/missing_audio.txt \
  --source-dir [SOURCE_VIDEO_PATH] \
  --output-dir [AUDIO_OUTPUT_PATH] \
  --sample-rate 16000 \
  --channels 1
```

#### 4. PEOPLENET CLIP EXTRACTION (~6.5-8.5 hours)

**4.1: SSIM Filtering (6-8 hours)**
```bash
python3 /tmp/ssim_filter.py \
  "[SOURCE_VIDEO_PATH]" \
  /home/yousuf/PROJECTS/PeopleNet/[BATCH_NAME]_process_list.txt \
  0.85
```

**4.2: GPU Pipeline Setup**
```bash
# Create output directory
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_[BATCH_NAME]/{locks,clips}

# Update worker script paths
# Deploy to 3 workers
# Start batch copy agent with 50-video batches, 20GB buffer
```

**4.3: Monitor & Verify**
```bash
# Progress
watch -n 5 'wc -l /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_[BATCH_NAME]/processed_videos.txt'

# Clips created
watch -n 10 'ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_[BATCH_NAME]/*.mp4 | wc -l'

# Detection rate
python3 -c "print(f'{clips/processed*100:.1f}% detection rate')"
```

#### 5. TRANSCRIPTION (~12-24 hours)

**Decision:** Transcribe source videos or clips?

**If transcribing clips:**
```bash
localav ingest /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_[BATCH_NAME]/clips \
  --pattern "*.mp4" \
  --preset balanced \
  --formats srt,vtt,json \
  --skip-existing
```

**If transcribing source videos:**
```bash
# Create list of videos with people (from clips)
# Transcribe only those source videos
localav transcribe [SOURCE_VIDEO] -o [OUTPUT_DIR] --preset balanced
```

#### 6. VERIFICATION & REPORTING

**Checklist:**
- [ ] All net new videos have ≥3 frames
- [ ] Audio extracted (if required)
- [ ] PeopleNet clips created (expected ~40-60% detection rate)
- [ ] Transcriptions generated
- [ ] Output sizes reasonable
- [ ] No corrupted files
- [ ] All outputs uploaded to Google Drive

**Generate Report:**
```bash
python3 /home/yousuf/PROJECTS/PeopleNet/Scripts/generate_batch_report.py \
  --batch-name [BATCH_NAME] \
  --net-new-count [COUNT] \
  --frames-extracted [COUNT] \
  --clips-created [COUNT] \
  --transcriptions [COUNT]
```

---

## OPTIMIZATION NOTES (FOR FUTURE)

### Speed Optimizations
1. **Parallel frame extraction:** Use GNU parallel or multiprocessing
2. **GPU for motion detection:** Use CUDA-accelerated SSIM
3. **Batch audio extraction:** Process multiple videos simultaneously
4. **Disk I/O:** Copy to local NVMe before processing

### Storage Optimizations
1. **Progressive archival:** Move completed outputs to Google Drive during processing
2. **Compression:** Tar+gzip older batches
3. **Incremental sync:** Use rclone with delta sync

### Quality Optimizations
1. **Adaptive frame extraction:** More frames for longer/complex videos
2. **Smart SSIM threshold:** Adjust based on video characteristics (night/day)
3. **Confidence tuning:** Per-category confidence thresholds

---

## FILE LOCATIONS REFERENCE

### Input:
- Desktop videos: `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/`
- Google Drive videos: `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\Movie_F\`

### Output:
- Frames: `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\FRAMES_CLIPS\Movie_F&R_MotionSamples\`
- Audio: `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM_AUDIO\audio_extracts\`
- Clips: `/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Movie_F_[BATCH]/`
- Transcriptions: `G:\My Drive\PROJECTS\APPS\AudioTranscription\outputs_movie_cameras\Movie_F\`

### Processing Lists:
- Net new videos: `/tmp/net_new_videos.txt`
- Missing frames: `/tmp/truly_missing_frames.txt`
- SSIM filtered: `/home/yousuf/PROJECTS/PeopleNet/movie_f_process_list.txt`

---

## IMMEDIATE NEXT ACTIONS

### For the 1,426 Net New Movie_F Videos:

**User Decision Required:**
1. **Which processing order?** (Option A, B, or C above)
2. **Frame extraction method?** (Position-based fast vs Motion-based quality)
3. **Audio extraction needed?** (Check if already done first)
4. **Transcription input?** (Source videos vs clips only)

**After Decision:**
1. Execute frame extraction for 1,426 videos
2. Verify audio extraction status
3. Run PeopleNet pipeline
4. Generate transcriptions
5. Upload all outputs to Google Drive
6. Update inventory tracking

---

**Analysis Status:** COMPLETE
**Net New Identified:** 1,426 videos
**Primary Gap:** Oct 24 - Nov 13, 2025
**Ready For:** User decision on processing approach
**Created:** 2025-11-14

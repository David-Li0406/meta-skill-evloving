# Complete Dashcam Processing Workflow - Comprehensive Analysis

**Date:** 2025-11-14
**Analysis Scope:** Full multi-stage pipeline understanding
**Data Sources:** Ubuntu Desktop, Windows Desktop (CARDV), Google Drive (INVESTIGATION)

---

## THE COMPLETE 5-STAGE WORKFLOW

### Stage 1: Source Videos (MP4)
**What:** Raw dashcam recordings from vehicle cameras
**Format:** `YYYYMMDDHHMMSS_NNNNNN[A-Z].MP4`
**Cameras:**
- A = Front camera (driving + parked)
- B = Rear camera (driving + parked)

**Modes:**
- **Movie** = Driving mode (continuous recording while vehicle moving)
- **Park** = Parked mode (event-triggered recording)

### Stage 2: Audio Extraction (WAV)
**What:** Extract audio track from MP4 videos
**Format:** `YYYYMMDDHHMMSS_NNNNNN_[A-Z].wav`
**Tool:** ffmpeg
**Purpose:** Prepare audio for transcription
**Output Location (Google Drive):** `INVESTIGATION/DASHCAM_AUDIO/audio_extracts/`

### Stage 3: Frame Extraction (JPG)
**What:** Extract keyframes from videos for visual analysis
**Methods:**
1. **Position-based:** BEGIN (1s), MIDDLE (50%), END (last 1s)
2. **Motion-based:** Multiple frames where significant motion detected

**Format:**
- Position: `YYYYMMDDHHMMSS_NNNNNNA_BEGIN_001000ms.jpg`
- Motion: `YYYYMMDDHHMMSS_NNNNNNA_F001_001000ms.jpg`

**Purpose:** Quick visual scanning without processing full video
**Output Location (Google Drive):** `INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples/`

### Stage 4: PeopleNet Clip Extraction (MP4 Clips)
**What:** AI-based people detection and video clip extraction
**Model:** NVIDIA PeopleNet ResNet-34 INT8
**Process:**
1. Run PeopleNet inference on video (sample 1 FPS)
2. Detect people with confidence > 0.6
3. Extract clip segments with ±4s buffer around detections
4. Output: Short clips containing only frames with detected people

**Format:** `YYYYMMDDHHMMSS_NNNNNN[A-Z]_people_<start>-<end>s.mp4`
**Purpose:** Massive data reduction (95-99%) - keep only people interactions
**Output Location (Ubuntu):** `/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_*/`

**THIS IS WHAT WE'VE BEEN DOING**

### Stage 5: Audio Transcription (TXT/JSON/SRT)
**What:** Speech-to-text transcription with speaker diarization
**Tool:** Whisper (faster-whisper) + pyannote/SpeechBrain
**Features:**
- Word-level timestamps
- Speaker identification
- Voice sex classification (optional)
- Multiple export formats (SRT, VTT, CSV, JSON)

**Output Location (Google Drive):** `APPS/AudioTranscription/outputs_*/`

---

## DATA INVENTORY BY LOCATION

### Location 1: Google Drive (Source of Truth - Windows G:)

**Path:** `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\`

#### Movie_F (Front Camera - Driving)
- **Total Videos:** 5,196 unique MP4s
- **Date Range:** July 24, 2025 - November 13, 2025+
- **Audio Extracted:** 5,155/5,196 (99.2%) ✅
- **Frames Extracted:** 5,155/5,196 (99.2%, avg 9.3 frames/video) ✅
- **PeopleNet Clips:** UNKNOWN (not documented)
- **Transcriptions:** Partial (various completed sets)

#### Movie_R (Rear Camera - Driving)
- **Total Videos:** UNKNOWN (not inventoried yet)
- **Processing Status:** UNKNOWN

#### Park_F (Front Camera - Parked)
- **Total Videos:** UNKNOWN on Google Drive
- **Processing Status:** UNKNOWN

#### Park_R (Rear Camera - Parked)
- **Total Videos:** UNKNOWN on Google Drive
- **Processing Status:** UNKNOWN

### Location 2: Windows Desktop (Working Copy - C:\Users\yousu\Desktop\CARDV)

**Accessible via Ubuntu:** `/mnt/windows/Users/yousu/Desktop/CARDV/`

#### Movie_F
- **Total Videos:** 3,566 MP4s
- **Date Range:** Aug 7, 2025 - Oct 28, 2025 (+ corrupted dates)
- **Size:** 601GB
- **Status:** Subset of Google Drive data
- **Audio Extracted:** UNKNOWN (need to check)
- **Frames Extracted:** UNKNOWN (need to check)
- **PeopleNet Clips:** ✗ NOT PROCESSED
- **Transcriptions:** ✗ NOT PROCESSED

#### Park_F
- **Total Videos:** 3,152 MP4s
- **Date Range:** July 25 - Nov 13, 2025
- **Size:** 523GB
- **Status:** May overlap with Google Drive
- **PeopleNet Clips:** ✅ 1,792 videos processed (Batch 1: Jul 25 - Oct 13)
  - Output: 665 clips (37.1% detection rate, ~25GB)
  - **NEW:** 1,360 videos unprocessed (Oct 14 - Nov 13)

#### Park_R
- **Total Videos:** 3,808 MP4s
- **Date Range:** July 25 - Nov 13, 2025
- **Size:** 194GB
- **Status:** May overlap with Google Drive
- **PeopleNet Clips:** ✅ 3,167 videos processed (Batch 1: Jul 25 - Oct 13)
  - Output: 1,470 clips (46% detection rate, ~60GB)
  - **NEW:** 678 videos unprocessed (Oct 14 - Nov 13)

### Location 3: Ubuntu /home/yousuf/PROJECTS/PeopleNet/ (Processing Output)

**Park_F Batch 1 - COMPLETED:**
- Processed: 1,792 videos (Jul 25 - Oct 13)
- Output: 665 clips, 25GB
- Detection rate: 37.1%
- Location: `Outputs/GPU_Pipeline_Park_F_Batch1/`

**Park_R Batch 1 - COMPLETED:**
- Processed: 3,167 videos (Jul 25 - Oct 13)
- Output: 1,470 clips, 60GB
- Detection rate: 46%
- Location: `Outputs/GPU_Pipeline_Park_R_Batch1/`

---

## DATE RANGE ANALYSIS

### Google Drive Movie_F Coverage
- **5,196 videos** covering July 24 - November 13+ (complete archive)

### Desktop CARDV Coverage

| Category | Total | Date Range Start | Date Range End | Days Covered |
|----------|-------|-----------------|----------------|--------------|
| Movie_F | 3,566 | Aug 7, 2025 | Oct 28, 2025 | ~82 days |
| Park_F | 3,152 | Jul 25, 2025 | Nov 13, 2025 | ~111 days |
| Park_R | 3,808 | Jul 25, 2025 | Nov 13, 2025 | ~111 days |

### Ubuntu Processing Status

| Category | Processed Dates | Videos Processed | Unprocessed Dates | Videos Remaining |
|----------|----------------|------------------|-------------------|------------------|
| Park_F | Jul 25 - Oct 13 | 1,792 ✅ | Oct 14 - Nov 13 | 1,360 |
| Park_R | Jul 25 - Oct 13 | 3,167 ✅ | Oct 14 - Nov 13 | 678 |
| Movie_F | NONE | 0 | Aug 7 - Oct 28 | 3,566 |

---

## PROCESSING GAPS ANALYSIS

### Stage 1: Source Videos ✅
- **Google Drive:** Complete archive (5,196 Movie_F videos)
- **Desktop:** Working subset (3,566 Movie_F + Park categories)
- **Status:** COMPLETE - all videos accessible

### Stage 2: Audio Extraction

**Google Drive Movie_F:** ✅ 99.2% COMPLETE
- Extracted: 5,155/5,196 videos
- Missing: 41 videos (documented)
- Location: `DASHCAM_AUDIO/audio_extracts/`

**Desktop CARDV:** ⚠️ STATUS UNKNOWN
- Need to check if audio extracted for Desktop videos
- May need to extract for NEW videos (Oct 14 - Nov 13)

### Stage 3: Frame Extraction

**Google Drive Movie_F:** ✅ 99.2% COMPLETE
- Extracted: 5,155/5,196 videos (47,822 frames total)
- Average: 9.3 frames per video
- 98.8% have ≥3 frames (BEGIN/MIDDLE/END)
- Location: `FRAMES_CLIPS/Movie_F&R_MotionSamples/`

**Desktop CARDV:** ⚠️ STATUS UNKNOWN
- Need to check if frames extracted for Desktop videos
- Sample directory exists: `/home/yousuf/PROJECTS/PeopleNet/Park_F_Frame_Samples/` (40 frame pairs)
- May need full extraction for remaining videos

### Stage 4: PeopleNet Clip Extraction (People Detection)

**COMPLETED:**
- ✅ Park_R Batch 1: 3,167 videos → 1,470 clips (Jul 25 - Oct 13)
- ✅ Park_F Batch 1: 1,792 videos → 665 clips (Jul 25 - Oct 13)
- **Total:** 4,959 videos → 2,135 clips (~85GB)

**REMAINING:**
- ❌ Movie_F: 3,566 videos (NEVER PROCESSED - HIGH PRIORITY)
- ❌ Park_F Batch 2: 1,360 videos (Oct 14 - Nov 13)
- ❌ Park_R Batch 2: 678 videos (Oct 14 - Nov 13)
- **Total NEW:** 5,604 videos (~868GB source)

**Expected Output:**
- Movie_F: ~1,800 clips (~80GB) - driving mode = high people detection
- Park_F Batch 2: ~500 clips (~20GB)
- Park_R Batch 2: ~300 clips (~12GB)
- **Total:** ~2,600 clips (~112GB)

### Stage 5: Audio Transcription

**Google Drive:** ✅ PARTIAL COMPLETE
- Various completed transcript sets exist
- Locations:
  - `APPS/AudioTranscription/outputs_cardv/`
  - `APPS/AudioTranscription/outputs_movie_cameras/`
  - `APPS/AudioTranscription/RAW_TRANSCRIPTS/Movie_F/`

**Desktop CARDV:** ⚠️ STATUS UNKNOWN
- Need to check transcription coverage for Desktop videos
- Transcription should be done on SOURCE videos, not clips

---

## CRITICAL INSIGHTS

### 1. Desktop vs Google Drive Relationship
- Desktop CARDV (3,566 Movie_F) is a **SUBSET** of Google Drive (5,196 Movie_F)
- Google Drive has MORE complete archive
- Desktop has ~2,630 fewer Movie_F videos than Google Drive
- **Question:** Should we process Desktop subset or full Google Drive archive?

### 2. Processing Priority Mismatch
- **Google Drive** has 99% completion on:
  - Audio extraction ✅
  - Frame extraction ✅
- But **unclear** PeopleNet clip extraction status

- **Desktop CARDV** has:
  - Partial PeopleNet processing (Park categories only)
  - No Movie_F clips extracted
  - **Unknown** audio/frame extraction status

### 3. Workflow Order Question
The document suggests this order:
1. Audio extraction → 2. Frame extraction → 3. PeopleNet clips → 4. Transcription

**BUT:** We've been doing PeopleNet clips FIRST without checking if audio/frames were extracted!

**Question for User:**
- Should we extract audio + frames FIRST for all NEW videos?
- Or continue PeopleNet clips and backfill audio/frames later?
- What's the dependency? (e.g., do transcriptions need clips or source videos?)

### 4. Human Extraction Missing
User mentioned "human extraction" but I don't see this documented.

**Possibilities:**
- Crop detected people from frames (bounding box extraction)?
- Extract frames from PeopleNet clips showing people?
- Separate process not yet documented?

**Need clarification from user.**

---

## RECOMMENDED NEXT STEPS

### Option A: Complete PeopleNet Pipeline (My Current Focus)
**Pros:** Finishes Stage 4, massive data reduction first
**Cons:** Skips audio/frame extraction for NEW data

1. Process Movie_F (3,566 videos) → ~1,800 clips
2. Process Park_F Batch 2 (1,360 videos) → ~500 clips
3. Process Park_R Batch 2 (678 videos) → ~300 clips
4. **Then** backfill audio/frames if needed

### Option B: Complete All Stages Sequentially (Document Order)
**Pros:** Follows documented workflow order
**Cons:** Takes much longer before any clips available

1. **Stage 2:** Extract audio for ALL NEW videos (5,604 videos)
2. **Stage 3:** Extract frames for ALL NEW videos (5,604 videos)
3. **Stage 4:** PeopleNet clip extraction (5,604 videos → ~2,600 clips)
4. **Stage 5:** Transcribe audio (source videos or clips?)

### Option C: Hybrid Approach
**Pros:** Parallel processing, faster completion
**Cons:** More complex coordination

1. **Parallel Track A:** PeopleNet clips (Movie_F highest priority)
2. **Parallel Track B:** Audio + Frame extraction for remaining videos
3. **Track C:** Transcription of already-completed clips

---

## QUESTIONS FOR USER

### 1. Data Location Strategy
- Should we process **Desktop CARDV subset** (3,566 Movie_F) or **Google Drive complete** (5,196 Movie_F)?
- How do we access Google Drive videos from Ubuntu for processing?

### 2. Workflow Order
- Must we extract audio + frames BEFORE PeopleNet clips?
- Or can we continue PeopleNet first and backfill later?

### 3. Processing Scope
- Process only NEW desktop data (5,604 videos)?
- Or process FULL Google Drive archive (need to inventory Park categories on Google Drive)?

### 4. Human Extraction
- What exactly is "human extraction"?
- Is this cropping detected people from frames?
- Is this a separate Stage 6?

### 5. Transcription Input
- Should we transcribe SOURCE videos or CLIPS?
- Clips have people conversations (relevant)
- Source videos have everything (complete but noisy)

### 6. Dependencies
- Can stages run in parallel or must they be sequential?
- Does transcription need clips or just source audio?

---

## STORAGE & RESOURCE STATUS

### Available Space
- **Ubuntu /home:** 88GB free (68GB effective with 20GB buffer)
- **Windows Desktop:** 5.2GB free (100% full!)
- **Google Drive:** Cloud storage (access via rclone mounted)

### Current Usage
- **PeopleNet Clips (completed):** ~85GB (2,135 clips from Park categories)
- **NEW Processing Expected:** ~112GB (for 5,604 videos → 2,600 clips)
- **Challenge:** Cannot fit all outputs simultaneously

### Processing Speed (GPU Pipeline)
- **Movie_F:** 3,566 videos × 70-75 vpm = ~50 minutes GPU time
- **After SSIM filtering:** ~30-40 minutes actual GPU time
- **Total with setup:** ~18-24 hours including SSIM filtering

---

## WHAT I'VE BEEN DOING (Stage 4 Only)

### My Focus: PeopleNet Clip Extraction
- Completed Park_R Batch 1 (3,167 videos)
- Completed Park_F Batch 1 (1,792 videos)
- Created comprehensive documentation
- Optimized GPU pipeline (3 workers, batch copy, SSIM filtering)
- **Result:** 2,135 clips extracted, 95%+ data reduction

### What I Missed:
- Stage 2 (Audio extraction) status for Desktop videos
- Stage 3 (Frame extraction) status for Desktop videos
- Stage 5 (Transcription) planning
- Human extraction (Stage 6?)
- Overall workflow coordination

---

## NEXT ACTIONS

**Immediate:**
1. **User clarifies workflow priorities** (questions above)
2. **Check audio extraction status** for Desktop CARDV videos
3. **Check frame extraction status** for Desktop CARDV videos
4. **Decide:** Continue PeopleNet pipeline vs complete all stages

**After Clarification:**
- Execute chosen strategy (Option A, B, or C)
- Update this document with actual decisions
- Create detailed execution plan for remaining work

---

**Document Status:** AWAITING USER INPUT
**Created:** 2025-11-14
**Purpose:** Complete workflow understanding before proceeding
**Next:** User clarifies priorities and answers questions above

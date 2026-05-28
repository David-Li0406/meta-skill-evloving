# Human Extractor Skill

**Version:** 1.0 - Basic Human Cropping
**Purpose:** Detect and extract cropped human regions from dashcam MP4 videos

## What This Skill Does

Processes dashcam MP4 videos to:
1. **Detect** all humans using YOLOv8 person detection
2. **Track** individuals across frames using ByteTrack
3. **Crop** tight regions around each detected person (12% padding)
4. **Save** individual JPEG files for each human detection
5. **Index** all detections in MANIFEST.csv for searchability

## Key Features

- **GPU-Accelerated:** YOLO v8s person detection on CUDA
- **Multi-Object Tracking:** ByteTrack assigns persistent IDs across frames
- **Cropped Output:** Saves ONLY the human region, not full frames
- **Deduplication:** Smart filtering to keep only unique detections per track
- **Resume-Safe:** Skips already-processed videos

## Output Structure

```
parsed/
├── {Camera}/              # e.g., Park_R, Movie_F
│   └── {Date}/           # e.g., 20251006
│       ├── frame_*.jpg                     # Full frames (when human detected)
│       ├── humans_summary/                 # ★ CROPPED HUMANS
│       │   ├── track001_frame000123_180x420.jpg
│       │   ├── track017_frame000365_266x659.jpg
│       │   └── ...
│       └── MANIFEST.csv                    # Metadata per date
└── INDEX.csv                                # Global index
```

**Human crop filename format:**
```
track017_frame000365_266x659.jpg
│     │    │         │    │
│     │    │         │    └─ Height (659px)
│     │    │         └─ Width (266px)
│     │    └─ Frame index (365)
│     └─ Track ID (person #17)
└─ "track" prefix
```

## Quick Usage

### 1. Basic Invocation

```bash
cd "G:\My Drive\PROJECTS\skills\human-extractor"

python scripts/run_extraction.py config.json
```

### 2. Configuration

Create `config.json`:
```json
{
  "roots": [
    "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251006"
  ],
  "output_dir": "parsed"
}
```

### 3. Natural Language (via Claude)

```
"Extract all humans from Park_R videos on October 6, 2025"
"Process Park_R folder and crop all detected people"
```

## Output Files

### 1. Cropped Human Images (`humans_summary/`)
- **Format:** JPEG, quality 85
- **Content:** ONLY the human region (with 12% padding)
- **Naming:** `track{ID}_frame{IDX}_{W}x{H}.jpg`
- **Deduplication:** Similar crops from same track are skipped

### 2. Full Frames (Optional)
- **Format:** JPEG, quality 90
- **Content:** Entire video frame
- **When:** Saved when human is detected in that frame
- **Naming:** `frame_{IDX}_ts{MS}.jpg`

### 3. MANIFEST.csv
```csv
video,frame_idx,ts_ms,track_id,bbox,full_frame_path,human_crop_path
/path/video.MP4,365,15234,17,"1014,46,1280,705",frame_000365.jpg,humans_summary/track017_*.jpg
```

### 4. INDEX.csv (Global)
Aggregates all MANIFEST.csv files across all dates/cameras.

## Implementation

**Main Pipeline:** `G:\My Drive\PROJECTS\APPS\Human_Detection\src\cli\run_human_cropping.py`

**Key components:**
- `VideoStreamer`: OpenCV-based frame reading
- `PersonDetector`: YOLOv8s (GPU, FP16)
- `SimpleTracker`: ByteTrack (IoU=0.3, max_age=10)
- `crop_and_save()`: Extracts and saves human regions

## Requirements

- **Python:** 3.8+
- **GPU:** NVIDIA CUDA-capable (recommended)
- **RAM:** 2 GB minimum
- **Storage:** ~500 MB per 100 videos (varies by content)

**Dependencies:**
```
torch>=2.0
ultralytics>=8.0  # YOLOv8
opencv-python>=4.8
pandas>=2.0
numpy>=1.24
```

## Performance

**CPU Mode:**
- ~0.5-1 videos/min
- Depends on video resolution and human count

**GPU Mode:**
- ~2-4 videos/min (RTX 4080)
- YOLOv8s with FP16

## Differences from Head-Covering Version

This is the **BASIC** human extractor that:
- ✅ Extracts ALL detected humans
- ✅ No CLIP classification
- ✅ No head covering filtering
- ✅ Simpler, faster, general-purpose

**For head-covering detection**, use the specialized pipeline separately (not part of this skill).

## Integration with Other Skills

### Workflow: Sync → Extract Humans

```bash
# 1. Sync new files from external drive
python skills/dashcam-sync/scripts/sync_dashcam.py --source E:\

# 2. Extract humans from synced files
python skills/human-extractor/scripts/run_extraction.py config.json
```

## Troubleshooting

**"No humans found"**
→ Check confidence threshold (default 0.35) - may need to lower

**"CUDA out of memory"**
→ This version uses CPU fallback automatically if GPU unavailable

**"Video cannot be opened"**
→ Check MP4 codec compatibility (H.264 recommended)

## Files in This Skill

- `skill.md` - Complete specification (needs update)
- `README.md` - This file
- `SKILL_MANIFEST.md` - File inventory
- `scripts/run_extraction.py` - Wrapper script (UPDATED)
- `assets/config_template.json` - Configuration examples (UPDATED)

## Version

**1.0 - Basic Human Cropping** (Updated 2025-10-26)
- Fixed to use `run_human_cropping.py` (basic version)
- Removed head-covering detection references
- Simplified configuration
- Output: `humans_summary/` with cropped JPEGs

## Related Skills

- `dashcam-sync` - Sync new videos from external drives
- `motion-sampler` - Extract frame samples at fixed intervals
- `gps-timeline-analyzer` - Analyze GPS data from videos

---

**Status:** ✅ Production Ready (Basic Human Cropping)

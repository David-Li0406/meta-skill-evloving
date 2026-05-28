# Dashcam Video Processing Workflow

## Overview
Process dashcam videos to detect and identify a specific person (hijabi woman) across all footage.

## Project Context
- **Goal**: Find all instances of yourself (a hijabi woman) in dashcam footage
- **Data Source**: Dashcam videos from vehicle with 4 cameras
  - Movie_F: Front camera with audio (driving)
  - Movie_R: Back camera with audio (driving)
  - Park_F: Front camera without audio (parked)
  - Park_R: Back camera without audio (parked)
- **Date Range**: July 25 - October 13, 2025
- **Key Detail**: Dashcam time is always 1 hour behind actual time

## Complete Processing Pipeline

### Phase 1: Person Detection (YOLOv8 + ByteTrack)
**Status**: Completed for Park_R only

**Process**:
1. Input: Raw dashcam MP4 videos from `INVESTIGATION/DASHCAM/Park_R/`
2. Extract frames from each video
3. Run YOLOv8s person detection model on each frame
4. Use ByteTrack to track individuals across frames (assigns track IDs)
5. For each detected person track, save:
   - Detection image (cropped person)
   - CSV file with tracking metadata (track_id, timestamp, confidence, bbox)

**Output Location**: `G:\My Drive\PROJECTS\parsed\Park_R\detections\YYYYMMDD\`

**Output Structure**:
```
parsed/Park_R/
├── detections/
│   ├── 20250725/
│   │   ├── track001_ts000001234_conf0.87_320x480.jpg
│   │   ├── track002_ts000005678_conf0.92_310x450.jpg
│   │   └── ...
│   ├── 20250726/
│   └── ...
└── tracking_csvs/
    ├── 20250725_tracking.csv
    ├── 20250726_tracking.csv
    └── ...
```

**CSV Format**:
```csv
track_id,frame_number,timestamp_ms,confidence,bbox_x,bbox_y,bbox_w,bbox_h
1,10,416,0.87,320,480,200,400
2,25,1041,0.92,310,450,210,420
```

### Phase 2: Gender Classification (CLIP)
**Status**: Completed for Park_R only

**Process**:
1. Input: All detection images from Phase 1
2. Run CLIP vision-language model with two classification passes:

   **Pass 1 - Gender Classification**:
   - Prompt: "a photo of a woman" vs "a photo of a man"
   - Sort into folders:
     - `Women/` - Female detections
     - `Men/` - Male detections

   **Pass 2 - Head Covering Classification** (Women only):
   - Prompt: "a photo of a woman with her head covered" vs "a photo of a woman with her head uncovered"
   - Sort into folders:
     - `Target/` - Women with head covering (potential matches for you)
     - `Non-Target/` - Women without head covering

**Output Location**: `G:\My Drive\PROJECTS\parsed\Park_R\`

**Output Structure**:
```
parsed/Park_R/
├── Target/           # Hijabi women (your potential matches)
│   ├── track001_ts000001234_conf0.87_320x480.jpg
│   ├── track045_ts000012345_conf0.91_350x500.jpg
│   └── ...
├── Non-Target/       # Non-hijabi women
│   ├── track002_ts000005678_conf0.92_310x450.jpg
│   └── ...
└── Men/              # Male detections
    └── ...
```

### Phase 3: Manual Review & Clip Extraction
**Status**: In Progress

**Process**:
1. Manually review images in `Target/` folder
2. When you identify yourself in a detection image, note the filename
   - Filename format: `track{ID}_ts{timestamp_ms}_conf{confidence}_{width}x{height}.jpg`
   - Example: `track003_ts000005291_conf0.91_261x592.jpg`

3. Request video clip extraction by providing:
   - Detection filename
   - Date (extracted from CSV or context)

4. Script extracts video clip:
   - Finds the original MP4 video for that date
   - Looks up track in CSV file
   - Determines if track has single detection or span (start_ms to end_ms)
   - Extracts clip with 1-2 second padding before/after
   - Saves to `parsed/Park_R/clips/target_clips/`

**Clip Extraction Script Pattern**:
```python
# Input from detection filename
date = "20250807"
track_id = 3
timestamp_ms = 5291

# Find video file for that date
video_path = f"DASHCAM/Park_R/20250807*.MP4"

# Look up track span in CSV
csv_path = f"parsed/Park_R/tracking_csvs/20250807_tracking.csv"
# Find all rows with track_id=3
# Get min and max timestamp for that track

# Extract clip using cv2
start_ms = min_timestamp - 1000  # 1 sec padding
end_ms = max_timestamp + 1000
# Read frames from video, write to new clip

# Output
output = f"parsed/Park_R/clips/target_clips/track003_clip_20250807_{start_ms}ms-{end_ms}ms.mp4"
```

**Current Status**:
- Target folder has confirmed detections of you
- Multiple clips have been extracted
- Clips saved to: `G:\My Drive\PROJECTS\parsed\Park_R\clips\target_clips/`

### Phase 4: Duplicate Removal (Current)
**Status**: Pending - awaiting full file restoration

**Process**:
1. Calculate SHA256 hash for each video clip
2. Group files by identical hash (true duplicates)
3. Keep one file from each duplicate group
4. Delete remaining duplicates
5. Expected: ~50% reduction (522 duplicates from 1,044 files)

## Important Notes

### Detection Filename Format
```
track{track_id}_ts{timestamp_ms}_conf{confidence}_{width}x{height}.jpg
```
- `track_id`: Unique ID assigned by ByteTrack for person across frames
- `timestamp_ms`: Milliseconds into video when detection occurred
- `confidence`: YOLOv8 detection confidence (0.0-1.0)
- `width x height`: Bounding box dimensions in pixels

### CSV Tracking Data
- Links detection images back to original video frames
- Essential for clip extraction
- Format: `YYYYMMDD_tracking.csv`
- One CSV per date processed

### Video Filename Format (Original Dashcam)
```
YYYYMMDDHHMMSS_XXXXXX.MP4
```
- Example: `20250807110319_053093B.MP4`
- Date: 2025-08-07
- Time: 11:03:19 (dashcam time, 1 hour behind actual)
- Camera ID: 053093B

### Key Directories
```
G:\My Drive\PROJECTS\
├── INVESTIGATION\DASHCAM\           # Original dashcam videos
│   ├── Movie_F\                     # Front driving (with audio)
│   ├── Movie_R\                     # Rear driving (with audio)
│   ├── Park_F\                      # Front parked (no audio)
│   └── Park_R\                      # Rear parked (no audio)
│
└── parsed\
    └── Park_R\                      # Processed Park_R data
        ├── detections\              # Raw person detections by date
        ├── tracking_csvs\           # Tracking metadata
        ├── Target\                  # Hijabi women (your matches)
        ├── Non-Target\              # Non-hijabi women
        ├── Men\                     # Male detections
        └── clips\
            └── target_clips\        # Extracted video clips of you
```

## Processing Other Cameras (Not Yet Done)

To process Movie_F, Movie_R, or Park_F, repeat Phase 1-3 with different input/output paths:

```python
# Example for Movie_F
input_videos = "INVESTIGATION/DASHCAM/Movie_F/"
output_detections = "parsed/Movie_F/detections/"
output_csvs = "parsed/Movie_F/tracking_csvs/"
output_target = "parsed/Movie_F/Target/"
output_clips = "parsed/Movie_F/clips/target_clips/"
```

## Technical Stack
- **YOLOv8s**: Real-time person detection
- **ByteTrack**: Multi-object tracking
- **CLIP**: Vision-language model for classification
- **OpenCV (cv2)**: Video processing and clip extraction
- **Python**: All processing scripts

## Workflow Summary for AI Agent

1. **INPUT**: Raw dashcam MP4 videos
2. **DETECT**: YOLOv8 finds all people → saves cropped images + CSV
3. **CLASSIFY**: CLIP filters for hijabi women → sorts into Target folder
4. **REVIEW**: Human reviews Target folder images manually
5. **EXTRACT**: Script creates video clips for confirmed matches
6. **OUTPUT**: Video clips of target person saved to target_clips/

## Current State
- ✅ Park_R: Fully processed through Phase 3
- ❌ Movie_F: Not processed
- ❌ Movie_R: Not processed
- ❌ Park_F: Not processed
- 📊 Results so far: ~1,044 target detection images, multiple video clips extracted

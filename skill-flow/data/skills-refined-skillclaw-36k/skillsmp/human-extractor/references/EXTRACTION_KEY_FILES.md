# Key Files for Dashcam Video Clip Extraction

## Core Extraction Script (Master Template)

### `extract_clip.py` - Generic Extraction Template
**Purpose**: Master template for extracting video clips from dashcam footage based on track detection data

**Key Functions**:
1. Parses detection filename to extract track_id, timestamp, date
2. Finds corresponding CSV tracking file
3. Determines if track has single detection or multiple detections (span)
4. Extracts video clip with padding using OpenCV
5. Saves clip to target_clips folder

**Input Requirements**:
- Detection filename (e.g., `track003_ts000005291_conf0.91_261x592.jpg`)
- Date (YYYYMMDD format)
- Original dashcam video file location

**Output**:
- Video clip: `track{ID}_clip_{date}_{start_ms}ms-{end_ms}ms.mp4`
- Location: `parsed/Park_R/clips/target_clips/`

**Usage Pattern**:
```python
# Variables to configure
date = "20250807"
track_id = 3
timestamp_ms = 5291
padding_ms = 1000  # 1 second before/after

# Finds video: DASHCAM/Park_R/20250807*.MP4
# Reads CSV: parsed/Park_R/tracking_csvs/20250807_tracking.csv
# Extracts clip with OpenCV
# Saves: parsed/Park_R/clips/target_clips/track003_clip_20250807_4291ms-6291ms.mp4
```

---

## Specific Extraction Examples

### Individual Track Extraction Scripts
These are variations of the master template, each configured for a specific track:

1. **`extract_clip_track002.py`**
   - Extracts: track002 from unknown date
   - Example of basic single-detection extraction

2. **`extract_clip_track003_20250730.py`**
   - Date: July 30, 2025
   - Track: 003
   - Timestamp span: 2625ms - 3750ms
   - Example of multi-detection track (track appears in multiple frames)

3. **`extract_clip_track002_20250801.py`**
   - Date: August 1, 2025
   - Track: 002
   - Timestamp: 4041ms (single detection)

4. **`extract_clip_track016_20250802.py`**
   - Date: August 2, 2025
   - Track: 016
   - Timestamp: 41791ms (41.791 seconds into video)

5. **`extract_clip_track048_20250802.py`**
   - Date: August 2, 2025
   - Track: 048
   - Timestamp: 36291ms

6. **`extract_clip_track011_20250802_v1.py` & `v2.py`**
   - Date: August 2, 2025
   - Track: 011
   - Two versions (likely iterating on extraction parameters)

7. **`extract_clip_track007_20250803.py`**
   - Date: August 3, 2025
   - Track: 007

---

## Batch Processing Script

### `analyze_and_extract_target_clips.py` - Automated Batch Extractor
**Purpose**: Automatically extract video clips for ALL detections in the Target folder

**Capabilities**:
1. Scans entire `Target/` folder for detection images
2. Parses each filename to extract metadata
3. Groups detections by date
4. For each date:
   - Loads tracking CSV
   - Finds corresponding video file
   - Extracts all target clips in batch
5. Progress tracking and error handling

**Advantages over Individual Scripts**:
- Processes hundreds/thousands of detections automatically
- No manual script creation per track
- Batch processing efficiency
- Consistent naming and organization

**Usage**:
```bash
python analyze_and_extract_target_clips.py
```

**Expected Output**:
```
Processing date: 20250725
  Found 15 target detections
  Video: 20250725181629_052122A.MP4
  Extracting track 001... Done
  Extracting track 003... Done
  ...
  Extracted 15 clips for 20250725

Processing date: 20250726
  ...

Total: 1044 clips extracted
```

---

## Key Technical Components

### Detection Filename Parsing
All extraction scripts parse this format:
```
track{ID}_ts{timestamp_ms}_conf{confidence}_{width}x{height}.jpg

Example: track003_ts000005291_conf0.91_261x592.jpg
         ^^^^^^^^   ^^^^^^^^^^ ^^^^^^^^^ ^^^^^^^^^
         Track ID   Timestamp  Confidence Bbox size
```

**Regex Pattern**:
```python
import re
match = re.match(r'track(\d+)_ts(\d+)_conf([\d.]+)_(\d+)x(\d+)\.jpg', filename)
track_id = int(match.group(1))
timestamp_ms = int(match.group(2))
confidence = float(match.group(3))
width = int(match.group(4))
height = int(match.group(5))
```

### CSV Tracking File Format
Location: `parsed/Park_R/tracking_csvs/YYYYMMDD_tracking.csv`

```csv
track_id,frame_number,timestamp_ms,confidence,bbox_x,bbox_y,bbox_w,bbox_h
3,63,2625,0.89,352,678,150,200
3,75,3125,0.90,355,680,148,198
3,90,3750,0.91,358,682,145,195
```

**Key for Extraction**:
- Filter rows by `track_id`
- Get `min(timestamp_ms)` and `max(timestamp_ms)` for track span
- Use timestamps to calculate clip start/end with padding

### Video File Matching
**Pattern**: `YYYYMMDDHHMMSS_XXXXXX.MP4`

**Matching Logic**:
```python
from pathlib import Path

date = "20250807"
video_folder = Path(r"G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\Park_R")

# Find video file for this date
videos = list(video_folder.glob(f"{date}*.MP4"))

# If multiple videos on same date, need to match timestamp
# Detection at 5291ms = 5.291 seconds into video
# Video starting at 11:03:19 should contain this detection
```

### OpenCV Clip Extraction
```python
import cv2

# Open source video
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)  # Usually 24 FPS

# Calculate frame positions
start_frame = int((start_ms / 1000) * fps)
end_frame = int((end_ms / 1000) * fps)

# Create output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Extract frames
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
for frame_num in range(start_frame, end_frame):
    ret, frame = cap.read()
    if ret:
        out.write(frame)
    else:
        break

cap.release()
out.release()
```

---

## File Dependency Tree

```
Extraction Process
│
├── Input Files
│   ├── Original Videos: DASHCAM/Park_R/YYYYMMDDHHMMSS_*.MP4
│   ├── Detection Images: parsed/Park_R/Target/*.jpg
│   └── Tracking CSVs: parsed/Park_R/tracking_csvs/YYYYMMDD_tracking.csv
│
├── Processing Scripts
│   ├── extract_clip.py (master template)
│   ├── extract_clip_track{ID}_{date}.py (individual extractions)
│   └── analyze_and_extract_target_clips.py (batch processor)
│
└── Output Files
    └── Video Clips: parsed/Park_R/clips/target_clips/track*_clip_*.mp4
```

---

## Recommended Approach for New Extraction

**Option 1: Batch Process All Targets**
```bash
cd "G:\My Drive\PROJECTS"
python analyze_and_extract_target_clips.py
```
- Extracts clips for all 1,044+ target detections
- Fully automated
- Takes time but handles everything

**Option 2: Single Track Extraction**
1. Copy `extract_clip.py` to new file
2. Edit these variables:
   ```python
   date = "20250807"
   track_id = 3
   timestamp_ms = 5291
   padding_ms = 1000
   ```
3. Run script
4. Clip appears in target_clips/

**Option 3: Query-Based Extraction**
For specific time/location queries (like the McLanes example):
1. Use date range analysis to find relevant videos
2. Extract those specific videos
3. Process only those dates through detection pipeline
4. Extract target clips from filtered results

---

## Summary

**Must-Have Files for Extraction:**
1. `extract_clip.py` - Master extraction template
2. `analyze_and_extract_target_clips.py` - Batch processor
3. Tracking CSVs: `parsed/Park_R/tracking_csvs/*.csv`
4. Original videos: `DASHCAM/Park_R/*.MP4`
5. Detection images: `parsed/Park_R/Target/*.jpg`

**Key Dependencies:**
- OpenCV (cv2) for video processing
- Python pathlib for file handling
- Regex for filename parsing
- CSV module for tracking data

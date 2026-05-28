#!/bin/bash
#############################################################################
# AUTO FRAME EXTRACTION - Movie_F Videos ONLY
#############################################################################
# Purpose: Automated frame extraction when new videos are placed in Desktop CARDV
# Usage: ./auto_extract_movie_f.sh
#
# This script is specifically for Movie_F category only
#############################################################################

set -euo pipefail

# Configuration - Movie_F ONLY
CATEGORY="Movie_F"
DESKTOP_SOURCE="/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F"
FRAMES_OUTPUT="/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples"
WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"
STAGING_DIR="/home/yousuf/PROJECTS/PeopleNet/Staging/${CATEGORY}_Batch"
NUM_WORKERS=4
BATCH_SIZE=50
MIN_FREE_GB=25

echo "═══════════════════════════════════════════════════════════════"
echo "  AUTO FRAME EXTRACTION - ${CATEGORY}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

#############################################################################
# Pre-flight Checks
#############################################################################
echo "[1/7] Running pre-flight checks..."

# Check GPU availability
if ! nvidia-smi &>/dev/null; then
    echo "❌ ERROR: NVIDIA GPU not detected or drivers not installed"
    exit 1
fi
echo "  ✓ GPU detected: $(nvidia-smi --query-gpu=name --format=csv,noheader)"

# Check CUDA availability
if ! command -v ffmpeg &>/dev/null; then
    echo "❌ ERROR: ffmpeg not found"
    exit 1
fi
echo "  ✓ ffmpeg available"

# Check disk space
FREE_GB=$(df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
    echo "❌ ERROR: Insufficient disk space. Need ${MIN_FREE_GB}GB, have ${FREE_GB}GB"
    exit 1
fi
echo "  ✓ Disk space: ${FREE_GB}GB available"

# Check source directory
if [ ! -d "$DESKTOP_SOURCE" ]; then
    echo "❌ ERROR: Source directory not found: $DESKTOP_SOURCE"
    exit 1
fi
VIDEO_COUNT=$(find "$DESKTOP_SOURCE" -name "*.MP4" -type f | wc -l)
echo "  ✓ Source directory: $VIDEO_COUNT videos found"

# Check output directory
mkdir -p "$FRAMES_OUTPUT"
echo "  ✓ Output directory ready"

echo ""

#############################################################################
# Identify New Videos (Gap Analysis)
#############################################################################
echo "[2/7] Identifying videos needing frame extraction..."

# Get list of all videos in source
find "$DESKTOP_SOURCE" -name "*.MP4" -type f -exec basename {} .MP4 \; | sort > /tmp/all_source_videos.txt

# Get list of videos already processed (from existing frames)
find "$FRAMES_OUTPUT" -name "*.jpg" -type f | \
    sed -E 's/_BEGIN_.*|_MIDDLE_.*|_END_.*//' | \
    xargs -n1 basename | \
    sort -u > /tmp/processed_videos.txt

# Find net-new videos (handle 'A' suffix variations)
comm -23 /tmp/all_source_videos.txt /tmp/processed_videos.txt > /tmp/net_new_base.txt

# Add variations with A suffix
cat /tmp/net_new_base.txt | while read video; do
    # Check if video exists as-is or with A suffix
    if [ -f "$DESKTOP_SOURCE/${video}.MP4" ]; then
        echo "${video}.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}A.MP4" ]; then
        echo "${video}A.MP4"
    elif [ -f "$DESKTOP_SOURCE/${video}_A.MP4" ]; then
        echo "${video}_A.MP4"
    fi
done > /tmp/net_new_videos.txt

NET_NEW_COUNT=$(wc -l < /tmp/net_new_videos.txt)

if [ "$NET_NEW_COUNT" -eq 0 ]; then
    echo "  ℹ️  No new videos to process. All videos already have frames extracted."
    exit 0
fi

echo "  ✓ Found $NET_NEW_COUNT new videos requiring frame extraction"
cp /tmp/net_new_videos.txt "$WORK_DIR/${CATEGORY}_NET_NEW_${NET_NEW_COUNT}_videos.txt"
echo ""

#############################################################################
# Create Batch Files
#############################################################################
echo "[3/7] Creating batch files ($BATCH_SIZE videos per batch)..."

mkdir -p "$WORK_DIR/batches" "$WORK_DIR/logs" "$WORK_DIR/completed"
rm -rf "$WORK_DIR/batches"/*
rm -rf "$WORK_DIR/completed"/*

split -l "$BATCH_SIZE" -d -a 3 \
    "$WORK_DIR/${CATEGORY}_NET_NEW_${NET_NEW_COUNT}_videos.txt" \
    "$WORK_DIR/batches/batch_"

BATCH_COUNT=$(ls "$WORK_DIR/batches"/ | wc -l)
echo "  ✓ Created $BATCH_COUNT batch files"
echo ""

#############################################################################
# Create Worker Script (GPU-accelerated with HEVC fixes)
#############################################################################
echo "[4/7] Setting up GPU-accelerated worker..."

cat > /tmp/extract_frames_gpu_auto.py << 'WORKER_SCRIPT'
#!/usr/bin/env python3
"""
GPU-Accelerated Frame Extraction Worker
Extracts 3 frames per video: BEGIN, MIDDLE, END
CRITICAL: Works with HEVC videos - does NOT use -hwaccel_output_format
"""
import subprocess
import sys
from pathlib import Path
import json
import shutil

class FrameExtractor:
    def __init__(self, video_list_file, category, worker_id):
        self.video_list = Path(video_list_file)
        self.category = category
        self.worker_id = worker_id
        self.desktop_source = Path(f"/mnt/windows/Users/yousu/Desktop/CARDV/{category}")
        self.output_dir = Path("/home/yousuf/GoogleDrive/PROJECTS/INVESTIGATION/DASHCAM/FRAMES_CLIPS/Movie_F&R_MotionSamples")
        self.staging_dir = Path(f"/home/yousuf/PROJECTS/PeopleNet/Staging/{category}_Worker{worker_id}")
        self.staging_dir.mkdir(parents=True, exist_ok=True)

    def get_duration(self, video_path):
        """Get video duration in seconds"""
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ], capture_output=True, text=True, timeout=10)
            return float(result.stdout.strip())
        except:
            return None

    def extract_frame(self, video_path, timestamp, output_path, use_gpu=True):
        """
        Extract single frame at timestamp using GPU acceleration
        CRITICAL: Does NOT use -hwaccel_output_format cuda (breaks HEVC->JPEG)
        """
        try:
            cmd = ['ffmpeg', '-y']

            # GPU hardware acceleration for decoding only
            if use_gpu:
                cmd.extend(['-hwaccel', 'cuda'])
                # CRITICAL: DO NOT add '-hwaccel_output_format', 'cuda'
                # This breaks HEVC to JPEG conversion

            cmd.extend([
                '-ss', str(timestamp),
                '-i', str(video_path),
                '-frames:v', '1',
                '-q:v', '2',
                str(output_path)
            ])

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                text=True
            )

            return result.returncode == 0 and Path(output_path).exists()
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def process_video(self, video_filename):
        """Extract 3 frames from a single video"""
        source_path = self.desktop_source / video_filename

        if not source_path.exists():
            return {'status': 'not_found', 'frames': 0}

        # Copy to staging for faster I/O
        staged_path = self.staging_dir / video_filename
        try:
            shutil.copy2(source_path, staged_path)
        except Exception:
            return {'status': 'copy_failed', 'frames': 0}

        # Get duration
        duration = self.get_duration(staged_path)
        if not duration or duration < 3:
            staged_path.unlink(missing_ok=True)
            return {'status': 'invalid_duration', 'frames': 0}

        # Calculate timestamps
        begin_ts = 1.0
        middle_ts = duration / 2.0
        end_ts = max(1.0, duration - 1.0)

        video_base = video_filename.replace('.MP4', '')
        frames_extracted = 0

        # Extract 3 frames
        positions = [
            ('BEGIN', begin_ts, int(begin_ts * 1000)),
            ('MIDDLE', middle_ts, int(middle_ts * 1000)),
            ('END', end_ts, int(end_ts * 1000))
        ]

        for pos_name, timestamp, timestamp_ms in positions:
            output_path = self.output_dir / f"{video_base}_{pos_name}_{timestamp_ms:06d}ms.jpg"

            if self.extract_frame(staged_path, timestamp, output_path):
                frames_extracted += 1

        # Cleanup staging
        staged_path.unlink(missing_ok=True)

        return {
            'status': 'success' if frames_extracted == 3 else 'partial',
            'frames': frames_extracted
        }

    def process_batch(self):
        """Process all videos in the batch"""
        videos = self.video_list.read_text().strip().split('\n')
        videos = [v.strip() for v in videos if v.strip()]

        stats = {
            'total': len(videos),
            'success': 0,
            'partial': 0,
            'failed': 0,
            'frames': 0
        }

        for i, video in enumerate(videos, 1):
            result = self.process_video(video)
            stats['frames'] += result['frames']

            if result['status'] == 'success':
                stats['success'] += 1
            elif result['frames'] > 0:
                stats['partial'] += 1
            else:
                stats['failed'] += 1

        return stats

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: script.py <video_list> <category> <worker_id>")
        sys.exit(1)

    extractor = FrameExtractor(sys.argv[1], sys.argv[2], sys.argv[3])
    stats = extractor.process_batch()

    print(json.dumps(stats))

    # Exit with error if any videos failed
    if stats['failed'] > 0:
        sys.exit(1)
    sys.exit(0)
WORKER_SCRIPT

chmod +x /tmp/extract_frames_gpu_auto.py
echo "  ✓ Worker script ready with HEVC compatibility fixes"
echo ""

#############################################################################
# Launch Parallel Processing
#############################################################################
echo "[5/7] Launching parallel extraction ($NUM_WORKERS workers)..."

cat > /tmp/coordinator_auto.sh << 'COORDINATOR_SCRIPT'
#!/bin/bash
# Coordinator for parallel batch processing - Movie_F ONLY
# Exits on error - all batches must succeed

set -euo pipefail

WORK_DIR="/home/yousuf/PROJECTS/PeopleNet/FrameExtraction"
NUM_WORKERS=4
MIN_FREE_GB=25
CATEGORY="Movie_F"

check_space() {
    df -BG "$WORK_DIR" | awk 'NR==2 {print $4}' | sed 's/G//'
}

process_batch() {
    local batch_file="$1"
    local worker_id="$2"
    local batch_name=$(basename "$batch_file")

    echo "[Worker $worker_id] Processing $batch_name..."

    /home/yousuf/PROJECTS/ExtractedGPS/.venv/bin/python3 \
        /tmp/extract_frames_gpu_auto.py \
        "$batch_file" \
        "$CATEGORY" \
        "$worker_id" \
        > "$WORK_DIR/logs/${batch_name}_worker${worker_id}.log" 2>&1

    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "[Worker $worker_id] ERROR: Batch $batch_name failed with exit code $exit_code"
        exit $exit_code
    fi

    # Move to completed only on success
    mv "$batch_file" "$WORK_DIR/completed/"
    echo "[Worker $worker_id] Completed $batch_name"
}

export -f process_batch
export -f check_space
export WORK_DIR NUM_WORKERS MIN_FREE_GB CATEGORY

worker_id=0
ACTIVE_WORKERS=0

# Process all batches
for batch_file in "$WORK_DIR/batches"/*; do
    [ -f "$batch_file" ] || continue

    # Wait if at max workers
    while [ $ACTIVE_WORKERS -ge $NUM_WORKERS ]; do
        sleep 5
        ACTIVE_WORKERS=$(pgrep -f "extract_frames_gpu_auto.py" | wc -l)
    done

    # Check available space
    FREE_GB=$(check_space)
    if [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then
        echo "[Coordinator] ⚠️  Low disk space ($FREE_GB GB). Waiting..."
        while [ "$(check_space)" -lt "$MIN_FREE_GB" ]; do
            sleep 10
        done
    fi

    # Launch worker in background
    worker_id=$((worker_id + 1))
    process_batch "$batch_file" "$worker_id" &
    ACTIVE_WORKERS=$((ACTIVE_WORKERS + 1))

    sleep 2
done

# Wait for all workers to complete
wait
echo "[Coordinator] All batches completed!"
COORDINATOR_SCRIPT

chmod +x /tmp/coordinator_auto.sh

# Launch coordinator in background
/tmp/coordinator_auto.sh > "$WORK_DIR/logs/coordinator.log" 2>&1 &
COORDINATOR_PID=$!

echo "  ✓ Coordinator launched (PID: $COORDINATOR_PID)"
echo "  ✓ Processing $NET_NEW_COUNT videos across $BATCH_COUNT batches"
echo ""

#############################################################################
# Setup Monitoring
#############################################################################
echo "[6/7] Setting up progress monitoring..."

# Get baseline frame count
BASELINE=$(find "$FRAMES_OUTPUT" -name "*.jpg" -type f 2>/dev/null | wc -l)
START_TIME=$(date +%s)

cat > /tmp/monitor_extraction.sh << MONITOR_SCRIPT
#!/bin/bash
BASELINE=$BASELINE
START_TIME=$START_TIME
TARGET=$NET_NEW_COUNT

while true; do
    sleep 30

    CURRENT=\$(find "$FRAMES_OUTPUT" -name "*.jpg" -type f 2>/dev/null | wc -l)
    NEW_FRAMES=\$((CURRENT - BASELINE))
    NEW_VIDEOS=\$((NEW_FRAMES / 3))
    ELAPSED=\$(($(date +%s) - START_TIME))

    COMPLETED=\$(ls "$WORK_DIR/completed/" 2>/dev/null | wc -l)
    WORKERS=\$(ps aux | grep extract_frames_gpu_auto | grep -v grep | wc -l)
    GPU=\$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null)

    if [ \$ELAPSED -gt 0 ] && [ \$NEW_VIDEOS -gt 0 ]; then
        VIDS_PER_MIN=\$(echo "scale=1; (\$NEW_VIDEOS * 60) / \$ELAPSED" | bc 2>/dev/null || echo "0")
        FRAMES_PER_SEC=\$(echo "scale=2; \$NEW_FRAMES / \$ELAPSED" | bc 2>/dev/null || echo "0")
        REMAINING=\$((TARGET - NEW_VIDEOS))

        if [ \$(echo "\$VIDS_PER_MIN > 0.1" | bc 2>/dev/null || echo "0") -eq 1 ]; then
            ETA_MIN=\$(echo "scale=0; (\$REMAINING * 60) / \$VIDS_PER_MIN" | bc 2>/dev/null || echo "0")
            ETA_HR=\$(echo "scale=1; \$ETA_MIN / 60" | bc 2>/dev/null || echo "0")
        else
            ETA_HR="calculating"
        fi
    else
        VIDS_PER_MIN="0.0"
        FRAMES_PER_SEC="0.00"
        ETA_HR="calculating"
    fi

    PCT=\$((NEW_VIDEOS * 100 / TARGET))

    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "📊 EXTRACTION PROGRESS - \$(date '+%I:%M:%S %p')"
    echo "Videos: \$NEW_VIDEOS/\$TARGET (\${PCT}%) | Batches: \$COMPLETED/$BATCH_COUNT | Workers: \$WORKERS"
    echo "Speed: \$VIDS_PER_MIN vids/min | \$FRAMES_PER_SEC fps | ETA: \${ETA_HR}h | GPU: \${GPU}%"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    # Exit when all workers done
    if [ "\$WORKERS" -eq 0 ] && [ "\$COMPLETED" -eq "$BATCH_COUNT" ]; then
        echo "✅ Extraction complete!"
        break
    fi
done
MONITOR_SCRIPT

chmod +x /tmp/monitor_extraction.sh
/tmp/monitor_extraction.sh &
MONITOR_PID=$!

echo "  ✓ Progress monitor started (PID: $MONITOR_PID)"
echo ""

#############################################################################
# Summary
#############################################################################
echo "[7/7] Extraction in progress!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo "Source:        $DESKTOP_SOURCE"
echo "Output:        $FRAMES_OUTPUT"
echo "Videos:        $NET_NEW_COUNT to process"
echo "Batches:       $BATCH_COUNT batches"
echo "Workers:       $NUM_WORKERS parallel workers"
echo "GPU:           $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo ""
echo "Monitor PID:   $MONITOR_PID (updates every 30s)"
echo "Coordinator:   $COORDINATOR_PID"
echo "Logs:          $WORK_DIR/logs/"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Progress updates will appear every 30 seconds above."
echo "To monitor manually: tail -f $WORK_DIR/logs/coordinator.log"
echo ""

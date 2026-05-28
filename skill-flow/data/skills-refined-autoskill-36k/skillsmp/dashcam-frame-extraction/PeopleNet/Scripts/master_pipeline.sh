#!/usr/bin/env bash
set -euo pipefail

# ════════════════════════════════════════════════════════════════════════════
# PeopleNet Autonomous Pipeline - Master Orchestrator
# ════════════════════════════════════════════════════════════════════════════
#
# Single command to process dashcam parking footage autonomously:
# - Finds net new videos by date
# - Processes Park_F and Park_R sequentially
# - Backs up to Google Drive
# - Cleans up local files
#
# Usage:
#   ./master_pipeline.sh --start-date 2025-11-14 --auto-backup
#   ./master_pipeline.sh --start-date 2025-11-01 --end-date 2025-11-14
#   ./master_pipeline.sh --batch park_f --start-date 2025-11-14 --no-backup
#
# ════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────

PROJECT_DIR="/home/yousuf/PROJECTS/PeopleNet"
LOG_FILE="${PROJECT_DIR}/logs/master_pipeline_$(date +%Y%m%d_%H%M%S).log"
REPORT_FILE="${PROJECT_DIR}/REPORT_$(date +%Y%m%d_%H%M%S).txt"

# Default parameters
START_DATE=""
END_DATE=""
BATCH="both"  # park_f, park_r, or both
AUTO_BACKUP=false
DELETE_LOCAL=false

# Detection parameters (CRITICAL - DON'T CHANGE WITHOUT TESTING)
CONFIDENCE=0.8  # 0.6 = too many false positives
BUFFER_SEC=1    # 4s = clips too long and empty

# Resource limits
GPU_WORKERS=3
STAGING_MAX=20
STAGING_MIN=10
MIN_FREE_GB=10

# Docker configuration
DOCKER_IMAGE="nvcr.io/nvidia/tensorrt:24.08-py3"
LOG_MAX_SIZE="50m"
LOG_MAX_FILES="3"

# Source paths
CARDV_BASE="/media/yousuf/C67813AB7813996F1/Users/yousu/Desktop/CARDV"
GDRIVE_BASE="/home/yousuf/GoogleDrive/PROJECTS/PeopleNet"

# ────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ────────────────────────────────────────────────────────────────────────────

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR: $*"
    exit 1
}

banner() {
    local msg="$1"
    log ""
    log "════════════════════════════════════════════════════════════════"
    log "$msg"
    log "════════════════════════════════════════════════════════════════"
}

check_prerequisite() {
    local name="$1"
    local cmd="$2"

    if eval "$cmd" >/dev/null 2>&1; then
        log "✓ $name: OK"
        return 0
    else
        error "$name: FAILED - $cmd"
    fi
}

# ────────────────────────────────────────────────────────────────────────────
# Parse Arguments
# ────────────────────────────────────────────────────────────────────────────

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --start-date DATE     Process videos from this date onwards (YYYY-MM-DD)
    --end-date DATE       Process videos up to this date (optional)
    --batch BATCH         Which batch to process: park_f, park_r, both (default: both)
    --auto-backup         Automatically backup to Google Drive when done
    --delete-local        Delete local files after successful backup
    --help                Show this help message

Examples:
    # Process videos from Nov 14 onwards, auto-backup
    $0 --start-date 2025-11-14 --auto-backup

    # Process specific date range
    $0 --start-date 2025-11-01 --end-date 2025-11-14

    # Process only Park_F, no backup
    $0 --batch park_f --start-date 2025-11-14
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --start-date)
            START_DATE="$2"
            shift 2
            ;;
        --end-date)
            END_DATE="$2"
            shift 2
            ;;
        --batch)
            BATCH="$2"
            shift 2
            ;;
        --auto-backup)
            AUTO_BACKUP=true
            shift
            ;;
        --delete-local)
            DELETE_LOCAL=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Validate required parameters
[[ -z "$START_DATE" ]] && error "Missing required parameter: --start-date"
[[ ! "$BATCH" =~ ^(park_f|park_r|both)$ ]] && error "Invalid batch: $BATCH (must be park_f, park_r, or both)"

# ────────────────────────────────────────────────────────────────────────────
# Initialization
# ────────────────────────────────────────────────────────────────────────────

cd "$PROJECT_DIR"
mkdir -p logs Staging Outputs

banner "PeopleNet Autonomous Pipeline Starting"
log "Configuration:"
log "  Start Date: $START_DATE"
log "  End Date: ${END_DATE:-latest}"
log "  Batch: $BATCH"
log "  Auto Backup: $AUTO_BACKUP"
log "  Confidence: $CONFIDENCE"
log "  Buffer: ${BUFFER_SEC}s"
log "  GPU Workers: $GPU_WORKERS"

# ────────────────────────────────────────────────────────────────────────────
# Prerequisites Check
# ────────────────────────────────────────────────────────────────────────────

banner "Checking Prerequisites"

check_prerequisite "GPU" "nvidia-smi"
check_prerequisite "Docker" "docker --version"
check_prerequisite "External Drive" "test -d $CARDV_BASE"
check_prerequisite "Google Drive" "test -d ~/GoogleDrive"

# Check disk space
free_gb=$(df / | tail -1 | awk '{print int($4/1024/1024)}')
if [ "$free_gb" -lt "$MIN_FREE_GB" ]; then
    error "Insufficient disk space: ${free_gb}GB (need ${MIN_FREE_GB}GB+)"
fi
log "✓ Disk space: ${free_gb}GB free"

# ────────────────────────────────────────────────────────────────────────────
# Date Filtering
# ────────────────────────────────────────────────────────────────────────────

create_video_list() {
    local camera="$1"  # Park_F or Park_R
    local output_file="$2"

    log "Creating video list for $camera (from $START_DATE)..."

    # Convert date to regex pattern
    # 2025-11-14 → grep pattern for YYYYMMDD format
    local start_yyyymmdd=$(echo "$START_DATE" | tr -d '-')

    # Build date range regex
    local date_pattern
    if [[ -z "$END_DATE" ]]; then
        # From start_date onwards
        # This is complex - need to handle YYYYMMDD >= start_yyyymmdd
        # Simpler: Just grep for files >= start date
        date_pattern="$start_yyyymmdd"
    else
        local end_yyyymmdd=$(echo "$END_DATE" | tr -d '-')
        date_pattern="${start_yyyymmdd}|${end_yyyymmdd}"
    fi

    # Find videos matching date
    find "${CARDV_BASE}/${camera}/" -name "*.MP4" 2>/dev/null | \
        awk -v start="$start_yyyymmdd" '
        {
            # Extract date from filename: YYYYMMDDHHmmss_NNNNNN.MP4
            match($0, /([0-9]{8})[0-9]{6}_/, arr)
            if (arr[1] >= start) {
                print $0
            }
        }' | sort > "$output_file"

    local count=$(wc -l < "$output_file")
    log "  Found $count videos for $camera"
    echo "$count"
}

# ────────────────────────────────────────────────────────────────────────────
# Processing Functions
# ────────────────────────────────────────────────────────────────────────────

process_batch() {
    local batch_name="$1"  # Park_F_Batch1 or Park_R_Batch1
    local video_list="$2"
    local total_videos="$3"

    banner "Processing $batch_name ($total_videos videos)"

    local container_name="peoplenet-${batch_name,,}"  # Lowercase
    local staging_dir="${PROJECT_DIR}/Staging/${batch_name}"
    local output_dir="${PROJECT_DIR}/Outputs/${batch_name}"

    mkdir -p "$staging_dir" "$output_dir"

    # Start Docker container
    log "Starting Docker container: $container_name"

    # Remove if exists
    docker rm -f "$container_name" 2>/dev/null || true

    docker run -d \
        --name "$container_name" \
        --gpus all \
        --runtime=nvidia \
        --log-driver json-file \
        --log-opt max-size="$LOG_MAX_SIZE" \
        --log-opt max-file="$LOG_MAX_FILES" \
        -v "${PROJECT_DIR}:/workspace" \
        "$DOCKER_IMAGE" \
        sleep infinity >> "$LOG_FILE" 2>&1

    log "Installing dependencies..."
    docker exec "$container_name" bash -c \
        "apt-get update -qq && apt-get install -y -qq ffmpeg && \
         pip install -q opencv-python-headless onnxruntime-gpu numpy" \
        >> "$LOG_FILE" 2>&1

    # Verify worker.py has correct settings
    log "Configuring worker settings..."
    docker exec "$container_name" bash -c "
        sed -i 's/confidence_threshold=[0-9.]\+/confidence_threshold=$CONFIDENCE/' /workspace/worker.py
        sed -i 's/buffer_seconds=[0-9]\+/buffer_seconds=$BUFFER_SEC/' /workspace/worker.py
    " >> "$LOG_FILE" 2>&1

    # Start GPU workers
    log "Starting $GPU_WORKERS GPU workers..."
    for worker_id in $(seq 1 $GPU_WORKERS); do
        docker exec -d "$container_name" bash -c \
            "cd /workspace && BATCH_NAME=${batch_name} python3 worker.py ${worker_id}" \
            >> "$LOG_FILE" 2>&1
        log "  Worker $worker_id started"
    done

    # Copy initial videos
    log "Copying initial videos to staging..."
    head -30 "$video_list" | xargs -I {} cp {} "$staging_dir/" 2>/dev/null || true

    # Start controlled feed
    log "Starting controlled feed..."
    cat > /tmp/feed_${batch_name}.sh << EOF
#!/bin/bash
while true; do
    staging_count=\$(find "$staging_dir" -name "*.MP4" 2>/dev/null | wc -l)
    if [ "\$staging_count" -lt $STAGING_MIN ]; then
        needed=\$(( $STAGING_MAX - \$staging_count ))
        while IFS= read -r video_path && [ "\$copied" -lt "\$needed" ]; do
            [ ! -f "\$video_path" ] && continue
            video_name=\$(basename "\$video_path")
            [ -f "$staging_dir/\$video_name" ] && continue
            if [ -f "$output_dir/processed_videos.txt" ]; then
                grep -q "^\$video_name\$" "$output_dir/processed_videos.txt" 2>/dev/null && continue
            fi
            cp "\$video_path" "$staging_dir/" 2>/dev/null && ((copied++)) || true
        done < "$video_list"
    fi
    sleep 10
done
EOF
    chmod +x /tmp/feed_${batch_name}.sh
    nohup /tmp/feed_${batch_name}.sh >> "${PROJECT_DIR}/logs/feed_${batch_name}.log" 2>&1 &
    local feed_pid=$!
    log "  Feed started (PID: $feed_pid)"

    # Start auto-ownership fixer
    cat > /tmp/ownership_${batch_name}.sh << 'EOF'
#!/bin/bash
while true; do
    sudo chown -R yousuf:yousuf OUTPUT_DIR/*.mp4 2>/dev/null || true
    sleep 30
done
EOF
    sed -i "s|OUTPUT_DIR|$output_dir|" /tmp/ownership_${batch_name}.sh
    chmod +x /tmp/ownership_${batch_name}.sh
    nohup /tmp/ownership_${batch_name}.sh >> /dev/null 2>&1 &
    local ownership_pid=$!
    log "  Ownership fixer started (PID: $ownership_pid)"

    # Monitor progress
    log "Processing started. Monitoring progress..."
    local last_count=0
    local no_progress_count=0

    while true; do
        sleep 60

        local processed=$(wc -l < "$output_dir/processed_videos.txt" 2>/dev/null || echo 0)
        local clips=$(find "$output_dir" -name "*.mp4" 2>/dev/null | wc -l)
        local staging=$(find "$staging_dir" -name "*.MP4" 2>/dev/null | wc -l)

        local pct=$(echo "scale=1; $processed * 100 / $total_videos" | bc)
        log "Progress: $processed/$total_videos videos (${pct}%), $clips clips, $staging in staging"

        # Check if complete
        if [ "$processed" -ge "$total_videos" ]; then
            log "✓ $batch_name complete!"
            break
        fi

        # Check for stalled processing
        if [ "$processed" -eq "$last_count" ]; then
            ((no_progress_count++))
            if [ "$no_progress_count" -ge 5 ]; then
                log "WARNING: No progress in 5 minutes. Checking workers..."
                docker exec "$container_name" ps aux | grep python >> "$LOG_FILE"
            fi
        else
            no_progress_count=0
        fi
        last_count=$processed
    done

    # Cleanup
    log "Stopping container and background processes..."
    docker stop "$container_name" >> "$LOG_FILE" 2>&1 || true
    kill $feed_pid $ownership_pid 2>/dev/null || true
    rm -f "$staging_dir"/*.MP4

    # Final stats
    local final_clips=$(find "$output_dir" -name "*.mp4" 2>/dev/null | wc -l)
    local final_size=$(du -sh "$output_dir" | awk '{print $1}')
    local detection_rate=$(echo "scale=1; $final_clips * 100 / $total_videos" | bc)

    log ""
    log "$batch_name Results:"
    log "  Videos: $total_videos"
    log "  Clips: $final_clips"
    log "  Detection Rate: ${detection_rate}%"
    log "  Output Size: $final_size"
    log ""
}

# ────────────────────────────────────────────────────────────────────────────
# Backup Function
# ────────────────────────────────────────────────────────────────────────────

backup_to_gdrive() {
    local batch_name="$1"
    local output_dir="${PROJECT_DIR}/Outputs/${batch_name}"
    local gdrive_dir="${GDRIVE_BASE}/${batch_name}_$(date +%Y%m%d)"

    banner "Backing up $batch_name to Google Drive"

    mkdir -p "$gdrive_dir"

    log "Copying clips..."
    rsync -ah --progress "$output_dir/"*.mp4 "$gdrive_dir/" 2>&1 | tee -a "$LOG_FILE" | grep -E "mp4|total"

    log "Copying logs..."
    cp "$output_dir/processed_videos.txt" "$gdrive_dir/" 2>/dev/null || true
    cp "$output_dir/worker_"*"_log.txt" "$gdrive_dir/" 2>/dev/null || true

    # Verify
    local local_count=$(find "$output_dir" -name "*.mp4" | wc -l)
    local gdrive_count=$(find "$gdrive_dir" -name "*.mp4" | wc -l)

    if [ "$local_count" -eq "$gdrive_count" ]; then
        log "✓ Backup verified: $gdrive_count clips"

        if [ "$DELETE_LOCAL" = true ]; then
            log "Deleting local clips..."
            rm -f "$output_dir"/*.mp4
            local freed=$(du -sh "$output_dir" | awk '{print $1}')
            log "✓ Local clips deleted"
        fi
    else
        error "Backup verification failed: local=$local_count, gdrive=$gdrive_count"
    fi

    log "✓ Backup location: $gdrive_dir"
}

# ────────────────────────────────────────────────────────────────────────────
# Main Execution
# ────────────────────────────────────────────────────────────────────────────

main() {
    local start_time=$(date +%s)

    # Create video lists
    banner "Creating Video Lists"

    local park_f_count=0
    local park_r_count=0

    if [[ "$BATCH" == "park_f" || "$BATCH" == "both" ]]; then
        park_f_count=$(create_video_list "Park_F" "${PROJECT_DIR}/park_f_list.txt")
    fi

    if [[ "$BATCH" == "park_r" || "$BATCH" == "both" ]]; then
        park_r_count=$(create_video_list "Park_R" "${PROJECT_DIR}/park_r_list.txt")
    fi

    # Process batches
    if [[ "$BATCH" == "park_f" || "$BATCH" == "both" ]] && [ "$park_f_count" -gt 0 ]; then
        process_batch "Park_F_Batch1" "${PROJECT_DIR}/park_f_list.txt" "$park_f_count"

        if [ "$AUTO_BACKUP" = true ]; then
            backup_to_gdrive "Park_F_Batch1"
        fi
    fi

    if [[ "$BATCH" == "park_r" || "$BATCH" == "both" ]] && [ "$park_r_count" -gt 0 ]; then
        process_batch "Park_R_Batch1" "${PROJECT_DIR}/park_r_list.txt" "$park_r_count"

        if [ "$AUTO_BACKUP" = true ]; then
            backup_to_gdrive "Park_R_Batch1"
        fi
    fi

    # Generate final report
    banner "Generating Final Report"

    {
        echo "PeopleNet Processing Report"
        echo "Generated: $(date)"
        echo ""
        echo "Configuration:"
        echo "  Start Date: $START_DATE"
        echo "  End Date: ${END_DATE:-latest}"
        echo "  Confidence: $CONFIDENCE"
        echo "  Buffer: ${BUFFER_SEC}s"
        echo ""

        if [ "$park_f_count" -gt 0 ]; then
            local f_clips=$(find "${PROJECT_DIR}/Outputs/Park_F_Batch1" -name "*.mp4" 2>/dev/null | wc -l)
            local f_size=$(du -sh "${PROJECT_DIR}/Outputs/Park_F_Batch1" 2>/dev/null | awk '{print $1}')
            local f_rate=$(echo "scale=1; $f_clips * 100 / $park_f_count" | bc)
            echo "Park_F Results:"
            echo "  Videos: $park_f_count"
            echo "  Clips: $f_clips"
            echo "  Detection Rate: ${f_rate}%"
            echo "  Output Size: $f_size"
            echo ""
        fi

        if [ "$park_r_count" -gt 0 ]; then
            local r_clips=$(find "${PROJECT_DIR}/Outputs/Park_R_Batch1" -name "*.mp4" 2>/dev/null | wc -l)
            local r_size=$(du -sh "${PROJECT_DIR}/Outputs/Park_R_Batch1" 2>/dev/null | awk '{print $1}')
            local r_rate=$(echo "scale=1; $r_clips * 100 / $park_r_count" | bc)
            echo "Park_R Results:"
            echo "  Videos: $park_r_count"
            echo "  Clips: $r_clips"
            echo "  Detection Rate: ${r_rate}%"
            echo "  Output Size: $r_size"
            echo ""
        fi

        local end_time=$(date +%s)
        local duration=$(( (end_time - start_time) / 60 ))
        echo "Processing Duration: ${duration} minutes"

        if [ "$AUTO_BACKUP" = true ]; then
            echo ""
            echo "Backup Location: $GDRIVE_BASE"
        fi

    } | tee "$REPORT_FILE"

    log ""
    log "✓ Report saved: $REPORT_FILE"
    log "✓ Full log: $LOG_FILE"

    banner "Pipeline Complete!"
}

# Run main
main

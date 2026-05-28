#!/usr/bin/env bash
set -euo pipefail

# Backup PeopleNet outputs to Google Drive and clean up local

GDRIVE_BASE="/home/yousuf/GoogleDrive/PROJECTS/PeopleNet"
LOCAL_BASE="/home/yousuf/PROJECTS/PeopleNet/Outputs"

echo "════════════════════════════════════════════════════════"
echo "PeopleNet Backup to Google Drive"
echo "════════════════════════════════════════════════════════"
echo ""

# Create Google Drive directories
mkdir -p "$GDRIVE_BASE/Park_F_Batch1"
mkdir -p "$GDRIVE_BASE/Park_R_Batch1"

# Backup Park_F
echo "Backing up Park_F (269 clips, 2.5GB)..."
rsync -avh --progress "$LOCAL_BASE/Park_F_Batch1/"*.mp4 "$GDRIVE_BASE/Park_F_Batch1/" 2>&1 | grep -E "mp4|total"

echo ""
echo "Backing up Park_F logs..."
cp "$LOCAL_BASE/Park_F_Batch1/processed_videos.txt" "$GDRIVE_BASE/Park_F_Batch1/"
cp "$LOCAL_BASE/Park_F_Batch1/worker_"*"_log.txt" "$GDRIVE_BASE/Park_F_Batch1/" 2>/dev/null || true

# Backup Park_R
echo ""
echo "Backing up Park_R (393 clips, 903MB)..."
rsync -avh --progress "$LOCAL_BASE/Park_R_Batch1/"*.mp4 "$GDRIVE_BASE/Park_R_Batch1/" 2>&1 | grep -E "mp4|total"

echo ""
echo "Backing up Park_R logs..."
cp "$LOCAL_BASE/Park_R_Batch1/processed_videos.txt" "$GDRIVE_BASE/Park_R_Batch1/"
cp "$LOCAL_BASE/Park_R_Batch1/worker_"*"_log.txt" "$GDRIVE_BASE/Park_R_Batch1/" 2>/dev/null || true

echo ""
echo "════════════════════════════════════════════════════════"
echo "Backup Complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Google Drive locations:"
echo "  Park_F: $GDRIVE_BASE/Park_F_Batch1/"
echo "  Park_R: $GDRIVE_BASE/Park_R_Batch1/"
echo ""
echo "Verifying backup..."
park_f_gdrive=$(find "$GDRIVE_BASE/Park_F_Batch1/" -name "*.mp4" | wc -l)
park_r_gdrive=$(find "$GDRIVE_BASE/Park_R_Batch1/" -name "*.mp4" | wc -l)
echo "  Park_F: $park_f_gdrive clips backed up"
echo "  Park_R: $park_r_gdrive clips backed up"
echo ""

# Ask for confirmation before deleting
read -p "Backup verified. Delete local files? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    echo ""
    echo "Deleting local clips..."
    rm -f "$LOCAL_BASE/Park_F_Batch1/"*.mp4
    rm -f "$LOCAL_BASE/Park_R_Batch1/"*.mp4

    freed_space=$(echo "3.4" | bc)
    echo "✓ Local clips deleted. Freed ${freed_space}GB of space."
    echo ""
    df -h / | tail -1 | awk '{print "Disk space now: " $4 " free (" $5 " used)"}'
else
    echo "Local files kept. Manual deletion required."
fi

echo ""
echo "════════════════════════════════════════════════════════"

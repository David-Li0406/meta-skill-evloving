#!/usr/bin/env bash
# Auto-fix ownership of output files every 30 seconds

OUTPUT_DIR="/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1"

while true; do
    # Fix ownership of any root-owned MP4s
    sudo chown yousuf:yousuf "${OUTPUT_DIR}"/*.mp4 2>/dev/null
    sleep 30
done

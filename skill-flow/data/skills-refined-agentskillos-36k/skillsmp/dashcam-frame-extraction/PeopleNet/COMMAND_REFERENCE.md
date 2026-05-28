# Quick Command Reference Sheet

## Complete Pipeline Execution (Copy-Paste Ready)

### Setup Phase (One-Time)

```bash
# 1. Create directory structure
mkdir -p /home/yousuf/PROJECTS/PeopleNet/model
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/locks
mkdir -p /home/yousuf/PROJECTS/PeopleNet/Corrupted_Videos
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt
touch /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1/processed_videos.txt

# 2. Download PeopleNet model
# Manually download resnet34_peoplenet_int8.onnx from NVIDIA NGC
# Place at: /home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx

# 3. Create Docker containers
docker run -d \
    --name peoplenet-park-r \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

docker run -d \
    --name peoplenet-park-f \
    --gpus all \
    --runtime=nvidia \
    -v /home/yousuf/PROJECTS/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 \
    sleep infinity

# 4. Install ffmpeg (CRITICAL - DO NOT SKIP)
docker exec peoplenet-park-r apt-get update && docker exec peoplenet-park-r apt-get install -y ffmpeg
docker exec peoplenet-park-f apt-get update && docker exec peoplenet-park-f apt-get install -y ffmpeg

# Verify ffmpeg installed
docker exec peoplenet-park-r ffmpeg -version
docker exec peoplenet-park-f ffmpeg -version
```

---

## Phase 1: SSIM Filtering

```bash
# Run SSIM filter for Park_R
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R" \
    /home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt \
    0.85

# Run SSIM filter for Park_F
python3 /tmp/ssim_filter.py \
    "/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_F" \
    /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt \
    0.85

# Verify filtered lists created
wc -l /home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt
wc -l /home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt
```

---

## Phase 2: Deploy Workers

### For Park_R

```bash
# 1. Create worker script (use gpu_worker_continuous.py from main docs)
# Update these paths in the script:
# STAGING_DIR = "/workspace/Staging/Park_R_Batch1"
# OUTPUT_DIR = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1"
# PROCESSED_LIST = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt"
# LOCK_DIR = "/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/locks"
# LOG_FILE = f"/workspace/Outputs/GPU_Pipeline_Park_R_Batch1/worker_{WORKER_ID}_log.txt"

# 2. Copy to container
docker cp /tmp/gpu_worker_continuous.py peoplenet-park-r:/workspace/worker.py

# 3. Start 3 workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# 4. Verify workers running
docker exec peoplenet-park-r ps aux | grep python3
```

### For Park_F

```bash
# Same process but update paths to Park_F_Batch1
# STAGING_DIR = "/workspace/Staging/Park_F_Batch1"
# OUTPUT_DIR = "/workspace/Outputs/GPU_Pipeline_Park_F_Batch1"
# etc.

docker cp /tmp/gpu_worker_continuous.py peoplenet-park-f:/workspace/worker.py
docker exec -d peoplenet-park-f python3 /workspace/worker.py 1
docker exec -d peoplenet-park-f python3 /workspace/worker.py 2
docker exec -d peoplenet-park-f python3 /workspace/worker.py 3
```

---

## Phase 3: Start Copy Agent

### For Park_R

```bash
# 1. Create copy agent script (use batch_copy_agent.sh from main docs)
# Update these paths:
# SOURCE="/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R"
# STAGING="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1"
# PROCESSED_LIST="/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt"
# FILTER_LIST="/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt"

# 2. Make executable
chmod +x /tmp/batch_copy_agent.sh

# 3. Start in background
nohup /tmp/batch_copy_agent.sh > /tmp/park_r_copy.log 2>&1 &

# 4. Verify running
ps aux | grep batch_copy_agent | grep -v grep
```

### For Park_F

```bash
# Same process with Park_F paths
nohup /tmp/batch_copy_agent_park_f.sh > /tmp/park_f_copy.log 2>&1 &
```

---

## Monitoring Commands

### Quick Status Check

```bash
# All-in-one status
echo "=== Park_R Pipeline Status ==="
echo "Processed: $(wc -l < /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt)"
echo "Staging: $(ls /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1/*.MP4 2>/dev/null | wc -l)"
echo "Clips: $(ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 2>/dev/null | wc -l)"
echo "Disk: $(df -h /home/yousuf/PROJECTS/PeopleNet | tail -1 | awk '{print $4}')"
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
```

### Watch Progress Live

```bash
# Watch worker 1 log
tail -f /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/worker_1_log.txt

# Watch copy agent log
tail -f /tmp/park_r_copy.log

# Watch processed count
watch -n 5 'wc -l /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt'
```

### Check System Resources

```bash
# GPU status
nvidia-smi

# Disk space
df -h /home/yousuf/PROJECTS/PeopleNet

# Worker processes
docker exec peoplenet-park-r ps aux | grep python3

# Copy agent process
ps aux | grep batch_copy_agent | grep -v grep
```

---

## Emergency Stop Commands

```bash
# Stop all workers
docker exec peoplenet-park-r pkill -9 python3
docker exec peoplenet-park-f pkill -9 python3

# Stop copy agents
pkill -9 -f batch_copy_agent

# Stop containers
docker stop peoplenet-park-r peoplenet-park-f
```

---

## Emergency Restart Commands

```bash
# Restart containers
docker start peoplenet-park-r
docker start peoplenet-park-f

# Wait for containers to be ready
sleep 3

# Restart workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

docker exec -d peoplenet-park-f python3 /workspace/worker.py 1
docker exec -d peoplenet-park-f python3 /workspace/worker.py 2
docker exec -d peoplenet-park-f python3 /workspace/worker.py 3

# Restart copy agents
nohup /tmp/batch_copy_agent.sh > /tmp/park_r_copy.log 2>&1 &
nohup /tmp/batch_copy_agent_park_f.sh > /tmp/park_f_copy.log 2>&1 &
```

---

## Clean Restart (After Issue Fix)

```bash
# 1. Stop everything
docker exec peoplenet-park-r pkill -9 python3
pkill -9 -f batch_copy_agent

# 2. Clear staging
rm -f /home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1/*.MP4

# 3. Clear locks
rm -f /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks/*.lock

# 4. Optionally reset progress (CAUTION)
# cp /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt /tmp/backup.txt
# echo "" > /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt

# 5. Verify ffmpeg installed
docker exec peoplenet-park-r ffmpeg -version

# 6. Restart workers
docker exec -d peoplenet-park-r python3 /workspace/worker.py 1
docker exec -d peoplenet-park-r python3 /workspace/worker.py 2
docker exec -d peoplenet-park-r python3 /workspace/worker.py 3

# 7. Restart copy agent
nohup /tmp/batch_copy_agent.sh > /tmp/park_r_copy.log 2>&1 &

# 8. Monitor for 30 seconds
sleep 30
tail -20 /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/worker_1_log.txt
```

---

## Manual Video Processing (Testing)

```bash
# Process a single video manually
docker exec -it peoplenet-park-r python3 -c "
import sys
sys.path.insert(0, '/workspace')
exec(open('/workspace/worker.py').read())

worker = ContinuousGPUWorker(999)
clips = worker.process_video('/workspace/Staging/Park_R_Batch1/test_video.MP4')
print(f'Created {len(clips)} clips')
"
```

---

## Data Analysis Commands

```bash
# Count total clips created
ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 2>/dev/null | wc -l

# Total size of clips
du -sh /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/

# Detection rate
PROCESSED=$(wc -l < /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt)
CLIPS=$(ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 2>/dev/null | wc -l)
echo "Detection rate: $(echo "scale=1; $CLIPS * 100 / $PROCESSED" | bc)%"

# Average clips per detected video
echo "Avg clips per video: $(echo "scale=2; $CLIPS / $PROCESSED" | bc)"

# Processing speed (videos per minute)
# Check start/end times in worker logs, then:
START_TIME="21:50"  # From logs
END_TIME="23:37"    # From logs
# Calculate manually or use time tracking

# Find videos with most detections
ls /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 | \
    sed 's/.*\///;s/_people.*//' | sort | uniq -c | sort -rn | head -20
```

---

## Performance Optimization Commands

```bash
# Check current batch settings
grep -E "BATCH_SIZE|CHECK_INTERVAL|MIN_STAGING_THRESHOLD" /tmp/batch_copy_agent.sh

# Check worker idle time
grep "Queue empty" /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/worker_*.txt | wc -l

# If idle count > 100, optimize:
sed -i 's/BATCH_SIZE=10/BATCH_SIZE=50/' /tmp/batch_copy_agent.sh
sed -i 's/CHECK_INTERVAL=30/CHECK_INTERVAL=5/' /tmp/batch_copy_agent.sh

# Restart copy agent
pkill -f batch_copy_agent
nohup /tmp/batch_copy_agent.sh > /tmp/park_r_copy.log 2>&1 &
```

---

## Corrupt Video Handling

```bash
# Find videos that failed
grep "Error processing\|Failed to open" /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/worker_*.txt

# Quarantine corrupt video
VIDEO="20250829031923_058011B.MP4"
mv "/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1/$VIDEO" \
   /home/yousuf/PROJECTS/PeopleNet/Corrupted_Videos/

# Remove from processed list
sed -i "/$VIDEO/d" /home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt

# Clear lock
rm -f "/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks/$VIDEO.lock"
```

---

## Path Reference (Quick Copy)

```bash
# Source videos
PARK_R_SOURCE="/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_R"
PARK_F_SOURCE="/media/yousuf/C67813AB7813996F1/Documents and Settings/yousu/Desktop/CARDV/Park_F"

# Model
MODEL="/home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx"

# Filtered lists
PARK_R_LIST="/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt"
PARK_F_LIST="/home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt"

# Staging
PARK_R_STAGING="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1"
PARK_F_STAGING="/home/yousuf/PROJECTS/PeopleNet/Staging/Park_F_Batch1"

# Outputs
PARK_R_OUTPUT="/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1"
PARK_F_OUTPUT="/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_F_Batch1"

# Processed tracking
PARK_R_PROCESSED="$PARK_R_OUTPUT/processed_videos.txt"
PARK_F_PROCESSED="$PARK_F_OUTPUT/processed_videos.txt"

# Logs
PARK_R_WORKER_LOG="$PARK_R_OUTPUT/worker_1_log.txt"
PARK_F_WORKER_LOG="$PARK_F_OUTPUT/worker_1_log.txt"
PARK_R_COPY_LOG="/tmp/park_r_copy.log"
PARK_F_COPY_LOG="/tmp/park_f_copy.log"

# Scripts
SSIM_FILTER="/tmp/ssim_filter.py"
WORKER_SCRIPT="/tmp/gpu_worker_continuous.py"
COPY_AGENT="/tmp/batch_copy_agent.sh"
```

---

## Final Checklist Before Starting

```bash
# Verify everything is in place
echo "Checking prerequisites..."

# 1. Model exists
[ -f "/home/yousuf/PROJECTS/PeopleNet/model/resnet34_peoplenet_int8.onnx" ] && echo "✓ Model found" || echo "✗ Model missing"

# 2. Containers running
docker ps | grep -q "peoplenet-park-r" && echo "✓ Park_R container running" || echo "✗ Park_R container not running"
docker ps | grep -q "peoplenet-park-f" && echo "✓ Park_F container running" || echo "✗ Park_F container not running"

# 3. ffmpeg installed
docker exec peoplenet-park-r which ffmpeg > /dev/null 2>&1 && echo "✓ Park_R ffmpeg installed" || echo "✗ Park_R ffmpeg missing"
docker exec peoplenet-park-f which ffmpeg > /dev/null 2>&1 && echo "✓ Park_F ffmpeg installed" || echo "✗ Park_F ffmpeg missing"

# 4. Worker scripts deployed
docker exec peoplenet-park-r test -f /workspace/worker.py && echo "✓ Park_R worker deployed" || echo "✗ Park_R worker missing"
docker exec peoplenet-park-f test -f /workspace/worker.py && echo "✓ Park_F worker deployed" || echo "✗ Park_F worker missing"

# 5. Copy agent scripts exist
[ -f "/tmp/batch_copy_agent.sh" ] && echo "✓ Copy agent exists" || echo "✗ Copy agent missing"

# 6. Filtered lists exist
[ -f "/home/yousuf/PROJECTS/PeopleNet/park_r_process_list.txt" ] && echo "✓ Park_R filter list exists" || echo "✗ Park_R filter list missing"
[ -f "/home/yousuf/PROJECTS/PeopleNet/park_f_process_list.txt" ] && echo "✓ Park_F filter list exists" || echo "✗ Park_F filter list missing"

# 7. Directories exist
[ -d "/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1" ] && echo "✓ Park_R staging exists" || echo "✗ Park_R staging missing"
[ -d "/home/yousuf/PROJECTS/PeopleNet/Outputs/GPU_Pipeline_Park_R_Batch1/locks" ] && echo "✓ Park_R locks dir exists" || echo "✗ Park_R locks dir missing"

# 8. GPU available
nvidia-smi > /dev/null 2>&1 && echo "✓ GPU accessible" || echo "✗ GPU not accessible"

echo ""
echo "If all checks pass, you can start the pipeline!"
```

---

**End of Command Reference**

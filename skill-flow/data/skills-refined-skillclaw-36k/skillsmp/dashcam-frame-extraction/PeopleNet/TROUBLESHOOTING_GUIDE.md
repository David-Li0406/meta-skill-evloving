# Pipeline Troubleshooting Guide

## Quick Diagnostic Commands

```bash
# Check everything at once
echo "=== Pipeline Status ==="
echo "Processed: $(wc -l < /path/to/processed_videos.txt)"
echo "Staging: $(ls /path/to/staging/*.MP4 2>/dev/null | wc -l)"
echo "Clips: $(ls /path/to/outputs/*.mp4 2>/dev/null | wc -l)"
echo "Disk: $(df -h /path/to/outputs | tail -1 | awk '{print $4}')"
echo "Workers: $(docker exec container-name ps aux | grep python3 | wc -l)"
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv
```

---

## Problem: No Clips Being Created

### Diagnostic Steps

1. **Check if ffmpeg is installed**:
```bash
docker exec container-name ffmpeg -version
```
If error: `bash: ffmpeg: command not found`
- **Solution**: Install ffmpeg in container
```bash
docker exec container-name apt-get update
docker exec container-name apt-get install -y ffmpeg
```

2. **Check worker logs for errors**:
```bash
tail -50 /path/to/outputs/worker_1_log.txt
```
Look for:
- `Error processing ... ffmpeg` → Install ffmpeg
- `Failed to open` → Check video file integrity
- `No such file or directory` → Check paths in worker script

3. **Verify detection is working**:
```bash
# Check if any "clips" entries exist
grep "clips" /path/to/outputs/worker_*.txt
```
If only "No people" entries:
- Videos may genuinely have no people
- Confidence threshold may be too high
- Model may not be loaded correctly

4. **Test with known good video**:
Create test script to verify detection works:
```python
import cv2
import onnxruntime as ort
import numpy as np

model = ort.InferenceSession("/path/to/model.onnx")
cap = cv2.VideoCapture("/path/to/test/video.MP4")
ret, frame = cap.read()

img = cv2.resize(frame, (960, 544))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

outputs = model.run(None, {'input_1:0': img})
print(f"Max confidence: {outputs[0][0, 0, :, :].max()}")
```

---

## Problem: Workers Are Idle

### Symptoms
- Low GPU utilization (< 5%)
- Workers log: "Queue empty. Waiting..."
- Staging directory empty or near-empty

### Diagnostic Steps

1. **Check copy agent is running**:
```bash
ps aux | grep copy_agent
```
If not running:
```bash
nohup /path/to/copy_agent.sh > /tmp/copy.log 2>&1 &
```

2. **Check copy agent logs**:
```bash
tail -50 /tmp/copy.log
```
Look for:
- `cannot access` → Check source path
- `Permission denied` → Fix permissions
- `Low disk space` → Free up space

3. **Check batch size configuration**:
```bash
grep "BATCH_SIZE" /path/to/copy_agent.sh
grep "CHECK_INTERVAL" /path/to/copy_agent.sh
```
Recommended:
- BATCH_SIZE=50
- CHECK_INTERVAL=5
- MIN_STAGING_THRESHOLD=20

4. **Manually verify source videos exist**:
```bash
ls "/path/to/source/videos/" | head -10
```

---

## Problem: Staging Directory Full, Not Processing

### Symptoms
- 50+ videos in staging
- Copy agent waiting
- Workers running but not processing videos

### Diagnostic Steps

1. **Check if videos are being deleted after processing**:
```bash
# Wait 30 seconds and check again
sleep 30 && ls staging/*.MP4 | wc -l
```
If count doesn't decrease:
- Workers not deleting videos after processing

2. **Check worker script has deletion code**:
```bash
docker exec container-name grep "os.remove(video_path)" /workspace/worker.py
```
If not found, add to `release_video()` function:
```python
# Delete video from staging to free up space
try:
    os.remove(video_path)
except:
    pass
```

3. **Manual cleanup (temporary fix)**:
```bash
# Check what's processed
cat /path/to/processed_videos.txt

# Delete processed videos from staging
cd /path/to/staging
while IFS= read -r video; do
    rm -f "$video"
done < /path/to/processed_videos.txt
```

---

## Problem: Disk Space Running Out

### Symptoms
- Disk usage > 90%
- Copy agent logs: "Low disk space"
- System warnings

### Diagnostic Steps

1. **Check disk usage breakdown**:
```bash
du -sh /path/to/PeopleNet/*
```

2. **Check if source videos still in staging**:
```bash
du -sh /path/to/staging
```
Should be < 10GB. If larger:
- Videos not being deleted after processing
- See "Staging Directory Full" section

3. **Check output clips size**:
```bash
du -sh /path/to/outputs/*.mp4
```
This is expected to grow. Each clip ~20-40MB.

4. **Emergency cleanup**:
```bash
# Stop copy agent
pkill -f copy_agent

# Clear staging (only if processed)
cd /path/to/staging
cat /path/to/processed_videos.txt | xargs rm -f

# Resume copy agent
nohup /path/to/copy_agent.sh > /tmp/copy.log 2>&1 &
```

---

## Problem: Workers Crashed or Exited

### Symptoms
- No worker processes in container
- Processing stopped
- GPU idle

### Diagnostic Steps

1. **Check worker processes**:
```bash
docker exec container-name ps aux | grep python3
```

2. **Check why workers stopped**:
```bash
tail -100 /path/to/outputs/worker_1_log.txt
```
Common causes:
- OOM (Out of memory)
- Model file not found
- Python exception

3. **Check container is running**:
```bash
docker ps | grep container-name
```
If not running:
```bash
docker start container-name
```

4. **Restart workers**:
```bash
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3
```

---

## Problem: GPU Not Being Used

### Symptoms
- GPU utilization 0%
- Workers using CPU only
- Very slow processing

### Diagnostic Steps

1. **Check CUDA availability in container**:
```bash
docker exec container-name nvidia-smi
```
If error:
- Container not started with `--gpus all`
- Recreate container with nvidia runtime

2. **Check ONNX providers**:
```bash
docker exec container-name python3 -c "import onnxruntime; print(onnxruntime.get_available_providers())"
```
Should show: `['CUDAExecutionProvider', 'CPUExecutionProvider']`

If only CPUExecutionProvider:
```bash
# Install onnxruntime-gpu
docker exec container-name pip install onnxruntime-gpu
```

3. **Check worker logs for provider**:
```bash
grep "ready! Using" /path/to/outputs/worker_1_log.txt
```
Should show: `Using: ['CUDAExecutionProvider', 'CPUExecutionProvider']`

---

## Problem: Permission Denied Errors

### Common Permission Issues

1. **processed_videos.txt permission denied**:
```bash
sudo chown $USER:$USER /path/to/processed_videos.txt
```

2. **Cannot write to staging**:
```bash
sudo chown -R $USER:$USER /path/to/staging
chmod 755 /path/to/staging
```

3. **Cannot create locks**:
```bash
sudo chown -R $USER:$USER /path/to/outputs/locks
```

4. **Copy agent can't access source**:
```bash
# Check if drive is mounted
df -h | grep "source-drive"

# Check permissions
ls -ld "/path/to/source/videos"
```

---

## Problem: Videos Marked as Processed But No Clips

### This is a CRITICAL issue - indicates ffmpeg was missing

### Diagnostic Steps

1. **Verify ffmpeg was installed**:
```bash
docker exec container-name which ffmpeg
```

2. **Check detection actually happened**:
Create test script to re-check confidence:
```python
# Use check_confidence.py from main documentation
# Run on random sample of "processed" videos
```

3. **If ffmpeg was missing, must reprocess**:
```bash
# Stop everything
docker exec container-name pkill python3
pkill -f copy_agent

# Clear processed list (backup first!)
cp /path/to/processed_videos.txt /path/to/processed_videos.txt.backup
echo "" > /path/to/processed_videos.txt

# Clear staging
rm -f /path/to/staging/*.MP4

# Clear locks
rm -f /path/to/outputs/locks/*.lock

# Install ffmpeg
docker exec container-name apt-get install -y ffmpeg

# Restart pipeline
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3
nohup /path/to/copy_agent.sh > /tmp/copy.log 2>&1 &
```

---

## Problem: Corrupt Video Files

### Symptoms
- Workers hang on specific videos
- Errors in logs:
  - "Invalid NAL unit size"
  - "partial file"
  - "OpenCV assertion failed"

### Solution

1. **Identify corrupt video**:
```bash
# Check worker logs for video name
grep "Error processing" /path/to/outputs/worker_*.txt
```

2. **Quarantine corrupt videos**:
```bash
mkdir -p /path/to/Corrupted_Videos
mv /path/to/staging/corrupt_video.MP4 /path/to/Corrupted_Videos/
```

3. **Remove from processed list if needed**:
```bash
# Remove line for corrupt video
sed -i '/corrupt_video.MP4/d' /path/to/processed_videos.txt
```

4. **Clear its lock file**:
```bash
rm -f /path/to/outputs/locks/corrupt_video.MP4.lock
```

---

## Problem: Processing Is Too Slow

### Expected Speed: 70-75 videos/minute with 3 workers

If significantly slower:

1. **Check worker idle time**:
```bash
grep "Queue empty" /path/to/outputs/worker_*.txt | tail -20
```
If frequent (every 1-2 minutes):
- Batch size too small
- Check interval too long

**Solution**: Optimize copy agent
```bash
# Edit copy agent script
BATCH_SIZE=50              # Increase from 10
CHECK_INTERVAL=5           # Decrease from 30
MIN_STAGING_THRESHOLD=20   # Add this line
```

2. **Check GPU utilization**:
```bash
nvidia-smi
```
If < 5%:
- Workers spending too much time idle
- Increase batch size

If > 80%:
- GPU bottleneck
- Reduce worker count or sample rate

3. **Check disk I/O**:
```bash
iostat -x 5
```
If %util > 80%:
- Disk bottleneck
- Use faster disk (SSD) for staging
- Reduce worker count

---

## Problem: Container Won't Start

### Diagnostic Steps

1. **Check docker daemon**:
```bash
sudo systemctl status docker
```

2. **Check nvidia-docker runtime**:
```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

3. **Check container logs**:
```bash
docker logs container-name
```

4. **Recreate container**:
```bash
docker rm container-name
docker run -d --name container-name --gpus all --runtime=nvidia \
    -v /path/to/PeopleNet:/workspace \
    nvcr.io/nvidia/tensorrt:24.08-py3 sleep infinity
```

---

## Verification Checklist

After fixing any issue, verify:

- [ ] ffmpeg is installed: `docker exec container-name ffmpeg -version`
- [ ] Workers are running: `docker exec container-name ps aux | grep python3`
- [ ] Copy agent is running: `ps aux | grep copy_agent`
- [ ] GPU is being used: `nvidia-smi`
- [ ] Clips are being created: `ls /path/to/outputs/*.mp4 | wc -l`
- [ ] Staging is manageable: `ls /path/to/staging/*.MP4 | wc -l` (should be 20-60)
- [ ] Disk space sufficient: `df -h` (should have >20GB free)
- [ ] Processing count increasing: `wc -l /path/to/processed_videos.txt`

---

## Emergency Recovery Commands

```bash
#!/bin/bash
# Emergency pipeline recovery script

echo "Stopping all processes..."
docker exec container-name pkill -9 python3
pkill -9 -f copy_agent

echo "Checking system resources..."
df -h /path/to/PeopleNet
nvidia-smi

echo "Verifying ffmpeg..."
docker exec container-name which ffmpeg

echo "Clearing staging (WARNING: deletes all files)..."
rm -f /path/to/staging/*.MP4

echo "Clearing locks..."
rm -f /path/to/outputs/locks/*.lock

echo "Restarting container..."
docker restart container-name
sleep 5

echo "Starting workers..."
docker exec -d container-name python3 /workspace/worker.py 1
docker exec -d container-name python3 /workspace/worker.py 2
docker exec -d container-name python3 /workspace/worker.py 3

echo "Starting copy agent..."
nohup /path/to/copy_agent.sh > /tmp/copy.log 2>&1 &

echo "Waiting 10 seconds..."
sleep 10

echo "Status check..."
docker exec container-name ps aux | grep python3
ps aux | grep copy_agent | grep -v grep
wc -l /path/to/processed_videos.txt
ls /path/to/staging/*.MP4 2>/dev/null | wc -l

echo "Monitor logs with:"
echo "  tail -f /path/to/outputs/worker_1_log.txt"
echo "  tail -f /tmp/copy.log"
```

---

## Performance Tuning Reference

| Issue | Current | Optimized | Impact |
|-------|---------|-----------|--------|
| Workers idle > 30% time | BATCH_SIZE=10 | BATCH_SIZE=50 | 5x faster |
| Workers idle > 50% time | CHECK_INTERVAL=30 | CHECK_INTERVAL=5 | 10x faster |
| Staging always empty | Copy on empty | Copy at <20 videos | 2x faster |
| Too many workers | 6 workers | 3 workers | Better stability |
| Sampling every frame | fps samples | fps/2 samples | 2x faster |

---

**End of Troubleshooting Guide**

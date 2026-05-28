# PeopleNet Quick Reference

## One-Command Operation

```bash
cd /home/yousuf/PROJECTS/PeopleNet
./Scripts/master_pipeline.sh --start-date 2025-11-14 --auto-backup
```

**That's it!** Walk away and return to clips in Google Drive.

---

## Common Commands

### Check Progress
```bash
# Park_F progress
./Scripts/monitor_progress.sh Park_F_Batch1

# Park_R progress
./Scripts/monitor_progress.sh Park_R_Batch1

# Live Docker logs
docker logs -f peoplenet-park_f_batch1
```

### Analyze Clip Quality
```bash
# Test if clip actually contains people
docker exec peoplenet-park_f_batch1 python3 /workspace/Scripts/analyze_clip.py \
  /workspace/Outputs/Park_F_Batch1/clip.mp4
```

### Manual Backup
```bash
./Scripts/backup_to_gdrive.sh
```

### Emergency Stop
```bash
# Stop all processing
docker stop $(docker ps -q --filter "name=peoplenet")
pkill -f "controlled_feed\|auto_fix_ownership\|auto_next_batch"
```

---

## Critical Parameters

| Setting | Value | Why |
|---------|-------|-----|
| confidence_threshold | 0.8 | 0.6 = false positives, 0.8 = real people |
| buffer_seconds | 1 | 4s = clips too long, 1s = dense clips |
| gpu_workers | 3 | Optimal for RTX 4080 SUPER |
| staging_max | 20 | Prevents disk overflow |
| log_max_size | 50m | Prevents Docker log bloat |

---

## Troubleshooting

**Problem:** No clips extracted
```bash
# Check if videos contain people
docker exec peoplenet-* python3 /workspace/Scripts/analyze_clip.py /path/to/video.MP4
```

**Problem:** Can't open clips
```bash
# Fix ownership
sudo chown -R yousuf:yousuf Outputs/*/
```

**Problem:** Disk full
```bash
# Check what's using space
du -sh Outputs/*/ Staging/*/
docker system df

# Clean Docker
docker system prune -a
```

**Problem:** Processing stalled
```bash
# Check workers
docker exec peoplenet-* ps aux | grep python

# Check GPU
nvidia-smi

# Restart workers
docker restart peoplenet-*
```

---

## Output Locations

**Local:**
- Park_F: `/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_F_Batch1/`
- Park_R: `/home/yousuf/PROJECTS/PeopleNet/Outputs/Park_R_Batch1/`

**Google Drive (after backup):**
- Park_F: `~/GoogleDrive/PROJECTS/PeopleNet/Park_F_Batch1_YYYYMMDD/`
- Park_R: `~/GoogleDrive/PROJECTS/PeopleNet/Park_R_Batch1_YYYYMMDD/`

---

## Expected Performance

| Metric | Value |
|--------|-------|
| Processing speed | ~13 videos/min (3 workers) |
| Detection rate | 40-50% (varies by camera) |
| Clip size | 6-15MB each |
| Duration | ~2 hours for 1,400 videos |
| Data reduction | 98.5% (240GB → 3.4GB) |

---

## Next Time Setup

1. Update start date in command:
   ```bash
   ./Scripts/master_pipeline.sh --start-date 2025-11-15 --auto-backup
   ```

2. Walk away

3. Return to clips in Google Drive

**Zero intervention required!**

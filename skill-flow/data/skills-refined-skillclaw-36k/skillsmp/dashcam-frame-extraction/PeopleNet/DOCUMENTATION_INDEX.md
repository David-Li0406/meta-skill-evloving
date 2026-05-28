# PeopleNet Documentation Index

## Start Here

### For Next Time (Minimal Intervention)
👉 **[README.md](README.md)** - Quick start with one command

### For First-Time Setup
👉 **[AUTONOMOUS_SETUP.md](AUTONOMOUS_SETUP.md)** - Complete setup guide

### For Daily Use
👉 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command cheat sheet

---

## Documentation Overview

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **README.md** | Project overview, quick start | First time, getting oriented |
| **AUTONOMOUS_SETUP.md** | Complete setup, architecture, troubleshooting | Setting up, understanding system, debugging |
| **QUICK_REFERENCE.md** | Common commands, parameters | Daily operations, quick lookup |
| **config.yaml** | Configuration settings | Customizing behavior |

---

## Key Files

### Core Components
- `worker.py` - GPU processing worker (DON'T DELETE)
- `model/resnet34_peoplenet_int8.onnx` - AI model (DON'T DELETE)

### Main Scripts
- `Scripts/master_pipeline.sh` - **ONE COMMAND TO RUN EVERYTHING**
- `Scripts/monitor_progress.sh` - Check progress
- `Scripts/analyze_clip.py` - Verify clip quality
- `Scripts/backup_to_gdrive.sh` - Manual backup

### Outputs
- `Outputs/Park_F_Batch1/` - Front camera clips
- `Outputs/Park_R_Batch1/` - Rear camera clips

---

## One-Command Usage

```bash
cd /home/yousuf/PROJECTS/PeopleNet
./Scripts/master_pipeline.sh --start-date 2025-11-14 --auto-backup
```

That's it. Walk away and return to clips in Google Drive.

---

## What's Documented

### In AUTONOMOUS_SETUP.md (25 pages):
✅ Complete pipeline architecture
✅ Why each component is needed  
✅ Critical configuration parameters
✅ All gotchas and solutions
✅ Monitoring and debugging
✅ Performance metrics
✅ Next-time zero-intervention workflow
✅ Why ChatGPT failed (lessons learned)
✅ Troubleshooting decision tree

### In master_pipeline.sh:
✅ Single script that does everything
✅ Date-based video filtering
✅ Auto-triggers Park_R after Park_F
✅ Controlled feed (space management)
✅ Docker log rotation
✅ Auto-ownership fixing
✅ Progress monitoring
✅ Automatic backup
✅ Report generation
✅ Error handling

### In config.yaml:
✅ All configurable parameters
✅ Comments explaining each setting
✅ Safe defaults
✅ Why each value was chosen

---

## Critical Success Factors

These settings made it work (don't change without testing):

```yaml
confidence_threshold: 0.8  # Not 0.6 (false positives)
buffer_seconds: 1          # Not 4 (empty clips)  
gpu_workers: 3             # Optimal for RTX 4080
staging_max: 20            # Prevents overflow
log_rotation: enabled      # Prevents 100GB bloat
```

---

## Last Run Results (Proof of Success)

**Date:** November 15, 2025  
**Videos:** 1,397 (698 Park_F + 699 Park_R)  
**Clips:** 662 (269 Park_F + 393 Park_R)  
**Output:** 3.4GB (2.5GB + 903MB)  
**Duration:** 102 minutes  
**Detection:** 47.4% average  
**Data Reduction:** 98.6% (240GB → 3.4GB)

**Status:** ✅ Fully autonomous - zero intervention

---

## Next Time Checklist

- [ ] Mount external drive
- [ ] Mount Google Drive  
- [ ] Check disk space (>10GB free)
- [ ] Update start date in command
- [ ] Run: `./Scripts/master_pipeline.sh --start-date YYYY-MM-DD --auto-backup`
- [ ] Walk away

**Expected completion:** ~2 hours for 1,400 videos

**Result:** Clips in Google Drive, ready to review

---

Generated: November 16, 2025

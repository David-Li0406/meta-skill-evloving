# PeopleNet Dashcam Processing Pipeline

## Overview

This pipeline processes dashcam MP4 videos to extract clips containing people using NVIDIA's PeopleNet AI model.

**Pipeline Flow:**
```
Raw MP4 Videos (180MB each)
    ↓
SSIM Motion Filter (removes static/parked videos)
    ↓
Filtered Video List (70-75% pass rate)
    ↓
GPU-Accelerated People Detection (NVIDIA PeopleNet)
    ↓
Detection Clips (10-40MB each, only segments with people)
```

## Documentation Files

This directory contains comprehensive documentation for replicating the entire pipeline:

### 1. **PIPELINE_DOCUMENTATION.md** (Main Documentation)
Complete step-by-step guide covering:
- Prerequisites and setup
- Phase 1: SSIM video filtering
- Phase 2: GPU infrastructure setup
- Phase 3: People detection processing
- Phase 4: Batch processing system
- Critical issues and solutions
- Configuration reference
- Performance optimization

**Use this for**: Understanding the complete system and implementing from scratch.

### 2. **COMMAND_REFERENCE.md** (Quick Commands)
Copy-paste ready commands for:
- Setup and installation
- Starting the pipeline
- Monitoring progress
- Emergency stop/restart
- Data analysis
- Performance optimization

**Use this for**: Quick execution and operational tasks.

### 3. **TROUBLESHOOTING_GUIDE.md** (Issue Resolution)
Diagnostic procedures and solutions for:
- No clips being created
- Workers idle/slow processing
- Disk space issues
- Permission errors
- Corrupt videos
- GPU not being used

**Use this for**: Debugging problems and fixing issues.

## Quick Start

```bash
# 1. Read main documentation
less PIPELINE_DOCUMENTATION.md

# 2. Verify prerequisites
docker --version
nvidia-smi
python3 --version

# 3. Follow setup in PIPELINE_DOCUMENTATION.md Phase 1-2

# 4. Use COMMAND_REFERENCE.md for execution commands

# 5. Monitor progress
tail -f Outputs/GPU_Pipeline_Park_R_Batch1/worker_1_log.txt

# 6. If issues occur, consult TROUBLESHOOTING_GUIDE.md
```

## Key Features

✅ **Two-stage filtering**: SSIM motion filter + PeopleNet detection
✅ **GPU acceleration**: NVIDIA TensorRT container with CUDA
✅ **Parallel processing**: 3 workers processing simultaneously
✅ **Batch management**: Automatic disk space and staging queue management
✅ **Resilient**: File-based locking prevents duplicate processing
✅ **Autonomous**: Runs continuously until all videos processed

## Performance Metrics

- **Processing Speed**: 70-75 videos/minute (3 GPU workers)
- **Detection Rate**: ~40-47% (Park_R and Park_F)
- **GPU Utilization**: 5-10% (inference is very fast)
- **Disk Requirements**: 20GB buffer + ~15-20GB per 1000 videos processed
- **Daily Capacity**: 100,000+ videos

## Project Statistics

### Park_R (Rear Camera)
- Source videos: ~4,500
- After SSIM filter: 3,130 (70% pass rate)
- Processed: 3,167 (includes some outside filter list)
- Detection clips created: ~1,470
- Detection rate: ~46%
- Total output size: ~60GB

### Park_F (Front Camera)
- Source videos: ~2,475
- After SSIM filter: 1,792 (72% pass rate)
- Processed: 1,100+ (in progress)
- Detection clips created: 380+
- Detection rate: ~41%
- Total output size: ~15GB

## Directory Structure

```
/home/yousuf/PROJECTS/PeopleNet/
├── README.md                               # This file
├── PIPELINE_DOCUMENTATION.md               # Complete technical documentation
├── COMMAND_REFERENCE.md                    # Quick command reference
├── TROUBLESHOOTING_GUIDE.md               # Issue resolution guide
├── model/
│   └── resnet34_peoplenet_int8.onnx       # PeopleNet AI model
├── Staging/
│   ├── Park_R_Batch1/                     # Temporary queue for Park_R
│   └── Park_F_Batch1/                     # Temporary queue for Park_F
├── Outputs/
│   ├── GPU_Pipeline_Park_R_Batch1/
│   │   ├── *.mp4                          # Detection clips
│   │   ├── processed_videos.txt           # Progress tracking
│   │   ├── worker_*_log.txt               # Worker logs
│   │   └── locks/                         # Processing locks
│   └── GPU_Pipeline_Park_F_Batch1/
│       └── (same structure)
├── park_r_process_list.txt                # SSIM filtered Park_R videos
├── park_f_process_list.txt                # SSIM filtered Park_F videos
└── Corrupted_Videos/                      # Quarantined corrupt files
```

## Technology Stack

- **OS**: Ubuntu 22.04 LTS
- **Container**: NVIDIA TensorRT 24.08 (Docker)
- **GPU**: NVIDIA RTX 4080 SUPER with CUDA 12.x
- **AI Model**: NVIDIA PeopleNet (ResNet-34, INT8)
- **Python**: 3.11
- **Key Libraries**:
  - onnxruntime-gpu (inference)
  - opencv-python (video processing)
  - scikit-image (SSIM filtering)
  - numpy (data processing)
  - ffmpeg (clip extraction)

## Critical Success Factors

1. **Install ffmpeg in container BEFORE starting workers**
   - Without this, clips won't be created (silent failure)

2. **Optimize batch size and check interval**
   - BATCH_SIZE=50, CHECK_INTERVAL=5 for optimal speed

3. **Monitor disk space**
   - Maintain 20GB buffer minimum

4. **Handle corrupt videos**
   - Quarantine rather than skip to prevent re-attempts

5. **Verify GPU is being used**
   - Check logs show "CUDAExecutionProvider"

## Common Pitfalls to Avoid

❌ Not installing ffmpeg → Silent failure, no clips created
❌ Small batch size (10) → Workers idle 50% of time, 10x slower
❌ Wrong file paths → Container can't access files
❌ Not deleting processed videos → Disk fills up
❌ Starting without checking prerequisites → Wasted time debugging

✅ Follow documentation exactly
✅ Use command reference for copy-paste commands
✅ Check troubleshooting guide if issues occur

## Support and Troubleshooting

1. **For setup issues**: See PIPELINE_DOCUMENTATION.md sections on Prerequisites and Setup
2. **For execution issues**: See COMMAND_REFERENCE.md for correct commands
3. **For runtime issues**: See TROUBLESHOOTING_GUIDE.md for diagnostics
4. **For performance issues**: See PIPELINE_DOCUMENTATION.md Performance Optimization section

## Replication Instructions for Another AI

**To replicate this pipeline completely**:

1. Read all documentation files in order:
   - README.md (this file) - Overview
   - PIPELINE_DOCUMENTATION.md - Complete technical guide
   - COMMAND_REFERENCE.md - Execution commands
   - TROUBLESHOOTING_GUIDE.md - Issue resolution

2. Follow PIPELINE_DOCUMENTATION.md exactly, section by section

3. Use COMMAND_REFERENCE.md for copy-paste commands (don't modify)

4. If any issues occur, immediately consult TROUBLESHOOTING_GUIDE.md

5. Key verification points:
   - ffmpeg installed in container
   - GPU being used (check logs)
   - Clips being created (not just "No people")
   - Workers staying busy (not idle)
   - Disk space maintained (>20GB free)

## Results Verification

After processing completes, verify:

```bash
# Total videos processed
wc -l Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt

# Total clips created
ls Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 | wc -l

# Detection rate
echo "Detection rate: $(ls Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 | wc -l) / $(wc -l < Outputs/GPU_Pipeline_Park_R_Batch1/processed_videos.txt) * 100" | bc -l

# Total output size
du -sh Outputs/GPU_Pipeline_Park_R_Batch1/

# Example clip
ls Outputs/GPU_Pipeline_Park_R_Batch1/*.mp4 | head -1
```

Expected results:
- Processing complete: All videos in filter list processed
- Clips created: 40-50% of processed videos should have clips
- No errors in logs: Check worker logs for errors
- Disk space recovered: Staging directory empty or near-empty

## License and Credits

- **PeopleNet Model**: NVIDIA (NGC Catalog)
- **TensorRT Container**: NVIDIA
- **Pipeline Implementation**: Custom development for dashcam processing

## Version History

- **v2.0** (2025-11-10): Optimized version with batch processing and auto-deletion
- **v1.0** (Initial): Basic sequential processing

---

**For detailed implementation, always refer to PIPELINE_DOCUMENTATION.md**

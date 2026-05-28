# Frame Extraction Pipeline - Movie_F

## Quick Access

**🤖 FOR AGENTS**: Start with [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) - Complete agent guide

**🚀 TO RUN**: Execute [`run_extraction.sh`](run_extraction.sh) - Main extraction script

**📖 Documentation**:
- [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) - Agent-specific instructions
- [`SKILL_README.md`](SKILL_README.md) - Skill overview
- [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) - One-page command reference
- [`README.md`](README.md) - Project overview
- [`DOCUMENTATION.md`](DOCUMENTATION.md) - Complete technical guide
- [`CRITICAL_FIXES_CHECKLIST.md`](CRITICAL_FIXES_CHECKLIST.md) - Pre-flight verification

**⚙️ Core Scripts**:
- [`run_extraction.sh`](run_extraction.sh) - Main orchestration script
- [`extract_frames_worker.py`](extract_frames_worker.py) - GPU worker process
- [`coordinator.sh`](coordinator.sh) - Parallel batch coordinator
- [`monitor.sh`](monitor.sh) - Progress monitoring
- [`show_results.sh`](show_results.sh) - Display extraction results

**📋 Configuration**:
- [`config.json`](config.json) - Settings and paths
- [`requirements.txt`](requirements.txt) - Dependencies

## What This Is

Automated GPU-accelerated frame extraction pipeline specifically for Movie_F dashcam videos.

**Key Features**:
- One-command execution
- Automatic gap analysis (identifies new videos)
- HEVC CUDA compatibility fixes
- Strict error handling (exits on any failure)
- Real-time progress monitoring
- Movie_F category ONLY

## Quick Start

```bash
# Place videos in /mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/
# Then run:
cd /home/yousuf/GoogleDrive/PROJECTS/skills/Dashcam
./run_extraction.sh
```

## Configuration

- **Category**: Movie_F only
- **Workers**: 4 parallel GPU workers
- **Batch size**: 50 videos per batch
- **Timeout**: 30 seconds per frame
- **Error handling**: Strict - exits on any failure

## Critical Settings

1. **HEVC Fix**: Uses `-hwaccel cuda` ONLY (no output format)
2. **Error Mode**: `set -euo pipefail` (strict)
3. **Worker Exit**: Returns error code if any video fails
4. **Filename Patterns**: Handles A suffix variations

## Performance

- **Speed**: 15-20 videos/minute
- **GPU Utilization**: 60-90%
- **Frames per video**: 3 (BEGIN, MIDDLE, END)
- **Error handling**: All videos must succeed

## Files

```
Dashcam/
├── INDEX.md                          ← This file - navigation guide
├── SKILL_README.md                   ← Skill overview
│
├── AGENT_INSTRUCTIONS.md             ← 🤖 Agent guide (START HERE for agents)
├── README.md                         ← Project overview
├── QUICK_REFERENCE.md                ← Command cheat sheet
├── DOCUMENTATION.md                  ← Complete technical docs
├── CRITICAL_FIXES_CHECKLIST.md       ← Pre-flight verification
│
├── run_extraction.sh                 ← 🚀 Main script (RUN THIS)
├── extract_frames_worker.py          ← GPU worker process
├── coordinator.sh                    ← Parallel batch coordinator
├── monitor.sh                        ← Progress monitoring
├── show_results.sh                   ← Results display
│
├── config.json                       ← Settings and paths
├── requirements.txt                  ← Dependencies
│
└── auto_extract_movie_f.sh           ← Legacy (use run_extraction.sh instead)
```

---

**Version**: 1.0
**Category**: Movie_F ONLY
**Last Updated**: 2025-01-14

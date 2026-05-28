# Frame Extraction - Quick Reference Card

**Movie_F ONLY** - This script is specifically for Movie_F category

## One-Command Execution

```bash
cd /home/yousuf/PROJECTS/PeopleNet/FrameExtraction
./auto_extract_movie_f.sh
```

## Input/Output

| What | Where |
|------|-------|
| **Input videos** | `/mnt/windows/Users/yousu/Desktop/CARDV/Movie_F/` |
| **Output frames** | `/home/yousuf/GoogleDrive/.../Movie_F&R_MotionSamples/` |
| **Logs** | `./logs/` |
| **Progress** | Prints every 30 seconds |

## Expected Results

| Metric | Value |
|--------|-------|
| Success rate | 70-85% |
| Speed | 15-20 vids/min |
| Frames/video | 3 (BEGIN/MIDDLE/END) |
| Timeout rate | 20-30% (normal) |

## Frame Naming

```
{videoname}_BEGIN_{timestamp}ms.jpg
{videoname}_MIDDLE_{timestamp}ms.jpg
{videoname}_END_{timestamp}ms.jpg
```

Example: `20250916042109_062060A_BEGIN_001000ms.jpg`

## Critical Fixes (Must Have)

1. **HEVC Fix**: Use `-hwaccel cuda` ONLY (no output format)
2. **Error Handling**: Strict mode - exits on any failure
3. **Timeout**: 30 seconds per frame
4. **Filenames**: Handle A suffix variations
5. **Category**: Movie_F only

## Monitoring

```bash
# Watch batches complete
watch -n 10 'ls completed/ | wc -l'

# Check workers
ps aux | grep extract_frames_gpu | grep -v grep

# GPU usage
nvidia-smi

# Tail logs
tail -f logs/coordinator.log
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 0% success | Check HEVC fix applied |
| Process exits on failure | This is intentional - all must succeed |
| Hangs forever | Check 30s timeout set |
| Videos not found | Check filename pattern matching |

## Stop Everything

```bash
pkill -f extract_frames_gpu
pkill -f coordinator_auto
pkill -f monitor_extraction
```

## Documentation

- **Full docs**: `DOCUMENTATION.md`
- **Critical fixes**: `CRITICAL_FIXES_CHECKLIST.md`
- **This card**: `QUICK_REFERENCE.md`

## Workflow Summary

1. User places Movie_F videos in Desktop CARDV/Movie_F directory
2. Run `./auto_extract_movie_f.sh`
3. Script auto-detects new videos
4. Creates batches, launches workers
5. Monitors progress every 30s
6. All videos must succeed or pipeline stops
7. Frames appear in Google Drive

**Total manual steps: 1 command**

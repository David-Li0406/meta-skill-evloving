# Human Extractor Skill Manifest

## Skill Metadata

**Skill Name:** human-extractor
**Version:** 1.0
**Created:** 2025-10-26
**Last Updated:** 2025-10-26
**Author:** System
**Status:** Production Ready

## Purpose

Extract human detections from dashcam MP4 videos using GPU-accelerated computer vision pipeline (YOLOv8 + ByteTrack + CLIP).

## Skill Files

### Core Documentation
| File | Purpose | Size | Status |
|------|---------|------|--------|
| `SKILL.md` | Complete skill specification | 15.9 KB | ✅ Complete |
| `README.md` | Quick start guide | 2.5 KB | ✅ Complete |
| `SKILL_MANIFEST.md` | This file - inventory & metadata | - | ✅ Complete |

### Scripts (`scripts/`)
| File | Purpose | Invocation |
|------|---------|------------|
| `run_extraction.py` | Main entry point wrapper | Called by Claude or user |
| `validate_paths.py` | Input path validation | Pre-run check |
| `merge_index_shards.py` | Merge INDEX shards to final | Post-run cleanup |

### Assets (`assets/`)
| File | Purpose | Format |
|------|---------|--------|
| `config_template.json` | Default configuration | JSON |
| `example_request.json` | Sample skill invocation | JSON |
| `camera_mapping.json` | File ID → Camera mapping | JSON |

### References (`references/`)
| File | Purpose | Source |
|------|---------|--------|
| `TECHNICAL_OVERVIEW_HEAD_COVERING_DETECTION.md` | CLIP pipeline details | Original project docs |
| `DASHCAM_PROCESSING_WORKFLOW.md` | Complete workflow guide | Original project docs |
| `EXTRACTION_KEY_FILES.md` | Script descriptions | Original project docs |

## External Dependencies

### Python Packages
```
torch>=2.0
ultralytics>=8.0
transformers>=4.30
opencv-python>=4.8
pandas>=2.0
pillow>=10.0
```

### External Projects
| Dependency | Location | Purpose |
|------------|----------|---------|
| Human_Detection | `G:\My Drive\PROJECTS\APPS\Human_Detection\` | Core pipeline implementation |
| YOLOv8 Model | `models/yolov8s.pt` | Person detection |
| CLIP Model | HuggingFace cache | Head covering classification |

## Data Flow

```
INPUT:
G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\{Camera}\{Date}\*.MP4

PROCESSING:
G:\My Drive\PROJECTS\APPS\Human_Detection\src\cli\*.py

OUTPUT:
G:\My Drive\PROJECTS\APPS\Human_Detection\parsed\ALL_CROPS\
  ├── *.webp (crop images)
  ├── INDEX.csv (master index)
  └── run_*.log (execution logs)
```

## Configuration Parameters

### Required
- `roots`: List of source directories

### Core Detection
- `confidence`: YOLOv8 threshold (default: 0.35)
- `iou`: NMS IoU threshold (default: 0.50)
- `yolo_batch`: Batch size (default: 64)

### CLIP Filtering
- `clip_filter.enabled`: Enable/disable (default: false)
- `clip_filter.threshold`: Confidence cutoff (default: 0.80)
- `clip_filter.batch`: Batch size (default: 384)

### Hardware
- `nvdec`: Use hardware decoding (default: true)
- `gpu_id`: CUDA device (default: 0)

### Output
- `single_output_dir`: Output path (default: "parsed\\ALL_CROPS")
- `save_full_frame`: Save annotated frames (default: false)
- `draw_boxes`: Annotate detections (default: true)

## Performance Benchmarks

### RTX 4080 16GB
| Metric | Value |
|--------|-------|
| Throughput | 3-4 videos/min |
| GPU Utilization | 80-90% |
| VRAM Usage | 6-10 GB |
| Processing Latency | <30s per video |

### Configuration Impact
| Change | Effect |
|--------|--------|
| NVDEC ON | 5-10x faster decode |
| YOLO batch 32→64 | +40% throughput |
| CLIP batch 256→384 | +25% throughput |
| Full-frame saves | -15% throughput |

## Error Handling

### Common Issues
1. **CUDA OOM:** Reduce batch sizes
2. **NVDEC unavailable:** Falls back to CPU decode
3. **Low GPU util:** Increase batches or workers
4. **Slow I/O:** Use SSD, disable full-frames

### Recovery Mechanisms
- Idempotent: Skip existing crops
- Shard-based: Resume from last complete shard
- Graceful degradation: Disable CLIP if unavailable

## Testing Checklist

- [ ] GPU available (`torch.cuda.is_available()`)
- [ ] Models exist (`yolov8s.pt`)
- [ ] Output directory writable
- [ ] Input paths exist
- [ ] NVDEC functional (optional)

## Output Validation

- [ ] `INDEX.csv` exists and non-empty
- [ ] Crop files match INDEX rows
- [ ] SHA1 hashes valid
- [ ] GPU utilization >70%
- [ ] No errors in run log

## Version History

**v1.0** (2025-10-26)
- Initial release
- YOLOv8s + ByteTrack + CLIP
- NVDEC support
- Unified output directory
- Global INDEX.csv

## Related Skills

- **gps-timeline-analyzer** - Analyze GPS data from same videos
- **audio-transcription** - Extract audio from same videos

## Support & Troubleshooting

See `SKILL.md` section "Troubleshooting" for detailed guidance on:
- CUDA errors
- Performance tuning
- Hardware compatibility
- Path resolution

## License & Attribution

Pipeline implementation from: `G:\My Drive\PROJECTS\APPS\Human_Detection\`

Models:
- YOLOv8: Ultralytics (AGPL-3.0)
- CLIP: OpenAI (MIT)
- ByteTrack: arXiv:2110.06864

## Contact

For issues or questions about this skill, check:
1. `parsed/ALL_CROPS/run_*.log` for error details
2. GPU diagnostics: `nvidia-smi`
3. PyTorch check: `python -c "import torch; print(torch.cuda.is_available())"`

---

**Manifest Version:** 1.0
**Last Validated:** 2025-10-26

# GPS Extraction Skill Package

**One-shot optimized GPS coordinate extraction from dashcam video frames**

Battle-tested on 27,856 real dashcam crops | **88.0% success rate** achieved

## Quick Start

```bash
cd /home/yousuf/PROJECTS/gps_extraction_skill
./run.sh /path/to/crop/files
```

That's it! The script handles everything automatically.

## What This Does

Extracts GPS coordinates from dashcam frame crops using GPU-accelerated OCR:

**Input:** Directory of cropped dashcam frames (JPG images)
**Output:** Excel file with GPS coordinates (lat, lon, raw OCR text)
**Time:** 30-45 minutes for ~28,000 images
**Success Rate:** 85-90% typical

## Package Contents

```
gps_extraction_skill/
├── run.sh                          # Main entry point - run this
├── scripts/
│   ├── extract_gps_optimized.sh   # Phase 1: GPU extraction
│   ├── decimal_recovery.py        # Phase 2: Fix missing decimals
│   ├── analyze_results.py         # Results analysis
│   └── monitor_progress.sh        # Real-time monitoring
├── config/
│   └── extraction.conf            # Configuration parameters
├── docs/
│   ├── AGENT_SPEC.md             # Complete agent specification
│   ├── CRITICAL_LEARNINGS.md     # Battle-tested insights
│   └── TROUBLESHOOTING.md        # Common issues & solutions
├── examples/
│   └── sample_output.xlsx        # Example output format
└── README.md                      # This file
```

## Prerequisites

1. **NVIDIA GPU** with CUDA support
2. **Python 3.11** environment with:
   - PaddleOCR (`paddleocr>=2.7.0`)
   - pandas, openpyxl
   - CUDA libraries (cudnn, cublas)
3. **20GB+ free disk space**

## Usage

### Basic Usage (Recommended)

```bash
./run.sh /path/to/crop/directory
```

The script will:
- ✅ Validate system requirements
- ✅ Check GPU availability
- ✅ Process all crops with optimal parameters
- ✅ Generate results Excel file
- ✅ Report success statistics

### Advanced Usage

**Custom Python environment:**
```bash
./run.sh /path/to/crops --python /path/to/python3
```

**Adjust worker count:**
```bash
./run.sh /path/to/crops --workers 2  # Use 2 GPU workers instead of 4
```

**Custom output location:**
```bash
./run.sh /path/to/crops --output /path/to/output.xlsx
```

**Run decimal recovery only:**
```bash
python scripts/decimal_recovery.py --input results.xlsx --output recovered.xlsx
```

## Configuration

Edit `config/extraction.conf` to customize:

```bash
CROP_WIDTH_PCT=0.70      # Crop width percentage (0.70 = 70%)
CROP_HEIGHT_PCT=0.22     # Crop height percentage
WORKERS=4                # Number of GPU workers
OCR_BACKEND=paddle       # OCR backend (paddle recommended)
```

**⚠️ Warning:** Do not set CROP_WIDTH_PCT below 0.70 - this will cause failures!

## Output Format

Excel file with columns:

| Column | Description | Example |
|--------|-------------|---------|
| frame_path | Path to crop file | `crops/video_F001_001000ms.jpg` |
| frame_filename | Filename only | `video_F001_001000ms.jpg` |
| latitude | Extracted latitude | `43.8878` |
| longitude | Extracted longitude | `-79.0829` |
| coordinates | Combined | `43.8878, -79.0829` |
| gps_raw | Raw OCR text | `N:43.8878 W79.0829` |
| gps_parsed | Parsed GPS | `N:43.8878 W:79.0829` |

## Monitoring Progress

In another terminal:

```bash
# Watch GPU utilization
watch -n 2 nvidia-smi

# Monitor progress
./scripts/monitor_progress.sh

# Check log file
tail -f logs/extraction.log
```

## Expected Performance

| Metric | Typical Value |
|--------|---------------|
| Processing speed | 6-8 images/second |
| Success rate | 85-90% |
| GPU utilization | 20-30% |
| Time for 28k images | 40-60 minutes |

## Troubleshooting

**Low success rate (<70%)?**
- Check crop width is set to 0.70 minimum
- Verify GPU is being used (run `nvidia-smi`)

**Out of memory errors?**
- Reduce workers: `./run.sh crops --workers 2`

**Very slow processing?**
- Check CUDA libraries are accessible
- Verify GPU mode is enabled

See `docs/TROUBLESHOOTING.md` for detailed solutions.

## Critical Success Factors

1. **Crop Width = 70% minimum** - This is non-negotiable
2. **GPU Acceleration** - 10x faster than CPU
3. **4 Parallel Workers** - Maximizes throughput
4. **Pre-flight Checks** - Catch issues early

## Battle-Tested Results

- **Test dataset:** 27,856 dashcam frame crops
- **Success rate:** 88.0% (24,501 coordinates)
- **Processing time:** 40 minutes
- **GPU:** NVIDIA RTX 3090 (similar results on RTX 2080+)

## Support

1. Check `docs/TROUBLESHOOTING.md`
2. Review `docs/CRITICAL_LEARNINGS.md`
3. Check log file: `logs/extraction.log`

## License

MIT License - Free to use and modify

## Version

**Version:** 1.0.0
**Last Updated:** 2025-11-16
**Status:** Production Ready ✅

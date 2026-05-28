# GPS Extraction Agent - One-Shot Optimized

You are a GPS extraction specialist agent designed to extract GPS coordinates from dashcam video frame crops with maximum efficiency and success rate.

## Mission
Extract GPS coordinates from 27,856 dashcam frame crop images using OCR, achieving 85%+ success rate in a single optimized run with minimal debugging.

## Critical Success Parameters (DO NOT DEVIATE)

### 1. Crop Dimensions - MOST CRITICAL
- **Width: 70% minimum** (55% will fail completely - DO NOT USE)
- **Height: 22% minimum** (10% will fail completely - DO NOT USE)
- These parameters are battle-tested and non-negotiable
- Reason: GPS overlay text needs wider horizontal space to be readable by OCR

### 2. OCR Backend
- **MUST use PaddleOCR with GPU acceleration**
- CPU mode is too slow (10x slower)
- EasyOCR performs worse on dashcam overlays
- Set CUDA library paths before starting:
  ```bash
  export CUDNN_LIB="<env_path>/site-packages/nvidia/cudnn/lib"
  export CUBLAS_LIB="<env_path>/site-packages/nvidia/cublas/lib"
  export LD_LIBRARY_PATH="${CUDNN_LIB}:${CUBLAS_LIB}:$LD_LIBRARY_PATH"
  ```

### 3. Parallel Processing
- **Use 4 workers minimum** (assuming sufficient GPU memory)
- Monitor GPU utilization (should stay 20-30% during processing)
- Set util-threshold: 90.0, mem-threshold: 85.0

### 4. GPS Parser
- **DO NOT create new parsers** - the existing `parse_gps_from_text()` in `src/extract_sample.py` is battle-tested
- It handles these formats successfully:
  - `N:43.8878 W:79.0829` (standard)
  - `N438878W790829` (missing decimals)
  - `N:43,8878` (comma decimals)
  - `N 43 34.1388 W 79 31.4082` (deg + decimal minutes)
- Wide crops solve most OCR issues - don't over-engineer the parser

## Optimal Execution Plan

### Phase 1: Initial Extraction (Target: 85%+ success)
```bash
#!/bin/bash
cd /home/yousuf/PROJECTS/ExtractedGPS

# Set CUDA paths
export CUDNN_LIB="/home/yousuf/PROJECTS/ExtractedGPS/.mambaforge/envs/paddle311/lib/python3.11/site-packages/nvidia/cudnn/lib"
export CUBLAS_LIB="/home/yousuf/PROJECTS/ExtractedGPS/.mambaforge/envs/paddle311/lib/python3.11/site-packages/nvidia/cublas/lib"
export LD_LIBRARY_PATH="${CUDNN_LIB}:${CUBLAS_LIB}:$LD_LIBRARY_PATH"

PYTHON_BIN="/home/yousuf/PROJECTS/ExtractedGPS/.mambaforge/envs/paddle311/bin/python3"

echo "Starting optimized GPS extraction..."
echo "Processing all 27,856 crops with GPU PaddleOCR..."

# Run on ALL crops at once with optimal parameters
$PYTHON_BIN src/run_multi.py \
  --python-bin "$PYTHON_BIN" \
  --workers 4 \
  --util-threshold 90.0 \
  --mem-threshold 85.0 \
  --source "staging/movief_all_crops_w055_h010" \
  --output-final "Outputs/FullExtraction/batch1_optimized.xlsx" \
  --missing-final "Outputs/FullExtraction/batch1_missing.csv" \
  --crop-width-pct 0.70 \
  --crop-height-pct 0.22 \
  --ocr-backend paddle \
  --aggregate-log "logs/batch1_optimized.log"

echo "Phase 1 complete!"
```

**Expected Results:**
- Success rate: 85-90% on first pass
- Processing time: ~30-45 minutes for 27,856 files
- GPU utilization: 20-30%

### Phase 2: Decimal-Fixing Recovery (Target: +2-3% recovery)

Only needed if Phase 1 has failures with missing decimals (OCR like `N438878W790829`)

```python
#!/usr/bin/env python3
"""Decimal-fixing recovery for missing decimal points in GPS coordinates"""
import pandas as pd
import re
from paddleocr import PaddleOCR

def fix_gps_decimals(text: str) -> str:
    """Fix missing decimals: N438746 → N:43.8746"""
    fixed = text.replace(',', '.')  # Handle comma decimals
    # N438746 → N:43.8746
    fixed = re.sub(r'([NnAa]):?(\d{2})(\d{4,5})([^0-9]|$)', r'N:\2.\3\4', fixed)
    # W790425 → W:79.0425
    fixed = re.sub(r'W:?(\d{2})(\d{4,5})([^0-9]|$)', r'W:\1.\2\3', fixed)
    return fixed

# Load failures from Phase 1
df = pd.read_excel('Outputs/FullExtraction/batch1_optimized.xlsx')
failures = df[df['latitude'].isna()].copy()

# Re-run OCR with decimal fixing
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True, show_log=False)
recovered = []

for idx, row in failures.iterrows():
    # Re-OCR the crop file
    result = ocr.ocr(row['frame_path'], cls=True)
    if result and result[0]:
        text = ' '.join([line[1][0] for line in result[0]])
        fixed_text = fix_gps_decimals(text)

        # Try parsing with fixed text
        from src.extract_sample import parse_gps_from_text
        lat, lon, raw, conf = parse_gps_from_text(fixed_text)

        if lat and lon:
            recovered.append({
                'frame_path': row['frame_path'],
                'latitude': lat,
                'longitude': lon,
                'gps_raw': text,
                'gps_parsed': fixed_text
            })

# Save recoveries
pd.DataFrame(recovered).to_excel('Outputs/FullExtraction/batch2_decimal_recovery.xlsx')
print(f"Recovered {len(recovered)} additional GPS coordinates")
```

### Phase 3: Final Statistics

```python
import pandas as pd

df1 = pd.read_excel('Outputs/FullExtraction/batch1_optimized.xlsx')
df2 = pd.read_excel('Outputs/FullExtraction/batch2_decimal_recovery.xlsx')

total_success = df1['latitude'].notna().sum() + len(df2)
total_crops = 27856

print(f"FINAL RESULTS:")
print(f"  Total GPS extracted: {total_success:,}")
print(f"  Success rate: {total_success/total_crops*100:.1f}%")
print(f"  Still missing: {27856 - total_success:,}")
```

## Pre-Flight Checklist

Before starting, verify:

1. **Disk Space:** Ensure 20GB+ free space
   ```bash
   df -h /home/yousuf  # Should show <80% usage
   ```

2. **GPU Available:**
   ```bash
   nvidia-smi  # Should show GPU with available memory
   ```

3. **CUDA Libraries Accessible:**
   ```bash
   ls $CUDNN_LIB/libcudnn.so*  # Should list files
   ls $CUBLAS_LIB/libcublas.so*  # Should list files
   ```

4. **Python Environment Active:**
   ```bash
   which python3  # Should point to paddle311 env
   python3 -c "import paddle; print(paddle.device.is_compiled_with_cuda())"  # Should be True
   ```

5. **Crop Files Exist:**
   ```bash
   ls staging/movief_all_crops_w055_h010/*.jpg | wc -l  # Should be 27856
   ```

6. **Docker Logs Won't Fill Disk:**
   ```bash
   docker inspect <container> | grep -A 10 log-driver
   # Should show max-size: "50m" or similar
   ```

## Common Failure Modes & Solutions

### Problem: 0% success rate
**Cause:** Crops too narrow (width < 60%)
**Solution:** MUST use 70% width minimum - restart with correct parameters

### Problem: Very low GPU utilization (<5%)
**Cause:** PaddleOCR defaulting to CPU mode
**Solution:** Check CUDA paths are set, verify GPU available

### Problem: "Out of memory" errors
**Cause:** Too many workers for available GPU memory
**Solution:** Reduce --workers from 4 to 2

### Problem: Disk space fills up during run
**Cause:** Docker logs growing unchecked
**Solution:** Configure log rotation before starting:
```bash
sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

### Problem: Low success rate (< 70%) with correct crop params
**Cause:** OCR quality issues with specific dashcam model
**Solution:** Try crop-height-pct 0.28 instead of 0.22

## Performance Benchmarks

Expected performance on typical hardware:
- **Processing speed:** ~6-8 images/second with 4 GPU workers
- **Time for 27,856 images:** 30-45 minutes
- **GPU memory usage:** 700-900 MB
- **GPU utilization:** 20-30% (PaddleOCR is not heavily GPU-bound)
- **Success rate:** 85-90% on first pass

## Key Insights from Battle-Testing

1. **Crop width is CRITICAL** - This is the #1 factor for success. 70% minimum.

2. **Don't over-engineer the parser** - The existing regex patterns handle 95%+ of formats. Wide crops solve OCR issues better than fancy parsers.

3. **GPU is essential for speed** - CPU mode takes 10x longer with no quality benefit.

4. **Process everything at once** - Don't split into batches unless forced by resource constraints.

5. **Failures are mostly genuine** - The remaining 10-15% failures are typically:
   - Corrupted video frames with no visible GPS overlay
   - Extreme motion blur during high-speed driving
   - GPS overlay turned off in dashcam settings
   - First few seconds of video before GPS lock

6. **Don't waste time on edge cases** - Achieving >85% is excellent for this use case. The remaining failures require manual review.

## Success Criteria

✅ **Minimum Acceptable:** 80% success rate (22,285 GPS coordinates)
✅ **Target:** 85% success rate (23,678 GPS coordinates)
✅ **Excellent:** 88%+ success rate (24,500+ GPS coordinates)

## Execution Time Estimate

- Phase 1 (initial extraction): 30-45 minutes
- Phase 2 (decimal recovery, if needed): 10-15 minutes
- **Total: 40-60 minutes to complete**

## Final Notes

- This process has been battle-tested on 27,856 real dashcam frame crops
- The optimal parameters are derived from multiple failed iterations
- Following this guide exactly should achieve 85-90% success rate on first attempt
- Any deviation from the critical parameters (especially crop width) will significantly reduce success rate
- The remaining 10-15% failures are expected and not worth extensive debugging

---

**Last Updated:** 2025-11-16
**Success Rate Achieved:** 88.0% (24,501/27,856)
**Agent Status:** Production-Ready

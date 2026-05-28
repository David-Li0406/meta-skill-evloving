# GPS Extraction - Troubleshooting Guide

Quick reference for common issues and solutions.

## Quick Diagnostics

Run these commands to diagnose issues:

```bash
# Check GPU
nvidia-smi

# Check disk space
df -h

# Check Python environment
python3 -c "import paddleocr; print('PaddleOCR OK')"

# Check crop files
find /path/to/crops -name "*.jpg" | wc -l

# Check logs
tail -50 logs/extraction.log
```

## Common Issues

### ❌ Low Success Rate (<70%)

**Symptoms:**
- Output shows success rate below 70%
- Most extractions failing

**Diagnosis:**
```bash
# Check what crop parameters were used
grep "crop-width-pct\|crop-height-pct" logs/extraction.log
```

**Solution:**
1. Verify crop width is set to 0.70 minimum in `config/extraction.conf`
2. Check that GPU is being used (run `nvidia-smi` during extraction)
3. Review sample failed crops visually to ensure GPS overlay is visible

**Prevention:**
- Never set CROP_WIDTH_PCT below 0.70
- Always run pre-flight checks before starting

---

### ❌ Out of Memory (OOM) Errors

**Symptoms:**
- "CUDA out of memory" errors
- Process crashes during execution
- GPU shows 100% memory usage

**Diagnosis:**
```bash
nvidia-smi  # Check GPU memory usage
```

**Solution:**
1. Reduce worker count in `config/extraction.conf`:
   ```bash
   WORKERS=2  # Instead of 4
   ```

2. Or run with fewer workers:
   ```bash
   ./run.sh /path/to/crops --workers 2
   ```

**Prevention:**
- Check available GPU memory before starting
- Use 2 workers for GPUs with <6GB memory

---

### ❌ Very Slow Processing (<2 images/second)

**Symptoms:**
- Processing taking much longer than expected
- GPU utilization very low (<5%)

**Diagnosis:**
```bash
# During extraction, run:
nvidia-smi
# Should show python process using GPU

# Check CUDA paths
echo $LD_LIBRARY_PATH
```

**Solution:**
1. Verify CUDA libraries are accessible:
   ```bash
   ls $CUDNN_LIB/libcudnn.so*
   ls $CUBLAS_LIB/libcublas.so*
   ```

2. Check PaddleOCR is using GPU:
   ```python
   import paddle
   print(paddle.device.is_compiled_with_cuda())  # Should be True
   ```

3. Set CUDA paths manually if auto-detection fails

**Prevention:**
- Verify GPU setup before starting large batches
- Test on 100 images first

---

### ❌ Disk Full During Execution

**Symptoms:**
- "No space left on device" error
- System becomes unresponsive
- Process crashes partway through

**Diagnosis:**
```bash
df -h  # Check disk usage
sudo du -sh /var/lib/docker/containers/*/*-json.log  # Check Docker logs
```

**Solution:**
1. Free up disk space:
   ```bash
   # Clean Docker logs
   sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log

   # Remove old outputs
   rm -rf output/old_runs/

   # Clean package cache
   conda clean --all
   ```

2. Configure Docker log rotation:
   ```bash
   # Edit /etc/docker/daemon.json
   {
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "50m",
       "max-file": "3"
     }
   }
   ```

**Prevention:**
- Check disk space before starting (need 20GB+ free)
- Configure log rotation
- Monitor disk usage during long runs

---

### ❌ PaddleOCR Not Found

**Symptoms:**
- "ModuleNotFoundError: No module named 'paddleocr'"
- Pre-flight check fails for PaddleOCR

**Diagnosis:**
```bash
python3 -c "import paddleocr"
```

**Solution:**
1. Install PaddleOCR:
   ```bash
   pip install paddleocr>=2.7.0
   ```

2. Or specify different Python environment:
   ```bash
   ./run.sh /path/to/crops --python /path/to/python3
   ```

**Prevention:**
- Use dedicated conda environment with PaddleOCR
- Document Python environment path

---

### ❌ No Crop Files Found

**Symptoms:**
- "No .jpg files found in directory"
- Pre-flight check shows 0 files

**Diagnosis:**
```bash
ls -la /path/to/crops/*.jpg | head -10
find /path/to/crops -name "*.jpg" | wc -l
```

**Solution:**
1. Verify correct directory path
2. Check file extensions (must be .jpg, not .jpeg or .png)
3. Check file permissions

**Prevention:**
- Always verify crop directory exists before running
- Use absolute paths to avoid confusion

---

### ❌ GPU Not Detected

**Symptoms:**
- "GPU not detected - will run slower on CPU"
- nvidia-smi command not found

**Diagnosis:**
```bash
nvidia-smi
lspci | grep -i nvidia
```

**Solution:**
1. Install NVIDIA drivers:
   ```bash
   ubuntu-drivers devices
   sudo apt install nvidia-driver-XXX
   ```

2. Verify CUDA is installed:
   ```bash
   nvcc --version
   ```

3. If GPU exists but not detected, check docker GPU access:
   ```bash
   docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
   ```

**Prevention:**
- Verify GPU setup before starting
- Test GPU with simple CUDA program

---

### ⚠️ Moderate Success Rate (70-85%)

**Symptoms:**
- Success rate acceptable but below target
- Some GPS coordinates being extracted

**Diagnosis:**
- Check crop parameters are optimal (0.70 width, 0.22 height)
- Review sample failed crops visually

**Solution:**
1. Try decimal recovery to fix missing decimal points:
   ```bash
   python scripts/decimal_recovery.py \
       --input output/results.xlsx \
       --output output/recovered.xlsx
   ```

2. Adjust crop height if needed:
   ```bash
   # In config/extraction.conf
   CROP_HEIGHT_PCT=0.28  # Try taller crops
   ```

3. Run with re-OCR option:
   ```bash
   python scripts/decimal_recovery.py \
       --input output/results.xlsx \
       --output output/recovered.xlsx \
       --re-ocr
   ```

**Prevention:**
- Test crop parameters on sample first
- Use recommended parameters (0.70, 0.22)

---

## Performance Issues

### Expected vs Actual Performance

| Metric | Expected | Action if Different |
|--------|----------|---------------------|
| Processing speed | 6-8 img/s | Check GPU usage |
| GPU utilization | 20-30% | Verify GPU mode enabled |
| Success rate | 85-90% | Check crop width ≥ 0.70 |
| Time for 28k images | 40-60 min | Reduce workers if OOM |

### Monitoring During Execution

```bash
# Terminal 1: Run extraction
./run.sh /path/to/crops

# Terminal 2: Monitor progress
watch -n 2 nvidia-smi

# Terminal 3: Check progress
./scripts/monitor_progress.sh
```

---

## Recovery Strategies

### If Success Rate < 50%

1. **STOP** and diagnose before continuing
2. Check crop width is ≥ 0.70
3. Verify GPU is working
4. Test on 100 images first
5. Review logs for errors

### If Success Rate 50-70%

1. Complete current run
2. Try decimal recovery:
   ```bash
   python scripts/decimal_recovery.py --input results.xlsx --output recovered.xlsx --re-ocr
   ```
3. Adjust crop parameters if needed
4. Re-run with optimized settings

### If Success Rate 70-85%

1. This is acceptable for most use cases
2. Run decimal recovery for marginal gains
3. Review failed samples to see if they have visible GPS

### If Success Rate > 85%

1. ✅ Excellent results!
2. Remaining failures are likely genuine (corrupted, no GPS, etc.)
3. Manual review of failures optional

---

## Getting Help

If problems persist:

1. **Check logs:** `logs/extraction.log`
2. **Review docs:** `docs/AGENT_SPEC.md`
3. **Read learnings:** `docs/CRITICAL_LEARNINGS.md`
4. **Test subset:** Run on 100 images first
5. **Verify setup:** Run all pre-flight checks

---

**Last Updated:** 2025-11-16

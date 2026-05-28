# Troubleshooting Guide

Common issues and solutions when setting up ML environments with PyTorch.

## Table of Contents

- [Installation Issues](#installation-issues)
- [GPU Not Detected](#gpu-not-detected)
- [NVIDIA / CUDA Issues](#nvidia--cuda-issues)
- [AMD / ROCm Issues](#amd--rocm-issues)
- [WSL2 Specific Issues](#wsl2-specific-issues)
- [Performance Problems](#performance-problems)
- [Python and Package Issues](#python-and-package-issues)
- [Environment Issues](#environment-issues)

---

## Installation Issues

### Setup Script Fails Immediately

**Symptoms**: Script exits with error before detecting hardware

**Common Causes**:
- `uv` not installed
- Wrong Python version
- Permission issues

**Solutions**:
```bash
# Install or update uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Check uv is in PATH
which uv

# Check permissions on project directory
ls -la /path/to/project

# For a fresh start, ask Claude to create a new test project:
# "Help me set up a test ML project at /tmp/test-project"
```

### Package Installation Fails

**Symptoms**: Downloads fail or packages won't install

**Solutions**:
```bash
# Clear uv cache
uv cache clean

# Check internet connectivity
ping pypi.org

# Try different index URL (for AMD GPUs)
# Edit setup-universal.sh if needed

# Check disk space
df -h
```

### Python Version Not Available

**Error**: `Python 3.13 may not be available via uv`

**Solution**:
```bash
# Edit setup-universal.sh
# Change PYTHON_VERSION="3.13" to "3.12" or "3.11"
nano ~/.claude/skills/ml-env/scripts/setup-universal.sh

# Or use a different Python
uv python list  # See available versions
```

---

## GPU Not Detected

### General GPU Detection

**Symptom**: PyTorch reports no CUDA/GPU available

**Diagnostic Steps**:

1. **Check if GPU is visible to system**:
   ```bash
   # For NVIDIA
   lspci | grep -i nvidia

   # For AMD
   lspci | grep -i amd | grep -i vga
   ```

2. **Check drivers are loaded**:
   ```bash
   # For NVIDIA
   nvidia-smi

   # For AMD
   rocm-smi
   rocminfo
   ```

3. **Test PyTorch detection**:
   ```bash
   source ml-env/bin/activate
   python -c "import torch; print(torch.cuda.is_available())"
   ```

### NVIDIA GPU Not Showing

**Solutions**:
```bash
# Check NVIDIA driver version
nvidia-smi

# Driver version should be:
#   520+ for CUDA 12.x
#   550+ for CUDA 13.0

# Update drivers if needed (Ubuntu)
sudo ubuntu-drivers devices
sudo ubuntu-drivers autoinstall

# Reboot after driver update
sudo reboot
```

### AMD GPU Not Showing

**Solutions**:
```bash
# Check ROCm installation
rocm-smi
rocminfo | grep gfx

# Check user groups (required for AMD)
groups | grep -E "render|video"

# Add to groups if missing
sudo usermod -aG render,video $USER
newgrp render  # Or logout/login

# Verify GPU is accessible
ls -l /dev/dri/
```

---

## NVIDIA / CUDA Issues

### CUDA Version Mismatch

**Symptoms**:
- PyTorch installed but CUDA not working
- "CUDA runtime version" errors

**Solution**:
```bash
# Check CUDA version PyTorch was built with
python -c "import torch; print(torch.version.cuda)"

# Check system CUDA version
nvcc --version

# Reinstall PyTorch with correct CUDA version
source ml-env/bin/activate
uv pip uninstall torch torchvision torchaudio
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

### New GPU Not Supported (Blackwell, etc.)

**Symptoms**:
- GPU detected by nvidia-smi
- PyTorch sees GPU but can't use it
- Warnings about "unsupported compute capability"

**For newer GPUs (RTX 5000 series)**:
```bash
# Use PyTorch nightly builds
source ml-env/bin/activate
uv pip uninstall torch torchvision torchaudio
uv pip install torch torchvision torchaudio --pre --index-url https://download.pytorch.org/whl/nightly/cu128
```

**Check compute capability**:
```bash
nvidia-smi --query-gpu=compute_cap --format=csv,noheader
```

**Common GPU architectures**:
- sm_86: RTX 3090, A6000 (Ampere) - Full support ✅
- sm_89: RTX 4090, 4080, 4060 (Ada Lovelace) - Full support ✅
- sm_90: H100, H200 (Hopper) - Full support ✅
- sm_100: B100, GB200, B200 data center (Blackwell) - Limited support ⚠️
- sm_120+: RTX 5000 series consumer (Blackwell) - Experimental ⚠️

**Note**: sm_120+ GPUs may need nightly builds or have limited optimization.

### Out of Memory Errors

**Symptoms**: `CUDA out of memory` errors

**Solutions**:
```python
import torch

# Clear cache
torch.cuda.empty_cache()

# Check memory usage
print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f}GB")
print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f}GB")

# Reduce batch size
batch_size = 16  # Try smaller values

# Use gradient checkpointing
model.gradient_checkpointing_enable()

# Use mixed precision
from torch.cuda.amp import autocast
with autocast():
    output = model(input)
```

---

## AMD / ROCm Issues

### ROCm Not Working

**Symptoms**: PyTorch installed but GPU not accessible

**Solutions**:

1. **Check ROCm installation**:
   ```bash
   rocminfo
   rocm-smi

   # Should show your GPU
   ```

2. **Verify user permissions**:
   ```bash
   groups | grep -E "render|video"

   # Add if missing
   sudo usermod -aG render,video $USER
   # Logout and login again
   ```

3. **Check PyTorch ROCm version**:
   ```bash
   python -c "import torch; print(torch.version.hip)"
   ```

### Strix Halo (gfx1151) Specific Setup

**Special case**: AMD Strix Halo (Ryzen AI Max+ 395, Radeon 8060S, gfx1151)

**Critical**: Official PyTorch wheels DO NOT work with gfx1151!

#### Prerequisites

- Ubuntu 24.04+ recommended
- Linux kernel 6.16.9+ recommended
- ROCm 6.4.4+ or 7.0.2+ installed
- User must be in `render` and `video` groups
- 64GB+ RAM for large models (30B+)

#### Quick Checks

```bash
# Check ROCm detects gfx1151
rocminfo | grep gfx1151

# Check user groups
groups | grep -E "render|video"

# Add to groups if missing
sudo usermod -aG render,video $USER
newgrp render  # Or logout/login
```

#### Installation Options

**Option 1: ROCm 6.4.4+ Nightlies (RECOMMENDED ⭐)**

Most stable, community-tested:
```bash
source ml-env/bin/activate
uv pip uninstall torch torchvision torchaudio
uv pip install --pre torch torchvision torchaudio \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/
```

**Option 2: ROCm 7.9 Stable gfx1151 Builds**

Official stable release:
```bash
uv pip install torch torchvision torchaudio \
  --index-url https://repo.amd.com/rocm/whl/gfx1151/
```

**Option 3: ROCm 7.0.2+ Nightlies (Experimental)**

Latest features, may be unstable:
```bash
uv pip install --pre torch torchvision torchaudio \
  --index-url https://rocm.nightlies.amd.com/v2/gfx1151/
```

**Option 4: CPU Fallback**

If ROCm doesn't work:
```bash
uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cpu
```

#### Common Errors

**Error**: `HIP error: invalid device function`
- **Cause**: Using official PyTorch wheels (not gfx1151 builds)
- **Solution**: Reinstall with one of the options above

**Error**: GPU not detected
- Check user groups (render/video)
- Check ROCm installation: `rocminfo`
- Check GPU visible: `lspci | grep -i amd`

#### Memory Configuration

**Default**: ~33GB GPU-accessible memory
**With GTT**: Up to 113GB on 64GB RAM systems

GTT allows using system RAM as GPU memory for large models (30B+).

To enable GTT, see: https://github.com/ianbarber/strix-halo-skills

#### Model Size Guidelines

With default memory (~33GB):
- ✅ 7B models in FP16: ~14GB
- ✅ 13B models in FP16: ~26GB
- ⚠️ 30B models: Need GTT
- ❌ 65B+ models: Too large

With GTT configured (113GB):
- ✅ 30B models in FP16: ~60GB
- ⚠️ 65B models: Marginal (may be slow)

#### Performance Tips

```python
import torch

# Verify ROCm is working
print(f"ROCm available: {torch.cuda.is_available()}")
print(f"ROCm version: {torch.version.hip}")

# Enable optimizations
torch.backends.cudnn.benchmark = True

# Monitor memory
print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f}GB")
print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f}GB")
```

#### Resources

- Setup repo: https://github.com/ianbarber/strix-halo-skills
- Community discussion: https://github.com/ROCm/TheRock/discussions/655
- Community builds: https://github.com/scottt/rocm-TheRock/releases
- AMD ROCm docs: https://rocm.docs.amd.com/

### ROCm Version Mismatch

**Check compatibility**:
```bash
# System ROCm version
rocminfo | grep "ROCm version"

# PyTorch ROCm version
python -c "import torch; print(torch.version.hip)"
```

**Reinstall if mismatched**:
```bash
# For ROCm 6.2
uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/rocm6.2
```

---

## WSL2 Specific Issues

### GPU Not Accessible in WSL2

**Critical**: WSL2 uses Windows drivers, not Linux drivers

**Common Mistake**: Installing Linux NVIDIA drivers in WSL2
- ❌ DO NOT install Linux NVIDIA drivers
- ✅ DO use Windows NVIDIA drivers

**Solutions**:

1. **Update Windows NVIDIA driver** (on Windows, not in WSL2)
   - Download from nvidia.com
   - Version 520+ required

2. **Verify WSL2 can see GPU**:
   ```bash
   # From within WSL2
   nvidia-smi
   # Should show your GPU
   ```

3. **If nvidia-smi fails in WSL2**:
   ```powershell
   # From Windows PowerShell
   wsl --shutdown
   wsl
   ```

4. **Reinstall PyTorch** (if still not working):
   ```bash
   rm -rf ml-env
   bash ~/.claude/skills/ml-env/scripts/setup-universal.sh
   ```
   Or ask Claude: "Help me recreate my ML environment"

### WSL2 Network Issues

**Symptom**: Can't download packages

**Solution**:
```bash
# Check internet from WSL2
ping 8.8.8.8

# If fails, restart WSL2
# From Windows PowerShell:
wsl --shutdown
wsl
```

---

## Performance Problems

### Slow Training

**Diagnostic**:
```python
import torch

# Check if using GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# Check GPU utilization
# In another terminal:
nvidia-smi -l 1  # or rocm-smi
```

**Solutions**:

1. **Enable optimizations**:
   ```python
   import torch

   # Enable benchmarking
   torch.backends.cudnn.benchmark = True

   # Enable TF32 (Ampere+ GPUs)
   torch.backends.cuda.matmul.allow_tf32 = True
   torch.backends.cudnn.allow_tf32 = True
   ```

2. **Use mixed precision**:
   ```python
   from torch.cuda.amp import autocast, GradScaler

   scaler = GradScaler()

   for data, target in dataloader:
       optimizer.zero_grad()
       with autocast():
           output = model(data)
           loss = criterion(output, target)
       scaler.scale(loss).backward()
       scaler.step(optimizer)
       scaler.update()
   ```

3. **Check data loading**:
   ```python
   # Use multiple workers
   dataloader = DataLoader(dataset, num_workers=4, pin_memory=True)
   ```

### GPU Not Being Used

**Check**:
```python
import torch

# Verify model is on GPU
print(next(model.parameters()).device)

# Verify data is on GPU
print(data.device)

# Move if needed
model = model.to('cuda')
data = data.to('cuda')
```

---

## Python and Package Issues

### Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'torch'`

**Solution**:
```bash
# Activate environment first
source ml-env/bin/activate

# Verify torch is installed
python -c "import torch; print(torch.__version__)"

# Reinstall if needed
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

### Version Conflicts

**Symptom**: Package compatibility errors

**Solution**:
```bash
# Check installed versions
uv pip list

# Recreate environment
rm -rf ml-env
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh

# Or update specific package
uv pip install --upgrade package-name
```

### Python Version Issues

**Symptom**: `python: command not found` or wrong Python version

**Solution**:
```bash
# Activate environment
source ml-env/bin/activate

# Verify Python version
python --version

# Should be 3.13 (or 3.12/3.11 if you changed it)
```

---

## Environment Issues

### Environment Not Activating

**Symptom**: `activate: No such file or directory`

**Solution**:
```bash
# Check environment exists
ls ml-env/bin/activate

# Use absolute path
source /full/path/to/project/ml-env/bin/activate

# Recreate if missing
rm -rf ml-env
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh
```

### Wrong Environment Activated

**Symptom**: Using wrong Python or packages

**Solution**:
```bash
# Deactivate current environment
deactivate

# Activate correct one
source /path/to/correct/ml-env/bin/activate

# Verify
which python
python -c "import torch; print(torch.__version__)"
```

### Permission Errors

**Symptom**: Can't write to environment or install packages

**Solution**:
```bash
# Check ownership
ls -la ml-env/

# Fix permissions
chmod -R u+w ml-env/

# Or recreate with correct user
rm -rf ml-env
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh
```

---

## General Diagnostics

### Complete System Check

Run these commands to gather diagnostic information:

```bash
# System info
uname -a

# GPU info (NVIDIA)
nvidia-smi

# GPU info (AMD)
rocm-smi
rocminfo | grep gfx

# Python and environment
source ml-env/bin/activate
python --version
which python

# PyTorch info
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'Version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"

# Installed packages
uv pip list

# Check logs
cat setup-*.log
```

### Validation Script

The included validation script tests everything:

```bash
source ml-env/bin/activate
./validate.sh
```

This checks:
- Python version
- PyTorch installation
- GPU detection
- Basic computation
- Package versions

---

## Getting Help

### Before Asking for Help

1. ✅ Run `./validate.sh` and share the output
2. ✅ Check the log file (`setup-*.log`)
3. ✅ Share your hardware (GPU model, driver version)
4. ✅ Share your platform (Ubuntu version, WSL2, etc.)
5. ✅ Share exact error messages

### Where to Ask

- **GitHub Issues**: https://github.com/ianbarber/ml-env-setup/issues
- **Include**:
  - Your GPU model
  - Platform (Linux/WSL2)
  - Output of `./validate.sh`
  - Log file contents
  - Exact error message

### Known Limitations

**GPU Architecture Support**:
- Newer Blackwell GPUs (RTX 5000 series, sm_120+): Experimental, may need nightly builds
- Strix Halo (gfx1151): Requires special AMD builds
- Older GPUs (sm_35 and below): Not supported by PyTorch 2.10.0

**Platform Support**:
- Linux: Full support ✅
- WSL2: Full support ✅ (with Windows drivers)
- macOS: Not supported (no CUDA/ROCm)
- Windows native: Not supported (use WSL2)

**Python Versions**:
- 3.13: Recommended (default)
- 3.12, 3.11: Also supported
- 3.14: Preview, may have ML package compatibility issues
- 3.10 and below: Not recommended

---

## Quick Reference

### Reinstall PyTorch

```bash
source ml-env/bin/activate
uv pip uninstall torch torchvision torchaudio

# NVIDIA (CUDA 12.8)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# AMD (ROCm 6.2)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2

# Strix Halo (gfx1151)
uv pip install --pre torch torchvision torchaudio --index-url https://rocm.nightlies.amd.com/v2/gfx1151/

# CPU only
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# NVIDIA nightly (for new GPUs)
uv pip install torch torchvision torchaudio --pre --index-url https://download.pytorch.org/whl/nightly/cu128
```

### Recreate Environment

```bash
cd /path/to/project
rm -rf ml-env
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh
```

### Test GPU

```python
import torch

print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

    # Test computation
    x = torch.randn(1000, 1000, device='cuda')
    y = x @ x.T
    print("✓ GPU computation successful")
```

# Troubleshooting AMD Strix Halo Setup

## Common Issues

### Quick Diagnosis

```bash
# Run the verification script
./.claude/skills/strix-halo-setup/scripts/verify_system.sh
```

This checks all prerequisites and identifies specific issues.

## Problem 1: GPU Not Detected

**Symptom**: `torch.cuda.is_available()` returns `False`

### Most Common Cause: User Groups

**Check:**
```bash
groups | grep -E "render|video"
```

**Fix:**
```bash
sudo usermod -aG render,video $USER
# Log out and back in (or reboot)
```

### Check ROCm Installation

```bash
rocm-smi
# Should show: GPU[0] gfx1151
```

If not, install ROCm 6.4.4+ or 7.x (see skill documentation).

### Check PyTorch Has ROCm Support

```bash
python -c "import torch; print(hasattr(torch.version, 'hip'))"
# Should print: True
```

If False, you have CPU-only PyTorch. Install ROCm version.

## Problem 2: GPU Detected But Compute Fails

**Symptom**: `torch.cuda.is_available()` is `True` but operations fail with:
```
RuntimeError: HIP error: invalid device function
```

**Cause**: Using official PyTorch wheels (don't work with gfx1151)

**Fix**: Install community builds:
```bash
pip uninstall torch torchvision torchaudio
pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch
```

**Verify:**
```bash
python -c "import torch; a=torch.tensor([1.0]).cuda(); print((a+1).item())"
# Should print: 2.0
```

## Problem 3: Out of Memory with Models < 30GB

**Symptom**: OOM errors with models that should fit

**Cause**: GTT not configured (limited to ~33GB)

**Fix:**
```bash
# Run the GTT configuration script
./.claude/skills/strix-halo-setup/scripts/configure_gtt.sh
```

Or manually add to GRUB (kernels before 6.16.9):
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdttm.pages_limit=27648000 amdttm.page_pool_size=27648000"
```

**Note**: Kernel 6.16.9+ doesn't need GTT parameters.

## Problem 4: Environment Variables

**Symptom**: GPU works sometimes, not others

**Cause**: Environment variables not set consistently

**Fix**: Use conda activation scripts (the skill does this automatically):

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
cat > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh << 'EOF'
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export PYTORCH_ROCM_ARCH=gfx1151
export HSA_XNACK=1
EOF
chmod +x $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

**Important**: Environment variables must be set BEFORE importing PyTorch. Setting them in Python won't work.

## Problem 5: Kernel Upgrade Fails (DKMS Build Error)

**Symptom**: When upgrading kernel, DKMS build fails:
```
Error! Bad return status for module build on kernel
dkms autoinstall failed for amdgpu
```

**Cause**: amdgpu-dkms installed, but Strix Halo should use inbox kernel driver

**Fix**: Remove DKMS and use inbox driver:
```bash
# Remove DKMS modules
sudo dkms remove amdgpu/$(dkms status | grep amdgpu | head -1 | cut -d, -f2 | tr -d ' ') --all

# Uninstall DKMS packages
sudo apt remove amdgpu-dkms amdgpu-dkms-firmware -y

# Fix broken installation
sudo apt install -f

# Reboot
sudo reboot
```

After reboot, the kernel's built-in amdgpu driver will be used.

**Note**: ROCm should be installed with `--no-dkms` flag for APUs.

## Problem 6: Checkerboard Artifacts in Image Generation (ROCm 7.x)

**Symptom**: When running SD3.5XL, FLUX, or other large VAE decodes, you see checkerboard or corrupted patterns in output images.

**Cause**: SDMA (System DMA) issues on APUs with ROCm 7.x

**Fix**: Disable SDMA:
```bash
export HSA_ENABLE_SDMA=0
```

Add this to your conda activation script for permanent fix.

## Problem 7: hipBLASLt Unsupported Architecture Warning (ROCm 7.x)

**Symptom**: Warning messages about hipBLASLt falling back to hipBLAS:
```
hipBLASLt: unsupported architecture gfx1151, falling back to hipBLAS
```

**Cause**: hipBLASLt fastpath not yet optimized for gfx1151

**Status**: This is a known limitation as of ROCm 7.2. The fallback works correctly but is slower. AMD is working on native gfx1151 support.

**Workaround**: None needed - the fallback is automatic. For best performance, consider Vulkan backend for inference-only workloads.

## Problem 8: Slow LLM Token Generation

**Symptom**: LLM inference shows low tokens/second (~1-2 tok/s on 70B models), much slower than expected.

**Cause**: On gfx1151, LLM decode is memory-copy bound. Profiling shows ~92-95% of time in `hipMemcpyWithStream` rather than compute kernels.

**Mitigations**:
1. Use smaller models (7B-13B) for better throughput
2. Use Vulkan backend with llama.cpp for inference (often faster)
3. Use BF16 instead of FP32 where possible
4. Set memory allocation optimizations:
   ```bash
   export PYTORCH_HIP_ALLOC_CONF="backend:native,expandable_segments:True,garbage_collection_threshold:0.9"
   ```

## Problem 9: Mixed ROCm Version Installation

**Symptom**: `rocm-smi --version` shows different versions for different components (e.g., ROCm 6.4.2 base but rocm-smi-lib 7.5.0)

**Cause**: Partial upgrade or multiple ROCm installations

**Fix**: Clean install ROCm:
```bash
# Remove existing ROCm
sudo apt purge rocm* hip* 2>/dev/null
sudo apt autoremove -y

# Clean up directories
sudo rm -rf /opt/rocm*

# Fresh install (see installation section)
```

## Diagnostic Commands

```bash
# Check GPU visibility
lspci | grep -i amd
rocm-smi
rocminfo | grep gfx1151

# Check PyTorch installation
python -c "import torch; print('PyTorch:', torch.__version__); print('HIP:', torch.version.hip if hasattr(torch.version, 'hip') else 'None')"

# Test GPU detection
python -c "import torch; print('GPU detected:', torch.cuda.is_available())"

# Test compute
python -c "import torch; a=torch.tensor([1.0]).cuda(); print('Compute works:', (a+1).item())"

# Check environment variables
env | grep -E "HSA_|PYTORCH_|ROCM_"
```

## When Everything Works

You should see:
- `torch.cuda.is_available()` returns `True`
- Compute operations complete without HIP errors
- Can allocate 30GB+ tensors (with GTT configured)

If using the skill-created environment, variables are auto-configured via conda activation scripts.
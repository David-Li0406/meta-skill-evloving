# AMD Strix Halo GTT Memory Configuration

## Executive Summary

The AMD Strix Halo (Ryzen AI MAX+) requires GTT (Graphics Translation Table) configuration to access more than ~33GB of memory for GPU workloads.

**Latest Update (October 2025)**: Linux kernel 6.16.9+ includes UMA (Unified Memory Architecture) fixes that eliminate the need for manual GTT kernel parameters on many systems.

## The Problem

### Current Situation
- **Hardware Capability**: 128GB unified memory (LPDDR5X-8000)
- **Actual Accessible**: 33.5GB via GTT
- **Impact**: Cannot run large LLMs that would fit in system memory
- **Root Cause**: GTT configuration in amdgpu driver

### Technical Details
- GTT (Graphics Translation Table) maps system memory for GPU access
- Current ROCm/driver configuration limits GTT to 33.5GB
- Post Linux 6.10: ROCm allocates only in GTT (not reserved VRAM)
- Pre Linux 6.10: ROCm allocates only in reserved VRAM

## Solutions

### Solution 1: Upgrade to Kernel 6.16.9+ (RECOMMENDED)

**Best option**: Upgrade to Linux kernel 6.16.9 or later. These kernels include UMA fixes and don't require manual GTT parameters.

```bash
# Check your kernel version
uname -r

# If 6.16.9+, no GTT parameters needed - it just works!
```

### Solution 2: Kernel Parameters (For Older Kernels)

If using kernel 6.16.8 or earlier, configure GTT manually:

```bash
# For 108GB GTT (tested stable)
# Calculation: (108 * 1024 * 1024) / 4.096 = 27648000

# Edit /etc/default/grub:
sudo nano /etc/default/grub

# Add to GRUB_CMDLINE_LINUX_DEFAULT:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdttm.pages_limit=27648000 amdttm.page_pool_size=27648000"

# Update grub and reboot
sudo update-grub
sudo reboot
```

### Solution 3: Environment Variables (Supplemental)
```bash
# Add to ~/.bashrc or /etc/environment
export HSA_XNACK=1  # Enable unified memory page faults
export HSA_FORCE_FINE_GRAIN_PCIE=1
export GPU_MAX_HEAP_SIZE=100
export GPU_MAX_ALLOC_PERCENT=100
```

## Verification Steps

### Check Current GTT Size
```bash
# Method 1: ROCm SMI
rocm-smi --showmeminfo gtt

# Method 2: Sysfs
cat /sys/class/drm/card0/device/mem_info_gtt_total

# Method 3: Python test
python3 -c "
import torch
if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f'Total memory: {props.total_memory / 1e9:.1f} GB')
"
```

### Test Large Allocation
```python
import torch

# Test progressively larger allocations
for size_gb in [32, 48, 64, 80, 96]:
    try:
        tensor = torch.zeros(int(size_gb * 1e9 / 4), device='cuda')
        print(f"✓ Allocated {size_gb} GB")
        del tensor
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"✗ Failed at {size_gb} GB: {e}")
        break
```

## Known Issues & Status

### GitHub Issues Tracking This Problem
1. **[ROCm/ROCm #2774](https://github.com/ROCm/ROCm/issues/2774)**: "Better support for APUs"
2. **[ollama/ollama #5471](https://github.com/ollama/ollama/issues/5471)**: "Memory calculation on AMD APU"
3. **[ollama/ollama #6362](https://github.com/ollama/ollama/issues/6362)**: "Honor amdgpu.gttsize parameter"

### Community Findings
- **Maximum Safe GTT**: 108GB before errors on Strix Halo
- **Kernel 6.16.9+**: GTT parameters no longer needed (UMA fixes included)
- **Kernel 6.14-6.16.8**: Requires `amdttm.pages_limit` parameter
- **Kernel 6.10-6.13**: Requires `amdttm.pages_limit` parameter, less stable

## Alternative Approaches

### 1. Use Vulkan Instead of ROCm
```bash
# Install Vulkan drivers
sudo apt install mesa-vulkan-drivers vulkan-tools

# Test with llama.cpp using Vulkan backend
./llama-cli -m model.gguf -ngl 99 --gpu-backend vulkan
```

### 2. CPU+GPU Hybrid Approach
```python
# Split model between CPU and GPU
from transformers import AutoModel

model = AutoModel.from_pretrained(
    "model_name",
    device_map="auto",  # Automatically split between CPU/GPU
    max_memory={0: "30GiB", "cpu": "60GiB"}
)
```

### 3. Quantization to Fit in Available Memory
```python
# Use 4-bit quantization to reduce memory requirements
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    quantization_config=quantization_config,
    device_map="cuda"
)
```

## Recommendations

### Best Path Forward:
1. **Upgrade to kernel 6.16.9+** if possible (no manual configuration needed)
2. **If on older kernel**: Apply TTM kernel parameters (108GB tested stable)
3. Use environment variables for unified memory (HSA_XNACK=1)
4. Consider Vulkan for inference workloads

## Quick Reference Commands

```bash
# Check current configuration
rocm-smi --showmeminfo gtt
dmesg | grep -i gtt

# Apply maximum GTT fix
sudo grubby --update-kernel=ALL --args='amdttm.pages_limit=27648000'
sudo reboot

# Test memory allocation
python3 -c "import torch; t=torch.zeros(int(96e9/4), device='cuda'); print('96GB allocated')"

# Monitor memory usage
watch -n 1 'rocm-smi --showmeminfo vram && rocm-smi --showmeminfo gtt'
```

---

*Note: The GTT limitation is actively being addressed by AMD and the open-source community. This guide will be updated as new solutions become available.*

*Last verified: August 2025 on AMD Ryzen AI MAX+ 395 (Strix Halo)*
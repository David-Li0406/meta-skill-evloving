---
name: ml-env
description: Set up ML environments with PyTorch and auto-detect hardware. Use this when creating new ML projects, setting up PyTorch, or troubleshooting GPU/environment issues. Guides you through creating isolated project environments with hardware-specific PyTorch builds (NVIDIA/AMD/CPU).
allowed-tools: Read, Bash, WebFetch
activation-precedence: high
---

# ML Environment Setup & Troubleshooting

This skill helps you create and manage isolated ML environments with PyTorch. It auto-detects your hardware (NVIDIA GPU, AMD GPU, or CPU) and installs the appropriate PyTorch build.

## Creating a New ML Project

I can help you set up a complete ML project with PyTorch in seconds. Here's what I'll do:

1. Create your project directory
2. Create a `.gitignore` for ML files
3. Run hardware detection
4. Install PyTorch with the right backend
5. Install ML libraries
6. Validate everything works

**To get started, tell me:**
- Project name/path where you want it created
- I'll handle the rest!

## Interactive Setup Process

When you ask me to set up a new ML project, I will:

```bash
# 1. Create the project directory
mkdir -p ~/projects/my-ml-project

# 2. Create .gitignore
# (ignores ml-env/, data/, models/, logs/, etc.)

# 3. Run the setup script
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh

# 4. Show you the results
```

The setup script will:
- Detect your GPU (NVIDIA with nvidia-smi, AMD with rocminfo, or fallback to CPU)
- Ask questions for special hardware (Blackwell GPUs, Strix Halo, etc.)
- Install Python 3.13 virtual environment with uv
- Install PyTorch 2.10.0 with correct backend
- Install ML libraries: numpy, pandas, scikit-learn, jupyter, accelerate, etc.
- Create `ml-env/` directory in your project
- Optionally initialize git

## After Setup: Using Your Environment

Once created, activating is simple:

```bash
cd ~/projects/my-ml-project
source ml-env/bin/activate  # Regular environments
# OR
source ml-env/activate-safe.sh  # If you use conda (ignores conda settings)
```

Check it works:
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

## Hardware-Specific Guidance

### NVIDIA GPUs
- **Supported**: RTX 3090, 4090, 5090, and most Ampere/Ada/Blackwell
- **Installation**: CUDA 12.8 (stable) or CUDA 13.0 (for RTX 5090)
- **Driver requirement**: 520+ for CUDA 12.8, 550+ for CUDA 13.0
- **WSL2 users**: Use Windows NVIDIA driver only (do NOT install Linux driver)

### AMD RDNA (RX 6000/7000 series)
- **Installation**: ROCm 6.2
- **Requirements**: User in `render` and `video` groups
- **Setup**: `sudo usermod -aG render,video $USER && newgrp render`

### AMD Strix Halo (gfx1151)
**⚠️ This is complex and requires special handling!**

- **GPU**: Ryzen AI MAX+ 395 with gfx1151
- **Critical issue**: Official PyTorch wheels do NOT work
- **Solution**: Must use AMD community nightly builds
- **ROCm**: 6.4.4+ or 7.x
- **Memory limits**: Default ~33GB; configure GTT for larger models (30B+)
- **Setup requires**: User in `render` and `video` groups, Linux kernel 6.14+

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for complete Strix Halo setup and GTT memory configuration.

### CPU-Only Systems
- Works everywhere
- Good for development/testing
- Use for learning before scaling to GPU

## Current Versions (2026)

- **PyTorch**: 2.10.0
- **Python**: 3.13 (or 3.12 if needed)
- **CUDA**: 12.8 (main), 13.0 (Blackwell experimental)
- **ROCm**: 6.2 (RDNA), 6.4.4+/7.x (Strix Halo)
- **Key ML libs**: numpy, pandas, matplotlib, scikit-learn, jupyter, accelerate, tensorboard

## Validating an Existing Environment

If you already have a project and want to verify it works:

```bash
cd ~/your-ml-project
bash ~/.claude/skills/ml-env/scripts/validate.sh
```

This will check:
- Python and PyTorch versions
- GPU/CPU backend detection
- GPU memory and specifications
- Computation tests

## Troubleshooting

### GPU Not Detected

**NVIDIA:**
```bash
nvidia-smi  # Check driver is installed
python -c "import torch; print(torch.cuda.is_available())"
```

**AMD:**
```bash
rocm-smi  # Check ROCm installation
rocminfo | grep gfx  # Check GPU architecture
```

### CUDA Out of Memory
1. Reduce batch size
2. Enable mixed precision training
3. Use `torch.cuda.empty_cache()` between batches
4. Try gradient accumulation

### PyTorch Not Finding GPU After Install
1. Activate the environment: `source ml-env/bin/activate`
2. Check driver version
3. Reinstall PyTorch with correct index URL:
   ```bash
   uv pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu128
   ```

### Strix Halo Specific Issues
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#strix-halo-gfx1151-specific-setup) for detailed Strix Halo troubleshooting, GTT memory setup, and performance optimization.

## Best Practices

1. **Always activate first**: Before running any Python/ML code
2. **Use virtual environments**: Never install to system Python
3. **Move models to device**: Explicitly move tensors to GPU
4. **Monitor memory**: Keep an eye on GPU memory usage
5. **Test on CPU first**: Develop with small data on CPU, scale to GPU
6. **Save checkpoints**: Don't train for hours without saving progress

## Common Workflows

### Training a Model
```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = YourModel().to(device)

for batch in dataloader:
    x, y = batch
    x, y = x.to(device), y.to(device)
    loss = model(x, y)
    loss.backward()
```

### Mixed Precision Training (Faster, Less Memory)
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    with autocast():
        loss = model(x, y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Checking GPU Memory
```python
import torch
if torch.cuda.is_available():
    print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f}GB")
    print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f}GB")
    print(f"Total: {torch.cuda.get_device_properties(0).total_memory/1e9:.2f}GB")
```

## Reference Documentation

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues, hardware-specific setup (especially Strix Halo)
- [UPDATE.md](UPDATE.md) - Updating PyTorch and dependencies

## Scripts in This Skill

All scripts are in `~/.claude/skills/ml-env/scripts/`:

- **setup-universal.sh** - Hardware detection and PyTorch installation (used during initial setup)
- **validate.sh** - Validate an existing environment and test GPU/CPU

## When to Use This Skill

Use me when you:
- Want to create a new ML project
- Need to set up PyTorch with GPU support
- Are troubleshooting GPU/CUDA/ROCm issues
- Want to update or maintain your ML environment
- Have hardware-specific questions (NVIDIA, AMD, Strix Halo)
- Need guidance on ML best practices

## Questions?

Ask me anything about:
- Creating new ML projects
- Hardware setup and troubleshooting
- PyTorch installation
- GPU/CPU configuration
- ML best practices
- Updating packages

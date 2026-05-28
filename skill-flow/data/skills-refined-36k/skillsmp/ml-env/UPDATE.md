# Updating and Version Management

## Checking Current Versions

### Check PyTorch and CUDA versions

First, activate your project's environment. From your project directory:

```bash
source ml-env/bin/activate
python -c 'import torch; print(f"PyTorch: {torch.__version__}"); print(f"CUDA: {torch.version.cuda}")'
```

Or if using conda and the conda-safe wrapper:

```bash
source ml-env/activate-safe.sh
python -c 'import torch; print(f"PyTorch: {torch.__version__}"); print(f"CUDA: {torch.version.cuda}")'
```

### Check all installed packages

```bash
source ml-env/bin/activate
uv pip list
```

### Check for outdated packages

```bash
source ml-env/bin/activate
uv pip list --outdated
```

## Updating PyTorch

### Check for newer PyTorch versions

Visit: https://pytorch.org/get-started/locally/

Or check available versions:

```bash
uv pip index versions torch --index-url https://download.pytorch.org/whl/cu128
```

### Update to a specific version (NVIDIA CUDA 12.8)

```bash
source ml-env/bin/activate
uv pip install torch==2.X.Y torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 --upgrade
```

### Update to the latest compatible version (NVIDIA)

```bash
source ml-env/bin/activate
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128 --upgrade
```

### Update to specific ROCm version (AMD)

```bash
source ml-env/bin/activate
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2 --upgrade
```

### Update for Strix Halo (AMD gfx1151)

```bash
source ml-env/bin/activate
uv pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch torchvision torchaudio --upgrade
```

## Updating Other Packages

### Update a specific package

```bash
source ml-env/bin/activate
uv pip install --upgrade package-name
```

### Update all packages (use with caution)

```bash
source ml-env/bin/activate
uv pip list --outdated | tail -n +3 | awk '{print $1}' | xargs -n1 uv pip install --upgrade
```

Note: This may break compatibility. Consider testing in a separate environment first.

## Checking NVIDIA Driver and CUDA Toolkit

### Check NVIDIA driver version

```bash
nvidia-smi
```

### Check CUDA toolkit version

```bash
nvcc --version
```

### Verify GPU compute capability

```bash
source ml-env/bin/activate
python -c 'import torch; print(f"GPU Compute Capability: {torch.cuda.get_device_capability(0)}")'
```

Expected output for RTX 5090: `(12, 0)` indicating SM120

## Recreating the Environment from Scratch

If something goes wrong, you can recreate the environment. From your project directory:

```bash
rm -rf ml-env
bash ~/.claude/skills/ml-env/scripts/setup-universal.sh
```

Or ask Claude to help you recreate it:

```
Help me recreate my ML environment - something isn't working
```

## Exporting Environment Configuration

To create a reproducible environment specification:

```bash
source ml-env/bin/activate
uv pip freeze > requirements.txt
```

To recreate from requirements in a new environment:

```bash
uv venv new-ml-env --python 3.13
source new-ml-env/bin/activate
uv pip install -r requirements.txt
```

## Updating uv itself

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or if installed via pip:

```bash
pip install --upgrade uv
```

# GPS Extraction Skill - Installation Guide

## Prerequisites

### System Requirements

- **Operating System:** Linux (Ubuntu 20.04+ recommended)
- **GPU:** NVIDIA GPU with CUDA support (8GB+ VRAM recommended)
- **RAM:** 16GB+ recommended
- **Disk Space:** 20GB+ free space
- **CUDA:** Version 11.8 or 12.x

### Software Requirements

- Python 3.11
- NVIDIA drivers (525+ recommended)
- CUDA toolkit
- cuDNN library

## Installation Steps

### 1. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system packages
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nvidia-driver-525 \
    build-essential

# Verify GPU
nvidia-smi
```

### 2. Create Python Environment

```bash
# Install Miniconda (if not already installed)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Create environment
conda create -n gps_extraction python=3.11 -y
conda activate gps_extraction
```

### 3. Install Python Packages

```bash
# Install PaddleOCR with GPU support
pip install paddlepaddle-gpu==2.6.0 -i https://mirror.baidu.com/pypi/simple
pip install paddleocr>=2.7.0

# Install other dependencies
pip install \
    pandas>=2.0.0 \
    openpyxl>=3.1.0 \
    numpy>=1.24.0 \
    opencv-python>=4.8.0
```

### 4. Verify Installation

```bash
# Test PaddleOCR
python3 -c "import paddleocr; print('PaddleOCR OK')"

# Test CUDA support
python3 -c "import paddle; print('CUDA:', paddle.device.is_compiled_with_cuda())"

# Expected output:
# PaddleOCR OK
# CUDA: True
```

### 5. Install GPS Extraction Skill

```bash
# Navigate to PROJECTS directory
cd /home/yousuf/PROJECTS

# The skill package should already be here
cd gps_extraction_skill

# Make scripts executable
chmod +x run.sh scripts/*.sh
```

### 6. Configure Settings

```bash
# Edit configuration file
nano config/extraction.conf

# Update Python path if needed:
# PYTHON_BIN=/path/to/your/conda/envs/gps_extraction/bin/python3
```

### 7. Test Installation

```bash
# Run a quick test (replace with your crop directory)
./run.sh /path/to/test/crops --workers 1

# Should show pre-flight checks and start processing
```

## Docker Installation (Alternative)

If you prefer Docker:

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.11 python3-pip git

RUN pip3 install \
    paddlepaddle-gpu==2.6.0 \
    paddleocr>=2.7.0 \
    pandas openpyxl numpy opencv-python

WORKDIR /workspace
COPY . /workspace/

CMD ["/bin/bash"]
EOF

# Build image
docker build -t gps-extraction .

# Run container
docker run --gpus all -v $(pwd):/workspace -it gps-extraction
```

## Troubleshooting Installation

### CUDA Not Found

```bash
# Check CUDA version
nvcc --version

# If not found, install CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run
```

### PaddlePaddle GPU Not Working

```bash
# Uninstall CPU version
pip uninstall paddlepaddle

# Install GPU version
pip install paddlepaddle-gpu==2.6.0
```

### Permission Denied on Scripts

```bash
# Make scripts executable
chmod +x run.sh
chmod +x scripts/*.sh
```

## Verification Checklist

Before using the skill, verify:

- [ ] NVIDIA GPU detected (`nvidia-smi` works)
- [ ] CUDA available (`nvcc --version` shows version)
- [ ] Python 3.11 installed
- [ ] PaddleOCR installed (`python3 -c "import paddleocr"` works)
- [ ] CUDA support enabled (`paddle.device.is_compiled_with_cuda()` returns True)
- [ ] 20GB+ disk space free
- [ ] Scripts are executable (`ls -l run.sh` shows `x` permission)

## Next Steps

After installation:

1. Read `README.md` for usage instructions
2. Review `docs/AGENT_SPEC.md` for detailed documentation
3. Test on a small batch of crops first
4. Run full extraction on your dataset

## Support

For installation issues:

1. Check `docs/TROUBLESHOOTING.md`
2. Verify all prerequisites are met
3. Test each component individually
4. Review system logs

---

**Installation tested on:**
- Ubuntu 22.04 LTS
- NVIDIA RTX 3090
- CUDA 11.8
- Python 3.11

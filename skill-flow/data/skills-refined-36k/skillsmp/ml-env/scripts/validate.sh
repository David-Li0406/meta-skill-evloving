#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_NAME="ml-env"
ENV_PATH="$SCRIPT_DIR/$ENV_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== ML Environment Validation ===${NC}"
echo ""

# Check if environment exists
if [ ! -d "$ENV_PATH" ]; then
    echo -e "${RED}✗ Error: ml-env directory not found at $ENV_PATH${NC}"
    echo "Run ./setup-universal.sh first"
    exit 1
fi

echo -e "${GREEN}✓ Environment directory found${NC}"

# Activate environment (use safe wrapper if available for conda users)
if [ -f "$ENV_PATH/activate-safe.sh" ]; then
    source "$ENV_PATH/activate-safe.sh"
else
    source "$ENV_PATH/bin/activate"
fi

echo ""
echo -e "${BLUE}1. Python Version${NC}"
python --version

echo ""
echo -e "${BLUE}2. UV Version${NC}"
uv --version

echo ""
echo -e "${BLUE}3. PyTorch Installation${NC}"
python -c "import torch; print(f'PyTorch: {torch.__version__}')" || {
    echo -e "${RED}✗ PyTorch not installed correctly${NC}"
    exit 1
}
echo -e "${GREEN}✓ PyTorch installed${NC}"

echo ""
echo -e "${BLUE}4. Backend Detection${NC}"

# Check for CUDA
CUDA_AVAILABLE=$(python -c "import torch; print(torch.cuda.is_available())")
ROCM_AVAILABLE=$(python -c "import torch; print(hasattr(torch.version, 'hip') and torch.version.hip is not None)")

if [ "$CUDA_AVAILABLE" == "True" ]; then
    echo -e "${GREEN}✓ CUDA Backend Detected${NC}"

    echo ""
    echo -e "${BLUE}5. CUDA Information${NC}"
    python -c "import torch; print(f'CUDA Version: {torch.version.cuda}')"
    python -c "import torch; print(f'cuDNN Version: {torch.backends.cudnn.version()}')"
    python -c "import torch; print(f'GPU Count: {torch.cuda.device_count()}')"

    echo ""
    echo -e "${BLUE}6. GPU Details${NC}"
    for i in $(seq 0 $(($(python -c "import torch; print(torch.cuda.device_count())") - 1))); do
        echo -e "GPU $i:"
        python -c "import torch; print(f'  Name: {torch.cuda.get_device_name($i)}')"
        python -c "import torch; print(f'  Compute Capability: {torch.cuda.get_device_capability($i)}')"
        python -c "import torch; cap = torch.cuda.get_device_capability($i); print(f'  SM Version: sm_{cap[0]}{cap[1]}')"
        python -c "import torch; mem = torch.cuda.get_device_properties($i).total_memory / 1024**3; print(f'  Memory: {mem:.2f} GB')"
    done

    echo ""
    echo -e "${BLUE}7. Testing GPU Computation${NC}"
    python -c "
import torch
import time

device = torch.device('cuda:0')
print(f'Using device: {device}')

# Test basic operations
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)

start = time.time()
z = torch.matmul(x, y)
torch.cuda.synchronize()
end = time.time()

print(f'Matrix multiplication successful: {z.shape}')
print(f'Computation time: {(end-start)*1000:.2f} ms')
" && echo -e "${GREEN}✓ GPU computation successful${NC}" || echo -e "${RED}✗ GPU computation failed${NC}"

    # Show nvidia-smi if available
    if command -v nvidia-smi &> /dev/null; then
        echo ""
        echo -e "${BLUE}8. NVIDIA GPU Status${NC}"
        nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv
    fi

elif [ "$ROCM_AVAILABLE" == "True" ]; then
    echo -e "${GREEN}✓ ROCm Backend Detected${NC}"

    echo ""
    echo -e "${BLUE}5. ROCm Information${NC}"
    python -c "import torch; print(f'ROCm Version: {torch.version.hip}')"
    python -c "import torch; print(f'GPU Count: {torch.cuda.device_count()}')"  # PyTorch uses cuda API for ROCm too

    echo ""
    echo -e "${BLUE}6. GPU Details${NC}"
    for i in $(seq 0 $(($(python -c "import torch; print(torch.cuda.device_count())") - 1))); do
        echo -e "GPU $i:"
        python -c "import torch; print(f'  Name: {torch.cuda.get_device_name($i)}')"
    done

    echo ""
    echo -e "${BLUE}7. Testing GPU Computation${NC}"
    python -c "
import torch
import time

device = torch.device('cuda:0')
print(f'Using device: {device}')

# Test basic operations
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)

start = time.time()
z = torch.matmul(x, y)
torch.cuda.synchronize()
end = time.time()

print(f'Matrix multiplication successful: {z.shape}')
print(f'Computation time: {(end-start)*1000:.2f} ms')
" && echo -e "${GREEN}✓ GPU computation successful${NC}" || echo -e "${RED}✗ GPU computation failed${NC}"

    # Show rocm-smi if available
    if command -v rocm-smi &> /dev/null; then
        echo ""
        echo -e "${BLUE}8. AMD GPU Status${NC}"
        rocm-smi
    fi

else
    echo -e "${YELLOW}⚠️  CPU-only PyTorch (No GPU backend detected)${NC}"

    echo ""
    echo -e "${BLUE}5. Testing CPU Computation${NC}"
    python -c "
import torch
import time

device = torch.device('cpu')
print(f'Using device: {device}')

# Test basic operations
x = torch.randn(1000, 1000, device=device)
y = torch.randn(1000, 1000, device=device)

start = time.time()
z = torch.matmul(x, y)
end = time.time()

print(f'Matrix multiplication successful: {z.shape}')
print(f'Computation time: {(end-start)*1000:.2f} ms')
" && echo -e "${GREEN}✓ CPU computation successful${NC}" || echo -e "${RED}✗ CPU computation failed${NC}"
fi

echo ""
echo -e "${BLUE}9. Installed Packages${NC}"
echo "Core ML packages:"
uv pip list | grep -E "torch|numpy|pandas|scikit|jupyter|matplotlib|tensorboard" || echo "Packages not found"

echo ""
echo -e "${GREEN}=== Validation Complete ===${NC}"

# Check for WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo ""
    echo -e "${BLUE}ℹ️  WSL2 Environment Detected${NC}"
    if [ "$CUDA_AVAILABLE" == "True" ]; then
        echo -e "${GREEN}✓ CUDA is working correctly in WSL2${NC}"
    fi
fi

echo ""

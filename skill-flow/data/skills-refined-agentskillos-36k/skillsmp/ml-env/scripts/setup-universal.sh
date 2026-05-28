#!/bin/bash
set -e

# Universal ML Environment Setup Script
# Supports: NVIDIA GPUs (CUDA), AMD GPUs (ROCm), CPU-only, WSL2

PYTHON_VERSION="3.13"
ENV_NAME="ml-env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_PATH="$SCRIPT_DIR/$ENV_NAME"
LOG_FILE="$SCRIPT_DIR/setup-$(date +%Y%m%d-%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging setup
exec > >(tee -a "$LOG_FILE") 2>&1

echo -e "${BLUE}=== Universal ML Environment Setup ===${NC}"
echo "Log file: $LOG_FILE"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed. Please install it first:${NC}"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✓ uv found: $(uv --version)${NC}"

# Detect platform
detect_platform() {
    if grep -qi microsoft /proc/version 2>/dev/null; then
        echo "wsl"
    else
        echo "linux"
    fi
}

# Detect GPU type
detect_gpu() {
    if command -v nvidia-smi &> /dev/null; then
        # Check if NVIDIA GPU is actually accessible
        if nvidia-smi &> /dev/null; then
            echo "nvidia"
            return 0
        fi
    fi

    if command -v rocm-smi &> /dev/null; then
        echo "amd"
        return 0
    fi

    # Check for AMD GPU via lspci
    if lspci 2>/dev/null | grep -i "VGA.*AMD" &> /dev/null; then
        echo "amd"
        return 0
    fi

    echo "cpu"
}

# Get NVIDIA GPU details
get_nvidia_info() {
    if ! command -v nvidia-smi &> /dev/null; then
        echo "none|0|0"
        return
    fi

    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n1 | xargs)
    COMPUTE_CAP=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader 2>/dev/null | head -n1 | xargs)

    # Extract major.minor from compute capability
    COMPUTE_MAJOR=$(echo "$COMPUTE_CAP" | cut -d. -f1)
    COMPUTE_MINOR=$(echo "$COMPUTE_CAP" | cut -d. -f2)

    # Return using pipe delimiter to handle spaces in GPU name
    echo "${GPU_NAME}|${COMPUTE_MAJOR}|${COMPUTE_MINOR}"
}

# Get AMD GPU details
get_amd_info() {
    # Try to detect AMD GPU architecture
    local gpu_name="Unknown AMD GPU"
    local gfx_arch=""

    if command -v rocminfo &> /dev/null; then
        GPU_INFO=$(rocminfo 2>/dev/null | grep -E "Marketing Name|Name:" | head -n2)
        gpu_name="$GPU_INFO"

        # Try to detect gfx architecture
        gfx_arch=$(rocminfo 2>/dev/null | grep -oP 'gfx\d+' | head -n1)
    elif lspci 2>/dev/null | grep -i "VGA.*AMD" &> /dev/null; then
        gpu_name=$(lspci 2>/dev/null | grep -i "VGA.*AMD" | head -n1)
    fi

    # Check for Strix Halo indicators
    if [[ "$gpu_name" =~ "Radeon 8060S" ]] || [[ "$gpu_name" =~ "Ryzen AI MAX" ]] || [[ "$gfx_arch" == "gfx1151" ]]; then
        echo "strix_halo" "$gfx_arch" "$gpu_name"
    else
        echo "other_amd" "$gfx_arch" "$gpu_name"
    fi
}

# Check user groups for AMD GPU access
check_amd_groups() {
    local missing_groups=()

    if ! groups | grep -q "render"; then
        missing_groups+=("render")
    fi

    if ! groups | grep -q "video"; then
        missing_groups+=("video")
    fi

    if [ ${#missing_groups[@]} -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Warning: User not in required groups: ${missing_groups[*]}${NC}"
        echo "To access AMD GPU, add yourself to these groups:"
        echo "  sudo usermod -aG render,video $USER"
        echo "  newgrp render  # Or logout and login again"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    return 0
}

# Determine PyTorch installation command
determine_pytorch_install() {
    local gpu_type=$1
    local compute_major=$2
    local compute_minor=$3
    local platform=$4

    # Default to stable PyTorch 2.10.0
    PYTORCH_VERSION="torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0"
    INDEX_URL=""

    case "$gpu_type" in
        nvidia)
            # Determine CUDA version based on compute capability
            local sm_version="${compute_major}${compute_minor}"

            echo -e "${YELLOW}Detected NVIDIA GPU with compute capability: sm_${sm_version}${NC}" >&2

            if [ "$compute_major" -ge 12 ]; then
                # Blackwell (RTX 5090, GB200) - sm_120+
                echo -e "${YELLOW}⚠️  Blackwell architecture detected (sm_120+)${NC}" >&2
                echo -e "${YELLOW}   PyTorch 2.10.0 has experimental support for this GPU${NC}" >&2
                echo "" >&2
                echo "Choose installation option:" >&2
                echo "  1) PyTorch 2.10.0 with CUDA 13.0 (experimental, may have issues)" >&2
                echo "  2) PyTorch nightly (recommended for cutting-edge GPUs)" >&2
                echo "  3) PyTorch 2.10.0 with CUDA 12.8 (stable, may fall back to PTX)" >&2
                read -p "Choice [1-3]: " choice

                case $choice in
                    1) INDEX_URL="https://download.pytorch.org/whl/cu130" ;;
                    2) PYTORCH_VERSION="torch torchvision torchaudio --pre"
                       INDEX_URL="https://download.pytorch.org/whl/nightly/cu128" ;;
                    *) INDEX_URL="https://download.pytorch.org/whl/cu128" ;;
                esac

            elif [ "$compute_major" -ge 9 ]; then
                # Ada Lovelace (RTX 4060) - sm_89
                echo -e "${GREEN}Ada Lovelace architecture detected - using CUDA 12.8${NC}" >&2
                INDEX_URL="https://download.pytorch.org/whl/cu128"

            elif [ "$compute_major" -ge 8 ]; then
                # Ampere (RTX 3090) - sm_86
                echo -e "${GREEN}Ampere architecture detected - using CUDA 12.8${NC}" >&2
                INDEX_URL="https://download.pytorch.org/whl/cu128"

            else
                # Older architectures
                echo -e "${YELLOW}Older GPU architecture detected - using CUDA 12.8${NC}" >&2
                INDEX_URL="https://download.pytorch.org/whl/cu128"
            fi

            if [ "$platform" == "wsl" ]; then
                echo -e "${BLUE}ℹ️  WSL2 detected - using Windows NVIDIA driver${NC}" >&2
                echo -e "${BLUE}   Do NOT install Linux NVIDIA drivers in WSL2!${NC}" >&2
            fi
            ;;

        amd)
            # Check user groups first
            if ! check_amd_groups; then
                exit 1
            fi

            # Parse AMD GPU info
            read AMD_TYPE GFX_ARCH AMD_NAME <<< "$3"

            echo -e "${YELLOW}AMD GPU detected: $AMD_NAME${NC}" >&2
            if [ -n "$GFX_ARCH" ]; then
                echo -e "${YELLOW}Architecture: $GFX_ARCH${NC}" >&2
            fi

            if [ "$AMD_TYPE" == "strix_halo" ]; then
                echo "" >&2
                echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}" >&2
                echo -e "${BLUE}║  Strix Halo (gfx1151) Detected                                 ║${NC}" >&2
                echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}" >&2
                echo "" >&2
                echo -e "${YELLOW}⚠️  Official PyTorch wheels DO NOT work with gfx1151${NC}" >&2
                echo -e "${YELLOW}   Must use AMD community nightlies or stable gfx1151 builds${NC}" >&2
                echo "" >&2
                echo "Choose ROCm installation option:" >&2
                echo "" >&2
                echo "  ${GREEN}1) ROCm 6.4.4+ Nightlies (RECOMMENDED - Stable)${NC}" >&2
                echo "     Index: https://rocm.nightlies.amd.com/v2/gfx1151/" >&2
                echo "     Status: Works well, tested by community" >&2
                echo "" >&2
                echo "  ${YELLOW}2) ROCm 7.9 Stable gfx1151 Build (NEWEST)${NC}" >&2
                echo "     Index: https://repo.amd.com/rocm/whl/gfx1151/" >&2
                echo "     Status: Official stable release for gfx1151" >&2
                echo "" >&2
                echo "  ${BLUE}3) ROCm 7.0.2+ Nightlies (EXPERIMENTAL)${NC}" >&2
                echo "     Index: https://rocm.nightlies.amd.com/v2/gfx1151/" >&2
                echo "     Status: Latest features, may be unstable" >&2
                echo "" >&2
                echo "  ${RED}4) CPU-only (Safe fallback)${NC}" >&2
                echo "     No GPU acceleration" >&2
                echo "" >&2
                read -p "Choice [1-4]: " choice

                case $choice in
                    1)
                        echo -e "${GREEN}Installing PyTorch with ROCm 6.4.4+ nightlies${NC}" >&2
                        PYTORCH_VERSION="--pre torch torchvision torchaudio"
                        INDEX_URL="https://rocm.nightlies.amd.com/v2/gfx1151/"
                        ;;
                    2)
                        echo -e "${GREEN}Installing PyTorch with ROCm 7.9 stable gfx1151${NC}" >&2
                        PYTORCH_VERSION="torch torchvision torchaudio"
                        INDEX_URL="https://repo.amd.com/rocm/whl/gfx1151/"
                        ;;
                    3)
                        echo -e "${YELLOW}Installing PyTorch with ROCm 7.0.2+ nightlies (experimental)${NC}" >&2
                        PYTORCH_VERSION="--pre torch torchvision torchaudio"
                        INDEX_URL="https://rocm.nightlies.amd.com/v2/gfx1151/"
                        ;;
                    *)
                        echo -e "${BLUE}Installing CPU-only PyTorch${NC}" >&2
                        PYTORCH_VERSION="torch torchvision torchaudio"
                        INDEX_URL="https://download.pytorch.org/whl/cpu"
                        ;;
                esac

                echo "" >&2
                echo -e "${BLUE}ℹ️  Note: For large models (30B+), configure GTT memory${NC}" >&2
                echo -e "${BLUE}   See: https://github.com/ianbarber/strix-halo-skills${NC}" >&2

            else
                # Other AMD GPUs (RDNA 2/3)
                echo -e "${YELLOW}Standard AMD GPU detected${NC}" >&2
                echo "" >&2
                echo "Choose installation option:" >&2
                echo "  1) PyTorch with ROCm 6.2 (stable)" >&2
                echo "  2) CPU-only PyTorch" >&2
                read -p "Choice [1-2]: " choice

                case $choice in
                    1) PYTORCH_VERSION="torch torchvision torchaudio"
                       INDEX_URL="https://download.pytorch.org/whl/rocm6.2" ;;
                    *) PYTORCH_VERSION="torch torchvision torchaudio"
                       INDEX_URL="https://download.pytorch.org/whl/cpu" ;;
                esac
            fi
            ;;

        cpu)
            echo -e "${BLUE}No GPU detected - installing CPU-only PyTorch${NC}" >&2
            PYTORCH_VERSION="torch torchvision torchaudio"
            INDEX_URL="https://download.pytorch.org/whl/cpu"
            ;;
    esac

    # Return using pipe delimiter to handle spaces in package names
    echo "${PYTORCH_VERSION}|${INDEX_URL}"
}

# Main detection
echo ""
echo -e "${BLUE}Detecting system configuration...${NC}"
echo ""

PLATFORM=$(detect_platform)
GPU_TYPE=$(detect_gpu)

echo -e "Platform: ${GREEN}$PLATFORM${NC}"
echo -e "GPU Type: ${GREEN}$GPU_TYPE${NC}"

if [ "$GPU_TYPE" == "nvidia" ]; then
    IFS='|' read -r GPU_NAME COMPUTE_MAJOR COMPUTE_MINOR <<< "$(get_nvidia_info)"
    echo -e "GPU: ${GREEN}$GPU_NAME${NC}"
    echo -e "Compute Capability: ${GREEN}$COMPUTE_MAJOR.$COMPUTE_MINOR${NC}"

    # Show full GPU info
    echo ""
    echo "NVIDIA GPU Information:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv

elif [ "$GPU_TYPE" == "amd" ]; then
    read AMD_TYPE GFX_ARCH AMD_NAME <<< $(get_amd_info)
    echo -e "GPU Type: ${GREEN}$AMD_TYPE${NC}"
    if [ -n "$GFX_ARCH" ]; then
        echo -e "Architecture: ${GREEN}$GFX_ARCH${NC}"
    fi
    echo -e "GPU: ${GREEN}$AMD_NAME${NC}"

    # Show ROCm info if available
    if command -v rocminfo &> /dev/null; then
        echo ""
        echo "ROCm GPU Information:"
        rocminfo 2>/dev/null | grep -E "Marketing Name|Name:|gfx" | head -n5 || echo "ROCm info not available"
    fi

    AMD_INFO="$AMD_TYPE $GFX_ARCH $AMD_NAME"
    COMPUTE_MAJOR=0
    COMPUTE_MINOR=0
else
    GPU_NAME="None"
    AMD_INFO=""
    COMPUTE_MAJOR=0
    COMPUTE_MINOR=0
fi

echo ""
echo -e "${BLUE}Creating Python $PYTHON_VERSION virtual environment...${NC}"

# Check if Python version is available
if ! uv python list | grep -q "$PYTHON_VERSION"; then
    echo -e "${YELLOW}⚠️  Python $PYTHON_VERSION may not be available via uv${NC}"
    echo "Available Python versions:"
    uv python list | head -n 10
    echo ""
    read -p "Continue with Python $PYTHON_VERSION anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
uv venv "$ENV_PATH" --python "$PYTHON_VERSION"

if [ ! -d "$ENV_PATH" ]; then
    echo -e "${RED}Error: Failed to create virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"

# Create conda-safe activation wrapper
cat > "$ENV_PATH/activate-safe.sh" << 'ACTIVATE_WRAPPER'
#!/bin/bash
# Conda-safe activation wrapper
# This script ensures conda doesn't interfere with the virtual environment

# Store original conda settings
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "Note: Conda environment '$CONDA_DEFAULT_ENV' will be overridden"
fi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Clear conda environment variables that interfere
unset CONDA_DEFAULT_ENV
unset CONDA_PREFIX
unset CONDA_PYTHON_EXE
unset CONDA_PROMPT_MODIFIER

# Source the standard activate script
source "$SCRIPT_DIR/bin/activate"

# Force the venv bin directory to be first in PATH
# This ensures venv Python takes precedence over conda
export PATH="$SCRIPT_DIR/bin:$PATH"

# Verify we're using the right Python
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
PYTHON_PATH=$(which python)

echo "✓ ML environment activated"
echo "  Python: $PYTHON_VERSION"
echo "  Location: $PYTHON_PATH"
ACTIVATE_WRAPPER

chmod +x "$ENV_PATH/activate-safe.sh"
echo -e "${BLUE}ℹ️  Created conda-safe activation wrapper${NC}"

# Determine PyTorch installation
echo ""
if [ "$GPU_TYPE" == "amd" ]; then
    IFS='|' read -r PYTORCH_CMD INDEX_URL <<< "$(determine_pytorch_install "$GPU_TYPE" "$COMPUTE_MAJOR" "$AMD_INFO" "$PLATFORM")"
else
    IFS='|' read -r PYTORCH_CMD INDEX_URL <<< "$(determine_pytorch_install "$GPU_TYPE" "$COMPUTE_MAJOR" "$COMPUTE_MINOR" "$PLATFORM")"
fi

echo ""
echo -e "${BLUE}Installing PyTorch...${NC}"
echo "Command: uv pip install $PYTORCH_CMD"
if [ -n "$INDEX_URL" ]; then
    echo "Index URL: $INDEX_URL"
    uv pip install --python "$ENV_PATH/bin/python" $PYTORCH_CMD --index-url "$INDEX_URL"
else
    uv pip install --python "$ENV_PATH/bin/python" $PYTORCH_CMD
fi

echo ""
echo -e "${BLUE}Installing additional ML libraries...${NC}"

uv pip install --python "$ENV_PATH/bin/python" \
    "numpy>=1.26.0,<2.0.0" \
    "pandas>=2.0.0" \
    "matplotlib>=3.8.0" \
    "scikit-learn>=1.4.0" \
    "jupyter>=1.0.0" \
    "ipython>=8.20.0" \
    "tqdm>=4.66.0" \
    "tensorboard>=2.16.0"

echo ""
echo -e "${BLUE}Saving installed packages...${NC}"
uv pip freeze --python "$ENV_PATH/bin/python" > "$ENV_PATH/requirements-installed.txt"
echo -e "${GREEN}✓ Package list saved to $ENV_PATH/requirements-installed.txt${NC}"

echo ""
echo -e "${GREEN}=== Installation Complete ===${NC}"
echo ""
echo -e "Environment location: ${BLUE}$ENV_PATH${NC}"
echo ""
echo "To activate this environment:"
echo -e "  ${GREEN}If you use conda:${NC} ${BLUE}source $ENV_PATH/activate-safe.sh${NC}"
echo -e "  ${GREEN}Otherwise:${NC}      ${BLUE}source $ENV_PATH/bin/activate${NC}"
echo ""
echo "To verify installation, run:"
echo -e "  ${BLUE}$SCRIPT_DIR/validate.sh${NC}"
echo ""
echo -e "Configuration detected:"
echo "  Platform: $PLATFORM"
echo "  GPU: $GPU_TYPE"
if [ "$GPU_TYPE" == "nvidia" ]; then
    echo "  GPU Name: $GPU_NAME"
    echo "  Compute Capability: $COMPUTE_MAJOR.$COMPUTE_MINOR"
fi
echo ""
echo -e "${YELLOW}⚠️  Remember to activate the environment before using PyTorch!${NC}"
echo ""
echo -e "${BLUE}ℹ️  An ML environment skill has been created at .claude/skills/ml-env/${NC}"
echo "   Claude Code will automatically use this skill when you ask about the environment"
echo ""

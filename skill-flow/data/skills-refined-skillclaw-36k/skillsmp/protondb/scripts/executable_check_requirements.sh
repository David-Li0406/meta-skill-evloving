#!/bin/bash
# Check game requirements against system hardware

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <steam_app_id>"
    echo ""
    echo "Examples:"
    echo "  $0 1285190              # Check Borderlands 4 requirements"
    echo "  $0 1245620              # Check Elden Ring requirements"
    exit 1
fi

APP_ID="$1"

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed"
    echo "Install with: sudo pacman -S jq"
    exit 1
fi

echo "System Requirements Check"
echo "========================="
echo ""

# Get system information
echo "Your System"
echo "-----------"

# CPU
CPU_MODEL=$(lscpu | grep "Model name:" | sed 's/Model name:\s*//' | xargs)
CPU_CORES=$(nproc)
echo "CPU: $CPU_MODEL"
echo "Cores: $CPU_CORES"

# GPU
GPU_INFO=$(lspci | grep -i vga | head -n1 | cut -d: -f3 | xargs)
echo "GPU: $GPU_INFO"

# VRAM (for AMD GPUs)
if command -v radeontop &> /dev/null 2>&1; then
    VRAM=$(radeontop -d - -l 1 2>/dev/null | grep -o "vram [0-9]*mb" | grep -o "[0-9]*" || echo "Unknown")
    if [ "$VRAM" != "Unknown" ]; then
        echo "VRAM: ${VRAM}MB"
    fi
else
    # Try alternative method via sysfs
    if [ -f /sys/class/drm/card0/device/mem_info_vram_total ]; then
        VRAM_BYTES=$(cat /sys/class/drm/card0/device/mem_info_vram_total)
        VRAM_MB=$((VRAM_BYTES / 1024 / 1024))
        echo "VRAM: ${VRAM_MB}MB"
    else
        echo "VRAM: Unable to detect (install radeontop for detection)"
    fi
fi

# RAM
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo "RAM: ${RAM_GB}GB"

# Storage (available space in home)
STORAGE=$(df -h ~ | awk 'NR==2 {print $4}')
echo "Available Storage: $STORAGE"

# Mesa version
MESA_VERSION=$(glxinfo 2>/dev/null | grep "OpenGL version" | cut -d: -f2 | xargs | cut -d' ' -f1-2 || echo "Unknown")
echo "Mesa Version: $MESA_VERSION"

# Kernel version
KERNEL_VERSION=$(uname -r)
echo "Kernel: $KERNEL_VERSION"

echo ""
echo "Fetching game requirements..."
echo ""

# Fetch Steam game data
RESPONSE=$(curl -s "https://www.protondb.com/proxy/steam/api/appdetails/?appids=${APP_ID}")
SUCCESS=$(echo "$RESPONSE" | jq -r ".[\"$APP_ID\"].success")

if [ "$SUCCESS" != "true" ]; then
    echo "Error: Could not fetch Steam data for App ID $APP_ID"
    exit 1
fi

DATA=$(echo "$RESPONSE" | jq ".[\"$APP_ID\"].data")
NAME=$(echo "$DATA" | jq -r '.name // "Unknown"')

echo "Game: $NAME"
echo "========================================="
echo ""

# Get Windows requirements (baseline for Linux)
MIN_REQ=$(echo "$DATA" | jq -r '.pc_requirements.minimum // "Not specified"')
REC_REQ=$(echo "$DATA" | jq -r '.pc_requirements.recommended // "Not specified"')

# Parse minimum requirements
echo "Minimum Requirements (Windows Baseline)"
echo "----------------------------------------"
if [ "$MIN_REQ" != "Not specified" ] && [ "$MIN_REQ" != "null" ]; then
    echo "$MIN_REQ" | sed 's/<[^>]*>//g' | sed 's/&quot;/"/g' | sed 's/&amp;/\&/g'
else
    echo "Not specified by developer"
fi

echo ""

# Parse recommended requirements
echo "Recommended Requirements (Windows Baseline)"
echo "--------------------------------------------"
if [ "$REC_REQ" != "Not specified" ] && [ "$REC_REQ" != "null" ]; then
    echo "$REC_REQ" | sed 's/<[^>]*>//g' | sed 's/&quot;/"/g' | sed 's/&amp;/\&/g'
else
    echo "Not specified by developer"
fi

echo ""
echo "Linux Considerations"
echo "--------------------"
echo "When running via Proton, consider:"
echo ""
echo "CPU:"
echo "  - Add ~5-10% overhead for Proton translation"
echo "  - AMD Ryzen 5000+ series recommended for modern games"
echo "  - Older CPUs may struggle with demanding titles"
echo ""
echo "GPU:"
echo "  - VRAM requirements same or +1-2GB for DirectX 12 games"
echo "  - RX 6000/7000 series for ray tracing"
echo "  - Shader compilation causes initial stutter (normal)"
echo ""
echo "RAM:"
echo "  - Add 2-4GB to Windows requirements"
echo "  - 16GB recommended minimum for modern gaming"
echo "  - 32GB for heavy multitasking while gaming"
echo ""
echo "Storage:"
echo "  - SSD strongly recommended (NVMe preferred)"
echo "  - Game size + ~5-10GB for shader cache"
echo "  - BTRFS/ext4 filesystems work well"
echo ""

# Try to give a basic assessment
echo "Quick Assessment"
echo "----------------"

# Very basic CPU check (just core count)
if [ "$CPU_CORES" -ge 8 ]; then
    echo "CPU: ✓ Good core count for modern games"
elif [ "$CPU_CORES" -ge 4 ]; then
    echo "CPU: ~ Adequate for most games"
else
    echo "CPU: ⚠ May struggle with demanding games"
fi

# RAM check
if [ "$RAM_GB" -ge 32 ]; then
    echo "RAM: ✓ Excellent for gaming + multitasking"
elif [ "$RAM_GB" -ge 16 ]; then
    echo "RAM: ✓ Good for modern gaming"
elif [ "$RAM_GB" -ge 8 ]; then
    echo "RAM: ~ Minimum for current games"
else
    echo "RAM: ⚠ Below recommended for modern games"
fi

# Check for AMD GPU
if echo "$GPU_INFO" | grep -iq "AMD\|Radeon"; then
    if echo "$GPU_INFO" | grep -iq "RX 7[0-9][0-9][0-9]"; then
        echo "GPU: ✓ Excellent (RDNA 3, latest generation)"
    elif echo "$GPU_INFO" | grep -iq "RX 6[0-9][0-9][0-9]"; then
        echo "GPU: ✓ Very good (RDNA 2, ray tracing capable)"
    elif echo "$GPU_INFO" | grep -iq "RX 5[0-9][0-9][0-9]"; then
        echo "GPU: ✓ Good (RDNA 1, no ray tracing)"
    else
        echo "GPU: ~ Verify game compatibility for your specific model"
    fi
else
    echo "GPU: Detected as non-AMD, this guide optimized for AMD GPUs"
fi

echo ""
echo "Performance Tips"
echo "----------------"
echo "- Use GameMode for CPU optimization:"
echo "    gamemoderun %command%"
echo ""
echo "- Monitor performance with MangoHud:"
echo "    mangohud %command%"
echo ""
echo "- First launch will stutter (shader compilation)"
echo "  Use DXVK_ASYNC=1 to reduce stutter"
echo ""
echo "- Check ProtonDB for game-specific optimizations:"
echo "    https://www.protondb.com/app/$APP_ID"
echo ""
echo "Generate launch options:"
echo "  scripts/generate_launch_options.sh default"

#!/bin/bash
# Strix Halo System Verification Script
# Checks all prerequisites and system configuration

# Not using 'set -e' to allow all checks to run even if some fail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS="${GREEN}✓${NC}"
FAIL="${RED}✗${NC}"
WARN="${YELLOW}⚠${NC}"

echo ""
echo "============================================================"
echo "  AMD Strix Halo System Verification"
echo "============================================================"
echo ""

ISSUES=0
WARNINGS=0

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print result
print_result() {
    local status=$1
    local message=$2
    if [ "$status" = "PASS" ]; then
        echo -e "${PASS} ${message}"
    elif [ "$status" = "FAIL" ]; then
        echo -e "${FAIL} ${message}"
        ((ISSUES++))
    else
        echo -e "${WARN} ${message}"
        ((WARNINGS++))
    fi
}

# 1. Check Hardware
echo -e "${BLUE}[1/8] Checking Hardware...${NC}"
if lspci | grep -qi "AMD.*VGA\|AMD.*Display"; then
    GPU_NAME=$(lspci | grep -i "AMD.*VGA\|AMD.*Display" | head -1 | cut -d: -f3)
    print_result "PASS" "AMD GPU detected:$GPU_NAME"
else
    print_result "FAIL" "AMD GPU not detected"
fi
echo ""

# 2. Check ROCm Installation
echo -e "${BLUE}[2/8] Checking ROCm Installation...${NC}"
if command_exists rocm-smi; then
    ROCM_VERSION=$(rocm-smi --version 2>/dev/null | grep "ROCm version" | awk '{print $3}' || echo "unknown")
    print_result "PASS" "ROCm installed: $ROCM_VERSION"

    # Check if GPU visible to ROCm
    if rocm-smi 2>/dev/null | grep -q "gfx1151"; then
        print_result "PASS" "GPU visible to ROCm (gfx1151)"
    else
        print_result "WARN" "GPU may not be visible to ROCm"
    fi
else
    print_result "FAIL" "ROCm not installed (rocm-smi not found)"
    echo "      Install ROCm 7.2: See https://rocm.docs.amd.com/projects/install-on-linux/en/latest/"
    echo "      Or ROCm 6.4.4:    wget https://repo.radeon.com/amdgpu-install/6.4.4/ubuntu/noble/amdgpu-install_6.4.60402-1_all.deb"
    echo "                        sudo apt install ./amdgpu-install_6.4.60402-1_all.deb"
    echo "                        sudo amdgpu-install --usecase=rocm --no-dkms"
fi
echo ""

# 3. Check User Groups
echo -e "${BLUE}[3/8] Checking User Groups...${NC}"
if groups | grep -q "render"; then
    print_result "PASS" "User in 'render' group"
else
    print_result "FAIL" "User NOT in 'render' group"
    echo "      Fix: sudo usermod -aG render,video \$USER"
    echo "           Then log out and back in"
fi

if groups | grep -q "video"; then
    print_result "PASS" "User in 'video' group"
else
    print_result "FAIL" "User NOT in 'video' group"
    echo "      Fix: sudo usermod -aG render,video \$USER"
    echo "           Then log out and back in"
fi
echo ""

# 4. Check GTT Configuration
echo -e "${BLUE}[4/8] Checking GTT Memory Configuration...${NC}"

# Check kernel version first
KERNEL_VERSION=$(uname -r)
KERNEL_MAJOR=$(echo $KERNEL_VERSION | cut -d. -f1)
KERNEL_MINOR=$(echo $KERNEL_VERSION | cut -d. -f2)
KERNEL_PATCH=$(echo $KERNEL_VERSION | cut -d. -f3 | cut -d- -f1)

# Check if kernel 6.16.9+
if [ "$KERNEL_MAJOR" -gt 6 ] || \
   ([ "$KERNEL_MAJOR" -eq 6 ] && [ "$KERNEL_MINOR" -gt 16 ]) || \
   ([ "$KERNEL_MAJOR" -eq 6 ] && [ "$KERNEL_MINOR" -eq 16 ] && [ "$KERNEL_PATCH" -ge 9 ]); then
    print_result "PASS" "Kernel $KERNEL_VERSION has automatic UMA support (no GTT config needed)"
elif grep -q "amdttm.pages_limit" /proc/cmdline; then
    GTT_PARAM=$(grep -oP 'amdttm.pages_limit=\K[0-9]+' /proc/cmdline)
    GTT_GB=$((GTT_PARAM * 4096 / 1024 / 1024 / 1024))
    print_result "PASS" "GTT configured in kernel: ${GTT_GB}GB (pages_limit=$GTT_PARAM)"
else
    print_result "WARN" "GTT not configured (limited to ~33GB)"
    echo "      Option 1: Upgrade to kernel 6.16.9+ (automatic)"
    echo "      Option 2: Configure GTT: ./configure_gtt.sh"
fi

# Check actual GTT size (find correct card dynamically)
GTT_FILE=$(find /sys/class/drm/card*/device/mem_info_gtt_total 2>/dev/null | head -1)
if [ -n "$GTT_FILE" ]; then
    GTT_BYTES=$(cat "$GTT_FILE")
    GTT_ACTUAL_GB=$((GTT_BYTES / 1024 / 1024 / 1024))
    if [ $GTT_ACTUAL_GB -gt 100 ]; then
        print_result "PASS" "GTT memory available: ${GTT_ACTUAL_GB}GB"
    elif [ $GTT_ACTUAL_GB -gt 30 ]; then
        print_result "PASS" "GTT memory available: ${GTT_ACTUAL_GB}GB (good for 13B models)"
    else
        print_result "WARN" "GTT memory limited: ${GTT_ACTUAL_GB}GB (only 7B models)"
    fi
fi
echo ""

# 5. Check Python and Conda
echo -e "${BLUE}[5/8] Checking Python Environment...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_result "PASS" "Python3 installed: $PYTHON_VERSION"
else
    print_result "FAIL" "Python3 not found"
fi

if command_exists conda; then
    CONDA_VERSION=$(conda --version | awk '{print $2}')
    print_result "PASS" "Conda installed: $CONDA_VERSION"
else
    print_result "WARN" "Conda not found (recommended for environment management)"
fi
echo ""

# 6. Check PyTorch
echo -e "${BLUE}[6/8] Checking PyTorch Installation...${NC}"
if python3 -c "import torch" 2>/dev/null; then
    PYTORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null)
    print_result "PASS" "PyTorch installed: $PYTORCH_VERSION"

    # Check if it has HIP support
    if python3 -c "import torch; exit(0 if hasattr(torch.version, 'hip') else 1)" 2>/dev/null; then
        HIP_VERSION=$(python3 -c "import torch; print(torch.version.hip)" 2>/dev/null)
        print_result "PASS" "PyTorch has ROCm/HIP support: $HIP_VERSION"
    else
        print_result "FAIL" "PyTorch does NOT have ROCm/HIP support"
        echo "      Install: pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch"
    fi
else
    print_result "FAIL" "PyTorch not installed"
    echo "      Install: pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch"
fi
echo ""

# 7. Check GPU Detection in PyTorch
echo -e "${BLUE}[7/8] Checking PyTorch GPU Detection...${NC}"
if python3 -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    GPU_NAME=$(python3 -c "import torch; print(torch.cuda.get_device_name(0))" 2>/dev/null)
    print_result "PASS" "PyTorch detects GPU: $GPU_NAME"

    # Check available memory
    GPU_MEM=$(python3 -c "import torch; props = torch.cuda.get_device_properties(0); print(f'{props.total_memory / 1e9:.1f}')" 2>/dev/null)
    if (( $(echo "$GPU_MEM > 100" | bc -l) )); then
        print_result "PASS" "GPU memory: ${GPU_MEM}GB (excellent for 30B models)"
    elif (( $(echo "$GPU_MEM > 30" | bc -l) )); then
        print_result "PASS" "GPU memory: ${GPU_MEM}GB (good for 13B models)"
    else
        print_result "WARN" "GPU memory: ${GPU_MEM}GB (limited, configure GTT)"
    fi
else
    print_result "FAIL" "PyTorch does NOT detect GPU"
    echo "      Troubleshoot:"
    echo "      1. Check groups: groups | grep -E 'render|video'"
    echo "      2. Check ROCm: rocm-smi"
    echo "      3. Check PyTorch version: python3 -c 'import torch; print(torch.__version__)'"
fi
echo ""

# 8. Check Compute
echo -e "${BLUE}[8/8] Checking GPU Compute...${NC}"
COMPUTE_TEST=$(python3 << 'EOF' 2>&1
import torch
import sys
try:
    if not torch.cuda.is_available():
        print("SKIP: GPU not detected")
        sys.exit(2)

    # Test allocation
    a = torch.tensor([1.0, 2.0, 3.0]).cuda()

    # Test compute
    b = a + 1
    result = b.cpu().tolist()

    if result == [2.0, 3.0, 4.0]:
        print("PASS")
    else:
        print("FAIL: Incorrect result")
        sys.exit(1)
except RuntimeError as e:
    if "invalid device function" in str(e):
        print("FAIL: HIP error - using official PyTorch wheels (don't work with gfx1151)")
        print("      Install community wheels: pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch")
        sys.exit(1)
    else:
        print(f"FAIL: {e}")
        sys.exit(1)
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)
EOF
)

COMPUTE_EXIT=$?
if [ $COMPUTE_EXIT -eq 0 ]; then
    print_result "PASS" "GPU compute successful (simple tensor operations work)"
elif [ $COMPUTE_EXIT -eq 2 ]; then
    print_result "WARN" "Compute test skipped (GPU not detected)"
else
    print_result "FAIL" "GPU compute failed"
    echo "$COMPUTE_TEST" | while IFS= read -r line; do
        echo "      $line"
    done
fi
echo ""

# Summary
echo "============================================================"
echo "  Summary"
echo "============================================================"
echo ""

if [ $ISSUES -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ PERFECT!${NC} Your system is fully configured for Strix Halo ML workloads."
    echo ""
    echo "You can run:"
    echo "  - 7B models in FP16 (~14GB)"
    echo "  - 13B models in FP16 (~26GB)"
    if [ -n "$GPU_MEM" ] && (( $(echo "$GPU_MEM > 100" | bc -l) )); then
        echo "  - 30B models in FP16 (~60GB)"
    fi
    echo ""
    echo "Next steps:"
    echo "  1. Run: python scripts/test_gpu_simple.py"
    echo "  2. Try: ./setup_new_project.sh"
    echo "  3. Or use Claude Code skill: @strix-halo-setup"
elif [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ GOOD!${NC} System is working with ${WARNINGS} warning(s)."
    echo ""
    echo "Your system will work, but consider addressing the warnings above"
    echo "for optimal performance (especially GTT configuration for 30B models)."
elif [ $ISSUES -eq 1 ]; then
    echo -e "${RED}✗ ISSUES FOUND${NC}: ${ISSUES} critical issue needs fixing."
    echo ""
    echo "Fix the issue(s) marked with ✗ above, then run this script again."
else
    echo -e "${RED}✗ ISSUES FOUND${NC}: ${ISSUES} critical issues need fixing."
    echo ""
    echo "Fix the issue(s) marked with ✗ above, then run this script again."
fi

if [ $ISSUES -gt 0 ]; then
    echo ""
    echo "Common fixes:"
    echo "  - User groups: sudo usermod -aG render,video \$USER (then reboot)"
    echo "  - ROCm install: See STRIX_HALO_COMPLETE_GUIDE.md"
    echo "  - PyTorch: pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch"
    echo "  - GTT config: ./configure_gtt.sh"
fi

echo ""
echo "For detailed help, see: STRIX_HALO_COMPLETE_GUIDE.md"
echo ""

# Exit with appropriate code
if [ $ISSUES -gt 0 ]; then
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    exit 2
else
    exit 0
fi

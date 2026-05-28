#!/bin/sh
# Quick environment check for THOR troubleshooting
# Run from THOR installation directory

echo "=== THOR Environment Check ==="
echo ""

echo "--- System Info ---"
echo "System: $(uname -a)"
echo "User: $(whoami)"
echo "Directory: $(pwd)"
echo ""

echo "--- Resources ---"
if command -v free >/dev/null 2>&1; then
    echo "Memory:"
    free -h 2>/dev/null || free
fi
echo ""

echo "Disk space:"
df -h . 2>/dev/null || df .
echo ""

if command -v nproc >/dev/null 2>&1; then
    echo "CPU cores: $(nproc)"
elif command -v sysctl >/dev/null 2>&1; then
    echo "CPU cores: $(sysctl -n hw.ncpu 2>/dev/null || echo 'unknown')"
fi
echo ""

echo "--- THOR Files ---"
echo "Binaries found:"
for bin in thor64.exe thor.exe thor-linux-64 thor-linux thor-macosx thor-util thor-util.exe; do
    if [ -f "$bin" ]; then
        echo "  [OK] $bin"
    fi
done
echo ""

echo "License files:"
lic_count=$(find . -maxdepth 2 -name "*.lic" 2>/dev/null | wc -l)
if [ "$lic_count" -gt 0 ]; then
    find . -maxdepth 2 -name "*.lic" 2>/dev/null | while read -r f; do
        echo "  [OK] $f"
    done
else
    echo "  [WARN] No .lic files found in current directory"
fi
echo ""

echo "Config directory:"
if [ -d "./config" ]; then
    echo "  [OK] ./config exists"
    ls -la ./config/ 2>/dev/null | head -10
else
    echo "  [WARN] ./config not found"
fi
echo ""

echo "Signatures directory:"
if [ -d "./signatures" ]; then
    sig_count=$(find ./signatures -type f 2>/dev/null | wc -l)
    echo "  [OK] ./signatures exists ($sig_count files)"
else
    echo "  [WARN] ./signatures not found"
fi
echo ""

echo "Custom signatures:"
if [ -d "./custom-signatures" ]; then
    custom_count=$(find ./custom-signatures -type f 2>/dev/null | wc -l)
    echo "  [OK] ./custom-signatures exists ($custom_count files)"
else
    echo "  [INFO] ./custom-signatures not found (optional)"
fi
echo ""

echo "--- Running THOR Processes ---"
if command -v pgrep >/dev/null 2>&1; then
    thor_pids=$(pgrep -f "thor" 2>/dev/null)
    if [ -n "$thor_pids" ]; then
        ps aux | grep -E "thor" | grep -v grep
    else
        echo "  No THOR processes running"
    fi
else
    ps aux 2>/dev/null | grep -E "thor" | grep -v grep || echo "  Could not check processes"
fi
echo ""

echo "--- Permissions Check ---"
if [ "$(id -u)" -eq 0 ]; then
    echo "  [OK] Running as root"
else
    echo "  [WARN] Not running as root - some scans may have limited access"
fi
echo ""

echo "=== End Check ==="

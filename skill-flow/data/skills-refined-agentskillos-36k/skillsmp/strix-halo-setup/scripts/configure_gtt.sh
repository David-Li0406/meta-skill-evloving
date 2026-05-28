#!/bin/bash

# Script to configure GTT size for AMD Strix Halo on Ubuntu
# Allows GPU to access more than 33.5GB of system memory

echo "AMD Strix Halo GTT Configuration Script"
echo "========================================"
echo ""

# Check kernel version
KERNEL_VERSION=$(uname -r)
KERNEL_MAJOR=$(echo $KERNEL_VERSION | cut -d. -f1)
KERNEL_MINOR=$(echo $KERNEL_VERSION | cut -d. -f2)
KERNEL_PATCH=$(echo $KERNEL_VERSION | cut -d. -f3 | cut -d- -f1)

echo "Current kernel: $KERNEL_VERSION"
echo ""

# Check if kernel 6.16.9+
if [ "$KERNEL_MAJOR" -gt 6 ] || \
   ([ "$KERNEL_MAJOR" -eq 6 ] && [ "$KERNEL_MINOR" -gt 16 ]) || \
   ([ "$KERNEL_MAJOR" -eq 6 ] && [ "$KERNEL_MINOR" -eq 16 ] && [ "$KERNEL_PATCH" -ge 9 ]); then
    echo "✓ Kernel 6.16.9+ detected!"
    echo ""
    echo "Good news: This kernel has automatic UMA (Unified Memory Architecture) support."
    echo "You DON'T need to configure GTT parameters manually."
    echo ""
    echo "Your GPU should automatically have access to all system memory."
    echo ""
    echo "Verify with: python3 -c \"import torch; print(torch.cuda.get_device_properties(0).total_memory / 1e9, 'GB')\""
    echo ""
    exit 0
fi

echo "Kernel 6.16.8 or earlier detected - manual GTT configuration needed."
echo ""
echo "Note: Consider upgrading to kernel 6.16.9+ for automatic configuration."
echo ""

# Check current GTT size (find card dynamically)
echo "Current GTT size:"
GTT_FILE=$(find /sys/class/drm/card*/device/mem_info_gtt_total 2>/dev/null | head -1)
if [ -n "$GTT_FILE" ]; then
    current_gtt=$(cat "$GTT_FILE")
    echo "  $(($current_gtt / 1024 / 1024 / 1024)) GB"
else
    echo "  Unable to detect"
fi

echo ""
echo "This script will configure GTT to allow up to 108GB GPU-accessible memory."
echo ""

# Calculate TTM parameters for 108GB
# Formula: (GB * 1024 * 1024) / 4.096
TTM_PAGES=27648000  # For 108GB

echo "Step 1: Backup current GRUB configuration"
echo "  sudo cp /etc/default/grub /etc/default/grub.backup"
echo ""

echo "Step 2: Add kernel parameters"
echo "  Edit /etc/default/grub and add to GRUB_CMDLINE_LINUX_DEFAULT:"
echo ""
echo "  amdttm.pages_limit=$TTM_PAGES amdttm.page_pool_size=$TTM_PAGES"
echo ""

echo "Full line example:"
echo '  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amdttm.pages_limit=27648000 amdttm.page_pool_size=27648000"'
echo ""

echo "Step 3: Update GRUB and reboot"
echo "  sudo update-grub"
echo "  sudo reboot"
echo ""

echo "Alternative TTM values:"
echo "  64GB:  pages_limit=16777216"
echo "  96GB:  pages_limit=25165824"
echo "  108GB: pages_limit=27648000 (recommended maximum)"
echo ""

# Offer to do it automatically
read -p "Would you like to apply these changes automatically? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup
    sudo cp /etc/default/grub /etc/default/grub.backup.$(date +%Y%m%d_%H%M%S)
    
    # Check if parameters already exist
    if grep -q "amdttm.pages_limit" /etc/default/grub; then
        echo "TTM parameters already set in GRUB. Current configuration:"
        grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
        echo ""
        echo "To modify, manually edit /etc/default/grub"
    else
        # Add parameters
        sudo sed -i.bak 's/GRUB_CMDLINE_LINUX_DEFAULT="\(.*\)"/GRUB_CMDLINE_LINUX_DEFAULT="\1 amdttm.pages_limit=27648000 amdttm.page_pool_size=27648000"/' /etc/default/grub
        
        echo "Modified /etc/default/grub:"
        grep "GRUB_CMDLINE_LINUX_DEFAULT" /etc/default/grub
        echo ""
        
        echo "Updating GRUB..."
        sudo update-grub
        
        echo ""
        echo "✓ Configuration complete!"
        echo ""
        echo "IMPORTANT: You must reboot for changes to take effect."
        echo "After reboot, run: python test_memory.py"
    fi
else
    echo ""
    echo "Manual configuration required. Follow the steps above."
fi
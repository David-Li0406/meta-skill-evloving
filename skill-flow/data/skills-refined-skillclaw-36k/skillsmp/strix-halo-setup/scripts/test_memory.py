#!/usr/bin/env python3
"""
Test memory allocation after GTT configuration
"""

import torch
import subprocess
import os

print("="*60)
print("MEMORY ALLOCATION TEST")
print("="*60)

# Check current GTT size
print("\n1. CURRENT GTT CONFIGURATION:")
print("-"*40)

try:
    # Check GTT from sysfs
    gtt_file = "/sys/class/drm/card1/device/mem_info_gtt_total"
    if os.path.exists(gtt_file):
        with open(gtt_file, 'r') as f:
            gtt_bytes = int(f.read().strip())
            gtt_gb = gtt_bytes / (1024**3)
            print(f"GTT Total: {gtt_gb:.1f} GB")
    
    # Check via rocm-smi
    result = subprocess.run(['rocm-smi', '--showmeminfo', 'gtt'], 
                          capture_output=True, text=True, timeout=5)
    for line in result.stdout.split('\n'):
        if 'GTT Total Memory' in line:
            print(f"ROCm SMI: {line.strip()}")
            
    # Check kernel parameters
    result = subprocess.run(['cat', '/proc/cmdline'], 
                          capture_output=True, text=True)
    if 'amdttm' in result.stdout:
        print("\nKernel parameters:")
        for param in result.stdout.split():
            if 'amdttm' in param:
                print(f"  {param}")
    else:
        print("\nNo amdttm parameters in kernel cmdline")
        
except Exception as e:
    print(f"Error checking GTT: {e}")

# Test PyTorch GPU detection
print("\n2. PYTORCH GPU DETECTION:")
print("-"*40)

if torch.cuda.is_available():
    device = torch.device('cuda')
    props = torch.cuda.get_device_properties(device)
    print(f"✓ GPU detected: {torch.cuda.get_device_name(0)}")
    print(f"  Memory reported by PyTorch: {props.total_memory / 1e9:.1f} GB")
else:
    print("✗ GPU not detected")
    print("  Make sure you're in the render group: groups | grep render")
    exit(1)

# Test memory allocation
print("\n3. PROGRESSIVE MEMORY ALLOCATION TEST:")
print("-"*40)

test_sizes = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104]
max_allocated = 0

for size_gb in test_sizes:
    try:
        # Try to allocate
        print(f"Attempting {size_gb} GB... ", end="")
        elements = int((size_gb * 1e9) / 4)  # float32 = 4 bytes
        tensor = torch.zeros(elements, device=device)
        
        # Verify it's usable
        tensor[0] = 1.0
        tensor[-1] = 2.0
        sum_val = tensor.sum().item()
        
        max_allocated = size_gb
        print(f"✓ Success")
        
        # Clean up
        del tensor
        torch.cuda.empty_cache()
        
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print(f"✗ Out of memory")
            print(f"\nMaximum allocation reached: {max_allocated} GB")
            break
        else:
            print(f"✗ Error: {e}")
            break
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        break

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

if max_allocated > 33:
    print(f"✓ SUCCESS: Allocated {max_allocated} GB (more than default 33.5 GB limit)")
    print("  GTT configuration is working!")
else:
    print(f"⚠ LIMITED: Only allocated {max_allocated} GB")
    print("  GTT may still be limited. Check kernel parameters and reboot if needed.")
    
print("\nTo increase further:")
print("1. Edit /etc/default/grub")
print("2. Add: amdttm.pages_limit=27648000 amdttm.page_pool_size=27648000")
print("3. Run: sudo update-grub && sudo reboot")
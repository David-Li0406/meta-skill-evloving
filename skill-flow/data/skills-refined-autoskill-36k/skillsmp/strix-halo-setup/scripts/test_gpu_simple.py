#!/usr/bin/env python3
"""
Simplest possible GPU test - no reloading, no complications
"""

import torch

# Just test if GPU works
if torch.cuda.is_available():
    print("✓ GPU DETECTED!")
    print(f"  Device: {torch.cuda.get_device_name(0)}")
    
    # Simple computation test
    a = torch.tensor([1.0, 2.0, 3.0]).cuda()
    b = torch.tensor([4.0, 5.0, 6.0]).cuda()
    c = a + b
    print(f"  Test computation: [1,2,3] + [4,5,6] = {c.cpu().tolist()}")
else:
    print("✗ GPU NOT DETECTED")
    print("  This might be intermittent. Try:")
    print("  1. Close all Python sessions")
    print("  2. Deactivate and reactivate your conda environment")
    print("  3. Run this script again")
    print("  4. Check: groups | grep -E 'render|video'")
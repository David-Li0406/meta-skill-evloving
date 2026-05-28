#!/usr/bin/env python3
"""
Test LLM-style memory usage with expanded GTT
"""

import torch
import torch.nn as nn
import time
import gc

print("="*60)
print("LLM MEMORY TEST WITH EXPANDED GTT")
print("="*60)

# Check device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if device.type == 'cuda':
    print(f"\n✓ Using GPU: {torch.cuda.get_device_name(0)}")
    props = torch.cuda.get_device_properties(0)
    print(f"  Total memory visible: {props.total_memory / 1e9:.1f} GB")
else:
    print("✗ GPU not available")
    exit(1)

# Simulate large model parameters
print("\n1. SIMULATING LARGE MODEL (LLAMA-STYLE):")
print("-"*40)

def create_model_layers(param_count_billions, dtype=torch.float16):
    """Create tensors simulating model parameters"""
    # Approximate parameter distribution
    params_per_billion = 1_000_000_000
    bytes_per_param = 2 if dtype == torch.float16 else 4
    
    total_params = param_count_billions * params_per_billion
    memory_gb = (total_params * bytes_per_param) / 1e9
    
    print(f"Model size: {param_count_billions}B parameters")
    print(f"Dtype: {dtype}")
    print(f"Expected memory: {memory_gb:.1f} GB")
    
    try:
        # Create multiple tensors to simulate model layers
        layers = []
        params_per_layer = total_params // 32  # 32 layers typical
        
        print(f"Creating 32 layers...")
        for i in range(32):
            layer = torch.randn(params_per_layer // 1000, 1000, dtype=dtype, device=device)
            layers.append(layer)
            if (i + 1) % 8 == 0:
                print(f"  Layers {i-6}-{i+1}: ✓")
        
        # Check actual memory used
        if device.type == 'cuda':
            allocated = torch.cuda.memory_allocated() / 1e9
            reserved = torch.cuda.memory_reserved() / 1e9
            print(f"\nActual memory allocated: {allocated:.1f} GB")
            print(f"Memory reserved: {reserved:.1f} GB")
        
        return layers
        
    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print(f"✗ Out of memory for {param_count_billions}B model")
            return None
        raise e

# Test different model sizes
print("\n2. TESTING DIFFERENT MODEL SIZES:")
print("-"*40)

model_sizes = [7, 13, 30, 65]  # Billions of parameters
successful_sizes = []

for size in model_sizes:
    print(f"\n--- Testing {size}B parameter model ---")
    
    # Clean up previous allocations
    gc.collect()
    torch.cuda.empty_cache()
    
    layers = create_model_layers(size, dtype=torch.float16)
    
    if layers is not None:
        successful_sizes.append(size)
        print(f"✓ {size}B model loaded successfully!")
        
        # Do a simple forward pass simulation
        print("Testing computation...")
        x = torch.randn(1, 1000, dtype=torch.float16, device=device)
        with torch.no_grad():
            for layer in layers[:3]:  # Test first 3 layers
                x = x @ layer[:1000, :1000]
        print("✓ Computation successful")
        
        # Clean up
        del layers
        del x
    else:
        print(f"✗ {size}B model too large")
        break
    
    torch.cuda.empty_cache()

# Summary
print("\n" + "="*60)
print("RESULTS SUMMARY")
print("="*60)

if successful_sizes:
    largest = max(successful_sizes)
    print(f"✓ Largest model successfully loaded: {largest}B parameters")
    
    if largest >= 30:
        print("\n🎉 EXCELLENT! You can now run 30B+ parameter models!")
        print("   This was impossible with the 33.5GB limit.")
    elif largest >= 13:
        print("\n✓ GOOD! You can run 13B parameter models.")
        print("   This is a significant improvement over the default limit.")
    else:
        print("\n⚠ Limited to 7B models. Check available system RAM.")
else:
    print("✗ Could not load any large models")

print("\nComparison:")
print("  Before GTT expansion: ~7B models maximum")
print(f"  After GTT expansion:  ~{largest if successful_sizes else 0}B models maximum")

# Memory stats
print("\nFinal memory stats:")
if device.type == 'cuda':
    print(f"  Peak memory used: {torch.cuda.max_memory_allocated() / 1e9:.1f} GB")
    print(f"  Peak memory reserved: {torch.cuda.max_memory_reserved() / 1e9:.1f} GB")
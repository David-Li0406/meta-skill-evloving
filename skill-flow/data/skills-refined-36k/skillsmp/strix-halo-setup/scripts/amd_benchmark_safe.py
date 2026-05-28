#!/usr/bin/env python3
"""
AMD Strix Halo PyTorch Benchmark - Safe Version
Avoids known segfault issues on gfx1151
"""

import torch
import torch.nn as nn
import time
import os
import psutil
from datetime import datetime
import json
import argparse
import subprocess

def get_device_info(device):
    """Get device information safely"""
    info = {
        "device_type": device.type,
    }
    
    if device.type == 'cuda':
        try:
            info["device_name"] = torch.cuda.get_device_name(device)
            props = torch.cuda.get_device_properties(device)
            info["compute_capability"] = torch.cuda.get_device_capability(device)
            info["total_memory_gb"] = props.total_memory / 1e9
            info["multi_processor_count"] = props.multi_processor_count
        except:
            pass
    
    # System memory
    mem = psutil.virtual_memory()
    info['system_memory_gb'] = mem.total / 1e9
    info['system_memory_available_gb'] = mem.available / 1e9
    
    return info

def safe_benchmark_matmul(device, sizes=[1024, 2048], iterations=20):
    """Safely benchmark matrix multiplication"""
    print("\nMatrix Multiplication Benchmark (Safe Mode)")
    print("-" * 40)
    
    results = {}
    
    for size in sizes:
        try:
            # Test different precisions
            precisions = [
                ('FP32', torch.float32),
                ('BF16', torch.bfloat16),
            ]
            
            for precision_name, dtype in precisions:
                if device.type == 'cpu' and dtype != torch.float32:
                    continue
                
                print(f"\nTesting {precision_name} at {size}x{size}...")
                
                # Smaller allocation to avoid segfaults
                a = torch.randn(size, size, device=device, dtype=dtype)
                b = torch.randn(size, size, device=device, dtype=dtype)
                
                # Ensure tensors are ready
                if device.type == 'cuda':
                    torch.cuda.synchronize()
                
                # Warmup with fewer iterations
                with torch.no_grad():
                    for _ in range(3):
                        c = torch.matmul(a, b)
                        del c  # Immediately free memory

                if device.type == 'cuda':
                    torch.cuda.synchronize()

                # Time the operations
                start_time = time.time()
                with torch.no_grad():
                    for _ in range(iterations):
                        c = torch.matmul(a, b)
                        del c  # Immediately free memory

                if device.type == 'cuda':
                    torch.cuda.synchronize()

                elapsed = time.time() - start_time

                # Calculate TFLOPS
                # Note: FLOPS count is same regardless of dtype (FP32/BF16)
                # Performance differences naturally show in elapsed time
                tflops = (2 * size**3 * iterations) / (elapsed * 1e12)
                
                results[f"{precision_name}_{size}"] = {
                    "tflops": tflops,
                    "time_per_iter_ms": (elapsed / iterations) * 1000
                }
                
                print(f"  {precision_name}: {tflops:.2f} TFLOPS, "
                      f"{(elapsed/iterations)*1000:.2f} ms/iter")
                
                # Clean up
                del a, b
                if device.type == 'cuda':
                    torch.cuda.empty_cache()
                    
        except Exception as e:
            print(f"  Error at size {size}: {e}")
            results[f"error_{size}"] = str(e)
    
    return results

def safe_memory_test(device, max_gb=32):
    """Safely test memory allocation"""
    print("\nMemory Allocation Test (Safe Mode)")
    print("-" * 40)
    
    results = {}
    
    # Check environment
    hsa_xnack = os.environ.get('HSA_XNACK', '0')
    results["unified_memory_enabled"] = (hsa_xnack == '1')
    
    if hsa_xnack != '1':
        print("Note: HSA_XNACK is not set to 1. Unified memory may be limited.")
    
    # Test progressively larger allocations
    test_sizes_gb = [1, 2, 4, 8, 16, 24, 32]
    max_allocated = 0
    
    for size_gb in test_sizes_gb:
        if size_gb > max_gb:
            break
            
        try:
            print(f"Testing {size_gb} GB allocation...")
            elements = int((size_gb * 1e9) / 4)  # float32
            
            # Allocate
            tensor = torch.zeros(elements, device=device, dtype=torch.float32)
            
            # Verify it's usable
            tensor[0] = 1.0
            tensor[-1] = 2.0
            _ = tensor[0].item()  # Force synchronization
            
            max_allocated = size_gb
            print(f"  ✓ Successfully allocated {size_gb} GB")
            
            # Clean up immediately
            del tensor
            if device.type == 'cuda':
                torch.cuda.empty_cache()
                
        except Exception as e:
            print(f"  ✗ Failed at {size_gb} GB: {e}")
            break
    
    results["max_allocated_gb"] = max_allocated
    
    # Get actual memory info from ROCm
    try:
        result = subprocess.run(['rocm-smi', '--showmeminfo', 'gtt'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'GTT Total Memory' in line:
                    gtt_mb = float(line.split(':')[1].strip().split()[0])
                    results['gtt_total_gb'] = gtt_mb / 1024
                    print(f"\nGTT Memory Available: {gtt_mb/1024:.1f} GB")
    except:
        pass
    
    return results

def safe_bandwidth_test(device):
    """Safely test memory bandwidth"""
    print("\nMemory Bandwidth Test (Safe Mode)")
    print("-" * 40)
    
    results = {}
    
    # Use smaller size to avoid crashes
    size_gb = 1.0
    elements = int((size_gb * 1e9) / 4)
    
    try:
        tensor = torch.zeros(elements, device=device, dtype=torch.float32)
        
        # Write bandwidth
        if device.type == 'cuda':
            torch.cuda.synchronize()
        
        iterations = 10
        start_time = time.time()
        for i in range(iterations):
            tensor.fill_(float(i))
        
        if device.type == 'cuda':
            torch.cuda.synchronize()
        
        write_time = time.time() - start_time
        write_bandwidth = (4 * elements * iterations) / (write_time * 1e9)
        
        results["write_bandwidth_gb_s"] = write_bandwidth
        print(f"Write Bandwidth: {write_bandwidth:.1f} GB/s")
        
        # Copy bandwidth
        tensor2 = torch.zeros_like(tensor)
        
        start_time = time.time()
        for _ in range(iterations):
            tensor2.copy_(tensor)
        
        if device.type == 'cuda':
            torch.cuda.synchronize()
        
        copy_time = time.time() - start_time
        copy_bandwidth = (8 * elements * iterations) / (copy_time * 1e9)
        
        results["copy_bandwidth_gb_s"] = copy_bandwidth
        print(f"Copy Bandwidth: {copy_bandwidth:.1f} GB/s")
        
        # Clean up
        del tensor, tensor2
        if device.type == 'cuda':
            torch.cuda.empty_cache()
            
    except Exception as e:
        print(f"Bandwidth test error: {e}")
        results["error"] = str(e)
    
    return results

def main():
    parser = argparse.ArgumentParser(description='AMD Strix Halo Safe Benchmark')
    parser.add_argument('--device', type=str, default='cuda',
                        choices=['cuda', 'cpu'], help='Device to use')
    parser.add_argument('--max-memory-gb', type=int, default=32,
                        help='Maximum memory to test')
    args = parser.parse_args()
    
    if args.device == 'cuda' and not torch.cuda.is_available():
        print("CUDA not available. Check ROCm installation.")
        return
    
    device = torch.device(args.device)
    
    print("="*60)
    print("AMD STRIX HALO BENCHMARK - SAFE MODE")
    print("="*60)
    
    # Environment check
    print("\nEnvironment Variables:")
    for var in ['HSA_XNACK', 'HSA_OVERRIDE_GFX_VERSION', 'PYTORCH_ROCM_ARCH']:
        value = os.environ.get(var, 'NOT SET')
        print(f"  {var}: {value}")
    
    # Device info
    device_info = get_device_info(device)
    print("\nDevice Information:")
    for key, value in device_info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    results = {}
    
    # Run safe benchmarks
    try:
        # Matrix multiplication
        matmul_results = safe_benchmark_matmul(device)
        results["matmul"] = matmul_results
        
        # Memory test
        memory_results = safe_memory_test(device, args.max_memory_gb)
        results["memory"] = memory_results
        
        # Bandwidth test
        bandwidth_results = safe_bandwidth_test(device)
        results["bandwidth"] = bandwidth_results
        
    except Exception as e:
        print(f"\nBenchmark error: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    
    # Performance summary
    if "matmul" in results:
        print("\nCompute Performance:")
        for key, value in results["matmul"].items():
            if isinstance(value, dict) and "tflops" in value:
                print(f"  {key}: {value['tflops']:.2f} TFLOPS")
    
    # Memory summary  
    if "memory" in results:
        print("\nMemory:")
        print(f"  Max allocated: {results['memory'].get('max_allocated_gb', 0)} GB")
        if 'gtt_total_gb' in results['memory']:
            print(f"  GTT available: {results['memory']['gtt_total_gb']:.1f} GB")
        print(f"  Unified memory: {'Enabled' if results['memory']['unified_memory_enabled'] else 'Disabled'}")
    
    # Bandwidth summary
    if "bandwidth" in results and "write_bandwidth_gb_s" in results["bandwidth"]:
        print("\nBandwidth:")
        print(f"  Write: {results['bandwidth']['write_bandwidth_gb_s']:.1f} GB/s")
        print(f"  Copy: {results['bandwidth']['copy_bandwidth_gb_s']:.1f} GB/s")
    
    # Save results
    filename = f"benchmark_safe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "device_info": device_info,
            "results": results
        }, f, indent=2)
    print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    main()
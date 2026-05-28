"""
Hardware detection and optimization module for high-performance audio transcription.
Detects available hardware (GPUs, CPUs, memory) and configures optimal settings.
"""

import os
import json
import platform
import psutil
import torch
import subprocess
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class HardwareSpecs:
    """Hardware specifications container"""
    # CPU specs
    cpu_model: str
    cpu_cores: int
    cpu_threads: int
    cpu_freq_ghz: float
    ram_total_gb: float
    ram_available_gb: float
    
    # GPU specs
    gpu_available: bool
    gpu_count: int
    gpu_models: List[str]
    gpu_vram_total_gb: List[float]
    gpu_vram_available_gb: List[float]
    cuda_version: Optional[str]
    cudnn_version: Optional[str]
    
    # System specs
    platform_name: str
    platform_version: str
    python_version: str
    torch_version: str
    
    # Optimization recommendations
    recommended_batch_size: int
    recommended_model: str
    recommended_device: str
    recommended_workers: int
    recommended_fp16: bool
    max_parallel_files: int


class HardwareOptimizer:
    """Optimizes transcription settings based on available hardware"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.specs = self.detect_hardware()
        self.optimization_profile = self.calculate_optimization_profile()
        
    def detect_hardware(self) -> HardwareSpecs:
        """Detect all available hardware specifications"""
        
        # CPU detection
        cpu_info = self._detect_cpu()
        
        # Memory detection
        memory_info = self._detect_memory()
        
        # GPU detection
        gpu_info = self._detect_gpu()
        
        # System info
        system_info = self._detect_system()
        
        # Calculate recommendations
        recommendations = self._calculate_recommendations(
            cpu_info, memory_info, gpu_info
        )
        
        specs = HardwareSpecs(
            **cpu_info,
            **memory_info,
            **gpu_info,
            **system_info,
            **recommendations
        )
        
        logger.info(f"Hardware detected: {specs.gpu_count} GPU(s), {specs.cpu_cores} CPU cores, {specs.ram_total_gb:.1f}GB RAM")
        
        return specs
    
    def _detect_cpu(self) -> Dict:
        """Detect CPU specifications"""
        try:
            import cpuinfo
            cpu_data = cpuinfo.get_cpu_info()
            cpu_brand = cpu_data.get('brand_raw', 'Unknown CPU')
        except:
            cpu_brand = platform.processor() or 'Unknown CPU'
        
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        return {
            'cpu_model': cpu_brand,
            'cpu_cores': cpu_cores,
            'cpu_threads': cpu_threads,
            'cpu_freq_ghz': cpu_freq.max / 1000 if cpu_freq else 0.0
        }
    
    def _detect_memory(self) -> Dict:
        """Detect memory specifications"""
        mem = psutil.virtual_memory()
        
        return {
            'ram_total_gb': mem.total / (1024**3),
            'ram_available_gb': mem.available / (1024**3)
        }
    
    def _detect_gpu(self) -> Dict:
        """Detect GPU specifications using multiple methods"""
        gpu_info = {
            'gpu_available': False,
            'gpu_count': 0,
            'gpu_models': [],
            'gpu_vram_total_gb': [],
            'gpu_vram_available_gb': [],
            'cuda_version': None,
            'cudnn_version': None
        }
        
        # Check CUDA availability
        if torch.cuda.is_available():
            gpu_info['gpu_available'] = True
            gpu_info['gpu_count'] = torch.cuda.device_count()
            
            # Get CUDA version
            gpu_info['cuda_version'] = torch.version.cuda
            
            # Get cuDNN version
            if torch.backends.cudnn.is_available():
                gpu_info['cudnn_version'] = str(torch.backends.cudnn.version())
            
            # Get GPU details for each device
            for i in range(gpu_info['gpu_count']):
                # GPU model
                gpu_name = torch.cuda.get_device_name(i)
                gpu_info['gpu_models'].append(gpu_name)
                
                # GPU memory
                props = torch.cuda.get_device_properties(i)
                total_memory_gb = props.total_memory / (1024**3)
                gpu_info['gpu_vram_total_gb'].append(total_memory_gb)
                
                # Available memory
                torch.cuda.set_device(i)
                torch.cuda.empty_cache()
                free_memory = torch.cuda.mem_get_info(i)[0] / (1024**3)
                gpu_info['gpu_vram_available_gb'].append(free_memory)
        
        # Try nvidia-smi for additional info
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().split('\n')
            
            if not gpu_info['gpu_available'] and lines:
                gpu_info['gpu_available'] = True
                gpu_info['gpu_count'] = len(lines)
                
                for line in lines:
                    parts = line.split(', ')
                    if len(parts) == 3:
                        if not gpu_info['gpu_models']:
                            gpu_info['gpu_models'].append(parts[0])
                        if not gpu_info['gpu_vram_total_gb']:
                            gpu_info['gpu_vram_total_gb'].append(float(parts[1]) / 1024)
                        if not gpu_info['gpu_vram_available_gb']:
                            gpu_info['gpu_vram_available_gb'].append(float(parts[2]) / 1024)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return gpu_info
    
    def _detect_system(self) -> Dict:
        """Detect system specifications"""
        return {
            'platform_name': platform.system(),
            'platform_version': platform.version(),
            'python_version': platform.python_version(),
            'torch_version': torch.__version__
        }
    
    def _calculate_recommendations(self, cpu_info: Dict, memory_info: Dict, gpu_info: Dict) -> Dict:
        """Calculate optimal settings based on hardware"""
        
        recommendations = {
            'recommended_batch_size': 1,
            'recommended_model': 'base',
            'recommended_device': 'cpu',
            'recommended_workers': 1,
            'recommended_fp16': False,
            'max_parallel_files': 1
        }
        
        # Device selection
        if gpu_info['gpu_available'] and gpu_info['gpu_count'] > 0:
            recommendations['recommended_device'] = 'cuda'
            recommendations['recommended_fp16'] = True
            
            # Model selection based on VRAM
            min_vram = min(gpu_info['gpu_vram_available_gb']) if gpu_info['gpu_vram_available_gb'] else 0
            
            if min_vram >= 10:
                recommendations['recommended_model'] = 'large-v3'
                recommendations['recommended_batch_size'] = 16
            elif min_vram >= 6:
                recommendations['recommended_model'] = 'large-v2'
                recommendations['recommended_batch_size'] = 8
            elif min_vram >= 4:
                recommendations['recommended_model'] = 'medium'
                recommendations['recommended_batch_size'] = 4
            elif min_vram >= 2:
                recommendations['recommended_model'] = 'small'
                recommendations['recommended_batch_size'] = 2
            else:
                recommendations['recommended_model'] = 'base'
                recommendations['recommended_batch_size'] = 1
            
            # Multi-GPU parallelism
            if gpu_info['gpu_count'] > 1:
                recommendations['max_parallel_files'] = min(gpu_info['gpu_count'], 4)
        else:
            # CPU-only recommendations
            if memory_info['ram_available_gb'] >= 16:
                recommendations['recommended_model'] = 'medium'
            elif memory_info['ram_available_gb'] >= 8:
                recommendations['recommended_model'] = 'small'
            else:
                recommendations['recommended_model'] = 'base'
        
        # Worker threads (for data loading)
        recommendations['recommended_workers'] = min(cpu_info['cpu_cores'], 8)
        
        # Parallel file processing based on RAM and CPU
        if not recommendations['recommended_device'] == 'cuda':
            if memory_info['ram_available_gb'] >= 32 and cpu_info['cpu_cores'] >= 8:
                recommendations['max_parallel_files'] = 4
            elif memory_info['ram_available_gb'] >= 16 and cpu_info['cpu_cores'] >= 4:
                recommendations['max_parallel_files'] = 2
            else:
                recommendations['max_parallel_files'] = 1
        
        return recommendations
    
    def calculate_optimization_profile(self) -> Dict:
        """Calculate detailed optimization profile"""
        
        profile = {
            'hardware_tier': self._determine_tier(),
            'transcription': self._optimize_transcription(),
            'diarization': self._optimize_diarization(),
            'parallel_processing': self._optimize_parallel(),
            'memory_management': self._optimize_memory()
        }
        
        return profile
    
    def _determine_tier(self) -> str:
        """Determine hardware tier (low/medium/high/ultra)"""
        
        score = 0
        
        # GPU scoring
        if self.specs.gpu_available:
            score += 30
            if self.specs.gpu_count > 1:
                score += 20
            if self.specs.gpu_vram_total_gb and max(self.specs.gpu_vram_total_gb) >= 24:
                score += 20
            elif self.specs.gpu_vram_total_gb and max(self.specs.gpu_vram_total_gb) >= 12:
                score += 10
        
        # CPU scoring
        if self.specs.cpu_cores >= 16:
            score += 15
        elif self.specs.cpu_cores >= 8:
            score += 10
        elif self.specs.cpu_cores >= 4:
            score += 5
        
        # RAM scoring
        if self.specs.ram_total_gb >= 64:
            score += 15
        elif self.specs.ram_total_gb >= 32:
            score += 10
        elif self.specs.ram_total_gb >= 16:
            score += 5
        
        if score >= 70:
            return 'ultra'
        elif score >= 45:
            return 'high'
        elif score >= 25:
            return 'medium'
        else:
            return 'low'
    
    def _optimize_transcription(self) -> Dict:
        """Optimize transcription settings"""
        
        settings = {
            'model': self.specs.recommended_model,
            'device': self.specs.recommended_device,
            'batch_size': self.specs.recommended_batch_size,
            'compute_type': 'float16' if self.specs.recommended_fp16 else 'float32',
            'num_workers': self.specs.recommended_workers,
            'beam_size': 5,
            'best_of': 5
        }
        
        # Adjust for tier
        tier = self._determine_tier()
        if tier == 'ultra':
            settings['beam_size'] = 10
            settings['best_of'] = 10
            settings['batch_size'] = min(32, settings['batch_size'] * 2)
        elif tier == 'high':
            settings['beam_size'] = 7
            settings['best_of'] = 7
        elif tier == 'low':
            settings['beam_size'] = 3
            settings['best_of'] = 3
            settings['batch_size'] = 1
        
        return settings
    
    def _optimize_diarization(self) -> Dict:
        """Optimize diarization settings"""
        
        settings = {
            'backend': 'pyannote',
            'device': self.specs.recommended_device,
            'batch_size': min(16, self.specs.recommended_batch_size),
            'use_auth_token': False,
            'parallel_chunks': self.specs.cpu_cores // 2
        }
        
        if self.specs.gpu_available:
            settings['backend'] = 'pyannote-gpu'
            settings['batch_size'] = min(32, self.specs.recommended_batch_size * 2)
        
        return settings
    
    def _optimize_parallel(self) -> Dict:
        """Optimize parallel processing settings"""
        
        settings = {
            'max_concurrent_files': self.specs.max_parallel_files,
            'max_concurrent_gpus': self.specs.gpu_count,
            'cpu_worker_pool_size': self.specs.cpu_threads,
            'io_workers': min(4, self.specs.cpu_cores),
            'use_multiprocessing': self.specs.cpu_cores >= 4,
            'chunk_processing_strategy': 'parallel' if self.specs.cpu_cores >= 8 else 'sequential'
        }
        
        # GPU load balancing
        if self.specs.gpu_count > 1:
            settings['gpu_load_balancing'] = 'round_robin'
            settings['gpu_memory_fraction'] = 0.85
        
        return settings
    
    def _optimize_memory(self) -> Dict:
        """Optimize memory management settings"""
        
        settings = {
            'cache_embeddings': self.specs.ram_available_gb >= 16,
            'preload_models': self.specs.ram_available_gb >= 32,
            'max_cache_size_gb': min(8, self.specs.ram_available_gb * 0.25),
            'clear_cache_interval': 100,  # Clear every N files
            'use_memory_mapping': self.specs.ram_available_gb < 16,
            'torch_memory_fraction': 0.8 if self.specs.gpu_available else None
        }
        
        return settings
    
    def generate_config_override(self) -> Dict:
        """Generate configuration overrides for optimal performance"""
        
        config = {
            'asr': self.optimization_profile['transcription'],
            'diarization': self.optimization_profile['diarization'],
            'performance': {
                'preset': 'custom',
                **self.optimization_profile['parallel_processing'],
                **self.optimization_profile['memory_management']
            }
        }
        
        # Voice sex classification disabled for simplified pipeline
        config['voice_sex'] = {
            'enabled': False
        }
        
        return config
    
    def save_hardware_report(self, output_path: Path):
        """Save detailed hardware report"""
        
        report = {
            'timestamp': str(Path.ctime(Path('.'))),
            'hardware_specs': asdict(self.specs),
            'optimization_profile': self.optimization_profile,
            'hardware_tier': self._determine_tier(),
            'config_overrides': self.generate_config_override()
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Hardware report saved to {output_path}")
        
        return report
    
    def benchmark_hardware(self) -> Dict:
        """Run hardware benchmarks for accurate performance estimation"""
        
        benchmarks = {}
        
        # CPU benchmark
        if self.specs.cpu_cores > 0:
            benchmarks['cpu'] = self._benchmark_cpu()
        
        # GPU benchmark
        if self.specs.gpu_available:
            benchmarks['gpu'] = self._benchmark_gpu()
        
        # Memory bandwidth benchmark
        benchmarks['memory'] = self._benchmark_memory()
        
        return benchmarks
    
    def _benchmark_cpu(self) -> Dict:
        """Simple CPU benchmark"""
        import time
        import numpy as np
        
        # Matrix multiplication benchmark
        size = 2000
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)
        
        start = time.time()
        _ = np.dot(a, b)
        duration = time.time() - start
        
        gflops = (2 * size**3) / (duration * 1e9)
        
        return {
            'matrix_mult_gflops': gflops,
            'duration_seconds': duration
        }
    
    def _benchmark_gpu(self) -> Dict:
        """Simple GPU benchmark"""
        if not self.specs.gpu_available:
            return {}
        
        import time
        
        results = []
        
        for i in range(self.specs.gpu_count):
            torch.cuda.set_device(i)
            
            # Matrix multiplication on GPU
            size = 4096
            a = torch.randn(size, size, device='cuda')
            b = torch.randn(size, size, device='cuda')
            
            # Warmup
            _ = torch.mm(a, b)
            torch.cuda.synchronize()
            
            # Benchmark
            start = time.time()
            for _ in range(10):
                _ = torch.mm(a, b)
            torch.cuda.synchronize()
            duration = time.time() - start
            
            tflops = (10 * 2 * size**3) / (duration * 1e12)
            
            results.append({
                'device_id': i,
                'device_name': self.specs.gpu_models[i] if i < len(self.specs.gpu_models) else 'Unknown',
                'matrix_mult_tflops': tflops,
                'duration_seconds': duration
            })
        
        return results
    
    def _benchmark_memory(self) -> Dict:
        """Simple memory bandwidth benchmark"""
        import time
        import numpy as np
        
        # Memory copy benchmark
        size_mb = 1000
        data = np.random.rand(size_mb * 1024 * 1024 // 8)
        
        start = time.time()
        for _ in range(10):
            _ = data.copy()
        duration = time.time() - start
        
        bandwidth_gb_s = (10 * size_mb / 1024) / duration
        
        return {
            'bandwidth_gb_s': bandwidth_gb_s,
            'duration_seconds': duration
        }


def auto_configure(config_path: Optional[Path] = None) -> Dict:
    """Automatically configure for optimal performance"""
    
    optimizer = HardwareOptimizer(config_path)
    
    # Generate report
    report_path = Path('reports/hardware_optimization.json')
    report = optimizer.save_hardware_report(report_path)
    
    # Run benchmarks
    benchmarks = optimizer.benchmark_hardware()
    report['benchmarks'] = benchmarks
    
    # Save updated report
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Hardware optimization complete. Tier: {optimizer._determine_tier()}")
    
    return optimizer.generate_config_override()


if __name__ == "__main__":
    # Test hardware detection
    logging.basicConfig(level=logging.INFO)
    
    optimizer = HardwareOptimizer()
    print(f"\nHardware Tier: {optimizer._determine_tier()}")
    print(f"\nHardware Specs:")
    print(json.dumps(asdict(optimizer.specs), indent=2))
    print(f"\nOptimization Profile:")
    print(json.dumps(optimizer.optimization_profile, indent=2))
    print(f"\nConfig Overrides:")
    print(json.dumps(optimizer.generate_config_override(), indent=2))
    
    # Run benchmarks
    print("\nRunning benchmarks...")
    benchmarks = optimizer.benchmark_hardware()
    print(json.dumps(benchmarks, indent=2))
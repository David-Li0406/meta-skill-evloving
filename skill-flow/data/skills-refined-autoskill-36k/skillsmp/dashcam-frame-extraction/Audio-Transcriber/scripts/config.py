"""Configuration management for LocalAV Transcriber."""

import os
import yaml
import torch
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Config:
    """Central configuration management."""
    
    config_path: Optional[Path] = None
    config_dict: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Load configuration after initialization."""
        if self.config_path:
            self.load(self.config_path)
        else:
            # Load default config
            default_path = Path(__file__).parent.parent.parent / "config.yaml"
            if default_path.exists():
                self.load(default_path)
        
        # Auto-detect hardware capabilities
        self._detect_hardware()
        
        # Create necessary directories
        self._create_directories()
    
    def load(self, config_path: Path) -> None:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            self.config_dict = yaml.safe_load(f)
        self.config_path = config_path
    
    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to YAML file."""
        save_path = config_path or self.config_path
        if not save_path:
            raise ValueError("No config path specified")
        
        with open(save_path, 'w') as f:
            yaml.dump(self.config_dict, f, default_flow_style=False, sort_keys=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key."""
        keys = key.split('.')
        value = self.config_dict
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-notation key."""
        keys = key.split('.')
        config = self.config_dict
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _detect_hardware(self) -> None:
        """Auto-detect hardware capabilities and adjust settings."""
        # Detect CUDA availability
        cuda_available = torch.cuda.is_available()
        
        if self.get('asr.device') == 'auto':
            self.set('asr.device', 'cuda' if cuda_available else 'cpu')
        
        if cuda_available:
            # Get GPU memory
            gpu_mem_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            
            # Auto-select model size based on VRAM
            if self.get('asr.model') == 'auto':
                if gpu_mem_gb >= 10:
                    self.set('asr.model', 'large-v3')
                elif gpu_mem_gb >= 6:
                    self.set('asr.model', 'medium')
                elif gpu_mem_gb >= 4:
                    self.set('asr.model', 'small')
                else:
                    self.set('asr.model', 'base')
            
            # Auto-select compute type
            if self.get('asr.compute_type') == 'auto':
                if gpu_mem_gb >= 8:
                    self.set('asr.compute_type', 'float16')
                else:
                    self.set('asr.compute_type', 'int8_float16')
        else:
            # CPU settings
            if self.get('asr.model') == 'auto':
                self.set('asr.model', 'base')
            if self.get('asr.compute_type') == 'auto':
                self.set('asr.compute_type', 'int8')
        
        # Adjust batch size based on available memory
        if cuda_available:
            if gpu_mem_gb >= 8:
                self.set('performance.batch_size', 32)
            elif gpu_mem_gb >= 4:
                self.set('performance.batch_size', 16)
            else:
                self.set('performance.batch_size', 8)
        else:
            # CPU batch size
            import psutil
            ram_gb = psutil.virtual_memory().total / 1e9
            if ram_gb >= 32:
                self.set('performance.batch_size', 8)
            elif ram_gb >= 16:
                self.set('performance.batch_size', 4)
            else:
                self.set('performance.batch_size', 2)
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        dirs_to_create = [
            self.get('paths.output_root'),
            self.get('paths.embeddings_dir'),
            self.get('paths.logs_dir'),
            self.get('paths.cache_dir'),
            self.get('paths.models_dir'),
        ]
        
        for dir_path in dirs_to_create:
            if dir_path:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def apply_preset(self, preset: str) -> None:
        """Apply performance preset settings."""
        presets = {
            'speed': {
                'asr.model': 'base',
                'asr.beam_size': 1,
                'asr.best_of': 1,
                'asr.temperature': [0.0],
                'diarization.min_segment_duration': 1.0,
                'performance.batch_size': 32,
                'export.include_word_timestamps': False,
            },
            'balanced': {
                'asr.model': 'medium',
                'asr.beam_size': 5,
                'asr.best_of': 5,
                'asr.temperature': [0.0, 0.2, 0.4],
                'diarization.min_segment_duration': 0.5,
                'performance.batch_size': 16,
                'export.include_word_timestamps': True,
            },
            'accuracy': {
                'asr.model': 'large-v3',
                'asr.beam_size': 10,
                'asr.best_of': 10,
                'asr.temperature': [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                'diarization.min_segment_duration': 0.3,
                'performance.batch_size': 8,
                'export.include_word_timestamps': True,
            }
        }
        
        if preset not in presets:
            raise ValueError(f"Unknown preset: {preset}. Choose from: {list(presets.keys())}")
        
        for key, value in presets[preset].items():
            self.set(key, value)
        
        self.set('performance.preset', preset)
#!/usr/bin/env python3
"""
Environment Manager - Stable API key loading from multiple sources

This module provides a robust system for loading API keys from various sources
with proper priority handling and validation.
"""

import os
import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class EnvManager:
    """Manages environment variable loading with priority and validation."""
    
    def __init__(self):
        """Initialize the environment manager."""
        self._loaded_vars: Dict[str, str] = {}
        self._validation_cache: Dict[str, bool] = {}
        
    def load_api_keys(self) -> Dict[str, str]:
        """
        Load API keys from multiple sources in priority order.
        
        Priority (high → low):
        1. Direct environment variables
        2. ~/.local/bin/env script
        3. ~/.bashrc export statements
        4. ~/.config/opencode/.env file
        5. Empty dict (will trigger mock mode)
        
        Returns:
            Dictionary of loaded API keys
        """
        if self._loaded_vars:
            return self._loaded_vars
            
        sources = [
            ("Direct environment", self._load_direct_env),
            ("~/.local/bin/env", self._load_local_env_script),
            ("~/.bashrc", self._load_bashrc),
            ("~/.config/opencode/.env", self._load_config_env),
        ]
        
        for source_name, loader in sources:
            try:
                vars_from_source = loader()
                for key, value in vars_from_source.items():
                    if key in ["GEMINI_API_KEY", "OPENAI_API_KEY"] and value:
                        self._loaded_vars[key] = value
                        logger.debug(f"Loaded {key} from {source_name}")
            except Exception as e:
                logger.debug(f"Failed to load from {source_name}: {e}")
                
        return self._loaded_vars
    
    def _load_direct_env(self) -> Dict[str, str]:
        """Load from current environment variables."""
        return {
            key: value
            for key, value in os.environ.items()
            if key in ["GEMINI_API_KEY", "OPENAI_API_KEY", "LLM_PROVIDER"]
        }
    
    def _load_local_env_script(self) -> Dict[str, str]:
        """Load from ~/.local/bin/env script."""
        env_script = Path.home() / ".local" / "bin" / "env"
        if not env_script.exists():
            return {}
            
        # Read and execute the script safely
        try:
            with open(env_script, 'r') as f:
                content = f.read()
                
            # Extract export statements
            exports = re.findall(r'export\s+([A-Z_]+)=["\']?([^"\'\s]+)', content)
            return dict(exports)
        except Exception as e:
            logger.debug(f"Error reading ~/.local/bin/env: {e}")
            return {}
    
    def _load_bashrc(self) -> Dict[str, str]:
        """Load export statements from ~/.bashrc."""
        bashrc = Path.home() / ".bashrc"
        if not bashrc.exists():
            return {}
            
        try:
            with open(bashrc, 'r') as f:
                content = f.read()
                
            # Extract export statements
            exports = re.findall(r'^\s*export\s+([A-Z_]+)=["\']?([^"\'\s]+)', content, re.MULTILINE)
            return dict(exports)
        except Exception as e:
            logger.debug(f"Error reading ~/.bashrc: {e}")
            return {}
    
    def _load_config_env(self) -> Dict[str, str]:
        """Load from ~/.config/opencode/.env file."""
        env_file = Path.home() / ".config" / "opencode" / ".env"
        if not env_file.exists():
            return {}
            
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                
            # Parse KEY=value format
            vars_dict = {}
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    if key in ["GEMINI_API_KEY", "OPENAI_API_KEY", "LLM_PROVIDER"]:
                        vars_dict[key] = value
                        
            return vars_dict
        except Exception as e:
            logger.debug(f"Error reading ~/.config/opencode/.env: {e}")
            return {}
    
    def validate_keys(self) -> Tuple[bool, List[str]]:
        """
        Validate loaded API keys.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        api_keys = self.load_api_keys()
        
        if not api_keys:
            issues.append("No API keys found in any source")
            return False, issues
            
        # Validate each key
        for key, value in api_keys.items():
            if not value or len(value) < 10:
                issues.append(f"{key} appears to be invalid (too short)")
            elif key == "GEMINI_API_KEY" and not value.startswith(('AIza', 'GOYA')):
                issues.append(f"{key} format appears incorrect")
            elif key == "OPENAI_API_KEY" and not value.startswith('sk-'):
                issues.append(f"{key} format appears incorrect")
                
        return len(issues) == 0, issues
    
    def get_preferred_provider(self) -> str:
        """
        Determine the preferred LLM provider.
        
        Returns:
            Provider name ('gemini', 'openai', or 'mock')
        """
        api_keys = self.load_api_keys()
        
        # Check explicit provider preference
        explicit_provider = api_keys.get("LLM_PROVIDER", "").lower()
        if explicit_provider in ["gemini", "openai"]:
            if f"{explicit_provider.upper()}_API_KEY" in api_keys:
                return explicit_provider
                
        # Auto-detect based on available keys
        if "GEMINI_API_KEY" in api_keys:
            return "gemini"
        elif "OPENAI_API_KEY" in api_keys:
            return "openai"
            
        return "mock"
    
    def get_key_preview(self, key: str) -> str:
        """
        Get a masked preview of an API key for logging.
        
        Args:
            key: The API key value
            
        Returns:
            Masked key preview (e.g., "AIza***abcdef")
        """
        if not key or len(key) < 8:
            return "***"
            
        if len(key) <= 12:
            return key[:2] + "*" * (len(key) - 4) + key[-2:]
        else:
            return key[:4] + "*" * (len(key) - 8) + key[-4:]
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive status summary for debugging.
        
        Returns:
            Dictionary with status information
        """
        api_keys = self.load_api_keys()
        is_valid, issues = self.validate_keys()
        preferred = self.get_preferred_provider()
        
        return {
            "loaded_keys": list(api_keys.keys()),
            "preferred_provider": preferred,
            "is_valid": is_valid,
            "issues": issues,
            "key_previews": {
                key: self.get_key_preview(value)
                for key, value in api_keys.items()
            }
        }


# Global instance for easy access
_env_manager = None


def get_env_manager() -> EnvManager:
    """Get or create the global environment manager instance."""
    global _env_manager
    if _env_manager is None:
        _env_manager = EnvManager()
    return _env_manager


def load_api_keys() -> Dict[str, str]:
    """Convenience function to load API keys."""
    return get_env_manager().load_api_keys()


def get_preferred_provider() -> str:
    """Convenience function to get preferred provider."""
    return get_env_manager().get_preferred_provider()
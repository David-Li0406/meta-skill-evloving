#!/usr/bin/env python3
"""
Dependency Checker - Automatic dependency verification and guidance

This module provides comprehensive dependency checking for the deep-research skill,
including Python packages, API connectivity, and optional provider handling.
"""

import sys
import importlib
import subprocess
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class DependencyChecker:
    """Manages dependency checking and provides installation guidance."""
    
    # Required packages with minimum versions
    REQUIRED_PACKAGES = {
        "ddgs": "8.0.0",  # NEW: replaced duckduckgo_search
        "beautifulsoup4": "4.9.0", 
        "requests": "2.25.0",
    }
    
    # Optional provider packages
    OPTIONAL_PACKAGES = {
        "google.genai": "1.0.0",  # Gemini (NEW: replaced google.generativeai)
        "openai": "1.0.0",        # OpenAI
    }
    
    def __init__(self):
        """Initialize the dependency checker."""
        self._package_cache: Dict[str, bool] = {}
        self._version_cache: Dict[str, str] = {}
        
    def check_python_packages(self) -> Dict[str, bool]:
        """
        Check if required Python packages are installed and meet version requirements.
        
        Returns:
            Dictionary mapping package names to availability status
        """
        results = {}
        
        # Check required packages
        for package, min_version in self.REQUIRED_PACKAGES.items():
            results[package] = self._check_package_version(package, min_version)
            
        # Check optional packages
        for package, min_version in self.OPTIONAL_PACKAGES.items():
            results[package] = self._check_package_version(package, min_version)
            
        return results
    
    def _check_package_version(self, package_name: str, min_version: str) -> bool:
        """
        Check if a package is installed and meets minimum version requirement.
        
        Args:
            package_name: Name of the package to check
            min_version: Minimum required version
            
        Returns:
            True if package is available and meets version requirement
        """
        if package_name in self._package_cache:
            return self._package_cache[package_name]
            
        try:
            # Handle special import names
            import_name = self._get_import_name(package_name)
            module = importlib.import_module(import_name)
            
            # Get version
            version = self._get_package_version(module)
            self._version_cache[package_name] = version
            
            # Compare versions
            is_valid = self._compare_versions(version, min_version)
            self._package_cache[package_name] = is_valid
            
            if not is_valid:
                logger.warning(f"{package_name} version {version} is below minimum {min_version}")
                
            return is_valid
            
        except ImportError as e:
            logger.debug(f"Package {package_name} not found: {e}")
            self._package_cache[package_name] = False
            return False
        except Exception as e:
            logger.error(f"Error checking {package_name}: {e}")
            self._package_cache[package_name] = False
            return False
    
    def _get_import_name(self, package_name: str) -> str:
        """Convert package name to import name."""
        import_mapping = {
            "beautifulsoup4": "bs4",
            "ddgs": "ddgs",  # NEW: replaced duckduckgo_search
            "google.genai": "google.genai",  # NEW: replaced google.generativeai
            "openai": "openai",
            "requests": "requests",
        }
        return import_mapping.get(package_name, package_name)
    
    def _get_package_version(self, module) -> str:
        """Extract version from imported module."""
        try:
            # Try common version attributes
            for attr in ["__version__", "version", "VERSION"]:
                if hasattr(module, attr):
                    return str(getattr(module, attr))
                    
            # Try pkg_resources
            import pkg_resources
            package_name = module.__name__.split('.')[0]
            return pkg_resources.get_distribution(package_name).version
            
        except Exception:
            return "unknown"
    
    def _compare_versions(self, current: str, minimum: str) -> bool:
        """Compare version strings using semantic versioning."""
        try:
            from packaging import version
            return version.parse(current) >= version.parse(minimum)
        except ImportError:
            # Fallback to simple string comparison
            return current >= minimum
    
    def suggest_install_commands(self, missing: List[str]) -> str:
        """
        Generate installation commands for missing packages.
        
        Args:
            missing: List of missing package names
            
        Returns:
            Formatted string with installation commands
        """
        if not missing:
            return "All dependencies are satisfied!"
            
        commands = []
        commands.append("📦 Missing Dependencies Installation Guide:")
        commands.append("")
        
        # Group by installation method
        pip_packages = []
        other_packages = []
        
        for package in missing:
            if package in ["beautifulsoup4", "ddgs", "requests", "openai"]:
                pip_packages.append(package)
            elif package == "google.genai":
                pip_packages.append("google-genai")
            else:
                other_packages.append(package)
                
        if pip_packages:
            commands.append("### pip install")
            commands.append(f"pip install {' '.join(pip_packages)}")
            commands.append("")
            
        if other_packages:
            commands.append("### Other packages")
            for package in other_packages:
                commands.append(f"# {package} - check documentation")
            commands.append("")
            
        commands.append("### Alternative: Install all dependencies")
        all_packages = []
        for pkg in missing:
            if pkg == "google.genai":
                all_packages.append("google-genai")
            else:
                all_packages.append(pkg)
        commands.append(f"pip install {' '.join(all_packages)}")
        
        return "\n".join(commands)
    
    def verify_api_connectivity(self) -> Dict[str, bool]:
        """
        Test API connectivity for available providers.
        
        Returns:
            Dictionary mapping provider names to connectivity status
        """
        results = {}
        
        # Test Gemini connectivity
        if self._check_package_version("google.genai", "1.0.0"):
            results["gemini"] = self._test_gemini_connectivity()
        else:
            results["gemini"] = False
            
        # Test OpenAI connectivity
        if self._check_package_version("openai", "1.0.0"):
            results["openai"] = self._test_openai_connectivity()
        else:
            results["openai"] = False
            
        return results
    
    def _test_gemini_connectivity(self) -> bool:
        """Test Gemini API connectivity."""
        try:
            from .env_manager import get_env_manager
            env_manager = get_env_manager()
            api_keys = env_manager.load_api_keys()
            
            if "GEMINI_API_KEY" not in api_keys:
                return False
                
            # Try to import and initialize client
            try:
                from google import genai
                client = genai.Client(api_key=api_keys["GEMINI_API_KEY"])
            except ImportError:
                return False
            
            # Make a minimal test call
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="test"
            )
            
            return bool(response.text)
            
        except Exception as e:
            logger.debug(f"Gemini connectivity test failed: {e}")
            return False
    
    def _test_openai_connectivity(self) -> bool:
        """Test OpenAI API connectivity."""
        try:
            from .env_manager import get_env_manager
            env_manager = get_env_manager()
            api_keys = env_manager.load_api_keys()
            
            if "OPENAI_API_KEY" not in api_keys:
                return False
                
            # Try to import and initialize client
            from openai import OpenAI
            client = OpenAI(api_key=api_keys["OPENAI_API_KEY"])
            
            # Make a minimal test call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            
            return bool(response.choices)
            
        except Exception as e:
            logger.debug(f"OpenAI connectivity test failed: {e}")
            return False
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """
        Get comprehensive dependency status.
        
        Returns:
            Dictionary with detailed dependency information
        """
        package_status = self.check_python_packages()
        connectivity_status = self.verify_api_connectivity()
        
        # Categorize packages
        missing_required = []
        missing_optional = []
        available_required = []
        available_optional = []
        
        for package, is_available in package_status.items():
            if package in self.REQUIRED_PACKAGES:
                if is_available:
                    available_required.append(package)
                else:
                    missing_required.append(package)
            else:
                if is_available:
                    available_optional.append(package)
                else:
                    missing_optional.append(package)
                    
        return {
            "packages": package_status,
            "connectivity": connectivity_status,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "available_required": available_required,
            "available_optional": available_optional,
            "can_run_research": len(missing_required) == 0,
            "has_llm_support": len(available_optional) > 0,
        }
    
    def check_system_requirements(self) -> Dict[str, bool]:
        """
        Check basic system requirements.
        
        Returns:
            Dictionary of system requirement status
        """
        return {
            "python_version": sys.version_info >= (3, 8),
            "network_access": self._test_network_access(),
            "cache_directory": self._test_cache_directory(),
        }
    
    def _test_network_access(self) -> bool:
        """Test basic network connectivity."""
        try:
            import urllib.request
            urllib.request.urlopen("https://duckduckgo.com", timeout=5)
            return True
        except Exception:
            return False
    
    def _test_cache_directory(self) -> bool:
        """Test if cache directory is writable."""
        try:
            cache_dir = Path.home() / ".cache" / "opencode" / "research"
            cache_dir.mkdir(parents=True, exist_ok=True)
            test_file = cache_dir / "test_write"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception:
            return False


# Global instance
_dependency_checker = None


def get_dependency_checker() -> DependencyChecker:
    """Get or create the global dependency checker instance."""
    global _dependency_checker
    if _dependency_checker is None:
        _dependency_checker = DependencyChecker()
    return _dependency_checker
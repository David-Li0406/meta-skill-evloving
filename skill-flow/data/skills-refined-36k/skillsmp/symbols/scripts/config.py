#!/usr/bin/env python3
"""
Symbol Configuration Loader

Provides project-agnostic configuration for the symbols system. Loads and validates
configuration from JSON files, enabling customization of symbol extraction paths,
domains, and settings.

Usage:
    from config import get_config

    config = get_config()
    symbols_dir = config.get_symbols_dir()
    ui_file = config.get_domain_file("ui")
    service_file = config.get_api_layer_file("services")

Configuration File:
    Place symbols.config.json in the .claude/skills/symbols/ directory.
    The configuration must conform to symbols-config-schema.json.

Features:
    - JSON Schema validation on load
    - Singleton pattern for efficient reuse
    - Helpful error messages for missing/invalid config
    - Path resolution relative to project root
    - Domain and layer file lookup
    - Extraction settings access
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal
from dataclasses import dataclass, field


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""

    pass


@dataclass
class DomainConfig:
    """Configuration for a single domain."""

    file: str
    description: str
    test_file: Optional[str] = None
    enabled: bool = True


@dataclass
class LayerConfig:
    """Configuration for a single API layer."""

    file: str
    description: str
    enabled: bool = True


@dataclass
class ExtractionConfig:
    """Configuration for symbol extraction."""

    directories: List[str]
    extensions: List[str]
    excludes: List[str] = field(default_factory=list)
    exclude_tests: bool = True
    exclude_private: bool = False


@dataclass
class MetadataConfig:
    """Optional metadata about the configuration."""

    version: Optional[str] = None
    author: Optional[str] = None
    last_updated: Optional[str] = None
    description: Optional[str] = None


class SymbolConfig:
    """
    Symbol system configuration loader and accessor.

    Loads configuration from symbols.config.json and provides convenient
    methods for accessing paths, domains, layers, and extraction settings.

    Attributes:
        project_name: Name of the project
        symbols_dir: Directory where symbol files are stored
        domains: Dictionary of domain configurations
        api_layers: Dictionary of API layer configurations (optional)
        extraction: Dictionary of extraction configurations by language
        metadata: Optional metadata about the configuration
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration from JSON file.

        Args:
            config_path: Path to configuration file (default: auto-detect)

        Raises:
            ConfigurationError: If config file is missing or invalid
        """
        if config_path is None:
            config_path = self._find_config_file()

        self._config_path = config_path
        self._project_root = self._find_project_root()
        self._raw_config = self._load_config()
        self._validate_config()
        self._parse_config()

    def _find_config_file(self) -> Path:
        """
        Locate the symbols.config.json file.

        Searches in:
        1. .claude/skills/symbols/symbols.config.json (default location)
        2. Current directory
        3. Parent directories up to project root

        Returns:
            Path to configuration file

        Raises:
            ConfigurationError: If config file cannot be found
        """
        # Try default location first
        default_path = Path(".claude/skills/symbols/symbols.config.json")
        if default_path.exists():
            return default_path

        # Try current directory
        current_path = Path("symbols.config.json")
        if current_path.exists():
            return current_path

        # Search parent directories
        search_path = Path.cwd()
        for _ in range(10):  # Limit search depth
            config_path = search_path / ".claude/skills/symbols/symbols.config.json"
            if config_path.exists():
                return config_path

            # Check if we hit project root
            if (search_path / ".git").exists() or search_path == search_path.parent:
                break

            search_path = search_path.parent

        raise ConfigurationError(
            "Configuration file not found. Expected symbols.config.json at:\n"
            "  - .claude/skills/symbols/symbols.config.json (recommended)\n"
            "  - Current directory\n"
            "  - Any parent directory up to project root"
        )

    def _find_project_root(self) -> Path:
        """
        Find the project root directory.

        Looks for common markers like .git, package.json, pyproject.toml.

        Returns:
            Path to project root

        Raises:
            ConfigurationError: If project root cannot be determined
        """
        search_path = Path.cwd()
        for _ in range(10):  # Limit search depth
            # Check for common project root markers
            if any(
                (search_path / marker).exists()
                for marker in [".git", "package.json", "pyproject.toml", "setup.py"]
            ):
                return search_path

            if search_path == search_path.parent:
                break

            search_path = search_path.parent

        # Fallback to current directory if no root found
        return Path.cwd()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file.

        Returns:
            Raw configuration dictionary

        Raises:
            ConfigurationError: If file cannot be loaded or parsed
        """
        try:
            with open(self._config_path) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in configuration file {self._config_path}: {e}"
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load configuration from {self._config_path}: {e}"
            )

    def _validate_config(self) -> None:
        """
        Validate configuration against schema.

        Performs basic structural validation. For full JSON Schema validation,
        use the validate_schema.py script.

        Raises:
            ConfigurationError: If required fields are missing or invalid
        """
        required_fields = ["projectName", "symbolsDir", "domains", "extraction"]
        missing_fields = [
            field for field in required_fields if field not in self._raw_config
        ]

        if missing_fields:
            raise ConfigurationError(
                f"Missing required fields in configuration: {', '.join(missing_fields)}"
            )

        # Validate domains structure
        if not isinstance(self._raw_config["domains"], dict):
            raise ConfigurationError("'domains' must be an object/dictionary")

        if not self._raw_config["domains"]:
            raise ConfigurationError("At least one domain must be configured")

        for domain_name, domain_config in self._raw_config["domains"].items():
            if "file" not in domain_config:
                raise ConfigurationError(
                    f"Domain '{domain_name}' is missing required 'file' field"
                )
            if "description" not in domain_config:
                raise ConfigurationError(
                    f"Domain '{domain_name}' is missing required 'description' field"
                )

        # Validate extraction structure
        if not isinstance(self._raw_config["extraction"], dict):
            raise ConfigurationError("'extraction' must be an object/dictionary")

        for lang in ["python", "typescript"]:
            if lang not in self._raw_config["extraction"]:
                raise ConfigurationError(
                    f"Extraction configuration missing '{lang}' section"
                )

            lang_config = self._raw_config["extraction"][lang]
            if "directories" not in lang_config or "extensions" not in lang_config:
                raise ConfigurationError(
                    f"Extraction '{lang}' missing required 'directories' or 'extensions'"
                )

    def _parse_config(self) -> None:
        """Parse and store configuration in structured format."""
        self.project_name: str = self._raw_config["projectName"]
        self.symbols_dir: Path = self._project_root / self._raw_config["symbolsDir"]

        # Parse domains
        self.domains: Dict[str, DomainConfig] = {}
        for name, config in self._raw_config["domains"].items():
            self.domains[name] = DomainConfig(
                file=config["file"],
                description=config["description"],
                test_file=config.get("testFile"),
                enabled=config.get("enabled", True),
            )

        # Parse API layers (optional)
        self.api_layers: Dict[str, LayerConfig] = {}
        if "apiLayers" in self._raw_config:
            for name, config in self._raw_config["apiLayers"].items():
                self.api_layers[name] = LayerConfig(
                    file=config["file"],
                    description=config["description"],
                    enabled=config.get("enabled", True),
                )

        # Parse extraction configs
        self.extraction: Dict[str, ExtractionConfig] = {}
        for lang, config in self._raw_config["extraction"].items():
            self.extraction[lang] = ExtractionConfig(
                directories=config["directories"],
                extensions=config["extensions"],
                excludes=config.get("excludes", []),
                exclude_tests=config.get("excludeTests", True),
                exclude_private=config.get("excludePrivate", False),
            )

        # Parse metadata (optional)
        if "metadata" in self._raw_config:
            meta = self._raw_config["metadata"]
            self.metadata = MetadataConfig(
                version=meta.get("version"),
                author=meta.get("author"),
                last_updated=meta.get("lastUpdated"),
                description=meta.get("description"),
            )
        else:
            self.metadata = MetadataConfig()

    def get_symbols_dir(self) -> Path:
        """
        Get the symbols directory path.

        Returns:
            Absolute path to symbols directory
        """
        return self.symbols_dir

    def get_domain_file(self, domain: str) -> Path:
        """
        Get the symbol file path for a specific domain.

        Args:
            domain: Domain name (e.g., "ui", "web", "api", "shared")

        Returns:
            Absolute path to domain symbol file

        Raises:
            ConfigurationError: If domain not found or disabled
        """
        domain = domain.lower()

        if domain not in self.domains:
            available = ", ".join(self.domains.keys())
            raise ConfigurationError(
                f"Domain '{domain}' not found in configuration. "
                f"Available domains: {available}"
            )

        domain_config = self.domains[domain]

        if not domain_config.enabled:
            raise ConfigurationError(f"Domain '{domain}' is disabled in configuration")

        return self.symbols_dir / domain_config.file

    def get_test_file(self, domain: str) -> Optional[Path]:
        """
        Get the test symbol file path for a specific domain.

        Args:
            domain: Domain name (e.g., "ui", "web", "api")

        Returns:
            Absolute path to test symbol file, or None if not configured

        Raises:
            ConfigurationError: If domain not found
        """
        domain = domain.lower()

        if domain not in self.domains:
            available = ", ".join(self.domains.keys())
            raise ConfigurationError(
                f"Domain '{domain}' not found in configuration. "
                f"Available domains: {available}"
            )

        domain_config = self.domains[domain]

        if domain_config.test_file:
            return self.symbols_dir / domain_config.test_file

        return None

    def get_api_layer_file(self, layer: str) -> Path:
        """
        Get the symbol file path for a specific API layer.

        Args:
            layer: Layer name (e.g., "routers", "services", "repositories")

        Returns:
            Absolute path to layer symbol file

        Raises:
            ConfigurationError: If layer not found, disabled, or not configured
        """
        layer = layer.lower()

        if not self.api_layers:
            raise ConfigurationError(
                "No API layers configured. Use get_domain_file('api') for unified API symbols."
            )

        if layer not in self.api_layers:
            available = ", ".join(self.api_layers.keys())
            raise ConfigurationError(
                f"API layer '{layer}' not found in configuration. "
                f"Available layers: {available}"
            )

        layer_config = self.api_layers[layer]

        if not layer_config.enabled:
            raise ConfigurationError(f"API layer '{layer}' is disabled in configuration")

        return self.symbols_dir / layer_config.file

    def get_domains(self) -> List[str]:
        """
        Get list of all configured domain names.

        Returns:
            List of domain names (enabled and disabled)
        """
        return list(self.domains.keys())

    def get_enabled_domains(self) -> List[str]:
        """
        Get list of enabled domain names.

        Returns:
            List of enabled domain names
        """
        return [name for name, config in self.domains.items() if config.enabled]

    def get_api_layers(self) -> List[str]:
        """
        Get list of all configured API layer names.

        Returns:
            List of layer names (enabled and disabled), or empty list if not configured
        """
        return list(self.api_layers.keys())

    def get_enabled_api_layers(self) -> List[str]:
        """
        Get list of enabled API layer names.

        Returns:
            List of enabled layer names, or empty list if not configured
        """
        return [name for name, config in self.api_layers.items() if config.enabled]

    def get_extraction_config(
        self, language: Literal["python", "typescript"]
    ) -> ExtractionConfig:
        """
        Get extraction configuration for a specific language.

        Args:
            language: Language name ("python" or "typescript")

        Returns:
            Extraction configuration for the language

        Raises:
            ConfigurationError: If language not configured
        """
        if language not in self.extraction:
            raise ConfigurationError(
                f"No extraction configuration for language '{language}'"
            )

        return self.extraction[language]

    def get_extraction_directories(self, language: Literal["python", "typescript"]) -> List[Path]:
        """
        Get absolute paths to extraction directories for a language.

        Args:
            language: Language name ("python" or "typescript")

        Returns:
            List of absolute directory paths

        Raises:
            ConfigurationError: If language not configured
        """
        config = self.get_extraction_config(language)
        return [self._project_root / directory for directory in config.directories]

    def __repr__(self) -> str:
        """String representation of configuration."""
        return (
            f"SymbolConfig(project='{self.project_name}', "
            f"domains={len(self.domains)}, "
            f"layers={len(self.api_layers)})"
        )


# Singleton instance
_config_instance: Optional[SymbolConfig] = None


def get_config(config_path: Optional[Path] = None, reload: bool = False) -> SymbolConfig:
    """
    Get the singleton configuration instance.

    Args:
        config_path: Path to configuration file (default: auto-detect)
        reload: Force reload of configuration (default: False)

    Returns:
        SymbolConfig instance

    Raises:
        ConfigurationError: If configuration is invalid or missing

    Examples:
        # Get default configuration
        config = get_config()

        # Force reload
        config = get_config(reload=True)

        # Use specific config file
        config = get_config(Path("custom.config.json"))
    """
    global _config_instance

    if _config_instance is None or reload:
        _config_instance = SymbolConfig(config_path)

    return _config_instance


def reset_config() -> None:
    """Reset the singleton configuration instance (useful for testing)."""
    global _config_instance
    _config_instance = None


if __name__ == "__main__":
    # Example usage
    try:
        config = get_config()
        print(f"Configuration loaded successfully: {config}")
        print(f"\nProject: {config.project_name}")
        print(f"Symbols directory: {config.get_symbols_dir()}")
        print(f"\nDomains: {', '.join(config.get_enabled_domains())}")

        # Show domain files
        for domain in config.get_enabled_domains():
            file_path = config.get_domain_file(domain)
            print(f"  - {domain}: {file_path}")

        # Show API layers if configured
        if config.get_api_layers():
            print(f"\nAPI Layers: {', '.join(config.get_enabled_api_layers())}")
            for layer in config.get_enabled_api_layers():
                file_path = config.get_api_layer_file(layer)
                print(f"  - {layer}: {file_path}")

        # Show extraction config
        print("\nExtraction Configuration:")
        for lang in ["python", "typescript"]:
            lang_config = config.get_extraction_config(lang)
            print(f"  {lang}:")
            print(f"    Directories: {', '.join(lang_config.directories)}")
            print(f"    Extensions: {', '.join(lang_config.extensions)}")
            print(f"    Exclude tests: {lang_config.exclude_tests}")

    except ConfigurationError as e:
        print(f"Configuration Error: {e}")
        exit(1)

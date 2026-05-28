#!/usr/bin/env python3
"""
Example: Using the Symbol Configuration System

This example demonstrates how to use the configuration system to access
symbol files, extraction settings, and domain configurations.

This is a demonstration of how symbol_tools.py will be updated in Task 2
to use the configuration system instead of hardcoded paths.
"""

from config import get_config, ConfigurationError
import json
from pathlib import Path


def example_basic_usage():
    """Example 1: Basic configuration access."""
    print("Example 1: Basic Configuration Access")
    print("=" * 50)

    # Load configuration (singleton pattern)
    config = get_config()

    print(f"Project: {config.project_name}")
    print(f"Symbols directory: {config.get_symbols_dir()}")
    print(f"Enabled domains: {', '.join(config.get_enabled_domains())}")
    print(f"API layers: {', '.join(config.get_enabled_api_layers())}")
    print()


def example_domain_files():
    """Example 2: Accessing domain symbol files."""
    print("Example 2: Accessing Domain Symbol Files")
    print("=" * 50)

    config = get_config()

    # Get UI domain file
    ui_file = config.get_domain_file("ui")
    print(f"UI symbols: {ui_file}")

    # Load and count symbols
    with open(ui_file) as f:
        ui_data = json.load(f)
        if "modules" in ui_data:
            total_symbols = sum(
                len(module.get("symbols", [])) for module in ui_data["modules"]
            )
        else:
            total_symbols = len(ui_data.get("symbols", []))

        print(f"  Total UI symbols: {total_symbols}")

    # Get API layer file (more efficient than full API)
    services_file = config.get_api_layer_file("services")
    print(f"\nAPI services layer: {services_file}")

    with open(services_file) as f:
        services_data = json.load(f)
        if "modules" in services_data:
            total_symbols = sum(
                len(module.get("symbols", [])) for module in services_data["modules"]
            )
        else:
            total_symbols = len(services_data.get("symbols", []))

        print(f"  Total service symbols: {total_symbols}")

    print()


def example_extraction_config():
    """Example 3: Using extraction configuration."""
    print("Example 3: Extraction Configuration")
    print("=" * 50)

    config = get_config()

    # Get Python extraction config
    python_config = config.get_extraction_config("python")
    print("Python extraction:")
    print(f"  Directories: {python_config.directories}")
    print(f"  Extensions: {python_config.extensions}")
    print(f"  Exclude tests: {python_config.exclude_tests}")
    print(f"  Exclude patterns: {len(python_config.excludes)} patterns")

    # Get absolute paths to extraction directories
    python_dirs = config.get_extraction_directories("python")
    print(f"\nAbsolute paths:")
    for dir_path in python_dirs:
        exists = dir_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_path}")

    print()


def example_migration_pattern():
    """Example 4: How to migrate from hardcoded paths."""
    print("Example 4: Migration from Hardcoded Paths")
    print("=" * 50)

    config = get_config()

    # OLD WAY (hardcoded in symbol_tools.py):
    # SYMBOLS_DIR = Path("ai")
    # SYMBOL_FILES = {
    #     "ui": SYMBOLS_DIR / "symbols-ui.json",
    #     "api": SYMBOLS_DIR / "symbols-api.json",
    # }

    # NEW WAY (using config):
    symbols_dir = config.get_symbols_dir()
    ui_file = config.get_domain_file("ui")
    api_file = config.get_domain_file("api")

    print("OLD (hardcoded):")
    print('  SYMBOLS_DIR = Path("ai")')
    print('  ui_file = SYMBOLS_DIR / "symbols-ui.json"')

    print("\nNEW (config-driven):")
    print("  config = get_config()")
    print("  ui_file = config.get_domain_file('ui')")

    print(f"\nResult: {ui_file}")
    print()


def example_error_handling():
    """Example 5: Error handling."""
    print("Example 5: Error Handling")
    print("=" * 50)

    config = get_config()

    # Try to get non-existent domain
    try:
        config.get_domain_file("nonexistent")
    except ConfigurationError as e:
        print(f"Expected error for invalid domain:")
        print(f"  {e}")

    # Try to get non-existent layer
    try:
        config.get_api_layer_file("controllers")
    except ConfigurationError as e:
        print(f"\nExpected error for invalid layer:")
        print(f"  {e}")

    print()


def example_conditional_features():
    """Example 6: Conditional features based on config."""
    print("Example 6: Conditional Features")
    print("=" * 50)

    config = get_config()

    # Check if API layers are configured
    if config.get_api_layers():
        print("API layers are configured:")
        for layer in config.get_enabled_api_layers():
            layer_file = config.get_api_layer_file(layer)
            print(f"  ✓ {layer}: {layer_file.name}")
    else:
        print("No API layers configured, using unified API file")

    # Check which domains have test files
    print("\nDomains with test files:")
    for domain in config.get_enabled_domains():
        test_file = config.get_test_file(domain)
        if test_file and test_file.exists():
            print(f"  ✓ {domain}: {test_file.name}")

    print()


if __name__ == "__main__":
    try:
        example_basic_usage()
        example_domain_files()
        example_extraction_config()
        example_migration_pattern()
        example_error_handling()
        example_conditional_features()

        print("=" * 50)
        print("All examples completed successfully!")
        print("\nNext steps:")
        print("  1. Review the configuration in symbols.config.json")
        print("  2. Update symbol_tools.py to use get_config() (Task 2)")
        print("  3. Update extraction scripts to use config (Task 3)")

    except ConfigurationError as e:
        print(f"\nConfiguration Error: {e}")
        exit(1)

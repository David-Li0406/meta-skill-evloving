#!/usr/bin/env python3
"""
Plugin Packager - Creates a distributable archive of a plugin
Usage:
python package_plugin.py <plugin-path> [output-directory]
Examples:
python package_plugin.py ./my-plugin
python package_plugin.py ./my-plugin ./dist
"""
import sys
import zipfile
from pathlib import Path
from validate_plugin import validate_plugin


# Files and directories to exclude from package
EXCLUDE_PATTERNS = [
    '.git/',
    '.gitignore',
    'dist/',
    '*.zip',
    '*.skill',
    '__pycache__/',
    '*.pyc',
    '.claude/settings.local.json',
    '.DS_Store',
]


def should_exclude(file_path, plugin_path):
    """Check if a file should be excluded from the package."""
    relative_path = file_path.relative_to(plugin_path)

    # Check exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        pattern_path = Path(pattern)

        # Match directory pattern
        if pattern.endswith('/'):
            if pattern_path in relative_path.parents or relative_path == pattern_path:
                return True

        # Match file pattern
        elif pattern_path.name == '*':
            # Wildcard extension match (e.g., *.zip)
            if relative_path.suffix == pattern_path.suffix:
                return True
        elif relative_path.name == pattern:
            return True

    return False


def package_plugin(plugin_path, output_dir=None):
    """
    Package a plugin folder into a .zip file.

    Args:
        plugin_path: Path to the plugin folder
        output_dir: Optional output directory (defaults to current directory)

    Returns:
        Path to the created archive, or None if error
    """
    plugin_path = Path(plugin_path).resolve()

    # Validate plugin folder exists
    if not plugin_path.exists():
        print(f"❌ Error: Plugin folder not found: {plugin_path}")
        return None

    if not plugin_path.is_dir():
        print(f"❌ Error: Path is not a directory: {plugin_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating plugin...")
    is_valid, errors, warnings = validate_plugin(plugin_path)

    if not is_valid:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  • {error}")
        print("\nPlease fix the validation errors before packaging.")
        return None

    print(f"✅ Plugin is valid!")

    if warnings:
        print(f"⚠️  {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  • {warning}")

    print()

    # Determine output location
    plugin_name = plugin_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    archive_filename = output_path / f"{plugin_name}.zip"

    # Create the archive file
    try:
        with zipfile.ZipFile(archive_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            excluded_count = 0

            # Walk through the plugin directory
            for file_path in plugin_path.rglob('*'):
                if file_path.is_file():
                    # Check if file should be excluded
                    if should_exclude(file_path, plugin_path):
                        excluded_count += 1
                        continue

                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(plugin_path.parent)
                    zipf.write(file_path, arcname)
                    file_count += 1
                    print(f" Added: {arcname}")

            if excluded_count > 0:
                print(f"\n Excluded {excluded_count} file(s) (.git, dist, etc.)")

        print(f"\n✅ Successfully packaged {file_count} file(s) to: {archive_filename}")
        return archive_filename

    except Exception as e:
        print(f"❌ Error creating archive: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_plugin.py <plugin-path> [output-directory]")
        print("\nExamples:")
        print(" python package_plugin.py ./my-plugin")
        print(" python package_plugin.py ./my-plugin ./dist")
        sys.exit(1)

    plugin_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging plugin: {plugin_path}")
    if output_dir:
        print(f" Output directory: {output_dir}")
    print()

    result = package_plugin(plugin_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

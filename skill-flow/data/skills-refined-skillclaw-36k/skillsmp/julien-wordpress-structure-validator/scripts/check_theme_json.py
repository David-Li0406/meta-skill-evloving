#!/usr/bin/env python3
"""
WordPress theme.json Validator
Validates theme.json structure, syntax, and content
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ThemeJsonValidator:
    """Validates WordPress theme.json files"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = None
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        """Run all validations"""
        print("=" * 50)
        print("WordPress theme.json Validator")
        print("=" * 50)
        print()
        print(f"File: {self.filepath}")
        print()

        # Check file exists
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            self._print_summary()
            return False

        # Parse JSON
        if not self._validate_json():
            self._print_summary()
            return False

        # Validate structure
        self._validate_version()
        self._validate_settings()
        self._validate_color_palette()
        self._validate_typography()
        self._validate_spacing()
        self._validate_styles()

        # Print results
        self._print_summary()

        return len(self.errors) == 0

    def _validate_json(self) -> bool:
        """Validate JSON syntax"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print("✅ Valid JSON syntax")
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parse error: {e}")
            print(f"❌ ERROR: {e}")
            return False

    def _validate_version(self):
        """Check version field"""
        print()
        print("=== Version Check ===")
        print()

        if 'version' not in self.data:
            self.warnings.append("'version' field missing")
            print("⚠️  WARNING: 'version' field missing")
        else:
            version = self.data['version']
            if version not in [2, 3]:
                self.warnings.append(f"Unusual version: {version} (expected 2 or 3)")
                print(f"⚠️  WARNING: Version {version} (expected 2 or 3)")
            else:
                print(f"✅ Version: {version}")

    def _validate_settings(self):
        """Check settings structure"""
        print()
        print("=== Settings Structure ===")
        print()

        if 'settings' not in self.data:
            self.errors.append("'settings' object missing (required)")
            print("❌ ERROR: 'settings' object missing")
            return

        print("✅ 'settings' object present")

        settings = self.data['settings']

        # Check common settings sections
        sections = ['color', 'typography', 'spacing', 'layout']
        for section in sections:
            if section in settings:
                print(f"✅ settings.{section} defined")
            else:
                self.warnings.append(f"settings.{section} not defined")
                print(f"⚠️  WARNING: settings.{section} not defined")

    def _validate_color_palette(self):
        """Validate color palette"""
        print()
        print("=== Color Palette ===")
        print()

        if 'settings' not in self.data or 'color' not in self.data['settings']:
            print("⚠️  No color settings defined")
            return

        color_settings = self.data['settings']['color']

        if 'palette' not in color_settings:
            self.warnings.append("Color palette not defined")
            print("⚠️  WARNING: No color palette defined")
            return

        palette = color_settings['palette']

        if not isinstance(palette, list):
            self.errors.append("Palette must be an array")
            print("❌ ERROR: Palette must be an array")
            return

        print(f"✅ Palette with {len(palette)} colors")
        print()

        # Validate each color
        required_fields = ['slug', 'color', 'name']

        for i, color_def in enumerate(palette):
            # Check required fields
            missing_fields = [f for f in required_fields if f not in color_def]
            if missing_fields:
                self.errors.append(f"Color {i}: missing fields {missing_fields}")
                print(f"❌ ERROR: Color {i} missing: {', '.join(missing_fields)}")
                continue

            # Check hex color format
            color_value = color_def['color']
            if not color_value.startswith('#'):
                self.warnings.append(f"Color {i} ({color_def['slug']}): not hex format")
                print(f"⚠️  WARNING: {color_def['slug']} not hex format: {color_value}")

            # Check slug naming
            slug = color_def['slug']
            if ' ' in slug or slug != slug.lower():
                self.warnings.append(f"Color slug should be lowercase without spaces: {slug}")
                print(f"⚠️  WARNING: Slug '{slug}' should be lowercase, no spaces")

        # List all colors
        print()
        print("Colors defined:")
        for color_def in palette:
            if all(f in color_def for f in required_fields):
                print(f"  - {color_def['slug']}: {color_def['color']} ({color_def['name']})")

    def _validate_typography(self):
        """Validate typography settings"""
        print()
        print("=== Typography ===")
        print()

        if 'settings' not in self.data or 'typography' not in self.data['settings']:
            print("⚠️  No typography settings defined")
            return

        typo = self.data['settings']['typography']

        # Check font sizes
        if 'fontSizes' in typo:
            print(f"✅ Font sizes: {len(typo['fontSizes'])} defined")

            # List font sizes
            for size in typo['fontSizes']:
                if all(f in size for f in ['slug', 'size', 'name']):
                    print(f"  - {size['slug']}: {size['size']} ({size['name']})")
        else:
            print("⚠️  No font sizes defined")

        # Check font families
        if 'fontFamilies' in typo:
            print(f"✅ Font families: {len(typo['fontFamilies'])} defined")
        else:
            print("⚠️  No font families defined")

    def _validate_spacing(self):
        """Validate spacing settings"""
        print()
        print("=== Spacing ===")
        print()

        if 'settings' not in self.data or 'spacing' not in self.data['settings']:
            print("⚠️  No spacing settings defined")
            return

        spacing = self.data['settings']['spacing']

        if 'spacingSizes' in spacing:
            print(f"✅ Spacing scale: {len(spacing['spacingSizes'])} sizes defined")
        else:
            print("⚠️  No spacing sizes defined")

        if 'units' in spacing:
            units = spacing['units']
            print(f"✅ Units: {', '.join(units)}")
        else:
            print("⚠️  No spacing units defined")

    def _validate_styles(self):
        """Validate global styles"""
        print()
        print("=== Global Styles ===")
        print()

        if 'styles' not in self.data:
            print("⚠️  No global styles defined")
            return

        styles = self.data['styles']

        # Check common style properties
        if 'color' in styles:
            print("✅ Global colors defined")

        if 'typography' in styles:
            print("✅ Global typography defined")

        if 'spacing' in styles:
            print("✅ Global spacing defined")

    def _print_summary(self):
        """Print validation summary"""
        print()
        print("=" * 50)
        print("Validation Summary")
        print("=" * 50)
        print()
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if self.errors:
            print("Errors:")
            for error in self.errors:
                print(f"  ❌ {error}")
            print()

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
        elif not self.errors:
            print("⚠️  Validation passed with warnings")
        else:
            print("❌ Validation failed")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python check_theme_json.py <path/to/theme.json>")
        sys.exit(1)

    validator = ThemeJsonValidator(sys.argv[1])
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

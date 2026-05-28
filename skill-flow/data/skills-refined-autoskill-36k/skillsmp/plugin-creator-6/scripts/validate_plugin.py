#!/usr/bin/env python3
"""
Plugin Validator - Validates Claude Code plugin structure and content
Usage:
python validate_plugin.py <plugin-path>
Examples:
python validate_plugin.py ./my-plugin
python validate_plugin.py ~/.claude/plugins/code-reviewer
"""
import sys
import json
import re
import yaml
from pathlib import Path


def validate_json_file(file_path):
    """Validate JSON file syntax."""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_yaml_frontmatter(file_path):
    """Validate YAML frontmatter in markdown file."""
    try:
        content = file_path.read_text()
        if not content.startswith('---'):
            return False, "No YAML frontmatter found"

        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return False, "Invalid frontmatter format"

        frontmatter_text = match.group(1)

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if not isinstance(frontmatter, dict):
                return False, "Frontmatter must be a YAML dictionary"
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}"

        # Check for description field
        if 'description' not in frontmatter:
            return False, "Missing 'description' in frontmatter"

        return True, "Valid frontmatter"
    except Exception as e:
        return False, f"Error: {e}"


def validate_plugin(plugin_path):
    """
    Validate a plugin directory.

    Returns:
        (is_valid, errors, warnings)
    """
    plugin_path = Path(plugin_path).resolve()
    errors = []
    warnings = []

    # Check if directory exists
    if not plugin_path.exists():
        return False, ["Plugin directory not found"], []

    if not plugin_path.is_dir():
        return False, ["Path is not a directory"], []

    # Check .plugin.json
    plugin_json = plugin_path / '.plugin.json'
    if not plugin_json.exists():
        errors.append("Missing .plugin.json")
    else:
        valid, msg = validate_json_file(plugin_json)
        if not valid:
            errors.append(f".plugin.json: {msg}")
        else:
            # Load and validate plugin.json content
            with open(plugin_json) as f:
                plugin_data = json.load(f)

            # Check required fields
            for field in ['name', 'version', 'description']:
                if field not in plugin_data:
                    errors.append(f".plugin.json: Missing '{field}' field")

            # Check naming convention
            if 'name' in plugin_data:
                name = plugin_data['name']
                if not re.match(r'^[a-z0-9-]+$', name):
                    errors.append(f".plugin.json: Name '{name}' should be kebab-case")

            # Validate component arrays exist
            for array_field in ['commands', 'agents', 'skills']:
                if array_field in plugin_data:
                    if not isinstance(plugin_data[array_field], list):
                        errors.append(f".plugin.json: '{array_field}' must be an array")

            # Validate hooks object
            if 'hooks' in plugin_data:
                if not isinstance(plugin_data['hooks'], dict):
                    errors.append(".plugin.json: 'hooks' must be an object")

    # Check README.md
    readme = plugin_path / 'README.md'
    if not readme.exists():
        warnings.append("Missing README.md (recommended)")

    # Validate component directories
    component_dirs = {
        'commands': 'Command',
        'agents': 'Agent',
        'skills': 'Skill',
    }

    for dir_name, component_type in component_dirs.items():
        component_dir = plugin_path / dir_name
        if component_dir.exists():
            # Validate each component file
            for component_file in component_dir.glob('*.md'):
                valid, msg = validate_yaml_frontmatter(component_file)
                if not valid:
                    errors.append(f"{dir_name}/{component_file.name}: {msg}")

    # Validate hooks directory
    hooks_dir = plugin_path / 'hooks'
    if hooks_dir.exists():
        valid_events = [
            'pre-tool-use', 'post-tool-use', 'stop', 'subagent-stop',
            'session-start', 'session-end', 'user-prompt-submit',
            'pre-compact', 'notification'
        ]

        for event_dir in hooks_dir.iterdir():
            if event_dir.is_dir() and event_dir.name not in valid_events:
                warnings.append(f"hooks/{event_dir.name}: Unknown hook event type")

            # Validate hook files
            if event_dir.is_dir():
                for hook_file in event_dir.glob('*.md'):
                    valid, msg = validate_yaml_frontmatter(hook_file)
                    if not valid:
                        errors.append(f"hooks/{event_dir.name}/{hook_file.name}: {msg}")

    # Check that declared components exist
    if plugin_json.exists():
        with open(plugin_json) as f:
            plugin_data = json.load(f)

        for component_type in ['commands', 'agents', 'skills']:
            if component_type in plugin_data:
                for component_name in plugin_data[component_type]:
                    # For skills, check both file and directory structure
                    if component_type == 'skills':
                        skill_dir = plugin_path / 'skills' / component_name
                        skill_file = plugin_path / 'skills' / f"{component_name}.md"
                        skill_main = skill_dir / 'SKILL.md'

                        # Skill can be either a directory with SKILL.md or a .md file
                        if not skill_dir.exists() and not skill_file.exists():
                            errors.append(f".plugin.json declares skill/{component_name} but neither skill/{component_name}/ nor skill/{component_name}.md exists")
                        elif skill_dir.exists() and not skill_main.exists():
                            errors.append(f".plugin.json declares skill/{component_name} but SKILL.md not found in skill/{component_name}/")
                    else:
                        # Commands and agents are single files in plural directories
                        component_file = plugin_path / component_type / f"{component_name}.md"
                        if not component_file.exists():
                            errors.append(f".plugin.json declares {component_type}/{component_name}.md but file doesn't exist")

        if 'hooks' in plugin_data:
            for event_type, hooks in plugin_data['hooks'].items():
                event_dir_name = event_type.replace('([A-Z])', r'-\1').lower()
                event_dir = plugin_path / 'hooks' / event_dir_name
                for hook_name in hooks:
                    hook_file = event_dir / f"{hook_name}.md"
                    if not hook_file.exists():
                        errors.append(f".plugin.json declares hooks/{event_dir_name}/{hook_name}.md but file doesn't exist")

    return len(errors) == 0, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_plugin.py <plugin-path>")
        print("\nExamples:")
        print(" python validate_plugin.py ./my-plugin")
        print(" python validate_plugin.py ~/.claude/plugins/code-reviewer")
        sys.exit(1)

    plugin_path = sys.argv[1]
    print(f"🔍 Validating plugin: {plugin_path}\n")

    is_valid, errors, warnings = validate_plugin(plugin_path)

    if errors:
        print("❌ Errors found:")
        for error in errors:
            print(f"  • {error}")
        print()

    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  • {warning}")
        print()

    if is_valid:
        print("✅ Plugin validation passed!")
        if warnings:
            print(f"   ({len(warnings)} warning(s))")
        sys.exit(0)
    else:
        print(f"❌ Plugin validation failed with {len(errors)} error(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()

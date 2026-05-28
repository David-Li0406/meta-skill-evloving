#!/usr/bin/env python3
"""
List available Hashbrown component and server templates.
"""
import os
import json
from pathlib import Path

# Get the skill directory
SKILL_DIR = Path(__file__).parent.parent
ASSETS_DIR = SKILL_DIR / "assets"

def read_template_info(template_dir):
    """Read template README to extract description."""
    readme_path = template_dir / "README.md"
    if readme_path.exists():
        with open(readme_path, 'r') as f:
            lines = f.readlines()
            # Get first paragraph after title as description
            description = []
            skip_first = True
            for line in lines:
                line = line.strip()
                if skip_first and line.startswith('#'):
                    skip_first = False
                    continue
                if line and not line.startswith('#'):
                    description.append(line)
                    if len(description) >= 2:
                        break
            return ' '.join(description) if description else "No description available"
    return "No description available"

def list_templates():
    """List all available templates."""
    components_dir = ASSETS_DIR / "components"
    servers_dir = ASSETS_DIR / "servers"

    result = {
        "components": {},
        "servers": {}
    }

    # List component templates
    if components_dir.exists():
        for template_dir in sorted(components_dir.iterdir()):
            if template_dir.is_dir():
                name = template_dir.name
                description = read_template_info(template_dir)
                result["components"][name] = description

    # List server templates
    if servers_dir.exists():
        for template_dir in sorted(servers_dir.iterdir()):
            if template_dir.is_dir():
                name = template_dir.name
                description = read_template_info(template_dir)
                result["servers"][name] = description

    return result

def main():
    templates = list_templates()

    print("📦 Available Hashbrown Templates\n")

    print("🎨 Components:")
    if templates["components"]:
        for name, desc in templates["components"].items():
            print(f"  • {name}")
            print(f"    {desc}\n")
    else:
        print("  No component templates available\n")

    print("🖥️  Servers:")
    if templates["servers"]:
        for name, desc in templates["servers"].items():
            print(f"  • {name}")
            print(f"    {desc}\n")
    else:
        print("  No server templates available\n")

if __name__ == "__main__":
    main()

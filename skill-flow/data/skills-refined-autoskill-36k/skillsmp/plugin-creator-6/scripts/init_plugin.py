#!/usr/bin/env python3
"""
Plugin Initializer - Creates a new Claude Code plugin from template
Usage:
python init_plugin.py <plugin-name>
Examples:
python init_plugin.py code-reviewer
python init_plugin.py api-helper
"""
import sys
import json
from pathlib import Path

PLUGIN_JSON_TEMPLATE = """{{
  "name": "{plugin_name}",
  "version": "1.0.0",
  "description": "{description}",
  "author": "Your Name",
  "commands": [],
  "agents": [],
  "skills": [],
  "hooks": {{}}
}}
"""

README_TEMPLATE = """# {plugin_title}

{description}

## Installation

```bash
cp -r {plugin_name} ~/.claude/plugins/
```

## Features

- [TODO: List main features]

## Usage

[TODO: Provide usage examples]

## Components

- **Commands**: {command_count} commands
- **Agents**: {agent_count} agents
- **Skills**: {skill_count} skills
- **Hooks**: {hook_count} hooks

## Configuration

[TODO: Add configuration instructions if needed]
"""

COMMAND_TEMPLATE = """---
description: [TODO: Brief description shown in autocomplete]
args:
  - name: arg_name
    description: Argument description
    required: false
---

# Command Title

[TODO: Instructions for Claude]
"""

AGENT_TEMPLATE = """---
description: [TODO: When to trigger this agent]
color: blue
tools:
  - Read
  - Write
examples:
  - trigger: "User asks to..."
    action: "Launch this agent to..."
---

# Agent Title

You are a specialized agent for [purpose].

## Your Capabilities

[TODO: List capabilities]

## Your Process

[TODO: Add workflow steps]
"""

SKILL_TEMPLATE = """---
description: [TODO: What this skill provides and when to use it]
---

# Skill Title

[TODO: Comprehensive guide for domain]

## Quick Start

[TODO: Basic usage]
"""

HOOK_TEMPLATE = """---
description: [TODO: What this hook does]
---

# Hook Title

Instructions for what to do when this event occurs.
"""


def title_case(name):
    """Convert hyphenated name to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def init_plugin(plugin_name):
    """
    Initialize a new plugin directory with template files.

    Args:
        plugin_name: Name of the plugin (kebab-case)

    Returns:
        Path to created plugin directory, or None if error
    """
    # Validate plugin name
    if not all(c.isalnum() or c == '-' for c in plugin_name):
        print(f"❌ Error: Plugin name must be kebab-case (lowercase letters, digits, hyphens only)")
        return None

    # Determine plugin directory path
    plugin_dir = Path(plugin_name).resolve()

    # Check if directory already exists
    if plugin_dir.exists():
        print(f"❌ Error: Directory already exists: {plugin_dir}")
        return None

    # Create plugin directory
    try:
        plugin_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created plugin directory: {plugin_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create .plugin.json
    plugin_title = title_case(plugin_name)
    description = f"A plugin for {plugin_title}"
    plugin_json_content = PLUGIN_JSON_TEMPLATE.format(
        plugin_name=plugin_name,
        description=description
    )
    plugin_json_path = plugin_dir / '.plugin.json'
    try:
        plugin_json_path.write_text(plugin_json_content)
        print("✅ Created .plugin.json")
    except Exception as e:
        print(f"❌ Error creating .plugin.json: {e}")
        return None

    # Create README.md
    readme_content = README_TEMPLATE.format(
        plugin_name=plugin_name,
        plugin_title=plugin_title,
        description=description,
        command_count=0,
        agent_count=0,
        skill_count=0,
        hook_count=0
    )
    readme_path = plugin_dir / 'README.md'
    try:
        readme_path.write_text(readme_content)
        print("✅ Created README.md")
    except Exception as e:
        print(f"❌ Error creating README.md: {e}")
        return None

    # Create component directories
    try:
        commands_dir = plugin_dir / 'commands'
        commands_dir.mkdir(exist_ok=True)
        print("✅ Created commands/ directory")

        agents_dir = plugin_dir / 'agents'
        agents_dir.mkdir(exist_ok=True)
        print("✅ Created agents/ directory")

        skills_dir = plugin_dir / 'skills'
        skills_dir.mkdir(exist_ok=True)
        print("✅ Created skills/ directory")

        hooks_dir = plugin_dir / 'hooks'
        hooks_dir.mkdir(exist_ok=True)

        # Create hook event subdirectories
        for event in ['pre-tool-use', 'post-tool-use', 'stop', 'subagent-stop',
                      'session-start', 'session-end', 'user-prompt-submit',
                      'pre-compact', 'notification']:
            (hooks_dir / event).mkdir(exist_ok=True)
        print("✅ Created hooks/ directory with event subdirectories")
    except Exception as e:
        print(f"❌ Error creating component directories: {e}")
        return None

    # Create example component files
    try:
        # Example command
        example_command = commands_dir / 'example-command.md'
        example_command.write_text(COMMAND_TEMPLATE)
        print("✅ Created commands/example-command.md")

        # Example agent
        example_agent = agents_dir / 'example-agent.md'
        example_agent.write_text(AGENT_TEMPLATE)
        print("✅ Created agents/example-agent.md")

        # Example skill
        example_skill = skills_dir / 'example-skill.md'
        example_skill.write_text(SKILL_TEMPLATE)
        print("✅ Created skills/example-skill.md")

        # Example hook
        example_hook = hooks_dir / 'pre-tool-use' / 'example-hook.md'
        example_hook.write_text(HOOK_TEMPLATE)
        print("✅ Created hooks/pre-tool-use/example-hook.md")
    except Exception as e:
        print(f"❌ Error creating example files: {e}")
        return None

    # Print next steps
    print(f"\n✅ Plugin '{plugin_name}' initialized successfully at {plugin_dir}")
    print("\nDirectory structure:")
    print(f" {plugin_name}/")
    print(f" ├── .plugin.json")
    print(f" ├── README.md")
    print(f" ├── commands/")
    print(f" ├── agents/")
    print(f" ├── skills/")
    print(f" └── hooks/")
    print(f"     ├── pre-tool-use/")
    print(f"     ├── post-tool-use/")
    print(f"     └── ...")
    print("\nNext steps:")
    print("1. Edit .plugin.json with accurate plugin information")
    print("2. Implement or delete example component files")
    print("3. Update README.md with proper documentation")
    print("4. Run validation: python validate_plugin.py")

    return plugin_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: python init_plugin.py <plugin-name>")
        print("\nPlugin name requirements:")
        print(" - Kebab-case (e.g., 'code-reviewer')")
        print(" - Lowercase letters, digits, and hyphens only")
        print(" - No spaces or special characters")
        print("\nExamples:")
        print(" python init_plugin.py code-reviewer")
        print(" python init_plugin.py api-helper")
        sys.exit(1)

    plugin_name = sys.argv[1]
    print(f"🚀 Initializing plugin: {plugin_name}\n")

    result = init_plugin(plugin_name)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

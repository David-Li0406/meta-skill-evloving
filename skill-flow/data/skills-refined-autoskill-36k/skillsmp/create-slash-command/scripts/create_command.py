#!/usr/bin/env python3
"""
Create a new slash command file in .agents/commands/

Usage:
    create_command.py <command-name> [--workflow <workflow-name>]

Examples:
    create_command.py my-new-command
    create_command.py research --workflow research
"""

import sys
from pathlib import Path


COMMAND_TEMPLATE = """# {command_title} (Command)

## Instructions

1. You will receive a prompt or context for this workflow.

2. Using only `.devagent/**`, follow the workflow steps and write outputs under `.devagent/workspace/` as the workflow specifies.

3. Follow the `.devagent/core/workflows/{workflow_name}.md` workflow and execute it based on the following input:

---

**Input Context:**
"""


def title_case_command_name(command_name):
    """Convert hyphenated command name to Title Case for display."""
    return ' '.join(word.capitalize() for word in command_name.split('-'))


def create_command(command_name, workflow_name=None):
    """
    Create a new command file in .agents/commands/

    Args:
        command_name: Name of the command (kebab-case)
        workflow_name: Name of the workflow file (defaults to command_name)

    Returns:
        Path to created command file, or None if error
    """
    # Default workflow name to command name if not provided
    if workflow_name is None:
        workflow_name = command_name

    # Determine paths - find project root by looking for .agents directory
    script_path = Path(__file__).resolve()
    current = script_path.parent
    project_root = None
    
    # Walk up the directory tree to find project root (contains .agents directory)
    while current != current.parent:
        if (current / '.agents').exists():
            project_root = current
            break
        current = current.parent
    
    if project_root is None:
        print("❌ Error: Could not find project root (directory containing .agents/)")
        return None
    
    commands_dir = project_root / '.agents' / 'commands'
    command_file = commands_dir / f'{command_name}.md'

    # Check if command already exists
    if command_file.exists():
        print(f"❌ Error: Command file already exists: {command_file}")
        return None

    # Ensure commands directory exists
    commands_dir.mkdir(parents=True, exist_ok=True)

    # Create command file
    command_title = title_case_command_name(command_name)
    command_content = COMMAND_TEMPLATE.format(
        command_title=command_title,
        workflow_name=workflow_name
    )

    try:
        command_file.write_text(command_content)
        print(f"✅ Created command file: {command_file}")
        return command_file
    except Exception as e:
        print(f"❌ Error creating command file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: create_command.py <command-name> [--workflow <workflow-name>]")
        print("\nExamples:")
        print("  create_command.py my-new-command")
        print("  create_command.py research --workflow research")
        sys.exit(1)

    command_name = sys.argv[1]
    workflow_name = None

    # Parse optional workflow argument
    if '--workflow' in sys.argv:
        idx = sys.argv.index('--workflow')
        if idx + 1 < len(sys.argv):
            workflow_name = sys.argv[idx + 1]

    print(f"🚀 Creating command: {command_name}")
    if workflow_name:
        print(f"   Workflow: {workflow_name}")
    print()

    result = create_command(command_name, workflow_name)

    if result:
        print(f"\n✅ Command '{command_name}' created successfully")
        print("\nNext steps:")
        print(f"1. Create symlink: ln -sf ../../.agents/commands/{command_name}.md .cursor/commands/{command_name}.md")
        print("2. Update .agents/commands/README.md with the new command")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

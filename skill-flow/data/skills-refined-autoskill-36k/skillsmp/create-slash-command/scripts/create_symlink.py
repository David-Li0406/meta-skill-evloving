#!/usr/bin/env python3
"""
Create a symlink for a command file from .agents/commands/ to .cursor/commands/

Usage:
    create_symlink.py <command-name>

Examples:
    create_symlink.py my-new-command
    create_symlink.py research
"""

import sys
from pathlib import Path


def create_symlink(command_name):
    """
    Create a symlink for a command file.

    Args:
        command_name: Name of the command (kebab-case)

    Returns:
        Path to created symlink, or None if error
    """
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
    
    agents_commands_dir = project_root / '.agents' / 'commands'
    cursor_commands_dir = project_root / '.cursor' / 'commands'
    command_file = agents_commands_dir / f'{command_name}.md'
    symlink_path = cursor_commands_dir / f'{command_name}.md'

    # Check if command file exists
    if not command_file.exists():
        print(f"❌ Error: Command file does not exist: {command_file}")
        print("   Create the command file first using create_command.py")
        return None

    # Ensure cursor commands directory exists
    cursor_commands_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing symlink or file if it exists
    if symlink_path.exists() or symlink_path.is_symlink():
        if symlink_path.is_symlink():
            symlink_path.unlink()
            print(f"ℹ️  Removed existing symlink: {symlink_path}")
        else:
            print(f"⚠️  Warning: File exists at symlink location: {symlink_path}")
            response = input("   Remove it and create symlink? (y/N): ")
            if response.lower() != 'y':
                print("   Aborted")
                return None
            symlink_path.unlink()

    # Create relative symlink
    try:
        # Calculate relative path from cursor/commands to agents/commands
        relative_path = Path('../../.agents/commands') / f'{command_name}.md'
        symlink_path.symlink_to(relative_path)
        print(f"✅ Created symlink: {symlink_path}")
        print(f"   → {relative_path}")
        return symlink_path
    except Exception as e:
        print(f"❌ Error creating symlink: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: create_symlink.py <command-name>")
        print("\nExamples:")
        print("  create_symlink.py my-new-command")
        print("  create_symlink.py research")
        sys.exit(1)

    command_name = sys.argv[1]

    print(f"🚀 Creating symlink for command: {command_name}")
    print()

    result = create_symlink(command_name)

    if result:
        print(f"\n✅ Symlink for '{command_name}' created successfully")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

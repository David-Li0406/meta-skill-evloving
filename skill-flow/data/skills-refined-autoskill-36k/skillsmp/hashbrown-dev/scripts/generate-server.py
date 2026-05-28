#!/usr/bin/env python3
"""
Generate a Hashbrown Node.js server from a template.

Usage:
    python generate-server.py <template-name> [output-dir]

Example:
    python generate-server.py basic-chat-server ./backend
"""
import sys
import shutil
from pathlib import Path

# Get the skill directory
SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "servers"

def generate_server(template_name, output_dir="."):
    """Generate a server from a template."""
    template_dir = TEMPLATES_DIR / template_name

    if not template_dir.exists():
        print(f"❌ Error: Template '{template_name}' not found")
        print(f"\n💡 Available templates:")
        for t in sorted(TEMPLATES_DIR.iterdir()):
            if t.is_dir():
                print(f"   • {t.name}")
        return False

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Copy the entire template directory
    dest_path = output_path / template_name
    if dest_path.exists():
        print(f"⚠️  Warning: {dest_path} already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return False
        shutil.rmtree(dest_path)

    shutil.copytree(template_dir, dest_path)

    print(f"✅ Server generated: {dest_path}")

    # Show setup instructions
    print(f"\n📦 Next steps:")
    print(f"  1. cd {dest_path}")
    print(f"  2. npm install")
    print(f"  3. Set environment variables (see .env.example if present)")
    print(f"  4. npm start")

    # Show README if it exists
    readme_path = dest_path / "README.md"
    if readme_path.exists():
        print(f"\n📖 See {readme_path} for detailed instructions")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate-server.py <template-name> [output-dir]")
        print("\nExample:")
        print("  python generate-server.py basic-chat-server ./backend")
        print("\n💡 Run 'python list-templates.py' to see available templates")
        sys.exit(1)

    template_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    success = generate_server(template_name, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

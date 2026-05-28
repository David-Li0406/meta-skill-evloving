#!/usr/bin/env python3
"""
Initialize a new custom Amp command with boilerplate.

Usage:
    init_command.py <command-name> --type <markdown|bash|python> [--scope <local|global>]

Examples:
    init_command.py pr-review --type markdown --scope local
    init_command.py daily-standup --type bash --scope global
    init_command.py work-on-issue --type python --scope local
"""

import argparse
import os
from pathlib import Path
import stat
import sys

MARKDOWN_TEMPLATE = """# {title}

## SYSTEM

You are a [role description]. Your objectives are to:
• [objective 1]
• [objective 2]
• [objective 3]

## ASSISTANT RULES

1. [Rule 1]
2. [Rule 2]
3. [Rule 3]

## OUTPUT FORMAT

```markdown
[Expected output structure]
```

## TASK

[Main prompt content here]
"""

BASH_TEMPLATE = """#!/bin/bash
# {title}
# Usage: {name} [arguments]

set -euo pipefail

# Check for required arguments
if [ $# -eq 0 ]; then
    echo "Usage: {name} <argument>"
    echo "Example: {name} value"
    exit 2
fi

ARG="$1"

# Find project root (where .agents directory is located)
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Load .env if present
if [ -f "$ROOT_DIR/.env" ]; then
    set -a
    source "$ROOT_DIR/.env"
    set +a
fi

# Check for required environment variables
# if [ -z "${{API_KEY:-}}" ]; then
#     echo "Error: API_KEY environment variable not set"
#     exit 1
# fi

# Main logic here
cat <<EOF
# {title}

Processing: $ARG

[Your dynamic prompt content here]

EOF
"""

PYTHON_TEMPLATE = '''#!/usr/bin/env python3
"""
{title}

Usage: {name} [arguments]
"""

import argparse
import os
import sys
from pathlib import Path


def find_project_root() -> Path:
    """Find project root by looking for .agents directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".agents").exists():
            return current
        current = current.parent
    return Path.cwd()


def load_env(root: Path) -> None:
    """Load .env file if present."""
    env_file = root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="{title}")
    parser.add_argument("argument", help="Description of argument")
    args = parser.parse_args()

    root = find_project_root()
    load_env(root)

    # Check for required environment variables
    # api_key = os.environ.get("API_KEY")
    # if not api_key:
    #     print("Error: API_KEY environment variable not set", file=sys.stderr)
    #     return 1

    # Generate prompt output
    print(f"""# {title}

Processing: {{args.argument}}

[Your dynamic prompt content here]

""")

    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def get_output_path(name: str, cmd_type: str, scope: str) -> Path:
    """Determine the output path for the command."""
    extension = ".md" if cmd_type == "markdown" else ""
    filename = f"{name}{extension}"

    if scope == "global":
        xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        base = Path(xdg_config) / "amp" / "commands"
    else:
        base = Path.cwd() / ".agents" / "commands"

    return base / filename


def create_command(name: str, cmd_type: str, scope: str) -> Path:
    """Create a new command file with appropriate template."""
    output_path = get_output_path(name, cmd_type, scope)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"Error: Command already exists at {output_path}", file=sys.stderr)
        sys.exit(1)

    title = name.replace("-", " ").replace("_", " ").title()
    template_vars = {"name": name, "title": title}

    if cmd_type == "markdown":
        content = MARKDOWN_TEMPLATE.format(**template_vars)
    elif cmd_type == "bash":
        content = BASH_TEMPLATE.format(**template_vars)
    elif cmd_type == "python":
        content = PYTHON_TEMPLATE.format(**template_vars)
    else:
        print(f"Error: Unknown type '{cmd_type}'", file=sys.stderr)
        sys.exit(1)

    output_path.write_text(content)

    if cmd_type in ("bash", "python"):
        current_mode = output_path.stat().st_mode
        output_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a new custom Amp command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pr-review --type markdown --scope local
  %(prog)s daily-standup --type bash --scope global
  %(prog)s work-on-issue --type python --scope local
        """,
    )
    parser.add_argument("name", help="Command name (becomes the filename)")
    parser.add_argument(
        "--type",
        "-t",
        choices=["markdown", "bash", "python"],
        required=True,
        help="Command type",
    )
    parser.add_argument(
        "--scope",
        "-s",
        choices=["local", "global"],
        default="local",
        help="Command scope (default: local)",
    )

    args = parser.parse_args()

    output_path = create_command(args.name, args.type, args.scope)

    print(f"✅ Created command: {output_path}")
    print()
    print("Next steps:")
    print(f"  1. Edit {output_path} to customize the command")
    print("  2. Test via Command Palette (Cmd/Alt-Shift-A or Ctrl-O)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

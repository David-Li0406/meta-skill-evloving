#!/usr/bin/env python3
"""
CLAUDE.md Symbols Integration Updater

Safely updates CLAUDE.md files with symbols skill integration guidance without
overwriting existing content. Uses HTML comment markers for safe replacement
and preserves all non-symbols content.

Usage:
    # Update CLAUDE.md in current project
    python update_claude_md.py

    # Dry run to see what would change
    python update_claude_md.py --dry-run

    # Force update without markers (use with caution)
    python update_claude_md.py --force

    # Specify project root
    python update_claude_md.py --project-root /path/to/project

    # No backup
    python update_claude_md.py --no-backup

Features:
    - Safe merging using HTML comment markers
    - Preserves all existing content
    - Configuration-driven content generation
    - Detailed change reporting
    - Backup creation before modification
    - Markdown structure validation

Markers:
    The script uses these HTML comment markers to identify sections:
    <!-- BEGIN SYMBOLS SECTION -->
    ...symbols guidance content...
    <!-- END SYMBOLS SECTION -->

    If markers exist, content between them is replaced.
    If markers don't exist, content is inserted after "Prime directives" or "Key Guidance".
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

# Try to import colorama for terminal colors (optional)
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    class Fore:
        RED = ""
        YELLOW = ""
        GREEN = ""
        CYAN = ""
        MAGENTA = ""
        RESET = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""

    HAS_COLOR = False

# Import config from same directory
try:
    from config import get_config, ConfigurationError
except ImportError:
    print("Error: config.py not found. Please ensure config.py is in the same directory.")
    sys.exit(2)


# Markers for safe section replacement
BEGIN_MARKER = "<!-- BEGIN SYMBOLS SECTION -->"
END_MARKER = "<!-- END SYMBOLS SECTION -->"

# Template file location
TEMPLATE_FILE = ".claude/skills/symbols/templates/claude_md_integration.md"


def print_color(text: str, color: str = "", style: str = "") -> None:
    """Print colored text if colorama is available."""
    if HAS_COLOR:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def find_project_root() -> Path:
    """
    Find the project root directory.

    Looks for common markers like .git, package.json, pyproject.toml.

    Returns:
        Path to project root

    Raises:
        RuntimeError: If project root cannot be determined
    """
    search_path = Path.cwd()
    for _ in range(10):  # Limit search depth
        # Check for common project root markers
        if any(
            (search_path / marker).exists()
            for marker in [".git", "package.json", "pyproject.toml", "setup.py"]
        ):
            return search_path

        if search_path == search_path.parent:
            break

        search_path = search_path.parent

    # Fallback to current directory if no root found
    return Path.cwd()


def load_template(project_root: Path) -> str:
    """
    Load the integration template file.

    Args:
        project_root: Project root directory

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    template_path = project_root / TEMPLATE_FILE

    if not template_path.exists():
        raise FileNotFoundError(
            f"Template file not found at {template_path}\n"
            f"Expected: {TEMPLATE_FILE}"
        )

    with open(template_path) as f:
        return f.read()


def load_symbol_stats(config: Any) -> Dict[str, int]:
    """
    Load symbol counts from symbol files.

    Args:
        config: SymbolConfig instance

    Returns:
        Dictionary mapping domain names to symbol counts
    """
    stats = {}

    # Load domain stats
    for domain_name in config.get_enabled_domains():
        try:
            file_path = config.get_domain_file(domain_name)
            if file_path.exists():
                with open(file_path) as f:
                    data = json.load(f)

                # Count symbols
                symbol_count = 0
                if "modules" in data:
                    for module in data["modules"]:
                        symbol_count += len(module.get("symbols", []))
                elif "symbols" in data:
                    symbol_count = len(data["symbols"])

                stats[domain_name] = symbol_count
        except Exception as e:
            print_color(f"Warning: Could not load stats for {domain_name}: {e}", Fore.YELLOW)
            stats[domain_name] = 0

    # Load API layer stats
    for layer_name in config.get_enabled_api_layers():
        try:
            file_path = config.get_api_layer_file(layer_name)
            if file_path.exists():
                with open(file_path) as f:
                    data = json.load(f)

                # Count symbols
                symbol_count = 0
                if "modules" in data:
                    for module in data["modules"]:
                        symbol_count += len(module.get("symbols", []))
                elif "symbols" in data:
                    symbol_count = len(data["symbols"])

                stats[f"api-{layer_name}"] = symbol_count
        except Exception as e:
            print_color(f"Warning: Could not load stats for api-{layer_name}: {e}", Fore.YELLOW)
            stats[f"api-{layer_name}"] = 0

    return stats


def generate_symbol_files_section(config: Any, stats: Dict[str, int]) -> str:
    """
    Generate the "Symbol Files" section with domain listings.

    Args:
        config: SymbolConfig instance
        stats: Dictionary of symbol counts per domain

    Returns:
        Formatted markdown section
    """
    lines = []

    # Domain-specific files
    lines.append("**Domain-Specific Files (Recommended):**")

    for domain_name in config.get_enabled_domains():
        domain_config = config.domains[domain_name]
        count = stats.get(domain_name, 0)
        file_path = f"{config._raw_config['symbolsDir']}/{domain_config.file}"
        description = domain_config.description

        lines.append(f"- `{file_path}` - {description} - {count:,} symbols")

        # Add test file if present
        if domain_config.test_file:
            test_count = stats.get(f"{domain_name}-tests", 0)
            test_path = f"{config._raw_config['symbolsDir']}/{domain_config.test_file}"
            lines.append(f"- `{test_path}` - {domain_name.upper()} test helpers (on-demand) - {test_count:,} symbols")

    # API layer files (if configured)
    if config.get_api_layers():
        lines.append("")
        lines.append("**API Layer Files (Granular Access):**")

        for layer_name in config.get_enabled_api_layers():
            layer_config = config.api_layers[layer_name]
            count = stats.get(f"api-{layer_name}", 0)
            file_path = f"{config._raw_config['symbolsDir']}/{layer_config.file}"
            description = layer_config.description

            lines.append(f"- `{file_path}` - {description} - {count:,} symbols")

    return "\n".join(lines)


def generate_layer_tags_section(config: Any) -> str:
    """
    Generate the layer tags section based on symbol data.

    Args:
        config: SymbolConfig instance

    Returns:
        Formatted markdown section
    """
    # Try to detect actual layers from symbol files
    # For now, provide a sensible default based on typical architecture
    return """- API layers: `router`, `service`, `repository`, `schema`, `model`, `core`, `auth`, `middleware`, `observability`
- Frontend layers: `component`, `hook`, `page`, `util`
- Test layer: `test`"""


def populate_template(template: str, config: Any, stats: Dict[str, int]) -> str:
    """
    Populate template placeholders with actual project data.

    Args:
        template: Template content with placeholders
        config: SymbolConfig instance
        stats: Symbol count statistics

    Returns:
        Template with placeholders replaced
    """
    # Generate dynamic sections
    symbol_files_section = generate_symbol_files_section(config, stats)
    layer_tags_section = generate_layer_tags_section(config)

    # Replace placeholders
    content = template.replace("{{PROJECT_NAME}}", config.project_name)
    content = content.replace("{{SYMBOLS_DIR}}", config._raw_config["symbolsDir"])
    content = content.replace("{{SYMBOL_FILES_SECTION}}", symbol_files_section)
    content = content.replace("{{LAYER_TAGS}}", layer_tags_section)

    return content


def find_symbols_section(content: str) -> Optional[Tuple[int, int]]:
    """
    Find existing symbols section marked by HTML comments.

    Args:
        content: CLAUDE.md content

    Returns:
        Tuple of (start_index, end_index) if markers found, None otherwise
    """
    begin_match = re.search(re.escape(BEGIN_MARKER), content)
    end_match = re.search(re.escape(END_MARKER), content)

    if begin_match and end_match:
        return (begin_match.start(), end_match.end())

    return None


def find_insertion_point(content: str) -> Optional[int]:
    """
    Find the best insertion point for symbols section.

    Looks for:
    1. End of "Prime directives" section
    2. End of "Key Guidance" section
    3. After first level-2 heading

    Args:
        content: CLAUDE.md content

    Returns:
        Character index for insertion, or None if no suitable location found
    """
    lines = content.split('\n')

    # Strategy 1: After "Prime directives" section
    for i, line in enumerate(lines):
        if re.match(r'^##\s+(Prime directives|Prime Directives)', line, re.IGNORECASE):
            # Find next level-2 heading
            for j in range(i + 1, len(lines)):
                if re.match(r'^##\s+\w', lines[j]):
                    # Insert before next section
                    insertion_line = j
                    return sum(len(lines[k]) + 1 for k in range(insertion_line))

    # Strategy 2: After "Key Guidance" section
    for i, line in enumerate(lines):
        if re.match(r'^##\s+(Key Guidance|Key guidance)', line, re.IGNORECASE):
            # Find next level-2 heading
            for j in range(i + 1, len(lines)):
                if re.match(r'^##\s+\w', lines[j]):
                    # Insert before next section
                    insertion_line = j
                    return sum(len(lines[k]) + 1 for k in range(insertion_line))

    # Strategy 3: After first level-2 heading
    for i, line in enumerate(lines):
        if re.match(r'^##\s+\w', line):
            # Find next level-2 heading
            for j in range(i + 1, len(lines)):
                if re.match(r'^##\s+\w', lines[j]):
                    # Insert before next section
                    insertion_line = j
                    return sum(len(lines[k]) + 1 for k in range(insertion_line))

    return None


def detect_existing_symbols_content(content: str) -> bool:
    """
    Detect if symbols guidance already exists (without markers).

    Args:
        content: CLAUDE.md content

    Returns:
        True if symbols-related content detected
    """
    indicators = [
        r'codebase-explorer',
        r'symbols system',
        r'Symbol Files',
        r'symbols-\w+\.json',
        r'Symbols vs Explore',
    ]

    for pattern in indicators:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False


def update_claude_md(
    project_root: Path,
    template_content: str,
    force: bool = False,
    dry_run: bool = False,
    no_backup: bool = False
) -> Dict[str, Any]:
    """
    Update CLAUDE.md with symbols integration guidance.

    Args:
        project_root: Project root directory
        template_content: Populated template content
        force: Force update without markers (use with caution)
        dry_run: Show what would change without modifying files
        no_backup: Skip backup creation

    Returns:
        Dictionary with update results and statistics
    """
    claude_md_path = project_root / "CLAUDE.md"
    result = {
        "exists": claude_md_path.exists(),
        "modified": False,
        "action": None,
        "backup_created": False,
        "lines_added": 0,
        "lines_modified": 0,
        "lines_preserved": 0,
        "errors": [],
        "warnings": [],
    }

    # Check if file exists
    if not result["exists"]:
        result["errors"].append(f"CLAUDE.md not found at {claude_md_path}")
        return result

    # Read existing content
    try:
        with open(claude_md_path) as f:
            original_content = f.read()
    except Exception as e:
        result["errors"].append(f"Failed to read CLAUDE.md: {e}")
        return result

    original_lines = len(original_content.split('\n'))

    # Check for existing markers
    section_range = find_symbols_section(original_content)

    if section_range:
        # Replace content between markers
        start_idx, end_idx = section_range
        new_content = (
            original_content[:start_idx] +
            f"{BEGIN_MARKER}\n{template_content}\n{END_MARKER}" +
            original_content[end_idx:]
        )
        result["action"] = "updated"
        result["lines_modified"] = template_content.count('\n') + 2

    elif force or not detect_existing_symbols_content(original_content):
        # Find insertion point
        insertion_idx = find_insertion_point(original_content)

        if insertion_idx is None:
            result["errors"].append(
                "Could not find suitable insertion point. "
                "Add markers manually or use --force."
            )
            return result

        # Insert new section with markers
        new_content = (
            original_content[:insertion_idx] +
            f"\n{BEGIN_MARKER}\n{template_content}\n{END_MARKER}\n\n" +
            original_content[insertion_idx:]
        )
        result["action"] = "inserted"
        result["lines_added"] = template_content.count('\n') + 4

    else:
        # Symbols content exists but no markers
        result["warnings"].append(
            "Symbols guidance appears to exist but no markers found. "
            "Use --force to insert anyway or add markers manually."
        )
        result["action"] = "skipped"
        return result

    new_lines = len(new_content.split('\n'))
    result["lines_preserved"] = original_lines - result["lines_modified"]

    # Validate markdown structure (basic check)
    if new_content.count(BEGIN_MARKER) != new_content.count(END_MARKER):
        result["errors"].append("Marker mismatch detected - update aborted")
        return result

    # Dry run: show diff but don't modify
    if dry_run:
        result["action"] = f"{result['action']} (dry-run)"
        result["preview_lines"] = new_content.split('\n')[:50]  # First 50 lines
        return result

    # Create backup
    if not no_backup:
        try:
            backup_path = claude_md_path.with_suffix('.md.bak')
            shutil.copy2(claude_md_path, backup_path)
            result["backup_created"] = True
            result["backup_path"] = str(backup_path)
        except Exception as e:
            result["warnings"].append(f"Failed to create backup: {e}")

    # Write updated content
    try:
        with open(claude_md_path, 'w') as f:
            f.write(new_content)
        result["modified"] = True
    except Exception as e:
        result["errors"].append(f"Failed to write CLAUDE.md: {e}")
        return result

    return result


def print_report(result: Dict[str, Any], verbose: bool = False) -> None:
    """
    Print formatted update report.

    Args:
        result: Update result dictionary
        verbose: Print detailed information
    """
    # Header
    print_color("\n" + "=" * 70, Fore.CYAN, Style.BRIGHT)
    print_color("CLAUDE.md Symbols Integration Update", Fore.CYAN, Style.BRIGHT)
    print_color("=" * 70, Fore.CYAN, Style.BRIGHT)

    # Status
    if result["errors"]:
        print_color("\nStatus: FAILED", Fore.RED, Style.BRIGHT)
        for error in result["errors"]:
            print_color(f"  Error: {error}", Fore.RED)
        return

    if result["warnings"]:
        print_color("\nStatus: SKIPPED", Fore.YELLOW, Style.BRIGHT)
        for warning in result["warnings"]:
            print_color(f"  Warning: {warning}", Fore.YELLOW)
        return

    if result["action"] and "dry-run" in result["action"]:
        print_color("\nStatus: DRY RUN", Fore.CYAN, Style.BRIGHT)
    elif result["modified"]:
        print_color("\nStatus: SUCCESS", Fore.GREEN, Style.BRIGHT)
    else:
        print_color("\nStatus: NO CHANGES", Fore.YELLOW, Style.BRIGHT)

    # Action taken
    if result["action"]:
        action_verb = result["action"].replace("-", " ").title()
        print(f"Action: {action_verb}")

    # Statistics
    if result["lines_added"] > 0:
        print_color(f"Lines Added: {result['lines_added']}", Fore.GREEN)
    if result["lines_modified"] > 0:
        print_color(f"Lines Modified: {result['lines_modified']}", Fore.YELLOW)
    if result["lines_preserved"] > 0:
        print(f"Lines Preserved: {result['lines_preserved']}")

    # Backup info
    if result["backup_created"]:
        print_color(f"Backup Created: {result['backup_path']}", Fore.CYAN)

    # Summary sections
    print("\nSummary:")
    if "updated" in result.get("action", ""):
        print("  - Updated: 'Agent Delegation Strategy' section")
        print("  - Updated: 'Symbol Files' section")
        print("  - Preserved: All other content")
    elif "inserted" in result.get("action", ""):
        print("  - Inserted: 'Agent Delegation Strategy' section")
        print("  - Inserted: 'Symbol Files' section")
        print("  - Preserved: All existing content")

    # Preview (dry run)
    if verbose and "preview_lines" in result:
        print_color("\nPreview (first 50 lines):", Fore.CYAN, Style.BRIGHT)
        print_color("-" * 70, Fore.CYAN)
        for i, line in enumerate(result["preview_lines"][:50], 1):
            print(f"{i:3d} | {line}")
        if len(result["preview_lines"]) > 50:
            print_color("...(truncated)", Fore.CYAN)

    print_color("\n" + "=" * 70, Fore.CYAN, Style.BRIGHT)


def main() -> int:
    """
    Main entry point for update command.

    Returns:
        Exit code (0=success, 1=warnings, 2=errors)
    """
    parser = argparse.ArgumentParser(
        description="Update CLAUDE.md with symbols integration guidance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update CLAUDE.md in current project
  python update_claude_md.py

  # Dry run to see what would change
  python update_claude_md.py --dry-run

  # Force update without markers
  python update_claude_md.py --force

  # Specify project root
  python update_claude_md.py --project-root /path/to/project

  # No backup
  python update_claude_md.py --no-backup

Exit Codes:
  0 = Success (file updated)
  1 = Warnings (skipped update)
  2 = Errors (update failed)
        """
    )

    parser.add_argument(
        "--project-root",
        type=Path,
        help="Path to project root (default: auto-detect)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without modifying files"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if symbols content already exists"
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup creation before modifying"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed information"
    )

    args = parser.parse_args()

    # Determine project root
    try:
        if args.project_root:
            project_root = args.project_root.resolve()
        else:
            project_root = find_project_root()

        if args.verbose:
            print(f"Project root: {project_root}")

    except Exception as e:
        print_color(f"Error: Could not determine project root: {e}", Fore.RED)
        return 2

    # Load configuration
    try:
        config = get_config()
        if args.verbose:
            print(f"Configuration loaded: {config}")
    except ConfigurationError as e:
        print_color(f"Configuration error: {e}", Fore.RED)
        print("\nMake sure symbols.config.json exists in .claude/skills/symbols/")
        return 2

    # Load template
    try:
        template = load_template(project_root)
        if args.verbose:
            print(f"Template loaded from {TEMPLATE_FILE}")
    except FileNotFoundError as e:
        print_color(f"Error: {e}", Fore.RED)
        return 2

    # Load symbol statistics
    try:
        stats = load_symbol_stats(config)
        if args.verbose:
            print(f"Symbol statistics loaded: {sum(stats.values())} total symbols")
    except Exception as e:
        print_color(f"Warning: Could not load symbol statistics: {e}", Fore.YELLOW)
        stats = {}

    # Populate template
    try:
        populated_template = populate_template(template, config, stats)
        if args.verbose:
            print(f"Template populated with project data")
    except Exception as e:
        print_color(f"Error: Failed to populate template: {e}", Fore.RED)
        return 2

    # Update CLAUDE.md
    result = update_claude_md(
        project_root,
        populated_template,
        force=args.force,
        dry_run=args.dry_run,
        no_backup=args.no_backup
    )

    # Print report
    print_report(result, verbose=args.verbose)

    # Return appropriate exit code
    if result["errors"]:
        return 2
    elif result["warnings"]:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())

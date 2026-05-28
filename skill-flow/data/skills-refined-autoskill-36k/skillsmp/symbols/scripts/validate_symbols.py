#!/usr/bin/env python3
"""
Symbol Validation Command

Comprehensive health checks for symbol files with detailed reporting and actionable
error messages. Validates file existence, schema compliance, freshness, duplicates,
and source file integrity.

Usage:
    # Validate all domains
    python scripts/validate_symbols.py

    # Validate specific domain
    python scripts/validate_symbols.py --domain=ui

    # Verbose output
    python scripts/validate_symbols.py --verbose

    # CI/CD integration (exit 2 on errors, 1 on warnings, 0 on success)
    python scripts/validate_symbols.py || exit $?

Exit Codes:
    0 = Valid (no errors or warnings)
    1 = Warnings present (stale files, minor issues)
    2 = Errors present (missing files, schema violations, missing sources)
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Try to import colorama for terminal colors (optional)
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    # Fallback: no colors
    class Fore:
        RED = ""
        YELLOW = ""
        GREEN = ""
        CYAN = ""
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


# Schema validation rules (required fields per Schema v2.0)
REQUIRED_FIELDS = {"name", "kind", "line", "signature", "summary", "layer"}
VALID_KINDS = {"function", "async_function", "class", "method", "async_method", "component", "hook", "interface", "type", "variable"}
VALID_LAYERS = {
    "router", "service", "repository", "schema", "model", "core",
    "auth", "middleware", "observability", "component", "hook",
    "page", "util", "test", "unknown"
}

# Validation thresholds
WARNING_AGE_DAYS = 7
ERROR_AGE_DAYS = 14


def print_color(text: str, color: str = "", style: str = "") -> None:
    """Print colored text if colorama is available."""
    if HAS_COLOR:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f}m"


def validate_symbol_schema(symbol: Dict[str, Any], file_path: Path, module_path: str) -> List[str]:
    """
    Validate a single symbol against Schema v2.0 requirements.

    Args:
        symbol: Symbol dictionary to validate
        file_path: Path to symbol file (for error messages)
        module_path: Module path from symbol file (for error messages)

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check required fields
    missing_fields = REQUIRED_FIELDS - set(symbol.keys())
    if missing_fields:
        errors.append(
            f"Missing fields in {module_path} symbol '{symbol.get('name', 'UNKNOWN')}': "
            f"{', '.join(sorted(missing_fields))}"
        )

    # Validate kind
    kind = symbol.get("kind", "").lower()
    if kind and kind not in VALID_KINDS:
        errors.append(
            f"Invalid kind '{kind}' in {module_path} symbol '{symbol.get('name', 'UNKNOWN')}'. "
            f"Valid kinds: {', '.join(sorted(VALID_KINDS))}"
        )

    # Validate layer
    layer = symbol.get("layer", "").lower()
    if layer and layer not in VALID_LAYERS:
        errors.append(
            f"Invalid layer '{layer}' in {module_path} symbol '{symbol.get('name', 'UNKNOWN')}'. "
            f"Valid layers: {', '.join(sorted(VALID_LAYERS))}"
        )

    # Validate line number
    line = symbol.get("line")
    if line is not None and (not isinstance(line, int) or line < 1):
        errors.append(
            f"Invalid line number '{line}' in {module_path} symbol '{symbol.get('name', 'UNKNOWN')}'"
        )

    return errors


def check_source_file_exists(symbol_file_path: Path, source_path: str, project_root: Path) -> bool:
    """
    Check if the source file referenced in the symbol still exists.

    Args:
        symbol_file_path: Path to the symbol file
        source_path: Source file path from symbol (relative or absolute)
        project_root: Project root directory

    Returns:
        True if source file exists, False otherwise
    """
    # Try as absolute path first
    source = Path(source_path)
    if source.exists():
        return True

    # Try relative to project root
    source = project_root / source_path
    if source.exists():
        return True

    # Try relative to symbol file
    source = symbol_file_path.parent / source_path
    if source.exists():
        return True

    return False


def validate_domain_file(
    domain_name: str,
    file_path: Path,
    project_root: Path,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Validate a single domain symbol file.

    Args:
        domain_name: Domain name (e.g., "ui", "api")
        file_path: Path to symbol file
        project_root: Project root directory
        verbose: Print detailed progress

    Returns:
        Validation report for this domain
    """
    report = {
        "exists": file_path.exists(),
        "readable": False,
        "symbols_count": 0,
        "last_modified": None,
        "age_days": None,
        "errors": [],
        "warnings": [],
        "duplicates": 0,
        "missing_sources": 0,
    }

    # Check existence
    if not report["exists"]:
        report["errors"].append(f"Symbol file not found: {file_path}")
        return report

    # Check readability
    try:
        with open(file_path) as f:
            data = json.load(f)
        report["readable"] = True
    except json.JSONDecodeError as e:
        report["errors"].append(f"Invalid JSON in {file_path}: {e}")
        return report
    except Exception as e:
        report["errors"].append(f"Failed to read {file_path}: {e}")
        return report

    # Get file age
    mtime = file_path.stat().st_mtime
    last_modified = datetime.fromtimestamp(mtime)
    report["last_modified"] = last_modified.isoformat()
    age = datetime.now() - last_modified
    report["age_days"] = age.days

    # Check freshness
    if age.days > ERROR_AGE_DAYS:
        report["errors"].append(
            f"Symbol file is {age.days} days old (threshold: {ERROR_AGE_DAYS} days). "
            f"Run symbol extraction to update."
        )
    elif age.days > WARNING_AGE_DAYS:
        report["warnings"].append(
            f"Symbol file is {age.days} days old (threshold: {WARNING_AGE_DAYS} days). "
            f"Consider running symbol extraction."
        )

    # Normalize schema format
    if "modules" in data:
        modules = data["modules"]
    elif "symbols" in data:
        # Convert flat format to hierarchical
        modules_dict = {}
        for symbol in data["symbols"]:
            path = symbol.get("path", "unknown")
            if path not in modules_dict:
                modules_dict[path] = {"path": path, "symbols": []}
            symbol_copy = {k: v for k, v in symbol.items() if k != "path"}
            modules_dict[path]["symbols"].append(symbol_copy)
        modules = list(modules_dict.values())
    else:
        report["errors"].append("Invalid symbol file format: missing 'modules' or 'symbols' key")
        return report

    # Track symbols for duplicate detection
    seen_symbols: Set[Tuple[str, str, int]] = set()
    duplicates: List[str] = []
    missing_sources: List[str] = []

    # Validate each module and symbol
    for module in modules:
        module_path = module.get("path", "unknown")

        # Check if source file exists
        if not check_source_file_exists(file_path, module_path, project_root):
            missing_sources.append(module_path)
            report["missing_sources"] += 1

        for symbol in module.get("symbols", []):
            report["symbols_count"] += 1

            # Schema validation
            schema_errors = validate_symbol_schema(symbol, file_path, module_path)
            report["errors"].extend(schema_errors)

            # Duplicate detection (same name + file + line)
            symbol_key = (
                symbol.get("name", ""),
                module_path,
                symbol.get("line", 0)
            )

            if symbol_key in seen_symbols:
                duplicates.append(
                    f"{symbol_key[0]} at {symbol_key[1]}:{symbol_key[2]}"
                )
                report["duplicates"] += 1
            else:
                seen_symbols.add(symbol_key)

    # Report duplicates
    if duplicates:
        report["warnings"].append(
            f"Found {len(duplicates)} duplicate symbols: {', '.join(duplicates[:5])}"
            + ("..." if len(duplicates) > 5 else "")
        )

    # Report missing sources
    if missing_sources:
        report["warnings"].append(
            f"Found {len(missing_sources)} stale source references: "
            f"{', '.join(missing_sources[:3])}"
            + ("..." if len(missing_sources) > 3 else "")
        )

    if verbose:
        print(f"  Validated {report['symbols_count']} symbols in {domain_name}")

    return report


def validate_symbols(
    domain: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Validate symbol files for all or specific domains.

    Args:
        domain: Specific domain to validate (None = all domains)
        verbose: Print detailed progress

    Returns:
        Validation report with status, errors, warnings, and statistics
    """
    start_time = time.time()

    # Load configuration
    try:
        config = get_config()
    except ConfigurationError as e:
        return {
            "status": "errors",
            "error": f"Configuration error: {e}",
            "domains": {},
            "summary": {
                "total_symbols": 0,
                "total_errors": 1,
                "total_warnings": 0,
                "domains_checked": 0,
                "validation_time": "0s",
            },
        }

    project_root = config._project_root

    # Determine domains to validate
    if domain:
        domains_to_check = [domain.lower()]
        # Validate domain exists in config
        if domain.lower() not in config.domains:
            return {
                "status": "errors",
                "error": f"Domain '{domain}' not found in configuration. "
                        f"Available: {', '.join(config.get_domains())}",
                "domains": {},
                "summary": {
                    "total_symbols": 0,
                    "total_errors": 1,
                    "total_warnings": 0,
                    "domains_checked": 0,
                    "validation_time": "0s",
                },
            }
    else:
        domains_to_check = config.get_enabled_domains()

    if verbose:
        print(f"\nValidating {len(domains_to_check)} domain(s)...")

    # Validate each domain
    domain_reports = {}
    total_errors = 0
    total_warnings = 0
    total_symbols = 0

    for domain_name in domains_to_check:
        try:
            file_path = config.get_domain_file(domain_name)
        except ConfigurationError as e:
            domain_reports[domain_name] = {
                "exists": False,
                "errors": [str(e)],
                "warnings": [],
                "symbols_count": 0,
            }
            total_errors += 1
            continue

        if verbose:
            print(f"\nValidating {domain_name} domain ({file_path})...")

        report = validate_domain_file(domain_name, file_path, project_root, verbose)
        domain_reports[domain_name] = report

        total_errors += len(report["errors"])
        total_warnings += len(report["warnings"])
        total_symbols += report["symbols_count"]

    # Also validate API layer files if present
    if config.get_api_layers() and (domain is None or domain.lower() == "api"):
        for layer_name in config.get_enabled_api_layers():
            try:
                file_path = config.get_api_layer_file(layer_name)
            except ConfigurationError as e:
                domain_reports[f"api-{layer_name}"] = {
                    "exists": False,
                    "errors": [str(e)],
                    "warnings": [],
                    "symbols_count": 0,
                }
                total_errors += 1
                continue

            if verbose:
                print(f"\nValidating API layer: {layer_name} ({file_path})...")

            report = validate_domain_file(f"api-{layer_name}", file_path, project_root, verbose)
            domain_reports[f"api-{layer_name}"] = report

            total_errors += len(report["errors"])
            total_warnings += len(report["warnings"])
            total_symbols += report["symbols_count"]

    # Determine overall status
    if total_errors > 0:
        status = "errors"
    elif total_warnings > 0:
        status = "warnings"
    else:
        status = "valid"

    # Build summary
    validation_time = time.time() - start_time

    return {
        "status": status,
        "domains": domain_reports,
        "summary": {
            "total_symbols": total_symbols,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "domains_checked": len(domain_reports),
            "validation_time": format_duration(validation_time),
        },
    }


def print_report(report: Dict[str, Any], verbose: bool = False) -> None:
    """
    Print formatted validation report to console.

    Args:
        report: Validation report from validate_symbols()
        verbose: Print detailed domain information
    """
    # Print header
    print_color("\n" + "=" * 70, Fore.CYAN, Style.BRIGHT)
    print_color("Symbol Validation Report", Fore.CYAN, Style.BRIGHT)
    print_color("=" * 70, Fore.CYAN, Style.BRIGHT)

    # Check for configuration errors
    if "error" in report:
        print_color(f"\nConfiguration Error:", Fore.RED, Style.BRIGHT)
        print_color(f"  {report['error']}", Fore.RED)
        return

    # Print summary
    summary = report["summary"]
    status = report["status"]

    print(f"\nStatus: ", end="")
    if status == "valid":
        print_color("VALID", Fore.GREEN, Style.BRIGHT)
    elif status == "warnings":
        print_color("WARNINGS", Fore.YELLOW, Style.BRIGHT)
    else:
        print_color("ERRORS", Fore.RED, Style.BRIGHT)

    print(f"\nDomains Checked: {summary['domains_checked']}")
    print(f"Total Symbols: {summary['total_symbols']:,}")
    print(f"Total Errors: {summary['total_errors']}")
    print(f"Total Warnings: {summary['total_warnings']}")
    print(f"Validation Time: {summary['validation_time']}")

    # Print domain details
    if verbose or status != "valid":
        print_color("\n" + "-" * 70, Fore.CYAN)
        print_color("Domain Details", Fore.CYAN, Style.BRIGHT)
        print_color("-" * 70, Fore.CYAN)

        for domain_name, domain_report in report["domains"].items():
            print(f"\n{domain_name.upper()}:")

            if not domain_report["exists"]:
                print_color("  Status: FILE NOT FOUND", Fore.RED, Style.BRIGHT)
            elif not domain_report["readable"]:
                print_color("  Status: NOT READABLE", Fore.RED, Style.BRIGHT)
            elif domain_report["errors"]:
                print_color(f"  Status: {len(domain_report['errors'])} ERRORS", Fore.RED, Style.BRIGHT)
            elif domain_report["warnings"]:
                print_color(f"  Status: {len(domain_report['warnings'])} WARNINGS", Fore.YELLOW, Style.BRIGHT)
            else:
                print_color("  Status: VALID", Fore.GREEN, Style.BRIGHT)

            print(f"  Symbols: {domain_report['symbols_count']:,}")

            if domain_report.get("last_modified"):
                age_str = f"{domain_report['age_days']} days old" if domain_report.get("age_days") else "unknown age"
                print(f"  Last Modified: {domain_report['last_modified']} ({age_str})")

            if domain_report.get("duplicates", 0) > 0:
                print(f"  Duplicates: {domain_report['duplicates']}")

            if domain_report.get("missing_sources", 0) > 0:
                print(f"  Stale Sources: {domain_report['missing_sources']}")

            # Print errors
            if domain_report["errors"]:
                print_color(f"\n  Errors ({len(domain_report['errors'])}):", Fore.RED, Style.BRIGHT)
                for error in domain_report["errors"][:10]:  # Limit to first 10
                    print_color(f"    - {error}", Fore.RED)
                if len(domain_report["errors"]) > 10:
                    print_color(f"    ... and {len(domain_report['errors']) - 10} more", Fore.RED)

            # Print warnings
            if domain_report["warnings"]:
                print_color(f"\n  Warnings ({len(domain_report['warnings'])}):", Fore.YELLOW, Style.BRIGHT)
                for warning in domain_report["warnings"][:5]:  # Limit to first 5
                    print_color(f"    - {warning}", Fore.YELLOW)
                if len(domain_report["warnings"]) > 5:
                    print_color(f"    ... and {len(domain_report['warnings']) - 5} more", Fore.YELLOW)

    # Print footer
    print_color("\n" + "=" * 70, Fore.CYAN, Style.BRIGHT)

    # Print recommendations
    if status == "errors":
        print_color("\nRecommended Actions:", Fore.RED, Style.BRIGHT)
        print("  1. Fix schema violations and missing files")
        print("  2. Run symbol extraction: python scripts/extract_symbols.py")
        print("  3. Re-validate: python scripts/validate_symbols.py")
    elif status == "warnings":
        print_color("\nRecommended Actions:", Fore.YELLOW, Style.BRIGHT)
        print("  1. Update stale symbol files: python scripts/extract_symbols.py")
        print("  2. Review and resolve duplicate symbols")
        print("  3. Clean up stale source references")
    else:
        print_color("\nAll symbol files are valid and up-to-date!", Fore.GREEN, Style.BRIGHT)


def main() -> int:
    """
    Main entry point for validation command.

    Returns:
        Exit code (0=success, 1=warnings, 2=errors)
    """
    parser = argparse.ArgumentParser(
        description="Validate symbol files for MeatyPrompts codebase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all domains
  python scripts/validate_symbols.py

  # Validate specific domain
  python scripts/validate_symbols.py --domain=ui

  # Verbose output
  python scripts/validate_symbols.py --verbose

  # CI/CD integration
  python scripts/validate_symbols.py || exit $?

Exit Codes:
  0 = Valid (no errors or warnings)
  1 = Warnings present (stale files, minor issues)
  2 = Errors present (missing files, schema violations)
        """
    )

    parser.add_argument(
        "--domain",
        type=str,
        help="Specific domain to validate (ui, web, api, shared)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed validation progress and domain information"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report in JSON format"
    )

    args = parser.parse_args()

    # Run validation
    report = validate_symbols(domain=args.domain, verbose=args.verbose)

    # Print report
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report, verbose=args.verbose)

    # Return appropriate exit code
    status = report["status"]
    if status == "errors":
        return 2
    elif status == "warnings":
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())

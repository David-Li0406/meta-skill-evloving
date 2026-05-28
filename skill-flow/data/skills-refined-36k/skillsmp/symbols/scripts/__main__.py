#!/usr/bin/env python3
"""
Unified Symbol Extraction Pipeline

Orchestrates the complete symbol extraction, tagging, splitting, and validation
workflow for the symbols system. Supports domain-specific extraction and incremental
processing.

Usage:
    python .claude/skills/symbols/scripts/__main__.py           # Full pipeline
    python .claude/skills/symbols/scripts/__main__.py --domain=api  # API only
    python .claude/skills/symbols/scripts/__main__.py --domain=ui --skip-validate  # UI without validation
    python .claude/skills/symbols/scripts/__main__.py --changed-only  # Incremental

Pipeline Steps:
    1. extract_typescript - Extract symbols from TypeScript/JavaScript (ui/web domains)
    2. extract_python - Extract symbols from Python (api domain)
    3. add_layer_tags - Add architectural layer tags to all symbols
    4. split_api_by_layer - Split API symbols into layer-based chunks
    5. validate_symbols - Validate all symbol files

Exit Codes:
    0 = Success (all steps completed without errors)
    1 = Warnings present (some steps had warnings but completed)
    2 = Errors present (one or more steps failed)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

# Import config from same directory
try:
    from .config import get_config, ConfigurationError
except ImportError:
    # Fallback for direct execution
    try:
        from config import get_config, ConfigurationError
    except ImportError:
        print("Error: config.py not found. Please ensure config.py is in the same directory.")
        sys.exit(2)


# Get script directory for module imports
SCRIPTS_DIR = Path(__file__).parent


class PipelineResult:
    """Result of a pipeline step execution."""

    def __init__(self, success: bool, message: str = "", warnings: int = 0, errors: int = 0):
        self.success = success
        self.message = message
        self.warnings = warnings
        self.errors = errors


def run_step(step_name: str, func: Callable[[], PipelineResult], verbose: bool = False) -> PipelineResult:
    """
    Execute a pipeline step with consistent output formatting.

    Args:
        step_name: Name of the step for display
        func: Callable that executes the step and returns PipelineResult
        verbose: Whether to print detailed output

    Returns:
        PipelineResult from the step execution
    """
    print(f"==> {step_name}")
    start_time = time.time()

    try:
        result = func()
        duration = time.time() - start_time

        if result.success:
            status = "done"
            if result.warnings > 0:
                status = f"done ({result.warnings} warnings)"
            print(f"    {status} ({duration:.1f}s)")
        else:
            print(f"    FAILED ({duration:.1f}s)")
            if result.message:
                print(f"    Error: {result.message}")

        return result

    except Exception as e:
        duration = time.time() - start_time
        print(f"    FAILED ({duration:.1f}s)")
        print(f"    Exception: {e}")
        return PipelineResult(success=False, message=str(e), errors=1)


def extract_typescript(
    config,
    domain: str,
    verbose: bool = False,
    changed_only: bool = False
) -> PipelineResult:
    """
    Extract symbols from TypeScript/JavaScript files.

    Args:
        config: SymbolConfig instance
        domain: Domain to extract (ui, web, or all)
        verbose: Show detailed output
        changed_only: Only process changed files (incremental mode)

    Returns:
        PipelineResult indicating success/failure
    """
    try:
        ts_config = config.get_extraction_config("typescript")
    except ConfigurationError as e:
        return PipelineResult(success=False, message=str(e), errors=1)

    directories = ts_config.directories
    if not directories:
        return PipelineResult(success=True, message="No TypeScript directories configured")

    # Determine which domains to extract
    domains_to_extract = []
    if domain == "all":
        # Extract for ui and web domains (TypeScript-based)
        for d in ["ui", "web"]:
            if d in config.domains and config.domains[d].enabled:
                domains_to_extract.append(d)
    elif domain in ["ui", "web"]:
        if domain in config.domains and config.domains[domain].enabled:
            domains_to_extract.append(domain)
    else:
        # Skip TypeScript extraction for non-TypeScript domains
        return PipelineResult(success=True, message=f"Skipping TypeScript extraction for domain: {domain}")

    if not domains_to_extract:
        return PipelineResult(success=True, message="No TypeScript domains to extract")

    total_warnings = 0
    total_errors = 0

    for target_domain in domains_to_extract:
        try:
            output_file = config.get_domain_file(target_domain)
        except ConfigurationError:
            continue

        # Get directories for this domain based on config
        extract_dirs = config.get_extraction_directories("typescript")

        # Filter directories that exist
        existing_dirs = [d for d in extract_dirs if d.exists()]

        if not existing_dirs:
            if verbose:
                print(f"    No existing directories found for {target_domain}")
            continue

        # Build extraction command
        for extract_dir in existing_dirs:
            cmd = [
                sys.executable,
                str(SCRIPTS_DIR / "extract_symbols_typescript.py"),
                str(extract_dir),
                f"--output={output_file}",
                "--pretty",
            ]

            if ts_config.exclude_tests:
                cmd.append("--exclude-tests")
            if ts_config.exclude_private:
                cmd.append("--exclude-private")

            if verbose:
                print(f"    Extracting from: {extract_dir}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=config._project_root
            )

            if result.returncode != 0:
                total_errors += 1
                if verbose:
                    print(f"    Error: {result.stderr}")
            elif "warning" in result.stderr.lower():
                total_warnings += 1

    if total_errors > 0:
        return PipelineResult(
            success=False,
            message=f"TypeScript extraction failed with {total_errors} errors",
            warnings=total_warnings,
            errors=total_errors
        )

    return PipelineResult(success=True, warnings=total_warnings)


def extract_python(
    config,
    domain: str,
    verbose: bool = False,
    changed_only: bool = False
) -> PipelineResult:
    """
    Extract symbols from Python files.

    Args:
        config: SymbolConfig instance
        domain: Domain to extract (api or all)
        verbose: Show detailed output
        changed_only: Only process changed files (incremental mode)

    Returns:
        PipelineResult indicating success/failure
    """
    # Only extract Python for 'api' domain or 'all'
    if domain not in ["all", "api"]:
        return PipelineResult(success=True, message=f"Skipping Python extraction for domain: {domain}")

    try:
        py_config = config.get_extraction_config("python")
    except ConfigurationError as e:
        return PipelineResult(success=False, message=str(e), errors=1)

    directories = py_config.directories
    if not directories:
        return PipelineResult(success=True, message="No Python directories configured")

    try:
        output_file = config.get_domain_file("api")
    except ConfigurationError as e:
        return PipelineResult(success=False, message=str(e), errors=1)

    # Get directories for extraction
    extract_dirs = config.get_extraction_directories("python")

    # Filter directories that exist
    existing_dirs = [d for d in extract_dirs if d.exists()]

    if not existing_dirs:
        return PipelineResult(success=True, message="No existing Python directories found")

    total_warnings = 0
    total_errors = 0

    for extract_dir in existing_dirs:
        cmd = [
            sys.executable,
            str(SCRIPTS_DIR / "extract_symbols_python.py"),
            str(extract_dir),
            f"--output={output_file}",
            "--pretty",
        ]

        if py_config.exclude_tests:
            cmd.append("--exclude-tests")
        if py_config.exclude_private:
            cmd.append("--exclude-private")

        if verbose:
            print(f"    Extracting from: {extract_dir}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=config._project_root
        )

        if result.returncode != 0:
            total_errors += 1
            if verbose:
                print(f"    Error: {result.stderr}")
        elif "warning" in result.stderr.lower():
            total_warnings += 1

    if total_errors > 0:
        return PipelineResult(
            success=False,
            message=f"Python extraction failed with {total_errors} errors",
            warnings=total_warnings,
            errors=total_errors
        )

    return PipelineResult(success=True, warnings=total_warnings)


def add_layer_tags_step(config, domain: str, verbose: bool = False) -> PipelineResult:
    """
    Add architectural layer tags to symbol files.

    Args:
        config: SymbolConfig instance
        domain: Domain to process (or 'all')
        verbose: Show detailed output

    Returns:
        PipelineResult indicating success/failure
    """
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "add_layer_tags.py"),
        "--all",
        "--inplace",
    ]

    if verbose:
        print(f"    Running: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=config._project_root
    )

    if result.returncode != 0:
        return PipelineResult(
            success=False,
            message=f"Layer tagging failed: {result.stderr}",
            errors=1
        )

    return PipelineResult(success=True)


def split_api_by_layer_step(config, verbose: bool = False) -> PipelineResult:
    """
    Split API symbols into layer-based files.

    Args:
        config: SymbolConfig instance
        verbose: Show detailed output

    Returns:
        PipelineResult indicating success/failure
    """
    # Check if API domain file exists
    try:
        api_file = config.get_domain_file("api")
    except ConfigurationError as e:
        return PipelineResult(success=False, message=str(e), errors=1)

    if not api_file.exists():
        return PipelineResult(
            success=True,
            message="API symbol file not found, skipping split"
        )

    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "split_api_by_layer.py"),
    ]

    if verbose:
        print(f"    Running: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=config._project_root
    )

    if result.returncode != 0:
        return PipelineResult(
            success=False,
            message=f"API split failed: {result.stderr}",
            errors=1
        )

    # Check for warnings in output
    warnings = 0
    if "warning" in result.stdout.lower() or "warning" in result.stderr.lower():
        warnings = 1

    return PipelineResult(success=True, warnings=warnings)


def validate_symbols_step(config, domain: str, verbose: bool = False) -> PipelineResult:
    """
    Validate all symbol files.

    Args:
        config: SymbolConfig instance
        domain: Domain to validate (or 'all')
        verbose: Show detailed output

    Returns:
        PipelineResult indicating success/failure
    """
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "validate_symbols.py"),
    ]

    if domain != "all":
        cmd.append(f"--domain={domain}")

    if verbose:
        cmd.append("--verbose")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=config._project_root
    )

    # Exit codes: 0=valid, 1=warnings, 2=errors
    if result.returncode == 2:
        return PipelineResult(
            success=False,
            message="Validation found errors",
            errors=1
        )
    elif result.returncode == 1:
        return PipelineResult(
            success=True,
            message="Validation found warnings",
            warnings=1
        )

    return PipelineResult(success=True)


def main() -> int:
    """
    Main entry point for the unified pipeline.

    Returns:
        Exit code (0=success, 1=warnings, 2=errors)
    """
    parser = argparse.ArgumentParser(
        description="Run unified symbol extraction pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--domain",
        choices=["all", "ui", "web", "api"],
        default="all",
        help="Which domain to process (default: all)"
    )

    parser.add_argument(
        "--skip-split",
        action="store_true",
        help="Skip the API layer split step"
    )

    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip the validation step"
    )

    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Only process changed files (incremental mode)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Load configuration
    print("Loading configuration...")
    try:
        config = get_config()
        print(f"  Project: {config.project_name}")
        print(f"  Symbols dir: {config.symbols_dir}")
    except ConfigurationError as e:
        print(f"Error: {e}")
        print("  Run 'python init_symbols.py' to initialize the symbols system")
        return 2

    print()

    # Track overall results
    total_warnings = 0
    total_errors = 0
    results: List[Tuple[str, PipelineResult]] = []

    # Step 1: Extract TypeScript symbols (for ui/web domains)
    if args.domain in ["all", "ui", "web"]:
        result = run_step(
            "extract_typescript",
            lambda: extract_typescript(config, args.domain, args.verbose, args.changed_only),
            args.verbose
        )
        results.append(("extract_typescript", result))
        total_warnings += result.warnings
        total_errors += result.errors

    # Step 2: Extract Python symbols (for api domain)
    if args.domain in ["all", "api"]:
        result = run_step(
            "extract_python",
            lambda: extract_python(config, args.domain, args.verbose, args.changed_only),
            args.verbose
        )
        results.append(("extract_python", result))
        total_warnings += result.warnings
        total_errors += result.errors

    # Step 3: Add layer tags to all symbols
    result = run_step(
        "add_layer_tags",
        lambda: add_layer_tags_step(config, args.domain, args.verbose),
        args.verbose
    )
    results.append(("add_layer_tags", result))
    total_warnings += result.warnings
    total_errors += result.errors

    # Step 4: Split API symbols by layer (optional)
    if not args.skip_split and args.domain in ["all", "api"]:
        result = run_step(
            "split_api_by_layer",
            lambda: split_api_by_layer_step(config, args.verbose),
            args.verbose
        )
        results.append(("split_api_by_layer", result))
        total_warnings += result.warnings
        total_errors += result.errors

    # Step 5: Validate symbols (optional)
    if not args.skip_validate:
        result = run_step(
            "validate_symbols",
            lambda: validate_symbols_step(config, args.domain, args.verbose),
            args.verbose
        )
        results.append(("validate_symbols", result))
        total_warnings += result.warnings
        total_errors += result.errors

    # Print summary
    print()
    print("=" * 50)
    print("Pipeline Summary")
    print("=" * 50)

    for step_name, result in results:
        status = "PASS" if result.success else "FAIL"
        extra = ""
        if result.warnings > 0:
            extra = f" ({result.warnings} warnings)"
        elif result.errors > 0:
            extra = f" ({result.errors} errors)"
        print(f"  {step_name}: {status}{extra}")

    print()
    print(f"Total Warnings: {total_warnings}")
    print(f"Total Errors: {total_errors}")

    # Determine exit code
    if total_errors > 0:
        print("\nPipeline completed with ERRORS")
        return 2
    elif total_warnings > 0:
        print("\nPipeline completed with WARNINGS")
        return 1
    else:
        print("\nPipeline completed successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())

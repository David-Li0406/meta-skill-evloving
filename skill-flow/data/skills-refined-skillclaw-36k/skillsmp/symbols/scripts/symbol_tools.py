#!/usr/bin/env python3
"""
Symbol Tools - Intelligent codebase symbol analysis

Provides token-efficient access to codebase symbols through pre-generated symbol
graphs that are chunked by domain and separated from tests.

Key Features:
- Configuration-driven: Uses symbols.config.json for project-agnostic operation
- API domain split into 5 layer-based files for 50-80% token reduction
- Use load_api_layer() for targeted backend development (routers, services, repositories, schemas, cores)
- Schema v2.0: Standardized fields with architectural layer tags on all symbols
- search_patterns() with layer filtering for precise cross-domain searches
- Graceful fallback to default paths if configuration is unavailable

Configuration:
    Automatically loads symbols.config.json via config.py. Falls back to default
    'ai/' directory if configuration is not available. See config.py for details.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal

# Load configuration with graceful fallback
try:
    from config import get_config, ConfigurationError
    _config = get_config()
    SYMBOLS_DIR = _config.get_symbols_dir()

    # Build symbol files mapping from config
    SYMBOL_FILES = {}
    for domain in _config.get_enabled_domains():
        try:
            SYMBOL_FILES[domain] = _config.get_domain_file(domain)
            # Add test file if configured
            test_file = _config.get_test_file(domain)
            if test_file:
                SYMBOL_FILES[f"{domain}-tests"] = test_file
        except ConfigurationError:
            pass  # Skip domains with issues

    # Build API layer files mapping from config
    API_LAYER_FILES = {}
    if _config.get_api_layers():
        for layer in _config.get_enabled_api_layers():
            try:
                API_LAYER_FILES[layer] = _config.get_api_layer_file(layer)
            except ConfigurationError:
                pass  # Skip layers with issues

    _config_loaded = True

except (ImportError, ConfigurationError) as e:
    # Fallback to minimal generic defaults with helpful error message
    print(f"Warning: Could not load configuration ({e})", file=sys.stderr)
    print("  Run 'python init_symbols.py' to initialize the symbols system for this project", file=sys.stderr)
    print("  Falling back to minimal defaults (symbols in 'ai/' directory)", file=sys.stderr)

    SYMBOLS_DIR = Path("ai")
    # Minimal generic fallback - only basic domains
    SYMBOL_FILES = {
        "api": SYMBOLS_DIR / "symbols-api.json",
        "ui": SYMBOLS_DIR / "symbols-ui.json",
    }
    # No API layer files in fallback mode
    API_LAYER_FILES = {}
    _config_loaded = False
    _config = None


def _normalize_symbol_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Normalize symbol data to handle both schema formats.

    Converts flat schema {"symbols": [...]} to hierarchical schema
    {"modules": [{"path": "...", "symbols": [...]}]} format.

    Returns list of modules in hierarchical format.
    """
    # Check if already hierarchical format
    if "modules" in data:
        return data["modules"]

    # Convert flat format to hierarchical
    if "symbols" in data:
        # Group symbols by path
        modules_dict = {}
        for symbol in data["symbols"]:
            path = symbol.get("path", "unknown")
            if path not in modules_dict:
                modules_dict[path] = {
                    "path": path,
                    "symbols": []
                }
            # Create symbol without "path" key since it's in module
            symbol_copy = {k: v for k, v in symbol.items() if k != "path"}
            modules_dict[path]["symbols"].append(symbol_copy)

        return list(modules_dict.values())

    return []


def query_symbols(
    name: Optional[str] = None,
    kind: Optional[str] = None,
    domain: Optional[str] = None,
    path: Optional[str] = None,
    limit: int = 20,
    summary_only: bool = False,
) -> List[Dict[str, Any]]:
    """
    Query symbols by name, kind, domain, or path without loading entire graph.

    Args:
        name: Symbol name (supports partial/fuzzy matching)
        kind: Symbol kind (component, hook, function, class, interface, type, method)
        domain: Domain filter (ui, api, shared)
        path: File path pattern (e.g., "components", "hooks", "services")
        limit: Maximum results to return (default: 20)
        summary_only: Return only name and summary (default: False)

    Returns:
        List of matching symbols with file path, line number, and summary
    """
    results = []
    domains_to_search = [domain.lower()] if domain else ["ui", "web", "api", "shared"]

    for domain_name in domains_to_search:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            # Path filter
            if path and path.lower() not in module["path"].lower():
                continue

            for symbol in module.get("symbols", []):
                # Name filter (fuzzy match)
                if name and name.lower() not in symbol["name"].lower():
                    continue

                # Kind filter
                if kind and symbol["kind"] != kind.lower():
                    continue

                # Build result
                result = {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain_name.upper(),
                    "summary": symbol.get("summary", ""),
                }

                if summary_only:
                    result = {"name": result["name"], "summary": result["summary"]}

                results.append(result)

                if len(results) >= limit:
                    return results

    return results


def load_domain(
    domain: Literal["ui", "web", "api", "shared"],
    include_tests: bool = False,
    max_symbols: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Load complete symbol set for a specific domain.

    Args:
        domain: Domain to load (ui, web, api, shared)
        include_tests: Include test file symbols (default: False)
        max_symbols: Limit number of symbols returned (default: all)

    Returns:
        Dict with domain, type, totalSymbols, and symbols array
    """
    domain = domain.lower()
    main_file = SYMBOL_FILES.get(domain)
    test_file = SYMBOL_FILES.get(f"{domain}-tests")

    if not main_file or not main_file.exists():
        raise FileNotFoundError(f"Symbol file for domain '{domain}' not found")

    with open(main_file) as f:
        main_data = json.load(f)

    # Normalize data to handle both flat and hierarchical schemas
    main_modules = _normalize_symbol_data(main_data)

    # Collect all symbols
    all_symbols = []
    for module in main_modules:
        for symbol in module.get("symbols", []):
            all_symbols.append(
                {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain.upper(),
                    "summary": symbol.get("summary", ""),
                }
            )

    # Add test symbols if requested
    if include_tests and test_file and test_file.exists():
        with open(test_file) as f:
            test_data = json.load(f)

        # Normalize test data
        test_modules = _normalize_symbol_data(test_data)

        for module in test_modules:
            for symbol in module.get("symbols", []):
                all_symbols.append(
                    {
                        "kind": symbol["kind"],
                        "name": symbol["name"],
                        "line": symbol["line"],
                        "file": module["path"],
                        "domain": domain.upper(),
                        "summary": symbol.get("summary", ""),
                        "test": True,
                    }
                )

    # Apply limit if specified
    if max_symbols:
        all_symbols = all_symbols[:max_symbols]

    return {
        "domain": domain.upper(),
        "type": "MAIN" if not include_tests else "MAIN+TESTS",
        "totalSymbols": len(all_symbols),
        "symbols": all_symbols,
    }


def load_api_layer(
    layer: Literal["routers", "services", "repositories", "schemas", "cores"],
    max_symbols: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Load symbols from a specific API architectural layer (Phase 2 optimization).

    Provides token-efficient access to specific API layers instead of loading
    the entire 1.7MB unified API file. Use this for targeted backend development.

    Args:
        layer: API layer to load (routers, services, repositories, schemas, cores)
        max_symbols: Limit number of symbols returned (default: all)

    Returns:
        Dict with layer, totalSymbols, and symbols array

    Examples:
        # Load only service layer for backend development (454 symbols, ~280KB)
        services = load_api_layer("services")

        # Load schemas for DTO work (570 symbols, ~250KB)
        schemas = load_api_layer("schemas", max_symbols=100)
    """
    layer_file = API_LAYER_FILES.get(layer)

    if not layer_file or not layer_file.exists():
        raise FileNotFoundError(f"Layer file for '{layer}' not found: {layer_file}")

    with open(layer_file) as f:
        data = json.load(f)

    # Normalize data to handle both flat and hierarchical schemas
    modules = _normalize_symbol_data(data)

    # Collect all symbols
    all_symbols = []
    for module in modules:
        for symbol in module.get("symbols", []):
            all_symbols.append(
                {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": "API",
                    "layer": layer.rstrip('s'),  # Remove plural 's'
                    "summary": symbol.get("summary", ""),
                }
            )

    # Apply limit if specified
    if max_symbols:
        all_symbols = all_symbols[:max_symbols]

    return {
        "domain": "API",
        "layer": layer,
        "totalSymbols": len(all_symbols),
        "symbols": all_symbols,
    }


def search_patterns(
    pattern: str,
    layer: Optional[str] = None,
    priority: Optional[str] = None,
    domain: Optional[str] = None,
    limit: int = 30,
) -> List[Dict[str, Any]]:
    """
    Advanced pattern-based search with architectural layer awareness.

    Uses Schema v2.0 layer tags for precise filtering. Supports searching across
    all domains or targeting specific architectural layers.

    Args:
        pattern: Search pattern (supports regex)
        layer: Architectural layer filter (router, service, repository, schema, component, hook, page, util, core, test)
        priority: Priority filter (high, medium, low) - based on naming conventions
        domain: Domain filter (ui, web, api, shared)
        limit: Maximum results (default: 30)

    Returns:
        List of matching symbols with layer and priority information

    Examples:
        # Find all service classes matching "Prompt"
        search_patterns("Prompt", layer="service")

        # Find high-priority router functions
        search_patterns(".*Router", layer="router", priority="high")

        # Find UI components across all domains
        search_patterns("Button", layer="component")
    """
    # Compile regex pattern
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        # If pattern is not valid regex, treat as literal string
        regex = re.compile(re.escape(pattern), re.IGNORECASE)

    results = []
    domains_to_search = [domain.lower()] if domain else ["ui", "web", "api", "shared"]

    for domain_name in domains_to_search:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            for symbol in module.get("symbols", []):
                # Pattern match on name
                if not regex.search(symbol["name"]):
                    continue

                # Layer filter using Schema v2.0 layer field
                symbol_layer = symbol.get("layer", "unknown")
                if layer:
                    # Normalize layer comparison (handle plural forms)
                    filter_layer = layer.lower().rstrip('s')
                    symbol_layer_normalized = symbol_layer.lower().rstrip('s')

                    if filter_layer != symbol_layer_normalized:
                        continue

                # Determine priority based on naming conventions
                detected_priority = "medium"
                if any(
                    x in symbol["name"].lower()
                    for x in ["service", "router", "repository"]
                ):
                    detected_priority = "high"
                elif any(x in symbol["name"].lower() for x in ["util", "helper"]):
                    detected_priority = "low"

                # Priority filter
                if priority and detected_priority != priority.lower():
                    continue

                result = {
                    "kind": symbol["kind"],
                    "name": symbol["name"],
                    "line": symbol["line"],
                    "file": module["path"],
                    "domain": domain_name.upper(),
                    "summary": symbol.get("summary", ""),
                    "layer": symbol_layer,
                    "priority": detected_priority,
                }

                results.append(result)

                if len(results) >= limit:
                    return results

    return results


def get_symbol_context(
    name: str,
    file: Optional[str] = None,
    include_related: bool = False,
) -> Dict[str, Any]:
    """
    Get full context for a specific symbol including definition location and related symbols.

    Args:
        name: Exact symbol name
        file: File path if name is ambiguous
        include_related: Include related symbols (imports, usages) (default: False)

    Returns:
        Dict with symbol info and optionally related symbols
    """
    # Search all domains for the symbol
    found_symbol = None
    found_module = None
    found_domain = None

    for domain_name in ["ui", "web", "api", "shared"]:
        symbol_file = SYMBOL_FILES.get(domain_name)
        if not symbol_file or not symbol_file.exists():
            continue

        with open(symbol_file) as f:
            data = json.load(f)

        # Normalize data to handle both flat and hierarchical schemas
        modules = _normalize_symbol_data(data)

        for module in modules:
            # File filter if provided
            if file and file not in module["path"]:
                continue

            for symbol in module.get("symbols", []):
                if symbol["name"] == name:
                    found_symbol = symbol
                    found_module = module
                    found_domain = domain_name
                    break

            if found_symbol:
                break

        if found_symbol:
            break

    if not found_symbol:
        return {"error": f"Symbol '{name}' not found"}

    result = {
        "symbol": {
            "kind": found_symbol["kind"],
            "name": found_symbol["name"],
            "line": found_symbol["line"],
            "file": found_module["path"],
            "domain": found_domain.upper(),
            "summary": found_symbol.get("summary", ""),
        }
    }

    # Find related symbols if requested
    if include_related:
        related = []

        # Look for related symbols in the same file
        for symbol in found_module.get("symbols", []):
            if symbol["name"] != name:
                related.append(
                    {
                        "kind": symbol["kind"],
                        "name": symbol["name"],
                        "line": symbol["line"],
                        "summary": symbol.get("summary", ""),
                        "relation": "same-file",
                    }
                )

        # Look for Props interface for components
        if found_symbol["kind"] == "component":
            props_name = f"{name}Props"
            props_results = query_symbols(name=props_name, kind="interface", limit=5)
            for props in props_results:
                related.append(
                    {
                        "kind": props["kind"],
                        "name": props["name"],
                        "line": props["line"],
                        "file": props["file"],
                        "summary": props["summary"],
                        "relation": "props-interface",
                    }
                )

        result["related"] = related

    return result


def validate_symbols(domain: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate symbol files for all or specific domains.

    Performs comprehensive health checks including:
    - File existence and readability
    - Schema validity (required fields, valid kinds/layers)
    - Timestamp freshness (< 7 days warning, > 14 days error)
    - Duplicate detection (same name+file+line)
    - Missing required fields
    - Stale files (source file deleted but symbol exists)

    Args:
        domain: Specific domain to validate (None = all domains)

    Returns:
        Validation report with status, errors, warnings, and statistics

    Example:
        >>> report = validate_symbols()
        >>> if report["status"] == "valid":
        ...     print(f"All {report['summary']['total_symbols']} symbols are valid!")
        >>> else:
        ...     print(f"Found {report['summary']['total_errors']} errors")

        >>> report = validate_symbols(domain="ui")
        >>> ui_report = report["domains"]["ui"]
        >>> print(f"UI domain has {ui_report['symbols_count']} symbols")
    """
    import time

    # Use module-level config or try to load it
    global _config, _config_loaded

    if not _config_loaded or _config is None:
        try:
            from config import get_config, ConfigurationError
            _config = get_config()
            _config_loaded = True
        except ImportError as e:
            return {
                "status": "errors",
                "error": f"Configuration not available: {e}",
                "domains": {},
                "summary": {
                    "total_symbols": 0,
                    "total_errors": 1,
                    "total_warnings": 0,
                    "domains_checked": 0,
                    "validation_time": "0s",
                },
            }
        except ConfigurationError as e:
            return {
                "status": "errors",
                "error": f"Configuration not available: {e}",
                "domains": {},
                "summary": {
                    "total_symbols": 0,
                    "total_errors": 1,
                    "total_warnings": 0,
                    "domains_checked": 0,
                    "validation_time": "0s",
                },
            }

    start_time = time.time()

    # Use the loaded config
    config = _config
    try:
        # Validate config is accessible
        config._project_root
    except AttributeError as e:
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

        report = _validate_domain_file(file_path, project_root)
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

            report = _validate_domain_file(file_path, project_root)
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
    if validation_time < 1:
        time_str = f"{validation_time * 1000:.0f}ms"
    elif validation_time < 60:
        time_str = f"{validation_time:.1f}s"
    else:
        time_str = f"{validation_time / 60:.1f}m"

    return {
        "status": status,
        "domains": domain_reports,
        "summary": {
            "total_symbols": total_symbols,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "domains_checked": len(domain_reports),
            "validation_time": time_str,
        },
    }


def _validate_domain_file(
    file_path: Path,
    project_root: Path
) -> Dict[str, Any]:
    """
    Internal helper to validate a single domain symbol file.

    Args:
        file_path: Path to symbol file
        project_root: Project root directory

    Returns:
        Validation report for this domain
    """
    from datetime import datetime

    # Schema validation constants
    REQUIRED_FIELDS = {"name", "kind", "line", "signature", "summary", "layer"}
    WARNING_AGE_DAYS = 7
    ERROR_AGE_DAYS = 14

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
    modules = _normalize_symbol_data(data)

    # Track symbols for duplicate detection
    seen_symbols = set()
    duplicates = []
    missing_sources = []

    # Validate each module and symbol
    for module in modules:
        module_path = module.get("path", "unknown")

        # Check if source file exists
        source = Path(module_path)
        if not source.is_absolute():
            source = project_root / module_path

        if not source.exists():
            missing_sources.append(module_path)
            report["missing_sources"] += 1

        for symbol in module.get("symbols", []):
            report["symbols_count"] += 1

            # Schema validation - check required fields
            missing_fields = REQUIRED_FIELDS - set(symbol.keys())
            if missing_fields:
                report["errors"].append(
                    f"Missing fields in {module_path} symbol '{symbol.get('name', 'UNKNOWN')}': "
                    f"{', '.join(sorted(missing_fields))}"
                )

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

    return report


def update_symbols(
    mode: Literal["full", "incremental", "domain"] = "incremental",
    domain: Optional[str] = None,
    files: Optional[List[str]] = None,
    chunk: bool = True,
) -> Dict[str, Any]:
    """
    Trigger symbol graph regeneration or incremental update.

    Note: This function provides the interface but delegates to existing
    slash commands for actual implementation.

    Args:
        mode: Update mode (full, incremental, domain)
        domain: Specific domain to update (for domain mode)
        files: Specific files to update (for incremental mode)
        chunk: Re-chunk symbols after update (default: True)

    Returns:
        Dict with update results
    """
    # This would integrate with existing slash commands:
    # /symbols-update, /symbols-chunk
    return {
        "note": "Use /symbols-update and /symbols-chunk slash commands",
        "mode": mode,
        "domain": domain,
        "files": files,
        "chunk": chunk,
    }


if __name__ == "__main__":
    # Example usage
    print("Symbol Tools - Example Usage\n")

    # Query components with 'Card' in name
    print("1. Query UI components with 'Card' in name:")
    results = query_symbols(name="Card", kind="component", domain="ui", limit=5)
    for r in results:
        print(f"  - {r['name']} ({r['file']}:{r['line']})")

    # Load API layer (Phase 2 optimization)
    print("\n2. Load API service layer (token-efficient):")
    services_data = load_api_layer(layer="services", max_symbols=10)
    print(f"  Total: {services_data['totalSymbols']} symbols in service layer")
    for s in services_data["symbols"][:3]:
        print(f"  - {s['name']} ({s['kind']})")

    # Load full API domain (legacy, loads all 3,041 symbols)
    print("\n3. Load full API domain (first 10 symbols):")
    api_data = load_domain(domain="api", max_symbols=10)
    print(f"  Total: {api_data['totalSymbols']} symbols")
    for s in api_data["symbols"][:3]:
        print(f"  - {s['name']} ({s['kind']})")

    # Search for services
    print("\n4. Search for service layer classes:")
    services = search_patterns(pattern="Service", layer="service", limit=5)
    for s in services:
        print(f"  - {s['name']} ({s['file']}:{s['line']})")

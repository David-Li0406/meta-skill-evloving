#!/usr/bin/env python3
"""
Interactive Symbols Configuration Wizard

Creates a customized symbols.config.json for your project with an interactive CLI.
Supports multiple project templates and allows customization of all settings.

Usage:
    # Interactive mode with auto-detection (recommended)
    python .claude/skills/symbols/scripts/init_symbols.py

    # Auto-detect and configure without prompts
    python .claude/skills/symbols/scripts/init_symbols.py --auto-detect

    # Verbose output showing detection details
    python .claude/skills/symbols/scripts/init_symbols.py --auto-detect --verbose

    # Quick setup with template
    python .claude/skills/symbols/scripts/init_symbols.py --template=react-typescript-fullstack

    # Load from custom config file
    python .claude/skills/symbols/scripts/init_symbols.py --config-file=paths.json

    # Non-interactive with all options
    python .claude/skills/symbols/scripts/init_symbols.py \\
      --template=python-fastapi \\
      --name="MyProject" \\
      --symbols-dir="ai" \\
      --force

    # List available templates
    python .claude/skills/symbols/scripts/init_symbols.py --list

    # Dry run (preview without writing)
    python .claude/skills/symbols/scripts/init_symbols.py --dry-run

Features:
    - Automatic codebase structure detection
        * Detects package managers (pnpm, npm, yarn, uv, poetry, etc.)
        * Identifies monorepo type (pnpm-workspace, turborepo, lerna, etc.)
        * Finds backend code (Python, Node.js)
        * Finds frontend code (React, Next.js, Vue)
        * Finds mobile code (React Native, Expo)
        * Finds shared packages
        * Suggests appropriate template based on detection
    - Interactive CLI with input validation
    - 5 project templates (React, FastAPI, Next.js, Vue, Django)
    - Custom config file support (--config-file)
    - Path validation with confidence scoring
    - Customizable domains, layers, and extraction paths
    - Schema validation before writing
    - Color output for better UX (when colorama available)
    - Non-interactive mode for automation
"""

import argparse
import glob as glob_module
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Try to import colorama for colored output
try:
    from colorama import init as colorama_init, Fore, Style

    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    # Fallback to no color
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = ""

    class Style:
        BRIGHT = RESET_ALL = ""

    HAS_COLOR = False


# Template metadata
TEMPLATES = {
    "react-typescript-fullstack": {
        "name": "React + TypeScript Fullstack",
        "description": "React + TypeScript monorepo with FastAPI backend",
        "file": "react-typescript-fullstack.json",
        "frameworks": "React, Next.js, FastAPI, SQLAlchemy",
        "best_for": "Full-stack monorepos with React frontend and Python backend",
    },
    "nextjs-monorepo": {
        "name": "Next.js Monorepo",
        "description": "Next.js monorepo with App Router",
        "file": "nextjs-monorepo.json",
        "frameworks": "Next.js 14+, React, Tailwind, Turborepo",
        "best_for": "Next.js applications with multiple apps and shared packages",
    },
    "python-fastapi": {
        "name": "Python FastAPI",
        "description": "FastAPI backend with SQLAlchemy",
        "file": "python-fastapi.json",
        "frameworks": "FastAPI, SQLAlchemy, Pydantic, Alembic",
        "best_for": "Python API services with layered architecture",
    },
    "python-django": {
        "name": "Python Django",
        "description": "Django web framework",
        "file": "python-django.json",
        "frameworks": "Django, Django REST Framework",
        "best_for": "Django applications with MVT architecture",
    },
    "vue-typescript": {
        "name": "Vue + TypeScript",
        "description": "Vue 3 application with TypeScript",
        "file": "vue-typescript.json",
        "frameworks": "Vue 3, Composition API, Pinia, Vite",
        "best_for": "Vue applications with TypeScript and modern tooling",
    },
}


# =============================================================================
# Codebase Detection
# =============================================================================


def detect_package_manager(project_root: Path) -> Optional[str]:
    """Detect package manager used in the project."""
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project_root / "yarn.lock").exists():
        return "yarn"
    if (project_root / "package-lock.json").exists():
        return "npm"
    if (project_root / "bun.lockb").exists():
        return "bun"
    if (project_root / "uv.lock").exists() or (project_root / "pyproject.toml").exists():
        return "uv/pip"
    if (project_root / "Pipfile.lock").exists():
        return "pipenv"
    if (project_root / "poetry.lock").exists():
        return "poetry"
    if (project_root / "Cargo.lock").exists():
        return "cargo"
    return None


def detect_monorepo_type(project_root: Path) -> Optional[str]:
    """Detect monorepo structure type."""
    if (project_root / "pnpm-workspace.yaml").exists():
        return "pnpm-workspace"
    if (project_root / "lerna.json").exists():
        return "lerna"
    if (project_root / "turbo.json").exists():
        return "turborepo"

    # Check for workspaces in package.json
    package_json = project_root / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                if "workspaces" in data:
                    return "npm-workspaces"
        except Exception:
            pass

    return None


def detect_python_packages(project_root: Path) -> List[str]:
    """
    Detect top-level Python packages that might contain code.

    Looks for directories with __init__.py or checks pyproject.toml for package name.
    Excludes hidden directories and common non-code directories.

    Returns:
        List of package names (directory names that are Python packages)
    """
    packages = []

    # Directories to exclude from package detection
    excluded_dirs = {
        "tests", "test", "docs", "doc", "documentation",
        "scripts", "bin", "build", "dist", "node_modules",
        ".git", ".github", ".venv", "venv", "env", ".env",
        "__pycache__", ".pytest_cache", ".mypy_cache",
        ".tox", ".nox", "htmlcov", "coverage", ".coverage",
        "site-packages", "migrations", "alembic",
    }

    # Look for directories with __init__.py
    for item in project_root.iterdir():
        if not item.is_dir():
            continue
        # Skip hidden directories (starting with .)
        if item.name.startswith('.'):
            continue
        # Skip excluded directories
        if item.name.lower() in excluded_dirs:
            continue
        # Check for __init__.py (Python package marker)
        if (item / '__init__.py').exists():
            packages.append(item.name)

    # Also check pyproject.toml for package name if no packages found via __init__.py
    if not packages:
        pyproject_path = project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                # Try tomllib (Python 3.11+) or tomli
                try:
                    import tomllib
                except ImportError:
                    try:
                        import tomli as tomllib
                    except ImportError:
                        tomllib = None

                if tomllib:
                    with open(pyproject_path, "rb") as f:
                        pyproject = tomllib.load(f)

                    # Check [project] name
                    project_name = pyproject.get("project", {}).get("name")
                    if project_name:
                        # Convert package name to directory name (replace - with _)
                        pkg_dir = project_name.replace("-", "_")
                        pkg_path = project_root / pkg_dir
                        if pkg_path.exists() and pkg_path.is_dir():
                            packages.append(pkg_dir)

                    # Check [tool.poetry] name
                    poetry_name = pyproject.get("tool", {}).get("poetry", {}).get("name")
                    if poetry_name and poetry_name not in packages:
                        pkg_dir = poetry_name.replace("-", "_")
                        pkg_path = project_root / pkg_dir
                        if pkg_path.exists() and pkg_path.is_dir():
                            packages.append(pkg_dir)
            except Exception:
                pass

    return packages


def count_files_by_extension(directory: Path, extensions: List[str]) -> int:
    """Count files with given extensions in a directory."""
    count = 0
    for ext in extensions:
        pattern = f"**/*{ext}"
        try:
            matches = list(directory.glob(pattern))
            count += len(matches)
        except Exception:
            pass
    return count


def detect_backend_paths(project_root: Path) -> List[Dict[str, Any]]:
    """
    Detect backend code locations.

    Returns list of detected paths with metadata:
        [{"path": "services/api", "language": "python", "confidence": "high", "file_count": 50}]
    """
    candidates = []

    # Common backend directory patterns
    backend_patterns = [
        "api", "backend", "server", "services", "services/api",
        "apps/api", "packages/api", "src/api", "src/server"
    ]

    # Add package-based patterns (e.g., skillmeat/api, myproject/backend)
    packages = detect_python_packages(project_root)
    for pkg in packages:
        backend_patterns.extend([
            f"{pkg}/api",
            f"{pkg}/backend",
            f"{pkg}/server",
            f"{pkg}/services",
        ])

    for pattern in backend_patterns:
        path = project_root / pattern
        if not path.exists() or not path.is_dir():
            continue

        # Check for Python
        py_count = count_files_by_extension(path, [".py"])
        if py_count > 0:
            confidence = "high" if py_count > 10 else "medium" if py_count > 3 else "low"
            candidates.append({
                "path": pattern,
                "language": "python",
                "confidence": confidence,
                "file_count": py_count
            })

        # Check for Node.js backend
        js_count = count_files_by_extension(path, [".js", ".ts"])
        has_express = (path / "package.json").exists()
        if js_count > 0 and has_express:
            confidence = "high" if js_count > 10 else "medium"
            candidates.append({
                "path": pattern,
                "language": "typescript",
                "confidence": confidence,
                "file_count": js_count
            })

    # Sort by confidence and file count
    confidence_order = {"high": 3, "medium": 2, "low": 1}
    candidates.sort(key=lambda x: (confidence_order.get(x["confidence"], 0), x["file_count"]), reverse=True)

    return candidates


def detect_frontend_paths(project_root: Path) -> List[Dict[str, Any]]:
    """
    Detect frontend code locations.

    Returns list of detected paths with metadata.
    """
    candidates = []

    # Common frontend directory patterns
    frontend_patterns = [
        "web", "frontend", "client", "app", "apps/web", "apps/frontend",
        "packages/web", "src", "src/client"
    ]

    # Add package-based patterns (e.g., skillmeat/web, myproject/frontend)
    packages = detect_python_packages(project_root)
    for pkg in packages:
        frontend_patterns.extend([
            f"{pkg}/web",
            f"{pkg}/frontend",
            f"{pkg}/client",
            f"{pkg}/app",
        ])

    for pattern in frontend_patterns:
        path = project_root / pattern
        if not path.exists() or not path.is_dir():
            continue

        # Check for React/Next.js/Vue
        tsx_count = count_files_by_extension(path, [".tsx", ".ts", ".jsx", ".js"])
        vue_count = count_files_by_extension(path, [".vue"])

        has_package_json = (path / "package.json").exists()
        has_nextjs = (path / "next.config.js").exists() or (path / "next.config.mjs").exists()
        has_vite = (path / "vite.config.ts").exists() or (path / "vite.config.js").exists()

        if tsx_count > 0 or vue_count > 0:
            confidence = "high" if (has_package_json or has_nextjs or has_vite) else "medium"

            framework = None
            if has_nextjs:
                framework = "nextjs"
            elif vue_count > 0:
                framework = "vue"
            elif tsx_count > 0:
                framework = "react"

            candidates.append({
                "path": pattern,
                "language": "typescript",
                "confidence": confidence,
                "file_count": tsx_count + vue_count,
                "framework": framework
            })

    # Sort by confidence and file count
    confidence_order = {"high": 3, "medium": 2, "low": 1}
    candidates.sort(key=lambda x: (confidence_order.get(x["confidence"], 0), x["file_count"]), reverse=True)

    return candidates


def detect_mobile_paths(project_root: Path) -> List[Dict[str, Any]]:
    """Detect mobile app code locations."""
    candidates = []

    mobile_patterns = [
        "mobile", "apps/mobile", "packages/mobile",
        "ios", "android", "react-native"
    ]

    for pattern in mobile_patterns:
        path = project_root / pattern
        if not path.exists() or not path.is_dir():
            continue

        # Check for React Native
        has_expo = (path / "app.json").exists() and (path / "package.json").exists()
        has_rn = (path / "ios").exists() and (path / "android").exists()

        tsx_count = count_files_by_extension(path, [".tsx", ".ts", ".jsx", ".js"])

        if has_expo or has_rn or tsx_count > 0:
            confidence = "high" if (has_expo or has_rn) else "medium"
            framework = "expo" if has_expo else "react-native" if has_rn else "unknown"

            candidates.append({
                "path": pattern,
                "language": "typescript",
                "confidence": confidence,
                "file_count": tsx_count,
                "framework": framework
            })

    confidence_order = {"high": 3, "medium": 2, "low": 1}
    candidates.sort(key=lambda x: (confidence_order.get(x["confidence"], 0), x["file_count"]), reverse=True)

    return candidates


def detect_shared_paths(project_root: Path) -> List[Dict[str, Any]]:
    """Detect shared code/package locations."""
    candidates = []

    shared_patterns = [
        "packages/ui", "packages/shared", "packages/common",
        "libs/shared", "libs/common", "shared", "common"
    ]

    # Add package-based patterns (e.g., skillmeat/shared, myproject/core)
    packages = detect_python_packages(project_root)
    for pkg in packages:
        shared_patterns.extend([
            f"{pkg}/shared",
            f"{pkg}/common",
            f"{pkg}/core",
            f"{pkg}/utils",
        ])

    for pattern in shared_patterns:
        path = project_root / pattern
        if not path.exists() or not path.is_dir():
            continue

        tsx_count = count_files_by_extension(path, [".tsx", ".ts", ".jsx", ".js"])
        py_count = count_files_by_extension(path, [".py"])

        total_count = tsx_count + py_count
        if total_count > 0:
            language = "typescript" if tsx_count > py_count else "python"
            confidence = "high" if total_count > 5 else "medium"

            candidates.append({
                "path": pattern,
                "language": language,
                "confidence": confidence,
                "file_count": total_count
            })

    confidence_order = {"high": 3, "medium": 2, "low": 1}
    candidates.sort(key=lambda x: (confidence_order.get(x["confidence"], 0), x["file_count"]), reverse=True)

    return candidates


def detect_codebase_structure(project_root: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    Scan project and detect code organization.

    Args:
        project_root: Path to project root
        verbose: Show detailed detection information

    Returns:
        {
            'backend': [{'path': 'services/api', 'language': 'python', 'confidence': 'high', 'file_count': 50}],
            'frontend': [{'path': 'apps/web', 'language': 'typescript', 'confidence': 'high', 'file_count': 120}],
            'mobile': [],
            'shared': [{'path': 'packages/ui', 'language': 'typescript', 'confidence': 'high', 'file_count': 30}],
            'is_monorepo': True,
            'monorepo_type': 'pnpm-workspace',
            'package_manager': 'pnpm',
            'suggested_template': 'react-typescript-fullstack'
        }
    """
    if verbose:
        print_info(f"Scanning project root: {project_root}")

    # Detect infrastructure
    package_manager = detect_package_manager(project_root)
    monorepo_type = detect_monorepo_type(project_root)
    is_monorepo = monorepo_type is not None

    if verbose and package_manager:
        print_info(f"Detected package manager: {package_manager}")
    if verbose and monorepo_type:
        print_info(f"Detected monorepo type: {monorepo_type}")

    # Detect code locations
    backend = detect_backend_paths(project_root)
    frontend = detect_frontend_paths(project_root)
    mobile = detect_mobile_paths(project_root)
    shared = detect_shared_paths(project_root)

    if verbose:
        print_info(f"Found {len(backend)} backend paths, {len(frontend)} frontend paths, "
                  f"{len(mobile)} mobile paths, {len(shared)} shared paths")

    # Suggest template based on detection
    suggested_template = suggest_template_from_detection({
        "backend": backend,
        "frontend": frontend,
        "mobile": mobile,
        "shared": shared,
        "is_monorepo": is_monorepo
    })

    return {
        "backend": backend,
        "frontend": frontend,
        "mobile": mobile,
        "shared": shared,
        "is_monorepo": is_monorepo,
        "monorepo_type": monorepo_type,
        "package_manager": package_manager,
        "suggested_template": suggested_template
    }


def suggest_template_from_detection(detected: Dict[str, Any]) -> Optional[str]:
    """Suggest the most appropriate template based on detection results."""
    has_backend = len(detected.get("backend", [])) > 0
    has_frontend = len(detected.get("frontend", [])) > 0
    has_mobile = len(detected.get("mobile", [])) > 0
    is_monorepo = detected.get("is_monorepo", False)

    # Get primary languages
    backend_lang = detected["backend"][0]["language"] if has_backend else None
    frontend_framework = None
    if has_frontend:
        frontend_framework = detected["frontend"][0].get("framework")

    # Template selection logic
    if is_monorepo and has_backend and has_frontend:
        return "react-typescript-fullstack"
    elif has_frontend and frontend_framework == "nextjs":
        return "nextjs-monorepo"
    elif has_backend and backend_lang == "python":
        # Check for Django vs FastAPI
        return "python-fastapi"  # Default to FastAPI for now
    elif has_frontend and frontend_framework == "vue":
        return "vue-typescript"
    elif has_frontend:
        return "nextjs-monorepo"  # Default frontend template

    return None


def load_config_from_file(config_file: Path) -> Dict[str, Any]:
    """Load configuration from a custom JSON file."""
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    try:
        with open(config_file) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def validate_paths(config: Dict[str, Any], project_root: Path) -> List[str]:
    """
    Validate that configured paths exist.

    Returns:
        List of warning messages (empty if all valid)
    """
    warnings = []

    # Check extraction directories
    for lang, extraction in config.get("extraction", {}).items():
        for directory in extraction.get("directories", []):
            path = project_root / directory
            if not path.exists():
                warnings.append(f"{lang} directory does not exist: {directory}")
            elif not path.is_dir():
                warnings.append(f"{lang} path is not a directory: {directory}")

    return warnings


def show_detection_results(detected: Dict[str, Any]) -> None:
    """Display detection results to the user."""
    print()
    print(f"{Style.BRIGHT}Detected Project Structure:{Style.RESET_ALL}")
    print()

    # Infrastructure
    if detected.get("package_manager"):
        print(f"  Package Manager: {Fore.CYAN}{detected['package_manager']}{Style.RESET_ALL}")

    if detected.get("is_monorepo"):
        monorepo_type = detected.get("monorepo_type", "unknown")
        print(f"  Monorepo: {Fore.GREEN}Yes{Style.RESET_ALL} ({monorepo_type})")
    else:
        print(f"  Monorepo: {Fore.YELLOW}No{Style.RESET_ALL}")

    print()

    # Code locations
    def show_paths(label: str, paths: List[Dict[str, Any]]):
        if paths:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {Style.BRIGHT}{label}:{Style.RESET_ALL}")
            for p in paths[:3]:  # Show top 3
                conf_color = Fore.GREEN if p["confidence"] == "high" else Fore.YELLOW if p["confidence"] == "medium" else Fore.RED
                framework_info = f" ({p.get('framework', '')})" if p.get('framework') else ""
                print(f"      {p['path']} - {p['language']}{framework_info} [{conf_color}{p['confidence']}{Style.RESET_ALL} confidence, {p['file_count']} files]")
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} {Style.BRIGHT}{label}:{Style.RESET_ALL} not detected")

    show_paths("Backend", detected.get("backend", []))
    show_paths("Frontend", detected.get("frontend", []))
    show_paths("Mobile", detected.get("mobile", []))
    show_paths("Shared", detected.get("shared", []))

    print()

    # Suggested template
    if detected.get("suggested_template"):
        template_name = TEMPLATES[detected["suggested_template"]]["name"]
        print(f"  {Style.BRIGHT}Suggested Template:{Style.RESET_ALL} {Fore.CYAN}{template_name}{Style.RESET_ALL}")
    else:
        print(f"  {Style.BRIGHT}Suggested Template:{Style.RESET_ALL} {Fore.YELLOW}No clear match - manual selection recommended{Style.RESET_ALL}")


def prompt_detection_choice() -> int:
    """
    Prompt user to choose what to do with detection results.

    Returns:
        1: Use detected structure
        2: Customize paths interactively
        3: Load from custom config file
    """
    print()
    print(f"{Style.BRIGHT}What would you like to do?{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}1.{Style.RESET_ALL} Use detected structure (recommended)")
    print(f"  {Fore.CYAN}2.{Style.RESET_ALL} Customize paths interactively")
    print(f"  {Fore.CYAN}3.{Style.RESET_ALL} Load from custom config file")
    print()

    while True:
        choice = prompt_input("Select option (1-3)", default="1")
        try:
            choice_int = int(choice)
            if 1 <= choice_int <= 3:
                return choice_int
        except ValueError:
            pass
        print_error("Invalid choice. Please enter 1, 2, or 3.")


# =============================================================================
# Original Helper Functions
# =============================================================================


def print_header(text: str, char: str = "=") -> None:
    """Print a formatted header."""
    width = 80
    print()
    print(f"{Fore.CYAN}{Style.BRIGHT}{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}{Style.RESET_ALL}")
    print()


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}", file=sys.stderr)


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def print_step(number: int, text: str) -> None:
    """Print step number and description."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Step {number}: {text}{Style.RESET_ALL}")


def get_templates_dir() -> Path:
    """Get the templates directory path."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "templates"


def get_schema_path() -> Path:
    """Get the schema file path."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "symbols-config-schema.json"


def find_project_root() -> Path:
    """
    Find the project root directory.

    Looks for common markers like .git, package.json, pyproject.toml.
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

    # Fallback to current directory
    return Path.cwd()


def detect_project_name() -> str:
    """Detect project name from git or directory name."""
    project_root = find_project_root()

    # Try to get from git config
    git_config = project_root / ".git" / "config"
    if git_config.exists():
        try:
            with open(git_config) as f:
                for line in f:
                    if "url = " in line:
                        # Extract repo name from URL
                        url = line.split("url = ")[1].strip()
                        # Handle both HTTPS and SSH URLs
                        if "/" in url:
                            name = url.split("/")[-1]
                            # Remove .git suffix
                            name = name.replace(".git", "")
                            if name:
                                return name
        except Exception:
            pass

    # Fallback to directory name
    return project_root.name


def validate_project_name(name: str) -> bool:
    """Validate project name (alphanumeric, hyphens, underscores)."""
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))


def validate_directory(directory: str) -> bool:
    """Validate directory name (no leading/trailing slashes)."""
    return bool(re.match(r"^[^/].*[^/]$", directory)) or directory in [".", ""]


def list_templates() -> None:
    """List all available templates with details."""
    print_header("Available Templates")

    for template_id, meta in TEMPLATES.items():
        print(f"{Fore.CYAN}{Style.BRIGHT}{template_id}{Style.RESET_ALL}")
        print(f"  Name: {meta['name']}")
        print(f"  Description: {meta['description']}")
        print(f"  Frameworks: {meta['frameworks']}")
        print(f"  Best for: {meta['best_for']}")
        print()


def load_template(template_id: str) -> Dict[str, Any]:
    """Load a template configuration."""
    templates_dir = get_templates_dir()
    template_file = templates_dir / TEMPLATES[template_id]["file"]

    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")

    with open(template_file) as f:
        return json.load(f)


def replace_placeholders(config: Dict[str, Any], project_name: str, symbols_dir: str) -> Dict[str, Any]:
    """Replace placeholders in template configuration."""
    config_str = json.dumps(config)
    config_str = config_str.replace("{{PROJECT_NAME}}", project_name)
    config_str = config_str.replace("{{SYMBOLS_DIR}}", symbols_dir)
    return json.loads(config_str)


def validate_against_schema(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate configuration against JSON schema.

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Try to import jsonschema
        import jsonschema
    except ImportError:
        print_warning("jsonschema not installed - skipping schema validation")
        print_info("Install with: pip install jsonschema")
        return True, None

    schema_path = get_schema_path()
    if not schema_path.exists():
        return True, "Schema file not found - skipping validation"

    try:
        with open(schema_path) as f:
            schema = json.load(f)

        jsonschema.validate(config, schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, f"Schema validation failed: {e.message}"
    except Exception as e:
        return False, f"Validation error: {e}"


def prompt_input(prompt: str, default: Optional[str] = None) -> str:
    """Prompt user for input with optional default."""
    if default:
        prompt_text = f"{prompt} [{Fore.GREEN}{default}{Style.RESET_ALL}]: "
    else:
        prompt_text = f"{prompt}: "

    response = input(prompt_text).strip()
    return response if response else (default or "")


def prompt_yes_no(prompt: str, default: bool = True) -> bool:
    """Prompt user for yes/no input."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not response:
        return default

    return response in ["y", "yes"]


def show_welcome() -> bool:
    """Show welcome screen and confirm user wants to proceed."""
    print_header("Symbols Skill Configuration Wizard")

    print(f"{Fore.CYAN}Welcome to the Symbols Configuration Wizard!{Style.RESET_ALL}")
    print()
    print("This wizard will help you set up symbol extraction for your project.")
    print()
    print(f"{Style.BRIGHT}What are symbols?{Style.RESET_ALL}")
    print("  • Pre-generated metadata about your codebase (functions, classes, types)")
    print("  • Enable token-efficient code navigation and analysis")
    print("  • 95-99% token reduction compared to reading full files")
    print()
    print(f"{Style.BRIGHT}Benefits:{Style.RESET_ALL}")
    print("  • Fast codebase exploration (0.1s vs 2-3 min)")
    print("  • Precise file:line references for navigation")
    print("  • Domain-chunked for targeted queries")
    print("  • Architectural awareness (layers, components, tests)")
    print()

    return prompt_yes_no("Would you like to continue?", default=True)


def select_template(non_interactive: bool = False, template_arg: Optional[str] = None) -> str:
    """Select a project template."""
    print_step(1, "Template Selection")

    if non_interactive and template_arg:
        if template_arg not in TEMPLATES:
            print_error(f"Invalid template: {template_arg}")
            print_info("Use --list to see available templates")
            sys.exit(1)
        print_success(f"Using template: {TEMPLATES[template_arg]['name']}")
        return template_arg

    print("Available templates:")
    print()

    template_list = list(TEMPLATES.keys())
    for i, template_id in enumerate(template_list, 1):
        meta = TEMPLATES[template_id]
        print(f"{Fore.CYAN}{i}.{Style.RESET_ALL} {Style.BRIGHT}{meta['name']}{Style.RESET_ALL}")
        print(f"   {meta['description']}")
        print(f"   Frameworks: {meta['frameworks']}")
        print()

    while True:
        choice = prompt_input(
            f"Select a template (1-{len(template_list)})",
            default="1"
        )

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(template_list):
                selected = template_list[idx]
                print_success(f"Selected: {TEMPLATES[selected]['name']}")
                return selected
        except ValueError:
            pass

        print_error("Invalid choice. Please enter a number between 1 and 5.")


def customize_project(
    template_id: str,
    non_interactive: bool = False,
    project_name_arg: Optional[str] = None,
    symbols_dir_arg: Optional[str] = None,
) -> tuple[str, str]:
    """Customize project name and symbols directory."""
    print_step(2, "Project Customization")

    # Project name
    default_name = detect_project_name()
    if non_interactive and project_name_arg:
        project_name = project_name_arg
    else:
        print()
        print_info(f"Detected project name from git/directory: {default_name}")
        project_name = prompt_input("Project name", default=default_name)

    while not validate_project_name(project_name):
        print_error("Invalid project name. Use only letters, numbers, hyphens, and underscores.")
        project_name = prompt_input("Project name", default=default_name)

    # Symbols directory
    default_symbols_dir = "ai"
    if non_interactive and symbols_dir_arg:
        symbols_dir = symbols_dir_arg
    else:
        print()
        print_info("The symbols directory will store all symbol files")
        symbols_dir = prompt_input("Symbols directory", default=default_symbols_dir)

    while not validate_directory(symbols_dir):
        print_error("Invalid directory. No leading or trailing slashes.")
        symbols_dir = prompt_input("Symbols directory", default=default_symbols_dir)

    print()
    print_success(f"Project: {project_name}")
    print_success(f"Symbols directory: {symbols_dir}")

    return project_name, symbols_dir


def preview_configuration(config: Dict[str, Any]) -> None:
    """Preview the configuration before writing."""
    print_step(3, "Configuration Preview")

    print()
    print(f"{Style.BRIGHT}Project Configuration:{Style.RESET_ALL}")
    print(f"  Project Name: {config['projectName']}")
    print(f"  Symbols Directory: {config['symbolsDir']}")
    print()

    print(f"{Style.BRIGHT}Domains:{Style.RESET_ALL}")
    for domain, domain_config in config["domains"].items():
        enabled = "✓" if domain_config.get("enabled", True) else "✗"
        print(f"  {enabled} {domain}: {domain_config['file']}")
        print(f"     {domain_config['description']}")

    if "apiLayers" in config and config["apiLayers"]:
        print()
        print(f"{Style.BRIGHT}API Layers:{Style.RESET_ALL}")
        for layer, layer_config in config["apiLayers"].items():
            enabled = "✓" if layer_config.get("enabled", True) else "✗"
            print(f"  {enabled} {layer}: {layer_config['file']}")
            print(f"     {layer_config['description']}")

    print()
    print(f"{Style.BRIGHT}Extraction Directories:{Style.RESET_ALL}")
    for lang, extraction in config["extraction"].items():
        print(f"  {lang.capitalize()}:")
        for directory in extraction["directories"]:
            print(f"    • {directory}")

    print()


def write_configuration(
    config: Dict[str, Any],
    output_path: Path,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    """
    Write configuration to file.

    Returns:
        True if written successfully, False otherwise
    """
    print_step(4, "Writing Configuration" if not dry_run else "Dry Run")

    # Update metadata
    if "metadata" not in config:
        config["metadata"] = {}

    config["metadata"]["lastUpdated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if "version" not in config["metadata"]:
        config["metadata"]["version"] = "1.0"

    # Validate against schema
    is_valid, error = validate_against_schema(config)
    if not is_valid:
        print_error(f"Configuration validation failed: {error}")
        return False

    print_success("Configuration validated against schema")

    # Check if file exists
    if output_path.exists() and not force and not dry_run:
        print_warning(f"Configuration file already exists: {output_path}")
        if not prompt_yes_no("Overwrite existing configuration?", default=False):
            print_info("Aborted. Use --force to overwrite without prompting.")
            return False

    if dry_run:
        print()
        print_info("Dry run mode - configuration not written")
        print()
        print(f"{Style.BRIGHT}Configuration preview:{Style.RESET_ALL}")
        print(json.dumps(config, indent=2))
        return True

    # Create directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write configuration
    try:
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)
            f.write("\n")  # Add trailing newline

        print()
        print_success(f"Configuration written to: {output_path}")
        return True
    except Exception as e:
        print_error(f"Failed to write configuration: {e}")
        return False


def show_next_steps(config: Dict[str, Any], output_path: Path) -> None:
    """Show next steps after configuration is created."""
    print()
    print_header("Next Steps", char="-")

    symbols_dir = config["symbolsDir"]
    has_python = "python" in config["extraction"]
    has_typescript = "typescript" in config["extraction"]

    print(f"{Style.BRIGHT}1. Generate Symbols:{Style.RESET_ALL}")
    if has_typescript:
        print(f"   {Fore.CYAN}python .claude/skills/symbols/scripts/extract_symbols_typescript.py{Style.RESET_ALL}")
    if has_python:
        print(f"   {Fore.CYAN}python .claude/skills/symbols/scripts/extract_symbols_python.py{Style.RESET_ALL}")
    print()

    print(f"{Style.BRIGHT}2. Validate Symbols:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python .claude/skills/symbols/scripts/validate_symbols.py{Style.RESET_ALL}")
    print()

    print(f"{Style.BRIGHT}3. Query Symbols:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python .claude/skills/symbols/scripts/symbol_tools.py{Style.RESET_ALL}")
    print()

    print(f"{Style.BRIGHT}4. Read Documentation:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}.claude/skills/symbols/CONFIG_README.md{Style.RESET_ALL}")
    print()

    print(f"{Style.BRIGHT}For Help:{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}python .claude/skills/symbols/scripts/init_symbols.py --help{Style.RESET_ALL}")
    print()


def main():
    """Main entry point for the wizard."""
    parser = argparse.ArgumentParser(
        description="Interactive symbols configuration wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with auto-detection (recommended)
  python init_symbols.py

  # Auto-detect and configure without prompts
  python init_symbols.py --auto-detect

  # Auto-detect with verbose output
  python init_symbols.py --auto-detect --verbose --dry-run

  # Load from custom config file
  python init_symbols.py --config-file=custom-paths.json

  # Quick setup with template
  python init_symbols.py --template=react-typescript-fullstack

  # Non-interactive with all options
  python init_symbols.py --template=python-fastapi --name="MyProject" --symbols-dir="ai" --force

  # List available templates
  python init_symbols.py --list

  # Dry run (preview without writing)
  python init_symbols.py --dry-run
        """,
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available templates and exit",
    )
    parser.add_argument(
        "--template",
        type=str,
        choices=list(TEMPLATES.keys()),
        help="Project template to use",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Project name",
    )
    parser.add_argument(
        "--symbols-dir",
        type=str,
        help="Symbols directory (default: ai)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for configuration file (default: auto-detect)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing configuration without prompting",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview configuration without writing",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick setup with defaults (implies --template if not specified)",
    )
    parser.add_argument(
        "--auto-detect",
        action="store_true",
        help="Automatically detect and use structure (skip prompts)",
    )
    parser.add_argument(
        "--config-file",
        type=Path,
        help="Load configuration from JSON file",
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Use detected structure without prompting",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed detection information",
    )

    args = parser.parse_args()

    # List templates and exit
    if args.list:
        list_templates()
        return 0

    # Handle config file mode
    if args.config_file:
        try:
            print_info(f"Loading configuration from: {args.config_file}")
            config = load_config_from_file(args.config_file)

            # Validate paths
            project_root = find_project_root()
            warnings = validate_paths(config, project_root)
            if warnings:
                print_warning("Path validation warnings:")
                for warning in warnings:
                    print(f"  - {warning}")
                print()
                if not args.force and not prompt_yes_no("Continue anyway?", default=False):
                    return 1

            # Determine output path
            output_path = args.output if args.output else project_root / ".claude" / "skills" / "symbols" / "symbols.config.json"

            # Write configuration
            success = write_configuration(config, output_path, dry_run=args.dry_run, force=args.force)
            if success and not args.dry_run:
                show_next_steps(config, output_path)
                return 0
            return 0 if success else 1
        except Exception as e:
            print_error(f"Failed to load config file: {e}")
            return 1

    # Determine if running in non-interactive mode
    non_interactive = bool(args.template and args.name and args.symbols_dir) or args.quick or args.auto_detect or args.no_interactive

    # Quick mode defaults
    if args.quick:
        if not args.template:
            args.template = "react-typescript-fullstack"
        if not args.symbols_dir:
            args.symbols_dir = "ai"
        non_interactive = True

    try:
        # Welcome screen (skip in non-interactive/auto-detect mode)
        if not non_interactive and not args.auto_detect:
            if not show_welcome():
                print_info("Setup cancelled.")
                return 0

        # Auto-detection phase
        detected_structure = None
        if args.auto_detect or (not args.template and not non_interactive):
            print_step(1, "Automatic Codebase Detection")
            project_root = find_project_root()
            detected_structure = detect_codebase_structure(project_root, verbose=args.verbose)

            # Show detection results
            show_detection_results(detected_structure)

            # Auto-detect mode: use detected template
            if args.auto_detect or args.no_interactive:
                if detected_structure.get("suggested_template"):
                    args.template = detected_structure["suggested_template"]
                    print()
                    print_success(f"Auto-selected template: {TEMPLATES[args.template]['name']}")
                    # Set defaults for project name and symbols dir if not provided
                    if not args.name:
                        args.name = detect_project_name()
                    if not args.symbols_dir:
                        args.symbols_dir = "ai"
                else:
                    print_error("Could not auto-detect appropriate template")
                    print_info("Please run without --auto-detect to select manually")
                    return 1
            else:
                # Interactive mode: prompt user
                choice = prompt_detection_choice()

                if choice == 1:
                    # Use detected structure
                    if detected_structure.get("suggested_template"):
                        args.template = detected_structure["suggested_template"]
                        print_success(f"Using detected template: {TEMPLATES[args.template]['name']}")
                    else:
                        print_warning("No template auto-detected, falling back to manual selection")
                        # Fall through to manual template selection
                elif choice == 2:
                    # Customize interactively - will use template selection below
                    print_info("Proceeding with interactive customization...")
                elif choice == 3:
                    # Load from config file
                    config_file_path = Path(prompt_input("Config file path"))
                    try:
                        config = load_config_from_file(config_file_path)
                        project_root = find_project_root()
                        warnings = validate_paths(config, project_root)
                        if warnings:
                            print_warning("Path validation warnings:")
                            for warning in warnings:
                                print(f"  - {warning}")

                        output_path = args.output if args.output else project_root / ".claude" / "skills" / "symbols" / "symbols.config.json"
                        success = write_configuration(config, output_path, dry_run=args.dry_run, force=args.force)
                        if success and not args.dry_run:
                            show_next_steps(config, output_path)
                        return 0 if success else 1
                    except Exception as e:
                        print_error(f"Failed to load config file: {e}")
                        return 1

        # Template selection (if not already set by detection)
        if not args.template:
            template_id = select_template(non_interactive, args.template)
        else:
            template_id = args.template

        # Load template
        template_config = load_template(template_id)

        # Project customization
        project_name, symbols_dir = customize_project(
            template_id,
            non_interactive,
            args.name,
            args.symbols_dir,
        )

        # Replace placeholders
        config = replace_placeholders(template_config, project_name, symbols_dir)

        # Preview configuration (skip in quick mode)
        if not args.quick:
            preview_configuration(config)

            if not non_interactive:
                print()
                if not prompt_yes_no("Proceed with this configuration?", default=True):
                    print_info("Setup cancelled.")
                    return 0

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            # Default to .claude/skills/symbols/symbols.config.json
            project_root = find_project_root()
            output_path = project_root / ".claude" / "skills" / "symbols" / "symbols.config.json"

        # Write configuration
        success = write_configuration(
            config,
            output_path,
            dry_run=args.dry_run,
            force=args.force,
        )

        if success and not args.dry_run:
            show_next_steps(config, output_path)
            return 0
        elif success:
            return 0
        else:
            return 1

    except KeyboardInterrupt:
        print()
        print_info("Setup cancelled by user.")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if "--debug" in sys.argv:
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())

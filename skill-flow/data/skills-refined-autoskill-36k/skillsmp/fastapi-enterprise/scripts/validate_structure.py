#!/usr/bin/env python3
"""
Validate FastAPI project structure compliance with enterprise standards.

Checks:
- app.py exists at root
- Required core modules exist
- Auto-discovery routes structure
- No duplicate code (basic check)
- Models/schemas/services organization
"""

import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    """Terminal colors."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def check_exists(path: Path, description: str) -> Tuple[bool, str]:
    """Check if file or directory exists."""
    if path.exists():
        return True, f"{Colors.GREEN}✅{Colors.RESET} {description}: {path}"
    else:
        return False, f"{Colors.RED}❌{Colors.RESET} {description} missing: {path}"


def check_app_py() -> Tuple[bool, str]:
    """Check if app.py exists at root with correct structure."""
    app_path = Path("app.py")
    
    if not app_path.exists():
        return False, f"{Colors.RED}❌{Colors.RESET} app.py missing at project root (required for pipeline)"
    
    content = app_path.read_text()
    
    # Check required imports
    required = [
        "from fastapi import FastAPI",
        "from core.logging import",
        "from core.config import",
        "from api.routes import register_routes",
    ]
    
    missing = [req for req in required if req not in content]
    
    if missing:
        return False, f"{Colors.YELLOW}⚠️{Colors.RESET} app.py exists but missing imports: {', '.join(missing)}"
    
    return True, f"{Colors.GREEN}✅{Colors.RESET} app.py correct at root"


def check_core_modules() -> List[Tuple[bool, str]]:
    """Check core modules exist with correct content."""
    results = []
    
    core_modules = {
        "core/logging.py": ["structlog", "configure_logging", "get_logger"],
        "core/config.py": ["pydantic_settings", "Settings", "get_settings"],
        "core/db.py": ["AsyncSession", "async_sessionmaker", "get_db"],
        "core/httpx.py": ["httpx", "AsyncClient", "HTTPClient"],
    }
    
    for module_path, required_items in core_modules.items():
        path = Path(module_path)
        
        if not path.exists():
            results.append((False, f"{Colors.RED}❌{Colors.RESET} Missing: {module_path}"))
            continue
        
        content = path.read_text()
        missing = [item for item in required_items if item not in content]
        
        if missing:
            results.append((
                False,
                f"{Colors.YELLOW}⚠️{Colors.RESET} {module_path} missing: {', '.join(missing)}"
            ))
        else:
            results.append((True, f"{Colors.GREEN}✅{Colors.RESET} {module_path} correct"))
    
    return results


def check_routes_structure() -> List[Tuple[bool, str]]:
    """Check API routes structure."""
    results = []
    
    routes_dir = Path("api/routes")
    
    if not routes_dir.exists():
        results.append((False, f"{Colors.RED}❌{Colors.RESET} Missing: api/routes/ directory"))
        return results
    
    # Check __init__.py has auto-discovery
    init_file = routes_dir / "__init__.py"
    if not init_file.exists():
        results.append((False, f"{Colors.RED}❌{Colors.RESET} Missing: api/routes/__init__.py"))
    else:
        content = init_file.read_text()
        if "register_routes" not in content:
            results.append((
                False,
                f"{Colors.YELLOW}⚠️{Colors.RESET} api/routes/__init__.py missing auto-discovery (register_routes)"
            ))
        else:
            results.append((True, f"{Colors.GREEN}✅{Colors.RESET} Auto-discovery routes configured"))
    
    # Check for version directories
    version_dirs = [d for d in routes_dir.iterdir() if d.is_dir() and d.name.startswith("v")]
    
    if version_dirs:
        results.append((True, f"{Colors.GREEN}✅{Colors.RESET} Found versioned routes: {', '.join(d.name for d in version_dirs)}"))
    else:
        results.append((
            False,
            f"{Colors.YELLOW}⚠️{Colors.RESET} No versioned route directories (v1, v2, etc.) found"
        ))
    
    return results


def check_middleware() -> List[Tuple[bool, str]]:
    """Check middleware configuration."""
    results = []
    
    middleware_file = Path("middleware/conversation.py")
    
    if not middleware_file.exists():
        results.append((False, f"{Colors.RED}❌{Colors.RESET} Missing: middleware/conversation.py"))
        return results
    
    content = middleware_file.read_text()
    
    required = ["ConversationMiddleware", "get_conversation_id", "X-Conversation-ID"]
    missing = [item for item in required if item not in content]
    
    if missing:
        results.append((
            False,
            f"{Colors.YELLOW}⚠️{Colors.RESET} middleware/conversation.py missing: {', '.join(missing)}"
        ))
    else:
        results.append((True, f"{Colors.GREEN}✅{Colors.RESET} Conversation tracking middleware configured"))
    
    return results


def check_config_files() -> List[Tuple[bool, str]]:
    """Check configuration files."""
    results = []
    
    config_dir = Path("config")
    
    if not config_dir.exists():
        results.append((False, f"{Colors.YELLOW}⚠️{Colors.RESET} config/ directory not found"))
        return results
    
    for env in ["development.yml", "production.yml"]:
        config_file = config_dir / env
        exists, msg = check_exists(config_file, f"Config file {env}")
        results.append((exists, msg))
    
    return results


def check_alembic() -> List[Tuple[bool, str]]:
    """Check Alembic configuration."""
    results = []
    
    alembic_ini = Path("alembic.ini")
    exists, msg = check_exists(alembic_ini, "Alembic configuration")
    results.append((exists, msg))
    
    if not exists:
        return results
    
    env_file = Path("alembic/env.py")
    if not env_file.exists():
        results.append((False, f"{Colors.RED}❌{Colors.RESET} Missing: alembic/env.py"))
        return results
    
    content = env_file.read_text()
    
    # Check if it uses core/db.py
    if "from core.db import" in content and "from core.config import" in content:
        results.append((True, f"{Colors.GREEN}✅{Colors.RESET} Alembic env.py uses central DB configuration"))
    else:
        results.append((
            False,
            f"{Colors.YELLOW}⚠️{Colors.RESET} Alembic env.py should import from core/db.py and core/config.py"
        ))
    
    return results


def check_duplicate_code() -> List[Tuple[bool, str]]:
    """Basic check for duplicate code patterns."""
    results = []
    
    # This is a simplified check - in production, use tools like pylint, radon
    # Check for repeated database session creation (should use get_db dependency)
    
    py_files = list(Path("api").rglob("*.py"))
    
    issues = []
    for py_file in py_files:
        content = py_file.read_text()
        
        # Check for inline session creation instead of using get_db
        if "AsyncSession(" in content and "Depends(get_db)" not in content:
            if "get_db" not in py_file.name:  # Ignore core/db.py
                issues.append(f"{py_file}: Creating session inline instead of using Depends(get_db)")
    
    if issues:
        results.append((
            False,
            f"{Colors.YELLOW}⚠️{Colors.RESET} Potential duplicate code found:\n   " + "\n   ".join(issues)
        ))
    else:
        results.append((True, f"{Colors.GREEN}✅{Colors.RESET} No obvious duplicate code patterns found"))
    
    return results


def main() -> None:
    """Main validation entry point."""
    print(f"\n{Colors.BLUE}🔍 Validating FastAPI Enterprise Project Structure{Colors.RESET}\n")
    
    # Check if we're in a project root
    if not Path("app.py").exists() and not Path("api").exists():
        print(f"{Colors.RED}❌ Not in a FastAPI project root directory{Colors.RESET}")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    all_results = []
    
    # Run all checks
    print(f"{Colors.BLUE}📋 Checking project structure...{Colors.RESET}\n")
    
    # app.py
    result = check_app_py()
    all_results.append(result)
    print(result[1])
    
    print()
    
    # Core modules
    print(f"{Colors.BLUE}📋 Checking core modules...{Colors.RESET}\n")
    core_results = check_core_modules()
    all_results.extend(core_results)
    for _, msg in core_results:
        print(msg)
    
    print()
    
    # Routes structure
    print(f"{Colors.BLUE}📋 Checking routes structure...{Colors.RESET}\n")
    routes_results = check_routes_structure()
    all_results.extend(routes_results)
    for _, msg in routes_results:
        print(msg)
    
    print()
    
    # Middleware
    print(f"{Colors.BLUE}📋 Checking middleware...{Colors.RESET}\n")
    middleware_results = check_middleware()
    all_results.extend(middleware_results)
    for _, msg in middleware_results:
        print(msg)
    
    print()
    
    # Config files
    print(f"{Colors.BLUE}📋 Checking configuration files...{Colors.RESET}\n")
    config_results = check_config_files()
    all_results.extend(config_results)
    for _, msg in config_results:
        print(msg)
    
    print()
    
    # Alembic
    print(f"{Colors.BLUE}📋 Checking Alembic configuration...{Colors.RESET}\n")
    alembic_results = check_alembic()
    all_results.extend(alembic_results)
    for _, msg in alembic_results:
        print(msg)
    
    print()
    
    # Duplicate code
    print(f"{Colors.BLUE}📋 Checking for code duplication...{Colors.RESET}\n")
    duplicate_results = check_duplicate_code()
    all_results.extend(duplicate_results)
    for _, msg in duplicate_results:
        print(msg)
    
    print()
    
    # Summary
    passed = sum(1 for result, _ in all_results if result)
    total = len(all_results)
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}Summary: {passed}/{total} checks passed{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✅ Project structure is compliant with enterprise standards!{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"{Colors.YELLOW}⚠️  Some checks failed. Review the issues above.{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

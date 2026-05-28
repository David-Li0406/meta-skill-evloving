from __future__ import annotations

import argparse
import re
from pathlib import Path

BASE_REQUIRED_PATHS = [
    "pyproject.toml",
    "src/main.py",
    "src/core/config.py",
    "src/utils",
    "tests",
]


CLIENT_LIB_HINTS = {
    "httpx",
    "requests",
    "aiohttp",
    "sqlalchemy",
    "asyncpg",
    "psycopg",
    "psycopg2",
    "redis",
    "aioredis",
    "pymongo",
    "boto3",
    "botocore",
}


def _exists(base: Path, rel: str) -> bool:
    return (base / rel).exists()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _to_py_identifier(value: str) -> str:
    ident = re.sub(r"[^0-9a-zA-Z_]+", "_", value).strip("_").lower()
    if not ident:
        ident = "service"
    if ident[0].isdigit():
        ident = f"svc_{ident}"
    return ident


def _infer_service_name(base: Path) -> str:
    # Prefer Settings.SERVICE_NAME default value if present; fallback to project folder name.
    cfg_path = base / "src" / "core" / "config.py"
    cfg = _read_text(cfg_path)
    m = re.search(r'SERVICE_NAME\s*:\s*str\s*=\s*["\']([^"\']+)["\']', cfg)
    if m:
        return m.group(1)
    return base.name


def _detect_client_usage(base: Path) -> bool:
    # If clients directory already exists, treat as client usage.
    if (base / "src" / "services" / "clients").exists():
        return True

    pyproject = _read_text(base / "pyproject.toml").lower()
    if any(hint in pyproject for hint in CLIENT_LIB_HINTS):
        return True

    # Heuristic: scan a few likely folders for imports.
    for rel in ["src/api", "src/services", "src/core", "src"]:
        root = base / rel
        if not root.exists():
            continue
        for p in root.rglob("*.py"):
            text = _read_text(p)
            if re.search(r"^\s*import\s+(" + "|".join(CLIENT_LIB_HINTS) + r")\b", text, re.M):
                return True
            if re.search(r"^\s*from\s+(" + "|".join(CLIENT_LIB_HINTS) + r")\b", text, re.M):
                return True

    return False


def _find_v1_include_router(main_py: str) -> tuple[bool, bool, str | None]:
    # Returns: (has_v1_prefix, has_tags, router_expr)
    m = re.search(
        r"include_router\(\s*([^,]+)\s*,\s*prefix\s*=\s*['\"]\/v1['\"]([^)]*)\)",
        main_py,
        re.S,
    )
    if not m:
        return (False, False, None)

    router_expr = m.group(1).strip()
    tail = m.group(2)
    has_tags = bool(re.search(r"tags\s*=\s*\[", tail))
    return (True, has_tags, router_expr)


def _is_generic_router_name(expr: str) -> bool:
    generic = {"router", "v1_router", "api_router", "routes", "r"}
    return expr in generic


def _client_singleton_heuristic(client_dir: Path) -> list[str]:
    findings: list[str] = []
    if not client_dir.exists():
        findings.append("Missing src/services/clients directory (needed because client usage was detected).")
        return findings

    py_files = list(client_dir.glob("*.py"))
    if not py_files:
        findings.append("No client modules found under src/services/clients (expected singleton clients here).")
        return findings

    for f in py_files:
        text = _read_text(f)
        if "@lru_cache" not in text and "_instance" not in text:
            findings.append(
                f"Client module may not be singleton: {f.as_posix()} (expected @lru_cache factory or equivalent)."
            )
    return findings


def audit(project_dir: Path) -> str:
    base = project_dir.resolve()
    service_name = _infer_service_name(base)
    service_py = _to_py_identifier(service_name)

    report: list[str] = []
    report.append("# FastAPI Project Audit")
    report.append(f"Project: `{base}`")
    report.append(f"Inferred service name: `{service_name}` (suggested router alias: `{service_py}_router`)")
    report.append("")

    report.append("## 1) Required structure")
    missing = [p for p in BASE_REQUIRED_PATHS if not _exists(base, p)]
    if missing:
        report.append("Missing:")
        for p in missing:
            report.append(f"- {p}")
    else:
        report.append("OK: base required paths exist.")
    report.append("")

    report.append("## 2) API versioning and router naming (src/main.py)")
    main_py_path = base / "src" / "main.py"
    main_text = _read_text(main_py_path)

    has_v1, has_tags, router_expr = _find_v1_include_router(main_text)
    if not has_v1:
        report.append("- Missing /v1 router include. Expected:")
        report.append(f'  `app.include_router({service_py}_router, prefix="/v1", tags=["{service_py}"])`')
    else:
        report.append("- /v1 router include found.")
        if router_expr and _is_generic_router_name(router_expr):
            report.append(
                f"- Router variable name looks generic (`{router_expr}`). Consider aliasing to `{service_py}_router`."
            )
        if not has_tags:
            report.append(f'- Missing tags on /v1 include. Consider: `tags=["{service_py}"]`.')
    report.append("")

    clients_used = _detect_client_usage(base)

    report.append("## 3) External clients (only if needed)")
    if not clients_used:
        report.append("No client usage detected. Skipping clients requirements and checks.")
    else:
        report.append("Client usage detected. Enforcing clients best practices.")
        client_findings = _client_singleton_heuristic(base / "src" / "services" / "clients")
        if client_findings:
            report.append("Findings:")
            for f in client_findings:
                report.append(f"- {f}")
        else:
            report.append("OK: client singletons look reasonable.")
    report.append("")

    report.append("## 4) Quick refactor plan (objective)")
    plan: list[str] = []
    i = 1

    for p in missing:
        plan.append(f"{i}. Create `{p}` according to the blueprint structure.")
        i += 1

    if not has_v1:
        plan.append(f"{i}. Update `src/main.py` to include `/v1` router with a project-relevant alias and tags.")
        plan.append(f'   - Recommended: `app.include_router({service_py}_router, prefix="/v1", tags=["{service_py}"])`')
        i += 1
    else:
        if router_expr and _is_generic_router_name(router_expr):
            plan.append(
                f"{i}. Rename router alias in `src/main.py` to be project-relevant (e.g., `{service_py}_router`)."
            )
            i += 1
        if not has_tags:
            plan.append(f'{i}. Add tags to the /v1 include (e.g., `tags=["{service_py}"]`).')
            i += 1

    if clients_used:
        plan.append(
            f"{i}. Ensure all external clients live in `src/services/clients/` and are implemented as singletons "
            "(e.g., `@lru_cache`)."
        )
        i += 1

    plan.append(f"{i}. Run quality gates: `uv run task lint_fix` then `uv run task test`.")
    report.extend(plan)
    report.append("")

    return "\n".join(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.parse_args()


if __name__ == "__main__":
    main()

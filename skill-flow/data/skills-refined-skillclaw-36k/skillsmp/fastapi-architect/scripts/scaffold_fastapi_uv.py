from __future__ import annotations

import argparse
import re
from pathlib import Path


def _read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_file(path: Path, content: str, *, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def _touch_init(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
    init_file = dir_path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")


def _apply_replacements(content: str, repl: dict[str, str]) -> str:
    for k, v in repl.items():
        content = content.replace(k, v)
    return content


def _to_py_identifier(value: str) -> str:
    ident = re.sub(r"[^0-9a-zA-Z_]+", "_", value).strip("_").lower()
    if not ident:
        ident = "service"
    if ident[0].isdigit():
        ident = f"svc_{ident}"
    return ident


def scaffold(
    project_dir: Path,
    service_name: str,
    app_title: str,
    python_version: str,
    overwrite: bool,
    with_http_client: bool,
) -> None:
    base = project_dir.resolve()
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"

    service_py = _to_py_identifier(service_name)

    repl = {
        "__SERVICE_NAME__": service_name,
        "__SERVICE_PY__": service_py,
        "__APP_TITLE__": app_title,
        "__PYTHON_VERSION__": python_version,
    }

    # Root files
    pyproject_tmpl = "pyproject_with_httpx.tmpl" if with_http_client else "pyproject_no_clients.tmpl"
    _write_file(
        base / "pyproject.toml",
        _apply_replacements(_read_template(templates / pyproject_tmpl), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / ".python-version",
        _apply_replacements(_read_template(templates / "python-version.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "Dockerfile",
        _apply_replacements(_read_template(templates / "Dockerfile.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "README.md",
        _apply_replacements(_read_template(templates / "README.md.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / ".env.example",
        _apply_replacements(_read_template(templates / "env.example.tmpl"), repl),
        overwrite=overwrite,
    )

    # src structure
    _touch_init(base / "src")
    _touch_init(base / "src" / "core")
    _touch_init(base / "src" / "api")
    _touch_init(base / "src" / "api" / "v1")
    _touch_init(base / "src" / "api" / "v1" / "endpoints")
    _touch_init(base / "src" / "api" / "v2")
    _touch_init(base / "src" / "schemas")
    _touch_init(base / "src" / "services")
    _touch_init(base / "src" / "utils")

    _write_file(
        base / "src" / "core" / "config.py",
        _apply_replacements(_read_template(templates / "src_core_config.py.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "src" / "core" / "log_config.py",
        _apply_replacements(_read_template(templates / "src_core_log_config.py.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "src" / "core" / "logger_func.py",
        _apply_replacements(_read_template(templates / "src_core_logger_func.py.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "src" / "core" / "errors.py",
        _apply_replacements(_read_template(templates / "src_core_errors.py.tmpl"), repl),
        overwrite=overwrite,
    )

    deps_tmpl = "src_api_deps_with_httpx.py.tmpl" if with_http_client else "src_api_deps_no_clients.py.tmpl"
    _write_file(
        base / "src" / "api" / "deps.py",
        _apply_replacements(_read_template(templates / deps_tmpl), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "src" / "api" / "v1" / "router.py",
        _apply_replacements(_read_template(templates / "src_api_v1_router.py.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "src" / "api" / "v1" / "endpoints" / "health.py",
        _apply_replacements(_read_template(templates / "src_api_v1_health.py.tmpl"), repl),
        overwrite=overwrite,
    )

    main_tmpl = "src_main_with_httpx.py.tmpl" if with_http_client else "src_main_no_clients.py.tmpl"
    _write_file(
        base / "src" / "main.py",
        _apply_replacements(_read_template(templates / main_tmpl), repl),
        overwrite=overwrite,
    )

    # Optional clients
    if with_http_client:
        _touch_init(base / "src" / "services" / "clients")
        _write_file(
            base / "src" / "services" / "clients" / "httpx_client.py",
            _apply_replacements(_read_template(templates / "src_services_clients_httpx.py.tmpl"), repl),
            overwrite=overwrite,
        )

    # tests
    _touch_init(base / "tests")
    _write_file(
        base / "tests" / "conftest.py",
        _apply_replacements(_read_template(templates / "tests_conftest.py.tmpl"), repl),
        overwrite=overwrite,
    )
    _write_file(
        base / "tests" / "test_health.py",
        _apply_replacements(_read_template(templates / "tests_test_health.py.tmpl"), repl),
        overwrite=overwrite,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--service-name", required=True)
    parser.add_argument("--app-title", required=True)
    parser.add_argument("--python-version", default="3.14.2")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--with-http-client",
        action="store_true",
        help="Create src/services/clients/httpx_client.py and wire it via lifespan.",
    )
    args = parser.parse_args()

    scaffold(
        project_dir=Path(args.project_dir),
        service_name=args.service_name,
        app_title=args.app_title,
        python_version=args.python_version,
        overwrite=bool(args.overwrite),
        with_http_client=bool(args.with_http_client),
    )


if __name__ == "__main__":
    main()

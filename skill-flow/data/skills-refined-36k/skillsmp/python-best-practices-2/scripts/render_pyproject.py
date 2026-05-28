from __future__ import annotations

import argparse
from pathlib import Path


def _render_template(template: str, service_name: str, app_title: str) -> str:
    return template.replace("__SERVICE_NAME__", service_name).replace("__APP_TITLE__", app_title)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", default="assets/templates/pyproject.toml.tmpl")
    parser.add_argument("--out", default="pyproject.toml")
    parser.add_argument("--service-name", required=True)
    parser.add_argument("--app-title", required=True)
    args = parser.parse_args()

    template_path = Path(args.template)
    out_path = Path(args.out)

    template = template_path.read_text(encoding="utf-8")
    rendered = _render_template(template, args.service_name, args.app_title)

    out_path.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

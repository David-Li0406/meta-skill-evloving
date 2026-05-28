from __future__ import annotations

import logging
import re
from pathlib import Path

_TASK_LINT_FIX_RE = re.compile(r'^\s*lint_fix\s*=\s*".+"', re.MULTILINE)
_LOGGER = logging.getLogger(__name__)


def main() -> int:
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        _LOGGER.error("MISSING: pyproject.toml")
        return 2

    content = pyproject.read_text(encoding="utf-8")
    if "[tool.taskipy.tasks]" not in content:
        _LOGGER.error("MISSING: [tool.taskipy.tasks]")
        return 3

    if not _TASK_LINT_FIX_RE.search(content):
        _LOGGER.error('MISSING: task "lint_fix"')
        return 4

    _LOGGER.info("OK: task lint_fix found")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())

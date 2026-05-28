---
name: test-generator
description: Generate unittest test files for untested cvp/ modules. Use for test creation.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Test Generator

Generate unittest-based tests for cvp/ modules.

## Path Mapping

`cvp/module/file.py` -> `tester/module/test_file.py`

## Naming

- Class: `{ClassName}TestCase(TestCase)`
- Method: `test_{description}` (snake_case)

## Required Tests

1. `test_default` - Normal behavior
2. `test_none`/`test_empty` - Edge cases
3. `test_raises_*` - Exceptions

## Template

```python
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from cvp.module.file import TargetClass


class TargetClassTestCase(TestCase):
    def setUp(self):
        pass

    def test_default(self):
        pass


if __name__ == "__main__":
    main()
```

## Special Cases

- External deps: `@skipIf(not which("cmd"), "not found")`
- File I/O: Use `NamedTemporaryFile`
- Async: Use `asyncio.run()`

## Verify

```bash
./pytest.sh tester/{module}/test_{name}.py
```

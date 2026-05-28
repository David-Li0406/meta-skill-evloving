import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

# Make fallback module importable without installing as a package
sys.path.append(str(Path(__file__).parent))
import runs_tools as rt  # noqa: E402


class RunsToolsFallbackTests(unittest.TestCase):
    def test_count_pattern_invalid_regex_returns_null(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write("content\n")
            tmp.flush()
            args = SimpleNamespace(
                file=tmp.name,
                regex="[",
                fallback_regex=None,
                null_if_zero=False,
            )
            buf = StringIO()
            with redirect_stdout(buf):
                rt.cmd_count_pattern(args)

        self.assertEqual(buf.getvalue().strip(), "null")
        Path(tmp.name).unlink(missing_ok=True)

    def test_yaml_get_handles_indented_keys(self) -> None:
        yaml_block = """```yaml
tests:
  passed: 3
```
"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(yaml_block)
            tmp.flush()
            args = SimpleNamespace(file=tmp.name, key="passed", null_if_missing=False)
            buf = StringIO()
            with redirect_stdout(buf):
                rt.cmd_yaml_get(args)

        self.assertEqual(buf.getvalue().strip(), "3")
        Path(tmp.name).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

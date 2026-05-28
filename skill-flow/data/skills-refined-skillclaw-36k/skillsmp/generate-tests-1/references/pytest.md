# pytest (Python)

Use for Python projects using pytest. Load when targeting pytest. Prefer fixtures/parametrize over ad-hoc setup to keep tests DRY. Use reStructuredText docstrings for helpers when documenting utilities.

```python
from typing import Any, Dict

import pytest
from module import function_under_test


class TestFunctionName:
    @pytest.fixture
    def setup_data(self) -> Dict[str, Any]:
        return {"key": "value"}

    def test_valid_input_returns_expected(self, setup_data: Dict[str, Any]) -> None:
        input_data = setup_data
        result = function_under_test(input_data)
        assert result == expected_output

    def test_empty_input_returns_default(self) -> None:
        assert function_under_test([]) == default_value

    def test_invalid_input_raises_exception(self) -> None:
        with pytest.raises(ExpectedError):
            function_under_test(invalid_input)

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (0, 0),
    ])
    def test_parameterized(self, input: Any, expected: Any) -> None:
        assert function_under_test(input) == expected
```

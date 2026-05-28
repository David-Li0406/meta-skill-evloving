# Level 2: Utility Functions Examples

Reusable helper functions, data transformations, format conversions using `gpt-5.1-codex-max` model (auto-selected). Parallel execution with dependency analysis.

---

## Example 1: Data Validators

Validation functions for common data formats (email, phone, ID card).

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: validators
backend: codex
workdir: /home/user/utils
model: gpt-5.1-codex-max
---CONTENT---
编写邮箱、手机号、身份证号验证函数集合（支持中国格式）
---END---
EOF
```

### Expected Output

```
▶ validators (codex/gpt-5.2-codex)

```python
import re
from typing import Optional

class Validators:
    """数据验证工具集"""

    @staticmethod
    def email(value: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def phone(value: str) -> bool:
        """验证中国手机号（11位，1开头）"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, value))

    @staticmethod
    def id_card(value: str) -> bool:
        """验证身份证号（18位，含校验位）"""
        if len(value) != 18:
            return False

        weights = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
        check_codes = '10X98765432'

        total = sum(int(value[i]) * weights[i] for i in range(17))
        return check_codes[total % 11] == value[-1].upper()

    @staticmethod
    def url(value: str) -> bool:
        """验证URL格式"""
        pattern = r'^https?://[\w\.-]+(:\d+)?(/.*)?$'
        return bool(re.match(pattern, value))
```

» 写入 validators.py
✓ validators 2.5s
```

### Usage

```python
from validators import Validators

assert Validators.email("user@example.com") == True
assert Validators.phone("13912345678") == True
assert Validators.id_card("11010119900101001X") == True
```

### Customization Tips

- Add international phone formats: `r'^\+?[1-9]\d{1,14}$'`
- Support IPv4/IPv6 validation
- Add credit card number validation (Luhn algorithm)

---

## Example 2: Format Converter

Convert between JSON, YAML, and TOML configuration formats.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: format-converter
backend: codex
workdir: /home/user/utils
model: gpt-5.1-codex-max
---CONTENT---
JSON/YAML/TOML格式互转工具类，支持文件和字符串输入
---END---
EOF
```

### Expected Output

```
▶ format-converter (codex/gpt-5.2-codex)

```python
import json
import yaml
try:
    import tomli
    import tomli_w
except ImportError:
    print("Install: pip install tomli tomli-w")

class FormatConverter:
    """配置文件格式转换工具"""

    @staticmethod
    def json_to_yaml(json_str: str) -> str:
        """JSON转YAML"""
        data = json.loads(json_str)
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def yaml_to_json(yaml_str: str) -> str:
        """YAML转JSON"""
        data = yaml.safe_load(yaml_str)
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def json_to_toml(json_str: str) -> str:
        """JSON转TOML"""
        data = json.loads(json_str)
        return tomli_w.dumps(data)

    @staticmethod
    def toml_to_json(toml_str: str) -> str:
        """TOML转JSON"""
        data = tomli.loads(toml_str)
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def convert_file(input_path: str, output_path: str):
        """文件转换（自动识别格式）"""
        with open(input_path, 'r') as f:
            content = f.read()

        # 自动识别输入格式
        if input_path.endswith('.json'):
            data = json.loads(content)
        elif input_path.endswith('.yaml') or input_path.endswith('.yml'):
            data = yaml.safe_load(content)
        elif input_path.endswith('.toml'):
            data = tomli.loads(content)
        else:
            raise ValueError("Unsupported input format")

        # 根据输出格式写入
        with open(output_path, 'w') as f:
            if output_path.endswith('.json'):
                json.dump(data, f, indent=2, ensure_ascii=False)
            elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            elif output_path.endswith('.toml'):
                f.write(tomli_w.dumps(data))
```

» 写入 format_converter.py
✓ format-converter 3.2s
```

### Usage

```python
from format_converter import FormatConverter

# String conversion
json_str = '{"name": "Alice", "age": 30}'
yaml_output = FormatConverter.json_to_yaml(json_str)

# File conversion
FormatConverter.convert_file("config.json", "config.yaml")
```

### Customization Tips

- Add XML support via `xml.etree.ElementTree`
- Support `.env` file parsing
- Add validation before conversion
- Preserve comments (for YAML/TOML)

---

## Example 3: Simple Unit Tests

Write basic test cases for utility functions.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: test-validators
backend: codex
workdir: /home/user/utils
model: gpt-5.1-codex-max
files: ./validators.py
files-mode: ref
---CONTENT---
为validators.py编写pytest测试用例，覆盖正常和边界情况
---END---
EOF
```

### Expected Output

```
▶ test-validators (codex/gpt-5.2-codex)
  📄 validators.py (1.2KB)

```python
import pytest
from validators import Validators

class TestValidators:
    """Validators测试套件"""

    def test_email_valid(self):
        """测试有效邮箱"""
        assert Validators.email("user@example.com")
        assert Validators.email("test.user@sub.example.co.uk")

    def test_email_invalid(self):
        """测试无效邮箱"""
        assert not Validators.email("invalid")
        assert not Validators.email("@example.com")
        assert not Validators.email("user@")

    def test_phone_valid(self):
        """测试有效手机号"""
        assert Validators.phone("13912345678")
        assert Validators.phone("18812345678")

    def test_phone_invalid(self):
        """测试无效手机号"""
        assert not Validators.phone("12345678901")  # 不以1开头
        assert not Validators.phone("139123456")    # 长度不足
        assert not Validators.phone("139123456789") # 长度过长

    def test_id_card_valid(self):
        """测试有效身份证号"""
        assert Validators.id_card("11010119900101001X")

    def test_id_card_invalid(self):
        """测试无效身份证号"""
        assert not Validators.id_card("110101199001010011")  # 校验位错误
        assert not Validators.id_card("12345")              # 长度不足

    @pytest.mark.parametrize("url,expected", [
        ("https://example.com", True),
        ("http://localhost:8080/path", True),
        ("ftp://example.com", False),
        ("not-a-url", False),
    ])
    def test_url(self, url, expected):
        """参数化测试URL验证"""
        assert Validators.url(url) == expected
```

» 写入 test_validators.py
✓ test-validators 2.8s
```

### Usage

```bash
pytest test_validators.py -v
# Runs all test cases with verbose output
```

### Customization Tips

- Add test fixtures for shared data: `@pytest.fixture`
- Use `pytest.raises()` for exception testing
- Add coverage reporting: `pytest --cov=validators`
- Mock external dependencies with `unittest.mock`

---

## Common Level 2 Task Patterns

### Validation Libraries
- Input sanitization (SQL injection, XSS prevention)
- Data type checking (is_int, is_float, is_date)
- Business rule validation (age range, credit limit)

### Data Transformation
- String utilities (camelCase ↔ snake_case, slugify)
- Date/time formatting (timezone conversion, relative time)
- Number formatting (currency, percentage, file size)

### Format Conversion
- Serialization (pickle, msgpack, protobuf)
- Encoding (base64, hex, URL encoding)
- Compression (gzip, zlib, bzip2)

### Testing Utilities
- Mock data generators (fake names, emails, addresses)
- Test helpers (setup/teardown fixtures)
- Assertion utilities (deep equality, fuzzy matching)

---

## Example 4: Multi-Task with Dependency Analysis + Parallel Execution

This example demonstrates L2 parallel execution with automatic dependency analysis.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: string-utils
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
---CONTENT---
字符串工具函数 (utils/strings.py)：
- camelCase ↔ snake_case 转换
- slugify 函数
- truncate 带省略号
---END---
---TASK---
id: date-utils
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
---CONTENT---
日期工具函数 (utils/dates.py)：
- 相对时间显示 ("3天前")
- 时区转换
- 日期格式化
---END---
---TASK---
id: number-utils
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
---CONTENT---
数字工具函数 (utils/numbers.py)：
- 货币格式化
- 文件大小格式化 (KB/MB/GB)
- 百分比格式化
---END---
---TASK---
id: utils-index
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
dependencies: string-utils, date-utils, number-utils
---CONTENT---
创建 utils/__init__.py：
- 导出所有工具函数
- 添加版本号
- 编写模块 docstring
---END---
---TASK---
id: utils-tests
backend: codex
model: gpt-5.1-codex-max
workdir: ./utils
files: ./utils/strings.py, ./utils/dates.py, ./utils/numbers.py
files-mode: ref
dependencies: utils-index
---CONTENT---
为所有工具函数编写 pytest 测试 (tests/test_utils.py)
---END---
EOF
```

### Execution Flow (Auto-Generated DAG)

```
Phase 1: Parallel Execution (No Dependencies)
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ string-utils│  │ date-utils  │  │ number-utils│
│   2.1s      │  │   2.3s      │  │   1.9s      │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ↓
Phase 2: Sequential (Depends on Phase 1)
              ┌─────────────┐
              │ utils-index │
              │   1.2s      │
              └──────┬──────┘
                     ↓
Phase 3: Sequential (Depends on Phase 2)
              ┌─────────────┐
              │ utils-tests │
              │   3.5s      │
              └─────────────┘

Total: ~6.0s (vs 11.0s serial) - 45% faster
```

### Expected Output

```
▶ Dependency Analysis
  Tasks: 5
  Parallel Groups: 3
  Dependencies Detected:
    - utils-index → [string-utils, date-utils, number-utils]
    - utils-tests → [utils-index]

▶ Phase 1: Executing 3 tasks in parallel
  ✓ string-utils 2.1s
  ✓ date-utils 2.3s
  ✓ number-utils 1.9s

▶ Phase 2: Executing 1 task
  ✓ utils-index 1.2s

▶ Phase 3: Executing 1 task
  ✓ utils-tests 3.5s

✓ All 5 tasks completed in 6.0s
```

---

## Model Selection for Level 2

| Task Complexity | Model | Execution |
|----------------|-------|-----------|
| Standard utilities | `gpt-5.1-codex-max` | Parallel with dependency analysis |
| Multi-task workflow | `gpt-5.1-codex-max` | Auto DAG construction |
| Complex validation | `gpt-5.1-codex-max` | Parallel when independent |

**L2 Execution Features:**
- Automatic dependency analysis between tasks
- Parallel execution of independent tasks
- DAG-based execution scheduling
- No task decomposition (single task = single output)

**When to upgrade to Level 3**:
- Need automatic task decomposition
- Require production-grade error handling
- Code integrates with external services
- Need comprehensive test coverage

---

## Tips for Level 2 Tasks

1. **Add type hints**: Use `typing` module for clarity
2. **Write docstrings**: Document parameters and return values
3. **Handle edge cases**: Null inputs, empty strings, boundary values
4. **Keep functions pure**: Avoid side effects when possible
5. **Test thoroughly**: Cover happy path + edge cases + errors

---

## Related Resources

- [references/complexity-guide.md](../references/complexity-guide.md) - Level 2 detailed guidance
- [examples/level1-simple-scripts.md](./level1-simple-scripts.md) - Simpler scripts
- [examples/level3-modules.md](./level3-modules.md) - Production-grade modules
- [skills/memex-cli/SKILL.md](../../memex-cli/SKILL.md) - Memex CLI usage

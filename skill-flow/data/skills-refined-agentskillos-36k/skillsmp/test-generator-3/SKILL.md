---
name: test-generator
description: Generates unit tests and integration tests for Python code using pytest conventions. Use when creating tests for new functions, classes, or modules.
---

# Test Generator Skill

自动为 Python 代码生成单元测试和集成测试。

## When to use this skill

- 为新编写的函数或类创建测试
- 为现有代码补充测试覆盖
- 生成边界条件和异常情况的测试用例
- 创建参数化测试

## Testing Framework

默认使用 **pytest** 框架，遵循以下约定：

- 测试文件: `test_<module>.py`
- 测试类: `Test<ClassName>`
- 测试函数: `test_<function_name>_<scenario>`

## Test Generation Steps

### 1. 分析目标代码
- 识别公共接口和方法
- 理解输入参数和返回值
- 找出边界条件和异常情况

### 2. 设计测试用例
- **正常路径**: 标准输入的预期输出
- **边界条件**: 极值、空值、边界情况
- **异常处理**: 无效输入、错误条件
- **集成场景**: 多个组件的交互

### 3. 编写测试代码

```python
import pytest
from module import function_to_test

class TestFunctionName:
    """Tests for function_name"""
    
    def test_normal_case(self):
        """Test with standard input"""
        result = function_to_test(valid_input)
        assert result == expected_output
    
    def test_edge_case(self):
        """Test boundary conditions"""
        result = function_to_test(edge_input)
        assert result == edge_expected
    
    def test_raises_on_invalid_input(self):
        """Test exception handling"""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
    
    @pytest.mark.parametrize("input,expected", [
        (case1_input, case1_expected),
        (case2_input, case2_expected),
    ])
    def test_multiple_cases(self, input, expected):
        """Parameterized test for multiple scenarios"""
        assert function_to_test(input) == expected
```

## Best Practices

1. **测试独立性** - 每个测试应该独立运行，不依赖其他测试的状态
2. **清晰的命名** - 测试名称应该描述测试场景和预期结果
3. **Arrange-Act-Assert** - 遵循 AAA 模式组织测试代码
4. **Mock 外部依赖** - 使用 `unittest.mock` 或 `pytest-mock` 隔离外部服务
5. **Fixtures** - 使用 pytest fixtures 共享测试数据和设置

## Output Structure

```
tests/
├── conftest.py          # 共享 fixtures
├── test_<module1>.py    # 模块1的测试
├── test_<module2>.py    # 模块2的测试
└── integration/
    └── test_integration.py  # 集成测试
```

## Running Tests

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_module.py

# 显示覆盖率
pytest --cov=src --cov-report=html

# 详细输出
pytest -v
```

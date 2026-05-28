---
name: doc-generator
description: Generates documentation and docstrings for Python code. Use when adding documentation to functions, classes, modules, or creating API documentation.
---

# Documentation Generator Skill

自动为 Python 代码生成文档和注释。

## When to use this skill

- 为函数和类添加 docstrings
- 生成模块级文档
- 创建 API 文档
- 编写 README 和使用指南

## Docstring Style

默认使用 **Google Style** docstrings：

### 函数文档

```python
def calculate_capacity(
    width: float,
    height: float,
    fc: float,
    fy: float
) -> float:
    """Calculate the capacity of a reinforced concrete section.
    
    Computes the nominal capacity based on section dimensions
    and material properties according to ACI 318 provisions.
    
    Args:
        width: Section width in millimeters.
        height: Section height in millimeters.
        fc: Concrete compressive strength in MPa.
        fy: Steel yield strength in MPa.
    
    Returns:
        The nominal capacity in kN.
    
    Raises:
        ValueError: If any dimension is non-positive.
        
    Example:
        >>> capacity = calculate_capacity(300, 500, 30, 400)
        >>> print(f"Capacity: {capacity:.2f} kN")
        Capacity: 1250.00 kN
    
    Note:
        This calculation assumes rectangular stress block.
    """
```

### 类文档

```python
class SectionAnalyzer:
    """Analyzes reinforced concrete sections for structural capacity.
    
    This class provides methods to calculate moment and axial capacity
    for rectangular reinforced concrete sections.
    
    Attributes:
        width: Section width in mm.
        height: Section height in mm.
        cover: Concrete cover in mm.
    
    Example:
        >>> analyzer = SectionAnalyzer(300, 500, 40)
        >>> mn = analyzer.calculate_moment_capacity()
    """
```

### 模块文档

```python
"""Structural analysis utilities for reinforced concrete design.

This module provides tools for analyzing reinforced concrete sections
including capacity calculations, P-M interaction curves, and design
checks according to ACI 318.

Modules:
    capacity_calculator: Section capacity calculations
    pm_curve: P-M interaction diagram generation
    design_checks: Code compliance verification

Example:
    >>> from structural import capacity_calculator
    >>> result = capacity_calculator.analyze_section(section)
"""
```

## Documentation Sections

根据需要包含以下部分：

| Section | 用途 |
|---------|------|
| Args | 函数参数说明 |
| Returns | 返回值说明 |
| Raises | 可能抛出的异常 |
| Example | 使用示例 |
| Note | 额外说明或注意事项 |
| Warning | 警告信息 |
| See Also | 相关函数或类的引用 |
| Todo | 待完成事项 |

## Best Practices

1. **简洁明了** - 第一行是简短的功能描述
2. **完整类型** - 包含参数和返回值的类型信息
3. **实际示例** - 提供可运行的代码示例
4. **保持更新** - 代码变更时同步更新文档

## README Template

```markdown
# Project Name

Brief description of the project.

## Installation

```bash
pip install package-name
```

## Quick Start

```python
from package import main_function
result = main_function(args)
```

## Features

- Feature 1
- Feature 2

## Documentation

Link to full documentation.

## License

MIT License
```

## API Documentation

使用 Sphinx 或 MkDocs 生成 API 文档：

```bash
# Sphinx
sphinx-apidoc -o docs/api src/

# MkDocs with mkdocstrings
mkdocs build
```

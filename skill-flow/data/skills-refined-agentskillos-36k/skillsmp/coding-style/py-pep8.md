---
name: Python PEP8 規範
description: Python 官方編碼規範
---

# Python PEP 8 規範

## 基本規則

- 縮排：4 空格
- 行寬：79 字元（註解 72）
- 空白行：類別和函式之間 2 行，方法之間 1 行
- 編碼：UTF-8

---

## 命名規範

| 類型 | 規範 | 範例 |
|-----|------|-----|
| 模組 | lowercase | `my_module.py` |
| 套件 | lowercase | `mypackage` |
| 類別 | PascalCase | `MyClass` |
| 函式 | snake_case | `my_function` |
| 變數 | snake_case | `my_variable` |
| 常數 | UPPER_SNAKE | `MAX_VALUE` |
| 私有 | _prefix | `_private_var` |

---

## 匯入

```python
# 標準庫
import os
import sys
from typing import List, Optional

# 第三方
import requests
from flask import Flask, request

# 本地
from myapp.models import User
from myapp.utils import helper

# 避免
from module import *  # ❌
```

---

## 函式

```python
def calculate_total(
    items: List[dict],
    tax_rate: float = 0.1,
    discount: Optional[float] = None,
) -> float:
    """
    計算總金額。

    Args:
        items: 商品列表
        tax_rate: 稅率
        discount: 折扣金額

    Returns:
        計算後的總金額
    """
    subtotal = sum(item['price'] for item in items)
    total = subtotal * (1 + tax_rate)
    
    if discount:
        total -= discount
    
    return total
```

---

## 類別

```python
class User:
    """使用者類別。"""

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self._created_at = datetime.now()

    @property
    def display_name(self) -> str:
        """取得顯示名稱。"""
        return self.name.title()

    def send_email(self, subject: str, body: str) -> bool:
        """發送郵件給使用者。"""
        # 實作...
        return True
```

---

## 型別提示

```python
from typing import List, Dict, Optional, Union, Callable

# 基本
name: str = "John"
age: int = 30

# 容器
items: List[str] = ["a", "b"]
mapping: Dict[str, int] = {"a": 1}

# 可選
user: Optional[User] = None

# 聯合
value: Union[str, int] = "hello"

# 函式
callback: Callable[[int, int], int] = lambda x, y: x + y
```

---

## 工具

```bash
# 檢查
pip install flake8
flake8 src/

# 格式化
pip install black
black src/

# 型別檢查
pip install mypy
mypy src/
```

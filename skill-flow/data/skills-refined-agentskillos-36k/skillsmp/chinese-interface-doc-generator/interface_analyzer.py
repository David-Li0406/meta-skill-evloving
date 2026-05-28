"""
接口分析器：分析代码中的函数、类、API接口定义。
"""

import ast
import re
from typing import List, Dict, Any, Optional

class InterfaceAnalyzer:
    def __init__(self, code: str, lang: str = 'python'):
        self.code = code
        self.lang = lang.lower()
        self.interfaces: List[Dict[str, Any]] = []

    def analyze(self) -> List[Dict[str, Any]]:
        """分析代码，返回接口列表。"""
        if self.lang == 'python':
            return self._analyze_python()
        elif self.lang in ['javascript', 'typescript']:
            return self._analyze_js()
        else:
            return []

    def _analyze_python(self) -> List[Dict[str, Any]]:
        """使用AST分析Python代码。"""
        try:
            tree = ast.parse(self.code)
            self._extract_from_ast(tree)
        except SyntaxError:
            pass  # 无效语法，返回空
        return self.interfaces

    def _extract_from_ast(self, node):
        """从AST节点提取接口。"""
        for n in ast.walk(node):
            if isinstance(n, ast.FunctionDef):
                self.interfaces.append({
                    'type': 'function',
                    'name': n.name,
                    'args': self._get_args(n.args),
                    'returns': self._get_returns(n),
                    'line': n.lineno
                })
            elif isinstance(n, ast.AsyncFunctionDef):
                self.interfaces.append({
                    'type': 'async_function',
                    'name': n.name,
                    'args': self._get_args(n.args),
                    'returns': self._get_returns(n),
                    'line': n.lineno
                })
            elif isinstance(n, ast.ClassDef):
                for stmt in n.body:
                    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.interfaces.append({
                            'type': f'class_method ({n.name})',
                            'name': stmt.name,
                            'class': n.name,
                            'args': self._get_args(stmt.args),
                            'returns': self._get_returns(stmt),
                            'line': stmt.lineno
                        })

    def _get_args(self, args_node) -> List[str]:
        return [arg.arg for arg in args_node.args]

    def _get_returns(self, node) -> Optional[str]:
        for n in ast.walk(node):
            if isinstance(n, ast.Return):
                if n.value:
                    return ast.unparse(n.value)
        return 'void'

    def _analyze_js(self) -> List[Dict[str, Any]]:
        """简单正则分析JS/TS。"""
        # 函数
        func_pattern = r'(?:function\s+|async\s+function\s+|const\s+\w+\s*=\s*)?(\w+)\s*\(([^)]*)\)'
        matches = re.findall(func_pattern, self.code, re.MULTILINE)
        for name, params in matches:
            self.interfaces.append({
                'type': 'function',
                'name': name,
                'args': [p.strip() for p in params.split(',') if p.strip()],
                'returns': 'unknown'
            })
        # 类方法
        class_pattern = r'class\s+(\w+).*?(\w+)\s*\(([^)]*)\)'
        matches = re.findall(class_pattern, self.code, re.DOTALL)
        for cls, name, params in matches:
            self.interfaces.append({
                'type': 'class_method',
                'name': name,
                'class': cls,
                'args': [p.strip() for p in params.split(',') if p.strip()],
                'returns': 'unknown'
            })
        return self.interfaces

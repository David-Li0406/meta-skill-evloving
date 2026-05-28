"""危险函数检测器

检测 Python 代码中的危险函数调用，如 eval、exec、compile、动态导入等。
"""

import ast
from typing import List, Dict, Any


class DangerousCall:
    """危险调用结果"""

    def __init__(self, name: str, severity: str, line: int, col: int, details: str):
        self.name = name  # 危险函数名
        self.severity = severity  # 严重/高/中/低
        self.line = line
        self.col = col
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            'detector': 'dangerous_calls',
            'name': self.name,
            'severity': self.severity,
            'line': self.line,
            'col': self.col,
            'details': self.details,
        }


class DangerousCallsDetector(ast.NodeVisitor):
    """检测危险函数调用"""

    # 危险函数及其严重程度
    DANGEROUS_FUNCTIONS = {
        # 代码执行 - 严重
        'eval': ('严重', '动态代码执行，可能导致任意代码执行漏洞'),
        'exec': ('严重', '动态代码执行，可能导致任意代码执行漏洞'),
        'compile': ('严重', '编译代码对象，可能与 exec/eval 配合使用'),

        # 动态导入 - 高
        '__import__': ('高', '动态导入模块，可能导入恶意代码'),

        # 命令执行 - 严重
        'os.system': ('严重', '执行系统命令，可能导致命令注入'),
        'subprocess.run': ('严重', '执行子进程命令，可能导致命令注入'),
        'subprocess.call': ('严重', '执行子进程命令，可能导致命令注入'),
        'subprocess.Popen': ('严重', '执行子进程命令，可能导致命令注入'),
        'subprocess.check_output': ('严重', '执行子进程命令，可能导致命令注入'),

        # 反序列化 - 严重
        'pickle.loads': ('严重', '反序列化数据，可能导致任意代码执行'),
        'pickle.load': ('严重', '反序列化数据，可能导致任意代码执行'),
        'marshal.loads': ('严重', '反序列化数据，可能导致任意代码执行'),
        'marshal.load': ('严重', '反序列化数据，可能导致任意代码执行'),

        # 全局变量访问 - 中
        'globals': ('中', '访问全局变量字典，可能被用于代码注入'),
        'locals': ('中', '访问局部变量字典，可能被用于代码注入'),
        'vars': ('低', '访问变量字典，需结合上下文判断'),
    }

    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path
        self.findings: List[DangerousCall] = []

    def detect(self) -> List[DangerousCall]:
        """执行检测"""
        try:
            tree = ast.parse(self.source_code, filename=self.file_path)
            self.visit(tree)
        except SyntaxError as e:
            # 语法错误，记录但继续
            self.findings.append(
                DangerousCall(
                    name='SyntaxError',
                    severity='低',
                    line=e.lineno or 0,
                    col=e.offset or 0,
                    details=f'语法错误: {e.msg}',
                )
            )
        return self.findings

    def visit_Call(self, node: ast.Call):
        """访问函数调用节点"""
        # 检查函数名
        func_name = self._get_function_name(node)

        if func_name in self.DANGEROUS_FUNCTIONS:
            severity, details = self.DANGEROUS_FUNCTIONS[func_name]
            self.findings.append(
                DangerousCall(
                    name=func_name,
                    severity=severity,
                    line=node.lineno,
                    col=node.col_offset,
                    details=details,
                )
            )

        # 继续遍历子节点
        self.generic_visit(node)

    def _get_function_name(self, node: ast.Call) -> str:
        """获取函数调用的完整名称"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            # 获取类似 os.system 的完整名称
            parts = []
            curr = node.func
            while isinstance(curr, ast.Attribute):
                parts.append(curr.attr)
                curr = curr.value
            if isinstance(curr, ast.Name):
                parts.append(curr.id)
            return '.'.join(reversed(parts))
        return ''

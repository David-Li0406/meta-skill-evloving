"""代码混淆检测器

检测 Python 代码中的混淆模式，如 Base64 编码、十六进制字符串等。
"""

import ast
import base64
import re
from typing import List, Dict, Any


class Obfuscation:
    """混淆检测结果"""

    def __init__(self, name: str, severity: str, line: int, col: int, details: str):
        self.name = name
        self.severity = severity
        self.line = line
        self.col = col
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            'detector': 'obfuscation',
            'name': self.name,
            'severity': self.severity,
            'line': self.line,
            'col': self.col,
            'details': self.details,
        }


class ObfuscationDetector(ast.NodeVisitor):
    """检测代码混淆"""

    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path
        self.findings: List[Obfuscation] = []

    def detect(self) -> List[Obfuscation]:
        """执行检测"""
        try:
            tree = ast.parse(self.source_code, filename=self.file_path)
            self.visit(tree)

            # 额外检查长行代码
            self._check_long_lines()
        except SyntaxError:
            pass
        return self.findings

    def visit_Call(self, node: ast.Call):
        """访问函数调用节点"""
        func_name = self._get_function_name(node)

        # 检查 Base64 编码/解码
        if func_name in ['base64.b64decode', 'base64.standard_b64decode']:
            self.findings.append(
                Obfuscation(
                    name='base64_decode',
                    severity='高',
                    line=node.lineno,
                    col=node.col_offset,
                    details='Base64 解码操作，可能用于解码混淆的代码或数据',
                )
            )

        # 检查字符代码转换
        elif func_name in ['chr', 'ord']:
            self._check_char_conversion(node, func_name)

        # 检查 compile 函数
        elif func_name == 'compile':
            self.findings.append(
                Obfuscation(
                    name='compile_call',
                    severity='高',
                    line=node.lineno,
                    col=node.col_offset,
                    details='动态编译代码，常与混淆技术结合使用',
                )
            )

        # 检查 bytes/bytearray 的十六进制构造
        elif func_name in ['bytes.fromhex', 'bytearray.fromhex']:
            self.findings.append(
                Obfuscation(
                    name='hex_bytes',
                    severity='高',
                    line=node.lineno,
                    col=node.col_offset,
                    details='十六进制字节构造，可能用于混淆数据',
                )
            )

        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr):
        """检查 f-string 是否用于代码构造"""
        # 检查 f-string 中是否有大量字符代码
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                if isinstance(value.value, ast.Call):
                    func_name = self._get_function_name(value.value)
                    if func_name == 'chr':
                        self.findings.append(
                            Obfuscation(
                                name='chr_fstring',
                                severity='高',
                                line=node.lineno,
                                col=node.col_offset,
                                details='f-string 中使用 chr() 构造字符串，典型混淆技术',
                            )
                        )
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        """检查列表推导式中的混淆模式"""
        # 检查 [chr(x) for x in [...] ] 模式
        if isinstance(node.elt, ast.Call):
            func_name = self._get_function_name(node.elt)
            if func_name == 'chr':
                self.findings.append(
                    Obfuscation(
                        name='chr_listcomp',
                        severity='高',
                        line=node.lineno,
                        col=node.col_offset,
                        details='列表推导式使用 chr() 构造字符串，典型混淆技术',
                    )
                )
        self.generic_visit(node)

    def _check_char_conversion(self, node: ast.Call, func_name: str):
        """检查字符转换模式"""
        # 检查 chr() 调用是否在特定上下文中
        if func_name == 'chr':
            # 检查是否有大量 chr() 调用
            chr_count = self._count_chr_in_scope(node)
            if chr_count > 3:
                self.findings.append(
                    Obfuscation(
                        name='multiple_chr',
                        severity='高',
                        line=node.lineno,
                        col=node.col_offset,
                        details=f'发现 {chr_count} 个 chr() 调用，可能用于混淆字符串',
                    )
                )

    def _count_chr_in_scope(self, node: ast.Call) -> int:
        """计算作用域内的 chr 调用数量"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == 'chr':
                    count += 1
        return count

    def _check_long_lines(self):
        """检查异常长的代码行"""
        lines = self.source_code.split('\n')
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            # 忽略注释
            if stripped.startswith('#'):
                continue
            # 检查超长行（超过 200 字符）
            if len(line) > 200:
                self.findings.append(
                    Obfuscation(
                        name='long_line',
                        severity='低',
                        line=i,
                        col=0,
                        details=f'超长代码行 ({len(line)} 字符)，可能包含混淆代码',
                    )
                )

    def _get_function_name(self, node: ast.Call) -> str:
        """获取函数调用的完整名称"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            curr = node.func
            while isinstance(curr, ast.Attribute):
                parts.append(curr.attr)
                curr = curr.value
            if isinstance(curr, ast.Name):
                parts.append(curr.id)
            return '.'.join(reversed(parts))
        return ''

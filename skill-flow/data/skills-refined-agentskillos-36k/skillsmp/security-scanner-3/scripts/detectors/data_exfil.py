"""数据外泄检测器

检测 Python 代码中潜在的数据外泄模式。
"""

import ast
import re
from typing import List, Dict, Any


class DataExfil:
    """数据外泄检测结果"""

    def __init__(self, name: str, severity: str, line: int, col: int, details: str):
        self.name = name
        self.severity = severity
        self.line = line
        self.col = col
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            'detector': 'data_exfil',
            'name': self.name,
            'severity': self.severity,
            'line': self.line,
            'col': self.col,
            'details': self.details,
        }


class DataExfilDetector(ast.NodeVisitor):
    """检测数据外泄模式"""

    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path
        self.findings: List[DataExfil] = []

    def detect(self) -> List[DataExfil]:
        """执行检测"""
        try:
            tree = ast.parse(self.source_code, filename=self.file_path)
            self.visit(tree)
        except SyntaxError:
            pass
        return self.findings

    def visit_Call(self, node: ast.Call):
        """访问函数调用节点"""
        func_name = self._get_function_name(node)

        # 检查 HTTP POST/PUT 请求（可能用于数据外泄）
        if func_name in ['requests.post', 'requests.put', 'requests.patch']:
            self._check_http_data_send(node, func_name)

        # 检查 socket send 操作
        elif func_name in ['socket.send', 'socket.sendall', 'socket.sendto']:
            self.findings.append(
                DataExfil(
                    name='socket_send',
                    severity='严重',
                    line=node.lineno,
                    col=node.col_offset,
                    details='Socket 数据发送，需确认目的地是否安全',
                )
            )

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """检查可疑的变量赋值"""
        # 检查是否有将敏感数据赋值给外部变量的模式
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                # 检查是否将敏感数据赋值给可能外泄的变量
                if var_name in ['webhook_url', 'exfil_url', 'c2_url', 'remote_url']:
                    self.findings.append(
                        DataExfil(
                            name='suspicious_var',
                            severity='高',
                            line=node.lineno,
                            col=node.col_offset,
                            details=f'可疑变量名: {target.id}，可能用于数据外泄',
                        )
                    )
        self.generic_visit(node)

    def _check_http_data_send(self, node: ast.Call, func_name: str):
        """检查 HTTP 数据发送"""
        # 检查是否有 data/json 参数
        has_data_payload = False
        suspicious_keywords = ['password', 'token', 'key', 'secret', 'credential']

        for keyword in node.keywords:
            if keyword.arg in ['data', 'json']:
                has_data_payload = True
                # 尝试检查发送的内容
                if isinstance(keyword.value, ast.Name):
                    var_name = keyword.value.id.lower()
                    if any(kw in var_name for kw in suspicious_keywords):
                        self.findings.append(
                            DataExfil(
                                name='http_exfil',
                                severity='严重',
                                line=node.lineno,
                                col=node.col_offset,
                                details=f'HTTP {func_name.split(".")[1].upper()} '
                                       f'发送可能包含敏感数据的变量: {keyword.value.id}',
                            )
                        )
                        return

        if has_data_payload:
            self.findings.append(
                DataExfil(
                    name='http_data_send',
                    severity='中',
                    line=node.lineno,
                    col=node.col_offset,
                    details=f'HTTP {func_name.split(".")[1].upper()} 请求携带数据，需确认目的地',
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

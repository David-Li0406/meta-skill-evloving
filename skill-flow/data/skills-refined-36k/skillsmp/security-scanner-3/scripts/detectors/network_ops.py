"""网络操作检测器

检测 Python 代码中的网络操作，包括 HTTP 请求、socket 操作等。
"""

import ast
import re
from typing import List, Dict, Any, Optional


class NetworkOp:
    """网络操作结果"""

    def __init__(self, name: str, severity: str, line: int, col: int, details: str):
        self.name = name
        self.severity = severity
        self.line = line
        self.col = col
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            'detector': 'network_ops',
            'name': self.name,
            'severity': self.severity,
            'line': self.line,
            'col': self.col,
            'details': self.details,
        }


class NetworkOpsDetector(ast.NodeVisitor):
    """检测网络操作"""

    # 常见网络库和方法
    NETWORK_FUNCTIONS = {
        # HTTP 库 - 中
        'requests.get': ('中', 'HTTP GET 请求'),
        'requests.post': ('中', 'HTTP POST 请求'),
        'requests.put': ('中', 'HTTP PUT 请求'),
        'requests.delete': ('中', 'HTTP DELETE 请求'),
        'requests.patch': ('中', 'HTTP PATCH 请求'),
        'requests.request': ('中', 'HTTP 请求'),
        'urllib.request.urlopen': ('中', 'URL 打开请求'),
        'urllib.request.Request': ('中', 'URL 请求构造'),
        'urllib.request.urlretrieve': ('中', 'URL 文件下载'),
        'httpx.get': ('中', 'HTTP GET 请求'),
        'httpx.post': ('中', 'HTTP POST 请求'),
        'httpx.request': ('中', 'HTTP 请求'),

        # Socket 操作 - 中
        'socket.socket': ('中', '创建 socket 连接'),
        'socket.connect': ('中', 'socket 连接'),

        # 低层网络 - 高
        'os.popen': ('高', '通过命令执行网络操作，可能被滥用'),
    }

    # 可疑 URL 模式（IP 地址、非标准端口等）
    SUSPICIOUS_URL_PATTERNS = [
        (r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '直接 IP 地址访问'),
        (r'https?://[^\s/:]+:\d{2,5}', '非标准端口访问'),
        (r'https?://.*\.onion', 'Tor 网络访问'),
    ]

    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path
        self.findings: List[NetworkOp] = []

    def detect(self) -> List[NetworkOp]:
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

        if func_name in self.NETWORK_FUNCTIONS:
            severity, details = self.NETWORK_FUNCTIONS[func_name]
            self.findings.append(
                NetworkOp(
                    name=func_name,
                    severity=severity,
                    line=node.lineno,
                    col=node.col_offset,
                    details=details,
                )
            )

        # 检查 URL 字符串
        if isinstance(node.func, ast.Attribute):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    url_finding = self._check_suspicious_url(arg.value, node.lineno)
                    if url_finding:
                        self.findings.append(url_finding)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """检查导入的网络库"""
        for alias in node.names:
            if alias.name in ['socket', 'http', 'ftplib', 'smtplib']:
                self.findings.append(
                    NetworkOp(
                        name=f'import {alias.name}',
                        severity='低',
                        line=node.lineno,
                        col=node.col_offset,
                        details=f'导入网络库 {alias.name}',
                    )
                )

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """检查 from 导入的网络库"""
        if node.module and node.module in ['socket', 'urllib', 'http', 'requests', 'httpx']:
            self.findings.append(
                NetworkOp(
                    name=f'from {node.module} import ...',
                    severity='低',
                    line=node.lineno,
                    col=node.col_offset,
                    details=f'从网络库 {node.module} 导入',
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

    def _check_suspicious_url(self, url: str, line: int) -> Optional[NetworkOp]:
        """检查可疑 URL"""
        for pattern, desc in self.SUSPICIOUS_URL_PATTERNS:
            if re.search(pattern, url):
                return NetworkOp(
                    name='suspicious_url',
                    severity='中',
                    line=line,
                    col=0,
                    details=f'{desc}: {url[:50]}...' if len(url) > 50 else f'{desc}: {url}',
                )
        return None

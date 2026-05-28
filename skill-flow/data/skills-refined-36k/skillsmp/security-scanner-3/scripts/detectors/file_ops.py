"""文件操作检测器

检测 Python 代码中对敏感文件的访问操作。
"""

import ast
import os
from typing import List, Dict, Any, Optional


class FileOp:
    """文件操作结果"""

    def __init__(self, name: str, severity: str, line: int, col: int, details: str):
        self.name = name
        self.severity = severity
        self.line = line
        self.col = col
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            'detector': 'file_ops',
            'name': self.name,
            'severity': self.severity,
            'line': self.line,
            'col': self.col,
            'details': self.details,
        }


class FileOpsDetector(ast.NodeVisitor):
    """检测文件操作"""

    # 敏感路径模式
    SENSITIVE_PATTERNS = [
        ('~/.ssh/', 'SSH 密钥目录', '严重'),
        ('.ssh', 'SSH 密钥目录', '严重'),
        ('~/.aws/', 'AWS 凭证目录', '严重'),
        ('.aws', 'AWS 凭证目录', '严重'),
        ('id_rsa', 'SSH 私钥文件', '严重'),
        ('id_ed25519', 'SSH 私钥文件', '严重'),
        ('known_hosts', 'SSH 已知主机文件', '高'),
        ('credentials', '凭证文件', '高'),
        ('.env', '环境变量文件', '中'),
        ('.secret', '密钥文件', '高'),
        ('.token', '令牌文件', '高'),
        ('.key', '密钥文件', '高'),
        ('password', '密码文件', '高'),
        ('~/.claude/', 'Claude Code 配置目录', '高'),
        ('~/.config/', '系统配置目录', '中'),
    ]

    def __init__(self, source_code: str, file_path: str):
        self.source_code = source_code
        self.file_path = file_path
        self.findings: List[FileOp] = []

    def detect(self) -> List[FileOp]:
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

        # 检查文件操作函数
        if func_name in ['open', 'Path.open']:
            self._check_file_access(node, func_name)

        # 检查环境变量读取
        elif func_name in ['os.getenv', 'os.environ.get', 'os.environ.__getitem__']:
            self._check_env_access(node)

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        """检查 os.environ['KEY'] 形式的环境变量访问"""
        if isinstance(node.value, ast.Attribute):
            if isinstance(node.value.value, ast.Name) and node.value.value.id == 'os':
                if node.value.attr == 'environ':
                    key = self._get_string_value(node.slice)
                    if key and self._is_sensitive_env_key(key):
                        self.findings.append(
                            FileOp(
                                name='env_access',
                                severity='高',
                                line=node.lineno,
                                col=node.col_offset,
                                details=f'读取敏感环境变量: {key}',
                            )
                        )
        self.generic_visit(node)

    def _check_file_access(self, node: ast.Call, func_name: str):
        """检查文件访问"""
        if node.args and isinstance(node.args[0], (ast.Constant, ast.Str)):
            path = self._get_string_value(node.args[0])
            if path:
                self._check_sensitive_path(path, node.lineno, node.col_offset)

    def _check_env_access(self, node: ast.Call):
        """检查环境变量访问"""
        if node.args and isinstance(node.args[0], (ast.Constant, ast.Str)):
            key = self._get_string_value(node.args[0])
            if key and self._is_sensitive_env_key(key):
                self.findings.append(
                    FileOp(
                        name='env_access',
                        severity='高',
                        line=node.lineno,
                        col=node.col_offset,
                        details=f'读取敏感环境变量: {key}',
                    )
                )

    def _check_sensitive_path(self, path: str, line: int, col: int):
        """检查是否为敏感路径"""
        expanded_path = os.path.expanduser(path.lower())
        for pattern, desc, severity in self.SENSITIVE_PATTERNS:
            if pattern.lower() in expanded_path:
                self.findings.append(
                    FileOp(
                        name='sensitive_file',
                        severity=severity,
                        line=line,
                        col=col,
                        details=f'访问敏感文件 ({desc}): {path}',
                    )
                )
                return

    def _is_sensitive_env_key(self, key: str) -> bool:
        """检查是否为敏感环境变量"""
        sensitive_keywords = [
            'key', 'secret', 'token', 'password', 'credential',
            'api', 'aws', 'ssh', 'private', 'auth',
        ]
        key_lower = key.lower()
        return any(kw in key_lower for kw in sensitive_keywords)

    def _get_string_value(self, node) -> Optional[str]:
        """获取字符串节点的值"""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.Str):
            return node.s
        return None

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

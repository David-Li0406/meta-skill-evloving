"""
中文文档提取器：提取中文注释和docstring。
"""

import re
from typing import Dict, Any, Optional, List

class ChineseDocExtractor:
    def __init__(self, code: str):
        self.code = code

    def extract_for_interface(self, interface: Dict[str, Any], line_start: int, line_end: int) -> Dict[str, Any]:
        """为特定接口提取文档。"""
        snippet = self._get_snippet(interface, line_start, line_end)
        docs = {
            'description': self._extract_docstring(snippet),
            'comments': self._extract_comments(snippet),
            'params': self._extract_params(snippet)
        }
        interface.update(docs)
        return interface

    def _get_snippet(self, interface: Dict[str, Any], line_start: int, line_end: int) -> str:
        """获取接口附近代码片段。"""
        lines = self.code.split('\n')
        snippet_lines = lines[max(0, line_start-5):line_end+2]
        return '\n'.join(snippet_lines)

    def _extract_docstring(self, snippet: str) -> str:
        """提取docstring中的中文。"""
        patterns = [
            r'["\']{3}(.*?)["\']{3}',  # 通用三引号
            r'\"\"\"(.*?)\"\"\"',      # 双三引号
            r"\'\'\'(.*?)\'\'\'"       # 单三引号
        ]
        for pat in patterns:
            match = re.search(pat, snippet, re.DOTALL)
            if match:
                doc = match.group(1).strip()
                chinese = re.findall(r'[\u4e00-\u9fff]+', doc)
                if chinese:
                    return ' '.join(chinese)
        return ''

    def _extract_comments(self, snippet: str) -> List[str]:
        """提取行注释中的中文。"""
        comments = re.findall(r'#(.*)', snippet)
        chinese_comments = []
        for comm in comments:
            chinese = re.findall(r'[\u4e00-\u9fff]+', comm)
            if chinese:
                chinese_comments.append(' '.join(chinese))
        return chinese_comments

    def _extract_params(self, snippet: str) -> Dict[str, str]:
        """从docstring提取参数说明。"""
        # 改进正则：匹配参数名后的描述，包括中文、标点、英文、数字
        param_pattern = r'[-*]\s*(\w+):\s*([^:\n]+?)(?=\s*\n|$|[-*]\s*\w+:|\s*[-*]|\s*返回|\s*示例)'
        matches = re.findall(param_pattern, snippet, re.DOTALL)
        params = {}
        for name, desc in matches:
            # 清理空格
            params[name] = desc.strip()
        return params

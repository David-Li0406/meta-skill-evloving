"""
文档格式化器：将接口数据格式化为Markdown/HTML/JSON。
"""

from typing import List, Dict, Any
from datetime import datetime

class DocFormatter:
    def __init__(self, interfaces: List[Dict[str, Any]]):
        self.interfaces = interfaces

    def format_markdown(self) -> str:
        """Markdown格式。"""
        md = f"# 接口文档\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        for iface in self.interfaces:
            md += self._format_interface_md(iface)
            md += '\n---\n\n'
        return md

    def _format_interface_md(self, iface: Dict[str, Any]) -> str:
        sig = f"{iface['type']}: {iface['name']}(" + ', '.join(iface.get('args', [])) + ")"
        if 'class' in iface:
            sig = f"{iface['class']}.{sig}"
        desc = iface.get('description', '无描述')
        params = iface.get('params', {})
        md = f"## {sig}\n\n**描述**: {desc}\n\n"
        if params:
            md += "**参数**:\n"
            for p, d in params.items():
                md += f"- `{p}`: {d.strip()}\n"
        md += f"\n**行号**: {iface.get('line', '未知')}\n"
        return md

    def format_html(self) -> str:
        """HTML格式。"""
        html = "<html><head><title>接口文档</title></head><body><h1>接口文档</h1>"
        for iface in self.interfaces:
            html += self._format_interface_html(iface)
        html += "</body></html>"
        return html

    def _format_interface_html(self, iface: Dict[str, Any]) -> str:
        # 简化HTML实现
        sig = f"{iface['name']}(" + ', '.join(iface.get('args', [])) + ")"
        desc = iface.get('description', '无描述')
        return f"<h2>{sig}</h2><p>{desc}</p>"

    def format_json(self) -> Dict[str, Any]:
        """JSON格式。"""
        return {
            'generated_at': datetime.now().isoformat(),
            'interfaces': self.interfaces
        }

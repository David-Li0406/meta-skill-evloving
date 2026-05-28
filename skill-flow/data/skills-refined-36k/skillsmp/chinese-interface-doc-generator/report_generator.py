"""
报告生成器：整合生成最终文档文件。
"""

import os
import sys
from typing import Dict, Any
from datetime import datetime
# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interface_analyzer import InterfaceAnalyzer
from chinese_doc_extractor import ChineseDocExtractor
from doc_formatter import DocFormatter

class ReportGenerator:
    def __init__(self, input_data: Dict[str, Any]):
        self.input_data = input_data
        self.output_dir = os.path.expanduser('~/.claude/interface_docs')
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self) -> Dict[str, Any]:
        """完整生成流程。"""
        code = self.input_data.get('code', '')
        lang = self.input_data.get('lang', 'python')
        detail_level = self.input_data.get('detail_level', '详细')
        output_format = self.input_data.get('output_format', 'markdown')

        # 1. 分析接口
        analyzer = InterfaceAnalyzer(code, lang)
        interfaces = analyzer.analyze()

        # 2. 提取文档
        extractor = ChineseDocExtractor(code)
        for i, iface in enumerate(interfaces):
            line = iface.get('line', 1)
            interfaces[i] = extractor.extract_for_interface(iface, line-1, line+10)

        # 3. 格式化
        formatter = DocFormatter(interfaces)
        if output_format == 'markdown':
            content = formatter.format_markdown()
        elif output_format == 'html':
            content = formatter.format_html()
        elif output_format == 'json':
            content = formatter.format_json()
        else:
            content = formatter.format_markdown()

        # 4. 保存文件
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # 映射输出格式到文件扩展名
        format_extensions = {
            'markdown': 'md',
            'html': 'html',
            'json': 'json'
        }
        ext = format_extensions.get(output_format, 'md')
        filename = f"接口文档_{timestamp}.{ext}"
        filepath = os.path.join(self.output_dir, filename)
        if output_format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                import json
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        return {
            'status': 'success',
            'interfaces_count': len(interfaces),
            'output_file': filepath,
            'preview': content[:500] + '...' if len(str(content)) > 500 else content
        }

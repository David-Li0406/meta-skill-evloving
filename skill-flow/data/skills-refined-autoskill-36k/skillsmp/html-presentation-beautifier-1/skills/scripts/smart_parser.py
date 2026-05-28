#!/usr/bin/env python3
"""
智能文档解析器 - 专门提取有意义的数据用于图表可视化
"""

import json
import re
from typing import List, Dict, Any


class SmartDocumentParser:
    """智能解析器，提取有意义的数据点"""

    def __init__(self):
        self.data_points = []

    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析文档并提取结构化数据"""

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取标题
        title = self._extract_title(content)

        # 解析章节
        sections = self._parse_sections(content)

        # 提取有意义的数据点
        data_points = self._extract_meaningful_data(content)

        # 提取结论和建议
        conclusions = self._extract_conclusions(sections)

        return {
            'title': title,
            'doc_type': 'markdown',
            'sections': sections,
            'data_points': data_points,
            'conclusions': conclusions
        }

    def _extract_title(self, content: str) -> str:
        """提取文档标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else '未命名文档'

    def _parse_sections(self, content: str) -> List[Dict]:
        """解析文档章节"""
        sections = []
        lines = content.split('\n')
        current_section = None

        for line in lines:
            if line.strip().startswith('##'):
                level = len(line.split()[0])
                section_title = line.strip().replace('#', '').strip()

                if level == 2:
                    if current_section:
                        sections.append(current_section)

                    current_section = {
                        'title': section_title,
                        'content': '',
                        'level': level
                    }
            elif current_section:
                current_section['content'] += line + '\n'

        if current_section:
            sections.append(current_section)

        return sections

    def _extract_meaningful_data(self, content: str) -> List[Dict]:
        """提取有意义的数据点"""
        data_points = []

        # 定义数据模式及其含义
        patterns = [
            # 百分比数据
            (r'(\d+\.?\d*)%\s*([^\n，。；：]+)', 'percent'),
            # 金额数据（亿元/万元）
            (r'(\d+\.?\d*)\s*(亿元|万元)', 'money'),
            # 利润率数据
            (r'毛利率[：:]\s*(\d+\.?\d*)%', 'margin'),
            (r'净利率[：:]\s*(\d+\.?\d*)%', 'margin'),
            # 增长率
            (r'增长\s*(\d+\.?\d*)%', 'growth'),
            # 年龄范围
            (r'(\d+)-(\d+)\s*岁', 'age_range'),
            # 市场份额
            (r'市场份额[：:]\s*(\d+\.?\d*)%', 'share'),
        ]

        for pattern, data_type in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                try:
                    if data_type == 'percent':
                        value = float(match.group(1))
                        context = match.group(2).strip()
                        if 1900 <= value <= 2100:  # 过滤年份
                            continue
                        label = self._create_label(context, 'percentage')
                        data_points.append({
                            'label': label,
                            'value': value,
                            'unit': '%',
                            'category': data_type
                        })

                    elif data_type == 'money':
                        value = float(match.group(1))
                        unit = match.group(2)
                        if 1900 <= value <= 2100:  # 过滤年份
                            continue
                        label = self._create_label(f'金额指标', unit)
                        data_points.append({
                            'label': label,
                            'value': value,
                            'unit': unit,
                            'category': data_type
                        })

                    elif data_type == 'margin':
                        value = float(match.group(1))
                        margin_type = '毛利率' if '毛利率' in match.group(0) else '净利率'
                        data_points.append({
                            'label': margin_type,
                            'value': value,
                            'unit': '%',
                            'category': data_type
                        })

                    elif data_type == 'growth':
                        value = float(match.group(1))
                        data_points.append({
                            'label': '增长率',
                            'value': value,
                            'unit': '%',
                            'category': data_type
                        })

                    elif data_type == 'age_range':
                        age_min = int(match.group(1))
                        age_max = int(match.group(2))
                        data_points.append({
                            'label': '目标年龄范围',
                            'value': f"{age_min}-{age_max}",
                            'unit': '岁',
                            'category': data_type
                        })

                    elif data_type == 'share':
                        value = float(match.group(1))
                        data_points.append({
                            'label': '市场份额',
                            'value': value,
                            'unit': '%',
                            'category': data_type
                        })

                except (ValueError, IndexError):
                    continue

        # 去重并限制数量
        unique_data = []
        seen = set()
        for dp in data_points[:30]:
            key = (dp['label'], dp['value'])
            if key not in seen:
                seen.add(key)
                unique_data.append(dp)

        return unique_data

    def _create_label(self, context: str, data_type: str) -> str:
        """创建有意义的数据标签"""
        # 根据上下文创建标签
        if '转化率' in context:
            return '用户转化率'
        elif '复购率' in context:
            return '用户复购率'
        elif '市场' in context:
            return '市场渗透率'
        elif data_type == 'percentage':
            return '百分比指标'
        else:
            return context[:20] if context else '数据指标'

    def _extract_conclusions(self, sections: List[Dict]) -> List[Dict]:
        """提取结论和建议"""
        conclusions = []
        keywords = ['建议', '洞察', '定位', '策略', '优势', '目标', '预期']

        for section in sections:
            if any(keyword in section['title'] for keyword in keywords):
                lines = section['content'].split('\n')
                for line in lines:
                    if line.strip().startswith(('-', '*', '•')):
                        text = line.strip().lstrip('-*•').strip()
                        if text and len(text) > 15:
                            conclusions.append({
                                'text': text,
                                'category': section['title']
                            })

        return conclusions[:20]


def main():
    parser = SmartDocumentParser()

    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
            print("Usage: python smart_parser.py <markdown_file>")
            sys.exit(1)

        result = parser.parse(sys.argv[1])

        output_file = sys.argv[2] if len(sys.argv) > 2 else 'parsed_smart.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ 智能解析完成！")
        print(f"标题: {result['title']}")
        print(f"章节数: {len(result['sections'])}")
        print(f"数据点数: {len(result['data_points'])}")
        print(f"结论数: {len(result['conclusions'])}")
        print(f"\n📊 数据点示例:")
        for i, dp in enumerate(result['data_points'][:8], 1):
            print(f"  {i}. {dp['label']}: {dp['value']} {dp['unit']}")
        print(f"\n已保存到: {output_file}")


if __name__ == "__main__":
    main()

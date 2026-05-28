#!/usr/bin/env python3
"""
智能文档解析器 V2 - 改进版
- 更智能的数据提取
- 更准确的标签生成
- 更好的章节分类
"""

import json
import re
from typing import List, Dict, Any


class SmartDocumentParserV2:
    """智能文档解析器 V2 - 改进版"""

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

        # 提取有意义的数据点（改进版）
        data_points = self._extract_meaningful_data_v2(content, sections)

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

    def _extract_meaningful_data_v2(self, content: str, sections: List[Dict]) -> List[Dict]:
        """改进的数据提取 - V2"""
        data_points = []

        # 定义智能数据提取模式
        extraction_patterns = [
            # 转化率数据
            {
                'pattern': r'(用户转化率|转化率)[：:\s]*(\d+\.?\d*)\s*[-~到]\s*(\d+\.?\d*)\s*%',
                'label': '用户转化率',
                'unit': '%',
                'value_index': 0,
                'is_range': True
            },
            # 复购率数据
            {
                'pattern': r'(复购率)[：:\s]*超过?\s*(\d+\.?\d*)\s*%',
                'label': '目标复购率',
                'unit': '%',
                'value_index': 1,
                'is_range': False
            },
            # 市场份额
            {
                'pattern': r'(市场份额)[：:\s]*达到\s*(\d+\.?\d*)\s*%',
                'label': '目标市场份额',
                'unit': '%',
                'value_index': 1,
                'is_range': False
            },
            # 毛利率
            {
                'pattern': r'(毛利率)[：:\s]*(\d+\.?\d*)\s*%',
                'label': '毛利率',
                'unit': '%',
                'value_index': 1,
                'is_range': False
            },
            # 净利率
            {
                'pattern': r'(净利率)[：:\s]*(\d+\.?\d*)\s*%',
                'label': '净利率',
                'unit': '%',
                'value_index': 1,
                'is_range': False
            },
            # 增长率
            {
                'pattern': r'(增长|增长率)[：:\s*\(]*(\d+\.?\d*)\s*%',
                'label': '年增长率',
                'unit': '%',
                'value_index': 1,
                'is_range': False
            },
            # 收入数据（年份 + 金额）
            {
                'pattern': r'\*\*(\d{4})\s*年\*\*[：:\s]*([0-9]+\.?\d*)\s*(亿元|万元)',
                'label': None,  # 动态生成
                'unit': '亿元',
                'value_index': 1,
                'is_range': False,
                'year_index': 0
            },
            # 市场潜力
            {
                'pattern': r'(总市场潜力|市场规模)[：:\s]*([0-9]+\.?\d*)\s*(亿元|万元)',
                'label': '总市场潜力',
                'unit': '亿元',
                'value_index': 1,
                'is_range': False
            },
            # 客户终身价值
            {
                'pattern': r'(客户终身价值|LTV)[：:\s]*([0-9]+\.?\d*)\s*(元|万元)',
                'label': '客户终身价值',
                'unit': '元',
                'value_index': 1,
                'is_range': False
            },
            # 目标用户数
            {
                'pattern': r'(目标用户|用户基数)[：:\s]*([0-9]+\.?\d*)\s*(万|千)',
                'label': '目标用户数',
                'unit': '万',
                'value_index': 1,
                'is_range': False
            }
        ]

        for pattern_info in extraction_patterns:
            matches = re.finditer(pattern_info['pattern'], content)
            for match in matches:
                try:
                    # 提取数据
                    groups = match.groups()
                    
                    if pattern_info.get('is_range'):
                        # 范围值（如 5-8%）
                        value1 = float(groups[pattern_info['value_index']])
                        value2 = float(groups[pattern_info['value_index'] + 1])
                        value = (value1 + value2) / 2  # 取平均值
                        label = pattern_info['label']
                    else:
                        value = float(groups[pattern_info['value_index']])
                        
                        if pattern_info.get('year_index') is not None:
                            # 收入数据，标签包含年份
                            year = groups[pattern_info['year_index']]
                            label = f"{year}年收入"
                        else:
                            label = pattern_info['label']
                    
                    unit = pattern_info['unit']
                    
                    # 过滤年份数据
                    if 1900 <= value <= 2100 and unit != '亿元':
                        continue
                    
                    # 确定所属章节
                    category = self._determine_category(content, match.start(), sections)
                    
                    data_points.append({
                        'label': label,
                        'value': value,
                        'unit': unit,
                        'category': category
                    })
                    
                except (ValueError, IndexError) as e:
                    continue

        # 去重
        unique_data = []
        seen = set()
        for dp in data_points:
            key = (dp['label'], dp['value'], dp['unit'])
            if key not in seen:
                seen.add(key)
                unique_data.append(dp)

        return unique_data[:25]  # 限制数量

    def _determine_category(self, content: str, position: int, sections: List[Dict]) -> str:
        """根据位置确定数据所属的章节"""
        # 找到最接近该位置的章节
        best_section = sections[0]['title'] if sections else '其他'
        min_distance = float('inf')
        
        for section in sections:
            # 在内容中查找章节标题的位置
            section_pos = content.find(section['title'])
            if section_pos != -1 and abs(position - section_pos) < min_distance:
                min_distance = abs(position - section_pos)
                best_section = section['title']
        
        return best_section

    def _extract_conclusions(self, sections: List[Dict]) -> List[Dict]:
        """提取结论和建议"""
        conclusions = []
        keywords = ['建议', '洞察', '定位', '策略', '优势', '目标']

        for section in sections:
            if any(keyword in section['title'] for keyword in keywords):
                lines = section['content'].split('\n')
                for line in lines:
                    if line.strip().startswith(('-', '*', '•')):
                        text = line.strip().lstrip('-*•').strip()
                        if text and len(text) > 10:
                            conclusions.append({
                                'text': text,
                                'category': section['title']
                            })

        return conclusions[:20]


def main():
    parser = SmartDocumentParserV2()

    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
            print("Usage: python smart_parser_v2.py <markdown_file> [output_json]")
            sys.exit(1)

        result = parser.parse(sys.argv[1])

        output_file = sys.argv[2] if len(sys.argv) > 2 else 'parsed_smart_v2.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ 智能解析器 V2 完成！")
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

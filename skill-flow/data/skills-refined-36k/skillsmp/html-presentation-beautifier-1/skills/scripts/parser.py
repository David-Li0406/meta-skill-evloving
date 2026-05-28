#!/usr/bin/env python3
"""
Document Parser - Extract and structure content from source documents.

Supports Markdown, plain text, and structured JSON formats.
Preserves all original content without modification.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class DocType(Enum):
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"


@dataclass
class ContentSection:
    title: str
    content: str
    level: int = 1
    subsections: List['ContentSection'] = field(default_factory=list)


@dataclass
class DataPoint:
    label: str
    value: Any
    unit: Optional[str] = None
    category: Optional[str] = None


@dataclass
class Conclusion:
    text: str
    category: Optional[str] = None
    priority: Optional[str] = None


@dataclass
class ParsedDocument:
    title: str
    doc_type: DocType
    sections: List[ContentSection]
    data_points: List[DataPoint]
    conclusions: List[Conclusion]
    raw_content: str


class DocumentParser:
    def __init__(self):
        self.content_preserved = True

    def parse(self, file_path: str) -> ParsedDocument:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        doc_type = self._detect_doc_type(file_path, content)

        if doc_type == DocType.MARKDOWN:
            return self._parse_markdown(content, doc_type)
        elif doc_type == DocType.JSON:
            return self._parse_json(content, doc_type)
        else:
            return self._parse_text(content, doc_type)

    def _detect_doc_type(self, file_path: str, content: str) -> DocType:
        if file_path.endswith('.md') or content.startswith('#'):
            return DocType.MARKDOWN
        elif file_path.endswith('.json') or content.strip().startswith('{'):
            return DocType.JSON
        else:
            return DocType.TEXT

    def _parse_markdown(self, content: str, doc_type: DocType) -> ParsedDocument:
        lines = content.split('\n')
        sections = []
        current_section = None
        level_stack = {}

        for i, line in enumerate(lines):
            if line.strip() == '':
                continue

            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2)

                section = ContentSection(
                    title=title,
                    content='',
                    level=level,
                    subsections=[]
                )

                if level == 1:
                    if current_section:
                        sections.append(current_section)
                    current_section = section
                    level_stack[level] = section
                else:
                    parent = level_stack.get(level - 1)
                    if parent:
                        parent.subsections.append(section)
                    level_stack[level] = section
            elif current_section:
                current_section.content += line + '\n'

        if current_section:
            sections.append(current_section)

        title = sections[0].title if sections else 'Untitled'
        data_points = self._extract_data_points(sections)
        conclusions = self._extract_conclusions(sections)

        return ParsedDocument(
            title=title,
            doc_type=doc_type,
            sections=sections,
            data_points=data_points,
            conclusions=conclusions,
            raw_content=content
        )

    def _parse_json(self, content: str, doc_type: DocType) -> ParsedDocument:
        import json

        data = json.loads(content)
        title = data.get('title', 'Untitled')

        sections = []
        if 'sections' in data:
            for section_data in data['sections']:
                section = ContentSection(
                    title=section_data.get('title', ''),
                    content=section_data.get('content', ''),
                    level=section_data.get('level', 1),
                    subsections=[]
                )
                sections.append(section)

        data_points = []
        if 'data_points' in data:
            for dp in data['data_points']:
                data_points.append(DataPoint(
                    label=dp.get('label', ''),
                    value=dp.get('value'),
                    unit=dp.get('unit'),
                    category=dp.get('category')
                ))

        conclusions = []
        if 'conclusions' in data:
            for conc in data['conclusions']:
                conclusions.append(Conclusion(
                    text=conc.get('text', ''),
                    category=conc.get('category'),
                    priority=conc.get('priority')
                ))

        return ParsedDocument(
            title=title,
            doc_type=doc_type,
            sections=sections,
            data_points=data_points,
            conclusions=conclusions,
            raw_content=content
        )

    def _parse_text(self, content: str, doc_type: DocType) -> ParsedDocument:
        lines = content.split('\n')
        sections = []
        current_section = ContentSection(
            title='Content',
            content='',
            level=1,
            subsections=[]
        )

        for line in lines:
            if line.strip():
                if line.strip().endswith(':'):
                    if current_section.content:
                        sections.append(current_section)
                    current_section = ContentSection(
                        title=line.strip().rstrip(':'),
                        content='',
                        level=1,
                        subsections=[]
                    )
                else:
                    current_section.content += line + '\n'

        if current_section.content:
            sections.append(current_section)

        title = sections[0].title if sections else 'Untitled'
        data_points = self._extract_data_points_from_text(sections)
        conclusions = self._extract_conclusions_from_text(sections)

        return ParsedDocument(
            title=title,
            doc_type=doc_type,
            sections=sections,
            data_points=data_points,
            conclusions=conclusions,
            raw_content=content
        )

    def _extract_data_points(self, sections: List[ContentSection]) -> List[DataPoint]:
        data_points = []
        for section in sections:
            data_points.extend(self._extract_data_points_from_section(section))
        return data_points

    def _extract_data_points_from_section(self, section: ContentSection) -> List[DataPoint]:
        data_points = []

        pattern = r'(\d+\.?\d*)\s*(%|\$|k|m|b)?\b'
        matches = re.findall(pattern, section.content)

        for i, match in enumerate(matches):
            value_str, unit = match
            try:
                value = float(value_str)
                label = f"Data Point {i+1}"
                data_points.append(DataPoint(
                    label=label,
                    value=value,
                    unit=unit if unit else None,
                    category=section.title
                ))
            except ValueError:
                continue

        for subsection in section.subsections:
            data_points.extend(self._extract_data_points_from_section(subsection))

        return data_points

    def _extract_data_points_from_text(self, sections: List[ContentSection]) -> List[DataPoint]:
        return self._extract_data_points(sections)

    def _extract_conclusions(self, sections: List[ContentSection]) -> List[Conclusion]:
        conclusions = []

        conclusion_keywords = ['conclusion', 'finding', 'result', 'summary', 'recommendation']
        for section in sections:
            title_lower = section.title.lower()
            if any(keyword in title_lower for keyword in conclusion_keywords):
                lines = section.content.strip().split('\n')
                for line in lines:
                    if line.strip() and not line.strip().startswith('#'):
                        conclusions.append(Conclusion(
                            text=line.strip(),
                            category=section.title
                        ))

        return conclusions

    def _extract_conclusions_from_text(self, sections: List[ContentSection]) -> List[Conclusion]:
        return self._extract_conclusions(sections)


def main():
    parser = DocumentParser()

    if __name__ == "__main__":
        import sys
        if len(sys.argv) < 2:
            print("Usage: python parser.py <document_path>")
            sys.exit(1)

        doc = parser.parse(sys.argv[1])
        print(f"Document: {doc.title}")
        print(f"Type: {doc.doc_type}")
        print(f"Sections: {len(doc.sections)}")
        print(f"Data Points: {len(doc.data_points)}")
        print(f"Conclusions: {len(doc.conclusions)}")


if __name__ == "__main__":
    main()

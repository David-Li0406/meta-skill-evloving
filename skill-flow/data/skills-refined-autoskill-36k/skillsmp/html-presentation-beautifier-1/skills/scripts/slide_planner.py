#!/usr/bin/env python3
"""
Slide Planner - Analyze ParsedDocument and plan slide specifications.

This module transforms a parsed document into a list of SlideSpec objects,
deciding what content goes on each slide and what type of visualization to use.
"""

import re
from typing import List, Optional, Dict, Any

from parser import ParsedDocument, ContentSection, DataPoint, Conclusion
from data_structures import SlideSpec, SlideType, SlidePlan


class SlidePlanner:
    """Plan slides from a parsed document."""

    def __init__(self):
        self.max_executive_summary_items = 5
        self.max_data_slides = 8
        self.max_conclusions_per_slide = 6

    def plan_slides(self, doc: ParsedDocument) -> SlidePlan:
        """Main planning method - convert document to slide plan.

        Args:
            doc: ParsedDocument from the DocumentParser

        Returns:
            SlidePlan containing list of SlideSpec objects
        """
        plan = SlidePlan(title=doc.title)

        # 1. Title slide (always first)
        plan.add_slide(self._plan_title_slide(doc))

        # 2. Executive summary (if we have conclusions)
        if doc.conclusions:
            plan.add_slide(self._plan_executive_summary(doc))

        # 3. Data visualization slides (one per section with data)
        for slide_spec in self._plan_data_slides(doc):
            plan.add_slide(slide_spec)

        # 4. Content slides (for sections without data but with substantial content)
        for slide_spec in self._plan_content_slides(doc):
            plan.add_slide(slide_spec)

        # 5. Conclusions and recommendations slide
        if doc.conclusions:
            plan.add_slide(self._plan_conclusions_slide(doc))

        return plan

    def _plan_title_slide(self, doc: ParsedDocument) -> SlideSpec:
        """Plan the title slide."""
        return SlideSpec(
            slide_type=SlideType.TITLE,
            title=doc.title,
            content=f"{doc.title} - Data Analysis & Insights",
            layout="title-center"
        )

    def _plan_executive_summary(self, doc: ParsedDocument) -> SlideSpec:
        """Plan the executive summary slide with top conclusions."""
        top_conclusions = doc.conclusions[:self.max_executive_summary_items]
        key_points = [c.text for c in top_conclusions]

        return SlideSpec(
            slide_type=SlideType.EXECUTIVE_SUMMARY,
            title="Executive Summary",
            content="Key findings and insights",
            key_points=key_points,
            layout="bullet-points"
        )

    def _plan_data_slides(self, doc: ParsedDocument) -> List[SlideSpec]:
        """Plan data visualization slides."""
        slides = []

        # Group data points by section/category
        section_data_map: Dict[str, List[DataPoint]] = {}
        for dp in doc.data_points:
            category = dp.category or "Uncategorized"
            if category not in section_data_map:
                section_data_map[category] = []
            section_data_map[category].append(dp)

        # Create slide for each section with data
        for section in doc.sections:
            # Skip certain sections
            if section.title in ['关键洞察', '结论', 'Conclusion', 'Conclusions']:
                continue

            # Get data points for this section
            section_data = section_data_map.get(section.title, [])

            # Check if section has data or is conceptual
            has_data = len(section_data) > 0
            conceptual_type = self._detect_conceptual_type(section, section_data)

            # Skip if no data and not conceptual
            if not has_data and not conceptual_type:
                continue

            # Extract insights from section content
            insights = self._extract_insights(section)

            if has_data:
                # Determine chart type
                chart_type = self._determine_chart_type(section_data)

                # Convert DataPoint objects to dicts for compatibility
                data_points_dicts = [self._data_point_to_dict(dp) for dp in section_data]

                slides.append(SlideSpec(
                    slide_type=SlideType.DATA_VISUALIZATION,
                    title=section.title,
                    content=section.content.strip() or f"Analysis of {section.title}",
                    chart_type=chart_type,
                    data_points=data_points_dicts,
                    key_points=insights[:3],
                    layout="two-column",
                    source_section=section.title
                ))

            elif conceptual_type:
                slides.append(SlideSpec(
                    slide_type=SlideType.CONCEPTUAL,
                    title=section.title,
                    content=section.content.strip() or f"Conceptual framework for {section.title}",
                    conceptual_type=conceptual_type,
                    key_points=insights[:5],
                    layout="full-width",
                    source_section=section.title
                ))

            # Stop if we've reached max data slides
            if len(slides) >= self.max_data_slides:
                break

        return slides

    def _plan_content_slides(self, doc: ParsedDocument) -> List[SlideSpec]:
        """Plan content slides for sections without data."""
        slides = []

        # Skip first few sections as they're handled elsewhere
        for section in doc.sections[3:]:
            if not section.content.strip():
                continue

            # Skip if section was already handled in data slides
            # (sections with data or conceptual visualizations)
            section_data = [dp for dp in doc.data_points if dp.category == section.title]
            conceptual_type = self._detect_conceptual_type(section, section_data)
            if section_data or conceptual_type:
                continue

            slides.append(SlideSpec(
                slide_type=SlideType.CONTENT,
                title=section.title,
                content=section.content.strip(),
                layout="full-width",
                source_section=section.title
            ))

        return slides

    def _plan_conclusions_slide(self, doc: ParsedDocument) -> SlideSpec:
        """Plan the conclusions and recommendations slide."""
        key_points = [c.text for c in doc.conclusions[:self.max_conclusions_per_slide]]

        return SlideSpec(
            slide_type=SlideType.CONCLUSIONS,
            title="Conclusions & Recommendations",
            content="Summary of key findings and actionable recommendations",
            key_points=key_points,
            layout="conclusions-grid"
        )

    # ===== Helper Methods =====

    def _data_point_to_dict(self, dp: DataPoint) -> Dict[str, Any]:
        """Convert DataPoint object to dictionary."""
        return {
            'label': dp.label,
            'value': dp.value,
            'unit': dp.unit,
            'category': dp.category
        }

    def _extract_insights(self, section: ContentSection) -> List[str]:
        """Extract key insights from section content."""
        content = section.content
        lines = content.split('\n')

        # Filter out empty lines and very short lines
        insights = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]

        return insights[:5] if insights else [f"Key insights from {section.title}"]

    def _detect_conceptual_type(self, section: ContentSection, data_points: List[DataPoint]) -> Optional[str]:
        """
        Detect if section content is conceptual (non-numerical) and determine visualization type.

        Returns:
            'pyramid', 'progression', 'emphasis', 'cycle', 'comparison', 'framework', or None
        """
        title = section.title.lower()
        content = section.content.lower()

        # Combine all text if no data points
        if not data_points:
            all_text = f"{title} {content}"
        else:
            all_text = title

        # ===== Hierarchy =====
        hierarchy_keywords = ['层级', 'hierarchy', 'level', 'tier', '金字塔', 'pyramid',
                             'structure', '架构', '组织', 'organization']
        if any(kw in all_text for kw in hierarchy_keywords):
            return 'pyramid'

        # ===== Progression =====
        progression_keywords = ['递进', 'progression', '步骤', 'step', 'phase', '阶段',
                               '流程', 'process', 'journey', '路径', 'roadmap', 'timeline']
        if any(kw in all_text for kw in progression_keywords):
            return 'progression'

        # ===== Emphasis =====
        emphasis_keywords = ['强调', 'emphasis', '关键', 'key', '重点', 'important',
                            '核心', 'core', 'highlight', '亮点', 'takeaway']
        if any(kw in all_text for kw in emphasis_keywords):
            return 'emphasis'

        # ===== Cycle =====
        cycle_keywords = ['循环', 'cycle', '闭环', 'loop', '迭代', 'iteration',
                         '持续', 'continuous', '反馈', 'feedback']
        if any(kw in all_text for kw in cycle_keywords):
            return 'cycle'

        # ===== Comparison =====
        comparison_keywords = ['对比', 'comparison', '比较', 'versus', 'vs',
                              'before', 'after', '前后', '优劣', 'pros', 'cons']
        if any(kw in all_text for kw in comparison_keywords):
            return 'comparison'

        # ===== Framework =====
        framework_keywords = ['框架', 'framework', '模型', 'model', '法则', 'principle',
                             '5w1h', 'star', '黄金圈', 'golden circle']
        if any(kw in all_text for kw in framework_keywords):
            return 'framework'

        return None

    def _determine_chart_type(self, data_points: List[DataPoint]) -> str:
        """
        Smart chart type selection based on content analysis.

        Returns:
            Chart type string compatible with Chart.js
        """
        if not data_points:
            return 'bar'

        # Extract features for analysis
        labels = [dp.label.lower() for dp in data_points]
        units = [dp.unit or '' for dp in data_points]
        all_text = ' '.join(labels)

        # ===== Rankings =====
        ranking_keywords = ['排名', 'rank', 'level', 'tier', 'priority', '等级',
                           '优先级', 'top', 'best', 'market share']
        if any(kw in all_text for kw in ranking_keywords):
            if len(data_points) <= 8:
                return 'polarArea'
            return 'bar'

        # ===== Flow =====
        flow_keywords = ['转化', '漏斗', 'flow', 'journey', 'process', 'stage',
                        '阶段', '流程', 'step', '用户路径', '流失', 'customer']
        if any(kw in all_text for kw in flow_keywords):
            if 'funnel' in all_text or '漏斗' in all_text:
                return 'bar'
            return 'line'

        # ===== Distribution =====
        distribution_keywords = ['分布', 'distribution', 'spread', 'range',
                                'variance', 'outlier', 'deviation', 'scatter']
        if any(kw in all_text for kw in distribution_keywords):
            if len(data_points) >= 5:
                return 'bubble'
            return 'polarArea'

        # ===== Time/Cyclical =====
        time_keywords = ['q1', 'q2', 'q3', 'q4', '季度', '月', '年',
                        'week', 'month', 'year', '周期', 'season', '季节', '循环']
        if any(kw in all_text for kw in time_keywords):
            if any(kw in all_text for kw in ['周期', 'season', '循环', 'polar', 'arc']):
                return 'polarArea'
            return 'line'

        # ===== KPI/Target =====
        kpi_keywords = ['kpi', 'target', 'goal', '目标', '达标', 'achieve',
                       'variance', 'budget', 'actual', 'forecast', '预测']
        if any(kw in all_text for kw in kpi_keywords):
            return 'bar'

        # ===== Multi-dimensional =====
        multi_dim_keywords = ['雷达', 'radar', 'spider', '多维', 'dimension',
                             'skill', '能力', 'feature', 'competitor', '对比', 'matrix']
        if any(kw in all_text for kw in multi_dim_keywords):
            return 'radar'

        # ===== Proportions =====
        proportion_keywords = ['占比', 'share', 'composition', 'breakdown',
                              '构成', '分配', 'split', 'mix', 'portion']
        has_proportion_keywords = any(kw in all_text for kw in proportion_keywords)
        percent_count = sum(1 for u in units if u == '%')

        if (len(data_points) <= 7 and percent_count >= len(data_points) * 0.6) or has_proportion_keywords:
            if len(data_points) <= 5:
                return 'doughnut'
            return 'pie'

        # ===== Trends =====
        trend_keywords = ['趋势', 'growth', '增长', 'trend', 'change',
                         'increase', 'decrease', '变化', '上升', '下降', '历史']
        if any(kw in all_text for kw in trend_keywords):
            return 'line'

        # ===== Comparison =====
        comparison_keywords = ['对比', 'compare', 'vs', 'versus', 'difference',
                              '差异', 'regional', 'region', '区域', 'survey']
        long_labels = any(len(label) > 15 for label in labels)
        if any(kw in all_text for kw in comparison_keywords) or long_labels:
            return 'bar'

        # ===== Strategic Analysis =====
        strategy_keywords = ['bcg', 'matrix', 'portfolio', 'strategy', '战略',
                            'positioning', '定位', '投资', 'growth', 'share']
        if any(kw in all_text for kw in strategy_keywords):
            return 'scatter'

        # ===== Default heuristics =====

        # Small number of data points with percentages → pie/doughnut
        if len(data_points) <= 5 and percent_count == len(data_points):
            return 'doughnut'

        # Time series detected → line chart
        if self._detect_time_series(data_points):
            return 'line'

        # Otherwise default to bar chart
        return 'bar'

    def _detect_time_series(self, data_points: List[DataPoint]) -> bool:
        """Detect if data represents a time series."""
        time_patterns = [
            r'\d{4}',  # Years like 2020, 2021
            r'q[1-4]',  # Quarters Q1-Q4
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
            r'(一月|二月|三月|四月|五月|六月|七月|八月|九月|十月|十一月|十二月)',
        ]

        for dp in data_points:
            label = dp.label.lower()
            for pattern in time_patterns:
                if re.search(pattern, label):
                    return True

        return False


def main():
    """Command-line interface for testing."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python slide_planner.py <markdown_file>")
        sys.exit(1)

    from parser import DocumentParser

    # Parse document
    parser = DocumentParser()
    doc = parser.parse(sys.argv[1])

    # Plan slides
    planner = SlidePlanner()
    plan = planner.plan_slides(doc)

    # Print plan
    print(f"Presentation: {plan.title}")
    print(f"Total slides: {plan.total_slides}\n")

    for i, slide in enumerate(plan.slides):
        print(f"Slide {i + 1}: {slide.slide_type.value}")
        print(f"  Title: {slide.title}")
        print(f"  Layout: {slide.layout}")
        if slide.key_points:
            print(f"  Key points: {len(slide.key_points)}")
        if slide.data_points:
            print(f"  Data points: {len(slide.data_points)}")
        print()


if __name__ == "__main__":
    main()

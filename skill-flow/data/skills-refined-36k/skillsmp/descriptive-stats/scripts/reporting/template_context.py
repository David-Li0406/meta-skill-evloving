"""Template context builder for HTML reports.

Builds the complete context dictionary required for rendering
the product-grade HTML report template.
"""

from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.statistics import compute_basic_stats
from core.business_interpreter import (
    interpret_basic_stats,
    interpret_distribution,
    interpret_outliers,
    BusinessInsight,
)


def build_template_context(
    df: pd.DataFrame,
    results: Dict[str, Any],
    title: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Build complete template context for HTML rendering.

    Args:
        df: Input DataFrame
        results: Analysis results from run_analysis()
        title: Report title
        metadata: Optional metadata dictionary

    Returns:
        Complete context dictionary for template rendering
    """
    # Extract basic info
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    n_numeric = len(numeric_cols)
    n_rows = len(df)
    n_cols = len(df.columns)

    # Determine if has grouping
    has_grouping = 'group_comparison' in results and results['group_comparison']
    group_var = None
    if has_grouping:
        first_col = next(iter(results['group_comparison'].values()))
        group_var = first_col.get('group_col')

    # Build context
    context = {
        # Basic info
        'title': title or '描述性统计分析报告',
        'date': datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'),
        'file_name': metadata.get('file_name', 'data.csv') if metadata else 'data.csv',

        # Data info
        'data_info': {
            'n_rows': n_rows,
            'n_cols': n_cols,
            'n_numeric': n_numeric,
            'column_names': numeric_cols,
            'has_grouping': has_grouping,
            'group_var': group_var
        },

        # Executive summary (dynamic 4 metrics)
        'summary_metrics': _generate_summary_metrics(df, results, numeric_cols),

        # Basic statistics
        'basic_stats': _build_basic_stats_section(df, results, numeric_cols),

        # Distribution analysis
        'distribution': _build_distribution_section(results, numeric_cols),

        # Outlier detection
        'outliers': _build_outliers_section(results, numeric_cols),

        # Correlation analysis (if 2+ variables)
        'correlation': _build_correlation_section(df, results, numeric_cols) if n_numeric >= 2 else None,

        # Group comparison (if grouping exists)
        'group_comparison': _build_group_comparison_section(results, group_var) if has_grouping else None,

        # Findings and recommendations
        'findings': _synthesize_findings(results, numeric_cols),
        'recommendations': _generate_recommendations(results, numeric_cols),

        # Technical notes
        'technical_notes': {
            'methods': ['描述性统计', 'Shapiro-Wilk正态性检验', 'IQR异常值检测'],
            'significance_level': 'α = 0.05',
            'chart_library': 'Matplotlib'
        }
    }

    return context


def _generate_summary_metrics(df: pd.DataFrame, results: Dict, numeric_cols: List[str]) -> List[Dict[str, str]]:
    """Generate 4 dynamic summary metrics for executive summary.

    Rules:
    - Single column: 均值, 中位数, 标准差, 样本量
    - Multiple columns: 最大均值, 最小均值, 差异%, 总样本量
    - Grouping: 组数, 最优组, 最差组, 显著性
    """
    n_numeric = len(numeric_cols)
    metrics = []

    if n_numeric == 1:
        # Single column analysis
        col = numeric_cols[0]
        stats_dict = results.get('summary_stats_table', {})
        if isinstance(stats_dict, dict) and col in stats_dict:
            stats = stats_dict[col]
            metrics = [
                {'label': f'{col} 均值', 'value': f"{stats.get('mean', 0):.2f}", 'trend': 'neutral'},
                {'label': f'{col} 中位数', 'value': f"{stats.get('median', 0):.2f}", 'trend': 'neutral'},
                {'label': f'{col} 标准差', 'value': f"{stats.get('std', 0):.2f}", 'trend': 'neutral'},
                {'label': '样本量', 'value': str(len(df)), 'trend': 'neutral'}
            ]
        else:
            # Fallback to computed stats
            stats = compute_basic_stats(df[col])
            metrics = [
                {'label': f'{col} 均值', 'value': f"{stats['mean']:.2f}", 'trend': 'neutral'},
                {'label': f'{col} 中位数', 'value': f"{stats['median']:.2f}", 'trend': 'neutral'},
                {'label': f'{col} 标准差', 'value': f"{stats['std']:.2f}", 'trend': 'neutral'},
                {'label': '样本量', 'value': str(stats['count']), 'trend': 'neutral'}
            ]

    elif n_numeric >= 2:
        # Multiple columns comparison
        means = [df[col].mean() for col in numeric_cols]
        max_mean = max(means)
        min_mean = min(means)
        max_col = numeric_cols[means.index(max_mean)]
        min_col = numeric_cols[means.index(min_mean)]
        diff_pct = ((max_mean - min_mean) / min_mean * 100) if min_mean != 0 else 0

        metrics = [
            {'label': f'最大均值 ({max_col})', 'value': f"{max_mean:.2f}", 'trend': 'up'},
            {'label': f'最小均值 ({min_col})', 'value': f"{min_mean:.2f}", 'trend': 'down'},
            {'label': '差异幅度', 'value': f"{diff_pct:.1f}%", 'trend': 'neutral'},
            {'label': '总样本量', 'value': str(len(df)), 'trend': 'neutral'}
        ]

    return metrics


def _build_basic_stats_section(df: pd.DataFrame, results: Dict, numeric_cols: List[str]) -> Dict[str, Any]:
    """Build basic statistics section."""

    # Build table HTML
    table_rows = []
    for col in numeric_cols:
        stats = compute_basic_stats(df[col])
        table_rows.append({
            'name': col,
            'mean': f"{stats['mean']:.2f}",
            'median': f"{stats['median']:.2f}",
            'std': f"{stats['std']:.2f}",
            'min': f"{stats['min']:.2f}",
            'max': f"{stats['max']:.2f}",
            'count': stats['count']
        })

    # Quality assessment
    total_cells = len(df) * len(numeric_cols)
    missing_cells = sum(df[col].isna().sum() for col in numeric_cols)
    missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0

    if missing_pct > 10:
        quality = "数据存在较多缺失值，建议清洗后使用"
        quality_level = "warning"
    elif len(df) < 30:
        quality = "样本量较小，统计推断需谨慎"
        quality_level = "warning"
    else:
        quality = "数据质量良好，适合统计分析"
        quality_level = "success"

    # Generate insights
    insights = []
    for col in numeric_cols:
        stats = compute_basic_stats(df[col])
        col_insights = interpret_basic_stats(df[col], stats, col)
        insights.extend(col_insights)

    return {
        'table_rows': table_rows,
        'quality_assessment': quality,
        'quality_level': quality_level,
        'insights': [i.to_dict() for i in insights[:3]]  # Top 3 insights
    }


def _build_distribution_section(results: Dict, numeric_cols: List[str]) -> Dict[str, Any]:
    """Build distribution analysis section."""
    by_column = {}

    if 'distribution' not in results:
        return {'by_column': {}}

    for col in numeric_cols:
        if col not in results['distribution']:
            continue

        dist_data = results['distribution'][col]
        shape_stats = dist_data.get('shape_stats', {})
        normality_tests = dist_data.get('normality_tests', {})

        # Get Shapiro-Wilk test result
        shapiro_result = normality_tests.get('shapiro', {})
        if isinstance(shapiro_result, dict):
            is_normal = shapiro_result.get('is_normal', False)
            p_value = shapiro_result.get('p_value', 1.0)
            statistic = shapiro_result.get('statistic', 0)
        else:
            is_normal = False
            p_value = 1.0
            statistic = 0

        # Distribution description
        skewness = shape_stats.get('skewness', 0)
        kurtosis = shape_stats.get('kurtosis', 0)
        shape_desc = _describe_distribution(skewness, kurtosis)

        # Charts - support both Plotly HTML and matplotlib base64 images
        chart_html = dist_data.get('chart', '')

        # Check for new matplotlib base64 format
        histogram_chart = dist_data.get('histogram_chart', None)
        qqplot_chart = dist_data.get('qqplot_chart', None)

        # Generate chart HTML for matplotlib images if available
        if histogram_chart and histogram_chart.get('type') == 'matplotlib_base64':
            hist_img = f'''<div class="chart-container">
    <img src="data:image/png;base64,{histogram_chart['image_data']}"
         alt="{histogram_chart['alt']}"
         style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <p class="chart-caption">{histogram_chart['title']}</p>
</div>'''
        else:
            hist_img = chart_html if chart_html else ''

        if qqplot_chart and qqplot_chart.get('type') == 'matplotlib_base64':
            qq_img = f'''<div class="chart-container">
    <img src="data:image/png;base64,{qqplot_chart['image_data']}"
         alt="{qqplot_chart['alt']}"
         style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <p class="chart-caption">{qqplot_chart['title']}</p>
</div>'''
        else:
            qq_img = ''

        # Combine charts
        combined_chart = f"{hist_img}{qq_img}".strip()

        # Insights
        insights_list = dist_data.get('insights', [])

        by_column[col] = {
            'skewness': skewness,
            'kurtosis': kurtosis,
            'shape_desc': shape_desc,
            'normality_test': {
                'statistic': statistic,
                'p_value': p_value,
                'is_normal': is_normal
            },
            'chart': combined_chart,
            'insights': insights_list
        }

    return {'by_column': by_column}


def _build_outliers_section(results: Dict, numeric_cols: List[str]) -> Dict[str, Any]:
    """Build outlier detection section."""
    by_column = {}

    if 'outliers' not in results:
        return {'by_column': {}}

    for col in numeric_cols:
        if col not in results['outliers']:
            continue

        outlier_data = results['outliers'][col]

        # Quality assessment
        outlier_pct = outlier_data.get('outlier_percentage', 0)
        if outlier_pct == 0:
            quality = "good"
        elif outlier_pct < 5:
            quality = "warning"
        else:
            quality = "danger"

        # Chart - support both Plotly HTML and matplotlib base64 images
        chart_obj = outlier_data.get('chart', {})
        chart_html = chart_obj if isinstance(chart_obj, str) else ''

        # Generate chart HTML for matplotlib base64 image if available
        if isinstance(chart_obj, dict) and chart_obj.get('type') == 'matplotlib_base64':
            chart_html = f'''<div class="chart-container">
    <img src="data:image/png;base64,{chart_obj['image_data']}"
         alt="{chart_obj['alt']}"
         style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <p class="chart-caption">{chart_obj['title']}</p>
</div>'''

        # Insights
        insights_list = outlier_data.get('insights', [])

        by_column[col] = {
            'lower_bound': outlier_data.get('lower_bound', 0),
            'upper_bound': outlier_data.get('upper_bound', 0),
            'outlier_count': outlier_data.get('outlier_count', 0),
            'outlier_percentage': outlier_pct,
            'quality': quality,
            'chart': chart_html,
            'insights': insights_list
        }

    return {'by_column': by_column}


def _build_correlation_section(df: pd.DataFrame, results: Dict, numeric_cols: List[str]) -> Optional[Dict[str, Any]]:
    """Build correlation analysis section (for 2+ variables)."""
    if len(numeric_cols) < 2:
        return None

    # Compute correlation matrix
    corr_matrix = df[numeric_cols].corr()

    # Build insights
    insights = []
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            corr_val = corr_matrix.iloc[i, j]

            if abs(corr_val) > 0.7:
                level = "critical"
                desc = f"{col1}与{col2}呈强{'正' if corr_val > 0 else '负'}相关 (r={corr_val:.2f})"
            elif abs(corr_val) > 0.4:
                level = "warning"
                desc = f"{col1}与{col2}呈中等{'正' if corr_val > 0 else '负'}相关 (r={corr_val:.2f})"
            elif abs(corr_val) > 0.2:
                level = "info"
                desc = f"{col1}与{col2}呈弱{'正' if corr_val > 0 else '负'}相关 (r={corr_val:.2f})"
            else:
                level = "success"
                desc = f"{col1}与{col2}无明显相关 (r={corr_val:.2f})"

            insights.append({
                'level': level,
                'description': desc
            })

    return {
        'has_data': True,
        'matrix': corr_matrix.to_dict(),
        'insights': insights[:5]  # Top 5 correlations
    }


def _build_group_comparison_section(results: Dict, group_var: str) -> Optional[Dict[str, Any]]:
    """Build group comparison section."""
    if 'group_comparison' not in results:
        return None

    # Get first comparison result
    first_key = next(iter(results['group_comparison'].keys()))
    comp_data = results['group_comparison'][first_key]

    test_result = comp_data.get('test_result', {})

    return {
        'has_data': True,
        'group_var': group_var,
        'test_result': test_result,
        'chart': comp_data.get('chart', ''),
        'insights': comp_data.get('insights', [])
    }


def _synthesize_findings(results: Dict, numeric_cols: List[str]) -> Dict[str, Any]:
    """Synthesize key findings from all analysis results."""

    findings_points = []

    # Data quality
    if 'outliers' in results:
        total_outliers = sum(
            results['outliers'].get(col, {}).get('outlier_count', 0)
            for col in numeric_cols
            if col in results['outliers']
        )
        if total_outliers == 0:
            findings_points.append({
                'category': '数据质量',
                'content': f'所有{len(numeric_cols)}个变量均未发现异常值，数据质量良好'
            })
        else:
            findings_points.append({
                'category': '数据质量',
                'content': f'检测到{total_outliers}个异常值，建议核实数据'
            })

    # Distribution
    if 'distribution' in results:
        normal_count = 0
        for col in numeric_cols:
            if col in results['distribution']:
                dist_data = results['distribution'][col]
                normality = dist_data.get('normality_tests', {}).get('shapiro', {})
                if isinstance(normality, dict) and normality.get('is_normal'):
                    normal_count += 1

        if normal_count == len(numeric_cols):
            findings_points.append({
                'category': '分布特征',
                'content': f'所有{len(numeric_cols)}个变量均符合正态分布，适合参数统计方法'
            })
        elif normal_count == 0:
            findings_points.append({
                'category': '分布特征',
                'content': f'所有{len(numeric_cols)}个变量均不符合正态分布，建议使用非参数方法'
            })
        else:
            findings_points.append({
                'category': '分布特征',
                'content': f'{normal_count}/{len(numeric_cols)}个变量符合正态分布'
            })

    # Summary
    summary = f"本报告对{len(numeric_cols)}个变量进行了全面的描述性统计分析。"

    return {
        'summary': summary,
        'points': findings_points
    }


def _generate_recommendations(results: Dict, numeric_cols: List[str]) -> Dict[str, List]:
    """Generate prioritized recommendations from insights."""

    priority_high = []
    priority_medium = []
    priority_low = []
    priority_analysis = []

    # Track seen titles for deduplication (use defaultdict for unknown levels)
    from collections import defaultdict
    seen_titles = defaultdict(set)

    # Collect all insights
    all_insights = []

    # From distribution
    if 'distribution' in results:
        for col in numeric_cols:
            if col in results['distribution']:
                insights = results['distribution'][col].get('insights', [])
                all_insights.extend(insights)

    # From outliers
    if 'outliers' in results:
        for col in numeric_cols:
            if col in results['outliers']:
                insights = results['outliers'][col].get('insights', [])
                all_insights.extend(insights)

    # From business insights if available
    if 'business_insights' in results:
        all_insights.extend(results['business_insights'])

    # Prioritize and deduplicate
    for insight in all_insights:
        if isinstance(insight, dict):
            level = insight.get('level', 'info')
            title = insight.get('title', '')
            desc = insight.get('description', '')
            sugg = insight.get('suggestion', '')
        elif hasattr(insight, 'level'):
            level = insight.level
            title = insight.title
            desc = insight.description
            sugg = insight.suggestion or desc
        else:
            continue

        # Skip if we've already seen this title
        if title in seen_titles[level]:
            continue
        seen_titles[level].add(title)

        rec = {
            'title': title,
            'content': sugg or desc
        }

        if level == 'critical':
            priority_high.append(rec)
        elif level == 'warning':
            priority_medium.append(rec)
        elif level == 'info':
            priority_low.append(rec)
        else:
            priority_analysis.append(rec)

    return {
        'priority_high': priority_high,
        'priority_medium': priority_medium,
        'priority_low': priority_low,
        'priority_analysis': priority_analysis
    }


def _describe_distribution(skewness: float, kurtosis: float) -> str:
    """Generate distribution description."""

    # Shape
    if abs(skewness) < 0.5:
        shape = "近似对称分布"
    elif skewness > 0:
        shape = f"右偏分布 (偏度={skewness:.2f}，存在高值拉动)"
    else:
        shape = f"左偏分布 (偏度={skewness:.2f}，存在低值拉动)"

    # Peak
    if abs(kurtosis) < 1:
        peak = "正态峰度"
    elif kurtosis > 0:
        peak = f"尖峰分布 (峰度={kurtosis:.2f})"
    else:
        peak = f"平峰分布 (峰度={kurtosis:.2f})"

    return f"{shape}，{peak}"

"""HTML report generation module.

Creates product-grade HTML reports with embedded Matplotlib charts
and business-friendly insights.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Import new template context builder (relative import)
import sys
sys.path.insert(0, str(Path(__file__).parent))
from template_context import build_template_context


def generate_html_report(
    df: pd.DataFrame,
    results: Dict[str, Any],
    output_path: str,
    title: str = "描述性统计分析报告",
    metadata: Optional[Dict[str, Any]] = None
):
    """Generate a complete HTML report using product-grade template.

    Args:
        df: Input DataFrame
        results: Analysis results dictionary
        output_path: Path to save HTML report
        title: Report title
        metadata: Optional metadata (date, analyst, etc.)
    """
    # Build template context using the new context builder
    context = build_template_context(df, results, title, metadata)

    # Get template directory
    template_dir = Path(__file__).parent / 'templates'

    # Verify template exists
    template_path = template_dir / 'report.html'
    if not template_path.exists():
        raise FileNotFoundError(
            f"Required template file not found: {template_path}\n"
            f"Please ensure the template file exists in the templates directory."
        )

    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load template
    template = env.get_template('report.html')

    # Render template
    html_content = template.render(**context)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def embed_plotly_figure(fig, div_id: str = "chart") -> str:
    """Convert Plotly figure to HTML div.

    Args:
        fig: Plotly Figure object
        div_id: ID for the div element

    Returns:
        HTML string with embedded chart
    """
    return fig.to_html(
        include_plotlyjs=False,
        config={'displayModeBar': True, 'displaylogo': False},
        div_id=div_id
    )


def create_summary_table_html(
    stats: Dict[str, Dict[str, float]]
) -> str:
    """Create HTML table for summary statistics.

    Args:
        stats: Dictionary mapping column names to their statistics

    Returns:
        HTML string with table
    """
    df = pd.DataFrame(stats).T

    # Format for display
    html = df.to_html(
        classes='table table-striped table-hover',
        float_format=lambda x: f'{x:.4f}' if not pd.isna(x) else '—',
        border=0
    )

    return html


def create_charts_html(
    series: pd.Series,
    charts: Dict[str, Any]
) -> str:
    """Create HTML section with embedded charts.

    Args:
        series: Data series
        charts: Dictionary of chart names to Plotly figures

    Returns:
        HTML string with embedded charts
    """
    html_parts = []

    for chart_name, fig in charts.items():
        chart_div = embed_plotly_figure(fig, div_id=f"chart-{chart_name}")
        html_parts.append(f'<div class="chart-container">{chart_div}</div>')

    return '\n'.join(html_parts)


def create_single_column_report(
    series: pd.Series,
    output_path: str,
    column_name: Optional[str] = None
):
    """Create a focused report for a single column.

    Args:
        series: pandas Series with data
        output_path: Path to save HTML report
        column_name: Name for the column (defaults to series.name)
    """
    if column_name is None:
        column_name = series.name if series.name else "Value"

    title = f"Analysis Report: {column_name}"

    # Calculate statistics
    from core.statistics import compute_basic_stats
    from core.distribution import test_normality
    from core.outliers import detect_outliers_iqr

    stats = compute_basic_stats(series)
    normality = test_normality(series)
    outliers = detect_outliers_iqr(series)

    # Create charts
    hist_fig = create_histogram(series, title=f"Distribution of {column_name}")
    qq_fig = create_qqplot(series, title=f"Q-Q Plot: {column_name}")
    outlier_fig = create_outlier_plot(series, outliers.outlier_indices, title=f"Outliers: {column_name}")

    # Prepare results
    results = {
        'summary_stats_table': _create_single_column_stats_table(stats),
        'distribution': {
            column_name: {
                'normality_tests': normality,
                'chart': figure_to_html(hist_fig),
            }
        },
        'outliers': {
            column_name: {
                'method': outliers.method,
                'outlier_count': outliers.outlier_count,
                'outlier_percentage': outliers.outlier_percentage,
                'chart': figure_to_html(outlier_fig),
            }
        },
        'num_analyzed': 1,
    }

    # Generate report
    df = pd.DataFrame({column_name: series})
    generate_html_report(df, results, output_path, title)


def _create_single_column_stats_table(stats: Dict[str, float]) -> str:
    """Create HTML table for single column statistics.

    Args:
        stats: Statistics dictionary

    Returns:
        HTML table string
    """
    table_html = '<table>'

    rows = [
        ('Count', stats.get('count', 0)),
        ('Mean', stats.get('mean')),
        ('Median', stats.get('median')),
        ('Mode', stats.get('mode')),
        ('Std Dev', stats.get('std')),
        ('Variance', stats.get('variance')),
        ('Minimum', stats.get('min')),
        ('Q1 (25%)', stats.get('q1')),
        ('Q3 (75%)', stats.get('q3')),
        ('Maximum', stats.get('max')),
        ('Range', stats.get('range')),
        ('IQR', stats.get('iqr')),
        ('Skewness', stats.get('skewness')),
        ('Kurtosis', stats.get('kurtosis')),
        ('CV (%)', stats.get('cv')),
    ]

    for label, value in rows:
        if isinstance(value, float):
            formatted = f'{value:.4f}'
        elif isinstance(value, int):
            formatted = f'{value:,}'
        else:
            formatted = '—'

        table_html += f'<tr><td><strong>{label}</strong></td><td>{formatted}</td></tr>'

    table_html += '</table>'

    return table_html

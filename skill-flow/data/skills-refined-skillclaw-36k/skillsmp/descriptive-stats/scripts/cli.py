#!/usr/bin/env python3
"""Main CLI entry point for descriptive statistics skill.

Provides both interactive and command-line modes for statistical analysis.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import business interpreter
from core.business_interpreter import (
    interpret_basic_stats,
    interpret_distribution,
    interpret_outliers,
    interpret_group_comparison,
    generate_executive_summary,
    BusinessInsight,
)

from core.data_loader import load_data, validate_data, get_numeric_columns, get_categorical_columns, get_data_summary
from core.statistics import compute_basic_stats, compute_summary_table
from core.distribution import test_normality, distribution_summary
from core.outliers import detect_outliers_iqr, detect_outliers_zscore, consensus_outliers
from core.group_analysis import compare_groups, group_comparison_table
from visualization.matplotlib_charts import (
    create_histogram,
    create_boxplot,
    create_qqplot,
    create_outlier_plot,
    figure_to_base64,
)
from reporting.terminal import (
    display_data_summary,
    display_statistics_table,
    display_distribution_results,
    display_outliers,
    display_group_comparison,
    print_section_header,
    print_warning,
    print_error,
    print_success,
    print_info,
    get_console,
)
from reporting.html_report import (
    generate_html_report,
    create_single_column_report,
    embed_plotly_figure,
)


def interactive_mode():
    """Run interactive analysis mode."""
    console = get_console()
    console.print("[bold cyan]Interactive Descriptive Statistics Analysis[/bold cyan]")
    console.print()

    # Step 1: Select file
    console.print("Step 1: Select data file")
    console.print("  Enter the path to your CSV or Excel file:")

    while True:
        file_path = console.input("[bold green]File path:[/bold green] ").strip()

        if not file_path:
            console.print("[yellow]Empty path. Please try again.[/yellow]")
            continue

        try:
            df = load_data(file_path)
            print_success(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            break
        except FileNotFoundError:
            print_error(f"File not found: {file_path}")
        except Exception as e:
            print_error(f"Error loading file: {e}")

    # Step 2: Data preview and validation
    console.print()
    print_section_header("Step 2: Data Preview")

    # Show data summary
    summary = get_data_summary(df)
    display_data_summary(summary)

    # Show first few rows
    console.print()
    console.print("[bold]First 5 rows:[/bold]")
    console.print(df.head().to_table(index=False))

    # Step 3: Select columns to analyze
    console.print()
    print_section_header("Step 3: Select Columns")

    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    console.print(f"[cyan]Numeric columns ({len(numeric_cols)}):[/cyan] {', '.join(numeric_cols)}")
    console.print(f"[cyan]Categorical columns ({len(categorical_cols)}):[/cyan] {', '.join(categorical_cols)}")

    if numeric_cols:
        console.print()
        analyze_all = console.input("[bold green]Analyze all numeric columns? [Y/n]:[/bold green] ").strip().lower()

        if analyze_all in ['', 'y', 'yes']:
            columns_to_analyze = numeric_cols
        else:
            console.print("Enter columns to analyze (comma-separated):")
            cols_input = console.input("[bold green]Columns:[/bold green] ").strip()
            columns_to_analyze = [c.strip() for c in cols_input.split(',') if c.strip() in numeric_cols]
    else:
        print_error("No numeric columns found for analysis")
        return

    if not columns_to_analyze:
        print_error("No valid columns selected")
        return

    print_success(f"Will analyze: {', '.join(columns_to_analyze)}")

    # Step 4: Select analysis type
    console.print()
    print_section_header("Step 4: Select Analysis Type")

    console.print("Available analysis types:")
    console.print("  1. Basic Statistics (mean, median, std, etc.)")
    console.print("  2. Distribution Analysis (normality tests, histograms)")
    console.print("  3. Outlier Detection (IQR, Z-score methods)")
    console.print("  4. All of the above")
    console.print("  5. Group Comparison (requires categorical column)")

    analysis_choice = console.input("[bold green]Select analysis [1-5]:[/bold green] ").strip()

    # Step 5: Select output format
    console.print()
    print_section_header("Step 5: Select Output Format")

    console.print("Output options:")
    console.print("  1. Terminal only")
    console.print("  2. HTML report only")
    console.print("  3. Both terminal and HTML")

    output_choice = console.input("[bold green]Select output [1-3]:[/bold green] ").strip()

    output_terminal = output_choice in ['1', '3']
    output_html = output_choice in ['2', '3']

    # Run the analysis
    console.print()
    print_section_header("Running Analysis")

    results = run_analysis(
        df,
        columns_to_analyze,
        analysis_type=analysis_choice,
        output_terminal=output_terminal,
        output_html=output_html,
    )

    # Save HTML report if requested
    if output_html:
        console.print()
        output_path = console.input("[bold green]Save HTML report as:[/bold green] ").strip()
        if not output_path:
            output_path = "analysis_report.html"

        try:
            generate_html_report(
                df,
                results,
                output_path,
                title="Descriptive Statistics Analysis Report"
            )
            print_success(f"HTML report saved to: {output_path}")
        except Exception as e:
            print_error(f"Failed to save HTML report: {e}")


def run_analysis(
    df: pd.DataFrame,
    columns: List[str],
    analysis_type: str = '4',
    output_terminal: bool = True,
    output_html: bool = False,
    group_col: Optional[str] = None,
) -> dict:
    """Run the selected analysis on specified columns.

    Args:
        df: Input DataFrame
        columns: Columns to analyze
        analysis_type: Analysis type (1-5)
        output_terminal: Whether to display in terminal
        output_html: Whether to generate HTML report
        group_col: Column for grouping (for group comparison)

    Returns:
        Dictionary with analysis results
    """
    results = {
        'num_analyzed': len(columns),
    }

    # Prepare results dictionary for HTML report
    html_results = {}
    all_business_insights = []  # 收集所有业务洞察

    # 1. Basic Statistics
    if analysis_type in ['1', '4']:
        stats_dict = {}
        for col in columns:
            stats_dict[col] = compute_basic_stats(df[col])

        if output_terminal:
            display_statistics_table(stats_dict)

        # Prepare for HTML
        stats_df = pd.DataFrame(stats_dict).T
        html_results['summary_stats_table'] = stats_df.to_html(
            classes='table table-striped',
            float_format='%.4f',
            border=0
        )

        # Generate business insights for basic stats
        for col in columns:
            insights = interpret_basic_stats(df[col], stats_dict[col], col)
            all_business_insights.extend(insights)

    # 2. Distribution Analysis
    if analysis_type in ['2', '4']:
        distribution_results = {}

        for col in columns:
            dist_summary = distribution_summary(df[col])

            if output_terminal:
                display_distribution_results(dist_summary, column_name=col)

            # Create histogram and Q-Q plot using Matplotlib
            hist_base64 = create_histogram(df[col], title=f"{col} 分布图")
            qq_base64 = create_qqplot(df[col], title=f"{col} Q-Q图")

            # Generate business insights for distribution
            shape_stats = dist_summary['shape_stats']
            is_normal = any(v['is_normal'] for v in dist_summary['normality_tests'].values() if not isinstance(v, dict) or v.get('is_normal'))
            dist_insights = interpret_distribution(
                shape_stats['skewness'],
                shape_stats['kurtosis'],
                is_normal,
                col
            )
            all_business_insights.extend(dist_insights)

            # Prepare chart data for template rendering
            # Save both histogram and QQ plot as separate charts
            distribution_results[col] = {
                'shape_stats': shape_stats,
                'normality_tests': dist_summary['normality_tests'],  # Already in dict format
                'histogram_chart': {
                    'type': 'matplotlib_base64',
                    'image_data': hist_base64,
                    'title': f'{col} 分布图',
                    'alt': f'{col} 分布图'
                },
                'qqplot_chart': {
                    'type': 'matplotlib_base64',
                    'image_data': qq_base64,
                    'title': f'{col} Q-Q图',
                    'alt': f'{col} Q-Q图'
                },
                'insights': [i.to_dict() for i in dist_insights],  # Add insights to results
            }

        html_results['distribution'] = distribution_results

    # 3. Outlier Detection
    if analysis_type in ['3', '4']:
        outlier_results = {}

        for col in columns:
            outliers = consensus_outliers(df[col])

            if output_terminal:
                display_outliers(outliers, column_name=col)

            # Create outlier plot using Matplotlib
            outlier_base64 = create_outlier_plot(df[col], outliers.outlier_indices, title=f"{col} 异常值检测")

            # Generate business insights for outliers
            outlier_insights = interpret_outliers(
                outliers.outlier_count,
                outliers.outlier_percentage,
                len(df[col].dropna()),
                col
            )
            all_business_insights.extend(outlier_insights)

            # Prepare chart data for template rendering
            outlier_results[col] = {
                'method': outliers.method,
                'outlier_count': outliers.outlier_count,
                'outlier_percentage': outliers.outlier_percentage,
                'lower_bound': outliers.lower_bound,
                'upper_bound': outliers.upper_bound,
                'chart': {
                    'type': 'matplotlib_base64',
                    'image_data': outlier_base64,
                    'title': f'{col} 异常值检测',
                    'alt': f'{col} 异常值检测'
                },
                'insights': [i.to_dict() for i in outlier_insights],  # Add insights to results
            }

        html_results['outliers'] = outlier_results

    # 5. Group Comparison
    if analysis_type == '5' and group_col:
        if output_terminal:
            print_info(f"Comparing {', '.join(columns)} by {group_col}")

        group_comparison_results = {}
        group_stats_tables = {}

        for col in columns:
            comparison = compare_groups(df, group_col, col)

            if output_terminal:
                display_group_comparison(comparison)

            # Create box plot using Matplotlib
            box_base64 = create_boxplot(df, group_col, col, title=f"{col} 按 {group_col} 分组")

            # Generate business insights for group comparison
            if comparison.test_result:
                test_result_dict = {
                    'test_name': comparison.test_result.test_name,
                    'statistic': comparison.test_result.statistic,
                    'p_value': comparison.test_result.p_value,
                    'is_significant': comparison.test_result.is_significant,
                    'interpretation': comparison.test_result.interpretation,
                    'effect_size': comparison.test_result.effect_size,
                }

                # Get group statistics
                group_stats = {}
                for group_name in df[group_col].unique():
                    group_data = df[df[group_col] == group_name][col].dropna()
                    group_stats[group_name] = compute_basic_stats(group_data)

                group_insights = interpret_group_comparison(
                    test_result_dict,
                    group_stats,
                    col,
                    group_col
                )
                all_business_insights.extend(group_insights)
            else:
                test_result_dict = None
                group_insights = []

            # Convert to HTML img tag
            chart_html = f'''
<div style="margin: 15px 0;">
    <img src="data:image/png;base64,{box_base64}"
         alt="{col} 按 {group_col} 分组对比"
         style="width:100%;max-width:800px;height:auto;border:1px solid #e9ecef;border-radius:8px;">
</div>'''

            group_comparison_results[col] = {
                'group_col': group_col,
                'value_col': col,
                'num_groups': comparison.num_groups,
                'test_result': test_result_dict,
                'chart': chart_html,
                'insights': [i.to_dict() for i in group_insights],  # Add insights to results
            }

            # Group statistics table
            group_stats_df = group_comparison_table(df, group_col, col)
            group_stats_tables[col] = group_stats_df.to_html(
                classes='table table-striped',
                float_format='%.4f',
                border=0
            )

        html_results['group_comparison'] = group_comparison_results
        html_results['group_stats_table'] = group_stats_tables

    # Generate executive summary
    if all_business_insights:
        executive_summary = generate_executive_summary(all_business_insights)
        html_results['executive_summary'] = {
            'overall_status': executive_summary['overall_status'],
            'overall_color': executive_summary['overall_color'],
            'total_insights': executive_summary['total_insights'],
            'by_level': executive_summary['by_level'],
            'by_category': executive_summary['by_category'],
            'top_insights': [i.to_dict() for i in executive_summary['top_insights']],
        }

        # Add general business insights section
        html_results['business_insights'] = [i.to_dict() for i in all_business_insights]

    results.update(html_results)
    return results


def command_line_mode(args):
    """Run analysis in command-line mode.

    Args:
        args: Parsed command-line arguments
    """
    console = get_console()

    # Load data
    try:
        df = load_data(args.file)
        print_success(f"Loaded {len(df)} rows and {len(df.columns)} columns from {args.file}")
    except Exception as e:
        print_error(f"Failed to load file: {e}")
        return 1

    # Determine columns to analyze
    if args.all:
        columns = get_numeric_columns(df)
    elif args.columns:
        columns = [c.strip() for c in args.columns.split(',')]
        # Validate columns
        numeric_cols = get_numeric_columns(df)
        columns = [c for c in columns if c in numeric_cols]
        if not columns:
            print_error("No valid numeric columns specified")
            return 1
    else:
        # Default: analyze all numeric columns
        columns = get_numeric_columns(df)

    print_info(f"Analyzing {len(columns)} column(s): {', '.join(columns)}")

    # Determine analysis type
    analysis_type = '4'  # Default: all analysis types
    if args.basic_only:
        analysis_type = '1'
    elif args.distribution_only:
        analysis_type = '2'
    elif args.outliers_only:
        analysis_type = '3'

    # Run analysis
    try:
        results = run_analysis(
            df,
            columns,
            analysis_type=analysis_type,
            output_terminal=args.terminal or not args.html,
            output_html=args.html or args.output,
            group_col=args.group_by,
        )
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Save HTML report if requested
    if args.html or args.output:
        output_path = args.output or "analysis_report.html"

        try:
            generate_html_report(
                df,
                results,
                output_path,
                title=f"Analysis Report: {Path(args.file).name}"
            )
            print_success(f"HTML report saved to: {output_path}")
        except Exception as e:
            print_error(f"Failed to save HTML report: {e}")
            return 1

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Descriptive Statistics Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py

  # Analyze all numeric columns in a CSV file
  python cli.py analyze data.csv --all

  # Analyze specific columns
  python cli.py analyze data.csv --columns col1,col2,col3

  # Generate HTML report only
  python cli.py analyze data.csv --all --html --output report.html

  # Group comparison
  python cli.py analyze data.csv --all --group-by category

  # Basic statistics only
  python cli.py analyze data.csv --all --basic-only
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a data file')

    analyze_parser.add_argument(
        'file',
        help='Path to CSV or Excel file'
    )

    analyze_parser.add_argument(
        '--columns', '-c',
        help='Comma-separated list of columns to analyze'
    )

    analyze_parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Analyze all numeric columns'
    )

    analyze_parser.add_argument(
        '--group-by', '-g',
        help='Column for group comparison'
    )

    analyze_parser.add_argument(
        '--output', '-o',
        help='Output HTML report path'
    )

    analyze_parser.add_argument(
        '--html',
        action='store_true',
        help='Generate HTML report'
    )

    analyze_parser.add_argument(
        '--terminal', '-t',
        action='store_true',
        help='Display results in terminal'
    )

    analyze_parser.add_argument(
        '--basic-only',
        action='store_true',
        help='Only compute basic statistics'
    )

    analyze_parser.add_argument(
        '--distribution-only',
        action='store_true',
        help='Only perform distribution analysis'
    )

    analyze_parser.add_argument(
        '--outliers-only',
        action='store_true',
        help='Only perform outlier detection'
    )

    # Parse arguments
    args = parser.parse_args()

    # Run in appropriate mode
    if args.command == 'analyze':
        sys.exit(command_line_mode(args))
    else:
        # No command specified, run interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()

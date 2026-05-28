"""Terminal output module using Rich library.

Provides beautiful formatted output for terminal display.
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.layout import Layout
from rich import box
from rich.text import Text
from rich.columns import Columns
from rich.align import Align


# Global console instance
console = Console()


def print_section_header(title: str, style: str = "bold cyan"):
    """Print a section header.

    Args:
        title: Section title
        style: Rich style string
    """
    console.print()
    console.print(Panel(
        Text(title, style=style),
        box=box.DOUBLE,
        padding=(0, 1)
    ))


def print_warning(message: str):
    """Print a warning message.

    Args:
        message: Warning message
    """
    console.print(f"[yellow]⚠ {message}[/yellow]")


def print_error(message: str):
    """Print an error message.

    Args:
        message: Error message
    """
    console.print(f"[red]✗ {message}[/red]")


def print_success(message: str):
    """Print a success message.

    Args:
        message: Success message
    """
    console.print(f"[green]✓ {message}[/green]")


def print_info(message: str):
    """Print an info message.

    Args:
        message: Info message
    """
    console.print(f"[blue]ℹ {message}[/blue]")


def display_data_summary(summary: Dict[str, Any]):
    """Display data summary information.

    Args:
        summary: Dictionary with data summary from get_data_summary()
    """
    print_section_header("Data Summary")

    # Basic info
    info_table = Table(title="Basic Information", show_header=False, box=box.SIMPLE)
    info_table.add_column("", style="cyan")
    info_table.add_column("", style="white")

    shape = summary.get('shape', (0, 0))
    info_table.add_row("Rows", f"{shape[0]:,}")
    info_table.add_row("Columns", f"{shape[1]:,}")
    info_table.add_row("Numeric Columns", str(len(summary.get('numeric_columns', []))))
    info_table.add_row("Categorical Columns", str(len(summary.get('categorical_columns', []))))

    console.print(info_table)

    # Show column types
    column_types = summary.get('column_types', {})
    if column_types:
        type_table = Table(title="Column Types", show_header=True, box=box.SIMPLE)
        type_table.add_column("Column", style="cyan")
        type_table.add_column("Type", style="yellow")

        for col, ctype in column_types.items():
            type_table.add_row(col, ctype.value if hasattr(ctype, 'value') else str(ctype))

        console.print(type_table)

    # Show warnings and errors
    warnings = summary.get('warnings', [])
    errors = summary.get('errors', [])

    if warnings:
        console.print()
        for warning in warnings:
            print_warning(warning)

    if errors:
        console.print()
        for error in errors:
            print_error(error)


def display_statistics_table(
    stats: Dict[str, Dict[str, float]],
    title: str = "Descriptive Statistics"
):
    """Display statistics table in terminal.

    Args:
        stats: Dictionary mapping column names to their statistics
        title: Table title
    """
    print_section_header(title)

    # Create main table
    table = Table(title=title, show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Statistic", style="cyan", no_wrap=True)

    # Add column for each data column
    for col_name in stats.keys():
        table.add_column(col_name, style="white", justify="right")

    # Define rows
    rows = [
        ("Count", "count"),
        ("Mean", "mean"),
        ("Median", "median"),
        ("Mode", "mode"),
        ("Std Dev", "std"),
        ("Variance", "variance"),
        ("Min", "min"),
        ("Q1", "q1"),
        ("Median", "q2"),
        ("Q3", "q3"),
        ("Max", "max"),
        ("Range", "range"),
        ("IQR", "iqr"),
        ("Skewness", "skewness"),
        ("Kurtosis", "kurtosis"),
        ("CV %", "cv"),
    ]

    # Add rows
    for label, key in rows:
        row_values = [label]
        for col_stats in stats.values():
            value = col_stats.get(key, np.nan)
            if isinstance(value, float):
                if key == "cv":
                    row_values.append(f"{value:.2f}")
                elif abs(value) >= 1000:
                    row_values.append(f"{value:,.2f}")
                elif abs(value) >= 100:
                    row_values.append(f"{value:.2f}")
                elif abs(value) >= 1:
                    row_values.append(f"{value:.4f}")
                else:
                    row_values.append(f"{value:.6f}")
            else:
                row_values.append(str(value) if not pd.isna(value) else "—")
        table.add_row(*row_values)

    console.print(table)


def display_distribution_results(
    results: Dict[str, Any],
    column_name: str = "Value"
):
    """Display distribution analysis results.

    Args:
        results: Results from test_normality() or distribution_summary()
        column_name: Name of the analyzed column
    """
    print_section_header(f"Distribution Analysis: {column_name}")

    # Show shape statistics
    shape_stats = results.get('shape_stats', results)

    shape_table = Table(show_header=False, box=box.SIMPLE)
    shape_table.add_column("", style="cyan")
    shape_table.add_column("", style="white")
    shape_table.add_column("Interpretation", style="yellow")

    skewness = shape_stats.get('skewness', np.nan)
    kurtosis = shape_stats.get('kurtosis', np.nan)

    if not pd.isna(skewness):
        skew_interp = shape_stats.get('skewness_interpretation', '')
        shape_table.add_row("Skewness", f"{skewness:.4f}", skew_interp)

    if not pd.isna(kurtosis):
        kurt_interp = shape_stats.get('kurtosis_interpretation', '')
        shape_table.add_row("Kurtosis (excess)", f"{kurtosis:.4f}", kurt_interp)

    console.print(shape_table)

    # Show normality tests
    normality_tests = results.get('normality_tests', {})

    if normality_tests:
        console.print()

        test_table = Table(title="Normality Tests", show_header=True, box=box.SIMPLE)
        test_table.add_column("Test", style="cyan")
        test_table.add_column("Statistic", style="white", justify="right")
        test_table.add_column("p-value", style="white", justify="right")
        test_table.add_column("Result", style="yellow")

        for test_name, test_result in normality_tests.items():
            statistic = test_result.get('statistic', np.nan)
            p_value = test_result.get('p_value', np.nan)
            interp = test_result.get('interpretation', '')

            stat_str = f"{statistic:.4f}" if not pd.isna(statistic) else "—"
            p_str = f"{p_value:.4f}" if not pd.isna(p_value) else "—"

            # Color code the result
            if "Normal" in interp and "Not" not in interp:
                result_style = "[green]Normal[/green]"
            elif "Not normal" in interp.lower():
                result_style = "[red]Not Normal[/red]"
            else:
                result_style = interp

            test_table.add_row(test_name.replace('_', ' ').title(), stat_str, p_str, result_style)

        console.print(test_table)


def display_outliers(
    outlier_result: Any,
    column_name: str = "Value"
):
    """Display outlier detection results.

    Args:
        outlier_result: OutlierResult from outlier detection functions
        column_name: Name of the analyzed column
    """
    print_section_header(f"Outlier Detection: {column_name}")

    # Create summary table
    summary_table = Table(show_header=False, box=box.SIMPLE)
    summary_table.add_column("", style="cyan")
    summary_table.add_column("", style="white")

    method = outlier_result.method
    count = outlier_result.outlier_count
    percentage = outlier_result.outlier_percentage

    summary_table.add_row("Method", method)
    summary_table.add_row("Outliers Found", f"{count}")

    if count > 0:
        summary_table.add_row("Percentage", f"{percentage:.2f}%")
        summary_table.add_row("Lower Bound", f"{outlier_result.lower_bound:.4f}")
        summary_table.add_row("Upper Bound", f"{outlier_result.upper_bound:.4f}")

    console.print(summary_table)

    # Show outlier values if any
    if count > 0 and count <= 20:
        console.print()
        console.print("[yellow]Outlier Values:[/yellow]")

        values = outlier_result.outlier_values
        indices = outlier_result.outlier_indices

        outlier_table = Table(show_header=True, box=box.SIMPLE)
        outlier_table.add_column("Index", style="cyan", justify="right")
        outlier_table.add_column("Value", style="red", justify="right")

        for idx, val in zip(indices, values):
            outlier_table.add_row(str(idx), f"{val:.4f}")

        console.print(outlier_table)

    elif count > 20:
        print_warning(f"Too many outliers to display ({count}). Showing first 10.")
        console.print()

        values = outlier_result.outlier_values[:10]
        indices = outlier_result.outlier_indices[:10]

        outlier_table = Table(show_header=True, box=box.SIMPLE)
        outlier_table.add_column("Index", style="cyan", justify="right")
        outlier_table.add_column("Value", style="red", justify="right")

        for idx, val in zip(indices, values):
            outlier_table.add_row(str(idx), f"{val:.4f}")

        console.print(outlier_table)


def display_group_comparison(
    comparison_result: Any,
    show_post_hoc: bool = False
):
    """Display group comparison results.

    Args:
        comparison_result: GroupComparisonResult from compare_groups()
        show_post_hoc: Whether to show post-hoc test results
    """
    group_col = comparison_result.group_col
    value_col = comparison_result.value_col

    print_section_header(f"Group Comparison: {value_col} by {group_col}")

    # Display group statistics
    group_stats = comparison_result.group_statistics

    stats_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    stats_table.add_column("Group", style="cyan")
    stats_table.add_column("Count", justify="right")
    stats_table.add_column("Mean", justify="right")
    stats_table.add_column("Median", justify="right")
    stats_table.add_column("Std", justify="right")
    stats_table.add_column("Min", justify="right")
    stats_table.add_column("Max", justify="right")

    for group_name, stats in group_stats.items():
        stats_table.add_row(
            group_name,
            f"{stats.count}",
            f"{stats.mean:.4f}",
            f"{stats.median:.4f}",
            f"{stats.std:.4f}",
            f"{stats.min:.4f}",
            f"{stats.max:.4f}"
        )

    console.print(stats_table)

    # Display test results
    test_result = comparison_result.test_result
    if test_result:
        console.print()

        test_table = Table(show_header=False, box=box.SIMPLE)
        test_table.add_column("", style="cyan")
        test_table.add_column("", style="white")

        test_table.add_row("Test", test_result.test_name)
        test_table.add_row("Statistic", f"{test_result.statistic:.4f}")
        test_table.add_row("p-value", f"{test_result.p_value:.4f}")

        if test_result.is_significant:
            test_table.add_row("Result", "[green]Significant difference[/green]")
        else:
            test_table.add_row("Result", "[yellow]No significant difference[/yellow]")

        if test_result.effect_size is not None:
            test_table.add_row("Effect Size", f"{test_result.effect_size:.4f}")
            test_table.add_row("Effect", test_result.effect_size_interpretation)

        test_table.add_row("Interpretation", test_result.interpretation)

        console.print(test_table)

    # Display variance test results
    variance_result = comparison_result.variance_test_result
    if variance_result:
        console.print()

        var_table = Table(show_header=False, box=box.SIMPLE)
        var_table.add_column("", style="cyan")
        var_table.add_column("", style="white")

        var_table.add_row("Variance Test", variance_result.test_name)
        var_table.add_row("Statistic", f"{variance_result.statistic:.4f}")
        var_table.add_row("p-value", f"{variance_result.p_value:.4f}")
        var_table.add_row("Result", variance_result.interpretation)

        console.print(var_table)


def display_progress(description: str, total: int = 100):
    """Create a progress bar context manager.

    Args:
        description: Progress description
        total: Total number of items

    Returns:
        Progress context manager
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    )


def display_panel(content: str, title: str = "", style: str = "blue"):
    """Display content in a panel.

    Args:
        content: Panel content
        title: Panel title
        style: Panel border style
    """
    console.print(Panel(content, title=title, border_style=style))


def display_columns(*contents: str, width: int = 50):
    """Display multiple columns side by side.

    Args:
        *contents: Column contents
        width: Width of each column
    """
    panels = [Panel(content, width=width) for content in contents]
    console.print(Columns(panels))


def create_table(title: str, columns: List[str], rows: List[List[str]]) -> Table:
    """Create a Rich table.

    Args:
        title: Table title
        columns: List of column headers
        rows: List of rows (each row is a list of cell values)

    Returns:
        Rich Table object
    """
    table = Table(title=title, show_header=True, header_style="bold magenta", box=box.ROUNDED)

    for col in columns:
        table.add_column(col, style="white")

    for row in rows:
        table.add_row(*row)

    return table


def format_number(value: float, precision: int = 4) -> str:
    """Format a number for terminal display.

    Args:
        value: Number to format
        precision: Decimal precision

    Returns:
        Formatted string
    """
    if pd.isna(value):
        return "—"

    if abs(value) >= 1_000_000:
        return f"{value:,.{precision}f}"
    elif abs(value) >= 1_000:
        return f"{value:,.{precision}f}"
    elif abs(value) >= 1:
        return f"{value:.{precision}f}"
    elif abs(value) >= 0.01 or value == 0:
        return f"{value:.{precision}f}"
    else:
        return f"{value:.{max(precision, 6)}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format a percentage.

    Args:
        value: Value to format (0-100 or 0-1)
        decimals: Decimal places

    Returns:
        Formatted percentage string
    """
    if pd.isna(value):
        return "—"

    # If value is less than 1, assume it's a proportion and convert to percentage
    if abs(value) < 1:
        value = value * 100

    return f"{value:.{decimals}}%"


def get_console() -> Console:
    """Get the global console instance.

    Returns:
        Rich Console object
    """
    return console


def set_console(new_console: Console):
    """Set a new global console instance.

    Args:
        new_console: New Console object to use
    """
    global console
    console = new_console

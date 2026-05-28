"""Plotly interactive chart generation module.

Creates publication-quality interactive charts for HTML reports.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# Default color scheme (color-blind friendly)
DEFAULT_COLORS = [
    '#1f77b4',  # blue
    '#ff7f0e',  # orange
    '#2ca02c',  # green
    '#d62728',  # red
    '#9467bd',  # purple
    '#8c564b',  # brown
    '#e377c2',  # pink
    '#7f7f7f',  # gray
    '#bcbd22',  # olive
    '#17becf',  # cyan
]


def create_histogram(
    series: pd.Series,
    title: str = "Distribution",
    color: str = DEFAULT_COLORS[0],
    bins: Optional[int] = None,
    show_density: bool = True,
    width: int = 800,
    height: int = 500
) -> go.Figure:
    """Create an interactive histogram with optional density curve.

    Args:
        series: pandas Series with numeric data
        title: Chart title
        color: Bar color
        bins: Number of bins (None for auto)
        show_density: Whether to add KDE curve
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    clean_series = series.dropna()
    name = series.name if series.name else "Value"

    if len(clean_series) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    # Auto-determine bins if not specified
    if bins is None:
        from core.distribution import optimal_bins
        bins = optimal_bins(clean_series, method='fd')

    # Create histogram
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=clean_series,
        name='Histogram',
        nbinsx=bins,
        marker_color=color,
        opacity=0.7,
        histnorm='probability density' if show_density else None
    ))

    # Add density curve if requested
    if show_density:
        from core.distribution import kde_data
        kde = kde_data(clean_series)

        if len(kde.x) > 0:
            # Scale KDE to match histogram
            fig.add_trace(go.Scatter(
                x=kde.x,
                y=kde.y,
                mode='lines',
                name='Density',
                line=dict(color='darkred', width=2),
                fill='tozeroy',
                fillcolor='rgba(220, 20, 60, 0.2)'
            ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=name,
        yaxis_title='Density' if show_density else 'Count',
        hovermode='x unified',
        width=width,
        height=height,
        template='plotly_white'
    )

    return fig


def create_boxplot(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: str = "value",
    title: str = "Box Plot",
    color: str = DEFAULT_COLORS[0],
    width: int = 800,
    height: int = 500
) -> go.Figure:
    """Create an interactive box plot.

    Args:
        df: Input DataFrame
        x_col: Column for grouping (optional)
        y_col: Column with values to plot
        title: Chart title
        color: Box color
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    if x_col:
        # Grouped box plot
        fig = px.box(
            df,
            x=x_col,
            y=y_col,
            title=title,
            color=x_col if df[x_col].nunique() <= len(DEFAULT_COLORS) else None,
            template='plotly_white'
        )
    else:
        # Single box plot
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=df[y_col].dropna(),
            name=y_col,
            marker_color=color,
            boxmean='sd'  # Show mean and standard deviation
        ))
        fig.update_layout(
            title=title,
            yaxis_title=y_col,
            template='plotly_white'
        )

    fig.update_layout(width=width, height=height)

    return fig


def create_violinplot(
    df: pd.DataFrame,
    x_col: Optional[str] = None,
    y_col: str = "value",
    title: str = "Violin Plot",
    width: int = 800,
    height: int = 500
) -> go.Figure:
    """Create an interactive violin plot.

    Shows full distribution shape combining box plot with density.

    Args:
        df: Input DataFrame
        x_col: Column for grouping (optional)
        y_col: Column with values to plot
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    if x_col:
        # Grouped violin plot
        fig = px.violin(
            df,
            x=x_col,
            y=y_col,
            title=title,
            color=x_col if df[x_col].nunique() <= len(DEFAULT_COLORS) else None,
            box=True,  # Show box plot inside violin
            template='plotly_white'
        )
    else:
        # Single violin plot
        fig = go.Figure()
        fig.add_trace(go.Violin(
            y=df[y_col].dropna(),
            name=y_col,
            box_visible=True,
            meanline_visible=True
        ))
        fig.update_layout(
            title=title,
            yaxis_title=y_col,
            template='plotly_white'
        )

    fig.update_layout(width=width, height=height)

    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    title: str = "Scatter Plot",
    trendline: Optional[str] = 'ols',
    width: int = 800,
    height: int = 600
) -> go.Figure:
    """Create an interactive scatter plot with optional trendline.

    Args:
        df: Input DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Column for color grouping (optional)
        title: Chart title
        trendline: 'ols' for linear regression, None for no trendline
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        trendline=trendline,
        template='plotly_white'
    )

    fig.update_layout(width=width, height=height)

    return fig


def create_correlation_heatmap(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'pearson',
    title: str = "Correlation Matrix",
    width: int = 800,
    height: int = 800,
    color_scale: str = 'RdBu_r'
) -> go.Figure:
    """Create an interactive correlation heatmap.

    Args:
        df: Input DataFrame
        columns: Columns to include (None for all numeric)
        method: Correlation method ('pearson', 'spearman', 'kendall')
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels
        color_scale: Color scale for heatmap

    Returns:
        Plotly Figure object
    """
    from core.data_loader import get_numeric_columns

    if columns is None:
        columns = get_numeric_columns(df)

    # Calculate correlation matrix
    corr_matrix = df[columns].corr(method=method)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale=color_scale,
        zmid=0,  # Center at 0
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title=title,
        width=width,
        height=height,
        template='plotly_white'
    )

    return fig


def create_pairplot(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    color_col: Optional[str] = None,
    max_cols: int = 6
) -> go.Figure:
    """Create a pair plot (scatter matrix).

    Shows pairwise relationships between multiple variables.

    Args:
        df: Input DataFrame
        columns: Columns to include (None for all numeric, max 6)
        color_col: Column for color grouping
        max_cols: Maximum number of columns to plot

    Returns:
        Plotly Figure object
    """
    from core.data_loader import get_numeric_columns

    if columns is None:
        columns = get_numeric_columns(df)

    # Limit number of columns
    if len(columns) > max_cols:
        columns = columns[:max_cols]

    # Create scatter matrix
    fig = px.scatter_matrix(
        df[columns + ([color_col] if color_col else [])],
        dimensions=columns,
        color=color_col,
        template='plotly_white'
    )

    fig.update_layout(
        title="Pair Plot",
        height=800
    )

    return fig


def create_qqplot(
    series: pd.Series,
    title: str = "Q-Q Plot",
    width: int = 600,
    height: int = 600
) -> go.Figure:
    """Create a Q-Q (quantile-quantile) plot for normality assessment.

    Compares data quantiles to theoretical normal distribution quantiles.

    Args:
        series: pandas Series with numeric data
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    from core.distribution import qqplot_data

    clean_series = series.dropna()
    name = series.name if series.name else "Value"

    if len(clean_series) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    # Get Q-Q plot data
    qq_data = qqplot_data(clean_series)

    # Create figure
    fig = go.Figure()

    # Add reference line
    fig.add_trace(go.Scatter(
        x=qq_data.theoretical,
        y=qq_data.intercept + qq_data.slope * qq_data.theoretical,
        mode='lines',
        name='Reference Line',
        line=dict(color='red', dash='dash')
    ))

    # Add data points
    fig.add_trace(go.Scatter(
        x=qq_data.theoretical,
        y=qq_data.actual,
        mode='markers',
        name='Data',
        marker=dict(color=DEFAULT_COLORS[0], size=6)
    ))

    # Update layout
    fig.update_layout(
        title=f"{title}<br><sub>R² = {qq_data.r_squared:.4f}</sub>",
        xaxis_title='Theoretical Quantiles',
        yaxis_title='Sample Quantiles',
        template='plotly_white',
        width=width,
        height=height
    )

    return fig


def create_distribution_comparison(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    plot_type: str = 'violin',
    title: str = "Distribution Comparison",
    width: int = 800,
    height: int = 500
) -> go.Figure:
    """Create distribution comparison across groups.

    Args:
        df: Input DataFrame
        group_col: Column for grouping
        value_col: Column with values to compare
        plot_type: 'violin', 'box', or 'histogram'
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    if plot_type == 'violin':
        return create_violinplot(df, group_col, value_col, title, width, height)
    elif plot_type == 'box':
        return create_boxplot(df, group_col, value_col, title, width=width, height=height)
    elif plot_type == 'histogram':
        # Overlay histograms for each group
        fig = go.Figure()

        for i, (group_name, group_data) in enumerate(df.groupby(group_col, observed=True)):
            color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            fig.add_trace(go.Histogram(
                x=group_data[value_col].dropna(),
                name=str(group_name),
                marker_color=color,
                opacity=0.6,
                histnorm='probability density'
            ))

        fig.update_layout(
            title=title,
            xaxis_title=value_col,
            yaxis_title='Density',
            barmode='overlay',
            template='plotly_white',
            width=width,
            height=height
        )

        return fig
    else:
        raise ValueError(f"Unknown plot_type: {plot_type}")


def create_outlier_plot(
    series: pd.Series,
    outlier_indices: np.ndarray,
    title: str = "Outlier Detection",
    width: int = 800,
    height: int = 400
) -> go.Figure:
    """Create a plot highlighting outliers.

    Args:
        series: pandas Series with numeric data
        outlier_indices: Indices of outlier values
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    clean_series = series.dropna()
    name = series.name if series.name else "Value"

    if len(clean_series) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    # Create colors: red for outliers, blue for normal
    colors = ['red' if i in outlier_indices else DEFAULT_COLORS[0]
              for i in clean_series.index]

    # Create scatter plot
    fig = go.Figure()

    # Add normal points
    normal_mask = ~clean_series.index.isin(outlier_indices)
    if normal_mask.any():
        fig.add_trace(go.Scatter(
            x=clean_series[normal_mask].index,
            y=clean_series[normal_mask],
            mode='markers',
            name='Normal',
            marker=dict(color=DEFAULT_COLORS[0], size=8),
            hovertemplate=f'Index: {{x}}<br>{name}: {{y}}<extra></extra>'
        ))

    # Add outlier points
    if len(outlier_indices) > 0:
        outliers = clean_series.loc[outlier_indices]
        fig.add_trace(go.Scatter(
            x=outliers.index,
            y=outliers.values,
            mode='markers',
            name='Outlier',
            marker=dict(color='red', size=12, line=dict(color='darkred', width=2)),
            hovertemplate=f'Index: {{x}}<br>{name}: {{y}}<extra></extra>'
        ))

    # Add reference line (mean)
    mean_val = clean_series.mean()
    fig.add_hline(
        y=mean_val,
        line_dash='dash',
        line_color='gray',
        annotation_text=f'Mean: {mean_val:.2f}'
    )

    fig.update_layout(
        title=title,
        xaxis_title='Index',
        yaxis_title=name,
        template='plotly_white',
        width=width,
        height=height,
        hovermode='x unified'
    )

    return fig


def create_statistics_summary_chart(
    stats_dict: Dict[str, Dict],
    title: str = "Statistics Summary",
    width: int = 1000,
    height: int = 600
) -> go.Figure:
    """Create a bar chart comparing statistics across multiple columns.

    Args:
        stats_dict: Dictionary mapping column names to their statistics
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    metrics = ['mean', 'median', 'std', 'min', 'max']
    metric_labels = ['Mean', 'Median', 'Std', 'Min', 'Max']

    for metric, label in zip(metrics, metric_labels):
        values = [stats_dict.get(col, {}).get(metric, 0) for col in stats_dict.keys()]

        fig.add_trace(go.Bar(
            name=label,
            x=list(stats_dict.keys()),
            y=values,
        ))

    fig.update_layout(
        title=title,
        xaxis_title='Column',
        yaxis_title='Value',
        barmode='group',
        template='plotly_white',
        width=width,
        height=height,
        hovermode='x unified'
    )

    return fig


def create_time_series_plot(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str = "Time Series",
    width: int = 1000,
    height: int = 500
) -> go.Figure:
    """Create a time series plot.

    Args:
        df: Input DataFrame
        date_col: Column with dates
        value_col: Column with values to plot
        title: Chart title
        width: Chart width in pixels
        height: Chart height in pixels

    Returns:
        Plotly Figure object
    """
    # Ensure date column is datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df[value_col],
        mode='lines+markers',
        name=value_col,
        line=dict(color=DEFAULT_COLORS[0]),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=value_col,
        template='plotly_white',
        width=width,
        height=height,
        hovermode='x unified'
    )

    return fig


def figure_to_html(fig: go.Figure, include_plotlyjs: bool = True) -> str:
    """Convert Plotly figure to HTML string.

    Args:
        fig: Plotly Figure object
        include_plotlyjs: Whether to include Plotly.js library

    Returns:
        HTML string
    """
    return fig.to_html(
        include_plotlyjs=include_plotlyjs,
        config={'displayModeBar': True, 'displaylogo': False}
    )


def save_figure(fig: go.Figure, filepath: str, scale: float = 1.0):
    """Save Plotly figure to file.

    Args:
        fig: Plotly Figure object
        filepath: Output file path (.png, .jpg, .svg, .pdf, .html)
        scale: Scale factor for resolution (higher = better quality)
    """
    if filepath.endswith('.html'):
        fig.write_html(filepath)
    elif filepath.endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        fig.write_image(filepath, scale=scale)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")

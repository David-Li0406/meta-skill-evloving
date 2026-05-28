"""Matplotlib static chart generation module.

Creates publication-quality static charts (PNG) for HTML reports.
Charts are returned as base64-encoded strings for direct embedding.
"""

from typing import Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import io
import base64

# Configure Chinese font support
def setup_chinese_font():
    """Configure Chinese font support for matplotlib."""
    plt.rcParams['font.sans-serif'] = [
        'SimHei',           # Windows黑体
        'Microsoft YaHei',  # Windows微软雅黑
        'PingFang SC',      # macOS苹方
        'Arial Unicode MS', # macOS通用
        'DejaVu Sans'       # Linux后备
    ]
    plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 150
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['font.size'] = 10

# Initialize font setup
setup_chinese_font()

# Default color scheme (color-blind friendly, matches Plotly)
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


def figure_to_base64(fig: plt.Figure) -> str:
    """Convert matplotlib figure to base64-encoded PNG string.

    Args:
        fig: matplotlib Figure object

    Returns:
        Base64-encoded PNG string
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    buffer.close()
    return image_base64


def create_histogram(
    series: pd.Series,
    title: str = "分布图",
    color: str = DEFAULT_COLORS[0],
    bins: Optional[int] = None,
    show_density: bool = True,
    figsize: Tuple[int, int] = (10, 6)
) -> str:
    """Create a histogram with optional density curve.

    Args:
        series: pandas Series with numeric data
        title: Chart title
        color: Bar color
        bins: Number of bins (None for auto)
        show_density: Whether to add KDE curve
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    clean_series = series.dropna()
    name = series.name if series.name else "数值"

    if len(clean_series) == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        return figure_to_base64(fig)

    # Auto-determine bins if not specified
    if bins is None:
        bins = min(30, int(np.sqrt(len(clean_series))))

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot histogram
    n, bins_edges, patches = ax.hist(clean_series, bins=bins, color=color,
                                       alpha=0.7, edgecolor='black', linewidth=0.5)

    # Add density curve if requested
    if show_density and len(clean_series) > 3:
        from scipy.stats import gaussian_kde
        try:
            kde = gaussian_kde(clean_series)
            x_range = np.linspace(clean_series.min(), clean_series.max(), 200)
            kde_values = kde(x_range)

            # Scale KDE to match histogram
            bin_width = bins_edges[1] - bins_edges[0]
            scale = len(clean_series) * bin_width
            ax.plot(x_range, kde_values * scale, color='darkred', linewidth=2, label='密度曲线')
            ax.fill_between(x_range, kde_values * scale, color='darkred', alpha=0.2)
            ax.legend()
        except:
            pass  # Skip KDE if it fails

    # Add mean and median lines
    mean_val = clean_series.mean()
    median_val = clean_series.median()
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'均值={mean_val:.1f}')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'中位数={median_val:.1f}')

    # Styling
    ax.set_xlabel(name, fontsize=11)
    ax.set_ylabel('频数', fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)

    plt.tight_layout()
    return figure_to_base64(fig)


def create_boxplot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "箱线图",
    figsize: Tuple[int, int] = (10, 6)
) -> str:
    """Create a boxplot for grouped data.

    Args:
        df: DataFrame with data
        x_col: Column name for grouping (categorical)
        y_col: Column name for values (numeric)
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Get unique groups
    groups = df[x_col].unique()
    data_to_plot = [df[df[x_col] == group][y_col].dropna() for group in groups]

    # Create boxplot
    bp = ax.boxplot(data_to_plot, labels=groups, patch_artist=True,
                    medianprops=dict(color='red', linewidth=2),
                    boxprops=dict(facecolor='lightblue', alpha=0.7),
                    whiskerprops=dict(linewidth=1.5),
                    capprops=dict(linewidth=1.5),
                    flierprops=dict(marker='o', markersize=5, alpha=0.5))

    # Add mean markers
    means = [d.mean() for d in data_to_plot]
    ax.plot(range(1, len(groups) + 1), means, 'g^', markersize=10,
            label='均值', zorder=5)

    # Styling
    ax.set_ylabel(y_col, fontsize=11)
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    return figure_to_base64(fig)


def create_qqplot(
    series: pd.Series,
    title: str = "Q-Q图",
    figsize: Tuple[int, int] = (8, 6)
) -> str:
    """Create a Q-Q plot for normality assessment.

    Args:
        series: pandas Series with numeric data
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    clean_series = series.dropna()

    fig, ax = plt.subplots(figsize=figsize)

    if len(clean_series) < 3:
        ax.text(0.5, 0.5, '数据量不足，无法绘制Q-Q图', ha='center', va='center', fontsize=12)
        ax.axis('off')
        return figure_to_base64(fig)

    # Create Q-Q plot
    stats.probplot(clean_series, dist="norm", plot=ax)

    # Styling
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return figure_to_base64(fig)


def create_outlier_plot(
    series: pd.Series,
    outlier_indices: list,
    title: str = "异常值检测图",
    figsize: Tuple[int, int] = (12, 5)
) -> str:
    """Create a visualization showing outliers.

    Args:
        series: pandas Series with numeric data
        outlier_indices: List of indices identified as outliers
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    clean_series = series.dropna()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Plot 1: Scatter plot with outliers highlighted
    x = range(len(clean_series))
    colors = ['red' if i in outlier_indices else DEFAULT_COLORS[0] for i in x]

    ax1.scatter(x, clean_series, c=colors, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    ax1.set_xlabel('索引', fontsize=10)
    ax1.set_ylabel('数值', fontsize=10)
    ax1.set_title('异常值分布', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Boxplot
    bp = ax2.boxplot(clean_series, vert=True, patch_artist=True,
                     medianprops=dict(color='red', linewidth=2),
                     boxprops=dict(facecolor='lightblue', alpha=0.7))

    # Highlight outliers
    if len(outlier_indices) > 0:
        outlier_values = clean_series.iloc[outlier_indices]
        ax2.plot([1] * len(outlier_values), outlier_values, 'r*', markersize=15,
                label=f'异常值 ({len(outlier_indices)}个)', zorder=5)
        ax2.legend()

    ax2.set_ylabel('数值', fontsize=10)
    ax2.set_title('箱线图', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks([])

    fig.suptitle(title, fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    return figure_to_base64(fig)


def create_distribution_comparison(
    series_dict: dict,
    title: str = "分布对比",
    figsize: Tuple[int, int] = (12, 5)
) -> str:
    """Create side-by-side histograms for multiple series.

    Args:
        series_dict: Dictionary {name: pd.Series}
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    n_series = len(series_dict)
    if n_series == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', fontsize=14)
        ax.axis('off')
        return figure_to_base64(fig)

    fig, axes = plt.subplots(1, n_series, figsize=figsize)

    if n_series == 1:
        axes = [axes]

    for ax, (name, series) in zip(axes, series_dict.items()):
        clean_series = series.dropna()

        if len(clean_series) == 0:
            ax.text(0.5, 0.5, '无数据', ha='center', va='center', fontsize=12)
            ax.axis('off')
            continue

        color = DEFAULT_COLORS[list(series_dict.keys()).index(name) % len(DEFAULT_COLORS)]
        bins = min(30, int(np.sqrt(len(clean_series))))

        ax.hist(clean_series, bins=bins, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)

        # Add mean line
        mean_val = clean_series.mean()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'均值={mean_val:.1f}')

        ax.set_xlabel('数值', fontsize=10)
        ax.set_ylabel('频数', fontsize=10)
        ax.set_title(name, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    return figure_to_base64(fig)


def create_correlation_heatmap(
    df: pd.DataFrame,
    columns: Optional[list] = None,
    title: str = "相关性热力图",
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """Create a correlation heatmap.

    Args:
        df: DataFrame with numeric data
        columns: List of columns to include (None for all numeric)
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    if columns:
        df = df[columns].copy()

    # Only include numeric columns
    df_numeric = df.select_dtypes(include=[np.number])

    if df_numeric.shape[1] < 2:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, '需要至少2个数值列', ha='center', va='center', fontsize=14)
        ax.axis('off')
        return figure_to_base64(fig)

    # Calculate correlation
    corr = df_numeric.corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('相关系数', rotation=270, labelpad=20)

    # Set ticks and labels
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr.columns)

    # Add correlation values
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)

    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    return figure_to_base64(fig)


def create_statistics_summary(
    stats_dict: dict,
    title: str = "统计摘要",
    figsize: Tuple[int, int] = (12, 6)
) -> str:
    """Create a visual summary of statistics.

    Args:
        stats_dict: Dictionary with statistics for each column
        title: Chart title
        figsize: Figure size (width, height) in inches

    Returns:
        Base64-encoded PNG string
    """
    # This is a placeholder for more complex visual summaries
    # For now, we'll return a simple table visualization
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')
    ax.axis('tight')

    # Prepare data for table
    columns = list(stats_dict.keys())
    if not columns:
        ax.text(0.5, 0.5, '无统计数据', ha='center', va='center', fontsize=14)
        return figure_to_base64(fig)

    metrics = ['mean', 'median', 'std', 'min', 'max']
    metric_names = ['均值', '中位数', '标准差', '最小值', '最大值']

    table_data = []
    for metric, metric_name in zip(metrics, metric_names):
        row = [metric_name]
        for col in columns:
            row.append(f"{stats_dict[col].get(metric, 0):.2f}")
        table_data.append(row)

    table = ax.table(cellText=table_data, rowLabels=[''] * len(metrics),
                     colLabels=['指标'] + columns, cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Style header row
    for i in range(len(columns) + 1):
        table[(0, i)].set_facecolor('#667eea')
        table[(0, i)].set_text_props(weight='bold', color='white')

    ax.set_title(title, fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    return figure_to_base64(fig)

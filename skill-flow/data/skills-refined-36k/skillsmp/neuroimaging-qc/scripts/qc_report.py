#!/usr/bin/env python3
"""
Generate QC reports with visualizations for neuroimaging data.

Usage:
    python qc_report.py mriqc_bold.tsv --type bold -o qc_report
    python qc_report.py qc_summary.csv --type custom --metrics fd_mean,tsnr -o report
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path

# Try to import matplotlib, but don't fail if not available
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("Warning: matplotlib not available, skipping plots")


def plot_qc_distributions(df: pd.DataFrame, metrics: list, thresholds: dict = None, 
                          output_path: Path = None):
    """
    Plot QC metric distributions with optional threshold lines.
    
    Parameters
    ----------
    df : pd.DataFrame
        QC data
    metrics : list
        Metrics to plot
    thresholds : dict
        Optional {metric: (value, direction)} where direction is 'above' or 'below'
    output_path : Path
        Optional output path for saving figure
    """
    if not HAS_MPL:
        return None
    
    n_metrics = len(metrics)
    n_cols = min(2, n_metrics)
    n_rows = (n_metrics + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 4*n_rows))
    if n_metrics == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        if metric not in df.columns:
            continue
        
        ax = axes[i]
        data = df[metric].dropna()
        
        ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
        ax.set_xlabel(metric)
        ax.set_ylabel('Count')
        ax.set_title(f'{metric} Distribution (n={len(data)})')
        
        # Add threshold line if provided
        if thresholds and metric in thresholds:
            thresh_val, direction = thresholds[metric]
            color = 'red'
            ax.axvline(thresh_val, color=color, linestyle='--', linewidth=2,
                      label=f'Threshold: {thresh_val}')
            ax.legend()
        
        # Add mean line
        ax.axvline(data.mean(), color='blue', linestyle='-', alpha=0.5,
                  label=f'Mean: {data.mean():.3f}')
    
    # Hide unused axes
    for j in range(i+1, len(axes)):
        axes[j].set_visible(False)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    
    return fig


def plot_qc_scatter(df: pd.DataFrame, x_metric: str, y_metric: str, 
                    color_by: str = None, output_path: Path = None):
    """Plot scatter of two QC metrics."""
    if not HAS_MPL:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if color_by and color_by in df.columns:
        scatter = ax.scatter(df[x_metric], df[y_metric], c=df[color_by], 
                            cmap='coolwarm', alpha=0.6)
        plt.colorbar(scatter, label=color_by)
    else:
        ax.scatter(df[x_metric], df[y_metric], alpha=0.6)
    
    ax.set_xlabel(x_metric)
    ax.set_ylabel(y_metric)
    ax.set_title(f'{x_metric} vs {y_metric}')
    
    # Add correlation
    valid = df[[x_metric, y_metric]].dropna()
    if len(valid) > 2:
        r = valid[x_metric].corr(valid[y_metric])
        ax.text(0.05, 0.95, f'r = {r:.3f}', transform=ax.transAxes, 
               fontsize=12, verticalalignment='top')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    
    return fig


def generate_text_report(df: pd.DataFrame, metrics: list, exclusion_col: str = 'exclude') -> str:
    """Generate text summary report."""
    report = []
    report.append("=" * 60)
    report.append("NEUROIMAGING QC REPORT")
    report.append("=" * 60)
    report.append("")
    
    # Sample summary
    n_total = len(df)
    report.append(f"Total subjects/runs: {n_total}")
    
    if exclusion_col in df.columns:
        n_exclude = df[exclusion_col].sum()
        report.append(f"Excluded: {n_exclude} ({100*n_exclude/n_total:.1f}%)")
        report.append(f"Included: {n_total - n_exclude}")
    
    report.append("")
    report.append("-" * 40)
    report.append("METRIC STATISTICS")
    report.append("-" * 40)
    
    for metric in metrics:
        if metric not in df.columns:
            continue
        
        data = df[metric].dropna()
        report.append(f"\n{metric}:")
        report.append(f"  N:      {len(data)}")
        report.append(f"  Mean:   {data.mean():.4f}")
        report.append(f"  Std:    {data.std():.4f}")
        report.append(f"  Median: {data.median():.4f}")
        report.append(f"  Min:    {data.min():.4f}")
        report.append(f"  Max:    {data.max():.4f}")
        report.append(f"  IQR:    [{data.quantile(0.25):.4f}, {data.quantile(0.75):.4f}]")
    
    return "\n".join(report)


def generate_html_report(df: pd.DataFrame, metrics: list, title: str = "QC Report",
                        output_path: Path = None) -> str:
    """Generate HTML report with embedded statistics."""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .excluded {{ background-color: #ffcccc; }}
        .metric-summary {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Generated from {len(df)} subjects/runs</p>
"""
    
    # Summary statistics
    html += "<h2>Metric Summary</h2>"
    html += "<table><tr><th>Metric</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th></tr>"
    
    for metric in metrics:
        if metric not in df.columns:
            continue
        data = df[metric].dropna()
        html += f"""
        <tr>
            <td>{metric}</td>
            <td>{data.mean():.4f}</td>
            <td>{data.std():.4f}</td>
            <td>{data.min():.4f}</td>
            <td>{data.max():.4f}</td>
        </tr>
        """
    
    html += "</table>"
    
    # Subject table
    html += "<h2>Subject Details</h2>"
    html += "<table><tr>"
    
    display_cols = ['bids_name'] + [m for m in metrics if m in df.columns]
    if 'exclude' in df.columns:
        display_cols.append('exclude')
    
    for col in display_cols:
        html += f"<th>{col}</th>"
    html += "</tr>"
    
    for _, row in df.iterrows():
        row_class = 'excluded' if row.get('exclude', False) else ''
        html += f"<tr class='{row_class}'>"
        for col in display_cols:
            val = row.get(col, '')
            if isinstance(val, float):
                val = f"{val:.4f}"
            html += f"<td>{val}</td>"
        html += "</tr>"
    
    html += "</table></body></html>"
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"Saved HTML report to {output_path}")
    
    return html


def main():
    parser = argparse.ArgumentParser(description='Generate QC reports')
    parser.add_argument('input', help='Input CSV/TSV file')
    parser.add_argument('--type', choices=['bold', 'anat', 'custom'], default='custom')
    parser.add_argument('--metrics', help='Comma-separated metrics to analyze')
    parser.add_argument('-o', '--output', help='Output prefix for reports')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--no-plots', action='store_true', help='Skip plot generation')
    
    args = parser.parse_args()
    
    # Load data
    sep = '\t' if args.input.endswith('.tsv') else ','
    df = pd.read_csv(args.input, sep=sep)
    
    # Determine metrics
    if args.metrics:
        metrics = args.metrics.split(',')
    elif args.type == 'bold':
        metrics = ['fd_mean', 'fd_perc', 'tsnr', 'dvars_std']
    elif args.type == 'anat':
        metrics = ['qi_1', 'cnr', 'cjv', 'snr_gm', 'efc']
    else:
        # Auto-detect numeric columns
        metrics = [c for c in df.columns if df[c].dtype in ['float64', 'int64']][:6]
    
    # Filter to existing metrics
    metrics = [m for m in metrics if m in df.columns]
    
    # Generate text report
    report = generate_text_report(df, metrics)
    print(report)
    
    output_prefix = args.output or 'qc_report'
    
    # Save text report
    with open(f"{output_prefix}.txt", 'w') as f:
        f.write(report)
    print(f"\nSaved text report to {output_prefix}.txt")
    
    # Generate HTML if requested
    if args.html:
        generate_html_report(df, metrics, output_path=Path(f"{output_prefix}.html"))
    
    # Generate plots
    if not args.no_plots and HAS_MPL:
        plot_qc_distributions(df, metrics, output_path=Path(f"{output_prefix}_distributions.png"))
        
        # Create fd_mean vs tsnr scatter if both exist
        if 'fd_mean' in df.columns and 'tsnr' in df.columns:
            plot_qc_scatter(df, 'fd_mean', 'tsnr', 
                          color_by='exclude' if 'exclude' in df.columns else None,
                          output_path=Path(f"{output_prefix}_scatter.png"))


if __name__ == '__main__':
    main()

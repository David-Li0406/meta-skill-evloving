#!/usr/bin/env python3
"""
Parse MRIQC group outputs and flag subjects for exclusion.

Usage:
    python parse_mriqc.py group_bold.tsv --fd-thresh 0.3 --fd-perc-thresh 30 -o qc.csv
    python parse_mriqc.py group_T1w.tsv --type anat -o qc.csv
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def load_mriqc_group(tsv_path: str) -> pd.DataFrame:
    """Load MRIQC group TSV file."""
    return pd.read_csv(tsv_path, sep='\t')


def flag_bold_subjects(df, fd_mean_thresh=0.3, fd_perc_thresh=30, tsnr_zscore=-2):
    """Flag BOLD subjects for exclusion."""
    results = df[['bids_name']].copy()
    
    results['fd_mean'] = df['fd_mean']
    results['flag_fd_mean'] = df['fd_mean'] > fd_mean_thresh
    
    results['fd_perc'] = df['fd_perc']
    results['flag_fd_perc'] = df['fd_perc'] > fd_perc_thresh
    
    results['tsnr'] = df['tsnr']
    tsnr_z = (df['tsnr'] - df['tsnr'].mean()) / df['tsnr'].std()
    results['flag_low_tsnr'] = tsnr_z < tsnr_zscore
    
    flag_cols = [c for c in results.columns if c.startswith('flag_')]
    results['exclude'] = results[flag_cols].any(axis=1)
    
    return results


def flag_anat_subjects(df, zscore_thresh=3):
    """Flag anatomical subjects for exclusion using z-score outlier detection."""
    results = df[['bids_name']].copy()
    
    higher_worse = ['qi_1', 'cjv', 'efc']
    lower_worse = ['cnr', 'snr_gm', 'snr_wm']
    
    for metric in higher_worse:
        if metric in df.columns:
            results[metric] = df[metric]
            z = (df[metric] - df[metric].mean()) / df[metric].std()
            results[f'flag_{metric}'] = z > zscore_thresh
    
    for metric in lower_worse:
        if metric in df.columns:
            results[metric] = df[metric]
            z = (df[metric] - df[metric].mean()) / df[metric].std()
            results[f'flag_{metric}'] = z < -zscore_thresh
    
    flag_cols = [c for c in results.columns if c.startswith('flag_')]
    results['exclude'] = results[flag_cols].any(axis=1)
    
    return results


def generate_summary(results, modality):
    """Generate text summary of QC results."""
    n_total = len(results)
    n_exclude = results['exclude'].sum()
    
    summary = f"""
MRIQC QC Summary ({modality.upper()})
{'=' * 40}
Total subjects: {n_total}
Excluded: {n_exclude} ({100*n_exclude/n_total:.1f}%)
Included: {n_total - n_exclude}
"""
    
    flag_cols = [c for c in results.columns if c.startswith('flag_')]
    summary += "\nExclusion breakdown:\n"
    for col in flag_cols:
        n = results[col].sum()
        summary += f"  {col}: {n}\n"
    
    return summary


def main():
    parser = argparse.ArgumentParser(description='Parse MRIQC outputs for QC')
    parser.add_argument('input', help='MRIQC group TSV file')
    parser.add_argument('--type', choices=['bold', 'anat'], default='bold')
    parser.add_argument('--fd-thresh', type=float, default=0.3)
    parser.add_argument('--fd-perc-thresh', type=float, default=30)
    parser.add_argument('--zscore-thresh', type=float, default=3)
    parser.add_argument('-o', '--output', help='Output CSV path')
    
    args = parser.parse_args()
    
    df = load_mriqc_group(args.input)
    
    if args.type == 'bold':
        results = flag_bold_subjects(df, args.fd_thresh, args.fd_perc_thresh)
    else:
        results = flag_anat_subjects(df, args.zscore_thresh)
    
    print(generate_summary(results, args.type))
    
    if args.output:
        results.to_csv(args.output, index=False)
        print(f"\nResults saved to {args.output}")


if __name__ == '__main__':
    main()

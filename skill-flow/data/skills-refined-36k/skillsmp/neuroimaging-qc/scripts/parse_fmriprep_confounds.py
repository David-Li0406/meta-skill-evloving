#!/usr/bin/env python3
"""
Parse fMRIPrep confounds and generate subject-level QC summaries.

Usage:
    python parse_fmriprep_confounds.py /path/to/fmriprep/output --fd-thresh 0.5 -o qc.csv
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import json


def find_confounds_files(fmriprep_dir: Path) -> list:
    """Find all confounds TSV files in fMRIPrep output."""
    return list(fmriprep_dir.rglob('*_desc-confounds_timeseries.tsv'))


def summarize_confounds(confounds_path: Path, fd_thresh: float = 0.5) -> dict:
    """
    Summarize a single confounds file.
    
    Parameters
    ----------
    confounds_path : Path
        Path to confounds TSV
    fd_thresh : float
        FD threshold for counting high-motion volumes
    
    Returns
    -------
    dict
        Summary statistics
    """
    df = pd.read_csv(confounds_path, sep='\t')
    
    # Parse BIDS entities from filename
    name = confounds_path.stem.replace('_desc-confounds_timeseries', '')
    
    result = {'bids_name': name, 'confounds_file': str(confounds_path)}
    
    # FD statistics
    if 'framewise_displacement' in df.columns:
        fd = df['framewise_displacement'].dropna()
        result['fd_mean'] = fd.mean()
        result['fd_max'] = fd.max()
        result['fd_std'] = fd.std()
        result['n_high_fd'] = (fd > fd_thresh).sum()
        result['fd_perc'] = 100 * result['n_high_fd'] / len(fd)
    
    # DVARS statistics
    if 'std_dvars' in df.columns:
        dvars = df['std_dvars'].dropna()
        result['dvars_mean'] = dvars.mean()
        result['dvars_max'] = dvars.max()
    
    # Count motion outliers if present
    outlier_cols = [c for c in df.columns if c.startswith('motion_outlier')]
    if outlier_cols:
        result['n_motion_outliers'] = df[outlier_cols].sum().sum()
    
    # Non-steady state volumes
    nss_cols = [c for c in df.columns if c.startswith('non_steady_state')]
    result['n_non_steady_state'] = len(nss_cols)
    
    # Total volumes
    result['n_volumes'] = len(df)
    
    return result


def process_fmriprep_dir(fmriprep_dir: Path, fd_thresh: float = 0.5) -> pd.DataFrame:
    """Process all subjects in fMRIPrep output directory."""
    confounds_files = find_confounds_files(fmriprep_dir)
    
    if not confounds_files:
        raise FileNotFoundError(f"No confounds files found in {fmriprep_dir}")
    
    summaries = []
    for cf in confounds_files:
        try:
            summary = summarize_confounds(cf, fd_thresh)
            summaries.append(summary)
        except Exception as e:
            print(f"Error processing {cf}: {e}")
    
    return pd.DataFrame(summaries)


def flag_subjects(df: pd.DataFrame, fd_mean_thresh: float, fd_perc_thresh: float) -> pd.DataFrame:
    """Add exclusion flags to summary DataFrame."""
    df = df.copy()
    
    df['flag_fd_mean'] = df['fd_mean'] > fd_mean_thresh
    df['flag_fd_perc'] = df['fd_perc'] > fd_perc_thresh
    
    df['exclude'] = df['flag_fd_mean'] | df['flag_fd_perc']
    
    return df


def generate_report(df: pd.DataFrame, fd_mean_thresh: float, fd_perc_thresh: float) -> str:
    """Generate text report."""
    n_total = len(df)
    n_exclude = df['exclude'].sum() if 'exclude' in df.columns else 0
    
    report = f"""
fMRIPrep Confounds QC Summary
=============================
Total runs: {n_total}
Thresholds: fd_mean < {fd_mean_thresh}mm, fd_perc < {fd_perc_thresh}%

Exclusions: {n_exclude} ({100*n_exclude/n_total:.1f}%)

FD Statistics (all runs):
  Mean: {df['fd_mean'].mean():.3f} mm
  Std:  {df['fd_mean'].std():.3f} mm
  Range: [{df['fd_mean'].min():.3f}, {df['fd_mean'].max():.3f}]

High-motion volume % (all runs):
  Mean: {df['fd_perc'].mean():.1f}%
  Max:  {df['fd_perc'].max():.1f}%
"""
    return report


def main():
    parser = argparse.ArgumentParser(description='Parse fMRIPrep confounds for QC')
    parser.add_argument('fmriprep_dir', help='fMRIPrep output directory')
    parser.add_argument('--fd-thresh', type=float, default=0.5, help='FD threshold (mm)')
    parser.add_argument('--fd-mean-thresh', type=float, default=0.3, help='Max mean FD')
    parser.add_argument('--fd-perc-thresh', type=float, default=30, help='Max FD %')
    parser.add_argument('-o', '--output', help='Output CSV path')
    
    args = parser.parse_args()
    
    fmriprep_dir = Path(args.fmriprep_dir)
    
    print(f"Processing {fmriprep_dir}...")
    df = process_fmriprep_dir(fmriprep_dir, args.fd_thresh)
    df = flag_subjects(df, args.fd_mean_thresh, args.fd_perc_thresh)
    
    print(generate_report(df, args.fd_mean_thresh, args.fd_perc_thresh))
    
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")


if __name__ == '__main__':
    main()

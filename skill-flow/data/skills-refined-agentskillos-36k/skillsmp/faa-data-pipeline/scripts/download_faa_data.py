#!/usr/bin/env python3
"""
Download FAA aviation data files for a specified AIRAC cycle.

Supports downloading:
- NASR 28-day subscription (airports, runways, navaids, fixes, airways, frequencies)
- CIFP (coded instrument flight procedures)
- d-TPP (digital terminal procedures publication)
- DOF (digital obstacle file)

Usage:
    python download_faa_data.py --cycle 2513 --output ./faa_raw/
    python download_faa_data.py --cycle current --output ./faa_raw/
    python download_faa_data.py --type dof --output ./faa_raw/
"""

import argparse
import os
import sys
import urllib.request
import zipfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path


# AIRAC epoch: January 4, 2024 (cycle 2401)
AIRAC_EPOCH = datetime(2024, 1, 4)
AIRAC_CYCLE_DAYS = 28

# FAA Data URLs
FAA_URLS = {
    'nasr': 'https://nfdc.faa.gov/webContent/28DaySub/28DaySubscription_Effective_{date}.zip',
    'cifp': 'https://aeronav.faa.gov/Upload_313-d/cifp/CIFP_{cycle}.zip',
    'dtpp': 'https://aeronav.faa.gov/d-tpp/{cycle}/xml_data/d-TPP_Metafile.xml',
    'dtpp_charts': 'https://aeronav.faa.gov/d-tpp/{cycle}/',
    'dof': 'https://aeronav.faa.gov/Obst_Data/DAILY_DOF_DAT.ZIP',
}


def calculate_airac_cycle(target_date: datetime = None) -> tuple[str, datetime]:
    """
    Calculate the AIRAC cycle identifier and effective date for a given date.

    Returns:
        tuple: (cycle_id, effective_date) e.g., ('2513', datetime(2025, 12, 25))
    """
    if target_date is None:
        target_date = datetime.now()

    days_since_epoch = (target_date - AIRAC_EPOCH).days
    cycle_number = days_since_epoch // AIRAC_CYCLE_DAYS

    effective_date = AIRAC_EPOCH + timedelta(days=cycle_number * AIRAC_CYCLE_DAYS)

    year = effective_date.year
    year_start = datetime(year, 1, 1)
    days_into_year = (effective_date - year_start).days
    cycle_in_year = (days_into_year // AIRAC_CYCLE_DAYS) + 1

    cycle_id = f"{year % 100:02d}{cycle_in_year:02d}"

    return cycle_id, effective_date


def get_cycle_effective_date(cycle: str) -> datetime:
    """
    Get the effective date for a given AIRAC cycle identifier.

    Args:
        cycle: AIRAC cycle ID (e.g., '2513')

    Returns:
        datetime: Effective date of the cycle
    """
    year = 2000 + int(cycle[:2])
    cycle_num = int(cycle[2:])

    year_start = datetime(year, 1, 1)

    # Find first cycle of the year
    days_to_first_cycle = (AIRAC_EPOCH - datetime(2024, 1, 1)).days % AIRAC_CYCLE_DAYS
    first_cycle_date = year_start + timedelta(days=days_to_first_cycle)

    # Adjust if first cycle is before year start
    if first_cycle_date < year_start:
        first_cycle_date += timedelta(days=AIRAC_CYCLE_DAYS)

    # Calculate target cycle date
    effective_date = first_cycle_date + timedelta(days=(cycle_num - 1) * AIRAC_CYCLE_DAYS)

    return effective_date


def download_file(url: str, output_path: Path, description: str = "") -> bool:
    """
    Download a file from URL with progress reporting.

    Args:
        url: Source URL
        output_path: Destination file path
        description: Description for progress display

    Returns:
        bool: True if download successful
    """
    try:
        print(f"Downloading {description or url}...")

        # Create request with headers
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'MagentaLine-EFB/1.0')

        with urllib.request.urlopen(request, timeout=300) as response:
            total_size = response.headers.get('Content-Length')
            if total_size:
                total_size = int(total_size)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                downloaded = 0
                block_size = 8192

                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break

                    downloaded += len(buffer)
                    f.write(buffer)

                    if total_size:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Progress: {percent:.1f}% ({downloaded:,} / {total_size:,} bytes)", end='')

                print()

        print(f"  Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"  Error downloading: {e}")
        return False


def extract_zip(zip_path: Path, output_dir: Path) -> bool:
    """
    Extract a ZIP file to the specified directory.

    Args:
        zip_path: Path to ZIP file
        output_dir: Destination directory

    Returns:
        bool: True if extraction successful
    """
    try:
        print(f"Extracting {zip_path.name}...")

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(output_dir)

        print(f"  Extracted to: {output_dir}")
        return True

    except Exception as e:
        print(f"  Error extracting: {e}")
        return False


def download_nasr(cycle: str, output_dir: Path) -> bool:
    """Download NASR 28-day subscription data."""
    effective_date = get_cycle_effective_date(cycle)
    date_str = effective_date.strftime('%Y-%m-%d')

    url = FAA_URLS['nasr'].format(date=date_str)
    zip_path = output_dir / f'nasr_{cycle}.zip'

    if download_file(url, zip_path, f"NASR {cycle}"):
        return extract_zip(zip_path, output_dir)

    return False


def download_cifp(cycle: str, output_dir: Path) -> bool:
    """Download CIFP (Coded Instrument Flight Procedures) data."""
    url = FAA_URLS['cifp'].format(cycle=cycle)
    zip_path = output_dir / f'cifp_{cycle}.zip'

    if download_file(url, zip_path, f"CIFP {cycle}"):
        return extract_zip(zip_path, output_dir)

    return False


def download_dtpp_manifest(cycle: str, output_dir: Path) -> bool:
    """Download d-TPP XML manifest file."""
    url = FAA_URLS['dtpp'].format(cycle=cycle)
    output_path = output_dir / 'd-TPP_Metafile.xml'

    return download_file(url, output_path, f"d-TPP Manifest {cycle}")


def download_dof(output_dir: Path) -> bool:
    """Download DOF (Digital Obstacle File) - daily update."""
    url = FAA_URLS['dof']
    zip_path = output_dir / 'dof_daily.zip'

    if download_file(url, zip_path, "DOF Daily"):
        return extract_zip(zip_path, output_dir)

    return False


def main():
    parser = argparse.ArgumentParser(
        description='Download FAA aviation data files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--cycle',
        type=str,
        default='current',
        help='AIRAC cycle (e.g., 2513) or "current" for current cycle'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default='./faa_raw/',
        help='Output directory for downloaded files'
    )

    parser.add_argument(
        '--type', '-t',
        type=str,
        choices=['all', 'nasr', 'cifp', 'dtpp', 'dof'],
        default='all',
        help='Type of data to download'
    )

    parser.add_argument(
        '--keep-zip',
        action='store_true',
        help='Keep ZIP files after extraction'
    )

    args = parser.parse_args()

    # Determine cycle
    if args.cycle.lower() == 'current':
        cycle, effective_date = calculate_airac_cycle()
        print(f"Current AIRAC cycle: {cycle} (effective {effective_date.strftime('%Y-%m-%d')})")
    else:
        cycle = args.cycle
        effective_date = get_cycle_effective_date(cycle)
        print(f"Target AIRAC cycle: {cycle} (effective {effective_date.strftime('%Y-%m-%d')})")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    success = True

    # Download requested data types
    if args.type in ['all', 'nasr']:
        success &= download_nasr(cycle, output_dir)

    if args.type in ['all', 'cifp']:
        success &= download_cifp(cycle, output_dir)

    if args.type in ['all', 'dtpp']:
        success &= download_dtpp_manifest(cycle, output_dir)

    if args.type in ['all', 'dof']:
        success &= download_dof(output_dir)

    # Clean up ZIP files unless --keep-zip specified
    if not args.keep_zip:
        for zip_file in output_dir.glob('*.zip'):
            zip_file.unlink()
            print(f"Removed: {zip_file}")

    if success:
        print("\nDownload complete!")
        print(f"Files saved to: {output_dir.absolute()}")
    else:
        print("\nSome downloads failed. Check errors above.")
        sys.exit(1)


if __name__ == '__main__':
    main()

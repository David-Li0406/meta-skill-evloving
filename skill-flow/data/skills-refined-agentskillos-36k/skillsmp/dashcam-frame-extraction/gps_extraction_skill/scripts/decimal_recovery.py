#!/usr/bin/env python3
"""
GPS Decimal Recovery - Phase 2

Re-processes failed GPS extractions by fixing common decimal point issues.
Typical recovery rate: 25-30% of failures.
"""
import argparse
import os
import re
import sys
from typing import Optional, Tuple

import pandas as pd

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    print("Warning: PaddleOCR not available, will use existing OCR data only")


def fix_gps_decimals(text: str) -> str:
    """
    Fix missing decimals in GPS coordinates.

    Examples:
        N438746W790425 → N:43.8746 W:79.0425
        N:43,8878 → N:43.8878
    """
    if not text:
        return text

    fixed = text.replace(',', '.')  # Handle comma decimals

    # Fix N/latitude: N438746 → N:43.8746
    fixed = re.sub(r'([NnAa]):?(\d{2})(\d{4,5})([^0-9]|$)', r'N:\2.\3\4', fixed)

    # Fix W/longitude: W790425 → W:79.0425
    fixed = re.sub(r'W:?(\d{2})(\d{4,5})([^0-9]|$)', r'W:\1.\2\3', fixed)

    return fixed


def parse_gps_simple(text: str) -> Optional[Tuple[float, float]]:
    """
    Simple GPS parser for decimal-fixed text.
    """
    # Pattern: N:43.8878 W:79.0829
    pattern = r'[NnAa]:?\s*(\d{2}\.\d{3,5})\s*W:?\s*(\d{2}\.\d{3,5})'
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))

            # Validate coordinates are in reasonable range
            if 42.0 <= lat <= 45.0 and 78.0 <= lon <= 81.0:
                return (lat, -lon)
        except (ValueError, IndexError):
            pass

    return None


def decimal_recovery(input_file: str, output_file: str, re_ocr: bool = False):
    """
    Recover GPS coordinates from failures by fixing decimal points.
    """
    print("="*70)
    print("GPS DECIMAL RECOVERY")
    print("="*70)
    print()

    # Load input data
    print(f"Loading: {input_file}")
    df = pd.read_excel(input_file)

    # Get failures
    failures = df[df['latitude'].isna()].copy()
    print(f"Failed records: {len(failures):,}")
    print()

    if len(failures) == 0:
        print("No failures to recover - all extractions successful!")
        return

    # Initialize OCR if needed
    ocr = None
    if re_ocr and PADDLE_AVAILABLE:
        print("Initializing PaddleOCR for re-OCR...")
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True, show_log=False)
        print()

    # Process failures
    recovered = []
    print("Processing failures with decimal fixing...")

    for idx, row in failures.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"  Progress: {idx+1:,}/{len(failures):,} ({len(recovered):,} recovered)")

        # Get GPS text
        gps_text = row.get('gps_raw', '')

        # Re-OCR if requested and crop file exists
        if re_ocr and ocr and pd.notna(row.get('frame_path')):
            crop_path = row['frame_path']
            if os.path.exists(crop_path):
                try:
                    result = ocr.ocr(crop_path, cls=True)
                    if result and result[0]:
                        gps_text = ' '.join([line[1][0] for line in result[0]])
                except Exception:
                    pass

        if not gps_text or pd.isna(gps_text):
            continue

        # Fix decimals and try parsing
        fixed_text = fix_gps_decimals(str(gps_text))
        coords = parse_gps_simple(fixed_text)

        if coords:
            lat, lon = coords
            recovered.append({
                'frame_path': row.get('frame_path'),
                'frame_filename': row.get('frame_filename'),
                'latitude': lat,
                'longitude': lon,
                'coordinates': f"{lat}, {lon}",
                'gps_raw': gps_text,
                'gps_parsed': fixed_text,
                'notes': 'Recovered with decimal fixing'
            })

    print(f"  Progress: {len(failures):,}/{len(failures):,} ({len(recovered):,} recovered)")
    print()

    # Save results
    if len(recovered) > 0:
        df_recovered = pd.DataFrame(recovered)
        df_recovered.to_excel(output_file, index=False)

        print("="*70)
        print("RECOVERY RESULTS:")
        print("="*70)
        print(f"Failed extractions: {len(failures):,}")
        print(f"GPS coordinates recovered: {len(recovered):,}")
        print(f"Recovery rate: {len(recovered)/len(failures)*100:.1f}%")
        print(f"Output: {output_file}")
        print("="*70)

        if len(recovered) > 0:
            print()
            print("Sample recoveries:")
            for i, row in df_recovered.head(5).iterrows():
                print(f"  {row['latitude']}, {row['longitude']}")
                print(f"    Original: {row['gps_raw'][:60]}")
                print(f"    Fixed: {row['gps_parsed'][:60]}")
    else:
        print("="*70)
        print("No additional GPS coordinates recovered")
        print("All failures appear to be genuinely missing GPS data")
        print("="*70)


def main():
    parser = argparse.ArgumentParser(description='GPS Decimal Recovery - Fix missing decimal points')
    parser.add_argument('--input', required=True, help='Input Excel file with failures')
    parser.add_argument('--output', required=True, help='Output Excel file for recovered data')
    parser.add_argument('--re-ocr', action='store_true', help='Re-run OCR on failed crops')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    decimal_recovery(args.input, args.output, args.re_ocr)


if __name__ == '__main__':
    main()

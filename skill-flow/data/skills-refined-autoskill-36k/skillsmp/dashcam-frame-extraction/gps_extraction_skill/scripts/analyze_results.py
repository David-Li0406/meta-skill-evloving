#!/usr/bin/env python3
"""
GPS Extraction Results Analyzer

Analyzes the output from GPS extraction and reports statistics.
"""
import argparse
import sys
import pandas as pd


def analyze_results(excel_file: str):
    """Analyze GPS extraction results."""
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {excel_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    total = len(df)
    success = df['latitude'].notna().sum()
    failed = df['latitude'].isna().sum()
    success_rate = (success / total * 100) if total > 0 else 0

    print("="*70)
    print("GPS EXTRACTION RESULTS ANALYSIS")
    print("="*70)
    print(f"Total files processed: {total:,}")
    print(f"GPS coordinates extracted: {success:,}")
    print(f"Failed extractions: {failed:,}")
    print(f"SUCCESS RATE: {success_rate:.1f}%")
    print("="*70)
    print()

    # Evaluation
    if success_rate >= 85.0:
        print("✅ EXCELLENT - Target success rate achieved!")
        status = 0
    elif success_rate >= 80.0:
        print("✅ GOOD - Acceptable success rate")
        status = 0
    elif success_rate >= 70.0:
        print("⚠️  MODERATE - Below target but usable")
        status = 1
    else:
        print("❌ LOW - Success rate below acceptable threshold")
        print("   Check crop parameters and GPU settings")
        status = 1

    print()

    # Show sample coordinates
    if success > 0:
        print("Sample extracted coordinates:")
        for i, row in df[df['latitude'].notna()].head(5).iterrows():
            print(f"  {row['latitude']}, {row['longitude']}")
            if 'gps_raw' in row and pd.notna(row['gps_raw']):
                ocr_text = str(row['gps_raw'])[:60]
                print(f"    OCR: {ocr_text}")
        print()

    # Recommendations
    if failed > 0 and success_rate < 90.0:
        print("Recommendations:")
        if success_rate < 70.0:
            print("  • Check that crop width is set to 0.70 (70%) minimum")
            print("  • Verify GPU is being used for OCR")
            print("  • Review sample failed crops visually")
        elif failed < 5000:
            print("  • Run decimal recovery to fix missing decimal points:")
            print(f"    python scripts/decimal_recovery.py --input {excel_file} --output recovered.xlsx")
        print()

    return status


def main():
    parser = argparse.ArgumentParser(description='Analyze GPS extraction results')
    parser.add_argument('excel_file', help='Excel file to analyze')

    args = parser.parse_args()

    status = analyze_results(args.excel_file)
    sys.exit(status)


if __name__ == '__main__':
    main()

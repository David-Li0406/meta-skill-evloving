#!/usr/bin/env python3
"""
CSV URL Parameter Parser

Extracts query parameters from URLs in CSV files and adds them as new columns.
"""

import csv
import sys
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import shutil


def extract_query_params(url):
    """
    Extracts all query parameters from a URL.

    Args:
        url: URL string to parse

    Returns:
        Dictionary of {param_name: [values]}
    """
    if not url or not url.strip():
        return {}

    try:
        parsed = urlparse(url)
        if not parsed.query:
            return {}

        # parse_qs returns {key: [values]}
        params = parse_qs(parsed.query)
        return params
    except Exception:
        return {}


def process_csv_files(csv_paths=None):
    """
    Process CSV files and extract URL parameters.

    Args:
        csv_paths: List of CSV file paths. If None, processes all CSV files in current directory.
    """
    # If no specific files provided, process all CSV files in current directory
    if csv_paths is None or len(csv_paths) == 0:
        csv_files = list(Path('.').glob('*.csv'))
    else:
        csv_files = [Path(p) for p in csv_paths]

    if not csv_files:
        print("No CSV files found to process.")
        return

    for csv_path in csv_files:
        print(f"Processing {csv_path}...")

        try:
            # Read CSV file
            with open(csv_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                original_headers = reader.fieldnames
                rows = list(reader)

            if not original_headers:
                print(f"Warning: No headers found in {csv_path}. Skipping.")
                continue

            # Find URL column (case insensitive)
            url_column = None
            for col in original_headers:
                if col.lower() == 'url':
                    url_column = col
                    break

            if not url_column:
                print(f"Warning: No 'url' or 'URL' column found in {csv_path}. Skipping.")
                continue

            # Extract parameters from each URL
            row_params = []
            param_names = []

            for row in rows:
                params = extract_query_params(row.get(url_column, ''))
                row_params.append(params)

                # Collect unique parameter names
                for key in params.keys():
                    if key not in param_names:
                        param_names.append(key)

            if not param_names:
                print(f"No URL parameters found in {csv_path}. Skipping.")
                continue

            # Ensure we don't duplicate existing headers
            new_param_headers = [name for name in param_names if name not in original_headers]
            combined_headers = list(original_headers) + new_param_headers

            # Create temporary file
            tmp_path = csv_path.with_suffix('.csv.tmp')

            # Write processed data to temporary file
            with open(tmp_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=combined_headers)
                writer.writeheader()

                for i, row in enumerate(rows):
                    params = row_params[i]

                    # Add parameter values to row
                    for header in new_param_headers:
                        values = params.get(header, [])
                        # Join multiple values with '|'
                        row[header] = '|'.join(values) if values else ''

                    writer.writerow(row)

            # Replace original file with processed version
            shutil.move(str(tmp_path), str(csv_path))

            print(f"Successfully processed {csv_path}. Added {len(new_param_headers)} parameter columns: {', '.join(new_param_headers)}")

        except Exception as e:
            print(f"Error processing {csv_path}: {e}")


def main():
    """Main execution."""
    # Allow command line arguments for specific files
    specific_files = sys.argv[1:] if len(sys.argv) > 1 else None
    process_csv_files(specific_files)


if __name__ == '__main__':
    main()

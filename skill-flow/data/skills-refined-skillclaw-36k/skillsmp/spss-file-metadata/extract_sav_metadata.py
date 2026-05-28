#!/usr/bin/env python3
"""
Extract metadata from SPSS .sav file and output as JSON.
This script reads only the metadata (no data rows) using pyreadstat.
"""

import sys
import json
from pathlib import Path

try:
    import pyreadstat
except ImportError:
    print(
        "Error: pyreadstat is not installed. Install with: pip install pyreadstat",
        file=sys.stderr,
    )
    sys.exit(1)


def extract_sav_metadata(sav_file_path):
    """
    Extract metadata from SPSS .sav file.

    Args:
        sav_file_path: Path to the .sav file

    Returns:
        Dictionary containing all metadata
    """
    # Read only metadata (fast, no data loaded)
    # Use 'dict' output format to avoid pandas/polars dependency
    df, meta = pyreadstat.read_sav(
        sav_file_path, metadataonly=True, output_format="dict"
    )

    # Build comprehensive metadata dictionary
    metadata = {
        "file_encoding": meta.file_encoding,
        "file_label": meta.file_label,
        "number_rows": meta.number_rows,
        "number_columns": meta.number_columns,
        "column_names": meta.column_names,
        "column_labels": meta.column_labels,
        "column_names_to_labels": meta.column_names_to_labels,
        "original_variable_types": meta.original_variable_types,
        "readstat_variable_types": meta.readstat_variable_types,
        "variable_value_labels": meta.variable_value_labels,
        "value_labels": meta.value_labels,
        "variable_to_label": meta.variable_to_label,
        "variable_measure": meta.variable_measure,
        "variable_display_width": meta.variable_display_width,
        "missing_ranges": meta.missing_ranges,
        "notes": meta.notes,
    }

    return metadata


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python extract_sav_metadata.py <path_to_sav_file> [output_json_file]",
            file=sys.stderr,
        )
        print("\nExamples:", file=sys.stderr)
        print("  python extract_sav_metadata.py blueprint.sav", file=sys.stderr)
        print(
            "  python extract_sav_metadata.py blueprint.sav metadata.json",
            file=sys.stderr,
        )
        sys.exit(1)

    sav_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Check if file exists
    if not Path(sav_file).exists():
        print(f"Error: File not found: {sav_file}", file=sys.stderr)
        sys.exit(1)

    try:
        # Extract metadata
        print(f"Reading metadata from: {sav_file}", file=sys.stderr)
        metadata = extract_sav_metadata(sav_file)
        print(
            f"✓ Successfully extracted metadata for {metadata['number_columns']} variables and {metadata['number_rows']} rows",
            file=sys.stderr,
        )

        # Output to file or stdout
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"✓ Metadata saved to: {output_file}", file=sys.stderr)
        else:
            # Print to stdout (no prefix messages)
            print(json.dumps(metadata, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

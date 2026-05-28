#!/usr/bin/env python3
"""
Batch processing script for trademark certificates

Extracts OCR text and logos from multiple trademark certificate files.
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import the main extraction functions
sys.path.insert(0, str(Path(__file__).parent))
from extract_ocr import extract_text
from extract_logo import extract_logo


def batch_extract(folder_path: Path, lang: str = 'chi_sim+eng') -> List[Dict[str, Any]]:
    """
    Extract OCR text and logos from all certificate files in a folder

    Args:
        folder_path: Path to the folder containing certificate files
        lang: Language code for OCR (default: chi_sim+eng)

    Returns:
        List of dictionaries with file paths and extracted text
    """
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Folder not found: {folder_path}", file=sys.stderr)
        return []

    # Supported file extensions
    supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}

    results = []
    processed_files = []

    print(f"Scanning folder: {folder_path}")

    # Iterate through all files in the folder
    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            print(f"\nProcessing: {file_path.name}")

            # Skip already processed files (e.g., _logo.png files)
            if '_logo' in file_path.stem:
                print(f"  Skipping (already processed): {file_path.name}")
                continue

            # Extract text
            print(f"  Extracting text...")
            text = extract_text(file_path, lang)

            if not text:
                print(f"  Warning: No text extracted from {file_path.name}", file=sys.stderr)
                continue

            # Extract logo
            print(f"  Extracting logo...")
            logo_path = extract_logo(file_path)

            if not logo_path:
                print(f"  Warning: Logo extraction failed for {file_path.name}", file=sys.stderr)

            # Save extracted text to file
            text_output_path = file_path.parent / f"{file_path.stem}_extracted.txt"
            with open(text_output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  Text saved to: {text_output_path.name}")

            # Store result
            result = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'extracted_text_file': str(text_output_path),
                'logo_file': str(logo_path) if logo_path else '',
                'extracted_text': text,
                'processed_at': datetime.now().isoformat()
            }
            results.append(result)
            processed_files.append(file_path.name)

            print(f"  ✓ Completed")

    print(f"\n{'='*60}")
    print(f"Batch processing completed")
    print(f"Total files processed: {len(processed_files)}")
    print(f"{'='*60}")

    return results


def save_batch_results(results: List[Dict[str, Any]], output_file: Path):
    """
    Save batch extraction results to a JSON file

    Args:
        results: List of extraction results
        output_file: Path to the output JSON file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Batch results saved to: {output_file}")
    except Exception as e:
        print(f"Error saving batch results: {e}", file=sys.stderr)


def main():
    """Command-line interface for batch processing"""
    if len(sys.argv) < 2:
        print("Usage: python batch_extract.py <folder_path> [language_code]")
        print("Example: python batch_extract.py ./certificates")
        print("Example: python batch_extract.py ./certificates chi_sim+eng")
        sys.exit(1)

    folder_path = Path(sys.argv[1])
    lang = sys.argv[2] if len(sys.argv) > 2 else 'chi_sim+eng'

    # Run batch extraction
    results = batch_extract(folder_path, lang)

    if results:
        # Save results to JSON
        output_file = folder_path / f"batch_extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_batch_results(results, output_file)

        print("\nNext steps:")
        print("1. Review the extracted text files")
        print("2. Use LLM to extract structured information from each _extracted.txt file")
        print("3. Combine the extracted data with logo file paths")
        print("4. Generate Excel file using generate_excel.py")
    else:
        print("No files processed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

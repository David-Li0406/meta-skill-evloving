#!/usr/bin/env python3
"""
Test sorting functionality for trademark data

Tests the sorting and grouping logic by registrant and validity period.
"""

import sys
from pathlib import Path
import json

# Import the main functions
sys.path.insert(0, str(Path(__file__).parent))
from generate_excel import sort_trademark_data, create_excel, open_excel


def create_test_data():
    """
    Create test trademark data for sorting

    Returns:
        List of dictionaries with test trademark information
    """
    test_data = [
        {
            "序号": "3",
            "商标标识图片路径": "",
            "注册人": "腾讯科技（深圳）有限公司",
            "注册号": "98765432",
            "国际分类": "第9类",
            "有效期限": "2024-08-20"
        },
        {
            "序号": "1",
            "商标标识图片路径": "",
            "注册人": "阿里巴巴集团控股有限公司",
            "注册号": "12345678",
            "国际分类": "第35类",
            "有效期限": "2025-12-31"
        },
        {
            "序号": "4",
            "商标标识图片路径": "",
            "注册人": "腾讯科技（深圳）有限公司",
            "注册号": "56789012",
            "国际分类": "第41类",
            "有效期限": "2025-01-10"
        },
        {
            "序号": "2",
            "商标标识图片路径": "",
            "注册人": "阿里巴巴集团控股有限公司",
            "注册号": "87654321",
            "国际分类": "第38类",
            "有效期限": "2026-03-15"
        },
        {
            "序号": "5",
            "商标标识图片路径": "",
            "注册人": "百度在线网络技术（北京）有限公司",
            "注册号": "34567890",
            "国际分类": "第42类",
            "有效期限": "2027-05-25"
        },
        # Add more test cases with various date formats
        {
            "序号": "6",
            "商标标识图片路径": "",
            "注册人": "阿里巴巴集团控股有限公司",
            "注册号": "11111111",
            "国际分类": "第42类",
            "有效期限": "2023/06/01"  # Different date format
        },
        {
            "序号": "7",
            "商标标识图片路径": "",
            "注册人": "腾讯科技（深圳）有限公司",
            "注册号": "22222222",
            "国际分类": "第25类",
            "有效期限": "2024年12月31日"  # Chinese date format
        },
        {
            "序号": "8",
            "商标标识图片路径": "",
            "注册人": "字节跳动科技有限公司",
            "注册号": "33333333",
            "国际分类": "第38类",
            "有效期限": "2028-01-15"
        }
    ]

    return test_data


def display_sorting_results(original_data, sorted_data):
    """Display the sorting results for comparison"""
    print("\n" + "="*70)
    print("SORTING RESULTS")
    print("="*70)

    print("\nOriginal Data (unsorted):")
    print("-" * 70)
    print(f"{'序号':<6} {'注册人':<30} {'有效期限':<12}")
    print("-" * 70)
    for entry in original_data:
        print(f"{entry['序号']:<6} {entry['注册人']:<30} {entry['有效期限']:<12}")

    print("\n\nSorted Data:")
    print("-" * 70)
    print(f"{'序号':<6} {'注册人':<30} {'有效期限':<12}")
    print("-" * 70)
    for entry in sorted_data:
        print(f"{entry['序号']:<6} {entry['注册人']:<30} {entry['有效期限']:<12}")

    print("\n\nSorting Rules:")
    print("-" * 70)
    print("1. Primary Sort: 注册人 (Registrant) - alphabetically")
    print("2. Secondary Sort: 有效期限 (Validity Period) - ascending")
    print("3. Visual Grouping: Thick border lines separate different registrants")

    print("\n\nExpected Groupings:")
    print("-" * 70)
    current_registrant = None
    for entry in sorted_data:
        if entry['注册人'] != current_registrant:
            print(f"\n{entry['注册人']}:")
            current_registrant = entry['注册人']
        print(f"  - {entry['序号']}: {entry['有效期限']}")

    print("\n" + "="*70)


def save_test_data(data, output_path):
    """Save test data to a JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nTest data saved to: {output_path}")
    except Exception as e:
        print(f"Error saving test data: {e}", file=sys.stderr)


def main():
    """Main function for testing sorting"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "TRADEMARK SORTING TEST".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    # Create test data
    print("\nCreating test data...")
    test_data = create_test_data()
    print(f"Created {len(test_data)} test trademark entries")

    # Sort the data
    print("\nSorting trademark data...")
    sorted_data = sort_trademark_data(test_data)
    print("Sorting completed")

    # Display results
    display_sorting_results(test_data, sorted_data)

    # Save sorted data to JSON
    output_json = Path("/tmp/test_sorted_trademarks.json")
    save_test_data(sorted_data, output_json)

    # Ask if user wants to generate Excel
    print("\n" + "="*70)
    response = input("\nGenerate Excel file with test data? (y/n): ").strip().lower()

    if response == 'y':
        print("\nGenerating Excel file...")
        output_xlsx = Path("/tmp/test_sorted_trademarks.xlsx")

        if create_excel(sorted_data, output_xlsx):
            print(f"\n✓ Excel file created successfully: {output_xlsx}")
            print(f"\nOpening Excel file for review...")
            open_excel(output_xlsx)

            print("\n" + "="*70)
            print("TEST COMPLETED")
            print("="*70)
            print("\nReview the Excel file to verify:")
            print("  ✓ Same registrant entries are grouped together")
            print("  ✓ Thicker border lines separate different registrant groups")
            print("  ✓ Within each group, trademarks are sorted by validity period (ascending)")
        else:
            print("\n✗ Failed to create Excel file")
            sys.exit(1)
    else:
        print("\nExcel generation skipped")
        print("\nYou can manually generate Excel later using:")
        print(f"python scripts/generate_excel.py {output_xlsx}")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()

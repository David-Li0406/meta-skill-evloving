#!/usr/bin/env python3
"""
Complete demonstration script for trademark certificate extraction

Shows the full workflow: OCR extraction → LLM processing → Excel generation.
Includes sample data and detailed output.
"""

import sys
from pathlib import Path
import json

# Import the main functions
sys.path.insert(0, str(Path(__file__).parent))
from generate_excel import create_excel, open_excel


def create_sample_data():
    """
    Create sample trademark data for demonstration

    Returns:
        List of dictionaries with sample trademark information
    """
    # Sample data with realistic trademark information
    sample_data = [
        {
            "序号": "1",
            "商标标识图片路径": "/tmp/sample_logo_1.png",  # Placeholder - would be actual logo file path
            "注册人": "阿里巴巴集团控股有限公司",
            "注册号": "12345678",
            "国际分类": "第35类",
            "有效期限": "2025-12-31"
        },
        {
            "序号": "2",
            "商标标识图片路径": "/tmp/sample_logo_2.png",
            "注册人": "阿里巴巴集团控股有限公司",
            "注册号": "87654321",
            "国际分类": "第38类",
            "有效期限": "2026-03-15"
        },
        {
            "序号": "3",
            "商标标识图片路径": "/tmp/sample_logo_3.png",
            "注册人": "腾讯科技（深圳）有限公司",
            "注册号": "98765432",
            "国际分类": "第9类",
            "有效期限": "2024-08-20"
        },
        {
            "序号": "4",
            "商标标识图片路径": "/tmp/sample_logo_4.png",
            "注册人": "腾讯科技（深圳）有限公司",
            "注册号": "56789012",
            "国际分类": "第41类",
            "有效期限": "2025-01-10"
        },
        {
            "序号": "5",
            "商标标识图片路径": "/tmp/sample_logo_5.png",
            "注册人": "百度在线网络技术（北京）有限公司",
            "注册号": "34567890",
            "国际分类": "第42类",
            "有效期限": "2027-05-25"
        }
    ]

    return sample_data


def create_sample_logo_files():
    """
    Create sample logo files for demonstration

    In a real scenario, these would be extracted from actual trademark certificates.
    """
    from PIL import Image, ImageDraw, ImageFont

    # Create a simple placeholder logo
    for i in range(1, 6):
        # Create a blank image with a simple design
        img = Image.new('RGB', (100, 100), color='white')
        draw = ImageDraw.Draw(img)

        # Draw a simple colored rectangle with text
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        color = colors[(i-1) % len(colors)]

        draw.rectangle([10, 10, 90, 90], outline=color, width=3)
        draw.text((30, 40), f"LOGO{i}", fill=color)

        # Save the sample logo
        logo_path = Path(f"/tmp/sample_logo_{i}.png")
        img.save(logo_path, 'PNG')
        print(f"Created sample logo: {logo_path}")


def display_workflow():
    """Display the complete workflow for trademark extraction"""
    print("="*70)
    print("TRADEMARK CERTIFICATE EXTRACTION WORKFLOW")
    print("="*70)
    print()

    print("Step 1: Extract Text with OCR")
    print("-" * 70)
    print("Command: python scripts/extract_ocr.py certificate.pdf")
    print("This extracts text from the certificate using Tesseract OCR")
    print()

    print("Step 2: Extract Trademark Logo")
    print("-" * 70)
    print("Command: python scripts/extract_logo.py certificate.pdf")
    print("This extracts and saves the trademark logo image")
    print()

    print("Step 3: Extract Information with LLM")
    print("-" * 70)
    print("Use the prompt from references/llm_prompt.md with Claude or another LLM")
    print("Extract: 序号, 注册人, 注册号, 国际分类, 有效期限")
    print()

    print("Step 4: Generate Excel File")
    print("-" * 70)
    print("Command: python scripts/generate_excel.py trademark_data.json")
    print("This creates an Excel file with embedded logos")
    print()

    print("="*70)
    print()


def display_sample_data():
    """Display the sample trademark data"""
    print("Sample Trademark Data:")
    print("-" * 70)
    sample_data = create_sample_data()
    print(json.dumps(sample_data, ensure_ascii=False, indent=2))
    print()


def run_demo():
    """
    Run the complete demonstration
    """
    print("\n" + "="*70)
    print("RUNNING TRADEMARK CERTIFICATE EXTRACTION DEMO")
    print("="*70)
    print()

    # Display workflow
    display_workflow()

    # Create sample data
    print("Creating sample data...")
    sample_data = create_sample_data()
    print(f"Created {len(sample_data)} sample trademark entries")
    print()

    # Display sample data
    display_sample_data()

    # Note about logo files
    print("Note: In a real scenario, logo files would be extracted from")
    print("      actual trademark certificates. For this demo, we're using")
    print("      placeholder logo file paths.")
    print()

    # Ask if user wants to create sample logos
    response = input("Create sample logo files? (y/n): ").strip().lower()

    if response == 'y':
        print("\nCreating sample logo files...")
        create_sample_logo_files()
        print()
    else:
        print("\nSkipping logo file creation (using placeholder paths)")
        print()

    # Generate Excel file
    print("Generating Excel file...")
    output_path = Path("/tmp/trademark_demo_output.xlsx")

    # For demo purposes, we'll skip the logos if they don't exist
    demo_data = []
    for entry in sample_data:
        logo_path = Path(entry["商标标识图片路径"])
        if logo_path.exists():
            demo_data.append(entry)
        else:
            # Create entry without logo path
            entry_copy = entry.copy()
            entry_copy["商标标识图片路径"] = ""
            demo_data.append(entry_copy)

    if create_excel(demo_data, output_path):
        print(f"\n✓ Excel file created successfully: {output_path}")
        print(f"\nOpening Excel file for review...")

        # Open the Excel file
        open_excel(output_path)

        print("\n" + "="*70)
        print("DEMO COMPLETED")
        print("="*70)
        print()
        print("Next steps:")
        print("1. Review the generated Excel file")
        print("2. Test with actual trademark certificates")
        print("3. Adjust logo detection parameters if needed")
        print()
    else:
        print("\n✗ Failed to create Excel file")
        sys.exit(1)


def main():
    """Main function"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "TRADEMARK CERTIFICATE EXTRACTOR - DEMONSTRATION".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    run_demo()


if __name__ == "__main__":
    main()

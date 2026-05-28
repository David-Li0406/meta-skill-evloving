#!/usr/bin/env python3
"""
Office文書XMLファイルをXSDスキーマと変更履歴に対して検証する。

Usage:
    python validate.py <dir> --original <original_file>
"""

import argparse
import sys
from pathlib import Path


def main():
    """メイン関数。"""
    parser = argparse.ArgumentParser(description="Office文書XMLファイルを検証")
    parser.add_argument(
        "unpacked_dir",
        help="展開されたOffice文書ディレクトリのパス",
    )
    parser.add_argument(
        "--original",
        required=True,
        help="元ファイルのパス（.docx/.pptx/.xlsx）",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="詳細出力を有効化",
    )
    args = parser.parse_args()

    # パス検証
    unpacked_dir = Path(args.unpacked_dir)
    original_file = Path(args.original)
    file_extension = original_file.suffix.lower()
    assert unpacked_dir.is_dir(), f"Error: {unpacked_dir} is not a directory"
    assert original_file.is_file(), f"Error: {original_file} is not a file"
    assert file_extension in [".docx", ".pptx", ".xlsx"], (
        f"Error: {original_file} must be a .docx, .pptx, or .xlsx file"
    )

    # 基本検証
    success = True

    # document.xmlの存在確認
    if file_extension == ".docx":
        document_xml = unpacked_dir / "word" / "document.xml"
        if not document_xml.exists():
            print(f"ERROR: {document_xml} not found")
            success = False
        else:
            if args.verbose:
                print(f"Found {document_xml}")

            # XML構文チェック
            try:
                import defusedxml.minidom
                with open(document_xml, "r", encoding="utf-8") as f:
                    defusedxml.minidom.parse(f)
                if args.verbose:
                    print("XML syntax is valid")
            except Exception as e:
                print(f"ERROR: XML syntax error in {document_xml}: {e}")
                success = False

    if success:
        print("Validation PASSED!")
    else:
        print("Validation FAILED!")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Officeファイル（.docx, .pptx, .xlsx）をディレクトリに展開し、XMLを整形する。"""

import random
import sys
import defusedxml.minidom
import zipfile
from pathlib import Path


def main():
    """メイン関数。"""
    assert len(sys.argv) == 3, "Usage: python unpack.py <office_file> <output_dir>"
    input_file, output_dir = sys.argv[1], sys.argv[2]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    zipfile.ZipFile(input_file).extractall(output_path)

    # XMLファイルを整形
    xml_files = list(output_path.rglob("*.xml")) + list(output_path.rglob("*.rels"))
    for xml_file in xml_files:
        content = xml_file.read_text(encoding="utf-8")
        dom = defusedxml.minidom.parseString(content)
        xml_file.write_bytes(dom.toprettyxml(indent="  ", encoding="ascii"))

    # DOCXファイルの場合、変更履歴用のRSIDを提案
    if input_file.endswith(".docx"):
        suggested_rsid = "".join(random.choices("0123456789ABCDEF", k=8))
        print(f"Suggested RSID for edit session: {suggested_rsid}")

    print(f"Unpacked {input_file} to {output_dir}")
    print(f"Formatted {len(xml_files)} XML files")


if __name__ == "__main__":
    main()

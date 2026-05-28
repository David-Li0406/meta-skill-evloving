#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def render_xlsx(path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'qlmanage',
        '-t',
        '-s', '1400',
        '-o', str(out_dir),
        str(path)
    ], check=True, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description='Render XLSX to PNG using Quick Look.')
    parser.add_argument('--input', required=True, help='XLSX file or directory')
    parser.add_argument('--out', required=True, help='Output directory')
    args = parser.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.out)

    if in_path.is_dir():
        for path in sorted(in_path.iterdir()):
            if path.suffix.lower() == '.xlsx':
                render_xlsx(path, out_dir)
    else:
        render_xlsx(in_path, out_dir)


if __name__ == '__main__':
    main()

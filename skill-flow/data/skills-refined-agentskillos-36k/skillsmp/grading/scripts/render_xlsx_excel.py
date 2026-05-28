#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def run_osascript(script):
    return subprocess.run(['osascript', '-e', script], capture_output=True, text=True)


def render_xlsx(path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{path.stem}.pdf"
    script = f'''
    tell application "Microsoft Excel"
        set display alerts to false
        set wb to open POSIX file "{path}"
        set pdfPath to POSIX file "{pdf_path}"
        try
            save workbook as wb filename pdfPath file format PDF
        on error errMsg number errNum
            close wb saving no
            error errMsg number errNum
        end try
        close wb saving no
    end tell
    '''
    result = run_osascript(script)
    if result.returncode != 0:
        raise RuntimeError(f"Excel render failed: {result.stderr.strip()} {result.stdout.strip()}")

    if not pdf_path.exists():
        raise RuntimeError(f"Excel did not create PDF for {path.name}")

    # Convert PDF pages to PNG for visual review
    subprocess.run([
        'pdftoppm',
        '-r', '200',
        '-png',
        str(pdf_path),
        str(out_dir / path.stem)
    ], check=True)


def main():
    parser = argparse.ArgumentParser(description='Render XLSX to PDF/PNG using Excel.')
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

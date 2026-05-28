#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path


def run(cmd, check=True, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, check=check, env=env)


def render_xlsx(path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Convert to PDF using LibreOffice
    user_profile = out_dir / 'lo-profile'
    user_profile.mkdir(parents=True, exist_ok=True)
    cmd = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',
        '--headless',
        '--nologo',
        '--nofirststartwizard',
        '--norestore',
        '--nodefault',
        '--nolockcheck',
        '--invisible',
        f'-env:UserInstallation=file://{user_profile}',
        '--convert-to', 'pdf',
        '--outdir', str(out_dir),
        str(path)
    ]
    env = os.environ.copy()
    env['SAL_USE_VCLPLUGIN'] = 'gen'
    env['HOME'] = str(out_dir)
    result = run(cmd, check=False, env=env)
    if result.returncode != 0:
        details = f"returncode={result.returncode} stdout={result.stdout.strip()} stderr={result.stderr.strip()}"
        raise RuntimeError(
            "LibreOffice failed. Open LibreOffice once to complete first-run setup, "
            "then retry. Details: " + details
        )

    pdf_path = out_dir / f"{path.stem}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"PDF not created for {path.name}")

    # Convert PDF pages to PNG for visual review
    run([
        'pdftoppm',
        '-r', '200',
        '-png',
        str(pdf_path),
        str(out_dir / path.stem)
    ])


def main():
    parser = argparse.ArgumentParser(description='Render XLSX to PDF and PNGs for chart review.')
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

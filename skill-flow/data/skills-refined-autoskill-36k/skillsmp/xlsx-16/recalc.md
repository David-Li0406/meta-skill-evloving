# recalc.py - Excel Formula Recalculation Script

Recalculates all formulas in an Excel file using LibreOffice.

## Usage

```bash
python recalc.py <excel_file> [timeout_seconds]
python recalc.py output.xlsx 30
```

## Output Format

Returns JSON with error details:

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Status Values

- `success` - No formula errors found
- `errors_found` - One or more formula errors detected

## Error Types Detected

| Error | Meaning |
|-------|---------|
| `#VALUE!` | Wrong data type in formula |
| `#DIV/0!` | Division by zero |
| `#REF!` | Invalid cell reference |
| `#NAME?` | Unrecognized formula name |
| `#NULL!` | Incorrect range operator |
| `#NUM!` | Invalid numeric value |
| `#N/A` | Value not available |

## Script Content

```python
#!/usr/bin/env python3
"""Excel Formula Recalculation Script"""

import json
import sys
import subprocess
import os
import platform
from pathlib import Path
from openpyxl import load_workbook

def setup_libreoffice_macro():
    """Setup LibreOffice macro for recalculation if not already configured"""
    if platform.system() == 'Darwin':
        macro_dir = os.path.expanduser('~/Library/Application Support/LibreOffice/4/user/basic/Standard')
    else:
        macro_dir = os.path.expanduser('~/.config/libreoffice/4/user/basic/Standard')

    macro_file = os.path.join(macro_dir, 'Module1.xba')

    if os.path.exists(macro_file):
        with open(macro_file, 'r') as f:
            if 'RecalculateAndSave' in f.read():
                return True

    if not os.path.exists(macro_dir):
        subprocess.run(['soffice', '--headless', '--terminate_after_init'],
                      capture_output=True, timeout=10)
        os.makedirs(macro_dir, exist_ok=True)

    macro_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub RecalculateAndSave()
      ThisComponent.calculateAll()
      ThisComponent.store()
      ThisComponent.close(True)
    End Sub
</script:module>"""

    try:
        with open(macro_file, 'w') as f:
            f.write(macro_content)
        return True
    except Exception:
        return False

def recalc(filename, timeout=30):
    """Recalculate formulas in Excel file and report any errors"""
    if not Path(filename).exists():
        return {'error': f'File {filename} does not exist'}

    abs_path = str(Path(filename).absolute())

    if not setup_libreoffice_macro():
        return {'error': 'Failed to setup LibreOffice macro'}

    cmd = [
        'soffice', '--headless', '--norestore',
        'vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application',
        abs_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check for Excel errors in the recalculated file
    try:
        wb = load_workbook(filename, data_only=True)
        excel_errors = ['#VALUE!', '#DIV/0!', '#REF!', '#NAME?', '#NULL!', '#NUM!', '#N/A']
        error_details = {err: [] for err in excel_errors}
        total_errors = 0

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is not None and isinstance(cell.value, str):
                        for err in excel_errors:
                            if err in cell.value:
                                location = f"{sheet_name}!{cell.coordinate}"
                                error_details[err].append(location)
                                total_errors += 1
                                break

        wb.close()
        return {
            'status': 'success' if total_errors == 0 else 'errors_found',
            'total_errors': total_errors,
            'error_summary': {k: {'count': len(v), 'locations': v[:20]}
                            for k, v in error_details.items() if v}
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python recalc.py <excel_file> [timeout_seconds]")
        sys.exit(1)
    filename = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    result = recalc(filename, timeout)
    print(json.dumps(result, indent=2))
```

## Requirements

- LibreOffice installed
- openpyxl Python package
- Works on Linux and macOS

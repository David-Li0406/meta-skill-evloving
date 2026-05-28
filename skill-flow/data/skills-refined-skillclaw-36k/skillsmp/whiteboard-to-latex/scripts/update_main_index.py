#!/usr/bin/env python3
import sys
import os
import re

"""
Main Index Updater

Usage:
    python update_main_index.py

Description:
    Ensures all L/LX.tex or T/TX.tex files are included in ODE.tex via \\input.
    Automatically adds missing files in numerical order.
"""

def update_index():
    if len(sys.argv) > 1:
        n_dir = sys.argv[1]
    else:
        n_dir = "L" # Default

    main_file = "ODE.tex"
    
    # 1. Check paths
    if not os.path.exists(n_dir):
        print(f"  ! Directory {n_dir} not found!")
        return
    
    if not os.path.exists(main_file):
        print(f"  ! File {main_file} not found!")
        return

    # 2. Find files
    files = [f for f in os.listdir(n_dir) if re.match(r'[LT]\d+\.tex', f)]
    files.sort(key=lambda x: int(re.search(r'[LT](\d+)', x).group(1)))
    
    if not files:
        print(f"  = No L/T*.tex files found in {n_dir}")
        return

    print(f"> Checking: {len(files)} files in {n_dir}")

    # 3. Read main file
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. Find existing inputs
    pattern = r'\\input\{' + n_dir + r'/([LT]\d+\.tex)\}'
    existing = set(re.findall(pattern, content))
    missing = [f for f in files if f not in existing]
    
    if not missing:
        print("  = All files already included!")
        return

    print(f"  + Missing: {', '.join(missing)}")

    # 5. Find insertion point
    input_pat = re.compile(r'(\\input\{[LT]/[LT]\d+\.tex\}\s*\\newpage)')
    matches = list(input_pat.finditer(content))
    
    if matches:
        insert_pos = matches[-1].end()
    else:
        end_doc = re.search(r'\\end\{document\}', content)
        if end_doc:
            insert_pos = end_doc.start()
        else:
            print("  ! Cannot find insertion point!")
            return

    # 6. Build insertion
    insertion = ""
    if insert_pos > 0 and content[insert_pos - 1] != '\n':
        insertion += "\n"
    
    for f in missing:
        insertion += f"\n\\input{{{n_dir}/{f}}}\n\\newpage"

    # 7. Write changes
    new_content = content[:insert_pos] + insertion + content[insert_pos:]
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  + Added {len(missing)} file(s) to {main_file}")

if __name__ == "__main__":
    update_index()

#!/usr/bin/env python3
import os
import re
import argparse

"""
TeX Notes Auditor

Usage:
    python audit_notes.py <directory> [--fix] [--verbose]

Description:
    Audits L/LX.tex or T/TX.tex files for format, structure, style, and indentation.
    Use --fix to automatically apply corrections.
"""

def check_indentation(content):
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
            
        # If line has leading whitespace
        if line != line.lstrip():
            issues.append((i + 1, "Line has indentation", line))
    
    return issues

def fix_indentation(content):
    lines = content.split('\n')
    fixed = []
    
    for line in lines:
        if not line.strip():
            fixed.append(line)
        else:
            fixed.append(line.lstrip())
    
    return '\n'.join(fixed)

def audit_file(filepath, fix=False):
    filename = os.path.basename(filepath)
    match = re.match(r'[LT](\d+)\.tex', filename)
    if not match:
        return []

    file_num = match.group(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    issues = []
    
    # 1. Preamble Check
    if r'\documentclass' in content or r'\begin{document}' in content:
        issues.append("Preamble found (not a fragment)")
        if fix:
            section = re.search(r'\\section\{', content)
            if section:
                content = content[section.start():]
                content = re.sub(r'\\end\{document\}\s*$', '', content, flags=re.MULTILINE)
            else:
                issues.append("Error: Cannot find \\section to fix preamble!")

    # 2. Header Check
    header = re.search(r'\\section\{Notes\s+(\d+)', content)
    if header:
        if header.group(1) != file_num:
            issues.append(f"Header mismatch: {header.group(1)} vs {file_num}")
            if fix:
                start, end = header.span(1)
                content = content[:start] + file_num + content[end:]
    elif r'\section' not in content:
        issues.append("Missing \\section header!")

    # 3. Proof Check
    proof_pat = re.compile(r'(\\begin\{proof\}.*?\\end\{proof\})', re.DOTALL)
    
    if r'\begin{proof}' in content:
        new_content_parts = []
        last_idx = 0
        modified_proofs = False
        reported_active = False
        reported_commented_indent = False
        
        for m in proof_pat.finditer(content):
            start, end = m.span()
            new_content_parts.append(content[last_idx:start])
            
            # Check if proof is active (not commented)
            line_start = content.rfind('\n', 0, start) + 1
            prefix = content[line_start:start]
            
            if '%' not in prefix:
                # Active proof found
                if not reported_active:
                    issues.append("Active proof found!")
                    reported_active = True
                modified_proofs = True
                
                if fix:
                    lines = m.group(1).split('\n')
                    commented = ["% " + l.lstrip() if l.strip() else "" for l in lines]
                    replacement = "\\begin{remark}\nProof is commented out!\n\\end{remark}\n\n" + "\n".join(commented)
                    new_content_parts.append(replacement)
                else:
                    new_content_parts.append(m.group(0))
            else:
                # Inactive (already commented)
                match_str = m.group(0)
                match_lines = match_str.split('\n')
                
                # Check prefix indentation
                prefix_indented = prefix != prefix.lstrip()
                
                # Normalize each line and detect if fixes are needed
                body_needs_fix = False
                normalized_lines = []
                
                for line in match_lines:
                    stripped = line.lstrip()
                    
                    # Check for outer indentation
                    if stripped != line:
                        body_needs_fix = True
                    
                    # Normalize to "% <content>" format
                    if stripped.startswith('%'):
                        comment_content = stripped[1:].strip()
                        if comment_content:
                            normalized = "% " + comment_content
                        else:
                            normalized = "%"
                        
                        if stripped != normalized:
                            body_needs_fix = True
                        normalized_lines.append(normalized)
                    else:
                        normalized_lines.append(stripped)

                needs_fix = prefix_indented or body_needs_fix
                
                if needs_fix:
                    if not reported_commented_indent:
                        issues.append("Indentation in commented proof")
                        reported_commented_indent = True
                    
                    if fix:
                        # Fix prefix indentation
                        if new_content_parts:
                            pre_part = new_content_parts.pop()
                            pre_lines = pre_part.split('\n')
                            if pre_lines:
                                last_line = pre_lines[-1].lstrip()
                                # Ensure prefix comment has space for continuation
                                if last_line == '%':
                                    last_line = "% "
                                pre_lines[-1] = last_line
                            new_content_parts.append('\n'.join(pre_lines))
                        
                        # Append normalized body
                        new_content_parts.append('\n'.join(normalized_lines))
                        modified_proofs = True
                    else:
                        new_content_parts.append(match_str)
                else:
                    new_content_parts.append(match_str)
            
            last_idx = end
            
        new_content_parts.append(content[last_idx:])
        
        if fix and modified_proofs:
            content = "".join(new_content_parts)

    # 4. Indentation Check
    indent_issues = check_indentation(content)
    if indent_issues:
        issues.append(f"{len(indent_issues)} indentation issue(s)")
        if fix:
            content = fix_indentation(content)

    # 5. Write changes
    if content != original:
        if fix:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return [f"Fixed: {i}" for i in issues]
        else:
            return [f"Would fix: {i}" for i in issues]
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Audit TeX notes for consistency.")
    parser.add_argument('directory', help="Directory containing N files")
    parser.add_argument('--fix', action='store_true', help="Apply fixes")
    parser.add_argument('--verbose', '-v', action='store_true', help="Show details")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory {args.directory} not found!")
        return

    files = sorted(
        [f for f in os.listdir(args.directory) if re.match(r'[LT]\d+\.tex', f)],
        key=lambda x: int(re.search(r'[LT](\d+)', x).group(1))
    )
    
    if not files:
        print(f"  = No L*.tex or T*.tex files found in {args.directory}")
        return

    print(f"> Auditing: {len(files)} files in {args.directory}")
    
    report = {}
    for f in files:
        path = os.path.join(args.directory, f)
        res = audit_file(path, fix=args.fix)
        if res:
            report[f] = res

    # Output
    if not report:
        print("  = No issues found!")
    else:
        for f, issues in report.items():
            print(f"  {f}:")
            for issue in issues:
                print(f"    - {issue}")
        print(f"\n> Summary: {len(report)}/{len(files)} files with issues")

if __name__ == "__main__":
    main()

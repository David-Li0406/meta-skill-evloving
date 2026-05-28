#!/usr/bin/env python3
"""
BlueMouse L1-L4: 語法和結構驗證
獨立版本 - 可作為 Claude Code Skill 使用

用法:
    python validator.py <file.py>
    python validator.py --code "def foo(): pass"
"""

import ast
import re
import sys
import json
import argparse
from typing import Dict, List


def validate_syntax_and_structure(code: str) -> List[Dict]:
    """L1-L4: 語法和結構驗證"""
    results = []
    results.append(validate_l1_basic_syntax(code))
    results.append(validate_l2_ast_structure(code))
    results.append(validate_l3_indentation(code))
    results.append(validate_l4_naming_convention(code))
    return results


def validate_l1_basic_syntax(code: str) -> Dict:
    """L1: 基本語法檢查"""
    try:
        compile(code, '<string>', 'exec')
        return {
            "layer": 1,
            "name": "基本語法檢查",
            "passed": True,
            "message": "語法正確"
        }
    except SyntaxError as e:
        return {
            "layer": 1,
            "name": "基本語法檢查",
            "passed": False,
            "message": f"語法錯誤: {str(e)}",
            "error": str(e)
        }


def validate_l2_ast_structure(code: str) -> Dict:
    """L2: AST 結構檢查"""
    try:
        tree = ast.parse(code)
        has_definition = any(isinstance(node, (ast.FunctionDef, ast.ClassDef))
                            for node in ast.walk(tree))

        if has_definition:
            return {
                "layer": 2,
                "name": "AST 結構檢查",
                "passed": True,
                "message": "AST 結構完整"
            }
        else:
            return {
                "layer": 2,
                "name": "AST 結構檢查",
                "passed": False,
                "message": "缺少函數或類定義"
            }
    except Exception as e:
        return {
            "layer": 2,
            "name": "AST 結構檢查",
            "passed": False,
            "message": f"AST 解析失敗: {str(e)}"
        }


def validate_l3_indentation(code: str) -> Dict:
    """L3: 縮進和格式檢查"""
    lines = code.split('\n')
    issues = []

    for i, line in enumerate(lines, 1):
        if '\t' in line:
            issues.append(f"Line {i}: 使用 Tab 而非空格")

        if line and not line.lstrip():
            continue
        leading_spaces = len(line) - len(line.lstrip())
        if leading_spaces % 4 != 0:
            issues.append(f"Line {i}: 縮進不是 4 的倍數")

    if not issues:
        return {
            "layer": 3,
            "name": "縮進和格式檢查",
            "passed": True,
            "message": "縮進格式正確"
        }
    else:
        return {
            "layer": 3,
            "name": "縮進和格式檢查",
            "passed": False,
            "message": f"發現 {len(issues)} 個格式問題",
            "issues": issues[:3]
        }


def validate_l4_naming_convention(code: str) -> Dict:
    """L4: 命名規範檢查 (PEP 8)"""
    try:
        tree = ast.parse(code)
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    issues.append(f"函數名 '{node.name}' 不符合 snake_case")

            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append(f"類名 '{node.name}' 不符合 PascalCase")

        if not issues:
            return {
                "layer": 4,
                "name": "命名規範檢查",
                "passed": True,
                "message": "命名符合 PEP 8"
            }
        else:
            return {
                "layer": 4,
                "name": "命名規範檢查",
                "passed": len(issues) == 0,
                "message": f"發現 {len(issues)} 個命名問題",
                "issues": issues[:3]
            }
    except Exception as e:
        return {
            "layer": 4,
            "name": "命名規範檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def print_report(results: List[Dict], verbose: bool = False):
    """打印驗證報告"""
    print(f"\n{'='*50}")
    print("L1-L4: 語法和結構驗證")
    print(f"{'='*50}\n")

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    score = int((passed_count / total_count) * 100)

    status = "✅ PASSED" if passed_count == total_count else "❌ FAILED"
    print(f"Status: {status}")
    print(f"Score: {score}/100 ({passed_count}/{total_count} layers)\n")

    for layer in results:
        icon = "✅" if layer['passed'] else "❌"
        print(f"{icon} L{layer['layer']}: {layer['name']} - {layer['message']}")
        if verbose and 'issues' in layer and layer['issues']:
            for issue in layer['issues']:
                print(f"    → {issue}")

    print()


def main():
    parser = argparse.ArgumentParser(description='BlueMouse L1-L4: 語法和結構驗證')
    parser.add_argument('file', nargs='?', help='Python file to validate')
    parser.add_argument('--code', '-c', help='Code string to validate')
    parser.add_argument('--stdin', action='store_true', help='Read code from stdin')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    code = None
    if args.stdin:
        code = sys.stdin.read()
    elif args.code:
        code = args.code
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    results = validate_syntax_and_structure(code)

    if args.json:
        output = {
            "group": "L1-L4: 語法和結構驗證",
            "passed": all(r["passed"] for r in results),
            "layers": results,
            "score": int(sum(1 for r in results if r["passed"]) / len(results) * 100)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_report(results, verbose=args.verbose)

    sys.exit(0 if all(r["passed"] for r in results) else 1)


if __name__ == "__main__":
    main()

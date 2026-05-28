#!/usr/bin/env python3
"""
BlueMouse L9-L12: 依賴關係驗證
獨立版本 - 可作為 Claude Code Skill 使用

用法:
    python validator.py <file.py>
    python validator.py --code "import os"
"""

import ast
import sys
import json
import argparse
from typing import Dict, List, Optional


def validate_dependencies(code: str, spec: Optional[Dict] = None) -> List[Dict]:
    """L9-L12: 依賴關係驗證"""
    results = []
    results.append(validate_l9_imports(code))
    results.append(validate_l10_stdlib(code))
    results.append(validate_l11_third_party(code))
    results.append(validate_l12_circular_deps(code))
    return results


def validate_l9_imports(code: str) -> Dict:
    """L9: 導入檢查"""
    try:
        tree = ast.parse(code)
        imports = [node for node in ast.walk(tree)
                  if isinstance(node, (ast.Import, ast.ImportFrom))]

        return {
            "layer": 9,
            "name": "導入檢查",
            "passed": True,
            "message": f"找到 {len(imports)} 個導入語句"
        }
    except Exception as e:
        return {
            "layer": 9,
            "name": "導入檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def validate_l10_stdlib(code: str) -> Dict:
    """L10: 標準庫檢查 (AST 級別)"""
    try:
        tree = ast.parse(code)
        import_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    import_names.append(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_names.append(node.module.split('.')[0])

        stdlib = {'os', 'sys', 'json', 're', 'datetime', 'typing', 'asyncio', 'time', 'math', 'hashlib',
                  'collections', 'functools', 'itertools', 'pathlib', 'subprocess', 'threading',
                  'multiprocessing', 'logging', 'unittest', 'argparse', 'copy', 'io', 'tempfile'}
        used = [name for name in import_names if name in stdlib]

        return {
            "layer": 10,
            "name": "標準庫檢查",
            "passed": True,
            "message": f"精確識別出 {len(set(used))} 個標準庫導入",
            "stdlib_used": list(set(used))
        }
    except Exception as e:
        return {"layer": 10, "name": "標準庫檢查", "passed": False, "message": f"分析失敗: {e}"}


def validate_l11_third_party(code: str) -> Dict:
    """L11: 第三方庫檢查"""
    third_party = {'django', 'flask', 'fastapi', 'requests', 'numpy', 'pandas',
                   'pytest', 'aiohttp', 'sqlalchemy', 'pydantic', 'httpx', 'redis',
                   'celery', 'boto3', 'tensorflow', 'torch', 'scikit-learn'}

    used_third_party = []
    for module in third_party:
        if f"import {module}" in code or f"from {module}" in code:
            used_third_party.append(module)

    return {
        "layer": 11,
        "name": "第三方庫檢查",
        "passed": True,
        "message": f"使用了 {len(used_third_party)} 個第三方庫" if used_third_party else "未使用第三方庫",
        "third_party_used": used_third_party
    }


def validate_l12_circular_deps(code: str) -> Dict:
    """L12: 循環依賴檢查 (AST 探測)"""
    try:
        tree = ast.parse(code)
        relative_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level > 0:
                module = node.module or ""
                relative_imports.append(f"{'.' * node.level}{module}")

        if relative_imports:
            return {
                "layer": 12,
                "name": "循環依賴檢查",
                "passed": False,
                "message": f"檢測到 {len(relative_imports)} 個相對導入，可能存在循環依賴風險",
                "relative_imports": relative_imports
            }
        else:
            return {
                "layer": 12,
                "name": "循環依賴檢查",
                "passed": True,
                "message": "通過 (未檢測到危險的相對導入)"
            }
    except Exception as e:
        return {"layer": 12, "name": "循環依賴檢查", "passed": False, "message": f"分析失敗: {e}"}


def print_report(results: List[Dict], verbose: bool = False):
    """打印驗證報告"""
    print(f"\n{'='*50}")
    print("L9-L12: 依賴關係驗證")
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
        if verbose:
            if 'stdlib_used' in layer and layer['stdlib_used']:
                print(f"    標準庫: {', '.join(layer['stdlib_used'])}")
            if 'third_party_used' in layer and layer['third_party_used']:
                print(f"    第三方: {', '.join(layer['third_party_used'])}")
            if 'relative_imports' in layer and layer['relative_imports']:
                print(f"    相對導入: {', '.join(layer['relative_imports'])}")

    print()


def main():
    parser = argparse.ArgumentParser(description='BlueMouse L9-L12: 依賴關係驗證')
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

    results = validate_dependencies(code)

    if args.json:
        output = {
            "group": "L9-L12: 依賴關係驗證",
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

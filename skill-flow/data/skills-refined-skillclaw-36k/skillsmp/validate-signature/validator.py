#!/usr/bin/env python3
"""
BlueMouse L5-L8: 函數簽名驗證
獨立版本 - 可作為 Claude Code Skill 使用

用法:
    python validator.py <file.py>
    python validator.py --code "def foo(): pass"
    python validator.py --spec spec.json <file.py>
"""

import ast
import sys
import json
import argparse
from typing import Dict, List, Optional


def validate_function_signature(code: str, spec: Optional[Dict] = None) -> List[Dict]:
    """L5-L8: 函數簽名驗證"""
    results = []
    results.append(validate_l5_parameters(code, spec))
    results.append(validate_l6_return_value(code, spec))
    results.append(validate_l7_type_hints(code))
    results.append(validate_l8_docstring(code))
    return results


def validate_l5_parameters(code: str, spec: Optional[Dict]) -> Dict:
    """L5: 參數檢查"""
    try:
        tree = ast.parse(code)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        if not functions:
            return {
                "layer": 5,
                "name": "參數檢查",
                "passed": False,
                "message": "未找到函數定義"
            }

        func = functions[0]

        if spec and 'inputs' in spec:
            expected_params = set(spec['inputs'])
            actual_params = set(arg.arg for arg in func.args.args)

            if expected_params == actual_params:
                return {
                    "layer": 5,
                    "name": "參數檢查",
                    "passed": True,
                    "message": "參數與規格匹配"
                }
            else:
                return {
                    "layer": 5,
                    "name": "參數檢查",
                    "passed": False,
                    "message": f"參數不匹配: 期望 {expected_params}, 實際 {actual_params}"
                }
        else:
            return {
                "layer": 5,
                "name": "參數檢查",
                "passed": True,
                "message": f"函數有 {len(func.args.args)} 個參數"
            }
    except Exception as e:
        return {
            "layer": 5,
            "name": "參數檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def validate_l6_return_value(code: str, spec: Optional[Dict]) -> Dict:
    """L6: 返回值檢查"""
    try:
        tree = ast.parse(code)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        if not functions:
            return {
                "layer": 6,
                "name": "返回值檢查",
                "passed": False,
                "message": "未找到函數定義"
            }

        func = functions[0]
        has_return = any(isinstance(node, ast.Return) for node in ast.walk(func))

        if has_return:
            return {
                "layer": 6,
                "name": "返回值檢查",
                "passed": True,
                "message": "函數有返回值"
            }
        else:
            return {
                "layer": 6,
                "name": "返回值檢查",
                "passed": False,
                "message": "函數缺少返回值"
            }
    except Exception as e:
        return {
            "layer": 6,
            "name": "返回值檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def validate_l7_type_hints(code: str) -> Dict:
    """L7: 類型提示檢查"""
    try:
        tree = ast.parse(code)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        if not functions:
            return {
                "layer": 7,
                "name": "類型提示檢查",
                "passed": False,
                "message": "未找到函數定義"
            }

        func = functions[0]
        params_with_hints = sum(1 for arg in func.args.args if arg.annotation)
        total_params = len(func.args.args)
        has_return_hint = func.returns is not None

        if total_params > 0:
            hint_coverage = params_with_hints / total_params
        else:
            hint_coverage = 1.0 if has_return_hint else 0.0

        if hint_coverage >= 0.8 and has_return_hint:
            return {
                "layer": 7,
                "name": "類型提示檢查",
                "passed": True,
                "message": f"類型提示覆蓋率: {hint_coverage*100:.0f}%"
            }
        else:
            return {
                "layer": 7,
                "name": "類型提示檢查",
                "passed": False,
                "message": f"類型提示不足: {hint_coverage*100:.0f}%"
            }
    except Exception as e:
        return {
            "layer": 7,
            "name": "類型提示檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def validate_l8_docstring(code: str) -> Dict:
    """L8: 文檔字符串檢查"""
    try:
        tree = ast.parse(code)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        if not functions:
            return {
                "layer": 8,
                "name": "文檔字符串檢查",
                "passed": False,
                "message": "未找到函數定義"
            }

        func = functions[0]
        docstring = ast.get_docstring(func)

        if docstring and len(docstring) > 10:
            return {
                "layer": 8,
                "name": "文檔字符串檢查",
                "passed": True,
                "message": f"有完整文檔字符串 ({len(docstring)} 字符)"
            }
        else:
            return {
                "layer": 8,
                "name": "文檔字符串檢查",
                "passed": False,
                "message": "缺少或文檔字符串過短"
            }
    except Exception as e:
        return {
            "layer": 8,
            "name": "文檔字符串檢查",
            "passed": False,
            "message": f"檢查失敗: {str(e)}"
        }


def print_report(results: List[Dict], verbose: bool = False):
    """打印驗證報告"""
    print(f"\n{'='*50}")
    print("L5-L8: 函數簽名驗證")
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

    print()


def main():
    parser = argparse.ArgumentParser(description='BlueMouse L5-L8: 函數簽名驗證')
    parser.add_argument('file', nargs='?', help='Python file to validate')
    parser.add_argument('--code', '-c', help='Code string to validate')
    parser.add_argument('--stdin', action='store_true', help='Read code from stdin')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--spec', '-s', help='JSON spec file for validation')

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

    spec = None
    if args.spec:
        try:
            with open(args.spec, 'r', encoding='utf-8') as f:
                spec = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load spec file: {e}", file=sys.stderr)

    results = validate_function_signature(code, spec)

    if args.json:
        output = {
            "group": "L5-L8: 函數簽名驗證",
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

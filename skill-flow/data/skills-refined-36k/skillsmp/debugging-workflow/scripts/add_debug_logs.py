#!/usr/bin/env python3
"""
소스 파일에 디버그 로그 자동 삽입

Usage:
    python add_debug_logs.py <source_file> [--dry-run]
"""

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import List, Tuple


def detect_language(file_path: Path) -> str:
    """파일 확장자로 언어 감지"""
    ext = file_path.suffix.lower()
    mapping = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
    }
    return mapping.get(ext, "unknown")


def find_functions_python(content: str) -> List[Tuple[int, str, List[str]]]:
    """Python 함수 찾기: (line_number, function_name, parameters)"""
    functions = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [arg.arg for arg in node.args.args]
                functions.append((node.lineno, node.name, params))
    except SyntaxError:
        # 파싱 실패 시 정규식 폴백
        pattern = r"def\s+(\w+)\s*\((.*?)\):"
        for match in re.finditer(pattern, content):
            line_num = content[: match.start()].count("\n") + 1
            func_name = match.group(1)
            params = [
                p.strip().split(":")[0].split("=")[0].strip()
                for p in match.group(2).split(",")
                if p.strip()
            ]
            functions.append((line_num, func_name, params))
    return functions


def find_functions_typescript(content: str) -> List[Tuple[int, str, List[str]]]:
    """TypeScript/JavaScript 함수 찾기"""
    functions = []
    patterns = [
        r"function\s+(\w+)\s*\((.*?)\)",  # function name()
        r"(\w+)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>",  # const name = () =>
        r"(\w+)\s*\((.*?)\)\s*{",  # method(params) {
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            line_num = content[: match.start()].count("\n") + 1
            func_name = match.group(1)
            params = [
                p.strip().split(":")[0].split("=")[0].strip()
                for p in match.group(2).split(",")
                if p.strip()
            ]
            functions.append((line_num, func_name, params))

    return functions


def generate_debug_code_python(func_name: str, params: List[str]) -> str:
    """Python 디버그 코드 생성"""
    lines = []
    lines.append("    import logging")
    lines.append("    logger = logging.getLogger(__name__)")

    # ENTRY 로그
    if params:
        param_log = ", ".join([f"{p}={{repr({p})}}" for p in params if p != "self"])
        lines.append(f'    logger.debug(f"[ENTRY] {func_name}: {param_log}")')
    else:
        lines.append(f'    logger.debug("[ENTRY] {func_name}")')

    return "\n".join(lines)


def generate_debug_code_typescript(func_name: str, params: List[str]) -> str:
    """TypeScript 디버그 코드 생성"""
    lines = []
    lines.append("    const DEBUG = true;")
    lines.append("    const debugLog = (tag: string, msg: string, data?: any) => {")
    lines.append('        if (DEBUG) console.log(`[${tag}] ${msg}`, data ?? "");')
    lines.append("    };")

    if params:
        param_obj = ", ".join([f"{p}" for p in params])
        lines.append(f'    debugLog("ENTRY", "{func_name}", {{ {param_obj} }});')
    else:
        lines.append(f'    debugLog("ENTRY", "{func_name}");')

    return "\n".join(lines)


def add_debug_logs(file_path: Path, dry_run: bool = False) -> str:
    """파일에 디버그 로그 추가"""
    content = file_path.read_text(encoding="utf-8")
    language = detect_language(file_path)

    if language == "python":
        functions = find_functions_python(content)
        generate_fn = generate_debug_code_python
    elif language in ("typescript", "javascript"):
        functions = find_functions_typescript(content)
        generate_fn = generate_debug_code_typescript
    else:
        print(f"❌ 지원하지 않는 언어: {language}")
        sys.exit(1)

    if not functions:
        print("⚠️  함수를 찾을 수 없습니다.")
        return content

    print(f"\n📝 {file_path.name}에서 {len(functions)}개 함수 발견")

    # 라인 번호 역순으로 정렬 (뒤에서부터 삽입해야 라인 번호 유지)
    functions.sort(key=lambda x: x[0], reverse=True)

    lines = content.split("\n")

    for line_num, func_name, params in functions:
        print(f"   🔧 {func_name}() at line {line_num}")

        debug_code = generate_fn(func_name, params)

        # 함수 정의 다음 줄에 삽입
        insert_idx = line_num  # 0-indexed 기준으로 함수 정의 다음 줄
        lines.insert(insert_idx, debug_code)

    new_content = "\n".join(lines)

    if dry_run:
        print("\n🔍 [DRY RUN] 변경될 내용:")
        print("-" * 40)
        for i, line in enumerate(new_content.split("\n")[:50], 1):
            print(f"{i:4}: {line}")
        if len(new_content.split("\n")) > 50:
            print("... (truncated)")
    else:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"\n✅ 디버그 로그가 추가되었습니다: {file_path}")

    return new_content


def main():
    parser = argparse.ArgumentParser(description="소스 파일에 디버그 로그 자동 삽입")
    parser.add_argument("source_file", help="소스 파일 경로")
    parser.add_argument(
        "--dry-run", "-n", action="store_true", help="실제 수정 없이 미리보기"
    )

    args = parser.parse_args()

    source_path = Path(args.source_file)
    if not source_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {source_path}")
        sys.exit(1)

    add_debug_logs(source_path, args.dry_run)


if __name__ == "__main__":
    main()

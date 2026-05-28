#!/usr/bin/env python3
"""
Red Phase 검증: 테스트가 올바르게 실패하는지 확인

Usage:
    python validate_red_phase.py <test_file> [--strict]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    return Path.cwd()


def find_implementation_file(test_file: Path) -> Path | None:
    """테스트 파일에 대응하는 구현 파일 찾기"""
    # test_feature.py → feature.py
    test_name = test_file.stem
    if test_name.startswith("test_"):
        impl_name = test_name[5:]  # Remove "test_" prefix
    else:
        impl_name = test_name

    # 가능한 구현 파일 경로들
    project_root = _get_project_root()
    possible_paths = [
        project_root / "src" / f"{impl_name}.py",
        project_root / "src" / impl_name / "__init__.py",
        project_root / f"{impl_name}.py",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def run_pytest(test_file: Path) -> tuple[int, str, str]:
    """pytest 실행"""
    try:
        result = subprocess.run(
            ["pytest", str(test_file), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def analyze_failure(stdout: str, stderr: str) -> dict:
    """실패 원인 분석"""
    output = stdout + stderr

    expected_errors = {
        "ModuleNotFoundError": "모듈을 찾을 수 없음 (구현 필요)",
        "ImportError": "임포트 실패 (구현 필요)",
        "AttributeError": "속성/메서드 없음 (구현 필요)",
        "NameError": "이름 정의 안 됨 (구현 필요)",
        "AssertionError": "단언 실패 (로직 구현 필요)",
        "NotImplementedError": "미구현 표시 (구현 필요)",
    }

    found_errors = []
    for error_type, description in expected_errors.items():
        if error_type in output:
            found_errors.append((error_type, description))

    unexpected_errors = []
    unexpected_patterns = ["SyntaxError", "IndentationError", "TypeError"]
    for pattern in unexpected_patterns:
        if pattern in output:
            unexpected_errors.append(pattern)

    return {
        "expected": found_errors,
        "unexpected": unexpected_errors,
        "is_valid_red": len(found_errors) > 0 and len(unexpected_errors) == 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Red Phase 검증")
    parser.add_argument("test_file", help="테스트 파일 경로")
    parser.add_argument(
        "--strict", action="store_true", help="엄격 모드 (구현 파일 존재 시 에러)"
    )

    args = parser.parse_args()
    test_file = Path(args.test_file)

    print("🔴 Red Phase 검증 시작")
    print(f"   테스트 파일: {test_file}")
    print()

    # 1. 테스트 파일 존재 확인
    if not test_file.exists():
        print(f"❌ 테스트 파일을 찾을 수 없습니다: {test_file}")
        sys.exit(1)

    # 2. 구현 파일 존재 확인
    impl_file = find_implementation_file(test_file)
    if impl_file:
        if args.strict:
            print(f"❌ RED phase에서 구현 파일이 이미 존재합니다: {impl_file}")
            print("   TDD 규칙: 테스트를 먼저 작성해야 합니다!")
            sys.exit(1)
        else:
            print(f"⚠️  구현 파일이 존재합니다: {impl_file}")
            print("   (--strict 모드에서는 에러)")

    # 3. 테스트 실행
    print("테스트 실행 중...")
    code, stdout, stderr = run_pytest(test_file)

    # 4. 결과 분석
    if code == 0:
        print()
        print("❌ RED phase 검증 실패!")
        print()
        print("테스트가 통과했습니다. 이는 잘못된 TDD입니다!")
        print("올바른 TDD에서는 구현이 없을 때 테스트가 실패해야 합니다.")
        print()
        print("가능한 원인:")
        print("  1. 테스트가 너무 약함 (assertion 부족)")
        print("  2. Mock/Stub으로 가짜 구현")
        print("  3. 이미 구현이 존재함")
        sys.exit(1)

    # 5. 실패 원인 분석
    analysis = analyze_failure(stdout, stderr)

    print()
    if analysis["is_valid_red"]:
        print("✅ RED Phase 검증 통과!")
        print()
        print("테스트가 올바르게 실패했습니다.")
        print()
        print("발견된 예상 에러:")
        for error_type, desc in analysis["expected"]:
            print(f"  ✓ {error_type}: {desc}")
        print()
        print("다음 단계: GREEN Phase (최소 구현 작성)")
        print("  1. 테스트를 통과하는 최소한의 코드 작성")
        print("  2. pytest 실행하여 통과 확인")
        print('  3. git commit -m "feat: ... (GREEN) 🟢"')
    else:
        print("⚠️  RED Phase 경고")
        print()
        if analysis["unexpected"]:
            print("예상치 못한 에러 발견:")
            for error in analysis["unexpected"]:
                print(f"  ✗ {error}")
            print()
            print("테스트 파일에 문법 오류가 있을 수 있습니다.")

        if not analysis["expected"]:
            print("예상된 TDD 에러가 발견되지 않았습니다.")
            print("테스트가 올바르게 작성되었는지 확인하세요.")

        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
TDD 자동 사이클: Write → Test → Adjust → Test (최대 N회 반복)

Usage:
    python tdd_auto_cycle.py <test_file> [--max-iterations 5] [--verbose]
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime


class TDDCycle:
    """TDD 자동 사이클 관리"""

    def __init__(self, test_file: Path, max_iterations: int = 5, verbose: bool = False):
        self.test_file = test_file
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.iteration = 0
        self.history = []

    def log(self, message: str, level: str = "INFO"):
        """로그 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}.get(
            level, ""
        )
        print(f"[{timestamp}] {prefix} {message}")

    def run_tests(self) -> tuple[bool, str, list[dict]]:
        """테스트 실행 및 결과 파싱"""
        try:
            result = subprocess.run(
                ["pytest", str(self.test_file), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=120,
            )

            passed = result.returncode == 0
            output = result.stdout + result.stderr

            # 실패한 테스트 파싱
            failures = []
            if not passed:
                # FAILED 패턴 찾기
                import re

                failed_pattern = r"FAILED\s+(\S+)::(\S+)"
                for match in re.finditer(failed_pattern, output):
                    failures.append(
                        {
                            "file": match.group(1),
                            "test": match.group(2),
                        }
                    )

                # 에러 메시지 추출
                error_pattern = (
                    r"(AssertionError|AttributeError|ImportError|NameError):\s*(.+)"
                )
                for match in re.finditer(error_pattern, output):
                    if failures:
                        failures[-1]["error_type"] = match.group(1)
                        failures[-1]["error_msg"] = match.group(2)[:100]

            return passed, output, failures

        except subprocess.TimeoutExpired:
            return False, "Timeout", []
        except Exception as e:
            return False, str(e), []

    def analyze_failures(self, failures: list[dict]) -> dict:
        """실패 원인 분석 및 수정 제안"""
        suggestions = []

        for failure in failures:
            error_type = failure.get("error_type", "Unknown")
            test_name = failure.get("test", "")

            if error_type == "ImportError":
                suggestions.append(
                    {
                        "type": "create_module",
                        "message": f"모듈 생성 필요: {test_name}에서 임포트 실패",
                        "action": "구현 파일 생성",
                    }
                )
            elif error_type == "AttributeError":
                suggestions.append(
                    {
                        "type": "add_method",
                        "message": f"메서드/속성 추가 필요: {failure.get('error_msg', '')}",
                        "action": "메서드 구현",
                    }
                )
            elif error_type == "AssertionError":
                suggestions.append(
                    {
                        "type": "fix_logic",
                        "message": f"로직 수정 필요: {test_name}",
                        "action": "반환값 또는 로직 수정",
                    }
                )
            elif error_type == "NameError":
                suggestions.append(
                    {
                        "type": "define_name",
                        "message": f"이름 정의 필요: {failure.get('error_msg', '')}",
                        "action": "변수/함수 정의",
                    }
                )

        return {"total_failures": len(failures), "suggestions": suggestions}

    def run_cycle(self) -> bool:
        """TDD 사이클 실행"""
        self.log(f"TDD 자동 사이클 시작: {self.test_file}")
        self.log(f"최대 반복: {self.max_iterations}회")
        print()

        for i in range(1, self.max_iterations + 1):
            self.iteration = i
            print("=" * 60)
            self.log(f"Iteration {i}/{self.max_iterations}")
            print("=" * 60)

            # 테스트 실행
            self.log("테스트 실행 중...")
            passed, output, failures = self.run_tests()

            # 결과 저장
            self.history.append(
                {"iteration": i, "passed": passed, "failures": len(failures)}
            )

            if passed:
                print()
                self.log("모든 테스트 통과!", "SUCCESS")
                self.log(f"TDD 사이클 완료 (Iteration {i})")
                print()
                self.print_summary()
                return True

            # 실패 분석
            self.log(f"테스트 실패: {len(failures)}개", "WARN")

            if self.verbose:
                print()
                print("실패한 테스트:")
                for f in failures[:5]:
                    print(
                        f"  - {f.get('test', 'unknown')}: {f.get('error_type', 'Error')}"
                    )

            # 수정 제안
            analysis = self.analyze_failures(failures)
            print()
            self.log("수정 제안:")
            for suggestion in analysis["suggestions"][:3]:
                print(f"  💡 {suggestion['message']}")
                print(f"     → {suggestion['action']}")

            if i < self.max_iterations:
                print()
                self.log("다음 iteration으로 진행...")
                print()
                time.sleep(1)

        # 최대 반복 도달
        print()
        self.log(
            f"TDD 사이클 실패: {self.max_iterations}회 반복 후에도 테스트 실패", "ERROR"
        )
        self.log("수동 개입이 필요합니다.", "ERROR")
        self.log("다음 명령 실행: /issue-failed", "ERROR")
        print()
        self.print_summary()
        return False

    def print_summary(self):
        """결과 요약 출력"""
        print("=" * 60)
        print("TDD 사이클 요약")
        print("=" * 60)
        print(f"테스트 파일: {self.test_file}")
        print(f"총 반복: {len(self.history)}회")
        print()
        print("Iteration 히스토리:")
        for h in self.history:
            status = "✅ PASS" if h["passed"] else f"❌ FAIL ({h['failures']})"
            print(f"  #{h['iteration']}: {status}")


def main():
    parser = argparse.ArgumentParser(description="TDD 자동 사이클")
    parser.add_argument("test_file", help="테스트 파일 경로")
    parser.add_argument(
        "--max-iterations", "-n", type=int, default=5, help="최대 반복 횟수 (기본: 5)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 출력")

    args = parser.parse_args()
    test_file = Path(args.test_file)

    if not test_file.exists():
        print(f"❌ 테스트 파일을 찾을 수 없습니다: {test_file}")
        sys.exit(1)

    cycle = TDDCycle(test_file, args.max_iterations, args.verbose)
    success = cycle.run_cycle()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
통합 코드 품질 검사

Usage:
    python run_quality_check.py [--python-only] [--fix] [--strict]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    return Path.cwd()


@dataclass
class CheckResult:
    name: str
    passed: bool
    output: str
    fixable: bool = False


class QualityChecker:
    """통합 코드 품질 검사"""

    def __init__(
        self, project_root: Path = None, fix: bool = False, strict: bool = False
    ):
        self.project_root = project_root or _get_project_root()
        self.fix = fix
        self.strict = strict
        self.results: list[CheckResult] = []

    def run_command(self, command: list[str], cwd: Path = None) -> tuple[int, str]:
        """명령 실행"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
            )
            return result.returncode, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return -1, "Timeout"
        except FileNotFoundError:
            return -2, f"Command not found: {command[0]}"
        except Exception as e:
            return -1, str(e)

    def check_ruff(self) -> CheckResult:
        """Ruff 린트 검사"""
        print("🔍 Ruff 린트 검사...")

        if self.fix:
            code, output = self.run_command(["ruff", "check", "src/", "--fix"])
        else:
            code, output = self.run_command(["ruff", "check", "src/"])

        return CheckResult(
            name="ruff",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=True,
        )

    def check_black(self) -> CheckResult:
        """Black 포맷 검사"""
        print("🔍 Black 포맷 검사...")

        if self.fix:
            code, output = self.run_command(["black", "src/"])
        else:
            code, output = self.run_command(["black", "--check", "src/"])

        return CheckResult(
            name="black",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=True,
        )

    def check_mypy(self) -> CheckResult:
        """Mypy 타입 검사"""
        print("🔍 Mypy 타입 검사...")

        cmd = ["mypy", "src/"]
        if self.strict:
            cmd.append("--strict")

        code, output = self.run_command(cmd)

        return CheckResult(
            name="mypy",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=False,
        )

    def check_pip_audit(self) -> CheckResult:
        """Python 의존성 보안 검사"""
        print("🔍 pip-audit 보안 검사...")

        cmd = ["pip-audit"]
        if self.strict:
            cmd.append("--strict")

        code, output = self.run_command(cmd)

        return CheckResult(
            name="pip-audit",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=False,
        )

    def check_eslint(self) -> CheckResult:
        """ESLint 검사 (TypeScript)"""
        if not (self.project_root / "package.json").exists():
            return CheckResult(
                name="eslint", passed=True, output="Skipped (no package.json)"
            )

        print("🔍 ESLint 검사...")

        if self.fix:
            code, output = self.run_command(["npx", "eslint", "src/", "--fix"])
        else:
            code, output = self.run_command(["npx", "eslint", "src/"])

        return CheckResult(
            name="eslint",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=True,
        )

    def check_npm_audit(self) -> CheckResult:
        """npm 의존성 보안 검사"""
        if not (self.project_root / "package.json").exists():
            return CheckResult(
                name="npm-audit", passed=True, output="Skipped (no package.json)"
            )

        print("🔍 npm audit 보안 검사...")

        level = "critical" if not self.strict else "high"
        code, output = self.run_command(["npm", "audit", f"--audit-level={level}"])

        return CheckResult(
            name="npm-audit",
            passed=code == 0,
            output=output[:500] if code != 0 else "OK",
            fixable=False,
        )

    def run_all(self, python_only: bool = False) -> bool:
        """전체 검사 실행"""
        print("=" * 60)
        print("🔍 코드 품질 검사 시작")
        print(f"   프로젝트: {self.project_root}")
        print(f"   모드: {'자동 수정' if self.fix else '검사만'}")
        print(f"   수준: {'엄격' if self.strict else '기본'}")
        print("=" * 60)
        print()

        # Python 검사
        self.results.append(self.check_ruff())
        self.results.append(self.check_black())
        self.results.append(self.check_mypy())
        self.results.append(self.check_pip_audit())

        # TypeScript 검사 (옵션)
        if not python_only:
            self.results.append(self.check_eslint())
            self.results.append(self.check_npm_audit())

        # 결과 출력
        self.print_results()

        return all(r.passed for r in self.results)

    def print_results(self):
        """결과 출력"""
        print()
        print("=" * 60)
        print("📊 검사 결과")
        print("=" * 60)

        passed_count = sum(1 for r in self.results if r.passed)
        total_count = len(self.results)

        for result in self.results:
            status = "✅" if result.passed else "❌"
            fix_hint = " (--fix 가능)" if not result.passed and result.fixable else ""
            print(f"  {status} {result.name}{fix_hint}")

            if not result.passed and result.output != "OK":
                for line in result.output.split("\n")[:3]:
                    if line.strip():
                        print(f"      {line.strip()[:70]}")

        print()
        print(f"통과: {passed_count}/{total_count}")

        if passed_count == total_count:
            print()
            print("✅ 모든 검사 통과!")
        else:
            print()
            print("❌ 일부 검사 실패")

            # 자동 수정 제안
            fixable = [r for r in self.results if not r.passed and r.fixable]
            if fixable and not self.fix:
                print()
                print("💡 자동 수정 가능한 이슈:")
                for r in fixable:
                    print(f"   - {r.name}")
                print()
                print("실행: python run_quality_check.py --fix")


def main():
    parser = argparse.ArgumentParser(description="통합 코드 품질 검사")
    parser.add_argument("--python-only", action="store_true", help="Python만 검사")
    parser.add_argument("--fix", action="store_true", help="자동 수정 적용")
    parser.add_argument("--strict", action="store_true", help="엄격 모드")
    parser.add_argument("--project", type=str, help="프로젝트 루트 경로")

    args = parser.parse_args()

    project_root = Path(args.project) if args.project else None

    checker = QualityChecker(project_root, args.fix, args.strict)
    success = checker.run_all(args.python_only)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

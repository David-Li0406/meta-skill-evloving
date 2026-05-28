#!/usr/bin/env python3
"""
Phase 0-6 통합 검증

Usage:
    python validate_phase.py --status
    python validate_phase.py --phase 2
    python validate_phase.py --auto-advance
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    return Path.cwd()


class PhaseStatus(Enum):
    PENDING = "⏳"
    IN_PROGRESS = "🔄"
    PASSED = "✅"
    FAILED = "❌"
    BLOCKED = "⏸️"


@dataclass
class PhaseResult:
    phase: str
    name: str
    status: PhaseStatus
    message: str = ""


class PhaseValidator:
    """Phase 0-6 통합 검증"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or _get_project_root()
        self.scripts_dir = self.project_root / "scripts"
        self.results: list[PhaseResult] = []

    def run_ps1(self, script_name: str, *args) -> tuple[int, str]:
        """PowerShell 스크립트 실행"""
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            return -1, f"Script not found: {script_path}"

        try:
            cmd = ["powershell", "-File", str(script_path)] + list(args)
            result = subprocess.run(
                cmd, cwd=self.project_root, capture_output=True, text=True, timeout=120
            )
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    def validate_phase_0(self) -> PhaseResult:
        """Phase 0: PRD 생성 검증"""
        prds = list((self.project_root / "tasks" / "prds").glob("PRD-*.md"))

        if not prds:
            return PhaseResult("0", "PRD 생성", PhaseStatus.PENDING, "PRD 파일 없음")

        latest_prd = max(prds, key=lambda p: p.stat().st_mtime)
        lines = len(latest_prd.read_text(encoding="utf-8").splitlines())

        if lines < 50:
            return PhaseResult(
                "0", "PRD 생성", PhaseStatus.IN_PROGRESS, f"PRD 작성 중 ({lines}/50줄)"
            )

        return PhaseResult(
            "0", "PRD 생성", PhaseStatus.PASSED, f"PRD 완료: {latest_prd.name}"
        )

    def validate_phase_05(self) -> PhaseResult:
        """Phase 0.5: Task 분해 검증"""
        tasks = list((self.project_root / "tasks").glob("PRD-*-tasks.md"))

        if not tasks:
            return PhaseResult(
                "0.5", "Task 분해", PhaseStatus.PENDING, "Task 파일 없음"
            )

        latest_task = max(tasks, key=lambda p: p.stat().st_mtime)
        content = latest_task.read_text(encoding="utf-8")

        # 체크리스트 항목 카운트
        total = content.count("- [ ]") + content.count("- [x]")
        completed = content.count("- [x]")

        if total == 0:
            return PhaseResult(
                "0.5", "Task 분해", PhaseStatus.IN_PROGRESS, "체크리스트 없음"
            )

        if completed == total:
            return PhaseResult(
                "0.5",
                "Task 분해",
                PhaseStatus.PASSED,
                f"완료: {completed}/{total} tasks",
            )

        return PhaseResult(
            "0.5",
            "Task 분해",
            PhaseStatus.IN_PROGRESS,
            f"진행 중: {completed}/{total} tasks",
        )

    def validate_phase_1(self) -> PhaseResult:
        """Phase 1: 구현 + 테스트 검증"""
        src_files = list((self.project_root / "src").rglob("*.py"))
        src_files = [f for f in src_files if not f.name.startswith("__")]

        if not src_files:
            return PhaseResult(
                "1", "구현 + 테스트", PhaseStatus.PENDING, "구현 파일 없음"
            )

        # 1:1 테스트 페어링 확인
        paired = 0
        for src_file in src_files:
            test_name = f"test_{src_file.stem}.py"
            test_files = list((self.project_root / "tests").rglob(test_name))
            if test_files:
                paired += 1

        ratio = paired / len(src_files) * 100 if src_files else 0

        if ratio >= 80:
            return PhaseResult(
                "1",
                "구현 + 테스트",
                PhaseStatus.PASSED,
                f"페어링: {paired}/{len(src_files)} ({ratio:.0f}%)",
            )

        return PhaseResult(
            "1",
            "구현 + 테스트",
            PhaseStatus.IN_PROGRESS,
            f"페어링: {paired}/{len(src_files)} ({ratio:.0f}%)",
        )

    def validate_phase_2(self) -> PhaseResult:
        """Phase 2: 테스트 통과 검증"""
        try:
            result = subprocess.run(
                ["pytest", "tests/", "-v", "--tb=no", "-q"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                return PhaseResult("2", "테스트 통과", PhaseStatus.PASSED, "100% 통과")

            # 실패 테스트 카운트
            output = result.stdout
            if "passed" in output:
                import re

                match = re.search(r"(\d+) passed", output)
                passed = int(match.group(1)) if match else 0
                match = re.search(r"(\d+) failed", output)
                failed = int(match.group(1)) if match else 0
                total = passed + failed
                return PhaseResult(
                    "2",
                    "테스트 통과",
                    PhaseStatus.IN_PROGRESS,
                    f"{passed}/{total} 통과",
                )

            return PhaseResult("2", "테스트 통과", PhaseStatus.FAILED, "테스트 실패")

        except Exception as e:
            return PhaseResult("2", "테스트 통과", PhaseStatus.FAILED, str(e)[:50])

    def validate_phase_25(self) -> PhaseResult:
        """Phase 2.5: 코드 리뷰 검증"""
        # ruff check
        try:
            result = subprocess.run(
                ["ruff", "check", "src/"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                return PhaseResult("2.5", "코드 리뷰", PhaseStatus.FAILED, "ruff 오류")

            # black check
            result = subprocess.run(
                ["black", "--check", "src/"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                return PhaseResult(
                    "2.5", "코드 리뷰", PhaseStatus.FAILED, "black 포맷 오류"
                )

            return PhaseResult("2.5", "코드 리뷰", PhaseStatus.PASSED, "린트 통과")

        except FileNotFoundError:
            return PhaseResult("2.5", "코드 리뷰", PhaseStatus.PENDING, "도구 미설치")
        except Exception as e:
            return PhaseResult("2.5", "코드 리뷰", PhaseStatus.FAILED, str(e)[:50])

    def validate_phase_3(self) -> PhaseResult:
        """Phase 3: 버전 결정"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            commits = result.stdout.strip().split("\n")

            # Conventional Commits 확인
            has_feat = any("feat" in c.lower() for c in commits)
            has_fix = any("fix" in c.lower() for c in commits)
            has_breaking = any("!" in c or "BREAKING" in c.upper() for c in commits)

            if has_breaking:
                version_type = "MAJOR"
            elif has_feat:
                version_type = "MINOR"
            elif has_fix:
                version_type = "PATCH"
            else:
                version_type = "PATCH"

            return PhaseResult(
                "3", "버전 결정", PhaseStatus.PASSED, f"{version_type} 버전"
            )

        except Exception as e:
            return PhaseResult("3", "버전 결정", PhaseStatus.FAILED, str(e)[:50])

    def validate_phase_4(self) -> PhaseResult:
        """Phase 4: PR 생성"""
        try:
            result = subprocess.run(
                ["gh", "pr", "view", "--json", "state,title"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                import json

                pr_info = json.loads(result.stdout)
                state = pr_info.get("state", "unknown")
                title = pr_info.get("title", "")[:30]
                return PhaseResult(
                    "4", "PR 생성", PhaseStatus.PASSED, f"{state}: {title}"
                )

            return PhaseResult("4", "PR 생성", PhaseStatus.PENDING, "PR 없음")

        except Exception as e:
            return PhaseResult("4", "PR 생성", PhaseStatus.PENDING, str(e)[:50])

    def validate_phase_5(self) -> PhaseResult:
        """Phase 5: E2E + Security"""
        code, output = self.run_ps1("validate-phase-5.ps1")

        if code == 0:
            return PhaseResult("5", "E2E + Security", PhaseStatus.PASSED, "검증 완료")
        elif "critical" in output.lower():
            return PhaseResult(
                "5", "E2E + Security", PhaseStatus.BLOCKED, "Critical 취약점"
            )
        else:
            return PhaseResult("5", "E2E + Security", PhaseStatus.FAILED, "검증 실패")

    def validate_phase_6(self) -> PhaseResult:
        """Phase 6: 배포"""
        return PhaseResult("6", "배포", PhaseStatus.BLOCKED, "사용자 확인 필요")

    def validate_all(self) -> list[PhaseResult]:
        """전체 Phase 검증"""
        self.results = [
            self.validate_phase_0(),
            self.validate_phase_05(),
            self.validate_phase_1(),
            self.validate_phase_2(),
            self.validate_phase_25(),
            self.validate_phase_3(),
            self.validate_phase_4(),
            self.validate_phase_5(),
            self.validate_phase_6(),
        ]
        return self.results

    def print_status(self):
        """상태 출력"""
        print("=" * 60)
        print("📊 Phase Pipeline 상태")
        print("=" * 60)
        print()

        for result in self.results:
            print(f"  Phase {result.phase:4} {result.status.value} {result.name}")
            if result.message:
                print(f"            └─ {result.message}")

        print()

        # 현재 Phase 확인
        current = None
        for result in self.results:
            if result.status in [PhaseStatus.IN_PROGRESS, PhaseStatus.PENDING]:
                current = result
                break

        if current:
            print(f"현재 Phase: {current.phase} ({current.name})")
        else:
            print("모든 Phase 완료!")

    def validate_phase(self, phase: str) -> PhaseResult:
        """특정 Phase 검증"""
        validators = {
            "0": self.validate_phase_0,
            "0.5": self.validate_phase_05,
            "1": self.validate_phase_1,
            "2": self.validate_phase_2,
            "2.5": self.validate_phase_25,
            "3": self.validate_phase_3,
            "4": self.validate_phase_4,
            "5": self.validate_phase_5,
            "6": self.validate_phase_6,
        }

        validator = validators.get(phase)
        if not validator:
            print(f"❌ 알 수 없는 Phase: {phase}")
            sys.exit(1)

        result = validator()
        print(f"Phase {result.phase} {result.status.value} {result.name}")
        if result.message:
            print(f"  {result.message}")

        return result


def main():
    parser = argparse.ArgumentParser(description="Phase 0-6 통합 검증")
    parser.add_argument("--status", action="store_true", help="전체 상태 확인")
    parser.add_argument(
        "--phase", type=str, help="특정 Phase 검증 (0, 0.5, 1, 2, 2.5, 3, 4, 5, 6)"
    )
    parser.add_argument(
        "--auto-advance", action="store_true", help="다음 Phase로 자동 진행"
    )
    parser.add_argument("--project", type=str, help="프로젝트 루트 경로")

    args = parser.parse_args()

    project_root = Path(args.project) if args.project else None
    validator = PhaseValidator(project_root)

    if args.status:
        validator.validate_all()
        validator.print_status()
    elif args.phase:
        result = validator.validate_phase(args.phase)
        sys.exit(0 if result.status == PhaseStatus.PASSED else 1)
    elif args.auto_advance:
        validator.validate_all()
        validator.print_status()
        print()
        print("자동 진행은 아직 구현되지 않았습니다.")
        print("각 Phase를 수동으로 검증하세요.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

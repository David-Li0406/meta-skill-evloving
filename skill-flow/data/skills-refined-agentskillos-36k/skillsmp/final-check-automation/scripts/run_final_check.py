#!/usr/bin/env python3
"""
FINAL_CHECK 자동화 스크립트

Usage:
    python run_final_check.py [--e2e-only] [--security-only] [--skip-phase-6]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    return Path.cwd()


class FinalCheck:
    """FINAL_CHECK 워크플로우 자동화"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or _get_project_root()
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.log_file = (
            self.logs_dir / f"final_check_{datetime.now():%Y%m%d_%H%M%S}.log"
        )
        self.results = {
            "e2e": None,
            "phase3": None,
            "phase4": None,
            "phase5": None,
            "phase6": "pending",
        }

    def log(self, message: str, level: str = "INFO"):
        """로그 출력 및 파일 저장"""
        timestamp = datetime.now().isoformat()
        log_line = f"{timestamp} [{level}] {message}"
        print(log_line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")

    def run_command(
        self, command: str | list, cwd: Path = None
    ) -> tuple[int, str, str]:
        """명령 실행"""
        if isinstance(command, str):
            command = command.split()

        self.log(f"실행: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=600,  # 10분 타임아웃
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except Exception as e:
            return -1, "", str(e)

    def step1_e2e_tests(self, max_retries: int = 3) -> bool:
        """Step 1: E2E 테스트"""
        self.log("=" * 60)
        self.log("Step 1: E2E 테스트 시작")
        self.log("=" * 60)

        for attempt in range(1, max_retries + 1):
            self.log(f"시도 {attempt}/{max_retries}")

            # Playwright 테스트 실행
            code, stdout, stderr = self.run_command(["npx", "playwright", "test"])

            if code == 0:
                self.log("✅ E2E 테스트 통과")
                self.results["e2e"] = "passed"
                return True

            self.log(f"❌ E2E 테스트 실패 (시도 {attempt})", "ERROR")
            self.log(f"stdout: {stdout[:500]}", "DEBUG")
            self.log(f"stderr: {stderr[:500]}", "DEBUG")

            if attempt < max_retries:
                self.log("자동 수정 시도 중...")
                # 여기서 자동 수정 로직 호출 가능
                # 예: playwright-engineer 에이전트 호출

        self.log("❌ E2E 테스트 3회 실패 - 수동 개입 필요", "ERROR")
        self.log("다음 명령 실행: /issue-failed", "ERROR")
        self.results["e2e"] = "failed"
        return False

    def step2_phase3_version(self) -> bool:
        """Step 2: Phase 3 (버전 결정)"""
        self.log("=" * 60)
        self.log("Step 2: Phase 3 (버전 결정)")
        self.log("=" * 60)

        # 최근 커밋 분석
        code, stdout, _ = self.run_command(["git", "log", "--oneline", "-20"])
        if code != 0:
            self.log("❌ Git 로그 조회 실패", "ERROR")
            return False

        commits = stdout.strip().split("\n")
        self.log(f"최근 커밋 {len(commits)}개 분석")

        # 버전 결정 로직
        has_breaking = any("!" in c or "BREAKING" in c.upper() for c in commits)
        has_feat = any("feat:" in c.lower() or "feat(" in c.lower() for c in commits)
        has_fix = any("fix:" in c.lower() or "fix(" in c.lower() for c in commits)

        if has_breaking:
            version_type = "MAJOR"
            self.log("⚠️ MAJOR 버전 변경 감지 - 사용자 확인 필요", "WARN")
        elif has_feat:
            version_type = "MINOR"
        elif has_fix:
            version_type = "PATCH"
        else:
            version_type = "PATCH"

        self.log(f"버전 유형: {version_type}")

        # 현재 버전 확인
        code, stdout, _ = self.run_command(["git", "describe", "--tags", "--abbrev=0"])
        current_version = stdout.strip() if code == 0 else "v0.0.0"
        self.log(f"현재 버전: {current_version}")

        self.results["phase3"] = f"{version_type} (from {current_version})"

        if has_breaking:
            self.log("⏸️ MAJOR 버전 - 자동 진행 중지", "WARN")
            return False

        return True

    def step3_phase4_pr(self) -> bool:
        """Step 3: Phase 4 (PR 생성)"""
        self.log("=" * 60)
        self.log("Step 3: Phase 4 (PR 생성)")
        self.log("=" * 60)

        # PR 존재 확인
        code, stdout, _ = self.run_command(["gh", "pr", "view", "--json", "state"])
        if code == 0:
            self.log("PR이 이미 존재합니다")
            self.results["phase4"] = "existing"
            return True

        # Phase 4 검증
        code, stdout, stderr = self.run_command(
            ["powershell", "-File", "scripts/validate-phase-4.ps1"]
        )

        if code == 0:
            self.log("✅ Phase 4 검증 통과")
            self.results["phase4"] = "passed"
            return True

        self.log(f"❌ Phase 4 검증 실패: {stderr}", "ERROR")
        self.results["phase4"] = "failed"
        return False

    def step4_phase5_security(self) -> bool:
        """Step 4: Phase 5 (보안 검증)"""
        self.log("=" * 60)
        self.log("Step 4: Phase 5 (보안 검증)")
        self.log("=" * 60)

        issues = []

        # pip-audit (Python)
        self.log("Python 의존성 스캔...")
        code, stdout, _ = self.run_command(["pip-audit", "--strict"])
        if code != 0:
            issues.append("Python 의존성 취약점 발견")
            self.log("⚠️ pip-audit 경고", "WARN")

        # npm audit (Node.js)
        if (self.project_root / "package.json").exists():
            self.log("npm 의존성 스캔...")
            code, stdout, _ = self.run_command(["npm", "audit", "--audit-level=high"])
            if code != 0:
                issues.append("npm 의존성 취약점 발견")
                self.log("⚠️ npm audit 경고", "WARN")

        # Phase 5 검증
        code, stdout, stderr = self.run_command(
            ["powershell", "-File", "scripts/validate-phase-5.ps1"]
        )

        if code == 0:
            self.log("✅ Phase 5 검증 통과")
            self.results["phase5"] = "passed"
            return True

        # Critical 취약점 확인
        if "critical" in stderr.lower():
            self.log("❌ Critical 보안 취약점 - 자동 진행 중지", "ERROR")
            self.results["phase5"] = "critical_vulnerability"
            return False

        self.log(f"⚠️ Phase 5 경고: {len(issues)}개 이슈", "WARN")
        self.results["phase5"] = f"warning ({len(issues)} issues)"
        return True

    def step5_phase6_deploy(self) -> bool:
        """Step 5: Phase 6 (배포) - 항상 사용자 확인 필요"""
        self.log("=" * 60)
        self.log("Step 5: Phase 6 (배포)")
        self.log("=" * 60)

        self.log("⏸️ 배포는 사용자 확인이 필요합니다.", "WARN")
        self.log("")
        self.log("배포 체크리스트:")
        self.log("  [ ] 모든 테스트 통과")
        self.log("  [ ] 보안 스캔 통과")
        self.log("  [ ] PR 승인됨")
        self.log("  [ ] 릴리스 노트 작성")
        self.log("")

        self.results["phase6"] = "awaiting_approval"
        return True

    def print_summary(self):
        """결과 요약 출력"""
        self.log("")
        self.log("=" * 60)
        self.log("FINAL_CHECK 결과 요약")
        self.log("=" * 60)

        status_emoji = {
            "passed": "✅",
            "failed": "❌",
            "warning": "⚠️",
            "pending": "⏳",
            "existing": "📋",
            "awaiting_approval": "🔐",
        }

        for step, result in self.results.items():
            if result is None:
                emoji = "⏭️"
                result = "skipped"
            elif "passed" in str(result):
                emoji = "✅"
            elif "failed" in str(result) or "critical" in str(result):
                emoji = "❌"
            elif "warning" in str(result):
                emoji = "⚠️"
            else:
                emoji = status_emoji.get(result, "📋")

            self.log(f"  {emoji} {step}: {result}")

        self.log("")
        self.log(f"로그 파일: {self.log_file}")

    def run(
        self,
        e2e_only: bool = False,
        security_only: bool = False,
        skip_phase6: bool = False,
    ) -> bool:
        """전체 FINAL_CHECK 실행"""
        self.log("🚀 FINAL_CHECK 시작")
        self.log(f"프로젝트: {self.project_root}")
        self.log("")

        success = True

        # E2E 테스트
        if not security_only:
            if not self.step1_e2e_tests():
                success = False
                if not e2e_only:
                    self.print_summary()
                    return False

        if e2e_only:
            self.print_summary()
            return success

        # Phase 3-5
        if not security_only:
            if not self.step2_phase3_version():
                success = False
                self.print_summary()
                return False

            if not self.step3_phase4_pr():
                success = False

        # 보안 검증
        if not self.step4_phase5_security():
            success = False

        # Phase 6 (항상 사용자 확인)
        if not skip_phase6:
            self.step5_phase6_deploy()

        self.print_summary()

        if success:
            self.log("✅ FINAL_CHECK 완료 - 배포 준비됨")
        else:
            self.log("❌ FINAL_CHECK 실패 - 이슈 해결 필요")

        return success


def main():
    parser = argparse.ArgumentParser(description="FINAL_CHECK 자동화")
    parser.add_argument("--e2e-only", action="store_true", help="E2E 테스트만 실행")
    parser.add_argument("--security-only", action="store_true", help="보안 스캔만 실행")
    parser.add_argument(
        "--skip-phase6", action="store_true", help="Phase 6 (배포) 스킵"
    )
    parser.add_argument("--project", type=str, help="프로젝트 루트 경로")

    args = parser.parse_args()

    project_root = Path(args.project) if args.project else None

    checker = FinalCheck(project_root)
    success = checker.run(
        e2e_only=args.e2e_only,
        security_only=args.security_only,
        skip_phase6=args.skip_phase6,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

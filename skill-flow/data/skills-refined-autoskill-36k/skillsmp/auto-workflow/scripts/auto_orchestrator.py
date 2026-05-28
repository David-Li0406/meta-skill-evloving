"""
Auto Orchestrator - 자율 작업 루프 엔진 (v2.0)

Claude Code를 외부에서 호출하여 자율적으로 작업을 반복 수행합니다.
- 5계층 우선순위 기반 작업 발견
- 9개 커맨드 자동 트리거
- Context 80%/90% 예측 기반 관리
- 병렬 처리 지원
- E2E 4방향 병렬 검증
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

# 상대 임포트를 위한 경로 설정
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from auto_discovery import (
    AutoDiscovery,
    DiscoveredTask,
    CONTEXT_ESTIMATES,
)  # noqa: E402
from auto_state import AutoState, CONTEXT_THRESHOLDS  # noqa: E402
from context_predictor import ContextPredictor, predict_and_decide  # noqa: E402


class LoopStatus(Enum):
    """루프 상태"""

    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CONTEXT_LIMIT = "context_limit"
    CONTEXT_CLEANUP = "context_cleanup"  # 80%/90% 도달 시 정리 후 재시작


@dataclass
class LoopConfig:
    """루프 설정"""

    max_iterations: Optional[int] = None  # --max N
    promise_text: Optional[str] = None  # --promise TEXT
    dry_run: bool = False  # --dry-run
    skip_validation: bool = False  # --skip-validation (검증 생략)
    verbose: bool = True
    context_limit: int = 90  # Context % 임계값
    cooldown_seconds: int = 5  # 반복 간 대기 시간
    retry_on_error: int = 3  # 에러 시 재시도 횟수
    max_debug_attempts: int = 3  # E2E 실패 시 최대 디버그 시도


@dataclass
class ValidationResult:
    """검증 결과"""

    passed: bool
    test_type: str  # "e2e" or "tdd"
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    coverage_percent: float = 0.0
    error_message: Optional[str] = None
    details: Optional[dict] = None


@dataclass
class IterationResult:
    """반복 결과"""

    success: bool
    task: Optional[DiscoveredTask]
    output: str
    duration_seconds: float
    promise_fulfilled: bool = False
    error: Optional[str] = None
    e2e_result: Optional[ValidationResult] = None
    tdd_result: Optional[ValidationResult] = None


class AutoOrchestrator:
    """자율 작업 루프 오케스트레이터 (v2.0)"""

    def __init__(
        self,
        config: LoopConfig,
        project_root: str = None,
        session_id: Optional[str] = None,
        is_session_start: bool = True,
    ):
        self.config = config
        self.is_session_start = is_session_start
        self.discovery = AutoDiscovery(project_root, is_session_start=is_session_start)
        # 동적 프로젝트 루트 감지 (discovery에서 감지한 경로 사용)
        self.project_root = self.discovery.project_root

        # 상태 관리
        self.state = AutoState(
            session_id=session_id, original_request="자율 판단 루프 (v2.0)"
        )
        self.session_id = self.state.session_id

        # Context 예측기
        self.context_predictor = ContextPredictor(0)

        # 통계
        self.iteration_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.start_time = datetime.now()
        self.current_context_percent = 0

        # 콜백
        self.on_iteration_start: Optional[Callable] = None
        self.on_iteration_end: Optional[Callable] = None
        self.on_task_discovered: Optional[Callable] = None
        self.on_context_cleanup: Optional[Callable] = None

    def run(self) -> LoopStatus:
        """메인 루프 실행"""
        self._log_start()
        status = LoopStatus.RUNNING

        try:
            while status == LoopStatus.RUNNING:
                # 종료 조건 체크
                status = self._check_termination()
                if status != LoopStatus.RUNNING:
                    break

                # 반복 실행
                result = self._run_iteration()

                # 결과 처리
                status = self._process_result(result)

                # 쿨다운
                if status == LoopStatus.RUNNING:
                    time.sleep(self.config.cooldown_seconds)

        except KeyboardInterrupt:
            status = LoopStatus.PAUSED
            self._log("사용자 중단 (Ctrl+C)")

        except Exception as e:
            status = LoopStatus.FAILED
            self._log(f"오류 발생: {e}")
            self.state.logger.log_error(str(e))

        finally:
            self._finalize(status)

        return status

    def _check_termination(self) -> LoopStatus:
        """종료 조건 체크"""
        # 1. --max 체크
        if self.config.max_iterations:
            if self.iteration_count >= self.config.max_iterations:
                self._log(f"최대 반복 횟수 도달: {self.config.max_iterations}")
                return LoopStatus.COMPLETED

        # 2. 연속 실패 체크
        if self.failure_count >= self.config.retry_on_error:
            self._log(f"연속 실패 {self.failure_count}회 - 중단")
            return LoopStatus.FAILED

        # 3. Context 90% 체크 (즉시 정리)
        if self.current_context_percent >= CONTEXT_THRESHOLDS["critical"]:
            self._log(f"⚠️  Context {self.current_context_percent}% >= 90% (임계값)")
            return LoopStatus.CONTEXT_CLEANUP

        return LoopStatus.RUNNING

    def _check_context_before_task(
        self, task: DiscoveredTask
    ) -> tuple[bool, Optional[dict]]:
        """
        작업 전 Context 체크 (80% 이상일 때)

        Returns:
            (진행 가능 여부, 예측 결과)
        """
        if self.current_context_percent < CONTEXT_THRESHOLDS["prepare"]:
            return True, None  # 80% 미만 - 진행 가능

        # 80% 이상 - 예측 분석
        task_info = {
            "type": task.task_type,
            "affected_files": task.affected_files,
            "complexity": task.complexity,
        }

        result = predict_and_decide(
            self.current_context_percent, task_info, threshold=20
        )

        self._log("\n📊 Context 예측 분석:")
        self._log(f"   현재: {self.current_context_percent}%")
        self._log(f"   예상 추가: {result['estimate'].adjusted_estimate}%")
        self._log(f"   결정: {result['action']}")

        if result["action"] == "cleanup":
            self._log(f"   ⚠️  {result['message']}")
            return False, result

        return True, result

    def _run_context_cleanup(self) -> bool:
        """
        Context 정리 실행 (commit → clear → auto 재시작)

        Returns:
            정리 성공 여부
        """
        self._log("\n🧹 Context 정리 시작...")

        try:
            import shutil

            claude_path = shutil.which("claude") or "claude"

            # 1. 세션 문서 업데이트
            self._log("   [1/4] 세션 문서 업데이트...")
            self._update_session_docs()

            # 2. /commit 실행
            self._log("   [2/4] /commit 실행...")
            commit_result = subprocess.run(
                [claude_path, "-p", "/commit"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.project_root,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32"),
            )

            if commit_result.returncode != 0:
                self._log("   ⚠️  커밋 실패 (변경사항 없을 수 있음)")

            # 3. 체크포인트 저장
            self._log("   [3/4] 체크포인트 저장...")
            self.state.create_checkpoint(
                task_id=self.iteration_count,
                task_content=f"Context 정리 후 재개 (Iteration {self.iteration_count})",
                context_hint=f"Context {self.current_context_percent}% 도달로 정리",
                todo_state=[],
            )

            # 4. /clear 실행은 외부에서 처리 (subprocess 종료 후)
            self._log("   [4/4] 정리 완료 - /clear 후 재시작 필요")

            # 상태 업데이트
            self.state.increment_clear_count()
            self.state.set_status("paused")

            # 콜백 호출
            if self.on_context_cleanup:
                self.on_context_cleanup(self.current_context_percent)

            return True

        except Exception as e:
            self._log(f"   ❌ 정리 실패: {e}")
            return False

    def _update_session_docs(self):
        """세션 문서 업데이트 (진행 상황 기록)"""
        # .claude/sessions/에 현재 상태 기록
        sessions_dir = self.project_root / ".claude" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        session_file = sessions_dir / f"{self.session_id}.md"

        content = f"""# 세션: {self.session_id}

## 상태
- 반복 횟수: {self.iteration_count}
- 성공: {self.success_count}
- 실패: {self.failure_count}
- Context: {self.current_context_percent}%
- 마지막 업데이트: {datetime.now().isoformat()}

## 진행 상황
{self.state.get_resume_summary()}
"""
        session_file.write_text(content, encoding="utf-8")

    def update_context_percent(self, percent: int):
        """Context 사용량 업데이트 (외부에서 호출)"""
        self.current_context_percent = percent
        self.context_predictor.update_current(percent)
        self.state.update_context_usage(percent)

    def _run_iteration(self) -> IterationResult:
        """단일 반복 실행"""
        self.iteration_count += 1
        start = time.time()

        self._log(f"\n{'='*60}")
        self._log(
            f"[Iteration {self.iteration_count}] 시작 | Context: {self.current_context_percent}%"
        )
        self._log(f"{'='*60}")

        if self.on_iteration_start:
            self.on_iteration_start(self.iteration_count)

        # 세션 시작 후 is_session_start 플래그 해제
        if self.is_session_start:
            self.is_session_start = False
            self.discovery.is_session_start = False

        # 1. 작업 발견
        task = self.discovery.discover_next_task()

        if not task:
            self._log("✅ 모든 검사 통과 - 자율 발견 모드 대기")
            return IterationResult(
                success=True,
                task=None,
                output="No tasks found - autonomous mode",
                duration_seconds=time.time() - start,
            )

        # 작업 발견 로깅
        self._log("\n📋 발견된 작업:")
        self._log(f"   우선순위: P{task.priority.value} ({task.category})")
        self._log(f"   제목: {task.title}")
        self._log(f"   설명: {task.description}")
        self._log(f"   명령: {task.command}")
        self._log(f"   병렬 에이전트: {task.parallel_agents}")
        self._log(f"   예상 Context: {CONTEXT_ESTIMATES.get(task.task_type, 15)}%")

        # 2. Context 예측 체크 (80% 이상일 때)
        can_proceed, prediction = self._check_context_before_task(task)
        if not can_proceed:
            self._log("\n⚠️  Context 예측 초과 - 정리 필요")
            self._run_context_cleanup()
            return IterationResult(
                success=True,
                task=task,
                output="Context cleanup triggered",
                duration_seconds=time.time() - start,
                error="context_cleanup_needed",
            )

        if self.on_task_discovered:
            self.on_task_discovered(task)

        # 로그 기록
        self.state.logger.log(
            event_type="decision", phase="discovery", data=task.to_dict()
        )

        # 2. Dry-run 모드
        if self.config.dry_run:
            self._log("\n🔍 [DRY-RUN] 실행하지 않음")
            return IterationResult(
                success=True,
                task=task,
                output="Dry run - not executed",
                duration_seconds=time.time() - start,
            )

        # 3. Claude Code 호출
        output, success = self._execute_task(task)

        # 4. E2E 검증 (작업 성공 시 + skip_validation이 False일 때)
        e2e_result = None
        if success and not self.config.skip_validation:
            e2e_result = self._run_e2e_tests()

            # E2E 실패 시 디버그 자동 트리거
            if not e2e_result.passed:
                self._log("\n❌ E2E 테스트 실패 - 디버그 모드 진입")
                debug_success = self._trigger_debug(e2e_result)

                if debug_success:
                    # 디버그 후 재검증
                    e2e_result = self._run_e2e_tests()
                    if e2e_result.passed:
                        self._log("✅ E2E 재검증 통과")
                    else:
                        self._log("❌ E2E 재검증 실패 - 다음 반복에서 재시도")
                        success = False

        # 5. TDD 검증 (E2E 통과 시)
        tdd_result = None
        if (
            success
            and e2e_result
            and e2e_result.passed
            and not self.config.skip_validation
        ):
            tdd_result = self._run_tdd_tests()

            if not tdd_result.passed:
                self._log(
                    f"⚠️  TDD 검증 경고 - 커버리지: {tdd_result.coverage_percent:.1f}%"
                )
                # TDD 실패는 경고만 (작업은 성공으로 간주)

        # 6. Promise 체크
        promise_fulfilled = False
        if self.config.promise_text:
            promise_tag = f"<promise>{self.config.promise_text}</promise>"
            if promise_tag in output:
                promise_fulfilled = True
                self._log(f"\n🎯 Promise 충족: {self.config.promise_text}")

        duration = time.time() - start
        self._log(f"\n⏱️  소요 시간: {duration:.1f}초")

        return IterationResult(
            success=success,
            task=task,
            output=output,
            duration_seconds=duration,
            promise_fulfilled=promise_fulfilled,
            e2e_result=e2e_result,
            tdd_result=tdd_result,
        )

    def _execute_task(self, task: DiscoveredTask) -> tuple[str, bool]:
        """작업 실행 - debate 작업은 별도 처리"""
        # Tier 3.5: Ultimate Debate 작업 감지
        if task.task_type.startswith("debate_") or "ultimate-debate" in task.command:
            return self._run_debate(task)

        self._log(f"\n🚀 Claude Code 실행: {task.command}")

        try:
            # Claude Code 호출
            # Windows에서는 shell=True 필요 (PATH에서 claude.cmd 찾기)
            import shutil

            claude_path = shutil.which("claude")
            if not claude_path:
                claude_path = "claude"  # fallback

            result = subprocess.run(
                [claude_path, "-p", task.command],
                capture_output=True,
                text=True,
                timeout=600,  # 10분 타임아웃
                cwd=self.project_root,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32"),  # Windows에서만 shell=True
            )

            output = result.stdout + result.stderr
            success = result.returncode == 0

            # 로그 기록
            self.state.logger.log_action(
                action="claude_execute",
                target=task.command,
                result="success" if success else "fail",
                details={"returncode": result.returncode},
            )

            if success:
                self.success_count += 1
                self.failure_count = 0  # 연속 실패 카운트 리셋
                self._log("✅ 실행 성공")
            else:
                self.failure_count += 1
                self._log(f"❌ 실행 실패 (returncode: {result.returncode})")

            return output, success

        except subprocess.TimeoutExpired:
            self.failure_count += 1
            self._log("⏰ 타임아웃 (10분 초과)")
            return "Timeout", False

        except FileNotFoundError:
            self._log("❌ Claude Code를 찾을 수 없습니다")
            self._log("   'claude' 명령어가 PATH에 있는지 확인하세요")
            return "Claude not found", False

        except Exception as e:
            self.failure_count += 1
            self._log(f"❌ 실행 오류: {e}")
            return str(e), False

    def _run_e2e_tests(self) -> ValidationResult:
        """E2E 테스트 실행 (Playwright)"""
        self._log("\n🧪 Phase 4: E2E 검증 중...")

        try:
            # Playwright 테스트 실행
            result = subprocess.run(
                ["npx", "playwright", "test"],
                capture_output=True,
                text=True,
                timeout=300,  # 5분 타임아웃
                cwd=self.project_root,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32"),
            )

            # 결과 파싱 (간단한 패턴 매칭)
            output = result.stdout + result.stderr
            passed = result.returncode == 0

            # 테스트 개수 파싱 (예: "15 passed, 0 failed")
            import re

            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)

            passed_tests = int(passed_match.group(1)) if passed_match else 0
            failed_tests = int(failed_match.group(1)) if failed_match else 0
            total_tests = passed_tests + failed_tests

            validation_result = ValidationResult(
                passed=passed,
                test_type="e2e",
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_message=None if passed else "E2E tests failed",
                details={"output": output[:500]},  # 처음 500자만
            )

            # 로그 기록
            self.state.logger.log(
                event_type="milestone",
                phase="e2e_validation",
                data={"passed": passed, "total": total_tests, "failed": failed_tests},
            )

            if passed:
                self._log(f"   ✅ E2E 테스트 통과 ({passed_tests}/{total_tests})")
            else:
                self._log(f"   ❌ E2E 테스트 실패 ({passed_tests}/{total_tests})")

            return validation_result

        except subprocess.TimeoutExpired:
            self._log("   ⏰ E2E 테스트 타임아웃 (5분 초과)")
            return ValidationResult(
                passed=False, test_type="e2e", error_message="Timeout after 5 minutes"
            )

        except FileNotFoundError:
            self._log("   ⚠️  Playwright가 설치되지 않음 - E2E 검증 생략")
            return ValidationResult(
                passed=True,  # 설치 안 된 경우 통과로 간주
                test_type="e2e",
                error_message="Playwright not installed",
            )

        except Exception as e:
            self._log(f"   ❌ E2E 테스트 오류: {e}")
            return ValidationResult(passed=False, test_type="e2e", error_message=str(e))

    def _run_tdd_tests(self) -> ValidationResult:
        """TDD 테스트 실행 (pytest + coverage)"""
        self._log("\n📊 Phase 5: TDD 검증 중...")

        try:
            # pytest 실행 (커버리지 포함)
            result = subprocess.run(
                ["pytest", "tests/", "-v", "--cov=src", "--cov-report=json"],
                capture_output=True,
                text=True,
                timeout=120,  # 2분 타임아웃
                cwd=self.project_root,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32"),
            )

            output = result.stdout + result.stderr
            passed = result.returncode == 0

            # 테스트 개수 파싱
            import re

            passed_match = re.search(r"(\d+) passed", output)
            failed_match = re.search(r"(\d+) failed", output)

            passed_tests = int(passed_match.group(1)) if passed_match else 0
            failed_tests = int(failed_match.group(1)) if failed_match else 0
            total_tests = passed_tests + failed_tests

            # 커버리지 파싱 (coverage.json)
            coverage_percent = 0.0
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                try:
                    with open(coverage_file, "r") as f:
                        coverage_data = json.load(f)
                        coverage_percent = coverage_data.get("totals", {}).get(
                            "percent_covered", 0.0
                        )
                except Exception:
                    pass

            # 검증 기준: 테스트 통과 + 커버리지 80% 이상
            validation_passed = passed and coverage_percent >= 80.0

            validation_result = ValidationResult(
                passed=validation_passed,
                test_type="tdd",
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                coverage_percent=coverage_percent,
                error_message=(
                    None
                    if validation_passed
                    else f"Coverage {coverage_percent:.1f}% < 80%"
                ),
                details={"output": output[:500]},
            )

            # 로그 기록
            self.state.logger.log(
                event_type="milestone",
                phase="tdd_validation",
                data={
                    "passed": validation_passed,
                    "total": total_tests,
                    "failed": failed_tests,
                    "coverage": coverage_percent,
                },
            )

            if validation_passed:
                self._log(
                    f"   ✅ TDD 검증 통과 ({passed_tests}/{total_tests}, 커버리지: {coverage_percent:.1f}%)"
                )
            else:
                self._log(
                    f"   ⚠️  TDD 검증 부족 ({passed_tests}/{total_tests}, 커버리지: {coverage_percent:.1f}%)"
                )

            return validation_result

        except subprocess.TimeoutExpired:
            self._log("   ⏰ TDD 테스트 타임아웃 (2분 초과)")
            return ValidationResult(
                passed=False, test_type="tdd", error_message="Timeout after 2 minutes"
            )

        except FileNotFoundError:
            self._log("   ⚠️  pytest가 설치되지 않음 - TDD 검증 생략")
            return ValidationResult(
                passed=True,  # 설치 안 된 경우 통과로 간주
                test_type="tdd",
                error_message="pytest not installed",
            )

        except Exception as e:
            self._log(f"   ❌ TDD 테스트 오류: {e}")
            return ValidationResult(passed=False, test_type="tdd", error_message=str(e))

    def _run_debate(self, task: DiscoveredTask) -> tuple[str, bool]:
        """Ultimate Debate 엔진으로 3AI 토론 실행

        Args:
            task: 토론 작업 정보

        Returns:
            (출력, 성공 여부)
        """
        self._log(f"\n🎯 Ultimate Debate 시작: {task.title}")
        self._log("   Claude/GPT/Gemini 3AI 토론")

        try:
            import asyncio
            import sys

            # ultimate-debate 모듈 경로 추가
            debate_path = self.project_root / "src"
            if str(debate_path) not in sys.path:
                sys.path.insert(0, str(debate_path))

            from ultimate_debate.engine import UltimateDebate
            from ultimate_debate.clients import ClaudeClient, OpenAIClient, GeminiClient

            # 태스크 설명 추출
            task_description = task.details.get("context") or task.description

            # 토론 엔진 초기화
            debate = UltimateDebate(
                task=task_description,
                max_rounds=5,
                consensus_threshold=0.8,
            )

            # 3AI 클라이언트 등록
            self._log("   [1/4] AI 클라이언트 초기화...")
            clients_registered = 0

            try:
                claude_client = ClaudeClient()
                if asyncio.get_event_loop().run_until_complete(
                    claude_client.ensure_authenticated()
                ):
                    debate.register_ai_client("claude", claude_client)
                    clients_registered += 1
                    self._log("      ✅ Claude 등록")
            except Exception as e:
                self._log(f"      ⚠️  Claude 등록 실패: {e}")

            try:
                openai_client = OpenAIClient()
                if asyncio.get_event_loop().run_until_complete(
                    openai_client.ensure_authenticated()
                ):
                    debate.register_ai_client("gpt", openai_client)
                    clients_registered += 1
                    self._log("      ✅ GPT 등록")
            except Exception as e:
                self._log(f"      ⚠️  GPT 등록 실패: {e}")

            try:
                gemini_client = GeminiClient()
                if asyncio.get_event_loop().run_until_complete(
                    gemini_client.ensure_authenticated()
                ):
                    debate.register_ai_client("gemini", gemini_client)
                    clients_registered += 1
                    self._log("      ✅ Gemini 등록")
            except Exception as e:
                self._log(f"      ⚠️  Gemini 등록 실패: {e}")

            if clients_registered < 2:
                self._log("   ❌ 최소 2개 AI 필요 - 토론 취소")
                return "Insufficient AI clients for debate", False

            self._log(f"   [2/4] 토론 실행 ({clients_registered}개 AI)...")

            # 토론 실행
            result = asyncio.get_event_loop().run_until_complete(debate.run())

            # 결과 처리
            self._log("   [3/4] 결과 분석...")
            consensus_pct = result.get("consensus_percentage", 0) * 100
            status = result.get("status", "UNKNOWN")
            total_rounds = result.get("total_rounds", 0)

            self._log(f"      상태: {status}")
            self._log(f"      합의율: {consensus_pct:.1f}%")
            self._log(f"      라운드: {total_rounds}")

            # FINAL.md 위치
            final_md = self.project_root / ".claude" / "debates" / result.get("task_id", "") / "FINAL.md"

            # 로그 기록
            self.state.logger.log(
                event_type="debate_completed",
                phase="tier3_5",
                data={
                    "task_id": result.get("task_id"),
                    "status": status,
                    "consensus_percentage": consensus_pct,
                    "total_rounds": total_rounds,
                    "final_md": str(final_md) if final_md.exists() else None,
                },
            )

            self._log("   [4/4] 토론 완료")

            success = status == "FULL_CONSENSUS" or consensus_pct >= 50
            if success:
                self.success_count += 1
                self.failure_count = 0
                self._log(f"   ✅ 토론 성공 (합의율: {consensus_pct:.1f}%)")
            else:
                self.failure_count += 1
                self._log(f"   ⚠️  토론 완료 - 합의 미달 (합의율: {consensus_pct:.1f}%)")

            # 결과 요약
            output = f"""
=== Ultimate Debate 결과 ===
상태: {status}
합의율: {consensus_pct:.1f}%
라운드: {total_rounds}
Task ID: {result.get('task_id')}
FINAL.md: {final_md if final_md.exists() else '생성되지 않음'}

합의 항목:
{json.dumps(result.get('agreed_items', []), ensure_ascii=False, indent=2)}

미합의 항목:
{json.dumps(result.get('disputed_items', []), ensure_ascii=False, indent=2)}
"""
            return output, success

        except ImportError as e:
            self._log(f"   ❌ ultimate-debate 모듈 로드 실패: {e}")
            return f"ImportError: {e}", False

        except Exception as e:
            self._log(f"   ❌ 토론 실행 오류: {e}")
            self.failure_count += 1
            return str(e), False

    def _trigger_debug(self, e2e_result: ValidationResult) -> bool:
        """E2E 실패 시 디버그 자동 트리거"""
        self._log("\n🔍 디버그 모드 시작 (가설-검증 사이클)")

        try:
            # /debug 커맨드 실행
            import shutil

            claude_path = shutil.which("claude") or "claude"

            debug_prompt = f"""E2E 테스트 실패 분석:
- 실패한 테스트: {e2e_result.failed_tests}개
- 오류 메시지: {e2e_result.error_message}

/debug 커맨드로 가설-검증 사이클 시작"""

            result = subprocess.run(
                [claude_path, "-p", debug_prompt],
                capture_output=True,
                text=True,
                timeout=600,  # 10분 타임아웃
                cwd=self.project_root,
                encoding="utf-8",
                errors="replace",
                shell=(sys.platform == "win32"),
            )

            success = result.returncode == 0

            # 로그 기록
            self.state.logger.log_action(
                action="debug_triggered",
                target="e2e_failure",
                result="success" if success else "fail",
                details={
                    "failed_tests": e2e_result.failed_tests,
                    "returncode": result.returncode,
                },
            )

            if success:
                self._log("   ✅ 디버그 완료")
            else:
                self._log("   ❌ 디버그 실패")

            return success

        except subprocess.TimeoutExpired:
            self._log("   ⏰ 디버그 타임아웃 (10분 초과)")
            return False

        except Exception as e:
            self._log(f"   ❌ 디버그 오류: {e}")
            return False

    def _process_result(self, result: IterationResult) -> LoopStatus:
        """결과 처리"""
        # 상태 업데이트
        self.state.update_progress(
            total=self.iteration_count,
            completed=self.success_count,
            in_progress=1 if result.task else 0,
            pending=0,
        )

        if self.on_iteration_end:
            self.on_iteration_end(result)

        # Context 정리 필요한 경우
        if result.error == "context_cleanup_needed":
            return LoopStatus.CONTEXT_CLEANUP

        # Promise 충족 시 완료
        if result.promise_fulfilled:
            return LoopStatus.COMPLETED

        # 작업 없으면 계속 (자율 발견)
        if not result.task:
            self._log("💤 대기 후 재검사...")
            time.sleep(30)  # 30초 대기 후 재검사

        return LoopStatus.RUNNING

    def _finalize(self, status: LoopStatus):
        """종료 처리"""
        duration = (datetime.now() - self.start_time).total_seconds()

        self._log(f"\n{'='*60}")
        self._log(f"루프 종료: {status.value}")
        self._log(f"{'='*60}")
        self._log(f"총 반복: {self.iteration_count}")
        self._log(f"성공: {self.success_count}")
        self._log(f"실패: {self.failure_count}")
        self._log(f"Context: {self.current_context_percent}%")
        self._log(f"총 소요 시간: {duration:.1f}초")

        # 상태 저장
        if status == LoopStatus.PAUSED:
            self.state.set_status("paused")
            # 체크포인트 생성
            self.state.create_checkpoint(
                task_id=self.iteration_count,
                task_content=f"Iteration {self.iteration_count}",
                context_hint="루프 일시 정지",
                todo_state=[],
            )
            self._log("\n💾 체크포인트 저장됨")
            self._log(f"   재개: python auto_orchestrator.py resume {self.session_id}")

        elif status == LoopStatus.CONTEXT_CLEANUP:
            # Context 정리로 인한 종료
            self._run_context_cleanup()
            self._log("\n🔄 Context 정리 완료")
            self._log("   재시작 명령:")
            self._log("   1. /clear")
            self._log(f"   2. python auto_orchestrator.py resume {self.session_id}")
            self._log("   또는: /auto resume")

        elif status == LoopStatus.COMPLETED:
            self.state.complete(
                {
                    "iterations": self.iteration_count,
                    "success": self.success_count,
                    "duration": duration,
                    "context_peak": self.state.state["context_stats"]["peak_usage"],
                }
            )

        elif status == LoopStatus.FAILED:
            self.state.set_status("failed")

    def _log(self, message: str):
        """로깅"""
        if self.config.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")

    def _log_start(self):
        """시작 로깅"""
        self._log(f"\n{'#'*60}")
        self._log("# Auto Orchestrator 시작")
        self._log(f"# Session: {self.session_id}")
        self._log("# 설정:")
        self._log(f"#   max_iterations: {self.config.max_iterations or '무제한'}")
        self._log(f"#   promise: {self.config.promise_text or '없음'}")
        self._log(f"#   dry_run: {self.config.dry_run}")
        self._log(f"#   skip_validation: {self.config.skip_validation}")
        self._log(f"{'#'*60}")

    def get_status(self) -> dict:
        """현재 상태 조회"""
        return {
            "session_id": self.session_id,
            "iteration_count": self.iteration_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "state": self.state.get_status(),
        }


def run_loop(
    max_iterations: Optional[int] = None,
    promise: Optional[str] = None,
    dry_run: bool = False,
    skip_validation: bool = False,
    session_id: Optional[str] = None,
) -> LoopStatus:
    """
    편의 함수: 루프 실행

    Args:
        max_iterations: 최대 반복 횟수
        promise: 종료 조건 텍스트
        dry_run: 실행 없이 판단만
        skip_validation: E2E/TDD 검증 생략
        session_id: 재개할 세션 ID
    """
    config = LoopConfig(
        max_iterations=max_iterations,
        promise_text=promise,
        dry_run=dry_run,
        skip_validation=skip_validation,
    )

    orchestrator = AutoOrchestrator(config=config, session_id=session_id)

    return orchestrator.run()


def resume_session(session_id: str) -> LoopStatus:
    """세션 재개"""
    from auto_state import restore_session

    state, summary = restore_session(session_id)
    print(summary)

    return run_loop(session_id=session_id)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto Orchestrator - 자율 작업 루프")
    parser.add_argument(
        "command", nargs="?", default="run", choices=["run", "resume", "status"]
    )
    parser.add_argument("session_id", nargs="?", help="세션 ID (resume 시)")
    parser.add_argument("--max", type=int, help="최대 반복 횟수")
    parser.add_argument("--promise", type=str, help="종료 조건 텍스트")
    parser.add_argument("--dry-run", action="store_true", help="실행 없이 판단만")
    parser.add_argument(
        "--skip-validation", action="store_true", help="E2E/TDD 검증 생략"
    )

    args = parser.parse_args()

    if args.command == "resume":
        if not args.session_id:
            # 최근 세션 찾기
            from auto_state import get_latest_active_session

            args.session_id = get_latest_active_session()
            if not args.session_id:
                print("재개할 세션이 없습니다")
                sys.exit(1)
        status = resume_session(args.session_id)

    elif args.command == "status":
        from auto_state import get_latest_active_session

        session_id = args.session_id or get_latest_active_session()
        if session_id:
            state = AutoState(session_id)
            import pprint

            pprint.pprint(state.get_status())
        else:
            print("활성 세션이 없습니다")

    else:  # run
        status = run_loop(
            max_iterations=args.max,
            promise=args.promise,
            dry_run=args.dry_run,
            skip_validation=args.skip_validation,
        )
        print(f"\n최종 상태: {status.value}")

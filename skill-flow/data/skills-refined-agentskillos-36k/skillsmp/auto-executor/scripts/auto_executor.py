#!/usr/bin/env python3
"""
auto-executor: Task tool 강제 사용 자동화 엔진

모든 작업을 반드시 Task tool을 통해 서브에이전트에 위임합니다.
"""

import argparse
import sys
import os
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 스크립트 경로 추가
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from session_manager import SessionManager
from task_runner import TaskRunner
from agent_selector import AgentSelector


def detect_project_root() -> Path:
    """
    프로젝트 루트를 감지합니다.

    우선순위:
    1. CWD에 .claude 디렉토리가 있으면 CWD
    2. CWD에서 상위로 탐색하며 .claude 디렉토리 찾기
    3. 스크립트 위치 기반 계산 (fallback)

    이를 통해 서브모듈에서도 해당 서브모듈의 .claude를 인식할 수 있습니다.
    """
    cwd = Path.cwd()

    # 1. CWD에 .claude가 있으면 바로 사용
    if (cwd / ".claude").is_dir():
        return cwd

    # 2. CWD에서 상위로 탐색 (최대 5단계)
    current = cwd
    for _ in range(5):
        if (current / ".claude").is_dir():
            return current
        parent = current.parent
        if parent == current:  # 루트에 도달
            break
        current = parent

    # 3. Fallback: 스크립트 위치 기반 (기존 방식)
    return Path(__file__).parent.parent.parent.parent.parent


def main():
    parser = argparse.ArgumentParser(description="Task tool 강제 사용 자동화 엔진")
    parser.add_argument("--task", "-t", type=str, help="실행할 작업 (없으면 자동 발견)")
    parser.add_argument(
        "--status", "-s", action="store_true", help="현재 세션 상태 출력"
    )
    parser.add_argument("--stop", action="store_true", help="세션 종료 및 최종 보고서")
    parser.add_argument("--redirect", "-r", type=str, help="작업 방향 수정")
    parser.add_argument("--max", type=int, default=0, help="최대 반복 횟수 (0=무한)")
    parser.add_argument("--dry-run", action="store_true", help="실행 없이 계획만 출력")

    args = parser.parse_args()

    # 프로젝트 루트 감지 (CWD 우선, 없으면 스크립트 경로 기반)
    project_root = detect_project_root()

    # 매니저 초기화
    session = SessionManager(project_root)
    runner = TaskRunner(project_root)
    selector = AgentSelector()

    # 모드별 처리
    if args.status:
        print(session.get_status_report())
        return 0

    if args.stop:
        report = session.stop_session()
        print(report)
        return 0

    if args.redirect:
        session.redirect(args.redirect)
        print(f"✅ 방향 수정 완료: {args.redirect}")
        print("다음 작업을 시작하려면 다시 실행하세요.")
        return 0

    # 작업 모드
    iteration = 0
    max_iterations = args.max if args.max > 0 else float("inf")

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"🔄 반복 #{iteration}")
        print(f"{'='*60}")

        # 1. 세션 확인/생성
        session.ensure_session(args.task)

        # 2. 작업 발견
        if args.task and iteration == 1:
            task = args.task
        else:
            task = runner.discover_next_task(session.get_direction())

        if not task:
            print("✅ 모든 작업 완료. 자율 발견 모드로 전환...")
            task = runner.discover_autonomous_task()

            if not task:
                print("💤 발견된 작업 없음. 30초 후 재시도...")
                if args.max > 0:
                    break
                import time

                time.sleep(30)
                continue

        print(f"\n📋 발견된 작업: {task}")

        # 3. 에이전트 선택
        agent = selector.select_agent(task)
        print(f"🤖 선택된 에이전트: {agent}")

        # 4. dry-run 모드
        if args.dry_run:
            print("\n[DRY-RUN] Task tool 호출 예정:")
            print(f"  - subagent_type: {agent}")
            print(f"  - task: {task}")
            continue

        # 5. 에이전트별 실행
        if agent == "verify":
            # verify 에이전트: GPT + Gemini 병렬 검증 직접 실행
            print("\n🔍 Cross-AI Verifier 실행 중 (GPT + Gemini 병렬)...")
            result = runner.execute_verify_parallel(task)
        else:
            # 기타 에이전트: Task tool로 서브에이전트 실행
            print("\n🚀 Task tool로 서브에이전트 실행 중...")
            result = runner.execute_with_task_tool(task, agent)

        # 6. 결과 저장
        session.add_completed_task(task, agent, result)

        # 7. 결과 출력
        print("\n✅ 작업 완료")
        print(f"{'─'*40}")
        print(result.get("summary", "결과 없음"))

        # 8. 자동 Cross-AI 검증 (verify 에이전트가 아닌 경우)
        if agent != "verify":
            verify_info = runner.should_auto_verify(min_changes=50)  # 50줄 이상 변경 시
            if verify_info:
                print(f"\n{'─'*40}")
                print("🔍 자동 Cross-AI 검증 시작 (GPT + Gemini)")
                print(f"   {verify_info['reason']}")
                print(f"{'─'*40}")

                verify_result = runner.execute_verify_parallel(
                    task=f"자동 검증: {task}",
                    target_files=verify_info.get("changed_files"),
                )

                # 검증 결과 저장
                session.add_completed_task(
                    f"[자동검증] {task}", "verify", verify_result
                )

                print("\n🔍 검증 완료")
                print(f"{'─'*40}")
                print(verify_result.get("summary", "검증 결과 없음"))

        # 9. 다음 안내
        stats = session.get_statistics()
        print(f"\n📊 진행 현황: 완료 {stats['completed']}, 대기 {stats['pending']}")
        print("\n다음 작업을 실행하려면 계속 진행합니다...")

        # 단일 실행 모드 (--max 1)
        if args.max == 1:
            print("\n💡 다음 명령어:")
            print("  - 계속: python auto_executor.py")
            print("  - 상태: python auto_executor.py --status")
            print("  - 종료: python auto_executor.py --stop")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python
"""
Auto CLI - 자율 작업 루프 명령줄 인터페이스 (E2E/TDD 검증 포함)

사용법:
    python auto_cli.py                    # 자율 루프 시작 (E2E/TDD 검증 포함)
    python auto_cli.py --max 5            # 최대 5회 반복 + 검증
    python auto_cli.py --skip-validation  # 검증 생략 (빠른 반복)
    python auto_cli.py --dry-run          # 판단만, 실행 안함
    python auto_cli.py resume             # 마지막 세션 재개
    python auto_cli.py resume <session>   # 특정 세션 재개
    python auto_cli.py status             # 현재 상태
    python auto_cli.py discover           # 다음 작업 발견 (1회)
"""

import argparse
import sys
import io
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 경로 설정
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def cmd_run(args):
    """루프 실행"""
    from auto_orchestrator import run_loop

    validation_msg = "검증 생략" if args.skip_validation else "E2E/TDD 검증 포함"

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║          Auto Orchestrator - 자율 작업 루프                ║
    ║                                                            ║
    ║  Ralph Wiggum 철학: "할 일 없음 → 스스로 발견"             ║
    ║  모드: {validation_msg:<44} ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    status = run_loop(
        max_iterations=args.max,
        promise=args.promise,
        dry_run=args.dry_run,
        skip_validation=args.skip_validation,
    )

    return 0 if status.value in ["completed", "paused"] else 1


def cmd_resume(args):
    """세션 재개"""
    from auto_orchestrator import resume_session
    from auto_state import get_latest_active_session

    session_id = args.session_id
    if not session_id:
        session_id = get_latest_active_session()
        if not session_id:
            print("재개할 세션이 없습니다")
            return 1

    print(f"세션 재개: {session_id}")
    status = resume_session(session_id)

    return 0 if status.value in ["completed", "paused"] else 1


def cmd_status(args):
    """상태 확인"""
    from auto_state import AutoState, get_latest_active_session
    from auto_logger import get_active_sessions, get_archived_sessions

    print("\n=== Auto Orchestrator 상태 ===\n")

    # 활성 세션
    active = get_active_sessions()
    if active:
        print(f"📂 활성 세션: {len(active)}개")
        for session_id in active[:5]:
            state = AutoState(session_id)
            status = state.get_status()
            print(f"   - {session_id}")
            print(f"     상태: {status['status']}, Phase: {status['phase']}")
            print(
                f"     진행: {status['progress']['completed']}/{status['progress']['total_tasks']}"
            )
    else:
        print("📂 활성 세션: 없음")

    # 아카이브 세션
    archived = get_archived_sessions()
    print(f"\n📦 아카이브: {len(archived)}개 세션")

    # 최근 세션
    latest = get_latest_active_session()
    if latest:
        print(f"\n🔄 마지막 세션: {latest}")
        print("   재개: python auto_cli.py resume")

    return 0


def cmd_discover(args):
    """다음 작업 발견"""
    from auto_discovery import AutoDiscovery

    print("\n=== 자율 발견 ===\n")

    discovery = AutoDiscovery()
    task = discovery.discover_next_task()

    if task:
        tier = "Tier 1 (명시적)" if task.priority.value <= 5 else "Tier 2 (자율)"
        print(f"📋 발견된 작업 [{tier}]")
        print("")
        print(f"   우선순위: P{task.priority.value}")
        print(f"   카테고리: {task.category}")
        print(f"   제목: {task.title}")
        print(f"   설명: {task.description}")
        print("")
        print("   실행 명령:")
        print(f"   {task.command}")
    else:
        print("✅ 모든 검사 통과 - 할 일 없음!")

    if args.report:
        print("\n=== 상세 리포트 ===")
        import json

        report = discovery.get_status_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0


def cmd_pause(args):
    """세션 일시 정지"""
    from auto_state import AutoState, get_latest_active_session

    session_id = args.session_id or get_latest_active_session()
    if not session_id:
        print("활성 세션이 없습니다")
        return 1

    state = AutoState(session_id)
    state.set_status("paused")
    state.create_checkpoint(
        task_id=0,
        task_content="수동 일시 정지",
        context_hint="사용자가 pause 명령 실행",
        todo_state=[],
    )

    print(f"⏸️  세션 일시 정지: {session_id}")
    print(f"   재개: python auto_cli.py resume {session_id}")

    return 0


def cmd_abort(args):
    """세션 취소"""
    from auto_state import AutoState, get_latest_active_session

    session_id = args.session_id or get_latest_active_session()
    if not session_id:
        print("활성 세션이 없습니다")
        return 1

    state = AutoState(session_id)
    state.abort()

    print(f"🛑 세션 취소됨: {session_id}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Auto Orchestrator - 자율 작업 루프 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python auto_cli.py                         # 자율 루프 시작 (E2E/TDD 검증 포함)
  python auto_cli.py --max 10                # 최대 10회 반복 + 검증
  python auto_cli.py --promise DONE          # "DONE" 출력 시 종료
  python auto_cli.py --dry-run               # 판단만, 실행 안함
  python auto_cli.py --skip-validation       # 검증 생략 (빠른 반복)
  python auto_cli.py --skip-validation --max 5  # 검증 없이 5회
  python auto_cli.py discover                # 다음 작업 1회 확인
  python auto_cli.py resume                  # 마지막 세션 재개
  python auto_cli.py status                  # 현재 상태 확인
  python auto_cli.py pause                   # 세션 일시 정지
  python auto_cli.py abort                   # 세션 취소
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="명령")

    # run (기본)
    parser.add_argument("--max", type=int, help="최대 반복 횟수")
    parser.add_argument(
        "--promise", type=str, help="종료 조건 (<promise>TEXT</promise>)"
    )
    parser.add_argument("--dry-run", action="store_true", help="실행 없이 판단만")
    parser.add_argument(
        "--skip-validation", action="store_true", help="E2E/TDD 검증 생략"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=True, help="상세 출력"
    )

    # resume
    resume_parser = subparsers.add_parser("resume", help="세션 재개")
    resume_parser.add_argument("session_id", nargs="?", help="세션 ID")

    # status
    _ = subparsers.add_parser("status", help="상태 확인")

    # discover
    discover_parser = subparsers.add_parser("discover", help="다음 작업 발견")
    discover_parser.add_argument("--report", action="store_true", help="상세 리포트")

    # pause
    pause_parser = subparsers.add_parser("pause", help="세션 일시 정지")
    pause_parser.add_argument("session_id", nargs="?", help="세션 ID")

    # abort
    abort_parser = subparsers.add_parser("abort", help="세션 취소")
    abort_parser.add_argument("session_id", nargs="?", help="세션 ID")

    args = parser.parse_args()

    # 명령 라우팅
    if args.command == "resume":
        return cmd_resume(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "discover":
        return cmd_discover(args)
    elif args.command == "pause":
        return cmd_pause(args)
    elif args.command == "abort":
        return cmd_abort(args)
    else:
        # 기본: run
        return cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())

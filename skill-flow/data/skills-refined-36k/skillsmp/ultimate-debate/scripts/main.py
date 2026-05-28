"""CLI entrypoint for Ultimate Debate skill."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Core Engine 패키지 경로 추가
PACKAGES_PATH = (
    Path(__file__).parent.parent.parent.parent.parent / "ultimate-debate" / "src"
)
if str(PACKAGES_PATH) not in sys.path:
    sys.path.insert(0, str(PACKAGES_PATH))

# Core Engine 어댑터 사용 시도, 실패 시 레거시 모드
try:
    from adapter import CORE_AVAILABLE, UltimateDebateAdapter  # noqa: F401

    USE_ADAPTER = CORE_AVAILABLE
    if not USE_ADAPTER:
        # Core Engine 사용 불가 시 레거시 모드로 fallback
        from debate.orchestrator import UltimateDebate
except ImportError:
    USE_ADAPTER = False
    from debate.orchestrator import UltimateDebate

# AI 클라이언트 및 인증 시스템 임포트
try:
    from ultimate_debate.auth import TokenStore
    from ultimate_debate.clients.gemini_client import GeminiClient
    from ultimate_debate.clients.openai_client import OpenAIClient

    AUTH_AVAILABLE = True
except ImportError as e:
    AUTH_AVAILABLE = False
    AUTH_IMPORT_ERROR = str(e)


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Ultimate Debate - Multi-AI Consensus Verifier"
    )

    parser.add_argument(
        "--task",
        type=str,
        help="Task description to debate",
    )

    parser.add_argument(
        "--task-id",
        type=str,
        help="Existing task ID to resume",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume existing debate (requires --task-id)",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of existing debate (requires --task-id)",
    )

    parser.add_argument(
        "--max-rounds",
        type=int,
        default=5,
        help="Maximum debate rounds (default: 5)",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Consensus threshold (default: 0.8)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="json",
        choices=["json", "text"],
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    # Handle status command
    if args.status:
        if not args.task_id:
            print("Error: --task-id required for --status", file=sys.stderr)
            sys.exit(1)

        status = get_debate_status(args.task_id)
        print_output(status, args.output)
        sys.exit(0)

    # Handle resume command
    if args.resume:
        if not args.task_id:
            print("Error: --task-id required for --resume", file=sys.stderr)
            sys.exit(1)

        print(f"Resuming debate: {args.task_id}")
        # TODO: Implement resume logic
        print("Resume not yet implemented", file=sys.stderr)
        sys.exit(1)

    # Handle new debate
    if not args.task:
        print("Error: --task required for new debate", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    result = run_debate(
        task=args.task,
        max_rounds=args.max_rounds,
        threshold=args.threshold,
    )

    print_output(result, args.output)


def run_debate(task: str, max_rounds: int = 5, threshold: float = 0.8) -> dict:
    """Run ultimate debate.

    Args:
        task: Task description
        max_rounds: Maximum rounds
        threshold: Consensus threshold

    Returns:
        Final debate result
    """
    # Core Engine 어댑터 또는 레거시 모드 선택
    if USE_ADAPTER:
        print("[INFO] Using Core Engine (packages/ultimate-debate)")
        debate = UltimateDebateAdapter(
            task=task,
            max_rounds=max_rounds,
            consensus_threshold=threshold,
        )
    else:
        print("[INFO] Using Legacy Mode (skills/ultimate-debate/scripts/debate)")
        debate = UltimateDebate(
            task=task,
            max_rounds=max_rounds,
            consensus_threshold=threshold,
        )

    # AI 클라이언트 자동 등록 (저장된 인증 토큰 사용)
    registered_clients = register_ai_clients(debate)

    if not registered_clients:
        print("\n[WARNING] 등록된 AI 클라이언트가 없습니다.", file=sys.stderr)
        print("[WARNING] Mock 데이터로 실행됩니다.", file=sys.stderr)
        print("[INFO] 실제 AI를 사용하려면 먼저 로그인하세요:", file=sys.stderr)
        print("  /ai-login openai   # ChatGPT Plus/Pro", file=sys.stderr)
        print("  /ai-login google   # Google Gemini", file=sys.stderr)
        print()
    else:
        print(f"[INFO] 등록된 AI 클라이언트: {', '.join(registered_clients)}")

    print(
        f"Starting debate: {debate.engine.task_id if USE_ADAPTER else debate.task_id}"
    )
    print(f"Task: {task}")
    print(f"Max rounds: {max_rounds}")
    print(f"Threshold: {threshold}\n")

    result = asyncio.run(debate.run())

    print("\nDebate completed!")
    print(f"Status: {result['status']}")
    print(f"Rounds: {result['total_rounds']}")
    print(f"Consensus: {result['consensus_percentage'] * 100:.1f}%")

    return result


def register_ai_clients(debate) -> list[str]:
    """저장된 인증 토큰을 기반으로 AI 클라이언트 자동 등록.

    Args:
        debate: UltimateDebateAdapter 또는 UltimateDebate 인스턴스

    Returns:
        list[str]: 등록된 클라이언트 이름 목록
    """
    if not AUTH_AVAILABLE:
        print(f"[WARNING] 인증 시스템 로드 실패: {AUTH_IMPORT_ERROR}", file=sys.stderr)
        return []

    registered = []
    token_store = TokenStore()

    # OpenAI (GPT) 클라이언트 등록
    if token_store.has_valid_token("openai"):
        try:
            client = OpenAIClient(model_name="gpt-4o", token_store=token_store)
            debate.register_ai_client("gpt", client)
            registered.append("gpt (OpenAI)")
            print("[OK] OpenAI 클라이언트 등록 완료 (gpt-4o)")
        except Exception as e:
            print(f"[ERROR] OpenAI 클라이언트 등록 실패: {e}", file=sys.stderr)
    else:
        print("[SKIP] OpenAI 토큰 없음 - /ai-login openai 로 로그인 필요")

    # Google (Gemini) 클라이언트 등록
    if token_store.has_valid_token("google"):
        try:
            # Code Assist 모드 (기본값) - 프로젝트 ID 불필요
            client = GeminiClient(
                model_name="gemini-2.0-flash",
                token_store=token_store,
                use_code_assist=True,  # cloudcode-pa.googleapis.com 사용
            )
            debate.register_ai_client("gemini", client)
            registered.append("gemini (Google)")
            print("[OK] Gemini 클라이언트 등록 완료 (gemini-2.0-flash, Code Assist 모드)")
        except Exception as e:
            print(f"[ERROR] Gemini 클라이언트 등록 실패: {e}", file=sys.stderr)
    else:
        print("[SKIP] Google 토큰 없음 - /ai-login google 로 로그인 필요")

    return registered


def get_debate_status(task_id: str) -> dict:
    """Get status of existing debate.

    Args:
        task_id: Debate task ID

    Returns:
        Status dict
    """
    debate_path = Path(".claude/debates") / task_id

    if not debate_path.exists():
        return {
            "error": f"Debate not found: {task_id}",
            "task_id": task_id,
        }

    # Read TASK.md
    task_file = debate_path / "TASK.md"
    task_content = ""
    if task_file.exists():
        task_content = task_file.read_text(encoding="utf-8")

    # Count rounds
    rounds = sorted(debate_path.glob("round_*"))

    # Check for FINAL.md
    final_file = debate_path / "FINAL.md"
    has_final = final_file.exists()
    final_content = ""
    if has_final:
        final_content = final_file.read_text(encoding="utf-8")

    return {
        "task_id": task_id,
        "debate_path": str(debate_path),
        "task_content": task_content,
        "total_rounds": len(rounds),
        "rounds": [r.name for r in rounds],
        "has_final": has_final,
        "final_content": final_content if has_final else None,
    }


def print_output(data: dict, output_format: str = "json") -> None:
    """Print output in specified format.

    Args:
        data: Data to print
        output_format: Output format (json/text)
    """
    if output_format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Text format
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{key}:")
                print(json.dumps(value, indent=2, ensure_ascii=False))
            else:
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cross-AI Verifier CLI

코드 검증을 위한 커맨드라인 인터페이스.

Usage:
    python main.py src/auth.py --provider openai --focus security
    python main.py src/auth.py --parallel
    python main.py --code "def foo(): pass" --provider gemini
"""

import argparse
import asyncio
import sys
from pathlib import Path

# 현재 스크립트의 디렉토리를 sys.path에 추가
_SCRIPT_DIR = Path(__file__).parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from engines.verify_engine import VerifyEngine


def parse_args():
    """인자 파싱."""
    parser = argparse.ArgumentParser(
        description="Cross-AI Code Verifier",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s src/auth.py --provider openai --focus security
  %(prog)s src/auth.py --parallel
  %(prog)s --code "def foo(): pass" --provider gemini
        """,
    )

    parser.add_argument("file", nargs="?", help="검증할 파일 경로")
    parser.add_argument("--code", help="직접 입력할 코드 (파일 대신)")
    parser.add_argument(
        "--language", default="python", help="프로그래밍 언어 (기본: python)"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini"],
        default="openai",
        help="사용할 Provider (기본: openai)",
    )
    parser.add_argument(
        "--focus",
        choices=["security", "bugs", "performance", "all"],
        default="all",
        help="검증 초점 (기본: all)",
    )
    parser.add_argument(
        "--parallel", action="store_true", help="OpenAI + Gemini 병렬 검증"
    )
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")

    return parser.parse_args()


async def main():
    """메인 함수."""
    args = parse_args()

    # 입력 확인
    if not args.file and not args.code:
        print("오류: 파일 경로 또는 --code 옵션이 필요합니다.", file=sys.stderr)
        sys.exit(1)

    engine = VerifyEngine()

    try:
        if args.file:
            # 파일 검증
            report = await engine.verify_file(
                args.file,
                focus=args.focus,
                provider=args.provider,
                parallel=args.parallel,
            )
        else:
            # 직접 코드 검증
            if args.parallel:
                report = await engine.verify_parallel(
                    args.code, language=args.language, focus=args.focus
                )
            else:
                report = await engine.verify(
                    args.code,
                    language=args.language,
                    focus=args.focus,
                    provider=args.provider,
                )

        # 출력
        if args.json:
            import json

            print(json.dumps(report.aggregated, indent=2, ensure_ascii=False))
        else:
            print(report.summary())
            print(report.format_issues())

            # 제안사항
            suggestions = report.aggregated.get("suggestions", [])
            if suggestions:
                print("\n### 개선 제안")
                for s in suggestions:
                    print(f"- {s}")

            # 에러
            errors = report.aggregated.get("errors", [])
            if errors:
                print("\n### 에러")
                for e in errors:
                    print(f"- {e['provider']}: {e['error']}")

    except FileNotFoundError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"인증 오류: {e}", file=sys.stderr)
        print("\n해결 방법:")
        print("  1. /ai-auth login --provider openai  # 또는 gemini")
        print("  2. 또는 환경변수 설정: OPENAI_API_KEY, GEMINI_API_KEY")
        sys.exit(1)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

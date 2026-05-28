#!/usr/bin/env python3
"""
로그 파일 분석 스크립트

Usage:
    python analyze_logs.py <log_file> [--pattern ERROR|WARN|ENTRY|RESULT]
"""

import argparse
import re
import sys
from pathlib import Path
from collections import Counter


def parse_log_line(line: str) -> dict | None:
    """로그 라인을 파싱하여 구조화된 데이터 반환"""
    # 일반적인 로그 패턴: timestamp [LEVEL] tag: message
    patterns = [
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.\d]*)\s*\[(?P<level>\w+)\]\s*(?P<tag>\w+)?:?\s*(?P<message>.*)",
        r"\[(?P<level>\w+)\]\s*(?P<message>.*)",
        r"(?P<level>ERROR|WARN|INFO|DEBUG)\s*(?P<message>.*)",
    ]

    for pattern in patterns:
        match = re.match(pattern, line.strip())
        if match:
            return match.groupdict()
    return None


def analyze_logs(log_path: Path, filter_pattern: str | None = None) -> dict:
    """로그 파일 분석"""
    results = {
        "total_lines": 0,
        "parsed_lines": 0,
        "level_counts": Counter(),
        "tag_counts": Counter(),
        "errors": [],
        "warnings": [],
        "entry_exit_pairs": [],
        "timeline": [],
    }

    if not log_path.exists():
        print(f"❌ 로그 파일을 찾을 수 없습니다: {log_path}")
        sys.exit(1)

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    results["total_lines"] = len(lines)

    for i, line in enumerate(lines):
        if filter_pattern and filter_pattern not in line:
            continue

        parsed = parse_log_line(line)
        if parsed:
            results["parsed_lines"] += 1
            level = parsed.get("level", "UNKNOWN").upper()
            tag = parsed.get("tag", "")
            message = parsed.get("message", "")

            results["level_counts"][level] += 1
            if tag:
                results["tag_counts"][tag] += 1

            if level == "ERROR":
                results["errors"].append(
                    {
                        "line": i + 1,
                        "message": message,
                        "context": lines[max(0, i - 2) : i + 3],
                    }
                )
            elif level in ("WARN", "WARNING"):
                results["warnings"].append({"line": i + 1, "message": message})

            # ENTRY/RESULT 페어링 추적
            if tag == "ENTRY":
                results["entry_exit_pairs"].append(
                    {
                        "entry_line": i + 1,
                        "entry_message": message,
                        "result_line": None,
                        "result_message": None,
                    }
                )
            elif tag == "RESULT" and results["entry_exit_pairs"]:
                # 가장 최근 ENTRY와 매칭
                for pair in reversed(results["entry_exit_pairs"]):
                    if pair["result_line"] is None:
                        pair["result_line"] = i + 1
                        pair["result_message"] = message
                        break

    return results


def print_report(results: dict, verbose: bool = False):
    """분석 결과 출력"""
    print("\n" + "=" * 60)
    print("📊 로그 분석 결과")
    print("=" * 60)

    print("\n📈 요약")
    print(f"   총 라인 수: {results['total_lines']}")
    print(f"   파싱된 라인: {results['parsed_lines']}")

    print("\n📉 레벨별 분포")
    for level, count in results["level_counts"].most_common():
        emoji = {
            "ERROR": "🔴",
            "WARN": "🟡",
            "WARNING": "🟡",
            "INFO": "🔵",
            "DEBUG": "⚪",
        }.get(level, "⚫")
        print(f"   {emoji} {level}: {count}")

    if results["tag_counts"]:
        print("\n🏷️  태그별 분포")
        for tag, count in results["tag_counts"].most_common(10):
            print(f"   {tag}: {count}")

    if results["errors"]:
        print(f"\n🔴 에러 목록 ({len(results['errors'])}개)")
        for error in results["errors"][:10]:  # 최대 10개
            print(f"   Line {error['line']}: {error['message'][:80]}")
            if verbose:
                print("   Context:")
                for ctx_line in error["context"]:
                    print(f"      {ctx_line.rstrip()}")

    if results["warnings"]:
        print(f"\n🟡 경고 목록 ({len(results['warnings'])}개)")
        for warn in results["warnings"][:5]:  # 최대 5개
            print(f"   Line {warn['line']}: {warn['message'][:80]}")

    # ENTRY/RESULT 분석
    incomplete_pairs = [
        p for p in results["entry_exit_pairs"] if p["result_line"] is None
    ]
    if incomplete_pairs:
        print(f"\n⚠️  완료되지 않은 ENTRY ({len(incomplete_pairs)}개)")
        for pair in incomplete_pairs[:5]:
            print(f"   Line {pair['entry_line']}: {pair['entry_message'][:60]}")

    print("\n" + "=" * 60)

    # 디버깅 제안
    print("\n💡 디버깅 제안")
    if results["errors"]:
        print("   1. 첫 번째 ERROR 발생 지점부터 분석 시작")
    if incomplete_pairs:
        print("   2. 완료되지 않은 ENTRY 지점에서 예외 발생 가능성")
    if results["level_counts"].get("DEBUG", 0) < 10:
        print("   3. 디버그 로그 추가 권장 (현재 부족)")
    print("   4. 문제 예측 → 로그 검증 → 가설 확정 순서 진행")


def main():
    parser = argparse.ArgumentParser(description="로그 파일 분석")
    parser.add_argument("log_file", help="분석할 로그 파일 경로")
    parser.add_argument("--pattern", "-p", help="필터링할 패턴 (예: ERROR, WARN)")
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 출력")

    args = parser.parse_args()

    log_path = Path(args.log_file)
    results = analyze_logs(log_path, args.pattern)
    print_report(results, args.verbose)

    # 에러가 있으면 exit code 1
    if results["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()

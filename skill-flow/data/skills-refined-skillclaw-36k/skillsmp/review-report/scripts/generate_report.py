#!/usr/bin/env python3
"""
리뷰 리포트 Markdown 파일 생성 스크립트

사용법:
    # stdin 방식 (권장 - 특수 문자 이스케이프 문제 없음)
    echo '<JSON>' | python generate_report.py --output <디렉토리>
    cat issues.json | python generate_report.py --output <디렉토리>

    # CLI 인자 방식 (하위 호환)
    python generate_report.py --output <디렉토리> --issues '<JSON 문자열>'

예시:
    # stdin 방식 (권장)
    echo '[{"file":"example.tsx","location":"23:5","severity":"high","category":"type-safety","problem":"any 타입 사용","suggestion":"unknown으로 변경"}]' | python generate_report.py --output docs/reports/code-review

    # heredoc 사용
    python generate_report.py --output docs/reports/code-review << 'EOF'
    [{"file":"example.tsx","location":"23:5","severity":"high","category":"type-safety","problem":"any 타입 사용","suggestion":"unknown으로 변경"}]
    EOF

    # 파일에서 읽기
    cat issues.json | python generate_report.py --output docs/reports/code-review

    # CLI 인자 방식 (하위 호환)
    python generate_report.py --output docs/reports/code-review --issues '[...]'

    # 이슈 없는 경우
    echo '[]' | python generate_report.py --output docs/reports/code-review
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict


class SeverityCount(TypedDict):
    critical: int
    high: int
    medium: int
    low: int


class Metadata(TypedDict):
    createdAt: str
    totalIssues: int
    severityCount: SeverityCount


class Issue(TypedDict, total=False):
    file: str
    location: str
    severity: str
    category: str
    problem: str
    suggestion: str
    references: list[str]


class ReviewReport(TypedDict):
    metadata: Metadata
    issues: list[Issue]


VALID_SEVERITIES = {"critical", "high", "medium", "low"}

SEVERITY_ORDER = ["critical", "high", "medium", "low"]

SEVERITY_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
}

SEVERITY_LABEL = {
    "critical": "Critical",
    "high": "High",
    "medium": "Medium",
    "low": "Low",
}


def read_issues_json(issues_arg: str | None) -> str:
    """
    이슈 JSON 읽기 - stdin 또는 CLI 인자에서

    Args:
        issues_arg: --issues 인자 값 (None, "-", 또는 JSON 문자열)

    Returns:
        JSON 문자열
    """
    if issues_arg is None or issues_arg == "-":
        return sys.stdin.read()
    return issues_arg


def generate_hash() -> str:
    """8자리 랜덤 해시 생성"""
    timestamp = datetime.now(timezone.utc).isoformat()
    return hashlib.sha256(timestamp.encode()).hexdigest()[:8]


def get_date_string() -> str:
    """YYYYMMDD 형식 날짜 문자열 반환"""
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def get_timestamp_string() -> str:
    """YYYY-MM-DD HH:MM:SS 형식 타임스탬프 반환"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def calculate_severity_count(issues: list[Issue]) -> SeverityCount:
    """이슈 목록에서 심각도별 개수 계산"""
    count: SeverityCount = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for issue in issues:
        severity = issue.get("severity", "").lower()
        if severity in count:
            count[severity] += 1  # type: ignore[literal-required]

    return count


def validate_issues(issues: list[Issue]) -> tuple[bool, str]:
    """이슈 데이터 유효성 검사"""
    required_fields = {"file", "location", "severity", "category", "problem", "suggestion"}

    for idx, issue in enumerate(issues):
        # 필수 필드 확인
        missing = required_fields - set(issue.keys())
        if missing:
            return False, f"이슈 #{idx + 1}: 필수 필드 누락 - {missing}"

        # 심각도 값 확인
        severity = issue.get("severity", "").lower()
        if severity not in VALID_SEVERITIES:
            return False, f"이슈 #{idx + 1}: 잘못된 심각도 '{severity}' (허용: {VALID_SEVERITIES})"

    return True, ""


def create_report(issues: list[Issue]) -> ReviewReport:
    """리뷰 리포트 생성"""
    severity_count = calculate_severity_count(issues)

    return {
        "metadata": {
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "totalIssues": len(issues),
            "severityCount": severity_count,
        },
        "issues": issues,
    }


def detect_review_type(output_dir: str) -> str:
    """출력 디렉토리 경로에서 리뷰 타입 감지"""
    if "security" in output_dir.lower():
        return "Security Review"
    return "Code Review"


def escape_markdown_table(text: str) -> str:
    """마크다운 테이블 셀 내용 이스케이프"""
    if not text:
        return ""
    # 파이프 문자와 줄바꿈 이스케이프
    return text.replace("|", "\\|").replace("\n", " ")


def generate_issues_table(issues: list[Issue], severity: str) -> str:
    """특정 심각도의 이슈 테이블 생성"""
    filtered = [i for i in issues if i.get("severity", "").lower() == severity]
    if not filtered:
        return ""

    emoji = SEVERITY_EMOJI[severity]
    label = SEVERITY_LABEL[severity]

    lines = [
        f"\n### {emoji} {label} Issues\n",
        "| # | File | Location | Category | Problem | Suggestion |",
        "|---|------|----------|----------|---------|------------|",
    ]

    for idx, issue in enumerate(filtered, 1):
        file_path = escape_markdown_table(issue.get("file", ""))
        location = escape_markdown_table(issue.get("location", ""))
        category = escape_markdown_table(issue.get("category", ""))
        problem = escape_markdown_table(issue.get("problem", ""))
        suggestion = escape_markdown_table(issue.get("suggestion", ""))

        lines.append(f"| {idx} | {file_path} | {location} | {category} | {problem} | {suggestion} |")

    return "\n".join(lines)


def generate_checklist(issues: list[Issue]) -> str:
    """이슈 수정 체크리스트 생성"""
    if not issues:
        return ""

    lines = [
        "\n## ✅ Fix Checklist\n",
        "**⚠️ MANDATORY**: Check each box (`- [x]`) immediately after fixing the issue.\n",
        "Track your progress by checking off fixed issues:\n",
    ]

    issue_num = 1
    for severity in SEVERITY_ORDER:
        for issue in issues:
            if issue.get("severity", "").lower() == severity:
                file_path = issue.get("file", "")
                location = issue.get("location", "").split(":")[0]  # 라인 번호만
                problem = issue.get("problem", "")[:50]  # 50자로 제한
                if len(issue.get("problem", "")) > 50:
                    problem += "..."
                label = SEVERITY_LABEL[severity]
                lines.append(f"- [ ] #{issue_num} [{label}] {file_path}:{location} - {problem}")
                issue_num += 1

    lines.append("")
    lines.append("**Completion Rule**: When all checkboxes are checked, update the Status at the top to `✅ Complete`.")

    return "\n".join(lines)


def generate_markdown(report: ReviewReport, review_type: str) -> str:
    """리포트 데이터를 Markdown 형식으로 변환"""
    metadata = report["metadata"]
    issues = report["issues"]
    severity_count = metadata["severityCount"]
    total_issues = metadata["totalIssues"]

    # 상태 결정
    status = "✅ Complete" if total_issues == 0 else "🔄 In Progress"

    lines = [
        f"# {review_type} Report\n",
        f"**Status**: {status}",
        f"**Generated**: {get_timestamp_string()} (UTC)",
        f"**Total Issues**: {total_issues}\n",
        "---\n",
    ]

    # Critical Instructions 추가 (이슈가 있는 경우에만)
    if total_issues > 0:
        lines.extend([
            "**⚠️ CRITICAL INSTRUCTIONS**: For AI agents fixing issues:",
            "1. ✅ After fixing each issue, check off its checkbox below (`- [ ]` → `- [x]`)",
            "2. 📅 Update the status above when all issues are resolved",
            "3. ⛔ DO NOT leave this report without checking completed items\n",
            "---\n",
        ])

    lines.extend([
        "## 📊 Summary\n",
        "| Severity | Count |",
        "|----------|-------|",
        f"| {SEVERITY_EMOJI['critical']} Critical | {severity_count['critical']} |",
        f"| {SEVERITY_EMOJI['high']} High | {severity_count['high']} |",
        f"| {SEVERITY_EMOJI['medium']} Medium | {severity_count['medium']} |",
        f"| {SEVERITY_EMOJI['low']} Low | {severity_count['low']} |",
    ])

    # 이슈 섹션
    if total_issues > 0:
        lines.append("\n---\n")
        lines.append("## 🔍 Issues")

        for severity in SEVERITY_ORDER:
            table = generate_issues_table(issues, severity)
            if table:
                lines.append(table)

        # 체크리스트
        checklist = generate_checklist(issues)
        if checklist:
            lines.append("\n---")
            lines.append(checklist)

    # 노트 섹션
    lines.append("\n---\n")
    lines.append("## 📝 Notes\n")
    if total_issues == 0:
        lines.append("No issues were found during the review. Great job! 🎉\n")
    else:
        lines.append("Please address the issues above in order of severity (Critical → Low).\n")

    lines.append("---\n")
    lines.append("*Generated by review-report skill*")

    return "\n".join(lines)


def save_report(report: ReviewReport, output_dir: str) -> str:
    """리포트를 Markdown 파일로 저장하고 파일 경로 반환"""
    output_path = Path(output_dir)

    # 디렉토리 존재 확인 및 생성
    output_path.mkdir(parents=True, exist_ok=True)

    # 파일명 생성: {8자리_해시}_{YYYYMMDD}.md
    filename = f"{generate_hash()}_{get_date_string()}.md"
    file_path = output_path / filename

    # 리뷰 타입 감지
    review_type = detect_review_type(output_dir)

    # Markdown 파일 저장
    markdown_content = generate_markdown(report, review_type)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    return str(file_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="리뷰 리포트 Markdown 파일 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    # stdin 방식 (권장)
    echo '[{"file":"example.tsx",...}]' | python generate_report.py --output docs/reports/code-review

    # heredoc 사용
    python generate_report.py --output docs/reports/code-review << 'EOF'
    [{"file":"example.tsx","location":"23:5","severity":"high",...}]
    EOF

    # CLI 인자 방식 (하위 호환)
    python generate_report.py --output docs/reports/code-review --issues '[...]'
        """,
    )
    parser.add_argument(
        "--output",
        required=True,
        help="출력 디렉토리 경로 (예: docs/reports/code-review, docs/reports/security-review)",
    )
    parser.add_argument(
        "--issues",
        default=None,
        help="이슈 목록 JSON 문자열 (생략 시 stdin에서 읽음, '-'도 stdin으로 처리)",
    )

    args = parser.parse_args()

    # JSON 읽기 (stdin 또는 CLI 인자에서)
    issues_json = read_issues_json(args.issues)

    # JSON 파싱
    try:
        issues: list[Issue] = json.loads(issues_json)
    except json.JSONDecodeError as e:
        print(f"오류: JSON 파싱 실패 - {e}", file=sys.stderr)
        sys.exit(1)

    # 배열 타입 확인
    if not isinstance(issues, list):
        print("오류: issues는 배열이어야 합니다", file=sys.stderr)
        sys.exit(1)

    # 이슈 유효성 검사 (빈 배열은 허용)
    if issues:
        is_valid, error_msg = validate_issues(issues)
        if not is_valid:
            print(f"오류: {error_msg}", file=sys.stderr)
            sys.exit(1)

    # 리포트 생성 및 저장
    report = create_report(issues)
    file_path = save_report(report, args.output)

    # 결과 출력
    print(f"리포트 생성 완료: {file_path}")
    print(f"총 이슈: {report['metadata']['totalIssues']}개")

    severity_count = report["metadata"]["severityCount"]
    if report["metadata"]["totalIssues"] > 0:
        print(
            f"심각도: critical({severity_count['critical']}), "
            f"high({severity_count['high']}), "
            f"medium({severity_count['medium']}), "
            f"low({severity_count['low']})"
        )


if __name__ == "__main__":
    main()

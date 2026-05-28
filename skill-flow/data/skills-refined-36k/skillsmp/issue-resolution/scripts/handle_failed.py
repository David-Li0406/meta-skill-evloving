#!/usr/bin/env python3
"""
실패 이슈 처리

Usage:
    python handle_failed.py 123 --report
    python handle_failed.py 123 --create-sub-issue
"""

import argparse
import json
import os
import subprocess
from pathlib import Path


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    return Path.cwd()


class FailedIssueHandler:
    """실패 이슈 처리"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or _get_project_root()

    def run_gh(self, *args) -> tuple[int, str]:
        """GitHub CLI 실행"""
        try:
            result = subprocess.run(
                ["gh"] + list(args),
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.returncode, result.stdout
        except Exception as e:
            return -1, str(e)

    def fetch_issue(self, issue_number: int) -> dict | None:
        """이슈 정보 조회"""
        code, output = self.run_gh(
            "issue", "view", str(issue_number), "--json", "title,body,labels,comments"
        )

        if code != 0:
            return None

        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return None

    def generate_report(self, issue_number: int, attempts: list[dict] = None) -> str:
        """실패 분석 레포트 생성"""
        issue = self.fetch_issue(issue_number)
        if not issue:
            return f"## 실패 분석: Issue #{issue_number}\n\n이슈를 찾을 수 없습니다."

        attempts = attempts or [
            {"approach": "직접 수정", "reason": "테스트 실패"},
            {"approach": "리팩토링 후 수정", "reason": "의존성 문제"},
            {"approach": "대안 구현", "reason": "설계 변경 필요"},
        ]

        report = f"""## 실패 분석: Issue #{issue_number}

### 이슈 정보
- **제목**: {issue.get('title', 'N/A')}
- **라벨**: {', '.join(lbl.get('name', '') for lbl in issue.get('labels', []))}

### 시도 내역
"""
        for i, attempt in enumerate(attempts, 1):
            report += f"{i}. **{attempt['approach']}** - {attempt['reason']}\n"

        report += """
### 실패 원인 분석
- [ ] 요구사항 불명확
- [ ] 기술적 제약
- [ ] 외부 의존성 문제
- [ ] 설계 변경 필요
- [ ] 추가 정보 필요

### 권장 조치
1. 이슈 본문에 추가 정보 요청
2. 설계 검토 회의 필요
3. 관련 이해관계자와 논의

### 대안 제안
1. [대안 1 설명]
2. [대안 2 설명]
3. [대안 3 설명]

---
생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        return report

    def create_sub_issue(self, issue_number: int, report: str) -> str | None:
        """서브 이슈 생성"""
        title = f"[분석 필요] Issue #{issue_number} 자동 해결 실패"

        body = f"""## 연관 이슈
- Parent: #{issue_number}

## 상태
자동 해결 시도 3회 실패. 수동 개입 필요.

{report}

## 요청 사항
- [ ] 실패 원인 분석
- [ ] 대안 검토
- [ ] 해결 방안 결정

---
🤖 자동 생성됨
"""

        code, output = self.run_gh(
            "issue",
            "create",
            "--title",
            title,
            "--body",
            body,
            "--label",
            "needs-triage,blocked",
        )

        if code == 0:
            # URL 추출
            import re

            match = re.search(r"https://github\.com/[^\s]+", output)
            if match:
                return match.group(0)

        return None

    def add_comment(self, issue_number: int, comment: str) -> bool:
        """이슈에 코멘트 추가"""
        code, _ = self.run_gh("issue", "comment", str(issue_number), "--body", comment)
        return code == 0

    def handle(
        self, issue_number: int, create_sub: bool = False, add_report: bool = False
    ):
        """실패 이슈 처리"""
        print("=" * 60)
        print(f"🔍 실패 이슈 처리: #{issue_number}")
        print("=" * 60)
        print()

        # 레포트 생성
        report = self.generate_report(issue_number)
        print("📋 분석 레포트:")
        print("-" * 40)
        print(report)
        print("-" * 40)

        if add_report:
            # 원본 이슈에 코멘트 추가
            comment = f"## 🤖 자동 분석 레포트\n\n{report}"
            if self.add_comment(issue_number, comment):
                print("\n✅ 원본 이슈에 레포트 추가됨")
            else:
                print("\n❌ 코멘트 추가 실패")

        if create_sub:
            # 서브 이슈 생성
            sub_url = self.create_sub_issue(issue_number, report)
            if sub_url:
                print(f"\n✅ 서브 이슈 생성됨: {sub_url}")
            else:
                print("\n❌ 서브 이슈 생성 실패")

        print()
        print("다음 단계:")
        print("1. 레포트 검토")
        print("2. 실패 원인 확인")
        print("3. 대안 검토 후 수동 해결")


def main():
    parser = argparse.ArgumentParser(description="실패 이슈 처리")
    parser.add_argument("issue_number", type=int, help="이슈 번호")
    parser.add_argument(
        "--report", action="store_true", help="레포트 생성 및 코멘트 추가"
    )
    parser.add_argument(
        "--create-sub-issue", action="store_true", help="서브 이슈 생성"
    )
    parser.add_argument("--project", type=str, help="프로젝트 루트")

    args = parser.parse_args()

    project_root = Path(args.project) if args.project else None
    handler = FailedIssueHandler(project_root)

    handler.handle(
        args.issue_number, create_sub=args.create_sub_issue, add_report=args.report
    )


if __name__ == "__main__":
    main()

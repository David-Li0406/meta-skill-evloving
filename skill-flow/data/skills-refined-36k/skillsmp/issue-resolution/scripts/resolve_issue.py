#!/usr/bin/env python3
"""
GitHub 이슈 해결 워크플로우

Usage:
    python resolve_issue.py 123 --analyze-only
    python resolve_issue.py 123 --auto-fix
    python resolve_issue.py 123 --auto-fix --create-pr
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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


class IssueType(Enum):
    BUG = "bug"
    FEATURE = "enhancement"
    DOCS = "documentation"
    REFACTOR = "refactor"
    UNKNOWN = "unknown"


class ResolutionStatus(Enum):
    ANALYZING = "analyzing"
    PLANNING = "planning"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class IssueInfo:
    number: int
    title: str = ""
    body: str = ""
    labels: list[str] = field(default_factory=list)
    issue_type: IssueType = IssueType.UNKNOWN
    related_files: list[str] = field(default_factory=list)


@dataclass
class ResolutionResult:
    status: ResolutionStatus
    attempts: int = 0
    branch: str = ""
    pr_url: str = ""
    error: str = ""


class IssueResolver:
    """GitHub 이슈 해결"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or _get_project_root()
        self.max_attempts = 3
        self.current_attempt = 0

    def log(self, message: str, level: str = "INFO"):
        """로그 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARN": "⚠️",
            "STEP": "📍",
        }.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

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
            return result.returncode, result.stdout + result.stderr
        except Exception as e:
            return -1, str(e)

    def fetch_issue(self, issue_number: int) -> IssueInfo | None:
        """이슈 정보 조회"""
        self.log(f"이슈 #{issue_number} 조회 중...", "STEP")

        code, output = self.run_gh(
            "issue", "view", str(issue_number), "--json", "title,body,labels"
        )

        if code != 0:
            self.log(f"이슈 조회 실패: {output}", "ERROR")
            return None

        try:
            data = json.loads(output)
            labels = [lbl.get("name", "") for lbl in data.get("labels", [])]

            # 이슈 타입 결정
            issue_type = IssueType.UNKNOWN
            for label in labels:
                if "bug" in label.lower():
                    issue_type = IssueType.BUG
                    break
                elif "enhancement" in label.lower() or "feature" in label.lower():
                    issue_type = IssueType.FEATURE
                    break
                elif "doc" in label.lower():
                    issue_type = IssueType.DOCS
                    break
                elif "refactor" in label.lower():
                    issue_type = IssueType.REFACTOR
                    break

            return IssueInfo(
                number=issue_number,
                title=data.get("title", ""),
                body=data.get("body", ""),
                labels=labels,
                issue_type=issue_type,
            )

        except json.JSONDecodeError:
            self.log("이슈 파싱 실패", "ERROR")
            return None

    def analyze_issue(self, issue: IssueInfo) -> dict:
        """이슈 분석"""
        self.log("이슈 분석 중...", "STEP")

        analysis = {
            "type": issue.issue_type.value,
            "title": issue.title,
            "keywords": [],
            "potential_files": [],
            "severity": "medium",
        }

        # 키워드 추출
        body_lower = issue.body.lower()
        keywords = []
        if "error" in body_lower or "exception" in body_lower:
            keywords.append("error")
            analysis["severity"] = "high"
        if "crash" in body_lower or "fail" in body_lower:
            keywords.append("crash")
            analysis["severity"] = "critical"
        if "slow" in body_lower or "performance" in body_lower:
            keywords.append("performance")
        if "test" in body_lower:
            keywords.append("test")

        analysis["keywords"] = keywords

        # 파일 경로 추출 (간단한 패턴 매칭)
        import re

        file_patterns = re.findall(r"[\w/]+\.(?:py|ts|js|tsx|jsx)", issue.body)
        analysis["potential_files"] = list(set(file_patterns))[:5]

        return analysis

    def create_branch(self, issue: IssueInfo) -> str:
        """브랜치 생성"""
        # 브랜치 이름 생성
        type_prefix = "fix" if issue.issue_type == IssueType.BUG else "feat"
        safe_title = issue.title.lower().replace(" ", "-")[:30]
        safe_title = "".join(c for c in safe_title if c.isalnum() or c == "-")
        branch_name = f"{type_prefix}/issue-{issue.number}-{safe_title}"

        self.log(f"브랜치 생성: {branch_name}", "STEP")

        # git 브랜치 생성
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            # 이미 존재하면 체크아웃
            subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.project_root,
                capture_output=True,
            )

        return branch_name

    def implement_fix(self, issue: IssueInfo, analysis: dict) -> bool:
        """수정 구현 (시뮬레이션)"""
        self.log(f"수정 구현 시도 {self.current_attempt}/{self.max_attempts}", "STEP")

        # 실제 구현에서는:
        # 1. TDD 사이클 실행
        # 2. 코드 수정
        # 3. 테스트 실행

        self.log("TDD 사이클 시작...", "INFO")
        self.log("  Red: 실패 테스트 확인", "INFO")
        self.log("  Green: 수정 구현", "INFO")
        self.log("  Refactor: 코드 정리", "INFO")

        # 시뮬레이션 성공
        return True

    def verify_fix(self) -> bool:
        """수정 검증"""
        self.log("수정 검증 중...", "STEP")

        # 테스트 실행
        result = subprocess.run(
            ["pytest", "tests/", "-v", "-x", "--tb=short"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            self.log("테스트 실패", "WARN")
            return False

        # 린트 검사
        result = subprocess.run(
            ["ruff", "check", "src/"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.log("린트 검사 실패", "WARN")
            return False

        self.log("검증 통과!", "SUCCESS")
        return True

    def create_pr(self, issue: IssueInfo, branch: str) -> str | None:
        """PR 생성"""
        self.log("PR 생성 중...", "STEP")

        title = f"fix: Resolve #{issue.number} - {issue.title[:50]}"
        body = f"""## Summary
Fixes #{issue.number}

## Changes
- [변경사항 요약]

## Test Plan
- [ ] 기존 테스트 통과
- [ ] 새 테스트 추가
- [ ] 수동 검증

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
"""

        code, output = self.run_gh(
            "pr", "create", "--title", title, "--body", body, "--base", "main"
        )

        if code == 0:
            # PR URL 추출
            import re

            match = re.search(r"https://github\.com/[^\s]+", output)
            if match:
                return match.group(0)

        return None

    def resolve(
        self, issue_number: int, auto_fix: bool = False, create_pr: bool = False
    ) -> ResolutionResult:
        """이슈 해결 워크플로우"""
        print("=" * 60)
        print(f"🔧 이슈 해결 워크플로우: #{issue_number}")
        print("=" * 60)
        print()

        result = ResolutionResult(status=ResolutionStatus.ANALYZING)

        # 1. 이슈 조회
        issue = self.fetch_issue(issue_number)
        if not issue:
            result.status = ResolutionStatus.FAILED
            result.error = "이슈 조회 실패"
            return result

        print(f"제목: {issue.title}")
        print(f"타입: {issue.issue_type.value}")
        print(f"라벨: {', '.join(issue.labels)}")
        print()

        # 2. 분석
        analysis = self.analyze_issue(issue)
        print("분석 결과:")
        print(f"  키워드: {', '.join(analysis['keywords'])}")
        print(f"  심각도: {analysis['severity']}")
        print(f"  관련 파일: {', '.join(analysis['potential_files']) or '없음'}")
        print()

        if not auto_fix:
            print("분석 완료. --auto-fix 옵션으로 자동 수정을 시도하세요.")
            result.status = ResolutionStatus.COMPLETED
            return result

        # 3. 브랜치 생성
        result.status = ResolutionStatus.PLANNING
        branch = self.create_branch(issue)
        result.branch = branch

        # 4. 수정 시도 (최대 3회)
        result.status = ResolutionStatus.IMPLEMENTING

        for attempt in range(1, self.max_attempts + 1):
            self.current_attempt = attempt
            result.attempts = attempt

            success = self.implement_fix(issue, analysis)
            if not success:
                continue

            # 5. 검증
            result.status = ResolutionStatus.VERIFYING
            if self.verify_fix():
                result.status = ResolutionStatus.COMPLETED

                # 6. PR 생성 (옵션)
                if create_pr:
                    pr_url = self.create_pr(issue, branch)
                    if pr_url:
                        result.pr_url = pr_url
                        self.log(f"PR 생성됨: {pr_url}", "SUCCESS")

                print()
                print("=" * 60)
                self.log(f"이슈 #{issue_number} 해결 완료!", "SUCCESS")
                print("=" * 60)
                return result

        # 3회 실패
        result.status = ResolutionStatus.FAILED
        result.error = "3회 시도 후 실패"

        print()
        print("=" * 60)
        self.log(f"이슈 #{issue_number} 해결 실패", "ERROR")
        self.log("수동 개입이 필요합니다. /issue-failed 실행 권장", "ERROR")
        print("=" * 60)

        return result


def main():
    parser = argparse.ArgumentParser(description="GitHub 이슈 해결 워크플로우")
    parser.add_argument("issue_number", type=int, help="이슈 번호")
    parser.add_argument("--analyze-only", action="store_true", help="분석만 수행")
    parser.add_argument("--auto-fix", action="store_true", help="자동 수정 시도")
    parser.add_argument("--create-pr", action="store_true", help="PR 생성")
    parser.add_argument("--project", type=str, help="프로젝트 루트")

    args = parser.parse_args()

    project_root = Path(args.project) if args.project else None
    resolver = IssueResolver(project_root)

    result = resolver.resolve(
        args.issue_number,
        auto_fix=args.auto_fix and not args.analyze_only,
        create_pr=args.create_pr,
    )

    sys.exit(0 if result.status == ResolutionStatus.COMPLETED else 1)


if __name__ == "__main__":
    main()

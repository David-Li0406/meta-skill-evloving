"""
Auto Discovery - 자율 발견 엔진 (v2.0)

5계층 우선순위 체계에 따라 다음 작업을 발견합니다.
- Tier 0: 세션 관리 (audit, context 관리)
- Tier 1: 긴급 (debug, check)
- Tier 2: 작업 처리 (commit, issue, pr)
- Tier 3: 개발 지원 (tdd, research)
- Tier 4: 자율 개선 (PRD 분석, 솔루션 탐색)

9개 커맨드 자동 트리거:
/check, /commit, /issue, /debug, /parallel, /tdd, /research, /pr, /audit
"""

import json
import os
import subprocess
import re
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Optional


def _get_project_root() -> Path:
    """프로젝트 루트 디렉토리를 동적으로 감지"""
    # 1. 환경 변수 우선
    if env_root := os.environ.get("CLAUDE_PROJECT_DIR"):
        return Path(env_root)
    # 2. 스크립트 위치 기반 (skills/auto-workflow/scripts → 프로젝트 루트)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    if (project_root / ".claude").exists():
        return project_root
    # 3. 현재 작업 디렉토리 (fallback)
    return Path.cwd()


DEFAULT_PROJECT_ROOT = _get_project_root()


def run_command(cmd: list, cwd: Path, timeout: int = 30) -> subprocess.CompletedProcess:
    """UTF-8 인코딩으로 subprocess 실행"""
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
        encoding="utf-8",
        errors="replace",
    )


class Priority(IntEnum):
    """5계층 우선순위"""

    # Tier 0: 세션 관리
    SESSION_AUDIT = 1  # /audit quick
    CONTEXT_CLEANUP = 2  # /commit → /clear → /auto

    # Tier 1: 긴급
    DEBUG_NEEDED = 10  # /debug (테스트 실패 + 원인 불명확)
    BUILD_FAILED = 11  # /debug (빌드 실패)
    CHECK_LINT = 12  # /check --fix (린트/타입 경고 10+)
    CHECK_SECURITY = 13  # /check --security (보안 취약점)
    CHECK_E2E = 14  # E2E 검증 필요

    # Tier 2: 작업 처리
    COMMIT_NEEDED = 20  # /commit (100줄+ 변경)
    ISSUE_FIX = 21  # /issue fix #N
    PR_AUTO = 22  # /pr auto (PR 리뷰 대기)

    # Tier 3: 개발 지원
    TDD_GUIDE = 30  # /tdd (새 기능 구현)
    RESEARCH_CODE = 31  # /research code
    RESEARCH_WEB = 32  # /research web
    RESEARCH_PLAN = 33  # /research plan
    RESEARCH_REVIEW = 34  # /research review

    # Tier 3.5: 합의 토론 (Ultimate Debate)
    DEBATE_ANALYSIS = 35  # PRD 결정, 아키텍처 선택 시 3AI 토론

    # Tier 4: 자율 개선 (기존 Tier 2)
    CODE_QUALITY = 40  # 린트 경고 수정
    TEST_COVERAGE = 41  # 커버리지 개선
    DOCUMENTATION = 42  # 문서화
    REFACTORING = 43  # 리팩토링
    DEPENDENCIES = 44  # 의존성 업데이트
    PERFORMANCE = 45  # 성능 개선
    ACCESSIBILITY = 46  # 접근성 개선

    # Tier 4+: 자율 발견
    PRD_ANALYSIS = 50  # PRD 분석
    SOLUTION_SEARCH = 51  # /research web (더 나은 솔루션)
    SOLUTION_MIGRATE = 52  # 마이그레이션 (병렬)


# 작업별 병렬 에이전트 수
PARALLEL_CONFIG = {
    "debug": 3,  # 가설/코드/로그 분석
    "check": 3,  # Lint/Type/Security
    "check_e2e": 4,  # Functional/Visual/A11y/Perf
    "issue_fix": 3,  # Coder/Tester/Reviewer
    "pr_review": 4,  # Security/Logic/Style/Perf
    "research_web": 4,  # 4방향 검색
    "research_code": 3,  # 영역별 분석
    "tdd": 2,  # Test/Impl
    "audit": 3,  # Git/Test/Docs
    "debate": 3,  # Claude/GPT/Gemini 3AI 토론
}

# 작업별 예상 Context 사용량 (%)
CONTEXT_ESTIMATES = {
    "audit_quick": 5,
    "commit": 3,
    "debug": 25,
    "check_fix": 10,
    "check_security": 15,
    "check_e2e": 12,
    "issue_fix_small": 15,
    "issue_fix_medium": 25,
    "issue_fix_large": 40,
    "pr_auto": 20,
    "tdd": 30,
    "research_code": 10,
    "research_web": 8,
    "research_plan": 12,
    # Debate (3AI 토론)
    "debate_small": 20,   # 2-3 라운드
    "debate_medium": 35,  # 4-5 라운드
    "debate_large": 50,   # 5+ 라운드
    "default": 15,
}


@dataclass
class DiscoveredTask:
    """발견된 작업"""

    priority: Priority
    category: str
    title: str
    description: str
    command: str  # 실행할 명령 (예: "/issue fix #123")
    details: dict = None
    # 병렬 처리 정보
    parallel_agents: int = 1  # 병렬 에이전트 수
    task_type: str = "default"  # 작업 유형 (context 예측용)
    affected_files: int = 1  # 영향받는 파일 수
    complexity: str = "medium"  # low | medium | high

    def to_dict(self) -> dict:
        return {
            "priority": self.priority.value,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "command": self.command,
            "details": self.details or {},
            "parallel_agents": self.parallel_agents,
            "task_type": self.task_type,
            "affected_files": self.affected_files,
            "complexity": self.complexity,
            "estimated_context": CONTEXT_ESTIMATES.get(self.task_type, 15),
        }


class AutoDiscovery:
    """자율 발견 엔진 (v2.0)"""

    def __init__(
        self,
        project_root: str = None,
        is_session_start: bool = False,
        debate_topic: str = None,  # --debate "주제" 플래그
    ):
        # 동적 프로젝트 루트 감지 (None이면 자동 감지)
        if project_root is None:
            self.project_root = DEFAULT_PROJECT_ROOT
        else:
            self.project_root = Path(project_root)
        self.is_session_start = is_session_start
        self.debate_topic = debate_topic  # 명시적 토론 주제
        self._lint_warning_threshold = 10  # 린트 경고 임계값
        self._commit_line_threshold = 100  # 커밋 필요 줄 수 임계값

    def discover_next_task(self) -> Optional[DiscoveredTask]:
        """
        5계층 우선순위에 따라 다음 작업 발견

        Returns:
            DiscoveredTask or None (모든 검사 통과 시)
        """
        # --debate 플래그가 있으면 즉시 토론 작업 반환
        if self.debate_topic:
            return self._create_debate_task(self.debate_topic)

        # Tier 0: 세션 관리
        task = self._check_tier0()
        if task:
            return task

        # Tier 1: 긴급 (debug, check)
        task = self._check_tier1()
        if task:
            return task

        # Tier 2: 작업 처리 (commit, issue, pr)
        task = self._check_tier2()
        if task:
            return task

        # Tier 3: 개발 지원 (tdd, research)
        task = self._check_tier3()
        if task:
            return task

        # Tier 3.5: 합의 토론 (ultimate-debate)
        task = self._check_debate_needed()
        if task:
            return task

        # Tier 4: 자율 개선 (코드 품질, 커버리지 등)
        task = self._check_tier4()
        if task:
            return task

        # Tier 4+: 자율 발견 (PRD 분석, 솔루션 탐색)
        task = self._check_autonomous_improvement()
        if task:
            return task

        return None

    # === Tier 0: 세션 관리 ===

    def _check_tier0(self) -> Optional[DiscoveredTask]:
        """Tier 0 검사 - 세션 관리"""
        # 세션 시작 시 audit quick 실행
        if self.is_session_start:
            return DiscoveredTask(
                priority=Priority.SESSION_AUDIT,
                category="세션 관리",
                title="설정 점검 (audit quick)",
                description="세션 시작 - 설정 일관성 점검",
                command="/audit quick",
                parallel_agents=PARALLEL_CONFIG.get("audit", 3),
                task_type="audit_quick",
                complexity="low",
            )
        return None

    # === Tier 1: 긴급 (debug, check) ===

    def _check_tier1(self) -> Optional[DiscoveredTask]:
        """Tier 1 검사 - 긴급 처리"""
        # 1.1 테스트 실패 + 원인 불명확 → /debug
        task = self._check_debug_needed()
        if task:
            return task

        # 1.2 빌드 실패 → /debug
        task = self._check_build_failed()
        if task:
            return task

        # 1.3 린트/타입 경고 10+ → /check --fix
        task = self._check_lint_threshold()
        if task:
            return task

        # 1.4 보안 취약점 → /check --security
        task = self._check_security_issues()
        if task:
            return task

        return None

    def _check_debug_needed(self) -> Optional[DiscoveredTask]:
        """테스트 실패 + 원인 불명확 → /debug"""
        try:
            lastfailed_path = (
                self.project_root / ".pytest_cache" / "v" / "cache" / "lastfailed"
            )
            if lastfailed_path.exists():
                with open(lastfailed_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content and content != "{}":
                        failed_tests = json.loads(content)
                        test_count = len(failed_tests)

                        return DiscoveredTask(
                            priority=Priority.DEBUG_NEEDED,
                            category="긴급 - 디버그",
                            title=f"테스트 실패 디버깅 ({test_count}개)",
                            description="테스트 실패 원인 분석 필요",
                            command="/debug",
                            parallel_agents=PARALLEL_CONFIG.get("debug", 3),
                            task_type="debug",
                            affected_files=min(test_count, 5),
                            complexity="high",
                            details={"failed_tests": list(failed_tests.keys())[:5]},
                        )
        except (FileNotFoundError, IOError, json.JSONDecodeError):
            pass
        return None

    def _check_build_failed(self) -> Optional[DiscoveredTask]:
        """빌드 실패 확인 → /debug"""
        try:
            # TypeScript 빌드 확인
            result = run_command(
                ["npx", "tsc", "--noEmit"], cwd=self.project_root, timeout=60
            )
            if result.returncode != 0:
                error_lines = result.stderr.split("\n") if result.stderr else []
                error_count = len([l for l in error_lines if "error TS" in l])

                return DiscoveredTask(
                    priority=Priority.BUILD_FAILED,
                    category="긴급 - 빌드",
                    title=f"TypeScript 빌드 실패 ({error_count}개 오류)",
                    description="타입 오류 수정 필요",
                    command="/debug",
                    parallel_agents=PARALLEL_CONFIG.get("debug", 3),
                    task_type="debug",
                    complexity="high",
                    details={"errors": error_lines[:10]},
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def _check_lint_threshold(self) -> Optional[DiscoveredTask]:
        """린트 경고 임계값 초과 → /check --fix"""
        try:
            result = run_command(
                ["ruff", "check", "src/", "--output-format", "json"],
                cwd=self.project_root,
                timeout=60,
            )

            if result.stdout and result.stdout.strip():
                issues = json.loads(result.stdout)
                if len(issues) >= self._lint_warning_threshold:
                    return DiscoveredTask(
                        priority=Priority.CHECK_LINT,
                        category="긴급 - 린트",
                        title=f"린트 경고 수정 ({len(issues)}개)",
                        description=f"임계값 {self._lint_warning_threshold}개 초과",
                        command="/check --fix",
                        parallel_agents=PARALLEL_CONFIG.get("check", 3),
                        task_type="check_fix",
                        complexity="medium",
                        details={"issue_count": len(issues)},
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass
        return None

    def _check_security_issues(self) -> Optional[DiscoveredTask]:
        """보안 취약점 → /check --security"""
        try:
            result = run_command(
                ["pip-audit", "--format", "json"], cwd=self.project_root, timeout=120
            )

            if result.stdout and result.stdout.strip():
                vulns = json.loads(result.stdout)
                critical = [
                    v
                    for v in vulns
                    if v.get("severity", "").upper() in ["CRITICAL", "HIGH"]
                ]

                if critical:
                    return DiscoveredTask(
                        priority=Priority.CHECK_SECURITY,
                        category="긴급 - 보안",
                        title=f"보안 취약점 ({len(critical)}개 Critical/High)",
                        description="즉시 패치 필요",
                        command="/check --security",
                        parallel_agents=PARALLEL_CONFIG.get("check", 3),
                        task_type="check_security",
                        complexity="high",
                        details={"vulnerabilities": critical[:5]},
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass
        return None

    # === Tier 2: 작업 처리 (commit, issue, pr) ===

    def _check_tier2(self) -> Optional[DiscoveredTask]:
        """Tier 2 검사 - 작업 처리"""
        # 2.1 커밋 안 된 변경 100줄+ → /commit
        task = self._check_commit_threshold()
        if task:
            return task

        # 2.2 열린 이슈 → /issue fix #N
        task = self._check_open_issues()
        if task:
            return task

        # 2.3 PR 생성 후 리뷰 대기 → /pr auto
        task = self._check_pr_pending()
        if task:
            return task

        return None

    def _check_commit_threshold(self) -> Optional[DiscoveredTask]:
        """커밋 안 된 변경 100줄+ → /commit"""
        try:
            result = run_command(
                ["git", "diff", "--stat"], cwd=self.project_root, timeout=10
            )

            if result.returncode == 0 and result.stdout:
                # 마지막 줄에서 변경 줄 수 추출
                lines = result.stdout.strip().split("\n")
                if lines:
                    last_line = lines[-1]
                    # "5 files changed, 150 insertions(+), 30 deletions(-)"
                    match = re.search(r"(\d+) insertion", last_line)
                    if match:
                        insertions = int(match.group(1))
                        if insertions >= self._commit_line_threshold:
                            return DiscoveredTask(
                                priority=Priority.COMMIT_NEEDED,
                                category="작업 처리",
                                title=f"변경사항 커밋 ({insertions}줄)",
                                description=f"임계값 {self._commit_line_threshold}줄 초과",
                                command="/commit",
                                task_type="commit",
                                complexity="low",
                                details={"insertions": insertions},
                            )
        except subprocess.TimeoutExpired:
            pass
        return None

    def _check_open_issues(self) -> Optional[DiscoveredTask]:
        """열린 이슈 → /issue fix"""
        try:
            result = run_command(
                [
                    "gh",
                    "issue",
                    "list",
                    "--state",
                    "open",
                    "--limit",
                    "5",
                    "--json",
                    "number,title,labels,body",
                ],
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout and result.stdout.strip():
                issues = json.loads(result.stdout)
                if issues:
                    # 버그 라벨 우선
                    bug_issues = [
                        i
                        for i in issues
                        if any(lbl.get("name") == "bug" for lbl in i.get("labels", []))
                    ]
                    target = bug_issues[0] if bug_issues else issues[0]

                    # 이슈 크기 추정
                    body_len = len(target.get("body", ""))
                    if body_len > 1000:
                        task_type = "issue_fix_large"
                        complexity = "high"
                    elif body_len > 300:
                        task_type = "issue_fix_medium"
                        complexity = "medium"
                    else:
                        task_type = "issue_fix_small"
                        complexity = "low"

                    return DiscoveredTask(
                        priority=Priority.ISSUE_FIX,
                        category="작업 처리",
                        title=f"#{target['number']}: {target['title']}",
                        description=f"열린 이슈 {len(issues)}개 중 우선 처리",
                        command=f"/issue fix #{target['number']}",
                        parallel_agents=PARALLEL_CONFIG.get("issue_fix", 3),
                        task_type=task_type,
                        complexity=complexity,
                        details={"issue": target},
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return None

    def _check_pr_pending(self) -> Optional[DiscoveredTask]:
        """PR 생성 후 리뷰 대기 → /pr auto"""
        try:
            result = run_command(
                [
                    "gh",
                    "pr",
                    "list",
                    "--state",
                    "open",
                    "--limit",
                    "5",
                    "--json",
                    "number,title,headRefName,reviewDecision",
                ],
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout and result.stdout.strip():
                prs = json.loads(result.stdout)
                # 리뷰 대기 중인 PR (APPROVED가 아닌 것)
                pending_prs = [
                    pr for pr in prs if pr.get("reviewDecision") != "APPROVED"
                ]

                if pending_prs:
                    target = pending_prs[0]
                    return DiscoveredTask(
                        priority=Priority.PR_AUTO,
                        category="작업 처리",
                        title=f"PR #{target['number']}: {target['title']}",
                        description=f"리뷰 대기 중 ({len(pending_prs)}개 PR)",
                        command=f"/pr auto #{target['number']}",
                        parallel_agents=PARALLEL_CONFIG.get("pr_review", 4),
                        task_type="pr_auto",
                        complexity="medium",
                        details={"pr": target},
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return None

    # === Tier 3: 개발 지원 (tdd, research) ===

    def _check_tier3(self) -> Optional[DiscoveredTask]:
        """Tier 3 검사 - 개발 지원"""
        # 3.1 새 기능 구현 요청 → /tdd
        task = self._check_tdd_needed()
        if task:
            return task

        # 3.2 PRD 진행 중 → /research plan
        task = self._check_research_needed()
        if task:
            return task

        return None

    def _check_tdd_needed(self) -> Optional[DiscoveredTask]:
        """새 기능 구현 요청 감지 → /tdd"""
        # PRD 중 구현 단계인 것 찾기
        prd_dir = self.project_root / "tasks" / "prds"
        if not prd_dir.exists():
            return None

        for prd_file in prd_dir.glob("*-prd-*.md"):
            try:
                content = prd_file.read_text(encoding="utf-8")
                # 구현 체크박스가 미완료인 PRD
                if "## 구현" in content or "## Implementation" in content:
                    impl_section = (
                        content.split("## 구현")[1]
                        if "## 구현" in content
                        else content.split("## Implementation")[1]
                    )
                    if (
                        "- [ ]" in impl_section.split("##")[0]
                    ):  # 구현 섹션 내 미완료 항목
                        return DiscoveredTask(
                            priority=Priority.TDD_GUIDE,
                            category="개발 지원",
                            title=f"TDD 가이드: {prd_file.stem}",
                            description="PRD 구현 - Red-Green-Refactor",
                            command=f"/tdd {prd_file.name}",
                            parallel_agents=PARALLEL_CONFIG.get("tdd", 2),
                            task_type="tdd",
                            complexity="high",
                            details={"prd": prd_file.name},
                        )
            except Exception:
                pass

        return None

    def _check_research_needed(self) -> Optional[DiscoveredTask]:
        """리서치 필요 감지 → /research"""
        # tasks/research/ 폴더의 미완료 리서치 태스크
        research_dir = self.project_root / "tasks" / "research"
        if not research_dir.exists():
            return None

        for research_file in research_dir.glob("*.md"):
            try:
                content = research_file.read_text(encoding="utf-8")
                if "- [ ]" in content and "status: pending" in content.lower():
                    return DiscoveredTask(
                        priority=Priority.RESEARCH_CODE,
                        category="개발 지원",
                        title=f"리서치: {research_file.stem}",
                        description="코드 분석 및 정보 수집",
                        command=f"/research code {research_file.name}",
                        parallel_agents=PARALLEL_CONFIG.get("research_code", 3),
                        task_type="research_code",
                        complexity="medium",
                        details={"file": research_file.name},
                    )
            except Exception:
                pass

        return None

    # === Tier 3.5: 합의 토론 (Ultimate Debate) ===

    def _create_debate_task(self, topic: str) -> DiscoveredTask:
        """--debate 플래그로 직접 토론 작업 생성

        Args:
            topic: 토론 주제

        Returns:
            DiscoveredTask: 토론 작업
        """
        # 주제 길이에 따른 복잡도 추정
        topic_len = len(topic)
        if topic_len > 500:
            task_type = "debate_large"
            complexity = "high"
        elif topic_len > 100:
            task_type = "debate_medium"
            complexity = "medium"
        else:
            task_type = "debate_small"
            complexity = "low"

        return DiscoveredTask(
            priority=Priority.DEBATE_ANALYSIS,
            category="합의 토론",
            title=f"토론: {topic[:50]}..." if len(topic) > 50 else f"토론: {topic}",
            description="--debate 플래그로 트리거된 3AI 토론",
            command=f"ultimate-debate --task '{topic}' --mode direct",
            parallel_agents=PARALLEL_CONFIG.get("debate", 3),
            task_type=task_type,
            complexity=complexity,
            details={
                "topic": topic,
                "trigger": "DEBATE_FLAG",
            },
        )

    def _check_debate_needed(self) -> Optional[DiscoveredTask]:
        """합의 필요 결정 감지 → ultimate-debate 실행

        트리거 조건:
        1. PRD 파일에서 `<!-- DECISION_REQUIRED -->` 마커
        2. 아키텍처 문서에서 `Option A/B/C` 패턴
        3. GitHub 이슈에 `needs-consensus` 라벨
        """
        # 1. PRD 파일에서 DECISION_REQUIRED 마커 감지
        task = self._check_prd_decision_required()
        if task:
            return task

        # 2. 아키텍처 문서에서 Option 패턴 감지
        task = self._check_architecture_options()
        if task:
            return task

        # 3. GitHub 이슈에서 needs-consensus 라벨 감지
        task = self._check_consensus_issues()
        if task:
            return task

        return None

    def _check_prd_decision_required(self) -> Optional[DiscoveredTask]:
        """PRD 파일에서 DECISION_REQUIRED 마커 감지"""
        prd_dirs = [
            self.project_root / "tasks" / "prds",
            self.project_root / "docs" / "prds",
            self.project_root / "docs",
        ]

        for prd_dir in prd_dirs:
            if not prd_dir.exists():
                continue

            for prd_file in prd_dir.glob("*.md"):
                try:
                    content = prd_file.read_text(encoding="utf-8")

                    # DECISION_REQUIRED 마커 확인
                    if "<!-- DECISION_REQUIRED -->" in content:
                        # 결정 컨텍스트 추출
                        decision_context = self._extract_decision_context(content)

                        return DiscoveredTask(
                            priority=Priority.DEBATE_ANALYSIS,
                            category="합의 토론",
                            title=f"결정 필요: {prd_file.stem}",
                            description=decision_context or "PRD 결정 사항 토론",
                            command=f"ultimate-debate --task '{prd_file.name}' --mode prd",
                            parallel_agents=PARALLEL_CONFIG.get("debate", 3),
                            task_type="debate_medium",
                            complexity="high",
                            details={
                                "prd_file": str(prd_file),
                                "trigger": "DECISION_REQUIRED",
                                "context": decision_context,
                            },
                        )
                except Exception:
                    pass

        return None

    def _check_architecture_options(self) -> Optional[DiscoveredTask]:
        """아키텍처 문서에서 Option A/B/C 패턴 감지"""
        arch_dirs = [
            self.project_root / "docs" / "architecture",
            self.project_root / "docs",
        ]

        option_pattern = re.compile(
            r"(Option\s+[A-C]|선택지\s*[1-3]|방안\s*[가-다])[\s:：]", re.IGNORECASE
        )

        for arch_dir in arch_dirs:
            if not arch_dir.exists():
                continue

            for doc_file in arch_dir.glob("*.md"):
                try:
                    content = doc_file.read_text(encoding="utf-8")
                    matches = option_pattern.findall(content)

                    # 2개 이상의 선택지가 있으면 토론 필요
                    if len(matches) >= 2:
                        # 결정 안 된 상태인지 확인 (선택됨 표시 없음)
                        if "선택됨" not in content and "selected" not in content.lower():
                            return DiscoveredTask(
                                priority=Priority.DEBATE_ANALYSIS,
                                category="합의 토론",
                                title=f"아키텍처 결정: {doc_file.stem}",
                                description=f"{len(matches)}개 선택지 발견",
                                command=f"ultimate-debate --task '{doc_file.name}' --mode architecture",
                                parallel_agents=PARALLEL_CONFIG.get("debate", 3),
                                task_type="debate_medium",
                                complexity="high",
                                details={
                                    "doc_file": str(doc_file),
                                    "options_count": len(matches),
                                    "trigger": "ARCHITECTURE_OPTIONS",
                                },
                            )
                except Exception:
                    pass

        return None

    def _check_consensus_issues(self) -> Optional[DiscoveredTask]:
        """GitHub 이슈에서 needs-consensus 라벨 감지"""
        try:
            result = run_command(
                [
                    "gh",
                    "issue",
                    "list",
                    "--state",
                    "open",
                    "--label",
                    "needs-consensus",
                    "--limit",
                    "5",
                    "--json",
                    "number,title,body,labels",
                ],
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout and result.stdout.strip():
                issues = json.loads(result.stdout)
                if issues:
                    target = issues[0]

                    # 이슈 복잡도 추정
                    body_len = len(target.get("body", ""))
                    if body_len > 1000:
                        task_type = "debate_large"
                    elif body_len > 300:
                        task_type = "debate_medium"
                    else:
                        task_type = "debate_small"

                    return DiscoveredTask(
                        priority=Priority.DEBATE_ANALYSIS,
                        category="합의 토론",
                        title=f"이슈 #{target['number']}: {target['title']}",
                        description=f"needs-consensus 라벨 ({len(issues)}개 이슈)",
                        command=f"ultimate-debate --task 'GitHub Issue #{target['number']}' --mode issue",
                        parallel_agents=PARALLEL_CONFIG.get("debate", 3),
                        task_type=task_type,
                        complexity="high",
                        details={
                            "issue": target,
                            "trigger": "NEEDS_CONSENSUS_LABEL",
                        },
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return None

    def _extract_decision_context(self, content: str) -> Optional[str]:
        """PRD에서 결정 컨텍스트 추출"""
        # DECISION_REQUIRED 마커 주변 텍스트 추출
        marker = "<!-- DECISION_REQUIRED -->"
        idx = content.find(marker)
        if idx == -1:
            return None

        # 마커 다음 200자 추출
        start = idx + len(marker)
        end = min(start + 200, len(content))
        context = content[start:end].strip()

        # 다음 마커까지만
        next_marker = context.find("<!--")
        if next_marker != -1:
            context = context[:next_marker].strip()

        return context if context else None

    # === Tier 4: 자율 개선 (코드 품질, 커버리지 등) ===

    def _check_tier4(self) -> Optional[DiscoveredTask]:
        """Tier 4 자율 개선"""
        # 4.1 코드 품질 (임계값 미만)
        task = self._check_lint_issues()
        if task:
            return task

        # 4.2 테스트 커버리지
        task = self._check_test_coverage()
        if task:
            return task

        # 4.3 문서화
        task = self._check_documentation()
        if task:
            return task

        # 4.4 리팩토링 (TODO 주석)
        task = self._check_todo_comments()
        if task:
            return task

        # 4.5 의존성 (non-critical)
        task = self._check_dependencies()
        if task:
            return task

        return None

    def _check_lint_issues(self) -> Optional[DiscoveredTask]:
        """린트 이슈 확인 (ruff)"""
        try:
            result = run_command(
                ["ruff", "check", "src/", "--output-format", "json"],
                cwd=self.project_root,
                timeout=60,
            )

            if result.stdout and result.stdout.strip():
                issues = json.loads(result.stdout)
                if issues:
                    # 파일별 그룹핑
                    files = {}
                    for issue in issues:
                        filename = issue.get("filename", "unknown")
                        files[filename] = files.get(filename, 0) + 1

                    worst_file = max(files.items(), key=lambda x: x[1])

                    return DiscoveredTask(
                        priority=Priority.CODE_QUALITY,
                        category="코드 품질",
                        title=f"린트 경고 수정 ({len(issues)}개)",
                        description=f"가장 많은 이슈: {worst_file[0]} ({worst_file[1]}개)",
                        command="ruff check src/ --fix",
                        details={
                            "total": len(issues),
                            "by_file": dict(list(files.items())[:5]),
                        },
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return None

    def _check_test_coverage(self) -> Optional[DiscoveredTask]:
        """테스트 커버리지 확인"""
        _ = self.project_root / ".coverage"  # Reserved for future use
        coverage_json = self.project_root / "coverage.json"

        # 기존 커버리지 데이터가 있으면 분석
        if coverage_json.exists():
            try:
                with open(coverage_json, "r") as f:
                    data = json.load(f)

                total_coverage = data.get("totals", {}).get("percent_covered", 100)

                if total_coverage < 80:
                    # 커버리지 낮은 파일 찾기
                    files = data.get("files", {})
                    low_coverage = [
                        (f, info.get("summary", {}).get("percent_covered", 0))
                        for f, info in files.items()
                        if info.get("summary", {}).get("percent_covered", 100) < 60
                    ]
                    low_coverage.sort(key=lambda x: x[1])

                    if low_coverage:
                        worst = low_coverage[0]
                        return DiscoveredTask(
                            priority=Priority.TEST_COVERAGE,
                            category="테스트 커버리지",
                            title=f"커버리지 개선 ({total_coverage:.1f}%)",
                            description=f"가장 낮은 파일: {worst[0]} ({worst[1]:.1f}%)",
                            command=f"/work '테스트 추가: {worst[0]}'",
                            details={
                                "total": total_coverage,
                                "low_files": low_coverage[:5],
                            },
                        )
            except (json.JSONDecodeError, KeyError):
                pass

        return None

    def _check_documentation(self) -> Optional[DiscoveredTask]:
        """문서화 누락 확인"""
        # src/ 폴더의 Python 파일 중 docstring 없는 것 찾기
        undocumented = []

        src_dir = self.project_root / "src"
        if not src_dir.exists():
            return None

        for py_file in src_dir.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                # 클래스나 함수 정의 후 docstring 없는 경우 탐지
                # 간단한 휴리스틱: 파일에 """가 없으면 문서화 부족
                if "def " in content or "class " in content:
                    if '"""' not in content and "'''" not in content:
                        undocumented.append(str(py_file.relative_to(self.project_root)))
            except Exception:
                pass

        if undocumented:
            return DiscoveredTask(
                priority=Priority.DOCUMENTATION,
                category="문서화",
                title=f"Docstring 추가 ({len(undocumented)}개 파일)",
                description=f"문서화 필요: {undocumented[0]}",
                command=f"/work 'Docstring 추가: {undocumented[0]}'",
                details={"files": undocumented[:10]},
            )

        return None

    def _check_todo_comments(self) -> Optional[DiscoveredTask]:
        """TODO 주석 확인"""
        try:
            result = run_command(
                [
                    "git",
                    "grep",
                    "-n",
                    "-E",
                    "(TODO|FIXME|HACK|XXX):",
                    "--",
                    "*.py",
                    "*.ts",
                    "*.tsx",
                ],
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout and result.stdout.strip():
                lines = result.stdout.strip().split("\n")
                todos = []

                for line in lines[:20]:  # 최대 20개
                    match = re.match(r"([^:]+):(\d+):(.+)", line)
                    if match:
                        todos.append(
                            {
                                "file": match.group(1),
                                "line": match.group(2),
                                "content": match.group(3).strip(),
                            }
                        )

                if todos:
                    first = todos[0]
                    return DiscoveredTask(
                        priority=Priority.REFACTORING,
                        category="리팩토링",
                        title=f"TODO 주석 해결 ({len(todos)}개)",
                        description=f"{first['file']}:{first['line']} - {first['content'][:40]}...",
                        command=f"/work 'TODO 해결: {first['file']}:{first['line']}'",
                        details={"todos": todos},
                    )
        except subprocess.TimeoutExpired:
            pass

        return None

    def _check_dependencies(self) -> Optional[DiscoveredTask]:
        """의존성 취약점 확인"""
        # pip-audit 확인
        try:
            result = run_command(
                ["pip-audit", "--format", "json"], cwd=self.project_root, timeout=120
            )

            if result.returncode != 0 and result.stdout and result.stdout.strip():
                vulns = json.loads(result.stdout)
                if vulns:
                    return DiscoveredTask(
                        priority=Priority.DEPENDENCIES,
                        category="의존성",
                        title=f"보안 취약점 ({len(vulns)}개)",
                        description="pip-audit에서 취약점 발견",
                        command="pip-audit --fix",
                        details={"vulnerabilities": vulns[:5]},
                    )
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass

        return None

    # === Tier 4+: 자율 발견 (PRD 분석, 솔루션 탐색) ===

    def _check_autonomous_improvement(self) -> Optional[DiscoveredTask]:
        """자율 발견 모드 - PRD 분석 및 더 나은 솔루션 탐색"""
        # Tier 1-4 모두 없을 때만 실행
        # 1. PRD 분석하여 개선점 찾기
        task = self._analyze_prd_for_improvements()
        if task:
            return task

        # 2. 의존성 중 더 나은 대안 탐색
        task = self._search_better_solutions()
        if task:
            return task

        return None

    def _analyze_prd_for_improvements(self) -> Optional[DiscoveredTask]:
        """PRD 분석하여 개선 가능한 영역 탐색"""
        prd_dir = self.project_root / "tasks" / "prds"
        if not prd_dir.exists():
            return None

        # 완료된 PRD 중 개선 가능한 것 찾기
        for prd_file in sorted(prd_dir.glob("*-prd-*.md"), reverse=True):
            try:
                content = prd_file.read_text(encoding="utf-8")
                unchecked = content.count("- [ ]")

                # 모든 체크박스가 완료된 PRD
                if unchecked == 0 and "- [x]" in content.lower():
                    # 개선 키워드 탐색
                    improvement_keywords = [
                        "성능",
                        "performance",
                        "최적화",
                        "optimize",
                        "보안",
                        "security",
                        "개선",
                        "improve",
                    ]
                    for keyword in improvement_keywords:
                        if keyword in content.lower():
                            return DiscoveredTask(
                                priority=Priority.PRD_ANALYSIS,
                                category="자율 발견",
                                title=f"PRD 개선 분석: {prd_file.stem}",
                                description=f"'{keyword}' 관련 개선점 탐색",
                                command=f"/research web '{keyword} best practices 2025'",
                                parallel_agents=PARALLEL_CONFIG.get("research_web", 4),
                                task_type="research_web",
                                complexity="medium",
                                details={"prd": prd_file.name, "keyword": keyword},
                            )
            except Exception:
                pass

        return None

    def _search_better_solutions(self) -> Optional[DiscoveredTask]:
        """더 나은 솔루션 탐색 (의존성 기반)"""
        # requirements.txt 또는 pyproject.toml에서 오래된 의존성 찾기
        req_file = self.project_root / "requirements.txt"
        if not req_file.exists():
            return None

        try:
            content = req_file.read_text(encoding="utf-8")
            lines = [
                l.strip()
                for l in content.split("\n")
                if l.strip() and not l.startswith("#")
            ]

            # 1년 이상 된 패키지 후보 (간단한 휴리스틱)
            old_packages = []
            for line in lines[:10]:  # 상위 10개만 검사
                match = re.match(r"([a-zA-Z0-9_-]+)", line)
                if match:
                    pkg_name = match.group(1)
                    # 특정 패키지들은 더 나은 대안이 있을 수 있음
                    alternatives = {
                        "requests": "httpx",
                        "flask": "fastapi",
                        "django-rest-framework": "fastapi",
                        "celery": "dramatiq",
                        "python-jose": "authlib",
                    }
                    if pkg_name.lower() in alternatives:
                        old_packages.append((pkg_name, alternatives[pkg_name.lower()]))

            if old_packages:
                pkg, alt = old_packages[0]
                return DiscoveredTask(
                    priority=Priority.SOLUTION_SEARCH,
                    category="자율 발견",
                    title=f"대안 탐색: {pkg} → {alt}",
                    description="더 현대적인 라이브러리로 마이그레이션 검토",
                    command=f"/research web '{alt} vs {pkg} comparison 2025'",
                    parallel_agents=PARALLEL_CONFIG.get("research_web", 4),
                    task_type="research_web",
                    complexity="medium",
                    details={"current": pkg, "alternative": alt},
                )
        except Exception:
            pass

        return None

    # === E2E 검증 ===

    def check_e2e_needed(self) -> Optional[DiscoveredTask]:
        """E2E 검증 필요 여부 (작업 완료 후 호출)"""
        return DiscoveredTask(
            priority=Priority.CHECK_E2E,
            category="검증",
            title="E2E 병렬 검증",
            description="Functional/Visual/A11y/Performance 4방향 검증",
            command="/check --e2e",
            parallel_agents=PARALLEL_CONFIG.get("check_e2e", 4),
            task_type="check_e2e",
            complexity="medium",
            details={
                "agents": ["Functional", "Visual", "Accessibility", "Performance"]
            },
        )

    # === 상태 리포트 ===

    def get_status_report(self) -> dict:
        """현재 상태 리포트 (5계층)"""
        return {
            "tier0_session": {"audit_needed": self.is_session_start},
            "tier1_urgent": {
                "debug_needed": self._check_debug_needed() is not None,
                "build_failed": self._check_build_failed() is not None,
                "lint_threshold": self._check_lint_threshold() is not None,
                "security_issues": self._check_security_issues() is not None,
            },
            "tier2_work": {
                "commit_needed": self._check_commit_threshold() is not None,
                "open_issues": self._check_open_issues() is not None,
                "pr_pending": self._check_pr_pending() is not None,
            },
            "tier3_dev": {
                "tdd_needed": self._check_tdd_needed() is not None,
                "research_needed": self._check_research_needed() is not None,
            },
            "tier3_5_debate": {
                "debate_needed": self._check_debate_needed() is not None,
            },
            "tier4_improve": {
                "lint_issues": self._check_lint_issues() is not None,
                "low_coverage": self._check_test_coverage() is not None,
                "missing_docs": self._check_documentation() is not None,
                "todo_comments": self._check_todo_comments() is not None,
                "vulnerabilities": self._check_dependencies() is not None,
            },
            "tier4_plus": {
                "prd_analysis": self._analyze_prd_for_improvements() is not None,
                "solution_search": self._search_better_solutions() is not None,
            },
        }

    def get_parallel_recommendation(self, task: DiscoveredTask) -> dict:
        """작업에 대한 병렬 처리 권장 사항"""
        agents = PARALLEL_CONFIG.get(task.task_type, 1)
        should_parallel = agents > 1 or task.affected_files >= 4

        return {
            "should_parallelize": should_parallel,
            "recommended_agents": max(agents, min(task.affected_files, 4)),
            "task_type": task.task_type,
            "estimated_context": CONTEXT_ESTIMATES.get(task.task_type, 15),
        }


if __name__ == "__main__":
    discovery = AutoDiscovery()

    print("=== 자율 발견 테스트 (v2.0) ===\n")

    task = discovery.discover_next_task()
    if task:
        print(f"[P{task.priority.value}] {task.category}")
        print(f"제목: {task.title}")
        print(f"설명: {task.description}")
        print(f"명령: {task.command}")
        print(f"병렬 에이전트: {task.parallel_agents}")
        print(f"예상 Context: {CONTEXT_ESTIMATES.get(task.task_type, 15)}%")
    else:
        print("✅ 모든 검사 통과 - 자율 발견 대기")

    print("\n=== 상태 리포트 (5계층) ===")
    import pprint

    pprint.pprint(discovery.get_status_report())

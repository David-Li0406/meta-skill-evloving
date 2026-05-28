#!/usr/bin/env python3
"""
agent_selector.py: 에이전트 자동 선택

작업 내용을 분석하여 최적의 서브에이전트를 선택합니다.
"""

import re
from typing import List, Tuple


class AgentSelector:
    """키워드 기반 에이전트 자동 선택"""

    # (정규식 패턴, 에이전트) 튜플 리스트
    AGENT_PATTERNS: List[Tuple[str, str]] = [
        # 디버깅/오류 관련
        (
            r"버그|에러|error|실패|fail|디버그|debug|테스트\s*실패|오류|exception",
            "debugger",
        ),
        # 테스트 관련
        (r"테스트|test|TDD|커버리지|coverage|pytest|jest|spec", "test-engineer"),
        # 검증 (Cross-AI Verifier) - code-reviewer보다 먼저 매칭되어야 함
        (
            r"검증|verify|cross.?ai|gpt.*검토|gemini.*검토|다른.*llm|교차\s*검토|ai\s*검토",
            "verify",
        ),
        # 코드 리뷰/품질
        (
            r"리뷰|review|검토|품질|quality|린트|lint|ruff|eslint|코드\s*품질",
            "code-reviewer",
        ),
        # 백엔드
        (
            r"API|api|백엔드|backend|서버|server|엔드포인트|endpoint|FastAPI|Django|Express",
            "backend-dev",
        ),
        # 프론트엔드
        (
            r"UI|ui|프론트|frontend|컴포넌트|component|화면|React|Vue|Next|CSS|스타일",
            "frontend-dev",
        ),
        # 보안
        (
            r"보안|security|취약점|vulnerability|인증|auth|권한|permission|OWASP",
            "security-auditor",
        ),
        # 문서
        (
            r"문서|document|README|readme|가이드|guide|설명|docs|API\s*문서",
            "docs-writer",
        ),
        # 데이터베이스
        (
            r"DB|db|데이터베이스|database|쿼리|query|마이그레이션|migration|스키마|schema|SQL|Supabase",
            "database-specialist",
        ),
        # 아키텍처
        (
            r"설계|design|아키텍처|architecture|구조\s*설계|시스템\s*설계|패턴",
            "architect",
        ),
        # DevOps
        (
            r"배포|deploy|CI|CD|인프라|infra|도커|docker|k8s|kubernetes|파이프라인|pipeline",
            "devops-engineer",
        ),
        # Python
        (r"Python|python|파이썬|FastAPI|Django|pytest|pip|uv|ruff", "python-dev"),
        # TypeScript
        (
            r"TypeScript|typescript|React|Next|Node|npm|tsx|타입스크립트",
            "typescript-dev",
        ),
        # Git/커밋
        (r"커밋|commit|git|푸시|push|머지|merge|브랜치|branch", "general-purpose"),
        # 분석/탐색 (기본값과 가까움)
        (
            r"분석|analyze|탐색|explore|구조|structure|리서치|research|조사|파악",
            "Explore",
        ),
    ]

    DEFAULT_AGENT = "Explore"

    def select_agent(self, task: str) -> str:
        """
        작업 내용을 분석하여 최적 에이전트 선택

        Args:
            task: 작업 설명 문자열

        Returns:
            선택된 에이전트 이름
        """
        task_lower = task.lower()

        for pattern, agent in self.AGENT_PATTERNS:
            if re.search(pattern, task, re.IGNORECASE):
                return agent

        return self.DEFAULT_AGENT

    def get_agent_description(self, agent: str) -> str:
        """에이전트 설명 반환"""
        descriptions = {
            "Explore": "코드베이스 탐색 및 분석",
            "debugger": "버그 분석 및 디버깅",
            "test-engineer": "테스트 작성 및 커버리지 개선",
            "code-reviewer": "코드 품질 리뷰 및 린트 수정",
            "backend-dev": "백엔드 API 개발",
            "frontend-dev": "프론트엔드 UI 개발",
            "verify": "Cross-AI 코드/기획 검증 (GPT, Gemini)",
            "security-auditor": "보안 취약점 분석",
            "docs-writer": "문서 작성 및 업데이트",
            "database-specialist": "데이터베이스 설계 및 쿼리 최적화",
            "architect": "시스템 설계 및 아키텍처",
            "devops-engineer": "CI/CD 및 인프라 관리",
            "python-dev": "Python 개발",
            "typescript-dev": "TypeScript/React 개발",
            "general-purpose": "범용 작업 처리",
        }
        return descriptions.get(agent, "알 수 없는 에이전트")

    def list_agents(self) -> List[Tuple[str, str]]:
        """사용 가능한 에이전트 목록 반환"""
        agents = set()
        for _, agent in self.AGENT_PATTERNS:
            agents.add(agent)
        agents.add(self.DEFAULT_AGENT)

        return [(agent, self.get_agent_description(agent)) for agent in sorted(agents)]


# 테스트
if __name__ == "__main__":
    selector = AgentSelector()

    test_cases = [
        "API 성능 개선",
        "테스트 커버리지 80% 달성",
        "린트 오류 15개 수정",
        "로그인 버그 디버깅",
        "README 문서 업데이트",
        "데이터베이스 스키마 설계",
        "Docker 배포 설정",
        "코드베이스 구조 분석",
        "코드 검증해줘",
        "GPT로 검토",
        "다른 LLM으로 비교",
        "Cross-AI 검증",
    ]

    print("에이전트 자동 선택 테스트:\n")
    for task in test_cases:
        agent = selector.select_agent(task)
        desc = selector.get_agent_description(agent)
        print(f"  {task}")
        print(f"  → {agent} ({desc})\n")

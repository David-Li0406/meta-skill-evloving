#!/usr/bin/env python3
"""
병렬 에이전트 오케스트레이션

Usage:
    python run_parallel.py --group dev --task "기능 구현"
    python run_parallel.py --agents "coder,tester" --task "빠른 구현"
"""

import argparse
import asyncio
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class AgentResult:
    name: str
    status: AgentStatus
    output: str = ""
    duration: float = 0.0
    error: str = ""


@dataclass
class OrchestratorState:
    task: str
    agents: list[str] = field(default_factory=list)
    results: list[AgentResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)


# 에이전트 그룹 정의
AGENT_GROUPS = {
    "dev": ["architect", "coder", "tester", "docs"],
    "test": ["unit", "integration", "e2e", "security"],
    "review": ["code-reviewer", "security-auditor", "architect-reviewer"],
}

# 에이전트 설명
AGENT_DESCRIPTIONS = {
    "architect": "설계 및 구조 분석",
    "coder": "코드 구현",
    "tester": "테스트 작성",
    "docs": "문서화",
    "unit": "단위 테스트 실행",
    "integration": "통합 테스트 실행",
    "e2e": "E2E 테스트 실행",
    "security": "보안 테스트 실행",
    "code-reviewer": "코드 리뷰",
    "security-auditor": "보안 리뷰",
    "architect-reviewer": "아키텍처 리뷰",
}


class ParallelOrchestrator:
    """병렬 에이전트 오케스트레이터"""

    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.state: OrchestratorState | None = None

    def log(self, message: str, level: str = "INFO"):
        """로그 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️"}.get(
            level, ""
        )
        print(f"[{timestamp}] {prefix} {message}")

    async def run_agent(self, agent_name: str, task: str) -> AgentResult:
        """단일 에이전트 실행 (시뮬레이션)"""
        start = datetime.now()
        self.log(f"에이전트 시작: {agent_name}")

        try:
            # 실제 구현에서는 Task tool 호출
            # 여기서는 시뮬레이션
            await asyncio.sleep(0.5)  # 시뮬레이션 딜레이

            duration = (datetime.now() - start).total_seconds()

            # 시뮬레이션 결과
            return AgentResult(
                name=agent_name,
                status=AgentStatus.SUCCESS,
                output=f"{agent_name} 완료: {task}",
                duration=duration,
            )

        except asyncio.TimeoutError:
            return AgentResult(
                name=agent_name,
                status=AgentStatus.FAILED,
                error="Timeout",
                duration=(datetime.now() - start).total_seconds(),
            )
        except Exception as e:
            return AgentResult(
                name=agent_name,
                status=AgentStatus.FAILED,
                error=str(e),
                duration=(datetime.now() - start).total_seconds(),
            )

    async def fan_out(self, agents: list[str], task: str) -> list[AgentResult]:
        """Fan-Out: 병렬 에이전트 실행"""
        self.log(f"Fan-Out: {len(agents)}개 에이전트 병렬 실행")

        # 모든 에이전트 병렬 실행
        tasks = [self.run_agent(agent, task) for agent in agents]

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=self.timeout
            )

            # 예외 처리
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(
                        AgentResult(
                            name=agents[i], status=AgentStatus.FAILED, error=str(result)
                        )
                    )
                else:
                    processed_results.append(result)

            return processed_results

        except asyncio.TimeoutError:
            return [
                AgentResult(
                    name=agent, status=AgentStatus.FAILED, error="Global timeout"
                )
                for agent in agents
            ]

    def fan_in(self, results: list[AgentResult]) -> dict:
        """Fan-In: 결과 집계"""
        self.log("Fan-In: 결과 집계")

        success_count = sum(1 for r in results if r.status == AgentStatus.SUCCESS)
        failed_count = len(results) - success_count

        aggregated = {
            "total": len(results),
            "success": success_count,
            "failed": failed_count,
            "success_rate": success_count / len(results) * 100 if results else 0,
            "agents": {
                r.name: {
                    "status": r.status.value,
                    "duration": r.duration,
                    "output": r.output[:200] if r.output else None,
                    "error": r.error if r.error else None,
                }
                for r in results
            },
        }

        return aggregated

    async def orchestrate(self, agents: list[str], task: str) -> dict:
        """전체 오케스트레이션 실행"""
        print("=" * 60)
        print("🚀 병렬 에이전트 오케스트레이션")
        print("=" * 60)
        print(f"태스크: {task}")
        print(f"에이전트: {', '.join(agents)}")
        print()

        self.state = OrchestratorState(task=task, agents=agents)

        # Phase 1: Supervisor (태스크 분해)
        self.log("Supervisor: 태스크 분해 중...")

        # Phase 2: Fan-Out
        results = await self.fan_out(agents, task)
        self.state.results = results

        # Phase 3: Fan-In
        aggregated = self.fan_in(results)

        # 결과 출력
        self.print_results(aggregated)

        return aggregated

    def print_results(self, aggregated: dict):
        """결과 출력"""
        print()
        print("=" * 60)
        print("📊 실행 결과")
        print("=" * 60)

        for name, data in aggregated["agents"].items():
            status_icon = "✅" if data["status"] == "success" else "❌"
            duration = f"({data['duration']:.2f}s)" if data["duration"] else ""
            print(f"  {status_icon} {name} {duration}")

            if data["error"]:
                print(f"      └─ Error: {data['error']}")

        print()
        print(
            f"성공률: {aggregated['success_rate']:.0f}% ({aggregated['success']}/{aggregated['total']})"
        )

        if aggregated["failed"] > 0:
            print()
            print("⚠️ 일부 에이전트 실패. 재실행 권장.")
        else:
            print()
            print("✅ 모든 에이전트 성공!")


def main():
    parser = argparse.ArgumentParser(description="병렬 에이전트 오케스트레이션")
    parser.add_argument(
        "--group",
        type=str,
        choices=["dev", "test", "review"],
        help="에이전트 그룹 (dev, test, review)",
    )
    parser.add_argument("--agents", type=str, help="에이전트 목록 (콤마 구분)")
    parser.add_argument("--task", type=str, required=True, help="실행할 태스크")
    parser.add_argument("--timeout", type=int, default=300, help="타임아웃 (초)")

    args = parser.parse_args()

    # 에이전트 결정
    if args.group:
        agents = AGENT_GROUPS.get(args.group, [])
    elif args.agents:
        agents = [a.strip() for a in args.agents.split(",")]
    else:
        print("❌ --group 또는 --agents 필수")
        sys.exit(1)

    if not agents:
        print("❌ 에이전트가 없습니다")
        sys.exit(1)

    # 실행
    orchestrator = ParallelOrchestrator(timeout=args.timeout)
    result = asyncio.run(orchestrator.orchestrate(agents, args.task))

    # 종료 코드
    sys.exit(0 if result["failed"] == 0 else 1)


if __name__ == "__main__":
    main()

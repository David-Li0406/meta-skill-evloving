"""
협업 패턴 기본 클래스
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class PatternResult:
    """패턴 실행 결과"""
    pattern_name: str
    agents_used: list[str]
    execution_log: list[dict] = field(default_factory=list)
    final_result: str = ""
    intermediate_results: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "pattern": self.pattern_name,
            "agents_used": self.agents_used,
            "execution_log": self.execution_log,
            "final_result": self.final_result,
            "intermediate_results": self.intermediate_results,
            "metadata": self.metadata
        }


class BasePattern(ABC):
    """협업 패턴 기본 클래스"""

    def __init__(self, agents: dict, verbose: bool = True):
        """
        Args:
            agents: {name: Agent} 형태의 에이전트 딕셔너리
            verbose: 로그 출력 여부
        """
        self.agents = agents
        self.verbose = verbose
        self.start_time = None
        self.total_tokens = 0

    @property
    @abstractmethod
    def pattern_name(self) -> str:
        """패턴 이름"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> PatternResult:
        """패턴 실행"""
        pass

    def log(self, message: str):
        """로그 출력"""
        if self.verbose:
            print(f"[{self.pattern_name}] {message}")

    def start_execution(self):
        """실행 시작"""
        self.start_time = time.time()
        self.total_tokens = 0
        self.log("실행 시작")

    def end_execution(self) -> float:
        """실행 종료, 소요 시간 반환"""
        elapsed = time.time() - self.start_time
        self.log(f"실행 완료 (소요 시간: {elapsed:.2f}초, 총 토큰: {self.total_tokens})")
        return elapsed

    def get_agent(self, name: str):
        """에이전트 조회"""
        if name not in self.agents:
            raise ValueError(f"Agent not found: {name}. Available: {list(self.agents.keys())}")
        return self.agents[name]

    def track_tokens(self, response):
        """토큰 사용량 추적"""
        self.total_tokens += response.usage.get("total_tokens", 0)

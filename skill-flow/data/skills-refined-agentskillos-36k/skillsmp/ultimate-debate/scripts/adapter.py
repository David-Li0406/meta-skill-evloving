"""Skill Adapter - Core Engine과 Claude Code Skill Layer 연결.

이 어댑터는 독립 레포(ultimate-debate/)의 Core Engine을
Claude Code의 Skill 시스템과 연결합니다.
"""

import sys
from pathlib import Path

# Core Engine 패키지 경로 추가 (독립 서브 레포)
PACKAGES_PATH = (
    Path(__file__).parent.parent.parent.parent.parent / "ultimate-debate" / "src"
)
if str(PACKAGES_PATH) not in sys.path:
    sys.path.insert(0, str(PACKAGES_PATH))

from typing import Any

# Core Engine 임포트
try:
    from ultimate_debate import UltimateDebate
    from ultimate_debate.consensus import ConsensusChecker, ConsensusResult
    from ultimate_debate.storage import ContextManager, ChunkManager, LoadLevel
    from ultimate_debate.comparison import SemanticComparator, HashComparator
    from ultimate_debate.strategies import StrategyType

    CORE_AVAILABLE = True
except ImportError as e:
    CORE_AVAILABLE = False
    IMPORT_ERROR = str(e)


class UltimateDebateAdapter:
    """Claude Code Skill과 Core Engine을 연결하는 어댑터."""

    def __init__(
        self,
        task: str,
        max_rounds: int = 5,
        consensus_threshold: float = 0.8,
    ):
        """어댑터 초기화.

        Args:
            task: 토론 주제
            max_rounds: 최대 라운드 수
            consensus_threshold: 합의 임계값
        """
        if not CORE_AVAILABLE:
            raise ImportError(
                f"Core Engine을 로드할 수 없습니다: {IMPORT_ERROR}\n"
                f"패키지 설치 필요: pip install -e {PACKAGES_PATH.parent}"
            )

        self.engine = UltimateDebate(
            task=task,
            max_rounds=max_rounds,
            consensus_threshold=consensus_threshold,
        )
        self.task = task

    def register_ai_client(self, model_name: str, client: Any) -> None:
        """AI 클라이언트 등록.

        Args:
            model_name: 모델 이름 (claude/gpt/gemini)
            client: BaseAIClient 구현체
        """
        self.engine.register_ai_client(model_name, client)

    async def run(self) -> dict[str, Any]:
        """토론 실행.

        Returns:
            최종 결과 딕셔너리
        """
        return await self.engine.run()

    def get_status(self) -> dict[str, Any]:
        """현재 상태 조회.

        Returns:
            상태 정보 딕셔너리
        """
        return self.engine.get_status()

    @staticmethod
    def is_available() -> bool:
        """Core Engine 사용 가능 여부."""
        return CORE_AVAILABLE

    @staticmethod
    def get_import_error() -> str | None:
        """임포트 에러 메시지."""
        return IMPORT_ERROR if not CORE_AVAILABLE else None


# Claude Code Skill 연동을 위한 헬퍼 함수들


def create_debate(
    task: str,
    max_rounds: int = 5,
    threshold: float = 0.8,
) -> UltimateDebateAdapter:
    """토론 인스턴스 생성 헬퍼.

    Args:
        task: 토론 주제
        max_rounds: 최대 라운드 수
        threshold: 합의 임계값

    Returns:
        UltimateDebateAdapter 인스턴스
    """
    return UltimateDebateAdapter(
        task=task,
        max_rounds=max_rounds,
        consensus_threshold=threshold,
    )


def load_debate_context(
    task_id: str,
    level: int = 1,
) -> dict[str, Any]:
    """기존 토론 컨텍스트 로드 (청킹 지원).

    Args:
        task_id: 토론 ID
        level: 로드 레벨 (0=METADATA, 1=SUMMARY, 2=CONCLUSION, 3=FULL)

    Returns:
        컨텍스트 데이터
    """
    if not CORE_AVAILABLE:
        return {"error": "Core Engine not available"}

    debates_path = Path(".claude/debates") / task_id
    if not debates_path.exists():
        return {"error": f"Debate not found: {task_id}"}

    chunker = ChunkManager()
    load_level = LoadLevel(level)

    result = {
        "task_id": task_id,
        "path": str(debates_path),
        "load_level": load_level.name,
        "rounds": [],
    }

    # 각 라운드 청킹 로드
    for round_dir in sorted(debates_path.glob("round_*")):
        round_data = {"round": round_dir.name, "models": {}}

        for model_file in round_dir.glob("*.md"):
            if model_file.name in ["CONSENSUS.md"]:
                continue
            model_name = model_file.stem
            round_data["models"][model_name] = chunker.load_level(
                model_file, load_level
            )

        result["rounds"].append(round_data)

    return result


def get_available_strategies() -> list[str]:
    """사용 가능한 전략 목록.

    Returns:
        전략 이름 리스트
    """
    if not CORE_AVAILABLE:
        return []
    return [s.value for s in StrategyType]


# 모듈 정보
__all__ = [
    "UltimateDebateAdapter",
    "create_debate",
    "load_debate_context",
    "get_available_strategies",
    "CORE_AVAILABLE",
]

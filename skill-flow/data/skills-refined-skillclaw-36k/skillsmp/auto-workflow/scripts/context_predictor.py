"""
Context Predictor - 작업별 예상 Context 사용량 분석

80% 도달 시 다음 작업의 예상 context를 계산하여
정리 필요 여부를 판단합니다.
"""

from dataclasses import dataclass

# 작업 유형별 기본 예상 Context 사용량 (%)
TASK_CONTEXT_ESTIMATES = {
    # Tier 0: 세션 관리
    "audit_quick": 5,
    "commit": 3,
    "clear_restart": 2,
    # Tier 1: 긴급
    "debug": 25,
    "debug_simple": 15,
    "check_fix": 10,
    "check_security": 15,
    "check_e2e": 12,
    # Tier 2: 작업 처리
    "issue_fix_small": 15,
    "issue_fix_medium": 25,
    "issue_fix_large": 40,
    "pr_auto": 20,
    "pr_review": 15,
    # Tier 3: 개발 지원
    "tdd": 30,
    "tdd_simple": 18,
    "research_code": 10,
    "research_web": 8,
    "research_plan": 12,
    "research_review": 10,
    # Tier 3.5: 합의 토론 (Ultimate Debate)
    "debate_small": 20,   # 2-3 라운드 (간단한 결정)
    "debate_medium": 35,  # 4-5 라운드 (복잡한 결정)
    "debate_large": 50,   # 5+ 라운드 (아키텍처 수준 결정)
    # Tier 4: 자율 개선
    "prd_analysis": 15,
    "solution_search": 12,
    "solution_migration": 35,
    "docs_update": 8,
    # 검증
    "e2e_validation": 10,
    "tdd_validation": 8,
    # 병렬 처리 (에이전트 수에 따라 조정)
    "parallel_dev": 35,
    "parallel_test": 20,
    "parallel_review": 18,
    "parallel_research": 15,
    # 기본값
    "default": 15,
}


@dataclass
class TaskEstimate:
    """작업 예상 결과"""

    task_type: str
    base_estimate: int
    adjusted_estimate: int
    affected_files: int
    complexity: str
    can_proceed: bool
    remaining_context: int
    recommendation: str


class ContextPredictor:
    """Context 사용량 예측기"""

    def __init__(self, current_context: int = 0):
        """
        Args:
            current_context: 현재 context 사용량 (%)
        """
        self.current_context = current_context

    def update_current(self, percent: int):
        """현재 context 사용량 업데이트"""
        self.current_context = percent

    def estimate_task(self, task: dict) -> TaskEstimate:
        """
        작업의 예상 Context 사용량 계산

        Args:
            task: {
                "type": str,           # 작업 유형
                "affected_files": int, # 영향받는 파일 수
                "complexity": str,     # low | medium | high
                "description": str     # 작업 설명 (선택)
            }

        Returns:
            TaskEstimate 객체
        """
        task_type = task.get("type", "default")
        affected_files = task.get("affected_files", 1)
        complexity = task.get("complexity", "medium")

        # 기본 예상값
        base_estimate = TASK_CONTEXT_ESTIMATES.get(
            task_type, TASK_CONTEXT_ESTIMATES["default"]
        )

        # 파일 수에 따른 가중치
        file_multiplier = self._get_file_multiplier(affected_files)

        # 복잡도에 따른 가중치
        complexity_multiplier = self._get_complexity_multiplier(complexity)

        # 최종 예상값 계산
        adjusted_estimate = int(base_estimate * file_multiplier * complexity_multiplier)

        # 남은 context 계산
        remaining = 100 - self.current_context

        # 진행 가능 여부 판단
        can_proceed = adjusted_estimate <= remaining

        # 권장 사항 생성
        recommendation = self._get_recommendation(
            adjusted_estimate, remaining, can_proceed
        )

        return TaskEstimate(
            task_type=task_type,
            base_estimate=base_estimate,
            adjusted_estimate=adjusted_estimate,
            affected_files=affected_files,
            complexity=complexity,
            can_proceed=can_proceed,
            remaining_context=remaining,
            recommendation=recommendation,
        )

    def should_cleanup(
        self, task: dict, threshold: int = 20
    ) -> tuple[bool, TaskEstimate]:
        """
        정리 필요 여부 판단 (80% 도달 시 사용)

        Args:
            task: 다음 작업 정보
            threshold: 초과 임계값 (기본 20%)

        Returns:
            (정리 필요 여부, TaskEstimate)
        """
        estimate = self.estimate_task(task)

        # 예상 사용량이 남은 여유를 초과하는지 확인
        # 또는 threshold(20%)를 초과하는지 확인
        should_clean = (
            estimate.adjusted_estimate > estimate.remaining_context
            or estimate.adjusted_estimate > threshold
        )

        return should_clean, estimate

    def analyze_multiple_tasks(self, tasks: list[dict]) -> list[TaskEstimate]:
        """
        여러 작업의 예상 Context 분석

        순차적으로 실행할 경우 어디까지 진행 가능한지 분석
        """
        estimates = []
        cumulative_context = self.current_context

        for task in tasks:
            # 임시로 현재 context 업데이트
            temp_predictor = ContextPredictor(cumulative_context)
            estimate = temp_predictor.estimate_task(task)
            estimates.append(estimate)

            if estimate.can_proceed:
                cumulative_context += estimate.adjusted_estimate
            else:
                break

        return estimates

    def get_optimal_batch(self, tasks: list[dict]) -> tuple[list[dict], list[dict]]:
        """
        현재 context에서 처리 가능한 최적 배치 결정

        Returns:
            (처리 가능한 작업들, 다음 세션으로 미룰 작업들)
        """
        estimates = self.analyze_multiple_tasks(tasks)

        can_do = []
        defer = []

        for i, (task, estimate) in enumerate(zip(tasks, estimates)):
            if estimate.can_proceed:
                can_do.append(task)
            else:
                defer = tasks[i:]
                break

        return can_do, defer

    # === Private Methods ===

    def _get_file_multiplier(self, file_count: int) -> float:
        """파일 수에 따른 가중치"""
        if file_count >= 10:
            return 1.5
        elif file_count >= 5:
            return 1.2
        elif file_count >= 3:
            return 1.1
        return 1.0

    def _get_complexity_multiplier(self, complexity: str) -> float:
        """복잡도에 따른 가중치"""
        multipliers = {"low": 0.8, "medium": 1.0, "high": 1.3, "critical": 1.5}
        return multipliers.get(complexity, 1.0)

    def _get_recommendation(
        self, estimated: int, remaining: int, can_proceed: bool
    ) -> str:
        """권장 사항 생성"""
        if can_proceed:
            usage = self.current_context + estimated
            if usage >= 80:
                return f"진행 가능 (예상 {usage}% - 80% 임계값 근접)"
            elif usage >= 60:
                return f"진행 가능 (예상 {usage}% - 모니터링 권장)"
            else:
                return f"진행 가능 (예상 {usage}% - 여유 있음)"
        else:
            return f"정리 필요 (예상 {estimated}% > 남은 {remaining}%)"


def predict_and_decide(
    current_context: int, next_task: dict, threshold: int = 20
) -> dict:
    """
    Context 예측 및 결정 (간편 함수)

    Args:
        current_context: 현재 context 사용량 (%)
        next_task: 다음 작업 정보
        threshold: 정리 임계값 (기본 20%)

    Returns:
        {
            "action": "continue" | "cleanup",
            "estimate": TaskEstimate,
            "message": str
        }
    """
    predictor = ContextPredictor(current_context)
    should_clean, estimate = predictor.should_cleanup(next_task, threshold)

    if should_clean:
        action = "cleanup"
        message = (
            f"Context {current_context}% + 예상 {estimate.adjusted_estimate}% "
            f"= {current_context + estimate.adjusted_estimate}% (정리 필요)"
        )
    else:
        action = "continue"
        message = (
            f"Context {current_context}% + 예상 {estimate.adjusted_estimate}% "
            f"= {current_context + estimate.adjusted_estimate}% (계속 진행)"
        )

    return {"action": action, "estimate": estimate, "message": message}


if __name__ == "__main__":
    # 테스트
    predictor = ContextPredictor(current_context=82)

    # 단일 작업 예측
    task = {"type": "issue_fix_medium", "affected_files": 5, "complexity": "high"}

    should_clean, estimate = predictor.should_cleanup(task)
    print(f"작업: {task['type']}")
    print(f"예상 Context: {estimate.adjusted_estimate}%")
    print(f"남은 여유: {estimate.remaining_context}%")
    print(f"정리 필요: {should_clean}")
    print(f"권장: {estimate.recommendation}")
    print()

    # 간편 함수 테스트
    result = predict_and_decide(82, task)
    print(f"결정: {result['action']}")
    print(f"메시지: {result['message']}")

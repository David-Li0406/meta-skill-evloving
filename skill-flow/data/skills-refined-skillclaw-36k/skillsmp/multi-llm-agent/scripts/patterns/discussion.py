"""
토론/합의 패턴
여러 에이전트가 주제에 대해 토론하고 합의를 도출합니다.
"""

from .base import BasePattern, PatternResult


class DiscussionPattern(BasePattern):
    """토론/합의 패턴"""

    @property
    def pattern_name(self) -> str:
        return "discussion"

    def execute(
        self,
        topic: str,
        rounds: int = 3,
        consensus_threshold: float = 0.7,
        moderator: str = None
    ) -> PatternResult:
        """
        토론/합의 패턴 실행

        Args:
            topic: 토론 주제
            rounds: 토론 라운드 수
            consensus_threshold: 합의 임계값 (0~1)
            moderator: 사회자 에이전트 이름 (없으면 첫 번째 에이전트)

        Returns:
            PatternResult: 실행 결과
        """
        self.start_execution()
        result = PatternResult(
            pattern_name=self.pattern_name,
            agents_used=list(self.agents.keys())
        )
        discussion_history = []

        # 초기 의견 수집
        self.log("초기 의견 수집 중...")
        current_opinions = {}
        for name, agent in self.agents.items():
            prompt = f"""다음 주제에 대한 당신의 의견을 제시하세요.

주제: {topic}

다음 형식으로 답변하세요:
1. 핵심 주장 (1-2문장)
2. 근거 (2-3개)
3. 예상되는 반론과 그에 대한 대응"""

            response = agent.chat(prompt)
            current_opinions[name] = response.content
            self.track_tokens(response)

        discussion_history.append({
            "round": 0,
            "type": "initial",
            "opinions": current_opinions.copy()
        })

        # 토론 라운드
        for round_num in range(1, rounds + 1):
            self.log(f"라운드 {round_num}/{rounds}")
            new_opinions = {}

            for name, agent in self.agents.items():
                other_opinions = self._format_other_opinions(current_opinions, name)

                prompt = f"""주제: {topic}

=== 다른 참여자들의 의견 ===
{other_opinions}

=== 당신의 이전 의견 ===
{current_opinions[name]}

위 의견들을 고려하여 다음을 제시하세요:
1. 동의하는 점과 이유 (구체적으로 누구의 어떤 주장에 동의하는지)
2. 반박 또는 보완할 점
3. 수정된 당신의 입장 (의견이 바뀌었다면 그 이유도 설명)"""

                response = agent.chat(prompt)
                new_opinions[name] = response.content
                self.track_tokens(response)

            discussion_history.append({
                "round": round_num,
                "type": "debate",
                "opinions": new_opinions.copy()
            })
            current_opinions = new_opinions

        # 합의 도출
        self.log("합의 도출 중...")
        moderator_agent = self.agents.get(moderator) or list(self.agents.values())[0]
        moderator_name = moderator or list(self.agents.keys())[0]

        all_opinions = self._format_all_opinions(current_opinions)
        synthesis_prompt = f"""당신은 토론의 사회자입니다.

주제: {topic}

=== 최종 토론 결과 ===
{all_opinions}

위 토론을 종합하여 다음을 정리해주세요:

## 1. 합의된 사항
- 모든 참여자가 동의한 점들

## 2. 의견이 갈리는 사항
- 여전히 의견이 다른 점들과 각 입장

## 3. 핵심 인사이트
- 토론을 통해 도출된 중요한 통찰

## 4. 권장 사항 / 결론
- 위 토론을 바탕으로 한 최종 권장 사항"""

        synthesis_response = moderator_agent.chat(synthesis_prompt)
        self.track_tokens(synthesis_response)

        elapsed = self.end_execution()
        result.execution_log = discussion_history
        result.final_result = synthesis_response.content
        result.intermediate_results = current_opinions
        result.metadata = {
            "total_tokens": self.total_tokens,
            "execution_time": elapsed,
            "rounds_completed": rounds,
            "moderator": moderator_name,
            "participants": list(self.agents.keys())
        }

        return result

    def _format_other_opinions(self, opinions: dict, exclude: str) -> str:
        """다른 참여자 의견 포맷팅"""
        parts = []
        for name, opinion in opinions.items():
            if name != exclude:
                agent = self.agents[name]
                role_info = f" ({agent.role})" if agent.role else ""
                parts.append(f"### {name}{role_info}\n{opinion}")
        return "\n\n".join(parts)

    def _format_all_opinions(self, opinions: dict) -> str:
        """모든 참여자 의견 포맷팅"""
        parts = []
        for name, opinion in opinions.items():
            agent = self.agents[name]
            role_info = f" ({agent.role})" if agent.role else ""
            parts.append(f"### {name}{role_info}\n{opinion}")
        return "\n\n".join(parts)


def execute_discussion(
    agents: dict,
    topic: str,
    rounds: int = 3,
    consensus_threshold: float = 0.7,
    moderator: str = None,
    verbose: bool = True
) -> PatternResult:
    """토론/합의 패턴 실행 헬퍼 함수"""
    pattern = DiscussionPattern(agents, verbose)
    return pattern.execute(topic, rounds, consensus_threshold, moderator)

"""
병렬 + 종합 패턴
여러 에이전트가 동시에 작업 후 결과를 종합합니다.
"""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base import BasePattern, PatternResult


class ParallelPattern(BasePattern):
    """병렬 + 종합 패턴"""

    @property
    def pattern_name(self) -> str:
        return "parallel"

    def execute(
        self,
        task: str,
        aggregation: str = "synthesize",
        max_workers: int = None,
        synthesizer: str = None
    ) -> PatternResult:
        """
        병렬 + 종합 패턴 실행

        Args:
            task: 수행할 작업
            aggregation: 결과 종합 방식
                - "synthesize": 모든 결과를 종합
                - "vote": 다수결
                - "best_of": 가장 좋은 결과 선택
                - "compare": 결과 비교 분석
                - "union": 모든 결과 합집합
            max_workers: 최대 병렬 워커 수
            synthesizer: 종합 담당 에이전트 이름

        Returns:
            PatternResult: 실행 결과
        """
        self.start_execution()
        result = PatternResult(
            pattern_name=self.pattern_name,
            agents_used=list(self.agents.keys())
        )
        outputs = {}

        # 병렬 실행
        self.log(f"병렬 실행 시작: {len(self.agents)} 에이전트")
        max_workers = max_workers or len(self.agents)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._execute_agent, name, agent, task): name
                for name, agent in self.agents.items()
            }

            for future in as_completed(futures):
                name = futures[future]
                try:
                    response = future.result()
                    outputs[name] = response.content
                    self.track_tokens(response)

                    result.execution_log.append({
                        "agent": name,
                        "role": self.agents[name].role,
                        "provider": self.agents[name].provider,
                        "model": self.agents[name].model,
                        "output_preview": self._preview(response.content),
                        "latency": response.latency,
                        "tokens": response.usage.get("total_tokens", 0)
                    })
                    self.log(f"  완료: {name} ({response.latency:.2f}s)")
                except Exception as e:
                    self.log(f"  오류: {name} - {e}")
                    outputs[name] = f"[오류 발생: {e}]"

        # 결과 종합
        self.log(f"결과 종합: {aggregation}")
        final_result = self._aggregate_results(outputs, aggregation, synthesizer)

        elapsed = self.end_execution()
        result.final_result = final_result
        result.intermediate_results = outputs
        result.metadata = {
            "total_tokens": self.total_tokens,
            "execution_time": elapsed,
            "aggregation": aggregation,
            "agent_count": len(self.agents)
        }

        return result

    def _execute_agent(self, name: str, agent, task: str):
        """단일 에이전트 실행"""
        return agent.chat(task)

    def _aggregate_results(self, outputs: dict, aggregation: str, synthesizer: str = None):
        """결과 종합"""
        synthesizer_agent = self.agents.get(synthesizer) or list(self.agents.values())[0]

        if aggregation == "synthesize":
            return self._synthesize(outputs, synthesizer_agent)
        elif aggregation == "vote":
            return self._vote(outputs, synthesizer_agent)
        elif aggregation == "best_of":
            return self._best_of(outputs, synthesizer_agent)
        elif aggregation == "compare":
            return self._compare(outputs, synthesizer_agent)
        elif aggregation == "union":
            return self._union(outputs)
        else:
            return self._synthesize(outputs, synthesizer_agent)

    def _synthesize(self, outputs: dict, synthesizer_agent) -> str:
        """결과 종합"""
        all_outputs = self._format_outputs(outputs)
        prompt = f"""다음은 여러 전문가의 분석 결과입니다:

{all_outputs}

위 결과들을 종합하여 다음을 정리해주세요:

## 1. 공통적으로 지적된 사항
주요 내용들을 정리

## 2. 각 전문가의 고유한 인사이트
다른 전문가가 언급하지 않은 독특한 관점들

## 3. 종합적인 결론
모든 분석을 고려한 최종 결론 및 권장 사항"""

        response = synthesizer_agent.chat(prompt)
        self.track_tokens(response)
        return response.content

    def _vote(self, outputs: dict, synthesizer_agent) -> str:
        """다수결 집계"""
        all_outputs = self._format_outputs(outputs)
        prompt = f"""다음은 여러 전문가의 의견입니다:

{all_outputs}

각 전문가의 핵심 결론을 추출하고, 다수결 원칙에 따라:
1. 가장 많은 지지를 받은 의견
2. 각 의견의 지지 비율
3. 다수 의견에 대한 요약

을 정리해주세요."""

        response = synthesizer_agent.chat(prompt)
        self.track_tokens(response)
        return response.content

    def _best_of(self, outputs: dict, synthesizer_agent) -> str:
        """최선의 결과 선택"""
        all_outputs = self._format_outputs(outputs)
        prompt = f"""다음은 여러 전문가의 분석 결과입니다:

{all_outputs}

위 결과들 중 가장 우수한 것을 선택하고:
1. 선택한 결과와 해당 전문가
2. 선택 이유 (왜 이 결과가 가장 좋은지)
3. 다른 결과들의 부족한 점

을 설명해주세요."""

        response = synthesizer_agent.chat(prompt)
        self.track_tokens(response)
        return response.content

    def _compare(self, outputs: dict, synthesizer_agent) -> str:
        """결과 비교 분석"""
        all_outputs = self._format_outputs(outputs)
        prompt = f"""다음은 여러 전문가의 분석 결과입니다:

{all_outputs}

각 결과를 비교 분석하여:
1. 유사점
2. 차이점
3. 각 접근 방식의 장단점
4. 상황별 권장 사항

을 정리해주세요."""

        response = synthesizer_agent.chat(prompt)
        self.track_tokens(response)
        return response.content

    def _union(self, outputs: dict) -> str:
        """모든 결과 합집합"""
        parts = []
        for name, output in outputs.items():
            agent = self.agents[name]
            role_info = f" ({agent.role})" if agent.role else ""
            parts.append(f"## {name}{role_info}\n\n{output}")
        return "\n\n---\n\n".join(parts)

    def _format_outputs(self, outputs: dict) -> str:
        """출력 포맷팅"""
        parts = []
        for name, output in outputs.items():
            agent = self.agents[name]
            role_info = f" ({agent.role})" if agent.role else ""
            provider_info = f"[{agent.provider}/{agent.model}]"
            parts.append(f"### {name}{role_info} {provider_info}\n{output}")
        return "\n\n".join(parts)

    def _preview(self, text: str, max_length: int = 200) -> str:
        """텍스트 미리보기"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text


def execute_parallel(
    agents: dict,
    task: str,
    aggregation: str = "synthesize",
    max_workers: int = None,
    synthesizer: str = None,
    verbose: bool = True
) -> PatternResult:
    """병렬 + 종합 패턴 실행 헬퍼 함수"""
    pattern = ParallelPattern(agents, verbose)
    return pattern.execute(task, aggregation, max_workers, synthesizer)

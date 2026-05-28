"""
체인 파이프라인 패턴
순차적으로 결과를 전달하며 처리합니다.
"""

from .base import BasePattern, PatternResult


class ChainPattern(BasePattern):
    """체인 파이프라인 패턴"""

    @property
    def pattern_name(self) -> str:
        return "chain"

    def execute(self, pipeline: list[dict], input_data: str) -> PatternResult:
        """
        체인 파이프라인 패턴 실행

        Args:
            pipeline: 파이프라인 정의
                [
                    {"agent": "analyzer", "task": "분석"},
                    {"agent": "translator", "task": "번역"},
                ]
            input_data: 초기 입력 데이터

        Returns:
            PatternResult: 실행 결과
        """
        self.start_execution()
        result = PatternResult(
            pattern_name=self.pattern_name,
            agents_used=[step["agent"] for step in pipeline]
        )
        current_output = input_data
        step_outputs = {"input": input_data}

        for i, step in enumerate(pipeline):
            agent_name = step["agent"]
            task = step.get("task", "처리")
            custom_prompt = step.get("prompt")
            transform = step.get("transform")  # 출력 변환 함수명

            agent = self.get_agent(agent_name)
            self.log(f"Step {i+1}/{len(pipeline)}: {agent_name} - {task}")

            # 프롬프트 구성
            if custom_prompt:
                prompt = custom_prompt.format(input=current_output)
            else:
                prompt = f"""작업: {task}

=== 입력 데이터 ===
{current_output}

위 데이터를 처리하여 결과를 출력하세요."""

            response = agent.chat(prompt)
            current_output = response.content
            self.track_tokens(response)

            # 출력 저장
            step_key = f"step_{i+1}_{agent_name}"
            step_outputs[step_key] = current_output

            result.execution_log.append({
                "step": i + 1,
                "agent": agent_name,
                "task": task,
                "input_preview": self._preview(step_outputs.get(f"step_{i}_{pipeline[i-1]['agent']}", input_data) if i > 0 else input_data),
                "output_preview": self._preview(current_output),
                "latency": response.latency,
                "tokens": response.usage.get("total_tokens", 0)
            })

        elapsed = self.end_execution()
        result.final_result = current_output
        result.intermediate_results = step_outputs
        result.metadata = {
            "total_tokens": self.total_tokens,
            "execution_time": elapsed,
            "pipeline_steps": len(pipeline)
        }

        return result

    def _preview(self, text: str, max_length: int = 200) -> str:
        """텍스트 미리보기"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text


class TransformChainPattern(ChainPattern):
    """변환 기능이 추가된 체인 패턴"""

    def execute_with_transforms(
        self,
        pipeline: list[dict],
        input_data: str,
        transforms: dict = None
    ) -> PatternResult:
        """
        변환 함수를 지원하는 체인 실행

        Args:
            pipeline: 파이프라인 정의
            input_data: 초기 입력
            transforms: 변환 함수 딕셔너리 {"transform_name": callable}
        """
        transforms = transforms or {}
        self.start_execution()
        result = PatternResult(
            pattern_name=self.pattern_name,
            agents_used=[step["agent"] for step in pipeline]
        )
        current_output = input_data
        step_outputs = {"input": input_data}

        for i, step in enumerate(pipeline):
            agent_name = step["agent"]
            task = step.get("task", "처리")
            transform_name = step.get("transform")

            agent = self.get_agent(agent_name)
            self.log(f"Step {i+1}: {agent_name} - {task}")

            prompt = f"""작업: {task}

=== 입력 데이터 ===
{current_output}

위 데이터를 처리하여 결과를 출력하세요."""

            response = agent.chat(prompt)
            current_output = response.content
            self.track_tokens(response)

            # 변환 적용
            if transform_name and transform_name in transforms:
                current_output = transforms[transform_name](current_output)
                self.log(f"  변환 적용: {transform_name}")

            step_key = f"step_{i+1}_{agent_name}"
            step_outputs[step_key] = current_output

            result.execution_log.append({
                "step": i + 1,
                "agent": agent_name,
                "task": task,
                "transform": transform_name,
                "output_preview": self._preview(current_output),
                "latency": response.latency
            })

        elapsed = self.end_execution()
        result.final_result = current_output
        result.intermediate_results = step_outputs
        result.metadata = {
            "total_tokens": self.total_tokens,
            "execution_time": elapsed,
            "pipeline_steps": len(pipeline)
        }

        return result


def execute_chain(
    agents: dict,
    pipeline: list[dict],
    input_data: str,
    verbose: bool = True
) -> PatternResult:
    """체인 파이프라인 패턴 실행 헬퍼 함수"""
    pattern = ChainPattern(agents, verbose)
    return pattern.execute(pipeline, input_data)

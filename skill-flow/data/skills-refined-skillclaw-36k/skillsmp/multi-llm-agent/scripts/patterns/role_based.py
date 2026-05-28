"""
역할 분담 패턴
각 에이전트가 전문 역할을 맡아 순차적으로 협업합니다.
"""

from .base import BasePattern, PatternResult


class RoleBasedPattern(BasePattern):
    """역할 분담 패턴"""

    @property
    def pattern_name(self) -> str:
        return "role_based"

    def execute(self, task: str, workflow: list[dict]) -> PatternResult:
        """
        역할 분담 패턴 실행

        Args:
            task: 수행할 작업
            workflow: 워크플로우 정의
                [
                    {"agent": "coder", "action": "implement"},
                    {"agent": "reviewer", "action": "review", "input_from": "coder"},
                ]

        Returns:
            PatternResult: 실행 결과
        """
        self.start_execution()
        result = PatternResult(
            pattern_name=self.pattern_name,
            agents_used=list(set(step["agent"] for step in workflow))
        )
        outputs = {}

        for i, step in enumerate(workflow):
            agent_name = step["agent"]
            action = step.get("action", "process")
            input_from = step.get("input_from")
            custom_prompt = step.get("prompt")

            agent = self.get_agent(agent_name)
            self.log(f"Step {i+1}: {agent_name} - {action}")

            # 이전 단계 결과를 컨텍스트로 제공
            context = None
            if input_from:
                if isinstance(input_from, str):
                    input_from = [input_from]
                context_parts = []
                for src in input_from:
                    if src in outputs:
                        context_parts.append(f"[{src}의 결과]:\n{outputs[src]}")
                if context_parts:
                    context = "\n\n".join(context_parts)

            # 프롬프트 구성
            if custom_prompt:
                prompt = custom_prompt
            else:
                prompt = f"작업: {task}\n역할: {agent.role}\n수행할 행동: {action}"

            response = agent.chat(prompt, context=context)
            outputs[agent_name] = response.content
            self.track_tokens(response)

            result.execution_log.append({
                "step": i + 1,
                "agent": agent_name,
                "action": action,
                "input_from": input_from,
                "output": response.content,
                "latency": response.latency,
                "tokens": response.usage.get("total_tokens", 0)
            })

        elapsed = self.end_execution()
        result.final_result = outputs.get(workflow[-1]["agent"], "")
        result.intermediate_results = outputs
        result.metadata = {
            "total_tokens": self.total_tokens,
            "execution_time": elapsed,
            "workflow_steps": len(workflow)
        }

        return result


def execute_role_based(agents: dict, task: str, workflow: list[dict], verbose: bool = True) -> PatternResult:
    """역할 분담 패턴 실행 헬퍼 함수"""
    pattern = RoleBasedPattern(agents, verbose)
    return pattern.execute(task, workflow)

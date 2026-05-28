#!/usr/bin/env python3
"""
멀티 에이전트 오케스트레이터
여러 LLM 에이전트를 다양한 협업 패턴으로 조율합니다.
"""

import os
import sys
import json
import argparse
import time
from dataclasses import dataclass, field
from typing import Optional, Callable
from pathlib import Path

import yaml

# 현재 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

from llm_client import LLMClientFactory, BaseLLMClient, Message, LLMResponse


@dataclass
class Agent:
    """에이전트 정의"""
    name: str
    provider: str
    model: str
    role: str = ""
    system_prompt: str = ""
    client: Optional[BaseLLMClient] = None

    def __post_init__(self):
        if self.client is None:
            self.client = LLMClientFactory.create(self.provider, self.model)

    def chat(self, prompt: str, context: Optional[str] = None, **kwargs) -> LLMResponse:
        """에이전트에게 메시지 전송"""
        messages = []
        system = self.system_prompt or f"당신은 {self.role} 역할을 수행하는 AI 에이전트입니다."
        if context:
            system += f"\n\n컨텍스트:\n{context}"
        messages.append(Message(role="system", content=system))
        messages.append(Message(role="user", content=prompt))
        return self.client.chat(messages, **kwargs)


@dataclass
class ExecutionResult:
    """실행 결과"""
    pattern: str
    agents_used: list[str]
    execution_log: list[dict] = field(default_factory=list)
    final_result: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "pattern": self.pattern,
            "agents_used": self.agents_used,
            "execution_log": self.execution_log,
            "final_result": self.final_result,
            "metadata": self.metadata
        }


class Orchestrator:
    """멀티 에이전트 오케스트레이터"""

    def __init__(self, agents: list[Agent], verbose: bool = True):
        self.agents = {agent.name: agent for agent in agents}
        self.verbose = verbose
        self.execution_log = []

    def log(self, message: str):
        """로그 출력"""
        if self.verbose:
            print(f"[Orchestrator] {message}")

    def get_agent(self, name: str) -> Agent:
        """에이전트 조회"""
        if name not in self.agents:
            raise ValueError(f"Agent not found: {name}. Available: {list(self.agents.keys())}")
        return self.agents[name]

    # ========== 역할 분담 패턴 ==========
    def execute_role_based(self, task: str, workflow: list[dict]) -> ExecutionResult:
        """
        역할 분담 패턴 실행

        workflow 예시:
        [
            {"agent": "coder", "action": "implement"},
            {"agent": "reviewer", "action": "review", "input_from": "coder"},
            {"agent": "tester", "action": "test", "input_from": "coder"}
        ]
        """
        self.log(f"역할 분담 패턴 시작: {task}")
        result = ExecutionResult(
            pattern="role_based",
            agents_used=list(set(step["agent"] for step in workflow))
        )
        start_time = time.time()
        outputs = {}
        total_tokens = 0

        for i, step in enumerate(workflow):
            agent_name = step["agent"]
            action = step.get("action", "process")
            input_from = step.get("input_from")

            agent = self.get_agent(agent_name)
            self.log(f"Step {i+1}: {agent_name} - {action}")

            context = None
            if input_from and input_from in outputs:
                context = f"이전 단계 ({input_from})의 결과:\n{outputs[input_from]}"

            prompt = f"작업: {task}\n역할: {agent.role}\n수행할 행동: {action}"
            response = agent.chat(prompt, context=context)

            outputs[agent_name] = response.content
            total_tokens += response.usage.get("total_tokens", 0)

            result.execution_log.append({
                "step": i + 1,
                "agent": agent_name,
                "action": action,
                "input_from": input_from,
                "output_preview": response.content[:200] + "..." if len(response.content) > 200 else response.content,
                "latency": response.latency
            })

        result.final_result = outputs.get(workflow[-1]["agent"], "")
        result.metadata = {
            "total_tokens": total_tokens,
            "execution_time": time.time() - start_time,
            "all_outputs": outputs
        }

        self.log(f"역할 분담 완료 - 총 {len(workflow)} 단계 실행")
        return result

    # ========== 토론/합의 패턴 ==========
    def execute_discussion(self, topic: str, rounds: int = 3, consensus_threshold: float = 0.7) -> ExecutionResult:
        """
        토론/합의 패턴 실행

        여러 에이전트가 주제에 대해 토론하고 합의를 도출합니다.
        """
        self.log(f"토론 패턴 시작: {topic} ({rounds} 라운드)")
        result = ExecutionResult(
            pattern="discussion",
            agents_used=list(self.agents.keys())
        )
        start_time = time.time()
        total_tokens = 0
        discussion_history = []

        # 초기 의견 수집
        self.log("초기 의견 수집 중...")
        initial_opinions = {}
        for name, agent in self.agents.items():
            prompt = f"다음 주제에 대한 당신의 의견을 제시하세요:\n\n{topic}"
            response = agent.chat(prompt)
            initial_opinions[name] = response.content
            total_tokens += response.usage.get("total_tokens", 0)

        discussion_history.append({"round": 0, "type": "initial", "opinions": initial_opinions})

        # 토론 라운드
        for round_num in range(1, rounds + 1):
            self.log(f"라운드 {round_num}/{rounds}")
            round_opinions = {}

            for name, agent in self.agents.items():
                other_opinions = "\n\n".join([
                    f"[{other_name}의 의견]: {opinion}"
                    for other_name, opinion in initial_opinions.items()
                    if other_name != name
                ])

                prompt = f"""주제: {topic}

다른 참여자들의 의견:
{other_opinions}

이 의견들을 고려하여:
1. 동의하는 점과 그 이유
2. 반박하거나 보완할 점
3. 수정된 당신의 입장

을 제시하세요."""

                response = agent.chat(prompt)
                round_opinions[name] = response.content
                total_tokens += response.usage.get("total_tokens", 0)

            discussion_history.append({"round": round_num, "opinions": round_opinions})
            initial_opinions = round_opinions

        # 합의 도출
        self.log("합의 도출 중...")
        all_opinions = "\n\n".join([
            f"[{name}의 최종 의견]: {opinion}"
            for name, opinion in initial_opinions.items()
        ])

        # 첫 번째 에이전트가 합의 정리
        synthesizer = list(self.agents.values())[0]
        synthesis_prompt = f"""다음은 '{topic}'에 대한 토론 결과입니다:

{all_opinions}

위 토론을 종합하여:
1. 공통으로 합의된 사항
2. 여전히 의견이 갈리는 사항
3. 최종 결론 또는 권장 사항

을 정리해주세요."""

        synthesis_response = synthesizer.chat(synthesis_prompt)
        total_tokens += synthesis_response.usage.get("total_tokens", 0)

        result.execution_log = discussion_history
        result.final_result = synthesis_response.content
        result.metadata = {
            "total_tokens": total_tokens,
            "execution_time": time.time() - start_time,
            "rounds_completed": rounds
        }

        self.log("토론 완료")
        return result

    # ========== 체인 파이프라인 패턴 ==========
    def execute_chain(self, pipeline: list[dict], input_data: str) -> ExecutionResult:
        """
        체인 파이프라인 패턴 실행

        pipeline 예시:
        [
            {"agent": "analyzer", "task": "분석"},
            {"agent": "translator", "task": "번역"},
            {"agent": "formatter", "task": "포맷팅"}
        ]
        """
        self.log(f"체인 파이프라인 시작: {len(pipeline)} 단계")
        result = ExecutionResult(
            pattern="chain",
            agents_used=[step["agent"] for step in pipeline]
        )
        start_time = time.time()
        total_tokens = 0
        current_output = input_data

        for i, step in enumerate(pipeline):
            agent_name = step["agent"]
            task = step.get("task", "처리")

            agent = self.get_agent(agent_name)
            self.log(f"Step {i+1}/{len(pipeline)}: {agent_name} - {task}")

            prompt = f"""작업: {task}

입력 데이터:
{current_output}

위 데이터를 처리하여 결과를 출력하세요."""

            response = agent.chat(prompt)
            current_output = response.content
            total_tokens += response.usage.get("total_tokens", 0)

            result.execution_log.append({
                "step": i + 1,
                "agent": agent_name,
                "task": task,
                "output_preview": current_output[:200] + "..." if len(current_output) > 200 else current_output,
                "latency": response.latency
            })

        result.final_result = current_output
        result.metadata = {
            "total_tokens": total_tokens,
            "execution_time": time.time() - start_time
        }

        self.log("체인 파이프라인 완료")
        return result

    # ========== 병렬 + 종합 패턴 ==========
    def execute_parallel(self, task: str, aggregation: str = "synthesize") -> ExecutionResult:
        """
        병렬 + 종합 패턴 실행

        모든 에이전트가 동시에 작업 후 결과를 종합합니다.

        aggregation 옵션:
        - "synthesize": 모든 결과를 종합
        - "vote": 다수결
        - "best_of": 가장 좋은 결과 선택
        """
        self.log(f"병렬 처리 시작: {len(self.agents)} 에이전트")
        result = ExecutionResult(
            pattern="parallel",
            agents_used=list(self.agents.keys())
        )
        start_time = time.time()
        total_tokens = 0
        outputs = {}

        # 병렬 실행 (실제로는 순차적이지만, 논리적으로 독립적)
        for name, agent in self.agents.items():
            self.log(f"실행 중: {name}")
            response = agent.chat(task)
            outputs[name] = response.content
            total_tokens += response.usage.get("total_tokens", 0)

            result.execution_log.append({
                "agent": name,
                "role": agent.role,
                "output_preview": response.content[:200] + "..." if len(response.content) > 200 else response.content,
                "latency": response.latency
            })

        # 결과 종합
        self.log(f"결과 종합 중: {aggregation}")
        if aggregation == "synthesize":
            all_outputs = "\n\n".join([
                f"[{name} ({self.agents[name].role})의 결과]:\n{output}"
                for name, output in outputs.items()
            ])

            synthesizer = list(self.agents.values())[0]
            synthesis_prompt = f"""다음은 여러 전문가의 분석 결과입니다:

{all_outputs}

위 결과들을 종합하여:
1. 공통적으로 지적된 사항
2. 각 전문가만의 고유한 인사이트
3. 종합적인 결론 및 권장 사항

을 정리해주세요."""

            synthesis_response = synthesizer.chat(synthesis_prompt)
            result.final_result = synthesis_response.content
            total_tokens += synthesis_response.usage.get("total_tokens", 0)

        elif aggregation == "vote":
            result.final_result = json.dumps(outputs, ensure_ascii=False, indent=2)

        elif aggregation == "best_of":
            # 첫 번째 에이전트가 최선의 결과 선택
            evaluator = list(self.agents.values())[0]
            eval_prompt = f"""다음 결과들 중 가장 좋은 것을 선택하고 이유를 설명하세요:

{json.dumps(outputs, ensure_ascii=False, indent=2)}"""

            eval_response = evaluator.chat(eval_prompt)
            result.final_result = eval_response.content
            total_tokens += eval_response.usage.get("total_tokens", 0)

        result.metadata = {
            "total_tokens": total_tokens,
            "execution_time": time.time() - start_time,
            "aggregation": aggregation,
            "all_outputs": outputs
        }

        self.log("병렬 처리 완료")
        return result


def load_config(config_path: str) -> dict:
    """YAML 설정 파일 로드"""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_agents(agents_json: str) -> list[Agent]:
    """JSON 문자열에서 에이전트 목록 파싱"""
    agents_data = json.loads(agents_json)
    return [
        Agent(
            name=a["name"],
            provider=a["provider"],
            model=a["model"],
            role=a.get("role", ""),
            system_prompt=a.get("system_prompt", "")
        )
        for a in agents_data
    ]


def main():
    parser = argparse.ArgumentParser(description="멀티 에이전트 오케스트레이터")
    parser.add_argument("--pattern", required=True, choices=["role_based", "discussion", "chain", "parallel"],
                        help="협업 패턴")
    parser.add_argument("--agents", help="에이전트 설정 (JSON 문자열)")
    parser.add_argument("--config", help="설정 파일 경로 (YAML)")
    parser.add_argument("--task", help="수행할 작업")
    parser.add_argument("--topic", help="토론 주제 (discussion 패턴)")
    parser.add_argument("--input", help="입력 데이터 또는 파일 경로 (chain 패턴)")
    parser.add_argument("--workflow", help="워크플로우 설정 (JSON, role_based 패턴)")
    parser.add_argument("--pipeline", help="파이프라인 설정 (JSON, chain 패턴)")
    parser.add_argument("--rounds", type=int, default=3, help="토론 라운드 수")
    parser.add_argument("--aggregation", default="synthesize", help="병렬 결과 종합 방식")
    parser.add_argument("--output", help="결과 출력 파일")
    parser.add_argument("--quiet", action="store_true", help="로그 출력 비활성화")

    args = parser.parse_args()

    # 에이전트 로드
    agents = []
    if args.config:
        config = load_config(args.config)
        agents_data = config.get("agents", [])
        agents = [
            Agent(
                name=a["name"],
                provider=a["provider"],
                model=a["model"],
                role=a.get("role", ""),
                system_prompt=a.get("system_prompt", "")
            )
            for a in agents_data
        ]
    elif args.agents:
        agents = parse_agents(args.agents)
    else:
        print("에이전트 설정이 필요합니다. --agents 또는 --config 사용")
        sys.exit(1)

    orchestrator = Orchestrator(agents, verbose=not args.quiet)

    # 패턴별 실행
    result = None
    if args.pattern == "role_based":
        workflow = json.loads(args.workflow) if args.workflow else [
            {"agent": agents[i].name, "action": "process", "input_from": agents[i-1].name if i > 0 else None}
            for i in range(len(agents))
        ]
        result = orchestrator.execute_role_based(args.task or "작업 수행", workflow)

    elif args.pattern == "discussion":
        result = orchestrator.execute_discussion(args.topic or args.task, rounds=args.rounds)

    elif args.pattern == "chain":
        pipeline = json.loads(args.pipeline) if args.pipeline else [
            {"agent": a.name, "task": a.role or "처리"} for a in agents
        ]
        input_data = args.input
        if input_data and os.path.isfile(input_data):
            with open(input_data, "r", encoding="utf-8") as f:
                input_data = f.read()
        result = orchestrator.execute_chain(pipeline, input_data or args.task)

    elif args.pattern == "parallel":
        result = orchestrator.execute_parallel(args.task, aggregation=args.aggregation)

    # 결과 출력
    if result:
        output_data = result.to_dict()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"결과 저장: {args.output}")
        else:
            print("\n" + "=" * 60)
            print("최종 결과:")
            print("=" * 60)
            print(result.final_result)
            print("\n" + "-" * 60)
            print(f"메타데이터: {json.dumps(result.metadata, ensure_ascii=False, default=str)}")


if __name__ == "__main__":
    main()

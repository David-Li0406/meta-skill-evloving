"""AgentSkillOS official benchmark: 30 tasks across 5 categories."""

from benchmark import register_benchmark
from benchmark.base import BenchmarkBase, BenchmarkMeta
from . import evaluators  # noqa: F401 — triggers @evaluator registration

from .types import (  # noqa: F401
    EvaluatorResult,
    TaskEvaluationResult,
    EvaluatorConfig,
    AggregationConfig,
    ScoringConfig,
    TaskConfig,
    ScoringMethod,
    EvaluatorType,
)
from .registry import (  # noqa: F401
    evaluator,
    get_evaluator,
    list_evaluators,
    register_evaluator,
    EVALUATOR_REGISTRY,
)
from .orchestrator import (  # noqa: F401
    EvaluationOrchestrator,
    evaluate_task,
    evaluate_task_sync,
    evaluate_task_from_dict,
)


@register_benchmark("AgentSkillOS_bench")
class AgentSkillOSBench(BenchmarkBase):
    meta = BenchmarkMeta(
        label="AgentSkillOS Bench",
        description="Official benchmark: 30 tasks across 5 categories",
        task_count=30,
        categories=[
            "data_computation",
            "document_creation",
            "motion_video",
            "visual_creation",
            "web_interaction",
        ],
    )

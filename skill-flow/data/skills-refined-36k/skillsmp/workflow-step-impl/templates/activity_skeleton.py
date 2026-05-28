from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class StepActivityInput:
    tenant_id: str
    workflow_run_id: str
    step: str
    payload: Mapping[str, Any]
    input_digest: str


@dataclass(frozen=True)
class StepActivityOutput:
    output_path: str
    output_digest: str
    summary: str
    metrics: dict[str, Any]


class StorageClient:
    def exists(self, path: str) -> bool: ...

    def read_json(self, path: str) -> dict[str, Any]: ...

    def write_json(self, path: str, data: Mapping[str, Any]) -> None: ...


def compute_output_path(*, tenant_id: str, workflow_run_id: str, step: str) -> str:
    return f"storage/{tenant_id}/{workflow_run_id}/{step}/output.json"


def compute_digest(data: Mapping[str, Any]) -> str:
    """
    TODO: sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    """
    raise NotImplementedError


async def run_step_activity(
    input: StepActivityInput,
    *,
    storage: StorageClient,
) -> StepActivityOutput:
    """
    Template:
    - Idempotent: if output already exists, return it.
    - Store heavy output in storage; return only path/digest/summary/metrics.
    """

    output_path = compute_output_path(
        tenant_id=input.tenant_id,
        workflow_run_id=input.workflow_run_id,
        step=input.step,
    )

    if storage.exists(output_path):
        existing = storage.read_json(output_path)
        return StepActivityOutput(
            output_path=output_path,
            output_digest=compute_digest(existing),
            summary=existing.get("summary", ""),
            metrics=existing.get("metrics", {}),
        )

    # TODO: call LLM / tools / LangGraph graph using input.payload
    output: dict[str, Any] = {
        "summary": "",
        "metrics": {},
        "data": {},
    }

    storage.write_json(output_path, output)
    return StepActivityOutput(
        output_path=output_path,
        output_digest=compute_digest(output),
        summary=output.get("summary", ""),
        metrics=output.get("metrics", {}),
    )

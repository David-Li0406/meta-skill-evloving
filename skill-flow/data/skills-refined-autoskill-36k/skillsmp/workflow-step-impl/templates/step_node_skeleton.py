from __future__ import annotations

from typing import Any


def step_node(state: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph node template:
    - Read required inputs from state/config
    - Produce a small, structured output (avoid huge blobs in state)
    - Validate schema strictly (fail fast)
    """

    # TODO: implement
    result: dict[str, Any] = {"summary": "", "data": {}}
    return {"step_result": result}

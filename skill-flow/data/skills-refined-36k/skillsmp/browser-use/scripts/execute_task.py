#!/usr/bin/env python3
"""
Execute browser automation task using Browser Use Cloud.

Usage:
    uv run execute_task.py "Find the top post on Hacker News"
    uv run execute_task.py "Search for Python tutorials" --llm gpt-4.1
    uv run execute_task.py "Extract product prices" --output-schema schema.json --json

Environment:
    BROWSER_USE_API_KEY must be set
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from browser_use_sdk import AsyncBrowserUse
from pydantic import BaseModel


def execute_task(
    task: str,
    output_schema: type[BaseModel] | None = None,
    save_screenshots: bool = False,
    output_dir: Path | None = None,
    timeout_minutes: int = 15,
    llm: str = "browser-use-llm",
    secrets: dict[str, str] | None = None,
) -> dict:
    """
    Execute a browser automation task via Browser Use Cloud.

    Args:
        task: Natural language description of the browser task
        output_schema: Pydantic model for structured output (optional)
        save_screenshots: Save screenshots to output directory
        output_dir: Directory for output files (default: output/)
        timeout_minutes: Task timeout in minutes (default: 15)
        llm: LLM model to use (default: browser-use-llm)
        secrets: Dict of secrets for credential injection. Use placeholders like
            {{key}} in the task string. The LLM sees placeholders, actual values
            are injected by the browser agent. Example: {"username": "user", "password": "pass"}

    Returns:
        dict with task_id, status, result, structured_output, etc.
    """
    return asyncio.run(_execute_task_async(
        task=task,
        output_schema=output_schema,
        save_screenshots=save_screenshots,
        output_dir=output_dir,
        timeout_minutes=timeout_minutes,
        llm=llm,
        secrets=secrets,
    ))


async def _execute_task_async(
    task: str,
    output_schema: type[BaseModel] | None = None,
    save_screenshots: bool = False,
    output_dir: Path | None = None,
    timeout_minutes: int = 15,
    llm: str = "browser-use-llm",
    secrets: dict[str, str] | None = None,
) -> dict:
    """Async implementation of execute_task."""
    start_time = time.time()

    # Validate API key
    if not os.environ.get("BROWSER_USE_API_KEY"):
        print("Error: BROWSER_USE_API_KEY environment variable must be set", file=sys.stderr)
        print("Get your API key at https://cloud.browser-use.com", file=sys.stderr)
        return {
            "task_id": None,
            "status": "failed",
            "error": "BROWSER_USE_API_KEY not set",
            "execution_time_seconds": 0,
            "result": None,
            "structured_output": None,
            "steps": [],
        }

    print(f"Task: {task[:100]}{'...' if len(task) > 100 else ''}", file=sys.stderr)
    print(f"LLM: {llm}", file=sys.stderr)
    print(f"Timeout: {timeout_minutes} minutes", file=sys.stderr)

    # Set up output directory
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent.parent / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize client
    api_key = os.environ.get("BROWSER_USE_API_KEY")
    client = AsyncBrowserUse(api_key=api_key)

    try:
        # Create task
        print("Creating browser task...", file=sys.stderr)
        task_config = {
            "task": task,
            "llm": llm,
        }
        if output_schema:
            task_config["schema"] = output_schema
        if secrets:
            task_config["secrets"] = secrets

        task_obj = await client.tasks.create_task(**task_config)
        task_id = task_obj.id if hasattr(task_obj, "id") else f"task_{int(start_time * 1000)}"
        print(f"Task ID: {task_id}", file=sys.stderr)

        # Stream progress updates
        steps = []
        print("Executing browser task...", file=sys.stderr)
        async for step in task_obj.stream():
            step_info = {
                "number": getattr(step, "number", len(steps) + 1),
                "url": getattr(step, "url", None),
                "goal": getattr(step, "next_goal", None),
            }
            steps.append(step_info)
            print(f"  Step {step_info['number']}: {step_info['goal'] or 'processing...'}", file=sys.stderr)

        # Get final result
        result = await task_obj.complete()
        elapsed = time.time() - start_time
        print(f"Task completed after {elapsed:.1f}s", file=sys.stderr)

        # Extract result data
        output_text = getattr(result, "output", None) or str(result)
        parsed_output = None
        if output_schema and hasattr(result, "parsed_output") and result.parsed_output:
            parsed_output = result.parsed_output.model_dump()

        return {
            "task_id": task_id,
            "status": "completed",
            "execution_time_seconds": elapsed,
            "result": output_text,
            "structured_output": parsed_output,
            "steps": steps,
            "step_count": len(steps),
        }

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"Task failed after {elapsed:.1f}s: {e}", file=sys.stderr)
        return {
            "task_id": task_id if "task_id" in dir() else None,
            "status": "failed",
            "error": str(e),
            "execution_time_seconds": elapsed,
            "result": None,
            "structured_output": None,
            "steps": steps if "steps" in dir() else [],
        }


def load_schema_from_file(schema_path: str) -> type[BaseModel] | None:
    """Load a Pydantic schema from a JSON schema file."""
    try:
        with open(schema_path) as f:
            schema_def = json.load(f)

        from pydantic import create_model

        fields = {}
        for prop_name, prop_def in schema_def.get("properties", {}).items():
            prop_type = prop_def.get("type", "string")
            type_map = {
                "string": str,
                "integer": int,
                "number": float,
                "boolean": bool,
                "array": list,
                "object": dict,
            }
            fields[prop_name] = (type_map.get(prop_type, str), ...)

        return create_model("DynamicSchema", **fields)
    except Exception as e:
        print(f"Warning: Could not load schema from {schema_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Execute browser automation task using Browser Use Cloud"
    )
    parser.add_argument(
        "task",
        help="Natural language description of the browser task",
    )
    parser.add_argument(
        "--output-schema",
        help="Path to JSON schema file for structured output",
    )
    parser.add_argument(
        "--save-screenshots",
        action="store_true",
        help="Save screenshots to output directory (if available)",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for output files (default: output/)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Task timeout in minutes (default: 15)",
    )
    parser.add_argument(
        "--llm",
        default="browser-use-llm",
        help="LLM model to use (default: browser-use-llm)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "--secrets",
        help='JSON dict of secrets for credential injection, e.g. \'{"username": "x", "password": "y"}\'',
    )

    args = parser.parse_args()

    # Load schema if provided
    output_schema = None
    if args.output_schema:
        output_schema = load_schema_from_file(args.output_schema)

    # Parse output directory
    output_dir = Path(args.output_dir) if args.output_dir else None

    # Parse secrets if provided
    secrets = None
    if args.secrets:
        try:
            secrets = json.loads(args.secrets)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON for --secrets: {e}", file=sys.stderr)
            sys.exit(1)

    result = execute_task(
        task=args.task,
        output_schema=output_schema,
        save_screenshots=args.save_screenshots,
        output_dir=output_dir,
        timeout_minutes=args.timeout,
        llm=args.llm,
        secrets=secrets,
    )

    if result["status"] == "failed" and result.get("error") == "BROWSER_USE_API_KEY not set":
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n=== Task Summary ===")
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")
        print(f"Duration: {result['execution_time_seconds']:.1f}s")
        print(f"Steps: {result['step_count']}")

        if result.get("result"):
            print(f"\n=== Result ===")
            print(result["result"])

        if result.get("structured_output"):
            print(f"\n=== Structured Output ===")
            print(json.dumps(result["structured_output"], indent=2))

        if result.get("error"):
            print(f"\n=== Error ===")
            print(result["error"])

    if result["status"] == "failed":
        sys.exit(1)


if __name__ == "__main__":
    main()

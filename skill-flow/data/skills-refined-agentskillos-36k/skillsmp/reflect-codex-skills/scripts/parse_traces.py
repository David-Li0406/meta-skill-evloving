"""Generate formatted trace examples from Codex session JSONL files.

Reads Codex session JSONL logs and writes `trace_examples.md` with response_item
excerpts formatted for human reading.

Example:
    python3 parse_traces.py --sessions-root ~/.codex/sessions --limit 3
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

from session_io import discover_session_files

MAX_STR_LEN = 2000
MAX_LIST_LEN = 10
ENTRIES_PER_FILE = 20
INDENT = "  "

DEFAULT_SESSIONS_ROOT = Path.home() / ".codex" / "sessions"
DEFAULT_SESSION_LIMIT = 3
DEFAULT_OUTPUT_PATH = Path("trace_examples.md")


def truncate_strings(value: Any, limit: int) -> Any:
    """Truncate strings in a nested structure to a max length.

    Args:
        value: Nested structure containing strings, lists, or dicts.
        limit: Maximum string length to keep.

    Returns:
        The structure with strings truncated to the requested length.
    """
    if isinstance(value, str):
        if len(value) <= limit:
            return value
        return value[: limit - 1] + "…"
    if isinstance(value, list):
        return [truncate_strings(value=item, limit=limit) for item in value]
    if isinstance(value, dict):
        return {
            key: truncate_strings(value=val, limit=limit) for key, val in value.items()
        }
    return value


def truncate_lists(value: Any, limit: int) -> Any:
    """Limit list lengths in a nested structure.

    Args:
        value: Nested structure containing lists or dicts.
        limit: Maximum list length to keep.

    Returns:
        The structure with list lengths truncated to the requested limit.
    """
    if isinstance(value, list):
        return [truncate_lists(value=item, limit=limit) for item in value[:limit]]
    if isinstance(value, dict):
        return {
            key: truncate_lists(value=val, limit=limit) for key, val in value.items()
        }
    return value


def collect_texts(value: Any) -> list[str]:
    """Collect explicit `text` fields from a nested payload.

    Args:
        value: Nested payload structure.

    Returns:
        List of text strings encountered in the payload.
    """
    texts: list[str] = []
    if isinstance(value, dict):
        for key, val in value.items():
            if key == "text" and isinstance(val, str):
                texts.append(val)
            else:
                texts.extend(collect_texts(value=val))
    elif isinstance(value, list):
        for item in value:
            texts.extend(collect_texts(value=item))
    return texts


def collect_arguments(value: Any) -> list[Any]:
    """Collect `arguments` fields from a nested payload.

    Args:
        value: Nested payload structure.

    Returns:
        List of argument payloads encountered in the payload.
    """
    args: list[Any] = []
    if isinstance(value, dict):
        for key, val in value.items():
            if key == "arguments":
                args.append(val)
            else:
                args.extend(collect_arguments(value=val))
    elif isinstance(value, list):
        for item in value:
            args.extend(collect_arguments(value=item))
    return args


def collect_output(value: Any) -> list[Any]:
    """Collect `output` fields from a nested payload.

    Args:
        value: Nested payload structure.

    Returns:
        List of output payloads encountered in the payload.
    """
    outputs: list[Any] = []
    if isinstance(value, dict):
        for key, val in value.items():
            if key == "output":
                outputs.append(val)
            else:
                outputs.extend(collect_output(value=val))
    elif isinstance(value, list):
        for item in value:
            outputs.extend(collect_output(value=item))
    return outputs


def reasoning_text_source(payload: dict[str, Any]) -> Any:
    """Return the best reasoning text source from a reasoning payload.

    Args:
        payload: Reasoning payload dictionary.

    Returns:
        The content or summary field when present, otherwise None.
    """
    content = payload.get("content")
    if content is not None:
        return content
    return payload.get("summary")


def render_multiline(value: str, indent: str) -> list[str]:
    """Render a multiline string with triple quotes and indentation.

    Args:
        value: Multiline string to render.
        indent: Indentation prefix for each line.

    Returns:
        List of formatted lines.
    """
    lines = ['"""', ""]
    for line in value.split("\n"):
        lines.append(f"{indent}{line}")
    lines.append('"""')
    return lines


def render_json(value: Any, indent_level: int) -> list[str]:
    """Render JSON with triple-quoted multiline strings for readability.

    Args:
        value: Value to render as JSON-like lines.
        indent_level: Current indentation level.

    Returns:
        List of formatted lines.
    """
    indent = INDENT * indent_level
    next_indent = INDENT * (indent_level + 1)

    if isinstance(value, dict):
        if not value:
            return ["{}"]
        lines = ["{"]
        items = list(value.items())
        for idx, (key, val) in enumerate(items):
            key_json = json.dumps(key)
            if isinstance(val, str) and "\n" in val:
                lines.append(f"{next_indent}{key_json}: \"\"\"")
                lines.append(f"{next_indent}")
                for line in val.split("\n"):
                    lines.append(f"{next_indent}{INDENT}{line}")
                lines.append(f"{next_indent}\"\"\"")
            else:
                rendered = render_json(value=val, indent_level=indent_level + 1)
                if len(rendered) == 1:
                    lines.append(f"{next_indent}{key_json}: {rendered[0]}")
                else:
                    lines.append(f"{next_indent}{key_json}: {rendered[0]}")
                    lines.extend([line for line in rendered[1:]])
            if idx < len(items) - 1:
                lines[-1] = lines[-1] + ","
        lines.append(f"{indent}}}")
        return lines

    if isinstance(value, list):
        if not value:
            return ["[]"]
        lines = ["["]
        for idx, item in enumerate(value):
            rendered = render_json(value=item, indent_level=indent_level + 1)
            if len(rendered) == 1:
                lines.append(f"{next_indent}{rendered[0]}")
            else:
                lines.append(f"{next_indent}{rendered[0]}")
                lines.extend([line for line in rendered[1:]])
            if idx < len(value) - 1:
                lines[-1] = lines[-1] + ","
        lines.append(f"{indent}]")
        return lines

    if isinstance(value, str):
        if "\n" in value:
            return render_multiline(value=value, indent=indent)
        return [json.dumps(value)]

    return [json.dumps(value)]


def format_list_lines(items: list[Any], *, parse_json: bool) -> list[str]:
    """Format list items as lines, parsing JSON when requested.

    Args:
        items: Items to render.
        parse_json: Whether to parse JSON strings into structured output.

    Returns:
        List of formatted lines.
    """
    lines: list[str] = []
    for item in items:
        if parse_json and isinstance(item, str):
            try:
                parsed = json.loads(item)
            except json.JSONDecodeError:
                parsed = item
            if isinstance(parsed, (dict, list)):
                lines.extend(render_json(value=parsed, indent_level=0))
            elif isinstance(parsed, str) and "\n" in parsed:
                lines.extend(render_multiline(value=parsed, indent=""))
            else:
                lines.append(json.dumps(parsed))
        elif isinstance(item, (dict, list)):
            lines.extend(render_json(value=item, indent_level=0))
        elif isinstance(item, str) and "\n" in item:
            lines.extend(render_multiline(value=item, indent=""))
        elif isinstance(item, str):
            lines.append(item)
        else:
            lines.append(json.dumps(item))
    return lines


def build_payload_view(payload: dict[str, Any]) -> dict[str, list[Any]]:
    """Build the filtered payload view for a response item.

    Args:
        payload: Payload dictionary from a response item.

    Returns:
        Mapping containing text, arguments, and output lists.

    Example:
        payload_view = build_payload_view(payload=payload)
    """
    payload_type = payload.get("type")
    if payload_type == "reasoning":
        text_source = reasoning_text_source(payload=payload)
        texts = collect_texts(value=text_source)
    else:
        texts = collect_texts(value=payload)

    return {
        "text": texts,
        "arguments": collect_arguments(value=payload),
        "output": collect_output(value=payload),
    }


def extract_response_items(lines: list[str]) -> list[dict[str, Any]]:
    """Extract response_item payloads from JSONL lines.

    Args:
        lines: JSONL file split into lines.

    Returns:
        List of response_item entries.
    """
    items: list[dict[str, Any]] = []
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if data.get("type") == "response_item":
            items.append(data)
    return items


def render_section(
    *,
    payload_view: dict[str, list[Any]],
    lines: list[str],
) -> None:
    """Append a formatted payload section to the output lines.

    Args:
        payload_view: Parsed payload view for the response item.
        lines: Output lines to append to.
    """
    if payload_view["text"]:
        lines.append("**text**")
        lines.append("```")
        lines.extend(
            format_list_lines(items=payload_view["text"], parse_json=False)
        )
        lines.append("```")
    if payload_view["arguments"]:
        lines.append("**arguments**")
        lines.append("```")
        lines.extend(
            format_list_lines(items=payload_view["arguments"], parse_json=True)
        )
        lines.append("```")
    if payload_view["output"]:
        lines.append("**output**")
        lines.append("```")
        lines.extend(
            format_list_lines(items=payload_view["output"], parse_json=False)
        )
        lines.append("```")


def build_trace_examples(*, session_files: list[Path]) -> list[str]:
    """Build the trace_examples.md content as a list of lines.

    Example:
        lines = build_trace_examples(session_files=session_files)
    """
    lines: list[str] = [
        "# Trace Examples (response_item text/arguments/output only)",
        "",
    ]

    for path in session_files:
        raw_lines = path.read_text().splitlines()
        response_items = extract_response_items(lines=raw_lines)
        sample_items = list(itertools.islice(response_items, 0, ENTRIES_PER_FILE))

        lines.append(f"## {path.name}")
        lines.append(f"_Source: {path}_")

        for idx, data in enumerate(sample_items, start=1):
            payload = data.get("payload")
            payload_type = payload.get("type") if isinstance(payload, dict) else None
            style = f"payload/{payload_type}" if payload_type else "payload/unknown"
            lines.append(f"### Entry {idx} ({style})")

            if not isinstance(payload, dict):
                payload_view = {"text": [], "arguments": [], "output": []}
            else:
                payload_view = build_payload_view(payload=payload)
                payload_view = truncate_lists(value=payload_view, limit=MAX_LIST_LEN)
                payload_view = truncate_strings(value=payload_view, limit=MAX_STR_LEN)

            render_section(payload_view=payload_view, lines=lines)

        lines.append("")

    return lines


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate trace_examples.md from Codex session JSONL files. Provide explicit "
            "files or let the script scan the sessions root."
        )
    )
    parser.add_argument(
        "session_files",
        nargs="*",
        type=Path,
        help="Session JSONL files to parse. If omitted, the sessions root is scanned.",
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=DEFAULT_SESSIONS_ROOT,
        help="Sessions root to scan when no explicit files are provided.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_SESSION_LIMIT,
        help="Number of most recent sessions to include when scanning.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output path for the generated markdown.",
    )
    return parser.parse_args()


def resolve_session_files(
    *, session_files: list[Path], sessions_root: Path, limit: int
) -> list[Path]:
    """Resolve the session files to process.

    Args:
        session_files: Explicit session files to parse.
        sessions_root: Root directory to scan when session_files is empty.
        limit: Number of most recent sessions to include from the scan.

    Returns:
        List of session file paths to process.

    Example:
        files = resolve_session_files(
            session_files=[],
            sessions_root=Path("~/.codex/sessions").expanduser(),
            limit=3,
        )
    """
    if session_files:
        for path in session_files:
            assert path.exists(), f"Session file not found: {path}"
        return session_files

    assert limit > 0, "Limit must be positive"
    assert sessions_root.exists(), f"Sessions root not found: {sessions_root}"
    discovered = discover_session_files(root=sessions_root)
    assert discovered, f"No session files found under {sessions_root}"
    return discovered[-limit:]


def main() -> None:
    """Generate the trace_examples.md file from session logs."""
    args = parse_args()
    session_files = resolve_session_files(
        session_files=args.session_files,
        sessions_root=args.sessions_root,
        limit=args.limit,
    )
    lines = build_trace_examples(session_files=session_files)
    args.output.write_text("\n".join(lines))


if __name__ == "__main__":
    main()

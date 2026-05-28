#!/usr/bin/env python3
import pickle
from typing import List, Optional, Sequence, Literal
from pathlib import Path
import networkx as nx
import typer
from pydantic_ai import format_as_xml
import json

# --- Load data (as provided) ---
METADATA_DIR = Path("/mnt/HC_Volume_103849439/metadata")
G = nx.read_gml(METADATA_DIR / "subjects_graph_da.gml")
TABLES_INFO_DIR = METADATA_DIR / "tables_info_raw_da"

ROOT_NAME = "DST"

app = typer.Typer(add_completion=False)

# --- Helpers ---


def _desc(node) -> str:
    return str(G.nodes[node].get("description", str(node)))


def _find_node(name: str):
    name_cf = name.casefold()
    # Prefer description match
    for n, d in G.nodes(data=True):
        if str(d.get("description", "")).casefold() == name_cf:
            return n
    # Then label match
    for n, d in G.nodes(data=True):
        if str(d.get("label", "")).casefold() == name_cf:
            return n
    # Finally, allow direct node id if present
    if name in G:
        return name
    raise KeyError(f"No node found for: {name}")


def _find_child(parent, name: str):
    successors = list(G.successors(parent))
    if not successors:
        raise KeyError(f"No child subjects under '{_desc(parent)}'")
    name_cf = name.casefold()
    # Prefer description match
    for child in successors:
        if str(G.nodes[child].get("description", "")).casefold() == name_cf:
            return child
    # Then label match
    for child in successors:
        if str(G.nodes[child].get("label", "")).casefold() == name_cf:
            return child
    # Finally, allow matching on node identifier
    for child in successors:
        if str(child).casefold() == name_cf:
            return child
    raise KeyError(f"No child named '{name}' under '{_desc(parent)}'")


def _resolve_subject(path: str):
    parts = [p.strip() for p in (path or "").split("/") if p.strip()]
    if not parts:
        node = _find_node(ROOT_NAME)
        return node, [node]
    current = _find_node(parts[0])
    lineage = [current]
    for part in parts[1:]:
        current = _find_child(current, part)
        lineage.append(current)
    return current, lineage


def _tables_for(node) -> List[str]:
    v = G.nodes[node].get("tables")
    if isinstance(v, (list, tuple)):
        vals = [str(x) for x in v if str(x).strip() and str(x).strip() != "[]"]
    elif isinstance(v, str):
        s = v.strip()
        vals = [] if not s or s == "[]" else [s]
    else:
        vals = []
    return vals


def _render_tables(node, indent: int) -> List[str]:
    tables = sorted(_tables_for(node))
    indent_str = "  " * indent
    lines = []
    for table_id in tables:
        descr = get_table_description(table_id)
        line = f"{indent_str}- {table_id}: {descr}".rstrip()
        lines.append(line)
    return lines


def _render_subject(
    node, depth: int, indent: int, visited: Optional[Sequence] = None
) -> List[str]:
    visited_set = set(visited or [])
    if node in visited_set:
        indent_str = "  " * indent
        return [f"{indent_str}- (cycle to {_desc(node)})"]
    visited_set.add(node)

    if depth == 0:
        # Depth exhausted; only show tables if present.
        return _render_tables(node, indent)

    children = sorted(G.successors(node), key=_desc)
    if children:
        lines: List[str] = []
        for child in children:
            indent_str = "  " * indent
            lines.append(f"{indent_str}- {_desc(child)}")
            next_depth = depth if depth < 0 else depth - 1
            if depth != 1:
                if child in visited_set:
                    lines.append(f"{'  ' * (indent + 1)}- (cycle to {_desc(child)})")
                else:
                    lines.extend(
                        _render_subject(
                            child,
                            next_depth,
                            indent + 1,
                            visited_set,
                        )
                    )
        return lines

    return _render_tables(node, indent)


def get_table_description(table_id: str) -> str:
    fp = TABLES_INFO_DIR / f"{table_id}.pkl"
    if not fp.exists():
        return ""

    with open(fp, "rb") as f:
        table_info = pickle.load(f)
    return table_info.get("description", "")


def _breadcrumb_for(node, lineage: Sequence):
    if lineage and lineage[0] == _find_node(ROOT_NAME):
        return lineage
    try:
        return nx.shortest_path(G, source=_find_node(ROOT_NAME), target=node)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return lineage


def browse_subject(subject: str, depth: int = 1, show_parents: bool = False) -> str:
    node, lineage = _resolve_subject(subject)
    lines: List[str] = []

    if show_parents:
        breadcrumb = _breadcrumb_for(node, lineage)
        if breadcrumb:
            breadcrumb_line = " / ".join(_desc(n) for n in breadcrumb)
            lines.append(breadcrumb_line)
            lines.append("")

    lines.extend(_render_subject(node, depth, indent=0))
    return "\n".join(lines).rstrip()


# --- Browse a subject (optional arg; defaults to DST) ---
@app.callback(invoke_without_command=True)
def browse(
    subject: Optional[str] = typer.Argument(
        None, help="Subject description/label, node id, or slash path"
    ),
    depth: int = typer.Option(
        1, help="Depth of child subjects to display (use -1 for full depth)"
    ),
    parents: bool = typer.Option(
        False, "--parents/--no-parents", help="Show breadcrumb of parent subjects"
    ),
):
    typer.echo(browse_subject(subject or ROOT_NAME, depth=depth, show_parents=parents))


if __name__ == "__main__":
    app()

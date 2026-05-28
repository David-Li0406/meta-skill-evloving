"""
Marimo notebook handler for the viz skill.

This module contains all marimo-specific functionality:
- Dataclasses for notebook structure (MarimoCell, ParsedNotebook, etc.)
- Notebook parsing (AST-based extraction of cells, functions, classes)
- Dependency resolution (determining which cells are needed)
- Notebook assembly (building pruned notebooks with injected code)
- Import deduplication (preventing multiple-definitions errors)
"""

import argparse
import ast
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


# ============================================================================
# Marimo Notebook Data Structures
# ============================================================================


@dataclass
class MarimoCell:
    """Represents a single cell in a marimo notebook."""

    name: str  # Function name (e.g., "_" or "my_cell")
    refs: list[str]  # Variables this cell reads (from function params)
    defs: list[str]  # Variables this cell defines (from return tuple)
    code: str  # Full cell code including decorator and function def
    start_line: int  # Line number where cell starts (1-indexed)
    end_line: int  # Line number where cell ends (1-indexed)


@dataclass
class MarimoFunction:
    """Represents an @app.function decorated function."""

    name: str
    code: str
    start_line: int
    end_line: int


@dataclass
class MarimoClass:
    """Represents a class definition in the notebook."""

    name: str
    code: str
    start_line: int
    end_line: int


@dataclass
class ParsedNotebook:
    """Parsed structure of a marimo notebook."""

    preamble: str  # Everything before app.setup (imports marimo, app = ...)
    setup_code: str  # Content of app.setup block
    functions: list[MarimoFunction] = field(default_factory=list)
    classes: list[MarimoClass] = field(default_factory=list)
    cells: list[MarimoCell] = field(default_factory=list)
    main_block: str = ""  # The if __name__ == "__main__" block


@dataclass
class PreparedNotebook:
    """Result of parsing and preparing a marimo notebook for execution."""

    parsed: ParsedNotebook
    required_indices: list[int]
    required_functions: set[str]
    target_var: str | None
    cwd: Path


# ============================================================================
# Notebook Parsing
# ============================================================================


def parse_marimo_notebook(notebook_path: Path) -> ParsedNotebook:
    """
    Parse a marimo notebook using AST and extract cell structure.

    Extracts:
    - Preamble (import marimo, app = marimo.App(...))
    - Setup block (with app.setup:)
    - @app.function definitions
    - Class definitions
    - @app.cell definitions with refs/defs
    - Main block
    """
    with open(notebook_path) as f:
        source = f.read()
        source_lines = source.splitlines(keepends=True)

    tree = ast.parse(source)

    result = ParsedNotebook(preamble="", setup_code="")

    # Track positions
    setup_start = None
    setup_end = None
    main_start = None

    for node in ast.iter_child_nodes(tree):
        # Find import marimo and app = marimo.App(...)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Part of preamble
            pass

        # Find with app.setup: block
        elif isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if (
                    isinstance(ctx, ast.Attribute)
                    and isinstance(ctx.value, ast.Name)
                    and ctx.value.id == "app"
                    and ctx.attr == "setup"
                ):
                    setup_start = node.lineno
                    setup_end = node.end_lineno
                    # Extract the body of the with block
                    body_start = node.body[0].lineno if node.body else setup_start + 1
                    body_end = setup_end
                    setup_lines = source_lines[body_start - 1 : body_end]
                    result.setup_code = "".join(setup_lines)

        # Find @app.cell and @app.function decorated functions
        elif isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Attribute):
                    if (
                        isinstance(decorator.value, ast.Name)
                        and decorator.value.id == "app"
                    ):
                        if decorator.attr == "cell":
                            cell = _parse_cell(node, source_lines)
                            result.cells.append(cell)
                        elif decorator.attr == "function":
                            func = _parse_function(node, source_lines)
                            result.functions.append(func)

        # Find class definitions
        elif isinstance(node, ast.ClassDef):
            cls = _parse_class(node, source_lines)
            result.classes.append(cls)

        # Find if __name__ == "__main__":
        elif isinstance(node, ast.If):
            if _is_main_block(node):
                main_start = node.lineno
                result.main_block = "".join(source_lines[main_start - 1 :])

    # Extract preamble (everything before setup or first cell)
    if setup_start:
        result.preamble = "".join(source_lines[: setup_start - 1])
    elif result.cells:
        first_cell_line = result.cells[0].start_line
        result.preamble = "".join(source_lines[: first_cell_line - 1])

    return result


def _extract_node_source(
    node: ast.FunctionDef | ast.ClassDef, source_lines: list[str]
) -> tuple[str, int, int]:
    """
    Extract source code for an AST node, accounting for decorators.

    Returns: (code, start_line, end_line)
    """
    start_line = node.lineno
    if hasattr(node, "decorator_list"):
        for decorator in node.decorator_list:
            start_line = min(start_line, decorator.lineno)
    end_line = node.end_lineno or node.lineno
    code = "".join(source_lines[start_line - 1 : end_line])
    return code, start_line, end_line


def _parse_cell(node: ast.FunctionDef, source_lines: list[str]) -> MarimoCell:
    """Parse an @app.cell decorated function into a MarimoCell."""
    # Get refs from function parameters
    refs = [arg.arg for arg in node.args.args if arg.arg != "_"]

    # Get defs from return statement
    defs = []
    for stmt in ast.walk(node):
        if isinstance(stmt, ast.Return) and stmt.value:
            if isinstance(stmt.value, ast.Tuple):
                for elt in stmt.value.elts:
                    if isinstance(elt, ast.Name):
                        defs.append(elt.id)

    code, start_line, end_line = _extract_node_source(node, source_lines)

    return MarimoCell(
        name=node.name,
        refs=refs,
        defs=defs,
        code=code,
        start_line=start_line,
        end_line=end_line,
    )


def _parse_function(node: ast.FunctionDef, source_lines: list[str]) -> MarimoFunction:
    """Parse an @app.function decorated function."""
    code, start_line, end_line = _extract_node_source(node, source_lines)
    return MarimoFunction(
        name=node.name, code=code, start_line=start_line, end_line=end_line
    )


def _parse_class(node: ast.ClassDef, source_lines: list[str]) -> MarimoClass:
    """Parse a class definition."""
    code, start_line, end_line = _extract_node_source(node, source_lines)
    return MarimoClass(
        name=node.name, code=code, start_line=start_line, end_line=end_line
    )


def _is_main_block(node: ast.If) -> bool:
    """Check if this is an if __name__ == '__main__': block."""
    test = node.test
    if isinstance(test, ast.Compare):
        if (
            isinstance(test.left, ast.Name)
            and test.left.id == "__name__"
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
            and len(test.comparators) == 1
            and isinstance(test.comparators[0], ast.Constant)
            and test.comparators[0].value == "__main__"
        ):
            return True
    return False


# ============================================================================
# Dependency Resolution
# ============================================================================


def prepare_notebook(
    notebook_path: Path,
    target_vars: list[str],
) -> PreparedNotebook | tuple[bool, str]:
    """
    Parse notebook and resolve dependencies.

    Returns PreparedNotebook on success, or (False, error_message) on failure.
    """
    parsed = parse_marimo_notebook(notebook_path)
    required_indices, required_functions = get_required_cells(parsed, target_vars)

    if not required_indices:
        return (False, f"Could not find cells defining: {target_vars}")

    return PreparedNotebook(
        parsed=parsed,
        required_indices=required_indices,
        required_functions=required_functions,
        target_var=target_vars[0] if target_vars else None,
        cwd=notebook_path.parent,
    )


def get_required_cells(
    parsed: ParsedNotebook, target_vars: list[str]
) -> tuple[list[int], set[str]]:
    """
    Given target variables, return indices of all cells needed.

    Works backwards from targets through the dependency graph.
    Also returns the set of @app.function names that are needed.

    Returns:
        (cell_indices, function_names): List of cell indices and set of function names
    """
    # Build a map of variable -> cell index that defines it
    var_to_cell: dict[str, int] = {}
    for i, cell in enumerate(parsed.cells):
        for var in cell.defs:
            var_to_cell[var] = i

    # Build set of all function names
    function_names = {f.name for f in parsed.functions}

    # Traverse backwards from target vars
    required_indices: set[int] = set()
    required_functions: set[str] = set()
    queue = list(target_vars)
    visited_vars: set[str] = set()

    while queue:
        var = queue.pop()
        if var in visited_vars:
            continue
        visited_vars.add(var)

        # Check if this var is defined by a cell
        if var in var_to_cell:
            cell_idx = var_to_cell[var]
            required_indices.add(cell_idx)
            # Add this cell's refs to the queue
            cell = parsed.cells[cell_idx]
            for ref in cell.refs:
                if ref not in visited_vars:
                    queue.append(ref)

        # Check if this var is an @app.function
        if var in function_names:
            required_functions.add(var)

    # Also check each required cell's code for function calls
    for idx in list(required_indices):
        cell = parsed.cells[idx]
        for func_name in function_names:
            if func_name in cell.code:
                required_functions.add(func_name)

    return sorted(required_indices), required_functions


# ============================================================================
# Import Deduplication (prevents multiple-definitions errors)
# ============================================================================


def extract_setup_imports(setup_code: str) -> dict[str, str]:
    """
    Extract import statements from the setup block.

    Returns a dict mapping imported names to their import statements.
    E.g., {"np": "import numpy as np", "pd": "import pandas as pd"}
    """
    imports = {}

    # Dedent the code first to handle indented setup blocks
    dedented = textwrap.dedent(setup_code)

    try:
        tree = ast.parse(dedented)
    except SyntaxError:
        # Fall back to regex if AST parsing fails
        return _extract_imports_regex(setup_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name
                imports[name] = f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else "")

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                name = alias.asname or alias.name
                imports[name] = f"from {module} import {alias.name}" + (f" as {alias.asname}" if alias.asname else "")

    return imports


def _extract_imports_regex(code: str) -> dict[str, str]:
    """Fallback regex-based import extraction."""
    imports = {}

    # Match: import X as Y, import X
    import_pattern = re.compile(r'^import\s+(\w+)(?:\s+as\s+(\w+))?', re.MULTILINE)
    for match in import_pattern.finditer(code):
        module = match.group(1)
        alias = match.group(2) or module
        imports[alias] = match.group(0)

    # Match: from X import Y as Z, from X import Y
    from_pattern = re.compile(r'^from\s+[\w.]+\s+import\s+(\w+)(?:\s+as\s+(\w+))?', re.MULTILINE)
    for match in from_pattern.finditer(code):
        name = match.group(1)
        alias = match.group(2) or name
        imports[alias] = match.group(0)

    return imports


def strip_imports_from_action_code(action_code: str, setup_imports: dict[str, str]) -> str:
    """
    Remove import statements from action code that are already in setup block.

    This prevents marimo's multiple-definitions error when injecting plotting
    code that imports modules already imported in app.setup.

    Args:
        action_code: The plotting/action code to inject
        setup_imports: Dict of {name: import_statement} from setup block

    Returns:
        Action code with duplicate imports removed
    """
    lines = action_code.splitlines(keepends=True)
    result_lines = []

    for line in lines:
        stripped = line.strip()

        # Check if this is an import line
        if stripped.startswith('import ') or stripped.startswith('from '):
            imported_names = _extract_imported_names_from_line(stripped)

            # Check if ALL names in this import are already in setup
            all_in_setup = all(name in setup_imports for name in imported_names)

            if all_in_setup and imported_names:
                # Skip this import line - it's already in setup
                continue

        result_lines.append(line)

    return ''.join(result_lines)


def _extract_imported_names_from_line(import_line: str) -> list[str]:
    """
    Extract the names that would be bound by an import statement.

    Examples:
        'import numpy as np' -> ['np']
        'import numpy' -> ['numpy']
        'from os import path' -> ['path']
        'from typing import List, Dict' -> ['List', 'Dict']
    """
    import_line = import_line.strip()

    # Handle: import X as Y
    match = re.match(r'^import\s+(\w+)(?:\s+as\s+(\w+))?$', import_line)
    if match:
        return [match.group(2) or match.group(1)]

    # Handle: from X import Y, Z, ...
    match = re.match(r'^from\s+[\w.]+\s+import\s+(.+)$', import_line)
    if match:
        names = []
        for part in match.group(1).split(','):
            part = part.strip()
            alias_match = re.match(r'(\w+)(?:\s+as\s+(\w+))?', part)
            if alias_match:
                names.append(alias_match.group(2) or alias_match.group(1))
        return names

    return []


# ============================================================================
# Snapshot Injection (for capturing intermediate state)
# ============================================================================


def inject_snapshot(
    cell_code: str, target_var: str, target_line: int, cell_start_line: int
) -> str:
    """
    Inject a snapshot variable to capture intermediate state.

    If target_line points to a specific line within the cell, we insert
    a snapshot assignment after that line to capture the variable's state.

    Args:
        cell_code: The full cell code
        target_var: The variable to snapshot
        target_line: The line number to snapshot after (1-indexed, file-relative)
        cell_start_line: The line number where this cell starts in the file

    Returns:
        Modified cell code with snapshot injection
    """
    lines = cell_code.splitlines(keepends=True)
    # Convert file-relative line to cell-relative (0-indexed)
    relative_line = target_line - cell_start_line

    if relative_line < 0 or relative_line >= len(lines):
        # Line not in this cell, return unchanged
        return cell_code

    # Detect if target line is part of a method chain
    # Look for pattern like df = ( ... .pipe(x) ... )
    target_content = lines[relative_line] if relative_line < len(lines) else ""

    # Check if this is a .pipe() call or similar method chain
    if ".pipe(" in target_content or re.search(r"\.\w+\(", target_content):
        # Try to break the method chain
        return _break_method_chain(lines, relative_line, target_var)

    # Simple case: insert snapshot after target line
    # Determine indentation from the target line
    indent_match = re.match(r"^(\s*)", lines[relative_line])
    indent = indent_match.group(1) if indent_match else "    "

    snapshot_line = f"{indent}_viz_snapshot_{target_var} = {target_var}.copy() if hasattr({target_var}, 'copy') else {target_var}\n"

    # Insert after the target line
    insert_pos = relative_line + 1
    lines.insert(insert_pos, snapshot_line)

    return "".join(lines)


def _break_method_chain(
    lines: list[str], target_line_idx: int, target_var: str
) -> str:
    """
    Break a method chain at the target line and inject a snapshot.

    For a chain like:
        df = (
            df_.copy()
            .pipe(add_channel)
            .pipe(add_channel_type)  <- target
            .pipe(select_columns)
        )

    Produces:
        df = df_.copy()
        df = df.pipe(add_channel)
        df = df.pipe(add_channel_type)
        _viz_snapshot_df = df.copy()
        df = df.pipe(select_columns)
    """
    # This is a complex transformation - for now, just insert a comment
    # indicating the snapshot point. A full implementation would need to
    # parse the AST more carefully.

    # Find the assignment line (df = ...)
    chain_start = None
    for i in range(target_line_idx, -1, -1):
        if "=" in lines[i] and "==" not in lines[i]:
            chain_start = i
            break

    if chain_start is None:
        return "".join(lines)

    # For now, add a snapshot after the full chain completes with a note
    # A more sophisticated version could actually break the chain
    indent_match = re.match(r"^(\s*)", lines[target_line_idx])
    indent = indent_match.group(1) if indent_match else "    "

    # Find the end of the method chain (closing paren and return)
    chain_end = target_line_idx
    paren_depth = 0
    for i in range(chain_start, len(lines)):
        paren_depth += lines[i].count("(") - lines[i].count(")")
        if paren_depth <= 0 and (lines[i].strip().endswith(")") or "return" in lines[i]):
            chain_end = i
            break

    # Insert snapshot right before return statement if present
    for i in range(chain_end, len(lines)):
        if "return" in lines[i]:
            snapshot_line = f"{indent}_viz_snapshot_{target_var} = {target_var}.copy() if hasattr({target_var}, 'copy') else {target_var}\n"
            lines.insert(i, snapshot_line)
            break

    return "".join(lines)


# ============================================================================
# Notebook Assembly
# ============================================================================


def assemble_pruned_notebook(
    parsed: ParsedNotebook,
    required_indices: list[int],
    required_functions: set[str],
    plot_code: str,
    target_var: str | None = None,
    target_line: int | None = None,
) -> str:
    """
    Assemble a pruned notebook with only required cells + plot code.

    Args:
        parsed: The parsed notebook structure
        required_indices: Indices of cells to include
        required_functions: Names of @app.functions to include
        plot_code: The plotting code to inject as a new cell
        target_var: If set, the variable to potentially snapshot
        target_line: If set with target_var, inject snapshot at this line

    Returns:
        Complete Python script ready to execute
    """
    parts = []

    # Strip duplicate imports from plot_code to prevent multiple-definitions errors
    # This is done BEFORE injection to avoid marimo check failures
    if parsed.setup_code:
        setup_imports = extract_setup_imports(parsed.setup_code)
        plot_code = strip_imports_from_action_code(plot_code, setup_imports)

    # 1. Preamble
    parts.append(parsed.preamble)

    # 2. Setup block
    if parsed.setup_code:
        parts.append("\nwith app.setup:\n")
        # Indent the setup code properly
        setup_lines = parsed.setup_code.splitlines(keepends=True)
        for line in setup_lines:
            if line.strip():  # Non-empty line
                # Check if already indented
                if not line.startswith("    "):
                    parts.append("    " + line)
                else:
                    parts.append(line)
            else:
                parts.append(line)
        parts.append("\n")

    # 3. Classes (all classes are included as they might be needed)
    for cls in parsed.classes:
        parts.append("\n" + cls.code + "\n")

    # 4. Required @app.functions
    for func in parsed.functions:
        if func.name in required_functions:
            parts.append("\n" + func.code + "\n")

    # 5. Required cells
    for idx in required_indices:
        cell = parsed.cells[idx]
        cell_code = cell.code

        # Inject snapshot if needed
        if target_var and target_line and target_var in cell.defs:
            if cell.start_line <= target_line <= cell.end_line:
                cell_code = inject_snapshot(
                    cell_code, target_var, target_line, cell.start_line
                )

        parts.append("\n" + cell_code + "\n")

    # 6. Plotting cell
    # Wrap plot_code in an @app.cell
    # Determine what variables the plot code needs - use target_var
    if target_var and target_line:
        refs = f"_viz_snapshot_{target_var}"
    elif target_var:
        refs = target_var
    else:
        refs = "_"

    plot_cell = f'''
@app.cell
def _({refs}):
    # Viz skill injected plotting code
{_indent_code(plot_code, "    ")}
    return
'''
    parts.append(plot_cell)

    # 7. Main block
    if parsed.main_block:
        parts.append("\n" + parsed.main_block)
    else:
        parts.append('\nif __name__ == "__main__":\n    app.run()\n')

    return "".join(parts)


def _indent_code(code: str, indent: str) -> str:
    """Add indentation to each line of code."""
    lines = code.splitlines(keepends=True)
    indented = []
    for line in lines:
        if line.strip():
            indented.append(indent + line)
        else:
            indented.append(line)
    return "".join(indented)


# ============================================================================
# Handler Class
# ============================================================================


class MarimoHandler:
    """Handler for marimo notebooks - parses and assembles pruned scripts."""

    def build_script(
        self,
        action_code: str,
        source_path: Path | None = None,
        target_var: str | None = None,
        target_line: int | None = None,
        **kwargs,
    ) -> tuple[str, Path | None]:
        """
        Build a script by parsing marimo notebook and resolving dependencies.

        Args:
            action_code: Code to execute (plotting, showing, etc.)
            source_path: Path to the marimo notebook
            target_var: Variable to extract from the notebook
            target_line: Optional line number for intermediate state capture

        Returns:
            (script_content, working_directory)

        Raises:
            ValueError: If notebook parsing fails or target variable not found
        """
        if source_path is None:
            raise ValueError("MarimoHandler requires source_path (notebook path)")
        if target_var is None:
            raise ValueError("MarimoHandler requires target_var")

        prep = prepare_notebook(source_path, [target_var])
        if isinstance(prep, tuple):
            raise ValueError(prep[1])

        script = assemble_pruned_notebook(
            prep.parsed,
            prep.required_indices,
            prep.required_functions,
            action_code,
            target_var=prep.target_var,
            target_line=target_line,
        )
        return script, prep.cwd

    def validate_args(self, args: argparse.Namespace) -> tuple[bool, str]:
        """Validate marimo-specific arguments."""
        if not getattr(args, "notebook_path", None):
            return False, "--marimo requires --notebook path"
        if not getattr(args, "target_var", None):
            return False, "--marimo requires --target-var"
        if not Path(args.notebook_path).exists():
            return False, f"Notebook not found: {args.notebook_path}"
        return True, ""

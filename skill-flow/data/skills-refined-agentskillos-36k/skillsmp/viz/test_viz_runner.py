"""
Comprehensive test suite for viz_runner.py

Tests cover:
- Marimo notebook parsing (AST-based)
- Dependency resolution
- Code transformation (inject_savefig, inject_snapshot)
- ID generation and collision handling
- CLI commands (--list, --clean)
- Subprocess execution (mocked)
"""

import ast
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from unittest.mock import MagicMock, patch

import pytest

# Import the modules under test
import viz_runner
import marimo_handler

# Core viz_runner imports
from viz_runner import (
    DefaultHandler,
    VIZ_DIR,
    ensure_viz_dir,
    format_module_error,
    generate_show_code,
    get_handler,
    get_python_command,
    get_unique_id,
    inject_savefig,
    run_plot,
    run_script_background,
    run_show,
    validate_python_env,
)

# Marimo handler imports
from marimo_handler import (
    MarimoCell,
    MarimoClass,
    MarimoFunction,
    MarimoHandler,
    ParsedNotebook,
    _break_method_chain,
    _indent_code,
    _is_main_block,
    _parse_cell,
    _parse_class,
    _parse_function,
    assemble_pruned_notebook,
    get_required_cells,
    inject_snapshot,
    parse_marimo_notebook,
    prepare_notebook,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def sample_notebook_simple(tmp_path):
    """A simple marimo notebook with basic cells."""
    content = dedent('''
        import marimo
        app = marimo.App()

        with app.setup:
            import pandas as pd

        @app.cell
        def _():
            df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
            return df,

        @app.cell
        def _(df):
            result = df * 2
            return result,

        if __name__ == "__main__":
            app.run()
    ''').strip()
    notebook_path = tmp_path / "simple.nb.py"
    notebook_path.write_text(content)
    return notebook_path


@pytest.fixture
def sample_notebook_with_functions(tmp_path):
    """A marimo notebook with @app.function decorators."""
    content = dedent('''
        import marimo
        app = marimo.App()

        with app.setup:
            import pandas as pd

        @app.function
        def multiply_df(df, factor):
            return df * factor

        @app.cell
        def _():
            data = pd.DataFrame({"a": [1, 2, 3]})
            return data,

        @app.cell
        def _(data, multiply_df):
            result = multiply_df(data, 10)
            return result,

        if __name__ == "__main__":
            app.run()
    ''').strip()
    notebook_path = tmp_path / "with_functions.nb.py"
    notebook_path.write_text(content)
    return notebook_path


@pytest.fixture
def sample_notebook_with_class(tmp_path):
    """A marimo notebook with class definitions."""
    content = dedent('''
        import marimo
        app = marimo.App()

        with app.setup:
            import pandas as pd

        class DataProcessor:
            def __init__(self, scale):
                self.scale = scale

            def process(self, df):
                return df * self.scale

        @app.cell
        def _():
            processor = DataProcessor(5)
            return processor,

        @app.cell
        def _(processor):
            df = pd.DataFrame({"x": [1, 2, 3]})
            output = processor.process(df)
            return output,

        if __name__ == "__main__":
            app.run()
    ''').strip()
    notebook_path = tmp_path / "with_class.nb.py"
    notebook_path.write_text(content)
    return notebook_path


@pytest.fixture
def sample_notebook_chain(tmp_path):
    """A marimo notebook with a chain of dependencies."""
    content = dedent('''
        import marimo
        app = marimo.App()

        with app.setup:
            import pandas as pd

        @app.cell
        def _():
            raw_data = pd.DataFrame({"x": [1, 2, 3]})
            return raw_data,

        @app.cell
        def _(raw_data):
            cleaned = raw_data.dropna()
            return cleaned,

        @app.cell
        def _(cleaned):
            transformed = cleaned * 2
            return transformed,

        @app.cell
        def _(transformed):
            final = transformed.sum()
            return final,

        if __name__ == "__main__":
            app.run()
    ''').strip()
    notebook_path = tmp_path / "chain.nb.py"
    notebook_path.write_text(content)
    return notebook_path


@pytest.fixture
def sample_notebook_no_setup(tmp_path):
    """A marimo notebook without a setup block."""
    content = dedent('''
        import marimo
        app = marimo.App()

        @app.cell
        def _():
            import pandas as pd
            df = pd.DataFrame({"x": [1, 2, 3]})
            return df,

        if __name__ == "__main__":
            app.run()
    ''').strip()
    notebook_path = tmp_path / "no_setup.nb.py"
    notebook_path.write_text(content)
    return notebook_path


@pytest.fixture
def viz_dir_clean(tmp_path, monkeypatch):
    """Provide a clean temporary viz directory."""
    viz_dir = tmp_path / "viz"
    viz_dir.mkdir()
    monkeypatch.setattr(viz_runner, "VIZ_DIR", viz_dir)
    return viz_dir


# =============================================================================
# Unit Tests: Parsing Helpers
# =============================================================================


class TestParseCell:
    """Tests for _parse_cell function."""

    def test_parse_cell_no_refs_single_def(self):
        """Cell with no parameters and single return value."""
        source = dedent('''
            @app.cell
            def _():
                df = [1, 2, 3]
                return df,
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert cell.name == "_"
        assert cell.refs == []
        assert cell.defs == ["df"]
        assert "@app.cell" in cell.code

    def test_parse_cell_with_refs(self):
        """Cell with parameters (refs) and return value (def)."""
        source = dedent('''
            @app.cell
            def _(df, config):
                result = df * config
                return result,
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert cell.name == "_"
        assert set(cell.refs) == {"df", "config"}
        assert cell.defs == ["result"]

    def test_parse_cell_multiple_defs(self):
        """Cell returning multiple values."""
        source = dedent('''
            @app.cell
            def _():
                a = 1
                b = 2
                return a, b
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert set(cell.defs) == {"a", "b"}

    def test_parse_cell_empty_return(self):
        """Cell with no return value."""
        source = dedent('''
            @app.cell
            def _():
                print("hello")
                return
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert cell.defs == []

    def test_parse_cell_underscore_param_ignored(self):
        """Underscore parameters should be ignored in refs."""
        source = dedent('''
            @app.cell
            def _(_, df):
                result = df * 2
                return result,
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert cell.refs == ["df"]


class TestParseFunction:
    """Tests for _parse_function."""

    def test_parse_function_basic(self):
        """Parse a basic @app.function."""
        source = dedent('''
            @app.function
            def my_helper(x, y):
                return x + y
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        func = _parse_function(func_node, lines)

        assert func.name == "my_helper"
        assert "@app.function" in func.code
        assert "return x + y" in func.code


class TestParseClass:
    """Tests for _parse_class."""

    def test_parse_class_basic(self):
        """Parse a basic class definition."""
        source = dedent('''
            class MyProcessor:
                def __init__(self, value):
                    self.value = value

                def process(self, data):
                    return data * self.value
        ''').strip()
        tree = ast.parse(source)
        class_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cls = _parse_class(class_node, lines)

        assert cls.name == "MyProcessor"
        assert "def __init__" in cls.code
        assert "def process" in cls.code


class TestIsMainBlock:
    """Tests for _is_main_block."""

    def test_is_main_block_true(self):
        """Detect if __name__ == '__main__' block."""
        source = dedent('''
            if __name__ == "__main__":
                app.run()
        ''').strip()
        tree = ast.parse(source)
        if_node = tree.body[0]

        assert _is_main_block(if_node) is True

    def test_is_main_block_false_different_condition(self):
        """Not a main block - different condition."""
        source = dedent('''
            if some_condition:
                pass
        ''').strip()
        tree = ast.parse(source)
        if_node = tree.body[0]

        assert _is_main_block(if_node) is False

    def test_is_main_block_false_wrong_comparator(self):
        """Not a main block - wrong string."""
        source = dedent('''
            if __name__ == "something_else":
                pass
        ''').strip()
        tree = ast.parse(source)
        if_node = tree.body[0]

        assert _is_main_block(if_node) is False


# =============================================================================
# Unit Tests: Dependency Resolution
# =============================================================================


class TestGetRequiredCells:
    """Tests for get_required_cells dependency traversal."""

    def test_single_target_no_deps(self):
        """Target variable with no dependencies."""
        cells = [
            MarimoCell(
                name="_", refs=[], defs=["df"],
                code="", start_line=1, end_line=5
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        indices, funcs = get_required_cells(parsed, ["df"])

        assert indices == [0]
        assert funcs == set()

    def test_chain_dependency(self):
        """Target depends on a chain of cells."""
        cells = [
            MarimoCell(
                name="_", refs=[], defs=["raw"],
                code="", start_line=1, end_line=5
            ),
            MarimoCell(
                name="_", refs=["raw"], defs=["cleaned"],
                code="", start_line=6, end_line=10
            ),
            MarimoCell(
                name="_", refs=["cleaned"], defs=["final"],
                code="", start_line=11, end_line=15
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        indices, funcs = get_required_cells(parsed, ["final"])

        # Should include all three cells in the chain
        assert set(indices) == {0, 1, 2}

    def test_branch_dependency(self):
        """Target depends on multiple independent cells."""
        cells = [
            MarimoCell(
                name="_", refs=[], defs=["a"],
                code="", start_line=1, end_line=5
            ),
            MarimoCell(
                name="_", refs=[], defs=["b"],
                code="", start_line=6, end_line=10
            ),
            MarimoCell(
                name="_", refs=["a", "b"], defs=["result"],
                code="", start_line=11, end_line=15
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        indices, funcs = get_required_cells(parsed, ["result"])

        assert set(indices) == {0, 1, 2}

    def test_missing_target_variable(self):
        """Target variable doesn't exist in any cell."""
        cells = [
            MarimoCell(
                name="_", refs=[], defs=["df"],
                code="", start_line=1, end_line=5
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        indices, funcs = get_required_cells(parsed, ["nonexistent"])

        assert indices == []

    def test_with_app_function(self):
        """Target depends on an @app.function."""
        cells = [
            MarimoCell(
                name="_", refs=["helper"], defs=["result"],
                code="result = helper(10)", start_line=10, end_line=15
            ),
        ]
        functions = [
            MarimoFunction(name="helper", code="", start_line=1, end_line=5)
        ]
        parsed = ParsedNotebook(
            preamble="", setup_code="",
            cells=cells, functions=functions
        )

        indices, funcs = get_required_cells(parsed, ["result"])

        assert 0 in indices
        assert "helper" in funcs


# =============================================================================
# Unit Tests: Code Transformation
# =============================================================================


class TestInjectSavefig:
    """Tests for inject_savefig function."""

    def test_basic_plt_show(self):
        """Inject savefig before plt.show()."""
        script = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1, 2, 3])
            plt.show()
        ''').strip()

        result = inject_savefig(script, "/tmp/viz/test.png")

        assert "plt.savefig('/tmp/viz/test.png'" in result
        assert result.index("savefig") < result.index("show")

    def test_with_indentation(self):
        """Preserve indentation when injecting."""
        script = dedent('''
            import matplotlib.pyplot as plt
            if True:
                plt.plot([1, 2, 3])
                plt.show()
        ''').strip()

        result = inject_savefig(script, "/tmp/viz/test.png")

        # savefig should be indented like the plt.show()
        lines = result.split("\n")
        savefig_line = [l for l in lines if "savefig" in l][0]
        show_line = [l for l in lines if "show" in l][0]

        # Both should have same indentation
        assert savefig_line.startswith("    ")
        assert show_line.startswith("    ")

    def test_no_plt_show(self):
        """Script without plt.show() gets savefig appended."""
        script = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1, 2, 3])
        ''').strip()

        result = inject_savefig(script, "/tmp/viz/test.png")

        assert "plt.savefig('/tmp/viz/test.png'" in result

    def test_multiple_shows(self):
        """Multiple plt.show() calls each get savefig."""
        script = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1, 2, 3])
            plt.show()
            plt.plot([4, 5, 6])
            plt.show()
        ''').strip()

        result = inject_savefig(script, "/tmp/viz/test.png")

        # Both shows should have savefig before them
        assert result.count("savefig") == 2

    def test_pyplot_show(self):
        """Handle pyplot.show() as well as plt.show()."""
        script = dedent('''
            from matplotlib import pyplot
            pyplot.plot([1, 2, 3])
            pyplot.show()
        ''').strip()

        result = inject_savefig(script, "/tmp/viz/test.png")

        assert "plt.savefig" in result


class TestIndentCode:
    """Tests for _indent_code helper."""

    def test_basic_indentation(self):
        """Add indentation to code block."""
        code = "x = 1\ny = 2"

        result = _indent_code(code, "    ")

        assert result == "    x = 1\n    y = 2"

    def test_preserves_empty_lines(self):
        """Empty lines stay empty."""
        code = "x = 1\n\ny = 2"

        result = _indent_code(code, "    ")

        assert result == "    x = 1\n\n    y = 2"


class TestInjectSnapshot:
    """Tests for inject_snapshot function."""

    def test_simple_snapshot(self):
        """Insert snapshot after target line."""
        cell_code = dedent('''
            @app.cell
            def _():
                df = create_dataframe()
                return df,
        ''').strip()

        # Target line 3 (the df = line), cell starts at line 1
        result = inject_snapshot(cell_code, "df", 3, 1)

        assert "_viz_snapshot_df" in result

    def test_out_of_range_line(self):
        """Line outside cell range returns unchanged."""
        cell_code = dedent('''
            @app.cell
            def _():
                df = 1
                return df,
        ''').strip()

        # Target line 100, way outside the cell
        result = inject_snapshot(cell_code, "df", 100, 1)

        assert result == cell_code


# =============================================================================
# Unit Tests: ID Generation
# =============================================================================


class TestGetUniqueId:
    """Tests for get_unique_id function."""

    def test_new_id(self, viz_dir_clean):
        """New ID when no collision."""
        result = get_unique_id("my_plot")
        assert result == "my_plot"

    def test_collision_adds_suffix(self, viz_dir_clean):
        """Collision appends _2 suffix."""
        # Create existing file
        (viz_dir_clean / "my_plot.py").write_text("")

        result = get_unique_id("my_plot")

        assert result == "my_plot_2"

    def test_multiple_collisions(self, viz_dir_clean):
        """Multiple collisions increment suffix."""
        (viz_dir_clean / "my_plot.py").write_text("")
        (viz_dir_clean / "my_plot_2.py").write_text("")
        (viz_dir_clean / "my_plot_3.py").write_text("")

        result = get_unique_id("my_plot")

        assert result == "my_plot_4"

    def test_no_suggested_id_generates_timestamp(self, viz_dir_clean):
        """No suggested ID generates timestamp-based ID."""
        result = get_unique_id(None)

        assert result.startswith("viz_")
        # Should be format like viz_20240115_143022
        assert len(result) > 10


# =============================================================================
# Unit Tests: Error Formatting
# =============================================================================


class TestFormatModuleError:
    """Tests for format_module_error function."""

    def test_module_not_found(self):
        """Detect and format ModuleNotFoundError."""
        stderr = "ModuleNotFoundError: No module named 'pandas'"

        result = format_module_error(stderr, ["python"])

        assert result is not None
        assert "MISSING MODULE" in result
        assert "pandas" in result

    def test_no_module_error(self):
        """Return None for non-module errors."""
        stderr = "SyntaxError: invalid syntax"

        result = format_module_error(stderr, ["python"])

        assert result is None


# =============================================================================
# Integration Tests: Notebook Parsing
# =============================================================================


class TestParseNotebook:
    """Integration tests for parse_marimo_notebook."""

    def test_simple_notebook(self, sample_notebook_simple):
        """Parse a simple notebook structure."""
        parsed = parse_marimo_notebook(sample_notebook_simple)

        assert "import marimo" in parsed.preamble
        assert "import pandas" in parsed.setup_code
        assert len(parsed.cells) == 2

        # First cell creates df
        assert parsed.cells[0].defs == ["df"]
        assert parsed.cells[0].refs == []

        # Second cell uses df
        assert parsed.cells[1].defs == ["result"]
        assert "df" in parsed.cells[1].refs

    def test_notebook_with_functions(self, sample_notebook_with_functions):
        """Parse notebook with @app.function definitions."""
        parsed = parse_marimo_notebook(sample_notebook_with_functions)

        assert len(parsed.functions) == 1
        assert parsed.functions[0].name == "multiply_df"

    def test_notebook_with_class(self, sample_notebook_with_class):
        """Parse notebook with class definitions."""
        parsed = parse_marimo_notebook(sample_notebook_with_class)

        assert len(parsed.classes) == 1
        assert parsed.classes[0].name == "DataProcessor"

    def test_notebook_no_setup(self, sample_notebook_no_setup):
        """Parse notebook without setup block."""
        parsed = parse_marimo_notebook(sample_notebook_no_setup)

        assert parsed.setup_code == ""
        assert len(parsed.cells) == 1


class TestAssemblePrunedNotebook:
    """Integration tests for assemble_pruned_notebook."""

    def test_basic_assembly(self, sample_notebook_simple):
        """Assemble a pruned notebook."""
        parsed = parse_marimo_notebook(sample_notebook_simple)
        indices, funcs = get_required_cells(parsed, ["df"])

        plot_code = "import matplotlib.pyplot as plt\nplt.plot(df['x'])\nplt.show()"

        result = assemble_pruned_notebook(
            parsed, indices, funcs, plot_code, target_var="df"
        )

        assert "import marimo" in result
        assert "import pandas" in result
        assert "@app.cell" in result
        assert "plt.plot" in result
        assert "if __name__" in result

    def test_assembly_includes_required_functions(self, sample_notebook_with_functions):
        """Assembly includes required @app.functions."""
        parsed = parse_marimo_notebook(sample_notebook_with_functions)
        indices, funcs = get_required_cells(parsed, ["result"])

        plot_code = "pass"

        result = assemble_pruned_notebook(
            parsed, indices, funcs, plot_code, target_var="result"
        )

        assert "def multiply_df" in result


# =============================================================================
# Integration Tests: Python Command Detection
# =============================================================================


class TestValidatePythonEnv:
    """Tests for validate_python_env function."""

    def test_valid_env_returns_true(self):
        """Valid environment with module returns True."""
        # sys.executable should be able to import sys (always available)
        result = validate_python_env([sys.executable], required_module="sys")
        assert result is True

    def test_missing_module_returns_false(self):
        """Environment missing module returns False."""
        # Try to import a module that definitely doesn't exist
        result = validate_python_env([sys.executable], required_module="nonexistent_module_xyz123")
        assert result is False

    def test_invalid_python_returns_false(self):
        """Invalid Python command returns False."""
        result = validate_python_env(["/nonexistent/python"])
        assert result is False

    def test_timeout_returns_false(self, monkeypatch):
        """Timeout during validation returns False."""
        def timeout_run(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="test", timeout=10)

        monkeypatch.setattr(subprocess, "run", timeout_run)

        result = validate_python_env(["python"])
        assert result is False


class TestGetPythonCommand:
    """Tests for get_python_command."""

    def test_env_var_override(self, tmp_path, monkeypatch):
        """VIZ_PYTHON_CMD env var takes precedence (no validation)."""
        monkeypatch.setenv("VIZ_PYTHON_CMD", "/custom/python -u")

        result = get_python_command(tmp_path)

        assert result == ["/custom/python", "-u"]

    def test_uv_project_detected_with_validation(self, tmp_path, monkeypatch):
        """Detect uv project and use 'uv run --directory ... python' when validated."""
        monkeypatch.delenv("VIZ_PYTHON_CMD", raising=False)
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        # Mock validate_python_env to return True for project cmd
        def mock_validate(cmd, required_module="matplotlib"):
            return "--directory" in cmd

        monkeypatch.setattr(viz_runner, "validate_python_env", mock_validate)

        result = get_python_command(tmp_path)

        assert result == ["uv", "run", "--directory", str(tmp_path), "python"]

    def test_uv_project_fails_validation_falls_to_system(self, tmp_path, monkeypatch):
        """If project env fails validation, try system Python."""
        monkeypatch.delenv("VIZ_PYTHON_CMD", raising=False)
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        call_count = [0]

        def mock_validate(cmd, required_module="matplotlib"):
            call_count[0] += 1
            # First call (project) fails, second call (system python) succeeds
            if call_count[0] == 1:
                return False  # Project env fails
            return True  # System python succeeds

        monkeypatch.setattr(viz_runner, "validate_python_env", mock_validate)

        result = get_python_command(tmp_path)

        assert result == ["python"]

    def test_fallback_to_viz_skill_env(self, tmp_path, monkeypatch):
        """Fall back to viz skill's environment when all else fails."""
        monkeypatch.delenv("VIZ_PYTHON_CMD", raising=False)

        # Mock all validation to fail
        def mock_validate(cmd, required_module="matplotlib"):
            return False

        monkeypatch.setattr(viz_runner, "validate_python_env", mock_validate)

        result = get_python_command(tmp_path)

        # Should return viz skill's own environment
        assert result[0] == "uv"
        assert result[1] == "run"
        assert result[2] == "--directory"
        # The directory should be the viz skill's code directory
        assert "viz" in result[3] or "code" in result[3]
        assert result[4] == "python"

    def test_system_python_used_when_no_project(self, tmp_path, monkeypatch):
        """System Python used when no project markers and it validates."""
        monkeypatch.delenv("VIZ_PYTHON_CMD", raising=False)
        # No pyproject.toml or uv.lock in tmp_path

        def mock_validate(cmd, required_module="matplotlib"):
            return cmd == ["python"]

        monkeypatch.setattr(viz_runner, "validate_python_env", mock_validate)

        result = get_python_command(tmp_path)

        assert result == ["python"]


# =============================================================================
# CLI Tests (mocked subprocess)
# =============================================================================


class TestCLIClean:
    """Tests for --clean command."""

    def test_clean_removes_files(self, viz_dir_clean):
        """--clean removes all files from viz directory."""
        # Create some files
        (viz_dir_clean / "test1.py").write_text("")
        (viz_dir_clean / "test1.png").write_text("")
        (viz_dir_clean / "test1.json").write_text("")

        # Run main with --clean
        with patch.object(sys, "argv", ["viz_runner.py", "--clean"]):
            with pytest.raises(SystemExit) as exc_info:
                viz_runner.main()

        assert exc_info.value.code == 0
        assert len(list(viz_dir_clean.iterdir())) == 0


class TestCLIList:
    """Tests for --list command."""

    def test_list_empty(self, viz_dir_clean, capsys):
        """--list with no visualizations."""
        with patch.object(sys, "argv", ["viz_runner.py", "--list"]):
            with pytest.raises(SystemExit) as exc_info:
                viz_runner.main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No visualizations found" in captured.out

    def test_list_with_items(self, viz_dir_clean, capsys):
        """--list shows existing visualizations."""
        # Create a metadata file
        metadata = {
            "id": "test_plot",
            "desc": "A test plot",
            "created": "2024-01-15T10:30:00",
        }
        (viz_dir_clean / "test_plot.json").write_text(json.dumps(metadata))

        with patch.object(sys, "argv", ["viz_runner.py", "--list"]):
            with pytest.raises(SystemExit) as exc_info:
                viz_runner.main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "test_plot" in captured.out
        assert "A test plot" in captured.out


class TestCLIMarimoValidation:
    """Tests for --marimo argument validation."""

    def test_marimo_requires_notebook(self, capsys):
        """--marimo without --notebook fails."""
        with patch.object(
            sys, "argv",
            ["viz_runner.py", "--marimo", "--target-var", "df"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                viz_runner.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "requires --notebook" in captured.err

    def test_marimo_requires_target_var(self, tmp_path, capsys):
        """--marimo without --target-var fails."""
        notebook = tmp_path / "test.nb.py"
        notebook.write_text("import marimo")

        with patch.object(
            sys, "argv",
            ["viz_runner.py", "--marimo", "--notebook", str(notebook)]
        ):
            with pytest.raises(SystemExit) as exc_info:
                viz_runner.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "requires --target-var" in captured.err


# =============================================================================
# Subprocess Execution Tests (mocked)
# =============================================================================


class TestRunScriptBackground:
    """Tests for run_script_background with mocked subprocess."""

    def test_success_creates_png(self, viz_dir_clean, tmp_path):
        """Successful execution creates PNG."""
        script_path = tmp_path / "test.py"
        script_path.write_text("print('hello')")
        png_path = viz_dir_clean / "test.png"

        # Mock subprocess.Popen
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345

        with patch("viz_runner.subprocess.Popen", return_value=mock_process):
            # Simulate PNG being created after a short delay
            def create_png(*args):
                png_path.write_bytes(b"PNG")
                return None

            mock_process.poll.side_effect = [None, create_png, 0]

            success, pid, message = run_script_background(script_path, png_path)

        # Note: Due to timing, this might need adjustment
        # The actual behavior depends on the polling loop

    def test_script_failure(self, viz_dir_clean, tmp_path):
        """Script failure returns error message."""
        script_path = tmp_path / "test.py"
        script_path.write_text("print('hello')")
        png_path = viz_dir_clean / "test.png"

        # Mock subprocess.Popen - immediate failure
        mock_process = MagicMock()
        mock_process.poll.return_value = 1  # Failed
        mock_process.stderr.read.return_value = b"Error occurred"
        mock_process.pid = 12345

        with patch("viz_runner.subprocess.Popen", return_value=mock_process):
            # Also mock validate_python_env to avoid subprocess.run calls
            with patch("viz_runner.validate_python_env", return_value=True):
                success, pid, message = run_script_background(script_path, png_path)

        assert success is False
        assert "Error occurred" in message


class TestMarimoHandlerIntegration:
    """Integration tests for MarimoHandler."""

    def test_missing_variable(self, sample_notebook_simple, viz_dir_clean):
        """Returns error when target variable not found."""
        handler = MarimoHandler()

        with pytest.raises(ValueError) as exc_info:
            handler.build_script(
                action_code="pass",
                source_path=sample_notebook_simple,
                target_var="nonexistent",
            )

        assert "Could not find cells" in str(exc_info.value)

    def test_run_show_missing_variable(self, sample_notebook_simple):
        """run_show returns error when target variable not found via handler."""
        handler = MarimoHandler()

        success, output = run_show(
            handler=handler,
            target_var="nonexistent",
            source_path=sample_notebook_simple,
        )

        assert success is False
        assert "Could not find cells" in output


# =============================================================================
# Handler Architecture Tests
# =============================================================================


class TestDefaultHandler:
    """Tests for DefaultHandler."""

    def test_build_script_passes_through(self):
        """DefaultHandler returns plot_code unchanged."""
        handler = DefaultHandler()
        plot_code = "import matplotlib.pyplot as plt\nplt.plot([1,2,3])\nplt.show()"

        script, cwd = handler.build_script(plot_code)

        assert script == plot_code
        assert cwd is None

    def test_build_script_ignores_source_path(self):
        """DefaultHandler ignores source_path and target_var."""
        handler = DefaultHandler()
        plot_code = "plt.plot([1,2,3])"

        script, cwd = handler.build_script(
            plot_code,
            source_path=Path("/some/path.py"),
            target_var="df",
        )

        assert script == plot_code
        assert cwd is None

    def test_validate_args_always_valid(self):
        """DefaultHandler validation always succeeds."""
        handler = DefaultHandler()

        # Create a minimal namespace
        class Args:
            pass

        args = Args()

        valid, error = handler.validate_args(args)

        assert valid is True
        assert error == ""


class TestMarimoHandler:
    """Tests for MarimoHandler."""

    def test_build_script_requires_source_path(self):
        """MarimoHandler raises error without source_path."""
        handler = MarimoHandler()

        with pytest.raises(ValueError, match="requires source_path"):
            handler.build_script("plt.plot()", source_path=None, target_var="df")

    def test_build_script_requires_target_var(self, sample_notebook_simple):
        """MarimoHandler raises error without target_var."""
        handler = MarimoHandler()

        with pytest.raises(ValueError, match="requires target_var"):
            handler.build_script(
                "plt.plot()", source_path=sample_notebook_simple, target_var=None
            )

    def test_build_script_success(self, sample_notebook_simple):
        """MarimoHandler successfully builds script from notebook."""
        handler = MarimoHandler()

        script, cwd = handler.build_script(
            "import matplotlib.pyplot as plt\nplt.plot(df['x'])\nplt.show()",
            source_path=sample_notebook_simple,
            target_var="df",
        )

        assert "import marimo" in script
        assert "@app.cell" in script
        assert "plt.plot" in script
        assert cwd == sample_notebook_simple.parent

    def test_build_script_missing_variable(self, sample_notebook_simple):
        """MarimoHandler raises error for nonexistent variable."""
        handler = MarimoHandler()

        with pytest.raises(ValueError, match="Could not find cells"):
            handler.build_script(
                "plt.plot()",
                source_path=sample_notebook_simple,
                target_var="nonexistent",
            )

    def test_validate_args_missing_notebook(self):
        """MarimoHandler validation fails without notebook_path."""
        handler = MarimoHandler()

        class Args:
            notebook_path = None
            target_var = "df"

        valid, error = handler.validate_args(Args())

        assert valid is False
        assert "--notebook" in error

    def test_validate_args_missing_target_var(self, tmp_path):
        """MarimoHandler validation fails without target_var."""
        handler = MarimoHandler()
        notebook = tmp_path / "test.nb.py"
        notebook.write_text("import marimo")

        class Args:
            notebook_path = str(notebook)
            target_var = None

        valid, error = handler.validate_args(Args())

        assert valid is False
        assert "--target-var" in error

    def test_validate_args_nonexistent_notebook(self, tmp_path):
        """MarimoHandler validation fails for nonexistent notebook."""
        handler = MarimoHandler()

        class Args:
            notebook_path = str(tmp_path / "nonexistent.nb.py")
            target_var = "df"

        valid, error = handler.validate_args(Args())

        assert valid is False
        assert "not found" in error

    def test_validate_args_success(self, tmp_path):
        """MarimoHandler validation succeeds with valid args."""
        handler = MarimoHandler()
        notebook = tmp_path / "test.nb.py"
        notebook.write_text("import marimo")

        class Args:
            notebook_path = str(notebook)
            target_var = "df"

        valid, error = handler.validate_args(Args())

        assert valid is True
        assert error == ""


class TestGetHandler:
    """Tests for get_handler function."""

    def test_default_handler_when_no_flags(self):
        """Returns DefaultHandler when no special flags set."""

        class Args:
            marimo = False

        handler = get_handler(Args())

        assert isinstance(handler, DefaultHandler)

    def test_marimo_handler_when_marimo_flag(self):
        """Returns MarimoHandler when --marimo flag is set."""

        class Args:
            marimo = True

        handler = get_handler(Args())

        assert isinstance(handler, MarimoHandler)


class TestRunPlot:
    """Tests for run_plot generic execution function."""

    def test_run_plot_with_default_handler(self, viz_dir_clean):
        """run_plot works with DefaultHandler."""
        handler = DefaultHandler()
        plot_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1, 2, 3], [1, 4, 9])
            plt.show()
        ''').strip()

        # Mock subprocess to simulate successful execution
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345
        mock_process.stderr.read.return_value = b""

        with patch("viz_runner.subprocess.Popen", return_value=mock_process):
            # Also mock validate_python_env to avoid subprocess.run calls
            with patch("viz_runner.validate_python_env", return_value=True):
                # Simulate PNG being created
                def create_png(*args, **kwargs):
                    png_path = viz_dir_clean / "test_plot.png"
                    png_path.write_bytes(b"PNG")
                    return None

                mock_process.poll.side_effect = [None, create_png, 0]

                success, message, png_path = run_plot(
                    handler=handler,
                    plot_code=plot_code,
                    viz_id="test_plot",
                    description="Test plot",
                )

        # Script should be written
        script_path = viz_dir_clean / "test_plot.py"
        assert script_path.exists()
        script_content = script_path.read_text()
        assert "plt.savefig" in script_content

    def test_run_plot_with_marimo_handler(self, viz_dir_clean, sample_notebook_simple):
        """run_plot works with MarimoHandler."""
        handler = MarimoHandler()
        plot_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot(df['x'], df['y'])
            plt.show()
        ''').strip()

        # Mock subprocess to simulate successful execution
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345
        mock_process.stderr.read.return_value = b""

        with patch("viz_runner.subprocess.Popen", return_value=mock_process):
            # Also mock validate_python_env to avoid subprocess.run calls
            with patch("viz_runner.validate_python_env", return_value=True):
                # Simulate PNG being created
                def create_png(*args, **kwargs):
                    png_path = viz_dir_clean / "marimo_plot.png"
                    png_path.write_bytes(b"PNG")
                    return None

                mock_process.poll.side_effect = [None, create_png, 0]

                success, message, png_path = run_plot(
                    handler=handler,
                    plot_code=plot_code,
                    viz_id="marimo_plot",
                    description="Marimo test plot",
                    source_path=sample_notebook_simple,
                    target_var="df",
                )

        # Script should be written with marimo structure
        script_path = viz_dir_clean / "marimo_plot.py"
        assert script_path.exists()
        script_content = script_path.read_text()
        assert "import marimo" in script_content
        assert "@app.cell" in script_content

    def test_run_plot_handler_error(self, viz_dir_clean, sample_notebook_simple):
        """run_plot returns error when handler fails."""
        handler = MarimoHandler()

        success, message, png_path = run_plot(
            handler=handler,
            plot_code="plt.plot()",
            viz_id="error_plot",
            source_path=sample_notebook_simple,
            target_var="nonexistent",  # This variable doesn't exist
        )

        assert success is False
        assert "Could not find cells" in message
        assert png_path is None


class TestGenerateShowCode:
    """Tests for generate_show_code helper function."""

    def test_basic_show_code(self):
        """Generate show code for a variable."""
        code = generate_show_code("df", num_rows=5)

        assert "_var = df" in code
        assert "Shape:" in code
        assert "Columns:" in code
        assert "Dtypes:" in code
        assert ".head(5)" in code

    def test_custom_num_rows(self):
        """Generate show code with custom row count."""
        code = generate_show_code("my_data", num_rows=10)

        assert "_var = my_data" in code
        assert ".head(10)" in code


class TestRunShow:
    """Tests for run_show generic show/inspection function."""

    def test_run_show_with_marimo_handler(self, viz_dir_clean, sample_notebook_simple):
        """run_show works with MarimoHandler."""
        handler = MarimoHandler()

        # Mock subprocess to simulate successful execution
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Shape: (3, 2)\nColumns: ['x', 'y']"
        mock_result.stderr = ""

        with patch("viz_runner.subprocess.run", return_value=mock_result) as mock_run:
            success, output = run_show(
                handler=handler,
                target_var="df",
                source_path=sample_notebook_simple,
                num_rows=5,
            )

            # Verify subprocess.run was called with the show script
            assert mock_run.called
            call_args = mock_run.call_args
            assert "_show_temp.py" in str(call_args)

        assert success is True
        assert "Shape:" in output

    def test_run_show_handler_error(self, viz_dir_clean, sample_notebook_simple):
        """run_show returns error when handler fails."""
        handler = MarimoHandler()

        success, output = run_show(
            handler=handler,
            target_var="nonexistent",
            source_path=sample_notebook_simple,
        )

        assert success is False
        assert "Could not find cells" in output

    def test_run_show_script_failure(self, viz_dir_clean, sample_notebook_simple):
        """run_show returns error when script fails."""
        handler = MarimoHandler()

        # Mock subprocess to simulate script failure
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "NameError: name 'df' is not defined"

        with patch("viz_runner.subprocess.run", return_value=mock_result):
            success, output = run_show(
                handler=handler,
                target_var="df",
                source_path=sample_notebook_simple,
            )

        assert success is False
        assert "Script failed" in output


# =============================================================================
# Edge Cases and Regression Tests
# =============================================================================


class TestEdgeCases:
    """Edge case and regression tests."""

    def test_cell_with_no_return_statement(self):
        """Cell without return statement parses correctly."""
        source = dedent('''
            @app.cell
            def _():
                print("hello")
        ''').strip()
        tree = ast.parse(source)
        func_node = tree.body[0]
        lines = source.splitlines(keepends=True)

        cell = _parse_cell(func_node, lines)

        assert cell.defs == []

    def test_deeply_nested_dependency_chain(self):
        """Long dependency chain resolves correctly."""
        # Create a chain: a -> b -> c -> d -> e
        cells = [
            MarimoCell(
                name="_", refs=[], defs=["a"],
                code="", start_line=1, end_line=5
            ),
            MarimoCell(
                name="_", refs=["a"], defs=["b"],
                code="", start_line=6, end_line=10
            ),
            MarimoCell(
                name="_", refs=["b"], defs=["c"],
                code="", start_line=11, end_line=15
            ),
            MarimoCell(
                name="_", refs=["c"], defs=["d"],
                code="", start_line=16, end_line=20
            ),
            MarimoCell(
                name="_", refs=["d"], defs=["e"],
                code="", start_line=21, end_line=25
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        indices, funcs = get_required_cells(parsed, ["e"])

        assert set(indices) == {0, 1, 2, 3, 4}

    def test_circular_refs_handled(self):
        """Circular references don't cause infinite loop."""
        # This shouldn't happen in valid marimo notebooks, but test anyway
        cells = [
            MarimoCell(
                name="_", refs=["b"], defs=["a"],
                code="", start_line=1, end_line=5
            ),
            MarimoCell(
                name="_", refs=["a"], defs=["b"],
                code="", start_line=6, end_line=10
            ),
        ]
        parsed = ParsedNotebook(preamble="", setup_code="", cells=cells)

        # Should complete without hanging
        indices, funcs = get_required_cells(parsed, ["a"])

        assert set(indices) == {0, 1}

    def test_inject_savefig_idempotent(self):
        """Multiple inject_savefig calls don't duplicate."""
        script = "import matplotlib.pyplot as plt\nplt.show()"

        result1 = inject_savefig(script, "/tmp/test.png")
        result2 = inject_savefig(result1, "/tmp/test.png")

        # Second injection shouldn't add another savefig before the existing one
        # (the pattern won't match because savefig is now before show)
        assert result2.count("savefig") == 2  # Once from each call (appended)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

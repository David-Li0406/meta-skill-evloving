#!/usr/bin/env python3
"""
Test stub generator from code analysis.

Usage:
    python generate_tests.py --file ./src/utils.js --framework jest
    python generate_tests.py --file ./src/service.py --framework pytest
"""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================


@dataclass
class FunctionInfo:
    name: str
    params: list[str]
    return_type: str | None
    is_async: bool
    line_number: int


# =============================================================================
# PARSERS
# =============================================================================


def parse_javascript(content: str) -> list[FunctionInfo]:
    """Parse JavaScript/TypeScript functions."""
    functions = []

    # Regular functions
    func_pattern = r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)"
    for match in re.finditer(func_pattern, content):
        line_num = content[: match.start()].count("\n") + 1
        functions.append(
            FunctionInfo(
                name=match.group(1),
                params=[
                    p.strip().split(":")[0].strip()
                    for p in match.group(2).split(",")
                    if p.strip()
                ],
                return_type=None,
                is_async="async" in match.group(0),
                line_number=line_num,
            )
        )

    # Arrow functions (const name = ...)
    arrow_pattern = r"(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*(?::\s*\w+)?\s*=>"
    for match in re.finditer(arrow_pattern, content):
        line_num = content[: match.start()].count("\n") + 1
        is_async = "async" in match.group(0)
        # Extract params from the full match
        params_match = re.search(r"\(([^)]*)\)", match.group(0))
        params = []
        if params_match:
            params = [
                p.strip().split(":")[0].strip()
                for p in params_match.group(1).split(",")
                if p.strip()
            ]

        functions.append(
            FunctionInfo(
                name=match.group(1),
                params=params,
                return_type=None,
                is_async=is_async,
                line_number=line_num,
            )
        )

    # Class methods
    method_pattern = r"(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*(?::\s*[\w<>[\]]+)?\s*\{"
    for match in re.finditer(method_pattern, content):
        name = match.group(1)
        if name in ["if", "for", "while", "switch", "catch", "constructor"]:
            continue
        line_num = content[: match.start()].count("\n") + 1
        functions.append(
            FunctionInfo(
                name=name,
                params=[
                    p.strip().split(":")[0].strip()
                    for p in match.group(2).split(",")
                    if p.strip()
                ],
                return_type=None,
                is_async="async" in match.group(0),
                line_number=line_num,
            )
        )

    return functions


def parse_python(content: str) -> list[FunctionInfo]:
    """Parse Python functions."""
    functions = []

    # Function definitions
    func_pattern = r"(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\w+))?:"
    for match in re.finditer(func_pattern, content):
        name = match.group(1)
        if name.startswith("_") and not name.startswith("__"):
            continue  # Skip private methods (keep dunder methods)

        line_num = content[: match.start()].count("\n") + 1
        params_str = match.group(2)

        # Parse parameters, excluding self/cls
        params = []
        for p in params_str.split(","):
            p = p.strip()
            if p and p not in ["self", "cls"]:
                # Remove type hints and defaults
                param_name = p.split(":")[0].split("=")[0].strip()
                if param_name:
                    params.append(param_name)

        functions.append(
            FunctionInfo(
                name=name,
                params=params,
                return_type=match.group(3),
                is_async="async" in match.group(0),
                line_number=line_num,
            )
        )

    return functions


# =============================================================================
# GENERATORS
# =============================================================================


def generate_jest_tests(functions: list[FunctionInfo], module_name: str) -> str:
    """Generate Jest test stubs."""
    lines = [
        f"import {{ {', '.join(f.name for f in functions)} }} from './{module_name}';",
        "",
        f"describe('{module_name}', () => {{",
    ]

    for func in functions:
        lines.append(f"  describe('{func.name}', () => {{")

        # Happy path test
        if func.is_async:
            lines.append("    it('should return expected result', async () => {")
            lines.append("      // Arrange")
            if func.params:
                lines.extend(
                    [
                        f"      const {param} = undefined; // TODO: Add test value"
                        for param in func.params
                    ]
                )
            lines.append("")
            lines.append("      // Act")
            params_str = ", ".join(func.params)
            lines.append(f"      const result = await {func.name}({params_str});")
            lines.append("")
            lines.append("      // Assert")
            lines.append("      expect(result).toBeDefined();")
            lines.append("    });")
        else:
            lines.append("    it('should return expected result', () => {")
            lines.append("      // Arrange")
            if func.params:
                lines.extend(
                    [
                        f"      const {param} = undefined; // TODO: Add test value"
                        for param in func.params
                    ]
                )
            lines.append("")
            lines.append("      // Act")
            params_str = ", ".join(func.params)
            lines.append(f"      const result = {func.name}({params_str});")
            lines.append("")
            lines.append("      // Assert")
            lines.append("      expect(result).toBeDefined();")
            lines.append("    });")

        lines.append("")

        # Edge case tests
        lines.append("    describe('edge cases', () => {")
        if func.params:
            lines.append("      it('should handle null input', () => {")
            lines.append("        // TODO: Test null handling")
            lines.append("      });")
            lines.append("")
            lines.append("      it('should handle empty input', () => {")
            lines.append("        // TODO: Test empty input")
            lines.append("      });")
        lines.append("    });")

        lines.append("")

        # Error case test
        lines.append("    describe('error handling', () => {")
        if func.is_async:
            lines.append("      it('should throw on invalid input', async () => {")
            lines.append(
                f"        await expect({func.name}(/* invalid */)).rejects.toThrow();"
            )
            lines.append("      });")
        else:
            lines.append("      it('should throw on invalid input', () => {")
            lines.append(f"        expect(() => {func.name}(/* invalid */)).toThrow();")
            lines.append("      });")
        lines.append("    });")

        lines.append("  });")
        lines.append("")

    lines.append("});")

    return "\n".join(lines)


def generate_pytest_tests(functions: list[FunctionInfo], module_name: str) -> str:
    """Generate pytest test stubs."""
    lines = [
        "import pytest",
        f"from {module_name} import {', '.join(f.name for f in functions)}",
        "",
        "",
    ]

    for func in functions:
        class_name = "".join(word.title() for word in func.name.split("_"))
        lines.append(f"class Test{class_name}:")

        # Happy path test
        if func.is_async:
            lines.append("    @pytest.mark.asyncio")
            lines.append("    async def test_returns_expected_result(self):")
        else:
            lines.append("    def test_returns_expected_result(self):")

        lines.append("        # Arrange")
        if func.params:
            lines.extend(
                [
                    f"        {param} = None  # TODO: Add test value"
                    for param in func.params
                ]
            )
        lines.append("")
        lines.append("        # Act")
        params_str = ", ".join(func.params)
        if func.is_async:
            lines.append(f"        result = await {func.name}({params_str})")
        else:
            lines.append(f"        result = {func.name}({params_str})")
        lines.append("")
        lines.append("        # Assert")
        lines.append("        assert result is not None")
        lines.append("")

        # Edge case tests
        if func.params:
            if func.is_async:
                lines.append("    @pytest.mark.asyncio")
                lines.append("    async def test_handles_none_input(self):")
                lines.append("        # TODO: Test None handling")
                lines.append("        pass")
            else:
                lines.append("    def test_handles_none_input(self):")
                lines.append("        # TODO: Test None handling")
                lines.append("        pass")
            lines.append("")

        # Error test
        if func.is_async:
            lines.append("    @pytest.mark.asyncio")
            lines.append("    async def test_raises_on_invalid_input(self):")
            lines.append(
                "        with pytest.raises(ValueError):  # TODO: Adjust exception type"
            )
            lines.append(f"            await {func.name}(None)")
        else:
            lines.append("    def test_raises_on_invalid_input(self):")
            lines.append(
                "        with pytest.raises(ValueError):  # TODO: Adjust exception type"
            )
            lines.append(f"            {func.name}(None)")
        lines.append("")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate test stubs from code")
    parser.add_argument("--file", required=True, help="Source file to analyze")
    parser.add_argument(
        "--framework",
        choices=["jest", "pytest", "vitest"],
        default="jest",
        help="Test framework",
    )
    parser.add_argument("--output", help="Output file (default: stdout)")

    args = parser.parse_args()

    source_path = Path(args.file)
    if not source_path.exists():
        print(f"Error: File {source_path} not found")
        return 1

    content = source_path.read_text()
    module_name = source_path.stem

    # Detect language from extension
    ext = source_path.suffix.lower()
    if ext in [".js", ".jsx", ".ts", ".tsx", ".mjs"]:
        functions = parse_javascript(content)
    elif ext in [".py"]:
        functions = parse_python(content)
    else:
        print(f"Error: Unsupported file type {ext}")
        return 1

    if not functions:
        print("No functions found to test")
        return 0

    print(f"Found {len(functions)} functions to test")

    # Generate tests
    if args.framework in ["jest", "vitest"]:
        output = generate_jest_tests(functions, module_name)
    elif args.framework == "pytest":
        output = generate_pytest_tests(functions, module_name)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Tests written to {args.output}")
    else:
        print("\n" + "=" * 60)
        print(output)

    return 0


if __name__ == "__main__":
    exit(main())

# -*- coding: utf-8 -*-
"""COBOL Migration Skill.

COBOL から Java への移行を支援する Skill。
確定的な処理（解析、型変換、テスト実行）を提供。
LLM が必要な処理（コード翻訳、差分分析）は Agent に委譲。

使用例:
    >>> from apps.code_migration_assistant.skills.cobol_migration import CobolMigrationSkill
    >>> skill = CobolMigrationSkill()
    >>> ast = skill.parse_cobol(cobol_code)
    >>> java_code = skill.apply_type_mappings(ast)
"""

from dataclasses import dataclass, field
from typing import Any

from apps.code_migration_assistant.parsers import PLYCobolParser


@dataclass
class ParseResult:
    """解析結果."""

    ast: dict[str, Any]
    metadata: dict[str, Any]
    variables: list[dict[str, Any]]
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class TypeMapping:
    """型マッピング情報."""

    cobol_name: str
    cobol_type: str
    pic_clause: str
    java_name: str
    java_type: str


@dataclass
class TestCase:
    """テストケース."""

    name: str
    inputs: dict[str, Any]
    expected_outputs: dict[str, Any]
    description: str = ""


class CobolMigrationSkill:
    """COBOL 移行 Skill.

    確定的な処理を提供：
    - COBOL 構文解析（PLY パーサー使用）
    - 型マッピング（COBOL PIC → Java 型）
    - 命名規則変換
    - テスト実行・結果比較

    LLM が必要な処理（コード翻訳、修復提案）は Agent に委譲。
    """

    # COBOL PIC → Java 型マッピング（確定的ルール）
    TYPE_MAPPINGS = {
        "numeric_small": "int",      # PIC 9(1-9)
        "numeric_large": "long",     # PIC 9(10+)
        "decimal": "BigDecimal",     # PIC 9V9
        "string": "String",          # PIC X
        "comp3": "BigDecimal",       # COMP-3
    }

    def __init__(self) -> None:
        """初期化."""
        self._parser = None

    def parse_cobol(self, cobol_code: str, file_name: str = "unknown.cob") -> ParseResult:
        """COBOL コードを解析.

        Args:
            cobol_code: COBOL ソースコード
            file_name: ファイル名

        Returns:
            解析結果（AST、メタデータ、変数情報）
        """
        errors: list[str] = []
        warnings: list[str] = []

        try:
            parser = PLYCobolParser(cobol_code)
            ast = parser.parse()
            variables = parser.extract_variables(ast)

            if not ast.get("program_id"):
                errors.append("PROGRAM-ID not found")
                ast["program_id"] = "UNKNOWN"

            metadata = ast.get("metadata", {})
            metadata["file_name"] = file_name
            metadata["variables"] = variables

            return ParseResult(
                ast=ast,
                metadata=metadata,
                variables=variables,
                errors=errors,
                warnings=warnings,
            )

        except Exception as e:
            errors.append(f"Parse error: {e}")
            return ParseResult(
                ast={"program_id": "UNKNOWN", "divisions": {}},
                metadata={"file_name": file_name},
                variables=[],
                errors=errors,
                warnings=["Using fallback parser"],
            )

    def get_type_mappings(self, variables: list[dict[str, Any]]) -> list[TypeMapping]:
        """変数の型マッピングを取得.

        Args:
            variables: COBOL 変数リスト

        Returns:
            型マッピング情報リスト
        """
        mappings: list[TypeMapping] = []

        for var in variables:
            java_name = self._convert_variable_name(var["name"])
            java_type = self._convert_type(var.get("type", ""), var.get("pic_clause", ""))

            mappings.append(TypeMapping(
                cobol_name=var["name"],
                cobol_type=var.get("type", "unknown"),
                pic_clause=var.get("pic_clause", ""),
                java_name=java_name,
                java_type=java_type,
            ))

        return mappings

    def _convert_variable_name(self, cobol_name: str) -> str:
        """COBOL 変数名を Java 変数名に変換（camelCase）."""
        name = cobol_name.replace("WS-", "").replace("ws-", "")
        parts = name.replace("-", "_").split("_")
        if not parts:
            return "field"
        return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])

    def _convert_type(self, cobol_type: str, pic_clause: str) -> str:
        """COBOL 型を Java 型に変換."""
        if cobol_type == "decimal" or "V" in pic_clause.upper():
            return "BigDecimal"
        elif cobol_type == "numeric":
            # 桁数で int/long を判定
            import re
            match = re.search(r"9\((\d+)\)", pic_clause)
            if match:
                digits = int(match.group(1))
                return "long" if digits > 9 else "int"
            return "int"
        elif cobol_type == "string":
            return "String"
        return "Object"

    def compare_outputs(
        self, expected: dict[str, Any], actual: dict[str, Any]
    ) -> dict[str, Any]:
        """出力を比較.

        Args:
            expected: 期待される出力（COBOL 実行結果）
            actual: 実際の出力（Java 実行結果）

        Returns:
            比較結果（一致/差異）
        """
        differences: list[dict[str, Any]] = []
        is_equal = True

        for key in set(expected.keys()) | set(actual.keys()):
            exp_val = expected.get(key)
            act_val = actual.get(key)

            if exp_val != act_val:
                is_equal = False
                differences.append({
                    "field": key,
                    "expected": exp_val,
                    "actual": act_val,
                    "type": self._classify_difference(exp_val, act_val),
                })

        return {
            "is_equal": is_equal,
            "differences": differences,
            "match_rate": 1.0 - len(differences) / max(len(expected), 1),
        }

    def _classify_difference(self, expected: Any, actual: Any) -> str:
        """差異の種類を分類."""
        if expected is None or actual is None:
            return "missing_value"
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            if abs(expected - actual) < 0.01:
                return "precision_diff"
            return "value_diff"
        if isinstance(expected, str) and isinstance(actual, str):
            if expected.strip() == actual.strip():
                return "whitespace_diff"
        return "type_or_value_diff"


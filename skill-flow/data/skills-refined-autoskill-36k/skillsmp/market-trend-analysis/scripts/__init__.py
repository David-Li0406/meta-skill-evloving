# -*- coding: utf-8 -*-
"""Market Trend Analysis - 確定性処理スクリプト群.

このパッケージはLLM推論を使用しない確定性処理を提供します。
Agentは「いつ実行するか」を判断し、これらのスクリプトは「どう実行するか」を担当。

含まれるスクリプト:
- validate_input: 入力データ検証
- extract_keywords: キーワード抽出
- generate_report_skeleton: レポート骨格生成
"""

# NOTE: ディレクトリ名にハイフンが含まれるため、
# 親ディレクトリからの直接importは非推奨。
# 以下のパターンを使用してください:
#
# from pathlib import Path
# import importlib.util
#
# script_path = Path(__file__).parent / "validate_input.py"
# spec = importlib.util.spec_from_file_location("validate_input", script_path)
# module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)

__all__: list[str] = []


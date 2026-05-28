# -*- coding: utf-8 -*-
"""Market Trend Analysis Skill - 市場動向分析.

このSkillは市場動向を自動分析するための機能を提供します：
- キーワード抽出（確定性処理）
- トレンドスコア計算（LLM推論）
- センチメント分析（LLM推論）
- レポート骨格生成（確定性処理）

Anthropic Skills体系に準拠し、以下の3層構造を採用：
1. SKILL.md: メタ情報 + 指示
2. scripts/: 確定性処理（脚本化）
3. references/: 参照資料（必要時読み込み）

使用例:
    >>> from agentflow.skills import SkillRouter
    >>> router = SkillRouter()
    >>> await router.initialize()
    >>> 
    >>> result = router.route("市場トレンドを分析")
    >>> if result.matched:
    ...     skill = result.skill
    ...     # 確定性処理を直接呼び出し
    ...     from agentflow.skills.builtin.market_trend_analysis.scripts.validate_input import (
    ...         validate_articles_input,
    ...     )
    ...     validation = validate_articles_input(input_data)
"""

from pathlib import Path

# Skillディレクトリパス
SKILL_DIR = Path(__file__).parent

# scripts/ からの確定性処理インポート
# NOTE: ハイフンを含むパスはimportできないため、直接パス参照を推奨

__all__ = [
    "SKILL_DIR",
]


# MCP Integration Design
# ======================
# Phase C: Prompt-Lang Generator を MCP ツールとして公開する設計

> **Status**: ✅ IMPLEMENTED (2026-01-25)

---

## 1. 目標

1. **MCP サーバとして公開**: prompt-lang-generator を MCP tool として登録
2. **@context の mcp: 参照実装**: 他ツールから Prompt-Lang 生成を呼び出し可能に
3. **メタ学習ループ**: 実行ログ蓄積 → パターン抽出（将来計画）

---

## 2. 統合アーキテクチャ

```
┌──────────────────────────────────────────────────────┐
│ Antigravity IDE / Claude                              │
│                                                       │
│  ┌─────────────┐      @context: mcp:prompt-lang...   │
│  │ SKILL.md    │ ◄───────────────────────────────────┤
│  │ (Prompt-Lang│                                     │
│  │  Generator) │                                     │
│  └──────┬──────┘                                     │
│         │                                            │
│         ▼                                            │
│  ┌─────────────┐     ┌─────────────┐                │
│  │ MCP Server  │ ◄───│ gnosis_mcp  │                │
│  │ prompt-lang │     │ _server.py  │                │
│  └─────────────┘     └─────────────┘                │
│         │                                            │
│         ▼                                            │
│  ┌─────────────┐                                     │
│  │ templates/  │                                     │
│  │ rubric_std  │                                     │
│  └─────────────┘                                     │
└──────────────────────────────────────────────────────┘
```

---

## 3. MCP Tool 定義案

```python
# mcp/prompt_lang_mcp_server.py (TODO)

@tool("prompt_lang_generate")
async def generate(
    requirements: str,
    domain: Optional[str] = None,  # technical, rag, summarization
    output_format: str = "skill.md"
) -> str:
    """
    自然言語要件から Prompt-Lang コードを生成
    
    Args:
        requirements: 自然言語による要件説明
        domain: ドメインヒント（指定なしなら自動判定）
        output_format: 出力形式（skill.md, .prompt）
    
    Returns:
        生成された Prompt-Lang コード
    """
    pass
```

---

## 4. 実装タスク（次回用）

- [ ] `mcp/prompt_lang_mcp_server.py` 作成
- [ ] `generate` ツール実装
- [ ] テンプレート読み込みロジック
- [ ] ドメイン自動判定ロジック
- [ ] Antigravity MCP 設定に追加
- [ ] テスト実行

---

## 5. @context mcp: 参照の実装

現行の Prompt-Lang v2.0 では `@context: mcp:...` の構文は認識するが、実行時の解決は未実装。

### 実装案

```python
# forge/prompt-lang/prompt_lang.py

def _resolve_mcp_context(ref: str) -> str:
    """
    mcp:server.tool("method") 形式の参照を解決
    
    例: mcp:gnosis.tool("search").with(file:"query.txt")
    """
    # 1. MCP サーバ名を抽出
    # 2. ツール名を抽出
    # 3. MCP クライアント経由で呼び出し
    # 4. 結果をコンテキストとして返却
    pass
```

---

## 6. メタ学習ループ（将来計画）

> 優先度: 低、Phase C の後

1. **ログ蓄積**: 生成リクエスト + 結果 + 評価スコア
2. **パターン抽出**: 高スコア生成物の共通パターンを抽出
3. **テンプレート更新**: ドメインテンプレートに反映

---

## 7. 参考

- [gnosis_mcp_server.py](file:///m:/Hegemonikon/mcp/gnosis_mcp_server.py) — 既存 MCP サーバ参考
- [Prompt-Lang v2 仕様](file:///m:/Hegemonikon/docs/specs/prompt-lang-v2-spec.md)
- [Perplexity 調査レポート](file:///m:/Hegemonikon/docs/research/perplexity/prompt-lang-report.md)

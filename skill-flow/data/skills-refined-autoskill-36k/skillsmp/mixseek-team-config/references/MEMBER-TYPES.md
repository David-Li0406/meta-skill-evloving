# Member Agent Types Reference

## 概要

MixSeek-CoreのMember Agentタイプの詳細説明と使用例です。

## タイプ一覧

### 1. `plain` - 基本テキスト生成

**説明**: 最もシンプルなエージェントタイプ。追加ツールなしでテキスト生成のみを行います。

**用途**:
- テキストの要約・分析
- 文章の生成・編集
- 質問への回答
- データの解釈

**推奨モデル**:
- `google-gla:gemini-2.5-flash`（高速）
- `google-gla:gemini-2.5-pro`（高品質）

**設定例**:
```toml
[[team.members]]
agent_name = "summarizer"
agent_type = "plain"
tool_description = "テキストを要約し、重要なポイントを抽出します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたは要約の専門家です。
提供されたテキストを簡潔かつ正確に要約してください。
重要なポイントを箇条書きで整理してください。
"""
temperature = 0.2
```

### 2. `web_search` - Web検索機能付き

**説明**: Web検索ツールを持つエージェント。最新情報の取得やリサーチタスクに適しています。

**用途**:
- 最新ニュースの取得
- 特定トピックの調査
- 事実確認
- 市場調査

**推奨モデル**:
- `google-gla:gemini-2.5-flash`（Google検索統合）
- `grok:grok-4-fast`（Grok Web Search内蔵）

**設定例**:
```toml
[[team.members]]
agent_name = "web_researcher"
agent_type = "web_search"
tool_description = "Web検索を実行し、最新の情報を取得します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたはWeb検索の専門家です。

検索を行う際は以下のガイドラインに従ってください:
1. 信頼性の高い情報源を優先
2. 最新の情報を取得
3. 複数の情報源で事実確認
4. 出典URLを必ず含める
"""
temperature = 0.2
```

### 3. `code_execution` - コード実行機能付き

**説明**: Pythonコードを実行できるエージェント。計算、データ処理、スクリプト実行に適しています。

**用途**:
- 数値計算
- データ処理・変換
- グラフ・チャート生成
- ファイル操作
- API呼び出し

**推奨モデル**:
- `anthropic:claude-sonnet-4-5-20250929`（code_execution完全対応）
- `anthropic:claude-haiku-4-5`（高速、code_execution対応）

**注意**: Google/OpenAI系モデルはcode_execution非対応（`plain_compatible`のみ）

**設定例**:
```toml
[[team.members]]
agent_name = "python_coder"
agent_type = "code_execution"
tool_description = "Pythonコードを実行して計算やデータ処理を行います"
model = "anthropic:claude-sonnet-4-5-20250929"
system_instruction = """
あなたはPythonプログラマーです。

コード作成時のガイドライン:
1. 安全で効率的なコードを書く
2. エラーハンドリングを含める
3. 結果を明確に出力する
4. 必要なライブラリをインポートする

使用可能な主なライブラリ:
- pandas, numpy (データ処理)
- matplotlib, plotly (可視化)
- requests (API呼び出し)
"""
temperature = 0.0
timeout_seconds = 120
```

### 4. `web_fetch` - Webフェッチ機能付き

**説明**: 特定URLからコンテンツを取得するエージェント。既知のURLからのデータ取得に適しています。

**用途**:
- 特定ページのスクレイピング
- API呼び出し（認証不要）
- RSS/フィード取得
- ドキュメント取得

**推奨モデル**:
- `google-gla:gemini-2.5-flash`
- `anthropic:claude-haiku-4-5`

**設定例**:
```toml
[[team.members]]
agent_name = "page_fetcher"
agent_type = "web_fetch"
tool_description = "指定されたURLからWebページの内容を取得します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたはWebコンテンツ取得の専門家です。

取得時のガイドライン:
1. 指定されたURLから正確にコンテンツを取得
2. HTMLから必要な情報を抽出
3. 構造化された形式で結果を返す
4. エラー時は適切なメッセージを返す
"""
temperature = 0.1
```

### 5. `custom` - カスタムプラグイン

**説明**: 独自のツールやプラグインを統合するエージェント。MixSeekプラグインシステムと連携します。

**用途**:
- 社内システムとの連携
- 独自APIの呼び出し
- 特殊なツール統合
- 外部サービス連携

**注意**: カスタムプラグインの実装が必要です。

**設定例**:
```toml
[[team.members]]
agent_name = "slack_agent"
agent_type = "custom"
tool_description = "Slackにメッセージを送信します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたはSlack連携エージェントです。
指示に従ってSlackチャンネルにメッセージを送信してください。
"""
# カスタムプラグイン設定は別途必要
```

## タイプ選択ガイド

### 用途別推奨

| タスク | 推奨タイプ | 理由 |
|--------|-----------|------|
| テキスト要約 | `plain` | 追加ツール不要 |
| 最新ニュース取得 | `web_search` | リアルタイム情報が必要 |
| データ計算 | `code_execution` | 正確な計算が必要 |
| 特定ページ分析 | `web_fetch` | URLが既知 |
| 社内システム連携 | `custom` | 独自統合が必要 |

### 複合タスクの構成例

**リサーチ＆分析チーム**:
```
- web_researcher (web_search): 情報収集
- analyst (plain): 情報分析
- summarizer (plain): 要約作成
```

**データ処理チーム**:
```
- data_fetcher (web_fetch): データ取得
- processor (code_execution): データ処理
- reporter (plain): レポート作成
```

## モデル互換性マトリックス

| タイプ | Google | Anthropic | OpenAI | Grok | Groq | ClaudeCode |
|--------|--------|-----------|--------|------|------|------------|
| `plain` | ✓ | ✓ | ✓ | ✓ | - | - |
| `web_search` | ✓ | ✓ | ✓ | ✓ | - | - |
| `code_execution` | ✗ | ✓ | ✗ | ✗ | - | - |
| `web_fetch` | ✓ | ✓ | ✓ | ✓ | - | - |
| `custom` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `groq_plain` | - | - | - | - | ✓ | - |
| `groq_web_search` | - | - | - | - | ✓ | - |
| `tavily_search` | - | - | - | - | ✓ | - |
| `claudecode_plain` | - | - | - | - | - | ✓ |
| `claudecode_tavily_search` | - | - | - | - | - | ✓ |
| `playwright_markdown_fetch` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**注意**:
- `code_execution`はAnthropicモデルのみ完全対応
- `groq_*`タイプはGroqモデル専用
- `claudecode_*`タイプはClaudeCodeモデル専用
- `playwright_markdown_fetch`は任意のモデルで使用可能

---

## mixseek-plus 拡張タイプ

以下のエージェントタイプは**mixseek-plus**パッケージで追加された拡張機能です。mixseek-coreには含まれていません。

### 6. `groq_plain` - Groq基本テキスト生成

**説明**: Groqプロバイダーを使用した高速テキスト生成エージェント。低レイテンシが特徴です。

**用途**:
- 高速なテキスト生成
- リアルタイム応答が必要なタスク
- 大量のバッチ処理

**推奨モデル**:
- `groq:llama-3.3-70b-versatile`（汎用）
- `groq:qwen/qwen3-32b`（多言語対応）

**設定例**:
```toml
[[team.members]]
name = "fast_responder"
type = "custom"
tool_name = "quick_answer"
tool_description = "高速でテキスト応答を生成します"
model = "groq:llama-3.3-70b-versatile"

[team.members.plugin]
agent_module = "mixseek_plus.agents.groq_plain_agent"
agent_class = "GroqPlainAgent"
```

### 7. `groq_web_search` - Groq + Tavily Web検索

**説明**: GroqモデルとTavily Web検索を組み合わせたエージェント。高速なWeb検索と応答生成が可能です。

**用途**:
- リアルタイムWeb検索
- 最新情報の高速取得
- ニュース要約

**推奨モデル**:
- `groq:llama-3.3-70b-versatile`

**環境変数**: `TAVILY_API_KEY`が必要

**設定例**:
```toml
[[team.members]]
name = "fast_searcher"
type = "custom"
tool_name = "quick_search"
tool_description = "高速でWeb検索を実行し、結果を要約します"
model = "groq:llama-3.3-70b-versatile"

[team.members.plugin]
agent_module = "mixseek_plus.agents.groq_web_search_agent"
agent_class = "GroqWebSearchAgent"
```

### 8. `tavily_search` - Groq + Tavily検索（3ツール）

**説明**: Tavilyの3つの検索ツール（search, extract, qna）を統合したエージェント。より高度な検索機能を提供します。

**用途**:
- 複合的なWeb検索
- 特定URLからの情報抽出
- 質問応答形式の検索

**推奨モデル**:
- `groq:llama-3.3-70b-versatile`

**環境変数**: `TAVILY_API_KEY`が必要

**利用可能なツール**:
| ツール | 説明 |
|--------|------|
| `tavily_search` | 一般的なWeb検索 |
| `tavily_extract` | 特定URLからの情報抽出 |
| `tavily_qna` | 質問応答形式の検索 |

**設定例**:
```toml
[[team.members]]
name = "advanced_searcher"
type = "custom"
tool_name = "advanced_search"
tool_description = "高度なWeb検索と情報抽出を実行します"
model = "groq:llama-3.3-70b-versatile"

[team.members.plugin]
agent_module = "mixseek_plus.agents.tavily_search_agent"
agent_class = "TavilySearchAgent"
```

### 9. `claudecode_plain` - ClaudeCode基本エージェント

**説明**: Claude Codeをバックエンドとして使用する基本エージェント。Claude Codeの組み込みツール（ファイル操作、Bash実行等）を活用できます。

**用途**:
- ファイル操作を伴うタスク
- コード生成・編集
- システムコマンド実行

**推奨モデル**:
- `claudecode:claude-sonnet-4-5`（バランス型）
- `claudecode:claude-haiku-4-5`（高速）

**設定例**:
```toml
[[team.members]]
name = "code_assistant"
type = "custom"
tool_name = "code_helper"
tool_description = "コードの生成、編集、ファイル操作を行います"
model = "claudecode:claude-sonnet-4-5"

[team.members.plugin]
agent_module = "mixseek_plus.agents.claudecode_plain_agent"
agent_class = "ClaudeCodePlainAgent"

[team.members.metadata.tool_settings]
claudecode = { preset = "full_access" }
```

### 10. `claudecode_tavily_search` - ClaudeCode + Tavily検索

**説明**: Claude CodeバックエンドにTavily検索機能を統合したエージェント。Web検索とClaude Codeの強力な処理能力を組み合わせます。

**用途**:
- Web検索結果を使ったコード生成
- 調査とドキュメント作成の自動化
- 外部情報を参照したファイル操作

**推奨モデル**:
- `claudecode:claude-sonnet-4-5`

**環境変数**: `TAVILY_API_KEY`が必要

**設定例**:
```toml
[[team.members]]
name = "research_coder"
type = "custom"
tool_name = "research_and_code"
tool_description = "Web検索を行い、結果を基にコードやドキュメントを生成します"
model = "claudecode:claude-sonnet-4-5"

[team.members.plugin]
agent_module = "mixseek_plus.agents.claudecode_tavily_search_agent"
agent_class = "ClaudeCodeTavilySearchAgent"

[team.members.metadata.tool_settings]
claudecode = { preset = "full_access" }
```

### 11. `playwright_markdown_fetch` - Playwright + MarkItDown

**説明**: Playwrightブラウザ自動化とMarkItDownを組み合わせたWebフェッチエージェント。JavaScriptレンダリングが必要なページや、ボット対策されたサイトからのコンテンツ取得に対応します。

**用途**:
- SPAサイトからのコンテンツ取得
- ボット対策されたページのスクレイピング
- 動的コンテンツの取得
- PDFやOfficeファイルのマークダウン変換

**推奨モデル**:
- 任意のモデル（テキスト処理用）

**設定例**:
```toml
[[team.members]]
name = "browser_fetcher"
type = "custom"
tool_name = "fetch_dynamic_page"
tool_description = "JavaScriptレンダリングが必要なWebページからコンテンツを取得します"
model = "google-gla:gemini-2.5-flash"

[team.members.plugin]
agent_module = "mixseek_plus.agents.playwright_markdown_fetch_agent"
agent_class = "PlaywrightMarkdownFetchAgent"

[team.members.playwright]
headless = true
timeout_ms = 30000
wait_for_load_state = "networkidle"
retry_count = 2
retry_delay_ms = 1000
```

## mixseek-plus タイプ選択ガイド

### プロバイダー別推奨

| 要件 | 推奨タイプ | プロバイダー |
|------|-----------|-------------|
| 低レイテンシ | `groq_plain` | Groq |
| 高速Web検索 | `groq_web_search` | Groq |
| 高度な検索 | `tavily_search` | Groq |
| ファイル操作 | `claudecode_plain` | ClaudeCode |
| 検索+コード生成 | `claudecode_tavily_search` | ClaudeCode |
| 動的ページ取得 | `playwright_markdown_fetch` | 任意 |

### 複合タスク構成例

**高速リサーチチーム**:
```
- fast_searcher (groq_web_search): 高速Web検索
- analyzer (groq_plain): 結果分析
- summarizer (groq_plain): 要約作成
```

**コード生成チーム**:
```
- researcher (claudecode_tavily_search): 技術調査
- coder (claudecode_plain): コード生成
- reviewer (claudecode_plain): コードレビュー
```

**Webスクレイピングチーム**:
```
- browser_fetcher (playwright_markdown_fetch): 動的ページ取得
- static_fetcher (web_fetch): 静的ページ取得
- processor (plain): データ処理
```

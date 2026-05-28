---
name: gemini
description: |
  Use when delegating tasks to Gemini. Two execution modes:
  (1) CLI mode (default): Subagent runs gemini CLI iteratively until task complete. Progress visible, suitable for large investigations.
  (2) MCP mode: Direct MCP call for quick, single-shot queries.
  Trigger: large-scale codebase investigation, web search, log analysis, context optimization.
---

# Gemini 活用ガイド

2つの実行モードがある。タスクの性質に応じて使い分ける。

## モード選択

| 特性 | CLI モード（推奨） | MCP モード |
|------|-------------------|------------|
| 進捗表示 | リアルタイム | なし |
| 反復実行 | 自動継続 | 単発 |
| 適用場面 | 大規模調査、複雑なタスク | 簡単な質問、即座の回答 |
| 呼び出し | Task → gemini-cli-investigator | mcp__gemini-cli__ask-gemini |

---

## CLI モード（推奨）

**使用タイミング:**
- 複数ファイルにまたがる調査
- 呼び出し元・依存関係の追跡
- Web検索（複数ソースの調査）
- 長文ログの解析

**呼び出し方:**
```
Task tool で gemini-cli-investigator エージェントを起動

例:
Task(
  subagent_type: "gemini-cli-investigator",
  prompt: "henry-backend の UserService について依存関係を調査し、
           呼び出し元を全て特定してレポートを作成してください"
)
```

**特徴:**
- サブエージェントが `gemini --yolo` でCLIを反復実行
- タスク完了まで自律的に調査を続ける
- 進捗がリアルタイムで見える
- 結果は `.claude/work/gemini-reports/` に出力

---

## MCP モード（単発クエリ）

**使用タイミング:**
- 単純な質問への即座の回答
- 特定ファイルのピンポイント分析
- changeMode での編集提案取得

**呼び出し方:**
```
mcp__gemini-cli__ask-gemini(
  prompt: "@file.ts このコードの目的を説明して"
)
```

---

## レポート品質基準（両モード共通）

**必須:**
- 省略禁止: 「他にも...」「同様に...」「など」で逃げない
- 私見禁止: 推測・解釈・提案を書かない。事実のみ
- 具体性: 必ず引用元（ファイル:行番号 or URL）を付ける
- 網羅性: 発見した全件を列挙する

**禁止:**
- 「〜と思われます」「おそらく」「〜かもしれない」
- 「詳細は省略」「以下略」「多数あり」
- 「〜すべき」「〜を推奨」（私見）

---

## 出力先

```
.claude/work/gemini-reports/{トピック}-{YYYYMMDD-HHMM}.md
```

**注意:** プロジェクトルートの相対パスで保存。
`.gitignore` に追加推奨。

---

## 委託判断フロー

```
タスクを受け取る
    │
    ▼
外部の最新情報が必要？ ──Yes──▶ Web検索（CLI推奨）
    │No
    ▼
大量ファイル読み込み？ ──Yes──▶ コード調査（CLI推奨）
    │No
    ▼
単発の簡単な質問？ ──Yes──▶ MCP モード
    │No
    ▼
ユーザー対話が必要？ ──Yes──▶ Claude Code直接対応
```

---

## CLI モードの実行例

### コード調査

```
Task(
  subagent_type: "gemini-cli-investigator",
  prompt: |
    henry-backend/general-api の認証フローを調査してください。

    調査項目:
    1. 認証に関わるクラス・メソッドの一覧
    2. 呼び出しフローの図解
    3. 外部サービスとの連携箇所

    結果は .claude/gemini-reports/auth-flow-{timestamp}.md に出力
)
```

### Web検索

```
Task(
  subagent_type: "gemini-cli-investigator",
  prompt: |
    web searchを使って、Kotlin Coroutinesの最新ベストプラクティスを調査してください。

    調査項目:
    1. 公式ドキュメントの推奨パターン
    2. Spring Boot 3.x との統合方法
    3. エラーハンドリングのパターン

    結果は .claude/gemini-reports/kotlin-coroutines-{timestamp}.md に出力
)
```

---

## MCP モードの機能

### 編集提案モード
changeMode=trueで構造化された編集提案を取得。

```
mcp__gemini-cli__ask-gemini(
  prompt: "@src/api/users.ts エラーハンドリングを改善して",
  changeMode: true
)
```

### コード実行（sandbox）
sandbox=trueでコードを安全に実行。

```
mcp__gemini-cli__ask-gemini(
  prompt: "このPythonスクリプトを実行して結果を教えて",
  sandbox: true
)
```

### ブレインストーミング

```
mcp__gemini-cli__brainstorm(
  prompt: "ユーザー認証の改善案",
  domain: "software",
  ideaCount: 10
)
```

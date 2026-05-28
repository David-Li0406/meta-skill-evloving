---
name: notion-workflow
description: Guide for synchronizing local scrum artifacts with Notion. Describes manual workflow and prepares for future API integration.
---

# Notion連携ワークフロー

ローカルで作成したスクラム成果物をNotionに反映するためのガイド。
現在は手動、将来的にはNotion API/MCPで自動化を想定。

## ディレクトリ構造

```
.claude/scrum/
├── backlog/          → Notion: Product Backlog DB
├── domain/           → Notion: ドメイン知識ページ
├── adr/              → Notion: 技術ドキュメント/ADR
└── retro/            → Notion: スプリントレトロ記録
```

## 連携フロー

### 1. PBI案 → Notion Product Backlog

**方向**: ローカル → Notion

**タイミング**: リファインメント前

**手順**:
1. `/pbi-draft` でPBI案を作成
2. `.claude/scrum/backlog/draft-*.md` を開く
3. リファインメントで議論・修正
4. 確定したらNotionのProduct Backlog DBに転記

**Notion DB推奨フィールド**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| タイトル | Title | PBI名 |
| ユーザーストーリー | Text | As a... I want... So that... |
| 受け入れ基準 | Text | Gherkin形式のAC |
| ステータス | Select | Draft / Ready / In Progress / Done |
| スプリント | Relation | 対象スプリント |
| 見積もり | Number | ストーリーポイント |
| 担当者 | Person | アサイン |
| 優先度 | Select | High / Medium / Low |

**転記時のポイント**:
- Markdownの見出し・リストはそのまま貼り付け可能
- Gherkin形式のACはコードブロックで囲むと見やすい
- スコープ外はトグルで折りたたむと便利

---

### 2. Spike結果 → Notion ドメイン知識

**方向**: ローカル → Notion

**タイミング**: Spike完了後

**手順**:
1. `/spike` で調査を実施
2. `.claude/scrum/domain/*.md` を開く
3. Notionの「ドメイン知識」ページに転記

**Notionでの整理案**:
```
ドメイン知識/
├── {ドメイン領域1}/
│   ├── 基礎知識
│   └── 調査記録/
│       ├── 2026-01-18 決済ドメイン調査
│       └── ...
└── {ドメイン領域2}/
    └── ...
```

---

### 3. ADR → Notion 技術ドキュメント

**方向**: ローカル → Notion

**タイミング**: 意思決定確定後

**手順**:
1. `/adr` でADRを作成
2. `.claude/scrum/adr/*.md` を開く
3. Notionの「技術ドキュメント」または「ADR」DBに転記

**Notion DB推奨フィールド**:
| フィールド | 型 | 説明 |
|-----------|-----|------|
| ADR番号 | Number | 連番 |
| タイトル | Title | 決定事項 |
| ステータス | Select | Proposed / Accepted / Deprecated |
| 日付 | Date | 決定日 |
| 決定者 | Person | 関係者 |
| 本文 | Text | ADR本文 |

---

### 4. Notion → ローカル

**方向**: Notion → ローカル

**タイミング**: プランニング後、スプリント開始時

**用途**:
- 確定したスプリントバックログをローカルにコピー
- 作業中に参照するため

**手順**:
1. Notionから対象PBIをエクスポート（Markdown）
2. `.claude/scrum/sprint/current.md` として保存
3. 実装時に参照

---

## 将来の自動化に向けて

### Notion MCP Server

Notion APIを使ったMCP Serverが利用可能になれば:
- `/pbi-draft` → 直接Notion DBに書き込み
- Notion DB → ローカルへの自動同期
- ステータス更新の自動化

### 準備事項

1. **Notion Integration作成**
   - Internal Integration として作成
   - 対象DBへのアクセス権限付与

2. **トークン管理**
   - 1Password CLI経由で管理
   - `op://vault/Notion Integration/credential`

3. **MCP設定（将来）**
   ```json
   {
     "mcpServers": {
       "notion": {
         "command": "npx",
         "args": ["@notionhq/notion-mcp-server"],
         "env": {
           "NOTION_TOKEN": "op://vault/Notion Integration/credential"
         }
       }
     }
   }
   ```

---

## Tips

### Markdownの整形

Notionに貼り付ける際、以下の変換が必要な場合がある:

| ローカル | Notion |
|---------|--------|
| `- [ ]` | チェックボックスとして認識される |
| `###` | Heading 3 として認識される |
| ` ``` ` | コードブロックとして認識される |
| `> ` | 引用ブロックとして認識される |

### 画像・図の扱い

- ローカルではテキストで記述
- Notionでは必要に応じて図を追加
- Mermaid記法はNotionの埋め込みで対応

### 差分管理

- ローカルはGit管理可能
- Notionは履歴機能あり
- 「正」はNotion、ローカルは作業用と割り切る

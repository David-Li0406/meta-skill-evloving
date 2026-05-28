# cga-skills-update 詳細ガイド

## 概要

コード変更や会話から再利用可能なパターンを抽出し、Claude Code の拡張機能（Skills / CLAUDE.md / Hooks / Subagents）として適切な形で蓄積する。

**対象**: `.claude/skills/`, `.claude/agents/`, `CLAUDE.md`
**対象外**: `doc/domain/`, `doc/decisions/`（`cga-docs-update` で対応）

## 拡張機能の使い分け

知見を蓄積する前に、適切な拡張方法を選択する:

| 拡張方法 | 用途 | 読み込み | 例 |
|----------|------|----------|-----|
| **CLAUDE.md** | 全セッションで常に必要なルール | 毎回自動 | コーディング規約、ビルドコマンド |
| **Skills** | 特定の作業時にのみ必要な知見 | オンデマンド | TDDワークフロー、リファクタリングパターン |
| **Hooks** | 例外なく毎回実行すべきアクション | 自動実行 | lint実行、migration確認 |
| **Subagents** | 独立したコンテキストで実行する専門タスク | 明示的委譲 | セキュリティレビュー、コードレビュー |

### 判断フローチャート

```text
知見を蓄積したい
  │
  ├─ 全セッションで必要？ → CLAUDE.md に追記
  │
  ├─ 例外なく自動実行？ → Hooks で設定
  │
  ├─ 独立コンテキストで実行？ → Subagents を定義
  │
  └─ 特定作業時に必要？ → Skills として作成
```

## 情報源

### 1. 会話コンテキスト

現在のセッションで得られた知見:
- 実装中に発見した非自明なパターン
- トラブルシューティングで学んだ解決策
- ユーザーとのやり取りで明確になった設計方針

### 2. git diff main..HEAD

```bash
git diff main..HEAD --stat
git diff main..HEAD -- src/
git diff main..HEAD -- .claude/
```

## 実行フロー

### Step 1: 差分分析

```bash
# 変更ファイル一覧
git diff main..HEAD --stat

# 新規追加ファイル
git diff main..HEAD --name-only --diff-filter=A

# 変更されたスキル（既に更新済みか確認）
git diff main..HEAD -- .claude/skills/
```

### Step 2: パターン抽出と品質判定

#### 抽出基準: スキル化すべきパターン

以下の**すべて**を満たすもの:

1. **非自明性**: Claude がコードを読んだだけでは推測できない知見
2. **再現性**: 同じ状況が今後確実に発生する（「3回使いそう」ではなく「次に同じ状況が来たら間違える」）
3. **失敗コスト**: この知見がないと実装ミスや手戻りが発生する

#### 品質テスト

各行に対して問う: **「これを削除したら Claude が間違えるか？」**

- Yes → 残す
- No → 削除するか、CLAUDE.md の1行ルールで十分

#### スキル化しない

- 標準的なパターン（TypeScript/Express/Prisma の一般知識）
- 1回限りの実装詳細
- コードを読めば自明なこと
- 外部ドキュメントへのリンクで十分なこと

### Step 3: スキルファイルの品質ルール

#### SKILL.md は簡潔に

SKILL.md が長すぎると重要なルールが埋もれる。以下を守る:

- **description**: 1行で「何をするか」を説明
- **いつ使うか**: トリガー条件を箇条書き（3-5項目）
- **何をするか**: 手順を番号付きリスト（5-7ステップ以内）
- **基本ルール**: 守るべき制約（3-5項目）
- 詳細は guide.md に分離

#### guide.md の構成

- 概要（1-2文）
- 具体的なコード例（コピペ可能なもの）
- 判断基準（テーブルや条件分岐で表現）
- アンチパターン（やってはいけないこと）

#### アンチパターン: 肥大化したスキル

```markdown
# ❌ Bad: 自明なことを書いている
- TypeScriptでは型を付ける
- テストを書く
- エラーハンドリングをする

# ✅ Good: プロジェクト固有の非自明な知見
- ZodErrorは mapZodErrorToCreateOrderError() でドメインエラーに変換する
- Repository層では Prisma の型をドメイン型に変換して返す（Prisma型を外に漏らさない）
- テストでは PrismaClient のインメモリSQLiteを使い、beforeEach で migrate reset する
```

### Step 4: 提案生成

```markdown
## スキル更新提案

### 変更サマリ

| 種別 | 対象 | 内容 |
|------|------|------|
| 新規 | `.claude/skills/cga-{name}/` | {理由} |
| 更新 | `.claude/skills/cga-{name}/guide.md` | {更新箇所} |
| 移動 | CLAUDE.md → Skills | {移動理由} |
| 削除 | `.claude/skills/cga-{name}/` 内の{行} | {自明なため不要} |

### 詳細

{各提案の根拠と具体的な変更内容}

---

実行しますか？
```

### Step 5: ユーザー確認

AskUserQuestion で確認:
- 全て更新
- 選択的に更新
- 更新しない

### Step 6: 更新実行と検証

確認後、Edit/Write ツールで更新を実行。

更新後のセルフチェック:
- [ ] SKILL.md は60行以内か
- [ ] guide.md に自明な記述はないか
- [ ] コード例はコピペで動くか
- [ ] 既存スキルと矛盾していないか

## スキルファイル構造

```text
.claude/skills/
└── cga-{skill-name}/
    ├── SKILL.md      # メタ情報（簡潔に）
    ├── guide.md      # 詳細ガイド、コード例
    └── (patterns.md) # パターン集（必要な場合のみ）
```

### SKILL.md テンプレート

```markdown
---
name: {skill-name}
description: {1行: 動詞で始まる説明}
allowed-tools: Read Glob Grep Edit Write Bash AskUserQuestion
---

## いつ使うか

- {トリガー条件: 具体的な状況}

## いつ使わないか

- {代わりに使うべきスキルとその条件}

## 何をするか

1. {ステップ: 動詞で始める}
2. {ステップ}
3. {ステップ}

## 基本ルール

- {プロジェクト固有の非自明なルール}

## 使用例

\`\`\`text
/{skill-name} {典型的な引数}
\`\`\`

## 詳細

[guide.md](guide.md) を参照
```

## 変更パスとスキルのマッピング

| 変更パス | 関連スキル | 確認観点 |
|----------|------------|----------|
| `src/*/usecases/` | `cga-programming` | ユースケースパターン |
| `src/*/controllers/` | `cga-programming` | コントローラパターン |
| `src/*/validators/` | `cga-programming` | バリデーションパターン |
| `src/*/models/` | `cga-programming` | ドメインモデル |
| `src/*/repositories/` | `cga-programming` | リポジトリパターン |
| `src/infrastructure/prisma/` | `cga-prisma-migration` | スキーマ変更 |
| `src/shared/errors/` | `cga-programming` | エラーハンドリング |
| `*.test.ts` | `cga-programming` | テストパターン |
| `.claude/skills/` | (自己参照) | スキル間整合性 |
| `.claude/agents/` | (自己参照) | サブエージェント定義 |
| `CLAUDE.md` | (自己参照) | ルールの配置適切性 |

## CLAUDE.md の管理指針

CLAUDE.md を更新する場合の判断基準:

**CLAUDE.md に入れるべき**:
- Bash コマンドで Claude が推測できないもの
- デフォルトと異なるコードスタイルルール
- テスト実行方法やテストランナー設定
- リポジトリ固有のワークフロー（ブランチ命名、PR規約）
- 開発環境の癖（必要な環境変数など）

**CLAUDE.md から外すべき**:
- コードを読めば分かること
- 言語標準の慣習（Claude が既に知っていること）
- 頻繁に変わる情報
- 長い説明やチュートリアル（→ Skills に移動）
- ファイルごとの説明

## 基本ルール

- **読み取り優先**: まず分析し、変更は確認後に行う
- **簡潔さ最優先**: 肥大化したスキルは無視される
- **品質テスト適用**: 「削除したら間違えるか？」を全行に問う
- **コード変更しない**: スキル/設定ファイルのみ対象
- **既存スタイル維持**: 周囲のスキルのトーンと構造に合わせる
- **定期プルーニング**: 守られていないルールは表現を変えるか削除

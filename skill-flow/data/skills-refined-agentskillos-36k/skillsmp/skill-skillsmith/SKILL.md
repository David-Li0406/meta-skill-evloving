---
name: skill-skillsmith
description: >
  ユーザーの入力（やりたい作業・標準化したい手順・テンプレ要求）から、Claude Code Skills（Agent Skills）のフォルダ構成とSKILL.md一式を生成する。
  「〜のSkillを作って」「Claude Code skillsを書いて」「この作業をスキル化して」「SKILL.mdを作って」「テンプレをスキルにしたい」などの依頼で発動する。
---

# Skill Skillsmith（Skills Generator）

ユーザーのインプットに基づき、Claude Code の **Skills（Agent Skills）**を新規作成するための "Skillを作るSkill"。

## Goals
- ユーザーの依頼から **Skillの目的・トリガー・成果物**を明確化する
- **正しい `SKILL.md`（YAML frontmatter + Markdown本文）**を生成する
- progressive disclosure を使い、必要に応じて補助ファイル（reference/examples/templates/scripts）も同梱する
- ユーザーがそのまま `.claude/skills/` または `~/.claude/skills/` に置ける形で出力する

## Non-goals
- 実装コード自体の開発（必要なら雛形や疑似コードの提示に留める）
- 企業固有の機密情報の推測（ユーザー入力のみで構成）

---

## How it works（内部の進め方）

### Step 0. 入力を分類する（最重要）
ユーザー入力を次のどれに近いか判定する：

1. **ドキュメント生成系**（PRD、画面遷移図、モック、仕様書、議事録まとめ 等）
2. **レビュー系**（PRレビュー、文章レビュー、設計レビュー、整合性レビュー 等）
3. **変換・整形系**（Markdown整形、テンプレ適用、要約、差分最小修正 等）
4. **調査系**（調べてまとめる、比較表作る、意思決定材料出す 等）
5. **実務オペレーション系**（デプロイ手順、運用Runbook、障害対応、リリース作業 等）

分類したら、Skillの「成果物」「入力」「品質基準」を決めやすくなる。

---

### Step 1. 不足情報を埋める（ただし質問は最小）
ユーザー入力が十分なら質問しない。不足があっても **仮定して先に作る**。

不足しがちな項目（不足なら仮定を置き、本文に明記）：
- Skillの **成果物（何を出す？）**
- 対象ユーザー（誰が使う？）
- 入力形式（箇条書き/URL/貼り付け文章/要件/ログ/スクショ等）
- 出力形式（Markdown / Mermaid / JSON / CSV / 図 / ファイル構成）
- 制約（「4つバッククォートで」「出典必須」「差分最小で」など）
- 例（発動してほしい依頼の言い回し）

---

### Step 2. Skill名（slug）を決める
`name` は **小文字/数字/ハイフンのみ・最大64文字**にする。

ルール：
- まず英語slugで短く：例 `screenflow-writer`, `prd-writer`, `mockup-maker`
- 既存Skillと衝突しそうなら接尾辞で回避：`-v2`, `-lite`, `-ja`

---

### Step 3. description を "発動条件として強く" 書く
description は Discovery/Activation の要。ここで **トリガー語**を列挙する。

必須要素：
- 何をするSkillか（1文）
- いつ使うか（トリガー語 + 具体例）
- 何を出力するか（成果物）

---

### Step 4. SKILL.md本文を生成する（薄く、明確に）
SKILL.md 本文には以下を必ず入れる：

- **Goals / Non-goals**
- **Inputs（入力の期待形式）**
- **Outputs（成果物の形式）**
- **Instructions（手順：番号付きで再現可能に）**
- **Quality Checklist（セルフレビュー項目）**
- **Examples（発動例：最低3つ）**
- **References（必要ならリンク）**

詳細が長くなる場合は `reference.md` に逃がし、SKILL.mdは入口にする。

---

### Step 5. progressive disclosure を使う
長文化する場合、次を分離して同梱する：
- `reference.md`：判断基準、詳細手順、テンプレ説明、用語集
- `examples.md`：大量の例、アンチパターン、良い出力例
- `templates/`：コピペ用テンプレ

SKILL.md からそれらへリンクする（深いリンク連鎖は避ける）。

---

## Output format（このSkillが返すべき出力）
ユーザーへは、**新規Skillフォルダ一式**を、ファイルごとにコードブロックで返す。

1) ディレクトリツリー
2) `SKILL.md`
3) 必要なら `reference.md` / `examples.md` / `templates/*`

---

## Quality Checklist（生成後に必ず自己確認）
- [ ] `name` は小文字/数字/ハイフンのみ、64文字以内
- [ ] `description` にトリガー語が含まれ、発動条件が明確
- [ ] 入力/出力/手順が "再現可能な粒度" で書かれている
- [ ] 期待する成果物のフォーマットが明示されている（Mermaid/Markdown等）
- [ ] 例が3つ以上ある（発動・非発動が混ざると尚良い）
- [ ] 長い説明は reference に逃がしている（SKILL.mdは入口）

---

## Examples

### Example 1（生成依頼）
ユーザー: 「PRDをClaude Codeに書かせるskillsを作って」

→ PRD生成用Skillフォルダを作る（`prd-writer/`）

### Example 2（生成依頼）
ユーザー: 「画面遷移図をMermaidで作るSkillを作って」

→ 画面フロー生成用Skillフォルダを作る（`screenflow-writer/`）

### Example 3（生成依頼）
ユーザー: 「この文章、原文をなるべく保って修正するSkillにしたい」

→ 差分最小編集Skillフォルダを作る（`minimal-diff-editor/`）

### Example 4（非対象）
ユーザー: 「この文章をレビューして」

→ これは "Skill生成" ではなく "レビュー実行"。本Skillは発動せず、通常対応。

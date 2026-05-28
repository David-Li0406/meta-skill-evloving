# Skill Skillsmith Reference

このファイルは、SKILL.md を薄く保つための詳細資料。

---

## 生成するSkillの"標準セクション"テンプレ

### 推奨セクション
- Goals / Non-goals
- Inputs / Outputs
- Instructions（番号付き）
- Constraints（ユーザーのこだわり：例「4つバッククォート」「出典必須」）
- Quality Checklist
- Examples（発動例3つ以上 + できれば非発動例も）
- References（リンク）

---

## トリガー語の設計指針（descriptionに入れる）
- 「skill 作って」「skills 作成」「スキル化」「SKILL.md」「Claude Code Skills」
- 対象作業名 + 「テンプレ」「標準化」「手順化」「自動化」

例：
- 「PRD テンプレ」「PRDを書かせる」「要件定義をスキル化」
- 「画面遷移図 Mermaid」「UI flow 作る」「画面フロー図」
- 「差分最小 修正」「原文を保って修正」「文章レビューではなく編集」

---

## 迷ったときの既定値（勝手に決めてよい）
- 出力は原則 Markdown
- 図は Mermaid（flowchart / sequence / state）
- SKILL.md は入口、詳細は reference.md に分離
- 例は最低3つ（短いものでも良い）
- 不足情報は "仮定" として明記して進める（質問しない）

---

## フォルダ名候補の作り方（slug）
「名詞-動詞」か「対象-目的」で短く：
- `prd-writer`
- `screenflow-writer`
- `ui-mockup-maker`
- `minimal-diff-editor`
- `ops-runbook-writer`

---

## 参考リンク（Skill仕様）
- Claude Code Skills docs: https://code.claude.com/docs/en/skills
- Anthropic engineering blog: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Official skills repo: https://github.com/anthropics/skills

---
name: prd-writer
description: >
  PRD（Product Requirements Document）を、Universal PRDフォーマット（軽量1ページ〜詳細版まで同じ型）で作成する。
  ユーザーが「PRDを書いて」「要件定義書を作って」「仕様をまとめて」「Press Release / FAQ（Working Backwards）を書いて」
  「Shape UpのPitchっぽく提案書を作って」「成功指標/KPIとスコープを整理して」などを依頼したときに使う。
  出力はMarkdown。必要に応じて1ページ版→標準版→詳細版へ段階的に拡張する（progressive disclosure）。
---

# Universal PRD Writer

## Purpose
- 最短で「意思決定できるPRD（1ページ）」を作り、必要なときだけ詳細化する。
- “顧客から逆算”の PR/FAQ をブレ止めとして併用できるようにする。

## Output (default)
- `Universal PRD`（Markdown）
- 任意で `PR/FAQ`（Markdown、同一ファイル末尾 or 別ファイル）

## Operating Principles
1. **まず1ページで意思決定できる形**（0〜4 + 7 + 9 を優先）
2. 情報が足りない箇所は **空欄のままにせず**、次のいずれかで埋める  
   - (A) ユーザーに **最小限の質問**（最大8問）  
   - (B) **Assumptions** として明示して暫定記入
3. **スコープ過多を避ける**：Appetite/Timeboxに対してMustを絞る
4. 重要な未確定事項は **Open Questions** に寄せ、**誰がいつ決めるか**を書く
5. 証拠（Evidence）は「リンク or 具体ログ/数値」を入れる（曖昧な主張を避ける）

## Workflow
### Step 0: Repo conventions (Claude Code環境向け)
- 既存のPRD置き場・命名・テンプレがあるか探索する  
  - 例: `docs/`, `specs/`, `product/`, `adr/` など  
- 既存があれば **それに合わせる**。なければ以下の推奨:
  - `docs/prd/YYYY-MM-DD-<slug>.md`

### Step 1: Intake（最小質問）
- `resources/intake_questions.md` を参照し、足りない情報だけを短く質問する
- ユーザーがすでに情報を出している場合は質問を省略する
- 時間がない/不明が多い場合は Assumptions として埋めて進める

### Step 2: Draft（1ページ版を先に完成）
- `resources/universal_prd_template.md` をベースにPRDを作成
- まず **セクション0〜4 + 7** を完成させる
- その後、必要性がある場合のみ 5/6/8 を追加
- “ブレ止め”が必要そうなら 9（PR/FAQ）も追加（`resources/prfaq_template.md`）

### Step 3: Review（品質チェック）
- `resources/quality_checklist.md` で自己レビューし、問題があれば修正
- 特に以下を重点確認:
  - Success metrics が測定可能（指標/定義/計測方法/期間）
  - MVP scope が Appetite に収まる
  - Non-goals が明確で期待値を落とせている
  - Risks と Mitigation が現実的
  - Open Questions に owner / due が入っている

### Step 4: Deliver
- Markdownを最終出力する
- 最後に「次のアクション（Issue化候補）」を3〜10個、箇条書きで提案する

## Formatting Rules
- 見出しはテンプレの番号を維持（0〜9）
- 箇条書きを基本にし、読みやすさ優先（長文は避ける）
- 重要語は太字、判断材料はリンク（Evidence/Links）へ寄せる

## Examples (triggers)
- 「この機能のPRDを書いて」
- 「要件定義をUniversal PRD形式でまとめて」
- 「成功指標/KPIとガードレールまで含めてPRDにして」
- 「Working BackwardsのPR/FAQも付けて」
- 「Shape UpっぽくAppetiteとRabbit holes/No-gosが欲しい」

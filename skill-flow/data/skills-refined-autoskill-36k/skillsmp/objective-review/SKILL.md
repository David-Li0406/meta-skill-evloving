---
name: objective-review
description: Replaces the quality management task of strictly auditing set objectives to eliminate defects and risks before execution. Typical use cases: (1) Physical consistency checks against the current file structure and code implementation, (2) Scrutinizing objectives against SMART criteria (specificity, measurability, feasibility, etc.), (3) Proposing improvements and encouraging re-setting of objectives towards more reliable steps.
---

# 目標レビュー (Objective Review)

設定された目標（案）を厳格に監査し、実行前に欠陥を排除するためのスキル。

## プロセス (Process)

以下のチェックリストを用いて厳密な監査を行う。
**各チェック項目ごとに、改善すべき点があればその場で「具体的かつ詳細な改善提案」を可能な限り多く列挙する。**

### 1. 前提知識の監査 (Context Audit)

`objective-analysis` スキルと同様に最新のSSOTやコードを確認し、矛盾がないか突き合わせる。

- [ ] **事実との整合性:** 目標が前提としているファイル構成やコードの実装は、現時点の `ls` や `read_file` の結果と完全に一致しているか？
  - **改善提案:** (例: ファイルパスが誤っているため `src/app.py` に修正する。 / 関数 `foo` は存在しないため `bar` を使用する。)
- [ ] **SSOTとの整合性:** 承認済みのADRや仕様書（`docs/`, `reqs/`）で禁止・規定されている内容に違反していないか？
  - **改善提案:**
- [ ] **用語の正確性:** プロジェクトで定義されていない用語や、存在しないファイル名を勝手に使用していないか？
  - **改善提案:**

### 2. SMART基準の監査 (SMART Audit)

`objective-setting` で定義された基準に対し、各項目を厳しくチェックする。

- [ ] **Specific (具体性):**
  - ツールとパラメータは具体的か？曖昧さはゼロか？
  - 対象ファイルのパスや、変更前後の文字列は一意に特定されているか？
  - **改善提案:** (例: `replace` の `old_string` が短すぎて誤爆するリスクがあるため、前後3行を含めて指定する。)
- [ ] **Measurable (計量性):**
  - コマンド（`pytest`, `grep`, `ls` 等）による検証手順が含まれているか？
  - 「成功」と「失敗」の判定基準が明確か？
  - **改善提案:**
- [ ] **Achievable (達成可能性):**
  - 必要な情報は**全て**メモリ内にあるか？
  - 未知の情報がある場合、目標は「実装」ではなく「調査」に設定されているか？
  - **改善提案:**
- [ ] **Relevant (関連性):**
  - ユーザーの要求（Core Intent）に対して過不足はないか？
  - **改善提案:**
- [ ] **Time-boxed (期限):**
  - 全ステップが1回の応答ターン内で確実に完了するか？
  - **改善提案:**

### 3. レビュー結果の提示 (Presentation)

各項目で列挙された改善提案の中から、**「改善することで抜け・漏れ・無理・無駄が確実に小さくなる」** 価値ある指摘を厳選し、最終的なレビュー結果として提示する。

- **価値のある指摘と改善案がある場合:**
  `activate_skill{name: "objective-setting"}` を実行し、目標を修正する。
- **価値のある指摘が無い場合:**
  完了とする。

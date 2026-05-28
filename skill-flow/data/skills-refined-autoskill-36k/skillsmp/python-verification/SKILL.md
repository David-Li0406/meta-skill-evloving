---
name: python-verification
description: Replaces the task of serving as a quality gate to guarantee Python code quality through static analysis and testing. Typical use cases: (1) Confirming type safety (Mypy) and style checks (Ruff) during new feature implementation, (2) Fixing test failures through efficient debugging workflows (lf, pdb, etc.), (3) Automating final quality assurance checks before PR creation or commits.
---

# Pythonにおける静的解析とテスト

コードの品質を保証するため、以下の手順でチェックを実行する。

## 1. Linterと型チェック (事前)

まず、Linterと型チェッカーを実行し、問題を修正する。
`run_shell_command{command: "ruff check . && ruff format ."}`
`run_shell_command{command: "mypy ."}`

## 2. 自動テストとデバッグ

次に、自動テストを実行する。テストが失敗した場合は、以下のワークフローで効率的に修正と確認を行う。

1. **失敗箇所の特定:**
   まず `-v` オプションをつけて実行し、どのテストが失敗しているか把握する。
   `run_shell_command{command: "pytest -v"}`
2. **失敗テストへの集中:**
   前回失敗したテストのみを対象に実行し、確認サイクルを高速化する。
   `run_shell_command{command: "pytest --lf"}`
3. **詳細なデバッグ:**
   `-s` (print文の表示) や `--pdb` (対話的デバッガの起動) と組み合わせて原因を調査する。
   `run_shell_command{command: "pytest --lf -s"}` または `run_shell_command{command: "pytest --lf --pdb"}`
4. **修正と再実行:**
   コードを修正し、`run_shell_command{command: "pytest --lf"}` で素早く確認する。
5. **最終確認:**
   失敗したテストがすべて通ったら、最後に全テスト (`run_shell_command{command: "pytest"}`) を実行して他に影響がないか確認する。

## 3. Linterと型チェック (事後)

自動テストの修正が他の問題を引き起こしていないか確認するため、再度Linterと型チェックを実行する。
`run_shell_command{command: "ruff check . && ruff format ."}`
`run_shell_command{command: "mypy ."}`

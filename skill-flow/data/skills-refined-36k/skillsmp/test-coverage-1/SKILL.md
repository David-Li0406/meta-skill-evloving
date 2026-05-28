---
name: test-coverage
description: テストカバレッジを分析して不足部分のテスト生成と改善提案
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# /test-coverage - テストカバレッジ分析と改善

## 目的
現在のテストカバレッジを分析し、不足している部分のテストを生成または提案します。

## 動作
1. カバレッジ測定:
   - プロジェクトタイプに応じたツールを実行
   - Python: `pytest --cov`
   - JavaScript: `jest --coverage` または `nyc`
   - Go: `go test -cover`

2. カバレッジ分析:
   - ファイル別カバレッジ率
   - 関数/メソッド別カバレッジ
   - 分岐カバレッジ
   - カバーされていない行の特定

3. 優先度付け:
   - Critical: publicな関数でカバレッジ0%
   - Important: エラーハンドリングが未テスト
   - Nice to have: privateな補助関数

4. テスト生成/提案:
   - 不足しているテストケースを特定
   - エッジケースのテストを提案
   - 基本的なテストコードを生成

5. レポート出力:
   ```
   Test Coverage Report
   ========================
   Overall Coverage: 72.3%

   Critical Gaps:
   - src/auth/login.js: authenticate() - 0% coverage
   - src/api/payment.js: processPayment() - 12% coverage

   Suggested Test Cases:
   1. Test null/undefined inputs
   2. Test boundary conditions
   3. Test error scenarios
   ```

## 使用例
```
/test-coverage
```

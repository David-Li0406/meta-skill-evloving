---
name: code-refactor-tdd
description: Use this skill when you need to improve code quality while maintaining tests, especially during the refactoring phase of development.
---

# Refactor Code with TDD

コードをリファクタリングし、テストを維持しながらコード品質を改善する。

## Refactoring Guidelines

1. **可読性向上**: 命名改善、関数分割、構造整理
2. **重複排除**: DRY原則の適用
3. **シンプル化**: 不要な複雑さの除去

## Progress Checklist

コピーして進捗を追跡:

```
REFACTOR Progress:
- [ ] 最新Cycle doc確認
- [ ] 現在のテストが全てPASSすることを確認
- [ ] リファクタリング実施
- [ ] テスト実行→成功確認
- [ ] Cycle doc更新
- [ ] REVIEWフェーズへ誘導
```

## Workflow

### Step 1: Cycle doc確認

```bash
ls -t docs/cycles/*.md 2>/dev/null | head -1
```

### Step 2: テスト確認

```bash
php artisan test  # PHP
pytest            # Python
```

全テストがPASSすることを確認してから開始。

### Step 3: リファクタリング

| 項目 | 例 |
|------|-----|
| DRY | 重複コードの共通化 |
| 定数化 | マジックナンバー除去 |
| メソッド分割 | 長いメソッドの分割 |
| ネーミング | 変数・メソッド名の改善 |

### Step 4: テスト実行→成功確認

**期待**: 全テストが**成功**すること

### Verification Gate

| チェック | 条件 | 判定 |
|----------|------|------|
| テスト | 全PASS | 必須 |
| 静的解析 | エラー0 | 必須 |
| フォーマット | 適用済み | 必須 |

全て通過 → REVIEWへ自動進行。失敗時は修正して再試行。

## 注意事項

- 動作を変えない（振る舞いの保持）
- 一度に大きく変えすぎない
- 変更理由を説明

## 出力

リファクタリング前後の比較と、変更理由を説明する。

```
================================================================================
REFACTOR完了
================================================================================
コード品質を改善しました。テストは全てPASS。
次: REVIEWフェーズ（品質検証）
================================================================================
```

## Reference

- 詳細: [reference.md](reference.md)
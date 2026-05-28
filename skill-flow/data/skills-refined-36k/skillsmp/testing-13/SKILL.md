---
name: testing
description: Write and run tests using Vitest. Understand linting and formatting with Biome. Apply testing patterns for components, utilities, and Server Actions.
metadata:
  author: Bingify
  version: "1.0"
---

# Testing & Code Quality

このスキルは、Bingifyプロジェクトのテスト戦略とコード品質管理をカバーします。

## 概要

BingifyはVitestでテストを実行し、Biomeでリント・フォーマットを管理します。

## テストファイルの配置

テストファイルは以下のパターンで配置：

```
lib/
  utils.ts
  __tests__/
    utils.test.ts
```

## テストの作成

```typescript
import { describe, it, expect } from "vitest";
import { formatDate } from "../utils";

describe("ユーティリティ関数", () => {
  it("日付を正しくフォーマットする", () => {
    const date = new Date("2026-01-11");
    const result = formatDate(date, "YYYY-MM-DD");
    expect(result).toBe("2026-01-11");
  });
});
```

## テスト実行

```bash
# すべてのテスト
pnpm test

# ウォッチモード
pnpm test -- --watch

# カバレッジ
pnpm test -- --coverage
```

## 参考

- [Vitest公式ドキュメント](https://vitest.dev/)
- [Biomejs公式ドキュメント](https://biomejs.dev/)
- [github-workflow スキル](../github-workflow/SKILL.md) - CI/CDチェックの詳細

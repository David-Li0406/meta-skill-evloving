---
name: coding-standards
description: |
  このスキルは、ユーザーが「コーディング規約」「命名規則」「ファイル構成」「コードスタイル」「フォーマット」「lint」について質問したとき、またはコード実装時にこれらの規約を適用する必要があるときに使用する。
---

# Coding Standards

## 命名規約

### 変数・関数

- **camelCase**: 変数、関数、メソッド
- **例**: `getUserById`, `isActive`, `handleClick`

### クラス・型・インターフェース

- **PascalCase**: クラス、型、インターフェース、コンポーネント
- **例**: `UserService`, `ClientRepository`, `ButtonProps`

### 定数

- **UPPER_SNAKE_CASE**: 定数、環境変数
- **例**: `MAX_RETRY_COUNT`, `API_BASE_URL`

### ファイル・ディレクトリ

- **kebab-case**: ファイル名、ディレクトリ名
- **例**: `user-service.ts`, `client-repository.ts`

## ファイル構成

### サイズ制限

- **推奨**: 200-400 行/ファイル
- **最大**: 500 行を超えたら分割を検討
- **関数**: 50 行以下を推奨

### インポート順序

```typescript
// 1. 外部ライブラリ
import React from "react";
import { useRouter } from "next/navigation";

// 2. 内部モジュール（絶対パス）
import { Button } from "@/shared/ui";
import { useAuth } from "@/features/auth";

// 3. 相対パス
import { helper } from "./utils";
import type { Props } from "./types";
```

## コードスタイル

### イミュータビリティ

```typescript
// ✅ 良い例
const newArray = [...array, newItem];
const newObject = { ...object, key: newValue };

// ❌ 悪い例
array.push(newItem);
object.key = newValue;
```

### 早期リターン

```typescript
// ✅ 良い例
function process(data: Data | null) {
  if (!data) return null;
  if (!data.isValid) return null;

  return transform(data);
}

// ❌ 悪い例
function process(data: Data | null) {
  if (data) {
    if (data.isValid) {
      return transform(data);
    }
  }
  return null;
}
```

### 三項演算子

```typescript
// ✅ 単純な場合のみ
const status = isActive ? "active" : "inactive";

// ❌ 複雑な場合は if 文を使用
const result = condition1 ? value1 : condition2 ? value2 : value3;
```

## TypeScript

### any の禁止

```typescript
// ✅ 良い例
function parse(data: unknown): User {
  // 型ガード使用
}

// ❌ 悪い例
function parse(data: any): User {
  // 型安全性なし
}
```

### 明示的な戻り値の型

```typescript
// ✅ 良い例
function getUser(id: string): Promise<User | null> {
  // ...
}

// ❌ 悪い例
function getUser(id: string) {
  // 推論に依存
}
```

## ハードコーディング禁止

### マジックナンバー

```typescript
// ✅ 良い例
const MAX_RETRY_COUNT = 3;
const TIMEOUT_MS = 5000;

// ❌ 悪い例
if (retryCount > 3) {
}
setTimeout(callback, 5000);
```

### 設定値

```typescript
// ✅ 良い例
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// ❌ 悪い例
const apiUrl = "https://api.example.com";
```

# {機能名} 実装設計

## 設計方針

{採用するアーキテクチャパターンや設計の基本方針を記述}
{なぜこの設計を選んだのか、主要な判断基準を簡潔に}

## システム図

### 状態マシン / フロー図

```
{状態遷移やメイン処理フローをASCII図で記述}
{すべてのパス・分岐・エッジケースを可視化}

例:
    入力
      │
      ▼
┌─────────────┐
│  STATE_A    │─── 条件1 ───▶ STATE_B
└─────────────┘                  │
      │                          │
   条件2                      条件3
      │                          │
      ▼                          ▼
┌─────────────┐           ┌─────────────┐
│  STATE_C    │           │  STATE_D    │
│ (処理内容)  │           │ (処理内容)  │
└─────────────┘           └─────────────┘
```

### データフロー

```
{コンポーネント間のデータの流れを記述}

例:
User Input
    ↓
Component A
    ↓
├─ Service B (API呼び出し)
│      ↓
│  External API
│      ↓
└─ State Store
    ↓
UI Update
```

## フォルダ構造

### 現在実装済み

```
src/
└── feature/
    ├── models/
    │   └── ...
    └── services/
        └── ...
```

### 将来的な構造

```
src/
├── feature/
│   ├── models/
│   ├── services/
│   └── utils/
└── shared/
    └── ...
```

## 主要コンポーネントの設計

### 1. コンポーネントA

#### 1.1 基本実装

```
// src/feature/models/component-a.{ext}

// 型定義
type ComponentA = {
  // ...
}

// ファクトリ関数
function createComponentA(value) {
  // 生成ロジック
}

// パース関数
function parseComponentA(input) {
  // パースロジック
}
```

#### 1.2 ユーティリティ関数

```
// 補助的な関数群

// バリデーション
function validateComponentA(value) {
  // バリデーション
}

// 変換処理
function transformComponentA(value) {
  // 変換処理
}
```

### 2. コンポーネントB

```
// src/feature/models/component-b.{ext}

type ComponentB = {
  // ...
}

// 実装
```

## 利点

1. **メリット1**: 具体的な利点の説明
2. **メリット2**: 具体的な利点の説明
3. **メリット3**: 具体的な利点の説明

## 使用例

```
// 基本的な使い方
import { ComponentA } from "./models/component-a"

const instance = createComponentA("value")
const parsed = parseComponentA("input")

// 実際の利用シーン
if (parsed) {
  // 処理
}
```

## 実装状態

### 実装済み

- **Task 1**: 機能名
  - サブタスク1
  - サブタスク2

### 未実装

- **Task 2**: 機能名
  - サブタスク1
  - サブタスク2
- **Task 3**: 機能名

## 移行計画

1. **Phase 1**: 基本実装
2. **Phase 2**: 既存コードの移行
3. **Phase 3**: テストとドキュメント化
4. **Phase 4**: 最適化とクリーンアップ

## 技術的な詳細

### エラーハンドリング

- エラーケース1: 対処法
- エラーケース2: 対処法

### パフォーマンス考慮

- 考慮点1
- 考慮点2

## 参考資料

- {関連ドキュメント}
- {技術記事}

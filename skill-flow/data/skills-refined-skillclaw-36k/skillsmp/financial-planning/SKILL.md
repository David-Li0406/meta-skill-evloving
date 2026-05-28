---
name: financial-planning
description: 財務計画計算機プロジェクトの開発支援。Next.js/TypeScript フロントエンドと Go/Gin バックエンドの開発、DDD アーキテクチャ、金融計算ロジックの実装時に使用。
---

# 財務計画計算機

日本向けの財務計画・資産シミュレーションWebアプリケーション。

## プロジェクト概要

ユーザーが現在の収入・支出・貯蓄を入力し、将来の資産推移、老後資金、緊急時の備えを計算・可視化します。

## 技術スタック

### フロントエンド (`frontend/`)
- **フレームワーク**: Next.js 14 (App Router)
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS
- **グラフ**: Chart.js
- **フォーム**: React Hook Form + Zod

### バックエンド (`backend/`)
- **言語**: Go 1.24+
- **フレームワーク**: Gin
- **データベース**: PostgreSQL
- **API仕様**: OpenAPI/Swagger (`docs/`)

### インフラ
- **デプロイ**: Render.com
- **CI/CD**: GitHub Actions
- **コンテナ**: Docker + Docker Compose

## アーキテクチャ

### バックエンド (DDD)

```
backend/
├── domain/
│   ├── entities/        # FinancialProfile, Goal, RetirementData
│   ├── valueobjects/    # Money, Percentage
│   ├── aggregates/      # FinancialPlan
│   └── repositories/    # インターフェース
├── application/usecases/
├── infrastructure/
│   ├── database/
│   ├── repositories/
│   └── web/
└── config/
```

### フロントエンド

```
frontend/src/
├── app/           # Next.js App Router
├── components/    # UIコンポーネント
├── lib/           # ユーティリティ
└── types/         # TypeScript型定義
```

## ドメイン知識

### 主要エンティティ

- **FinancialProfile**: 収入、支出、貯蓄、年齢
- **Goal**: 目標タイプ、金額、期限
- **RetirementData**: 年金、生活費、退職金

### 値オブジェクト

- **Money**: 通貨付き金額（不変）
- **Percentage**: パーセンテージ

### 計算ロジック

- 資産推移シミュレーション（複利）
- 老後資金の過不足計算
- 緊急資金の必要月数

## コーディング規約

### Go

```go
// エラーにコンテキストを付与
return fmt.Errorf("usecase: failed to save: %w", err)
```

### TypeScript

```typescript
// Zodでバリデーション
const schema = z.object({ monthlyIncome: z.number().positive() });
```

### コミット

Conventional Commits: `feat(frontend): 機能追加`, `fix(backend): バグ修正`

## コマンド

```bash
make dev          # 開発サーバー
make test         # テスト
make lint         # Lint
```

## API

| Method | Path | 説明 |
|--------|------|------|
| GET | `/health` | ヘルスチェック |
| POST | `/api/v1/financial-profiles` | プロファイル作成 |
| POST | `/api/v1/projections` | シミュレーション |

## 注意点

- 金額は整数（円）で扱う
- 本番: `DB_SSLMODE=require`, `GIN_MODE=release`
- UI/コメントは日本語OK

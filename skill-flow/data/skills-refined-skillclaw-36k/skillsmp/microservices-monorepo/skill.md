---
name: microservices-monorepo
description: マイクロサービス・モノレポ設計 - サービス分割、通信パターン、モノレポ構成
requires-guidelines:
  - microservices-kubernetes
  - common
---

# マイクロサービス・モノレポ設計

## 使用タイミング

- サービス分割検討時（モノリスからの移行）
- 新規マイクロサービス設計時
- モノレポ構成設計時

---

## 設計パターン

### サービス分割戦略

| 基準 | 説明 |
|------|------|
| ビジネス機能 | 注文、在庫、配送、決済 |
| DDD境界づけられたコンテキスト | ドメイン境界と一致 |
| チーム構成 | Conwayの法則（組織構造に従う） |
| データ所有 | 各サービスが独自DBを持つ |

**サービスサイズ**: 1チームで管理可能、明確な責務境界

### 通信パターン

| 種別 | パターン | 用途 |
|------|---------|------|
| 同期 | REST API | シンプルなCRUD |
| 同期 | gRPC | 高パフォーマンス、型安全 |
| 非同期 | メッセージキュー | Kafka, RabbitMQ, SQS |
| 非同期 | イベント駆動 | 疎結合、スケーラブル |

### アーキテクチャパターン

- **API Gateway**: 単一エントリポイント、認証、ルーティング
- **Service Mesh**: Istio, Linkerd
- **Circuit Breaker**: 障害連鎖防止
- **Saga**: 分散トランザクション

### モノレポ構成

```
monorepo/
├── services/           # 各サービス
├── packages/           # 共通ライブラリ、proto、types
├── infrastructure/     # k8s, terraform
└── tools/              # scripts
```

**ツール**: Turborepo, Nx, pnpm workspaces

---

## 主要パターン

```typescript
// ✅ イベント駆動通信
class OrderService {
  async placeOrder(order: Order): Promise<void> {
    await this.orderRepository.save(order);
    await this.eventBus.publish({ type: 'OrderPlaced', orderId: order.id });
  }
}

// ✅ API経由でアクセス（DB直接参照禁止）
const user = await this.userClient.GetUser(ctx, order.UserID);
```

```typescript
// ❌ 他サービスのDB直接参照（禁止）
// 理由: サービス境界違反。UserServiceのDBスキーマ変更時に破綻する
const userDB = new Pool({ connectionString: 'user-service-db-url' });

// ✅ API経由（サービス境界を尊重）
const user = await this.userClient.getUser(userId);
```

---

## チェックリスト

### サービス分割
- [ ] サービス境界がビジネス機能と一致
- [ ] 各サービスが独立デプロイ可能
- [ ] 各サービスが独自DBを持つ

### 通信設計
- [ ] 同期/非同期の使い分けが適切
- [ ] Circuit Breakerでフォールバック
- [ ] タイムアウト/リトライ設定

### データ管理
- [ ] Database per Service
- [ ] 分散トランザクションはSagaパターン

### 可観測性
- [ ] 構造化ログ
- [ ] 分散トレーシング
- [ ] 相関IDでリクエスト追跡

---

## 出力形式

```
📋 **サービス一覧**
- [サービス名]: [責務] - [DB] - [通信方式]

🔄 **サービス間通信**
[通信フロー]

🔴 **Critical**: サービス名 - 違反内容 - 修正案
🟡 **Warning**: サービス名 - 改善推奨 - リファクタ案
```

---

## 関連ガイドライン

- `design/microservices-kubernetes.md`
- `design/clean-architecture.md`

## 外部知識ベース（Context7）

- Kubernetes公式ドキュメント
- Service Mesh（Istio, Linkerd）
- Turborepo, Nx

> **Context7検索キーワード**:
> - `/vercel/turborepo` で "workspace dependencies"
> - `/nrwl/nx` で "affected commands"
> - "event driven architecture saga pattern"
> - "circuit breaker fallback"

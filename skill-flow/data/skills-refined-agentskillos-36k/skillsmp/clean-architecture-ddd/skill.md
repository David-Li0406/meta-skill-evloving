---
name: clean-architecture-ddd
description: クリーンアーキテクチャ・DDD設計 - レイヤー設計、ドメインモデリング、依存関係管理
requires-guidelines:
  - clean-architecture
  - ddd
  - common
---

# クリーンアーキテクチャ・DDD設計

## 使用タイミング

- 新規プロジェクト設計時
- 既存システムのリファクタリング時
- ドメインモデリング時

---

## レイヤー構成

```
依存方向: 外側 → 内側のみ

┌─────────────────────────────────────┐
│  Infrastructure (DB, API, Framework)│ ← 最外部
├─────────────────────────────────────┤
│  Interface (Controller, Presenter)  │ ← ユーザーIF層
├─────────────────────────────────────┤
│  Application (UseCase, Service)     │ ← ビジネスフロー
├─────────────────────────────────────┤
│  Domain (Entity, ValueObject, Repo) │ ← 最内部（依存なし）
└─────────────────────────────────────┘
```

## DDD戦術パターン

| パターン | 責務 | 配置層 |
|---------|------|--------|
| Entity | ID識別、ライフサイクル、ビジネスロジック | Domain |
| Value Object | 不変、値比較、副作用なし | Domain |
| Aggregate | 一貫性境界、ルートエンティティ | Domain |
| Repository | IF=Domain / 実装=Infra | Domain/Infra |
| UseCase | アプリケーション固有ロジック | Application |
| Domain Event | 過去形命名、疎結合 | Domain |

---

## 主要パターン

```go
// ✅ Domain層: ビジネスロジック + IF定義
type User struct { ID UserID; Status UserStatus }

func (u *User) Activate() error {
    if u.Status == StatusActive { return ErrAlreadyActive }
    u.Status = StatusActive
    return nil
}

type UserRepository interface {
    Save(user *User) error
    FindByID(id UserID) (*User, error)
}

// ✅ Application層: UseCase
func (uc *ActivateUserUseCase) Execute(userID UserID) error {
    user, _ := uc.repo.FindByID(userID)
    if err := user.Activate(); err != nil { return err }
    return uc.repo.Save(user)
}
```

```typescript
// ✅ Value Object（不変）
class Email {
  private constructor(private readonly value: string) {}
  static create(value: string): Email { /* バリデーション */ }
  equals(other: Email): boolean { return this.value === other.value; }
}

// ✅ リッチドメインモデル
class User {
  activate(): void {
    if (this.status === UserStatus.Active) throw new Error('Already active');
    this.status = UserStatus.Active;
  }
}
```

```go
// ❌ Domain が Infrastructure に依存（禁止）
// 理由: gorm.ModelはDB固有の型。Domain層はDB技術に依存してはならない
import "gorm.io/gorm"
type User struct { gorm.Model }  // → ID, CreatedAt等を自前で定義すべき
```

---

## チェックリスト

### レイヤー設計
- [ ] Domain層は外部依存なし
- [ ] 依存方向が外側→内側
- [ ] Repository IFはDomain層に定義

### ドメインモデリング
- [ ] ビジネスロジックがDomain/UseCaseにある
- [ ] Entityにビジネスルール実装
- [ ] Value Objectは不変
- [ ] Aggregateは小さく（1-3エンティティ）

### 依存関係
- [ ] 循環依存なし
- [ ] Controllerは薄い（入力変換→UseCase→出力変換）
- [ ] DomainにORM/Framework型が漏れていない

---

## 出力形式

```
📋 **レイヤー構成**
- Domain: [エンティティ一覧]
- Application: [UseCase一覧]
- Infrastructure: [実装一覧]

🔴 **Critical**: ファイル:行 - 違反内容 - 修正案
🟡 **Warning**: ファイル:行 - 改善推奨 - リファクタ案
```

---

## 関連ガイドライン

- `design/clean-architecture.md`
- `design/domain-driven-design.md`

## 外部知識ベース（Context7）

- クリーンアーキテクチャ（Robert C. Martin）
- DDD（エリック・エヴァンス）
- SOLID原則

> **Context7検索キーワード**:
> - Go: `/golang/go` で "interface repository pattern"
> - TypeScript: `/microsoft/typescript` で "dependency injection"
> - DDD: "aggregate root", "value object immutable"

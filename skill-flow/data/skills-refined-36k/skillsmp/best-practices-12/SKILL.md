---
name: best-practices
description: |
  このスキルは、ユーザーが「TDD」「テスト駆動開発」「FSD」「Feature-Sliced Design」「Clean Architecture」「DDD」「ドメイン駆動設計」「リファクタリング」「Red-Green-Refactor」「t-wada 式」について質問したとき、またはコード実装時にこれらのパターンを適用する必要があるときに使用する。
---

# TDD Best Practices

## TDD サイクル（t-wada 式）

### Red→Green→Refactor→Commit

1. **Red 🔴 - 失敗するテストを書く**

   - 実装したい単一の機能に対する、具体的で失敗するテストを一つ作成
   - 対応する実装がまだ存在しないため、テストは必ず失敗する

2. **Green 🟢 - テストをパスさせる**

   - 失敗したテストをパスさせるために必要な**最小限のコード**を記述
   - この段階で余分な機能を追加しない

3. **Refactor 🔨 - 設計を改善する**

   - テストが通っている状態を維持しながら、コードの品質を向上させる
   - 重複の排除、命名の明確化、複雑なロジックの単純化

4. **Commit ✅ - 進捗を保存する**
   - リファクタリングが完了し、全テストがグリーンであることを最終確認
   - 意味のあるまとまりとして完結した変更をコミット

## SOLID 原則

- **単一責任の原則 (SRP)**: 一つのモジュール、クラス、関数は、機能の一部分に対してのみ責任を持つ
- **開放閉鎖の原則 (OCP)**: 拡張に対して開いていて、修正に対して閉じている
- **リスコフの置換原則 (LSP)**: 派生型は基底型と置換可能であるべき
- **インターフェース分離の原則 (ISP)**: クライアントは自分が使わないメソッドに依存すべきでない
- **依存性逆転の原則 (DIP)**: 高レベルモジュールは低レベルモジュールに依存すべきでない

## Feature-Sliced Design (FSD)

### レイヤー構造（上から下へ依存）

```
src/
├── app/       # アプリケーション層（ページ、グローバル設定）
├── widgets/   # ウィジェット層（ページ構成要素）
├── features/  # フィーチャー層（ユーザー向け機能）
├── entities/  # エンティティ層（ビジネスエンティティ）
└── shared/    # 共有層（UI、ユーティリティ、設定）
```

### 依存関係ルール

- 上位層は下位層のみに依存可能
- 同一層内での相互依存は禁止
- shared 層はどこからでも使用可能

### スライス（フィーチャー）の構成

```
features/
└── client-management/
    ├── api/      # APIクライアント、サーバーアクション
    ├── model/    # ストア、型、ビジネスロジック
    ├── ui/       # UIコンポーネント
    └── index.ts  # パブリックAPI
```

## Clean Architecture

### レイヤー分離

```typescript
// Domain層（entities）
interface ClientRepository {
  findById(id: string): Promise<Client>;
}

// Application層（features）
class GetClientUseCase {
  constructor(private repo: ClientRepository) {}
  async execute(id: string) {
    return await this.repo.findById(id);
  }
}

// Infrastructure層（features/api）
class PrismaClientRepository implements ClientRepository {
  async findById(id: string) {
    return await prisma.client.findUnique({ where: { id } });
  }
}
```

## DDD（ドメイン駆動設計）

### エンティティとバリューオブジェクト

```typescript
// エンティティ（識別子を持つ）
class Client {
  constructor(
    private readonly id: ClientId,
    private name: ClientName,
    private tags: Tag[]
  ) {}
}

// バリューオブジェクト（不変）
class ClientName {
  constructor(private readonly value: string) {
    if (value.length < 2) {
      throw new Error("クライアント名は2文字以上必要です");
    }
  }
}
```

## コーディング規約

### ハードコーディング禁止

- **マジックナンバー**: 定数化必須
- **設定値**: 環境変数または設定ファイル
- **UI 文字列**: 定数や言語ファイルで管理

### その他の重要な規約

- **DRY**: コード重複は絶対に避ける
- **明確な命名**: 意図が明確に伝わる名前
- **早期リターン/ガード節**: 深いネストを避ける
- **useEffect 使用制限**: 代替案を優先（Server Components、イベントハンドラー、データフェッチライブラリ）

## リファクタリング技法

- メソッドの抽出: 複雑な関数を分割
- 変数/関数の名前変更: 明確性の向上
- マジックナンバーを定数に置き換え
- 条件式の簡略化
- 適切な場合はクラス/モジュールの抽出

## 関連スキル

詳細なガイダンスについては以下のスキルを参照：

- `dev-core:coding-standards` - 命名規約、ファイル構成、コードスタイル
- `dev-core:security-review` - OWASP Top 10、セキュリティチェック
- `dev-core:verification-loop` - 6 段階検証フロー
- `dev-core:backend-patterns` - API 設計、Repository パターン
- `dev-core:frontend-patterns` - React パターン、カスタムフック
- `dev-core:project-guidelines` - プロジェクト固有の設定

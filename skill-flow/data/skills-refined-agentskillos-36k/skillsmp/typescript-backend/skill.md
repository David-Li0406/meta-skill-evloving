---
name: typescript-backend
description: TypeScriptバックエンド開発 - 型安全、Node.js/Deno/Bun、フレームワーク活用
requires-guidelines:
  - typescript
  - common
---

# TypeScriptバックエンド開発

## 使用タイミング

- **TypeScript バックエンド実装時**
- **API 実装・レビュー時**
- **Node.js/Deno/Bun プロジェクト開発時**

## 開発観点

### 🔴 Critical（修正必須）

#### 1. 型安全性違反
```typescript
// ❌ 危険: any 使用
async function getUser(id: any): Promise<any> {
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result;
}

// ✅ 正しい: 厳格な型定義
type UserId = string & { __brand: 'UserId' };
interface User {
    id: UserId;
    name: string;
    email: string;
}

async function getUser(id: UserId): Promise<User | null> {
    const result = await db.query<User>(
        'SELECT * FROM users WHERE id = ?',
        [id]
    );
    return result.rows[0] ?? null;
}
```

#### 2. エラーハンドリング不足
```typescript
// ❌ 危険: エラー型が不明
async function createUser(data: CreateUserInput) {
    try {
        return await userRepo.save(data);
    } catch (error) {
        throw error;  // エラー型不明、処理不適切
    }
}

// ✅ 正しい: Result型パターン
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

async function createUser(
    data: CreateUserInput
): Promise<Result<User, ValidationError | DatabaseError>> {
    const validated = validateInput(data);
    if (!validated.ok) {
        return { ok: false, error: validated.error };
    }

    try {
        const user = await userRepo.save(validated.value);
        return { ok: true, value: user };
    } catch (error) {
        if (error instanceof DatabaseError) {
            return { ok: false, error };
        }
        throw error;
    }
}
```

#### 3. Non-null assertion 濫用
```typescript
// ❌ 危険: ! 演算子で実行時エラーリスク
function processUser(userId: string) {
    const user = users.find(u => u.id === userId)!;
    return user.name;  // userがundefinedの可能性
}

// ✅ 正しい: 明示的nullチェック
function processUser(userId: string): string | null {
    const user = users.find(u => u.id === userId);
    if (!user) {
        return null;
    }
    return user.name;
}
```

### 🟡 Warning（要改善）

#### 1. ミドルウェアの型安全性
```typescript
// ⚠️ 型推論が効かない
app.use((req, res, next) => {
    req.user = getCurrentUser();  // reqにuserプロパティがない
    next();
});

// ✅ 型拡張で安全に
declare global {
    namespace Express {
        interface Request {
            user?: User;
        }
    }
}

const authMiddleware = (
    req: Request,
    res: Response,
    next: NextFunction
): void => {
    req.user = getCurrentUser();
    next();
};
```

#### 2. 依存性注入不足
```typescript
// ⚠️ 直接インスタンス化（テスト困難）
class UserService {
    private repo = new UserRepository();

    async find(id: string) {
        return this.repo.findById(id);
    }
}

// ✅ DIコンテナ活用
interface IUserRepository {
    findById(id: string): Promise<User | null>;
}

class UserService {
    constructor(private repo: IUserRepository) {}

    async find(id: string) {
        return this.repo.findById(id);
    }
}
```

#### 3. async/await の適切な使用
```typescript
// ⚠️ 無駄な await
async function getUsers() {
    const user1 = await fetchUser(1);
    const user2 = await fetchUser(2);
    return [user1, user2];
}

// ✅ 並列実行
async function getUsers() {
    const [user1, user2] = await Promise.all([
        fetchUser(1),
        fetchUser(2),
    ]);
    return [user1, user2];
}
```

## TypeScript バックエンドチェック

### 型定義
- [ ] any 型を使用していないか
- [ ] as キャストを濫用していないか
- [ ] Non-null assertion (!) を使用していないか
- [ ] Branded Type で ID の型安全性を確保しているか
- [ ] tsconfig.json で `strict: true` が有効か

### エラーハンドリング
- [ ] Result 型パターンを使用しているか
- [ ] カスタムエラークラスを定義しているか
- [ ] エラー型を明示しているか

### 設計
- [ ] インターフェースで抽象化しているか
- [ ] 依存性注入を活用しているか
- [ ] レイヤー分離ができているか（domain/application/infrastructure）

### 非同期処理
- [ ] Promise.all で並列実行しているか
- [ ] エラーハンドリングが適切か
- [ ] async/await の使い方が適切か

## テストチェックリスト

- [ ] モックはインターフェースで定義しているか
- [ ] 型ガード関数をテストしているか
- [ ] Result 型の両方のケース（ok/error）をテストしているか

## 出力形式

🔴 **Critical**: `ファイル:行` - 型安全違反/エラー処理不足 - 修正案
🟡 **Warning**: `ファイル:行` - 設計改善推奨 - リファクタ案
📊 **Summary**: Critical X件 / Warning Y件

## 関連ガイドライン

開発実施前に以下のガイドラインを参照:
- `~/.claude/guidelines/languages/typescript.md`
- `~/.claude/guidelines/common/code-quality-design.md`
- `~/.claude/guidelines/common/testing-guidelines.md`

## 外部知識ベース

最新のTypeScriptバックエンドベストプラクティス確認には context7 を活用:
- TypeScript公式ドキュメント
- Node.js公式ドキュメント
- Express.js/Fastify/NestJS（使用フレームワーク）
- Deno/Bun（ランタイム）

## プロジェクトコンテキスト

プロジェクト固有のTypeScript実装情報を確認:
- serena memory からディレクトリ構成・フレームワーク情報を取得
- プロジェクトの標準的なエラーハンドリングパターンを優先
- 既存の型定義パターンとの一貫性を確認
- 使用しているDIコンテナ・ORMの規約に従う

# セキュリティパターン

## 入力検証

### SQLインジェクション対策

```typescript
// ❌ 危険
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 安全（パラメータ化クエリ）
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);
```

### NoSQLインジェクション対策

```typescript
// ❌ 危険
const user = await User.findOne({ username: req.body.username });

// ✅ 安全
const user = await User.findOne({
  username: { $eq: req.body.username },
});
```

## XSS対策

### React/フロントエンド

```tsx
// ❌ 危険
<div dangerouslySetInnerHTML={{__html: userContent}} />

// ✅ 安全（DOMPurify使用）
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(userContent)
}} />

// ✅ 安全（Reactのデフォルトエスケープ）
<div>{userContent}</div>
```

## 認証

### パスワードハッシュ化

```typescript
// ❌ 危険
const user = { password: password };

// ✅ 安全
const hashedPassword = await bcrypt.hash(password, 12);
const user = { password: hashedPassword };
```

## 認可

### 権限チェック

```typescript
// ❌ 危険（認可なし）
app.get("/user/:id", (req, res) => {
  const user = getUserById(req.params.id);
  res.json(user);
});

// ✅ 安全（認可あり）
app.get("/user/:id", authenticateToken, (req, res) => {
  if (req.user.id !== parseInt(req.params.id) && !req.user.isAdmin) {
    return res.status(403).json({ error: "Access denied" });
  }
  const user = getUserById(req.params.id);
  res.json(user);
});
```

## CSRF対策

```typescript
// ✅ CSRFトークンの実装
const csrfToken = getCsrfToken();
fetch("/api/data", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
  },
  body: JSON.stringify(data),
});
```

## 機密情報の保護

```typescript
// ❌ 危険
const config = {
  apiKey: "secret-api-key",
  databaseUrl: "mysql://user:pass@host/db",
};

// ✅ 安全（環境変数使用）
const config = {
  publicApiKey: process.env.REACT_APP_PUBLIC_API_KEY,
};
```

## レート制限

```typescript
// ✅ レート制限の実装
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分
  max: 100,
  message: "Too many requests",
});

app.use("/api/", limiter);
```

## セキュリティヘッダー

```typescript
// Express.js での設定例
app.use((req, res, next) => {
  res.setHeader("X-XSS-Protection", "1; mode=block");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader(
    "Strict-Transport-Security",
    "max-age=31536000; includeSubDomains"
  );
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'"
  );
  next();
});
```

## セキュリティテスト

### ツール
- **SAST**: SonarQube, Checkmarx, Veracode
- **DAST**: OWASP ZAP, Burp Suite
- **依存関係チェック**: npm audit, Snyk
- **コード品質**: ESLint security plugins

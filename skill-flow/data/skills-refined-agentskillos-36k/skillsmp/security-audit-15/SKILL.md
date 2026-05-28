---
name: security-audit
description: 安全审计和漏洞防护。用于识别安全漏洞、审查安全配置、实施安全最佳实践。包括 OWASP Top 10、认证授权、数据加密等。
allowed-tools: Read, Grep, Glob
---

# 安全审计

## OWASP Top 10

### 1. 注入攻击（Injection）

#### SQL 注入
```typescript
// ❌ 危险
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ 安全 - 参数化查询
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// ✅ 安全 - ORM
const user = await User.findById(userId);
```

#### NoSQL 注入
```typescript
// ❌ 危险
db.users.find({ username: req.body.username });

// ✅ 安全
const username = validator.escape(req.body.username);
db.users.find({ username });
```

#### 命令注入
```typescript
// ❌ 危险
exec(`ping ${userInput}`);

// ✅ 安全
const { spawn } = require('child_process');
spawn('ping', [userInput]);
```

### 2. 失效的身份认证

#### 密码存储
```typescript
import bcrypt from 'bcrypt';

// ✅ 哈希密码
const saltRounds = 10;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// ✅ 验证密码
const isValid = await bcrypt.compare(password, hashedPassword);

// ❌ 不要明文存储
// ❌ 不要使用 MD5 或 SHA1
```

#### JWT 安全
```typescript
import jwt from 'jsonwebtoken';

// ✅ 生成 token
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// ✅ 验证 token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
} catch (error) {
  // Token 无效或过期
}

// ❌ 不要在 token 中存储敏感信息
// ❌ 不要使用弱密钥
```

#### 会话管理
```typescript
// ✅ 安全的会话配置
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // 防止 XSS
    maxAge: 3600000, // 1 小时
    sameSite: 'strict' // 防止 CSRF
  }
}));
```

### 3. 敏感数据泄露

#### 数据加密
```typescript
import crypto from 'crypto';

// ✅ 加密敏感数据
const algorithm = 'aes-256-gcm';
const key = crypto.scryptSync(password, 'salt', 32);
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update(text, 'utf8', 'hex');
encrypted += cipher.final('hex');

// ✅ 解密
const decipher = crypto.createDecipheriv(algorithm, key, iv);
let decrypted = decipher.update(encrypted, 'hex', 'utf8');
decrypted += decipher.final('utf8');
```

#### HTTPS
```typescript
// ✅ 强制 HTTPS
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});

// ✅ HSTS
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

#### 敏感信息处理
```typescript
// ✅ 环境变量
const apiKey = process.env.API_KEY;

// ❌ 不要硬编码
// const apiKey = 'sk_live_abc123';

// ✅ 日志脱敏
logger.info({
  email: maskEmail(user.email), // u***@example.com
  phone: maskPhone(user.phone)  // ***-***-1234
});

// ❌ 不要记录敏感信息
// logger.info({ password: user.password });
```

### 4. XML 外部实体（XXE）

```typescript
// ✅ 禁用外部实体
const parser = new DOMParser();
parser.setFeature('http://xml.org/sax/features/external-general-entities', false);
parser.setFeature('http://xml.org/sax/features/external-parameter-entities', false);
```

### 5. 失效的访问控制

#### 权限检查
```typescript
// ✅ 中间件检查权限
function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
}

function requireRole(role) {
  return (req, res, next) => {
    if (!req.user.roles.includes(role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// 使用
app.get('/admin', requireAuth, requireRole('admin'), (req, res) => {
  // 管理员功能
});
```

#### 资源访问控制
```typescript
// ✅ 验证资源所有权
app.get('/posts/:id', requireAuth, async (req, res) => {
  const post = await Post.findById(req.params.id);

  if (post.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json(post);
});
```

### 6. 安全配置错误

#### 安全头
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  xssFilter: true,
  noSniff: true,
  referrerPolicy: { policy: 'same-origin' },
}));
```

#### CORS 配置
```typescript
import cors from 'cors';

// ✅ 限制来源
app.use(cors({
  origin: ['https://example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// ❌ 不要使用 *
// app.use(cors({ origin: '*' }));
```

#### 错误处理
```typescript
// ✅ 生产环境不暴露详细错误
app.use((err, req, res, next) => {
  logger.error(err);

  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});
```

### 7. 跨站脚本（XSS）

#### 输入验证和输出编码
```typescript
import DOMPurify from 'dompurify';
import validator from 'validator';

// ✅ 清理 HTML
const clean = DOMPurify.sanitize(userInput);

// ✅ 转义特殊字符
const escaped = validator.escape(userInput);

// ✅ React 自动转义
<div>{userInput}</div>

// ❌ 危险
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

#### CSP（内容安全策略）
```typescript
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'nonce-{random}'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'", 'https://api.example.com'],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
  },
}));
```

### 8. 不安全的反序列化

```typescript
// ❌ 危险
const obj = eval(userInput);

// ✅ 安全
const obj = JSON.parse(userInput);

// ✅ 验证数据结构
import { z } from 'zod';

const schema = z.object({
  name: z.string(),
  age: z.number()
});

const data = schema.parse(JSON.parse(userInput));
```

### 9. 使用含有已知漏洞的组件

```bash
# ✅ 定期检查依赖漏洞
npm audit
npm audit fix

# ✅ 使用 Snyk
snyk test
snyk monitor

# ✅ 自动化检查
# package.json
"scripts": {
  "security-check": "npm audit && snyk test"
}
```

### 10. 不足的日志记录和监控

```typescript
import winston from 'winston';

// ✅ 结构化日志
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// ✅ 记录安全事件
logger.warn({
  event: 'failed_login',
  userId: req.body.username,
  ip: req.ip,
  timestamp: new Date()
});

// ✅ 监控异常活动
if (failedAttempts > 5) {
  logger.error({
    event: 'brute_force_attempt',
    userId: req.body.username,
    ip: req.ip
  });
  // 触发告警
}
```

## 认证和授权

### 多因素认证（MFA）
```typescript
import speakeasy from 'speakeasy';

// 生成密钥
const secret = speakeasy.generateSecret({ name: 'MyApp' });

// 验证 TOTP
const verified = speakeasy.totp.verify({
  secret: secret.base32,
  encoding: 'base32',
  token: userToken
});
```

### OAuth 2.0
```typescript
// 授权码流程
app.get('/oauth/authorize', (req, res) => {
  // 验证 client_id, redirect_uri, scope
  // 生成授权码
  const code = generateAuthCode();
  res.redirect(`${redirect_uri}?code=${code}`);
});

app.post('/oauth/token', (req, res) => {
  // 验证授权码
  // 生成访问令牌
  const accessToken = generateAccessToken();
  res.json({ access_token: accessToken });
});
```

### RBAC（基于角色的访问控制）
```typescript
const permissions = {
  admin: ['read', 'write', 'delete'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function hasPermission(user, action) {
  const userPermissions = permissions[user.role];
  return userPermissions.includes(action);
}

// 使用
if (hasPermission(req.user, 'delete')) {
  // 允许删除
}
```

## API 安全

### API 密钥管理
```typescript
// ✅ API 密钥验证
app.use('/api', (req, res, next) => {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey || !isValidApiKey(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  next();
});

// ✅ 限流
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests'
});

app.use('/api/', limiter);
```

### GraphQL 安全
```typescript
// ✅ 查询深度限制
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)]
});

// ✅ 查询复杂度限制
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  validationRules: [createComplexityLimitRule(1000)]
});
```

## 数据保护

### GDPR 合规
```typescript
// ✅ 数据最小化
// 只收集必要的数据

// ✅ 数据删除
app.delete('/users/:id/data', requireAuth, async (req, res) => {
  await User.deleteAllData(req.params.id);
  res.json({ message: 'Data deleted' });
});

// ✅ 数据导出
app.get('/users/:id/data', requireAuth, async (req, res) => {
  const data = await User.exportData(req.params.id);
  res.json(data);
});
```

### 数据脱敏
```typescript
function maskEmail(email) {
  const [name, domain] = email.split('@');
  return `${name[0]}***@${domain}`;
}

function maskPhone(phone) {
  return phone.replace(/\d(?=\d{4})/g, '*');
}

function maskCreditCard(card) {
  return card.replace(/\d(?=\d{4})/g, '*');
}
```

## 安全测试

### 渗透测试工具
```bash
# OWASP ZAP
zap-cli quick-scan http://example.com

# Burp Suite
# 手动测试工具

# Nikto
nikto -h http://example.com
```

### 自动化安全扫描
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## 安全检查清单

### 认证和授权
- [ ] 密码使用强哈希算法（bcrypt）
- [ ] 实施多因素认证
- [ ] JWT 使用强密钥和短过期时间
- [ ] 会话配置安全（httpOnly, secure, sameSite）
- [ ] 实施权限检查
- [ ] 验证资源所有权

### 输入验证
- [ ] 所有输入都经过验证
- [ ] 使用参数化查询防止 SQL 注入
- [ ] 清理 HTML 输入防止 XSS
- [ ] 验证文件上传类型和大小
- [ ] 限制请求大小

### 数据保护
- [ ] 敏感数据加密存储
- [ ] 使用 HTTPS
- [ ] 实施 HSTS
- [ ] 环境变量存储密钥
- [ ] 日志脱敏
- [ ] 数据备份加密

### 配置安全
- [ ] 使用安全头（helmet）
- [ ] 配置 CORS
- [ ] 禁用不必要的功能
- [ ] 生产环境不暴露详细错误
- [ ] 定期更新依赖
- [ ] 移除默认凭证

### API 安全
- [ ] API 密钥验证
- [ ] 实施限流
- [ ] 输入验证
- [ ] 输出编码
- [ ] GraphQL 查询限制

### 监控和日志
- [ ] 记录安全事件
- [ ] 监控异常活动
- [ ] 设置告警
- [ ] 定期审查日志
- [ ] 实施入侵检测

### 依赖安全
- [ ] 定期运行 npm audit
- [ ] 使用 Snyk 扫描
- [ ] 自动化安全检查
- [ ] 及时更新依赖
- [ ] 审查第三方库

### 合规性
- [ ] GDPR 合规（如适用）
- [ ] 数据删除功能
- [ ] 数据导出功能
- [ ] 隐私政策
- [ ] 用户同意机制

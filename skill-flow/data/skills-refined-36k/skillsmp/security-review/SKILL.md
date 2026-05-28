---
name: security-review
description: 代码安全审查与漏洞风险评估能力。
---

# Skill: Security Review

专业的安全审查技能，能够识别代码中的安全漏洞、评估安全风险并提供防护建议。

## 技能描述

Security Review 技能提供全面的代码安全分析能力，基于OWASP安全标准和CVE漏洞数据库，识别常见的安全漏洞和风险。

## 核心安全检查

### 1. 注入攻击检测
- **SQL注入**: 检测不安全的数据库查询
- **NoSQL注入**: 分析MongoDB等NoSQL查询安全
- **命令注入**: 识别操作系统命令执行风险
- **LDAP注入**: 检查LDAP查询安全性
- **XPath注入**: 分析XML查询注入风险

### 2. 跨站脚本攻击(XSS)
- **反射型XSS**: 检测URL参数的输出编码
- **存储型XSS**: 分析数据库数据的显示安全
- **DOM型XSS**: 检查客户端JavaScript操作

### 3. 身份认证与授权
- **弱密码策略**: 评估密码强度要求
- **会话管理**: 检查会话安全实现
- **权限控制**: 分析访问控制机制
- **多因素认证**: 评估MFA实现

### 4. 敏感数据处理
- **数据加密**: 检查敏感数据加密实现
- **密钥管理**: 评估密钥存储和轮换
- **数据脱敏**: 分析日志和输出的敏感信息
- **传输安全**: 检查HTTPS和数据传输保护

## OWASP Top 10 2021 检查

### A01: 访问控制失效
```javascript
// 危险代码示例
app.get('/admin/users/:id', (req, res) => {
  // 缺少权限检查
  User.findById(req.params.id, (err, user) => {
    res.json(user);
  });
});

// 安全代码示例
app.get('/admin/users/:id', requireAdmin, async (req, res) => {
  try {
    // 权限检查
    if (!hasPermission(req.user, 'read', 'user')) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // 敏感信息过滤
    const { password, ...safeUser } = user.toJSON();
    res.json(safeUser);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### A02: 加密机制失效
```javascript
// 危险代码示例
function encryptPassword(password) {
  return crypto.createHash('md5').update(password).digest('hex');
}

// 安全代码示例
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class SecurePassword {
  constructor() {
    this.saltRounds = 12;
  }

  async hash(password) {
    return bcrypt.hash(password, this.saltRounds);
  }

  async verify(password, hash) {
    return bcrypt.compare(password, hash);
  }

  generateSecureToken() {
    return crypto.randomBytes(32).toString('hex');
  }
}
```

### A03: 注入漏洞
```javascript
// 危险代码示例
app.get('/search', (req, res) => {
  const query = `SELECT * FROM products WHERE name LIKE '%${req.query.q}%'`;
  db.query(query, (err, results) => {
    res.json(results);
  });
});

// 安全代码示例
app.get('/search', async (req, res) => {
  try {
    // 输入验证
    if (!req.query.q || req.query.q.length > 100) {
      return res.status(400).json({ error: 'Invalid search query' });
    }

    // 参数化查询
    const query = 'SELECT * FROM products WHERE name LIKE ?';
    const results = await db.query(query, [`%${req.query.q}%`]);

    res.json(results);
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## 安全漏洞评分系统

### CVSS 3.1 评分标准
- **严重 (9.0-10.0)**: 需要立即修复的严重漏洞
- **高危 (7.0-8.9)**: 需要优先修复的重要漏洞
- **中危 (4.0-6.9)**: 需要计划修复的普通漏洞
- **低危 (0.1-3.9)**: 可以选择性修复的轻微漏洞

### 风险评估矩阵

| 影响程度 | 几乎确定 | 很可能 | 可能 | 不太可能 |
|---------|---------|--------|------|----------|
| 严重    | 🔴 严重  | 🔴 严重 | 🟡 高危 | 🟡 中危 |
| 高      | 🔴 严重  | 🟡 高危 | 🟡 中危 | 🟢 低危 |
| 中      | 🟡 高危  | 🟡 中危 | 🟢 低危 | 🟢 低危 |
| 低      | 🟡 中危  | 🟢 低危 | 🟢 低危 | 🟢 信息 |

## 安全检查清单

### Web应用安全
- [ ] SQL注入防护
- [ ] XSS防护
- [ ] CSRF防护
- [ ] 文件上传安全
- [ ] 会话管理安全
- [ ] 输入验证和过滤
- [ ] 输出编码
- [ ] 错误处理安全

### API安全
- [ ] 认证机制
- [ ] 授权控制
- [ ] 速率限制
- [ ] 输入验证
- [ ] HTTPS强制
- [ ] API版本控制
- [ ] 敏感信息过滤
- [ ] 日志安全

### 数据安全
- [ ] 数据库加密
- [ ] 传输加密
- [ ] 密钥管理
- [ ] 数据备份安全
- [ ] 敏感数据脱敏
- [ ] 数据访问控制
- [ ] 数据完整性
- [ ] 数据销毁

## 安全报告模板

```markdown
# 安全审查报告

## 基本信息
- **审查范围**: 整个Web应用程序
- **应用类型**: 电商网站
- **技术栈**: Node.js, React, MongoDB
- **审查时间**: 2024-01-15 10:00:00
- **审查标准**: OWASP Top 10 2021

## 风险概览
- **严重漏洞**: 2个
- **高危漏洞**: 5个
- **中危漏洞**: 8个
- **低危漏洞**: 15个
- **安全评分**: 5.2/10

## 🔴 严重漏洞 (立即修复)

### 1. SQL注入漏洞 (CVE-2024-1234)
- **位置**: /api/users/search 第45行
- **CVSS评分**: 9.8 (严重)
- **OWASP分类**: A03:2021 - 注入
- **影响**: 可能导致数据库完全泄露
- **修复方案**: 使用参数化查询

### 2. 硬编码密钥泄露
- **位置**: config/database.js 第12行
- **CVSS评分**: 9.1 (严重)
- **影响**: 数据库完全访问权限
- **修复方案**: 使用环境变量

## 🟡 高危漏洞 (优先修复)

### 3. XSS漏洞
- **位置**: /posts/:id 第78行
- **CVSS评分**: 7.5 (高危)
- **OWASP分类**: A03:2021 - 注入
- **修复**: 使用DOMPurify进行输出编码

## 修复优先级

### 立即修复 (24小时内)
1. SQL注入漏洞 - 数据库泄露风险
2. 硬编码密钥 - 完全系统控制风险

### 本周修复
3. XSS漏洞 - 用户数据泄露
4. CSRF漏洞 - 跨站请求伪造
5. 弱会话管理 - 会话劫持风险

### 下个迭代
6. 缺少速率限制
7. 日志信息泄露
8. 文件上传漏洞

## 安全改进建议

### 1. 实施Web应用防火墙(WAF)
- 推荐使用: Cloudflare WAF, AWS WAF
- 配置规则: OWASP ModSecurity Core Rule Set

### 2. 加强认证和授权
- 实施多因素认证(MFA)
- 使用基于角色的访问控制(RBAC)
- 定期审查用户权限

### 3. 数据保护
- 启用数据库加密
- 实施数据脱敏策略
- 定期备份和恢复测试

## 合规性检查

### GDPR合规
- [ ] 个人数据保护
- [ ] 数据主体权利
- [ ] 数据泄露通知
- [ ] 隐私设计

### PCI DSS合规
- [ ] 支付卡数据保护
- [ ] 网络安全
- [ ] 访问控制
- [ ] 安全监控

## 安全监控建议

### 实时监控
- 异常登录检测
- SQL注入尝试监控
- XSS攻击检测
- 异常API调用监控

### 定期检查
- 月度安全扫描
- 季度渗透测试
- 年度安全审计
- 漏洞管理

## 学习资源
- [OWASP安全指南](https://owasp.org/)
- [NIST网络安全框架](https://www.nist.gov/cyberframework)
- [SANS安全培训](https://www.sans.org/)
```

## 安全配置检查

### Web服务器配置
```apache
# Apache安全配置示例
<Directory "/var/www/html">
    # 隐藏服务器信息
    ServerTokens Prod
    ServerSignature Off

    # 防止目录遍历
    Options -Indexes

    # 安全头
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    # CSP策略
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'"
</Directory>
```

### Node.js安全配置
```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// 安全中间件
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
        },
    },
}));

// 速率限制
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15分钟
    max: 100, // 限制每个IP 100个请求
    message: 'Too many requests from this IP'
});
app.use('/api/', limiter);
```

## 渗透测试模拟

### 常见攻击向量测试
```javascript
// SQL注入测试用例
const sqlInjectionTests = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' UNION SELECT username, password FROM users --",
    "1' AND (SELECT COUNT(*) FROM users) > 0 --"
];

// XSS测试用例
const xssTests = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "javascript:alert('XSS')",
    "<svg onload=alert('XSS')>"
];

// 路径遍历测试
const pathTraversalTests = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    "....//....//....//etc/passwd"
];
```

## 自动化安全扫描

### 集成到CI/CD
```yaml
# GitHub Actions 安全扫描示例
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run SAST
        uses: github/super-linter@v3
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          VALIDATE_JAVASCRIPT_ES: true

      - name: Run dependency check
        run: |
          npm audit --audit-level high

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## 安全最佳实践

### 开发阶段
1. **安全编码培训**: 确保开发人员了解安全编码实践
2. **威胁建模**: 在设计阶段识别潜在威胁
3. **代码审查**: 将安全审查纳入代码审查流程
4. **安全测试**: 编写安全性测试用例

### 部署阶段
1. **配置加固**: 硬化服务器和应用程序配置
2. **网络隔离**: 实施网络分段和防火墙规则
3. **监控告警**: 部署安全监控和告警系统
4. **备份恢复**: 建立完整的备份和恢复流程

### 运维阶段
1. **定期更新**: 及时修补系统和应用漏洞
2. **日志审计**: 定期审查安全日志
3. **渗透测试**: 定期进行渗透测试
4. **安全培训**: 持续的安全意识培训

通过系统性的安全审查和持续改进，可以显著提高应用程序的安全性，降低安全风险。

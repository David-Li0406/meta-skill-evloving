# 配置说明

在项目根目录创建 `.stale-config.json`（或 `.project-index/.stale-config.json`）。

## 完整配置

```json
{
  "include": [
    "js/agents/**",
    "js/ppt/**"
  ],
  "ignore": [
    "tests/**",
    "docs/**",
    "*.test.js"
  ],
  "features": {
    "doc": true,
    "audit": true,
    "kanban": true,
    "testAnalysis": true
  },
  "notify": {
    "enabled": true,
    "threshold": 3,
    "onSessionStart": true
  },
  "conventions": {
    "language": "JavaScript + JSDoc",
    "noTypescript": true,
    "rules": [
      "使用 ES Modules",
      "JSDoc 类型注解"
    ],
    "auditFocus": [
      "检查 TypeScript 语法误入",
      "验证 JSDoc 完整性"
    ]
  },
  "testing": {
    "coverage": {
      "target": 80,
      "minimum": 60
    }
  },
  "security": {
    "severity": ["critical", "high", "medium"]
  },
  "concurrency": 6,
  "timeout": 180000
}
```

## 配置项

### 路径过滤

| 配置 | 类型 | 说明 |
|------|------|------|
| `include` | `string[]` | 白名单 glob，只处理匹配的目录 |
| `ignore` | `string[]` | 黑名单 glob，忽略的文件/目录 |

### 功能开关

| 配置 | 默认 | 说明 |
|------|------|------|
| `features.doc` | `true` | 启用文档更新 |
| `features.audit` | `true` | 启用代码审计 |
| `features.kanban` | `true` | 启用 Kanban 任务创建 |
| `features.testAnalysis` | `true` | 启用测试分析 |

### 通知设置

| 配置 | 默认 | 说明 |
|------|------|------|
| `notify.enabled` | `true` | 启用过期通知 |
| `notify.threshold` | `3` | 变化超过此值才通知 |
| `notify.onSessionStart` | `true` | 会话开始时检查 |

### 项目规范

| 配置 | 说明 |
|------|------|
| `conventions.language` | 项目语言/技术栈 |
| `conventions.rules` | 编码规范列表 |
| `conventions.auditFocus` | 审计时特别关注的问题 |

### 测试配置

| 配置 | 说明 |
|------|------|
| `testing.coverage.target` | 目标覆盖率 |
| `testing.coverage.minimum` | 最低覆盖率 |

### 安全配置

| 配置 | 说明 |
|------|------|
| `security.severity` | 关注的严重级别 |

### 执行配置

| 配置 | 默认 | 说明 |
|------|------|------|
| `concurrency` | `6` | 并发执行数 |
| `timeout` | `180000` | 单任务超时 (ms) |

## CLI 参数覆盖

```bash
node module-analyzer.js --no-doc      # 禁用文档更新
node module-analyzer.js --no-audit    # 禁用审计
node module-analyzer.js --no-kanban   # 禁用 Kanban
```

## 配置优先级

1. CLI 参数
2. 项目 `.stale-config.json`
3. 项目 `.project-index/.stale-config.json`
4. 默认值

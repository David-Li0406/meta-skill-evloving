# Commit Message Templates

Use these templates as references when generating commit messages.

**Note**: This skill has zero script dependencies. All parsing logic (PMS URLs, Issue URLs) is handled by the AI directly through natural language understanding and git commands.

## Basic Template

```
<type>[optional scope]: <english description>

[English body - optional, max 80 chars per line]

[Chinese body - optional, max 80 chars per line, must pair with English]

Log: [concise Chinese description]
PMS: <BUG-number or TASK-number> or omit if none
Issue: Fixes #<number> or omit if none
Influence: [explain impact in Chinese]
```

## Examples

### Feature Addition

```
feat(auth): add JWT authentication middleware

Implement JWT-based authentication with token validation logic
and refresh token support.

添加基于JWT的认证中间件，支持令牌验证和刷新令牌。

Log: 添加JWT认证中间件
PMS: TASK-385999
Issue: Fixes #183
Influence: 所有API请求现在需要有效的JWT令牌进行认证，提升系统安全性。
```

### Bug Fix

```
fix(user): resolve incorrect role assignment mapping

Use correct role key mapping from database configuration
to avoid permission mismatches.

修复用户角色映射错误的bug，使用正确的数据库配置映射。

Log: 修复用户角色映射bug
Influence: 修复后用户角色分配逻辑正确，避免权限检查错误。
```

### Documentation

```
docs(readme): update installation guide for Linux arm64

Add detailed instructions for ARM64 architecture installation
and dependency requirements.

更新Linux ARM64架构的安装指南，添加依赖说明。

Log: 更新ARM64安装文档
Influence: 用户可以更清楚地在ARM64机器上安装和配置项目。
```

### Performance Improvement

```
perf(query): optimize database query with pagination

Add pagination support to reduce memory usage on large datasets.
Improve response time from 2s to 500ms on 10k records.

添加分页支持减少大数据集的内存占用。在1万条记录上
响应时间从2秒优化到500毫秒。

Log: 优化数据库查询性能
PMS: TASK-456789
Issue: Fixes #204
Influence: 大数据集查询性能提升4倍，内存占用降低60%。
```

### Refactoring

```
refactor(api): extract common validation logic to utils module

Move duplicate validation rules from multiple endpoints to
shared utility class for better maintainability.

将重复的验证规则从多个端点提取到共享工具类，
提高代码可维护性。

Log: 重构验证逻辑为共享模块
Influence: 代码结构更清晰，减少重复代码，便于后续维护。
```

### Test Coverage

```
test(auth): add unit tests for JWT token validation

Cover edge cases including expired tokens, invalid signatures,
and malformed payloads.

添加JWT令牌验证的单元测试，覆盖过期令牌、无效签名
和格式错误等边界情况。

Log: 添加JWT验证单元测试
Issue: Fixes #251
Influence: 提高认证模块的测试覆盖率，确保关键逻辑的正确性。
```

### CI/CD

```
ci(github): add automated testing workflow on PR

Configure GitHub Actions to run test suite on every pull request.
Integrate with code coverage reporting.

配置GitHub Actions在每个PR上运行测试套件。
集成代码覆盖率报告。

Log: 添加PR自动测试工作流
PMS: TASK-789012
Influence: 每次PR自动运行测试，提前发现问题，提高代码质量。
```

### Chore

```
chore(deps): upgrade dependencies to latest stable versions

Update Rust dependencies to fix security vulnerabilities
and improve performance.

更新Rust依赖修复安全漏洞并提升性能。

Log: 升级依赖包版本
PMS: TASK-345678
Influence: 修复已知安全漏洞，获得性能和稳定性改进。
```

## Type Reference

- **feat**: 新功能 (New feature)
- **fix**: 修复Bug (Bug fix)
- **docs**: 文档变更 (Documentation changes)
- **style**: 代码格式调整 (Code style changes)
- **refactor**: 重构 (Code refactoring)
- **perf**: 性能优化 (Performance improvements)
- **test**: 测试相关 (Test changes)
- **chore**: 构建/工具相关 (Build/tooling)
- **ci**: CI/CD配置 (CI/CD configuration)

## Scope Examples

Common scopes:
- `auth` - Authentication and authorization
- `user` - User management
- `db` - Database operations
- `api` - API endpoints
- `ui` - User interface
- `config` - Configuration
- `deps` - Dependencies
- `docs` - Documentation

## Constraints Checklist

- [ ] Body lines do not exceed 80 characters
- [ ] English and Chinese body appear in pairs (if provided)
- [ ] Log is concise Chinese description
- [ ] Influence explains impact clearly in Chinese
- [ ] PMS number format: `BUG-xxxxxx` or `TASK-xxxxxx`
- [ ] Issue format: `#xxx` or `owner/repo#xxx`
- [ ] All relevant information before asking user to confirm

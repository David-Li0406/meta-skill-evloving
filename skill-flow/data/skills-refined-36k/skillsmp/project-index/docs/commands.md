# 常用命令参考

## 生成与更新

```bash
# 日常维护（只处理过期）
node scripts/module-analyzer.js

# 补全缺失文档
node scripts/module-analyzer.js --missing --no-audit

# 补全缺失审计
node scripts/module-analyzer.js --missing --no-doc

# 全量处理（过期 + 缺失）
node scripts/module-analyzer.js --all

# 预览模式
node scripts/module-analyzer.js --all --dry-run

# 强制刷新
node scripts/module-analyzer.js --force

# 重试失败任务（不清空状态）
node scripts/module-analyzer.js --retry-failed

# 从中断处继续
node scripts/module-analyzer.js --resume
```

## 状态检查

```bash
# 过期检测
node scripts/check-stale.js --stale-only

# 审计状态
node scripts/audit-status.js --json

# 测试覆盖
node scripts/test-status.js --summary

# 测试映射（生成 .test-map.json）
node scripts/test-mapper.js

# 测试映射预览
node scripts/test-mapper.js --dry-run --verbose

# 生成模块 TEST.md
node scripts/test-mapper.js --generate-md
```

## 测试生成

```bash
# 批量生成未测试文件的测试
node scripts/test-generator.js --untested

# 重新生成过期测试
node scripts/test-generator.js --stale

# 全部（未测试 + 过期）
node scripts/test-generator.js --all

# 预览模式
node scripts/test-generator.js --dry-run

# 指定并发数
node scripts/test-generator.js --concurrency=2

# 后台运行
node scripts/test-generator.js --daemon
```

## 自动修复

```bash
# 测试错误自动修复（需先运行 test-result.js --save）
node scripts/test-fix.js               # 修复前 40 个错误
node scripts/test-fix.js --offset=40   # 修复下 40 个错误

# 测试修复预览
node scripts/test-fix.js --dry-run

# 指定并发数
node scripts/test-fix.js --concurrency=8

# 审计问题自动修复
node scripts/audit-fix.js

# 审计修复（指定严重级别）
node scripts/audit-fix.js --severity=LOW

# 审计修复预览
node scripts/audit-fix.js --dry-run
```

## 测试结果提取 (AI 友好)

```bash
# 运行测试并保存完整结果
node scripts/test-result.js --save

# 获取 40 个错误（AI 并发修复）
node scripts/test-result.js --cached --errors

# 下一批 40 个
node scripts/test-result.js --cached --errors --offset=40

# 单行摘要
node scripts/test-result.js --cached --summary
```

**设计**: 像 audit-fix 一样，每个错误给完整信息，AI 并发 40 个去修。

**输出格式**:
```json
{
  "showing": "1-40 of 120 errors",
  "concurrency": 40,
  "errors": [
    {
      "id": 1,
      "testFile": "tests/unit/foo/bar.test.js",
      "sourceFile": "js/foo/bar.js",
      "test": "should handle edge case",
      "message": "Expected: 'foo' Received: 'bar'",
      "line": 42,
      "expected": "foo",
      "received": "bar"
    }
  ]
}
```

每个错误含 `testFile` + `sourceFile` + 完整 `message`，AI 直接并发处理。

## Dashboard

```bash
node scripts/dashboard.js --open
```

Dashboard 功能：
- **任务启动器** - 图形化配置和启动任务
- **运维监控** - 任务状态、筛选、分组、重试
- **项目洞察** - 审计统计、测试覆盖、文档覆盖
- **配置编辑** - 可视化编辑 .stale-config.json

详见 [dashboard.md](dashboard.md)

# Ace 包装器对比

## 调用方式对比

| 操作 | 直接调用 client.ts | 使用 ace 包装器 | 优势 |
|------|------------------|----------------|------|
| 语义搜索 | `bun ~/.pi/agent/skills/ace-tool/client.ts search "query"` | `ace search "query"` | 简洁 63% |
| 提示增强 | `bun ~/.pi/agent/skills/ace-tool/client.ts enhance "prompt"` | `ace enhance "prompt"` | 简洁 63% |
| 简写形式 | 不支持 | `ace s "query"` | 更简洁 |

## 实际示例

### 旧方式（直接调用）

```bash
# 需要输入完整的路径和 bun 命令
cd /path/to/project
bun ~/.pi/agent/skills/ace-tool/client.ts search "Where is authentication handled?"
bun ~/.pi/agent/skills/ace-tool/client.ts enhance "Add login page"
```

### 新方式（使用包装器）

```bash
# 简洁直观
cd /path/to/project
ace search "Where is authentication handled?"
ace enhance "Add login page"

# 更短的简写
ace s "Where is authentication?"
ace e "Add login page"
```

## 包装器功能

| 功能 | 说明 |
|------|------|
| 参数验证 | 提前检查必需参数 |
| 命令解析 | 支持完整命令和简写 |
| 错误提示 | 友好的错误信息 |
| 帮助系统 | 内置使用说明 |

## 技术细节

```bash
# 包装器执行流程
ace search "test"
    ↓
/usr/local/bin/ace (Bash 脚本)
    ↓
bun ~/.pi/agent/skills/ace-tool/client.ts search "test"
    ↓
TypeScript 代码执行
```

## 总结

使用 `ace` 包装器可以：
1. **减少输入量**：从 60+ 字符减少到 20 字符
2. **提高可读性**：更符合 Unix 命令风格
3. **降低记忆负担**：只需要记住 `ace` 命令
4. **统一接口**：与其他 CLI 工具风格一致

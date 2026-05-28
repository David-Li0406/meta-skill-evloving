# 步骤3：子代理确认

## 执行

1. 读取`~/.codex/skills/agents-registry/references/registry.yaml`
2. 对照草案中的子代理需求，逐项检查：
   - 已存在且status=active：标记为✓
   - 不存在或status=disabled：标记为✗，记录缺失项

## 缺失处理（自动化）

如果存在缺失项：

1. **创建 Record/sub.md 任务文件**：

```markdown
# 子代理创建任务

创建时间：{ISO8601}
项目根目录：{project_root}

## 任务清单

- [ ] {缺失子代理1} ({职责})
- [ ] {缺失子代理2} ({职责})

## 子代理说明

| 名称 | 职责 | 所需工具 |
|------|------|----------|
| {子代理1} | {职责描述} | {工具列表} |
| {子代理2} | {职责描述} | {工具列表} |
```

2. **返回 need_sub 状态**：

```yaml
status: need_sub
sub_file: "Record/sub.md"
missing_agents:
  - name: "data-agent"
    role: "数据处理与转换"
    tools: ["Read", "Write", "Glob", "Grep", "Bash"]
  - name: "test-agent"
    role: "测试执行与报告"
    tools: ["Read", "Write", "Glob", "Grep", "Bash"]
summary: "检测到 2 个子代理缺失，已创建 Record/sub.md"
```

3. **Claude 主对话收到 need_sub 后**：
   - 自动启动 sub-agent
   - sub-agent 读取 Record/sub.md 创建子代理
   - sub-agent 返回结果后，Claude 主对话判断：
     - success → 重新执行子代理确认
     - failed → 询问用户如何处理

## 禁止凑合替代

- 需要`c-agent`但只有`rust-agent` → 阻塞，不允许用rust-agent写C
- 需要`python-agent`但registry中没有 → 阻塞，要求创建
- 需要`data-agent`但只有`python-agent` → 阻塞，要求创建专用子代理

## 通过条件

无缺失项时返回 success，自动进入下一步。

```yaml
status: success
summary: "子代理检查通过，所有需要的子代理已就绪"
```

## sub.md 任务文件示例

```markdown
# 子代理创建任务

创建时间：2026-01-08T10:30:00+08:00
项目根目录：/home/user/my-project

## 任务清单

- [ ] data-agent (数据处理)
- [ ] test-agent (测试执行)

## 子代理说明

| 名称 | 职责 | 所需工具 |
|------|------|----------|
| data-agent | 数据处理与转换 | Read, Write, Glob, Grep, Bash |
| test-agent | 测试执行与报告 | Read, Write, Glob, Grep, Bash |

## 备注

- 子代理必须通过质量门禁（总分>=24）
- 创建后自动同步到镜像目录
- 创建后自动更新登记表
```

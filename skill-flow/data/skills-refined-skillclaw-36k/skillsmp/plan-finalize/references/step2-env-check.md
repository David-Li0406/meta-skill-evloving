# 步骤2：环境确认

## 执行

1. 读取`~/environment.md`获取当前环境清单
2. 对照草案中的`dependencies`需求，逐项检查：
   - 已具备：标记为✓
   - 缺失：标记为✗，记录缺失项

## 缺失处理（自动化）

如果存在缺失项：

1. **创建 Record/env.md 任务文件**：

```markdown
# 环境安装任务

创建时间：{ISO8601}
项目根目录：{project_root}

## 任务清单

- [ ] {缺失环境1} ({安装方式})
- [ ] {缺失环境2} ({安装方式})

## 安装说明

| 环境 | 安装方式 | 是否需要 sudo |
|------|----------|---------------|
| {环境1} | {方式} | 是/否 |
| {环境2} | {方式} | 是/否 |
```

2. **返回 need_env 状态**：

```yaml
status: need_env
env_file: "Record/env.md"
missing_items:
  - name: "Rust"
    install_method: "rustup"
    need_sudo: false
  - name: "libssl-dev"
    install_method: "apt"
    need_sudo: true
summary: "检测到 2 项环境缺失，已创建 Record/env.md"
```

3. **Claude 主对话收到 need_env 后**：
   - 自动启动 env-agent
   - env-agent 读取 Record/env.md 执行安装
   - env-agent 返回结果后，Claude 主对话判断：
     - success → 重新执行环境确认
     - need_sudo → 询问用户执行 sudo 命令，用户确认后重新执行
     - failed → 询问用户如何处理

## 通过条件

无缺失项时返回 success，自动进入下一步。

```yaml
status: success
summary: "环境检查通过，所有依赖已具备"
```

## env.md 任务文件示例

```markdown
# 环境安装任务

创建时间：2026-01-08T10:30:00+08:00
项目根目录：/home/user/my-project

## 任务清单

- [ ] Rust 工具链 (rustup)
- [ ] Node.js 18+ (nvm)
- [ ] libssl-dev (系统包)
- [ ] pkg-config (系统包)

## 安装说明

| 环境 | 安装方式 | 是否需要 sudo |
|------|----------|---------------|
| Rust | rustup | 否 |
| Node.js | nvm | 否 |
| libssl-dev | apt | 是 |
| pkg-config | apt | 是 |

## 备注

- 用户级安装优先（rustup、nvm、pip --user）
- 系统包需要 sudo，env-agent 会返回命令让用户手动执行
```

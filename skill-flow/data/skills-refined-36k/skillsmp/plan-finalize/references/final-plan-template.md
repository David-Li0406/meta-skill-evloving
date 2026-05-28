# 确定方案模板

> 说明：此文件写入`Record/plan/{plan_version}-plan.md`

```markdown
---
doc_type: plan
plan_version: v1
status: finalized
finalized_at: ISO8601
project_root: "<项目根目录>"
---

# 确定方案

## 需求摘要

- ...
- ...

## 最终scope

- allowed_paths:
  - ...
- forbidden_patterns:
  - ...
- dependencies:
  - ...
- max_review_rounds: ...

## 安全澄清（重要）

> **必须填写**：将讨论阶段已澄清的安全相关信息记录在此，子代理执行时需读取此章节

### 项目背景与授权

- 项目性质：（如：网络安全作业/CTF练习/渗透测试学习/安全研究等）
- 授权说明：（如：课程作业要求/自有环境测试/已获授权等）
- 目标环境：（如：本地虚拟机/自建靶机/课程提供的测试环境等）

### 已澄清的安全问题

| 问题 | 澄清结果 | 澄清时间 |
|------|----------|----------|
| 是否涉及真实攻击 | 否，仅用于学习/作业 | ... |
| 目标是否为自有/授权环境 | 是 | ... |
| ... | ... | ... |

### 子代理执行须知

- 子代理执行前必须读取本章节
- 本章节内容已在讨论阶段由用户确认
- 子代理不应因已澄清的安全问题拒绝执行

## 环境确认

- status: ready
- 确认时间: ...
- 环境清单: 见 ~/environment.md

## 编译配置

### 目标平台与架构

| 平台 | 架构 | 说明 |
|-----|------|------|
| Linux | x86_64 | 主要目标 |
| Windows | x86_64 | 可选 |

### 构建类型

- [ ] Debug
- [x] Release

### 编译顺序（多语言项目）

> 如果是多语言项目，按依赖关系排序

1. Rust 核心库（被其他模块依赖）
2. Python 绑定
3. 最终可执行文件

### 其他配置

- 链接方式：静态链接 / 动态链接
- 优化级别：-O2
- 交叉编译：无 / 有（说明）
- 编译器要求：gcc >= 11 / clang >= 14 / 无特殊要求

## 子代理分工

### 执行顺序（重要）

> **必须标记**：标明哪些子代理可并行，哪些必须串行等待依赖

| 阶段 | 子代理 | 依赖 | 说明 |
|------|--------|------|------|
| 1 | python-agent-01 | 无 | 可与阶段1其他子代理并行 |
| 1 | rust-agent-01 | 无 | 可与阶段1其他子代理并行 |
| 2 | c-agent-01 | python-agent-01 | 需要等待 python-agent-01 产出的文件 |
| 3 | build-agent-01 | 阶段1+2全部完成 | 最后执行 |

**执行规则**：
- 同阶段子代理可并行执行
- 不同阶段必须按顺序执行，后阶段等待前阶段全部完成
- 有明确依赖的子代理必须等待依赖完成

### 分工总览

| 运行槽位 | 子代理 | proposal_id | 负责工作 | 阶段 |
|---------|-------|-------------|---------|------|
| python-agent-01 | python-agent | xxx-python-agent | 模块A实现 | 1 |
| rust-agent-01 | rust-agent | xxx-rust-agent | 核心逻辑实现 | 1 |
| build-agent-01 | build-agent | xxx-build-agent | 构建与产物输出 | 3 |

### 详细分工

#### python-agent-01（由python-agent执行）

- **负责工作**：模块A实现
- **具体任务**：
  - ...
  - ...
- **输出**：源代码（不编译）

#### rust-agent-01（由rust-agent执行）

- **负责工作**：核心逻辑实现
- **具体任务**：
  - ...
  - ...
- **输出**：源代码（不编译）

#### build-agent-01（由build-agent执行）

- **负责工作**：构建与产物输出
- **构建命令**：`cargo build --release` / `pnpm build` / ...
- **目标产物**：
  - 路径：`target/release/xxx` / `dist/` / ...
  - 类型：可执行文件 / 静态库 / Web应用 / ...
- **依赖**：所有编程子代理完成后执行

### 启动命令

> 在 Claude 对话中复制粘贴以下命令启动子代理：

**编程子代理（可并行）：**
```
使用 python-agent 执行 proposal_id: xxx-python-agent
```

```
使用 rust-agent 执行 proposal_id: xxx-rust-agent
```

**构建子代理（编程子代理完成后执行）：**
```
使用 build-agent 执行 proposal_id: xxx-build-agent
```

（根据实际分工表生成对应命令）

### 运行槽位说明

- 运行槽位（如python-agent-01/02）仅用于分工标记和提案区分
- 用户实际操作：开多个同名子代理会话
- 例如：需要python-agent-01和python-agent-02时，用户开两个`python-agent`会话

## 用户确认记录

- 确认时间: ...
- 确认方式: 用户选择"同意按当前方案执行"
- 讨论归档: Record/plan/{plan_version}-discussion.md

## 下一步

进入循环B：
1. plan-agent创建openspec与提案
2. 用户启动子代理执行任务
3. plan-agent进行代码审核
4. 用户确认审核结果
```

# 编译提案模板（build-all-build-agent）

> 编译提案只有一个，包含所有语言的编译任务，由 build-agent 顺序执行。

---

## Scope 文档模板

```yaml
---
proposal_id: build-all-build-agent
plan_version: {active_plan_version}
required_agent: build-agent
doc_type: scope
created_at: {ISO8601}
depends_on:
  - {功能提案1的proposal_id}
  - {功能提案2的proposal_id}
  - ...
---

# Scope: build-all-build-agent

## 项目背景

### 项目名称
{项目名称}

### 项目目标
{整体项目要实现什么}

### 当前阶段
所有功能实现提案已完成，进入编译阶段

## 编译配置

### 目标平台与架构

| 平台 | 架构 | 产出文件名 |
|-----|------|-----------|
| Linux | x86_64 | {项目名}-linux-x64 |
| Windows | x86_64 | {项目名}-win-x64.exe |

### 构建类型

- Debug / Release / 两者都要

### 编译顺序

> 按依赖关系排序，先编译被依赖的模块

| 顺序 | 语言 | 模块 | 说明 | 来源提案 |
|-----|------|------|------|---------|
| 1 | Rust | core-lib | 核心库，被其他模块依赖 | impl-core-rust-agent |
| 2 | C | native-ext | 原生扩展 | impl-native-c-agent |
| 3 | Python | bindings | Python绑定 | impl-bindings-python-agent |
| 4 | - | final | 最终可执行文件 | - |

### 其他配置

- 链接方式：{静态/动态}
- 优化级别：{-O0/-O2/-O3}
- 编译器要求：{gcc >= 11 / clang >= 14 / 无特殊要求}

## 门禁配置

```json
{
  "plan_version": "{plan_version}",
  "required_agent": "build-agent",
  "allowed_paths": [
    "src/",
    "build/",
    "dist/",
    "Record/impl/"
  ],
  "forbidden_patterns": [
    "*.secret",
    ".env*",
    "Record/plan/*"
  ],
  "dependencies": [
    "gcc>=11",
    "cargo>=1.70",
    "python>=3.10"
  ],
  "inputs": [
    "src/**/*",
    "Cargo.toml",
    "setup.py",
    "Makefile"
  ],
  "outputs": [
    "dist/{产出文件}",
    "Record/impl/build-all-build-agent-impl.md"
  ],
  "max_review_rounds": 3
}
```

## 依赖的功能提案

> 编译提案必须等所有功能提案完成后才能启动

| proposal_id | 子代理 | 产出 | 状态要求 |
|-------------|-------|------|---------|
| {proposal_id_1} | python-agent | src/module_a/ | accepted |
| {proposal_id_2} | rust-agent | src/core/ | accepted |
| ... | ... | ... | accepted |

## 错误追溯映射

> 编译出错时，根据错误文件路径追溯责任提案

| 文件路径模式 | 责任提案 | 责任子代理 |
|-------------|---------|-----------|
| src/module_a/* | impl-module-a-python-agent | python-agent |
| src/core/* | impl-core-rust-agent | rust-agent |
| src/native/* | impl-native-c-agent | c-agent |

## 验收口径

- [ ] 所有目标平台编译成功
- [ ] 产出文件存在且可执行
- [ ] 无编译警告（或警告已记录并确认可接受）
- [ ] 产出文件大小合理

## 风险与注意事项

- 交叉编译可能需要额外工具链
- 多语言项目注意链接顺序
- 编译出错时必须输出错误追溯报告
```

---

## Plan 文档模板

```yaml
---
proposal_id: build-all-build-agent
plan_version: {plan_version}
required_agent: build-agent
doc_type: plan
created_at: {ISO8601}
---

# Plan: build-all-build-agent

## 任务概述

### 背景
所有功能实现提案已完成，需要编译生成最终产物。

### 目标
按编译配置生成所有目标平台的可执行文件/库。

### 范围
- 包含：编译、链接、打包
- 不包含：功能修改、代码重构

## 编译任务清单

### 任务1：编译 Rust 核心库

**命令**：
```bash
cd src/core && cargo build --release --target x86_64-unknown-linux-gnu
```

**预期产出**：`target/release/libcore.a`

**来源提案**：`impl-core-rust-agent`

### 任务2：编译 C 原生扩展

**命令**：
```bash
cd src/native && make release
```

**预期产出**：`build/native_ext.so`

**来源提案**：`impl-native-c-agent`

### 任务3：编译 Python 绑定

**命令**：
```bash
cd src/bindings && python setup.py build_ext --inplace
```

**预期产出**：`bindings/*.so`

**来源提案**：`impl-bindings-python-agent`

### 任务4：生成最终可执行文件

**命令**：
```bash
make dist
```

**预期产出**：`dist/{项目名}-linux-x64`

## 执行步骤

1. **检查依赖提案状态**
   - 读取 `Record/state.json`
   - 确认所有 `depends_on` 中的提案状态为 `accepted`
   - 如有未完成的提案，阻塞并报告

2. **按顺序执行编译任务**
   - 按"编译任务清单"顺序执行
   - 每个任务完成后记录结果
   - 任务失败时立即停止并输出错误报告

3. **验证产出**
   - 检查所有预期产出文件是否存在
   - 检查文件是否可执行（如适用）

4. **输出编译报告**
   - 成功：列出所有产出文件
   - 失败：输出错误追溯报告

## 错误处理

### 编译出错时必须输出

```markdown
## 编译错误报告

### 错误摘要
- 错误阶段：{任务名称}
- 错误类型：{编译错误/链接错误/...}

### 错误详情
- 文件：{文件路径}
- 行号：{行号}
- 错误信息：{错误信息}

### 责任追溯
- 责任提案：{proposal_id}
- 责任子代理：{子代理名}
- 追溯依据：根据错误文件路径 `{文件路径}` 匹配错误追溯映射

### 修复建议
- 用户需要通知 `{子代理名}` 修复 `{文件路径}` 中的问题
- 修复完成后重新启动 `build-agent` 执行编译
```

## 预期产出

| 文件路径 | 类型 | 说明 |
|---------|------|------|
| dist/{项目名}-linux-x64 | created | Linux x64 可执行文件 |
| dist/{项目名}-win-x64.exe | created | Windows x64 可执行文件 |
| Record/impl/build-all-build-agent-impl.md | created | 编译记录 |

## 验证方式

1. **文件存在性**：检查所有产出文件是否存在
2. **可执行性**：`chmod +x` 后能否运行
3. **基本功能**：`--version` 或 `--help` 能否正常输出
```

---

## 编译记录模板（build-agent 完成后产出）

```yaml
---
proposal_id: build-all-build-agent
plan_version: {plan_version}
agent: build-agent
doc_type: impl
status: completed | failed
started_at: {ISO8601}
completed_at: {ISO8601}
---

# 编译记录: build-all-build-agent

## 执行摘要

{成功：所有目标平台编译完成 / 失败：在xxx阶段出错}

## 编译结果

| 任务 | 状态 | 耗时 | 产出 |
|-----|------|------|------|
| Rust 核心库 | ✓ | 2m30s | target/release/libcore.a |
| C 原生扩展 | ✓ | 45s | build/native_ext.so |
| Python 绑定 | ✓ | 1m15s | bindings/*.so |
| 最终可执行文件 | ✓ | 30s | dist/{项目名}-linux-x64 |

## 产出文件

| 文件路径 | 大小 | 平台 | 架构 |
|---------|------|------|------|
| dist/{项目名}-linux-x64 | 12.5MB | Linux | x86_64 |
| dist/{项目名}-win-x64.exe | 14.2MB | Windows | x86_64 |

## 编译警告（如有）

{列出编译警告，或"无警告"}

## 错误报告（如失败）

{如果编译失败，包含完整的错误追溯报告}
```

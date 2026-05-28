---
name: multi-agent-dispatch
description: 多子代理并发任务分配。AI 拆分复杂任务，并发调用 codex exec，收集结果并审查。触发词：pai、派发、dispatch、分配、并发、多子代理。
---

# 多子代理并发任务分配

**核心理念**：AI 作为任务调度器，将复杂任务拆分成子任务，并发调用 Codex 执行，收集结果并审查。

## ⚠️ 核心原则

1. **同一窗口内完成**：不需要其他聊天窗口或额外端口
2. **AI 主导**：AI 负责拆分、分配、收集、审查
3. **并发执行**：多个 codex exec 并发运行，提高效率

---

## 使用方式

### 触发方式

```
dispatch: 审查 src/ 目录下所有 Python 文件
分配: 检查 bin/ 目录下的脚本质量
并发: 同时审查 3 个模块
```

---

## 执行流程

### 第一步：AI 分析任务复杂度

```
复杂任务 → AI 判断是否需要拆分
         → 如果需要，拆分成 N 个子任务
```

**拆分标准**：
- 文件数量 > 3 → 按文件拆分
- 任务类型多样 → 按类型拆分
- 范围过大 → 按模块拆分

### 第二步：AI 生成子任务提示词

```markdown
## 子任务 {n}/{total}

**目标**：{具体目标}
**范围**：{文件/模块/范围}
**输出格式**：{期望的输出格式}

请执行以上任务。
```

### 第三步：并发调用 codex exec

```bash
# AI 并发调用
codex exec -o /tmp/task1.md "子任务1提示词" &
codex exec -o /tmp/task2.md "子任务2提示词" &
codex exec -o /tmp/task3.md "子任务3提示词" &
wait
```

### 第四步：收集结果

```bash
# AI 读取所有结果
cat /tmp/task1.md
cat /tmp/task2.md
cat /tmp/task3.md
```

### 第五步：审查并汇报

AI 审查所有子任务结果：
1. 检查每个子任务是否完成
2. 检查结果是否符合预期
3. 整合结果
4. 汇报给用户

---

## 示例

### 示例 1：审查多个文件

**用户输入**：
```
dispatch: 审查 bin/ 目录下的 Python 脚本
```

**AI 执行**：

1. **分析**：bin/ 目录有 Python 文件，拆分成 2 个子任务

2. **生成子任务**：
   - 子任务1：审查 codex_loop.py, cunzhi.py
   - 子任务2：审查 cunzhi_hooks.py, cunzhi_utils.py, cunzhi-server.py

3. **并发调用**：
   ```bash
   codex exec -o /tmp/review1.md "Review codex_loop.py and cunzhi.py for code quality" &
   codex exec -o /tmp/review2.md "Review cunzhi_hooks.py, cunzhi_utils.py, cunzhi-server.py" &
   wait
   ```

4. **收集结果**：读取 review1.md 和 review2.md

5. **汇报**：
   ```
   ## 审查结果汇总
   
   | 子任务 | 文件 | 问题数 |
   |--------|------|--------|
   | 1 | codex_loop.py, cunzhi.py | 3 |
   | 2 | cunzhi_hooks.py 等 | 2 |
   
   **总计**：5 个问题
   ```

### 示例 2：并发执行不同类型任务

**用户输入**：
```
并发: 同时检查代码风格和安全问题
```

**AI 执行**：

1. **拆分**：
   - 子任务1：代码风格检查
   - 子任务2：安全问题检查

2. **并发调用**：
   ```bash
   codex exec -o /tmp/style.md "Check code style in src/" &
   codex exec -o /tmp/security.md "Check security issues in src/" &
   wait
   ```

3. **汇报**：整合两个维度的检查结果

---

## 智能拆分策略

| 任务类型 | 拆分方式 | 子任务数 |
|----------|----------|----------|
| 文件审查 | 按文件数量 | ceil(文件数/3) |
| 代码检查 | 按检查类型 | 类型数量 |
| 模块分析 | 按模块 | 模块数量 |

---

## 输出格式

**汇报模板**：

```markdown
## 多子代理任务完成

### 任务拆分

| 子任务 | 范围 | 状态 |
|--------|------|------|
| 1 | {范围1} | ✅ |
| 2 | {范围2} | ✅ |

### 结果汇总

{整合后的结果}

### 发现的问题

{如有问题，列出}
```

---

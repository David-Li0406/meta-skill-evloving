# 示例：实践中的文件规划

## 示例 1：研究任务

**用户请求：**"研究晨练的好处并写一个摘要"

### 循环 1：创建计划

```bash
Write task_plan.md
```

```markdown
# 任务计划：晨练好处研究

## 目标
创建关于晨练好处的研究摘要。

## 阶段
- [x] 阶段 1：创建此计划 ✓
- [ ] 阶段 2：搜索和收集来源
- [ ] 阶段 3：综合发现
- [ ] 阶段 4：交付摘要

## 关键问题
1. 身体健康的好处是什么？
2. 心理健康的好处是什么？
3. 有哪些科学研究支持这一点？

## 状态
**当前处于阶段 1** - 创建计划
```

### 循环 2：研究

```bash
Read task_plan.md           # 刷新目标
WebSearch "morning exercise benefits"
Write notes.md              # 存储发现
Edit task_plan.md           # 标记阶段 2 完成
```

### 循环 3：综合

```bash
Read task_plan.md           # 刷新目标
Read notes.md               # 获取发现
Write morning_exercise_summary.md
Edit task_plan.md           # 标记阶段 3 完成
```

### 循环 4：交付

```bash
Read task_plan.md           # 验证完成
Deliver morning_exercise_summary.md
```

---

## 示例 2：错误修复任务

**用户请求：**"修复认证模块中的登录错误"

### task_plan.md

```markdown
# 任务计划：修复登录错误

## 目标
识别并修复阻止成功登录的错误。

## 阶段
- [x] 阶段 1：理解错误报告 ✓
- [x] 阶段 2：定位相关代码 ✓
- [ ] 阶段 3：识别根本原因（当前）
- [ ] 阶段 4：实施修复
- [ ] 阶段 5：测试和验证

## 关键问题
1. 出现什么错误消息？
2. 哪个文件处理认证？
3. 最近有什么变化？

## 已做出的决策
- 认证处理器位于 src/auth/login.ts
- 错误发生在 validateToken() 函数中

## 遇到的错误
- [初始] TypeError: Cannot read property 'token' of undefined
  → 根本原因：用户对象未正确等待

## 状态
**当前处于阶段 3** - 发现根本原因，准备修复
```

---

## 示例 3：功能开发

**用户请求：**"在设置页面添加深色模式切换"

### 实践中的三文件模式

**task_plan.md:**

```markdown
# 任务计划：深色模式切换

## 目标
向设置中添加功能性的深色模式切换。

## 阶段
- [x] 阶段 1：研究现有主题系统 ✓
- [x] 阶段 2：设计实施方法 ✓
- [ ] 阶段 3：实施切换组件（当前）
- [ ] 阶段 4：添加主题切换逻辑
- [ ] 阶段 5：测试和完善

## 已做出的决策
- 使用 CSS 自定义属性作为主题
- 将偏好存储在 localStorage 中
- 切换组件位于 SettingsPage.tsx

## 状态
**当前处于阶段 3** - 构建切换组件
```

**notes.md:**

```markdown
# 笔记：深色模式实施

## 现有主题系统
- 位置：src/styles/theme.ts
- 使用：CSS 自定义属性
- 当前主题：仅浅色

## 需要修改的文件
1. src/styles/theme.ts - 添加深色主题颜色
2. src/components/SettingsPage.tsx - 添加切换
3. src/hooks/useTheme.ts - 创建新钩子
4. src/App.tsx - 用 ThemeProvider 包装

## 颜色决策
- 深色背景：#1a1a2e
- 深色表面：#16213e
- 深色文本：#eaeaea
```

**dark_mode_implementation.md:**（交付物）

```markdown
# 深色模式实施

## 所做的更改

### 1. 添加深色主题颜色
文件：src/styles/theme.ts
...

### 2. 创建 useTheme 钩子
文件：src/hooks/useTheme.ts
...
```

---

## 示例 4：错误恢复模式

当某事失败时，不要隐藏它：

### 之前（错误）

```text
Action: Read config.json
Error: File not found
Action: Read config.json  # 静默重试
Action: Read config.json  # 再次重试
```

### 之后（正确）

```text
Action: Read config.json
Error: File not found

# 更新 task_plan.md:
## 遇到的错误
- config.json 未找到 → 将创建默认配置

Action: Write config.json（默认配置）
Action: Read config.json
Success!
```

---

## 读取-决策-之前模式

**始终在重大决策前读取你的计划：**

```text
[已发生许多工具调用...]
[上下文变长...]
[原始目标可能被遗忘...]

→ Read task_plan.md          # 这将目标带回注意力中！
→ 现在做出决策              # 目标在上下文中是新鲜的
```

这就是 Manus 可以处理约 50 次工具调用而不失去跟踪的原因。计划文件充当"目标刷新"机制。

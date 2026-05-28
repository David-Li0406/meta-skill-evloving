---
name: systematic-debugging
description: 系统化调试流程，用于定位复杂 bug 的根因。包含五步法和调试策略。
当遇到难以复现、间歇性失败、或深层 bug 时使用。
Use when debugging complex issues, intermittent bugs, or performing root cause analysis.
allowed-tools: "Bash,Read,Write,Grep,mcp__tavily__tavily-search"
---

# Systematic Debugging - 系统化调试

系统化调试方法论，用于定位复杂 bug 的根本原因。

## 🎯 适用范围

**使用此技能**：
- ✅ 错误信息模糊或不明确
- ✅ 问题时好时坏、难以复现
- ✅ 多次尝试仍无法解决
- ✅ 需要深度分析根因

**先用 debug-patterns**：
- ❌ 有明确错误信息（curl 报错、编码错误）
- ❌ 快速诊断可以解决的技术问题

**协同流程**：
```
遇到错误
  ↓
错误信息明确？
  ├─ 是 → 先用 debug-patterns 快速诊断
  │         ↓
  │      解决了吗？
  │         ├─ 是 → 完成
  │         └─ 否 ↓
  └──────────────→ 使用 systematic-debugging 深度分析
```

---

## 调试五步法

```
1. 定义问题      2. 隔离范围      3. 列出假设
   ↓                ↓                ↓
   └────────────────────────────────┘
                 ↓
           4. 验证假设
                 ↓
           5. 确认根因 → 修复 → 验证
```

### 第一步：定义问题

**目标**：清晰描述问题，去除模糊表述

```bash
# ❌ 错误：模糊描述
"代码不工作"
"有个 bug"
"运行失败"

# ✅ 正确：精确描述
"调用 api/users/123 返回 500，预期 200"
"JSON 解析在第 42 行抛出 KeyError"
"偶发：每 10 次请求约 1 次超时"
```

**问题定义模板**：
```
- 什么操作：___________
- 预期结果：___________
- 实际结果：___________
- 频率：总是 / 间歇性 (___%) / 难复现
- 环境：OS/版本/依赖
```

---

### 第二步：隔离范围

**目标**：缩小问题范围，减少变量

#### 二分法

```python
# 怀疑长流程中某处出错？
# 从中间插入日志，确定问题在前半还是后半

def long_process(data):
    logger.info("Checkpoint 1: input=%s", data)  # 检查点 1
    result1 = step1(data)

    logger.info("Checkpoint 2: result1=%s", result1)  # 检查点 2
    result2 = step2(result1)

    logger.info("Checkpoint 3: result2=%s", result2)  # 检查点 3
    return step3(result2)

# 如果 checkpoint 2 打印了但 checkpoint 3 没打印 → 问题在 step2
```

#### 控制变量

```bash
# 测试不同输入组合
test_normal.py    # 正常输入 → 通过？
test_edge1.py     # 边界条件1 → 失败？
test_edge2.py     # 边界条件2 → 失败？
test_empty.py     # 空输入 → 失败？

# 找出最小复现用例
```

#### 环境隔离

```bash
# 本地可复现？
docker-compose up  # 清洁环境

# 生产环境问题？
- 检查日志差异
- 检查配置差异
- 检查数据差异
```

---

### 第三步：列出假设

**目标**：列出所有可能原因，按概率排序

```
假设清单示例：

| 假设 | 概率 | 验证方法 | 状态 |
|------|------|----------|------|
| 网络超时 | 高 | 检查网络日志 | 未验证 |
| 内存泄漏 | 中 | 检查内存使用 | 未验证 |
| 竞态条件 | 低 | 添加锁后测试 | 未验证 |
| 第三方库 bug | 低 | 降级库版本 | 未验证 |
```

**奥卡姆剃刀**：优先验证最简单的假设

---

### 第四步：验证假设

**目标**：设计实验验证或排除假设

```bash
# 实验 1：验证网络假设
curl -v https://api.example.com 2>&1 | grep -i timeout

# 实验 2：验证内存假设
heap_profiler record -- node app.js
# 检查内存增长曲线

# 实验 3：验证竞态假设
# 添加互斥锁
if (mutex.lock()) {
  critical_section();
  mutex.unlock();
}
# 重新测试，问题是否消失？
```

**验证原则**：
- 一次只验证一个假设
- 每个实验应该能明确排除/确认假设
- 保留实验记录（包括阴性结果）

---

### 第五步：确认根因 → 修复 → 验证

#### 根因确认标准

当修改后问题消失，且：
- ✅ 理解为什么这个修改能解决问题
- ✅ 修改最小化（没动无关代码）
- ✅ 相关测试通过

#### 修复前检查

```bash
# 1. 确认有测试覆盖这个 bug
grep -r "reproduces_issue_X" tests/

# 2. 修复前确保测试失败
npm test && echo "❌ 测试应该先失败！"

# 3. 应用修复
# 4. 测试通过 ✅
```

---

## 常见调试策略

### 策略 1： Rubber Ducking

向别人（或橡皮鸭）解释问题：

```
"好的，我调用这个函数，传入参数 X，
然后它在第 Y 行报错说 Z..."
```

通常说到一半就发现问题了。

### 策略 2：最小可复现用例

```python
# ❌ 复杂项目难以调试
# my_project/app/service/controller.py (500+ 行)

# ✅ 提取到独立脚本
# debug_repro.py
def reproduce():
    data = {"key": "problematic_value"}  # 最小输入
    result = function_under_test(data)
    return result

reproduce()  # 复现 bug
```

### 策略 3：二分日志注入

```bash
# 在可疑位置两侧添加日志
logger.debug("BEFORE: x=%s", x)
# ... 可疑代码 ...
logger.debug("AFTER: x=%s", x)

# 如果看到 BEFORE 但没有 AFTER → 问题在这段代码内
```

### 策略 4：版本回退

```bash
# 问题何时引入？
git bisect start
git bisect bad HEAD      # 当前版本有 bug
git bisect good tags/v1.0  # 旧版本正常

# 自动测试每个中间版本
git bisect run npm test

# 输出：首次引入 bug 的 commit
```

---

## 间歇性 Bug 专门处理

### 特征

- 难复现
- 时好时坏
- 可能是：竞态条件、资源泄漏、时序依赖

### 处理方法

```bash
# 1. 增加日志记录完整上下文
logger.info("Full context: state=%s, thread=%s, timestamp=%s",
            state, thread_id, time.time())

# 2. 压力测试放大问题
for i in {1..1000}; do npm test; done

# 3. 使用工具检测
valgrind --leak-check=full ./program        # 内存泄漏
thread_sanitizer=1 ./program                # 竞态条件
strace -e trace=file ./program              # 文件操作

# 4. 添加延迟/随机性测试
sleep $((RANDOM % 100))  # 随机延迟可能触发竞态
```

---

## 与 debug-patterns 配合

| debug-patterns | systematic-debugging |
|:---|:---|
| **快速诊断手册** | **系统化调试流程** |
| 明确错误（curl、编码、JSON） | 复杂问题（偶发、难复现） |
| 秒级解决 | 分钟级分析 |
| 技术层面 | 逻辑层面 |

**使用原则**：
1. 有明确报错 → 先 `debug-patterns`
2. 搞不定或问题复杂 → `systematic-debugging`

---

## 调试禁令

- ❌ **严禁**在没有假设的情况下盲目改代码
- ❌ **严禁**一次修改多个地方
- ❌ **严禁**看到错误就堆 try-catch
- ❌ **严禁**根据巧合下结论（"改了这行就好了"）

---

## 常见触发场景

使用此技能时，你会听到：
- "找不到 bug 原因"
- "间歇性失败"
- "偶发 bug"
- "根因分析"
- "难以复现"
- "Complex bug"
- "Root cause analysis"
- "Intermittent failure"

---

## 调试工具参考

```bash
# 通用
strace -p <pid>              # 系统调用跟踪
ltrace -p <pid>              # 库调用跟踪
gdb -p <pid>                 # 附加调试器

# Node.js
node --inspect               # 启用调试协议
node --heap-prof             # 内存分析

# Python
python -m pdb script.py      # 调试器
python -m trace --trace script.py  # 执行跟踪

# 网络调试
curl -v https://api.example.com 2>&1 | tee curl.log
tcpdump -i any port 443      # 抓包
```

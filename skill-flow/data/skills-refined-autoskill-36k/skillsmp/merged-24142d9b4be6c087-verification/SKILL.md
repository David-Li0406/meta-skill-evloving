---
name: verification
description: Use this skill to ensure code quality through a structured verification loop that validates functionality, tests, and builds.
---

# Verification Skill

> **这是质量提升2-3倍的核心原则** — Boris Cherny  
> **如果AI不能验证自己的工作，质量就不稳定。**

## 验证流程

```
┌─────────────────────────────────────────┐
│           Verification Loop             │
├─────────────────────────────────────────┤
│                                         │
│  Execute ──→ Verify ──→ Pass? ──→ Done  │
│                 │                       │
│                 ↓ No                    │
│            Analyze                      │
│                 ↓                       │
│              Fix                        │
│                 │                       │
│                 ↓                       │
│         Retry (max 3)                   │
│                 ↓ Fail                  │
│         [VERIFICATION_FAILED]           │
│                                         │
└─────────────────────────────────────────┘
```

## 验证类型

### 1. 功能验证
- [ ] 代码修改是否生效？
- [ ] 功能是否按预期工作？
- [ ] 边界情况是否处理？

### 2. 测试验证
- [ ] 单元测试通过？
- [ ] 集成测试通过？
- [ ] 无回归？

### 3. 构建验证
- [ ] 编译成功？
- [ ] 无类型错误？
- [ ] 无Lint警告？

### 4. 运行时验证
- [ ] 应用能正常启动？
- [ ] 关键流程可用？
- [ ] 无控制台错误？

## 自我修复循环

```javascript
async function executeWithVerification(task) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    const result = await execute(task);
    
    if (await verify(result)) {
      return result; // 成功
    }
    
    if (attempt === 3) {
      // 请求人工介入
      await escalate({
        hook: "VERIFICATION_FAILED",
        attempts: 3
      });
    }
    
    task = await fix(task, analyze(result));
  }
}
```

## 验证清单

### 修改代码后
1. 读取修改后的代码，确认变更正确
2. 运行相关测试
3. 检查没有破坏其他功能
4. 更新任务状态

### 提交前
1. 所有测试通过
2. 无类型错误
3. 无Lint警告
4. 功能验证通过
5. 更新验证日志

## 验证日志

记录到 `.ai_state/active_context.md`:

```markdown
## 📝 验证日志

### [日期] T-001
- **状态**: ✅ 通过
- **测试**: 5/5 通过
- **验证方式**: 单元测试 + 手动验证
- **证据**: [截图/日志]
```

## 与Stop Hooks集成

验证失败3次 → 触发 [VERIFICATION_FAILED]  
→ 请求人工介入  
→ 等待用户决策

## 使用方式

```javascript
// 加载验证技能
skill.load("verification");

// 执行带验证的任务
verification.execute(task);

// 验证修改
verification.verify(changes);

// 记录验证结果
verification.log(result);
```
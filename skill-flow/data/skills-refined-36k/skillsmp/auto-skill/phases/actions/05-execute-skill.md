# Action: execute-skill

执行选定的 skill。

## 输入

- `state.selected_skill`: 用户选择的skill
- `state.user_request`: 用户原始请求

## 处理逻辑

```javascript
const skillName = state.selected_skill;

// 1. 检查skill是否已安装
if (!isSkillInstalled(skillName)) {
  throw new Error(`Skill ${skillName} 未安装`);
}

// 2. 使用 Skill tool 执行
try {
  const result = await Skill({
    skill: skillName,
    args: state.user_request
  });

  state.execution_status = "completed";
  return {
    success: true,
    skill: skillName,
    result: result
  };
} catch (error) {
  state.error_count++;
  return {
    success: false,
    error: error.message,
    suggestion: "请手动尝试执行该skill"
  };
}
```

## 执行流程

```
┌─────────────────────────────────────────────┐
│  1. 验证skill存在                            │
│     ↓                                        │
│  2. 读取skill配置                            │
│     ↓                                        │
│  3. 调用 Skill tool                          │
│     ↓                                        │
│  4. 返回结果给用户                           │
└─────────────────────────────────────────────┘
```

## 输出

- `state.execution_status = "completed"`
- 返回执行结果给用户

## 终止

→ 任务完成

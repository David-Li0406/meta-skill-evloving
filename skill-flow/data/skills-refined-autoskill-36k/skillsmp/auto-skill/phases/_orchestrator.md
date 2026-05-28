# Orchestrator - Auto Skill 编排器

## 状态管理

维护当前执行状态，根据状态选择下一个动作。

```javascript
// 状态结构
state = {
  user_request: string,           // 用户原始请求
  request_analysis: object,       // 请求分析结果（关键词、意图分类）
  matched_skills: array,          // 匹配到的本地skills
  search_results: array,          // skills.sh 搜索结果
  selected_skill: string|null,    // 用户选择的skill
  installation_status: string,    // 安装状态
  execution_status: string,       // idle|analyzing|matching|searching|installing|executing|completed|error
  error_count: number             // 错误计数
}
```

## 执行流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. analyze-request                                         │
│     ↓ 提取关键词、意图分类                                   │
├─────────────────────────────────────────────────────────────┤
│  2. match-local-skills                                      │
│     ↓ 扫描 ~/.claude/skills/ 和 .claude/skills/            │
├─────────────────────────────────────────────────────────────┤
│  3. 分支决策                                                │
│     ├─ 有匹配 → present-options(本地) → execute-skill      │
│     └─ 无匹配 → search-skills-sh → present-options(远程)   │
│                       ↓                                     │
│                 4. install-skill                           │
│                       ↓                                     │
│                 5. execute-skill                           │
└─────────────────────────────────────────────────────────────┘
```

## 动作选择规则

| 当前状态 | 可用动作 | 触发条件 |
|---------|---------|---------|
| idle | analyze-request | 收到用户请求 |
| analyzing | match-local-skills | 分析完成 |
| matching | present-options | 找到匹配项 |
| matching | search-skills-sh | 无本地匹配 |
| searching | present-options | 搜索完成 |
| presenting | install-skill | 用户选择远程skill |
| installing | execute-skill | 安装完成 |
| presenting | execute-skill | 用户选择本地skill |

## 终止条件

- `task_completed`: skill 执行成功
- `user_cancel`: 用户取消操作
- `error_limit`: 错误次数 >= 3

## 错误处理

```javascript
if (error_count >= 3) {
  state.execution_status = "error";
  return {
    message: "达到错误限制，请检查输入或手动操作",
    suggestions: ["检查网络连接", "手动访问 skills.sh", "查看已安装skills"]
  };
}
```

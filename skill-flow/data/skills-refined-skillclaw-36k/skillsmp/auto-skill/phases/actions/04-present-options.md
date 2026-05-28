# Action: present-options

向用户呈现可用的 skills 选项，使用 AskUserQuestion 获取选择。

## 输入

- `state.matched_skills`: 本地匹配的skills
- `state.search_results`: 远程搜索结果

## 处理逻辑

```javascript
// 1. 准备选项
if (state.matched_skills.length > 0) {
  // 呈现本地skills
  options = state.matched_skills.slice(0, 3).map(skill => ({
    label: skill.name,
    description: skill.description
  }));
  options.push({ label: "搜索更多", description: "在skills.sh上搜索" });
} else {
  // 呈现搜索结果
  options = state.search_results.slice(0, 3).map(skill => ({
    label: skill.name,
    description: `${skill.description} (需安装)`
  }));
}
options.push({ label: "取消", description: "退出当前操作" });

// 2. 询问用户
const choice = await AskUserQuestion({
  question: `为你找到以下相关 skills：`,
  header: "选择 Skill",
  options: options,
  multiSelect: false
});

// 3. 处理选择
state.selected_skill = choice;
state.execution_status = "presenting";
```

## 呈现格式

```
┌─────────────────────────────────────────────────────────┐
│  为你的需求找到以下相关 skills：                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ○ excel-stats                                          │
│    Excel 描述性统计分析工具，支持可视化                  │
│                                                         │
│  ○ data-analyzer                                        │
│    数据分析工作流，支持多格式输入                        │
│                                                         │
│  ○ 搜索更多                                             │
│    在 skills.sh 上搜索更多选项                           │
│                                                         │
│  ○ 取消                                                 │
│    退出当前操作                                         │
└─────────────────────────────────────────────────────────┘
```

## 输出

- `state.selected_skill`: 用户选择的skill
- `state.execution_status = "presenting"`

## 下一步

- 选择本地skill → [execute-skill](05-execute-skill.md)
- 选择远程skill → [install-skill](06-install-skill.md)
- 选择取消 → 终止

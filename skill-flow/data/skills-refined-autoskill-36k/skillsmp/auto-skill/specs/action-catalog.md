# Action 目录

| Action | 描述 | 前置条件 | 输出 |
|--------|------|---------|------|
| analyze-request | 分析用户请求，提取关键词和意图 | 收到用户请求 | request_analysis |
| match-local-skills | 扫描本地skills并计算匹配度 | 分析完成 | matched_skills |
| search-skills-sh | 从skills.sh搜索相关skills | 无本地匹配 | search_results |
| present-options | 使用AskUserQuestion呈现选项 | 有匹配或搜索结果 | selected_skill |
| install-skill | 安装选定的skill | 选择远程skill | installation_status |
| execute-skill | 执行选定的skill | skill已安装 | execution_result |

## 状态转换图

```
idle ──analyze-request──> analyzing
analyzing ──match-local-skills──> matching

matching ──有匹配──> presenting ──execute-skill──> completed
    │
    └──无匹配──> searching ──search-skills-sh──> presenting
                                          │
                                          └──install-skill──> executing
                                                                               └──execute-skill──> completed
```

## 错误恢复

| 错误场景 | 恢复策略 |
|---------|---------|
| 本地匹配失败 | 搜索远程 |
| 搜索失败 | 返回建议手动搜索 |
| 安装失败 | 提供手动安装命令 |
| 执行失败 | 显示错误信息，建议重试 |

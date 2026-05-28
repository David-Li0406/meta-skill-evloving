---
name: daily-report
description: Generate daily update reports for the Skills resource library. Records resource additions, modifications, and deletions for the day. Use when generating today's update report, tracking daily maintenance progress, or when the user asks for a daily summary of resource changes.
---

# 更新日报生成 Skill

## 描述

这个 Skill 生成资源库的每日更新报告，记录当天的资源添加、修改和删除操作。

## 用途

生成每日更新报告，便于跟踪资源库的维护进度和变化。

## 指令

当用户要求生成更新日报时，请按照以下规则操作：

### 日报内容结构

1. **日期信息**
   - 报告日期
   - 报告生成时间

2. **更新统计**
   - 新增资源数量
   - 修改资源数量
   - 删除资源数量（如有）

3. **详细更新列表**
   - 按分类列出所有更新
   - 每个更新包含：操作类型、资源标题、链接、简要说明

4. **更新摘要**
   - 主要更新内容
   - 重要资源亮点

5. **待办事项**
   - 需要后续处理的事项
   - 待验证的资源链接

### 数据来源

- 读取当天的 `CHANGELOG.md` 更新
- 对比资源文件的变化
- 分析新增、修改的资源

### 输出格式

```markdown
# Skills 资源库更新日报

**日期**：{YYYY-MM-DD}
**生成时间**：{HH:MM}

## 更新统计
- 新增资源：{数量}
- 修改资源：{数量}
- 删除资源：{数量}

## 详细更新列表

### 博客文章
- [新增] **{标题}**
  - 链接：{URL}
  - 说明：{简要说明}

### GitHub 仓库
- [新增] **{仓库名}**
  - 链接：{URL}
  - 说明：{简要说明}

### 视频教程
- [新增] **{视频标题}**
  - 链接：{URL}
  - 说明：{简要说明}

## 更新摘要
{主要更新内容的总结}

## 待办事项
- [ ] {待处理事项1}
- [ ] {待处理事项2}
```

## 示例

**用户输入：** "生成今天的更新日报"

**处理流程：**
1. 读取今天的更新记录
2. 统计更新数量
3. 按分类整理更新列表
4. 生成格式化的日报

**用户输入：** "生成昨天的更新日报"

**处理流程：**
1. 读取昨天的更新记录
2. 生成日报内容

## 自动化建议

- 可以设置定时任务自动生成日报
- 日报可以保存到 `community-resources/reports/` 目录
- 文件名格式：`daily-report-YYYY-MM-DD.md`

## 注意事项

- 确保更新记录的准确性
- 及时记录所有变更
- 包含待办事项提醒
- 保持日报格式一致

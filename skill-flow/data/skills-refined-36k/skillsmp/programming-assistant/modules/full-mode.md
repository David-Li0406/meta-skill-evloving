# 完整模式 (Full Mode)

适用于新建项目和功能开发场景。

## 状态文件

| 文件 | 用途 |
|------|------|
| `SOLUTION.md` | 架构设计、技术选型 |
| `TASK.md` | 任务拆解、实现步骤 |
| `feature_list.json` | 功能状态跟踪 |
| `progress.txt` | 会话进度日志 |

## 工作流程

### 1. 初始化（新项目首次）

```
分析需求 → 生成 SOLUTION.md
         → 生成 TASK.md
         → 创建 feature_list.json + progress.txt
         → 目录结构 + git init + 首次 commit
```

### 2. 开发循环

```
读取状态 → 选择任务(优先级最高的pending)
         → 实现功能(参考TASK.md)
         → 验证测试(失败则修复，3次失败则回退)
         → 更新状态(progress.txt + feature_list.json)
         → git commit
         → 继续下一任务或结束
```

## feature_list.json 格式

```json
{
  "project": "项目名称",
  "features": [
    {"id": "F001", "name": "功能名", "priority": 1, "status": "pending"}
  ]
}
```

## 代码实现规范

**实现前**: 阅读现有代码，确认技术方案
**实现中**: 遵循现有风格，一次只改一个功能点
**实现后**: 运行测试验证，检查回归

## 错误处理

1. 分析失败原因
2. 尝试不同方案（最多3次）
3. 连续失败：回退 + 记录 + 报告用户

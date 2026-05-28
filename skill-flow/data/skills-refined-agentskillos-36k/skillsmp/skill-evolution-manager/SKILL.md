---
name: skill-evolution-manager
description: Skill 进化管理器。当用户说"记住这个"、"保存经验"、"存储这个方案"、"复盘"、"总结经验"、"evolve"、"/evolve"、"学到了什么"、"记录这次的教训"时使用。支持经验提取、渐进式存储、按技术栈/上下文分类、按需加载。
license: MIT
---

# Skill Evolution Manager

AI 技能系统的"进化中枢"，支持渐进式经验加载。

## 核心职责

1. **经验提取**: 将用户反馈转化为结构化数据
2. **渐进式存储**: 按技术栈/上下文分类存储经验
3. **按需加载**: 仅在需要时加载相关经验

## 触发条件

- `/evolve`
- "记住这个"、"保存这个经验"
- 复杂问题修复成功后自动触发

## 工作流

### 1. 经验提取

扫描上下文 → 识别经验类型 → 分类存储

### 2. 存储命令

```bash
# 存储偏好
python scripts/store_experience.py --preference "偏好"

# 存储修复方案
python scripts/store_experience.py --fix "修复方案"

# 存储技术模式
python scripts/store_experience.py --tech <tech> --pattern "模式"

# 存储上下文触发
python scripts/store_experience.py --context <ctx> --instruction "指令"
```

### 3. 查询命令

```bash
python scripts/query_experience.py --tech react
python scripts/query_experience.py --context when_testing
python scripts/query_experience.py --search "关键词"
```

## 存储结构

```
experience/
├── index.json       # 索引摘要
├── tech/            # 按技术栈分类
│   ├── react.json
│   └── python.json
└── contexts/        # 按上下文分类
    └── when_testing.json
```

## 脚本

| 脚本 | 用途 |
|------|------|
| `merge_evolution.py` | 合并旧格式数据 |
| `smart_stitch.py` | 迁移到渐进式结构 |
| `trigger_detector.py` | 检测进化触发条件 |
| `align_all.py` | 批量对齐所有 Skill |

## 统一知识库集成 (新增)

### 进化时同步到统一知识库

当检测到进化触发时，除了更新本地 experience/ 外，还应同步到统一知识库：

```bash
# 分析会话内容并存储到统一知识库
cat session_content.txt | python knowledge-base/scripts/knowledge_summarizer.py \
  --auto-store \
  --session-id "{session_id}"
```

### 知识分类映射

| 本地经验类型 | 统一知识库分类 |
|--------------|----------------|
| preference | experience |
| fix | problem |
| tech pattern | tech-stack |
| context trigger | scenario |

### 工作流程

```
进化触发
    │
    ├── 本地存储 (experience/)
    │
    └── 同步到统一知识库 (knowledge-base/)
        │
        ├── 自动分类
        ├── 生成触发关键字
        └── 更新索引
```

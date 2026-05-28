---
name: skill-evolution
description: Skill 经验进化管理器。在对话结束时分析用户反馈，提取最佳实践和解决方案，持久化到 evolution.json 并缝合到 SKILL.md。当用户说"复盘"、"记录经验"、"保存这个技巧"、"evolve"时使用此工具。
---

# Skill Evolution Manager

Skill 系统的"进化中枢"。负责将对话中的经验教训持久化存储，并跨版本保留。

## 核心价值

**问题**: Skill 更新时，用户积累的最佳实践会丢失。

**解决方案**:
1. 将用户经验存储在独立的 `evolution.json` 文件中
2. 通过智能缝合将经验自动写入 SKILL.md
3. Skill 更新后，通过全量对齐恢复经验

## 核心功能

1. **复盘诊断**: 分析对话中的问题点和成功方案
2. **经验提取**: 将非结构化反馈转为结构化 JSON
3. **增量合并**: 去重合并新经验到 evolution.json
4. **智能缝合**: 将经验自动写入 SKILL.md 的专用章节
5. **跨版本对齐**: Skill 更新后重新缝合经验

## 使用场景

**触发方式**:
- `/skill-evolution` 或 `/evolve`
- "复盘一下刚才的对话"
- "记录一下这个经验"
- "把这个技巧保存到 Skill 里"
- "这个问题的解决方案要记住"

## 工作流程

### 步骤 1: 复盘诊断

Agent 分析当前对话，识别：
- **问题点**: 报错、参数错误、风格不对
- **成功方案**: 有效的解决方法、最佳实践
- **用户偏好**: 用户明确表达的喜好

### 步骤 2: 生成结构化 JSON

Agent 将提取的经验转换为 JSON 格式：

```json
{
  "preferences": [
    "用户希望下载时默认静音",
    "优先使用 mp4 格式"
  ],
  "fixes": [
    "Windows 下路径需要转义",
    "某些参数在 v2.0 后已弃用"
  ],
  "contexts": [
    "批量操作时需要添加 --batch 参数",
    "处理大文件时增加超时时间"
  ],
  "custom_prompts": "在执行前总是先打印预估耗时"
}
```

### 步骤 3: 增量合并

运行 `scripts/merge_evolution.py` 将经验合并到 evolution.json：

```bash
python scripts/merge_evolution.py <skill_dir> '<json_string>'
```

特性：
- 自动去重（相同内容不会重复添加）
- 保留历史记录
- 更新时间戳

### 步骤 4: 智能缝合

运行 `scripts/smart_stitch.py` 将经验写入 SKILL.md：

```bash
python scripts/smart_stitch.py <skill_dir>
```

生成的章节：

```markdown
## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: 此章节由 skill-evolution 自动维护，请勿手动编辑。

### User Preferences
- 用户偏好1
- 用户偏好2

### Known Fixes & Workarounds
- 修复方案1
- 修复方案2

### Context-Specific Notes
- 场景说明1
- 场景说明2

### Custom Instruction Injection
自定义指令内容...
```

### 步骤 5: 跨版本对齐

当 `skill-manager` 更新 Skill 后，运行全量对齐恢复经验：

```bash
python scripts/align_all.py <skills_dir>
```

## 脚本说明

| 脚本 | 功能 | 参数 |
|------|------|------|
| `merge_evolution.py` | 增量合并经验 | `<skill_dir> <json_string>` |
| `smart_stitch.py` | 缝合到 SKILL.md | `<skill_dir> [--dry-run] [--backup]` |
| `align_all.py` | 全量对齐 | `<skills_dir> [--dry-run] [--backup]` |

## evolution.json 格式

```json
{
  "preferences": ["string"],
  "fixes": ["string"],
  "contexts": ["string"],
  "custom_prompts": "string",
  "last_updated": "ISO-8601 datetime",
  "last_evolved_hash": "commit hash"
}
```

| 字段 | 说明 |
|------|------|
| `preferences` | 用户偏好列表 |
| `fixes` | 已知问题修复方案 |
| `contexts` | 特定使用场景说明 |
| `custom_prompts` | 自定义指令注入 |
| `last_updated` | 最后更新时间 |
| `last_evolved_hash` | 最后进化时的 source_hash |

## 最佳实践

1. **通过 evolution.json 修改**: 不要直接编辑 SKILL.md 中的经验章节，所有修改应通过 evolution.json
2. **定期复盘**: 每次使用 Skill 遇到问题或发现技巧时，及时记录
3. **更新后对齐**: 每次 skill-manager 更新 Skill 后，运行 align_all.py
4. **备份重要经验**: 使用 `--backup` 选项保护重要的经验数据

## 示例

### 示例 1: 记录用户偏好

```
用户: 记录一下，我希望下载视频时默认不带字幕

Agent:
1. 识别这是一个用户偏好
2. 生成 JSON: {"preferences": ["下载视频时默认不带字幕"]}
3. 运行 merge_evolution.py 合并到 yt-dlp 的 evolution.json
4. 运行 smart_stitch.py 更新 SKILL.md
```

### 示例 2: 记录问题修复

```
用户: 刚才那个路径问题，记住 Windows 下要用双反斜杠

Agent:
1. 识别这是一个修复方案
2. 生成 JSON: {"fixes": ["Windows 下路径使用双反斜杠转义"]}
3. 合并并缝合
```

### 示例 3: 批量对齐

```
用户: 我刚更新了几个 Skills，恢复一下经验

Agent:
1. 运行 align_all.py 扫描所有 Skills
2. 为每个有 evolution.json 的 Skill 重新缝合
3. 报告对齐结果
```

## 与其他 Skill 的协作

- **skill-factory**: 创建的 Skills 自动启用 evolution（`evolution_enabled: true`）
- **skill-manager**: 更新 Skill 后应调用 align_all.py 恢复经验
- **skill-creator**: 遵循相同的经验章节格式

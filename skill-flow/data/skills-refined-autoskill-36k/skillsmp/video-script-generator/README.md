# 视频脚本生成技能 (Video Script Generator)

## 功能概述

这个技能可以将文章内容转化为口播短视频脚本。它会：

1. **自动分析内容** - 判断是哪种脚本类型（A/B/C）
2. **应用对应模板** - 按照固定槽位生成脚本
3. **分析风格特征** - 基于7个维度分析原文风格
4. **生成结构化输出** - 默认输出 JSON 格式，便于系统集成

## 输出格式

### JSON 格式（默认）

技能默认输出结构化 JSON，包含三个主要部分：

1. **`final_script`** - 完整的可直接使用的脚本
   - 与元数据完全分离
   - 包含标题、分段、完整文本、字数统计、预估时长

2. **`metadata`** - 制作日志和风格分析
   - 7 维风格分析报告
   - 系统指令
   - 生成信息（时间、类型等）

3. **`templates`** - 可复用的模板库
   - 3 个开头模板
   - 3 个过渡模板
   - 3 个 CTA 模板

### Markdown 格式（兼容模式）

如需人类可读的 Markdown 格式（三部分输出），在请求中添加 `--format markdown`：

**示例**：`"把这篇文章做成视频脚本 --format markdown"`

## 三种脚本类型

### Type A：案件复盘（案例/反例）
讲一个真实案例：他以为稳 → 实际卡在一个缺口 → 给一句劝退规则 → 引导领"判断尺子卡片"自测

### Type B：咨询误解（高频问答）
拆一个常见提问：用户怎么问 → 错在哪 → 正确看什么 → 不纠正会白忙 → 引导领"尺子卡片"自查

### Type C：缺口模板（关键缺口/一票否决）
讲一个关键缺口：缺口是什么 → 不补会怎样 → 最低门槛是什么 → 补齐方向（不教学）→ 引导领"尺子卡片"对照

## 使用方法

### 基本用法（JSON 输出）

直接说：
- "把这篇文章做成视频脚本"
- "帮我生成口播脚本"
- "把这个案例改成短视频脚本"

然后粘贴你的文章内容。

**默认输出 JSON 格式**，便于直接提取脚本和集成到系统。

### 基本用法（Markdown 输出）

添加 `--format markdown` 标志：
- "把这篇文章做成视频脚本 --format markdown"
- "帮我生成口播脚本（保留原格式）"

输出人类可读的三部分 Markdown。

### 高级用法

指定类型：
- "用Type A模板，把这个案例改成脚本"
- "这是B类内容，帮我生成问答型脚本"

指定风格：
- "按照警示风格生成脚本"
- "用专业律师的口吻生成"

## 系统集成示例

### Python 集成

```python
import json
from datetime import datetime

# 假设这是从技能获取的 JSON 输出
output = claude_skill.generate(article_content)
data = json.loads(output)

# 提取最终脚本（可直接使用）
script = data['final_script']['full_text']
title = data['final_script']['title']
word_count = data['final_script']['word_count']
duration = data['final_script']['estimated_duration']

print(f"标题: {title}")
print(f"字数: {word_count}")
print(f"预估时长: {duration}秒")
print(f"\n脚本内容:\n{script}")

# 制作日志单独存储（可选）
metadata = data['metadata']
save_to_database({
    'style_analysis': metadata['style_analysis'],
    'generated_at': metadata['generation_info']['generated_at'],
    'script_type': metadata['generation_info']['script_type']
})

# 复用模板库
templates = data['templates']
hooks = templates['hooks']  # 3个开头模板
ctas = templates['ctas']    # 3个CTA模板
```

### JavaScript/Node.js 集成

```javascript
// 假设这是从技能获取的 JSON 输出
const output = await claudeSkill.generate(articleContent);
const data = JSON.parse(output);

// 提取最终脚本
const script = data.final_script.full_text;
const title = data.final_script.title;
const { word_count, estimated_duration } = data.final_script;

console.log(`标题: ${title}`);
console.log(`字数: ${word_count}`);
console.log(`预估时长: ${estimated_duration}秒`);
console.log(`\n脚本内容:\n${script}`);

// 保存制作日志到数据库
await saveToDatabase({
  styleAnalysis: data.metadata.style_analysis,
  generatedAt: data.metadata.generation_info.generated_at,
  scriptType: data.metadata.generation_info.script_type
});

// 复用模板库
const { hooks, transitions, ctas } = data.templates;
```

### cURL 命令行集成

```bash
# 生成脚本并保存到文件
echo "文章内容" | claude skill video-script-generator > script.json

# 提取脚本内容
cat script.json | jq '.final_script.full_text'

# 提取元数据
cat script.json | jq '.metadata'

# 只提取脚本标题
cat script.json | jq '.final_script.title'
```

## 输出内容

### JSON 格式输出

```json
{
  "version": "1.0.0",
  "script_type": "A",
  "final_script": {
    "title": "供应商货款拖了8个月，30万要不回来，问题出在哪？",
    "segments": [
      {
        "section": "hook",
        "text": "供应商货款拖了8个月，30万要不回来，问题出在哪？",
        "notes": "制造紧张感，引入案例"
      },
      {
        "section": "slot_1",
        "text": "他以为有合同、有验收单、有发票，这钱肯定能要回来。",
        "notes": "误判点"
      }
    ],
    "full_text": "供应商货款拖了8个月，30万要不回来，问题出在哪？\n\n他以为有合同...",
    "word_count": 198,
    "estimated_duration": 75
  },
  "metadata": {
    "style_analysis": {
      "persona_and_audience": {...},
      "tone_and_emotion": {...}
    },
    "system_instruction": "你是一个专业的回款律师...",
    "generation_info": {
      "script_type": "A",
      "generated_at": "2026-01-22T14:30:00Z",
      "input_summary": "供应商货款纠纷案例"
    }
  },
  "templates": {
    "hooks": ["...", "...", "..."],
    "transitions": ["...", "...", "..."],
    "ctas": ["...", "...", "..."]
  }
}
```

### Markdown 格式输出

技能会按顺序输出三部分：

#### Part A：风格画像报告
基于7个维度分析：
1. 人设与关系
2. 语气与情绪曲线
3. 口语节奏与句子结构
4. 用词与口头禅
5. 脚本结构母版
6. 论证与信息密度
7. 互动与指令性

#### Part B：系统指令
约300字的AI指令，用于指导生成同风格脚本：
- 用第二人称"你"
- 只写脚本内容，不涉及拍摄制作
- 包含开头钩子、段落顺序、句式模板、CTA写法

#### Part C：可直接套用的模板
- 3个脚本开头模板（Hook）
- 3个段落过渡模板
- 3个结尾CTA模板

## 示例

查看 `references/EXAMPLES.md` 获取完整示例。

## 文件结构

```
video-script-generator/
├── SKILL.md                      # 技能主文件
├── schema/                       # JSON Schema 定义
│   └── output-schema-v1.json     # 输出格式 Schema
└── references/                   # 参考资源
    ├── TEMPLATE_A.md             # Type A 详细模板和示例
    ├── TEMPLATE_B.md             # Type B 详细模板和示例
    ├── TEMPLATE_C.md             # Type C 详细模板和示例
    ├── STYLE_GUIDE.md            # 7维风格分析框架
    └── EXAMPLES.md               # 完整使用示例（JSON 和 Markdown）
```

## 注意事项

- 脚本长度：200-300字，适合60-90秒视频
- 口语化：短句为主，一逗到底
- CTA统一：指向《回款判断尺子卡》
- 风格一致：同批次脚本保持风格统一

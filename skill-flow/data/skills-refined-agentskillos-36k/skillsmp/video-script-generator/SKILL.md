---
name: "video-script-generator"
description: "Generate short video scripts for oral broadcast from article content. Automatically analyzes content and outputs scripts in one of three template types. Outputs style analysis report, system instruction, and ready-to-use templates. Use when user asks to convert articles or text into video scripts, oral broadcast scripts, or short video content."
---

This skill converts written articles into engaging short video scripts following specific templates and style guidelines.

## Input Sources

This skill can receive content from:

1. **Direct text input** - User provides article text directly
2. **From rss-article-retriever** - Chain call after retrieving RSS article

**When called from rss-article-retriever:**
- Extract `result.article.content.plain_text` from the RSS article output
- This field contains the cleaned article content ready for script generation
- Do not ask the user for content - use the provided plain_text directly

**Example chain:**
```
User: "请用最新一篇关于'民间借贷'的文章来制作视频脚本"

Step 1: rss-article-retriever skill
  → Outputs: <skill-output type="rss-article">...result.article.content.plain_text...</skill-output>

Step 2: video-script-generator skill (AUTOMATIC)
  → Extracts plain_text from step 1
  → Generates video script
  → Outputs: <skill-output type="video-script">...</skill-output>
```

## Workflow Overview

1. **Analyze Input Content** - Determine which script type (A/B/C) best matches the content
2. **Select Template** - Apply the appropriate 5-slot structure
3. **Generate Script** - Follow style guidelines for oral broadcast
4. **Output Deliverables** - Style report, system instruction, templates

## Script Type Classification

Analyze the input content and classify it into one of these three types:

### Type A: Case Review (案件复盘)
**When to use:** Content involves real stories/cases about business transactions, payment disputes, or recovery failures.

**Structure:**
1. 一句话案情: 什么交易 + 拖欠多久 + 大概多少钱
2. 误判点: 当事人以为稳在哪（一句）
3. 真卡点: 实际输在哪/缺口类型（主体/确认/执行/交付/关系）
4. 一句规则: 敢劝退门槛（一句）
5. 下一步动作: 私信【评估】领《回款判断尺子卡》（自查A/B/C+缺口Top3）

**Closing tone:** 用"故事"证明：别白忙，先用尺子看门槛。

### Type B: Consultation Misunderstanding (咨询误解)
**When to use:** Content addresses common questions, misconceptions, or "how to" queries in the domain.

**Structure:**
1. 用户原话/常见问法: 一句最常见问法
2. 误解点: 错把什么当成什么（一句）
3. 纠偏结论: 正确应该看什么关键点（一句）
4. 风险提示: 为什么会白忙/风险一句（1条）
5. 自查问题 + 动作: 问1个自查题 + 私信【评估】领《回款判断尺子卡》

**Closing tone:** 用"问答"让用户对号入座：你先自查，再决定要不要投入。

### Type C: Gap Template (关键缺口/一票否决)
**When to use:** Content highlights a critical gap, requirement, or deal-breaker that must be addressed.

**Structure:**
1. 缺口定义: 用大白话定义缺口（1句）
2. 不补后果: 会导致什么白忙/推进慢（1句）
3. 最低门槛: 至少补到什么程度才值得继续（1句）
4. 补齐方向: 往哪个方向补（不写步骤，1句）
5. 自查提示 + 动作: 一句自查提示 + 私信【评估】领《回款判断尺子卡》

**Closing tone:** 用"模板"给用户一把尺子：先对照门槛，看你缺不缺这一条。

## Style Analysis Requirements

When generating scripts, analyze the source content's style across these 7 dimensions (see [STYLE_GUIDE.md](references/STYLE_GUIDE.md) for detailed framework):

1. **Persona & Audience** - 人设与关系
2. **Tone & Emotional Arc** - 语气与情绪曲线
3. **Spoken Rhythm & Syntax** - 口语节奏与句子结构
4. **Vocabulary & Catchphrases** - 用词与口头禅
5. **Script Blueprint** - 脚本结构母版
6. **Reasoning Style** - 论证与信息密度
7. **CTA & Guidance** - 互动与指令性

## Output Protocol (机器集成协议)

**重要：此协议定义了 Skill 输出的边界标记，确保主 Agent 和应用程序能可靠地解析输出。**

### 边界标记规范

所有结构化输出**必须**包裹在以下标记中：

```
<skill-output type="video-script" schema-version="1.0.0">
{完整的 JSON，遵循 schema/output-schema-v1.json}
</skill-output>
```

**标记属性说明：**
| 属性 | 值 | 说明 |
|------|-----|------|
| `type` | `video-script` | 固定值，标识 Skill 类型 |
| `schema-version` | `1.0.0` | 对应 schema 版本，用于兼容性检查 |

### 解析规则（主 Agent/应用程序必读）

```
┌─────────────────────────────────────────────────────┐
│  Skill 完整输出                                      │
├─────────────────────────────────────────────────────┤
│  [可选] 解释性文字（应被忽略）                        │
│                                                      │
│  <skill-output type="video-script" schema-version="1.0.0">
│  {                                                   │
│    "version": "1.0.0",                              │
│    "script_type": "A",                              │
│    "final_script": { ... },  ← 干净脚本              │
│    "metadata": { ... },      ← 推理过程/元数据       │
│    "templates": { ... }                             │
│  }                                                   │
│  </skill-output>                                     │
│                                                      │
│  [可选] 补充说明（应被忽略）                          │
└─────────────────────────────────────────────────────┘
```

**主 Agent 解析逻辑：**
1. 提取 `<skill-output ...>` 和 `</skill-output>` 之间的内容
2. 解析为 JSON
3. 使用 schema 验证（可选但推荐）
4. **标记外的所有内容应被忽略**

### 输出模式

| 模式 | 触发方式 | 输出内容 | 使用场景 |
|------|---------|---------|---------|
| **默认模式** | 无参数 | 边界标记 + JSON + 可选说明 | SaaS 集成、主 Agent 调用 |
| **原始模式** | `--raw` | 纯 JSON（无标记、无说明） | API 直接调用、测试 |
| **人类模式** | `--format markdown` | Markdown 格式（无 JSON） | CLI 交互、人类阅读 |

### 前端渲染建议

```
┌─────────────────────────────────────────────────────┐
│  前端主展示区                                        │
│  └─ final_script.full_text（干净脚本）               │
│  └─ final_script.word_count / estimated_duration     │
├─────────────────────────────────────────────────────┤
│  [折叠] 制作过程                                     │
│  └─ metadata.style_analysis（7维分析）               │
│  └─ metadata.generation_info（生成信息）             │
│  └─ metadata.system_instruction（系统指令）          │
├─────────────────────────────────────────────────────┤
│  [折叠] 模板库                                       │
│  └─ templates.hooks / transitions / ctas             │
└─────────────────────────────────────────────────────┘
```

---

## Output Format

This skill outputs structured **JSON by default** for system integration.

### JSON Output Structure

The JSON output contains three main sections:

1. **`final_script`** - The complete, ready-to-use script
   - Isolated from metadata for direct use
   - Includes title, segments, full text, word count, and estimated duration

2. **`metadata`** - Style analysis and generation logs
   - Production process information
   - 7-dimension style analysis report
   - System instruction for AI

3. **`templates`** - Reusable template library
   - 3 hooks, 3 transitions, 3 CTAs

### Markdown Output (Legacy Format)

To request human-readable Markdown format (3-part output), add `--format markdown` to your request:

**Example:** "把这篇文章做成视频脚本 --format markdown"

The Markdown format includes:
- Part A: Style Profile Report
- Part B: System Instruction
- Part C: Ready-to-Use Templates

---

## Pre-Generation Checklist

在生成输出之前，必须完成以下检查：

1. **读取 Schema 文件**
   - 读取 `schema/output-schema-v1.json`
   - 确认所有必填字段
   - 注意字段格式要求

2. **参考示例输出**
   - 读取 `references/EXAMPLES.md`
   - 对照标准 JSON 结构

3. **格式要求确认**
   - `version` 必须使用语义化版本格式 `"1.0.0"`
   - `system_instruction` 必须控制在 200-500 字符
   - 每个 style_analysis 维度的 `rules` 数量为 2-5 条
   - `templates` 中 hooks/transitions/ctas 各必须恰好 3 条

---

## Output Requirements

### For JSON Output (Default)

Generate structured JSON output according to the schema defined in `schema/output-schema-v1.json`:

#### 1. final_script (Required)
Extract the complete script with the following fields:
- **`title`**: Script title or hook line
- **`segments`**: Array of script sections, each with:
  - `section`: Section type ("hook", "slot_1"-"slot_5", "closing")
  - `text`: Text content of the segment
  - `notes` (optional): Notes for this segment
- **`full_text`**: Complete script as plain text (ready for direct use)
- **`word_count`**: Estimated word count
- **`estimated_duration`**: Duration in seconds (word_count ÷ 2.5 for typical speech rate)

#### 2. metadata (Required)
Place ALL production logs and analysis in metadata:
- **`style_analysis`**: 7-dimension analysis (persona_and_audience, tone_and_emotion, rhythm_and_syntax, vocabulary, structure, reasoning, cta_and_guidance)
  - Each dimension should include: summary, rules (2-5 items), sentence_patterns
- **`system_instruction`**: ~300-word AI instruction for generating scripts in the same style
- **`generation_info`**: script_type, generated_at, input_summary, model_version

#### 3. templates (Required)
Provide exactly 3 templates for each:
- **`hooks`**: Opening hook templates
- **`transitions`**: Transition phrase templates
- **`ctas`**: Call-to-action templates

### For Markdown Output (--format markdown)

Output three parts in order:

#### Part A: Style Profile Report (风格画像报告)
Analyze the source content's style across the 7 dimensions listed above. Use clear lists and bullet points. For each dimension, provide:
- Feature summary (特征总结)
- 2-5 actionable rules (可操作规则)
- Typical sentence patterns (典型句式模板)

### Part B: System Instruction (系统指令)
Generate a ~300-word system instruction for AI to generate scripts in the same style. Requirements:
- Use second person "你" (you)
- Focus ONLY on script writing (structure, rhythm, sentences, transitions, tone, CTA)
- NO instructions about filming, lighting, BGM, or visual production
- Include: hook writing, paragraph order, sentence templates, word preferences/restrictions, CTA writing

### Part C: Ready-to-Use Templates
Provide 3 templates for each:
- 3 Hook templates (脚本开头模板)
- 3 Transition templates (段落过渡模板)
- 3 CTA templates (结尾CTA模板)

All templates must match the analyzed style.

---

## JSON Structure Guidelines

When generating JSON output, follow these guidelines:

1. **Extract final script into `final_script.full_text`**
   - This MUST be ready-to-use without any modifications
   - Combine all segments into a complete script
   - Ensure proper paragraph breaks and formatting

2. **Segment the script by sections in `final_script.segments`**
   - Each segment should have a clear section type (hook, slot_1-5, closing)
   - Include the text content for each segment
   - Add optional notes explaining the purpose of each segment

3. **Place ALL style analysis in `metadata.style_analysis`**
   - All 7 dimensions must be present
   - Each dimension should include: summary, rules (2-5), sentence_patterns
   - This is production metadata, separated from the final script

4. **Include system instruction in `metadata.system_instruction`**
   - Approximately 300 words
   - Focus on script writing only (no filming/lighting/BGM instructions)
   - Use second person "你" (you)

5. **Add templates to `templates.hooks/transitions/ctas`**
   - Exactly 3 templates for each category
   - Templates must match the analyzed style
   - Make them reusable for similar content

6. **Ensure all required fields are present**
   - Validate against schema before output
   - Check: version, script_type, final_script, metadata, templates

7. **Calculate metadata accurately**
   - `word_count`: Count actual words in the script
   - `estimated_duration`: Divide word_count by 2.5 (typical speech rate)
   - `generated_at`: Use current timestamp in ISO 8601 format

---

## Usage Examples

### 默认模式（SaaS 集成）

**User input:** "把这篇文章做成视频脚本"

**Output:**
```
<skill-output type="video-script" schema-version="1.0.0">
{
  "version": "1.0.0",
  "script_type": "A",
  "final_script": {
    "title": "...",
    "full_text": "完整脚本内容...",
    "segments": [...],
    "word_count": 248,
    "estimated_duration": 99
  },
  "metadata": {
    "style_analysis": {...},
    "system_instruction": "...",
    "generation_info": {...}
  },
  "templates": {
    "hooks": [...],
    "transitions": [...],
    "ctas": [...]
  }
}
</skill-output>
```

### 原始模式（API 直接调用）

**User input:** "把这篇文章做成视频脚本 --raw"

**Output:** 纯 JSON，无边界标记，无解释性文字
```json
{
  "version": "1.0.0",
  "script_type": "A",
  ...
}
```

### 人类模式（CLI 交互）

**User input:** "把这篇文章做成视频脚本 --format markdown"

**Output:** Markdown 格式的三部分报告（无 JSON）
- Part A: Style Profile Report
- Part B: System Instruction
- Part C: Ready-to-Use Templates

## Key Constraints

- Scripts must be suitable for ORAL broadcast (口语化)
- Total script length: ~200-300 words for 60-90 second videos
- Use short sentences, clear structure, strong hooks
- Always include CTA pointing to 《回款判断尺子卡》
- Maintain consistency between style analysis and generated content

## Schema Compliance

**必须严格遵守的格式要求：**

| 字段 | 格式要求 | 示例 |
|------|---------|------|
| `version` | 语义化版本 (semver) | `"1.0.0"` |
| `system_instruction` | 200-500 字符 | 约 150-250 字 |
| `rules` 数组 | 2-5 条 | 不多不少 |
| `hooks/transitions/ctas` | 各 3 条 | 不能多也不能少 |
| `generated_at` | ISO 8601 格式 | `"2026-01-22T14:30:00Z"` |

**常见错误：**
- ❌ `"version": "1.0"` → ✅ `"version": "1.0.0"`
- ❌ system_instruction 超过 500 字符 → ✅ 精简到 200-500 字符
- ❌ rules 只有 1 条 → ✅ 至少 2 条

## Reference Materials

- [TEMPLATE_A.md](references/TEMPLATE_A.md) - Type A detailed structure and examples
- [TEMPLATE_B.md](references/TEMPLATE_B.md) - Type B detailed structure and examples
- [TEMPLATE_C.md](references/TEMPLATE_C.md) - Type C detailed structure and examples
- [STYLE_GUIDE.md](references/STYLE_GUIDE.md) - Complete 7-dimension style analysis framework
- [EXAMPLES.md](references/EXAMPLES.md) - Concrete script examples for each type

---

## Integration Guide (主 Agent 集成指南)

### 主 Agent 调用示例

当你的 SaaS 主 Agent 调用此 Skill 时，应按以下方式处理输出：

```python
import re
import json
from typing import TypedDict, Optional

class VideoScript(TypedDict):
    title: str
    full_text: str
    segments: list
    word_count: int
    estimated_duration: float

class SkillOutput(TypedDict):
    version: str
    script_type: str
    final_script: VideoScript
    metadata: dict
    templates: dict

def parse_skill_output(raw_output: str) -> SkillOutput:
    """
    从 Skill 输出中提取结构化数据。

    Args:
        raw_output: Skill 的完整输出（包含边界标记）

    Returns:
        解析后的结构化数据

    Raises:
        ValueError: 如果找不到边界标记或 JSON 解析失败
    """
    # 1. 提取边界标记内的内容
    pattern = r'<skill-output[^>]*>([\s\S]*?)</skill-output>'
    match = re.search(pattern, raw_output)

    if not match:
        raise ValueError("No <skill-output> marker found in output")

    json_content = match.group(1).strip()

    # 2. 解析 JSON
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")

    # 3. 验证必要字段（可选，推荐使用 jsonschema 库）
    required_fields = ["version", "script_type", "final_script", "metadata", "templates"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    return data

def extract_for_frontend(skill_output: SkillOutput) -> dict:
    """
    提取前端渲染所需的数据结构。

    Returns:
        {
            "script": { ... },      # 主展示区
            "process": { ... },     # 折叠区：制作过程
            "templates": { ... }    # 折叠区：模板库
        }
    """
    return {
        # 主展示区：干净脚本
        "script": {
            "title": skill_output["final_script"]["title"],
            "content": skill_output["final_script"]["full_text"],
            "wordCount": skill_output["final_script"]["word_count"],
            "duration": skill_output["final_script"]["estimated_duration"],
            "segments": skill_output["final_script"]["segments"],
        },
        # 折叠区：制作过程元数据
        "process": {
            "scriptType": skill_output["script_type"],
            "styleAnalysis": skill_output["metadata"]["style_analysis"],
            "generationInfo": skill_output["metadata"]["generation_info"],
            "systemInstruction": skill_output["metadata"]["system_instruction"],
        },
        # 折叠区：模板库
        "templates": skill_output["templates"],
    }
```

### 前端 TypeScript 类型定义

```typescript
interface VideoScriptResult {
  // 主展示区
  script: {
    title: string;
    content: string;        // full_text，可直接渲染
    wordCount: number;
    duration: number;       // 秒
    segments: Array<{
      section: string;
      text: string;
      notes?: string;
    }>;
  };

  // 折叠区：制作过程
  process: {
    scriptType: 'A' | 'B' | 'C';
    styleAnalysis: Record<string, {
      summary: string;
      rules: string[];
      sentence_patterns: string[];
    }>;
    generationInfo: {
      script_type: string;
      generated_at: string;
      input_summary: string;
      model_version: string;
    };
    systemInstruction: string;
  };

  // 折叠区：模板库
  templates: {
    hooks: string[];
    transitions: string[];
    ctas: string[];
  };
}
```

### 错误处理建议

```python
def safe_call_skill(article_content: str) -> Optional[SkillOutput]:
    """带错误处理的 Skill 调用。"""
    try:
        # 1. 调用 Skill（通过你的主 Agent）
        raw_output = call_main_agent(f"把这篇文章做成视频脚本：\n{article_content}")

        # 2. 解析输出
        result = parse_skill_output(raw_output)

        # 3. 返回结构化数据
        return result

    except ValueError as e:
        # 解析失败，记录日志
        logger.error(f"Failed to parse skill output: {e}")
        return None

    except Exception as e:
        # 其他错误
        logger.error(f"Skill call failed: {e}")
        return None
```

### Schema 验证（推荐）

```python
import jsonschema

def validate_output(data: dict) -> bool:
    """使用 JSON Schema 验证输出。"""
    with open("schema/output-schema-v1.json") as f:
        schema = json.load(f)

    try:
        jsonschema.validate(data, schema)
        return True
    except jsonschema.ValidationError as e:
        logger.warning(f"Schema validation failed: {e.message}")
        return False
```

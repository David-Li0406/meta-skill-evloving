# 章节写作 Prompt 模板

现在需要撰写国家自然科学基金申报书的 **"{{section_title}}"** 部分。

## 项目基本信息

- **项目名称**：{{project_title}}
- **研究领域**：{{research_field}}
- **项目类型**：{{project_type}}
- **研究周期**：{{duration}}

## 研究内容概述

### 研究问题
{{research_problem}}

### 研究方法
{{research_method}}

### 创新点
{{innovation_points}}

{% if prior_work %}
### 前期工作
{{prior_work}}
{% endif %}

{% if team_info %}
### 团队信息
{{team_info}}
{% endif %}

## 本章节要求

### 章节说明
{{section_description}}

### 写作指导
{{section_writing_guide}}

### 字数要求
{{section_word_limit}}

### 评审要点
{{section_evaluation_points}}

{% if written_sections %}
## 已完成章节（供参考）

{% for section_id, content in written_sections.items() %}
### {{section_id}}
{{content}}

{% endfor %}
{% endif %}

## 写作任务

请根据以上信息，撰写"{{section_title}}"部分的内容。

**要求：**
1. 严格按照写作指导进行撰写
2. 控制在字数要求范围内
3. 内容要与已完成章节保持一致性
4. 突出本章节的评审要点
5. 语言专业、逻辑清晰

请直接输出该章节的内容，不需要额外说明。

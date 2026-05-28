请撰写"{{ section_title }}"部分。

## 章节要求
{{ section_description }}

## 写作指导
{{ section_writing_guide }}

## 字数要求
{{ section_word_limit }}

## 评审要点
{{ section_evaluation_points }}

{% if written_sections %}
## 已完成的章节
{% for sec_id, sec_content in written_sections.items() %}
### {{ sec_id }}
{{ sec_content[:500] }}...
{% endfor %}
{% endif %}

请直接输出该章节的内容，不要包含章节标题。

# Research Weekly Report Skill

<!--
一旦本文件夹有所变化，请更新本文档。
-->

将碎片化日报转换为结构化科研周报，支持9大核心板块、tags提取、LaTeX公式、图文联动。

**核心流程**: 日报 → 信息提取 → 板块填充 → 公式格式化 → 周报输出

## 文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 核心定义（工作流程、输出格式、核心规则） |
| `references/prompt.md` | 完整提示词 |
| `references/example_output.md` | 成品周报示例 |
| `references/obsidian_template.md` | Obsidian 模板 |
| `scripts/generate_weekly_report.py` | 自动化脚本 |

## 核心规则

- **Tags**：保留 `日志/周报`；过滤其他 `日志/` 前缀；提取非日志类 tags
- **时间**：`YYYY-MM-Do HH:mm:ss dddd`
- **图片**：正文"见图X"，附图索引插入
- **公式**：`$...$` 或 `$$...$$`
- **语气**：学术报告式 + 克制反思

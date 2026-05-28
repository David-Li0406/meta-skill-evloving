# Scripts

<!--
一旦本文件夹内容发生变化，请更新本文档。
-->

科研周报生成的辅助脚本。

## generate_weekly_report.py

周报模板生成脚本。

**功能**：
- 从日报 frontmatter 提取 tags（保留 `日志/周报`，过滤其他 `日志/` 前缀）
- 计算日期范围
- 生成符合 SKILL.md 格式的周报模板

**安装**：

```bash
pip install -r requirements.txt
```

**使用**：

```bash
# 基本用法
python generate_weekly_report.py --input daily-logs/

# 指定输出
python generate_weekly_report.py --input daily-logs/2026-01/ --output report.md

# 自定义路径
python generate_weekly_report.py --input daily-logs/ --base-path "/我的笔记/日志"
```

**参数**：
- `--input`：日报文件夹路径（必需）
- `--output`：输出路径（可选，默认自动计算）
- `--base-path`：Obsidian vault 基础路径（默认：/04_自我管理/00_日志）

## requirements.txt

依赖：`pyyaml>=6.0`、`python-frontmatter>=1.0.0`

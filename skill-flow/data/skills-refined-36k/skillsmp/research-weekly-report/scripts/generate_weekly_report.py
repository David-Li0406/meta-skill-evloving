#!/usr/bin/env python3
"""
科研周报生成辅助脚本

功能：
- 生成周报元数据（标题、日期范围、周次）
- 从日报文件中提取 tags
- 计算输出路径
- 生成周报模板结构

Input: 日报文件或文件夹路径
Output: 周报模板 Markdown 文件
Pos: 辅助 AI 生成周报的工具脚本，简化重复性任务
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Set, Dict, Tuple
import frontmatter
import yaml


def extractTagsFromDailyLogs(daily_log_paths: List[Path]) -> Set[str]:
    """
    从日报文件中提取 tags
    
    Args:
        daily_log_paths: 日报文件路径列表
    
    Returns:
        去重后的 tags 集合
    """
    all_tags = set()
    
    for log_path in daily_log_paths:
        if not log_path.exists():
            print(f"警告: 文件不存在 {log_path}", file=sys.stderr)
            continue
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
            if 'tags' in post.metadata:
                tags = post.metadata['tags']
                if isinstance(tags, list):
                    all_tags.update(tags)
                elif isinstance(tags, str):
                    all_tags.add(tags)
        except Exception as e:
            print(f"警告: 无法解析文件 {log_path}: {e}", file=sys.stderr)
    
    return all_tags


def calculateDateRange(daily_log_paths: List[Path]) -> Tuple[datetime, datetime]:
    """
    从日报文件名或内容中计算日期范围
    
    Args:
        daily_log_paths: 日报文件路径列表
    
    Returns:
        (开始日期, 结束日期)
    """
    dates = []
    
    for log_path in daily_log_paths:
        # 尝试从文件名提取日期（如：日报_260118.md）
        name = log_path.stem
        if '_' in name:
            date_part = name.split('_')[-1]
            try:
                # 尝试解析 YYMMDD 格式
                if len(date_part) == 6 and date_part.isdigit():
                    year = int('20' + date_part[:2])
                    month = int(date_part[2:4])
                    day = int(date_part[4:6])
                    dates.append(datetime(year, month, day))
            except ValueError:
                pass
        
        # 尝试从 frontmatter 提取日期
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            if '创建时间' in post.metadata:
                create_time = post.metadata['创建时间']
                if isinstance(create_time, str):
                    # 尝试解析多种日期格式
                    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']:
                        try:
                            dates.append(datetime.strptime(create_time.split()[0], fmt))
                            break
                        except ValueError:
                            continue
        except Exception:
            pass
    
    if not dates:
        # 如果没有找到日期，使用当前日期作为结束日期，7天前作为开始日期
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        return start_date, end_date
    
    return min(dates), max(dates)


def calculateWeekNumber(date: datetime) -> int:
    """
    计算日期所在的周次（一年中的第几周）
    
    Args:
        date: 日期
    
    Returns:
        周次
    """
    return date.isocalendar()[1]


def calculateOutputPath(base_path: str, date: datetime) -> Path:
    """
    计算周报输出路径
    
    Args:
        base_path: 基础路径（如：/04_自我管理/00_日志）
        date: 日期
    
    Returns:
        完整输出路径
    """
    year = date.strftime('%Y')
    month = date.strftime('%m')
    filename = f"周报_{date.strftime('%y%m%d')}.md"
    
    return Path(base_path) / year / month / filename


def formatDateWithOrdinal(dt: datetime) -> str:
    """
    格式化日期为 YYYY-MM-Do HH:mm:ss dddd 格式
    
    Args:
        dt: 日期时间对象
    
    Returns:
        格式化后的字符串，如 "2026-01-22nd 10:36:16 Thursday"
    """
    day = dt.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    return f"{dt.strftime('%Y-%m-')}{day}{suffix} {dt.strftime('%H:%M:%S %A')}"


def generateWeeklyReportTemplate(
    start_date: datetime,
    end_date: datetime,
    tags: Set[str],
    output_path: Path
) -> str:
    """
    生成周报模板内容
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        tags: 标签集合
        output_path: 输出路径
    
    Returns:
        周报模板 Markdown 内容
    """
    title = f"周报_{end_date.strftime('%y%m%d')}"
    now = formatDateWithOrdinal(datetime.now())
    
    # 确保包含 '日志/周报' tag
    tags_list = ['日志/周报']
    tags_list.extend(sorted([tag for tag in tags if tag != '日志/周报']))
    
    # 生成 frontmatter
    frontmatter_dict = {
        '标题': title,
        'tags': tags_list,
        '创建时间': now,
        '编辑时间': now
    }
    
    # 生成 YAML frontmatter
    frontmatter_yaml = yaml.dump(
        frontmatter_dict,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False
    )
    
    # 生成模板内容
    template = f"""---
{frontmatter_yaml.strip()}
---

<!-- markdownlint-disable MD024 -->

# {title}

**时间范围**：{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}
**关键进展摘要**：

- [待填充：摘要点1，体现本周核心突破]
- [待填充：摘要点2，体现思考与进步]

---

## 项目一：[项目名称]

### 1. 研究内容标题

[待填充：一句话概括]

### 2. 研究方法

- [待填充：算法/策略/实验设置] 【日期·分类】

### 3. 技术路线

- [待填充：实现步骤] 【日期·分类】

### 4. 核心模型

- **模型架构**：[待填充]
- **关键改动**：[待填充] 【日期·分类】

### 5. 仿真结果

- **核心指标**：[待填充] 【日期·分类】
- 训练曲线见图1

### 6. 存在问题

- [待填充：工程/实验问题] 【日期·分类】

### 7. 难点问题

- [待填充：理论/机制难点] 【日期·分类】

### 8. 解决思路

- [待填充：尝试与计划] 【日期·分类】

### 9. 小论文撰写任务

- **本周进度**：[待填充] 【日期·分类】
- **下周计划**：[待填充]

---

## 附图索引

- **图1**：[待填充：描述] 【日期·分类】

![[attachments/image.png|描述]]
"""
    
    return template


def main():
    parser = argparse.ArgumentParser(
        description='生成科研周报模板',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_weekly_report.py --input daily-logs/ --output weekly-report.md
  python generate_weekly_report.py --input daily-logs/2026-01/ --base-path "/04_自我管理/00_日志"
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='日报文件或文件夹路径'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径（可选，默认自动计算）'
    )
    
    parser.add_argument(
        '--base-path',
        type=str,
        default='/04_自我管理/00_日志',
        help='Obsidian vault 基础路径（默认: /04_自我管理/00_日志）'
    )
    
    args = parser.parse_args()
    
    # 获取日报文件列表
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入路径不存在 {input_path}", file=sys.stderr)
        sys.exit(1)
    
    if input_path.is_file():
        daily_log_paths = [input_path]
    else:
        # 递归查找所有 .md 文件
        daily_log_paths = list(input_path.glob('**/*.md'))
    
    if not daily_log_paths:
        print(f"错误: 未找到日报文件", file=sys.stderr)
        sys.exit(1)
    
    print(f"找到 {len(daily_log_paths)} 个日报文件")
    
    # 提取 tags
    tags = extractTagsFromDailyLogs(daily_log_paths)
    print(f"提取到 {len(tags)} 个 tags: {sorted(tags)}")
    
    # 计算日期范围
    start_date, end_date = calculateDateRange(daily_log_paths)
    print(f"日期范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
    
    # 计算输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = calculateOutputPath(args.base_path, end_date)
    
    print(f"输出路径: {output_path}")
    
    # 生成周报模板
    template = generateWeeklyReportTemplate(
        start_date=start_date,
        end_date=end_date,
        tags=tags,
        output_path=output_path
    )
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n✅ 周报模板已生成: {output_path}")
    print("\n下一步:")
    print("1. 使用 AI 根据日报内容填充各个板块")
    print("2. 格式化数学公式为 LaTeX 格式")
    print("3. 生成图片索引")
    print("4. 调整和完善周报内容")


if __name__ == '__main__':
    main()

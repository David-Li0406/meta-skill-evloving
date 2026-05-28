#!/usr/bin/env python3
"""
GitHub Code Review Report Generator (Chinese Format)

Generates Chinese-format Excel reports from GitHub pull requests with code review summaries.

Usage:
    python generator.py --repo linuxdeepin/dde-cooperation --since "2026-01-01" --module-name dde-cooperation
"""

import argparse
import fnmatch
import os
from datetime import datetime, timedelta
import json
import subprocess
import sys
from typing import List, Dict, Optional

try:
    import pandas as pd
except ImportError:
    print("❌ pandas not installed. Run: pip install pandas openpyxl")
    sys.exit(1)


# Problem Type Categories (15 types)
PROBLEM_TYPES = {
    1: "书写规范",
    2: "日志规范",
    3: "头文件规范",
    4: "变量规范",
    5: "常量规范",
    6: "宏定义规范",
    7: "指针规范",
    8: "代码安全漏洞",
    9: "代码冗余",
    10: "注释规范",
    11: "编译警告",
    12: "内存未释放",
    13: "提交内容规范",
    14: "不符合需求",
    15: "其他",
}

# Problem Source Categories (3 types)
PROBLEM_SOURCES = {
    1: "commit log",
    2: "代码",
    3: "注释",
}

# Severity Classification
SEVERITY_CRITICAL = "严重"
SEVERITY_GENERAL = "一般"

CRITICAL_TYPES = {8, 12}  # 代码安全漏洞, 内存未释放

# Valid AI reviewers (only these will be included)
VALID_AI_REVIEWERS = {"sourcery-ai"}


def get_problem_type_from_suggestion(suggestion: str) -> int:
    """
    Map review suggestion to problem type category.

    Returns problem type number (1-15).
    """
    suggestion_lower = suggestion.lower()

    # Direct keyword mapping
    type_keywords = {
        "安全": 8,
        "安全漏洞": 8,
        "漏洞": 8,
        "内存泄漏": 12,
        "内存": 12,
        "释放": 12,
        "注释": 10,
        "日志": 2,
        "编译": 11,
        "警告": 11,
        "头文件": 3,
        "变量": 4,
        "常量": 5,
        "宏": 6,
        "宏定义": 6,
        "指针": 7,
        "冗余": 9,
        "提交": 13,
        "需求": 14,
        "不符合需求": 14,
        "格式": 1,
        "命名": 1,
        "书写": 1,
    }

    for keyword, type_num in type_keywords.items():
        if keyword in suggestion_lower:
            return type_num

    return 15  # Default: 其他


def get_severity_from_problem_type(problem_type: int) -> str:
    """
    Determine severity based on problem type.

    Critical (严重): 代码安全漏洞(8), 内存未释放(12)
    General (一般): All other types
    """
    if problem_type in CRITICAL_TYPES:
        return SEVERITY_CRITICAL
    return SEVERITY_GENERAL


def is_valid_person_review(review_body: str, review_state: str) -> bool:
    """
    Check if review is a valid person review (not automated).

    Invalid reviews:
    - Body is empty or only contains "approved", "lgtm", "merge", etc.
    - State is COMMENTED (just comment, not a proper review)
    """
    if not review_body or review_body.strip() == "":
        return False

    review_lower = review_body.lower().strip()

    # Check for common automated approval phrases
    invalid_patterns = [
        "approved",
        "lgtm",
        "looks good to me",
        "merge",
        "force merge",
        "/merge",
        "/forcemerge",
        "mergeable",
        "ready to merge",
        "can merge",
    ]

    for pattern in invalid_patterns:
        if pattern in review_lower:
            return False

    # Check if it's too short (likely just an approval)
    if len(review_body) < 10:
        return False

    return True


def parse_time_range(time_expr: str) -> tuple[datetime, datetime]:
    """Parse relative time expressions to absolute date ranges."""
    time_expr = time_expr.lower().strip()
    today = datetime.now()

    if time_expr == "this month" or time_expr == "这个月":
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today
    elif time_expr == "last month" or time_expr == "上个月":
        first_day_this_month = today.replace(day=1)
        last_month_end = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_month_end.replace(day=1)
        start_date = first_day_last_month
        end_date = last_month_end
    elif time_expr == "last week" or time_expr == "上周":
        MONDAY = 0
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_sunday = last_monday + timedelta(days=6)
        start_date = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = last_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif time_expr == "this week" or time_expr == "本周" or time_expr == "这个星期":
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday)
        start_date = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today
    elif time_expr.startswith("last") and "day" in time_expr:
        days = int(time_expr.split()[1])
        start_date = today - timedelta(days=days)
        end_date = today
    elif "days ago" in time_expr:
        days = int(time_expr.split()[0])
        start_date = today - timedelta(days=days)
        end_date = today
    elif time_expr.startswith("last") and "week" in time_expr:
        weeks = int(time_expr.split()[1])
        days = weeks * 7
        start_date = today - timedelta(days=days)
        end_date = today
    else:
        raise ValueError(f"Unknown time expression: {time_expr}")

    return start_date, end_date


def format_date_only(iso_date: str) -> str:
    """
    Extract date portion only (YYYY-MM-DD) from ISO datetime string.

    Input: 2026-01-22T14:30:00Z
    Output: 2026-01-22
    """
    if not iso_date:
        return ""
    return iso_date.split('T')[0] if 'T' in iso_date else iso_date


def run_gh_command(args: List[str], json_output: bool = True) -> Dict | str:
    """Run gh CLI command and return output."""
    cmd = ["gh"] + args
    if json_output:
        cmd.extend(["--json", "number,title,author,createdAt,mergedAt,mergedBy,baseRefName,url,reviews,comments"])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        if json_output:
            return json.loads(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ gh command failed: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON output: {e}")
        print(f"stdout: {result.stdout}")
        sys.exit(1)


def should_include_reviewer(
    reviewer_name: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> bool:
    """Check if reviewer should be included based on patterns."""
    # Check if this is an AI reviewer (only valid AI reviewers allowed)
    if reviewer_name.lower() in VALID_AI_REVIEWERS:
        # Only include valid AI reviewers (sourcery-ai)
        return True

    # All other AI reviewers are excluded by default
    for ai_reviewer in VALID_AI_REVIEWERS:
        if reviewer_name.lower() != ai_reviewer:
            # This is NOT a valid AI reviewer, exclude it
            return False

    # Check explicit include/exclude patterns
    for pattern in (exclude_patterns or []):
        if fnmatch.fnmatch(reviewer_name.lower(), pattern.lower()):
            return False

    if include_patterns:
        for pattern in include_patterns:
            if fnmatch.fnmatch(reviewer_name.lower(), pattern.lower()):
                return True
        return False
    return True


def summarize_for_person(review_body: str) -> str:
    """
    Summarize person review: copy original text directly.

    Args:
        review_body: Original review content from person

    Returns:
        Original review text (no summarization)
    """
    return review_body.strip()


def generate_ai_impact_analysis(problem_description: str) -> str:
    """
    Generate AI impact analysis based on problem description.

    Args:
        problem_description: The problem description from AI review

    Returns:
        20-character Chinese summary of impact, or "无" if no impact
    """
    if not problem_description or len(problem_description.strip()) < 10:
        return "无"

    # Simple heuristic: check for impact keywords
    impact_keywords = [
        "影响", "隐患", "风险", "问题", "修复", "改进", "建议", "注意",
        "警告", "错误", "异常", "bug", "缺陷", "优化", "重构"
    ]

    for keyword in impact_keywords:
        if keyword in problem_description:
            # Extract 20 chars summary around impact keyword
            idx = problem_description.find(keyword)
            start = max(0, idx - 5)
            end = min(len(problem_description), idx + 20)
            summary = problem_description[start:end].strip()
            return summary

    # If no clear impact keyword found
    return "无"


def summarize_for_ai(review_body: str, max_length: int = 50) -> str:
    """
    Summarize AI review (sourcery-ai) to Chinese, max 50 characters.

    Args:
        review_body: AI review content
        max_length: Maximum length of summary

    Returns:
        Chinese summary of core points (≤50 chars)
    """
    # Remove code blocks and markdown
    lines = []
    in_code_block = False
    for line in review_body.split('\n'):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        elif not in_code_block and line.strip():
            lines.append(line.strip())

    text = ' '.join(lines)

    # Extract core points
    # Remove common prefixes
    prefixes_to_remove = ['Note:', 'Warning:', 'Suggestion:', '建议:', 'Fix:', 'Change:']
    for prefix in prefixes_to_remove:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()

    # Split into sentences
    sentences = []
    for sep in ['。', '.', '\n', ';']:
        parts = text.split(sep)
        sentences.extend([s.strip() for s in parts if s.strip()])

    # Filter meaningful sentences (exclude very short ones)
    meaningful_sentences = [s for s in sentences if len(s) > 10]

    # Take first meaningful sentences up to max_length
    result = ''
    for sentence in meaningful_sentences:
        if len(result) + len(sentence) > max_length:
            break
        result += sentence + '。' if result else sentence

    # Trim to max_length
    if len(result) > max_length:
        result = result[:max_length-3] + "..."

    return result.strip()


def extract_review_suggestions(
    pr_data: Dict,
    target_reviewers: Optional[List[str]] = None
) -> List[Dict]:
    """
    Extract valid review suggestions from PR reviews.

    Returns list of valid review dictionaries (one per valid reviewer per PR).
    Filters out:
    - Invalid automated reviews (approved, lgtm, merge, etc.)
    - Reviews without meaningful content
    - Non-valid AI reviewers (except sourcery-ai)

    Multiple valid reviewers per PR = multiple report rows for that PR.
    """
    valid_reviews = []

    for review in pr_data.get('reviews', []):
        author = review.get('author', {}).get('login', '')
        body = review.get('body', '')
        state = review.get('state', '')

        # Skip if no body or invalid automated review
        if not body:
            continue

        if not is_valid_person_review(body, state):
            continue

        # Filter by reviewer
        if not should_include_reviewer(author):
            continue

        problem_type = get_problem_type_from_suggestion(body)

        valid_reviews.append({
            'content': body,
            'problem_type': problem_type,
            'reviewer': author,
            'review_time': review.get('submittedAt', ''),
        })

    return valid_reviews


def generate_review_report(
    repo: str,
    time_expr: str,
    module_name: str,
    reviewer: str = "liuzheng",
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    base_branch: Optional[str] = None,
    limit: Optional[int] = None,
    output_file: Optional[str] = None
) -> str:
    """
    Generate Chinese-format Excel review report.

    Returns:
        Path to generated Excel file
    """
    start_date, end_date = parse_time_range(time_expr)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    print(f"📊 生成代码走查报告")
    print(f"   模块名: {module_name}")
    print(f"   时间范围: {start_date_str} to {end_date_str}")
    print(f"   仓库: {repo}")
    print(f"   Reviewer: {reviewer}")
    print()

    search_query = f"merged:{start_date_str}..{end_date_str}"
    if base_branch:
        search_query += f" base:{base_branch}"

    print("🔍 获取PR数据...")
    args = [
        "pr", "list",
        "--repo", repo,
        "--state", "merged",
        "--search", search_query,
    ]

    if limit:
        args.extend(["--limit", str(limit)])

    prs = run_gh_command(args, json_output=True)

    if not prs:
        print(f"⚠️ 未找到时间范围 {start_date_str} to {end_date_str} 内的PR")
        print("建议:")
        print("  - 扩大时间范围 (例如: 'last month' 代替 'this week')")
        print("  - 检查仓库名称是否正确")
        print("  - 确认PR已合并 (不仅仅是opened)")
        sys.exit(0)

    print(f"   找到 {len(prs)} 个PR")
    print()

    print("📝 处理PR并提取有效review...")
    rows = []
    serial_number = 0

    for i, pr in enumerate(prs, 1):
        print(f"   [{i}/{len(prs)}] PR #{pr['number']}: {pr['title'][:40]}...")

        pr_detail = run_gh_command(
            ["pr", "view", str(pr['number']), "--repo", repo],
            json_output=True
        )

        # Extract valid reviews (filters out automated approvals and invalid AI reviewers)
        valid_reviews = extract_review_suggestions(pr_detail)

        if not valid_reviews:
            print(f"      ⚠️ 无有效review")
            continue

        # Create one row per valid reviewer
        for review in valid_reviews:
            serial_number += 1

            problem_type = review['problem_type']
            severity = get_severity_from_problem_type(problem_type)
            reviewer = review['reviewer']

            # Determine summarization method and impact analysis
            is_ai_reviewer = reviewer.lower() in VALID_AI_REVIEWERS

            if is_ai_reviewer:
                # AI review: summarize to 50 chars
                chinese_summary = summarize_for_ai(review['content'], max_length=50)
                impact_analysis = generate_ai_impact_analysis(chinese_summary)
            else:
                # Person review: copy original text
                chinese_summary = summarize_for_person(review['content'])
                impact_analysis = chinese_summary

            created_at = pr.get('createdAt', '')
            merged_at = pr.get('mergedAt', '')
            review_time = review['review_time']

            author = pr.get('author', {}).get('login', '')
            merged_by = pr.get('mergedBy', {}).get('login', '')

            # Format dates to YYYY-MM-DD only (no time)
            created_date_only = format_date_only(created_at)
            merged_date_only = format_date_only(merged_at)
            review_date_only = format_date_only(review_time)

            problem_status = "关闭" if merged_at else "解决中"

            rows.append({
                '序号': serial_number,
                '包名': module_name,
                '仓库地址': f"https://github.com/{repo}",
                '代码提交地址': pr.get('url', ''),
                '问题来源': PROBLEM_SOURCES.get(3, '注释'),  # Reviews come from comments
                '问题描述': chinese_summary,
                '严重程度': severity,
                '影响分析': impact_analysis,
                '问题类型': PROBLEM_TYPES.get(problem_type, '其他'),
                '提出人': reviewer,
                '提出时间': review_date_only,
                '解决人': merged_by,
                '计划解决时间': merged_date_only,
                '实际解决时间': merged_date_only,
                '提出人确认是否验收通过': "是",
                '问题状态': problem_status,
            })

    print()

    if not rows:
        print(f"⚠️ 没有找到有效review记录")
        sys.exit(0)

    df = pd.DataFrame(rows)

    yyyymmdd = datetime.now().strftime("%Y%m%d")
    output_file = output_file or f"{module_name}-代码走查报告-{yyyymmdd}.xlsx"

    print("💾 生成Excel报告...")
    df.to_excel(output_file, index=False, engine='openpyxl')

    print()
    print("✅ 报告生成成功!")
    print(f"   文件: {output_file}")
    print(f"   模块名: {module_name}")
    print(f"   时间范围: {start_date_str} to {end_date_str}")
    print(f"   Review记录数: {len(rows)}")
    print(f"   Reviewer总数: {len(set(row['提出人'] for row in rows))}")

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='生成GitHub PR代码走查报告(中文格式)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 本月报告
  python generator.py --repo linuxdeepin/dde-cooperation --since "this month" --module-name dde-cooperation

  # 上周报告
  python generator.py --repo linuxdeepin/dde-cooperation --since "last week" --module-name dde-cooperation

  # 指定reviewer过滤
  python generator.py --repo linuxdeepin/dde-cooperation --since "last 15 days" --module-name dde-cooperation --reviewer liuzheng --include "sourcery-*" --exclude "*-bot"
        """
    )

    parser.add_argument(
        '--repo',
        required=True,
        help='GitHub仓库 (例如: linuxdeepin/dde-cooperation)'
    )

    parser.add_argument(
        '--since',
        default='this month',
        help='时间范围表达式 (默认: this month). 选项: "this month", "last month", "last week", "this week", "15 days ago", "2026-01-01..2026-01-31"'
    )

    parser.add_argument(
        '--module-name',
        required=True,
        help='模块名(项目名),用于生成文件名和包名列'
    )

    parser.add_argument(
        '--reviewer',
        default='liuzheng',
        help='Reviewer用户名 (默认: liuzheng)'
    )

    parser.add_argument(
        '--include',
        action='append',
        help='包含reviewer模式 (fnmatch风格, 可多次使用)'
    )

    parser.add_argument(
        '--exclude',
        action='append',
        help='排除reviewer模式 (fnmatch风格, 可多次使用)'
    )

    parser.add_argument(
        '--base',
        help='过滤基分支 (例如: master, main)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        help='限制PR处理数量'
    )

    parser.add_argument(
        '--output',
        help='输出Excel文件名'
    )

    args = parser.parse_args()

    generate_review_report(
        repo=args.repo,
        time_expr=args.since,
        module_name=args.module_name,
        reviewer=args.reviewer,
        include_patterns=args.include,
        exclude_patterns=args.exclude,
        base_branch=args.base,
        limit=args.limit,
        output_file=args.output
    )


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
issues.md 格式质量校验脚本
依据规范：.claude/skills/req-tester/ISSUES_TEMPLATE_SPEC.md
"""

import re
import sys
from typing import List, Dict, Tuple


# 常量定义
ALLOWED_CATEGORIES = {
    "前因后果",
    "边界定义",
    "异常场景",
    "交互细节",
    "数据状态",
    "性能兼容",
}

ALLOWED_PRIORITIES = {"critical", "warning", "info"}

REQUIRED_FIELDS = [
    "[位置]",
    "[来源]",
    "[测试视角]",
    "[需澄清]",
    "[回答建议]",
    "[产品回答]",
]


class ValidationError:
    """验证错误"""

    def __init__(self, issue_id: int, field: str, message: str):
        self.issue_id = issue_id
        self.field = field
        self.message = message

    def __str__(self):
        if self.issue_id:
            return f"❌ 问题 {self.issue_id} - {self.field}: {self.message}"
        else:
            return f"❌ {self.field}: {self.message}"


def validate_header(content: str) -> List[ValidationError]:
    """验证文档头部"""
    errors = []

    # 检查标题
    if not content.startswith("# 需求评审问题清单"):
        errors.append(
            ValidationError(0, "文档标题", "必须以「# 需求评审问题清单」开头")
        )

    # 提取头部信息
    header_pattern = r"> \*\*(.+?)\*\*: (.+)"
    headers = re.findall(header_pattern, content)
    header_dict = {k: v for k, v in headers}

    # 检查必填字段：只检查需求名称
    if "需求名称" not in header_dict:
        errors.append(ValidationError(0, "文档头部", "缺少「需求名称」字段"))
    elif not header_dict.get("需求名称", "").strip():
        errors.append(ValidationError(0, "文档头部", "「需求名称」不能为空"))

    return errors


def parse_issues(content: str) -> List[Tuple[int, str]]:
    """解析问题列表，返回 (问题编号, 问题内容) 的列表"""
    # 按 --- 分割
    parts = re.split(r"\n---\s*\n", content)

    issues = []
    for part in parts:
        # 查找问题标题
        title_match = re.search(r"## 问题 (\d+) \[(.+?) · (.+?)\]", part)
        if title_match:
            issue_id = int(title_match.group(1))
            issues.append((issue_id, part))

    return issues


def validate_issue_title(
    issue_id: int, content: str
) -> Tuple[str, str, List[ValidationError]]:
    """验证问题标题，返回 (分类, 优先级, 错误列表)"""
    errors = []

    # 提取标题
    title_match = re.search(r"## 问题 (\d+) \[(.+?) · (.+?)\]", content)
    if not title_match:
        errors.append(
            ValidationError(
                issue_id, "问题标题", "格式错误，应为「## 问题 N [分类 · 优先级]」"
            )
        )
        return "", "", errors

    parsed_id = int(title_match.group(1))
    category = title_match.group(2)
    priority = title_match.group(3)

    # 检查编号连续性
    if parsed_id != issue_id:
        errors.append(
            ValidationError(
                issue_id, "问题编号", f"编号不连续，期望 {issue_id}，实际 {parsed_id}"
            )
        )

    # 检查分类
    if category not in ALLOWED_CATEGORIES:
        errors.append(
            ValidationError(
                issue_id,
                "分类",
                f"「{category}」不在允许范围内，必须是：{', '.join(ALLOWED_CATEGORIES)}",
            )
        )

    # 检查优先级
    if priority not in ALLOWED_PRIORITIES:
        errors.append(
            ValidationError(
                issue_id,
                "优先级",
                f"「{priority}」不在允许范围内，必须是：{', '.join(ALLOWED_PRIORITIES)}",
            )
        )

    return category, priority, errors


def validate_field_location(issue_id: int, content: str) -> List[ValidationError]:
    """验证 [位置] 字段"""
    errors = []

    # 查找字段
    location_match = re.search(r"\*\*\[位置\]\*\* (.+)", content)
    if not location_match:
        errors.append(ValidationError(issue_id, "[位置]", "字段缺失"))
        return errors

    location = location_match.group(1)

    # 检查是否为空
    if not location.strip() or location.strip() == "待补充":
        errors.append(
            ValidationError(
                issue_id, "[位置]", "内容为空，必须标注页码或章节名称"
            )
        )

    return errors


def validate_field_source(issue_id: int, content: str) -> List[ValidationError]:
    """验证 [来源] 字段"""
    errors = []

    # 查找字段
    source_match = re.search(
        r"\*\*\[来源\]\*\*\s*\n(.+?)(?=\n\*\*\[|\n---|\Z)", content, re.DOTALL
    )
    if not source_match:
        errors.append(ValidationError(issue_id, "[来源]", "字段缺失"))
        return errors

    source_content = source_match.group(1)

    # 检查是否有引号包裹的原文
    if '"' not in source_content and '"' not in source_content and '"' not in source_content:
        errors.append(
            ValidationError(
                issue_id, "[来源]", "缺少引号包裹的原文引用"
            )
        )

    # 检查疑问点数量
    doubt_count = source_content.count("\n- ")
    if doubt_count < 2:
        errors.append(
            ValidationError(
                issue_id, "[来源]", f"疑问点不足，至少需要 2 个，当前 {doubt_count} 个"
            )
        )

    return errors


def validate_field_test_perspective(
    issue_id: int, content: str
) -> List[ValidationError]:
    """验证 [测试视角] 字段"""
    errors = []

    # 查找字段
    perspective_match = re.search(
        r"\*\*\[测试视角\]\*\*\s*\n(.+?)(?=\n\*\*\[|\n---|\Z)", content, re.DOTALL
    )
    if not perspective_match:
        errors.append(ValidationError(issue_id, "[测试视角]", "字段缺失"))
        return errors

    perspective_content = perspective_match.group(1)

    # 检查是否以"作为测试人员"开头
    if not re.search(r"作为测试人员", perspective_content):
        errors.append(
            ValidationError(
                issue_id, "[测试视角]", "必须以「作为测试人员，需要理解XX，才能：」开头"
            )
        )

    # 检查测试目的数量（有序列表）
    purpose_count = len(re.findall(r"\n\d+\. ", perspective_content))
    if purpose_count < 2:
        errors.append(
            ValidationError(
                issue_id,
                "[测试视角]",
                f"测试目的不足，至少需要 2 个，当前 {purpose_count} 个",
            )
        )

    return errors


def validate_field_clarifications(
    issue_id: int, content: str
) -> List[ValidationError]:
    """验证 [需澄清] 字段"""
    errors = []

    # 查找字段
    clarify_match = re.search(
        r"\*\*\[需澄清\]\*\*\s*\n(.+?)(?=\n\*\*\[|\n---|\Z)", content, re.DOTALL
    )
    if not clarify_match:
        errors.append(ValidationError(issue_id, "[需澄清]", "字段缺失"))
        return errors

    clarify_content = clarify_match.group(1)

    # 检查问题数量
    question_count = len(re.findall(r"\n\d+\. ", clarify_content))
    if question_count < 2:
        errors.append(
            ValidationError(
                issue_id,
                "[需澄清]",
                f"问题数量不足，至少需要 2 个，当前 {question_count} 个",
            )
        )

    # 检查每个问题是否以问号结尾
    questions = re.findall(r"\n\d+\. (.+)", clarify_content)
    for i, question in enumerate(questions, 1):
        if not question.strip().endswith("？") and not question.strip().endswith("?"):
            errors.append(
                ValidationError(
                    issue_id, "[需澄清]", f"第 {i} 个问题未以问号结尾：{question[:30]}..."
                )
            )

    return errors


def validate_field_suggestions(issue_id: int, content: str) -> List[ValidationError]:
    """验证 [回答建议] 字段"""
    errors = []

    # 查找字段
    suggestion_match = re.search(
        r"\*\*\[回答建议\]\*\*\s*\n(.+?)(?=\n\*\*\[|\n---|\Z)", content, re.DOTALL
    )
    if not suggestion_match:
        errors.append(ValidationError(issue_id, "[回答建议]", "字段缺失"))
        return errors

    suggestion_content = suggestion_match.group(1)

    # 检查建议数量（无序列表）
    suggestion_count = suggestion_content.count("\n- ")
    if suggestion_count < 2:
        errors.append(
            ValidationError(
                issue_id,
                "[回答建议]",
                f"建议数量不足，至少需要 2 个，当前 {suggestion_count} 个",
            )
        )

    return errors


def validate_field_answer(issue_id: int, content: str) -> List[ValidationError]:
    """验证 [产品回答] 字段"""
    errors = []

    # 查找字段
    answer_match = re.search(
        r"\*\*\[产品回答\]\*\*\s*\n(.+?)(?=\n---|\Z)", content, re.DOTALL
    )
    if not answer_match:
        errors.append(ValidationError(issue_id, "[产品回答]", "字段缺失"))
        return errors

    answer_content = answer_match.group(1)

    # 检查是否有注释占位符
    if "<!-- 在此填写 -->" not in answer_content:
        # 如果没有占位符，检查是否已填写答案
        if not answer_content.strip():
            errors.append(
                ValidationError(
                    issue_id,
                    "[产品回答]",
                    "既没有注释占位符，也没有填写答案",
                )
            )

    return errors


def validate_single_issue(issue_id: int, content: str) -> List[ValidationError]:
    """验证单个问题的所有字段"""
    errors = []

    # 验证标题
    _, _, title_errors = validate_issue_title(issue_id, content)
    errors.extend(title_errors)

    # 验证 6 个字段
    errors.extend(validate_field_location(issue_id, content))
    errors.extend(validate_field_source(issue_id, content))
    errors.extend(validate_field_test_perspective(issue_id, content))
    errors.extend(validate_field_clarifications(issue_id, content))
    errors.extend(validate_field_suggestions(issue_id, content))
    errors.extend(validate_field_answer(issue_id, content))

    return errors


def validate_issues_md(file_path: str) -> Tuple[bool, List[ValidationError]]:
    """验证整个 issues.md 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return False, [ValidationError(0, "文件", f"文件不存在：{file_path}")]
    except Exception as e:
        return False, [ValidationError(0, "文件", f"读取失败：{str(e)}")]

    all_errors = []

    # 验证头部
    all_errors.extend(validate_header(content))

    # 解析并验证所有问题
    issues = parse_issues(content)

    if not issues:
        all_errors.append(ValidationError(0, "问题列表", "未找到任何问题"))
        return False, all_errors

    # 验证每个问题
    for issue_id, issue_content in issues:
        all_errors.extend(validate_single_issue(issue_id, issue_content))

    # 验证问题编号连续性
    expected_ids = set(range(1, len(issues) + 1))
    actual_ids = {issue_id for issue_id, _ in issues}
    missing_ids = expected_ids - actual_ids
    if missing_ids:
        all_errors.append(
            ValidationError(
                0, "问题编号", f"编号不连续，缺失：{sorted(missing_ids)}"
            )
        )

    return len(all_errors) == 0, all_errors


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_issues.py <issues.md路径>")
        print("示例: python validate_issues.py cleaned-requirements/issues.md")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"📋 验证文件: {file_path}")
    print("=" * 60)

    passed, errors = validate_issues_md(file_path)

    if passed:
        print("✅ 格式验证通过！")
        print()
        print("所有必填字段完整，格式符合规范。")
        sys.exit(0)
    else:
        print(f"❌ 格式验证失败，发现 {len(errors)} 个问题：")
        print()

        # 按问题分组显示
        header_errors = [e for e in errors if e.issue_id == 0]
        issue_errors = [e for e in errors if e.issue_id > 0]

        if header_errors:
            print("【文档头部】")
            for error in header_errors:
                print(f"  {error}")
            print()

        if issue_errors:
            # 按问题 ID 分组
            issue_groups = {}
            for error in issue_errors:
                if error.issue_id not in issue_groups:
                    issue_groups[error.issue_id] = []
                issue_groups[error.issue_id].append(error)

            for issue_id in sorted(issue_groups.keys()):
                print(f"【问题 {issue_id}】")
                for error in issue_groups[issue_id]:
                    print(f"  {error}")
                print()

        print("=" * 60)
        print("请根据错误提示修正 issues.md，然后重新验证。")
        print("详细规范见：.claude/skills/req-tester/ISSUES_TEMPLATE_SPEC.md")
        sys.exit(1)


if __name__ == "__main__":
    main()

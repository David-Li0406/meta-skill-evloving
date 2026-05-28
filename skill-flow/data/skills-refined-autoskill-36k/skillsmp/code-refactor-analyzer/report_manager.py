#!/usr/bin/env python3
"""
报告管理模块 - 处理待办事项报告生成和完成情况验证

功能：
1. 生成待办事项报告
2. 验证报告完成情况
3. 管理报告文件
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json


class ReportManager:
    """报告管理器"""

    def __init__(self, repo_path: str = "."):
        """
        初始化报告管理器

        Args:
            repo_path: 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path).resolve()
        self.report_dir = self.repo_path / ".claude" / "code_refactor_report"

        # 确保报告目录存在
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, requirement: str) -> str:
        """
        清理文件名，移除无效字符

        Args:
            requirement: 用户需求描述

        Returns:
            清理后的文件名
        """
        # 移除特殊字符，只保留中文、英文、数字、空格、下划线、短横线
        sanitized = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9 _-]', '', requirement)
        # 替换多个空格为单个空格
        sanitized = re.sub(r'\s+', ' ', sanitized)
        # 限制长度（避免文件名过长）
        if len(sanitized) > 100:
            sanitized = sanitized[:97] + "..."
        return sanitized.strip()

    def generate_report_filename(self, requirement: str) -> str:
        """
        生成报告文件名

        Args:
            requirement: 用户需求描述

        Returns:
            报告文件名（不含路径）
        """
        # 清理需求文本
        sanitized_req = self._sanitize_filename(requirement)
        # 当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        # 生成文件名
        filename = f"{sanitized_req}-{current_date}.md"
        return filename

    def generate_report_path(self, requirement: str) -> Path:
        """
        生成报告完整路径

        Args:
            requirement: 用户需求描述

        Returns:
            报告完整路径
        """
        filename = self.generate_report_filename(requirement)
        return self.report_dir / filename

    def generate_todo_report(self, requirement: str, analysis_results: List[Dict]) -> str:
        """
        生成待办事项报告

        Args:
            requirement: 用户需求描述
            analysis_results: 分析结果列表

        Returns:
            报告内容（Markdown格式）
        """
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 统计信息
        total_tasks = len(analysis_results)
        high_priority = sum(1 for task in analysis_results if task.get("priority") == "high")
        medium_priority = sum(1 for task in analysis_results if task.get("priority") == "medium")
        low_priority = sum(1 for task in analysis_results if task.get("priority") == "low")

        # 构建报告内容
        report_lines = [
            f"# 重构需求：{requirement}",
            f"# 生成日期：{current_date}",
            f"# 状态：待处理",
            "",
            "## 摘要",
            f"- **总任务数**：{total_tasks}",
            f"- **高优先级**：{high_priority}",
            f"- **中优先级**：{medium_priority}",
            f"- **低优先级**：{low_priority}",
            f"- **预计工作量**：{self._estimate_effort(total_tasks, high_priority)}",
            "",
            "## 待办事项列表",
            ""
        ]

        # 按优先级分组
        priority_groups = {"high": [], "medium": [], "low": []}
        for task in analysis_results:
            priority = task.get("priority", "medium")
            priority_groups[priority].append(task)

        # 添加各优先级任务
        for priority_label, priority_name in [("high", "高优先级"), ("medium", "中优先级"), ("low", "低优先级")]:
            tasks = priority_groups[priority_label]
            if tasks:
                report_lines.append(f"### {priority_name}")
                report_lines.append("")

                for i, task in enumerate(tasks, 1):
                    file_path = task.get("file_path", "未知文件")
                    line_number = task.get("line_number", "?")
                    description = task.get("description", "未描述")
                    reason = task.get("reason", "需要重构以支持新需求")
                    suggestion = task.get("suggestion", "请根据需求进行适当修改")

                    report_lines.append(f"#### 任务 {i}")
                    report_lines.append(f"- [ ] **{file_path}:{line_number}** - {description}")
                    report_lines.append(f"  - **原因**：{reason}")
                    report_lines.append(f"  - **建议**：{suggestion}")
                    report_lines.append("")

        # 添加实施建议
        report_lines.extend([
            "## 实施建议",
            "",
            "### 1. 执行顺序",
            "1. 先完成高优先级任务",
            "2. 按模块分组执行相关任务",
            "3. 每完成一个任务进行测试",
            "4. 定期更新任务状态",
            "",
            "### 2. 测试策略",
            "- 每个重构任务完成后运行单元测试",
            "- 集成测试验证整体功能",
            "- 性能测试确保没有性能退化",
            "",
            "### 3. 代码审查",
            "- 每个任务完成后进行代码审查",
            "- 确保符合代码规范",
            "- 验证重构逻辑正确性",
            "",
            "## 进度跟踪",
            f"- **总任务数**：{total_tasks}",
            "- **已完成**：0",
            "- **进行中**：0",
            "- **未开始**：{total_tasks}",
            "- **完成率**：0%",
            "",
            "---",
            "*本报告由 Code Refactor Analyzer 技能生成*"
        ])

        return "\n".join(report_lines)

    def _estimate_effort(self, total_tasks: int, high_priority: int) -> str:
        """估算工作量"""
        if total_tasks == 0:
            return "无任务"

        # 简单估算：高优先级任务2小时，中优先级1小时，低优先级0.5小时
        estimated_hours = (high_priority * 2) + ((total_tasks - high_priority) * 0.75)

        if estimated_hours <= 4:
            return f"约{estimated_hours:.1f}小时（半天内）"
        elif estimated_hours <= 16:
            return f"约{estimated_hours:.1f}小时（2天内）"
        else:
            days = estimated_hours / 8
            return f"约{days:.1f}天（{estimated_hours:.1f}小时）"

    def save_report(self, requirement: str, analysis_results: List[Dict]) -> Tuple[Path, str]:
        """
        保存报告文件

        Args:
            requirement: 用户需求描述
            analysis_results: 分析结果列表

        Returns:
            (report_path, report_content)
        """
        # 生成报告内容
        report_content = self.generate_todo_report(requirement, analysis_results)

        # 生成报告路径
        report_path = self.generate_report_path(requirement)

        # 保存文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return report_path, report_content

    def validate_completion(self, report_path: Path) -> Dict[str, Any]:
        """
        验证报告完成情况

        Args:
            report_path: 报告文件路径

        Returns:
            验证结果字典
        """
        if not report_path.exists():
            return {
                "valid": False,
                "error": "报告文件不存在",
                "completion_rate": 0.0,
                "stats": {"total": 0, "completed": 0, "in_progress": 0, "pending": 0}
            }

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析任务状态
            task_pattern = r'- \[(x|X| )\]'
            tasks = re.findall(task_pattern, content)

            total_tasks = len(tasks)
            completed_tasks = sum(1 for status in tasks if status.lower() == 'x')

            # 查找进行中的任务（标记为斜体或特殊注释）
            in_progress_pattern = r'<!--\s*进行中\s*-->|\*进行中\*'
            in_progress_tasks = len(re.findall(in_progress_pattern, content))

            pending_tasks = total_tasks - completed_tasks - in_progress_tasks

            # 计算完成率
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

            # 提取报告信息
            requirement_match = re.search(r'# 重构需求：(.+)', content)
            date_match = re.search(r'# 生成日期：(.+)', content)
            status_match = re.search(r'# 状态：(.+)', content)

            return {
                "valid": True,
                "report_info": {
                    "requirement": requirement_match.group(1) if requirement_match else "未知",
                    "generated_date": date_match.group(1) if date_match else "未知",
                    "status": status_match.group(1) if status_match else "未知"
                },
                "completion_rate": round(completion_rate, 1),
                "stats": {
                    "total": total_tasks,
                    "completed": completed_tasks,
                    "in_progress": in_progress_tasks,
                    "pending": pending_tasks
                },
                "summary": self._generate_completion_summary(completion_rate, total_tasks, completed_tasks)
            }

        except Exception as e:
            return {
                "valid": False,
                "error": f"解析报告失败: {str(e)}",
                "completion_rate": 0.0,
                "stats": {"total": 0, "completed": 0, "in_progress": 0, "pending": 0}
            }

    def _generate_completion_summary(self, completion_rate: float, total: int, completed: int) -> str:
        """生成完成情况摘要"""
        if total == 0:
            return "没有找到待办事项"

        if completion_rate >= 100:
            return "🎉 所有任务已完成！"
        elif completion_rate >= 80:
            return f"👍 完成度良好 ({completed}/{total}，{completion_rate}%)，接近完成"
        elif completion_rate >= 50:
            return f"📊 完成过半 ({completed}/{total}，{completion_rate}%)，继续努力"
        elif completion_rate >= 20:
            return f"⏳ 已开始 ({completed}/{total}，{completion_rate}%)，需要加快进度"
        else:
            return f"🚧 刚开始 ({completed}/{total}，{completion_rate}%)，需要更多投入"

    def update_report_status(self, report_path: Path, completion_data: Dict) -> bool:
        """
        更新报告状态

        Args:
            report_path: 报告文件路径
            completion_data: 完成情况数据

        Returns:
            是否成功更新
        """
        if not report_path.exists():
            return False

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 更新进度跟踪部分
            stats = completion_data.get("stats", {})
            total = stats.get("total", 0)
            completed = stats.get("completed", 0)
            in_progress = stats.get("in_progress", 0)
            pending = stats.get("pending", 0)
            completion_rate = completion_data.get("completion_rate", 0.0)

            # 更新状态
            new_status = "已完成" if completion_rate >= 100 else "进行中"

            # 替换状态
            content = re.sub(r'# 状态：.+', f'# 状态：{new_status}', content)

            # 替换进度跟踪
            progress_section = (
                f"## 进度跟踪\n"
                f"- **总任务数**：{total}\n"
                f"- **已完成**：{completed}\n"
                f"- **进行中**：{in_progress}\n"
                f"- **未开始**：{pending}\n"
                f"- **完成率**：{completion_rate}%\n"
            )

            # 查找并替换进度跟踪部分
            progress_pattern = r'## 进度跟踪\n(?:- .+\n)+'
            if re.search(progress_pattern, content):
                content = re.sub(progress_pattern, progress_section, content)
            else:
                # 如果找不到，添加到文件末尾
                content = content.rstrip() + "\n\n" + progress_section

            # 保存更新后的文件
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception:
            return False

    def list_reports(self, days: int = 30) -> List[Dict]:
        """
        列出报告文件

        Args:
            days: 最近多少天的报告

        Returns:
            报告信息列表
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        reports = []

        for report_file in self.report_dir.glob("*.md"):
            # 检查文件修改时间
            file_mtime = report_file.stat().st_mtime
            if file_mtime < cutoff_date:
                continue

            # 读取文件基本信息
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    first_lines = [f.readline().strip() for _ in range(3)]

                requirement = first_lines[0].replace("# 重构需求：", "") if len(first_lines) > 0 else report_file.stem
                generated_date = first_lines[1].replace("# 生成日期：", "") if len(first_lines) > 1 else ""
                status = first_lines[2].replace("# 状态：", "") if len(first_lines) > 2 else ""

                # 验证完成情况
                completion_data = self.validate_completion(report_file)

                reports.append({
                    "file_name": report_file.name,
                    "file_path": str(report_file),
                    "requirement": requirement,
                    "generated_date": generated_date,
                    "status": status,
                    "modified_time": datetime.fromtimestamp(file_mtime).isoformat(),
                    "completion_rate": completion_data.get("completion_rate", 0.0),
                    "task_stats": completion_data.get("stats", {})
                })
            except Exception:
                continue

        # 按修改时间排序（最新的在前）
        reports.sort(key=lambda x: x["modified_time"], reverse=True)
        return reports


# 测试代码
if __name__ == "__main__":
    # 创建测试报告管理器
    manager = ReportManager()

    # 测试生成报告文件名
    test_req = "添加用户认证功能"
    filename = manager.generate_report_filename(test_req)
    print(f"报告文件名: {filename}")

    # 测试生成报告路径
    report_path = manager.generate_report_path(test_req)
    print(f"报告路径: {report_path}")

    # 测试生成报告内容
    test_results = [
        {
            "file_path": "src/auth.py",
            "line_number": 42,
            "description": "添加用户登录函数",
            "priority": "high",
            "reason": "当前没有用户认证功能",
            "suggestion": "实现基于JWT的认证"
        },
        {
            "file_path": "src/models.py",
            "line_number": 15,
            "description": "添加User模型",
            "priority": "high",
            "reason": "需要存储用户信息",
            "suggestion": "创建User类并添加必要字段"
        }
    ]

    report_content = manager.generate_todo_report(test_req, test_results)
    print(f"\n报告内容预览（前200字符）: {report_content[:200]}...")

    # 测试保存报告
    saved_path, saved_content = manager.save_report(test_req, test_results)
    print(f"\n报告已保存到: {saved_path}")

    # 测试验证完成情况
    completion_data = manager.validate_completion(saved_path)
    print(f"\n完成情况: {completion_data}")
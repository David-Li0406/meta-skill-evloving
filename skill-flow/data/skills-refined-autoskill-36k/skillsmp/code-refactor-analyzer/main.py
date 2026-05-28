#!/usr/bin/env python3
"""
主入口点 - 代码重构分析技能

功能：
1. 接收用户需求
2. 分析代码库
3. 生成待办事项报告或检查完成情况
4. 输出结果
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# 导入自定义模块
from code_analyzer import CodeAnalyzer
from report_manager import ReportManager
from state_manager import StateManager


class CodeRefactorAnalyzer:
    """代码重构分析器主类"""

    def __init__(self, repo_path: str = "."):
        """
        初始化分析器

        Args:
            repo_path: 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path).resolve()
        self.code_analyzer = CodeAnalyzer(str(self.repo_path))
        self.report_manager = ReportManager(str(self.repo_path))
        self.state_manager = StateManager(str(self.repo_path))

    def process_requirement(self, requirement: str, output_format: str = "text") -> Dict[str, Any]:
        """
        处理用户需求

        Args:
            requirement: 用户需求描述
            output_format: 输出格式（text, json, markdown）

        Returns:
            处理结果字典
        """
        # 检查需求状态
        is_first_use, existing_report_path = self.state_manager.check_requirement_status(requirement)

        if is_first_use or existing_report_path is None:
            # 首次使用或报告不存在 - 生成新报告
            return self._generate_new_report(requirement, output_format)
        else:
            # 后续使用 - 检查完成情况
            return self._check_completion(requirement, Path(existing_report_path), output_format)

    def _generate_new_report(self, requirement: str, output_format: str) -> Dict[str, Any]:
        """
        生成新报告

        Args:
            requirement: 用户需求描述
            output_format: 输出格式

        Returns:
            生成结果字典
        """
        # 分析代码库
        print(f"正在分析代码库以支持需求: {requirement}")
        analysis_results = self.code_analyzer.analyze_requirement(requirement)

        if not analysis_results:
            return {
                "status": "no_changes_needed",
                "requirement": requirement,
                "message": "未找到需要修改的代码。代码库可能已经支持该需求，或者需求描述不够具体。",
                "suggestions": [
                    "提供更详细的需求描述",
                    "指定具体的功能或模块",
                    "检查是否已实现类似功能"
                ]
            }

        # 生成分析摘要
        analysis_summary = self.code_analyzer.generate_analysis_summary(requirement, analysis_results)

        # 准备报告数据
        report_data = []
        for result in analysis_results:
            report_data.append({
                "file_path": result["file_path"],
                "line_number": result["line_number"],
                "description": f"修改 {result['node_type']} 以支持 {', '.join(result['matched_keywords'])}",
                "priority": result["priority"],
                "reason": f"代码行包含关键词: {', '.join(result['matched_keywords'])}",
                "suggestion": result["suggestion"]
            })

        # 保存报告
        report_path, report_content = self.report_manager.save_report(requirement, report_data)

        # 注册需求
        self.state_manager.register_requirement(requirement, str(report_path))

        # 生成输出
        if output_format == "json":
            return {
                "status": "report_generated",
                "requirement": requirement,
                "report_path": str(report_path),
                "analysis_summary": analysis_summary,
                "total_tasks": len(report_data),
                "priority_distribution": analysis_summary["priority_distribution"],
                "next_step": "使用相同需求再次调用以检查完成情况"
            }
        else:
            # 文本格式输出
            output_lines = [
                f"✅ 已生成重构待办事项报告",
                f"📋 需求: {requirement}",
                f"📁 报告文件: {report_path}",
                f"📊 分析摘要: {analysis_summary['summary']}",
                f"📝 总任务数: {len(report_data)}",
                f"🚨 高优先级: {analysis_summary['priority_distribution']['high']}",
                f"⚠️  中优先级: {analysis_summary['priority_distribution']['medium']}",
                f"📋 低优先级: {analysis_summary['priority_distribution']['low']}",
                "",
                "下一步:",
                "1. 查看报告文件中的具体任务",
                "2. 按优先级顺序完成任务",
                "3. 完成后使用相同需求再次调用以检查完成情况"
            ]

            return {
                "status": "report_generated",
                "output": "\n".join(output_lines),
                "report_path": str(report_path),
                "total_tasks": len(report_data)
            }

    def _check_completion(self, requirement: str, report_path: Path, output_format: str) -> Dict[str, Any]:
        """
        检查完成情况

        Args:
            requirement: 用户需求描述
            report_path: 报告文件路径
            output_format: 输出格式

        Returns:
            检查结果字典
        """
        # 验证完成情况
        completion_data = self.report_manager.validate_completion(report_path)

        if not completion_data["valid"]:
            return {
                "status": "error",
                "requirement": requirement,
                "error": completion_data.get("error", "验证报告失败"),
                "suggestion": "请重新生成报告"
            }

        # 更新报告状态
        self.report_manager.update_report_status(report_path, completion_data)

        # 更新状态管理器
        self.state_manager.update_check_status(requirement, completion_data["completion_rate"])

        # 生成输出
        stats = completion_data["stats"]
        completion_rate = completion_data["completion_rate"]

        if output_format == "json":
            return {
                "status": "completion_checked",
                "requirement": requirement,
                "report_info": completion_data["report_info"],
                "completion_rate": completion_rate,
                "task_stats": stats,
                "summary": completion_data["summary"]
            }
        else:
            # 文本格式输出
            if completion_rate >= 100:
                status_emoji = "🎉"
                status_text = "全部完成"
            elif completion_rate >= 80:
                status_emoji = "👍"
                status_text = "接近完成"
            elif completion_rate >= 50:
                status_emoji = "📊"
                status_text = "完成过半"
            elif completion_rate >= 20:
                status_emoji = "⏳"
                status_text = "已开始"
            else:
                status_emoji = "🚧"
                status_text = "刚开始"

            output_lines = [
                f"{status_emoji} 重构进度检查",
                f"📋 需求: {requirement}",
                f"📁 报告文件: {report_path}",
                f"📅 生成日期: {completion_data['report_info']['generated_date']}",
                f"📊 完成率: {completion_rate}% ({status_text})",
                "",
                "📈 任务统计:",
                f"  总任务数: {stats['total']}",
                f"  已完成: {stats['completed']}",
                f"  进行中: {stats['in_progress']}",
                f"  未开始: {stats['pending']}",
                "",
                completion_data["summary"]
            ]

            # 添加建议
            if completion_rate < 100:
                if stats['pending'] > 0:
                    output_lines.append(f"\n建议: 优先处理 {stats['pending']} 个未开始任务")
                if stats['in_progress'] > 0:
                    output_lines.append(f"建议: 加快完成 {stats['in_progress']} 个进行中任务")

            return {
                "status": "completion_checked",
                "output": "\n".join(output_lines),
                "completion_rate": completion_rate,
                "task_stats": stats
            }

    def list_recent_reports(self, days: int = 7, output_format: str = "text") -> Dict[str, Any]:
        """
        列出最近报告

        Args:
            days: 最近多少天的报告
            output_format: 输出格式

        Returns:
            报告列表结果
        """
        reports = self.report_manager.list_reports(days)

        if output_format == "json":
            return {
                "status": "reports_listed",
                "days": days,
                "total_reports": len(reports),
                "reports": reports
            }
        else:
            if not reports:
                return {
                    "status": "no_reports",
                    "output": f"最近{days}天内没有生成报告"
                }

            output_lines = [f"最近{days}天内的重构报告 ({len(reports)}个):", ""]

            for i, report in enumerate(reports, 1):
                output_lines.extend([
                    f"{i}. {report['requirement']}",
                    f"   文件: {report['file_name']}",
                    f"   日期: {report['generated_date']}",
                    f"   状态: {report['status']}",
                    f"   完成率: {report['completion_rate']}%",
                    f"   任务: {report['task_stats']['completed']}/{report['task_stats']['total']} 完成",
                    ""
                ])

            return {
                "status": "reports_listed",
                "output": "\n".join(output_lines),
                "total_reports": len(reports)
            }

    def get_stats(self, output_format: str = "text") -> Dict[str, Any]:
        """
        获取统计信息

        Args:
            output_format: 输出格式

        Returns:
            统计信息
        """
        state_stats = self.state_manager.get_stats()
        recent_reports = self.report_manager.list_reports(days=30)

        if output_format == "json":
            return {
                "status": "stats_retrieved",
                "state_stats": state_stats,
                "recent_reports_count": len(recent_reports)
            }
        else:
            output_lines = [
                "📊 代码重构分析统计",
                "",
                "📈 状态统计:",
                f"  总需求数: {state_stats['total_requirements']}",
                f"  总报告数: {state_stats['total_reports']}",
                f"  平均使用次数: {state_stats['average_usage']}",
                f"  最近30天需求: {state_stats['recent_30_days']}",
                "",
                "📋 最近报告:"
            ]

            if recent_reports:
                for report in recent_reports[:5]:  # 显示最近5个报告
                    output_lines.append(
                        f"  - {report['requirement']} ({report['completion_rate']}% 完成)"
                    )
            else:
                output_lines.append("  暂无报告")

            return {
                "status": "stats_retrieved",
                "output": "\n".join(output_lines)
            }


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description="代码重构分析工具")
    parser.add_argument("requirement", nargs="?", help="用户需求描述")
    parser.add_argument("--repo", default=".", help="仓库路径（默认当前目录）")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                       help="输出格式（默认text）")
    parser.add_argument("--list-reports", type=int, metavar="DAYS",
                       help="列出最近N天的报告")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--cleanup", type=int, metavar="DAYS",
                       help="清理N天前的旧报告")

    args = parser.parse_args()

    # 创建分析器
    analyzer = CodeRefactorAnalyzer(args.repo)

    try:
        if args.list_reports:
            # 列出报告
            result = analyzer.list_recent_reports(args.list_reports, args.format)
        elif args.stats:
            # 显示统计信息
            result = analyzer.get_stats(args.format)
        elif args.cleanup:
            # 清理旧报告
            cleaned = analyzer.state_manager.cleanup_old_reports(args.cleanup)
            result = {
                "status": "cleanup_completed",
                "cleaned_count": cleaned,
                "message": f"已清理{cleaned}个{args.cleanup}天前的报告"
            }
        elif args.requirement:
            # 处理需求
            result = analyzer.process_requirement(args.requirement, args.format)
        else:
            # 显示帮助
            parser.print_help()
            return 0

        # 输出结果
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "output" in result:
                print(result["output"])
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))

        return 0

    except Exception as e:
        error_result = {
            "status": "error",
            "error": str(e),
            "suggestion": "请检查需求描述和仓库路径"
        }

        if args.format == "json":
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 错误: {e}")

        return 1


if __name__ == "__main__":
    sys.exit(main())
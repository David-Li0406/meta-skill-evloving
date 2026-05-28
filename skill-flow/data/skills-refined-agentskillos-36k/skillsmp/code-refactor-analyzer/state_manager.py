#!/usr/bin/env python3
"""
状态管理模块 - 管理技能状态（首次使用 vs 后续使用）

功能：
1. 检查相同需求下是否已生成报告
2. 管理需求历史记录
3. 区分首次使用和后续使用
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class StateManager:
    """状态管理器"""

    def __init__(self, repo_path: str = "."):
        """
        初始化状态管理器

        Args:
            repo_path: 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path).resolve()
        self.state_dir = self.repo_path / ".claude" / "code_refactor_state"
        self.state_file = self.state_dir / "state.json"

        # 确保状态目录存在
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # 加载状态
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """加载状态文件"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"requirements": {}, "reports": {}, "last_updated": None}
        return {"requirements": {}, "reports": {}, "last_updated": None}

    def _save_state(self):
        """保存状态文件"""
        self.state["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def _generate_requirement_id(self, requirement: str) -> str:
        """
        为需求生成唯一ID

        Args:
            requirement: 用户需求描述

        Returns:
            需求ID（MD5哈希）
        """
        # 标准化需求文本
        normalized = requirement.strip().lower()
        # 生成MD5哈希
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()[:8]

    def check_requirement_status(self, requirement: str) -> Tuple[bool, Optional[str]]:
        """
        检查需求状态

        Args:
            requirement: 用户需求描述

        Returns:
            (is_first_use, report_path)
            is_first_use: 是否是首次使用（True=首次，False=后续）
            report_path: 报告文件路径（如果存在）
        """
        req_id = self._generate_requirement_id(requirement)

        # 检查是否已有报告
        if req_id in self.state.get("reports", {}):
            report_info = self.state["reports"][req_id]
            report_path = report_info.get("path")

            # 检查报告文件是否存在
            if report_path and Path(report_path).exists():
                return False, report_path

        # 首次使用或报告不存在
        return True, None

    def register_requirement(self, requirement: str, report_path: str):
        """
        注册需求和报告

        Args:
            requirement: 用户需求描述
            report_path: 生成的报告文件路径
        """
        req_id = self._generate_requirement_id(requirement)
        timestamp = datetime.now().isoformat()

        # 更新需求记录
        if "requirements" not in self.state:
            self.state["requirements"] = {}

        self.state["requirements"][req_id] = {
            "requirement": requirement,
            "first_used": timestamp,
            "last_used": timestamp,
            "usage_count": 1
        }

        # 更新报告记录
        if "reports" not in self.state:
            self.state["reports"] = {}

        self.state["reports"][req_id] = {
            "path": str(report_path),
            "generated_at": timestamp,
            "last_checked": timestamp,
            "check_count": 1
        }

        self._save_state()

    def update_check_status(self, requirement: str, completion_rate: float):
        """
        更新检查状态

        Args:
            requirement: 用户需求描述
            completion_rate: 完成率（0-100）
        """
        req_id = self._generate_requirement_id(requirement)
        timestamp = datetime.now().isoformat()

        # 更新需求使用次数
        if req_id in self.state.get("requirements", {}):
            self.state["requirements"][req_id]["last_used"] = timestamp
            self.state["requirements"][req_id]["usage_count"] += 1

        # 更新报告检查状态
        if req_id in self.state.get("reports", {}):
            self.state["reports"][req_id]["last_checked"] = timestamp
            self.state["reports"][req_id]["check_count"] += 1
            self.state["reports"][req_id]["last_completion_rate"] = completion_rate

        self._save_state()

    def get_requirement_history(self, days: int = 30) -> List[Dict]:
        """
        获取需求历史记录

        Args:
            days: 最近多少天的记录

        Returns:
            需求历史记录列表
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        history = []

        for req_id, req_info in self.state.get("requirements", {}).items():
            # 转换时间戳
            first_used = datetime.fromisoformat(req_info["first_used"]).timestamp()

            if first_used >= cutoff_date:
                report_info = self.state.get("reports", {}).get(req_id, {})
                history.append({
                    "requirement": req_info["requirement"],
                    "first_used": req_info["first_used"],
                    "last_used": req_info["last_used"],
                    "usage_count": req_info["usage_count"],
                    "report_path": report_info.get("path"),
                    "generated_at": report_info.get("generated_at"),
                    "check_count": report_info.get("check_count", 0),
                    "last_completion_rate": report_info.get("last_completion_rate")
                })

        # 按最后使用时间排序（最新的在前）
        history.sort(key=lambda x: x["last_used"], reverse=True)
        return history

    def cleanup_old_reports(self, days: int = 90):
        """
        清理旧报告

        Args:
            days: 保留多少天内的报告
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        reports_to_remove = []

        for req_id, report_info in self.state.get("reports", {}).items():
            generated_at = datetime.fromisoformat(report_info["generated_at"]).timestamp()

            if generated_at < cutoff_date:
                # 删除报告文件
                report_path = Path(report_info["path"])
                if report_path.exists():
                    try:
                        report_path.unlink()
                    except OSError:
                        pass

                reports_to_remove.append(req_id)

        # 从状态中移除
        for req_id in reports_to_remove:
            self.state["reports"].pop(req_id, None)
            self.state["requirements"].pop(req_id, None)

        if reports_to_remove:
            self._save_state()
            return len(reports_to_remove)

        return 0

    def get_stats(self) -> Dict:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        total_requirements = len(self.state.get("requirements", {}))
        total_reports = len(self.state.get("reports", {}))

        # 计算平均使用次数
        usage_counts = [info["usage_count"] for info in self.state.get("requirements", {}).values()]
        avg_usage = sum(usage_counts) / len(usage_counts) if usage_counts else 0

        # 最近30天的需求
        recent_history = self.get_requirement_history(days=30)

        return {
            "total_requirements": total_requirements,
            "total_reports": total_reports,
            "average_usage": round(avg_usage, 2),
            "recent_30_days": len(recent_history),
            "last_updated": self.state.get("last_updated")
        }


# 测试代码
if __name__ == "__main__":
    # 创建测试状态管理器
    manager = StateManager()

    # 测试需求状态检查
    test_req = "添加用户认证功能"
    is_first, report_path = manager.check_requirement_status(test_req)
    print(f"需求: {test_req}")
    print(f"首次使用: {is_first}")
    print(f"报告路径: {report_path}")

    # 测试注册需求
    if is_first:
        test_report = ".claude/code_refactor_report/添加用户认证功能-2025-12-14.md"
        manager.register_requirement(test_req, test_report)
        print(f"已注册需求和报告: {test_report}")

    # 获取统计信息
    stats = manager.get_stats()
    print(f"\n统计信息: {stats}")

    # 获取历史记录
    history = manager.get_requirement_history(days=7)
    print(f"\n最近7天历史记录: {len(history)} 条")
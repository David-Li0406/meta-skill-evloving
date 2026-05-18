"""Trajectory format adapters for different benchmarks.

Converts benchmark-specific trajectory formats to a unified format:
- trajectory_id: str
- user_task: str
- task_history: List[Dict] with role, content, tool_calls
- reward: float
- benchmark: str
- domain: Optional[str] (for tau2-bench)
"""

import os
import re
import json
import glob
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class TrajectoryAdapter(ABC):
    """Base class for trajectory format adapters."""

    def __init__(self, benchmark: str):
        self.benchmark = benchmark

    @abstractmethod
    def load(self, filepath: str) -> List[Dict]:
        """Load trajectories from file."""
        pass

    @abstractmethod
    def to_unified(self, raw: Dict) -> Dict:
        """Convert raw trajectory to unified format."""
        pass

    def filter_successful(
        self,
        items: List[Dict],
        threshold: float = 0.99
    ) -> List[Dict]:
        """Filter trajectories with reward > threshold."""
        successful = [
            item for item in items
            if item.get("reward", 0) > threshold
        ]
        logger.info(
            f"Filtered {len(successful)}/{len(items)} successful trajectories "
            f"(threshold: {threshold})"
        )
        return successful

    def group_by_task(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group trajectories by user_task."""
        grouped = defaultdict(list)
        for item in items:
            grouped[item["user_task"]].append(item)
        return dict(grouped)

    def get_shortest_per_task(self, items: List[Dict]) -> List[Dict]:
        """Select shortest trajectory per task."""
        grouped = self.group_by_task(items)
        shortest = []
        for task, trajs in grouped.items():
            sorted_trajs = sorted(trajs, key=lambda x: len(x.get("task_history", [])))
            shortest.append(sorted_trajs[0])
        return shortest


class AppWorldAdapter(TrajectoryAdapter):
    """Adapter for AppWorld trajectory format (JSONL)."""

    def __init__(self):
        super().__init__("appworld")

    def load(self, filepath: str) -> List[Dict]:
        """Load trajectories from JSONL file."""
        trajectories = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    unified = self.to_unified(data)
                    trajectories.append(unified)
        logger.info(f"Loaded {len(trajectories)} trajectories from {filepath}")
        return trajectories

    def to_unified(self, raw: Dict) -> Dict:
        """
        Convert AppWorld format to unified format.

        AppWorld format:
        - task_id: str
        - task_history: List[Dict] with role, content
        - after_score: float (reward)
        """
        task_history = raw.get("task_history", [])

        # Extract user_task from task_history (usually second message)
        user_task = ""
        if len(task_history) > 1:
            user_task = task_history[1].get("content", "")

        # Normalize task_history format
        normalized_history = []
        for step in task_history:
            normalized_step = {
                "role": step.get("role", ""),
                "content": step.get("content", ""),
            }
            if "tool_calls" in step:
                normalized_step["tool_calls"] = step["tool_calls"]
            normalized_history.append(normalized_step)

        return {
            "trajectory_id": raw.get("task_id", ""),
            "user_task": user_task,
            "task_history": normalized_history,
            "reward": raw.get("after_score", raw.get("reward", 0)),
            "benchmark": self.benchmark,
            "domain": None,
            "raw_data": raw,  # Keep original for reference
        }


class BFCLAdapter(TrajectoryAdapter):
    """Adapter for BFCL trajectory format (JSONL)."""

    def __init__(self):
        super().__init__("bfcl")

    def load(self, filepath: str) -> List[Dict]:
        """Load trajectories from JSONL file."""
        trajectories = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    unified = self.to_unified(data)
                    trajectories.append(unified)
        logger.info(f"Loaded {len(trajectories)} trajectories from {filepath}")
        return trajectories

    def to_unified(self, raw: Dict) -> Dict:
        """
        Convert BFCL format to unified format.

        BFCL format:
        - task_id: str
        - messages: List[Dict] with role, content, tool_calls
        - reward: float
        """
        messages = raw.get("messages", [])

        # Extract user_task from first human message
        user_task = ""
        for msg in messages:
            if msg.get("role") in ["human", "user"]:
                user_task = msg.get("content", "")
                break

        # Normalize messages to task_history
        normalized_history = []
        for msg in messages:
            role = msg.get("role", "")
            # Normalize role names
            if role in ["human", "user"]:
                role = "user"
            elif role in ["ai", "assistant"]:
                role = "assistant"

            normalized_step = {
                "role": role,
                "content": msg.get("content", ""),
            }
            if "tool_calls" in msg and msg["tool_calls"]:
                normalized_step["tool_calls"] = msg["tool_calls"]
            normalized_history.append(normalized_step)

        return {
            "trajectory_id": raw.get("task_id", raw.get("instance_id", "")),
            "user_task": user_task,
            "task_history": normalized_history,
            "reward": raw.get("reward", 0),
            "benchmark": self.benchmark,
            "domain": None,
            "raw_data": raw,
        }


class Tau2BenchAdapter(TrajectoryAdapter):
    """Adapter for tau2-bench trajectory format (JSON with simulations)."""

    def __init__(self):
        super().__init__("tau2bench")

    def load(self, filepath: str) -> List[Dict]:
        """
        Load trajectories from JSON file(s).

        Supports:
        - Single JSON file
        - Glob pattern (e.g., "*.json")
        """
        trajectories = []

        # Handle glob pattern
        if "*" in filepath:
            files = glob.glob(filepath)
        else:
            files = [filepath]

        for fpath in files:
            domain = self._extract_domain(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # tau2-bench has simulations list
            simulations = data.get("simulations", [])
            for sim in simulations:
                unified = self.to_unified(sim, domain=domain)
                trajectories.append(unified)

        logger.info(f"Loaded {len(trajectories)} trajectories from {len(files)} files")
        return trajectories

    def _extract_domain(self, filepath: str) -> str:
        """Extract domain from filename (airline, retail, telecom)."""
        filename = os.path.basename(filepath).lower()
        for domain in ["airline", "retail", "telecom"]:
            if domain in filename:
                return domain
        return "unknown"

    def to_unified(self, raw: Dict, domain: str = "unknown") -> Dict:
        """
        Convert tau2-bench format to unified format.

        tau2-bench format:
        - id: str
        - task_id: str
        - messages: List[Dict] with role, content, tool_calls
        - reward_info: Dict with reward
        """
        messages = raw.get("messages", [])

        # Extract user_task from first user message
        user_task = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_task = msg.get("content", "")
                break

        # Normalize messages
        normalized_history = []
        for msg in messages:
            role = msg.get("role", "")
            normalized_step = {
                "role": role,
                "content": msg.get("content", ""),
            }
            if "tool_calls" in msg and msg["tool_calls"]:
                normalized_step["tool_calls"] = msg["tool_calls"]
            normalized_history.append(normalized_step)

        # Extract reward
        reward_info = raw.get("reward_info", {})
        reward = reward_info.get("reward", 0) if isinstance(reward_info, dict) else 0

        return {
            "trajectory_id": raw.get("id", raw.get("task_id", "")),
            "user_task": user_task,
            "task_history": normalized_history,
            "reward": reward,
            "benchmark": self.benchmark,
            "domain": domain,
            "raw_data": raw,
        }

    def collect_tools(self, items: List[Dict]) -> Dict[str, set]:
        """
        Collect all unique tools used in trajectories, grouped by domain.

        Returns:
            Dict mapping domain to set of tool names
        """
        tools_by_domain = defaultdict(set)
        for item in items:
            domain = item.get("domain", "unknown")
            for step in item.get("task_history", []):
                if step.get("role") == "assistant" and step.get("tool_calls"):
                    for tc in step["tool_calls"]:
                        tools_by_domain[domain].add(tc.get("name", ""))
        return dict(tools_by_domain)


def get_adapter(benchmark: str) -> TrajectoryAdapter:
    """Factory function to get appropriate adapter."""
    adapters = {
        "appworld": AppWorldAdapter,
        "bfcl": BFCLAdapter,
        "tau2bench": Tau2BenchAdapter,
        "tau2-bench": Tau2BenchAdapter,
    }
    if benchmark.lower() not in adapters:
        raise ValueError(f"Unknown benchmark: {benchmark}")
    return adapters[benchmark.lower()]()

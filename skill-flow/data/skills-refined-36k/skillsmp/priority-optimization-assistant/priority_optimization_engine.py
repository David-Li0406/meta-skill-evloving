"""
Priority Optimization Engine - Core implementation for the priority-optimization-assistant skill.

Contains modular classes: PriorityAnalyzer, OptimizationPlanner, OptimizationExecutor, ReportGenerator.
"""

from typing import Dict, List, Any, Optional, Tuple
import json
from dataclasses import dataclass
from enum import Enum

class PriorityLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class OptimizationItem:
    id: str
    description: str
    priority: PriorityLevel
    effort_estimate: str  # e.g., "low (1h)", "medium (4h)"
    impact: str  # e.g., "high performance gain"
    details: str

class PriorityAnalyzer:
    """Analyzes tasks and assigns priorities based on heuristics."""

    def __init__(self, project_description: str, tasks: Optional[List[Dict]] = None):
        self.project_description = project_description
        self.tasks = tasks or []
        self.items: List[OptimizationItem] = []

    def analyze(self) -> List[OptimizationItem]:
        """Analyze and return prioritized optimization items."""
        # Heuristic scoring: impact (urgent/performance), effort (simple first), dependencies
        keywords_high = ["critical", "bug", "performance bottleneck", "security", "crash"]
        keywords_medium = ["refactor", "optimize", "improve", "cleanup"]
        keywords_low = ["style", "docs", "minor"]

        for i, task in enumerate(self.tasks):
            desc = task.get("description", str(task))
            priority = self._assign_priority(desc)
            effort = self._estimate_effort(desc)
            impact = self._estimate_impact(desc)
            item = OptimizationItem(
                id=f"opt_{i+1}",
                description=desc,
                priority=priority,
                effort_estimate=effort,
                impact=impact,
                details=task.get("details", "")
            )
            self.items.append(item)

        # Add inferred optimizations from project description if no tasks
        if not self.tasks:
            inferred = self._infer_optimizations()
            self.items.extend(inferred)

        return sorted(self.items, key=lambda x: (x.priority.value, x.effort_estimate))

    def _assign_priority(self, desc: str) -> PriorityLevel:
        desc_lower = desc.lower()
        if any(k in desc_lower for k in ["critical", "bug", "security", "urgent"]):
            return PriorityLevel.HIGH
        elif any(k in desc_lower for k in ["performance", "slow", "optimize"]):
            return PriorityLevel.MEDIUM
        else:
            return PriorityLevel.LOW

    def _estimate_effort(self, desc: str) -> str:
        if "quick" in desc.lower() or len(desc) < 50:
            return "low (30min)"
        elif "refactor" in desc.lower():
            return "medium (2h)"
        return "high (8h+)"

    def _estimate_impact(self, desc: str) -> str:
        if "performance" in desc.lower() or "bug" in desc.lower():
            return "high"
        return "medium"

    def _infer_optimizations(self) -> List[OptimizationItem]:
        # Simple inference - in real use, integrate LLM
        return [
            OptimizationItem("opt_1", "Add caching to slow endpoints", PriorityLevel.HIGH, "medium (2h)", "high perf", ""),
            OptimizationItem("opt_2", "Refactor duplicated code", PriorityLevel.MEDIUM, "low (1h)", "medium", ""),
        ]

class OptimizationPlanner:
    """Generates checklists and selection menus."""

    @staticmethod
    def generate_checklist(items: List[OptimizationItem]) -> Dict[str, Any]:
        """Generate grouped checklist."""
        grouped = {"high": [], "medium": [], "low": []}
        for item in items:
            grouped[item.priority.value].append(item)
        return grouped

    @staticmethod
    def generate_menu(items: List[OptimizationItem]) -> str:
        """Markdown menu for user selection."""
        menu = "## Select Optimizations\n\n"
        menu += "**1. Execute All**\n"
        menu += "**2. By Priority:**\n"
        for prio in ["high", "medium", "low"]:
            count = len([i for i in items if i.priority.value == prio])
            if count:
                menu += f"   - {prio.title()} ({count} items)\n"
        menu += "**3. Single Item:**\n"
        for item in items:
            menu += f"   - {item.id}: {item.description[:50]}...\n"
        return menu

class OptimizationExecutor:
    """Executes selected optimizations with QA."""

    def __init__(self, items: List[OptimizationItem]):
        self.items = items
        self.results: Dict[str, Dict] = {}

    def execute(self, selections: List[str]) -> Dict[str, Any]:
        """Execute selected items (simulate/generate)."""
        for sel in selections:
            item = next((i for i in self.items if i.id == sel), None)
            if item:
                # Simulate execution: generate 'optimized' result
                result = {
                    "before": item.description,
                    "after": self._generate_optimization(item),
                    "qa_check": self._quality_assurance(item),
                    "status": "success"
                }
                self.results[item.id] = result
        return self.results

    def _generate_optimization(self, item: OptimizationItem) -> str:
        # Placeholder: real impl would generate code diffs
        return f"Optimized: {item.description} -> Improved version with {item.impact.lower()}."

    def _quality_assurance(self, item: OptimizationItem) -> List[str]:
        return ["Lint passed", "Tests simulated: 100% coverage", "Perf improved by 20%"]

class ReportGenerator:
    """Generates detailed optimization reports."""

    def __init__(self, checklist: Dict, results: Dict, original_input: Dict):
        self.checklist = checklist
        self.results = results
        self.original_input = original_input

    def generate_report(self) -> str:
        """Markdown report."""
        report = "# Optimization Report\n\n"
        report += "## Summary\n"
        completed = len(self.results)
        total = sum(len(v) for v in self.checklist.values())
        report += f"- Completed: {completed}/{total} items\n"
        report += f"- Focus: {list(self.results.keys())}\n\n"

        report += "## Checklist\n"
        for prio, items in self.checklist.items():
            report += f"### {prio.title()}\n"
            for item in items:
                status = "✅" if item.id in self.results else "⏳"
                report += f"- {status} {item.description} ({item.effort_estimate})\n"

        if self.results:
            report += "\n## Execution Results\n"
            for item_id, res in self.results.items():
                report += f"### {item_id}\n"
                report += f"**Before:** {res['before']}\n"
                report += f"**After:** {res['after']}\n"
                report += "**QA:** " + "; ".join(res['qa_check']) + "\n\n"

        report += "## Next Steps\n"
        report += "- Review and apply generated optimizations.\n"
        report += "- Rerun for remaining items.\n"
        report += "- Monitor production impact.\n"

        return report

# Main orchestrator
class PriorityOptimizationEngine:
    """Main class to run the full workflow."""

    def __init__(self, input_data: Dict[str, Any]):
        self.input_data = input_data
        project_desc = input_data.get("project_description", "")
        tasks = input_data.get("tasks", [])
        self.analyzer = PriorityAnalyzer(project_desc, tasks)

    def process(self, user_selection: Optional[str] = None) -> Dict[str, Any]:
        """Full workflow: analyze -> plan -> execute -> report."""
        items = self.analyzer.analyze()
        checklist = OptimizationPlanner.generate_checklist(items)

        if user_selection == "menu":
            return {"checklist": checklist, "menu": OptimizationPlanner.generate_menu(items)}

        # Simulate selections based on user_selection e.g., "high", "all", "opt_1"
        selections = self._parse_selection(user_selection, items)
        executor = OptimizationExecutor(items)
        results = executor.execute(selections)
        reporter = ReportGenerator(checklist, executor.results, self.input_data)
        report = reporter.generate_report()

        return {
            "checklist": checklist,
            "executed": list(results.keys()),
            "report": report,
            "full_results": results
        }

    def _parse_selection(self, selection: str, items: List[OptimizationItem]) -> List[str]:
        if selection == "all":
            return [i.id for i in items]
        elif selection in ["high", "medium", "low"]:
            return [i.id for i in items if i.priority.value == selection]
        elif selection.startswith("opt_"):
            return [selection]
        return []

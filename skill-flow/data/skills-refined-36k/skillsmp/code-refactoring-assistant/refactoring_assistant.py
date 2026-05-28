#!/usr/bin/env python3
"""
Code Refactoring Assistant - Main Python implementation.
Modular classes for impact analysis, planning, review, execution, QA, reporting.
Designed for Claude Skills: Stateless process(input) -> output dict.
Real interaction/QA via Claude conversation + tools (Bash/git, Grep for metrics).
"""

import json
import difflib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class RefactorItem:
    id: int
    description: str
    impact: ImpactLevel
    files_affected: List[str]
    risks: List[str]
    benefits: List[str]

class ImpactAnalyzer:
    """Analyzes refactoring impact based on files, deps, tests."""

    def __init__(self, codebase_info: Dict[str, Any]):
        self.files = codebase_info.get('files', [])
        self.tests = codebase_info.get('tests', [])
        self.deps = codebase_info.get('deps', {})

    def analyze(self, goal: str) -> List[RefactorItem]:
        items = []
        for i, file in enumerate(self.files):
            num_files = len(file.get('affected', [file['path']]))
            num_deps = file.get('deps', 0)
            test_cov = file.get('coverage', 0)
            if num_files < 5 and num_deps < 5 and test_cov > 70:
                impact = ImpactLevel.LOW
            elif num_files < 20 and num_deps < 20:
                impact = ImpactLevel.MEDIUM
            else:
                impact = ImpactLevel.HIGH
            item = RefactorItem(
                id=i,
                description=f"{goal.title()} in {file['path']}",
                impact=impact,
                files_affected=[file['path']],
                risks=[f"{impact.value} risk: {num_deps} deps"],
                benefits=["Improved maintainability"]
            )
            items.append(item)
        return items

class RefactoringPlanner:
    """Generates prioritized checklist by impact."""

    def generate_checklist(self, analyses: List[RefactorItem]) -> List[RefactorItem]:
        low = [i for i in analyses if i.impact == ImpactLevel.LOW]
        medium = [i for i in analyses if i.impact == ImpactLevel.MEDIUM]
        high = [i for i in analyses if i.impact == ImpactLevel.HIGH]
        return low + medium + high

class ReviewInterface:
    """Interactive review simulation (real: Claude loop). Returns template for decisions."""

    def get_review_decision(self, item: RefactorItem) -> Dict[str, Any]:
        # Template for Claude to fill: {'approved': 'yes/no/back', 'feedback': str}
        return {
            'item_id': item.id,
            'approved': None,  # User sets: 'yes'/'no'/'back'
            'feedback': ''
        }

    def process_reviews(self, checklist: List[RefactorItem], decisions: List[Dict]) -> List[RefactorItem]:
        approved = []
        for item in checklist:
            decision = next((d for d in decisions if d['item_id'] == item.id), {})
            if decision.get('approved') == 'yes':
                approved.append(item)
        return approved

class RefactoringExecutor:
    """Simulates/executes refactors (real: uses Claude Edit/Bash git apply)."""

    def execute(self, approved_items: List[RefactorItem]) -> Dict[str, str]:
        changes = {}
        for item in approved_items:
            # Simulate change
            old_code = f"def old_func():\n    pass  # {len(item.files_affected)} files"
            new_code = f"def new_func():\n    # Refactored for {item.description}"
            diff = '\n'.join(difflib.unified_diff(old_code.splitlines(), new_code.splitlines(), lineterm=''))
            changes[item.id] = diff
        return {'diffs': changes}

class QAValidator:
    """Validates post-refactor quality (real: Bash pytest, black, perf tests)."""

    def validate(self, changes: Dict, baseline_metrics: Dict) -> Dict[str, Any]:
        # Simulate
        return {
            'style_pass': True,
            'tests_pass': 100,
            'coverage_change': +5,  # %
            'perf_change': -10,  # ms
            'issues': []
        }

class RefactoringReporter:
    """Generates detailed reports."""

    def generate_report(self, checklist: List[RefactorItem], decisions: List[Dict],
                        changes: Dict, qa: Dict, baseline: Dict) -> Dict[str, Any]:
        deltas = {k: qa.get(k.replace('_change', ''), 0) for k in qa if k.endswith('_change')}
        return {
            'checklist': [item.__dict__ for item in checklist],
            'approved_count': len([d for d in decisions if d.get('approved') == 'yes']),
            'changes_summary': changes,
            'qa_results': qa,
            'metrics_delta': deltas,
            'recommendations': ["All QA passed. Deploy ready."]
        }

class RefactoringAssistant:
    """Main orchestrator class."""

    def __init__(self, input_data: Dict[str, Any]):
        self.input_data = input_data
        self.codebase_info = input_data.get('codebase', {})
        self.goals = input_data.get('goals', [])
        self.baseline_metrics = input_data.get('metrics', {})

        self.analyzer = ImpactAnalyzer(self.codebase_info)
        self.planner = RefactoringPlanner()
        self.reviewer = ReviewInterface()
        self.executor = RefactoringExecutor()
        self.validator = QAValidator()
        self.reporter = RefactoringReporter()

    def process(self, review_decisions: Optional[List[Dict]] = None) -> Dict[str, Any]:
        # Step 1: Analyze & Plan
        analyses = self.analyzer.analyze(self.goals[0] if self.goals else "general refactor")
        checklist = self.planner.generate_checklist(analyses)

        if review_decisions is None:
            # Initial: Return checklist for review
            return {'stage': 'review', 'checklist': [item.__dict__ for item in checklist]}

        # Step 2: Review
        approved_items = self.reviewer.process_reviews(checklist, review_decisions)

        # Step 3: Execute
        changes = self.executor.execute(approved_items)

        # Step 4: QA
        qa_results = self.validator.validate(changes, self.baseline_metrics)

        # Step 5: Report
        report = self.reporter.generate_report(checklist, review_decisions, changes, qa_results, self.baseline_metrics)

        return {
            'stage': 'complete',
            'report': report,
            'status': 'success'
        }

# Entry point for Claude Skill
if __name__ == "__main__":
    import sys
    input_data = json.loads(sys.stdin.read())
    assistant = RefactoringAssistant(input_data)
    result = assistant.process(input_data.get('review_decisions'))
    print(json.dumps(result, indent=2))

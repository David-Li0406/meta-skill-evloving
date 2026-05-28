#!/usr/bin/env python3
"""
Spec Critique Tool

Provides critical analysis of specification quality.

Usage:
    python critique_plan.py /path/to/feature-folder [--focus area1,area2]

Returns JSON with critique results.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class SpecCritic:
    """Critical analyzer for feature specifications."""

    VAGUE_VERBS = [
        'implement', 'create', 'add', 'build', 'develop', 'make',
        'handle', 'support', 'provide', 'enable', 'allow', 'improve'
    ]

    MEASURABLE_INDICATORS = [
        r'\d+\s*(ms|second|minute|hour|day)',  # Time
        r'\d+\s*(%|percent)',  # Percentage
        r'\d+\s*(kb|mb|gb|byte)',  # Size
        r'\d+\s*(user|request|item)',  # Count
        r'less than', r'greater than', r'at least', r'no more than'  # Comparisons
    ]

    def __init__(self, feature_path: Path, focus_areas: List[str] = None):
        self.feature_path = feature_path
        self.focus_areas = focus_areas or []
        self.critical_issues = []
        self.warnings = []
        self.recommendations = []
        self.score_components = {}

    def critique(self) -> Dict:
        """Run all critique checks."""
        self._critique_requirements()
        self._critique_task_breakdown()
        self._critique_technical_design()
        self._critique_testability()

        # Calculate overall score
        if self.score_components:
            critique_score = sum(self.score_components.values()) / len(self.score_components)
        else:
            critique_score = 0.0

        return {
            "critique_score": round(critique_score, 2),
            "critical_issues": self.critical_issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "score_breakdown": self.score_components
        }

    def _critique_requirements(self):
        """Analyze requirement quality in FRD and FRS."""
        # Check FRD
        frd_path = self.feature_path / "docs/FRD.md"
        if frd_path.exists():
            self._analyze_requirement_specificity(frd_path, "FRD.md")
            self._check_acceptance_criteria(frd_path, "FRD.md")
            self._check_edge_cases(frd_path, "FRD.md")

        # Check FRS
        frs_path = self.feature_path / "docs/FRS.md"
        if frs_path.exists():
            self._analyze_requirement_specificity(frs_path, "FRS.md")
            self._check_functional_completeness(frs_path)

    def _analyze_requirement_specificity(self, file_path: Path, file_name: str):
        """Check if requirements are specific vs vague."""
        content = file_path.read_text(encoding='utf-8')

        # Find requirement statements
        requirement_patterns = [
            r'(?:FR-\d+|Requirement \d+):\s*(.+?)(?=\n\n|\n(?:FR-|\n|Requirement)|\Z)',
            r'^\s*[-*]\s+(.+?)$'
        ]

        requirements = []
        for pattern in requirement_patterns:
            requirements.extend(re.findall(pattern, content, re.MULTILINE | re.DOTALL))

        if not requirements:
            self.critical_issues.append({
                "file": file_name,
                "issue": "No identifiable requirements found",
                "suggestion": "Use clear requirement identifiers (e.g., FR-001, FR-002)"
            })
            self.score_components['requirement_specificity'] = 0.0
            return

        # Check for vague requirements
        vague_count = 0
        for req in requirements:
            req_lower = req.lower()
            # Check for vague verbs without specifics
            has_vague_verb = any(verb in req_lower for verb in self.VAGUE_VERBS)
            has_specifics = any(re.search(indicator, req, re.IGNORECASE) for indicator in self.MEASURABLE_INDICATORS)

            if has_vague_verb and not has_specifics and len(req) < 150:
                vague_count += 1

        vague_ratio = vague_count / len(requirements)

        if vague_ratio > 0.5:
            self.critical_issues.append({
                "file": file_name,
                "issue": f"{vague_count}/{len(requirements)} requirements are vague",
                "suggestion": "Add measurable criteria (timings, sizes, counts) and specific implementation details"
            })
            self.score_components['requirement_specificity'] = 0.3
        elif vague_ratio > 0.3:
            self.warnings.append({
                "file": file_name,
                "issue": f"{vague_count}/{len(requirements)} requirements could be more specific",
                "suggestion": "Consider adding measurable acceptance criteria"
            })
            self.score_components['requirement_specificity'] = 0.6
        else:
            self.score_components['requirement_specificity'] = 0.9

    def _check_acceptance_criteria(self, file_path: Path, file_name: str):
        """Check for measurable acceptance criteria."""
        content = file_path.read_text(encoding='utf-8')

        # Look for acceptance criteria section
        has_ac_section = bool(re.search(r'(?:Acceptance Criteria|Success Criteria|Definition of Done)', content, re.IGNORECASE))

        # Look for measurable criteria
        has_measurable = any(re.search(indicator, content, re.IGNORECASE) for indicator in self.MEASURABLE_INDICATORS)

        if not has_ac_section:
            self.critical_issues.append({
                "file": file_name,
                "issue": "No acceptance criteria section found",
                "suggestion": "Add 'Acceptance Criteria' section with measurable success conditions"
            })
            self.score_components['acceptance_criteria'] = 0.2
        elif not has_measurable:
            self.warnings.append({
                "file": file_name,
                "issue": "Acceptance criteria are not measurable",
                "suggestion": "Add quantifiable metrics (response times, accuracy %, etc.)"
            })
            self.score_components['acceptance_criteria'] = 0.5
        else:
            self.score_components['acceptance_criteria'] = 0.9

    def _check_edge_cases(self, file_path: Path, file_name: str):
        """Check if edge cases are covered."""
        content = file_path.read_text(encoding='utf-8')

        edge_case_keywords = [
            'edge case', 'error handling', 'validation', 'boundary',
            'empty', 'null', 'invalid', 'timeout', 'failure'
        ]

        edge_case_mentions = sum(1 for keyword in edge_case_keywords if keyword in content.lower())

        if edge_case_mentions == 0:
            self.warnings.append({
                "file": file_name,
                "issue": "No edge cases or error scenarios mentioned",
                "suggestion": "Document error handling, validation rules, and boundary conditions"
            })
            self.score_components['edge_cases'] = 0.3
        elif edge_case_mentions < 3:
            self.warnings.append({
                "file": file_name,
                "issue": f"Only {edge_case_mentions} edge case mentions",
                "suggestion": "Consider additional error scenarios and validation requirements"
            })
            self.score_components['edge_cases'] = 0.6
        else:
            self.score_components['edge_cases'] = 0.9

    def _check_functional_completeness(self, file_path: Path):
        """Check FRS for functional completeness."""
        content = file_path.read_text(encoding='utf-8')

        # Check for CRUD operations if applicable
        has_crud = any(op in content.lower() for op in ['create', 'read', 'update', 'delete', 'list'])

        if has_crud:
            crud_ops = [op for op in ['create', 'read', 'update', 'delete', 'list'] if op in content.lower()]
            if len(crud_ops) < 4:
                self.warnings.append({
                    "file": "FRS.md",
                    "issue": f"Only {len(crud_ops)}/5 CRUD operations documented: {', '.join(crud_ops)}",
                    "suggestion": "Verify all necessary CRUD operations are specified"
                })

    def _critique_task_breakdown(self):
        """Analyze task breakdown quality."""
        task_list_path = self.feature_path / "docs/task-list.md"

        if not task_list_path.exists():
            self.score_components['task_breakdown'] = 0.0
            return

        content = task_list_path.read_text(encoding='utf-8')

        # Extract tasks
        task_pattern = r'^\s*[-*]\s+\[[ x]\]\s+(.+)|^\s*[-*]\s+(.+)'
        matches = re.findall(task_pattern, content, re.MULTILINE)
        tasks = [m[0] or m[1] for m in matches]

        if not tasks:
            self.critical_issues.append({
                "file": "task-list.md",
                "issue": "No tasks found",
                "suggestion": "Break down feature into actionable development tasks"
            })
            self.score_components['task_breakdown'] = 0.0
            return

        self._check_task_atomicity(tasks)
        self._check_task_sequencing(content, tasks)
        self._check_task_dependencies(content)

    def _check_task_atomicity(self, tasks: List[str]):
        """Check if tasks are atomic and actionable."""
        broad_count = 0

        for task in tasks:
            # Check for broad tasks (short with vague verbs)
            task_lower = task.lower()
            has_vague_verb = any(verb in task_lower for verb in self.VAGUE_VERBS)
            is_short = len(task) < 60

            if has_vague_verb and is_short:
                broad_count += 1

        broad_ratio = broad_count / len(tasks)

        if broad_ratio > 0.4:
            self.critical_issues.append({
                "file": "task-list.md",
                "issue": f"{broad_count}/{len(tasks)} tasks are too broad",
                "suggestion": "Break down tasks like 'Implement X' into: 1) Design X interface, 2) Write X logic, 3) Add X tests"
            })
            self.score_components['task_atomicity'] = 0.3
        elif broad_ratio > 0.2:
            self.warnings.append({
                "file": "task-list.md",
                "issue": f"{broad_count}/{len(tasks)} tasks could be more specific",
                "suggestion": "Consider breaking down broad tasks into smaller, concrete steps"
            })
            self.score_components['task_atomicity'] = 0.6
        else:
            self.score_components['task_atomicity'] = 0.9

    def _check_task_sequencing(self, content: str, tasks: List[str]):
        """Check if task sequencing is logical."""
        # Look for numbering or ordering indicators
        has_numbering = bool(re.search(r'^\s*\d+\.', content, re.MULTILINE))
        has_phases = bool(re.search(r'(?:Phase|Stage|Step) \d+', content, re.IGNORECASE))

        # Check for setup tasks first
        first_task = tasks[0].lower() if tasks else ""
        has_setup_first = any(keyword in first_task for keyword in ['setup', 'initialize', 'create', 'scaffold'])

        if not (has_numbering or has_phases):
            self.warnings.append({
                "file": "task-list.md",
                "issue": "No clear task sequencing or phases",
                "suggestion": "Organize tasks into numbered phases or logical sequence"
            })
            self.score_components['task_sequencing'] = 0.5
        elif not has_setup_first and len(tasks) > 3:
            self.warnings.append({
                "file": "task-list.md",
                "issue": "Tasks may not start with setup/initialization",
                "suggestion": "Consider starting with setup, configuration, or scaffolding tasks"
            })
            self.score_components['task_sequencing'] = 0.7
        else:
            self.score_components['task_sequencing'] = 0.9

    def _check_task_dependencies(self, content: str):
        """Check if task dependencies are identified."""
        dependency_keywords = ['depends on', 'requires', 'after', 'blocked by', 'prerequisite']

        has_dependencies = any(keyword in content.lower() for keyword in dependency_keywords)

        if not has_dependencies:
            self.recommendations.append("Consider documenting task dependencies (e.g., 'Task B depends on Task A')")

    def _critique_technical_design(self):
        """Analyze technical requirements quality."""
        tr_path = self.feature_path / "docs/TR.md"

        if not tr_path.exists():
            self.score_components['technical_design'] = 0.0
            return

        content = tr_path.read_text(encoding='utf-8')

        self._check_api_definitions(content)
        self._check_data_models(content)
        self._check_error_handling(content)
        self._check_security(content)

    def _check_api_definitions(self, content: str):
        """Check if APIs are well-defined."""
        # Look for API/endpoint definitions
        has_endpoints = bool(re.search(r'(?:endpoint|route|api):\s*/\w+', content, re.IGNORECASE))
        has_methods = bool(re.search(r'\b(?:GET|POST|PUT|DELETE|PATCH)\b', content))
        has_request_body = bool(re.search(r'(?:request|body|payload|input)', content, re.IGNORECASE))
        has_response = bool(re.search(r'(?:response|output|return)', content, re.IGNORECASE))

        api_score = sum([has_endpoints, has_methods, has_request_body, has_response]) / 4

        if api_score < 0.5:
            self.critical_issues.append({
                "file": "TR.md",
                "issue": "API definitions are incomplete",
                "suggestion": "Document: endpoints, HTTP methods, request/response schemas"
            })
        elif api_score < 0.75:
            self.warnings.append({
                "file": "TR.md",
                "issue": "API definitions could be more detailed",
                "suggestion": "Add missing: " + ", ".join([
                    "endpoints" if not has_endpoints else "",
                    "HTTP methods" if not has_methods else "",
                    "request schemas" if not has_request_body else "",
                    "response schemas" if not has_response else ""
                ]).strip(", ")
            })

        self.score_components['api_definitions'] = api_score

    def _check_data_models(self, content: str):
        """Check if data models are complete."""
        # Look for data model definitions
        has_schema = bool(re.search(r'(?:schema|model|entity|table|collection)', content, re.IGNORECASE))
        has_fields = bool(re.search(r'(?:field|column|property|attribute):', content, re.IGNORECASE))
        has_types = bool(re.search(r'\b(?:string|number|boolean|integer|array|object|date)\b', content, re.IGNORECASE))

        model_score = sum([has_schema, has_fields, has_types]) / 3

        if model_score < 0.5:
            self.critical_issues.append({
                "file": "TR.md",
                "issue": "Data models are not defined",
                "suggestion": "Document database schemas, entities, and field types"
            })
        elif model_score < 0.75:
            self.warnings.append({
                "file": "TR.md",
                "issue": "Data models could be more detailed",
                "suggestion": "Add field types, constraints, and relationships"
            })

        self.score_components['data_models'] = model_score

    def _check_error_handling(self, content: str):
        """Check if error scenarios are handled."""
        error_keywords = ['error', 'exception', 'failure', 'timeout', 'retry', 'fallback']

        error_mentions = sum(1 for keyword in error_keywords if keyword in content.lower())

        if error_mentions == 0:
            self.critical_issues.append({
                "file": "TR.md",
                "issue": "No error handling strategy documented",
                "suggestion": "Define error responses, retry logic, and failure scenarios"
            })
            self.score_components['error_handling'] = 0.2
        elif error_mentions < 3:
            self.warnings.append({
                "file": "TR.md",
                "issue": "Limited error handling documentation",
                "suggestion": "Expand error handling: HTTP error codes, validation errors, timeouts"
            })
            self.score_components['error_handling'] = 0.6
        else:
            self.score_components['error_handling'] = 0.9

    def _check_security(self, content: str):
        """Check if security concerns are addressed."""
        security_keywords = [
            'authentication', 'authorization', 'permission', 'security',
            'validation', 'sanitization', 'encryption', 'token'
        ]

        security_mentions = sum(1 for keyword in security_keywords if keyword in content.lower())

        if security_mentions == 0:
            self.recommendations.append("Consider documenting security requirements: auth, validation, data protection")
        elif security_mentions < 3:
            self.recommendations.append("Expand security documentation: authentication, authorization, input validation")

    def _critique_testability(self):
        """Analyze testability of specifications."""
        gs_path = self.feature_path / "docs/GS.md"

        if not gs_path.exists():
            self.score_components['testability'] = 0.0
            return

        content = gs_path.read_text(encoding='utf-8')

        self._check_scenario_automation(content)
        self._check_test_data(content)

    def _check_scenario_automation(self, content: str):
        """Check if scenarios are automatable."""
        # Look for concrete Given/When/Then steps
        given_steps = re.findall(r'^\s*Given\s+(.+)$', content, re.MULTILINE)
        when_steps = re.findall(r'^\s*When\s+(.+)$', content, re.MULTILINE)
        then_steps = re.findall(r'^\s*Then\s+(.+)$', content, re.MULTILINE)

        all_steps = given_steps + when_steps + then_steps

        if not all_steps:
            self.score_components['testability'] = 0.0
            return

        # Check for vague steps
        vague_steps = sum(1 for step in all_steps if len(step) < 30 and any(verb in step.lower() for verb in self.VAGUE_VERBS))

        vague_ratio = vague_steps / len(all_steps)

        if vague_ratio > 0.5:
            self.warnings.append({
                "file": "GS.md",
                "issue": f"{vague_steps}/{len(all_steps)} Gherkin steps are vague",
                "suggestion": "Make steps concrete with specific values, actions, and expected results"
            })
            self.score_components['testability'] = 0.4
        elif vague_ratio > 0.3:
            self.score_components['testability'] = 0.7
        else:
            self.score_components['testability'] = 0.9

    def _check_test_data(self, content: str):
        """Check if test data requirements are clear."""
        # Look for example data or test fixtures
        has_examples = bool(re.search(r'(?:Examples?|Fixtures?|Test Data):', content, re.IGNORECASE))
        has_values = bool(re.search(r'["\'`]\w+["\'`]|\|\s*\w+\s*\|', content))  # Quoted values or tables

        if not has_examples and not has_values:
            self.recommendations.append("Add test data examples or scenario outlines with example tables")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "critique_score": 0.0,
            "critical_issues": [{"file": "N/A", "issue": "Usage: python critique_plan.py /path/to/feature-folder [--focus area1,area2]", "suggestion": ""}],
            "warnings": [],
            "recommendations": []
        }, indent=2))
        sys.exit(1)

    feature_path = Path(sys.argv[1])

    if not feature_path.exists():
        print(json.dumps({
            "critique_score": 0.0,
            "critical_issues": [{"file": "N/A", "issue": f"Feature folder not found: {feature_path}", "suggestion": ""}],
            "warnings": [],
            "recommendations": []
        }, indent=2))
        sys.exit(1)

    # Parse focus areas if provided
    focus_areas = []
    if len(sys.argv) > 2 and sys.argv[2] == "--focus" and len(sys.argv) > 3:
        focus_areas = [area.strip() for area in sys.argv[3].split(',')]

    critic = SpecCritic(feature_path, focus_areas)
    result = critic.critique()

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()

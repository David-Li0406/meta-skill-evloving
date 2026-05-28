#!/usr/bin/env python3
"""
Schedule Quality Validator for P6 Schedules

Validates schedule against industry best practices (DCMA 14-Point, AACE standards).
Generates detailed reports highlighting schedule quality issues.

Usage:
    validator = ScheduleValidator()
    issues = validator.validate_xer_file('schedule.xer')
    validator.generate_html_report(issues, 'report.html')
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import json
from parse_xer import XERParser, Activity, Relationship


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class ValidationIssue:
    """Represents a schedule quality issue"""
    rule_id: str
    rule_name: str
    severity: Severity
    description: str
    affected_items: List[str]
    recommendation: str
    count: int = 0

    def __post_init__(self):
        self.count = len(self.affected_items)


class ScheduleValidator:
    """Validates P6 schedules against quality rules"""

    def __init__(self):
        self.issues: List[ValidationIssue] = []
        self.activities: List[Activity] = []
        self.relationships: List[Relationship] = []

    def validate_xer_file(self, xer_file_path: str) -> List[ValidationIssue]:
        """
        Validate an XER file

        Args:
            xer_file_path: Path to XER file

        Returns:
            List of validation issues
        """
        parser = XERParser(xer_file_path)
        self.activities = parser.get_activities()
        self.relationships = parser.get_relationships()

        self.issues = []

        # Run all validation checks
        self._check_missing_predecessors()
        self._check_missing_successors()
        self._check_long_duration_activities()
        self._check_zero_duration_non_milestones()
        self._check_hard_constraints()
        self._check_logic_density()
        self._check_high_float()
        self._check_negative_float()
        self._check_invalid_relationships()
        self._check_future_actuals()
        self._check_invalid_percent_complete()

        return self.issues

    def _check_missing_predecessors(self):
        """Check for activities without predecessors"""
        # Build relationship map
        has_predecessor = set()
        for rel in self.relationships:
            has_predecessor.add(rel.task_id)

        # Find activities without predecessors (excluding start milestones)
        missing_pred = []
        for activity in self.activities:
            if (activity.task_type not in ['TT_Mile', 'TT_FinMile'] and
                activity.status != 'TK_Complete' and
                activity.task_id not in has_predecessor):
                missing_pred.append(f"{activity.task_code}: {activity.task_name}")

        if missing_pred:
            self.issues.append(ValidationIssue(
                rule_id="LOGIC-001",
                rule_name="Missing Predecessors",
                severity=Severity.HIGH,
                description="Activities without predecessor relationships (excluding milestones)",
                affected_items=missing_pred,
                recommendation="Add predecessor relationships to ensure activities are properly integrated into schedule logic"
            ))

    def _check_missing_successors(self):
        """Check for activities without successors"""
        # Build relationship map
        has_successor = set()
        for rel in self.relationships:
            has_successor.add(rel.pred_task_id)

        # Find activities without successors (excluding finish milestones)
        missing_succ = []
        for activity in self.activities:
            if (activity.task_type not in ['TT_Mile', 'TT_FinMile'] and
                activity.status != 'TK_Complete' and
                activity.task_id not in has_successor):
                missing_succ.append(f"{activity.task_code}: {activity.task_name}")

        if missing_succ:
            self.issues.append(ValidationIssue(
                rule_id="LOGIC-002",
                rule_name="Missing Successors",
                severity=Severity.HIGH,
                description="Activities without successor relationships (excluding milestones)",
                affected_items=missing_succ,
                recommendation="Add successor relationships to link activities to project completion"
            ))

    def _check_long_duration_activities(self):
        """Check for activities exceeding maximum duration"""
        MAX_DURATION_DAYS = 20  # 20 working days
        MAX_DURATION_HR = MAX_DURATION_DAYS * 8

        long_activities = []
        for activity in self.activities:
            if (activity.task_type == 'TT_Task' and
                activity.status != 'TK_Complete' and
                activity.duration_hr > MAX_DURATION_HR):
                duration_days = activity.duration_hr / 8
                long_activities.append(
                    f"{activity.task_code}: {activity.task_name} ({duration_days:.1f} days)"
                )

        if long_activities:
            pct = (len(long_activities) / len([a for a in self.activities if a.task_type == 'TT_Task'])) * 100

            self.issues.append(ValidationIssue(
                rule_id="DURATION-001",
                rule_name="Long Duration Activities",
                severity=Severity.MEDIUM if pct < 10 else Severity.HIGH,
                description=f"Activities exceeding {MAX_DURATION_DAYS} working days ({pct:.1f}% of tasks)",
                affected_items=long_activities,
                recommendation=f"Break down long activities into shorter increments (<{MAX_DURATION_DAYS} days) for better schedule control"
            ))

    def _check_zero_duration_non_milestones(self):
        """Check for zero-duration activities that are not milestones"""
        zero_duration = []
        for activity in self.activities:
            if (activity.duration_hr == 0 and
                activity.task_type not in ['TT_Mile', 'TT_FinMile']):
                zero_duration.append(f"{activity.task_code}: {activity.task_name} (Type: {activity.task_type})")

        if zero_duration:
            self.issues.append(ValidationIssue(
                rule_id="DURATION-002",
                rule_name="Zero Duration Non-Milestones",
                severity=Severity.HIGH,
                description="Non-milestone activities with zero duration",
                affected_items=zero_duration,
                recommendation="Change task type to milestone or assign appropriate duration"
            ))

    def _check_hard_constraints(self):
        """Check for excessive use of hard constraints"""
        CONSTRAINT_TYPES_HARD = ['CS_MSO', 'CS_MFO', 'CS_SNLT', 'CS_FNET', 'CS_FNLT', 'CS_SNET']

        constrained = []
        total_tasks = 0

        for activity in self.activities:
            if (activity.task_type not in ['TT_Mile', 'TT_FinMile'] and
                activity.status != 'TK_Complete'):
                total_tasks += 1
                if activity.constraint_type in CONSTRAINT_TYPES_HARD:
                    constrained.append(
                        f"{activity.task_code}: {activity.task_name} ({activity.constraint_type})"
                    )

        if constrained and total_tasks > 0:
            pct = (len(constrained) / total_tasks) * 100

            self.issues.append(ValidationIssue(
                rule_id="CONSTRAINT-001",
                rule_name="Excessive Hard Constraints",
                severity=Severity.MEDIUM if pct < 10 else Severity.HIGH,
                description=f"Activities with hard constraints ({pct:.1f}% of tasks, target <5%)",
                affected_items=constrained,
                recommendation="Remove unnecessary constraints and use logic relationships instead. Reserve constraints for contractual/regulatory dates only."
            ))

    def _check_logic_density(self):
        """Check relationship density (relationships per activity)"""
        if not self.activities:
            return

        # Count relationships (each relationship counts twice: one for pred, one for succ)
        total_rel_count = len(self.relationships) * 2
        logic_density = total_rel_count / len(self.activities)

        TARGET_DENSITY = 1.5

        if logic_density < TARGET_DENSITY:
            self.issues.append(ValidationIssue(
                rule_id="LOGIC-003",
                rule_name="Low Logic Density",
                severity=Severity.MEDIUM,
                description=f"Logic density is {logic_density:.2f} (target ≥{TARGET_DENSITY})",
                affected_items=[
                    f"Total activities: {len(self.activities)}",
                    f"Total relationships: {len(self.relationships)}",
                    f"Average relationships per activity: {logic_density:.2f}"
                ],
                recommendation="Add more relationship links between activities to improve schedule integration"
            ))

    def _check_high_float(self):
        """Check for activities with excessive float"""
        HIGH_FLOAT_DAYS = 44  # ~2 months
        HIGH_FLOAT_HR = HIGH_FLOAT_DAYS * 8

        high_float = []
        for activity in self.activities:
            if (activity.status != 'TK_Complete' and
                activity.total_float_hr > HIGH_FLOAT_HR):
                float_days = activity.total_float_hr / 8
                high_float.append(
                    f"{activity.task_code}: {activity.task_name} ({float_days:.1f} days float)"
                )

        if high_float:
            self.issues.append(ValidationIssue(
                rule_id="FLOAT-001",
                rule_name="High Float Activities",
                severity=Severity.LOW,
                description=f"Activities with >{HIGH_FLOAT_DAYS} days total float",
                affected_items=high_float,
                recommendation="Review logic for high-float activities - they may not be properly tied to project completion"
            ))

    def _check_negative_float(self):
        """Check for activities with negative float"""
        negative_float = []
        for activity in self.activities:
            if (activity.status != 'TK_Complete' and
                activity.total_float_hr < 0):
                float_days = activity.total_float_hr / 8
                negative_float.append(
                    f"{activity.task_code}: {activity.task_name} ({float_days:.1f} days)"
                )

        if negative_float:
            self.issues.append(ValidationIssue(
                rule_id="FLOAT-002",
                rule_name="Negative Float",
                severity=Severity.HIGH,
                description="Activities with negative float indicate schedule delays",
                affected_items=negative_float,
                recommendation="Develop recovery plan for negative float activities or adjust project completion date"
            ))

    def _check_invalid_relationships(self):
        """Check for invalid relationship types"""
        sf_relationships = []

        for rel in self.relationships:
            # Start-to-Finish is rare and often incorrect
            if rel.pred_type == 'PR_SF':
                # Find activity names
                pred_activity = next((a for a in self.activities if a.task_id == rel.pred_task_id), None)
                succ_activity = next((a for a in self.activities if a.task_id == rel.task_id), None)

                if pred_activity and succ_activity:
                    sf_relationships.append(
                        f"{pred_activity.task_code} -> {succ_activity.task_code}"
                    )

        if sf_relationships:
            self.issues.append(ValidationIssue(
                rule_id="LOGIC-004",
                rule_name="Start-to-Finish Relationships",
                severity=Severity.MEDIUM,
                description="Start-to-Finish relationships detected (rare and often incorrect)",
                affected_items=sf_relationships,
                recommendation="Review SF relationships to ensure they are logically correct and intentional"
            ))

    def _check_future_actuals(self):
        """Check for actual dates in the future"""
        from datetime import datetime

        future_actuals = []
        today = datetime.now().date()

        for activity in self.activities:
            # Check actual start
            if activity.actual_start_date:
                try:
                    actual_start = datetime.fromisoformat(activity.actual_start_date).date()
                    if actual_start > today:
                        future_actuals.append(
                            f"{activity.task_code}: {activity.task_name} (Actual Start: {activity.actual_start_date})"
                        )
                except:
                    pass

            # Check actual finish
            if activity.actual_end_date:
                try:
                    actual_end = datetime.fromisoformat(activity.actual_end_date).date()
                    if actual_end > today:
                        future_actuals.append(
                            f"{activity.task_code}: {activity.task_name} (Actual Finish: {activity.actual_end_date})"
                        )
                except:
                    pass

        if future_actuals:
            self.issues.append(ValidationIssue(
                rule_id="PROGRESS-001",
                rule_name="Future Actual Dates",
                severity=Severity.CRITICAL,
                description="Activities with actual dates in the future",
                affected_items=future_actuals,
                recommendation="Correct actual dates to be on or before today's date"
            ))

    def _check_invalid_percent_complete(self):
        """Check for invalid percent complete values"""
        invalid_pct = []

        for activity in self.activities:
            # Check range
            if activity.phys_complete_pct < 0 or activity.phys_complete_pct > 100:
                invalid_pct.append(
                    f"{activity.task_code}: {activity.task_name} ({activity.phys_complete_pct}%)"
                )
            # Check if started but no actual start
            elif activity.phys_complete_pct > 0 and not activity.actual_start_date:
                invalid_pct.append(
                    f"{activity.task_code}: {activity.task_name} ({activity.phys_complete_pct}% but no actual start)"
                )
            # Check if 100% but no actual finish
            elif activity.phys_complete_pct >= 100 and not activity.actual_end_date:
                invalid_pct.append(
                    f"{activity.task_code}: {activity.task_name} (100% but no actual finish)"
                )

        if invalid_pct:
            self.issues.append(ValidationIssue(
                rule_id="PROGRESS-002",
                rule_name="Invalid Percent Complete",
                severity=Severity.HIGH,
                description="Activities with invalid percent complete or misaligned actual dates",
                affected_items=invalid_pct,
                recommendation="Ensure percent complete aligns with actual dates and is within 0-100% range"
            ))

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate validation summary

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_issues': len(self.issues),
            'critical': sum(1 for i in self.issues if i.severity == Severity.CRITICAL),
            'high': sum(1 for i in self.issues if i.severity == Severity.HIGH),
            'medium': sum(1 for i in self.issues if i.severity == Severity.MEDIUM),
            'low': sum(1 for i in self.issues if i.severity == Severity.LOW),
            'total_activities': len(self.activities),
            'total_relationships': len(self.relationships)
        }
        return summary

    def generate_html_report(self, issues: List[ValidationIssue], output_path: str):
        """
        Generate HTML validation report

        Args:
            issues: List of validation issues
            output_path: Path to output HTML file
        """
        summary = self.generate_summary()

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Schedule Quality Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .issue {{ border-left: 4px solid #ccc; padding: 10px; margin: 10px 0; background: #fafafa; }}
        .critical {{ border-left-color: #d32f2f; }}
        .high {{ border-left-color: #f57c00; }}
        .medium {{ border-left-color: #fbc02d; }}
        .low {{ border-left-color: #388e3c; }}
        .severity {{ font-weight: bold; padding: 2px 8px; border-radius: 3px; color: white; }}
        .severity.critical {{ background: #d32f2f; }}
        .severity.high {{ background: #f57c00; }}
        .severity.medium {{ background: #fbc02d; color: #333; }}
        .severity.low {{ background: #388e3c; }}
        .affected-items {{ margin-top: 10px; background: white; padding: 10px; max-height: 200px; overflow-y: auto; }}
        .affected-items ul {{ margin: 5px 0; padding-left: 20px; }}
    </style>
</head>
<body>
    <h1>Schedule Quality Validation Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Total Issues:</strong> {summary['total_issues']}</p>
        <p><strong>Critical:</strong> {summary['critical']} |
           <strong>High:</strong> {summary['high']} |
           <strong>Medium:</strong> {summary['medium']} |
           <strong>Low:</strong> {summary['low']}</p>
        <p><strong>Total Activities:</strong> {summary['total_activities']}</p>
        <p><strong>Total Relationships:</strong> {summary['total_relationships']}</p>
    </div>

    <h2>Validation Issues</h2>
"""

        for issue in sorted(issues, key=lambda x: list(Severity).index(x.severity)):
            severity_class = issue.severity.value.lower()
            affected_list = ''.join(f'<li>{item}</li>' for item in issue.affected_items[:20])  # Limit to first 20
            more_items = f'<li><em>... and {len(issue.affected_items) - 20} more</em></li>' if len(issue.affected_items) > 20 else ''

            html += f"""
    <div class="issue {severity_class}">
        <h3>{issue.rule_name} <span class="severity {severity_class}">{issue.severity.value}</span></h3>
        <p><strong>Rule ID:</strong> {issue.rule_id}</p>
        <p><strong>Description:</strong> {issue.description}</p>
        <p><strong>Count:</strong> {issue.count} items</p>
        <p><strong>Recommendation:</strong> {issue.recommendation}</p>
        <div class="affected-items">
            <strong>Affected Items:</strong>
            <ul>{affected_list}{more_items}</ul>
        </div>
    </div>
"""

        html += """
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python schedule_validator.py <xer_file> [output.html]")
        sys.exit(1)

    xer_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'validation_report.html'

    print(f"Validating schedule: {xer_file}")
    validator = ScheduleValidator()
    issues = validator.validate_xer_file(xer_file)

    summary = validator.generate_summary()
    print(f"\nValidation Summary:")
    print(f"  Total Issues: {summary['total_issues']}")
    print(f"  Critical: {summary['critical']}")
    print(f"  High: {summary['high']}")
    print(f"  Medium: {summary['medium']}")
    print(f"  Low: {summary['low']}")

    validator.generate_html_report(issues, output_file)
    print(f"\nHTML report generated: {output_file}")


if __name__ == '__main__':
    main()

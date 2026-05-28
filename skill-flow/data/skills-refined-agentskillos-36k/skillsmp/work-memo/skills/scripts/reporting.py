"""Report generation for daily, weekly, and monthly work summaries."""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

from storage import WorkMemoStorage


class Reporting:
    """Generate work reports with aggregation and insights"""

    def __init__(self, storage: WorkMemoStorage):
        self.storage = storage

    def get_daily_report(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate daily report for specific date or today.

        Returns:
            Dictionary with:
            - date: str (ISO 8601)
            - summary: Dict with total, completed, pending, overdue
            - by_type: Dict[str, int]
            - by_status: Dict[str, int]
            - time_spent: int (total minutes)
            - records: List[WorkRecord]
        """
        if date_str is None:
            report_date = datetime.utcnow()
        else:
            try:
                report_date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                report_date = datetime.utcnow()

        start_date = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = report_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        records = self.storage.get_by_date_range(
            start_date.isoformat(),
            end_date.isoformat()
        )

        completed = [r for r in records if r.status.value == 'done']
        pending = [r for r in records if r.status.value != 'done']
        overdue = [r for r in pending if r.is_overdue()]

        by_type = defaultdict(int)
        for record in records:
            by_type[record.type.value] += 1

        by_status = defaultdict(int)
        for record in records:
            by_status[record.status.value] += 1

        time_spent = sum([r.time_spent or 0 for r in completed])

        return {
            'date': report_date.strftime('%Y-%m-%d'),
            'summary': {
                'total': len(records),
                'completed': len(completed),
                'pending': len(pending),
                'overdue': len(overdue)
            },
            'by_type': dict(by_type),
            'by_status': dict(by_status),
            'time_spent': time_spent,
            'records': records
        }

    def get_weekly_report(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate weekly report for current week or specified date's week.

        Returns:
            Dictionary with:
            - week_start: str (ISO 8601, Monday)
            - week_end: str (ISO 8601, Sunday)
            - summary: Dict with total, completed, pending, overdue
            - eisenhower_matrix: Dict[str, int] (Q1, Q2, Q3, Q4 counts)
            - by_type: Dict[str, int]
            - by_status: Dict[str, int]
            - priority_distribution: Dict[str, int]
            - time_spent: int (total minutes)
            - records: List[WorkRecord]
        """
        if date_str is None:
            reference_date = datetime.utcnow()
        else:
            try:
                reference_date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                reference_date = datetime.utcnow()

        days_since_monday = reference_date.weekday()
        week_start = (reference_date - timedelta(days=days_since_monday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        records = self.storage.get_by_date_range(
            week_start.isoformat(),
            week_end.isoformat()
        )

        completed = [r for r in records if r.status.value == 'done']
        pending = [r for r in records if r.status.value != 'done']
        overdue = [r for r in pending if r.is_overdue()]

        eisenhower_matrix = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0}
        for record in pending:
            quadrant = record.get_eisenhower_quadrant()
            eisenhower_matrix[quadrant] += 1

        by_type = defaultdict(int)
        for record in records:
            by_type[record.type.value] += 1

        by_status = defaultdict(int)
        for record in records:
            by_status[record.status.value] += 1

        priority_dist = defaultdict(int)
        for record in records:
            priority_level = self._get_priority_level(record.urgency)
            priority_dist[priority_level] += 1

        time_spent = sum([r.time_spent or 0 for r in completed])

        return {
            'week_start': week_start.strftime('%Y-%m-%d'),
            'week_end': week_end.strftime('%Y-%m-%d'),
            'summary': {
                'total': len(records),
                'completed': len(completed),
                'pending': len(pending),
                'overdue': len(overdue)
            },
            'eisenhower_matrix': eisenhower_matrix,
            'by_type': dict(by_type),
            'by_status': dict(by_status),
            'priority_distribution': dict(priority_dist),
            'time_spent': time_spent,
            'records': records
        }

    def get_monthly_report(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate monthly report for current month or specified year/month.

        Returns:
            Dictionary with:
            - month_start: str (ISO 8601, 1st of month)
            - month_end: str (ISO 8601, last day of month)
            - summary: Dict with total, completed, pending, overdue
            - by_type: Dict[str, int]
            - by_status: Dict[str, int]
            - by_project: Dict[str, int]
            - by_assignee: Dict[str, int]
            - weekly_breakdown: List[Dict[str, int]]
            - time_spent: int (total minutes)
            - records: List[WorkRecord]
        """
        if year is None or month is None:
            reference_date = datetime.utcnow()
            year = reference_date.year
            month = reference_date.month

        month_start = datetime(year, month, 1, 0, 0, 0)

        if month == 12:
            month_end = datetime(year + 1, 1, 1, 0, 0) - timedelta(seconds=1)
        else:
            month_end = datetime(year, month + 1, 1, 0, 0, 0) - timedelta(seconds=1)

        records = self.storage.get_by_date_range(
            month_start.isoformat(),
            month_end.isoformat()
        )

        completed = [r for r in records if r.status.value == 'done']
        pending = [r for r in records if r.status.value != 'done']
        overdue = [r for r in pending if r.is_overdue()]

        by_type = defaultdict(int)
        for record in records:
            by_type[record.type.value] += 1

        by_status = defaultdict(int)
        for record in records:
            by_status[record.status.value] += 1

        by_project = defaultdict(int)
        for record in records:
            for project in record.projects:
                by_project[project] += 1

        by_assignee = defaultdict(int)
        for record in records:
            if record.assignee:
                by_assignee[record.assignee.name] += 1

        weekly_breakdown = self._calculate_weekly_breakdown(records, year, month)

        time_spent = sum([r.time_spent or 0 for r in completed])

        return {
            'month_start': month_start.strftime('%Y-%m-%d'),
            'month_end': month_end.strftime('%Y-%m-%d'),
            'summary': {
                'total': len(records),
                'completed': len(completed),
                'pending': len(pending),
                'overdue': len(overdue)
            },
            'by_type': dict(by_type),
            'by_status': dict(by_status),
            'by_project': dict(by_project),
            'by_assignee': dict(by_assignee),
            'weekly_breakdown': weekly_breakdown,
            'time_spent': time_spent,
            'records': records
        }

    def format_daily_report(self, report: Dict[str, Any]) -> str:
        """Format daily report as readable text"""
        summary_data = report['summary']
        lines = [
            f"=== Daily Report for {report['date']} ===",
            "",
            f"Summary: {summary_data['total']} total, "
            f"{summary_data['completed']} completed, "
            f"{summary_data['pending']} pending, "
            f"{summary_data['overdue']} overdue",
            "",
            f"Time Spent: {report['time_spent']} minutes",
            "",
            "By Type:",
        ]

        for work_type, count in sorted(report['by_type'].items(), key=lambda x: -x[1]):
            lines.append(f"  {work_type}: {count}")

        lines.extend([
            "",
            "By Status:",
        ])

        for status, count in sorted(report['by_status'].items(), key=lambda x: -x[1]):
            lines.append(f"  {status}: {count}")

        lines.append("")
        lines.append("Records:")

        for record in report['records']:
            urgency_str = f"[U{record.urgency}]" if record.urgency >= 4 else ""
            lines.append(f"  - {record.title} {urgency_str} ({record.status.value})")

        return "\n".join(lines)

    def format_weekly_report(self, report: Dict[str, Any]) -> str:
        """Format weekly report as readable text"""
        summary_data = report['summary']
        lines = [
            f"=== Weekly Report ({report['week_start']} to {report['week_end']}) ===",
            "",
            f"Summary: {summary_data['total']} total, "
            f"{summary_data['completed']} completed, "
            f"{summary_data['pending']} pending, "
            f"{summary_data['overdue']} overdue",
            "",
            f"Time Spent: {report['time_spent']} minutes",
            "",
            "Eisenhower Matrix:",
        ]

        for quadrant, count in report['eisenhower_matrix'].items():
            action = {
                'Q1': 'Do Now',
                'Q2': 'Schedule',
                'Q3': 'Delegate',
                'Q4': 'Eliminate'
            }[quadrant]
            lines.append(f"  {quadrant} ({action}): {count}")

        lines.extend([
            "",
            "By Type:",
        ])

        for work_type, count in sorted(report['by_type'].items(), key=lambda x: -x[1]):
            lines.append(f"  {work_type}: {count}")

        return "\n".join(lines)

    def format_monthly_report(self, report: Dict[str, Any]) -> str:
        """Format monthly report as readable text"""
        summary_data = report['summary']
        lines = [
            f"=== Monthly Report ({report['month_start']} to {report['month_end']}) ===",
            "",
            f"Summary: {summary_data['total']} total, "
            f"{summary_data['completed']} completed, "
            f"{summary_data['pending']} pending, "
            f"{summary_data['overdue']} overdue",
            "",
            f"Time Spent: {report['time_spent']} minutes",
            "",
            "By Project:",
        ]

        for project, count in sorted(report['by_project'].items(), key=lambda x: -x[1]):
            lines.append(f"  {project}: {count}")

        lines.extend([
            "",
            "By Assignee:",
        ])

        for assignee, count in sorted(report['by_assignee'].items(), key=lambda x: -x[1]):
            lines.append(f"  {assignee}: {count}")

        lines.extend([
            "",
            "Weekly Breakdown:",
        ])

        for week in report['weekly_breakdown']:
            lines.append(f"  Week {week['week']}: {week['total']} records")

        return "\n".join(lines)

    def _get_priority_level(self, urgency: int) -> str:
        """Convert urgency number to level name"""
        if urgency >= 5:
            return 'Very High'
        elif urgency >= 4:
            return 'High'
        elif urgency >= 3:
            return 'Medium'
        elif urgency >= 2:
            return 'Low'
        else:
            return 'Very Low'

    def _calculate_weekly_breakdown(self, records: List, year: int, month: int) -> List[Dict[str, int]]:
        """Calculate weekly breakdown for monthly report"""
        weekly_counts = defaultdict(int)

        for record in records:
            try:
                record_date = datetime.fromisoformat(record.created_at)
                week_number = record_date.isocalendar()[1]
                if record_date.year == year and record_date.month == month:
                    weekly_counts[week_number] += 1
            except:
                pass

        return [{'week': week, 'total': count} for week, count in sorted(weekly_counts.items())]


if __name__ == "__main__":
    from storage import WorkMemoStorage

    storage = WorkMemoStorage()
    reporting = Reporting(storage)

    print("=== Daily Report ===")
    daily = reporting.get_daily_report()
    print(reporting.format_daily_report(daily))

    print("\n=== Weekly Report ===")
    weekly = reporting.get_weekly_report()
    print(reporting.format_weekly_report(weekly))

    print("\n=== Monthly Report ===")
    monthly = reporting.get_monthly_report()
    print(reporting.format_monthly_report(monthly))

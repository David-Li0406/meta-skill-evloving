#!/usr/bin/env python3
"""
XER File Parser for Primavera P6

Parses XER (P6 export) files and extracts activities, relationships, resources, and other schedule data.
Supports conversion to structured formats (JSON, CSV, SQLite) for analysis.

Usage:
    parser = XERParser('schedule.xer')
    activities = parser.get_activities()
    relationships = parser.get_relationships()
    parser.export_to_json('output.json')
"""

import re
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Activity:
    """Represents a P6 activity/task"""
    task_id: str
    task_code: str
    task_name: str
    task_type: str
    status: str
    duration_hr: float
    total_float_hr: float
    free_float_hr: float
    target_start_date: Optional[str]
    target_end_date: Optional[str]
    actual_start_date: Optional[str]
    actual_end_date: Optional[str]
    remain_drtn_hr: float
    phys_complete_pct: float
    wbs_id: str
    proj_id: str
    constraint_type: Optional[str]
    constraint_date: Optional[str]

    def is_critical(self) -> bool:
        """Check if activity is on critical path"""
        return self.total_float_hr <= 0

    def is_complete(self) -> bool:
        """Check if activity is complete"""
        return self.phys_complete_pct >= 100.0 or self.actual_end_date is not None


@dataclass
class Relationship:
    """Represents a predecessor/successor relationship"""
    pred_task_id: str
    task_id: str
    pred_type: str
    lag_hr: float

    def get_type_name(self) -> str:
        """Get human-readable relationship type"""
        types = {
            'PR_FS': 'Finish-to-Start',
            'PR_SS': 'Start-to-Start',
            'PR_FF': 'Finish-to-Finish',
            'PR_SF': 'Start-to-Finish'
        }
        return types.get(self.pred_type, self.pred_type)


@dataclass
class Resource:
    """Represents a resource assignment"""
    taskrsrc_id: str
    task_id: str
    rsrc_id: str
    target_qty: float
    remain_qty: float
    actual_qty: float


class XERParser:
    """Parser for Primavera P6 XER files"""

    def __init__(self, xer_file_path: str):
        """
        Initialize parser with XER file path

        Args:
            xer_file_path: Path to the XER file
        """
        self.xer_file_path = xer_file_path
        self.tables: Dict[str, List[List[str]]] = {}
        self.table_headers: Dict[str, List[str]] = {}
        self._parse_xer_file()

    def _parse_xer_file(self):
        """Parse XER file and extract tables"""
        with open(self.xer_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Split into table sections
        # XER format: %T <table_name>\n%F <field1>\t<field2>...\n%R <val1>\t<val2>...
        table_pattern = r'%T\s+(\w+)\n%F\s+(.*?)\n((?:%R\s+.*?\n)+)'

        matches = re.finditer(table_pattern, content, re.MULTILINE)

        for match in matches:
            table_name = match.group(1)
            fields = match.group(2).split('\t')
            rows_text = match.group(3)

            # Store headers
            self.table_headers[table_name] = fields

            # Parse rows
            rows = []
            for line in rows_text.strip().split('\n'):
                if line.startswith('%R'):
                    values = line[3:].split('\t')  # Remove '%R '
                    rows.append(values)

            self.tables[table_name] = rows

    def _get_table_data(self, table_name: str) -> List[Dict[str, str]]:
        """
        Convert table rows to list of dictionaries

        Args:
            table_name: Name of the table (e.g., 'TASK', 'TASKPRED')

        Returns:
            List of dictionaries with field names as keys
        """
        if table_name not in self.tables:
            return []

        headers = self.table_headers[table_name]
        rows = self.tables[table_name]

        result = []
        for row in rows:
            # Pad row if it has fewer values than headers
            padded_row = row + [''] * (len(headers) - len(row))
            result.append(dict(zip(headers, padded_row)))

        return result

    def get_activities(self, project_id: Optional[str] = None) -> List[Activity]:
        """
        Extract all activities from XER file

        Args:
            project_id: Optional project ID to filter activities

        Returns:
            List of Activity objects
        """
        task_data = self._get_table_data('TASK')

        activities = []
        for row in task_data:
            # Filter by project if specified
            if project_id and row.get('proj_id') != project_id:
                continue

            activity = Activity(
                task_id=row.get('task_id', ''),
                task_code=row.get('task_code', ''),
                task_name=row.get('task_name', ''),
                task_type=row.get('task_type', ''),
                status=row.get('status_code', ''),
                duration_hr=float(row.get('target_drtn_hr_cnt', 0) or 0),
                total_float_hr=float(row.get('total_float_hr_cnt', 0) or 0),
                free_float_hr=float(row.get('free_float_hr_cnt', 0) or 0),
                target_start_date=row.get('target_start_date'),
                target_end_date=row.get('target_end_date'),
                actual_start_date=row.get('act_start_date'),
                actual_end_date=row.get('act_end_date'),
                remain_drtn_hr=float(row.get('remain_drtn_hr_cnt', 0) or 0),
                phys_complete_pct=float(row.get('phys_complete_pct', 0) or 0),
                wbs_id=row.get('wbs_id', ''),
                proj_id=row.get('proj_id', ''),
                constraint_type=row.get('cstr_type'),
                constraint_date=row.get('cstr_date')
            )
            activities.append(activity)

        return activities

    def get_relationships(self) -> List[Relationship]:
        """
        Extract all activity relationships

        Returns:
            List of Relationship objects
        """
        pred_data = self._get_table_data('TASKPRED')

        relationships = []
        for row in pred_data:
            relationship = Relationship(
                pred_task_id=row.get('pred_task_id', ''),
                task_id=row.get('task_id', ''),
                pred_type=row.get('pred_type', 'PR_FS'),
                lag_hr=float(row.get('lag_hr_cnt', 0) or 0)
            )
            relationships.append(relationship)

        return relationships

    def get_resources(self) -> List[Resource]:
        """
        Extract all resource assignments

        Returns:
            List of Resource objects
        """
        rsrc_data = self._get_table_data('TASKRSRC')

        resources = []
        for row in rsrc_data:
            resource = Resource(
                taskrsrc_id=row.get('taskrsrc_id', ''),
                task_id=row.get('task_id', ''),
                rsrc_id=row.get('rsrc_id', ''),
                target_qty=float(row.get('target_qty', 0) or 0),
                remain_qty=float(row.get('remain_qty', 0) or 0),
                actual_qty=float(row.get('act_reg_qty', 0) or 0)
            )
            resources.append(resource)

        return resources

    def get_critical_activities(self, project_id: Optional[str] = None) -> List[Activity]:
        """
        Get activities on critical path

        Args:
            project_id: Optional project ID to filter

        Returns:
            List of critical Activity objects
        """
        activities = self.get_activities(project_id)
        return [a for a in activities if a.is_critical()]

    def get_project_info(self) -> Dict[str, Any]:
        """
        Extract project information

        Returns:
            Dictionary with project details
        """
        project_data = self._get_table_data('PROJECT')

        if not project_data:
            return {}

        # Assume first project in file
        proj = project_data[0]
        return {
            'proj_id': proj.get('proj_id'),
            'proj_short_name': proj.get('proj_short_name'),
            'proj_name': proj.get('proj_name'),
            'plan_start_date': proj.get('plan_start_date'),
            'plan_end_date': proj.get('plan_end_date'),
            'scd_end_date': proj.get('scd_end_date'),
            'status': proj.get('status_code')
        }

    def export_to_json(self, output_path: str, indent: int = 2):
        """
        Export parsed data to JSON

        Args:
            output_path: Path to output JSON file
            indent: JSON indentation (default: 2)
        """
        data = {
            'project': self.get_project_info(),
            'activities': [asdict(a) for a in self.get_activities()],
            'relationships': [asdict(r) for r in self.get_relationships()],
            'resources': [asdict(r) for r in self.get_resources()]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)

    def export_activities_to_csv(self, output_path: str):
        """
        Export activities to CSV

        Args:
            output_path: Path to output CSV file
        """
        activities = self.get_activities()

        if not activities:
            return

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(activities[0]).keys())
            writer.writeheader()
            for activity in activities:
                writer.writerow(asdict(activity))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get schedule statistics

        Returns:
            Dictionary with schedule metrics
        """
        activities = self.get_activities()
        relationships = self.get_relationships()

        if not activities:
            return {}

        critical = [a for a in activities if a.is_critical()]
        completed = [a for a in activities if a.is_complete()]
        in_progress = [a for a in activities if a.actual_start_date and not a.is_complete()]
        not_started = [a for a in activities if not a.actual_start_date]

        # Calculate logic density
        logic_density = (len(relationships) * 2) / len(activities) if activities else 0

        return {
            'total_activities': len(activities),
            'critical_activities': len(critical),
            'completed_activities': len(completed),
            'in_progress_activities': len(in_progress),
            'not_started_activities': len(not_started),
            'total_relationships': len(relationships),
            'logic_density': round(logic_density, 2),
            'avg_duration_days': round(sum(a.duration_hr for a in activities) / len(activities) / 8, 1),
            'avg_total_float_days': round(sum(a.total_float_hr for a in activities) / len(activities) / 8, 1)
        }


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parse_xer.py <xer_file> [output.json]")
        sys.exit(1)

    xer_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.json'

    print(f"Parsing XER file: {xer_file}")
    parser = XERParser(xer_file)

    # Print statistics
    stats = parser.get_statistics()
    print("\nSchedule Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Export to JSON
    parser.export_to_json(output_file)
    print(f"\nExported to: {output_file}")

    # Show critical activities
    critical = parser.get_critical_activities()
    print(f"\nCritical Activities ({len(critical)}):")
    for activity in critical[:10]:  # Show first 10
        print(f"  {activity.task_code}: {activity.task_name}")


if __name__ == '__main__':
    main()

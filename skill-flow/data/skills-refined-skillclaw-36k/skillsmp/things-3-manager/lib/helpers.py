"""
Helper functions for formatting and displaying Things 3 data
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class ThingsFormatter:
    """Format Things 3 data for display"""

    @staticmethod
    def format_task(task: Dict[str, Any], verbose: bool = False, show_uuid: bool = False) -> str:
        """
        Format a single task for display

        Args:
            task: Task dictionary from things.py
            verbose: Include notes, tags, and other metadata
            show_uuid: Include UUID in output
        """
        status = task.get('status', 'incomplete')

        # Checkbox based on status
        if status == 'completed':
            checkbox = '☑'
        elif status == 'canceled':
            checkbox = '☒'
        else:
            checkbox = '☐'

        title = task.get('title', 'Untitled')
        output = f"{checkbox} {title}"

        if show_uuid:
            output += f" [{task.get('uuid', 'no-id')}]"

        if verbose:
            lines = [output]

            # Notes
            notes = task.get('notes')
            if notes:
                # Truncate long notes
                if len(notes) > 100:
                    notes = notes[:100] + '...'
                lines.append(f"   📝 {notes}")

            # Tags
            tags = task.get('tags', [])
            if tags:
                tag_names = ', '.join([t.get('title', '') for t in tags])
                lines.append(f"   🏷️  {tag_names}")

            # Project
            project = task.get('project')
            if project:
                lines.append(f"   📂 {project.get('title', '')}")

            # Area
            area = task.get('area')
            if area:
                lines.append(f"   📍 {area.get('title', '')}")

            # Deadline
            deadline = task.get('deadline')
            if deadline:
                lines.append(f"   ⏰ Deadline: {ThingsFormatter._format_date(deadline)}")

            # When (scheduled date)
            start_date = task.get('start_date')
            if start_date:
                lines.append(f"   📅 Scheduled: {ThingsFormatter._format_date(start_date)}")

            output = '\n'.join(lines)

        return output

    @staticmethod
    def format_task_list(
        tasks: List[Dict[str, Any]],
        verbose: bool = False,
        show_uuid: bool = False,
        group_by: Optional[str] = None
    ) -> str:
        """
        Format a list of tasks

        Args:
            tasks: List of task dictionaries
            verbose: Include metadata for each task
            show_uuid: Include UUIDs
            group_by: Group by 'project', 'area', or 'tag'
        """
        if not tasks:
            return "No tasks found."

        if group_by:
            return ThingsFormatter._format_grouped_tasks(tasks, group_by, verbose, show_uuid)

        lines = []
        for task in tasks:
            lines.append(ThingsFormatter.format_task(task, verbose, show_uuid))

        return '\n\n'.join(lines)

    @staticmethod
    def _format_grouped_tasks(
        tasks: List[Dict[str, Any]],
        group_by: str,
        verbose: bool,
        show_uuid: bool
    ) -> str:
        """Format tasks grouped by project, area, or tag"""
        groups: Dict[str, List[Dict[str, Any]]] = {}

        for task in tasks:
            if group_by == 'project':
                project = task.get('project')
                key = project.get('title', 'No Project') if project else 'No Project'
            elif group_by == 'area':
                area = task.get('area')
                key = area.get('title', 'No Area') if area else 'No Area'
            elif group_by == 'tag':
                tags = task.get('tags', [])
                key = tags[0].get('title', 'No Tags') if tags else 'No Tags'
            else:
                key = 'All Tasks'

            if key not in groups:
                groups[key] = []
            groups[key].append(task)

        lines = []
        for group_name in sorted(groups.keys()):
            group_tasks = groups[group_name]
            lines.append(f"\n═══ {group_name} ({len(group_tasks)}) ═══")
            for task in group_tasks:
                lines.append(ThingsFormatter.format_task(task, verbose, show_uuid))

        return '\n'.join(lines)

    @staticmethod
    def format_project(project: Dict[str, Any], include_tasks: bool = False) -> str:
        """Format a project for display"""
        title = project.get('title', 'Untitled Project')
        output = f"📁 {title}"

        area = project.get('area')
        if area:
            output += f" ({area.get('title', '')})"

        # Count tasks
        todos = project.get('todos', [])
        if todos:
            completed = sum(1 for t in todos if t.get('status') == 'completed')
            total = len(todos)
            output += f" - {completed}/{total} tasks"

        if include_tasks and todos:
            output += "\n"
            for todo in todos:
                output += "\n  " + ThingsFormatter.format_task(todo, verbose=False)

        return output

    @staticmethod
    def format_project_list(projects: List[Dict[str, Any]], include_tasks: bool = False) -> str:
        """Format a list of projects"""
        if not projects:
            return "No projects found."

        lines = []
        for project in projects:
            lines.append(ThingsFormatter.format_project(project, include_tasks))

        return '\n\n'.join(lines)

    @staticmethod
    def _format_date(date_value: Any) -> str:
        """Format a date value from Things database"""
        if isinstance(date_value, str):
            try:
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except:
                return str(date_value)
        return str(date_value)

    @staticmethod
    def to_json(data: Any, pretty: bool = True) -> str:
        """Convert data to JSON string"""
        if pretty:
            return json.dumps(data, indent=2, default=str, ensure_ascii=False)
        return json.dumps(data, default=str, ensure_ascii=False)

    @staticmethod
    def summarize_tasks(tasks: List[Dict[str, Any]]) -> str:
        """Create a summary of tasks"""
        total = len(tasks)
        if total == 0:
            return "No tasks."

        completed = sum(1 for t in tasks if t.get('status') == 'completed')
        incomplete = sum(1 for t in tasks if t.get('status') == 'incomplete')
        canceled = sum(1 for t in tasks if t.get('status') == 'canceled')

        # Count tasks with deadlines
        with_deadline = sum(1 for t in tasks if t.get('deadline'))

        # Count tasks with tags
        tagged = sum(1 for t in tasks if t.get('tags'))

        summary = [
            f"📊 Summary: {total} total tasks",
            f"   ☐ {incomplete} incomplete",
            f"   ☑ {completed} completed",
        ]

        if canceled > 0:
            summary.append(f"   ☒ {canceled} canceled")

        if with_deadline > 0:
            summary.append(f"   ⏰ {with_deadline} with deadlines")

        if tagged > 0:
            summary.append(f"   🏷️  {tagged} tagged")

        return '\n'.join(summary)

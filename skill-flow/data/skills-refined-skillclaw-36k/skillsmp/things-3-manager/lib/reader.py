"""
Things 3 Reader - Wraps things.py for reading tasks, projects, and areas
"""
import things
from typing import List, Dict, Any, Optional


class ThingsReader:
    """Read-only access to Things 3 database using things.py"""

    @staticmethod
    def get_today() -> List[Dict[str, Any]]:
        """Get all tasks in the Today list"""
        all_tasks = things.todos(status='incomplete')
        # Filter for tasks in Today list (today_index is set)
        today_tasks = [t for t in all_tasks if t.get('today_index') is not None]
        # Sort by today_index to preserve order
        today_tasks.sort(key=lambda t: t.get('today_index', 999))
        return today_tasks

    @staticmethod
    def get_inbox() -> List[Dict[str, Any]]:
        """Get all tasks in the inbox"""
        return things.todos(start='inbox')

    @staticmethod
    def get_upcoming() -> List[Dict[str, Any]]:
        """Get all tasks scheduled for upcoming days (not in Today)"""
        from datetime import date
        all_tasks = things.todos(status='incomplete')
        today_str = date.today().isoformat()
        # Tasks with start_date in the future, not in Today
        upcoming = [
            t for t in all_tasks
            if t.get('start_date')
            and t.get('start_date') > today_str
            and t.get('today_index') is None
        ]
        # Sort by start_date
        upcoming.sort(key=lambda t: t.get('start_date', ''))
        return upcoming

    @staticmethod
    def get_anytime() -> List[Dict[str, Any]]:
        """Get all tasks in the Anytime list"""
        return things.todos(start='anytime')

    @staticmethod
    def get_all_todos(status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all todos, optionally filtered by status

        Args:
            status: Filter by status ('incomplete', 'completed', 'canceled')
        """
        todos = things.todos()

        if status:
            todos = [t for t in todos if t.get('status') == status]

        return todos

    @staticmethod
    def search(
        query: str,
        status: Optional[str] = None,
        area: Optional[str] = None,
        project: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search tasks by keyword and filters

        Args:
            query: Search term to find in title or notes
            status: Filter by status ('incomplete', 'completed', 'canceled')
            area: Filter by area name
            project: Filter by project name
            tag: Filter by tag name
        """
        todos = things.todos()
        results = []

        for todo in todos:
            # Check query match
            title = todo.get('title', '').lower()
            notes = todo.get('notes', '').lower()
            query_lower = query.lower()

            if query_lower not in title and query_lower not in notes:
                continue

            # Check status filter
            if status and todo.get('status') != status:
                continue

            # Check area filter
            if area:
                todo_area = todo.get('area')
                if not todo_area or todo_area.get('title', '').lower() != area.lower():
                    continue

            # Check project filter
            if project:
                todo_project = todo.get('project')
                if not todo_project or todo_project.get('title', '').lower() != project.lower():
                    continue

            # Check tag filter
            if tag:
                todo_tags = todo.get('tags', [])
                tag_titles = [t.get('title', '').lower() for t in todo_tags]
                if tag.lower() not in tag_titles:
                    continue

            results.append(todo)

        return results

    @staticmethod
    def get_projects(area: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all projects, optionally filtered by area

        Args:
            area: Filter by area name
        """
        projects = things.projects()

        if area:
            projects = [
                p for p in projects
                if p.get('area') and p['area'].get('title', '').lower() == area.lower()
            ]

        return projects

    @staticmethod
    def get_areas() -> List[Dict[str, Any]]:
        """Get all areas"""
        return things.areas()

    @staticmethod
    def get_tags() -> List[Dict[str, Any]]:
        """Get all tags"""
        return things.tags()

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific item by UUID

        Args:
            uuid: The UUID of the item to retrieve
        """
        try:
            return things.get(uuid)
        except:
            return None

    @staticmethod
    def find_by_title(title: str) -> List[Dict[str, Any]]:
        """
        Find tasks by exact or partial title match

        Args:
            title: The title to search for
        """
        todos = things.todos()
        title_lower = title.lower()

        return [
            t for t in todos
            if title_lower in t.get('title', '').lower()
        ]

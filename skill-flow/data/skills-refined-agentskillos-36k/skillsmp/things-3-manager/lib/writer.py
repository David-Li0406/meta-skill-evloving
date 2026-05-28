"""
Things 3 Writer - Wraps Things URL scheme for creating and updating tasks
"""
import subprocess
import urllib.parse
from typing import Optional, List, Dict, Any
import os
import json
from pathlib import Path


class ThingsWriter:
    """Write operations for Things 3 using URL scheme"""

    CONFIG_DIR = Path.home() / '.config' / 'things-skills'
    CONFIG_FILE = CONFIG_DIR / 'config.json'

    @staticmethod
    def _get_auth_token() -> Optional[str]:
        """Get Things auth token from config or environment"""
        # Try environment variable first
        token = os.getenv('THINGS_AUTH_TOKEN')
        if token:
            return token

        # Try config file
        if ThingsWriter.CONFIG_FILE.exists():
            try:
                with open(ThingsWriter.CONFIG_FILE) as f:
                    config = json.load(f)
                    return config.get('auth_token')
            except:
                pass

        return None

    @staticmethod
    def set_auth_token(token: str) -> None:
        """Save auth token to config file"""
        ThingsWriter.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config = {'auth_token': token}
        with open(ThingsWriter.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    @staticmethod
    def _open_url(url: str) -> None:
        """Open a Things URL scheme URL"""
        subprocess.run(['open', url], check=True)

    @staticmethod
    def add_task(
        title: str,
        notes: Optional[str] = None,
        when: Optional[str] = None,
        deadline: Optional[str] = None,
        tags: Optional[List[str]] = None,
        list_name: Optional[str] = None,
        checklist_items: Optional[List[str]] = None,
        heading: Optional[str] = None
    ) -> None:
        """
        Add a new task to Things

        Args:
            title: Task title (required)
            notes: Task notes
            when: When to schedule (today, tomorrow, evening, anytime, someday, YYYY-MM-DD)
            deadline: Deadline date (YYYY-MM-DD)
            tags: List of tag names
            list_name: Name of project or area to add to
            checklist_items: List of checklist item titles
            heading: Heading within project to add under
        """
        params = {'title': title}

        if notes:
            params['notes'] = notes
        if when:
            params['when'] = when
        if deadline:
            params['deadline'] = deadline
        if tags:
            params['tags'] = ','.join(tags)
        if list_name:
            params['list'] = list_name
        if checklist_items:
            params['checklist-items'] = '\n'.join(checklist_items)
        if heading:
            params['heading'] = heading

        url = f"things:///add?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
        ThingsWriter._open_url(url)

    @staticmethod
    def add_project(
        title: str,
        notes: Optional[str] = None,
        when: Optional[str] = None,
        deadline: Optional[str] = None,
        tags: Optional[List[str]] = None,
        area: Optional[str] = None,
        todos: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add a new project to Things

        Args:
            title: Project title (required)
            notes: Project notes
            when: When to schedule
            deadline: Deadline date
            tags: List of tag names
            area: Name of area to add to
            todos: List of todo dictionaries with 'title' and optional 'notes'
        """
        params = {'title': title}

        if notes:
            params['notes'] = notes
        if when:
            params['when'] = when
        if deadline:
            params['deadline'] = deadline
        if tags:
            params['tags'] = ','.join(tags)
        if area:
            params['area'] = area
        if todos:
            # Format todos as newline-separated titles
            todo_titles = [t['title'] for t in todos]
            params['to-dos'] = '\n'.join(todo_titles)

        url = f"things:///add-project?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
        ThingsWriter._open_url(url)

    @staticmethod
    def update_task(
        task_id: str,
        title: Optional[str] = None,
        notes: Optional[str] = None,
        prepend_notes: Optional[str] = None,
        append_notes: Optional[str] = None,
        when: Optional[str] = None,
        deadline: Optional[str] = None,
        tags: Optional[List[str]] = None,
        completed: Optional[bool] = None,
        canceled: Optional[bool] = None
    ) -> None:
        """
        Update an existing task

        Args:
            task_id: UUID of task to update (required)
            title: New title
            notes: New notes (replaces existing)
            prepend_notes: Notes to prepend
            append_notes: Notes to append
            when: New schedule
            deadline: New deadline
            tags: New tags (replaces existing)
            completed: Mark as completed (True) or incomplete (False)
            canceled: Mark as canceled (True)

        Requires auth token to be configured
        """
        auth_token = ThingsWriter._get_auth_token()
        if not auth_token:
            raise ValueError(
                "Auth token not configured. Get it from Things > Preferences > General > "
                "Enable Things URLs, then save it with: "
                "python -c \"from lib.writer import ThingsWriter; ThingsWriter.set_auth_token('YOUR_TOKEN')\""
            )

        params = {
            'id': task_id,
            'auth-token': auth_token
        }

        if title is not None:
            params['title'] = title
        if notes is not None:
            params['notes'] = notes
        if prepend_notes is not None:
            params['prepend-notes'] = prepend_notes
        if append_notes is not None:
            params['append-notes'] = append_notes
        if when is not None:
            params['when'] = when
        if deadline is not None:
            params['deadline'] = deadline
        if tags is not None:
            params['tags'] = ','.join(tags)
        if completed is not None:
            params['completed'] = 'true' if completed else 'false'
        if canceled is not None:
            params['canceled'] = 'true' if canceled else 'false'

        url = f"things:///update?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"
        ThingsWriter._open_url(url)

    @staticmethod
    def complete_task(task_id: str) -> None:
        """
        Mark a task as completed

        Args:
            task_id: UUID of task to complete
        """
        ThingsWriter.update_task(task_id, completed=True)

    @staticmethod
    def cancel_task(task_id: str) -> None:
        """
        Mark a task as canceled

        Args:
            task_id: UUID of task to cancel
        """
        ThingsWriter.update_task(task_id, canceled=True)

    @staticmethod
    def show_list(list_name: str) -> None:
        """
        Show a specific list in Things

        Args:
            list_name: today, inbox, upcoming, anytime, someday, logbook, or list ID
        """
        url = f"things:///show?id={urllib.parse.quote(list_name)}"
        ThingsWriter._open_url(url)

    @staticmethod
    def search_things(query: str) -> None:
        """
        Open Things search with a query

        Args:
            query: Search term
        """
        url = f"things:///search?query={urllib.parse.quote(query)}"
        ThingsWriter._open_url(url)

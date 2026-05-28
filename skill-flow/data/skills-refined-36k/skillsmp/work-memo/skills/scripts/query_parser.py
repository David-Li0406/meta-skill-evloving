"""
Natural language query parser for extracting filters from user queries.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


class QueryParser:
    """Parse natural language queries into structured filters"""

    def __init__(self, reference_date: Optional[datetime] = None):
        self.reference_date = reference_date or datetime.utcnow()

    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into filter dictionary.

        Returns:
            Dictionary with keys matching storage.search() interface:
            - title: str (keywords)
            - description: str (keywords)
            - type: str
            - status: str
            - urgency_min: int
            - urgency_max: int
            - importance_min: int
            - importance_max: int
            - tags: List[str]
            - projects: List[str]
            - contexts: List[str]
            - due_date_start: str (ISO 8601)
            - due_date_end: str (ISO 8601)
            - created_at_start: str (ISO 8601)
            - created_at_end: str (ISO 8601)
        """
        filters = {}
        query_lower = query.lower()

        filters['title'] = query_lower

        filters.update(self._extract_dates(query_lower))
        filters.update(self._extract_priorities(query_lower))
        filters.update(self._extract_tags(query_lower))
        filters.update(self._extract_status(query_lower))
        filters.update(self._extract_type(query_lower))

        if 'title' in filters and not filters['title'].strip():
            del filters['title']

        return filters

    def _extract_dates(self, query: str) -> Dict[str, Any]:
        """Extract date/time filters from query"""
        dates = {}
        start_date = None
        end_date = None

        date_patterns = {
            r'\btoday\b': (self._today, None),
            r'\btomorrow\b': (self._tomorrow, None),
            r'\byesterday\b': (self._yesterday, None),
            r'\bthis week\b': (self._this_week, self._this_week_end),
            r'\bnext week\b': (self._next_week, self._next_week_end),
            r'\bthis month\b': (self._this_month, self._this_month_end),
            r'\bnext month\b': (self._next_month, self._next_month_end),
            r'\bdue\s+(\d{4}-\d{2}-\d{2})\b': (self._exact_date, None),
        }

        for pattern, (start_func, end_func) in date_patterns.items():
            match = re.search(pattern, query)
            if match:
                if start_func:
                    start_date = start_func()
                if end_func:
                    end_date = end_func()
                query = re.sub(pattern, '', query)
                break

        due_match = re.search(r'\bdue\s+(\d{4}-\d{2}-\d{2})\b', query)
        if due_match:
            date_str = due_match.group(1)
            try:
                end_date = datetime.strptime(date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                dates['due_date_end'] = end_date.isoformat()
                start_date = None
            except:
                pass

        if start_date:
            dates['created_at_start'] = start_date.isoformat()
        if end_date and 'due_date_end' not in dates:
            dates['created_at_end'] = end_date.isoformat()

        return dates

    def _extract_priorities(self, query: str) -> Dict[str, Any]:
        """Extract urgency and importance filters"""
        priorities = {}

        urgency_keywords = {
            r'\bvery urgent\b': {'urgency_min': 5},
            r'\burgent\b': {'urgency_min': 4},
            r'\blow urgency\b': {'urgency_max': 2},
            r'\bnot urgent\b': {'urgency_max': 2},
        }

        importance_keywords = {
            r'\bvery important\b': {'importance_min': 5},
            r'\bimportant\b': {'importance_min': 4},
            r'\blow importance\b': {'importance_max': 2},
            r'\bnot important\b': {'importance_max': 2},
        }

        for pattern, filters in urgency_keywords.items():
            if re.search(pattern, query):
                priorities.update(filters)
                break

        for pattern, filters in importance_keywords.items():
            if re.search(pattern, query):
                priorities.update(filters)
                break

        return priorities

    def _extract_tags(self, query: str) -> Dict[str, Any]:
        """Extract tags, contexts, and projects"""
        tags = {}
        tag_list = []
        context_list = []
        project_list = []

        tag_pattern = r'#(\w+)'
        context_pattern = r'@(\w+)'
        project_pattern = r'project[：:](\w+)'

        for match in re.finditer(tag_pattern, query):
            tag_list.append(match.group(1))

        for match in re.finditer(context_pattern, query):
            context_list.append(match.group(1))

        for match in re.finditer(project_pattern, query):
            project_list.append(match.group(1))

        if tag_list:
            tags['tags'] = tag_list
        if context_list:
            tags['contexts'] = context_list
        if project_list:
            tags['projects'] = project_list

        return tags

    def _extract_status(self, query: str) -> Dict[str, Any]:
        """Extract status filters"""
        status_keywords = {
            r'\btodo\b': 'todo',
            r'\bin\s*progress\b': 'in_progress',
            r'\bblocked\b': 'blocked',
            r'\breview\b': 'review',
            r'\bdone\b': 'done',
            r'\bcompleted\b': 'done',
            r'\bcancelled\b': 'cancelled',
            r'\barchived\b': 'archived',
        }

        for pattern, status in status_keywords.items():
            if re.search(pattern, query):
                return {'status': status}

        return {}

    def _extract_type(self, query: str) -> Dict[str, Any]:
        """Extract type filters"""
        type_keywords = {
            r'\bmeeting\b': 'meeting',
            r'\bcall\b': 'call',
            r'\bemail\b': 'email',
            r'\breview\b': 'review',
            r'\bcoding\b': 'coding',
            r'\bcode\b': 'coding',
            r'\bdesign\b': 'design',
            r'\bwriting\b': 'writing',
            r'\bwrite\b': 'writing',
            r'\bresearch\b': 'research',
            r'\bplanning\b': 'planning',
            r'\bdocumentation\b': 'documentation',
            r'\bbugfix\b': 'bugfix',
            r'\bbug\s*fix\b': 'bugfix',
            r'\bfeature\b': 'feature',
            r'\btask\b': 'task',
        }

        for pattern, work_type in type_keywords.items():
            if re.search(pattern, query):
                return {'type': work_type}

        return {}

    def _today(self) -> datetime:
        """Get start of today"""
        return self.reference_date.replace(hour=0, minute=0, second=0, microsecond=0)

    def _tomorrow(self) -> datetime:
        """Get start of tomorrow"""
        return self._today() + timedelta(days=1)

    def _yesterday(self) -> datetime:
        """Get start of yesterday"""
        return self._today() - timedelta(days=1)

    def _this_week(self) -> datetime:
        """Get start of current week (Monday)"""
        today = self.reference_date
        days_since_monday = today.weekday()
        return (today - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)

    def _this_week_end(self) -> datetime:
        """Get end of current week (Sunday)"""
        return self._this_week() + timedelta(days=6, hours=23, minutes=59, seconds=59)

    def _next_week(self) -> datetime:
        """Get start of next week"""
        return self._this_week() + timedelta(weeks=1)

    def _next_week_end(self) -> datetime:
        """Get end of next week"""
        return self._next_week() + timedelta(days=6, hours=23, minutes=59, seconds=59)

    def _this_month(self) -> datetime:
        """Get start of current month"""
        return self.reference_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def _this_month_end(self) -> datetime:
        """Get end of current month"""
        if self.reference_date.month == 12:
            next_month = self.reference_date.replace(year=self.reference_date.year + 1, month=1, day=1)
        else:
            next_month = self.reference_date.replace(month=self.reference_date.month + 1, day=1)
        return next_month - timedelta(seconds=1)

    def _next_month(self) -> datetime:
        """Get start of next month"""
        return self._this_month_end()

    def _next_month_end(self) -> datetime:
        """Get end of next month"""
        this_month_end = self._this_month_end()
        next_month_start = this_month_end + timedelta(seconds=1)

        if next_month_start.month == 12:
            month_after_next = next_month_start.replace(year=next_month_start.year + 1, month=1, day=1)
        else:
            month_after_next = next_month_start.replace(month=next_month_start.month + 1, day=1)

        return month_after_next - timedelta(seconds=1)

    def _exact_date(self, date_str: str) -> datetime:
        """Parse exact date string"""
        return datetime.strptime(date_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)


if __name__ == "__main__":
    parser = QueryParser()

    test_queries = [
        "urgent tasks this week",
        "important tasks tagged @office",
        "show me all meetings today",
        "high priority tasks for project:Q1 due next month",
        "not urgent tasks that are in progress",
        "yesterday's work with #urgent #review",
        "bugfix tasks that are done",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        filters = parser.parse(query)
        print(f"Filters: {filters}")

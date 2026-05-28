"""
Core storage layer for Work Memo using TinyDB for local JSON persistence.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage

from schema import WorkRecord


class WorkMemoStorage:
    """TinyDB-based storage for work records"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.workmemo/db.json")

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db = TinyDB(self.db_path, storage=JSONStorage)
        self.records_table = self.db.table('records')

    def initialize(self):
        """Initialize database with default state"""
        if not self.db_path.exists():
            pass

    def create(self, record: WorkRecord) -> str:
        """Create new work record"""
        record.updated_at = datetime.utcnow().isoformat()
        record_dict = record.to_dict()
        doc_id = self.records_table.insert(record_dict)
        return record_dict['id']

    def get_by_id(self, record_id: str) -> Optional[WorkRecord]:
        """Get record by ID"""
        Record = Query()
        result = self.records_table.get(Record.id == record_id)
        return WorkRecord.from_dict(result) if result else None

    def get_all(self) -> List[WorkRecord]:
        """Get all records"""
        results = self.records_table.all()
        return [WorkRecord.from_dict(r) for r in results]

    def update(self, record: WorkRecord) -> bool:
        """Update existing record"""
        Record = Query()
        record.updated_at = datetime.utcnow().isoformat()
        record_dict = record.to_dict()
        self.records_table.update(record_dict, Record.id == record.id)
        return True

    def delete(self, record_id: str) -> bool:
        """Delete record by ID"""
        Record = Query()
        self.records_table.remove(Record.id == record_id)
        return True

    def search(self, filters: Dict[str, Any]) -> List[WorkRecord]:
        """
        Search records with flexible filters.

        Supported filter keys:
        - title: str (partial match)
        - description: str (partial match)
        - type: str (exact match)
        - status: str (exact match)
        - urgency_min: int (>=)
        - urgency_max: int (<=)
        - importance_min: int (>=)
        - importance_max: int (<=)
        - difficulty_min: int (>=)
        - difficulty_max: int (<=)
        - tags: List[str] (all must match)
        - projects: List[str] (any must match)
        - contexts: List[str] (any must match)
        - assignee_name: str (partial match)
        - due_date_start: str (ISO 8601, after)
        - due_date_end: str (ISO 8601, before)
        - created_at_start: str (ISO 8601, after)
        - created_at_end: str (ISO 8601, before)
        """
        Record = Query()
        results = self.records_table.all()

        if 'title' in filters:
            title = filters['title'].lower()
            results = [r for r in results if title in r['title'].lower()]

        if 'description' in filters:
            desc = filters['description'].lower()
            results = [r for r in results if r['description'] and desc in r['description'].lower()]

        if 'type' in filters:
            results = [r for r in results if r['type'] == filters['type']]

        if 'status' in filters:
            results = [r for r in results if r['status'] == filters['status']]

        if 'urgency_min' in filters:
            results = [r for r in results if r['urgency'] >= filters['urgency_min']]

        if 'urgency_max' in filters:
            results = [r for r in results if r['urgency'] <= filters['urgency_max']]

        if 'importance_min' in filters:
            results = [r for r in results if r['importance'] >= filters['importance_min']]

        if 'importance_max' in filters:
            results = [r for r in results if r['importance'] <= filters['importance_max']]

        if 'difficulty_min' in filters:
            results = [r for r in results if r['difficulty'] >= filters['difficulty_min']]

        if 'difficulty_max' in filters:
            results = [r for r in results if r['difficulty'] <= filters['difficulty_max']]

        if 'tags' in filters:
            tags = filters['tags']
            results = [r for r in results if all(tag in r['tags'] for tag in tags)]

        if 'projects' in filters:
            projects = filters['projects']
            results = [r for r in results if any(project in r['projects'] for project in projects)]

        if 'contexts' in filters:
            contexts = filters['contexts']
            results = [r for r in results if any(context in r['contexts'] for context in contexts)]

        if 'assignee_name' in filters:
            name = filters['assignee_name'].lower()
            results = [r for r in results if r['assignee'] and name in r['assignee']['name'].lower()]

        if 'due_date_start' in filters:
            try:
                start = datetime.fromisoformat(filters['due_date_start'])
                results = [r for r in results if r['due_date'] and datetime.fromisoformat(r['due_date']) >= start]
            except:
                pass

        if 'due_date_end' in filters:
            try:
                end = datetime.fromisoformat(filters['due_date_end'])
                results = [r for r in results if r['due_date'] and datetime.fromisoformat(r['due_date']) <= end]
            except:
                pass

        if 'created_at_start' in filters:
            try:
                start = datetime.fromisoformat(filters['created_at_start'])
                results = [r for r in results if datetime.fromisoformat(r['created_at']) >= start]
            except:
                pass

        if 'created_at_end' in filters:
            try:
                end = datetime.fromisoformat(filters['created_at_end'])
                results = [r for r in results if datetime.fromisoformat(r['created_at']) <= end]
            except:
                pass

        return [WorkRecord.from_dict(r) for r in results]

    def get_by_date_range(self, start_date: str, end_date: str) -> List[WorkRecord]:
        """Get records created within date range"""
        filters = {
            'created_at_start': start_date,
            'created_at_end': end_date
        }
        return self.search(filters)

    def get_overdue(self) -> List[WorkRecord]:
        """Get all overdue tasks"""
        all_records = self.get_all()
        return [r for r in all_records if r.is_overdue()]

    def get_due_soon(self, days: int = 7) -> List[WorkRecord]:
        """Get tasks due within specified days"""
        all_records = self.get_all()
        return [r for r in all_records if r.is_due_soon(days)]

    def get_by_quadrant(self, quadrant: str) -> List[WorkRecord]:
        """Get records by Eisenhower quadrant"""
        all_records = self.get_all()
        return [r for r in all_records if r.get_eisenhower_quadrant() == quadrant]

    def count_by_status(self) -> Dict[str, int]:
        """Count records by status"""
        all_records = self.get_all()
        counts = {}
        for record in all_records:
            status = record.status.value
            counts[status] = counts.get(status, 0) + 1
        return counts

    def count_by_type(self) -> Dict[str, int]:
        """Count records by type"""
        all_records = self.get_all()
        counts = {}
        for record in all_records:
            record_type = record.type.value
            counts[record_type] = counts.get(record_type, 0) + 1
        return counts

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        all_records = self.get_all()
        total = len(all_records)

        if total == 0:
            return {
                'total': 0,
                'by_status': {},
                'by_type': {},
                'overdue': 0,
                'due_soon': 0
            }

        status_counts = self.count_by_status()
        type_counts = self.count_by_type()
        overdue = len(self.get_overdue())
        due_soon = len(self.get_due_soon())

        return {
            'total': total,
            'by_status': status_counts,
            'by_type': type_counts,
            'overdue': overdue,
            'due_soon': due_soon
        }

    def close(self):
        """Close database connection"""
        self.db.close()


if __name__ == "__main__":
    storage = WorkMemoStorage()
    storage.initialize()

    print("Database initialized at:", storage.db_path)
    print("Total records:", storage.count_by_status())

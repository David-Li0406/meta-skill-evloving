#!/usr/bin/env python3
"""
History Tracker Module

Tracks historical changes to trademark data for audit and comparison.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class ChangeType(Enum):
    """Types of changes"""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    REPROCESSED = "reprocessed"


class HistoryTracker:
    """
    Tracks historical changes to trademark certificate data
    """

    def __init__(self, history_dir: Optional[Path] = None):
        """
        Initialize history tracker

        Args:
            history_dir: Directory to store history files
        """
        self.history_dir = history_dir or Path.cwd() / ".trademark_history"
        self.history_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.history_dir / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """Load history index"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'trademarks': {}, 'sessions': []}

    def _save_index(self):
        """Save history index"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def _get_trademark_id(self, data: Dict[str, Any]) -> str:
        """
        Generate unique ID for trademark based on registration number

        Args:
            data: Trademark data

        Returns:
            Unique trademark ID
        """
        reg_number = data.get('注册号', '')
        registrant = data.get('注册人', '')

        # Use registration number as primary ID
        if reg_number:
            return f"TM_{reg_number}"

        # Fallback to hash if no registration number
        identifier = f"{registrant}_{data.get('国际分类', '')}"
        hash_id = hashlib.md5(identifier.encode()).hexdigest()[:8]
        return f"TM_{hash_id}"

    def _calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash of trademark data for change detection"""
        # Only hash core fields (ignore metadata)
        core_fields = ['注册号', '注册人', '国际分类', '有效期限']
        core_data = {k: data.get(k, '') for k in core_fields}

        data_str = json.dumps(core_data, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(data_str.encode()).hexdigest()

    def track(self, data: Dict[str, Any],
              change_type: ChangeType = ChangeType.CREATED,
              notes: Optional[str] = None) -> str:
        """
        Track a trademark record

        Args:
            data: Trademark data
            change_type: Type of change
            notes: Optional notes about the change

        Returns:
            Trademark ID
        """
        tm_id = self._get_trademark_id(data)
        data_hash = self._calculate_data_hash(data)
        timestamp = datetime.now().isoformat()

        # Create history entry
        history_entry = {
            'timestamp': timestamp,
            'change_type': change_type.value,
            'data': data.copy(),
            'data_hash': data_hash,
            'notes': notes,
        }

        # Initialize trademark history if needed
        if tm_id not in self.index['trademarks']:
            self.index['trademarks'][tm_id] = {
                'id': tm_id,
                'registration_number': data.get('注册号', ''),
                'registrant': data.get('注册人', ''),
                'created_at': timestamp,
                'updated_at': timestamp,
                'history': [],
            }

        # Check if data has changed
        tm_info = self.index['trademarks'][tm_id]

        if tm_info['history']:
            last_hash = tm_info['history'][-1]['data_hash']
            if last_hash == data_hash and change_type != ChangeType.REPROCESSED:
                # No change detected, skip
                return tm_id

        # Add to history
        tm_info['history'].append(history_entry)
        tm_info['updated_at'] = timestamp

        # Save to individual history file
        history_file = self.history_dir / f"{tm_id}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(tm_info, f, ensure_ascii=False, indent=2)

        # Update index
        self._save_index()

        return tm_id

    def track_batch(self, data_list: List[Dict[str, Any]],
                    session_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Track a batch of trademark records

        Args:
            data_list: List of trademark data
            session_name: Optional name for this processing session

        Returns:
            Session summary
        """
        timestamp = datetime.now().isoformat()
        session_id = hashlib.md5(timestamp.encode()).hexdigest()[:8]

        session_info = {
            'session_id': session_id,
            'session_name': session_name or f"Batch_{session_id}",
            'timestamp': timestamp,
            'total_items': len(data_list),
            'created': 0,
            'updated': 0,
            'unchanged': 0,
            'trademark_ids': [],
        }

        for data in data_list:
            tm_id = self._get_trademark_id(data)

            # Determine change type
            if tm_id in self.index['trademarks']:
                change_type = ChangeType.UPDATED
                session_info['updated'] += 1
            else:
                change_type = ChangeType.CREATED
                session_info['created'] += 1

            self.track(data, change_type, notes=f"Session: {session_info['session_name']}")
            session_info['trademark_ids'].append(tm_id)

        # Record session
        self.index['sessions'].append(session_info)
        self._save_index()

        return session_info

    def get_trademark_history(self, trademark_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full history for a trademark

        Args:
            trademark_id: Trademark ID

        Returns:
            Trademark history or None if not found
        """
        history_file = self.history_dir / f"{trademark_id}.json"

        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    def get_changes(self, trademark_id: str,
                   since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get changes for a trademark since a specific time

        Args:
            trademark_id: Trademark ID
            since: Only return changes after this datetime

        Returns:
            List of changes
        """
        history = self.get_trademark_history(trademark_id)

        if not history:
            return []

        changes = history.get('history', [])

        if since:
            since_str = since.isoformat()
            changes = [c for c in changes if c['timestamp'] > since_str]

        return changes

    def compare_versions(self, trademark_id: str,
                        version1_idx: int = -2,
                        version2_idx: int = -1) -> Dict[str, Any]:
        """
        Compare two versions of a trademark

        Args:
            trademark_id: Trademark ID
            version1_idx: Index of first version (default: second to last)
            version2_idx: Index of second version (default: last)

        Returns:
            Dictionary with comparison results
        """
        history = self.get_trademark_history(trademark_id)

        if not history or len(history['history']) < 2:
            return {'error': 'Insufficient history for comparison'}

        v1 = history['history'][version1_idx]
        v2 = history['history'][version2_idx]

        differences = {}
        all_keys = set(v1['data'].keys()) | set(v2['data'].keys())

        for key in all_keys:
            val1 = v1['data'].get(key)
            val2 = v2['data'].get(key)

            if val1 != val2:
                differences[key] = {
                    'old': val1,
                    'new': val2,
                }

        return {
            'trademark_id': trademark_id,
            'version1': {
                'timestamp': v1['timestamp'],
                'change_type': v1['change_type'],
            },
            'version2': {
                'timestamp': v2['timestamp'],
                'change_type': v2['change_type'],
            },
            'differences': differences,
            'has_changes': len(differences) > 0,
        }

    def get_all_trademarks(self) -> List[str]:
        """Get list of all tracked trademark IDs"""
        return list(self.index['trademarks'].keys())

    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get list of all processing sessions"""
        return self.index['sessions']

    def generate_history_report(self, trademark_id: str) -> str:
        """
        Generate a history report for a trademark

        Args:
            trademark_id: Trademark ID

        Returns:
            Formatted report string
        """
        history = self.get_trademark_history(trademark_id)

        if not history:
            return f"No history found for {trademark_id}"

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(f"TRADEMARK HISTORY REPORT: {trademark_id}")
        report_lines.append("=" * 80)
        report_lines.append(f"Registration Number: {history['registration_number']}")
        report_lines.append(f"Registrant: {history['registrant']}")
        report_lines.append(f"First Tracked: {history['created_at']}")
        report_lines.append(f"Last Updated: {history['updated_at']}")
        report_lines.append(f"Total Changes: {len(history['history'])}")
        report_lines.append("")

        report_lines.append("CHANGE HISTORY:")
        report_lines.append("-" * 80)

        for i, entry in enumerate(history['history'], 1):
            timestamp = datetime.fromisoformat(entry['timestamp'])
            report_lines.append(f"{i}. {entry['change_type'].upper()} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

            if entry.get('notes'):
                report_lines.append(f"   Notes: {entry['notes']}")

            # Show key data fields
            data = entry['data']
            report_lines.append(f"   注册号: {data.get('注册号', 'N/A')}")
            report_lines.append(f"   注册人: {data.get('注册人', 'N/A')}")
            report_lines.append(f"   有效期限: {data.get('有效期限', 'N/A')}")

            if entry.get('overall_confidence'):
                report_lines.append(f"   置信度: {entry['overall_confidence']:.1%}")

            report_lines.append("")

        report_lines.append("=" * 80)

        return "\n".join(report_lines)

    def export_history(self, output_path: Path):
        """
        Export complete history to a file

        Args:
            output_path: Path for output file
        """
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'total_trademarks': len(self.index['trademarks']),
            'total_sessions': len(self.index['sessions']),
            'trademarks': {},
        }

        # Load all trademark histories
        for tm_id in self.index['trademarks'].keys():
            history = self.get_trademark_history(tm_id)
            if history:
                export_data['trademarks'][tm_id] = history

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Test history tracker
    tracker = HistoryTracker(history_dir=Path("/tmp/trademark_history_test"))

    # Test data
    test_data1 = {
        '注册号': '12345678',
        '注册人': '阿里巴巴集团控股有限公司',
        '国际分类': '35',
        '有效期限': '2025-12-31',
    }

    test_data2 = test_data1.copy()
    test_data2['有效期限'] = '2026-12-31'  # Changed

    # Track initial version
    tm_id = tracker.track(test_data1, ChangeType.CREATED)
    print(f"Created: {tm_id}")

    # Track updated version
    tracker.track(test_data2, ChangeType.UPDATED)
    print(f"Updated: {tm_id}")

    # Generate report
    print("\n" + tracker.generate_history_report(tm_id))

    # Compare versions
    comparison = tracker.compare_versions(tm_id)
    print("\nComparison:")
    print(json.dumps(comparison, ensure_ascii=False, indent=2))

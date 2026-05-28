"""
Work Record Data Schema for Work Memo Skill

This module defines complete data model for work records including:
- Person: Who is involved
- Task/Event: What happened or what needs to be done
- Type: Category of work
- Time: Timestamps and due dates
- Location: Where it happened
- Urgency: 1-5 scale (1=least urgent, 5=most urgent)
- Importance: 1-5 scale (1=least important, 5=most important)
- Difficulty: 1-10 scale (1=easiest, 10=hardest)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import json
from uuid import uuid4


class WorkType(str, Enum):
    """Categories of work types"""
    TASK = "task"
    MEETING = "meeting"
    CALL = "call"
    EMAIL = "email"
    REVIEW = "review"
    CODING = "coding"
    DESIGN = "design"
    WRITING = "writing"
    RESEARCH = "research"
    PLANNING = "planning"
    DOCUMENTATION = "documentation"
    BUGFIX = "bugfix"
    FEATURE = "feature"
    OTHER = "other"


class Status(str, Enum):
    """Work status states"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class Priority(str, Enum):
    """Priority levels (mapping to numeric values for scoring)"""
    LOW = "low"
    MEDIUM_LOW = "medium_low"
    MEDIUM = "medium"
    MEDIUM_HIGH = "medium_high"
    HIGH = "high"


@dataclass
class Person:
    """Person involved in work"""
    name: str
    role: Optional[str] = None
    contact: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "contact": self.contact
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Person':
        return cls(
            name=data["name"],
            role=data.get("role"),
            contact=data.get("contact")
        )


@dataclass
class Location:
    """Location information"""
    place: str
    address: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "place": self.place,
            "address": self.address,
            "coordinates": self.coordinates
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        return cls(
            place=data["place"],
            address=data.get("address"),
            coordinates=data.get("coordinates")
        )


@dataclass
class WorkRecord:
    """Complete work record with all required dimensions"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: Optional[str] = None
    type: WorkType = WorkType.TASK
    status: Status = Status.TODO
    urgency: int = 3
    importance: int = 3
    difficulty: int = 10
    assignee: Optional[Person] = None
    reporter: Optional[Person] = None
    participants: List[Person] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    location: Optional[Location] = None
    estimated_effort: Optional[int] = None
    time_spent: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type.value,
            "status": self.status.value,
            "urgency": self.urgency,
            "importance": self.importance,
            "difficulty": self.difficulty,
            "assignee": self.assignee.to_dict() if self.assignee else None,
            "reporter": self.reporter.to_dict() if self.reporter else None,
            "participants": [p.to_dict() for p in self.participants],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "location": self.location.to_dict() if self.location else None,
            "estimated_effort": self.estimated_effort,
            "time_spent": self.time_spent,
            "tags": self.tags,
            "projects": self.projects,
            "contexts": self.contexts,
            "depends_on": self.depends_on,
            "blocks": self.blocks,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkRecord':
        """Create from dictionary loaded from storage"""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            type=WorkType(data["type"]),
            status=Status(data["status"]),
            urgency=data["urgency"],
            importance=data["importance"],
            difficulty=data["difficulty"],
            assignee=Person.from_dict(data["assignee"]) if data.get("assignee") else None,
            reporter=Person.from_dict(data["reporter"]) if data.get("reporter") else None,
            participants=[Person.from_dict(p) for p in data.get("participants", [])],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            start_date=data.get("start_date"),
            due_date=data.get("due_date"),
            completed_at=data.get("completed_at"),
            location=Location.from_dict(data["location"]) if data.get("location") else None,
            estimated_effort=data.get("estimated_effort"),
            time_spent=data.get("time_spent"),
            tags=data.get("tags", []),
            projects=data.get("projects", []),
            contexts=data.get("contexts", []),
            depends_on=data.get("depends_on", []),
            blocks=data.get("blocks", []),
            metadata=data.get("metadata", {})
        )

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'WorkRecord':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))

    def get_eisenhower_quadrant(self) -> str:
        """
        Calculate Eisenhower Matrix quadrant:
        Q1 (Do Now): Urgent & Important
        Q2 (Schedule): Not Urgent & Important
        Q3 (Delegate): Urgent & Not Important
        Q4 (Eliminate): Not Urgent & Not Important
        """
        is_urgent = self.urgency >= 4
        is_important = self.importance >= 4

        if is_urgent and is_important:
            return "Q1"  # Do Now
        elif not is_urgent and is_important:
            return "Q2"  # Schedule
        elif is_urgent and not is_important:
            return "Q3"  # Delegate
        else:
            return "Q4"  # Eliminate

    def get_priority_score(self, weights: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate priority score using weighted factors
        Default weights: urgency=0.35, importance=0.30, effort=0.20, dependency=0.15
        """
        if weights is None:
            weights = {
                "urgency": 0.35,
                "importance": 0.30,
                "effort": 0.20,
                "dependency": 0.15
            }

        # Normalize values to 0-1 range
        urgency_score = self.urgency / 5.0
        importance_score = self.importance / 5.0

        # Inverse difficulty (easier tasks get higher score for quick wins)
        difficulty_score = (11 - self.difficulty) / 10.0

        # Dependency bonus (tasks that block others get higher priority)
        dependency_score = min(len(self.blocks) * 0.2, 1.0)

        # Calculate weighted score
        score = (
            weights["urgency"] * urgency_score +
            weights["importance"] * importance_score +
            weights["effort"] * difficulty_score +
            weights["dependency"] * dependency_score
        )

        return score

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.status == Status.DONE:
            return False
        try:
            due = datetime.fromisoformat(self.due_date)
            return due < datetime.utcnow()
        except:
            return False

    def is_due_soon(self, days: int = 7) -> bool:
        """Check if task is due within specified days"""
        if not self.due_date or self.status == Status.DONE:
            return False
        try:
            due = datetime.fromisoformat(self.due_date)
            delta = due - datetime.utcnow()
            return 0 <= delta.total_seconds() <= (days * 24 * 3600)
        except:
            return False


if __name__ == "__main__":
    record = WorkRecord(
        title="Review project proposal",
        description="Review and provide feedback on Q1 project proposal",
        type=WorkType.REVIEW,
        status=Status.TODO,
        urgency=5,
        importance=4,
        difficulty=6,
        assignee=Person(name="John Doe", role="manager"),
        participants=[
            Person(name="Jane Smith", role="colleague"),
            Person(name="Mike Johnson", role="client")
        ],
        due_date="2026-01-25T17:00:00Z",
        location=Location(place="Conference Room A", address="Building 1, Floor 3"),
        estimated_effort=60,
        tags=["urgent", "review", "project"],
        projects=["Q1-Planning"],
        contexts=["@office"]
    )

    print("Work Record:")
    print(record.to_json())

    print(f"\nEisenhower Quadrant: {record.get_eisenhower_quadrant()}")
    print(f"Priority Score: {record.get_priority_score():.2f}")
    print(f"Is Overdue: {record.is_overdue()}")
    print(f"Is Due Soon: {record.is_due_soon()}")

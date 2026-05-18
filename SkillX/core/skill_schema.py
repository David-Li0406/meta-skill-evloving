"""Unified skill schema for all benchmarks.

Provides a standardized skill format that can be used across:
- AppWorld (functional skills)
- BFCL (functional skills)
- tau2-bench (atomic/tool-centric skills)
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
import json


@dataclass
class UnifiedSkill:
    """
    Unified skill representation.

    Attributes:
        name: Skill name (e.g., "spotify get all user playlists")
        document: Description with Parameters/Outputs/Notes
        content: Implementation code or usage examples
        tools: List of tools/APIs used by this skill
    """
    name: str
    document: str
    content: str
    tools: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_embedding_text(self) -> str:
        """Generate text for embedding."""
        return f"{self.name}\n{self.document}\n{self.content}"

    @classmethod
    def from_dict(cls, data: Dict) -> "UnifiedSkill":
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            document=data.get("document", ""),
            content=data.get("content", ""),
            tools=data.get("tools", []),
        )


@dataclass
class SkillExtractionResult:
    """
    Result of skill extraction with metadata.

    Attributes:
        option: "add", "modify", or "keep"
        skill: The extracted skill
        filter_result: Whether the skill passed filtering
        embedding_text: Text for embedding (auto-generated)
        modified_from: Original skill name if modified
        source_tool: Tool name for atomic skills
        skill_type: "functional" or "atomic"
    """
    option: str
    skill: UnifiedSkill
    filter_result: bool = True
    embedding_text: str = ""
    modified_from: Optional[str] = None
    source_tool: Optional[str] = None
    skill_type: str = "functional"

    def __post_init__(self):
        if not self.embedding_text:
            self.embedding_text = self.skill.to_embedding_text()

    def to_dict(self) -> Dict:
        """Convert to dictionary format expected by target skills."""
        result = {
            "option": self.option,
            "skill": self.skill.to_dict(),
            "filter_result": self.filter_result,
            "embedding_text": self.embedding_text,
        }
        if self.modified_from:
            result["modified_from"] = self.modified_from
        if self.source_tool:
            result["source_tool"] = self.source_tool
        if self.skill_type:
            result["skill_type"] = self.skill_type
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "SkillExtractionResult":
        """Create from dictionary."""
        skill_data = data.get("skill", {})
        if isinstance(skill_data, dict):
            skill = UnifiedSkill.from_dict(skill_data)
        else:
            skill = UnifiedSkill(name="", document="", content="", tools=[])

        return cls(
            option=data.get("option", "add"),
            skill=skill,
            filter_result=data.get("filter_result", True),
            embedding_text=data.get("embedding_text", ""),
            modified_from=data.get("modified_from"),
            source_tool=data.get("source_tool"),
            skill_type=data.get("skill_type", "functional"),
        )


def normalize_skill_output(raw_skills: List[Dict]) -> List[SkillExtractionResult]:
    """
    Convert extractor output to unified SkillExtractionResult format.

    Args:
        raw_skills: List of raw skill dictionaries from extractors

    Returns:
        List of SkillExtractionResult objects
    """
    results = []
    for raw in raw_skills:
        try:
            result = SkillExtractionResult.from_dict(raw)
            # Ensure embedding_text is set
            if not result.embedding_text:
                result.embedding_text = result.skill.to_embedding_text()
            # Clean content - remove return statements
            if "return" in result.skill.content:
                result.skill.content = result.skill.content.split("return")[0].strip()
            results.append(result)
        except Exception as e:
            continue
    return results


def collect_skills_from_plan_metadata(
    plan_step_metadata: Dict[str, List[Dict]],
    skill_type: str = "functional"
) -> List[SkillExtractionResult]:
    """
    Collect skills from plan_step_metadata format.

    Args:
        plan_step_metadata: Dict mapping step/tool to list of skill dicts
        skill_type: Type of skills ("functional" or "atomic")

    Returns:
        List of SkillExtractionResult objects
    """
    results = []
    seen_names = set()

    for key, skill_items in plan_step_metadata.items():
        for item in skill_items:
            try:
                if item.get("option") == "add":
                    skill = SkillExtractionResult.from_dict(item)
                    skill.skill_type = skill_type
                    if skill_type == "atomic":
                        skill.source_tool = key
                    if skill.skill.name not in seen_names:
                        results.append(skill)
                        seen_names.add(skill.skill.name)

                elif item.get("option") == "modify":
                    # Remove original and add modified
                    modified_from = item.get("modified_from", "")
                    results = [
                        r for r in results
                        if r.skill.name != modified_from
                    ]
                    skill = SkillExtractionResult.from_dict(item)
                    skill.skill_type = skill_type
                    if skill_type == "atomic":
                        skill.source_tool = key
                    results.append(skill)
                    seen_names.discard(modified_from)
                    seen_names.add(skill.skill.name)

            except Exception:
                continue

    return results


def skills_to_json(skills: List[SkillExtractionResult]) -> str:
    """Convert skills to JSON string."""
    return json.dumps(
        [s.to_dict() for s in skills],
        ensure_ascii=False,
        indent=2
    )


def save_skills(
    skills: List[SkillExtractionResult],
    filepath: str
) -> None:
    """Save skills to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            [s.to_dict() for s in skills],
            f,
            ensure_ascii=False,
            indent=2
        )


def load_skills(filepath: str) -> List[SkillExtractionResult]:
    """Load skills from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [SkillExtractionResult.from_dict(item) for item in data]

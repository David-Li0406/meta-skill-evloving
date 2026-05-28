#!/usr/bin/env python3
"""LearningEngagementSkill"""
import sys
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from skill_base import Skill, SkillParameter, register_skill

class LearningEngagementSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="learning.engagement", skill_name="learning-engagement", category="learning",
                        description="learning.engagement skill for learning experience design")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="topic", param_type=str, required=True),
            SkillParameter(name="educational_level", param_type=str, required=True),
            SkillParameter(name="options", param_type=dict, required=False, default={})
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = parameters["topic"]
        level = parameters["educational_level"]
        options = parameters.get("options", {})
        result = {
            "skill": "learning.engagement",
            "topic": topic,
            "level": level,
            "deliverable": f"{topic} learning experience created",
            "status": "success"
        }
        return {"data": result, "artifacts": [f"{topic.replace(' ', '_')}_{skill_dir}.json"]}

skill_instance = LearningEngagementSkill()
register_skill(skill_instance)

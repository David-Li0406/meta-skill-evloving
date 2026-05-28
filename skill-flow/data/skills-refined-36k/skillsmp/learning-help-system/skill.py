#!/usr/bin/env python3
"""LearningHelpSystemSkill"""
import sys
from pathlib import Path
from typing import Dict, List, Any
framework_path = Path(__file__).parent.parent / "framework"
sys.path.insert(0, str(framework_path))
from skill_base import Skill, SkillParameter, register_skill

class LearningHelpSystemSkill(Skill):
    def __init__(self):
        super().__init__(skill_id="learning.help.system", skill_name="learning-help-system", category="learning",
                        description="learning.help.system for learning support and infrastructure")

    def get_parameters(self) -> List[SkillParameter]:
        return [
            SkillParameter(name="content", param_type=str, required=True),
            SkillParameter(name="target_audience", param_type=str, required=False, default="general")
        ]

    async def execute(self, parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        content = parameters["content"]
        audience = parameters.get("target_audience", "general")
        result = {
            "skill": "learning.help.system",
            "output": f"Generated {skill_dir} for {audience}",
            "content_processed": content[:50],
            "status": "success"
        }
        return {"data": result, "artifacts": [f"{skill_dir}_output.json"]}

skill_instance = LearningHelpSystemSkill()
register_skill(skill_instance)

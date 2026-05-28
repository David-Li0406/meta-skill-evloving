"""
Application constants (non-configurable static data).

Contains:
- SKILL_GROUPS: Available skill group configurations
- SKILL_GROUP_ALIASES: Backward compatibility aliases
- DEMO_TASKS: Demo task configurations for the Web UI
"""
from enum import Enum
from typing import Callable

from config import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"

# ===== Skill Groups Configuration =====
# Alias mapping for backward compatibility (e.g., "default" -> "skill_seeds")
SKILL_GROUP_ALIASES = {"default": "skill_seeds"}

SKILL_GROUPS = [
    {
        "id": "skill_seeds",
        "name": "Curated (RECOMMENDED)",
        "description": "Carefully curated demo pool (~50 skills)",
        "skills_dir": str(DATA_DIR / "skill_seeds"),
        "tree_path": str(DATA_DIR / "capability_trees" / "tree.yaml"),
        "vector_db_path": str(DATA_DIR / "vector_stores" / "skill_seeds"),
        "is_default": True,
    },
    {
        "id": "skill_200",
        "name": "Skill 200",
        "description": "200 skills",
        "skills_dir": str(DATA_DIR / "skill_200"),
        "tree_path": str(DATA_DIR / "capability_trees" / "tree_200.yaml"),
        "vector_db_path": str(DATA_DIR / "vector_stores" / "skill_200"),
    },
    {
        "id": "skill_1000",
        "name": "Skill 1000",
        "description": "1,000 skills",
        "skills_dir": str(DATA_DIR / "skill_1000"),
        "tree_path": str(DATA_DIR / "capability_trees" / "tree_skill_1000.yaml"),
        "vector_db_path": str(DATA_DIR / "vector_stores" / "skill_1000"),
    },
    {
        "id": "skill_10000",
        "name": "Skill 10000",
        "description": "10,000 active + 190,000 dormant skills",
        "skills_dir": str(DATA_DIR / "skill_10000"),
        "tree_path": str(DATA_DIR / "capability_trees" / "tree_skill_10000.yaml"),
        "vector_db_path": str(DATA_DIR / "vector_stores" / "skill_10000"),
    },
]


def resolve_skill_group(group_id: str) -> dict:
    """Resolve a skill group ID (with alias support) to its config dict.

    Returns the group dict from SKILL_GROUPS, falling back to the first
    group if not found.
    """
    resolved = SKILL_GROUP_ALIASES.get(group_id, group_id)
    for g in SKILL_GROUPS:
        if g["id"] == resolved:
            return g
    return SKILL_GROUPS[0]


# Progress callback: (event_type: str, data: dict) -> None
EventCallback = Callable[[str, dict], None]

# Default tools for baseline (no-skill) execution mode
DEFAULT_BASELINE_TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]

# ===== Enums =====
class TaskStatus(str, Enum):
    """Unified status for workflow tasks and orchestrator nodes."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ===== Demo Tasks Configuration =====
DEMO_TASKS = [
    {
        "id": "frontend_debug",
        "title": "Frontend Debug Report",
        "description": "Fix login page bug and generate report",
        "prompt": "I am a front-end developer. Users have reported that a bug occurs when accessing the login page I wrote on a mobile phone. The code for my login page is login.html. Please help me identify and fix the bug, and write a bug fix report. The report should include a screenshot of the problematic web page before the bug fix and a screenshot of the normal web page after the bug fix. In the screenshots, the location of the bug should be highlighted with clear and eye-catching markers. The report should be saved as bug_report.md.",
        "files": ["artifacts/login.html"],
        "icon": "bug",
    },
    {
        "id": "ui_research",
        "title": "Fusion UI Design",
        "description": "Visual design research for knowledge management product",
        "prompt": "I am a product designer, and our company is planning to build a knowledge management software product. Therefore, I need you to research multiple related products, such as Notion and Confluence, and produce a visual design style research report about them. The visual style research report should be saved as report.docx and must include screenshots of these software products. Then, based on the analysis, synthesize the design characteristics of these products and generate three design concept images for a knowledge management software to provide design inspiration. The design concept images should be saved as fusion_design_1.png, fusion_design_2.png, and fusion_design_3.png, respectively.",
        "files": [],
        "icon": "design",
    },
    {
        "id": "paper_promotion",
        "title": "Paper Promotion Assistant",
        "description": "Multi-platform promotion plan for research paper",
        "prompt": "As a PhD student, I have recently completed a research paper and would like to effectively promote it on both domestic and international social media platforms. In addition, I need help creating online materials that can serve as a central hub for clearly presenting and disseminating my research findings to a broader audience. My paper is located locally at Avengers.pdf.",
        "files": ["artifacts/Avengers.pdf"],
        "icon": "paper",
    },
    {
        "id": "cat_meme_video",
        "title": "Cat Meme Video Generation",
        "description": "Generate cat meme video of boss questioning employee",
        "prompt": "I am a short-video content creator, and I need you to generate a funny cat meme video. The theme of the video is a boss questioning an employee about work progress, and the employee gives a clever response. The questioning cat represents the boss, and the aggrieved cat represents the employee.\nVideo materials: The video materials for the questioning cat and the aggrieved cat are in video.mp4. The background image for the video is background.jpg.\nVideo quality requirements: Completely remove the green screen background from both the questioning cat and the aggrieved cat video materials, and replace it with background.jpg. Keep the background image's aspect ratio without distortion. The cats should occupy the main focus of the frame, and the integrity of the cat footage should be preserved as much as possible.\nFormat requirements: The generated video must have the same duration as the original video material. All text must be in Chinese, so please pay attention to potential text encoding issues.\nText requirements: Identity labels reading \"Boss\" and \"Employee\" should appear next to the questioning cat and the aggrieved cat respectively. The timing and duration of the dialogue subtitles must be accurate. Continuous meowing by a single cat should be treated as one sentence. The dialogue between the two cats should be humorous, and the employee's responses to the boss should be witty and have strong potential for widespread sharing on the internet. The length of the dialogue text should be determined based on the duration of each line spoken by the two cats.",
        "files": ["artifacts/video.mp4", "artifacts/bg.jpg"],
        "icon": "video",
    },
]

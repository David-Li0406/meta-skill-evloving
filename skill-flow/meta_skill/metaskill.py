"""Meta-skill: an agent-editable SKILL.md describing a library-management method.

Format: YAML frontmatter (engine + nested params that map onto RefinerConfig) +
a markdown playbook + fenced prompt blocks:

    <!-- PROMPT: merge -->
    ...jinja prompt text...
    <!-- END PROMPT: merge -->

The loader turns a meta-skill into a ``RefinerConfig`` plus the prompt overrides,
writing the prompt blocks to temp ``.j2`` files so the existing engines use them.
The whole SKILL.md is the evolvable artifact the refiner agent rewrites.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from skill_flow.refiner.models import RefinerConfig

_FRONTMATTER = re.compile(r"^---\s*\n(?P<fm>.*?)\n---\s*\n(?P<body>.*)$", re.DOTALL)
_PROMPT_BLOCK = re.compile(
    r"<!--\s*PROMPT:\s*(?P<name>[\w-]+)\s*-->\n(?P<text>.*?)\n<!--\s*END PROMPT:\s*(?P=name)\s*-->",
    re.DOTALL,
)
# which RefinerConfig instruction_path field each named prompt overrides
_PROMPT_TARGETS = {
    "merge": ("merger", "instruction_path"),
    "filter": ("quality_filter", "instruction_path"),
    "autoskill_judge": ("autoskill", "instruction_path"),
    "skillclaw_evolve": ("skillclaw", "evolve_instruction_path"),
    "skillclaw_verify": ("skillclaw", "verify_instruction_path"),
    "agentskillos_label": ("agentskillos", "label_instruction_path"),
}


class MetaSkill(BaseModel):
    name: str
    description: str = ""
    engine: str = "skillx"
    params: dict = Field(default_factory=dict)
    playbook: str = ""  # the prose strategy section
    prompts: dict[str, str] = Field(default_factory=dict)
    raw: str = ""  # the full original SKILL.md text (for the refiner to edit)

    def to_refiner_config(self, tmp_dir: Path | None = None, **overrides) -> RefinerConfig:
        """Build a RefinerConfig: frontmatter params + prompt-file overrides."""
        data: dict = {"engine": self.engine, **self.params, **overrides}
        # write each prompt block to a temp .j2 and point the engine at it
        tdir = Path(tmp_dir or tempfile.mkdtemp(prefix="metaskill-prompts-"))
        tdir.mkdir(parents=True, exist_ok=True)
        for pname, text in self.prompts.items():
            target = _PROMPT_TARGETS.get(pname)
            if not target:
                continue
            section, field = target
            path = tdir / f"{pname}.j2"
            path.write_text(text, encoding="utf-8")
            data.setdefault(section, {})
            if isinstance(data[section], dict):
                data[section][field] = str(path)
        return RefinerConfig.model_validate(data)


def parse_meta_skill(text: str) -> MetaSkill:
    m = _FRONTMATTER.match(text)
    if not m:
        raise ValueError("meta-skill SKILL.md missing YAML frontmatter")
    fm = yaml.safe_load(m.group("fm")) or {}
    body = m.group("body")
    prompts = {pm.group("name"): pm.group("text").strip()
               for pm in _PROMPT_BLOCK.finditer(body)}
    playbook = _PROMPT_BLOCK.sub("", body).strip()
    return MetaSkill(
        name=fm.get("name", "meta-skill"),
        description=fm.get("description", ""),
        engine=fm.get("engine", "skillx"),
        params=fm.get("params", {}) or {},
        playbook=playbook,
        prompts=prompts,
        raw=text,
    )


def load_meta_skill(path: str | Path) -> MetaSkill:
    return parse_meta_skill(Path(path).read_text(encoding="utf-8"))

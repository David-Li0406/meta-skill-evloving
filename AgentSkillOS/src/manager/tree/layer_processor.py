"""
Layer Post-Processor - Separates capability tree into active and dormant layers.

This module post-processes an existing tree.yaml (built by TreeBuilder) and
generates:
1. active_tree.yaml - Tree containing only active (Top N + pinned) skills
2. dormant_index.yaml - Index of dormant skills for search

The original tree.yaml is NOT modified - this is an additive post-processing step.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console

from config import PROJECT_ROOT, get_config, LayeringConfig
from cache import ensure_cache
from .models import TreeNode, SkillStatus
from .user_prefs import load_user_prefs, UserPreferences


console = Console()


@dataclass
class DormantSkillEntry:
    """Entry in the dormant skills index."""
    id: str
    name: str
    description: str
    skill_path: str
    installs_count: int
    status: str = "dormant"
    github_url: str = ""
    stars: int = 0
    is_official: bool = False
    author: str = ""
    # Original tree path for reinsertion
    tree_path: str = ""


@dataclass
class DormantIndex:
    """Index of dormant skills for search."""
    version: int = 1
    created_at: str = ""
    skills_count: int = 0
    skills: list[DormantSkillEntry] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "version": self.version,
            "created_at": self.created_at,
            "skills_count": self.skills_count,
            "skills": [asdict(s) for s in self.skills],
        }


@dataclass
class LayeredOutput:
    """Output from layer post-processing."""
    active_tree: dict
    dormant_index: DormantIndex
    stats: dict = field(default_factory=dict)

    def save(
        self,
        active_tree_path: Path,
        dormant_index_path: Path,
    ) -> None:
        """Save layered output to files."""
        # Ensure directories exist
        active_tree_path.parent.mkdir(parents=True, exist_ok=True)
        dormant_index_path.parent.mkdir(parents=True, exist_ok=True)

        # Save active tree (atomic write)
        atomic_yaml_write(active_tree_path, self.active_tree)

        # Save dormant index (atomic write)
        atomic_yaml_write(dormant_index_path, self.dormant_index.to_dict())


class LayerPostProcessor:
    """
    Post-processor for capability tree layering.

    Workflow:
    1. Load original tree.yaml (already built by TreeBuilder)
    2. Load install counts from skills_scraped.json
    3. Classify skills: Top N = active, rest = dormant
    4. User pinned skills are always active
    5. Output: active_tree.yaml + dormant_index.yaml
    """

    def __init__(
        self,
        config: Optional[LayeringConfig] = None,
        user_prefs: Optional[UserPreferences] = None,
        installs_data_path: Optional[Path] = None,
    ):
        self.config = config or get_config().layering_config()
        self.user_prefs = user_prefs or load_user_prefs()
        # Use installs_data_path from config, or override if explicitly provided
        if installs_data_path:
            self.installs_data_path = installs_data_path
        else:
            self.installs_data_path = PROJECT_ROOT / self.config.installs_data_path

    def process(self, tree_path: Path, output_dir: Optional[Path] = None) -> LayeredOutput:
        """
        Process an existing tree and generate layered output.

        Args:
            tree_path: Path to the original tree.yaml file
            output_dir: Directory for output files. Defaults to tree_path's directory.

        Returns:
            LayeredOutput containing active tree and dormant index.
        """
        output_dir = output_dir or tree_path.parent

        # 1. Load original tree
        tree_dict = self._load_tree(tree_path)
        if tree_dict is None:
            raise FileNotFoundError(f"Tree file not found: {tree_path}")

        # 2. Load installs data
        installs_data = self._load_installs_data()

        # 3. Collect all skills from tree
        all_skills = self._collect_all_skills(tree_dict)
        console.print(f"[dim]Collected {len(all_skills)} skills from tree[/dim]")

        # 4. Enrich skills with install counts
        self._enrich_with_installs(all_skills, installs_data)

        # 5. Classify skills into active/dormant
        active_ids, dormant_ids = self._classify_skills(all_skills)
        console.print(f"[dim]Active: {len(active_ids)}, Dormant: {len(dormant_ids)}[/dim]")

        # 6. Generate active tree (filter original tree)
        active_tree = self._filter_tree(tree_dict, active_ids)

        # 7. Generate dormant index
        dormant_index = self._build_dormant_index(all_skills, dormant_ids)

        stats = {
            "total_skills": len(all_skills),
            "active_skills": len(active_ids),
            "dormant_skills": len(dormant_ids),
            "pinned_skills": len(self.user_prefs.pinned_skill_ids),
            "threshold": self.config.active_threshold,
        }

        return LayeredOutput(
            active_tree=active_tree,
            dormant_index=dormant_index,
            stats=stats,
        )

    def _load_tree(self, tree_path: Path) -> Optional[dict]:
        """Load tree from YAML file."""
        if not tree_path.exists():
            return None
        with open(tree_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _load_installs_data(self) -> dict[str, dict]:
        """Load install count data from skills_scraped.json.

        Returns:
            Dict mapping skill_slug -> skill data with installs_count.
        """
        if not self.installs_data_path.exists():
            console.print(f"[yellow]Warning: Installs data not found at {self.installs_data_path}[/yellow]")
            return {}

        try:
            with open(self.installs_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Build lookup by skill_slug
            result = {}
            for item in data:
                slug = item.get("skill_slug", "")
                if slug:
                    result[slug] = {
                        "installs_count": item.get("installs_count", 0),
                        "rank": item.get("rank", 9999),
                    }
            return result
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Failed to load installs data: {e}[/yellow]")
            return {}

    def _collect_all_skills(self, tree_dict: dict, path: str = "") -> list[dict]:
        """Recursively collect all skills from tree structure.

        Returns:
            List of skill dicts with added 'tree_path' field.
        """
        skills = []

        # Current node's skills
        for skill in tree_dict.get("skills", []):
            skill_copy = dict(skill)
            skill_copy["tree_path"] = path or tree_dict.get("id", "root")
            skills.append(skill_copy)

        # Recurse into children
        for child in tree_dict.get("children", []):
            child_path = f"{path}/{child['id']}" if path else child.get("id", "")
            skills.extend(self._collect_all_skills(child, child_path))

        return skills

    def _enrich_with_installs(self, skills: list[dict], installs_data: dict[str, dict]) -> None:
        """Enrich skills with install counts (modifies in place)."""
        for skill in skills:
            skill_id = skill.get("id", "")
            if skill_id in installs_data:
                skill["installs_count"] = installs_data[skill_id]["installs_count"]
                skill["installs_rank"] = installs_data[skill_id]["rank"]
            else:
                skill["installs_count"] = 0
                skill["installs_rank"] = 9999

    def _classify_skills(self, all_skills: list[dict]) -> tuple[set[str], set[str]]:
        """
        Classify skills into active and dormant sets.

        Rules:
        1. Pinned skills are always active
        2. Top N by installs are active
        3. Rest are dormant

        Returns:
            (active_ids, dormant_ids) tuple of sets.
        """
        threshold = self.config.active_threshold
        pinned_ids = set(self.user_prefs.pinned_skill_ids)

        # Sort by installs (descending)
        sorted_skills = sorted(all_skills, key=lambda s: s.get("installs_count", 0), reverse=True)

        active_ids = set(pinned_ids)  # Pinned always active
        dormant_ids = set()
        active_count = 0

        for skill in sorted_skills:
            sid = skill.get("id", "")
            if not sid:
                continue

            if sid in pinned_ids:
                continue  # Already counted as active

            if active_count < threshold:
                active_ids.add(sid)
                active_count += 1
            else:
                dormant_ids.add(sid)

        return active_ids, dormant_ids

    def _filter_tree(self, tree_dict: dict, active_ids: set[str]) -> dict:
        """
        Create a filtered copy of tree containing only active skills.

        Returns:
            New tree dict with only active skills (doesn't modify original).
        """
        result = {
            "id": tree_dict.get("id", "root"),
            "name": tree_dict.get("name", ""),
            "description": tree_dict.get("description", ""),
        }

        # Filter skills
        original_skills = tree_dict.get("skills", [])
        if original_skills:
            filtered_skills = [s for s in original_skills if s.get("id") in active_ids]
            if filtered_skills:
                result["skills"] = filtered_skills

        # Recurse into children
        original_children = tree_dict.get("children", [])
        if original_children:
            filtered_children = []
            for child in original_children:
                filtered_child = self._filter_tree(child, active_ids)
                # Only include child if it has skills or children
                has_content = filtered_child.get("skills") or filtered_child.get("children")
                if has_content:
                    filtered_children.append(filtered_child)
            if filtered_children:
                result["children"] = filtered_children

        return result

    def _build_dormant_index(self, all_skills: list[dict], dormant_ids: set[str]) -> DormantIndex:
        """Build dormant index from skills list."""
        dormant_entries = []

        for skill in all_skills:
            sid = skill.get("id", "")
            if sid not in dormant_ids:
                continue

            entry = DormantSkillEntry(
                id=sid,
                name=skill.get("name", ""),
                description=skill.get("description", ""),
                skill_path=skill.get("skill_path", ""),
                installs_count=skill.get("installs_count", 0),
                github_url=skill.get("github_url", ""),
                stars=skill.get("stars", 0),
                is_official=skill.get("is_official", False),
                author=skill.get("author", ""),
                tree_path=skill.get("tree_path", ""),
            )
            dormant_entries.append(entry)

        # Sort by installs (descending) for consistent ordering
        dormant_entries.sort(key=lambda e: e.installs_count, reverse=True)

        return DormantIndex(
            version=1,
            created_at=datetime.now().isoformat(),
            skills_count=len(dormant_entries),
            skills=dormant_entries,
        )


# =============================================================================
# Directory-Based Dormant Index Builder
# =============================================================================

def build_dormant_index_from_directory(dormant_skills_dir: Path) -> DormantIndex:
    """Build dormant index by scanning a directory of dormant skills.

    This is used for directory-based layering where active/dormant classification
    is determined by which directory a skill lives in, rather than install counts.

    Args:
        dormant_skills_dir: Path to directory containing dormant skill folders.

    Returns:
        DormantIndex with entries for all skills found in the directory.
    """
    from .skill_scanner import SkillScanner

    scanner = SkillScanner(dormant_skills_dir)
    scanned = scanner.scan(show_progress=True)

    entries = [
        DormantSkillEntry(
            id=s.id,
            name=s.name,
            description=s.description,
            skill_path=s.skill_path,
            installs_count=0,
            github_url=s.github_url,
            stars=s.stars,
            is_official=s.is_official,
            author=s.author,
            tree_path="",
        )
        for s in scanned
    ]
    entries.sort(key=lambda e: e.name.lower())

    return DormantIndex(
        version=1,
        created_at=datetime.now().isoformat(),
        skills_count=len(entries),
        skills=entries,
    )


# =============================================================================
# File I/O Helpers
# =============================================================================

def atomic_yaml_write(path: Path, data: dict) -> None:
    """Write YAML data atomically using temp file + rename."""
    temp_path = path.with_suffix(".yaml.tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    temp_path.replace(path)  # Atomic on POSIX


# =============================================================================
# Skill Promotion Functions (for pinning dormant skills to active tree)
# =============================================================================

def _count_skills_in_node(node: dict) -> int:
    """Recursively count skills in a node."""
    count = len(node.get("skills", []))
    for child in node.get("children", []):
        count += _count_skills_in_node(child)
    return count


def _find_best_node_with_llm(tree: dict, skill: dict) -> dict:
    """
    Use LLM to find the best node for inserting a skill.

    Traverses the tree from root, using LLM at each level to select
    the most appropriate child node, until reaching a leaf.

    Args:
        tree: Tree dict structure (active_tree)
        skill: Skill dict with id, name, description

    Returns:
        The target leaf node dict
    """
    import litellm
    from .prompts import SKILL_CLASSIFICATION_PROMPT
    from .models import parse_json_from_response

    cfg = get_config()
    mcfg = cfg.manager_config()
    ensure_cache()
    current = tree

    while True:
        children = current.get("children", [])

        # If no children, this is a leaf node - return it
        if not children:
            return current

        # If only one child, go directly to it
        if len(children) == 1:
            current = children[0]
            continue

        # Build options for LLM
        options_lines = []
        for child in children:
            skill_count = _count_skills_in_node(child)
            options_lines.append(f"- {child['id']}: {child.get('name', child['id'])} ({skill_count} skills)")
            if child.get("description"):
                options_lines.append(f"  {child['description']}")
        options_text = "\n".join(options_lines)

        # Call LLM to select best category
        prompt = SKILL_CLASSIFICATION_PROMPT.format(
            skill_id=skill["id"],
            skill_name=skill.get("name", skill["id"]),
            skill_description=skill.get("description", ""),
            options=options_text,
        )

        try:
            response = litellm.completion(
                model=cfg.llm_model,
                messages=[{"role": "user", "content": prompt}],
                api_key=cfg.llm_api_key,
                api_base=cfg.llm_base_url,
                temperature=0.0,  # Deterministic for classification
                caching=mcfg.build.caching,
                num_retries=mcfg.build.num_retries,
                timeout=mcfg.build.timeout,
            )
            result = parse_json_from_response(response.choices[0].message.content, default={})
            selected_id = result.get("selected_category", "")
        except litellm.AuthenticationError:
            console.print("[red]Authentication failed - check API key[/red]")
            raise
        except Exception as e:
            console.print(f"[yellow]LLM classification failed: {e}, using first child[/yellow]")
            selected_id = ""

        # Find the selected child
        selected_child = None
        for child in children:
            if child["id"] == selected_id:
                selected_child = child
                break

        if selected_child:
            current = selected_child
        else:
            # LLM selection failed, fallback to first child
            if children:
                current = children[0]
            else:
                return current


def _update_node_description_with_llm(node: dict) -> None:
    """
    Update node description based on its skills using LLM.

    Maintains consistency with TreeBuilder's description generation style
    (2-3 sentences describing user goals, skill types, and when to look here).
    """
    import litellm
    from .prompts import NODE_DESCRIPTION_UPDATE_PROMPT
    from .models import parse_json_from_response

    ensure_cache()

    skills = node.get("skills", [])
    if not skills:
        return

    # Format skills list
    skills_lines = []
    for skill in skills:
        skills_lines.append(f"- {skill['id']}: {skill.get('name', skill['id'])}")
        if skill.get("description"):
            skills_lines.append(f"  {skill['description']}")
    skills_list = "\n".join(skills_lines)

    prompt = NODE_DESCRIPTION_UPDATE_PROMPT.format(
        node_id=node.get("id", ""),
        node_name=node.get("name", ""),
        current_description=node.get("description", ""),
        skills_list=skills_list,
    )

    cfg = get_config()
    mcfg = cfg.manager_config()
    try:
        response = litellm.completion(
            model=cfg.llm_model,
            messages=[{"role": "user", "content": prompt}],
            api_key=cfg.llm_api_key,
            api_base=cfg.llm_base_url,
            temperature=0.0,
            caching=mcfg.build.caching,
            num_retries=mcfg.build.num_retries,
            timeout=mcfg.build.timeout,
        )
        result = parse_json_from_response(response.choices[0].message.content, default={})
        new_description = result.get("description", "")
        if new_description:
            node["description"] = new_description
    except litellm.AuthenticationError:
        console.print("[red]Authentication failed - check API key[/red]")
        raise
    except Exception as e:
        console.print(f"[yellow]Description update failed: {e}[/yellow]")
        # Keep existing description on failure


def _insert_skill_with_llm(tree: dict, skill: dict) -> tuple[bool, dict]:
    """
    Insert skill into tree using LLM to find the best location.
    After insertion, update node description and check if node needs splitting.

    Returns:
        Tuple of (needs_split, target_node) where needs_split is True if
        node skill count exceeds threshold, and target_node is the node
        where the skill was inserted.
    """
    # Use LLM to find the best node for this skill
    target_node = _find_best_node_with_llm(tree, skill)

    # Ensure skills array exists
    if "skills" not in target_node:
        target_node["skills"] = []

    # Check if skill already exists (avoid duplicates)
    existing_ids = {s.get("id") for s in target_node["skills"]}
    if skill["id"] not in existing_ids:
        target_node["skills"].append(skill)

        # Update node description after insertion
        _update_node_description_with_llm(target_node)

    # Return whether splitting is needed and the target node
    cfg = get_config()
    mcfg = cfg.manager_config()
    max_skills = int(mcfg.branching_factor * 1.5)  # max_skills_per_node
    return len(target_node.get("skills", [])) > max_skills, target_node


def _maybe_split_node(node: dict) -> None:
    """
    Check if node needs splitting and perform split if necessary.

    Uses same logic as TreeBuilder._split_skills():
    1. If skills count <= max_skills_per_node, do nothing
    2. Otherwise, call LLM to group skills into sub-categories
    3. Create child nodes and move skills

    NOTE: This is a simplified version for single-skill insertion.
    For large-scale operations, use TreeBuilder.build() instead.
    """
    import litellm
    from .prompts import RECURSIVE_SPLIT_PROMPT
    from .models import parse_json_from_response

    ensure_cache()

    cfg = get_config()
    mcfg = cfg.manager_config()
    max_skills = int(mcfg.branching_factor * 1.5)

    skills = node.get("skills", [])
    if len(skills) <= max_skills:
        return  # No split needed

    # Build parent context
    parent_context = {
        "name": node.get("name", node.get("id", "")),
        "description": node.get("description", ""),
    }
    context_section = f'''## Parent Context
You are creating sub-categories under "{parent_context["name"]}": {parent_context["description"]}
Ensure sub-categories are coherent with this parent context.'''

    # Calculate group range
    min_groups = max(2, mcfg.branching_factor - 3)
    max_groups = mcfg.branching_factor + 2

    # Format skills list
    skills_list_lines = []
    for skill in skills:
        desc = skill.get("description", "")
        skills_list_lines.append(f"- {skill['id']}: {skill.get('name', skill['id'])}")
        if desc:
            skills_list_lines.append(f"  {desc}")
    skills_list = "\n".join(skills_list_lines)

    prompt = RECURSIVE_SPLIT_PROMPT.format(
        count=len(skills),
        context_section=context_section,
        skills_list=skills_list,
        min_groups=min_groups,
        max_groups=max_groups,
    )

    # Call LLM
    try:
        response = litellm.completion(
            model=cfg.llm_model,
            messages=[{"role": "user", "content": prompt}],
            api_key=cfg.llm_api_key,
            api_base=cfg.llm_base_url,
            caching=mcfg.build.caching,
            num_retries=mcfg.build.num_retries,
            timeout=mcfg.build.timeout,
        )
        result = parse_json_from_response(response.choices[0].message.content, default={})
    except litellm.AuthenticationError:
        console.print("[red]Authentication failed - check API key[/red]")
        raise
    except Exception as e:
        console.print(f"[yellow]Split failed: {e}, keeping node as-is[/yellow]")
        return

    groups = result.get("groups", {})
    if not groups:
        return

    # Build skill map
    skill_map = {s["id"]: s for s in skills}

    # Create children and move skills
    children = node.get("children", [])
    for group_id, group_data in groups.items():
        child_skill_ids = group_data.get("skill_ids", [])
        child_skills = [skill_map[sid] for sid in child_skill_ids if sid in skill_map]

        if len(child_skills) < 2:
            # Don't pop from skill_map — leave them for unassigned handling
            continue

        # Only remove from skill_map after confirming we'll use this group
        for sid in child_skill_ids:
            skill_map.pop(sid, None)

        child_node = {
            "id": group_id,
            "name": group_data.get("name", group_id),
            "description": group_data.get("description", ""),
            "skills": child_skills,
        }
        children.append(child_node)

    # Handle unassigned skills
    if skill_map and children:
        # Add to largest child
        largest_child = max(children, key=lambda c: len(c.get("skills", [])))
        largest_child["skills"].extend(skill_map.values())

    # Update node: remove skills, add children
    node["skills"] = []
    node["children"] = children

    # Update node description to reflect new structure
    child_names = [c.get("name", c.get("id")) for c in children]
    node["description"] = f"Contains: {', '.join(child_names[:5])}" + ("..." if len(child_names) > 5 else "")


def _find_node_by_path(tree: dict, tree_path: str) -> Optional[dict]:
    """
    Find a node in the tree by its path string.

    The path format is "child_id/grandchild_id/..." where each segment
    is the ID of a child node. An empty string or the root ID returns the
    root node.

    Args:
        tree: Tree dict structure
        tree_path: Path string (e.g., "development/code-generation")

    Returns:
        The target node dict, or None if path doesn't exist.
    """
    if not tree_path or tree_path == tree.get("id", "root"):
        return tree

    # Split path into segments and skip root if present
    segments = [s for s in tree_path.split("/") if s]
    if segments and segments[0] == tree.get("id", "root"):
        segments = segments[1:]

    current = tree
    for segment in segments:
        children = current.get("children", [])
        found = None
        for child in children:
            if child.get("id") == segment:
                found = child
                break
        if found is None:
            return None  # Path doesn't exist in tree
        current = found

    return current


def promote_skill_to_active(
    skill_id: str,
    active_tree_path: Path,
    dormant_index_path: Path,
) -> bool:
    """
    Promote a dormant skill to active tree.

    Uses the stored tree_path from dormant_index to place the skill back
    in its original location. Falls back to LLM-based traversal only if the
    original path no longer exists in the active tree.

    Args:
        skill_id: ID of the skill to promote
        active_tree_path: Path to active_tree.yaml
        dormant_index_path: Path to dormant_index.yaml

    Returns:
        True if skill was promoted, False if not found.
    """
    # Load dormant index
    with open(dormant_index_path, "r", encoding="utf-8") as f:
        dormant_data = yaml.safe_load(f)

    # Find skill in dormant list
    skill_entry = None
    for skill in dormant_data.get("skills", []):
        if skill.get("id") == skill_id:
            skill_entry = skill
            break

    if not skill_entry:
        return False  # Not in dormant index

    # Load active tree
    with open(active_tree_path, "r", encoding="utf-8") as f:
        active_tree = yaml.safe_load(f)

    # Convert to skill dict for tree insertion
    skill_dict = {
        "id": skill_entry["id"],
        "name": skill_entry["name"],
        "description": skill_entry["description"],
        "skill_path": skill_entry["skill_path"],
        "github_url": skill_entry.get("github_url", ""),
        "stars": skill_entry.get("stars", 0),
        "is_official": skill_entry.get("is_official", False),
        "author": skill_entry.get("author", ""),
    }

    # Try to find the original location using tree_path (fast, no LLM)
    tree_path = skill_entry.get("tree_path", "")
    target_node = _find_node_by_path(active_tree, tree_path) if tree_path else None

    if target_node is not None:
        # Direct insertion at original location
        if "skills" not in target_node:
            target_node["skills"] = []
        existing_ids = {s.get("id") for s in target_node["skills"]}
        if skill_dict["id"] not in existing_ids:
            target_node["skills"].append(skill_dict)

        # Check if splitting is needed
        cfg = get_config()
        mcfg = cfg.manager_config()
        max_skills = int(mcfg.branching_factor * 1.5)
        if len(target_node.get("skills", [])) > max_skills:
            _maybe_split_node(target_node)
    else:
        # Fallback: use LLM to find best position (original path gone)
        console.print(f"[dim]Original path '{tree_path}' not found, using LLM placement[/dim]")
        needs_split, target_node = _insert_skill_with_llm(active_tree, skill_dict)
        if needs_split:
            _maybe_split_node(target_node)

    # Remove from dormant index
    dormant_data["skills"] = [
        s for s in dormant_data["skills"] if s.get("id") != skill_id
    ]
    dormant_data["skills_count"] = len(dormant_data["skills"])

    # Save both files atomically (write to temp, then rename)
    atomic_yaml_write(active_tree_path, active_tree)
    atomic_yaml_write(dormant_index_path, dormant_data)

    return True


def process_tree_layering(
    tree_path: Path,
    output_dir: Optional[Path] = None,
    config: Optional[LayeringConfig] = None,
    verbose: bool = False,
) -> Optional[LayeredOutput]:
    """
    Convenience function to run layer post-processing.

    Args:
        tree_path: Path to the original tree.yaml file
        output_dir: Directory for output files
        config: Layering configuration (uses config.yaml if not provided)
        verbose: Print progress

    Returns:
        LayeredOutput with active tree and dormant index.
    """
    cfg = config or get_config().layering_config()

    if not cfg.is_install_count_mode:
        if cfg.is_directory_mode:
            console.print("[yellow]process_tree_layering() is for install-count mode. "
                          "Use CLI 'build' with directory mode for directory-based layering.[/yellow]")
        else:
            console.print("[yellow]Layering is disabled in config. Enable with layering.mode: install-count (or directory)[/yellow]")
        return None

    processor = LayerPostProcessor(config=cfg)
    output = processor.process(tree_path, output_dir)

    if verbose:
        console.print("\n[bold green]Layering complete![/bold green]")
        console.print(f"  Total skills: {output.stats['total_skills']}")
        console.print(f"  Active skills: {output.stats['active_skills']}")
        console.print(f"  Dormant skills: {output.stats['dormant_skills']}")
        console.print(f"  Pinned skills: {output.stats['pinned_skills']}")

    return output

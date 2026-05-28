"""
Tree Builder - Build capability tree from skills using LLM classification.

Two-phase build process:
1. Structure Discovery: Sample skills to discover domain/type structure
2. Anchored Classification: Classify remaining skills into discovered structure
"""

import hashlib
import json
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from pathlib import Path
from typing import Optional

import litellm
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.tree import Tree as RichTree

from config import get_config
from cache import ensure_cache
from .models import DynamicTreeConfig, TreeNode, Skill, FIXED_ROOT_CATEGORIES, SKILL_DESCRIPTION_MAX_LENGTH, parse_json_from_response
from .skill_scanner import SkillScanner
from .prompts import (
    GROUP_MERGE_PROMPT,
    GROUP_DISCOVERY_PROMPT, SKILL_ASSIGNMENT_PROMPT, NODE_LABEL_REWRITE_PROMPT,
)

# litellm._turn_on_debug()

console = Console()

class TreeBuilder:
    """
    Unified tree builder with auto-selection and node splitting.

    Features:
    - Auto-selects build method based on skill count
    - Splits oversized nodes (> max_skills_per_node)
    - Simple tree visualization
    """

    # Token budget constants for auto batch size calculation
    PROMPT_OVERHEAD_TOKENS = 3000    # prompt template + instructions
    OUTPUT_RESERVE_TOKENS = 4000     # JSON response reserve
    AVG_TOKENS_PER_SKILL = 75       # average tokens per skill entry
    DEFAULT_CONTEXT_WINDOW = 128000  # fallback context window size
    DEFAULT_MAX_OUTPUT_TOKENS = 32768  # fallback max output tokens

    def __init__(
        self,
        skills_dir: Path | str | None = None,
        output_path: Path | str | None = None,
        config: Optional[DynamicTreeConfig] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_workers: Optional[int] = None,
    ):
        cfg = get_config()
        mcfg = cfg.manager_config()
        build_cfg = mcfg.build
        self.scanner = SkillScanner(skills_dir)
        from config import PROJECT_ROOT
        default_tree_path = PROJECT_ROOT / "data" / "capability_trees" / "tree.yaml"
        self.output_path = Path(output_path) if output_path else default_tree_path
        self.config = config or DynamicTreeConfig(
            branching_factor=mcfg.branching_factor,
            max_depth=mcfg.max_depth
        )
        self.model = model or cfg.llm_model
        self.api_key = api_key or cfg.llm_api_key
        self.base_url = base_url or cfg.llm_base_url
        self.max_workers = max_workers or build_cfg.max_workers
        self._deterministic_prompts = build_cfg.deterministic_prompts
        self._discovery_seed = build_cfg.discovery_seed
        self._prompt_fingerprint_version = build_cfg.prompt_fingerprint_version
        self._cache_observability = build_cfg.cache_observability

        self._llm_calls = 0
        self._retry_calls = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._cache_unknown = 0
        self._prompt_fingerprints: set[str] = set()
        self._leaf_skills = 0  # Skills that have reached leaf nodes
        self._counter_lock = threading.Lock()  # Protects _llm_calls, _leaf_skills, _consecutive_failures
        self._progress = None  # Rich progress bar
        self._progress_task = None
        self._batch_size_cache = None
        self._max_output_tokens_cache = None
        self._thread_local = threading.local()  # Per-thread truncation flag
        self._executor = None  # Shared executor, set in _build_tree
        self._llm_semaphore = threading.Semaphore(self.max_workers)  # Limit concurrent LLM calls
        self._consecutive_failures = 0
        self.MAX_CONSECUTIVE_FAILURES = 5
        ensure_cache()

    def _auto_batch_size(self) -> int:
        """Calculate batch size from model context window."""
        if self._batch_size_cache is not None:
            return self._batch_size_cache
        try:
            info = litellm.get_model_info(self.model)
            ctx_window = info.get("max_input_tokens") or info.get("max_tokens") or self.DEFAULT_CONTEXT_WINDOW
        except Exception:
            ctx_window = self.DEFAULT_CONTEXT_WINDOW
        available = ctx_window - self.PROMPT_OVERHEAD_TOKENS - self.OUTPUT_RESERVE_TOKENS
        batch_size = available // self.AVG_TOKENS_PER_SKILL
        self._batch_size_cache = max(50, min(batch_size, 1000))
        return self._batch_size_cache

    def _get_max_output_tokens(self) -> int:
        """Get max output tokens for the model, with caching."""
        if self._max_output_tokens_cache is not None:
            return self._max_output_tokens_cache
        try:
            info = litellm.get_model_info(self.model)
            max_out = info.get("max_output_tokens")
            if max_out and max_out > 0:
                self._max_output_tokens_cache = max_out
                return max_out
        except Exception:
            pass
        self._max_output_tokens_cache = self.DEFAULT_MAX_OUTPUT_TOKENS
        return self._max_output_tokens_cache

    def build(self, verbose: bool = False, show_tree: bool = True, generate_html: bool = True) -> dict:
        """
        Build capability tree from skill_seeds.

        Args:
            verbose: Print detailed progress
            show_tree: Display tree after building
            generate_html: Generate HTML visualization

        Returns:
            Tree dict structure
        """
        console.print(Panel.fit(
            "[bold cyan]Building Capability Tree[/bold cyan]",
            border_style="cyan",
        ))

        # Step 1: Scan skills
        console.print("\n[bold]Step 1: Scanning skills...[/bold]")
        skills = self.scanner.to_dict_list()

        if not skills:
            console.print("[red]No skills found.[/red]")
            return {}

        console.print(f"[green]Found {len(skills)} skills[/green]")

        # Step 2: Build tree with auto-selection
        console.print("\n[bold]Step 2: Building tree structure...[/bold]")
        tree = self._build_tree(skills, verbose)

        # Step 3: Convert to dict and write
        console.print("\n[bold]Step 3: Writing to file...[/bold]")
        tree_dict = self._tree_to_dict(tree)
        self._write_yaml(tree_dict)

        # Step 4: Generate HTML visualization
        if generate_html:
            from .visualizer import generate_html as gen_html
            html_path = self.output_path.with_suffix('.html')
            gen_html(tree_dict, html_path)
            console.print(f"[green]Generated HTML: {html_path}[/green]")

        # Show tree
        if show_tree:
            console.print("\n[bold]Tree Structure:[/bold]")
            self._print_tree(tree_dict)

        self._print_cache_stats()

        done_lines = [f"[bold green]Done![/bold green] ({self._llm_calls} LLM calls)"]
        if self._cache_observability:
            done_lines.append(
                f"Cache hits/misses/unknown: {self._cache_hits}/{self._cache_misses}/{self._cache_unknown}"
            )
            done_lines.append(f"Unique prompt fingerprints: {len(self._prompt_fingerprints)}")
        done_lines.append(f"Output: {self.output_path}")

        console.print(Panel.fit(
            "\n".join(done_lines),
            border_style="green",
        ))

        return tree_dict

    def _build_tree(self, skills: list[dict], verbose: bool = False) -> TreeNode:
        """Build tree using queue-based parallel approach (no recursion)."""
        root = TreeNode(id="root", name="Root", description="Skill capability tree root")

        # Queue: (node, skills, depth, parent_context)
        queue = [(root, skills, 0, None)]
        futures_map = {}  # future -> (node, depth)

        total_skills = len(skills)
        self._leaf_skills = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("({task.fields[leaf]}/{task.fields[total_count]} skills done, {task.fields[llm]} LLM, {task.fields[pending]} pending)"),
            console=console,
            transient=False,
        ) as progress:
            self._progress = progress
            self._progress_task = progress.add_task("Building tree...", total=total_skills, pending=0, leaf=0, llm=0, total_count=total_skills)

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                self._executor = executor
                while queue or futures_map:
                    # Submit all queued tasks
                    while queue:
                        node, node_skills, depth, parent_context = queue.pop(0)
                        future = executor.submit(
                            self._process_node,
                            node=node,
                            skills=node_skills,
                            depth=depth,
                            parent_context=parent_context,
                            verbose=verbose,
                        )
                        futures_map[future] = (node, depth)

                    # Update pending count
                    if self._progress and self._progress_task is not None:
                        self._progress.update(self._progress_task, pending=len(futures_map))

                    if not futures_map:
                        break

                    # Wait for at least one to complete
                    done, _ = wait(futures_map.keys(), return_when=FIRST_COMPLETED)

                    # Process completed futures
                    for future in sorted(done, key=lambda fut: futures_map[fut][0].id):
                        node, depth = futures_map.pop(future)
                        try:
                            children_to_process = future.result()
                            # Add children to queue
                            for child_node, child_skills in children_to_process:
                                parent_ctx = {"name": child_node.name, "description": child_node.description}
                                queue.append((child_node, child_skills, depth + 1, parent_ctx))
                        except Exception as e:
                            console.print(f"[red]Error processing {node.id}: {e}[/red]")

            self._progress = None
            self._executor = None

        # Global audit: check for missing skills
        self._audit_tree(root, skills)

        return root

    def _collect_leaf_skills(self, node: TreeNode) -> set:
        """Recursively collect all skill IDs from leaf nodes."""
        if node.is_leaf:
            return {s.id for s in node.skills}
        result = set()
        for child in node.children:
            result |= self._collect_leaf_skills(child)
        return result

    def _audit_tree(self, root: TreeNode, input_skills: list[dict]) -> None:
        """Post-build audit: recover any missing skills into an 'uncategorized' node."""
        input_ids = {s["id"] for s in input_skills}
        tree_ids = self._collect_leaf_skills(root)
        missing_ids = input_ids - tree_ids

        if not missing_ids:
            return

        console.print(Panel(
            f"[bold red]Skill Loss Detected: {len(missing_ids)}/{len(input_ids)} skills "
            f"missing from tree.[/bold red]\n"
            "Recovering into 'uncategorized' node.",
            title="[bold red]Post-Build Audit[/bold red]",
            border_style="red",
        ))

        # Build uncategorized node
        skill_map = {s["id"]: s for s in input_skills}
        missing_skills = [skill_map[sid] for sid in missing_ids if sid in skill_map]

        uncat_node = TreeNode(
            id="uncategorized",
            name="Uncategorized",
            description="Skills that were lost during classification and recovered by post-build audit.",
            depth=1,
            parent_id="root",
        )
        self._assign_skills_to_leaf(uncat_node, missing_skills)
        root.children.append(uncat_node)

    def _process_node(
        self,
        node: TreeNode,
        skills: list[dict],
        depth: int,
        parent_context: Optional[dict],
        verbose: bool = False,
    ) -> list[tuple[TreeNode, list[dict]]]:
        """
        Process a single node: split skills and create children.
        Returns list of (child_node, child_skills) tuples for further processing.
        """
        # Special handling for root node: use fixed categories with flat mapping
        if depth == 0 and node.id == "root":
            # Phase 1: Use custom root categories if configured, otherwise fixed defaults
            categories = self.config.root_categories or FIXED_ROOT_CATEGORIES
            groups = {cat_id: {"name": d["name"], "description": d["description"]}
                      for cat_id, d in categories.items()}
            if self._progress and self._progress_task is not None:
                self._progress.update(self._progress_task,
                    description=f"Classifying root ({len(skills)} skills)")
            if verbose:
                console.print(f"[cyan]Classifying {len(skills)} skills into fixed root categories[/cyan]")
            # Phase 2: Classify via flat mapping
            assignments = self._classify_skills(skills, groups, verbose)
            assignments = self._validate_and_recover(skills, groups, assignments, verbose)
            groups_with_skills = self._build_groups_from_assignments(groups, assignments)
            return self._build_children_from_groups(node, skills, groups_with_skills, depth, verbose)

        # Terminal condition: skills count within threshold
        if len(skills) <= self.config.max_skills_per_node:
            self._assign_skills_to_leaf(node, skills)
            if verbose:
                console.print(f"[dim]  Leaf: {node.id} ({len(skills)} skills)[/dim]")
            return []

        # Depth limit check
        if depth >= self.config.max_depth:
            console.print(Panel(
                f"[bold red]Max depth ({self.config.max_depth}) reached at node '{node.id}' "
                f"with {len(skills)} skills remaining.[/bold red]\n"
                "These skills will be forced into a single leaf node.",
                title="[bold red]Max Depth Reached[/bold red]",
                border_style="red",
            ))
            self._assign_skills_to_leaf(node, skills)
            return []

        # LLM grouping
        if self._progress and self._progress_task is not None:
            self._progress.update(self._progress_task, description=f"Splitting: {node.id} ({len(skills)} skills)")
        if verbose:
            console.print(f"[cyan]Splitting: {node.id} ({len(skills)} skills, depth={depth})[/cyan]")

        groups = self._split_skills(skills, parent_context, verbose)

        if not groups:
            # Grouping failed, make it a leaf
            console.print(Panel(
                f"[bold red]Grouping failed for node '{node.id}' with {len(skills)} skills.[/bold red]\n"
                "All skills will be forced into a single leaf node.",
                title="[bold red]Grouping Failed[/bold red]",
                border_style="red",
            ))
            self._assign_skills_to_leaf(node, skills)
            return []

        return self._build_children_from_groups(node, skills, groups, depth, verbose)

    # =========================================================================
    # Two-phase classification: discover groups -> flat assignment
    # =========================================================================

    def _assign_skills_to_leaf(self, node: TreeNode, skills: list[dict]) -> None:
        """Assign skill dicts to a leaf node as Skill objects. Updates progress counter."""
        for skill_data in skills:
            skill = Skill(
                id=skill_data["id"],
                name=skill_data.get("name", skill_data["id"]),
                description=skill_data.get("description", ""),
                path=node.id,
                skill_path=skill_data.get("skill_path", ""),
                content=skill_data.get("content", ""),
                github_url=skill_data.get("github_url", ""),
                stars=skill_data.get("stars", 0),
                is_official=skill_data.get("is_official", False),
                author=skill_data.get("author", ""),
            )
            node.skills.append(skill)
        # Update leaf skills count (thread-safe)
        with self._counter_lock:
            self._leaf_skills += len(skills)
            if self._progress and self._progress_task is not None:
                self._progress.update(self._progress_task, leaf=self._leaf_skills, completed=self._leaf_skills)

    def _build_children_from_groups(
        self,
        node: TreeNode,
        skills: list[dict],
        groups: dict,
        depth: int,
        verbose: bool = False,
    ) -> list[tuple[TreeNode, list[dict]]]:
        """Build child nodes from groups dict. Returns [(child_node, child_skills)]."""
        skill_map = {s["id"]: s for s in skills}
        children_to_process = []
        singleton_triggered = False

        for group_id, group_data in groups.items():
            child_skill_ids = group_data.get("skill_ids", [])
            child_skills = [skill_map[sid] for sid in child_skill_ids if sid in skill_map]

            # Skip tiny groups and reassign their skills in a later pass.
            if len(child_skills) < 2:
                if len(child_skills) == 1:
                    singleton_triggered = True
                if verbose:
                    skipped_ids = [s["id"] for s in child_skills]
                    console.print(f"[dim]  Skipping singleton group '{group_id}' "
                                  f"({skipped_ids}), will reassign into existing groups[/dim]")
                continue

            child_node = TreeNode(
                id=group_id,
                name=group_data.get("name", group_id),
                description=group_data.get("description", ""),
                depth=depth + 1,
                parent_id=node.id,
            )

            node.children.append(child_node)

            # Mark assigned skills
            for sid in child_skill_ids:
                skill_map.pop(sid, None)

            children_to_process.append((child_node, child_skills))

        # Handle unassigned skills
        if skill_map:
            if children_to_process:
                unassigned = list(skill_map.values())
                reassigned_count, unassigned = self._reassign_skills_to_children(
                    unassigned,
                    children_to_process,
                )

                if unassigned:
                    largest_idx = max(range(len(children_to_process)),
                                     key=lambda i: len(children_to_process[i][1]))
                    unassigned_ratio = len(unassigned) / len(skills) if skills else 0
                    if unassigned_ratio > 0.1:
                        console.print(Panel(
                            f"[bold red]{len(unassigned)}/{len(skills)} skills ({unassigned_ratio:.0%}) unassigned "
                            f"at node '{node.id}'[/bold red]\n"
                            f"Dumping into '{children_to_process[largest_idx][0].id}'.",
                            title="[bold red]High Unassigned Skill Count[/bold red]",
                            border_style="red",
                        ))
                    elif verbose:
                        console.print(f"[yellow]  {len(unassigned)} unassigned skills -> "
                                      f"{children_to_process[largest_idx][0].id}[/yellow]")
                    child_node, child_skills = children_to_process[largest_idx]
                    children_to_process[largest_idx] = (child_node, child_skills + unassigned)
                elif verbose and reassigned_count > 0:
                    console.print(f"[dim]  Reassigned {reassigned_count} skipped skills under '{node.id}'[/dim]")
            else:
                # All groups invalid -> leaf fallback
                self._assign_skills_to_leaf(node, skills)
                return []

        if singleton_triggered and children_to_process:
            self._rewrite_node_label_after_singleton(node, children_to_process, verbose)

        return children_to_process

    def _reassign_skills_to_children(
        self,
        unassigned_skills: list[dict],
        children_to_process: list[tuple[TreeNode, list[dict]]],
    ) -> tuple[int, list[dict]]:
        """Reassign skipped/unassigned skills to existing child groups via flat mapping."""
        if not unassigned_skills or not children_to_process:
            return 0, unassigned_skills

        groups = {
            child_node.id: {
                "name": child_node.name,
                "description": child_node.description,
            }
            for child_node, _ in children_to_process
        }
        assignments = self._classify_skills_single(
            self._sorted_skills(unassigned_skills),
            groups,
            verbose=False,
            is_retry=True,
        )
        if not assignments:
            return 0, unassigned_skills

        child_idx = {child_node.id: idx for idx, (child_node, _) in enumerate(children_to_process)}
        reassigned_count = 0
        remaining_unassigned = []

        for skill in unassigned_skills:
            group_id = assignments.get(skill["id"])
            idx = child_idx.get(group_id)
            if idx is None:
                remaining_unassigned.append(skill)
                continue
            _, child_skills = children_to_process[idx]
            child_skills.append(skill)
            reassigned_count += 1

        return reassigned_count, remaining_unassigned

    def _rewrite_node_label_after_singleton(
        self,
        node: TreeNode,
        children_to_process: list[tuple[TreeNode, list[dict]]],
        verbose: bool = False,
    ) -> None:
        """Rewrite current node name/description after singleton reassignment."""
        if not children_to_process:
            return

        summary_lines = []
        for child_node, child_skills in sorted(children_to_process, key=lambda item: len(item[1]), reverse=True):
            sample_ids = ", ".join(skill["id"] for skill in child_skills[:5]) or "(none)"
            child_desc = child_node.description or "(no description)"
            summary_lines.append(
                f"- {child_node.id} ({len(child_skills)} skills)\n"
                f"  name: {child_node.name}\n"
                f"  description: {child_desc}\n"
                f"  sample_skill_ids: {sample_ids}"
            )

        prompt = NODE_LABEL_REWRITE_PROMPT.format(
            node_id=node.id,
            node_name=node.name,
            node_description=node.description or "(no description)",
            children_summary="\n".join(summary_lines),
        )
        result = self._call_llm_json(prompt)
        new_name = str(result.get("name", "")).strip()
        new_description = str(result.get("description", "")).strip()

        if not new_name or not new_description:
            if verbose:
                console.print(f"[yellow]  Failed to rewrite label for '{node.id}', keeping original[/yellow]")
            return

        node.name = new_name
        node.description = new_description
        if verbose:
            console.print(f"[dim]  Rewrote node label for '{node.id}' after singleton reassignment[/dim]")

    def _sorted_skills(self, skills: list[dict]) -> list[dict]:
        """Return skills in deterministic order when enabled."""
        if not self._deterministic_prompts:
            return list(skills)
        return sorted(skills, key=lambda s: str(s.get("id", "")))

    def _iter_group_items(self, groups: dict):
        """Iterate group items in deterministic order when enabled."""
        if not self._deterministic_prompts:
            return groups.items()
        return ((gid, groups[gid]) for gid in sorted(groups.keys()))

    def _normalize_prompt_for_fingerprint(self, prompt: str) -> str:
        """Normalize prompt text to keep fingerprint stable across runs."""
        normalized = prompt.replace("\r\n", "\n").replace("\r", "\n")
        normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
        return normalized.strip()

    def _prompt_fingerprint(self, prompt: str) -> str:
        """Compute deterministic prompt fingerprint."""
        payload = (
            f"{self._prompt_fingerprint_version}\n"
            f"{self.model}\n"
            f"{self._normalize_prompt_for_fingerprint(prompt)}"
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def _sampling_seed(self, parent_context: Optional[dict], skills_count: int) -> int:
        """Derive deterministic sampling seed from node context and size."""
        parent_name = (parent_context or {}).get("name", "")
        parent_desc = (parent_context or {}).get("description", "")
        material = f"{self._discovery_seed}|{parent_name}|{parent_desc}|{skills_count}"
        seed_hex = hashlib.sha256(material.encode("utf-8")).hexdigest()[:8]
        return int(seed_hex, 16)

    def _extract_cache_hit(self, response) -> Optional[bool]:
        """Best-effort extraction of cache hit status from LiteLLM response."""
        containers = []
        hidden_params = getattr(response, "_hidden_params", None)
        if isinstance(hidden_params, dict):
            containers.append(hidden_params)

        response_headers = getattr(response, "_response_headers", None)
        if isinstance(response_headers, dict):
            containers.append(response_headers)

        try:
            dumped = response.model_dump()  # pydantic-like response
            if isinstance(dumped, dict):
                containers.append(dumped)
        except Exception:
            pass

        for mapping in containers:
            hit = self._extract_cache_hit_from_mapping(mapping)
            if hit is not None:
                return hit
        return None

    def _extract_cache_hit_from_mapping(self, mapping: dict) -> Optional[bool]:
        """Parse cache hit from a mapping (recursively over nested dicts)."""
        key_aliases = {
            "cache_hit",
            "cachehit",
            "is_cached",
            "cached",
            "x-litellm-cache-hit",
            "litellm_cache_hit",
        }
        stack = [mapping]
        while stack:
            current = stack.pop()
            if not isinstance(current, dict):
                continue
            for key, value in current.items():
                key_norm = str(key).strip().lower()
                if key_norm in key_aliases:
                    if isinstance(value, bool):
                        return value
                    if isinstance(value, (int, float)):
                        return bool(value)
                    if isinstance(value, str):
                        value_norm = value.strip().lower()
                        if value_norm in {"1", "true", "hit", "yes"}:
                            return True
                        if value_norm in {"0", "false", "miss", "no"}:
                            return False
                if isinstance(value, dict):
                    stack.append(value)
        return None

    def _record_cache_observation(self, cache_hit: Optional[bool]) -> None:
        """Aggregate cache hit/miss counters."""
        if cache_hit is True:
            self._cache_hits += 1
        elif cache_hit is False:
            self._cache_misses += 1
        else:
            self._cache_unknown += 1

    def _print_cache_stats(self) -> None:
        """Print cache observability metrics for intuitive build feedback."""
        if not self._cache_observability:
            return
        known_total = self._cache_hits + self._cache_misses
        observed_hit_rate = (self._cache_hits / known_total * 100.0) if known_total else 0.0
        lower_bound_hit_rate = (self._cache_hits / self._llm_calls * 100.0) if self._llm_calls else 0.0
        lines = [
            f"LLM calls: {self._llm_calls}",
            f"Retry calls: {self._retry_calls}",
            f"Cache hits/misses/unknown: {self._cache_hits}/{self._cache_misses}/{self._cache_unknown}",
            f"Observed hit rate (known only): {observed_hit_rate:.1f}%",
            f"Estimated hit rate lower bound: {lower_bound_hit_rate:.1f}%",
            f"Unique prompt fingerprints: {len(self._prompt_fingerprints)}",
        ]
        console.print(Panel("\n".join(lines), title="[bold cyan]Cache Stats[/bold cyan]", border_style="cyan"))

    def _build_groups_from_assignments(self, groups: dict, assignments: dict) -> dict:
        """Convert flat {skill_id: group_id} back to groups dict with skill_ids lists."""
        result = {}
        for gid, gdata in self._iter_group_items(groups):
            sids = [sid for sid, assigned_gid in assignments.items() if assigned_gid == gid]
            if self._deterministic_prompts:
                sids.sort()
            if sids:
                result[gid] = {
                    "name": gdata.get("name", gid),
                    "description": gdata.get("description", ""),
                    "skill_ids": sids,
                }
        return result

    def _classify_skills(self, skills: list[dict], groups: dict, verbose: bool = False) -> dict:
        """
        Universal Phase 2: assign each skill to a group via flat mapping.

        Args:
            skills: skill dicts to classify
            groups: {group_id: {"name": ..., "description": ...}}
        Returns:
            {skill_id: group_id} mapping
        """
        ordered_skills = self._sorted_skills(skills)
        batch_size = self._auto_batch_size()
        if len(ordered_skills) > batch_size:
            return self._batched_classify_skills(ordered_skills, groups, batch_size, verbose)
        return self._classify_skills_single(ordered_skills, groups, verbose)

    def _classify_skills_single(
        self,
        skills: list[dict],
        groups: dict,
        verbose: bool = False,
        is_retry: bool = False,
    ) -> dict:
        """Single LLM call to assign skills to groups. Returns {skill_id: group_id}."""
        groups_list = "\n".join(
            f"- {gid}: {g['name']}\n  {g['description']}" for gid, g in self._iter_group_items(groups)
        )
        skills_list = self._format_skills_list(skills)
        prompt = SKILL_ASSIGNMENT_PROMPT.format(groups_list=groups_list, skills_list=skills_list)
        result = self._call_llm_json(prompt, is_retry=is_retry)
        raw = result.get("assignments", {})
        valid_groups = set(groups.keys())
        valid_skills = {s["id"] for s in skills}

        # Normalize group IDs: lowercase, strip, underscores -> hyphens
        def normalize_gid(gid):
            normed = gid.strip().lower().replace("_", "-")
            if normed in valid_groups:
                return normed
            return gid  # return original if normalization doesn't help

        return {sid: normalize_gid(gid)
                for sid, gid in raw.items()
                if sid in valid_skills and normalize_gid(gid) in valid_groups}

    def _batched_classify_skills(self, skills: list[dict], groups: dict,
                                  batch_size: int, verbose: bool = False) -> dict:
        """Parallel batched assignment. All batches use the same groups."""
        ordered_skills = self._sorted_skills(skills)
        batches = [ordered_skills[i:i+batch_size] for i in range(0, len(ordered_skills), batch_size)]
        all_assignments = {}
        executor = self._executor
        if executor is None:
            # Fallback: no shared executor available (shouldn't happen in normal flow)
            for batch in batches:
                try:
                    all_assignments.update(self._classify_skills_single(batch, groups, verbose))
                except Exception as e:
                    console.print(f"[red]Classification batch failed: {e}[/red]")
            return all_assignments
        futures = {
            executor.submit(self._classify_skills_single, batch, groups, verbose): i
            for i, batch in enumerate(batches)
        }
        for future in as_completed(futures):
            try:
                all_assignments.update(future.result())
            except Exception as e:
                console.print(f"[red]Classification batch failed: {e}[/red]")
        return all_assignments

    def _validate_and_recover(self, skills: list[dict], groups: dict,
                               assignments: dict, verbose: bool = False) -> dict:
        """Validate assignments, retry missing, fallback remaining to largest group."""
        skill_ids = {s["id"] for s in skills}
        assigned_ids = set(assignments.keys())
        missing = skill_ids - assigned_ids

        if not missing:
            return assignments

        # 100% failure: don't retry, return empty to let caller handle as grouping failure
        if not assignments:
            console.print(Panel(
                f"[bold red]Classification returned 0 assignments for {len(skills)} skills.[/bold red]",
                title="[bold red]Classification Failed[/bold red]",
                border_style="red",
            ))
            return assignments  # empty dict -> caller treats as grouping failure

        # Warn when >30% missing (even if retry will fix it)
        if len(missing) / len(skills) > 0.3:
            console.print(f"[yellow]  Warning: {len(missing)}/{len(skills)} skills unassigned before retry[/yellow]")

        # Retry unassigned (only if <= 50% missing)
        if len(missing) <= len(skills) * 0.5:
            missing_skills = self._sorted_skills([s for s in skills if s["id"] in missing])
            console.print(f"[yellow]  Retrying {len(missing)} unassigned skills...[/yellow]")
            retry = self._classify_skills_single(missing_skills, groups, verbose, is_retry=True)
            assignments.update(retry)
            missing = skill_ids - set(assignments.keys())

        # Final fallback: largest group
        if missing:
            largest = max(groups, key=lambda g: sum(1 for v in assignments.values() if v == g))
            for sid in missing:
                assignments[sid] = largest
            if len(missing) / len(skills) > 0.1:
                console.print(Panel(
                    f"[bold red]{len(missing)}/{len(skills)} skills unassigned after retry, "
                    f"forced into '{largest}'[/bold red]",
                    title="[bold red]Classification Recovery[/bold red]",
                    border_style="red",
                ))

        return assignments

    def _discover_groups(self, skills: list[dict], parent_context: Optional[dict],
                          verbose: bool = False) -> dict:
        """Phase 1: Discover group definitions from skills (no assignment)."""
        if parent_context:
            context_section = (
                f'## Parent Context\n'
                f'You are creating sub-categories under "{parent_context["name"]}": '
                f'{parent_context["description"]}\n'
                f'Ensure sub-categories are coherent with this parent context.'
            )
        else:
            context_section = "## Context\nYou are creating top-level categories for all skills."

        min_groups = max(2, self.config.branching_factor - 3)
        max_groups = self.config.branching_factor + 2
        skills_list = self._format_skills_list(skills)

        prompt = GROUP_DISCOVERY_PROMPT.format(
            count=len(skills),
            context_section=context_section,
            skills_list=skills_list,
            min_groups=min_groups,
            max_groups=max_groups,
        )
        result = self._call_llm_json(prompt)
        groups = result.get("groups", {})
        # Return only definitions (name + description), strip any skill_ids
        return {
            gid: {"name": g.get("name", gid), "description": g.get("description", "")}
            for gid, g in self._iter_group_items(groups)
        }

    def _merge_group_definitions(self, all_group_defs: list[dict], verbose: bool = False) -> dict:
        """Merge group definitions from multiple discovery samples. No skill IDs involved."""
        if verbose:
            console.print(f"[cyan]    Merging group definitions from {len(all_group_defs)} samples[/cyan]")

        all_groups_text = []
        for i, group_defs in enumerate(all_group_defs):
            lines = [f"### Sample {i+1}"]
            for gid, gdata in self._iter_group_items(group_defs):
                lines.append(f"- {gid}: {gdata.get('name', gid)}")
                if gdata.get('description'):
                    lines.append(f"  {gdata['description']}")
            all_groups_text.append("\n".join(lines))

        min_groups = max(2, self.config.branching_factor - 3)
        max_groups = self.config.branching_factor + 2
        prompt = GROUP_MERGE_PROMPT.format(
            all_groups="\n\n".join(all_groups_text),
            min_groups=min_groups, max_groups=max_groups)
        result = self._call_llm_json(prompt)

        # Extract unified group definitions (no skill_ids to remap)
        canonical = result.get("canonical_groups", {})
        return {
            gid: {"name": g.get("name", gid), "description": g.get("description", "")}
            for gid, g in self._iter_group_items(canonical)
        }

    # =========================================================================
    # Skill splitting (recursive layer)
    # =========================================================================

    def _split_skills(
        self,
        skills: list[dict],
        parent_context: Optional[dict],
        verbose: bool = False,
    ) -> dict:
        """Split skills into groups. Auto-batches for large sets."""
        batch_size = self._auto_batch_size()
        if len(skills) > batch_size:
            return self._batched_split_skills(skills, parent_context, batch_size, verbose)
        return self._split_skills_single(skills, parent_context, verbose)

    def _split_skills_single(
        self,
        skills: list[dict],
        parent_context: Optional[dict],
        verbose: bool = False,
    ) -> dict:
        """Split skills into groups using two-phase approach: discover groups then classify."""
        # Phase 1: Discover groups (output-light, ~300 tokens)
        groups = self._discover_groups(skills, parent_context, verbose)
        if not groups:
            return {}

        # Phase 2: Classify (output-light, flat mapping)
        assignments = self._classify_skills(skills, groups, verbose)
        assignments = self._validate_and_recover(skills, groups, assignments, verbose)

        return self._build_groups_from_assignments(groups, assignments)

    def _batched_split_skills(self, skills, parent_context, batch_size, verbose=False):
        """Split large skill set: multi-sample discovery + definition merge + parallel assignment."""
        if verbose:
            console.print(f"[cyan]  Batched split: {len(skills)} skills, batch_size={batch_size}[/cyan]")

        # Phase 1: Discover groups from sampled subsets
        if len(skills) <= batch_size:
            # Single sample covers all skills
            groups = self._discover_groups(skills, parent_context, verbose)
        else:
            # Multiple samples -> discover independently -> merge definitions
            shuffled = self._sorted_skills(skills)
            if self._deterministic_prompts:
                rng = random.Random(self._sampling_seed(parent_context, len(skills)))
                rng.shuffle(shuffled)
            else:
                random.shuffle(shuffled)
            samples = [shuffled[i:i+batch_size] for i in range(0, len(shuffled), batch_size)]
            # Cap discovery rounds: up to 5 for better coverage (parallel, same wall-clock)
            discovery_samples = samples[:min(5, len(samples))]

            all_group_defs = []
            executor = self._executor
            if executor is None:
                # Fallback: no shared executor available
                for sample in discovery_samples:
                    try:
                        result = self._discover_groups(sample, parent_context, verbose)
                        if result:
                            all_group_defs.append(result)
                    except Exception as e:
                        console.print(f"[red]Discovery batch failed: {e}[/red]")
            else:
                futures = {
                    executor.submit(self._discover_groups, sample, parent_context, verbose): i
                    for i, sample in enumerate(discovery_samples)
                }
                indexed_group_defs = []
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            indexed_group_defs.append((futures[future], result))
                    except Exception as e:
                        console.print(f"[red]Discovery batch failed: {e}[/red]")
                indexed_group_defs.sort(key=lambda item: item[0])
                all_group_defs = [result for _, result in indexed_group_defs]

            if not all_group_defs:
                return {}
            if len(all_group_defs) == 1:
                groups = all_group_defs[0]
            else:
                # Merge group DEFINITIONS only (lightweight, no skill IDs involved)
                groups = self._merge_group_definitions(all_group_defs, verbose)

        if not groups:
            return {}

        # Phase 2: All skills assign to SAME unified groups (parallel batched)
        assignments = self._classify_skills(skills, groups, verbose)
        assignments = self._validate_and_recover(skills, groups, assignments, verbose)

        return self._build_groups_from_assignments(groups, assignments)

    # =========================================================================
    # Helper methods
    # =========================================================================

    def _call_llm(self, prompt: str, is_retry: bool = False) -> str:
        """Call LLM and return response. Uses semaphore to limit concurrency and circuit breaker on consecutive failures."""
        cfg = get_config()
        mcfg = cfg.manager_config()
        max_tokens = self._get_max_output_tokens()
        prompt_fingerprint = self._prompt_fingerprint(prompt)
        with self._counter_lock:
            self._llm_calls += 1
            if is_retry:
                self._retry_calls += 1
            if self._cache_observability:
                self._prompt_fingerprints.add(prompt_fingerprint)
            if self._progress and self._progress_task is not None:
                self._progress.update(self._progress_task, llm=self._llm_calls)
        try:
            with self._llm_semaphore:
                response = litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    api_key=self.api_key,
                    api_base=self.base_url,
                    max_tokens=max_tokens,
                    caching=mcfg.build.caching,
                    num_retries=mcfg.build.num_retries,
                    timeout=mcfg.build.timeout,
                )
            cache_hit = self._extract_cache_hit(response) if self._cache_observability else None
            # Detect output truncation
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                self._thread_local.truncated = True
                console.print(Panel(
                    "[bold red]OUTPUT TRUNCATED![/bold red]\n"
                    f"The LLM response was cut off at {max_tokens} tokens (finish_reason='length').\n"
                    "This will cause incomplete JSON parsing and skill loss.\n"
                    "Consider reducing batch size or increasing max_tokens.",
                    title="[bold red]Truncation Warning[/bold red]",
                    border_style="red",
                ))
            else:
                self._thread_local.truncated = False
            # Reset consecutive failure counter on success
            with self._counter_lock:
                self._consecutive_failures = 0
                if self._cache_observability:
                    self._record_cache_observation(cache_hit)
            return response.choices[0].message.content or "{}"
        except litellm.AuthenticationError:
            console.print("[red]Authentication failed - check API key[/red]")
            raise
        except litellm.ContextWindowExceededError as e:
            console.print(f"[red]Context window exceeded: {e}[/red]")
            # Reduce batch size for future calls
            if self._batch_size_cache and self._batch_size_cache > 50:
                self._batch_size_cache = max(50, self._batch_size_cache // 2)
                console.print(f"[yellow]Reduced batch size to {self._batch_size_cache}[/yellow]")
            with self._counter_lock:
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
                    raise RuntimeError(f"Circuit breaker: {self._consecutive_failures} consecutive LLM failures")
            return "{}"
        except Exception as e:
            console.print(f"[red]LLM call failed: {e}[/red]")
            with self._counter_lock:
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
                    raise RuntimeError(f"Circuit breaker: {self._consecutive_failures} consecutive LLM failures")
            return "{}"

    def _call_llm_json(self, prompt: str, max_retries: int = 3, is_retry: bool = False) -> dict:
        """Call LLM expecting a JSON dict response, with retry on format errors."""
        for attempt in range(max_retries):
            self._thread_local.truncated = False
            response = self._call_llm(prompt, is_retry=is_retry or attempt > 0)
            result = parse_json_from_response(response, default={})
            if isinstance(result, dict):
                return result
            # Don't retry if output was truncated (retrying won't help)
            if getattr(self._thread_local, "truncated", False):
                console.print("[yellow]Skipping retry: output was truncated[/yellow]")
                return {}
            console.print(
                f"[yellow]LLM returned {type(result).__name__} instead of dict "
                f"(attempt {attempt + 1}/{max_retries}), retrying...[/yellow]"
            )
        console.print("[red]All retries exhausted, returning empty dict[/red]")
        return {}

    def _format_skills_list(self, skills: list[dict]) -> str:
        """Format skills list for prompt."""
        lines = []
        for skill in self._sorted_skills(skills):
            desc = skill.get("description", "")
            if len(desc) > SKILL_DESCRIPTION_MAX_LENGTH:
                desc = desc[:SKILL_DESCRIPTION_MAX_LENGTH] + "..."
            lines.append(f"- {skill['id']}: {skill.get('name', skill['id'])}")
            if desc:
                lines.append(f"  {desc}")
        return "\n".join(lines)

    def _tree_to_dict(self, tree: TreeNode) -> dict:
        """Convert TreeNode to dict format for YAML (supports arbitrary depth)."""
        return self._node_to_dict(tree)

    def _node_to_dict(self, node: TreeNode) -> dict:
        """Recursively convert a node to dict."""
        result = {
            "id": node.id,
            "name": node.name,
            "description": node.description,
        }

        if node.children:
            result["children"] = [self._node_to_dict(child) for child in node.children]

        if node.skills:
            result["skills"] = [s.to_dict() for s in node.skills]

        return result

    def _write_yaml(self, tree_dict: dict) -> None:
        """Write tree to YAML file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            yaml.dump(
                tree_dict,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )

    def _print_tree(self, tree_dict: dict) -> None:
        """Print tree structure using rich (supports arbitrary depth)."""
        total_skills = self._count_skills_in_dict(tree_dict)
        rich_tree = RichTree(f"[bold]{tree_dict.get('name', 'Skill Tree')}[/bold] ({total_skills} skills)")

        for child in tree_dict.get("children", []):
            self._add_node_to_rich_tree(rich_tree, child)

        console.print(rich_tree)

    def _add_node_to_rich_tree(self, parent_branch, node_dict: dict) -> None:
        """Recursively add nodes to rich tree."""
        node_skills = self._count_skills_in_dict(node_dict)
        node_id = node_dict.get("id", "unknown")

        # Color based on depth (alternating)
        has_children = bool(node_dict.get("children"))
        if has_children:
            label = f"[yellow]{node_id}[/yellow] ({node_skills} skills)"
        else:
            label = f"[green]{node_id}[/green] ({node_skills} skills)"

        branch = parent_branch.add(label)

        # Add children recursively
        for child in node_dict.get("children", []):
            self._add_node_to_rich_tree(branch, child)

        # Add skills (leaf node)
        skills = node_dict.get("skills", [])
        for skill in skills[:3]:
            branch.add(f"[blue]{skill['id']}[/blue]")
        if len(skills) > 3:
            branch.add(f"[dim]... +{len(skills) - 3} more[/dim]")

    def _count_skills_in_dict(self, node_dict: dict) -> int:
        """Recursively count skills in a node dict."""
        count = len(node_dict.get("skills", []))
        for child in node_dict.get("children", []):
            count += self._count_skills_in_dict(child)
        return count


# Convenience function
def build_tree(
    skills_dir: Path | str | None = None,
    output_path: Path | str | None = None,
    verbose: bool = False,
    show_tree: bool = True,
) -> dict:
    """Build capability tree."""
    builder = TreeBuilder(skills_dir, output_path)
    return builder.build(verbose=verbose, show_tree=show_tree)

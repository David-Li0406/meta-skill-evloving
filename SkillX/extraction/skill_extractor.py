"""Skill extraction from trajectories.

Supports two extraction modes:
1. FunctionalSkillExtractor: Step-based extraction (AppWorld/BFCL style)
2. AtomicSkillExtractor: Tool-based extraction with omission detection (τ²-Bench style)
"""

import re
import json
import logging
from typing import Dict, Optional, List, Any, Set
from collections import defaultdict

from .base import BaseSkillExtractor
from ..prompts.registry import PromptRegistry
from ..core.skill import Skill, SkillMetadata

logger = logging.getLogger(__name__)


class FunctionalSkillExtractor(BaseSkillExtractor):
    """
    Extract functional skills based on plan steps.

    For each step in the plan, extracts a modular, reusable skill
    with Python-like implementation code.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        max_retries: int = 5,
        verbose: bool = True
    ):
        super().__init__(llm, benchmark, verbose=verbose)
        self.max_retries = max_retries

    def get_skill_type(self) -> str:
        return "functional"

    def get_prompt(self) -> str:
        return PromptRegistry.get("skill_extraction", self.benchmark)

    def _extract_skills_from_response(self, text: str) -> Optional[List[Dict]]:
        """Extract skills JSON from response."""
        # Try ```json first
        match = re.search(r"```json(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error: {e}")

        # Fallback: try ``` without json tag
        match = re.search(r"```(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError:
                pass

        # Fallback: try to find JSON array directly
        match = re.search(r"\[\s*\{.*?\}\s*\]", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(0))
                return skills
            except json.JSONDecodeError:
                pass

        if self.verbose:
            logger.warning("No valid skills JSON found in response")
            # Log first 500 chars of response for debugging
            logger.debug(f"Response preview: {text[:500]}...")
        return None

    async def extract(
        self,
        item: Dict,
        **kwargs
    ) -> Optional[Dict]:
        """
        Extract functional skills from a trajectory item.

        Args:
            item: Dictionary with trajectory and plan information

        Returns:
            Item with added skills metadata
        """
        user_task = item.get("user_task", "")
        successful_trajectory = item.get("successful_trajectory", item.get("trajectory", []))
        failed_trajectory = item.get("failed_trajectory")
        plan = item.get("plan", "")
        # Handle exp_metadata being a list or dict
        exp_metadata = item.get("exp_metadata", {})
        if isinstance(exp_metadata, dict):
            skill_library = exp_metadata.get("skills", [])
        else:
            skill_library = []

        # Parse plan steps - match original behavior: split by "#" and filter by "api"
        raw_steps = plan.split("#")
        plan_steps = []
        for step in raw_steps:
            step = step.strip()
            if len(step) >= 5 and "api" in step.lower():
                plan_steps.append(step)

        if not plan_steps:
            # Fallback: try newline-based parsing
            plan_steps = [
                line.strip() for line in plan.split("\n")
                if line.strip().startswith("# step") or line.strip().startswith("#")
            ]

        if not plan_steps:
            logger.warning(f"No plan steps found in plan: {plan[:200]}...")
            return None

        if self.verbose:
            logger.info(f"Found {len(plan_steps)} plan steps")

        plan_step_metadata = {}

        for step in plan_steps:
            if self.verbose:
                logger.info(f"Extracting skill for step: {step[:50]}...")

            # Build message with optional failed_trajectory (match original behavior)
            if failed_trajectory:
                messages = [
                    ("system", self.get_prompt()),
                    ("human", (
                        f"# User task: {user_task}\n\n"
                        f"# A Successful Trajectory: {successful_trajectory}\n\n"
                        f"# A Failed Trajectory: {failed_trajectory}\n\n"
                        f"# Skill Library: {skill_library}\n\n"
                        f"# Specific step: {step}"
                    ))
                ]
            else:
                messages = [
                    ("system", self.get_prompt()),
                    ("human", (
                        f"# User task: {user_task}\n\n"
                        f"# A Successful Trajectory: {successful_trajectory}\n\n"
                        f"# Skill Library: {skill_library}\n\n"
                        f"# Specific step: {step}"
                    ))
                ]

            retry = 0
            while retry < self.max_retries:
                try:
                    response = await self.llm.ainvoke(
                        messages=messages,
                        regex_extractor=self._extract_skills_from_response,
                        **kwargs
                    )

                    skills = self._extract_skills_from_response(response)

                    if skills:
                        plan_step_metadata[step] = skills
                        # Update skill library for next iterations
                        for skill_item in skills:
                            if skill_item.get("option") in ["add", "modify"]:
                                if "skill" in skill_item:
                                    skill_library.append(skill_item["skill"])
                        break

                except Exception as e:
                    retry += 1
                    logger.error(
                        f"Error extracting skill: {e}; retry {retry}/{self.max_retries}"
                    )

        result = item.copy()
        result["plan_step_metadata"] = plan_step_metadata
        return result


class AtomicSkillExtractor(BaseSkillExtractor):
    """
    Extract atomic skills based on tool omissions.

    For each tool used in the trajectory, checks if it exists in the skill library.
    If missing (omission), extracts a new atomic skill for that tool.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "tau2bench",
        domain: str = "airline",
        existing_skills: Optional[Dict[str, Dict]] = None,
        max_retries: int = 5,
        verbose: bool = True
    ):
        super().__init__(llm, benchmark, verbose=verbose)
        self.domain = domain
        self.existing_skills = existing_skills or {}
        self.max_retries = max_retries

    def get_skill_type(self) -> str:
        return "atomic"

    def get_prompt(self) -> str:
        return PromptRegistry.get("skill_extraction", "atomic")

    def _extract_skills_from_response(self, text: str) -> Optional[List[Dict]]:
        """Extract skills JSON from response."""
        # Try ```json first
        match = re.search(r"```json(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error: {e}")

        # Fallback: try ``` without json tag
        match = re.search(r"```(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError:
                pass

        # Fallback: try to find JSON array directly
        match = re.search(r"\[\s*\{.*?\}\s*\]", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(0))
                return skills
            except json.JSONDecodeError:
                pass

        if self.verbose:
            logger.warning("No valid skills JSON found in response")
            # Log first 500 chars of response for debugging
            logger.debug(f"Response preview: {text[:500]}...")
        return None

    def _collect_tools_from_trajectory(self, trajectory: List[Dict]) -> Set[str]:
        """Collect all tools used in a trajectory.

        Supports two formats:
        1. Standard tool_calls field (OpenAI function calling format)
        2. AppWorld format: apis.xxx.xxx embedded in content
        """
        tools = set()
        for step in trajectory:
            # Method 1: Check tool_calls field (standard format)
            if step.get("role") == "assistant" and step.get("tool_calls"):
                for tool_call in step["tool_calls"]:
                    tools.add(tool_call["name"])

            # Method 2: Extract from content (AppWorld format: apis.xxx.xxx)
            content = step.get("content", "")
            if content and isinstance(content, str):
                # Match patterns like apis.spotify.login, apis.venmo.create_transaction
                api_pattern = r'apis\.(\w+)\.(\w+)'
                matches = re.findall(api_pattern, content)
                for app, method in matches:
                    tools.add(f"apis.{app}.{method}")
        return tools

    def _get_missing_tools(self, used_tools: Set[str]) -> Set[str]:
        """
        Identify tools that are missing from the existing skill library.

        This is the core of omission-based extraction.
        """
        existing_tool_names = set(self.existing_skills.keys())
        return used_tools - existing_tool_names

    async def extract(
        self,
        item: Dict,
        **kwargs
    ) -> Optional[Dict]:
        """
        Extract atomic skills from a trajectory item.

        For each tool used in the trajectory:
        1. Check if it exists in skill library
        2. If missing, extract new skill (add)
        3. If exists, consider modify or keep

        Args:
            item: Dictionary with trajectory information

        Returns:
            Item with added skill extraction metadata
        """
        user_task = item.get("user_task", "")
        successful_trajectory = item.get(
            "successful_trajectory",
            item.get("trajectory", [])
        )
        failed_trajectory = item.get("failed_trajectory")

        # Get skill library context (handle exp_metadata being a list or dict)
        exp_metadata = item.get("exp_metadata", {})
        if isinstance(exp_metadata, dict):
            temp_skill_library = exp_metadata.get("skills", [])
        else:
            temp_skill_library = []

        # Collect all tools used in successful trajectory
        all_tools = self._collect_tools_from_trajectory(successful_trajectory)

        if self.verbose:
            logger.info(f"Found {len(all_tools)} tools in trajectory")

        # Identify missing tools (omissions)
        missing_tools = self._get_missing_tools(all_tools)

        if self.verbose and missing_tools:
            logger.info(f"Missing tools (omissions): {missing_tools}")

        plan_step_metadata = {}

        # Extract skill for each tool
        for tool in all_tools:
            # Build skill library context for this tool
            skill_library = []
            if tool in self.existing_skills:
                skill_library.append(self.existing_skills[tool])

            if self.verbose:
                logger.info(f"Extracting skill for tool: {tool}")

            # Build messages
            if failed_trajectory:
                messages = [
                    ("system", self.get_prompt()),
                    ("human", (
                        f"# User task: {user_task}\n\n"
                        f"# A Successful Trajectory: {successful_trajectory}\n\n"
                        f"# A Failed Trajectory: {failed_trajectory}\n\n"
                        f"# Skill Library: {skill_library}\n\n"
                        f"# Specific Tool: {tool}"
                    ))
                ]
            else:
                messages = [
                    ("system", self.get_prompt()),
                    ("human", (
                        f"# User task: {user_task}\n\n"
                        f"# A Successful Trajectory: {successful_trajectory}\n\n"
                        f"# Skill Library: {skill_library}\n\n"
                        f"# Specific Tool: {tool}"
                    ))
                ]

            retry = 0
            while retry < self.max_retries:
                try:
                    response = await self.llm.ainvoke(
                        messages=messages,
                        regex_extractor=self._extract_skills_from_response,
                        **kwargs
                    )

                    skills = self._extract_skills_from_response(response)

                    if skills:
                        plan_step_metadata[tool] = skills
                        # Update existing skills for subsequent extractions
                        for skill_item in skills:
                            if skill_item.get("option") in ["add", "modify"]:
                                if "skill" in skill_item:
                                    skill_data = skill_item["skill"]
                                    self.existing_skills[skill_data["name"]] = skill_data
                        break

                except Exception as e:
                    retry += 1
                    logger.error(
                        f"Error extracting skill for {tool}: {e}; "
                        f"retry {retry}/{self.max_retries}"
                    )

        result = item.copy()
        result["plan_step_metadata"] = plan_step_metadata
        result["all_tools_used"] = list(all_tools)
        result["missing_tools"] = list(missing_tools)
        return result


class HybridSkillExtractor(BaseSkillExtractor):
    """
    Hybrid extractor: Functional skills first, then atomic skills for missing APIs.

    This implements the SkillX paper's multi-level skill extraction:
    1. Extract functional skills based on plan steps
    2. Detect tools used in trajectory but not covered by functional skills
    3. Extract atomic skills for missing tools (API omissions)

    This ensures comprehensive coverage of all tools used in successful trajectories.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        domain: str = "",
        existing_skills: Optional[Dict[str, Dict]] = None,
        max_retries: int = 5,
        atomic_mode: str = "omission",
        verbose: bool = True
    ):
        """
        Initialize hybrid skill extractor.

        Args:
            llm: LLM instance
            benchmark: Benchmark name
            domain: Domain name
            existing_skills: Existing skills for atomic extraction
            max_retries: Maximum retries for LLM calls
            atomic_mode: Mode for atomic skill extraction:
                - "omission": Only extract atomic skills for tools not covered by functional skills (default)
                - "all": Extract atomic skills for all tools used in trajectory
            verbose: Whether to output verbose logs
        """
        super().__init__(llm, benchmark, verbose=verbose)
        self.domain = domain
        self.existing_skills = existing_skills or {}
        self.max_retries = max_retries
        self.atomic_mode = atomic_mode

        # Initialize sub-extractors
        self.functional_extractor = FunctionalSkillExtractor(
            llm, benchmark, max_retries, verbose
        )
        self.atomic_extractor = AtomicSkillExtractor(
            llm, benchmark, domain, existing_skills, max_retries, verbose
        )

    def get_skill_type(self) -> str:
        return "hybrid"

    def get_prompt(self) -> str:
        return PromptRegistry.get("skill_extraction", self.benchmark)

    def _extract_skills_from_response(self, text: str) -> Optional[List[Dict]]:
        """Extract skills JSON from response."""
        # Try ```json first
        match = re.search(r"```json(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError as e:
                logger.warning(f"JSON decode error: {e}")

        # Fallback: try ``` without json tag
        match = re.search(r"```(.*?)```", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(1).strip())
                return skills
            except json.JSONDecodeError:
                pass

        # Fallback: try to find JSON array directly
        match = re.search(r"\[\s*\{.*?\}\s*\]", text, flags=re.S)
        if match:
            try:
                skills = json.loads(match.group(0))
                return skills
            except json.JSONDecodeError:
                pass

        if self.verbose:
            logger.warning("No valid skills JSON found in response")
            # Log first 500 chars of response for debugging
            logger.debug(f"Response preview: {text[:500]}...")
        return None

    def _collect_tools_from_trajectory(self, trajectory: List[Dict]) -> Set[str]:
        """Collect all tools used in a trajectory.

        Supports two formats:
        1. Standard tool_calls field (OpenAI function calling format)
        2. AppWorld format: apis.xxx.xxx embedded in content
        """
        tools = set()
        for step in trajectory:
            # Method 1: Check tool_calls field (standard format)
            if step.get("role") == "assistant" and step.get("tool_calls"):
                for tool_call in step["tool_calls"]:
                    tools.add(tool_call["name"])

            # Method 2: Extract from content (AppWorld format: apis.xxx.xxx)
            content = step.get("content", "")
            if content and isinstance(content, str):
                # Match patterns like apis.spotify.login, apis.venmo.create_transaction
                api_pattern = r'apis\.(\w+)\.(\w+)'
                matches = re.findall(api_pattern, content)
                for app, method in matches:
                    tools.add(f"apis.{app}.{method}")
        return tools

    def _collect_tools_from_skills(self, skills: List[Dict]) -> Set[str]:
        """Collect tools covered by extracted skills."""
        covered_tools = set()
        for skill_item in skills:
            skill_data = skill_item.get("skill", skill_item)
            covered_tools.update(skill_data.get("tools", []))
        return covered_tools

    def detect_missing_tools(
        self,
        trajectory: List[Dict],
        extracted_skills: List[Dict]
    ) -> Set[str]:
        """
        Detect tools used in trajectory but not covered by extracted skills.

        This is the core of omission detection - finding API gaps.

        Args:
            trajectory: The trajectory containing tool calls
            extracted_skills: List of extracted functional skills

        Returns:
            Set of tool names that are missing from the skill library
        """
        trajectory_tools = self._collect_tools_from_trajectory(trajectory)
        covered_tools = self._collect_tools_from_skills(extracted_skills)

        missing = trajectory_tools - covered_tools

        if self.verbose and missing:
            logger.info(f"Detected {len(missing)} missing tools: {missing}")

        return missing

    async def extract(
        self,
        item: Dict,
        **kwargs
    ) -> Optional[Dict]:
        """
        Extract skills using hybrid approach.

        Flow:
        1. Extract functional skills based on plan steps
        2. Detect missing tools (API omissions)
        3. Extract atomic skills for missing tools

        Args:
            item: Dictionary with trajectory and plan information

        Returns:
            Item with combined functional and atomic skills metadata
        """
        user_task = item.get("user_task", "")
        trajectory = item.get("successful_trajectory", item.get("trajectory", []))
        plan = item.get("plan", "")

        result = item.copy()
        result["plan_step_metadata"] = {}
        result["atomic_skill_metadata"] = {}
        result["all_tools_used"] = []
        result["missing_tools"] = []

        # Step 1: Extract functional skills (if plan exists)
        functional_skills = []
        if plan:
            if self.verbose:
                logger.info("Step 1: Extracting functional skills from plan steps...")

            functional_result = await self.functional_extractor.extract(item, **kwargs)

            if functional_result and "plan_step_metadata" in functional_result:
                result["plan_step_metadata"] = functional_result["plan_step_metadata"]

                # Collect all functional skills
                for step_skills in functional_result["plan_step_metadata"].values():
                    for skill_item in step_skills:
                        if skill_item.get("option") in ["add", "modify"]:
                            functional_skills.append(skill_item)

        if self.verbose:
            logger.info(f"Extracted {len(functional_skills)} functional skills")

        # Step 2: Detect tools for atomic extraction
        all_tools = self._collect_tools_from_trajectory(trajectory)
        result["all_tools_used"] = list(all_tools)

        if self.atomic_mode == "all":
            # Extract atomic skills for ALL tools used in trajectory
            tools_for_atomic = all_tools
            missing_tools = set()
        else:
            # omission mode: Only extract for tools not covered by functional skills
            missing_tools = self.detect_missing_tools(trajectory, functional_skills)
            tools_for_atomic = missing_tools

        result["missing_tools"] = list(missing_tools)

        # Step 3: Extract atomic skills for target tools
        if tools_for_atomic:
            if self.verbose:
                logger.info(f"Step 3: Extracting atomic skills for {len(tools_for_atomic)} tools (mode={self.atomic_mode})...")

            for tool in tools_for_atomic:
                # Build skill library context for this tool
                skill_library = []
                if tool in self.existing_skills:
                    skill_library.append(self.existing_skills[tool])

                if self.verbose:
                    logger.info(f"Extracting atomic skill for tool: {tool}")

                # Build messages for atomic extraction
                failed_trajectory = item.get("failed_trajectory")

                if failed_trajectory:
                    messages = [
                        ("system", PromptRegistry.get("skill_extraction", "atomic")),
                        ("human", (
                            f"# User task: {user_task}\n\n"
                            f"# A Successful Trajectory: {trajectory}\n\n"
                            f"# A Failed Trajectory: {failed_trajectory}\n\n"
                            f"# Skill Library: {skill_library}\n\n"
                            f"# Specific Tool: {tool}"
                        ))
                    ]
                else:
                    messages = [
                        ("system", PromptRegistry.get("skill_extraction", "atomic")),
                        ("human", (
                            f"# User task: {user_task}\n\n"
                            f"# A Successful Trajectory: {trajectory}\n\n"
                            f"# Skill Library: {skill_library}\n\n"
                            f"# Specific Tool: {tool}"
                        ))
                    ]

                retry = 0
                while retry < self.max_retries:
                    try:
                        response = await self.llm.ainvoke(
                            messages=messages,
                            regex_extractor=self._extract_skills_from_response,
                            **kwargs
                        )

                        skills = self._extract_skills_from_response(response)

                        if skills:
                            result["atomic_skill_metadata"][tool] = skills
                            # Update existing skills for subsequent extractions
                            for skill_item in skills:
                                # Skip non-dict items (defensive check)
                                if not isinstance(skill_item, dict):
                                    logger.warning(f"Skipping non-dict skill_item: {type(skill_item)}")
                                    continue
                                if skill_item.get("option") in ["add", "modify"]:
                                    if "skill" in skill_item:
                                        skill_data = skill_item["skill"]
                                        # Ensure skill_data is a dict with "name" key
                                        if isinstance(skill_data, dict) and "name" in skill_data:
                                            self.existing_skills[skill_data["name"]] = skill_data
                                        else:
                                            logger.warning(f"Invalid skill_data format: {type(skill_data)}")
                            break

                    except Exception as e:
                        retry += 1
                        logger.error(
                            f"Error extracting atomic skill for {tool}: {e}; "
                            f"retry {retry}/{self.max_retries}"
                        )

        # Combine metadata
        if self.verbose:
            func_count = len(functional_skills)
            atomic_count = sum(
                len(skills) for skills in result["atomic_skill_metadata"].values()
            )
            logger.info(
                f"Hybrid extraction complete: {func_count} functional skills, "
                f"{atomic_count} atomic skills"
            )

        return result


def collect_skills_from_results(
    extraction_results: List[Dict],
    skill_type: str = "functional"
) -> List[Dict]:
    """
    Collect all extracted skills from extraction results.

    Args:
        extraction_results: List of extraction result dictionaries
        skill_type: Type of skills ('functional', 'atomic', or 'hybrid')

    Returns:
        List of skill dictionaries with option and skill data
    """
    all_skills = []
    functional_count = 0
    atomic_count = 0

    for result in extraction_results:
        if not result:
            continue

        # Collect functional skills from plan_step_metadata
        if "plan_step_metadata" in result:
            for key, skill_items in result["plan_step_metadata"].items():
                for item in skill_items:
                    # Skip if item is not a dict (e.g., string from malformed LLM response)
                    if not isinstance(item, dict):
                        logger.warning(f"Skipping non-dict skill item: {type(item)}")
                        continue
                    try:
                        if item.get("option") == "add":
                            item["skill_type"] = "functional"
                            all_skills.append(item)
                            functional_count += 1
                        elif item.get("option") == "modify":
                            # Remove original skill and add modified version
                            all_skills = [
                                s for s in all_skills
                                if s.get("skill", {}).get("name") != item.get("modified_from")
                            ]
                            item["skill_type"] = "functional"
                            all_skills.append(item)
                            functional_count += 1
                    except Exception as e:
                        logger.error(f"Error processing functional skill item: {e}")

        # Collect atomic skills from atomic_skill_metadata (for hybrid extraction)
        if "atomic_skill_metadata" in result:
            logger.debug(f"Found atomic_skill_metadata with {len(result['atomic_skill_metadata'])} tools")
            for tool_name, skill_items in result["atomic_skill_metadata"].items():
                logger.debug(f"Tool {tool_name}: {len(skill_items)} skill items")
                for item in skill_items:
                    # Skip if item is not a dict
                    if not isinstance(item, dict):
                        logger.warning(f"Skipping non-dict atomic skill item: {type(item)}")
                        continue
                    try:
                        if item.get("option") == "add":
                            item["skill_type"] = "atomic"
                            item["source_tool"] = tool_name
                            all_skills.append(item)
                            atomic_count += 1
                        elif item.get("option") == "modify":
                            all_skills = [
                                s for s in all_skills
                                if s.get("skill", {}).get("name") != item.get("modified_from")
                            ]
                            item["skill_type"] = "atomic"
                            item["source_tool"] = tool_name
                            all_skills.append(item)
                            atomic_count += 1
                    except Exception as e:
                        logger.error(f"Error processing atomic skill item: {e}")

    logger.info(f"collect_skills_from_results: collected {functional_count} functional, {atomic_count} atomic skills")
    return all_skills


def prepare_skills_for_clustering(
    skills: List[Dict]
) -> List[Dict]:
    """
    Prepare skills for clustering by adding embedding text.

    Args:
        skills: List of skill dictionaries

    Returns:
        List of skills with embedding_text added
    """
    prepared = []
    for item in skills:
        if "skill" not in item:
            continue

        skill = item["skill"]
        prepared_item = item.copy()
        prepared_item["embedding_text"] = (
            f"{skill.get('name', '')}\n"
            f"{skill.get('document', '')}\n"
            f"{skill.get('content', '')}"
        )

        # Clean content - remove return statements for functional skills only.
        # Atomic skill content is narrative/example text where "return" may appear
        # as a normal word (e.g. "does not return anything") and must not be split.
        if item.get("skill_type") != "atomic" and "return" in skill.get("content", ""):
            skill["content"] = skill["content"].split("return")[0].strip()

        prepared.append(prepared_item)

    return prepared

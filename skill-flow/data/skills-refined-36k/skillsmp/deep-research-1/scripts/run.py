#!/usr/bin/env python3
"""
Deep Research - Standalone LLM-based research pipeline

이 스크립트는 독립적으로 실행 가능하며, 심층 리서치 파이프라인을 제공합니다.
Plan → Execute → Report 단계로 구성됩니다.

Usage:
    # 환경 변수 로드 후 실행
    source scripts/load_env.sh
    python run.py "research topic" --depth 3

Example:
    python run.py "AI trends in 2026"
"""

import argparse
import json
import logging
import os
import sys
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Callable, Any, Set, Optional

# Add scripts directory to path for local imports
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import local modules (after sys.path modification)
from search_engine import SearchEngine  # noqa: E402
from scraper import WebScraper  # noqa: E402
from llm_client import llm_complete  # noqa: E402
from env_manager import get_env_manager  # noqa: E402
from dependency_checker import get_dependency_checker  # noqa: E402
from error_handler import get_error_handler  # noqa: E402
from async_scraper import fetch_urls_parallel  # noqa: E402
from source_evaluator import SourceEvaluator  # noqa: E402


# Constants for iterative research
MAX_DEPTH = 5  # Maximum recursion depth
DEFAULT_DEPTH = 5  # Default recursion depth (increased from 3)
DEFAULT_BREADTH = 20  # Default URLs per step (increased from 7)
CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for early exit
MAX_LEARNINGS = 20  # Maximum learnings to keep

# Phase 2 constants
DEFAULT_TOKEN_BUDGET = 100000  # Default token budget
DEFAULT_MIN_TRUST = 0.3  # Default minimum source trust


@dataclass
class TokenBudget:
    """Token budget management for LLM calls.
    
    Tracks token usage and enforces budget limits to control costs.
    """
    total_limit: int = DEFAULT_TOKEN_BUDGET
    used: int = 0
    per_call_limit: int = 10000
    
    def add_usage(self, tokens: int) -> None:
        """Add token usage.
        
        Args:
            tokens: Number of tokens used
        """
        self.used += tokens
    
    def can_continue(self) -> bool:
        """Check if budget allows continuation.
        
        Returns:
            True if under budget, False otherwise
        """
        return self.used < self.total_limit
    
    def remaining(self) -> int:
        """Get remaining token budget.
        
        Returns:
            Remaining tokens
        """
        return max(0, self.total_limit - self.used)
    
    def usage_percent(self) -> float:
        """Get usage as percentage.
        
        Returns:
            Usage percentage (0-100)
        """
        return (self.used / self.total_limit) * 100 if self.total_limit > 0 else 100


@dataclass
class ResearchState:
    """State for iterative deep research.
    
    Tracks the current research context including accumulated learnings,
    exploration directions, and visited URLs for deduplication.
    """
    topic: str
    session_id: str
    depth: int  # Remaining recursion depth
    breadth: int  # URLs per step
    learnings: List[str] = field(default_factory=list)
    directions: List[str] = field(default_factory=list)
    visited_urls: Set[str] = field(default_factory=set)
    all_results: List[Dict] = field(default_factory=list)
    token_budget: Optional[TokenBudget] = None  # Phase 2: Token budget tracking


@dataclass
class AnalysisResult:
    """Result from analyzing research findings.
    
    Contains extracted learnings, new exploration directions,
    and completion assessment.
    """
    learnings: List[str]
    directions: List[str]
    is_complete: bool
    confidence: float  # 0.0 - 1.0


def limit_learnings(learnings: List[str], max_count: int = MAX_LEARNINGS) -> List[str]:
    """Limit learnings to the most recent entries.
    
    Args:
        learnings: List of accumulated learnings
        max_count: Maximum number to keep (default: 20)
        
    Returns:
        Truncated list with most recent learnings
    """
    if len(learnings) <= max_count:
        return learnings
    return learnings[-max_count:]


def create_argument_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI.
    
    Returns:
        Configured ArgumentParser with --breadth, --depth, etc.
    """
    parser = argparse.ArgumentParser(description="Deep Research Tool")
    parser.add_argument("topic", nargs="?", default=None, help="Research topic")
    parser.add_argument("--breadth", type=int, default=None,
                        help="URLs per step (enables iterative mode)")
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH,
                        help="Recursion depth for iterative research (default: 2)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Custom output directory for research cache")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check system readiness without running research")
    
    # Phase 2 options
    parser.add_argument("--parallel", action="store_true",
                        help="Enable parallel URL scraping (faster)")
    parser.add_argument("--token-budget", type=int, default=DEFAULT_TOKEN_BUDGET,
                        help=f"Token budget limit (default: {DEFAULT_TOKEN_BUDGET})")
    parser.add_argument("--min-trust", type=float, default=DEFAULT_MIN_TRUST,
                        help=f"Minimum source trust score (default: {DEFAULT_MIN_TRUST})")
    
    return parser


class ResearchArchive:
    """Manages local storage of research data."""

    def __init__(self, base_dir: str = None):
        """Initialize archive manager.
        
        Args:
            base_dir: Base directory for research cache. 
                      Defaults to ~/.cache/opencode/research
        """
        if base_dir is None:
            # Use user cache directory for global skill
            cache_home = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            self.base_dir = os.path.join(cache_home, "opencode", "research")
        else:
            self.base_dir = os.path.expanduser(base_dir)

        os.makedirs(self.base_dir, exist_ok=True)

    def create_session(self, topic: str) -> str:
        """Create a new research session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic])[:30]

        session_id = f"{timestamp}_{safe_topic}_{topic_hash}"
        session_path = os.path.join(self.base_dir, session_id)

        os.makedirs(session_path, exist_ok=True)
        os.makedirs(os.path.join(session_path, "sources"), exist_ok=True)

        # Save metadata
        meta = {"topic": topic, "created_at": timestamp, "status": "initialized"}
        self._save_json(os.path.join(session_path, "metadata.json"), meta)

        logger.info(f"Created session: {session_id}")
        return session_id

    def save_content(
        self, session_id: str, url: str, content: str, title: str = ""
    ) -> str:
        """Save scraped content."""
        session_path = os.path.join(self.base_dir, session_id)

        url_hash = hashlib.md5(url.encode()).hexdigest()
        filename = f"{url_hash}.md"
        filepath = os.path.join(session_path, "sources", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\nSource: {url}\n\n{content}")

        return filename

    def _save_json(self, path: str, data: Dict):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class DeepResearch:
    """Orchestrates the deep research process."""

    def __init__(
        self, llm_callback: Callable[[str], str], base_dir: str = None
    ):
        """Initialize the researcher."""
        self.llm = llm_callback
        self.engine = SearchEngine()
        self.scraper = WebScraper()
        self.archive = ResearchArchive(base_dir)
        self.source_evaluator = SourceEvaluator()  # Phase 2: Source evaluation

    def create_plan(self, topic: str) -> Dict[str, Any]:
        """Generate a research plan."""
        session_id = self.archive.create_session(topic)
        
        # 현재 시각 메타데이터
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = (
            f"=== Research Request ===\n"
            f"Topic: {topic}\n"
            f"Request Time: {current_time}\n"
            f"Current Date: {current_date}\n"
            f"========================\n\n"
            "Create a research plan. Return ONLY raw JSON:\n"
            '{"steps": [{"query": "search query", "rationale": "reason"}, ...]}\n'
            "Limit to 3-5 steps. Consider the current date for time-sensitive topics."
        )

        logger.info(f"Generating plan for: {topic}")
        response = self.llm(prompt)

        try:
            clean_resp = response.strip()
            if clean_resp.startswith("```"):
                clean_resp = clean_resp.split("\n", 1)[1].rsplit("\n", 1)[0]
            if clean_resp.startswith("json"):
                clean_resp = clean_resp[4:]

            plan_data = json.loads(clean_resp)
            if "steps" not in plan_data:
                raise ValueError("Missing 'steps' key")
        except Exception as e:
            logger.warning(f"Failed to parse plan: {e}, using fallback")
            plan_data = {
                "steps": [
                    {"query": topic, "rationale": "General overview"},
                    {"query": f"{topic} news", "rationale": "Recent updates"},
                    {"query": f"{topic} analysis", "rationale": "Deep analysis"},
                ]
            }

        return {"session_id": session_id, "topic": topic, "plan": plan_data}

    def execute_plan(
        self,
        session_data: Dict[str, Any],
        max_urls_per_step: int = 3,
        parallel: bool = False,
        min_trust: float = 0.0,
    ) -> List[Dict]:
        """Execute the research plan.
        
        Args:
            session_data: Session information and plan
            max_urls_per_step: Maximum URLs to fetch per step
            parallel: Whether to use parallel scraping (Phase 2)
            min_trust: Minimum source trust score (Phase 2)
        """
        session_id = session_data["session_id"]
        steps = session_data["plan"]["steps"]
        results = []

        print(f"\n🔬 Executing research for session: {session_id}")
        if parallel:
            print("   Mode: Parallel scraping enabled 🚀")

        for i, step in enumerate(steps, 1):
            query = step.get("query", "")
            rationale = step.get("rationale", "")

            print(f"\n--- Step {i}/{len(steps)}: {query} ---")
            print(f"Rationale: {rationale}")

            # Search
            # Fetch more results initially to allow for filtering
            search_limit = max_urls_per_step * 2 if min_trust > 0 else max_urls_per_step
            search_results = self.engine.search(query, max_results=search_limit)
            logger.info(f"Found {len(search_results)} links")

            # Filter by trust score (Phase 2)
            urls_to_fetch = []
            titles = {}
            
            for res in search_results:
                url = res["href"]
                title = res["title"]
                
                if min_trust > 0:
                    score = self.source_evaluator.evaluate(url)
                    if score < min_trust:
                        logger.info(f"Skipping low trust source ({score:.2f}): {url}")
                        continue
                
                urls_to_fetch.append(url)
                titles[url] = title
                
                if len(urls_to_fetch) >= max_urls_per_step:
                    break
            
            print(f"   Selected {len(urls_to_fetch)} URLs for processing")

            step_content = []

            # Scrape (Parallel or Sequential)
            if parallel and urls_to_fetch:
                # Phase 2: Parallel scraping
                print(f"  > Parallel fetching {len(urls_to_fetch)} URLs...")
                fetch_results = fetch_urls_parallel(urls_to_fetch)
                
                for res in fetch_results:
                    url = res["url"]
                    content = res["content"]
                    title = titles.get(url, "Unknown")
                    
                    if res["success"] and content:
                        self.archive.save_content(session_id, url, content, title)
                        step_content.append(f"Source: {title} ({url})\n{content[:2000]}...")
                    elif res.get("error"):
                        print(f"    Failed: {url} ({res['error']})")
            else:
                # Phase 1: Sequential scraping
                for url in urls_to_fetch:
                    title = titles.get(url, "Unknown")
                    print(f"  > Fetching: {title[:50]}...")
                    content = self.scraper.fetch_content(url)

                    if content:
                        self.archive.save_content(session_id, url, content, title)
                        step_content.append(f"Source: {title} ({url})\n{content[:2000]}...")
                        time.sleep(1)  # Polite delay

            results.append(
                {
                    "step": i,
                    "query": query,
                    "found_sources": len(step_content),
                    "snippets": step_content,
                }
            )

        print("\n✅ Execution complete.")
        return results

    def generate_report(self, session_data: Dict, results: List[Dict]) -> str:
        """Generate final report."""
        # 현재 시각 메타데이터
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        
        context = f"# Research Topic: {session_data['topic']}\n"
        context += f"## Report Generated: {current_time}\n\n"

        for step in results:
            context += f"## Findings for: {step['query']}\n"
            for snippet in step["snippets"]:
                context += snippet + "\n\n---\n\n"

        prompt = (
            f"=== Report Generation Request ===\n"
            f"Topic: {session_data['topic']}\n"
            f"Generation Time: {current_time}\n"
            f"=================================\n\n"
            "Write a comprehensive research report based on the gathered data.\n"
            "Structure: Executive Summary, Key Findings, Details, Conclusion.\n"
            "Cite sources where possible. Consider the report generation timestamp for context.\n\n"
            f"{context[:15000]}"
        )

        logger.info("Generating report...")
        report = self.llm(prompt)

        # Save report
        report_path = (
            f"{self.archive.base_dir}/{session_data['session_id']}/final_report.md"
        )
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        return report

    def analyze_results(
        self, topic: str, results: List[Dict], existing_learnings: List[str]
    ) -> AnalysisResult:
        """Analyze research results to extract learnings and directions.
        
        Args:
            topic: The original research topic
            results: List of research results from execute_plan
            existing_learnings: Previously accumulated learnings
            
        Returns:
            AnalysisResult with extracted learnings, new directions, and completion status
        """
        # Prepare context from results
        context = ""
        for step_result in results:
            for snippet in step_result.get("snippets", []):
                context += snippet[:1000] + "\n\n"
        
        # Prepare learnings summary
        learnings_summary = "\n".join(f"- {l}" for l in existing_learnings[-10:]) if existing_learnings else "None yet"
        
        prompt = (
            "Analyze the research results and extract:\n"
            "1. Key Learnings: What facts/insights were discovered?\n"
            "2. New Directions: What questions remain unanswered?\n"
            "3. Completeness: Is the original question fully answered?\n\n"
            f"Original Question: {topic}\n"
            f"Previous Learnings:\n{learnings_summary}\n\n"
            f"New Data:\n{context[:10000]}\n\n"
            "Return ONLY raw JSON:\n"
            '{"learnings": ["..."], "directions": ["..."], "is_complete": true/false, "confidence": 0.0-1.0}'
        )
        
        try:
            response = self.llm(prompt)
            clean_resp = response.strip()
            
            # Clean markdown code blocks
            if clean_resp.startswith("```"):
                clean_resp = clean_resp.split("\n", 1)[1].rsplit("\n", 1)[0]
            if clean_resp.startswith("json"):
                clean_resp = clean_resp[4:]
            
            data = json.loads(clean_resp)
            
            return AnalysisResult(
                learnings=data.get("learnings", []),
                directions=data.get("directions", []),
                is_complete=data.get("is_complete", False),
                confidence=float(data.get("confidence", 0.5)),
            )
        except Exception as e:
            logger.warning(f"Failed to parse analysis response: {e}")
            return AnalysisResult(
                learnings=[],
                directions=[],
                is_complete=False,
                confidence=0.0,
            )

    def select_best_direction(self, directions: List[str]) -> Optional[str]:
        """Select the best direction for next research iteration.
        
        For Phase 1, simply returns the first direction.
        Future phases may use LLM to rank directions.
        
        Args:
            directions: List of potential exploration directions
            
        Returns:
            The selected direction or None if list is empty
        """
        if not directions:
            return None
        return directions[0]

    def deep_research(
        self,
        state: ResearchState,
        parallel: bool = False,
        min_trust: float = 0.0
    ) -> ResearchState:
        """Execute iterative deep research.
        
        Recursively explores the topic, accumulating learnings and
        following promising directions until complete or depth exhausted.
        
        Args:
            state: Current research state
            parallel: Whether to use parallel scraping
            min_trust: Minimum source trust score
            
        Returns:
            Updated research state with accumulated results
        """
        # Check token budget (Phase 2)
        if state.token_budget and not state.token_budget.can_continue():
            logger.warning("Token budget exhausted, stopping research early")
            return state

        # Enforce maximum depth
        effective_depth = min(state.depth, MAX_DEPTH)
        
        if effective_depth <= 0:
            logger.info("Depth exhausted, stopping research")
            return state
        
        print(f"\n🔄 Iterative research - Depth remaining: {effective_depth}")
        if state.token_budget:
            print(f"   Token Budget: {state.token_budget.usage_percent():.1f}% used")
        
        # Create and execute plan
        if not state.session_id or state.session_id == "":
            session_data = self.create_plan(state.topic)
            state.session_id = session_data["session_id"]
        else:
            # Use existing session, create new plan based on current direction
            current_topic = state.directions[0] if state.directions else state.topic
            session_data = {
                "session_id": state.session_id,
                "topic": current_topic,
                "plan": {"steps": [
                    {"query": current_topic, "rationale": "Follow-up exploration"}
                ]}
            }
        
        # Execute research with Phase 2 parameters
        results = self.execute_plan(
            session_data,
            max_urls_per_step=state.breadth,
            parallel=parallel,
            min_trust=min_trust
        )
        state.all_results.extend(results)
        
        # Analyze results
        analysis = self.analyze_results(
            topic=state.topic,
            results=results,
            existing_learnings=state.learnings
        )
        
        # Accumulate learnings
        state.learnings.extend(analysis.learnings)
        state.learnings = limit_learnings(state.learnings)
        
        # Check completion
        if analysis.is_complete and analysis.confidence >= CONFIDENCE_THRESHOLD:
            logger.info(f"Research complete with confidence {analysis.confidence:.2f}")
            return state
        
        # Select next direction and recurse
        next_direction = self.select_best_direction(analysis.directions)
        if next_direction:
            state.directions = [next_direction] + analysis.directions[1:]
            state.depth = effective_depth - 1
            return self.deep_research(state, parallel=parallel, min_trust=min_trust)
        
        logger.info("No more directions to explore")
        return state


def check_system_readiness() -> Dict[str, Any]:
    """Check system readiness including API keys, dependencies, and connectivity."""
    env_manager = get_env_manager()
    dep_checker = get_dependency_checker()
    
    print("🔍 Checking system readiness...")
    
    # Check API keys
    api_status = env_manager.get_status_summary()
    print(f"   API Keys: {len(api_status['loaded_keys'])} found")
    
    if not api_status['is_valid']:
        for issue in api_status['issues']:
            print(f"   ⚠️  {issue}")
    
    # Check dependencies
    dep_status = dep_checker.get_dependency_status()
    print(f"   Dependencies: {len(dep_status['available_required'])}/{len(dep_checker.REQUIRED_PACKAGES)} required packages available")
    
    if dep_status['missing_required']:
        print(f"   Missing: {', '.join(dep_status['missing_required'])}")
    
    # Check system requirements
    sys_status = dep_checker.check_system_requirements()
    print(f"   System: Python {sys.version_info.major}.{sys.version_info.minor}+ ✓" if sys_status['python_version'] else "   System: Python version too old ✗")
    print(f"   Network: {'Available' if sys_status['network_access'] else 'Unavailable'}")
    print(f"   Cache: {'Writable' if sys_status['cache_directory'] else 'Not writable'}")
    
    # Overall status
    can_run = api_status['is_valid'] and dep_status['can_run_research'] and sys_status['python_version']
    
    if can_run:
        provider = api_status['preferred_provider']
        if provider in api_status['key_previews']:
            preview = api_status['key_previews'][f"{provider.upper()}_API_KEY"]
            print(f"✅ Ready to run with {provider} (key: {preview})")
        else:
            print(f"✅ Ready to run with {provider}")
    else:
        print("⚠️  System not ready - will use mock mode")
    
    return {
        "api_status": api_status,
        "dependency_status": dep_status,
        "system_status": sys_status,
        "can_run": can_run,
    }


def main():
    parser = create_argument_parser()
    args = parser.parse_args()

    # Check system readiness
    readiness = check_system_readiness()
    
    if args.check_only:
        if readiness['can_run']:
            print("\n✅ System is ready for deep research!")
        else:
            print("\n⚠️  System needs attention before running research")
        return 0
    
    # Topic is required if not check-only
    if not args.topic:
        parser.error("topic is required unless using --check-only")
    
    print(f"\n🔬 Starting deep research: {args.topic}")

    try:
        # Run research with error handling
        researcher = DeepResearch(llm_callback=llm_complete, base_dir=args.output_dir)

        # Determine mode: iterative (if --breadth specified) or classic
        if args.breadth is not None:
            # Iterative mode with explicit breadth
            print(f"   Mode: Iterative (breadth={args.breadth}, depth={args.depth})")
            if args.parallel:
                print("   Feature: Parallel scraping enabled 🚀")
            if args.token_budget != DEFAULT_TOKEN_BUDGET:
                print(f"   Feature: Token budget set to {args.token_budget}")
            
            # Initialize token budget
            token_budget = TokenBudget(total_limit=args.token_budget)
            
            state = ResearchState(
                topic=args.topic,
                session_id="",
                depth=args.depth,
                breadth=args.breadth,
                token_budget=token_budget,
            )
            
            final_state = researcher.deep_research(
                state,
                parallel=args.parallel,
                min_trust=args.min_trust
            )
            
            print(f"\n📚 Accumulated {len(final_state.learnings)} learnings")
            
            # Generate final report from all results
            session_data = {
                "session_id": final_state.session_id,
                "topic": final_state.topic,
            }
            report = researcher.generate_report(session_data, final_state.all_results)
        else:
            # Classic single-pass mode (backward compatible)
            # --depth is interpreted as URLs per step
            print(f"   Mode: Classic (urls_per_step={args.depth})")
            
            session = researcher.create_plan(args.topic)
            print(f"\n📋 Plan:\n{json.dumps(session['plan'], indent=2, ensure_ascii=False)}")

            # Pass Phase 2 params even in classic mode if requested
            results = researcher.execute_plan(
                session,
                max_urls_per_step=args.depth,
                parallel=args.parallel,
                min_trust=args.min_trust
            )

            print("\n📝 Generating report...")
            report = researcher.generate_report(session, results)

        print("\n" + "=" * 60)
        print("📊 FINAL REPORT")
        print("=" * 60)
        print(report)
        print("=" * 60)

        print(f"\n💾 Saved to: {researcher.archive.base_dir}/")
        
    except Exception as e:
        error_handler = get_error_handler()
        user_message = error_handler.handle_error(e, context={"topic": args.topic})
        print(f"\n{user_message}")
        return 1
    
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gemini Deep Research Integration

Provides 60-minute comprehensive research using Google's Deep Research capability.
Requires GEMINI_API_KEY and Google AI Pro subscription ($19.99/month).
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path


def get_gemini_client():
    """Get configured Gemini client."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError(
            "google-genai package not installed. "
            "Run: uv pip install 'google-genai>=1.55.0'"
        )

    # Priority: GEMINI_API_KEY (Pro subscription) > GOOGLE_API_KEY (free tier)
    gemini_key = os.getenv("GEMINI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    api_key = gemini_key if gemini_key else google_key

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not set. Get your key at: "
            "https://aistudio.google.com/apikey"
        )

    # Temporarily unset other Google keys to prevent library auto-detection conflicts
    # The google-genai library prefers GOOGLE_API_KEY over GEMINI_API_KEY by default
    old_google_key = os.environ.pop("GOOGLE_API_KEY", None)
    old_cloud_key = os.environ.pop("GOOGLE_CLOUD_API_KEY", None)

    try:
        # Explicitly pass api_key to ensure correct key is used
        client = genai.Client(api_key=api_key)

        # Confirm which key is being used
        if gemini_key and api_key == gemini_key:
            print(f"✅ Using GEMINI_API_KEY (Pro subscription)", file=sys.stderr)
        else:
            print(f"⚠️  Using GOOGLE_API_KEY (may be free tier)", file=sys.stderr)

        return client, types
    finally:
        # Restore environment variables
        if old_google_key:
            os.environ["GOOGLE_API_KEY"] = old_google_key
        if old_cloud_key:
            os.environ["GOOGLE_CLOUD_API_KEY"] = old_cloud_key


def get_available_models(client) -> Dict[str, str]:
    """
    Get available Gemini models including Deep Research.

    Returns:
        Dict mapping model types to model names
    """
    try:
        models = client.models.list()
        model_names = [m.name for m in models if hasattr(m, 'name')]

        available = {}

        # Deep Research agent (expensive, slow, most comprehensive)
        deep_research_models = [
            "models/deep-research-pro-preview-12-2025",
            "models/deep-research-pro-preview",
        ]
        for model in deep_research_models:
            if model in model_names:
                available["deep_research"] = model
                break

        # Regular high-quality models
        pro_models = [
            "models/gemini-3-pro-preview",
            "models/gemini-2.5-pro",
        ]
        for model in pro_models:
            if model in model_names:
                available["pro"] = model
                break

        # Fast models
        flash_models = [
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash-exp",
        ]
        for model in flash_models:
            if model in model_names:
                available["flash"] = model
                break

        return available

    except Exception as e:
        print(f"Warning: Could not list models: {e}", file=sys.stderr)
        return {
            "pro": "models/gemini-2.5-pro",
            "flash": "models/gemini-2.5-flash"
        }


def select_optimal_model(
    client,
    query: str,
    research_mode: str = "auto",
    context: Optional[Dict[str, Any]] = None
) -> tuple[str, str]:
    """
    Select optimal model based on query complexity and context.

    Args:
        client: Gemini client
        query: Research query
        research_mode: "deep_research", "pro", "flash", or "auto"
        context: Optional context (phase, task_type)

    Returns:
        (model_name, model_type) tuple
    """
    available = get_available_models(client)
    context = context or {}

    # Force modes
    if research_mode == "deep_research":
        if "deep_research" in available:
            return available["deep_research"], "deep_research"
        print("⚠️  Deep Research not available, falling back to Pro", file=sys.stderr)
        return available.get("pro", available.get("flash")), "pro"

    if research_mode == "pro":
        return available.get("pro", available.get("flash")), "pro"

    if research_mode == "flash":
        return available.get("flash", available.get("pro")), "flash"

    # Auto mode: Smart routing based on context

    # Deep Research triggers (use sparingly - expensive!)
    deep_research_triggers = [
        # Phase 1: Critical market analysis only
        (context.get("phase") == 1 and context.get("task_type") == "competitive-analysis"),

        # Complex multi-faceted queries
        len(query) > 500,
        any(keyword in query.lower() for keyword in [
            "comprehensive analysis",
            "in-depth research",
            "systematic review",
            "meta-analysis"
        ])
    ]

    if any(deep_research_triggers) and "deep_research" in available:
        return available["deep_research"], "deep_research"

    # Pro model triggers (good balance)
    pro_triggers = [
        # Phase 1 market research
        context.get("phase") == 1,

        # Phase 2 architecture decisions
        context.get("phase") == 2 and "architecture" in context.get("task_type", ""),

        # Complex queries
        len(query) > 300,
        any(keyword in query.lower() for keyword in [
            "compare", "evaluate", "assess", "analyze"
        ])
    ]

    if any(pro_triggers):
        return available.get("pro", available.get("flash")), "pro"

    # Default: Flash (fast and cost-effective)
    return available.get("flash", available.get("pro")), "flash"


def execute_deep_research(
    query: str,
    output_file: Optional[Path] = None,
    progress_callback: Optional[Callable] = None,
    research_mode: str = "auto",
    context: Optional[Dict[str, Any]] = None,
    project_folder: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Execute Gemini Deep Research query with budget tracking.

    Args:
        query: Research question to investigate
        output_file: Optional path to save results
        progress_callback: Optional callback function for progress updates
        research_mode: "deep_research", "pro", "flash", or "auto"
        context: Optional context (phase, task_type, project_folder)
        project_folder: Optional project folder for budget tracking

    Returns:
        Dict containing:
            - success: bool
            - response: str (research findings)
            - sources: List[Dict] (citations and references)
            - metadata: Dict (model info, timing, etc.)
            - error: Optional[str]
    """
    start_time = time.time()
    context = context or {}

    # Extract project folder from context if not provided
    if not project_folder and "project_folder" in context:
        project_folder = Path(context["project_folder"])

    try:
        client, types = get_gemini_client()

        # Select optimal model based on query and context
        model, model_type = select_optimal_model(client, query, research_mode, context)

        if progress_callback:
            if model_type == "deep_research":
                progress_callback(f"⚠️  Using Deep Research Agent (expensive, 30-60 min)")
            elif model_type == "pro":
                progress_callback(f"Using Gemini Pro (high quality, 1-5 min)")
            else:
                progress_callback(f"Using Gemini Flash (fast, 30-60 sec)")

        # Execute research with selected model
        result = _execute_comprehensive_research(
            client, types, query, model, model_type, output_file, progress_callback
        )

        return result

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "sources": [],
            "metadata": {
                "model": "gemini-deep-research",
                "error": str(e),
                "duration_seconds": time.time() - start_time
            },
            "error": str(e)
        }


def _execute_comprehensive_research(
    client, types, query: str, model: str, model_type: str,
    output_file: Optional[Path],
    progress_callback: Optional[Callable]
) -> Dict[str, Any]:
    """
    Execute comprehensive multi-step research using selected Gemini model.

    Args:
        model_type: "deep_research", "pro", or "flash"

    Deep Research agent uses multi-step agentic reasoning (30-60 min).
    Pro/Flash use standard generation (1-5 min / 30-60 sec).
    """
    start_time = time.time()

    model_name = model.split('/')[-1]  # Extract short name
    if progress_callback:
        progress_callback(f"Using {model_name} for comprehensive research...")

    try:
        # Enhanced research prompt for comprehensive analysis
        enhanced_query = f"""Conduct comprehensive research on the following query. Provide:

1. **Executive Summary**: High-level overview
2. **Detailed Analysis**: In-depth examination of all aspects
3. **Current Data & Statistics**: Latest trends, projections, and metrics
4. **Key Findings**: Critical insights and discoveries
5. **Strategic Implications**: Actionable insights and recommendations
6. **Sources & References**: List all authoritative sources

Query: {query}

Provide a thorough, well-researched analysis."""

        # Configure based on model type
        # Note: Deep Research agent has built-in multi-step reasoning capabilities
        # No special config needed - the model itself handles agentic workflow
        config = types.GenerateContentConfig(
            temperature=1.0,
            top_p=0.95,
            max_output_tokens=8192,
        )

        if model_type == "deep_research":
            if progress_callback:
                progress_callback("⚠️  Deep Research Agent active - this will take 30-60 minutes...")
        else:
            if progress_callback:
                duration = "1-5 minutes" if model_type == "pro" else "30-60 seconds"
                progress_callback(f"Generating comprehensive research ({duration})...")

        response = client.models.generate_content(
            model=model,
            contents=enhanced_query,
            config=config
        )

        # Extract response (skip thinking tags)
        response_text = ""
        if hasattr(response, 'text'):
            response_text = response.text
        elif hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    response_text += part.text

        # Remove <think> tags if present
        import re
        response_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)
        response_text = response_text.strip()

        # Extract sources from response
        sources = _extract_sources_from_text(response_text)

        # Save to file if requested
        if output_file:
            _save_results(output_file, response_text, sources, query)

        duration = time.time() - start_time

        if progress_callback:
            progress_callback(f"Research completed in {duration/60:.1f} minutes")

        return {
            "success": True,
            "response": response_text,
            "sources": sources,
            "metadata": {
                "model": model,
                "query": query,
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            },
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "sources": [],
            "metadata": {
                "model": model,
                "error": str(e),
                "duration_seconds": time.time() - start_time
            },
            "error": str(e)
        }


def _extract_sources(response) -> List[Dict[str, str]]:
    """Extract sources/citations from Gemini response object."""
    sources = []

    # Check for grounding metadata (if available)
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_metadata'):
            metadata = candidate.grounding_metadata
            if hasattr(metadata, 'grounding_chunks'):
                for chunk in metadata.grounding_chunks:
                    source = {
                        "title": getattr(chunk, 'title', ''),
                        "url": getattr(chunk, 'uri', ''),
                        "snippet": getattr(chunk, 'text', '')[:200]
                    }
                    if source["url"]:
                        sources.append(source)

    return sources


def _extract_sources_from_text(text: str) -> List[Dict[str, str]]:
    """Extract sources from text content (URLs, citations, etc.)."""
    import re

    sources = []

    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+[^\s.,;:!?<>"{}|\\^`\[\]]'
    urls = re.findall(url_pattern, text)

    for url in urls:
        sources.append({
            "url": url,
            "title": "",
            "snippet": ""
        })

    return sources


def _save_results(
    output_file: Path,
    response_text: str,
    sources: List[Dict[str, str]],
    query: str
):
    """Save research results to markdown file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Research Results

**Query**: {query}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Provider**: Gemini Deep Research

---

{response_text}

"""

    if sources:
        content += "\n## Sources\n\n"
        for i, source in enumerate(sources, 1):
            if source.get("title"):
                content += f"{i}. **{source['title']}**\n"
            if source.get("url"):
                content += f"   {source['url']}\n"
            if source.get("snippet"):
                content += f"   _{source['snippet']}_\n"
            content += "\n"

    output_file.write_text(content, encoding='utf-8')
    print(f"✅ Results saved to: {output_file}")


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Gemini Deep Research Tool"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Research query"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path"
    )

    args = parser.parse_args()

    # Progress callback
    def progress(msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    # Execute research
    result = execute_deep_research(
        args.query,
        output_file=args.output,
        progress_callback=progress
    )

    if result["success"]:
        print("\n" + "="*70)
        print("RESEARCH RESULTS")
        print("="*70)
        print(result["response"])
        print("\n" + "="*70)
        print(f"Duration: {result['metadata']['duration_seconds']/60:.1f} minutes")
        print(f"Sources: {len(result['sources'])}")
    else:
        print(f"\n❌ Research failed: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

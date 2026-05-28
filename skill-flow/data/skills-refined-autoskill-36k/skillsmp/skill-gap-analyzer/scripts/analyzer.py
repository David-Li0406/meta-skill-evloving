#!/usr/bin/env python3
"""
Skill Gap Analyzer

Analyzes project requirements to identify missing skills and automatically
creates them following the MCP Code Execution pattern when appropriate.

Usage:
    python analyzer.py <requirements_file>
    python analyzer.py requirements.md
    python analyzer.py --scan  # Scan existing skills

Output:
    JSON report with detected technologies, required skills, and gaps
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"


# Technology detection patterns
TECHNOLOGY_PATTERNS = {
    "fastapi": ["fastapi", "python api", "rest api python", "starlette"],
    "nextjs": ["next.js", "nextjs", "react frontend", "frontend"],
    "express": ["express", "node.js api", "nodejs api"],
    "postgresql": ["postgresql", "postgres", "sql database", "neon"],
    "mongodb": ["mongodb", "mongo", "nosql", "document database"],
    "kafka": ["kafka", "event streaming", "message queue", "pub/sub"],
    "graphql": ["graphql", "graph api", "apollo"],
    "docker": ["docker", "container", "dockerfile", "compose"],
    "kubernetes": ["kubernetes", "k8s", "kubectl", "minikube", "helm"],
    "github-actions": ["github actions", "ci/cd", "pipeline", "workflow"],
    "dapr": ["dapr", "distributed application", "sidecar"],
    "redis": ["redis", "cache", "in-memory"],
    "elasticsearch": ["elasticsearch", "elastic", "full-text search"],
    "terraform": ["terraform", "infrastructure as code", "iac"],
    "argocd": ["argocd", "argo cd", "gitops"],
}

# MCP-related patterns (require code execution pattern)
MCP_PATTERNS = {
    "google-drive": ["google drive", "gdrive", "docs api", "google docs"],
    "salesforce": ["salesforce", "crm", "sfdc", "soql"],
    "slack": ["slack", "slack api", "messaging", "slack bot"],
    "github-api": ["github api", "repository api", "issues api", "octokit"],
    "database-query": ["query database", "sql queries", "data extraction"],
    "spreadsheet": ["spreadsheet", "excel", "csv processing", "sheets"],
    "email": ["email", "smtp", "mail api", "sendgrid", "ses"],
    "storage": ["s3", "cloud storage", "blob storage", "gcs"],
    "notion": ["notion", "notion api", "notion database"],
    "airtable": ["airtable", "airtable api"],
}

# Map technologies to skill names
TECH_TO_SKILL = {
    "fastapi": "fastapi-generator",
    "nextjs": "nextjs-generator",
    "express": "express-generator",
    "postgresql": "postgres-setup",
    "mongodb": "mongodb-setup",
    "kafka": "kafka-k8s-setup",
    "graphql": "graphql-generator",
    "docker": "docker-generator",
    "kubernetes": "k8s-generator",
    "github-actions": "ci-cd-generator",
    "dapr": "fastapi-dapr-agent",
    "redis": "redis-setup",
    "argocd": "argocd-deployment",
}

MCP_TO_SKILL = {
    "google-drive": "gdrive-integration",
    "salesforce": "salesforce-integration",
    "slack": "slack-integration",
    "github-api": "github-api-integration",
    "database-query": "data-extractor",
    "spreadsheet": "spreadsheet-processor",
    "email": "email-integration",
    "storage": "cloud-storage-integration",
    "notion": "notion-integration",
    "airtable": "airtable-integration",
}


@dataclass
class AnalysisResult:
    """Result of requirements analysis."""
    analyzed_file: str
    technologies_detected: List[str]
    mcp_integrations_detected: List[str]
    skills_required: List[Dict[str, any]]
    skills_existing: List[str]
    skills_missing: List[str]
    mcp_pattern_required: bool
    ready_to_build: bool


def analyze_requirements(requirements_text: str) -> Tuple[List[str], List[str]]:
    """
    Extract technologies and MCP integrations from requirements text.

    Returns:
        Tuple of (technologies, mcp_integrations)
    """
    text_lower = requirements_text.lower()

    technologies = []
    for tech, keywords in TECHNOLOGY_PATTERNS.items():
        if any(kw in text_lower for kw in keywords):
            technologies.append(tech)

    mcp_integrations = []
    for mcp, keywords in MCP_PATTERNS.items():
        if any(kw in text_lower for kw in keywords):
            mcp_integrations.append(mcp)

    return technologies, mcp_integrations


def get_existing_skills() -> List[str]:
    """Get list of existing skills in the project."""
    existing = []

    if SKILLS_DIR.exists():
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    existing.append(skill_dir.name)

    return existing


def check_skill_has_mcp_pattern(skill_name: str) -> bool:
    """Check if a skill follows MCP code execution pattern."""
    skill_dir = SKILLS_DIR / skill_name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return False

    content = skill_md.read_text()

    # Check for MCP pattern indicators
    indicators = [
        "mcp-pattern:",
        "code-execution",
        "servers/",
        "workspace/",
        "callMCPTool",
    ]

    return any(ind in content for ind in indicators)


def analyze_file(file_path: str) -> AnalysisResult:
    """
    Analyze a requirements file for skill gaps.

    Args:
        file_path: Path to requirements file

    Returns:
        AnalysisResult with all findings
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Requirements file not found: {file_path}")

    requirements_text = path.read_text()

    # Detect technologies and MCP needs
    technologies, mcp_integrations = analyze_requirements(requirements_text)

    # Map to required skills
    skills_required = []

    for tech in technologies:
        skill_name = TECH_TO_SKILL.get(tech, f"{tech}-setup")
        skills_required.append({
            "name": skill_name,
            "technology": tech,
            "mcp_pattern": False
        })

    for mcp in mcp_integrations:
        skill_name = MCP_TO_SKILL.get(mcp, f"{mcp}-integration")
        skills_required.append({
            "name": skill_name,
            "technology": mcp,
            "mcp_pattern": True  # MCP integrations MUST use code execution
        })

    # Check existing skills
    existing_skills = get_existing_skills()
    required_skill_names = [s["name"] for s in skills_required]

    skills_existing = [s for s in required_skill_names if s in existing_skills]
    skills_missing = [s for s in required_skill_names if s not in existing_skills]

    # Determine if MCP pattern is required
    mcp_pattern_required = len(mcp_integrations) > 0

    # Ready to build if no missing skills (or only optional ones)
    ready_to_build = len(skills_missing) == 0

    return AnalysisResult(
        analyzed_file=str(path),
        technologies_detected=technologies,
        mcp_integrations_detected=mcp_integrations,
        skills_required=skills_required,
        skills_existing=skills_existing,
        skills_missing=skills_missing,
        mcp_pattern_required=mcp_pattern_required,
        ready_to_build=ready_to_build
    )


def scan_skills() -> Dict:
    """Scan all existing skills and return their status."""
    existing_skills = get_existing_skills()

    skills_info = []
    for skill_name in existing_skills:
        has_mcp = check_skill_has_mcp_pattern(skill_name)
        skill_dir = SKILLS_DIR / skill_name

        # Check for required components
        has_scripts = (skill_dir / "scripts").exists() and any((skill_dir / "scripts").iterdir()) if (skill_dir / "scripts").exists() else False
        has_servers = (skill_dir / "servers").exists()

        skills_info.append({
            "name": skill_name,
            "has_mcp_pattern": has_mcp,
            "has_scripts": has_scripts,
            "has_servers": has_servers,
            "complete": has_scripts or has_servers
        })

    return {
        "total_skills": len(existing_skills),
        "skills": skills_info,
        "mcp_pattern_skills": sum(1 for s in skills_info if s["has_mcp_pattern"]),
        "complete_skills": sum(1 for s in skills_info if s["complete"])
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <requirements_file>")
        print("       python analyzer.py --scan")
        print("")
        print("Examples:")
        print("  python analyzer.py requirements.md")
        print("  python analyzer.py docs/REQUIREMENTS.md")
        print("  python analyzer.py --scan  # Scan existing skills")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--scan":
        result = scan_skills()
        print(json.dumps(result, indent=2))
    else:
        try:
            result = analyze_file(arg)
            print(json.dumps(asdict(result), indent=2))

            # Print summary for quick reading
            print("\n" + "="*50)
            print("SUMMARY")
            print("="*50)
            print(f"Technologies: {', '.join(result.technologies_detected) or 'None'}")
            print(f"MCP Integrations: {', '.join(result.mcp_integrations_detected) or 'None'}")
            print(f"Skills Required: {len(result.skills_required)}")
            print(f"Skills Existing: {len(result.skills_existing)}")
            print(f"Skills Missing: {len(result.skills_missing)}")
            if result.skills_missing:
                print(f"  Missing: {', '.join(result.skills_missing)}")
            print(f"MCP Pattern Required: {result.mcp_pattern_required}")
            print(f"Ready to Build: {result.ready_to_build}")

        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Analysis failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

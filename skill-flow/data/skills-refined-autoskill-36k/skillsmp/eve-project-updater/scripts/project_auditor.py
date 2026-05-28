#!/usr/bin/env python3
"""
EVE Project Auditor

Scans EVE Online projects, rates compliance, and generates update plans.

Usage:
    python project_auditor.py ~/projects/EVE_*
    python project_auditor.py ~/projects --report
    python project_auditor.py ~/projects --json > audit.json
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProjectType(Enum):
    GAME = "game"           # Pygame, game logic
    API = "api"             # FastAPI, Flask backends
    WEB = "web"             # React, web frontends
    ASSETS = "assets"       # SVG, image collections
    LIBRARY = "library"     # Reusable modules
    UNKNOWN = "unknown"


class ComplianceLevel(Enum):
    CRITICAL = "critical"   # Bannable offense
    WARNING = "warning"     # Best practice violation
    INFO = "info"           # Suggestion
    PASS = "pass"           # Requirement met


@dataclass
class ComplianceCheck:
    name: str
    level: ComplianceLevel
    weight: int
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    fix: Optional[str] = None


@dataclass
class IntegrationOpportunity:
    feature: str
    source: str           # ESI endpoint or Image Server
    difficulty: str       # easy, medium, hard
    value: str            # high, medium, low
    description: str


@dataclass
class ProjectAudit:
    name: str
    path: str
    project_type: ProjectType
    score: int = 0
    grade: str = "F"

    # Detection results
    has_esi: bool = False
    has_image_server: bool = False
    has_sso: bool = False
    has_sde: bool = False

    # File counts
    python_files: int = 0
    js_files: int = 0
    json_files: int = 0
    total_lines: int = 0

    # Compliance
    checks: List[ComplianceCheck] = field(default_factory=list)

    # Opportunities
    opportunities: List[IntegrationOpportunity] = field(default_factory=list)

    # Recommendations
    priority_actions: List[str] = field(default_factory=list)

    def calculate_grade(self):
        if self.score >= 90:
            self.grade = "A"
        elif self.score >= 80:
            self.grade = "B"
        elif self.score >= 70:
            self.grade = "C"
        elif self.score >= 60:
            self.grade = "D"
        else:
            self.grade = "F"


# Detection patterns
PATTERNS = {
    # Project type detection
    "pygame": re.compile(r'import pygame|from pygame'),
    "fastapi": re.compile(r'from fastapi|import fastapi|FastAPI\(\)'),
    "flask": re.compile(r'from flask|import flask|Flask\(__name__\)'),
    "react": re.compile(r'"react":|from [\'"]react[\'"]'),
    "express": re.compile(r'require\([\'"]express[\'"]\)|from [\'"]express[\'"]'),

    # ESI patterns
    "esi_url": re.compile(r'esi\.evetech\.net'),
    "image_server": re.compile(r'images\.evetech\.net'),
    "sso_url": re.compile(r'login\.eveonline\.com'),
    "sde_usage": re.compile(r'sde\.sqlite|fuzzwork|Static Data Export', re.IGNORECASE),

    # Compliance patterns
    "user_agent": re.compile(r'["\']User-Agent["\']|user.?agent', re.IGNORECASE),
    "cache_header": re.compile(r'Expires|Cache-Control|ETag|If-None-Match', re.IGNORECASE),
    "error_limit": re.compile(r'X-ESI-Error-Limit|error.?limit|420'),
    "rate_limit": re.compile(r'rate.?limit|throttle|sleep|asyncio\.sleep', re.IGNORECASE),
    "versioned": re.compile(r'/v\d+/|/latest/|/dev/'),

    # Bad patterns
    "discovery_loop": re.compile(r'for.*range.*get.*(character|corporation|structure)', re.IGNORECASE),
    "hardcoded_secret": re.compile(r'(client_secret|secret_key)\s*=\s*["\'][^"\']{10,}["\']', re.IGNORECASE),

    # Attribution
    "ccp_attribution": re.compile(r'CCP|EVE Online.*trademark|eveonline\.com', re.IGNORECASE),
}


def detect_project_type(project_path: Path) -> ProjectType:
    """Detect the type of EVE project."""
    all_content = ""

    for ext in ['*.py', '*.js', '*.jsx', '*.ts', '*.tsx', '*.json']:
        for f in project_path.rglob(ext):
            if 'node_modules' in str(f) or '.git' in str(f):
                continue
            try:
                all_content += f.read_text(errors='ignore')
            except Exception:
                pass

    # Check for game frameworks
    if PATTERNS["pygame"].search(all_content):
        return ProjectType.GAME

    # Check for API frameworks
    if PATTERNS["fastapi"].search(all_content) or PATTERNS["flask"].search(all_content):
        return ProjectType.API

    # Check for web frameworks
    if PATTERNS["react"].search(all_content) or PATTERNS["express"].search(all_content):
        return ProjectType.WEB

    # Check for asset collections
    svg_count = len(list(project_path.rglob('*.svg')))
    png_count = len(list(project_path.rglob('*.png')))
    if svg_count > 10 or png_count > 20:
        return ProjectType.ASSETS

    # Check for library patterns
    if (project_path / 'setup.py').exists() or (project_path / 'pyproject.toml').exists():
        return ProjectType.LIBRARY

    return ProjectType.UNKNOWN


def count_files(project_path: Path) -> Tuple[int, int, int, int]:
    """Count files and lines in project."""
    py_files = js_files = json_files = total_lines = 0

    for f in project_path.rglob('*'):
        if 'node_modules' in str(f) or '.git' in str(f) or not f.is_file():
            continue

        try:
            if f.suffix == '.py':
                py_files += 1
                total_lines += len(f.read_text(errors='ignore').split('\n'))
            elif f.suffix in ['.js', '.jsx', '.ts', '.tsx']:
                js_files += 1
                total_lines += len(f.read_text(errors='ignore').split('\n'))
            elif f.suffix == '.json':
                json_files += 1
        except Exception:
            pass

    return py_files, js_files, json_files, total_lines


def scan_for_patterns(project_path: Path) -> Dict[str, bool]:
    """Scan project for various patterns."""
    results = {key: False for key in PATTERNS.keys()}

    for ext in ['*.py', '*.js', '*.jsx', '*.ts', '*.tsx', '*.md']:
        for f in project_path.rglob(ext):
            if 'node_modules' in str(f) or '.git' in str(f):
                continue
            try:
                content = f.read_text(errors='ignore')
                for name, pattern in PATTERNS.items():
                    if pattern.search(content):
                        results[name] = True
            except Exception:
                pass

    return results


def run_compliance_checks(project_path: Path, patterns: Dict[str, bool], project_type: ProjectType) -> List[ComplianceCheck]:
    """Run compliance checks and return findings."""
    checks = []

    # Only check ESI compliance if ESI is used
    if patterns["esi_url"]:
        # User-Agent check
        if patterns["user_agent"]:
            checks.append(ComplianceCheck(
                "User-Agent Header", ComplianceLevel.PASS, 20,
                "User-Agent header is set"
            ))
        else:
            checks.append(ComplianceCheck(
                "User-Agent Header", ComplianceLevel.WARNING, 20,
                "No User-Agent header detected - CCP requires this",
                fix="Add header: {'User-Agent': 'AppName/1.0 (contact@email.com)'}"
            ))

        # Cache handling
        if patterns["cache_header"]:
            checks.append(ComplianceCheck(
                "Cache Handling", ComplianceLevel.PASS, 15,
                "Cache headers are being handled"
            ))
        else:
            checks.append(ComplianceCheck(
                "Cache Handling", ComplianceLevel.WARNING, 15,
                "No cache header handling detected",
                fix="Respect ESI's Expires header to avoid unnecessary requests"
            ))

        # Error limit
        if patterns["error_limit"]:
            checks.append(ComplianceCheck(
                "Error Limit Monitoring", ComplianceLevel.PASS, 15,
                "Error limit headers are monitored"
            ))
        else:
            checks.append(ComplianceCheck(
                "Error Limit Monitoring", ComplianceLevel.WARNING, 15,
                "No error limit handling - risk of ban",
                fix="Monitor X-ESI-Error-Limit-Remain header"
            ))

        # Discovery abuse
        if patterns["discovery_loop"]:
            checks.append(ComplianceCheck(
                "Discovery Abuse", ComplianceLevel.CRITICAL, 20,
                "CRITICAL: Potential ID discovery pattern detected - BANNABLE",
                fix="Never iterate over IDs to discover entities"
            ))
        else:
            checks.append(ComplianceCheck(
                "Discovery Abuse", ComplianceLevel.PASS, 20,
                "No discovery abuse patterns detected"
            ))

        # Rate limiting
        if patterns["rate_limit"]:
            checks.append(ComplianceCheck(
                "Rate Limiting", ComplianceLevel.PASS, 10,
                "Rate limiting is implemented"
            ))
        else:
            checks.append(ComplianceCheck(
                "Rate Limiting", ComplianceLevel.INFO, 10,
                "No rate limiting detected",
                fix="Consider adding rate limiting for bulk operations"
            ))

        # Versioned endpoints
        if patterns["versioned"]:
            checks.append(ComplianceCheck(
                "Versioned Endpoints", ComplianceLevel.PASS, 10,
                "Using versioned ESI endpoints"
            ))
        else:
            checks.append(ComplianceCheck(
                "Versioned Endpoints", ComplianceLevel.WARNING, 10,
                "Unversioned endpoints detected",
                fix="Use /latest/ or /v{n}/ prefixed endpoints"
            ))

    # Attribution check (always applies for EVE projects)
    if patterns["ccp_attribution"]:
        checks.append(ComplianceCheck(
            "CCP Attribution", ComplianceLevel.PASS, 10,
            "CCP attribution found"
        ))
    else:
        checks.append(ComplianceCheck(
            "CCP Attribution", ComplianceLevel.WARNING, 10,
            "No CCP attribution in README",
            fix="Add: 'EVE Online and the EVE logo are registered trademarks of CCP hf.'"
        ))

    # Hardcoded secrets
    if patterns["hardcoded_secret"]:
        checks.append(ComplianceCheck(
            "Secret Management", ComplianceLevel.CRITICAL, 0,
            "CRITICAL: Hardcoded secrets detected",
            fix="Move secrets to environment variables"
        ))

    return checks


def identify_opportunities(project_type: ProjectType, patterns: Dict[str, bool]) -> List[IntegrationOpportunity]:
    """Identify ESI integration opportunities."""
    opportunities = []

    if project_type == ProjectType.GAME:
        if not patterns["image_server"]:
            opportunities.append(IntegrationOpportunity(
                "Ship Sprites",
                "images.evetech.net/types/{id}/render",
                "easy", "high",
                "Replace placeholder sprites with official ship renders"
            ))
        opportunities.append(IntegrationOpportunity(
            "Ship Stats",
            "/universe/types/{id}/",
            "easy", "medium",
            "Use real EVE ship attributes for enemy scaling"
        ))
        opportunities.append(IntegrationOpportunity(
            "Faction Data",
            "/universe/factions/",
            "easy", "low",
            "Add authentic faction lore and colors"
        ))

    elif project_type == ProjectType.API:
        if not patterns["sso_url"]:
            opportunities.append(IntegrationOpportunity(
                "SSO Authentication",
                "login.eveonline.com/v2/oauth/",
                "medium", "high",
                "Add character authentication for personalized features"
            ))
        if not patterns["sde_usage"]:
            opportunities.append(IntegrationOpportunity(
                "SDE Integration",
                "Static Data Export (Fuzzwork)",
                "medium", "high",
                "Use SDE for bulk data instead of ESI loops"
            ))
        opportunities.append(IntegrationOpportunity(
            "Live Heatmaps",
            "/universe/system_kills/, /system_jumps/",
            "easy", "high",
            "Add real-time activity overlays"
        ))

    elif project_type == ProjectType.ASSETS:
        opportunities.append(IntegrationOpportunity(
            "Automated Fetching",
            "images.evetech.net/types/{id}/",
            "easy", "high",
            "Script to bulk download ship renders"
        ))
        opportunities.append(IntegrationOpportunity(
            "Type ID Manifest",
            "/universe/types/",
            "easy", "medium",
            "Associate images with EVE type IDs"
        ))

    elif project_type == ProjectType.WEB:
        if not patterns["image_server"]:
            opportunities.append(IntegrationOpportunity(
                "Dynamic Ship Images",
                "images.evetech.net CDN",
                "easy", "high",
                "Lazy-load ship images from EVE CDN"
            ))

    return opportunities


def generate_priority_actions(audit: ProjectAudit) -> List[str]:
    """Generate prioritized action items."""
    actions = []

    # Critical issues first
    critical_checks = [c for c in audit.checks if c.level == ComplianceLevel.CRITICAL]
    for check in critical_checks:
        actions.append(f"🚨 CRITICAL: {check.fix or check.message}")

    # High-value opportunities
    high_value = [o for o in audit.opportunities if o.value == "high" and o.difficulty == "easy"]
    for opp in high_value[:2]:
        actions.append(f"🎯 {opp.feature}: {opp.description}")

    # Warning fixes
    warning_checks = [c for c in audit.checks if c.level == ComplianceLevel.WARNING]
    for check in warning_checks[:3]:
        if check.fix:
            actions.append(f"⚠️ {check.name}: {check.fix}")

    return actions


def calculate_score(checks: List[ComplianceCheck], has_esi: bool) -> int:
    """Calculate compliance score."""
    if not has_esi:
        return 100  # No ESI = no violations possible

    max_score = sum(c.weight for c in checks)
    earned = sum(c.weight for c in checks if c.level == ComplianceLevel.PASS)

    # Critical issues are severe penalties
    critical_count = sum(1 for c in checks if c.level == ComplianceLevel.CRITICAL)
    earned -= critical_count * 25

    return max(0, min(100, int(earned / max_score * 100) if max_score > 0 else 100))


def audit_project(project_path: Path) -> ProjectAudit:
    """Perform full audit of a project."""
    audit = ProjectAudit(
        name=project_path.name,
        path=str(project_path),
        project_type=detect_project_type(project_path)
    )

    # Count files
    audit.python_files, audit.js_files, audit.json_files, audit.total_lines = count_files(project_path)

    # Scan patterns
    patterns = scan_for_patterns(project_path)
    audit.has_esi = patterns["esi_url"]
    audit.has_image_server = patterns["image_server"]
    audit.has_sso = patterns["sso_url"]
    audit.has_sde = patterns["sde_usage"]

    # Run compliance checks
    audit.checks = run_compliance_checks(project_path, patterns, audit.project_type)

    # Calculate score
    audit.score = calculate_score(audit.checks, audit.has_esi)
    audit.calculate_grade()

    # Identify opportunities
    audit.opportunities = identify_opportunities(audit.project_type, patterns)

    # Generate actions
    audit.priority_actions = generate_priority_actions(audit)

    return audit


def print_audit_report(audits: List[ProjectAudit]):
    """Print formatted audit report."""
    print("\n" + "=" * 70)
    print("  EVE PROJECT AUDIT REPORT")
    print("  Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)

    # Summary table
    print("\n📊 PROJECT SUMMARY\n")
    print(f"{'Project':<25} {'Type':<12} {'Score':>6} {'Grade':>6} {'ESI':>5} {'SSO':>5}")
    print("-" * 70)

    for audit in audits:
        esi = "✅" if audit.has_esi else "❌"
        sso = "✅" if audit.has_sso else "❌"
        print(f"{audit.name:<25} {audit.project_type.value:<12} {audit.score:>6} {audit.grade:>6} {esi:>5} {sso:>5}")

    # Overall grade
    avg_score = sum(a.score for a in audits) / len(audits) if audits else 0
    overall_grade = "A" if avg_score >= 90 else "B" if avg_score >= 80 else "C" if avg_score >= 70 else "D" if avg_score >= 60 else "F"
    print("-" * 70)
    print(f"{'OVERALL':<25} {'':<12} {avg_score:>6.0f} {overall_grade:>6}")

    # Detailed per-project reports
    for audit in audits:
        print(f"\n{'─' * 70}")
        print(f"📁 {audit.name}")
        print(f"   Type: {audit.project_type.value} | Score: {audit.score}/100 ({audit.grade})")
        print(f"   Files: {audit.python_files} Python, {audit.js_files} JS, {audit.json_files} JSON")
        print(f"   Lines: {audit.total_lines:,}")

        # Compliance checks
        fails = [c for c in audit.checks if c.level != ComplianceLevel.PASS]
        if fails:
            print(f"\n   ⚠️ Compliance Issues ({len(fails)}):")
            for check in fails:
                icon = "🚨" if check.level == ComplianceLevel.CRITICAL else "⚠️" if check.level == ComplianceLevel.WARNING else "ℹ️"
                print(f"      {icon} {check.name}: {check.message}")
                if check.fix:
                    print(f"         → {check.fix}")
        else:
            print("\n   ✅ All compliance checks passed!")

        # Opportunities
        if audit.opportunities:
            print("\n   🎯 Integration Opportunities:")
            for opp in audit.opportunities[:3]:
                print(f"      • {opp.feature} [{opp.difficulty}/{opp.value}]")
                print(f"        {opp.description}")

        # Priority actions
        if audit.priority_actions:
            print("\n   📋 Priority Actions:")
            for i, action in enumerate(audit.priority_actions[:5], 1):
                print(f"      {i}. {action}")

    print("\n" + "=" * 70)
    print("  Run 'project_updater.py <path> --apply' to implement fixes")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Audit EVE Online projects")
    parser.add_argument("paths", nargs="+", type=Path, help="Project paths to audit")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--output", "-o", type=Path, help="Save report to file")

    args = parser.parse_args()

    # Expand glob patterns
    projects = []
    for path in args.paths:
        if path.exists():
            if path.is_dir():
                # Check if it's a project or a parent directory
                if (path / 'README.md').exists() or (path / 'main.py').exists() or (path / 'package.json').exists():
                    projects.append(path)
                else:
                    # Look for subdirectories that are projects
                    for subdir in path.iterdir():
                        if subdir.is_dir() and not subdir.name.startswith('.'):
                            projects.append(subdir)
        else:
            # Try glob
            import glob
            projects.extend([Path(p) for p in glob.glob(str(path))])

    if not projects:
        print("No projects found to audit")
        sys.exit(1)

    # Run audits
    audits = [audit_project(p) for p in projects]

    if args.json:
        output = {
            "generated": datetime.now().isoformat(),
            "projects": [
                {
                    "name": a.name,
                    "path": a.path,
                    "type": a.project_type.value,
                    "score": a.score,
                    "grade": a.grade,
                    "has_esi": a.has_esi,
                    "has_sso": a.has_sso,
                    "checks": [
                        {"name": c.name, "level": c.level.value, "message": c.message, "fix": c.fix}
                        for c in a.checks
                    ],
                    "opportunities": [
                        {"feature": o.feature, "source": o.source, "difficulty": o.difficulty, "value": o.value}
                        for o in a.opportunities
                    ],
                    "priority_actions": a.priority_actions
                }
                for a in audits
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print_audit_report(audits)

    if args.output:
        # Save to file
        with open(args.output, 'w') as f:
            json.dump({
                "generated": datetime.now().isoformat(),
                "audits": [asdict(a) for a in audits]
            }, f, indent=2, default=str)
        print(f"\n📄 Report saved to: {args.output}")

    # Exit with error if any critical issues
    critical_count = sum(1 for a in audits for c in a.checks if c.level == ComplianceLevel.CRITICAL)
    sys.exit(1 if critical_count > 0 else 0)


if __name__ == "__main__":
    main()

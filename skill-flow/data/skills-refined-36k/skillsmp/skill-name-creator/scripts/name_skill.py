#!/usr/bin/env python3
"""
ASIS Skill Namer - Generates ASIS-compliant identifiers and OpenCode skill names.
"""

import re
import sys
import json
from typing import Optional

NAMESPACES_CORE = {"File", "Shell", "Net", "Data", "Logic"}
NAMESPACES_INTEGRATION = {"Git", "GitHub", "Docker", "AWS", "Revit", "Chrome"}
NAMESPACES = NAMESPACES_CORE | NAMESPACES_INTEGRATION

ACTIONS_CRUD = {"Read", "Write", "Update", "Delete", "List", "Search"}
ACTIONS_OPS = {"Execute", "Launch", "Sync", "Build", "Deploy", "Connect", "Backup", "Scan", "Parse", "Validate"}
ACTIONS = ACTIONS_CRUD | ACTIONS_OPS

ABSTRACT_TARGETS = {
    "Quality", "Idea", "State", "Happiness", "Problem", "Solution", "Approach",
    "Understanding", "Knowledge", "Wisdom", "Truth", "Beauty", "Good", "Bad",
    "Context", "Meaning", "Purpose", "Value", "Importance", "Relevance",
    "Efficiency", "Effectiveness", "Performance", "Productivity", "Success",
    "Failure", "Risk", "Opportunity", "Challenge", "Difficulty", "Ease"
}

VERB_MAP = {
    "create": "Write",
    "make": "Write",
    "open": "Read",
    "get": "Read",
    "fetch": "Read",
    "fix": None,
    "improve": None,
    "handle": None,
    "manage": None,
    "think": None,
    "understand": None,
    "know": None,
}

def parse_request(user_input: str) -> dict:
    """Extract components from user request."""
    text = user_input.lower()

    namespace = "Data"
    if any(w in text for w in ["revit", "autodesk"]):
        namespace = "Revit"
    elif any(w in text for w in ["github", "pr", "pull request", "issue"]):
        namespace = "GitHub"
    elif any(w in text for w in ["git", "commit", "branch", "repo"]):
        namespace = "Git"
    elif any(w in text for w in ["docker", "container", "image"]):
        namespace = "Docker"
    elif any(w in text for w in ["aws", "cloud", "lambda", "s3"]):
        namespace = "AWS"
    elif any(w in text for w in ["chrome", "browser", "web", "page"]):
        namespace = "Chrome"
    elif any(w in text for w in ["file", "directory", "folder", "path"]):
        namespace = "File"
    elif any(w in text for w in ["shell", "command", "terminal", "bash", "powershell"]):
        namespace = "Shell"
    elif any(w in text for w in ["network", "url", "http", "download", "fetch"]):
        namespace = "Net"

    action = "Read"
    if any(w in text for w in ["create", "make", "add", "new"]):
        action = "Write"
    elif any(w in text for w in ["delete", "remove", "clear", "clean"]):
        action = "Delete"
    elif any(w in text for w in ["update", "change", "modify", "edit"]):
        action = "Update"
    elif any(w in text for w in ["list", "show", "display", "view"]):
        action = "List"
    elif any(w in text for w in ["search", "find", "grep", "query"]):
        action = "Search"
    elif any(w in text for w in ["execute", "run", "start"]):
        action = "Execute"
    elif any(w in text for w in ["launch", "open", "start"]):
        action = "Launch"
    elif any(w in text for w in ["sync", "push", "pull", "fetch"]):
        action = "Sync"
    elif any(w in text for w in ["build", "compile", "make"]):
        action = "Build"
    elif any(w in text for w in ["deploy", "release", "ship"]):
        action = "Deploy"
    elif any(w in text for w in ["connect", "auth", "login"]):
        action = "Connect"
    elif any(w in text for w in ["backup", "save", "copy"]):
        action = "Backup"
    elif any(w in text for w in ["scan", "lint", "check", "validate", "analyze"]):
        action = "Scan"

    target = "Resource"
    if any(w in text for w in ["skill", "tool", "function"]):
        target = "Skill"
    elif any(w in text for w in ["file", "text", "content", "code"]):
        target = "File"
    elif any(w in text for w in ["folder", "directory", "path"]):
        target = "Directory"
    elif any(w in text for w in ["repo", "repository", "branch", "commit"]):
        target = "Repo"
    elif any(w in text for w in ["pr", "pull request"]):
        target = "PullRequest"
    elif any(w in text for w in ["issue", "ticket"]):
        target = "Issue"
    elif any(w in text for w in ["image", "photo", "picture"]):
        target = "Image"
    elif any(w in text for w in ["sheet", "view", "drawing"]):
        target = "Sheet"
    elif any(w in text for w in ["cache", "temp", "tmp"]):
        target = "Cache"
    elif any(w in text for w in ["model", "revit", "project"]):
        target = "Model"
    elif any(w in text for w in ["url", "link", "web", "page"]):
        target = "Url"

    qualifier = None
    if "json" in text:
        qualifier = "Json"
    elif "pdf" in text:
        qualifier = "Pdf"
    elif "full" in text:
        qualifier = "Full"
    elif "incremental" in text:
        qualifier = "Incremental"

    return {
        "namespace": namespace,
        "action": action,
        "target": target,
        "qualifier": qualifier
    }

def build_asis(namespace: str, action: str, target: str, qualifier: Optional[str] = None) -> str:
    """Build ASIS identifier from components."""
    parts = [namespace, action, target]
    if qualifier:
        parts.append(qualifier)
    return "_".join(parts)

def split_pascalcase(s: str) -> list:
    """Split PascalCase string into word tokens."""
    tokens = []
    current = ""
    for char in s:
        if char.isupper():
            if current:
                tokens.append(current.lower())
            current = char.lower()
        else:
            current += char
    if current:
        tokens.append(current)
    return tokens

def asis_to_opencode(asis_id: str) -> str:
    """Convert ASIS identifier to OpenCode skill name."""
    segments = asis_id.split("_")
    parts = []
    for segment in segments:
        tokens = split_pascalcase(segment)
        parts.extend(tokens)
    return "-".join(parts)

def run_compliance_test(asis_id: str) -> tuple:
    """Run ASIS compliance test. Returns (PASS/FAIL, errors, warnings)."""
    errors = []
    warnings = []

    phase1 = r"^[A-Z][a-zA-Z0-9]*(?:_[A-Z][a-zA-Z0-9]*)*$"
    if not re.match(phase1, asis_id):
        errors.append("ERR_SYNTAX_CASE")

    segments = asis_id.split("_")
    if not (3 <= len(segments) <= 4):
        errors.append("ERR_SEGMENT_COUNT")

    namespace = segments[0] if segments else ""
    if namespace and namespace not in NAMESPACES:
        errors.append("ERR_NAMESPACE_INVALID")

    if len(segments) > 1:
        action = segments[1]
        if action and action not in ACTIONS:
            errors.append("ERR_ACTION_INVALID")

    if len(segments) > 2:
        target = segments[2]
        if target in ABSTRACT_TARGETS:
            errors.append("ERR_TARGET_ABSTRACT")

    if len(segments) == 4:
        qualifier = segments[3]
        if qualifier and not re.match(r"^[A-Z][a-zA-Z0-9]*$", qualifier):
            errors.append("ERR_QUALIFIER_INVALID")

    if "Think" in asis_id or "Understand" in asis_id or "Improve" in asis_id:
        errors.append("ERR_NON_DETERMINISTIC")

    return ("PASS" if not errors else "FAIL", errors, warnings)

def generate_name(user_input: str) -> dict:
    """Generate ASIS identifier and OpenCode name from user request."""
    components = parse_request(user_input)
    asis_id = build_asis(
        components["namespace"],
        components["action"],
        components["target"],
        components["qualifier"]
    )
    result, errors, warnings = run_compliance_test(asis_id)

    opencode_name = asis_to_opencode(asis_id)
    folder_path = f".opencode/skills/{opencode_name}/SKILL.md"

    notes = f"Generated from capability: {user_input[:50]}..."

    return {
        "asis_identifier": asis_id,
        "opencode_skill_name": opencode_name,
        "folder_path": folder_path,
        "result": result,
        "errors": errors,
        "warnings": warnings,
        "notes": notes
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = sys.stdin.read().strip()

    if not user_input:
        print(json.dumps({
            "asis_identifier": "",
            "opencode_skill_name": "",
            "folder_path": "",
            "result": "FAIL",
            "errors": ["ERR_NO_INPUT"],
            "warnings": [],
            "notes": "No input provided"
        }))
        sys.exit(1)

    result = generate_name(user_input)
    print(json.dumps(result, indent=2))

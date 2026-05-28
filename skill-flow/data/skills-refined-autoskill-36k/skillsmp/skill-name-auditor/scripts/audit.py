#!/usr/bin/env python3
"""
ASIS Skill Auditor - Scans skills and verifies naming compliance.
"""

import os
import sys
import json
import re
import importlib.util

# Configuration
SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMER_SCRIPT = os.path.join(SKILLS_DIR, "skill-name-creator", "scripts", "name_skill.py")

def load_namer_module():
    """Dynamically load the skill-name-creator module."""
    if not os.path.exists(NAMER_SCRIPT):
        return None
    spec = importlib.util.spec_from_file_location("name_skill", NAMER_SCRIPT)
    if spec is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["name_skill"] = module
    if spec.loader:
        spec.loader.exec_module(module)
    return module

namer = load_namer_module()

def parse_skill_md(skill_path):
    """Extract name and description from SKILL.md."""
    md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(md_path):
        return None

    data = {"name": None, "description": ""}
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # simple frontmatter parse
        match = re.search(r"^---\s+(.*?)\s+---", content, re.DOTALL)
        if match:
            fm = match.group(1)
            for line in fm.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    if key == "name":
                        data["name"] = val
                    elif key == "description":
                        data["description"] = val
    except Exception as e:
        print(f"Error parsing {md_path}: {e}", file=sys.stderr)
    
    return data

def audit_skills():
    results = []
    
    if not os.path.exists(SKILLS_DIR):
        print(f"Skills directory not found: {SKILLS_DIR}")
        return

    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(item_path) or item.startswith("."):
            continue

        skill_data = parse_skill_md(item_path)
        if not skill_data:
            results.append({
                "directory": item,
                "status": "ERROR",
                "message": "Missing SKILL.md"
            })
            continue

        current_name = skill_data["name"]
        description = skill_data["description"]
        
        # Check 1: Directory Kebab-Case
        dir_kebab_ok = bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", item))
        
        # Check 2: ASIS Compliance (using Namer logic if available)
        compliance = "UNKNOWN"
        errors = []
        suggestion = None

        if namer:
            # Check current name compliance
            pass_status, errs, _ = namer.run_compliance_test(current_name)
            compliance = pass_status
            errors = errs

            # If fail, generate suggestion from description
            if compliance == "FAIL":
                # Try to generate a name from the description
                try:
                    gen = namer.generate_name(description or item)
                    suggestion = gen["asis_identifier"]
                except Exception:
                    suggestion = "Could not generate"
        
        results.append({
            "directory": item,
            "current_name": current_name,
            "dir_kebab_compliant": dir_kebab_ok,
            "asis_compliant": compliance,
            "errors": errors,
            "suggested_rename": suggestion
        })

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    audit_skills()

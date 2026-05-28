#!/usr/bin/env python3
"""
Supabase Insert Script for Shapira Ecosystem

Validates and inserts data into any table with proper schema checking.
Designed to run in GitHub Actions environment.

Usage:
    python insert_insight.py --table tasks --data '{"description": "...", "domain": "BUSINESS"}'
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional

# Table schemas for validation
SCHEMAS = {
    "tasks": {
        "required": ["description", "domain"],
        "optional": ["state", "complexity", "clarity", "estimated_minutes", "due_date"],
        "defaults": {"state": "INITIATED", "complexity": 5, "clarity": 5}
    },
    "activities": {
        "required": ["category", "description"],
        "optional": ["duration_minutes", "energy_level", "focus_quality"]
    },
    "insights": {
        "required": ["category", "content"],
        "optional": ["tags", "source", "business_application"]
    },
    "learning_sessions": {
        "required": ["source", "key_takeaways"],
        "optional": ["business_application", "duration_minutes", "category"]
    },
    "auction_results": {
        "required": ["case_number"],
        "optional": ["property_address", "judgment_amount", "max_bid", "recommendation", "liens", "bcpao_data"]
    },
    "michael_swim_times": {
        "required": ["event", "time", "meet"],
        "optional": ["date", "place", "splits", "notes"]
    },
    "michael_nutrition": {
        "required": ["date", "day_type"],
        "optional": ["meals", "macros", "keto_compliant", "notes"]
    },
    "task_interventions": {
        "required": ["task_id", "level"],
        "optional": ["message", "user_response", "outcome"]
    },
    "health_logs": {
        "required": ["date"],
        "optional": ["sleep_hours", "energy_1_10", "focus_quality", "exercise", "notes"]
    }
}

# Valid domains for Life OS
VALID_DOMAINS = ["BUSINESS", "MICHAEL", "FAMILY", "PERSONAL"]

# Valid task states
VALID_STATES = ["INITIATED", "SOLUTION_PROVIDED", "IN_PROGRESS", "COMPLETED", "ABANDONED", "BLOCKED", "DEFERRED"]


def validate_data(table: str, data: dict) -> tuple[bool, Optional[str]]:
    """Validate data against table schema."""
    if table not in SCHEMAS:
        return False, f"Unknown table: {table}"
    
    schema = SCHEMAS[table]
    
    # Check required fields
    for field in schema["required"]:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Apply defaults
    if "defaults" in schema:
        for field, default in schema["defaults"].items():
            if field not in data:
                data[field] = default
    
    # Domain validation
    if "domain" in data and data["domain"] not in VALID_DOMAINS:
        return False, f"Invalid domain: {data['domain']}. Must be one of {VALID_DOMAINS}"
    
    # State validation
    if "state" in data and data["state"] not in VALID_STATES:
        return False, f"Invalid state: {data['state']}. Must be one of {VALID_STATES}"
    
    return True, None


def insert_data(table: str, data: dict) -> dict:
    """Insert data into Supabase table."""
    try:
        from supabase import create_client
    except ImportError:
        return {"success": False, "error": "supabase-py not installed"}
    
    url = os.environ.get("SUPABASE_URL", "https://mocerqjnksmhcjzxrewo.supabase.co")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")
    
    if not key:
        return {"success": False, "error": "SUPABASE_SERVICE_ROLE_KEY not set"}
    
    # Add timestamp
    data["created_at"] = datetime.utcnow().isoformat()
    
    try:
        client = create_client(url, key)
        result = client.table(table).insert(data).execute()
        
        return {
            "success": True,
            "rows_affected": len(result.data),
            "data": result.data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Insert data into Supabase")
    parser.add_argument("--table", required=True, help="Target table name")
    parser.add_argument("--data", required=True, help="JSON data to insert")
    parser.add_argument("--validate-only", action="store_true", help="Only validate, don't insert")
    
    args = parser.parse_args()
    
    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    
    # Validate
    valid, error = validate_data(args.table, data)
    if not valid:
        print(f"❌ Validation failed: {error}")
        sys.exit(1)
    
    print(f"✅ Validation passed for table: {args.table}")
    
    if args.validate_only:
        print(json.dumps({"valid": True, "data": data}, indent=2))
        sys.exit(0)
    
    # Insert
    result = insert_data(args.table, data)
    
    if result["success"]:
        print(f"✅ Inserted {result['rows_affected']} row(s)")
        print(json.dumps(result, indent=2))
        sys.exit(0)
    else:
        print(f"❌ Insert failed: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()

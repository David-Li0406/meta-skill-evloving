#!/usr/bin/env python3
"""
Validate Resume JSON Schema

Usage:
    python3 validate.py <resume_json>

Dependencies:
    pip install pydantic
"""

import sys
import argparse
import json
from typing import List, Optional
from pydantic import BaseModel, ValidationError


class WorkExperience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: Optional[str] = None
    description: str


class Education(BaseModel):
    school: str
    degree: str
    graduation_date: Optional[str] = None


class Resume(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience: List[WorkExperience] = []
    education: List[Education] = []


def validate_resume(json_data):
    try:
        Resume.model_validate(json_data)
        return True, "Valid"
    except ValidationError as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Validate resume JSON schema")
    parser.add_argument("resume_file", help="Path to resume JSON file")

    args = parser.parse_args()

    try:
        with open(args.resume_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    is_valid, message = validate_resume(data)

    if is_valid:
        print("✅ Resume JSON is valid")
        sys.exit(0)
    else:
        print("❌ Validation Failed", file=sys.stderr)
        print(message, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

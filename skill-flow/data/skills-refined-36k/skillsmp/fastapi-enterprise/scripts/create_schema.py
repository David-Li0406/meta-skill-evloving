#!/usr/bin/env python3
"""
Create Pydantic schema files.

Usage:
    python create_schema.py --name User --module auth
"""

import argparse
import sys
from pathlib import Path


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    result = []
    for i, char in enumerate(text):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def create_schema_file(
    schema_name: str,
    module: str = None,
) -> Path:
    """Create Pydantic schema file."""
    
    if module:
        schema_path = Path("schemas") / module / f"{to_snake_case(schema_name)}.py"
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py
        init_file = schema_path.parent / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
    else:
        schema_path = Path("schemas") / f"{to_snake_case(schema_name)}.py"
        schema_path.parent.mkdir(parents=True, exist_ok=True)
    
    if schema_path.exists():
        print(f"Error: Schema file {schema_path} already exists!")
        sys.exit(1)
    
    content = f'''"""
Pydantic schemas for {schema_name}.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class {schema_name}Base(BaseModel):
    """Base schema with common fields."""
    
    # TODO: Add common fields that are shared between Create/Update/Response
    # Example:
    # name: str = Field(..., min_length=1, max_length=255, description="Name")
    # description: Optional[str] = Field(None, max_length=1000, description="Description")
    pass


class {schema_name}Create(BaseModel):
    """Schema for creating a new {schema_name}."""
    
    # TODO: Add required fields for creation
    # Example:
    # name: str = Field(..., min_length=1, max_length=255, description="Name")
    # email: str = Field(..., description="Email address")
    # is_active: bool = Field(True, description="Active status")
    pass


class {schema_name}Update(BaseModel):
    """Schema for updating an existing {schema_name}."""
    
    # TODO: Add optional fields for update (all fields should be Optional)
    # Example:
    # name: Optional[str] = Field(None, min_length=1, max_length=255, description="Name")
    # email: Optional[str] = Field(None, description="Email address")
    # is_active: Optional[bool] = Field(None, description="Active status")
    pass


class {schema_name}Response(BaseModel):
    """Schema for {schema_name} response (from database)."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    # TODO: Add all fields from the model
    # Example:
    # name: str
    # email: str
    # is_active: bool
    created_at: datetime
    updated_at: datetime


class {schema_name}List(BaseModel):
    """Schema for paginated list of {schema_name}s."""
    
    items: list[{schema_name}Response]
    total: int
    page: int = 1
    page_size: int = 10
    total_pages: int
'''
    
    schema_path.write_text(content)
    return schema_path


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create Pydantic schema files"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Schema class name in PascalCase (e.g., User, ProductCategory)",
    )
    parser.add_argument(
        "--module",
        help="Module name for organizing schemas (e.g., auth, products)",
    )
    
    args = parser.parse_args()
    
    # Validate we're in a FastAPI project
    if not Path("schemas").exists():
        print("Error: Not in a FastAPI project root (schemas/ directory not found)")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    print(f"Creating schema: {args.name}")
    if args.module:
        print(f"Module: {args.module}")
    print()
    
    # Create schema file
    schema_path = create_schema_file(args.name, args.module)
    print(f"✅ Created schema: {schema_path}")
    
    print()
    print("Next steps:")
    print(f"1. Edit {schema_path} to add your fields")
    print(f"2. Import in your endpoint: from schemas.{args.module + '.' if args.module else ''}{to_snake_case(args.name)} import {args.name}Create, {args.name}Response")
    print("3. Use in endpoint type hints")
    print()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Create a new API endpoint with boilerplate code.

Usage:
    python create_endpoint.py --module user --service role --method post --path add-rule
    
Creates: api/routes/v1/user/role.py with add_rule endpoint
"""

import argparse
import sys
from pathlib import Path
from typing import Literal

MethodType = Literal["get", "post", "put", "delete", "patch"]


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    return text.replace("-", "_").replace(" ", "_").lower()


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase."""
    return "".join(word.capitalize() for word in text.replace("-", " ").split())


INIT_FILE = "__init__.py"


def create_endpoint_file(
    module: str,
    service: str,
    method: MethodType,
    path: str,
    version: str = "v1",
) -> None:
    """Create endpoint file with router and function."""
    
    # Build file path: api/routes/v1/user/role.py
    file_path = Path("api/routes") / version / module / f"{service}.py"
    
    # Create directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    for parent in [file_path.parent, file_path.parent.parent]:
        init_file = parent / INIT_FILE
        if not init_file.exists():
            init_file.write_text("")
    
    # Function name from path: add-rule -> add_rule
    function_name = to_snake_case(path)
    
    # Build endpoint content
    if file_path.exists():
        print(f"File {file_path} already exists. Adding new endpoint...")
        content = file_path.read_text()
        
        # Add new endpoint function
        new_endpoint = f'''

@router.{method}("/{path}")
async def {function_name}():
    """
    {method.upper()} /{path}
    
    TODO: Implement business logic
    """
    return {{"message": "{function_name} endpoint"}}
'''
        content += new_endpoint
        file_path.write_text(content)
        
    else:
        # Create new file with router
        content = f'''"""
{module.capitalize()} - {service.capitalize()} endpoints.

Auto-discovered routes for /{version}/{module}/{service}
Tag: {module.capitalize()} (auto-generated from parent folder)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.logging import get_logger

logger = get_logger(__name__)

# Router will be auto-discovered and registered
# Prefix: /api/{version}/{module}/{service}
# Tag: {module.capitalize()}
router = APIRouter()


@router.{method}("/{path}")
async def {function_name}(
    db: AsyncSession = Depends(get_db),
):
    """
    {method.upper()} /{path}
    
    TODO: Implement business logic
    - Add request/response schemas
    - Implement service layer call
    - Add authentication/authorization if needed
    """
    logger.info("{function_name} endpoint called")
    
    # TODO: Call service layer
    # result = await some_service.{function_name}(db)
    
    return {{"message": "{function_name} endpoint"}}
'''
        file_path.write_text(content)
    
    print(f"✅ Created endpoint: {file_path}")
    print(f"   URL: {method.upper()} /api/{version}/{module}/{service}/{path}")
    print(f"   Function: {function_name}()")
    print()
    print("Next steps:")
    print(f"1. Create schemas in: schemas/{module}/{service}.py")
    print(f"2. Create service in: services/{module}/{service}.py")
    print("3. Add authentication/authorization if needed")
    print("4. Test the endpoint: http://localhost:8000/docs")


def create_schema_file(module: str, service: str) -> None:
    """Create Pydantic schema file."""
    
    schema_path = Path("schemas") / module / f"{service}.py"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_file = schema_path.parent / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")
    
    if schema_path.exists():
        print(f"Schema file {schema_path} already exists.")
        return
    
    class_name = to_pascal_case(service)
    
    content = f'''"""
Pydantic schemas for {module}/{service}.
"""

from typing import Optional
from pydantic import BaseModel, Field


class {class_name}Base(BaseModel):
    """Base schema for {service}."""
    
    # TODO: Add common fields
    pass


class {class_name}Create(BaseModel):
    """Schema for creating {service}."""
    
    # TODO: Add required fields for creation
    name: str = Field(..., description="Name")


class {class_name}Update(BaseModel):
    """Schema for updating {service}."""
    
    # TODO: Add optional fields for update
    name: Optional[str] = Field(None, description="Name")


class {class_name}Response(BaseModel):
    """Schema for {service} response."""
    
    id: int
    name: str
    
    model_config = {{"from_attributes": True}}
'''
    
    schema_path.write_text(content)
    print(f"✅ Created schema: {schema_path}")


def create_service_file(module: str, service: str) -> None:
    """Create service layer file."""
    
    service_path = Path("services") / module / f"{service}.py"
    service_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_file = service_path.parent / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")
    
    if service_path.exists():
        print(f"Service file {service_path} already exists.")
        return
    
    class_name = to_pascal_case(service)
    
    content = f'''"""
Business logic for {module}/{service}.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
# from models.{module} import {class_name}Model
# from schemas.{module}.{service} import {class_name}Create, {class_name}Update, {class_name}Response

logger = get_logger(__name__)


class {class_name}Service:
    """Service layer for {service} business logic."""
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List:
        """Get all {service}s."""
        logger.info("Getting all {service}s")
        
        # TODO: Implement query
        # result = await db.execute(select({class_name}Model))
        # return result.scalars().all()
        
        return []
    
    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int) -> Optional:
        """Get {service} by ID."""
        logger.info("Getting {service}", item_id=item_id)
        
        # TODO: Implement query
        # result = await db.execute(
        #     select({class_name}Model).where({class_name}Model.id == item_id)
        # )
        # return result.scalar_one_or_none()
        
        return None
    
    @staticmethod
    async def create(db: AsyncSession, data) -> None:
        """Create new {service}."""
        logger.info("Creating {service}", data=data)
        
        # TODO: Implement creation
        # item = {class_name}Model(**data.model_dump())
        # db.add(item)
        # await db.commit()
        # await db.refresh(item)
        # return item
        
        pass
    
    @staticmethod
    async def update(db: AsyncSession, item_id: int, data) -> Optional:
        """Update {service}."""
        logger.info("Updating {service}", item_id=item_id, data=data)
        
        # TODO: Implement update
        # item = await {class_name}Service.get_by_id(db, item_id)
        # if not item:
        #     return None
        #
        # for key, value in data.model_dump(exclude_unset=True).items():
        #     setattr(item, key, value)
        #
        # await db.commit()
        # await db.refresh(item)
        # return item
        
        return None
    
    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> bool:
        """Delete {service}."""
        logger.info("Deleting {service}", item_id=item_id)
        
        # TODO: Implement deletion
        # item = await {class_name}Service.get_by_id(db, item_id)
        # if not item:
        #     return False
        #
        # await db.delete(item)
        # await db.commit()
        # return True
        
        return False


# Singleton instance
{service}_service = {class_name}Service()
'''
    
    service_path.write_text(content)
    print(f"✅ Created service: {service_path}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new API endpoint with boilerplate"
    )
    parser.add_argument(
        "--module",
        required=True,
        help="Module name (e.g., user, product)",
    )
    parser.add_argument(
        "--service",
        required=True,
        help="Service name (e.g., role, category)",
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=["get", "post", "put", "delete", "patch"],
        help="HTTP method",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Endpoint path (e.g., add-rule, list-all)",
    )
    parser.add_argument(
        "--version",
        default="v1",
        help="API version (default: v1)",
    )
    parser.add_argument(
        "--with-schema",
        action="store_true",
        help="Also create schema file",
    )
    parser.add_argument(
        "--with-service",
        action="store_true",
        help="Also create service file",
    )
    
    args = parser.parse_args()
    
    # Validate we're in a FastAPI project
    if not Path("api/routes").exists():
        print("Error: Not in a FastAPI project root (api/routes not found)")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    print(f"Creating endpoint: {args.method.upper()} /api/{args.version}/{args.module}/{args.service}/{args.path}")
    print()
    
    create_endpoint_file(
        args.module,
        args.service,
        args.method,
        args.path,
        args.version,
    )
    
    if args.with_schema:
        create_schema_file(args.module, args.service)
    
    if args.with_service:
        create_service_file(args.module, args.service)
    
    print()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

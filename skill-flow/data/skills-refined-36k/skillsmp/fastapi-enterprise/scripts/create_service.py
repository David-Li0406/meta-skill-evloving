#!/usr/bin/env python3
"""
Create service layer file with business logic template.

Usage:
    python create_service.py --name User --module auth
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


def create_service_file(
    service_name: str,
    module: str = None,
) -> Path:
    """Create service layer file."""
    
    if module:
        service_path = Path("services") / module / f"{to_snake_case(service_name)}.py"
        service_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py
        init_file = service_path.parent / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
    else:
        service_path = Path("services") / f"{to_snake_case(service_name)}.py"
        service_path.parent.mkdir(parents=True, exist_ok=True)
    
    if service_path.exists():
        print(f"Error: Service file {service_path} already exists!")
        sys.exit(1)
    
    snake_name = to_snake_case(service_name)
    
    content = f'''"""
Business logic for {service_name}.

This service handles all business operations related to {service_name}.
Keep database-specific code in models, business logic here.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
# from models.{module + '.' if module else ''}{snake_name} import {service_name}
# from schemas.{module + '.' if module else ''}{snake_name} import (
#     {service_name}Create,
#     {service_name}Update,
#     {service_name}Response,
# )

logger = get_logger(__name__)


class {service_name}Service:
    """Service layer for {service_name} business logic."""
    
    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List:
        """
        Get all {service_name}s with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of {service_name} objects
        """
        logger.info("Getting all {snake_name}s", skip=skip, limit=limit)
        
        # TODO: Implement query
        # stmt = select({service_name}).offset(skip).limit(limit)
        # result = await db.execute(stmt)
        # return result.scalars().all()
        
        return []
    
    async def get_by_id(
        self,
        db: AsyncSession,
        item_id: int,
    ) -> Optional:
        """
        Get {service_name} by ID.
        
        Args:
            db: Database session
            item_id: ID of the {service_name}
            
        Returns:
            {service_name} object or None if not found
        """
        logger.info("Getting {snake_name} by ID", item_id=item_id)
        
        # TODO: Implement query
        # stmt = select({service_name}).where({service_name}.id == item_id)
        # result = await db.execute(stmt)
        # return result.scalar_one_or_none()
        
        return None
    
    async def create(
        self,
        db: AsyncSession,
        data,  # TODO: Type as {service_name}Create
    ):
        """
        Create a new {service_name}.
        
        Args:
            db: Database session
            data: {service_name} creation data
            
        Returns:
            Created {service_name} object
        """
        logger.info("Creating {snake_name}", data=data)
        
        # TODO: Add business logic validation
        # Example: Check if name already exists, validate business rules, etc.
        
        # TODO: Implement creation
        # item = {service_name}(**data.model_dump())
        # db.add(item)
        # await db.commit()
        # await db.refresh(item)
        # return item
        
        pass
    
    async def update(
        self,
        db: AsyncSession,
        item_id: int,
        data,  # TODO: Type as {service_name}Update
    ) -> Optional:
        """
        Update an existing {service_name}.
        
        Args:
            db: Database session
            item_id: ID of the {service_name} to update
            data: Update data
            
        Returns:
            Updated {service_name} object or None if not found
        """
        logger.info("Updating {snake_name}", item_id=item_id, data=data)
        
        # Get existing item
        item = await self.get_by_id(db, item_id)
        if not item:
            logger.warning("{service_name} not found", item_id=item_id)
            return None
        
        # TODO: Add business logic validation
        
        # Update fields
        # for key, value in data.model_dump(exclude_unset=True).items():
        #     setattr(item, key, value)
        
        # await db.commit()
        # await db.refresh(item)
        # return item
        
        return None
    
    async def delete(
        self,
        db: AsyncSession,
        item_id: int,
    ) -> bool:
        """
        Delete a {service_name}.
        
        Args:
            db: Database session
            item_id: ID of the {service_name} to delete
            
        Returns:
            True if deleted, False if not found
        """
        logger.info("Deleting {snake_name}", item_id=item_id)
        
        # Get existing item
        item = await self.get_by_id(db, item_id)
        if not item:
            logger.warning("{service_name} not found", item_id=item_id)
            return False
        
        # TODO: Add business logic checks
        # Example: Check if item can be deleted (no dependencies, etc.)
        
        # await db.delete(item)
        # await db.commit()
        # return True
        
        return False
    
    async def count(self, db: AsyncSession) -> int:
        """
        Get total count of {service_name}s.
        
        Args:
            db: Database session
            
        Returns:
            Total count
        """
        logger.info("Counting {snake_name}s")
        
        # TODO: Implement count
        # from sqlalchemy import func
        # stmt = select(func.count()).select_from({service_name})
        # result = await db.execute(stmt)
        # return result.scalar_one()
        
        return 0


# Singleton instance for use in endpoints
{snake_name}_service = {service_name}Service()
'''
    
    service_path.write_text(content)
    return service_path


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create service layer file with business logic"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Service class name in PascalCase (e.g., User, ProductCategory)",
    )
    parser.add_argument(
        "--module",
        help="Module name for organizing services (e.g., auth, products)",
    )
    
    args = parser.parse_args()
    
    # Validate we're in a FastAPI project
    if not Path("services").exists():
        print("Error: Not in a FastAPI project root (services/ directory not found)")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    print(f"Creating service: {args.name}")
    if args.module:
        print(f"Module: {args.module}")
    print()
    
    # Create service file
    service_path = create_service_file(args.name, args.module)
    print(f"✅ Created service: {service_path}")
    
    print()
    print("Next steps:")
    print(f"1. Edit {service_path} to implement business logic")
    print(f"2. Import in your endpoint: from services.{args.module + '.' if args.module else ''}{to_snake_case(args.name)} import {to_snake_case(args.name)}_service")
    print(f"3. Use in endpoint: result = await {to_snake_case(args.name)}_service.get_all(db)")
    print()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

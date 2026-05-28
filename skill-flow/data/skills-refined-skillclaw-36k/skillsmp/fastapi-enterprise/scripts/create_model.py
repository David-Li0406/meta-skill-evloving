#!/usr/bin/env python3
"""
Create a new SQLAlchemy model and generate Alembic migration.

Usage:
    python create_model.py --name User --table users --module auth
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    result = []
    for i, char in enumerate(text):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


INIT_FILE = "__init__.py"


def create_model_file(
    model_name: str,
    table_name: str,
    module: Optional[str] = None,
) -> Path:
    """Create SQLAlchemy model file."""
    
    if module:
        model_path = Path("models") / module / f"{to_snake_case(model_name)}.py"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py
        init_file = model_path.parent / INIT_FILE
        if not init_file.exists():
            init_file.write_text("")
    else:
        model_path = Path("models") / f"{to_snake_case(model_name)}.py"
        model_path.parent.mkdir(parents=True, exist_ok=True)
    
    if model_path.exists():
        print(f"Error: Model file {model_path} already exists!")
        sys.exit(1)
    
    content = f'''"""
{model_name} database model.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class {model_name}(Base):
    """
    {model_name} model.
    
    TODO: Add model description and business logic
    """
    
    __tablename__ = "{table_name}"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # TODO: Add your fields here
    # Example fields:
    # name: Mapped[str] = mapped_column(String(255), nullable=False)
    # email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # is_active: Mapped[bool] = mapped_column(default=True)
    # description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    
    # Timestamps (recommended for all models)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<{model_name}(id={{self.id}})>"
'''
    
    model_path.write_text(content)
    return model_path


def update_models_init(module: Optional[str], model_name: str) -> None:
    """Update models/__init__.py to import new model."""
    
    if module:
        init_path = Path("models") / module / INIT_FILE
    else:
        init_path = Path("models") / INIT_FILE
    
    # Read existing content
    if init_path.exists():
        content = init_path.read_text()
    else:
        content = '"""Database models."""\n\n'
    
    # Add import if not already present
    import_line = f"from .{to_snake_case(model_name)} import {model_name}\n"
    if import_line not in content:
        content += import_line
    
    # Add to __all__ if exists
    if "__all__" in content:
        # Find __all__ list and add model
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "__all__" in line and model_name not in line:
                # Add to existing __all__
                if "]" in line:
                    lines[i] = line.replace("]", f', "{model_name}"]')
                else:
                    # Multi-line __all__
                    for j in range(i, len(lines)):
                        if "]" in lines[j]:
                            lines[j] = lines[j].replace("]", f'    "{model_name}",\n]')
                            break
                break
        content = "\n".join(lines)
    else:
        # Add __all__
        content += f'\n__all__ = ["{model_name}"]\n'
    
    init_path.write_text(content)


def generate_migration(model_name: str, message: Optional[str] = None) -> None:
    """Generate Alembic migration."""
    
    migration_message = message or f"Add {model_name} model"
    
    print(f"\n🔄 Generating Alembic migration: {migration_message}")
    
    try:
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", migration_message],
            capture_output=True,
            text=True,
            check=True,
        )
        
        print("✅ Migration generated successfully!")
        print(result.stdout)
        
        if result.stderr:
            print("Warnings:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate migration: {e}")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Alembic not found. Make sure it's installed and alembic.ini exists.")
        print("Run: pip install alembic")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new SQLAlchemy model and migration"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Model class name in PascalCase (e.g., User, ProductCategory)",
    )
    parser.add_argument(
        "--table",
        required=True,
        help="Database table name in snake_case (e.g., users, product_categories)",
    )
    parser.add_argument(
        "--module",
        help="Module name for organizing models (e.g., auth, products)",
    )
    parser.add_argument(
        "--message",
        help="Custom migration message (default: 'Add {ModelName} model')",
    )
    parser.add_argument(
        "--no-migration",
        action="store_true",
        help="Don't generate Alembic migration (only create model file)",
    )
    
    args = parser.parse_args()
    
    # Validate we're in a FastAPI project
    if not Path("models").exists():
        print("Error: Not in a FastAPI project root (models/ directory not found)")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    print(f"Creating model: {args.name}")
    print(f"Table name: {args.table}")
    if args.module:
        print(f"Module: {args.module}")
    print()
    
    # Create model file
    model_path = create_model_file(args.name, args.table, args.module)
    print(f"✅ Created model: {model_path}")
    
    # Update __init__.py
    update_models_init(args.module, args.name)
    print("✅ Updated models/__init__.py")
    
    # Import the model to make it available to Alembic
    print("\n⚠️  Important: Edit the model file to add your fields before generating migration!")
    print(f"   File: {model_path}")
    print()
    
    if not args.no_migration:
        response = input("Generate migration now? (y/N): ")
        if response.lower() == "y":
            generate_migration(args.name, args.message)
            print()
            print("Next steps:")
            print("1. Review migration file in alembic/versions/")
            print("2. Apply migration: alembic upgrade head")
        else:
            print()
            print("To generate migration later, run:")
            print(f'  alembic revision --autogenerate -m "Add {args.name} model"')
    
    print()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

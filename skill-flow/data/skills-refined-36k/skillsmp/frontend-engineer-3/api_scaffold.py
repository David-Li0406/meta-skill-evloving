import os
import sys

def scaffold_api_domain(domain, entity_name):
    base_dir = r"d:\Alders360\sportsmanagement\app\domains"
    domain_path = os.path.join(base_dir, domain)
    
    # Create directory structure matching sportsmanagement/app
    dirs = ["routes", "services", "repositories", "models"]
    for d in dirs:
        path = os.path.join(domain_path, d)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "__init__.py"), "w") as f:
            pass

    entity_lower = entity_name.lower()

    # 1. Repository Scaffold
    repo_content = f"""from sqlalchemy.orm import Session
from app.db.models import {entity_name} # Central models file

class {entity_name}Repository:
    def __init__(self, db: Session):
        self.db = db

    async def get_all(self):
        # Implement high-speed query
        return self.db.query({entity_name}).all()
"""
    with open(os.path.join(domain_path, "repositories", f"{entity_lower}_repository.py"), "w") as f:
        f.write(repo_content)

    # 2. Service Scaffold
    service_content = f"""from app.domains.{domain}.repositories.{entity_lower}_repository import {entity_name}Repository

class {entity_name}Service:
    def __init__(self, repo: {entity_name}Repository):
        self.repo = repo

    async def get_{entity_lower}s(self):
        return await self.repo.get_all()
"""
    with open(os.path.join(domain_path, "services", f"{entity_lower}_service.py"), "w") as f:
        f.write(service_content)

    # 3. Model Scaffold (Pydantic Schemas - as per project convention)
    model_content = f"""from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class {entity_name}Base(BaseModel):
    pass

class {entity_name}Response(BaseModel):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
"""
    with open(os.path.join(domain_path, "models", f"{entity_lower}.py"), "w") as f:
        f.write(model_content)

    # 4. Route Scaffold
    route_content = f"""from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.domains.{domain}.services.{entity_lower}_service import {entity_name}Service
from app.domains.{domain}.repositories.{entity_lower}_repository import {entity_name}Repository
from app.domains.{domain}.models.{entity_lower} import {entity_name}Response
from typing import List

# NOTE: Centralized error handling is managed in app/main.py 
# via RequestValidationError and Exception handlers.

router = APIRouter(prefix="/{domain}/{entity_lower}", tags=["{domain}"])

def get_{entity_lower}_service(db: Session = Depends(get_db)):
    repo = {entity_name}Repository(db)
    return {entity_name}Service(repo)

@router.get("/", response_model=List[{entity_name}Response])
async def list_{entity_lower}s(service: {entity_name}Service = Depends(get_{entity_lower}_service)):
    \"\"\"
    List all {entity_lower} entities.
    Errors are handled globally in main.py.
    \"\"\"
    try:
        return await service.get_{entity_lower}s()
    except Exception as e:
        # Global handler in main.py will catch unexpected errors
        raise e
"""
    with open(os.path.join(domain_path, "routes", f"{entity_lower}_routes.py"), "w") as f:
        f.write(route_content)

    print(f"Scaffolded enterprise domain '{domain}' for entity '{entity_name}' in {domain_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python api_scaffold.py <domain> <entity_name>")
    else:
        scaffold_api_domain(sys.argv[1], sys.argv[2])

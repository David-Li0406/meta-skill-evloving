import os
import sys

def scaffold_db_model(domain, model_name, partitioned=False):
    base_dir = r"d:\Alders360\sportsmanagement\app"
    domain_path = os.path.join(base_dir, "domains", domain)
    models_path = os.path.join(domain_path, "models")
    
    if not os.path.exists(models_path):
        os.makedirs(models_path)
        with open(os.path.join(models_path, "__init__.py"), "w") as f:
            pass

    # System Design Features:
    # 1. Declarative Partitioning support
    # 2. Composite Indexing for high-speed queries
    # 3. Soft Delete pattern (is_deleted)
    # 4. JSONB for flexibile metadata
    
    partition_meta = ""
    if partitioned:
        partition_meta = f', postgresql_partition_by="RANGE(created_at)"'

    file_content = f"""from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Index, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class {model_name}(Base):
    __tablename__ = "{domain}_{model_name.lower()}s"
    __table_args__ = (
        Index("idx_{domain}_{model_name.lower()}_user_created", "created_at", text("user_id")),
        {partition_meta}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft Delete for Enterprise Integrity
    is_deleted = Column(Boolean, default=False, index=True)
    
    # Flexible metadata for evolving metrics
    meta_data = Column(JSONB, server_default=text("'{{}}'"))

    # Relationships
    # user = relationship("User", back_populates="{model_name.lower()}s")
"""
    
    file_path = os.path.join(models_path, f"{model_name.lower()}.py")
    with open(file_path, "w") as f:
        f.write(file_content)
    
    # Scaffold Materialized View Skeleton
    view_path = os.path.join(domain_path, "queries")
    os.makedirs(view_path, exist_ok=True)
    with open(os.path.join(view_path, f"mv_{model_name.lower()}_stats.sql"), "w") as f:
        f.write(f"-- Materialized View for O(1) performance\nCREATE MATERIALIZED VIEW mv_{domain}_{model_name.lower()}_stats AS\nSELECT user_id, count(*)\nFROM {domain}_{model_name.lower()}s\nWHERE is_deleted = false\nGROUP BY user_id;\n\nCREATE INDEX idx_mv_{domain}_{model_name.lower()}_user ON mv_{domain}_{model_name.lower()}_stats(user_id);")

    print(f"Scaffolded enterprise model {model_name} in {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python db_init.py <domain> <model_name> [partitioned=True|False]")
    else:
        is_part = sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False
        scaffold_db_model(sys.argv[1], sys.argv[2], is_part)

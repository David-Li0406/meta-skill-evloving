# Models & Schemas

## The Golden Rule

**Models = Database**
**Schemas = API**

Never expose models directly to API responses. Always use Pydantic schemas.

---

## SQLAlchemy Models (Database)

### Basic Model
```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Article(Base):
    __tablename__ = "article"

    article_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    full_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    source_url = Column(Text)  # Direct URL instead of foreign key

    # Relationships
    projects = relationship(
        "Project",
        secondary="article_describes_project",
        back_populates="articles"
    )
```

### Relationships

**One-to-Many:**
```python
# models.py
class City(Base):
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String, unique=True, nullable=False)

    # One city has many projects
    projects = relationship("Project", back_populates="city")


class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"))

    # Many projects belong to one city
    city = relationship("City", back_populates="projects")
```

**Many-to-Many:**
```python
# Association table
article_projects = Table(
    "article_projects",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.article_id")),
    Column("project_id", Integer, ForeignKey("projects.project_id"))
)

class Article(Base):
    # ...
    projects = relationship(
        "Project",
        secondary=article_projects,
        back_populates="articles"
    )

class Project(Base):
    # ...
    articles = relationship(
        "Article",
        secondary=article_projects,
        back_populates="projects"
    )
```

---

## Pydantic Schemas (API)

### Input Schema (Create/Update)
```python
# schemas.py
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    """For POST /articles - input validation"""
    title: str = Field(min_length=1, max_length=500)
    full_text: Optional[str] = None
    source_url: Optional[str] = None

    # Custom validation
    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
```

### Response Schema (Output)
```python
class ArticleResponse(BaseModel):
    """For API responses - serialization"""
    article_id: int
    title: str
    full_text: Optional[str]
    created_at: datetime
    source_url: Optional[str]

    # Enable ORM mode to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

# Usage:
@app.get("/articles/{id}", response_model=ArticleResponse)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(
        models.Article.article_id == id
    ).first()
    if not article:
        raise HTTPException(status_code=404)
    return article  # Pydantic auto-converts SQLAlchemy model
```

### Nested Schemas
```python
class ProjectResponse(BaseModel):
    project_id: int
    project_name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ArticleWithProjectsResponse(BaseModel):
    """Response with nested project data"""
    article_id: int
    title: str
    created_at: datetime
    source_url: Optional[str]
    projects: List[ProjectResponse]  # Nested schema

    model_config = ConfigDict(from_attributes=True)

# FastAPI automatically handles nested serialization!
```

---

## Common Patterns

### Pattern: Separate Create/Update/Response

```python
# Input for creating
class CityCreate(BaseModel):
    city_name: str = Field(min_length=1, max_length=100)

# Input for updating (all fields optional)
class CityUpdate(BaseModel):
    city_name: Optional[str] = Field(None, min_length=1, max_length=100)

# Output for responses
class CityResponse(BaseModel):
    city_id: int
    city_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### Pattern: Inherit to Reduce Duplication

```python
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str  # Only for input

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    # No password field!

    model_config = ConfigDict(from_attributes=True)
```

### Pattern: List Responses

```python
from typing import List

class ArticleListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    results: List[ArticleResponse]

@app.get("/articles", response_model=ArticleListResponse)
def list_articles(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    total = db.query(models.Article).count()
    articles = db.query(models.Article).offset(skip).limit(limit).all()

    return ArticleListResponse(
        total=total,
        skip=skip,
        limit=limit,
        results=articles  # Pydantic converts each
    )
```

---

## Field Validation

### Built-in Validators
```python
from pydantic import Field, HttpUrl, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    age: int = Field(ge=0, le=120)  # Greater/equal, less/equal
    username: str = Field(min_length=3, max_length=50)
    website: Optional[HttpUrl] = None  # Validates URL format
    password: constr(min_length=8)  # Constrained string
```

### Custom Validators
```python
from pydantic import field_validator

class ArticleCreate(BaseModel):
    title: str
    tags: List[str]

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        if len(v) > 10:
            raise ValueError("Maximum 10 tags allowed")
        return [tag.lower().strip() for tag in v]

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if "spam" in v.lower():
            raise ValueError("Spam detected in title")
        return v
```

---

## Model Configuration

### ConfigDict Options
```python
from pydantic import ConfigDict

class ArticleResponse(BaseModel):
    article_id: int
    title: str

    model_config = ConfigDict(
        from_attributes=True,    # Enable ORM mode (SQLAlchemy)
        populate_by_name=True,    # Allow field population by alias
        str_strip_whitespace=True # Auto-strip strings
    )
```

---

## Computed Fields

```python
from pydantic import computed_field

class ArticleResponse(BaseModel):
    article_id: int
    title: str
    full_text: Optional[str]

    @computed_field
    @property
    def preview(self) -> str:
        """First 100 characters of full_text"""
        if not self.full_text:
            return ""
        return self.full_text[:100] + "..." if len(self.full_text) > 100 else self.full_text

    model_config = ConfigDict(from_attributes=True)

# Response includes "preview" field automatically!
```

---

## Security: NEVER Expose Sensitive Fields

```python
# ❌ NEVER DO THIS
class UserResponse(BaseModel):
    id: int
    email: str
    hashed_password: str  # DANGEROUS!

# ✅ ALWAYS DO THIS
class UserResponse(BaseModel):
    id: int
    email: str
    # No password fields at all!

    model_config = ConfigDict(from_attributes=True)
```

---

## Quick Reference

### Common Field Types
```python
from pydantic import HttpUrl, EmailStr, UUID4, Json
from datetime import datetime, date
from typing import Optional, List, Dict

str           # String
int           # Integer
float         # Float
bool          # Boolean
datetime      # Datetime
date          # Date
EmailStr      # Validated email
HttpUrl       # Validated URL
UUID4         # UUID
Json          # JSON data
Optional[str] # Can be None
List[str]     # List of strings
Dict[str, Any] # Dictionary
```

### Common Validations
```python
Field(gt=0)              # Greater than 0
Field(ge=0)              # Greater or equal to 0
Field(lt=100)            # Less than 100
Field(le=100)            # Less or equal to 100
Field(min_length=1)      # Min string length
Field(max_length=100)    # Max string length
Field(regex=r'^[a-z]+$') # Regex pattern
Field(default=0)         # Default value
```

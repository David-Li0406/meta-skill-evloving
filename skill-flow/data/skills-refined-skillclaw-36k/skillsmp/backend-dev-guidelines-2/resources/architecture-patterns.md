# Architecture & Patterns

## Layered Architecture Deep Dive

### Layer Responsibilities

**Routes Layer (FastAPI endpoints)**
- Define HTTP endpoints
- Extract request parameters
- Call service layer
- Return responses
- **NO business logic**

**Service Layer**
- Business logic and orchestration
- Coordinate between multiple repositories
- Implement business rules
- Handle transactions
- Call external APIs if needed

**Repository Layer (Optional - only for complex queries)**
- Complex database queries
- Query optimization
- Joins and aggregations
- Raw SQL if needed

**Model Layer (SQLAlchemy)**
- Database schema definition
- Relationships
- Table structure

---

## When to Extract to Services

### Current Pattern (Acceptable for Simple CRUD)
```python
# main.py
@app.post("/articles/")
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Article).filter(
        models.Article.source_url == article.source_url
    ).first()
    if existing:
        return existing

    db_article = models.Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
```

**This is FINE when:**
- Logic is <20 lines
- Single model/table
- No complex business rules
- Used in only one endpoint

### When to Extract to Service
```python
# When logic grows to this complexity:
@app.post("/ingest/reddit-json/")
async def ingest_json_payload(payload: List[dict], db: Session = Depends(get_db)):
    articles_created = 0
    projects_created = 0
    # ... 100+ lines of logic
    # Multiple models (City, Project, Article)
    # Complex relationships
    # Error handling
    # Used in 2 endpoints (file + JSON)
```

**Extract to service when:**
- Logic is >30 lines
- Multiple models involved
- Complex business rules
- Needs to be reused
- Needs unit testing

### Refactored with Service
```python
# services/ingest_service.py
from typing import List, Dict
from sqlalchemy.orm import Session
from app import models, schemas

class IngestionStats:
    def __init__(self):
        self.articles_created = 0
        self.projects_created = 0
        self.cities_created = 0
        self.errors: List[str] = []

class IngestionService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_reddit_posts(
        self,
        posts: List[Dict]
    ) -> IngestionStats:
        """Ingest Reddit posts with full transaction safety."""
        stats = IngestionStats()

        try:
            for idx, post_data in enumerate(posts):
                try:
                    post = schemas.RedditPost(**post_data)

                    # Get or create city
                    city = self._get_or_create_city(post.city)
                    if city.city_id is None:
                        stats.cities_created += 1

                    # Get or create project
                    project = self._get_or_create_project(
                        post.project,
                        city.city_id
                    )
                    if project.project_id is None:
                        stats.projects_created += 1

                    # Create article
                    article = self._create_article(post)
                    article.projects.append(project)
                    stats.articles_created += 1

                except Exception as e:
                    stats.errors.append(f"Error at post {idx}: {str(e)}")
                    continue

            self.db.commit()
            return stats

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def _get_or_create_city(self, city_name: str) -> models.City:
        city = self.db.query(models.City).filter(
            models.City.city_name == city_name
        ).first()

        if not city:
            city = models.City(city_name=city_name)
            self.db.add(city)
            self.db.flush()

        return city

    def _get_or_create_project(
        self,
        project_name: str,
        city_id: int
    ) -> models.Project:
        project = self.db.query(models.Project).filter(
            models.Project.project_name == project_name,
            models.Project.city_id == city_id
        ).first()

        if not project:
            project = models.Project(
                project_name=project_name,
                city_id=city_id
            )
            self.db.add(project)
            self.db.flush()

        return project

    def _create_article(
        self,
        post: schemas.RedditPost
    ) -> models.Article:
        try:
            created_at = datetime.fromisoformat(
                post.created_at.replace("Z", "+00:00")
            )
        except:
            created_at = datetime.utcnow()

        article = models.Article(
            title=post.title,
            full_text=post.full_text,
            created_at=created_at,
            source_url=post.source_url,
            raw_data=post.model_dump()
        )
        self.db.add(article)
        self.db.flush()
        return article


# routes/reddit.py
@router.post("/ingest/reddit-json/")
async def ingest_reddit_json(
    payload: List[dict],
    db: Session = Depends(get_db)
):
    """Ingest Reddit posts from JSON payload."""
    service = IngestionService(db)
    stats = service.ingest_reddit_posts(payload)

    return {
        "success": True,
        "articles_created": stats.articles_created,
        "projects_created": stats.projects_created,
        "cities_created": stats.cities_created,
        "errors": stats.errors
    }
```

---

## When to Create Repositories

**Only create repositories for:**
1. Complex queries with multiple joins
2. Raw SQL queries
3. Query optimization concerns
4. Reusable query patterns

### Example: Article Search (Complex enough for Repository)

```python
# repositories/article_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models

class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query: Optional[str] = None,
        city: Optional[str] = None,
        project: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[models.Article], int]:
        """
        Complex search with joins and filters.
        Returns (results, total_count)
        """
        articles_query = self.db.query(models.Article)

        # Text search
        if query:
            articles_query = articles_query.filter(
                or_(
                    models.Article.title.ilike(f"%{query}%"),
                    models.Article.full_text.ilike(f"%{query}%")
                )
            )

        # Join for city/project filters
        if city or project:
            articles_query = articles_query.join(
                models.Article.projects
            ).join(
                models.Project.city
            )

            if city:
                articles_query = articles_query.filter(
                    models.City.city_name.ilike(f"%{city}%")
                )

            if project:
                articles_query = articles_query.filter(
                    models.Project.project_name.ilike(f"%{project}%")
                )

        total = articles_query.count()
        results = articles_query.offset(skip).limit(limit).all()

        return results, total


# services/article_service.py
class ArticleService:
    def __init__(self, db: Session):
        self.repo = ArticleRepository(db)

    def search_articles(
        self,
        query: Optional[str],
        city: Optional[str],
        project: Optional[str],
        skip: int,
        limit: int
    ):
        results, total = self.repo.search(query, city, project, skip, limit)

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "results": [
                schemas.ArticleResponse.model_validate(r)
                for r in results
            ]
        }


# routes/articles.py
@router.get("/search")
def search_articles(
    query: Optional[str] = None,
    city: Optional[str] = None,
    project: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = ArticleService(db)
    return service.search_articles(query, city, project, skip, limit)
```

---

## Dependency Injection Patterns

### Basic Pattern (Already using this!)
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
```

### Service Injection Pattern
```python
# Services with dependency injection
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@app.get("/users")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()
```

### Settings Injection Pattern
```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

@app.get("/config")
def show_config(settings: Settings = Depends(get_settings)):
    return {"db": settings.database_url}
```

---

## Summary: When to Use Each Layer

| Complexity | Pattern | Example |
|------------|---------|---------|
| Simple CRUD (< 20 lines) | Route only | Get/Create single model |
| Medium logic (20-50 lines) | Route + inline logic | Simple business rules |
| Complex logic (> 50 lines) | Route → Service | Multiple models, transactions |
| Complex queries | Route → Service → Repository | Joins, aggregations, search |

**Start simple, refactor when needed!**

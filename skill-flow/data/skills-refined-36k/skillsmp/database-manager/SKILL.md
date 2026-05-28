---
name: database-manager
description: Manage PostgreSQL database for NutriProfile. Use this skill when working with SQLAlchemy models, Alembic migrations, query optimization, or database schema changes. Covers async operations and Fly Postgres deployment.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile Database Manager Skill

You are a database management expert for the NutriProfile application. This skill helps you work with PostgreSQL, SQLAlchemy async, and Alembic migrations.

## Database Stack

- **Database**: PostgreSQL (Fly Postgres in production)
- **ORM**: SQLAlchemy 2.0 with async support
- **Migrations**: Alembic
- **Connection**: asyncpg driver

## Connection Configuration

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/nutriprofile"

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# backend/app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set True for SQL logging
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## SQLAlchemy Models

### Model Structure

```
backend/app/models/
├── __init__.py
├── user.py           # User, authentication
├── profile.py        # Nutritional profile
├── food_log.py       # FoodLog, FoodItem, DailyNutrition
├── recipe.py         # Recipe, FavoriteRecipe, RecipeHistory
├── activity.py       # ActivityLog, WeightLog, Goal
├── gamification.py   # Achievement, Streak, UserStats, Notification
└── subscription.py   # Subscription
```

### Model Example

```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    preferred_language = Column(String(5), default="en")
    subscription_tier = Column(String(20), default="free")
    trial_ends_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    food_logs = relationship("FoodLog", back_populates="user")
    recipes = relationship("Recipe", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

### Relationship Patterns

```python
# One-to-One
class User(Base):
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="profile")

# One-to-Many
class User(Base):
    food_logs = relationship("FoodLog", back_populates="user")

class FoodLog(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="food_logs")

# Many-to-Many
class Recipe(Base):
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes")

class Tag(Base):
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags")

recipe_tags = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id")),
    Column("tag_id", ForeignKey("tags.id"))
)
```

## Async Database Operations

### CRUD Operations

```python
# backend/app/services/recipe.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recipe import Recipe

class RecipeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # CREATE
    async def create(self, user_id: int, data: RecipeCreate) -> Recipe:
        recipe = Recipe(
            user_id=user_id,
            **data.model_dump()
        )
        self.db.add(recipe)
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    # READ (single)
    async def get(self, recipe_id: int, user_id: int) -> Recipe | None:
        result = await self.db.execute(
            select(Recipe).where(
                Recipe.id == recipe_id,
                Recipe.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    # READ (list)
    async def get_all(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> list[Recipe]:
        result = await self.db.execute(
            select(Recipe)
            .where(Recipe.user_id == user_id)
            .order_by(Recipe.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # UPDATE
    async def update(
        self,
        recipe_id: int,
        user_id: int,
        data: RecipeUpdate
    ) -> Recipe | None:
        recipe = await self.get(recipe_id, user_id)
        if not recipe:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(recipe, key, value)

        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    # DELETE
    async def delete(self, recipe_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            delete(Recipe).where(
                Recipe.id == recipe_id,
                Recipe.user_id == user_id
            )
        )
        await self.db.commit()
        return result.rowcount > 0
```

### Complex Queries

```python
# Aggregation
from sqlalchemy import func

async def get_daily_calories(user_id: int, date: date) -> float:
    result = await self.db.execute(
        select(func.sum(FoodLog.total_calories))
        .where(
            FoodLog.user_id == user_id,
            func.date(FoodLog.created_at) == date
        )
    )
    return result.scalar() or 0.0

# Join with eager loading
from sqlalchemy.orm import selectinload

async def get_user_with_profile(user_id: int) -> User:
    result = await self.db.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# Subquery
from sqlalchemy import select

subquery = (
    select(FoodLog.user_id, func.count(FoodLog.id).label("log_count"))
    .group_by(FoodLog.user_id)
    .subquery()
)

result = await self.db.execute(
    select(User, subquery.c.log_count)
    .outerjoin(subquery, User.id == subquery.c.user_id)
)
```

## Alembic Migrations

### Configuration

```python
# backend/alembic/env.py
from app.database import Base
from app.models import user, profile, food_log, recipe, activity, gamification, subscription

target_metadata = Base.metadata
```

### Creating Migrations

```bash
# Auto-generate migration from model changes
cd backend
alembic revision --autogenerate -m "add trial_ends_at to users"

# Create empty migration for manual changes
alembic revision -m "add custom index"
```

### Migration Examples

```python
# alembic/versions/xxxx_add_trial_ends_at.py
"""add trial_ends_at to users

Revision ID: xxxx
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        'users',
        sa.Column('trial_ends_at', sa.DateTime(timezone=True), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'trial_ends_at')
```

```python
# Adding index
def upgrade():
    op.create_index(
        'ix_food_logs_user_date',
        'food_logs',
        ['user_id', sa.text('DATE(created_at)')]
    )

def downgrade():
    op.drop_index('ix_food_logs_user_date')
```

### Running Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade xxxx

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## Fly Postgres

### Connection in Production

```toml
# backend/fly.toml
[env]
  DATABASE_URL = "postgres://nutriprofile:password@nutriprofile-db.internal:5432/nutriprofile?sslmode=disable"
```

### Connecting to Production DB

```bash
# Via Fly proxy
fly proxy 5432 -a nutriprofile-db

# Then connect with psql
psql postgres://nutriprofile:password@localhost:5432/nutriprofile

# Or run migrations remotely
fly ssh console -a nutriprofile-api
cd /app
alembic upgrade head
```

### Database Backups

```bash
# Create backup
fly postgres backup create -a nutriprofile-db

# List backups
fly postgres backup list -a nutriprofile-db

# Restore backup
fly postgres backup restore <backup-id> -a nutriprofile-db
```

## Performance Optimization

### Indexes

```python
# In model definition
class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime(timezone=True), index=True)

    __table_args__ = (
        Index('ix_food_logs_user_date', 'user_id', text('DATE(created_at)')),
    )
```

### Query Optimization

```python
# Avoid N+1 queries - use eager loading
result = await self.db.execute(
    select(FoodLog)
    .options(selectinload(FoodLog.items))
    .where(FoodLog.user_id == user_id)
)

# Use pagination
.offset(skip).limit(limit)

# Select only needed columns
select(User.id, User.email, User.name)

# Use exists() for existence checks
from sqlalchemy import exists
await self.db.execute(
    select(exists().where(User.email == email))
)
```

## Data Models Reference

### Users & Profiles
```sql
users (id, email, hashed_password, name, is_active, preferred_language, subscription_tier, trial_ends_at, created_at, updated_at)
profiles (id, user_id, age, gender, height, weight, activity_level, fitness_goal, diet_type, allergies, bmr, tdee, daily_calories, protein_target, carbs_target, fat_target, health_conditions, medications, created_at, updated_at)
```

### Food & Nutrition
```sql
food_logs (id, user_id, meal_type, image_url, detected_items, user_corrections, total_calories, total_protein, total_carbs, total_fat, confidence_score, source, created_at)
daily_nutrition (id, user_id, date, target_calories, actual_calories, target_protein, actual_protein, target_carbs, actual_carbs, target_fat, actual_fat, water_intake, created_at)
```

### Recipes
```sql
recipes (id, user_id, name, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, protein_per_serving, carbs_per_serving, fat_per_serving, difficulty, cuisine_type, tags, image_url, confidence_score, created_at)
favorite_recipes (id, user_id, recipe_id, created_at)
recipe_history (id, user_id, recipe_id, generated_at, ingredients_used, preferences_applied)
```

### Activity & Goals
```sql
activity_logs (id, user_id, activity_type, duration, intensity, distance, calories_burned, calories_source, heart_rate_avg, steps, notes, created_at)
weight_logs (id, user_id, weight, body_fat_percentage, muscle_mass, notes, created_at)
goals (id, user_id, goal_type, target_value, current_value, period, is_completed, created_at, completed_at)
```

### Gamification
```sql
achievements (id, user_id, achievement_type, unlocked_at)
streaks (id, user_id, streak_type, current_count, longest_count, last_activity_date)
user_stats (id, user_id, xp, level, total_meals_logged, total_recipes_generated, total_activities_logged, created_at, updated_at)
notifications (id, user_id, type, title, message, is_read, created_at)
```

### Subscriptions
```sql
subscriptions (id, user_id, tier, status, current_period_start, current_period_end, cancel_at_period_end, ls_subscription_id, ls_customer_id, ls_variant_id, ls_order_id, created_at, updated_at)
usage_tracking (id, user_id, date, vision_analyses, recipe_generations, coach_messages, created_at, updated_at)
```

## Best Practices

1. **Always use async** - All database operations should be async
2. **Commit/rollback properly** - Use the get_db dependency
3. **Eager load relationships** - Avoid N+1 queries
4. **Index frequently queried columns** - user_id, created_at
5. **Use migrations** - Never modify schema directly
6. **Test migrations** - Apply locally before production
7. **Backup before migrations** - Especially for destructive changes

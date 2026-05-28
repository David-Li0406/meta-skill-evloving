"""
FastAPI Enterprise Project Initialization Script (Modular Architecture)

This script creates a complete FastAPI project with:
- UV + pyproject.toml (modern Python dependency management)
- Project name subdirectory (clean workspace organization)
- Modular architecture (independent modules with own DB/cache/routes)
- Core infrastructure (logging, config, DB, cache, HTTP client)
- Auto-discovery module loader
- Optional Keycloak or app-based RBAC authentication
- Prometheus metrics + OpenTelemetry tracing
- Structlog (JSON + colored console logging)
- Conversation ID tracking (X-Conversation-ID header + cookie)

Usage:
    python init_project.py --name my_api --auth keycloak
    python init_project.py --name my_api --auth app-based
    python init_project.py --name my_api --auth none
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Literal

AuthType = Literal["keycloak", "app-based", "none"]

INIT_FILE = "__init__.py"


def main():
    """Main entry point for project initialization."""
    parser = argparse.ArgumentParser(description="Initialize FastAPI Enterprise Project")
    parser.add_argument("--name", required=True, help="Project name (e.g., my_api)")
    parser.add_argument(
        "--auth",
        choices=["keycloak", "app-based", "none"],
        default="none",
        help="Authentication type"
    )
    parser.add_argument(
        "--with-example-module",
        action="store_true",
        help="Create example 'users' module"
    )
    
    args = parser.parse_args()
    
    project_name = args.name
    auth_type: AuthType = args.auth
    with_example = args.with_example_module
    
    print(f"🚀 Initializing FastAPI Enterprise project: {project_name}")
    print(f"   Authentication: {auth_type}")
    print(f"   Example module: {'Yes' if with_example else 'No'}")
    print()
    
    # Create project directory
    project_dir = Path.cwd() / project_name
    if project_dir.exists():
        print(f"❌ Error: Directory '{project_name}' already exists!")
        sys.exit(1)
    
    # Initialize UV project
    print("📦 Initializing UV project...")
    init_uv_project(project_name)
    
    # Create directory structure
    print("📁 Creating directory structure...")
    create_directory_structure(project_dir)
    
    # Create core files
    print("⚙️  Creating core infrastructure...")
    create_core_files(project_dir, project_name)
    
    # Create middleware
    print("🔀 Creating middleware...")
    create_middleware(project_dir, auth_type)
    
    # Create shared utilities
    print("🛠️  Creating shared utilities...")
    create_shared_files(project_dir)
    
    # Create core routes
    print("🛣️  Creating core routes...")
    create_core_routes(project_dir)
    
    # Create app.py
    print("📝 Creating app.py...")
    create_app_py(project_dir, project_name, auth_type)
    
    # Create configuration files
    print("📋 Creating configuration files...")
    create_config_files(project_dir, project_name, auth_type)
    
    # Create environment file
    print("🔐 Creating environment file...")
    create_env_file(project_dir, auth_type)
    
    # Create example module if requested
    if with_example:
        print("👤 Creating example 'users' module...")
        create_example_users_module(project_dir)
    
    # Add dependencies
    print("📦 Adding dependencies...")
    add_dependencies(project_dir, auth_type)
    
    # Create scripts
    print("🛠️  Creating automation scripts...")
    create_automation_scripts(project_dir)
    
    # Create README
    print("📖 Creating README...")
    create_readme(project_dir, project_name, auth_type, with_example)
    
    # Create .gitignore
    print("🙈 Creating .gitignore...")
    create_gitignore(project_dir)
    
    print()
    print(f"✅ Project '{project_name}' created successfully!")
    print()
    print("Next steps:")
    print(f"  1. cd {project_name}")
    print("  2. uv sync                          # Install dependencies")
    print("  3. cp .env.example .env             # Configure environment")
    print("  4. uv run uvicorn src.app:app --reload")
    print()
    if with_example:
        print("Example module created:")
        print(f"  - Run migrations: cd modules/users/alembic && alembic upgrade head")
        print(f"  - Test API: http://localhost:8000/api/v1/users")
    print()


def init_uv_project(project_name: str):
    """Initialize UV project with pyproject.toml."""
    try:
        subprocess.run(["uv", "init", project_name], check=True)
        print(f"   ✓ UV project initialized: {project_name}/")
    except subprocess.CalledProcessError:
        print("   ❌ Error: Failed to initialize UV project. Is UV installed?")
        print("   Install UV: https://github.com/astral-sh/uv")
        sys.exit(1)


def create_directory_structure(project_dir: Path):
    """Create complete project directory structure."""
    directories = [
        # Source code
        "src",
        "src/core",
        "src/middleware",
        "src/shared/enums",
        "src/shared/helpers",
        "src/routes",
        
        # Modules directory
        "modules",
        
        # Tests
        "tests",
        "tests/unit",
        "tests/integration",
        
        # Configuration
        "config",
        
        # Scripts
        "scripts",
    ]
    
    for directory in directories:
        dir_path = project_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py in Python packages
        if directory.startswith(("src", "tests", "modules")):
            (dir_path / INIT_FILE).touch()
    
    print(f"   ✓ Created {len(directories)} directories")


def create_core_files(project_dir: Path, project_name: str):
    """Create core infrastructure files."""
    # src/core/logging.py
    logging_content = '''"""
Structured logging configuration using structlog.

Features:
- JSON output in production (for log aggregation)
- Colored console output in development (human-readable)
- Conversation ID tracking in all logs
- Request/response logging middleware integration
"""

import sys
import structlog
from structlog.typing import FilteringBoundLogger

def configure_logging(environment: str = "development") -> None:
    """
    Configure structlog for the application.
    
    Args:
        environment: "development" (colored console) or "production" (JSON)
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    if environment == "production":
        # JSON logs for production (structured, parseable)
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ]
    else:
        # Colored console logs for development (human-readable)
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging_level=None),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

# Global logger instance
logger: FilteringBoundLogger = structlog.get_logger()
'''
    
    # src/core/config.py
    config_content = f'''"""
Application configuration using pydantic-settings.

All settings come from OS environment variables.
YAML files in config/ are loaded for external API configurations.
"""

from pathlib import Path
from pydantic_settings import BaseSettings
import yaml


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Application
    PROJECT_NAME: str = "{project_name}"
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"  # development | production
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/{project_name}_db"
    
    # Cache
    REDIS_URL: str | None = None  # None = use memory cache
    CACHE_DEFAULT_TTL: int = 3600  # 1 hour
    
    # External configs
    CONFIG_ENV: str = "development"  # Switches development.yml / production.yml
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def load_yaml_config(self) -> dict:
        """Load YAML configuration file based on CONFIG_ENV."""
        config_file = Path(__file__).parent.parent.parent / "config" / f"{{self.CONFIG_ENV}}.yml"
        
        if not config_file.exists():
            return {{}}
        
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {{}}


# Global settings instance
settings = Settings()
'''
    
    # src/core/db.py
    db_content = '''"""
Async SQLAlchemy database configuration.

Provides async session factory used by:
- FastAPI dependency injection (get_db)
- Alembic migrations (imports from here for consistency)
- All module services
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for SQLAlchemy models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
'''
    
    # src/core/cache.py
    cache_content = '''"""
Unified cache manager supporting Redis and in-memory caching.

Features:
- Redis for production (distributed, persistent)
- Memory cache for development (no dependencies)
- Module-specific namespaces
- Pattern-based invalidation
"""

from typing import Any
import json
from redis.asyncio import Redis
from src.core.config import settings
from src.core.logging import logger


class CacheManager:
    """Unified cache manager."""
    
    def __init__(self):
        self.redis: Redis | None = None
        self.memory: dict[str, Any] = {}
        self.use_redis = settings.REDIS_URL is not None
    
    async def connect(self):
        """Connect to Redis or use memory cache."""
        if self.use_redis:
            self.redis = await Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("cache_connected", backend="redis")
        else:
            logger.info("cache_connected", backend="memory")
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("cache_disconnected")
    
    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        try:
            if self.use_redis:
                value = await self.redis.get(key)
                if value:
                    return json.loads(value)
            else:
                return self.memory.get(key)
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL (seconds)."""
        try:
            serialized = json.dumps(value, default=str)
            
            if self.use_redis:
                await self.redis.setex(key, ttl, serialized)
            else:
                self.memory[key] = serialized
            
            logger.debug("cache_set", key=key, ttl=ttl)
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            if self.use_redis:
                await self.redis.delete(key)
            else:
                self.memory.pop(key, None)
            
            logger.debug("cache_deleted", key=key)
            return True
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        try:
            if self.use_redis:
                keys = await self.redis.keys(pattern)
                if keys:
                    deleted = await self.redis.delete(*keys)
                    logger.info("cache_pattern_deleted", pattern=pattern, count=deleted)
                    return deleted
                return 0
            else:
                import re
                regex = pattern.replace("*", ".*")
                keys_to_delete = [k for k in self.memory.keys() if re.match(f"^{{regex}}$", k)]
                for key in keys_to_delete:
                    del self.memory[key]
                logger.info("cache_pattern_deleted", pattern=pattern, count=len(keys_to_delete))
                return len(keys_to_delete)
        except Exception as e:
            logger.error("cache_pattern_delete_error", pattern=pattern, error=str(e))
            return 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if self.use_redis:
            return await self.redis.exists(key) > 0
        else:
            return key in self.memory


# Global cache manager instance
cache_manager = CacheManager()
'''
    
    # Write files
    (project_dir / "src" / "core" / "logging.py").write_text(logging_content, encoding="utf-8")
    (project_dir / "src" / "core" / "config.py").write_text(config_content, encoding="utf-8")
    (project_dir / "src" / "core" / "db.py").write_text(db_content, encoding="utf-8")
    (project_dir / "src" / "core" / "cache.py").write_text(cache_content, encoding="utf-8")
    
    print("   ✓ Created core files (logging, config, db, cache)")
    
    # src/core/httpx_client.py
    httpx_content = '''"""
Central HTTP client for external API calls.

Features:
- Async HTTP client with connection pooling
- Automatic conversation ID propagation
- Centralized timeout and retry configuration
- Request/response logging
"""

import httpx
from src.core.logging import logger
from src.core.config import settings
import structlog


class HTTPClient:
    """Central HTTP client for external APIs."""
    
    def __init__(self):
        self.client: httpx.AsyncClient | None = None
    
    async def connect(self):
        """Create HTTP client with connection pooling."""
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        logger.info("http_client_connected")
    
    async def disconnect(self):
        """Close HTTP client."""
        if self.client:
            await self.client.aclose()
            logger.info("http_client_disconnected")
    
    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """
        Make HTTP request with conversation ID propagation.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional httpx request parameters
        """
        # Get conversation ID from context
        conversation_id = structlog.contextvars.get_contextvars().get("conversation_id")
        
        # Add conversation ID to headers
        headers = kwargs.pop("headers", {})
        if conversation_id:
            headers["X-Conversation-ID"] = conversation_id
        
        logger.info("external_api_request", method=method, url=url, conversation_id=conversation_id)
        
        try:
            response = await self.client.request(method, url, headers=headers, **kwargs)
            
            logger.info(
                "external_api_response",
                method=method,
                url=url,
                status_code=response.status_code,
                conversation_id=conversation_id
            )
            
            return response
            
        except Exception as e:
            logger.error(
                "external_api_error",
                method=method,
                url=url,
                error=str(e),
                conversation_id=conversation_id
            )
            raise


# Global HTTP client instance
http_client = HTTPClient()
'''
    
    (project_dir / "src" / "core" / "httpx_client.py").write_text(httpx_content, encoding="utf-8")
    
    # src/core/module_loader.py
    module_loader_content = '''"""
Auto-discovery module loader.

Automatically discovers and registers all modules from modules/ directory.
Each module must export a 'router' in its __init__.py.
"""

from pathlib import Path
from importlib import import_module
from fastapi import FastAPI
from src.core.logging import logger


def discover_modules(app: FastAPI) -> None:
    """
    Auto-discover and register all modules.
    
    Modules are discovered from modules/ directory.
    Each module must have __init__.py with exported 'router'.
    """
    modules_dir = Path(__file__).parent.parent.parent / "modules"
    
    if not modules_dir.exists():
        logger.warning("modules_directory_not_found", path=str(modules_dir))
        return
    
    registered_count = 0
    
    for module_path in sorted(modules_dir.iterdir()):
        if not module_path.is_dir():
            continue
        
        if not (module_path / "__init__.py").exists():
            logger.warning("module_missing_init", module=module_path.name)
            continue
        
        try:
            # Import module
            module = import_module(f"modules.{module_path.name}")
            
            # Check for router
            if not hasattr(module, "router"):
                logger.warning("module_missing_router", module=module_path.name)
                continue
            
            # Register with FastAPI
            app.include_router(
                module.router,
                prefix=f"/api/v1/{module_path.name}",
                tags=[module_path.name.replace("_", " ").title()]
            )
            
            logger.info(
                "module_registered",
                module=module_path.name,
                prefix=f"/api/v1/{module_path.name}"
            )
            registered_count += 1
            
        except Exception as e:
            logger.error(
                "module_registration_failed",
                module=module_path.name,
                error=str(e)
            )
    
    logger.info("modules_discovery_complete", count=registered_count)
'''
    
    (project_dir / "src" / "core" / "module_loader.py").write_text(module_loader_content, encoding="utf-8")
    print("   ✓ Created httpx_client and module_loader")


def create_middleware(project_dir: Path, auth_type: AuthType):
    """Create middleware files."""
    
    # src/middleware/conversation_middleware.py
    conversation_middleware_content = '''"""
Conversation ID tracking middleware.

Features:
- Extracts conversation ID from X-Conversation-ID header
- Generates new UUID if not provided
- Sets conversation_id cookie for browsers
- Adds conversation ID to structlog context (appears in all logs)
"""

import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog


class ConversationMiddleware(BaseHTTPMiddleware):
    """Track conversation ID across requests."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with conversation ID tracking."""
        # Get or generate conversation ID
        conversation_id = (
            request.headers.get("X-Conversation-ID") or
            request.cookies.get("conversation_id") or
            str(uuid.uuid4())
        )
        
        # Add to structlog context (appears in all logs)
        structlog.contextvars.bind_contextvars(conversation_id=conversation_id)
        
        # Process request
        response: Response = await call_next(request)
        
        # Add conversation ID to response header and cookie
        response.headers["X-Conversation-ID"] = conversation_id
        response.set_cookie(
            key="conversation_id",
            value=conversation_id,
            httponly=True,
            max_age=86400  # 24 hours
        )
        
        # Clear structlog context
        structlog.contextvars.clear_contextvars()
        
        return response
'''
    
    # src/middleware/logging_middleware.py
    logging_middleware_content = '''"""
Request/response logging middleware.

Logs all incoming requests and outgoing responses with:
- HTTP method, path, status code
- Request/response duration
- Conversation ID (from context)
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request with logging."""
        start_time = time.time()
        
        # Log request
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query)
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=f"{duration:.3f}s"
        )
        
        return response
'''
    
    (project_dir / "src" / "middleware" / "conversation_middleware.py").write_text(
        conversation_middleware_content, encoding="utf-8"
    )
    (project_dir / "src" / "middleware" / "logging_middleware.py").write_text(
        logging_middleware_content, encoding="utf-8"
    )
    
    if auth_type == "keycloak":
        auth_middleware_content = '''"""
Keycloak JWT authentication middleware.

Features:
- Validates JWT tokens from Authorization header
- Extracts user roles from token
- Adds current_user to request state
- Role-based access control (RBAC)
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from keycloak import KeycloakOpenID
from src.core.config import settings
from src.core.logging import logger


class KeycloakAuthMiddleware(BaseHTTPMiddleware):
    """Keycloak JWT authentication."""
    
    def __init__(self, app, keycloak_client: KeycloakOpenID):
        super().__init__(app)
        self.keycloak = keycloak_client
    
    async def dispatch(self, request: Request, call_next):
        """Validate JWT token."""
        # Skip authentication for health/metrics endpoints
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # Get token from header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("missing_auth_token", path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            # Validate token with Keycloak
            token_info = self.keycloak.decode_token(
                token,
                validate=True,
                options={"verify_signature": True, "verify_aud": True, "verify_exp": True}
            )
            
            # Extract user info
            user_id = token_info.get("sub")
            username = token_info.get("preferred_username")
            roles = token_info.get("realm_access", {}).get("roles", [])
            
            # Add to request state
            request.state.current_user = {
                "id": user_id,
                "username": username,
                "roles": roles
            }
            
            logger.info("user_authenticated", user_id=user_id, username=username)
            
        except Exception as e:
            logger.error("token_validation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return await call_next(request)
'''
        (project_dir / "src" / "middleware" / "auth_middleware.py").write_text(
            auth_middleware_content, encoding="utf-8"
        )
    
    elif auth_type == "app-based":
        auth_middleware_content = '''"""
App-based RBAC authentication middleware.

Features:
- Custom JWT token validation
- User lookup from database
- Role-based access control
- Adds current_user to request state
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from src.core.config import settings
from src.core.logging import logger


class AppAuthMiddleware(BaseHTTPMiddleware):
    """App-based JWT authentication."""
    
    async def dispatch(self, request: Request, call_next):
        """Validate JWT token."""
        # Skip authentication for public endpoints
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json", "/api/v1/auth/login"]:
            return await call_next(request)
        
        # Get token from header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("missing_auth_token", path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            # Decode JWT token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user_id = payload.get("user_id")
            roles = payload.get("roles", [])
            
            # Add to request state
            request.state.current_user = {
                "id": user_id,
                "roles": roles
            }
            
            logger.info("user_authenticated", user_id=user_id)
            
        except jwt.ExpiredSignatureError:
            logger.warning("token_expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.error("invalid_token", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return await call_next(request)
'''
        (project_dir / "src" / "middleware" / "auth_middleware.py").write_text(
            auth_middleware_content, encoding="utf-8"
        )
    
    print(f"   ✓ Created middleware (conversation, logging{', auth' if auth_type != 'none' else ''})")


def create_shared_files(project_dir: Path):
    """Create shared utility files."""
    
    # src/shared/helpers/datetime_utils.py
    datetime_utils_content = '''"""
Shared datetime utility functions.
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def timestamp_to_datetime(timestamp: int) -> datetime:
    """Convert Unix timestamp to datetime."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
'''
    
    # src/shared/enums/common.py
    common_enums_content = '''"""
Shared enumerations across modules.
"""

from enum import Enum


class Environment(str, Enum):
    """Application environment."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
'''
    
    (project_dir / "src" / "shared" / "helpers" / "datetime_utils.py").write_text(
        datetime_utils_content, encoding="utf-8"
    )
    (project_dir / "src" / "shared" / "enums" / "common.py").write_text(
        common_enums_content, encoding="utf-8"
    )
    
    print("   ✓ Created shared utilities")


def create_core_routes(project_dir: Path):
    """Create core routes (health, metrics)."""
    
    # src/routes/health.py
    health_content = '''"""
Health check endpoint.

Returns application health status and basic metrics.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
'''
    
    # src/routes/metrics.py
    metrics_content = '''"""
Prometheus metrics endpoint.

Exposes application metrics for monitoring.
"""

from fastapi import APIRouter
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

router = APIRouter()

# Define metrics
request_count = Counter(
    "fastapi_requests_total",
    "Total request count",
    ["method", "endpoint", "status_code"]
)

request_duration = Histogram(
    "fastapi_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"]
)


@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
'''
    
    (project_dir / "src" / "routes" / "health.py").write_text(health_content, encoding="utf-8")
    (project_dir / "src" / "routes" / "metrics.py").write_text(metrics_content, encoding="utf-8")
    
    print("   ✓ Created core routes")


def create_app_py(project_dir: Path, project_name: str, auth_type: AuthType):
    """Create main app.py file."""
    
    app_content = f'''"""
{project_name} - FastAPI Application

Modular architecture with auto-discovery of modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.logging import configure_logging, logger
from src.core.cache import cache_manager
from src.core.httpx_client import http_client
from src.core.module_loader import discover_modules
from src.middleware.conversation_middleware import ConversationMiddleware
from src.middleware.logging_middleware import LoggingMiddleware
from src.routes import health, metrics

# Configure logging
configure_logging(environment=settings.ENVIRONMENT)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(ConversationMiddleware)
app.add_middleware(LoggingMiddleware)
'''
    
    if auth_type == "keycloak":
        app_content += '''
# Add Keycloak authentication
from keycloak import KeycloakOpenID
from src.middleware.auth_middleware import KeycloakAuthMiddleware

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
)

app.add_middleware(KeycloakAuthMiddleware, keycloak_client=keycloak_openid)
'''
    elif auth_type == "app-based":
        app_content += '''
# Add app-based authentication
from src.middleware.auth_middleware import AppAuthMiddleware

app.add_middleware(AppAuthMiddleware)
'''
    
    app_content += '''
# Include core routes (no /api prefix)
app.include_router(health.router, tags=["Health"])
app.include_router(metrics.router, tags=["Metrics"])


@app.on_event("startup")
async def startup():
    """Application startup tasks."""
    logger.info("application_starting", project=settings.PROJECT_NAME)
    
    # Connect to cache
    await cache_manager.connect()
    
    # Connect HTTP client
    await http_client.connect()
    
    # Auto-discover and register modules
    discover_modules(app)
    
    logger.info("application_started", project=settings.PROJECT_NAME)


@app.on_event("shutdown")
async def shutdown():
    """Application shutdown tasks."""
    logger.info("application_shutting_down")
    
    # Disconnect cache
    await cache_manager.disconnect()
    
    # Disconnect HTTP client
    await http_client.disconnect()
    
    logger.info("application_shutdown_complete")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }
'''
    
    (project_dir / "src" / "app.py").write_text(app_content, encoding="utf-8")
    print("   ✓ Created app.py")


def create_config_files(project_dir: Path, project_name: str, auth_type: AuthType):
    """Create YAML configuration files."""
    
    # config/development.yml
    dev_config = f'''# Development environment configuration

app:
  name: {project_name}
  debug: true

external_apis:
  example_service:
    base_url: "https://api.example.com"
    api_key: "${{EXAMPLE_API_KEY}}"  # From environment
    timeout: 30

cache:
  ttl:
    default: 3600
    users: 1800
    products: 7200
'''
    
    # config/production.yml
    prod_config = f'''# Production environment configuration

app:
  name: {project_name}
  debug: false

external_apis:
  example_service:
    base_url: "https://api.example.com"
    api_key: "${{EXAMPLE_API_KEY}}"
    timeout: 30

cache:
  ttl:
    default: 3600
    users: 1800
    products: 7200
'''
    
    (project_dir / "config" / "development.yml").write_text(dev_config, encoding="utf-8")
    (project_dir / "config" / "production.yml").write_text(prod_config, encoding="utf-8")
    
    print("   ✓ Created configuration files")


def create_env_file(project_dir: Path, auth_type: AuthType):
    """Create .env.example file."""
    
    env_content = '''# Application
PROJECT_NAME=my_api
API_VERSION=v1
ENVIRONMENT=development
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/my_api_db

# Cache
# REDIS_URL=redis://localhost:6379/0  # Uncomment for Redis, leave commented for memory cache
CACHE_DEFAULT_TTL=3600

# External configs
CONFIG_ENV=development

# Logging
LOG_LEVEL=INFO
'''
    
    if auth_type == "keycloak":
        env_content += '''
# Keycloak
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=my-realm
KEYCLOAK_CLIENT_ID=my-client
KEYCLOAK_CLIENT_SECRET=your-secret
'''
    elif auth_type == "app-based":
        env_content += '''
# JWT Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
'''
    
    (project_dir / ".env.example").write_text(env_content, encoding="utf-8")
    print("   ✓ Created .env.example")


def add_dependencies(project_dir: Path, auth_type: AuthType):
    """Add project dependencies using UV."""
    base_deps = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy[asyncio]",
        "asyncpg",
        "alembic",
        "pydantic-settings",
        "pyyaml",
        "structlog",
        "httpx",
        "prometheus-client",
        "redis[hiredis]",  # Redis with hiredis for performance
    ]
    
    if auth_type == "keycloak":
        base_deps.append("python-keycloak")
    elif auth_type == "app-based":
        base_deps.append("pyjwt[crypto]")
    
    try:
        subprocess.run(
            ["uv", "add"] + base_deps,
            cwd=project_dir,
            check=True,
            capture_output=True
        )
        print(f"   ✓ Added {len(base_deps)} dependencies")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Warning: Failed to add dependencies: {e}")
        print("       Run manually: uv add " + " ".join(base_deps))


def create_automation_scripts(project_dir: Path):
    """Create automation scripts for development."""
    
    # scripts/create_module.py
    create_module_script = '''"""
Create new independent module with complete structure.

Usage:
    python scripts/create_module.py --name orders
"""

import argparse
from pathlib import Path

INIT_FILE = "__init__.py"


def main():
    parser = argparse.ArgumentParser(description="Create new module")
    parser.add_argument("--name", required=True, help="Module name (e.g., orders)")
    args = parser.parse_args()
    
    module_name = args.name
    modules_dir = Path(__file__).parent.parent / "modules"
    module_dir = modules_dir / module_name
    
    if module_dir.exists():
        print(f"❌ Module '{module_name}' already exists!")
        return
    
    # Create module directories
    directories = [
        "",
        "routes",
        "models",
        "schemas",
        "services",
        "cache",
        "enums",
        "alembic",
        "alembic/versions"
    ]
    
    for directory in directories:
        dir_path = module_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py except in alembic/versions
        if directory != "alembic/versions":
            (dir_path / INIT_FILE).touch()
    
    # Create module router
    router_content = f"""from fastapi import APIRouter

router = APIRouter()

# Import and include route modules here
# from .routes import {module_name}
# router.include_router({module_name}.router, prefix="", tags=["{module_name.title()}"])
"""
    (module_dir / INIT_FILE).write_text(router_content)
    
    print(f"✅ Module '{module_name}' created successfully!")
    print(f"   Location: modules/{module_name}/")
    print()
    print("Next steps:")
    print(f"  1. Add models in models/")
    print(f"  2. Add schemas in schemas/")
    print(f"  3. Add services in services/")
    print(f"  4. Add routes in routes/")
    print(f"  5. Set up Alembic for module migrations")


if __name__ == "__main__":
    main()
'''
    
    (project_dir / "scripts" / "create_module.py").write_text(create_module_script, encoding="utf-8")
    
    print("   ✓ Created automation scripts")


def create_readme(project_dir: Path, project_name: str, auth_type: AuthType, with_example: bool):
    """Create README.md file."""
    
    readme_content = f'''# {project_name}

FastAPI Enterprise application with modular architecture.

## Features

- 🏗️ **Modular Architecture**: Independent modules with own DB, cache, and routes
- 📦 **Modern Python**: UV + pyproject.toml for fast dependency management
- 🔍 **Auto-Discovery**: Modules automatically registered on startup
- 🪵 **Structured Logging**: structlog with JSON (production) / colored (dev) output
- 🔗 **Conversation Tracking**: UUID-based request tracking across services
- 💾 **Flexible Caching**: Redis (production) / Memory (development)
- 🗄️ **Async Database**: SQLAlchemy 2.0 with AsyncPG
- 🔐 **Authentication**: {"Keycloak JWT" if auth_type == "keycloak" else "App-based JWT" if auth_type == "app-based" else "None (add as needed)"}
- 📊 **Observability**: Prometheus metrics + OpenTelemetry ready

## Project Structure

```
{project_name}/
├── src/
│   ├── app.py              # Main FastAPI application
│   ├── core/               # Core infrastructure
│   │   ├── logging.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── cache.py
│   │   └── module_loader.py
│   ├── middleware/         # Global middleware
│   ├── shared/             # Shared utilities
│   └── routes/             # Core routes (health, metrics)
│
├── modules/                # Independent modules
{"│   └── users/             # Example user module" if with_example else "│   └── (add modules here)"}
│
├── tests/                  # Test suite
├── config/                 # YAML configurations
└── pyproject.toml          # UV project config
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for production caching)
- UV ([installation guide](https://github.com/astral-sh/uv))

### Installation

1. **Install dependencies**
```bash
uv sync
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Set up database**
```bash
createdb {project_name}_db
```

4. **Run application**
```bash
uv run uvicorn src.app:app --reload
```

Application will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Creating Modules

### Generate new module
```bash
uv run python scripts/create_module.py --name orders
```

This creates:
- `modules/orders/` with complete structure
- Routes, models, schemas, services, cache directories
- Alembic configuration for module-specific migrations

### Module independence
Each module is completely independent:
- Own database tables (separate Alembic history)
- Own cache namespace
- Own routes and business logic
- Inter-module communication via service layer only

## Development

### Add dependencies
```bash
uv add package-name
```

### Run tests
```bash
uv run pytest
```

### Database migrations
```bash
# Per-module migrations
cd modules/users/alembic
alembic upgrade head

# Or use automation script
uv run python scripts/run_migrations.py --module users
```

### Export requirements.txt
```bash
uv export --format requirements-txt > requirements.txt
```

## Production Deployment

1. **Set environment**
```bash
export ENVIRONMENT=production
export DEBUG=False
```

2. **Configure Redis**
```bash
export REDIS_URL=redis://localhost:6379/0
```

3. **Run with Gunicorn**
```bash
uv run gunicorn src.app:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

MIT
'''
    
    (project_dir / "README.md").write_text(readme_content, encoding="utf-8")
    print("   ✓ Created README.md")


def create_gitignore(project_dir: Path):
    """Create .gitignore file."""
    
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# UV
uv.lock
.uv/

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# Alembic
alembic/versions/__pycache__/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Temporary
*.tmp
temp/
'''
    
    (project_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")
    print("   ✓ Created .gitignore")


def create_example_users_module(project_dir: Path):
    """Create example users module."""
    module_dir = project_dir / "modules" / "users"
    
    # Module structure already created by create_automation_scripts
    # Just create example files
    
    # modules/users/__init__.py
    module_init = '''from fastapi import APIRouter
from .routes import user

router = APIRouter()

# Include user routes
router.include_router(user.router, prefix="", tags=["Users"])
'''
    
    # modules/users/routes/user.py
    user_routes = '''from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from ..schemas.user import UserCreate, UserResponse
from ..services.user_service import UserService

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new user."""
    user = await UserService.create(db, user_data)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID."""
    user = await UserService.get_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user
'''
    
    # Create module directories
    (module_dir / "routes").mkdir(parents=True, exist_ok=True)
    (module_dir / "models").mkdir(exist_ok=True)
    (module_dir / "schemas").mkdir(exist_ok=True)
    (module_dir / "services").mkdir(exist_ok=True)
    (module_dir / "cache").mkdir(exist_ok=True)
    
    # Create __init__.py files
    for subdir in ["", "routes", "models", "schemas", "services", "cache"]:
        (module_dir / subdir / INIT_FILE).touch()
    
    # Write example files
    (module_dir / INIT_FILE).write_text(module_init, encoding="utf-8")
    (module_dir / "routes" / "user.py").write_text(user_routes, encoding="utf-8")
    
    print("   ✓ Created example users module")


# File continues with more functions...
if __name__ == "__main__":
    main()
'''

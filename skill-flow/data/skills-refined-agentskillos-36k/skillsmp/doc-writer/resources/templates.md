# Documentation Templates

Minimal, proven templates for technical documentation. Use as-is or adapt to your needs.

## Core Templates

These are the essential docs for most projects:

---

## README.md

**When**: Every repository needs one
**Length**: 50-100 lines ideal, 200 max

```markdown
# project-name

One-line description of what this does.

## Install

```bash
pip install project-name
# or
npm install project-name
```

## Quick Start

```python
from project import Client

client = Client(api_key="key")
result = client.do_thing()
```

## Configuration

Key configuration options if non-obvious:

- `API_KEY`: Your API key from dashboard
- `TIMEOUT`: Request timeout in seconds (default: 30)

## Documentation

Full docs at https://docs.example.com

## License

MIT
```

**What to cut:**
- "About" or "Introduction" section
- "Features" list (show in code)
- "Roadmap" or "Future Plans"
- "Contributing" (link to CONTRIBUTING.md instead)

---

## ARCHITECTURE.md

**When**: Multiple components OR non-obvious design decisions
**Length**: 100-300 lines depending on complexity

```markdown
# Architecture

## System Overview

```
┌─────────┐      ┌──────────┐      ┌──────────┐
│ Web API │─────▶│ Queue    │─────▶│ Workers  │
└─────────┘      └──────────┘      └──────────┘
     │                                    │
     ▼                                    ▼
┌─────────┐                        ┌──────────┐
│ Redis   │                        │ Postgres │
└─────────┘                        └──────────┘
```

- **Web API**: Express.js, handles HTTP requests, publishes jobs to queue
- **Queue**: Redis + Bull, distributes work to workers
- **Workers**: Node.js processes, execute background jobs
- **Redis**: Session storage + job queue
- **Postgres**: Persistent data storage

## Data Flow

1. Client sends request to Web API
2. API validates, writes to Postgres, publishes job to Queue
3. Worker picks up job, processes, updates Postgres
4. Client polls API for results or receives webhook

## Key Design Decisions

### Why Redis for queue instead of database polling?
- Need to process 10K+ jobs/min
- Database polling adds latency and load
- Bull provides retry logic and job prioritization

### Why separate workers from web API?
- CPU-intensive processing (image resizing, PDF generation)
- Prevents API request timeouts
- Scales worker and API independently

### Why webhooks instead of WebSockets?
- Most clients are server-side (no persistent connection)
- Webhooks integrate with existing infrastructure
- Simpler failure recovery (retry logic)

## Component Details

### Web API
- Tech: Express.js, Node 20+
- Entry: `src/api/server.js`
- Routes: `src/api/routes/`
- Auth: JWT tokens in Redis

### Workers
- Tech: Node.js, Bull workers
- Entry: `src/workers/index.js`
- Job handlers: `src/workers/jobs/`
- Concurrency: 5 workers/process

## Deployment

- API: 3+ EC2 instances behind ALB
- Workers: Auto-scaling group (2-20 instances)
- Redis: ElastiCache cluster
- Postgres: RDS Multi-AZ
```

**What to cut:**
- Implementation details (variable names, file structure if obvious)
- Historical context ("We used to use X but switched to Y")
- Obvious explanations (don't explain what Express.js is)

---

## TROUBLESHOOTING.md

**When**: Users encounter common issues OR non-obvious errors
**Length**: 20-100 lines total

```markdown
# Troubleshooting

Common issues and solutions.

## Installation

### npm install fails with "EACCES: permission denied"

**Solution**: Don't use sudo. Fix npm permissions:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

### Python module not found after installation

**Cause**: Multiple Python versions installed

**Solution**: Use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install package-name
```

## Runtime

### API returns 500 error

**Check**: Environment variables set?
```bash
echo $API_KEY  # Should not be empty
```

**Solution**: Copy `.env.example` to `.env` and fill in values.

### Connection timeout to database

**Cause**: Database not running or wrong credentials

**Solution**:
1. Check database is running: `pg_isready -h localhost`
2. Verify connection string in `.env`
3. Check firewall allows port 5432

## Performance

### Slow API responses (>1s)

**Check**: Database indexes exist?
```sql
SELECT * FROM pg_indexes WHERE tablename = 'users';
```

**Solution**: Add index on frequently queried columns:
```sql
CREATE INDEX idx_users_email ON users(email);
```
```

**What to cut:**
- Issues that only happened once
- Obvious errors with clear messages
- Problems fixed in latest version (update instead)

---

## API Documentation

**When**: Public API, library, or SDK
**Length**: 5-20 lines per function/class

### Function Template

```python
def process_payment(
    amount: Decimal,
    currency: str,
    customer_id: str,
    idempotency_key: str = None
) -> Payment:
    """Process a payment transaction.

    Args:
        amount: Payment amount (e.g., Decimal("10.99"))
        currency: ISO 4217 currency code (e.g., "USD")
        customer_id: Customer's unique identifier
        idempotency_key: Optional key to prevent duplicate charges

    Returns:
        Payment object with id, status, and timestamp fields

    Raises:
        InvalidAmountError: If amount <= 0
        PaymentFailedError: If payment provider rejects transaction

    Example:
        payment = process_payment(
            amount=Decimal("29.99"),
            currency="USD",
            customer_id="cus_123"
        )
        print(payment.status)  # "succeeded"
    """
```

### Class Template

```python
class APIClient:
    """HTTP client for the FooBar API.

    Handles authentication, retries, and rate limiting automatically.

    Args:
        api_key: Your API key from the dashboard
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum retry attempts for failed requests (default: 3)

    Example:
        client = APIClient(api_key="sk_live_...", timeout=60)
        response = client.get("/users/123")
    """

    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        ...

    def get(self, path: str, params: dict = None) -> Response:
        """Send GET request.

        Args:
            path: API endpoint path (e.g., "/users/123")
            params: Optional query parameters

        Returns:
            Response object with status_code, data, and headers

        Example:
            response = client.get("/users", params={"limit": 10})
        """
```

**What to cut:**
- Redundant descriptions ("This function processes a payment" when name is `process_payment`)
- Type information in docstring if already in type hints
- Obvious parameter explanations (`user_id: The user ID`)

---

## Examples / Tutorials

**When**: Integration is non-trivial OR common use cases need guidance
**Length**: 20-100 lines of code + minimal comments

### Minimal Example Template

```markdown
# Example: User Authentication

Shows how to authenticate users and manage sessions.

## Setup

```python
from auth import Authenticator
from database import Database

db = Database("postgresql://localhost/myapp")
auth = Authenticator(db, secret_key="your-secret")
```

## Register New User

```python
# Validate and hash password
user = auth.register(
    email="user@example.com",
    password="secure_password_123"
)

print(f"User created: {user.id}")
```

## Login

```python
# Returns token on success, None on failure
token = auth.login(
    email="user@example.com",
    password="secure_password_123"
)

if token:
    print(f"Access token: {token}")
```

## Verify Token

```python
# Validate token from Authorization header
user = auth.verify_token(token)

if user:
    print(f"Authenticated as: {user.email}")
else:
    print("Invalid token")
```

## Complete Flow

```python
from auth import Authenticator

auth = Authenticator(secret_key="your-secret")

# Registration
user = auth.register("user@example.com", "password123")

# Login
token = auth.login("user@example.com", "password123")

# Protected endpoint
authenticated_user = auth.verify_token(token)
```
```

### Tutorial Template

```markdown
# Tutorial: Building a REST API

Learn to build a REST API with authentication and database persistence.

## What You'll Build

An API with endpoints for creating, reading, updating, and deleting users.

## Prerequisites

- Python 3.9+
- PostgreSQL installed

## Step 1: Project Setup

```bash
mkdir myapi && cd myapi
python -m venv venv
source venv/bin/activate
pip install flask sqlalchemy psycopg2
```

## Step 2: Database Model

Create `models.py`:

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
```

## Step 3: API Endpoints

Create `app.py`:

```python
from flask import Flask, request, jsonify
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine("postgresql://localhost/myapi")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/users", methods=["POST"])
def create_user():
    session = Session()
    user = User(email=request.json["email"], name=request.json["name"])
    session.add(user)
    session.commit()
    return jsonify({"id": user.id}), 201

@app.route("/users/<int:user_id>")
def get_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": user.id, "email": user.email, "name": user.name})
```

## Step 4: Run the API

```bash
flask run
```

Test it:
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'
```
```

**What to cut:**
- Excessive explanatory comments in code
- Multiple ways to do the same thing (show one recommended way)
- Trivial examples (don't show how to call a function that takes no parameters)

---

## Selection Guide

| Need | Use Template | Typical Length |
|------|--------------|----------------|
| Project introduction | README.md | 50-100 lines |
| System design overview | ARCHITECTURE.md | 100-300 lines |
| Common issues/solutions | TROUBLESHOOTING.md | 20-100 lines total |
| Function/class reference | API docs | 5-20 lines each |
| Integration guide | Example | 20-50 lines code |
| Step-by-step tutorial | Tutorial | 50-200 lines code |

---

## General Tips

1. **Start minimal, expand only if needed** - Begin with the smallest template, add sections when users ask
2. **Code examples > prose** - Show working code instead of explaining in paragraphs
3. **One example per concept** - Don't show 5 ways to authenticate, show the recommended way
4. **Real code, not pseudocode** - Examples should copy-paste and run
5. **Update with breaking changes** - Outdated docs worse than no docs
6. **Link don't duplicate** - Reference existing docs instead of repeating them

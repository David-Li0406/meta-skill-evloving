# CRUD API Template

A complete template for building CRUD (Create, Read, Update, Delete) APIs with FastAPI.

## Features

- RESTful API design
- Pydantic models for validation
- In-memory data storage (easily replaceable with database)
- Proper HTTP status codes
- Error handling
- API documentation

## Structure

```
crud-api-template/
├── main.py           # Main application
├── models.py         # Pydantic models
├── schemas.py        # Request/Response schemas
└── requirements.txt  # Dependencies
```

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
fastapi dev main.py
```

3. Access the API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `POST /items/` - Create a new item
- `GET /items/` - List all items
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

## Next Steps

Replace the in-memory storage with a real database:
- See `references/databases.md` for PostgreSQL, MySQL, MongoDB integration
- Use SQLAlchemy or Beanie for ORM
- Add proper data persistence

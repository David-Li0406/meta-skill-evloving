# Python Project Structure

## Package Layout

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   └── test_main.py
├── pyproject.toml
├── README.md
└── .gitignore
```

## FastAPI Project

```
myapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   └── routers/
│       ├── users.py
│       └── items.py
├── tests/
├── alembic/  # migrations
├── pyproject.toml
└── .env
```

## Use src/ Layout

Benefits of src/ layout:
- Prevents accidental imports from development directory
- Forces proper package installation
- Cleaner test isolation

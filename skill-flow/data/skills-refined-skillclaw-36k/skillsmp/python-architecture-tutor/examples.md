# Example Python Project Structure (src layout)

This example demonstrates a clean, manageable structure for a medium-sized Python application.

```text
my_awesome_project/
├── pyproject.toml         # Build system requirements and metadata
├── requirements.txt       # Dependencies
├── .env.example           # Template for environment variables
├── src/
│   └── awesome_app/       # Main package
│       ├── __init__.py
│       ├── main.py        # Entry point
│       ├── core/          # Business logic and entities
│       │   ├── __init__.py
│       │   └── models.py
│       ├── services/      # Process-oriented logic
│       │   ├── __init__.py
│       │   └── calculator.py
│       └── utils/         # Helper functions
│           ├── __init__.py
│           └── helpers.py
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_core.py
│   └── test_services.py
└── README.md
```

## Practical Tips for Students

1. **Keep it Simple**: Only add folders when you have more than 3-4 related files.
2. **Naming**: Use lowercase with underscores for modules and packages.
3. **Circular Imports**: If Module A imports Module B, and Module B imports Module A, Python will complain. This is usually a sign that your architecture needs rethinking (maybe a third module C for shared code).

# {{ cookiecutter.project_name }}

Django application using RAPID horizontal layer architecture with uv for dependency management.

## Commands

Run `just` to see available commands.

Key commands:
- `just run` - Start development server
- `just migrate` - Run database migrations
- `just test` - Run tests
- `just shell` - Django shell with IPython

## RAPID Architecture

This project follows the RAPID horizontal layer architecture:

### Data Layer (`{{ cookiecutter.package_name }}/data/`)
- `models/` - Django model definitions
- `migrations/` - Database migrations

### Readers (`{{ cookiecutter.package_name }}/readers/`)
Read-only business logic. Functions that retrieve and process data without side effects.

### Actions (`{{ cookiecutter.package_name }}/actions/`)
State-changing business logic. Functions that modify database state or trigger external actions.

### Interfaces (`{{ cookiecutter.package_name }}/interfaces/`)
- `http/api/` - DRF views, serializers, and URLs
- `http/templates/` - HTML templates
- `management_commands/management/commands/` - Custom Django management commands

## Dependencies

- Add runtime deps: `uv add <package>`
- Add dev deps: `uv add --dev <package>`
- Run anything: `uv run <command>`

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `DEBUG` - Enable debug mode (default: true)
- `SECRET_KEY` - Django secret key (required in production)
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

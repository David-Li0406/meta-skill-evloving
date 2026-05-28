# {{ cookiecutter.project_name }}
{% if cookiecutter.description %}
{{ cookiecutter.description }}
{% endif %}
## Development

### Local Development

```bash
# Start PostgreSQL
docker compose up -d db

# Run migrations
just migrate

# Start development server
just run
```

### Docker Development

```bash
# Start all services
just docker-up

# Run migrations
just docker-migrate
```

## Commands

Run `just` to see all available commands.

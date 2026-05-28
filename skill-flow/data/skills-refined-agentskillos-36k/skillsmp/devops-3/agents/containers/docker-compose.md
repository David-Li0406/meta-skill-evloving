---
name: docker-compose
description: Orchestration locale avec Docker Compose
workflows:
  - id: compose-setup
    template: wf-creation
    phase: Production
    name: Setup Docker Compose
    duration: 0.5-1 jour
  - id: compose-evolution
    template: wf-evolution
    phase: Réalisation
    name: Évolution stack Compose
    duration: 0.5 jour
---

# Agent Docker Compose

Tu es un expert Docker Compose capable de configurer des environnements de développement et de test multi-containers.

## Tu NE fais PAS

- ❌ Décisions stratégiques sur l'architecture de conteneurisation → `direction-technique`
- ❌ Développement du code applicatif → `backend-developer`, `frontend-developer`
- ❌ Stratégie de tests → `testing-process`
- ❌ Processus de développement → `web-dev-process`

## Responsabilités

- Configuration docker-compose.yml
- Orchestration multi-services
- Réseaux et volumes
- Environnements de développement
- Override et profils

## Structure de Base

### Application Web avec DB

```yaml
# docker-compose.yml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  postgres_data:
  redis_data:

networks:
  backend:
    driver: bridge
```

## Patterns Avancés

### Multi-environment avec Override

```yaml
# docker-compose.yml (base)
version: '3.9'

services:
  app:
    build: .
    environment:
      - NODE_ENV=${NODE_ENV:-development}

# docker-compose.override.yml (dev - chargé automatiquement)
version: '3.9'

services:
  app:
    volumes:
      - .:/app
    ports:
      - "3000:3000"
    command: npm run dev

# docker-compose.prod.yml
version: '3.9'

services:
  app:
    build:
      target: production
    restart: always
    deploy:
      replicas: 3
```

Usage :
```bash
# Dev (charge automatiquement override)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Profils

```yaml
version: '3.9'

services:
  app:
    build: .
    profiles: ["app", "full"]

  db:
    image: postgres:15
    profiles: ["app", "full", "db-only"]

  monitoring:
    image: grafana/grafana
    profiles: ["full", "monitoring"]

  debug:
    image: nicolaka/netshoot
    profiles: ["debug"]
```

Usage :
```bash
docker compose --profile app up        # app + db
docker compose --profile full up       # tout
docker compose --profile debug up      # debug container
```

### Build Multi-stage

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: ${BUILD_TARGET:-development}
      args:
        NODE_VERSION: 20
        BUILD_DATE: ${BUILD_DATE}
      cache_from:
        - myapp:cache
    image: myapp:${TAG:-latest}
```

## Réseaux

### Réseau Isolé par Service

```yaml
services:
  frontend:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Pas d'accès internet
```

### Réseau Externe

```yaml
networks:
  proxy:
    external: true
    name: traefik_network

services:
  app:
    networks:
      - proxy
      - internal
```

## Volumes

### Types de Volumes

```yaml
services:
  app:
    volumes:
      # Bind mount (dev)
      - ./src:/app/src:ro

      # Named volume (persistance)
      - node_modules:/app/node_modules

      # Tmpfs (performance)
      - type: tmpfs
        target: /app/tmp

volumes:
  node_modules:
    driver: local

  # Volume avec options
  data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
```

## Health Checks

### Configuration Complète

```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Dépendances avec Conditions

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
      migrations:
        condition: service_completed_successfully
```

## Environnements

### Variables d'Environnement

```yaml
services:
  app:
    environment:
      # Inline
      - NODE_ENV=development

      # Depuis host
      - API_KEY

      # Avec default
      - LOG_LEVEL=${LOG_LEVEL:-info}

    env_file:
      - .env
      - .env.local
```

### Fichier .env

```bash
# .env
COMPOSE_PROJECT_NAME=myapp
POSTGRES_USER=user
POSTGRES_PASSWORD=secret
```

## Développement

### Hot Reload

```yaml
services:
  frontend:
    build:
      context: ./frontend
      target: dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true  # Pour Windows/Mac
    command: npm run dev
```

### Debug Mode

```yaml
services:
  api:
    build:
      target: debug
    ports:
      - "3000:3000"
      - "9229:9229"  # Node debug port
    command: node --inspect=0.0.0.0:9229 src/index.js
```

## Testing

### Stack de Test

```yaml
# docker-compose.test.yml
version: '3.9'

services:
  test:
    build:
      context: .
      target: test
    environment:
      - DATABASE_URL=postgres://test:test@db:5432/test_db
    depends_on:
      db:
        condition: service_healthy
    command: npm run test:ci

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    tmpfs:
      - /var/lib/postgresql/data  # DB en mémoire
```

```bash
docker compose -f docker-compose.test.yml run --rm test
```

## Extensions

### Fragments Réutilisables (YAML Anchors)

```yaml
x-app-common: &app-common
  build: .
  environment: &app-env
    NODE_ENV: production
  restart: unless-stopped
  logging: &logging
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"

services:
  api:
    <<: *app-common
    ports:
      - "3000:3000"

  worker:
    <<: *app-common
    command: npm run worker
```

### Extension Fields

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "10m"

services:
  app:
    logging: *default-logging
```

## Commandes Utiles

```bash
# Démarrer en arrière-plan
docker compose up -d

# Rebuild et démarrer
docker compose up --build

# Logs en temps réel
docker compose logs -f app

# Exécuter commande
docker compose exec app npm run migrate

# Scale service
docker compose up -d --scale worker=3

# Nettoyer tout
docker compose down -v --remove-orphans
```

## Livrables

| Livrable | Description |
|----------|-------------|
| docker-compose.yml | Configuration base |
| docker-compose.override.yml | Override développement |
| docker-compose.prod.yml | Configuration production |
| .env.example | Variables d'environnement |

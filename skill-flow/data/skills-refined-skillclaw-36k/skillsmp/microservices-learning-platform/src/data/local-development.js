/**
 * Local Development Guide Data
 * Complete guide for running microservices locally using Docker
 */

export const localDevelopmentData = {
    title: "Local Development & Testing Guide",
    description: "Run microservices locally using Docker, Docker Compose, and development tools",
    lastUpdated: "January 2026",
    version: "1.0.0",

    sections: [
        // Section 1: Prerequisites
        {
            id: "prerequisites",
            emoji: "📋",
            shortTitle: "Prerequisites",
            title: "Prerequisites & Setup",
            subtitle: "Tools you need before starting local development",
            description: `Before running microservices locally, ensure you have all the required tools installed.`,
            subsections: [
                {
                    title: "Required Tools",
                    content: `Install these tools on your development machine:`,
                    code: `# ═══════════════════════════════════════════════════════════
# REQUIRED TOOLS FOR LOCAL MICROSERVICES DEVELOPMENT
# ═══════════════════════════════════════════════════════════

# 1. Docker Desktop (includes Docker & Docker Compose)
#    Download: https://www.docker.com/products/docker-desktop
#    Verify installation:
docker --version          # Docker version 24.0+
docker compose version    # Docker Compose version v2.20+

# 2. Node.js (for JavaScript/TypeScript services)
#    Download: https://nodejs.org/ (LTS version recommended)
node --version            # v20.x or higher
npm --version             # 10.x or higher

# 3. Git
git --version             # 2.40+

# 4. Code Editor (VS Code recommended)
#    Extensions: Docker, ESLint, Prettier, Thunder Client

# 5. Optional but recommended:
#    - kubectl (for Kubernetes testing)
#    - k9s (Kubernetes CLI UI)
#    - Lens (Kubernetes IDE)
#    - Postman or Insomnia (API testing)`,
                    codeLanguage: "bash",
                    codeFilename: "prerequisites.sh"
                },
                {
                    title: "Docker Desktop Settings",
                    content: `Configure Docker Desktop for optimal microservices development:`,
                    code: `# Recommended Docker Desktop Settings:
# ═══════════════════════════════════════════════════════════

# Resources (Settings > Resources):
#   - CPUs: 4+ cores
#   - Memory: 8GB+ RAM (16GB recommended for 5+ services)
#   - Disk: 50GB+

# Enable these features (Settings > General):
#   ✅ Start Docker Desktop when you log in
#   ✅ Use Docker Compose V2

# Enable Kubernetes (Settings > Kubernetes):
#   ✅ Enable Kubernetes (optional, for K8s testing)

# WSL 2 Backend (Windows only):
#   ✅ Use the WSL 2 based engine`,
                    codeLanguage: "bash",
                    codeFilename: "docker-settings"
                }
            ],
            checklist: [
                "✅ Docker Desktop installed and running",
                "✅ Docker Compose V2 available",
                "✅ Node.js 20+ installed",
                "✅ At least 8GB RAM allocated to Docker",
                "✅ Git configured with your credentials"
            ]
        },

        // Section 2: Monorepo Local Development
        {
            id: "monorepo-local",
            emoji: "🏢",
            shortTitle: "Monorepo Local",
            title: "Running Monorepo Services Locally",
            subtitle: "Complete Docker Compose setup for monorepo architecture",
            description: `In a monorepo, all services live in one repository. We use Docker Compose to orchestrate all services, databases, and infrastructure locally.`,
            diagram: `┌─────────────────────────────────────────────────────────────────────────────────┐
│                        MONOREPO LOCAL ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    microservices-platform/
    │
    ├── docker-compose.yml          ◄─── Orchestrates everything
    ├── docker-compose.dev.yml      ◄─── Development overrides (hot reload)
    ├── docker-compose.test.yml     ◄─── Test environment
    │
    ├── services/
    │   ├── user-service/           ──┐
    │   ├── product-service/        ──┼──► Each has its own Dockerfile
    │   ├── order-service/          ──┤
    │   └── api-gateway/            ──┘
    │
    └── infrastructure/
        ├── postgres/               ◄─── Database init scripts
        ├── redis/                  ◄─── Cache config
        ├── rabbitmq/               ◄─── Message broker
        └── nginx/                  ◄─── Reverse proxy config

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                           DOCKER NETWORK                                    │
    │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
    │  │   User    │  │  Product  │  │   Order   │  │    API    │               │
    │  │  Service  │  │  Service  │  │  Service  │  │  Gateway  │               │
    │  │  :3001    │  │  :3002    │  │  :3003    │  │   :3000   │◄── Entry     │
    │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └───────────┘    Point     │
    │        │              │              │                                     │
    │        └──────────────┴──────────────┘                                     │
    │                       │                                                    │
    │  ┌───────────┐  ┌───────────┐  ┌───────────┐                              │
    │  │ PostgreSQL│  │   Redis   │  │ RabbitMQ  │                              │
    │  │   :5432   │  │   :6379   │  │   :5672   │                              │
    │  └───────────┘  └───────────┘  └───────────┘                              │
    └─────────────────────────────────────────────────────────────────────────────┘`,
            subsections: [
                {
                    title: "Project Structure",
                    content: `Set up your monorepo with this structure for local development:`,
                    code: `microservices-platform/
├── docker-compose.yml              # Base compose file
├── docker-compose.dev.yml          # Dev overrides (volumes, hot reload)
├── docker-compose.test.yml         # Test environment
├── .env                            # Environment variables
├── .env.example                    # Template for team
│
├── services/
│   ├── api-gateway/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.dev          # Dev Dockerfile with hot reload
│   │   └── package.json
│   │
│   ├── user-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.dev
│   │   ├── package.json
│   │   └── prisma/
│   │       └── schema.prisma
│   │
│   ├── product-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── Dockerfile.dev
│   │   └── package.json
│   │
│   └── order-service/
│       ├── src/
│       ├── Dockerfile
│       ├── Dockerfile.dev
│       └── package.json
│
├── libs/                           # Shared libraries
│   ├── common/
│   ├── database/
│   └── contracts/
│
├── infrastructure/
│   ├── postgres/
│   │   └── init/
│   │       ├── 01-create-databases.sql
│   │       └── 02-create-users.sql
│   ├── redis/
│   │   └── redis.conf
│   ├── rabbitmq/
│   │   └── rabbitmq.conf
│   └── nginx/
│       └── nginx.conf
│
└── scripts/
    ├── setup.sh                    # Initial setup script
    ├── start-dev.sh                # Start development environment
    └── reset-db.sh                 # Reset databases`,
                    codeLanguage: "text",
                    codeFilename: "monorepo-structure"
                },
                {
                    title: "Docker Compose - Base Configuration",
                    content: `The base \`docker-compose.yml\` defines all services and their configurations:`,
                    code: `# docker-compose.yml
# ═══════════════════════════════════════════════════════════
# MONOREPO BASE DOCKER COMPOSE
# ═══════════════════════════════════════════════════════════

version: '3.8'

services:
  # ─────────────────────────────────────────────────────────
  # API GATEWAY - Entry point for all requests
  # ─────────────────────────────────────────────────────────
  api-gateway:
    build:
      context: .
      dockerfile: services/api-gateway/Dockerfile
    container_name: api-gateway
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - PORT=3000
      - USER_SERVICE_URL=http://user-service:3001
      - PRODUCT_SERVICE_URL=http://product-service:3002
      - ORDER_SERVICE_URL=http://order-service:3003
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=\${JWT_SECRET}
    depends_on:
      - user-service
      - product-service
      - order-service
      - redis
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ─────────────────────────────────────────────────────────
  # USER SERVICE
  # ─────────────────────────────────────────────────────────
  user-service:
    build:
      context: .
      dockerfile: services/user-service/Dockerfile
    container_name: user-service
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=development
      - PORT=3001
      - DATABASE_URL=postgresql://postgres:\${POSTGRES_PASSWORD}@postgres:5432/users_db
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbitmq:5672
      - JWT_SECRET=\${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
      rabbitmq:
        condition: service_healthy
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ─────────────────────────────────────────────────────────
  # PRODUCT SERVICE
  # ─────────────────────────────────────────────────────────
  product-service:
    build:
      context: .
      dockerfile: services/product-service/Dockerfile
    container_name: product-service
    ports:
      - "3002:3002"
    environment:
      - NODE_ENV=development
      - PORT=3002
      - DATABASE_URL=postgresql://postgres:\${POSTGRES_PASSWORD}@postgres:5432/products_db
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ─────────────────────────────────────────────────────────
  # ORDER SERVICE
  # ─────────────────────────────────────────────────────────
  order-service:
    build:
      context: .
      dockerfile: services/order-service/Dockerfile
    container_name: order-service
    ports:
      - "3003:3003"
    environment:
      - NODE_ENV=development
      - PORT=3003
      - DATABASE_URL=postgresql://postgres:\${POSTGRES_PASSWORD}@postgres:5432/orders_db
      - REDIS_URL=redis://redis:6379
      - RABBITMQ_URL=amqp://rabbitmq:5672
      - USER_SERVICE_URL=http://user-service:3001
      - PRODUCT_SERVICE_URL=http://product-service:3002
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
      rabbitmq:
        condition: service_healthy
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3003/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ─────────────────────────────────────────────────────────
  # INFRASTRUCTURE SERVICES
  # ─────────────────────────────────────────────────────────
  
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=\${POSTGRES_PASSWORD}
      - POSTGRES_MULTIPLE_DATABASES=users_db,products_db,orders_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infrastructure/postgres/init:/docker-entrypoint-initdb.d
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - "5672:5672"     # AMQP port
      - "15672:15672"   # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=\${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - microservices-network
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Adminer - Database UI (optional)
  adminer:
    image: adminer
    container_name: adminer
    ports:
      - "8080:8080"
    networks:
      - microservices-network

# ─────────────────────────────────────────────────────────
# NETWORKS & VOLUMES
# ─────────────────────────────────────────────────────────
networks:
  microservices-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.yml"
                },
                {
                    title: "Development Override (Hot Reload)",
                    content: `The \`docker-compose.dev.yml\` adds development-specific features like hot reloading:`,
                    code: `# docker-compose.dev.yml
# ═══════════════════════════════════════════════════════════
# DEVELOPMENT OVERRIDES - Use with: docker compose -f docker-compose.yml -f docker-compose.dev.yml up
# ═══════════════════════════════════════════════════════════

version: '3.8'

services:
  # ─────────────────────────────────────────────────────────
  # API GATEWAY - Development mode with hot reload
  # ─────────────────────────────────────────────────────────
  api-gateway:
    build:
      context: .
      dockerfile: services/api-gateway/Dockerfile.dev
    volumes:
      # Mount source code for hot reload
      - ./services/api-gateway/src:/app/src:ro
      - ./libs:/app/libs:ro
      # Exclude node_modules
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev

  # ─────────────────────────────────────────────────────────
  # USER SERVICE - Development mode
  # ─────────────────────────────────────────────────────────
  user-service:
    build:
      context: .
      dockerfile: services/user-service/Dockerfile.dev
    volumes:
      - ./services/user-service/src:/app/src:ro
      - ./services/user-service/prisma:/app/prisma:ro
      - ./libs:/app/libs:ro
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev

  # ─────────────────────────────────────────────────────────
  # PRODUCT SERVICE - Development mode
  # ─────────────────────────────────────────────────────────
  product-service:
    build:
      context: .
      dockerfile: services/product-service/Dockerfile.dev
    volumes:
      - ./services/product-service/src:/app/src:ro
      - ./libs:/app/libs:ro
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev

  # ─────────────────────────────────────────────────────────
  # ORDER SERVICE - Development mode
  # ─────────────────────────────────────────────────────────
  order-service:
    build:
      context: .
      dockerfile: services/order-service/Dockerfile.dev
    volumes:
      - ./services/order-service/src:/app/src:ro
      - ./libs:/app/libs:ro
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
    command: npm run dev`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.dev.yml"
                },
                {
                    title: "Development Dockerfile",
                    content: `Each service needs a development Dockerfile with hot reload support:`,
                    code: `# services/user-service/Dockerfile.dev
# ═══════════════════════════════════════════════════════════
# DEVELOPMENT DOCKERFILE - Hot reload enabled
# ═══════════════════════════════════════════════════════════

FROM node:20-alpine

# Install development tools
RUN apk add --no-cache \\
    wget \\
    curl

WORKDIR /app

# Copy package files from root (monorepo)
COPY package*.json ./
COPY nx.json ./
COPY tsconfig.base.json ./

# Copy service package.json
COPY services/user-service/package*.json ./services/user-service/

# Copy shared libs
COPY libs/ ./libs/

# Install ALL dependencies (including devDependencies)
RUN npm ci

# Copy service source (will be overridden by volume in dev)
COPY services/user-service/ ./services/user-service/

WORKDIR /app/services/user-service

# Expose port
EXPOSE 3001

# Default command (overridden in docker-compose.dev.yml)
CMD ["npm", "run", "dev"]`,
                    codeLanguage: "dockerfile",
                    codeFilename: "Dockerfile.dev"
                },
                {
                    title: "Environment Variables",
                    content: `Create a \`.env\` file in your project root:`,
                    code: `# .env
# ═══════════════════════════════════════════════════════════
# LOCAL DEVELOPMENT ENVIRONMENT VARIABLES
# ═══════════════════════════════════════════════════════════
# Copy this file to .env and fill in your values
# NEVER commit .env to Git!

# ─────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────
POSTGRES_PASSWORD=localdev123
POSTGRES_USER=postgres

# ─────────────────────────────────────────────────────────
# Message Broker
# ─────────────────────────────────────────────────────────
RABBITMQ_PASSWORD=localdev123

# ─────────────────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────────────────
JWT_SECRET=your-super-secret-jwt-key-for-local-dev-only
JWT_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d

# ─────────────────────────────────────────────────────────
# Service URLs (for running outside Docker)
# ─────────────────────────────────────────────────────────
USER_SERVICE_URL=http://localhost:3001
PRODUCT_SERVICE_URL=http://localhost:3002
ORDER_SERVICE_URL=http://localhost:3003

# ─────────────────────────────────────────────────────────
# External Services (use local or sandbox)
# ─────────────────────────────────────────────────────────
STRIPE_SECRET_KEY=sk_test_xxxx
SENDGRID_API_KEY=SG.xxxx`,
                    codeLanguage: "bash",
                    codeFilename: ".env"
                },
                {
                    title: "PostgreSQL Init Script",
                    content: `Automatically create multiple databases when PostgreSQL starts:`,
                    code: `-- infrastructure/postgres/init/01-create-databases.sql
-- ═══════════════════════════════════════════════════════════
-- CREATE DATABASES FOR EACH MICROSERVICE
-- ═══════════════════════════════════════════════════════════

-- Create databases
CREATE DATABASE users_db;
CREATE DATABASE products_db;
CREATE DATABASE orders_db;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE users_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE products_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE orders_db TO postgres;

-- Connect to users_db and create schema
\\c users_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Connect to products_db and create schema
\\c products_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Connect to orders_db and create schema
\\c orders_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`,
                    codeLanguage: "sql",
                    codeFilename: "01-create-databases.sql"
                },
                {
                    title: "Running the Monorepo Locally",
                    content: `Use these commands to manage your local development environment:`,
                    code: `# ═══════════════════════════════════════════════════════════
# MONOREPO LOCAL DEVELOPMENT COMMANDS
# ═══════════════════════════════════════════════════════════

# 1. First time setup - copy environment file
cp .env.example .env

# 2. Start ALL services (production-like build)
docker compose up -d

# 3. Start with hot reload (RECOMMENDED for development)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 4. View logs for all services
docker compose logs -f

# 5. View logs for specific service
docker compose logs -f user-service

# 6. Rebuild a specific service after Dockerfile changes
docker compose build user-service
docker compose up -d user-service

# 7. Rebuild all services
docker compose build --no-cache
docker compose up -d

# 8. Stop all services (keeps data)
docker compose down

# 9. Stop and REMOVE all data (fresh start)
docker compose down -v

# 10. Run database migrations (user-service example)
docker compose exec user-service npx prisma migrate dev

# 11. Open shell in a container
docker compose exec user-service sh

# 12. Check service health
docker compose ps

# 13. View resource usage
docker stats

# ═══════════════════════════════════════════════════════════
# COMMON WORKFLOWS
# ═══════════════════════════════════════════════════════════

# Start fresh (nuke everything and rebuild)
docker compose down -v
docker system prune -f
docker compose build --no-cache
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Quick restart of one service
docker compose restart user-service

# Scale a service (run multiple instances)
docker compose up -d --scale product-service=3`,
                    codeLanguage: "bash",
                    codeFilename: "commands.sh",
                    keyPoints: [
                        "Use `-f` flags to combine compose files for development",
                        "Hot reload requires volume mounts in dev override file",
                        "Use `docker compose logs -f` to follow logs in real-time",
                        "Use `down -v` to reset all data for a fresh start",
                        "Run migrations inside containers to use correct database URL"
                    ]
                }
            ],
            tip: "Create a `Makefile` or `scripts/` folder with shortcuts like `make dev`, `make logs`, `make reset` for faster development workflow!"
        },

        // Section 3: Polyrepo Local Development
        {
            id: "polyrepo-local",
            emoji: "📦",
            shortTitle: "Polyrepo Local",
            title: "Running Individual Microservices Locally",
            subtitle: "Docker setup for polyrepo (separate repository) architecture",
            description: `In a polyrepo setup, each service has its own repository. For local development, you'll need a way to run multiple services together while keeping them independent.`,
            diagram: `┌─────────────────────────────────────────────────────────────────────────────────┐
│                        POLYREPO LOCAL ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────────┘

    Your Machine:
    │
    ├── ~/projects/user-service/        ◄─── git clone user-service
    │   ├── docker-compose.yml          ◄─── Service + its dependencies only
    │   └── docker-compose.deps.yml     ◄─── Just infrastructure
    │
    ├── ~/projects/product-service/     ◄─── git clone product-service
    │   ├── docker-compose.yml
    │   └── docker-compose.deps.yml
    │
    ├── ~/projects/order-service/       ◄─── git clone order-service
    │   ├── docker-compose.yml
    │   └── docker-compose.deps.yml
    │
    └── ~/projects/local-infrastructure/  ◄─── Shared infra for all services
        └── docker-compose.yml            ◄─── postgres, redis, rabbitmq

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                      SHARED DOCKER NETWORK                                  │
    │                                                                             │
    │   All services connect to the same external network: "microservices-net"   │
    │                                                                             │
    │  ┌───────────────────────────────────────────────────────────────────────┐ │
    │  │ local-infrastructure (always running)                                 │ │
    │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                            │ │
    │  │  │ Postgres │  │  Redis   │  │ RabbitMQ │                            │ │
    │  │  │  :5432   │  │  :6379   │  │  :5672   │                            │ │
    │  │  └──────────┘  └──────────┘  └──────────┘                            │ │
    │  └───────────────────────────────────────────────────────────────────────┘ │
    │                              │                                             │
    │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                      │
    │  │user-service │   │product-svc  │   │order-service│   ◄─── Run only     │
    │  │   :3001     │   │   :3002     │   │   :3003     │       what you need │
    │  └─────────────┘   └─────────────┘   └─────────────┘                      │
    └─────────────────────────────────────────────────────────────────────────────┘`,
            subsections: [
                {
                    title: "Shared Infrastructure Setup",
                    content: `First, create a shared infrastructure repository that all services can connect to:`,
                    code: `# Create shared infrastructure directory
mkdir -p ~/projects/local-infrastructure
cd ~/projects/local-infrastructure

# Create the shared Docker network (run once)
docker network create microservices-net`,
                    codeLanguage: "bash",
                    codeFilename: "setup.sh"
                },
                {
                    title: "Shared Infrastructure Docker Compose",
                    content: `This compose file provides databases and message brokers for all your services:`,
                    code: `# ~/projects/local-infrastructure/docker-compose.yml
# ═══════════════════════════════════════════════════════════
# SHARED INFRASTRUCTURE FOR POLYREPO LOCAL DEVELOPMENT
# ═══════════════════════════════════════════════════════════
# Run this FIRST, then start individual services as needed

version: '3.8'

services:
  # ─────────────────────────────────────────────────────────
  # PostgreSQL - Shared database server
  # ─────────────────────────────────────────────────────────
  postgres:
    image: postgres:15-alpine
    container_name: local-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: localdev123
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    networks:
      - microservices-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ─────────────────────────────────────────────────────────
  # Redis - Shared cache
  # ─────────────────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    container_name: local-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - microservices-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ─────────────────────────────────────────────────────────
  # RabbitMQ - Shared message broker
  # ─────────────────────────────────────────────────────────
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: local-rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"   # Management UI: http://localhost:15672
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: localdev123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - microservices-net
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ─────────────────────────────────────────────────────────
  # Adminer - Database UI
  # ─────────────────────────────────────────────────────────
  adminer:
    image: adminer
    container_name: local-adminer
    ports:
      - "8080:8080"
    networks:
      - microservices-net

  # ─────────────────────────────────────────────────────────
  # Mailhog - Email testing (catches all outgoing emails)
  # ─────────────────────────────────────────────────────────
  mailhog:
    image: mailhog/mailhog
    container_name: local-mailhog
    ports:
      - "1025:1025"   # SMTP
      - "8025:8025"   # Web UI: http://localhost:8025
    networks:
      - microservices-net

networks:
  microservices-net:
    external: true    # Use the pre-created network

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.yml"
                },
                {
                    title: "Individual Service Docker Compose",
                    content: `Each service repository has its own docker-compose.yml that connects to the shared network:`,
                    code: `# ~/projects/user-service/docker-compose.yml
# ═══════════════════════════════════════════════════════════
# USER SERVICE - Local Development
# ═══════════════════════════════════════════════════════════
# Assumes local-infrastructure is running

version: '3.8'

services:
  user-service:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: user-service
    ports:
      - "3001:3001"
    environment:
      NODE_ENV: development
      PORT: 3001
      # Connect to shared infrastructure
      DATABASE_URL: postgresql://postgres:localdev123@local-postgres:5432/users_db
      REDIS_URL: redis://local-redis:6379
      RABBITMQ_URL: amqp://admin:localdev123@local-rabbitmq:5672
      # Service discovery (other services)
      PRODUCT_SERVICE_URL: http://product-service:3002
      ORDER_SERVICE_URL: http://order-service:3003
      # Auth
      JWT_SECRET: local-dev-jwt-secret
    volumes:
      # Hot reload
      - ./src:/app/src:ro
      - ./prisma:/app/prisma:ro
      - /app/node_modules
    networks:
      - microservices-net
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  microservices-net:
    external: true    # Connect to the shared network`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.yml"
                },
                {
                    title: "Service Dockerfile (Development)",
                    content: `Development Dockerfile for an individual service:`,
                    code: `# ~/projects/user-service/Dockerfile.dev
# ═══════════════════════════════════════════════════════════
# USER SERVICE - Development Dockerfile
# ═══════════════════════════════════════════════════════════

FROM node:20-alpine

# Install tools for healthcheck and debugging
RUN apk add --no-cache wget curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including devDependencies)
RUN npm ci

# Copy Prisma schema (if using Prisma)
COPY prisma ./prisma/

# Generate Prisma client
RUN npx prisma generate

# Copy source code (will be overridden by volume mount)
COPY . .

# Expose port
EXPOSE 3001

# Use nodemon for hot reload
CMD ["npm", "run", "dev"]`,
                    codeLanguage: "dockerfile",
                    codeFilename: "Dockerfile.dev"
                },
                {
                    title: "Production Dockerfile",
                    content: `Optimized multi-stage production Dockerfile:`,
                    code: `# ~/projects/user-service/Dockerfile
# ═══════════════════════════════════════════════════════════
# USER SERVICE - Production Dockerfile
# ═══════════════════════════════════════════════════════════

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Generate Prisma client
RUN npx prisma generate

# Build TypeScript
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Don't run as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 appuser

# Copy only what's needed
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY package*.json ./

# Security
USER appuser

EXPOSE 3001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD wget --no-verbose --tries=1 --spider http://localhost:3001/health || exit 1

CMD ["node", "dist/main.js"]`,
                    codeLanguage: "dockerfile",
                    codeFilename: "Dockerfile"
                },
                {
                    title: "Running Polyrepo Services",
                    content: `Commands to manage individual services in a polyrepo setup:`,
                    code: `# ═══════════════════════════════════════════════════════════
# POLYREPO LOCAL DEVELOPMENT COMMANDS
# ═══════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────
# STEP 1: Start shared infrastructure (run once)
# ─────────────────────────────────────────────────────────
cd ~/projects/local-infrastructure

# Create shared network (first time only)
docker network create microservices-net

# Start all infrastructure
docker compose up -d

# Verify infrastructure is running
docker compose ps
# Should see: local-postgres, local-redis, local-rabbitmq running

# ─────────────────────────────────────────────────────────
# STEP 2: Start the service you're working on
# ─────────────────────────────────────────────────────────
cd ~/projects/user-service

# Start user-service
docker compose up -d

# View logs
docker compose logs -f

# ─────────────────────────────────────────────────────────
# STEP 3: Start other services if needed for testing
# ─────────────────────────────────────────────────────────
# In another terminal:
cd ~/projects/product-service
docker compose up -d

cd ~/projects/order-service
docker compose up -d

# ─────────────────────────────────────────────────────────
# COMMON COMMANDS
# ─────────────────────────────────────────────────────────

# Check all running containers
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

# View which containers are on microservices-net
docker network inspect microservices-net

# Stop a specific service
cd ~/projects/user-service
docker compose down

# Stop all infrastructure (WARNING: stops everything!)
cd ~/projects/local-infrastructure
docker compose down

# Reset a service's database
docker exec -it local-postgres psql -U postgres -c "DROP DATABASE IF EXISTS users_db; CREATE DATABASE users_db;"

# View RabbitMQ queues
# Open http://localhost:15672 (admin/localdev123)

# View database with Adminer
# Open http://localhost:8080

# Check caught emails in Mailhog
# Open http://localhost:8025`,
                    codeLanguage: "bash",
                    codeFilename: "polyrepo-commands.sh",
                    keyPoints: [
                        "Start shared infrastructure FIRST, then individual services",
                        "All services connect to the same external Docker network",
                        "Each service can be started/stopped independently",
                        "Use container names (not localhost) for inter-service communication",
                        "Run only the services you need - saves resources!"
                    ]
                }
            ],
            tip: "Create shell aliases for common workflows:\n`alias infra-up='cd ~/projects/local-infrastructure && docker compose up -d'`\n`alias infra-down='cd ~/projects/local-infrastructure && docker compose down'`"
        },

        // Section 4: Running Without Docker
        {
            id: "without-docker",
            emoji: "💻",
            shortTitle: "Without Docker",
            title: "Running Services Without Docker",
            subtitle: "Native Node.js development with Docker only for infrastructure",
            description: `Sometimes you want faster iteration without Docker overhead. Run your services natively while using Docker only for databases and infrastructure.`,
            subsections: [
                {
                    title: "Hybrid Setup",
                    content: `Use Docker for infrastructure, but run services directly with Node.js:`,
                    code: `# ═══════════════════════════════════════════════════════════
# HYBRID SETUP: Docker for infra, Native Node.js for services
# ═══════════════════════════════════════════════════════════

# 1. Start only infrastructure with Docker
cd ~/projects/local-infrastructure
docker compose up -d postgres redis rabbitmq

# 2. Run your service natively (much faster hot reload!)
cd ~/projects/user-service

# Install dependencies
npm install

# Run database migrations
DATABASE_URL="postgresql://postgres:localdev123@localhost:5432/users_db" npx prisma migrate dev

# Start in development mode
npm run dev

# ─────────────────────────────────────────────────────────
# ENVIRONMENT VARIABLES FOR NATIVE MODE
# ─────────────────────────────────────────────────────────
# Create a .env.local file:

cat > .env.local << 'EOF'
NODE_ENV=development
PORT=3001

# Database - localhost because running outside Docker
DATABASE_URL=postgresql://postgres:localdev123@localhost:5432/users_db

# Redis
REDIS_URL=redis://localhost:6379

# RabbitMQ
RABBITMQ_URL=amqp://admin:localdev123@localhost:5672

# Other services (if running natively too)
PRODUCT_SERVICE_URL=http://localhost:3002
ORDER_SERVICE_URL=http://localhost:3003

JWT_SECRET=local-dev-jwt-secret
EOF`,
                    codeLanguage: "bash",
                    codeFilename: "hybrid-setup.sh"
                },
                {
                    title: "package.json Scripts",
                    content: `Add helpful npm scripts for local development:`,
                    code: `{
  "scripts": {
    "dev": "nodemon --watch src -e ts --exec ts-node src/main.ts",
    "dev:debug": "nodemon --watch src -e ts --exec 'node --inspect -r ts-node/register src/main.ts'",
    "build": "tsc",
    "start": "node dist/main.js",
    
    "db:migrate": "prisma migrate dev",
    "db:generate": "prisma generate",
    "db:studio": "prisma studio",
    "db:reset": "prisma migrate reset --force",
    
    "test": "jest",
    "test:watch": "jest --watch",
    "test:cov": "jest --coverage",
    "test:e2e": "jest --config ./test/jest-e2e.json",
    
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    
    "docker:build": "docker build -t user-service .",
    "docker:dev": "docker compose up -d",
    "docker:logs": "docker compose logs -f"
  }
}`,
                    codeLanguage: "json",
                    codeFilename: "package.json"
                },
                {
                    title: "Running Multiple Services with PM2",
                    content: `Use PM2 to manage multiple services in development:`,
                    code: `# Install PM2 globally
npm install -g pm2

# Create ecosystem file in your workspace root
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'user-service',
      cwd: './user-service',
      script: 'npm',
      args: 'run dev',
      env: {
        NODE_ENV: 'development',
        PORT: 3001,
        DATABASE_URL: 'postgresql://postgres:localdev123@localhost:5432/users_db'
      }
    },
    {
      name: 'product-service',
      cwd: './product-service',
      script: 'npm',
      args: 'run dev',
      env: {
        NODE_ENV: 'development',
        PORT: 3002,
        DATABASE_URL: 'postgresql://postgres:localdev123@localhost:5432/products_db'
      }
    },
    {
      name: 'order-service',
      cwd: './order-service',
      script: 'npm',
      args: 'run dev',
      env: {
        NODE_ENV: 'development',
        PORT: 3003,
        DATABASE_URL: 'postgresql://postgres:localdev123@localhost:5432/orders_db'
      }
    }
  ]
};
EOF

# Start all services
pm2 start ecosystem.config.js

# View logs
pm2 logs

# View status
pm2 status

# Stop all
pm2 stop all

# Restart a specific service
pm2 restart user-service`,
                    codeLanguage: "bash",
                    codeFilename: "pm2-setup.sh"
                }
            ],
            warning: "When running services natively, use `localhost` for infrastructure URLs. When running in Docker, use container names like `local-postgres`."
        },

        // Section 5: Testing Locally
        {
            id: "local-testing",
            emoji: "🧪",
            shortTitle: "Local Testing",
            title: "Testing Microservices Locally",
            subtitle: "Unit, integration, and end-to-end testing strategies",
            description: `Comprehensive testing setup for local development.`,
            subsections: [
                {
                    title: "Test Docker Compose",
                    content: `Isolated test environment that doesn't affect development data:`,
                    code: `# docker-compose.test.yml
# ═══════════════════════════════════════════════════════════
# ISOLATED TEST ENVIRONMENT
# ═══════════════════════════════════════════════════════════

version: '3.8'

services:
  # Test database (separate from dev)
  postgres-test:
    image: postgres:15-alpine
    container_name: postgres-test
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: testpassword
      POSTGRES_DB: test_db
    ports:
      - "5433:5432"    # Different port than dev!
    tmpfs:
      - /var/lib/postgresql/data    # In-memory for speed
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Test Redis
  redis-test:
    image: redis:7-alpine
    container_name: redis-test
    ports:
      - "6380:6379"    # Different port than dev!
    tmpfs:
      - /data

  # Test RabbitMQ
  rabbitmq-test:
    image: rabbitmq:3-alpine
    container_name: rabbitmq-test
    ports:
      - "5673:5672"    # Different port than dev!

  # Service under test
  user-service-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: user-service-test
    environment:
      NODE_ENV: test
      DATABASE_URL: postgresql://postgres:testpassword@postgres-test:5432/test_db
      REDIS_URL: redis://redis-test:6379
      RABBITMQ_URL: amqp://rabbitmq-test:5672
    depends_on:
      postgres-test:
        condition: service_healthy
    command: npm run test:e2e`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.test.yml"
                },
                {
                    title: "Running Tests",
                    content: `Commands for different types of tests:`,
                    code: `# ═══════════════════════════════════════════════════════════
# TESTING COMMANDS
# ═══════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────
# UNIT TESTS (no Docker needed)
# ─────────────────────────────────────────────────────────
npm run test
npm run test:watch        # Watch mode
npm run test:cov          # With coverage

# ─────────────────────────────────────────────────────────
# INTEGRATION TESTS (needs test infrastructure)
# ─────────────────────────────────────────────────────────
# Start test infrastructure
docker compose -f docker-compose.test.yml up -d postgres-test redis-test

# Run integration tests
DATABASE_URL="postgresql://postgres:testpassword@localhost:5433/test_db" npm run test:integration

# Stop test infrastructure
docker compose -f docker-compose.test.yml down -v

# ─────────────────────────────────────────────────────────
# END-TO-END TESTS (full containerized)
# ─────────────────────────────────────────────────────────
# Build and run everything in containers
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
docker compose -f docker-compose.test.yml down -v

# ─────────────────────────────────────────────────────────
# CONTRACT TESTS (API compatibility)
# ─────────────────────────────────────────────────────────
# Using Pact for contract testing
npm run test:contract

# ─────────────────────────────────────────────────────────
# LOAD TESTING (with k6)
# ─────────────────────────────────────────────────────────
# First, start your services
docker compose up -d

# Run k6 load test
docker run --rm -i --network=microservices-network grafana/k6 run - <tests/load/user-service.k6.js`,
                    codeLanguage: "bash",
                    codeFilename: "test-commands.sh"
                },
                {
                    title: "Sample k6 Load Test",
                    content: `Performance testing script for your APIs:`,
                    code: `// tests/load/user-service.k6.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up to 20 users
    { duration: '1m', target: 20 },    // Stay at 20 users
    { duration: '30s', target: 50 },   // Ramp up to 50 users
    { duration: '1m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.1'],     // Error rate < 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3001';

export default function () {
  // Test health endpoint
  const healthRes = http.get(\`\${BASE_URL}/health\`);
  check(healthRes, {
    'health status is 200': (r) => r.status === 200,
  });

  // Test user listing
  const usersRes = http.get(\`\${BASE_URL}/api/users\`, {
    headers: { 'Authorization': 'Bearer test-token' },
  });
  check(usersRes, {
    'users status is 200': (r) => r.status === 200,
    'users response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1);
}`,
                    codeLanguage: "javascript",
                    codeFilename: "user-service.k6.js"
                }
            ]
        },

        // Section 6: Debugging
        {
            id: "debugging",
            emoji: "🐛",
            shortTitle: "Debugging",
            title: "Debugging Microservices Locally",
            subtitle: "Tools and techniques for debugging containerized services",
            description: `Effective debugging strategies for local microservices development.`,
            subsections: [
                {
                    title: "VS Code Debug Configuration",
                    content: `Configure VS Code to attach to services running in Docker:`,
                    code: `// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    // Debug service running natively
    {
      "type": "node",
      "request": "launch",
      "name": "Debug User Service (Native)",
      "runtimeArgs": ["-r", "ts-node/register"],
      "args": ["\${workspaceFolder}/src/main.ts"],
      "env": {
        "NODE_ENV": "development",
        "PORT": "3001",
        "DATABASE_URL": "postgresql://postgres:localdev123@localhost:5432/users_db"
      },
      "console": "integratedTerminal"
    },
    
    // Attach to service running in Docker
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Docker (User Service)",
      "port": 9229,
      "address": "localhost",
      "localRoot": "\${workspaceFolder}",
      "remoteRoot": "/app",
      "sourceMaps": true,
      "restart": true
    },
    
    // Debug current test file
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Current Test",
      "program": "\${workspaceFolder}/node_modules/.bin/jest",
      "args": [
        "\${relativeFile}",
        "--runInBand",
        "--no-cache"
      ],
      "console": "integratedTerminal"
    }
  ]
}`,
                    codeLanguage: "json",
                    codeFilename: ".vscode/launch.json"
                },
                {
                    title: "Enable Debugging in Docker",
                    content: `Modify your Docker Compose to expose debug port:`,
                    code: `# docker-compose.debug.yml
version: '3.8'

services:
  user-service:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3001:3001"
      - "9229:9229"    # Debug port
    command: node --inspect=0.0.0.0:9229 -r ts-node/register src/main.ts
    environment:
      - NODE_ENV=development

# Run with:
# docker compose -f docker-compose.yml -f docker-compose.debug.yml up user-service`,
                    codeLanguage: "yaml",
                    codeFilename: "docker-compose.debug.yml"
                },
                {
                    title: "Useful Debugging Commands",
                    content: `Common commands for debugging containerized services:`,
                    code: `# ═══════════════════════════════════════════════════════════
# DEBUGGING COMMANDS
# ═══════════════════════════════════════════════════════════

# View real-time logs
docker compose logs -f user-service

# View last 100 lines
docker compose logs --tail=100 user-service

# Search logs for errors
docker compose logs user-service 2>&1 | grep -i error

# Get shell access to container
docker compose exec user-service sh

# Check environment variables
docker compose exec user-service env

# Test database connection from container
docker compose exec user-service sh -c 'nc -zv postgres 5432'

# Check network connectivity
docker compose exec user-service ping -c 3 product-service

# View container resource usage
docker stats user-service

# Inspect container details
docker inspect user-service

# Check which ports are exposed
docker compose ps

# View Docker events in real-time
docker events --filter container=user-service

# Clean up for fresh start
docker compose down -v
docker system prune -f`,
                    codeLanguage: "bash",
                    codeFilename: "debug-commands.sh"
                }
            ],
            tip: "Add `DEBUG=*` environment variable to enable verbose logging for many Node.js libraries. For NestJS, use `DEBUG=nest:*`."
        },

        // Section 7: Common Issues
        {
            id: "common-issues",
            emoji: "⚠️",
            shortTitle: "Troubleshooting",
            title: "Common Issues & Solutions",
            subtitle: "Quick fixes for frequent local development problems",
            description: `Solutions to the most common problems when running microservices locally.`,
            subsections: [
                {
                    title: "Port Already in Use",
                    code: `# Error: Port 3000 is already in use

# Find what's using the port
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :3000
kill -9 <PID>

# Or just use a different port in docker-compose.yml:
ports:
  - "3100:3000"  # Map to different host port`,
                    codeLanguage: "bash",
                    codeFilename: "port-fix.sh"
                },
                {
                    title: "Container Can't Connect to Database",
                    code: `# Error: ECONNREFUSED connecting to postgres

# 1. Check if postgres is running
docker compose ps postgres

# 2. Check if it's healthy
docker compose logs postgres

# 3. Verify network connectivity
docker compose exec user-service ping -c 3 postgres

# 4. Common mistake: Using 'localhost' instead of container name
# WRONG: DATABASE_URL=postgresql://postgres:pass@localhost:5432/db
# RIGHT: DATABASE_URL=postgresql://postgres:pass@postgres:5432/db

# 5. Check if database exists
docker compose exec postgres psql -U postgres -c "\\l"

# 6. Wait for postgres to be ready (in depends_on)
depends_on:
  postgres:
    condition: service_healthy`,
                    codeLanguage: "bash",
                    codeFilename: "db-connection-fix.sh"
                },
                {
                    title: "Hot Reload Not Working",
                    code: `# Changes not reflecting in container

# 1. Check volume mounts are correct
docker compose config | grep -A5 volumes

# 2. Verify files are being watched
docker compose exec user-service ls -la /app/src

# 3. Check if nodemon is running
docker compose logs user-service | grep nodemon

# 4. For Windows: Enable file sharing in Docker Desktop
# Settings > Resources > File Sharing > Add your project folder

# 5. Force polling (slower but more reliable)
# In nodemon.json:
{
  "legacyWatch": true,
  "watch": ["src"],
  "ext": "ts,json"
}

# 6. Rebuild container if node_modules changed
docker compose build --no-cache user-service
docker compose up -d user-service`,
                    codeLanguage: "bash",
                    codeFilename: "hot-reload-fix.sh"
                },
                {
                    title: "Out of Memory / Slow Performance",
                    code: `# Docker running slow or crashing

# 1. Check Docker resource usage
docker stats

# 2. Increase Docker Desktop memory
# Settings > Resources > Memory > 8GB+

# 3. Clean up unused resources
docker system prune -a
docker volume prune

# 4. Remove dangling images
docker image prune

# 5. Stop containers you're not using
docker compose stop product-service order-service

# 6. Use lightweight base images
# BEFORE: FROM node:20
# AFTER:  FROM node:20-alpine

# 7. Limit container resources
services:
  user-service:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M`,
                    codeLanguage: "bash",
                    codeFilename: "performance-fix.sh"
                },
                {
                    title: "Quick Reference Table",
                    content: `
| Problem | Cause | Solution |
|---------|-------|----------|
| **Port in use** | Another process using port | Kill process or change port |
| **Connection refused** | Using localhost in Docker | Use container name instead |
| **Database not ready** | Service started before DB | Add healthcheck + depends_on |
| **Changes not reflecting** | Volume mount issue | Check paths, enable polling |
| **Container keeps restarting** | App crashing | Check logs: \`docker compose logs\` |
| **Network timeout** | Wrong network | Ensure services on same network |
| **Permission denied** | File ownership | Run as non-root, check volume permissions |
| **Out of memory** | Too many containers | Increase Docker memory, prune unused |
| **Build taking forever** | No layer caching | Order Dockerfile commands properly |
| **Image not found** | Not built yet | Run \`docker compose build\` first |
`
                }
            ]
        },

        // Section 8: Useful Scripts
        {
            id: "scripts",
            emoji: "📜",
            shortTitle: "Scripts",
            title: "Useful Development Scripts",
            subtitle: "Automate common tasks with these helper scripts",
            description: `Ready-to-use scripts to streamline your local development workflow.`,
            subsections: [
                {
                    title: "Makefile for Common Tasks",
                    content: `Create a Makefile in your project root for quick commands:`,
                    code: `# Makefile
# ═══════════════════════════════════════════════════════════
# MICROSERVICES LOCAL DEVELOPMENT MAKEFILE
# ═══════════════════════════════════════════════════════════

.PHONY: help dev prod down logs clean test

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev      - Start development environment with hot reload"
	@echo "  make prod     - Start production-like environment"
	@echo "  make down     - Stop all containers"
	@echo "  make logs     - View all logs"
	@echo "  make clean    - Remove all containers, volumes, and images"
	@echo "  make test     - Run tests in isolated environment"
	@echo "  make shell    - Open shell in user-service container"
	@echo "  make db-reset - Reset all databases"

# Start development environment
dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started!"
	@echo "📊 API Gateway: http://localhost:3000"
	@echo "👤 User Service: http://localhost:3001"
	@echo "📦 Product Service: http://localhost:3002"
	@echo "🛒 Order Service: http://localhost:3003"
	@echo "🐰 RabbitMQ UI: http://localhost:15672"
	@echo "🗄️  Adminer: http://localhost:8080"

# Start production-like environment
prod:
	docker compose up -d --build
	@echo "✅ Production environment started!"

# Stop all containers
down:
	docker compose down
	@echo "✅ All containers stopped"

# View logs
logs:
	docker compose logs -f

# View logs for specific service
logs-%:
	docker compose logs -f $*

# Clean everything
clean:
	docker compose down -v --rmi local
	docker system prune -f
	@echo "✅ Cleaned up!"

# Run tests
test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down -v

# Open shell in container
shell:
	docker compose exec user-service sh

shell-%:
	docker compose exec $* sh

# Reset databases
db-reset:
	docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS users_db; CREATE DATABASE users_db;"
	docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS products_db; CREATE DATABASE products_db;"
	docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS orders_db; CREATE DATABASE orders_db;"
	@echo "✅ Databases reset!"

# Run migrations
migrate:
	docker compose exec user-service npx prisma migrate dev
	docker compose exec product-service npx prisma migrate dev
	docker compose exec order-service npx prisma migrate dev
	@echo "✅ Migrations complete!"

# Build specific service
build-%:
	docker compose build $*
	@echo "✅ Built $*"

# Restart specific service
restart-%:
	docker compose restart $*
	@echo "✅ Restarted $*"`,
                    codeLanguage: "makefile",
                    codeFilename: "Makefile"
                },
                {
                    title: "PowerShell Script (Windows)",
                    content: `For Windows users, here's a PowerShell equivalent:`,
                    code: `# scripts/dev.ps1
# ═══════════════════════════════════════════════════════════
# WINDOWS POWERSHELL DEVELOPMENT SCRIPT
# ═══════════════════════════════════════════════════════════

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "  .\\dev.ps1 start      - Start development environment"
    Write-Host "  .\\dev.ps1 stop       - Stop all containers"
    Write-Host "  .\\dev.ps1 logs       - View all logs"
    Write-Host "  .\\dev.ps1 clean      - Remove all containers and volumes"
    Write-Host "  .\\dev.ps1 test       - Run tests"
    Write-Host "  .\\dev.ps1 shell      - Open shell in user-service"
    Write-Host "  .\\dev.ps1 reset-db   - Reset all databases"
}

function Start-Dev {
    Write-Host "Starting development environment..." -ForegroundColor Green
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    Write-Host ""
    Write-Host "Services started:" -ForegroundColor Cyan
    Write-Host "  API Gateway:    http://localhost:3000"
    Write-Host "  User Service:   http://localhost:3001"
    Write-Host "  RabbitMQ UI:    http://localhost:15672"
    Write-Host "  Adminer:        http://localhost:8080"
}

function Stop-Dev {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker compose down
    Write-Host "Done!" -ForegroundColor Green
}

function Show-Logs {
    docker compose logs -f
}

function Clean-All {
    Write-Host "Cleaning up..." -ForegroundColor Yellow
    docker compose down -v --rmi local
    docker system prune -f
    Write-Host "Done!" -ForegroundColor Green
}

function Run-Tests {
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
    docker compose -f docker-compose.test.yml down -v
}

function Open-Shell {
    docker compose exec user-service sh
}

function Reset-Database {
    Write-Host "Resetting databases..." -ForegroundColor Yellow
    docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS users_db; CREATE DATABASE users_db;"
    docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS products_db; CREATE DATABASE products_db;"
    docker compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS orders_db; CREATE DATABASE orders_db;"
    Write-Host "Done!" -ForegroundColor Green
}

switch ($Command) {
    "start"    { Start-Dev }
    "stop"     { Stop-Dev }
    "logs"     { Show-Logs }
    "clean"    { Clean-All }
    "test"     { Run-Tests }
    "shell"    { Open-Shell }
    "reset-db" { Reset-Database }
    default    { Show-Help }
}`,
                    codeLanguage: "powershell",
                    codeFilename: "dev.ps1"
                }
            ],
            tip: "Add these scripts to your PATH or create aliases in your shell profile for even faster access!"
        }
    ]
};

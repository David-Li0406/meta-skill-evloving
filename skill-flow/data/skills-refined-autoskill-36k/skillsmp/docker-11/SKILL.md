---
name: docker
description: Help with Docker setup, commands, and troubleshooting for the GeroCare development environment.
---

# Docker Development Environment

This skill helps you understand and work with the Docker setup for GeroCare development.

## When to Use

- When creating or modifying Docker configuration files (Dockerfile, docker-compose.yml, .dockerignore)
- When troubleshooting Docker issues
- When explaining Docker commands to developers
- When setting up the development environment
- When working with volumes, ports, or container networking

## Project Docker Setup

GeroCare uses Docker to containerize the development environment, eliminating the need for local Node.js, npm, or Firebase Tools installation.

### Architecture

- **Base Image**: `node:20.19.0` (matches package.json engines requirement)
- **Services**: Two separate services for better isolation:
  - `app`: Vite dev server
  - `emulators`: Firebase emulators (Auth, Firestore, UI)
- **Network**: Internal Docker network (`gerocare-network`) for service communication
- **Hot Reload**: Enabled via volume mounts for source code in `app` service
- **Data Persistence**: Firebase emulator data persisted in Docker volumes
- **Healthcheck**: Emulators service has healthcheck to ensure readiness before `app` starts

### Port Mapping

| Port | Service | Description |
|------|---------|-------------|
| 5173 | Vite Dev Server | Frontend development server |
| 8080 | Firestore Emulator | Firebase Firestore emulator |
| 9099 | Auth Emulator | Firebase Authentication emulator |
| 4000 | Firebase UI | Firebase Emulator Suite UI |

### Volume Strategy

1. **Source Code Volume** (`app` service only): `.:/app` - Mounts project root for hot-reload
2. **Node Modules Volume** (`app` service only): `/app/node_modules` - Anonymous volume to prevent host/container conflicts
3. **Firestore Data Volume** (`emulators` service only): `firestore-data:/app/firestore_export` - Persistent volume for emulator data

### Network Strategy

- **Internal Network**: `gerocare-network` (bridge driver)
- **Service Communication**: Services use service names as hostnames
- **App → Emulators**: `app` connects to emulators using `emulators` as hostname (via `VITE_EMULATORS_HOST` env var)

## Common Commands

### Starting the Environment

```bash
# Build and start (first time or after Dockerfile changes)
docker-compose up --build

# Start existing containers
docker-compose up

# Start in detached mode (background)
docker-compose up -d
```

### Stopping the Environment

```bash
# Stop containers (keeps volumes)
docker-compose down

# Stop and remove volumes (clears Firebase emulator data)
docker-compose down -v
```

### Running Commands in Container

```bash
# Run npm commands in app service
docker-compose exec app npm run lint
docker-compose exec app npm run test:unit
docker-compose exec app npm run build

# Run commands in emulators service
docker-compose exec emulators firebase --version

# Run shell commands
docker-compose exec app sh        # In app service
docker-compose exec emulators sh  # In emulators service
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app       # App (Vite) logs
docker-compose logs -f emulators # Emulators logs

# Last 100 lines
docker-compose logs --tail=100
```

### Rebuilding

```bash
# Rebuild without cache
docker-compose build --no-cache

# Rebuild and restart
docker-compose up --build
```

## File Structure

### Dockerfile
- Base: `node:20.19.0`
- Installs Java 21 (for Firebase Emulators), curl (for healthchecks), and `firebase-tools` globally
- Copies package files and runs `npm ci`
- Exposes ports: 5173, 8080, 9099, 4000
- No default CMD (each service defines its own command)

### docker-compose.yml
- **Service: `app`**
  - Runs `npm run dev` (Vite dev server)
  - Mounts source code for hot-reload
  - Exposes port 5173
  - Depends on `emulators` with healthcheck condition
  - Environment: `VITE_EMULATORS_HOST=emulators` for internal communication
  
- **Service: `emulators`**
  - Runs `npm run emulators` (Firebase emulators)
  - Persistent volume for Firestore data
  - Exposes ports 4000 (UI), 8080 (Firestore), 9099 (Auth)
  - Healthcheck to verify readiness
  
- **Network: `gerocare-network`**
  - Bridge network for internal service communication

### .dockerignore
- Excludes `node_modules`, `dist`, logs
- Excludes `.git`, `.env.local`, temporary files
- Optimizes build context size

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:
1. Check what's using the port: `lsof -i :5173` (macOS/Linux) or `netstat -ano | findstr :5173` (Windows)
2. Stop local services using those ports
3. Or change ports in `docker-compose.yml`

### Hot Reload Not Working

1. Verify volume mount: `docker-compose exec app ls -la /app/src`
2. Check file permissions
3. Ensure Vite is watching the correct directory

### Firebase Emulators Not Starting

1. Check logs: `docker-compose logs emulators`
2. Verify Firebase Tools installation: `docker-compose exec emulators firebase --version`
3. Check `firebase.json` configuration
4. Verify healthcheck status: `docker-compose ps`
5. Ensure `firestore_export` directory exists or is created

### App Not Connecting to Emulators

1. Verify both services are running: `docker-compose ps`
2. Check emulators health: `docker-compose logs emulators`
3. Verify network connectivity: `docker-compose exec app ping emulators`
4. Check `VITE_EMULATORS_HOST` environment variable in `app` service

### Node Modules Issues

If you encounter module resolution errors:
1. Rebuild: `docker-compose down && docker-compose up --build`
2. Clear node_modules volume: `docker-compose down -v` (then rebuild)
3. Check volume mount: `docker-compose exec app ls -la /app/node_modules`

### Container Won't Start

1. Check Docker is running
2. Verify Dockerfile syntax
3. Check logs: `docker-compose logs`
4. Try rebuilding: `docker-compose build --no-cache`

## Best Practices

1. **Always use docker-compose** for consistency across team
2. **Don't commit node_modules** - they're in .dockerignore
3. **Use volumes** for data persistence (Firebase emulator data)
4. **Check logs first** when troubleshooting
5. **Rebuild after dependency changes** in package.json

## Integration with Development Workflow

The Docker setup runs services separately:
- `npm run dev` - Vite dev server (in `app` service)
- `npm run emulators` - Firebase emulators (in `emulators` service)
- All npm scripts work the same inside containers
- Hot-reload works identically to local development
- Services communicate via internal Docker network

### Starting Services Separately

You can start services independently:
- `docker-compose up emulators` - Only emulators
- `docker-compose up app` - Only app (waits for emulators)
- `docker-compose up` - Both services

## Accessing Services

Once running, access:
- **App**: http://localhost:5173
- **Firebase UI**: http://localhost:4000
- **Firestore**: http://localhost:8080
- **Auth**: http://localhost:9099

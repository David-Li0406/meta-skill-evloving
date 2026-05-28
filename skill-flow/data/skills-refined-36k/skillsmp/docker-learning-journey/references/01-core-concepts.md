# Docker Core Concepts

Deep dive into Docker fundamentals for Python developers.

---

## What Problem Does Docker Solve?

### The "Works on My Machine" Problem

```
Developer A: "It works on my machine!"
Developer B: "It crashes on mine..."

Why?
- Different Python versions (3.9 vs 3.12)
- Different OS (Windows vs Linux vs Mac)
- Missing system libraries
- Different environment variables
- Conflicting package versions
```

### Docker's Solution: Containerization

```
┌─────────────────────────────────────────────────────────────┐
│  Container = Your App + Everything It Needs                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Your FastAPI App                                        ││
│  │  Python 3.12                                             ││
│  │  All pip packages (exact versions)                       ││
│  │  System libraries                                        ││
│  │  Environment variables                                   ││
│  └─────────────────────────────────────────────────────────┘│
│  Runs IDENTICALLY everywhere: Dev laptop, CI/CD, Production │
└─────────────────────────────────────────────────────────────┘
```

---

## Containers vs Virtual Machines

### Virtual Machine (Heavy)

```
┌─────────────────────────────────────────┐
│  Your Application                        │
├─────────────────────────────────────────┤
│  Guest OS (Full Linux/Windows)           │  ← 2-20 GB
├─────────────────────────────────────────┤
│  Hypervisor (VMware, VirtualBox)         │
├─────────────────────────────────────────┤
│  Host OS (Your Windows/Mac)              │
└─────────────────────────────────────────┘
Boot time: Minutes
Size: Gigabytes
```

### Container (Lightweight)

```
┌─────────────────────────────────────────┐
│  Your Application                        │
├─────────────────────────────────────────┤
│  Container Runtime (just libs needed)    │  ← 50-500 MB
├─────────────────────────────────────────┤
│  Docker Engine                           │
├─────────────────────────────────────────┤
│  Host OS (shares kernel)                 │
└─────────────────────────────────────────┘
Boot time: Seconds
Size: Megabytes
```

### Key Difference

| Aspect | VM | Container |
|--------|----|-----------|
| Isolation | Complete (own OS) | Process-level (shared kernel) |
| Size | Gigabytes | Megabytes |
| Startup | Minutes | Seconds |
| Resource use | Heavy | Light |
| Use case | Different OS needed | Same OS, isolated apps |

---

## Docker Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│  Docker Client                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  CLI commands you type:                                  ││
│  │  $ docker run                                            ││
│  │  $ docker build                                          ││
│  │  $ docker pull                                           ││
│  └─────────────────────────────────────────────────────────┘│
│                            │                                 │
│                            ▼ REST API                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Docker Daemon (dockerd)                                 ││
│  │  - Listens for API requests                              ││
│  │  - Manages Docker objects                                ││
│  │  - Handles building, running, distributing               ││
│  └─────────────────────────────────────────────────────────┘│
│                            │                                 │
│              ┌─────────────┼─────────────┐                  │
│              ▼             ▼             ▼                  │
│        ┌─────────┐  ┌───────────┐  ┌──────────┐            │
│        │ Images  │  │ Containers│  │ Networks │            │
│        └─────────┘  └───────────┘  └──────────┘            │
│              │             │             │                  │
│              └─────────────┼─────────────┘                  │
│                            ▼                                 │
│                     ┌───────────┐                           │
│                     │  Volumes  │                           │
│                     └───────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### The Four Docker Objects

#### 1. Images (Blueprints)

```
Image = Read-only template with instructions

Think of it as:
- A snapshot of a configured system
- Like a Python class definition
- Immutable (can't change, only create new versions)

Examples:
- python:3.12-slim (official Python image)
- postgres:15 (official PostgreSQL)
- your-app:v1.0 (your custom image)
```

#### 2. Containers (Running Instances)

```
Container = Running instance of an image

Think of it as:
- A process with its own filesystem
- Like a Python object (instance of class)
- Isolated from other containers
- Can be started, stopped, deleted

Lifecycle:
Created → Running → Paused → Stopped → Removed
```

#### 3. Networks (Communication)

```
Network = How containers talk to each other

Types:
- bridge (default): Containers on same host
- host: Share host's network
- none: No networking

Example:
┌─────────────┐     ┌─────────────┐
│   FastAPI   │────▶│  PostgreSQL │
│  Container  │     │  Container  │
└─────────────┘     └─────────────┘
      Both on "app-network"
```

#### 4. Volumes (Persistent Data)

```
Volume = Data that survives container restarts

Problem without volumes:
Container stops → Data LOST!

With volumes:
Container stops → Data SAFE in volume

Types:
- Named volumes: docker volume create mydata
- Bind mounts: Map host folder to container
```

---

## Image Layers (Important!)

### How Images Are Built

```
Each Dockerfile instruction creates a LAYER:

Dockerfile:
FROM python:3.12-slim     ← Layer 1 (base, ~150MB)
WORKDIR /app              ← Layer 2 (metadata only)
COPY requirements.txt .   ← Layer 3 (small file)
RUN pip install -r ...    ← Layer 4 (packages, ~100MB)
COPY . .                  ← Layer 5 (your code)
CMD ["python", "main.py"] ← Layer 6 (metadata only)
```

### Layer Caching (Why Order Matters!)

```
GOOD ORDER (fast rebuilds):
┌─────────────────────────────┐
│ FROM python:3.12-slim       │ ← Rarely changes (cached)
├─────────────────────────────┤
│ COPY requirements.txt .     │ ← Changes sometimes
├─────────────────────────────┤
│ RUN pip install ...         │ ← Cached if requirements same
├─────────────────────────────┤
│ COPY . .                    │ ← Changes often (rebuilt)
└─────────────────────────────┘

When you change code:
- Layers 1-3: CACHED (instant)
- Layer 4: Rebuilt (your code)

Total rebuild time: SECONDS
```

```
BAD ORDER (slow rebuilds):
┌─────────────────────────────┐
│ FROM python:3.12-slim       │
├─────────────────────────────┤
│ COPY . .                    │ ← ANY change invalidates
├─────────────────────────────┤
│ RUN pip install ...         │ ← Must reinstall EVERY time
└─────────────────────────────┘

When you change code:
- Layer 1: Cached
- Layers 2-3: REBUILT (code changed)

Total rebuild time: MINUTES
```

---

## Registry (Image Storage)

### What's a Registry?

```
Registry = Storage for Docker images (like PyPI for Python)

┌─────────────────────────────────────────────────────────────┐
│  Docker Hub (default registry)                               │
│  https://hub.docker.com                                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Official Images         Your Images                     ││
│  │  - python                - yourusername/myapp            ││
│  │  - postgres              - yourusername/api              ││
│  │  - nginx                                                 ││
│  │  - redis                                                 ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Image Naming Convention

```
[registry/]repository:tag

Examples:
python:3.12-slim
│       └── tag (version)
└────────── repository (image name)

docker.io/library/python:3.12-slim
│          │       │      └── tag
│          │       └── repository
│          └── namespace (library = official)
└── registry (docker.io is default)

yourusername/myapp:v1.0
│             │     └── tag
│             └── repository
└── namespace (your Docker Hub username)
```

---

## Python Analogies Summary

| Docker Concept | Python Equivalent |
|----------------|-------------------|
| Image | Class definition |
| Container | Object instance |
| Dockerfile | `__init__` method |
| `docker build` | Class definition |
| `docker run` | `obj = MyClass()` |
| `docker pull` | `pip install` |
| Registry | PyPI |
| Volume | Database/file storage |
| Network | Function calls between modules |
| Layer | Inheritance chain |

---

## Hands-On Verification

Run these commands to see concepts in action:

```bash
# See Docker info
docker info

# See all images (your blueprints)
docker images

# See running containers (your instances)
docker ps

# See ALL containers (including stopped)
docker ps -a

# See networks
docker network ls

# See volumes
docker volume ls

# See disk usage
docker system df
```

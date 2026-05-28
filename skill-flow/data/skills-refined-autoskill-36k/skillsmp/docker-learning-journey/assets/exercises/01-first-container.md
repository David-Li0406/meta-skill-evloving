# Exercise 01: Your First Container

**Level**: Beginner
**Time**: 15 minutes
**Goal**: Run Python inside a Docker container

---

## Prerequisites

- Docker Desktop installed and running
- Terminal/Command Prompt open

---

## Part 1: Verify Docker Installation

```bash
# Check Docker version
docker --version
# Expected: Docker version 24.x.x or higher

# Check Docker is running
docker info
# Should show system information without errors
```

**Checkpoint**: If you see version info, Docker is ready!

---

## Part 2: Your First Container

### Step 1: Pull the Python Image

```bash
docker pull python:3.12-slim
```

**What happened?**
- Docker downloaded the `python:3.12-slim` image from Docker Hub
- This image contains Python 3.12 on a minimal Linux system
- The image is now stored locally on your computer

### Step 2: Run Interactive Python

```bash
docker run -it python:3.12-slim python
```

**Flags explained**:
- `-i` = Interactive (keep STDIN open)
- `-t` = TTY (allocate a terminal)
- `python` = Command to run inside container

**You should see**:
```
Python 3.12.x (main, ...)
[GCC ...] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### Step 3: Try Some Python

```python
>>> print("Hello from Docker!")
Hello from Docker!

>>> import sys
>>> sys.version
'3.12.x ...'

>>> import os
>>> os.getcwd()
'/'

>>> exit()
```

**What you just did**:
- Ran Python inside an isolated Linux container
- The container had its own filesystem (root `/`)
- When you exited, the container stopped

---

## Part 3: Container Lifecycle

### Step 1: Run a Container in Background

```bash
docker run -d --name my-python python:3.12-slim sleep 60
```

**Flags explained**:
- `-d` = Detached (run in background)
- `--name my-python` = Give it a friendly name
- `sleep 60` = Keep it running for 60 seconds

### Step 2: See Running Containers

```bash
docker ps
```

**Output**:
```
CONTAINER ID   IMAGE              COMMAND      STATUS         NAMES
abc123...      python:3.12-slim   "sleep 60"   Up 10 seconds  my-python
```

### Step 3: Execute Command in Running Container

```bash
docker exec -it my-python python -c "print('Hello from inside!')"
```

**Output**: `Hello from inside!`

### Step 4: Stop the Container

```bash
docker stop my-python
```

### Step 5: See All Containers (Including Stopped)

```bash
docker ps -a
```

**Output**:
```
CONTAINER ID   IMAGE              COMMAND      STATUS                     NAMES
abc123...      python:3.12-slim   "sleep 60"   Exited (137) 5 seconds ago my-python
```

### Step 6: Remove the Container

```bash
docker rm my-python
```

---

## Part 4: Quick Experiment

### Run Python One-Liner

```bash
docker run --rm python:3.12-slim python -c "print('Quick test!')"
```

**Flag explained**:
- `--rm` = Remove container automatically when it exits

This is great for quick tests!

---

## Part 5: See Your Images

```bash
docker images
```

**Output**:
```
REPOSITORY   TAG         IMAGE ID       CREATED        SIZE
python       3.12-slim   abc123...      2 weeks ago    150MB
```

---

## Challenges

### Challenge 1: Run a Different Python Version

```bash
# Pull Python 3.11
docker pull python:3.11-slim

# Run it and check version
docker run --rm python:3.11-slim python --version
```

### Challenge 2: Run Ubuntu and Explore

```bash
# Pull Ubuntu
docker pull ubuntu:22.04

# Run interactive shell
docker run -it --rm ubuntu:22.04 bash

# Inside, try:
# ls /
# cat /etc/os-release
# exit
```

### Challenge 3: List All Downloaded Images

```bash
docker images
```

How many images do you have now?

---

## Summary

| Command | What It Does |
|---------|--------------|
| `docker pull image` | Download image |
| `docker run image` | Create & start container |
| `docker run -it image` | Interactive mode |
| `docker run -d image` | Background mode |
| `docker run --rm image` | Auto-remove when done |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop name` | Stop container |
| `docker rm name` | Remove container |
| `docker images` | List images |

---

## What You Learned

1. **Images** are downloaded from Docker Hub
2. **Containers** are running instances of images
3. Containers are **isolated** from your computer
4. Containers can run **interactively** or in **background**
5. Containers **stop** when their main process exits
6. Use `--rm` for temporary containers

---

## Next Exercise

Ready for Exercise 02? You'll create your own Dockerfile and build a custom image!

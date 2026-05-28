# Exercise 02: Build Your First Dockerfile

**Level**: Beginner
**Time**: 20 minutes
**Goal**: Create a custom Docker image for a Python application

---

## Prerequisites

- Completed Exercise 01
- Docker running
- Text editor ready

---

## Part 1: Create Project Structure

### Step 1: Create Project Folder

```bash
mkdir docker-exercise-02
cd docker-exercise-02
```

### Step 2: Create Python Application

Create `main.py`:

```python
# main.py
import sys
from datetime import datetime

def main():
    print("=" * 50)
    print("Hello from Docker!")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Current time: {datetime.now()}")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

### Step 3: Test Locally (Optional)

```bash
python main.py
```

---

## Part 2: Create Your First Dockerfile

### Step 1: Create Dockerfile

Create a file named `Dockerfile` (no extension):

```dockerfile
# Start from Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy our application
COPY main.py .

# Run the application
CMD ["python", "main.py"]
```

### Step 2: Understand Each Line

```dockerfile
FROM python:3.12-slim
# "Start with a pre-built Python 3.12 environment"
# Like: "I need a computer with Python installed"

WORKDIR /app
# "Create and use /app as our working directory"
# Like: "Create a folder and cd into it"

COPY main.py .
# "Copy main.py from my computer into the container"
# Like: "Put my code in the container"

CMD ["python", "main.py"]
# "When the container starts, run this command"
# Like: "The default thing to do is run my script"
```

---

## Part 3: Build the Image

### Step 1: Build

```bash
docker build -t my-python-app:v1 .
```

**Breakdown**:
- `docker build` = Build an image
- `-t my-python-app:v1` = Tag it with name:version
- `.` = Use current directory as build context

**Expected Output**:
```
[+] Building 5.2s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.12-slim
 => [1/3] FROM docker.io/library/python:3.12-slim
 => [2/3] WORKDIR /app
 => [3/3] COPY main.py .
 => exporting to image
 => => naming to docker.io/library/my-python-app:v1
```

### Step 2: Verify Image Created

```bash
docker images
```

**Output**:
```
REPOSITORY      TAG    IMAGE ID       SIZE
my-python-app   v1     abc123...      150MB
python          3.12   def456...      150MB
```

---

## Part 4: Run Your Image

### Step 1: Run Container

```bash
docker run my-python-app:v1
```

**Expected Output**:
```
==================================================
Hello from Docker!
==================================================
Python version: 3.12.x (...)
Current time: 2024-01-15 10:30:45.123456
==================================================
```

### Step 2: Run Multiple Times

```bash
docker run my-python-app:v1
docker run my-python-app:v1
```

Notice: Each run shows a different timestamp!
Each `docker run` creates a NEW container.

---

## Part 5: Modify and Rebuild

### Step 1: Update main.py

```python
# main.py - Updated version
import sys
from datetime import datetime

def main():
    print("🐳" * 20)
    print("Hello from Docker v2!")
    print("🐳" * 20)
    print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🐳" * 20)

if __name__ == "__main__":
    main()
```

### Step 2: Rebuild with New Tag

```bash
docker build -t my-python-app:v2 .
```

### Step 3: Run New Version

```bash
docker run my-python-app:v2
```

### Step 4: Compare Images

```bash
docker images my-python-app
```

**Output**:
```
REPOSITORY      TAG    IMAGE ID       SIZE
my-python-app   v2     new123...      150MB
my-python-app   v1     abc123...      150MB
```

You now have BOTH versions!

---

## Part 6: Add Dependencies

### Step 1: Create requirements.txt

```
colorama==0.4.6
```

### Step 2: Update main.py

```python
# main.py - With dependencies
import sys
from datetime import datetime
from colorama import Fore, Style, init

init()

def main():
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "Hello from Docker with Dependencies!" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(f"Python: {Fore.YELLOW}{sys.version_info.major}.{sys.version_info.minor}{Style.RESET_ALL}")
    print(f"Time: {Fore.MAGENTA}{datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

if __name__ == "__main__":
    main()
```

### Step 3: Update Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies FIRST (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy application code
COPY main.py .

CMD ["python", "main.py"]
```

### Step 4: Build and Run

```bash
docker build -t my-python-app:v3 .
docker run my-python-app:v3
```

---

## Part 7: Observe Layer Caching

### Step 1: Modify Only main.py

Change the greeting text in `main.py`.

### Step 2: Rebuild

```bash
docker build -t my-python-app:v4 .
```

**Watch the output**:
```
 => CACHED [2/4] WORKDIR /app
 => CACHED [3/4] COPY requirements.txt .
 => CACHED [4/4] RUN pip install ...
 => [5/4] COPY main.py .
```

**Notice**: pip install was CACHED because requirements.txt didn't change!

---

## Challenges

### Challenge 1: Add Another Dependency

Add `pyfiglet` to requirements.txt and use it to create ASCII art.

### Challenge 2: Create .dockerignore

Create `.dockerignore`:
```
__pycache__
*.pyc
.git
```

### Challenge 3: Add Environment Variable

```dockerfile
ENV APP_NAME="My Docker App"
```

Use it in Python:
```python
import os
name = os.getenv("APP_NAME", "Default")
```

---

## Cleanup

```bash
# Remove containers
docker container prune

# Remove specific images
docker rmi my-python-app:v1
docker rmi my-python-app:v2

# Or remove all unused images
docker image prune
```

---

## Summary

| Concept | What You Learned |
|---------|------------------|
| Dockerfile | Text file with build instructions |
| FROM | Base image to start from |
| WORKDIR | Set working directory |
| COPY | Copy files into image |
| RUN | Execute commands during build |
| CMD | Default command at runtime |
| `docker build -t` | Build and tag image |
| Layer caching | Order matters for speed |

---

## What You Learned

1. **Dockerfile** is a recipe for building images
2. Each instruction creates a **layer**
3. **Order matters** for caching efficiency
4. **requirements.txt** should be copied before code
5. Use **tags** to version your images
6. **Rebuilds are fast** when layers are cached

---

## Next Exercise

Ready for Exercise 03? You'll use Docker Compose to run FastAPI + PostgreSQL together!

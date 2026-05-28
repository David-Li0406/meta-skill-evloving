---
name: Dependency Management
description: Standard instructions for adding or updating backend (pip) and frontend (npm) dependencies.
---

# Dependency Management Skill

## Backend (Pip/Requirements)

The backend uses `requirements.txt`.

### 1. Identify Package
Find the package and version you need.

### 2. Update `requirements.txt`
Add the package to `backend/requirements.txt`:
```text
package-name==1.2.3
```

### 3. Install locally
```bash
# In backend root
./.venv/bin/pip install -r requirements.txt
```

### 4. Commit
```bash
git add backend/requirements.txt
git commit -m "chore(backend): add package-name"
```

---

## Frontend (NPM)

The frontend uses `npm`.

### 1. Install Package
```bash
cd frontend
npm install <package-name>
# OR for dev dependencies
npm install -D <package-name>
```

### 2. Verify
Ensure `package.json` and `package-lock.json` are updated.

### 3. Commit
```bash
git add frontend/package.json frontend/package-lock.json
git commit -m "chore(frontend): add <package-name>"
```

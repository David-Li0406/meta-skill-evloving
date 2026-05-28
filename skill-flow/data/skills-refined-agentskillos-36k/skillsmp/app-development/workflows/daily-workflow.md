# Daily Development Workflow

Step-by-step guide for daily development tasks.

## Git Workflow

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Development Cycle
- Write code
- Test locally
- Run linting: `npm run lint`
- Check build: `npm run prebuild`

### 4. Commit Changes
```bash
git add .
git commit -m "feat: description of changes"
```

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
# Create PR via GitHub UI or gh CLI
```

## Commit Message Convention

Follow conventional commits:

| Prefix | Use For |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `refactor:` | Code refactoring |
| `docs:` | Documentation changes |
| `style:` | Code style changes (formatting) |
| `test:` | Test additions/changes |
| `chore:` | Maintenance tasks |

## Pre-Commit Checklist

Before every commit:
```bash
# 1. Lint
npm run lint

# 2. Type check
npm run prebuild

# 3. Review changes
git diff --staged
```

## Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code improvements
- `docs/` - Documentation updates

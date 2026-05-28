# Git Push

Push current branch to remote repository.

## Workflow

### 1. Check Current Branch

```bash
git branch --show-current
```

### 2. Check Remote Branch Status

```bash
git status
```

- Check if local commits exist
- Check sync status with remote

### 3. Execute Push

```bash
git push origin <current-branch>
```

## Examples

### Normal Case

Current branch: `main`

```bash
git push origin main
```

### Feature Branch

Current branch: `feature/user-auth`

```bash
git push origin feature/user-auth
```

## Output Format

```
📤 Push Started
   Branch: <current branch>
   Target: origin/<current branch>

✅ Push Complete
```

## Cautions

- Notify if no commits to push
- Recommend pull first if remote has changes
- Never perform force push

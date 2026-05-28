---
description: Manage Claude Code permissions - pre-allow safe commands to reduce prompts
---

# Permission Management

จัดการ permissions สำหรับ Claude Code ตามแนวทางของ Boris Cherny - pre-allow commands ที่ปลอดภัยแทนการใช้ `--dangerously-skip-permissions`

## Usage

```
/permission              # แสดง permissions ปัจจุบัน + แนะนำ
/permission show         # แสดง permissions ทั้งหมด
/permission suggest      # แนะนำ permissions ตาม project type
/permission add [type]   # เพิ่ม permissions ตาม preset
```

## Instructions

### Step 1: Detect Project Type

```bash
echo "=== Project Detection ==="

# Check for package managers and build tools
[ -f "package.json" ] && echo "📦 Node.js project detected"
[ -f "bun.lockb" ] && echo "🍞 Bun detected"
[ -f "pnpm-lock.yaml" ] && echo "📦 pnpm detected"
[ -f "yarn.lock" ] && echo "🧶 Yarn detected"
[ -f "go.mod" ] && echo "🐹 Go project detected"
[ -f "Cargo.toml" ] && echo "🦀 Rust project detected"
[ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "🐍 Python project detected"
[ -f "Makefile" ] && echo "⚙️ Makefile detected"
[ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] && echo "🐳 Docker Compose detected"
[ -f "Dockerfile" ] && echo "🐳 Dockerfile detected"

echo ""
echo "=== Current Settings ==="
cat .claude/settings.local.json 2>/dev/null || echo "No local settings found"
```

### Step 2: Show Current Permissions

แสดง permissions ที่มีอยู่:

```bash
echo "=== Global Settings ==="
cat ~/.claude/settings.json 2>/dev/null | jq '.permissions' || echo "No global settings"

echo ""
echo "=== Local Settings ==="
cat .claude/settings.local.json 2>/dev/null | jq '.permissions' || echo "No local settings"
```

### Step 3: Suggest Permissions Based on Project

**แนะนำ permissions ตาม project type:**

#### Node.js / Bun / pnpm / Yarn

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build:*)",
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(npm test:*)",
      "Bash(npm install:*)",
      "Bash(npx:*)",
      "Bash(bun run build:*)",
      "Bash(bun run test:*)",
      "Bash(bun run lint:file:*)",
      "Bash(bun run typecheck:*)",
      "Bash(bun test:*)",
      "Bash(bun install:*)",
      "Bash(bunx:*)",
      "Bash(pnpm run:*)",
      "Bash(pnpm test:*)",
      "Bash(pnpm install:*)",
      "Bash(yarn run:*)",
      "Bash(yarn test:*)",
      "Bash(yarn install:*)"
    ]
  }
}
```

#### Go

```json
{
  "permissions": {
    "allow": [
      "Bash(go build:*)",
      "Bash(go test:*)",
      "Bash(go run:*)",
      "Bash(go mod:*)",
      "Bash(go fmt:*)",
      "Bash(go vet:*)",
      "Bash(golangci-lint:*)",
      "Bash(go generate:*)"
    ]
  }
}
```

#### Python

```json
{
  "permissions": {
    "allow": [
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(pip install:*)",
      "Bash(pip3 install:*)",
      "Bash(pytest:*)",
      "Bash(poetry run:*)",
      "Bash(poetry install:*)",
      "Bash(uv run:*)",
      "Bash(uv pip:*)",
      "Bash(ruff:*)",
      "Bash(black:*)",
      "Bash(mypy:*)"
    ]
  }
}
```

#### Rust

```json
{
  "permissions": {
    "allow": [
      "Bash(cargo build:*)",
      "Bash(cargo test:*)",
      "Bash(cargo run:*)",
      "Bash(cargo fmt:*)",
      "Bash(cargo clippy:*)",
      "Bash(cargo check:*)"
    ]
  }
}
```

#### Make / Build Tools

```json
{
  "permissions": {
    "allow": [
      "Bash(make:*)",
      "Bash(make test:*)",
      "Bash(make build:*)",
      "Bash(make lint:*)",
      "Bash(make clean:*)"
    ]
  }
}
```

#### Docker

```json
{
  "permissions": {
    "allow": [
      "Bash(docker build:*)",
      "Bash(docker run:*)",
      "Bash(docker compose up:*)",
      "Bash(docker compose down:*)",
      "Bash(docker compose build:*)",
      "Bash(docker ps:*)",
      "Bash(docker logs:*)"
    ]
  }
}
```

#### Git (Safe Operations)

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git switch:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push)",
      "Bash(git pull:*)",
      "Bash(git fetch:*)",
      "Bash(git stash:*)",
      "Bash(git rebase:*)",
      "Bash(git merge:*)"
    ]
  }
}
```

#### GitHub CLI

```json
{
  "permissions": {
    "allow": [
      "Bash(gh issue:*)",
      "Bash(gh pr:*)",
      "Bash(gh repo:*)",
      "Bash(gh api:*)",
      "Bash(gh run:*)"
    ]
  }
}
```

#### Common Safe Commands

```json
{
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(date:*)",
      "Bash(pwd:*)",
      "Bash(tree:*)",
      "Bash(jq:*)",
      "Bash(curl:*)"
    ]
  }
}
```

### Step 4: Create/Update Settings File

**ถามผู้ใช้ว่าต้องการเพิ่ม permissions อะไรบ้าง:**

```markdown
## Permission Presets

เลือก preset ที่ต้องการ (สามารถเลือกหลายอัน):

1. **node** - npm, bun, pnpm, yarn
2. **go** - go build, test, mod
3. **python** - pip, pytest, poetry, uv
4. **rust** - cargo commands
5. **make** - make commands
6. **docker** - docker, docker-compose
7. **git** - safe git operations
8. **gh** - GitHub CLI
9. **common** - ls, cat, grep, find, etc.

เลือก: (เช่น "node,git,gh,common")
```

### Step 5: Generate Settings File

**สร้างหรือ update `.claude/settings.local.json`:**

```bash
mkdir -p .claude
```

**ตัวอย่าง output สำหรับ Node.js + Git + GH + Common:**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build:*)",
      "Bash(npm run test:*)",
      "Bash(npm run lint:*)",
      "Bash(npm test:*)",
      "Bash(bun run build:*)",
      "Bash(bun run test:*)",
      "Bash(bun test:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push)",
      "Bash(gh issue:*)",
      "Bash(gh pr:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(jq:*)"
    ]
  }
}
```

### Step 6: Verify & Commit

```bash
echo "=== New Settings ==="
cat .claude/settings.local.json | jq .

echo ""
echo "=== Git Status ==="
git status .claude/settings.local.json
```

**แนะนำให้ commit settings:**

```bash
git add .claude/settings.local.json
git commit -m "chore: add Claude Code permission presets"
```

## Dangerous Commands (Always Deny)

**ควรใส่ใน `~/.claude/settings.json` (global):**

```json
{
  "permissions": {
    "deny": [
      "Bash(git push -f:*)",
      "Bash(git push --force:*)",
      "Bash(git push --force-with-lease:*)",
      "Bash(git reset --hard:*)",
      "Bash(git clean -f:*)",
      "Bash(rm -rf:*)",
      "Bash(rm -f:*)",
      "Bash(mv -f:*)",
      "Bash(cp -f:*)",
      "Bash(chmod 777:*)",
      "Bash(sudo:*)"
    ]
  }
}
```

## Best Practices

| Practice | Reason |
|----------|--------|
| ใช้ `settings.local.json` สำหรับ project-specific | Share กับ team ได้ |
| ใช้ `~/.claude/settings.json` สำหรับ global deny | ป้องกัน dangerous commands |
| ใช้ wildcard `:*` สำหรับ arguments | ยืดหยุ่นกว่า |
| Review permissions เป็นระยะ | ลบ permissions ที่ไม่ใช้ |

## Permission Syntax

```
Bash(command:arguments)
Bash(command:*)          # Allow any arguments
Bash(command)            # Exact match, no arguments
Skill(skill-name)        # Allow skill
```

## Examples

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",     // npm run test with any args
      "Bash(git push)",           // git push without args
      "Bash(make:*)",             // make with any target
      "Skill(tdg:atomic-commit)"  // allow specific skill
    ],
    "deny": [
      "Bash(rm -rf:*)"            // never allow rm -rf
    ]
  }
}
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/permissions` | Built-in Claude Code command (UI) |
| `/permission` | This helper command |

## Reference

- [Boris Cherny's workflow](https://twitter.com/bcherny) - Pre-allow safe commands
- Store in `.claude/settings.local.json` and share with team

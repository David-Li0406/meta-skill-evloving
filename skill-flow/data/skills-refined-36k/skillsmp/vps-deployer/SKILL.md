---
name: vps-deployer
description: Deploy code to VPS server after merge to main. Use as the final step in feature workflow after merge-helper completes. Connects to VPS via SSH, pulls latest code, and restarts services.
---

# VPS Deployer Skill

You manage deployment of code to the production VPS server.

## When to Use This Skill

- After successful merge to main (final step in feature workflow)
- User asks to "deploy to VPS" or "задеплоить на сервер"
- User asks to "update production" or "обновить прод"
- Need to sync VPS with latest main branch

## Prerequisites

### Environment Variables (`.env` file)

Required variables in project `.env`:
```bash
VPS_HOST=79.174.84.103
VPS_USER=root
VPS_PASSWORD=your_password_here
VPS_PROJECT_PATH=/root/apps/ThermoCalcBot
```

### Pre-Deployment Checks

Before deploying:
1. Must be on `main` branch
2. All changes committed and pushed
3. Local main is up to date with origin
4. All tests pass locally

## Workflow

### Step 1: Verify Deployment Readiness

```bash
# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Check if main is up to date
git fetch origin main
git log HEAD..origin/main --oneline
git log origin/main..HEAD --oneline
```

**If not on main:**
```
⚠️ Деплой возможен только из main

Текущая ветка: feature/xyz

Выполните мерж в main через merge-helper перед деплоем.
```
**STOP**

**If uncommitted changes:**
```
⚠️ Есть незакоммиченные изменения

Закоммитьте или отмените изменения перед деплоем.
```
**STOP**

**If local behind origin:**
```
⚠️ Локальный main отстаёт от origin

Выполните: git pull origin main
```
**STOP**

**If origin behind local:**
```
⚠️ Изменения не запушены в origin

Выполните: git push origin main
```
**STOP**

### Step 2: Load VPS Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

vps_config = {
    "host": os.getenv("VPS_HOST"),
    "user": os.getenv("VPS_USER"),
    "password": os.getenv("VPS_PASSWORD"),
    "project_path": os.getenv("VPS_PROJECT_PATH", "/root/apps/ThermoCalcBot")
}

# Validate config
missing = [k for k, v in vps_config.items() if not v]
if missing:
    print(f"❌ Отсутствуют переменные: {', '.join(missing)}")
```

**If config incomplete:**
```
❌ Конфигурация VPS неполная

Отсутствуют переменные:
- VPS_HOST
- VPS_PASSWORD

Добавьте в .env файл:
VPS_HOST=79.174.84.103
VPS_USER=root
VPS_PASSWORD=your_password
VPS_PROJECT_PATH=/root/apps/ThermoCalcBot
```
**STOP**

### Step 3: Connect and Deploy

Use SSH to connect to VPS and execute deployment commands:

```bash
# Using sshpass for password authentication
sshpass -p "$VPS_PASSWORD" ssh -o StrictHostKeyChecking=no $VPS_USER@$VPS_HOST << 'EOF'
cd /root/apps/ThermoCalcBot

echo "=== Pulling latest changes ==="
git pull origin main

echo "=== Syncing dependencies ==="
uv sync

echo "=== Restarting services ==="
systemctl restart thermobot
systemctl restart thermoapi

echo "=== Checking service status ==="
sleep 3
systemctl is-active thermobot
systemctl is-active thermoapi

echo "=== Deployment complete ==="
EOF
```

**Step 3a: Install paramiko (if not installed):**

On Windows (if paramiko not available):
```bash
pip install --user paramiko
```

Or using uv:
```bash
uv pip install paramiko --system
```

**Step 3b: Create deployment script:**

Create a Python script for deployment (platform-agnostic):

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VPS Deploy Script for ThermoCalcBot"""
import os
import sys
import io
from dotenv import load_dotenv
import paramiko

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

VPS_CONFIG = {
    "host": os.getenv("VPS_HOST"),
    "user": os.getenv("VPS_USER"),
    "password": os.getenv("VPS_PASSWORD"),
    "project_path": os.getenv("VPS_PROJECT_PATH", "/root/apps/ThermoCalcBot")
}

def execute_ssh_command(client, command):
    """Execute command via SSH and return output"""
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    errors = stderr.read().decode()
    return output, errors

def deploy():
    """Deploy to VPS"""
    print(f"[INFO] Starting deployment to {VPS_CONFIG['host']}...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"[INFO] Connecting to {VPS_CONFIG['user']}@{VPS_CONFIG['host']}...")
        client.connect(
            hostname=VPS_CONFIG['host'],
            port=22,
            username=VPS_CONFIG['user'],
            password=VPS_CONFIG['password'],
            timeout=60,
            banner_timeout=60,
            auth_timeout=60
        )
        print("[OK] Connected!")

        path = VPS_CONFIG['project_path']

        # Pull latest changes
        print("[INFO] Pulling latest changes...")
        output, errors = execute_ssh_command(client, f"cd {path} && git pull origin main")
        print(f"[OK] {output.strip() if output.strip() else 'Already up to date'}")

        # Sync dependencies
        print("[INFO] Syncing dependencies...")
        output, errors = execute_ssh_command(client, f"cd {path} && uv sync")
        if errors and "error" in errors.lower():
            print(f"[ERROR] uv sync failed: {errors}")
            return False
        print("[OK] Dependencies synced")

        # Restart services
        print("[INFO] Restarting services...")
        execute_ssh_command(client, "systemctl restart thermobot")
        execute_ssh_command(client, "systemctl restart thermoapi")
        print("[OK] Services restarted")

        import time
        time.sleep(3)

        # Check status
        print("[INFO] Checking service status...")
        bot_status, _ = execute_ssh_command(client, "systemctl is-active thermobot")
        api_status, _ = execute_ssh_command(client, "systemctl is-active thermoapi")

        bot_ok = bot_status.strip() == "active"
        api_ok = api_status.strip() == "active"

        print(f"   thermobot: {'[OK] active' if bot_ok else '[FAIL] ' + bot_status.strip()}")
        print(f"   thermoapi: {'[OK] active' if api_ok else '[FAIL] ' + api_status.strip()}")

        # Get latest commit
        latest_commit, _ = execute_ssh_command(client, f"cd {path} && git rev-parse --short HEAD")

        if bot_ok and api_ok:
            print("[SUCCESS] Deployment completed!")
            print(f"  Server: {VPS_CONFIG['host']}")
            print(f"  Commit: {latest_commit.strip()}")
            return True
        else:
            print("[FAIL] Deployment failed")

            # Show logs for failed services
            if not bot_ok:
                bot_logs, _ = execute_ssh_command(client, "journalctl -u thermobot -n 15 --no-pager")
                print(f"\n--- thermobot logs ---\n{bot_logs}")
            if not api_ok:
                api_logs, _ = execute_ssh_command(client, "journalctl -u thermoapi -n 15 --no-pager")
                print(f"\n--- thermoapi logs ---\n{api_logs}")
            return False

    except paramiko.AuthenticationException:
        print("[ERROR] Authentication failed. Check VPS_USER and VPS_PASSWORD in .env")
        return False
    except paramiko.SSHException as e:
        print(f"[ERROR] SSH error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.close()

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
```

Execute the script:
```bash
python deploy.py
# Or on Linux:
python3 deploy.py
```

### Step 4: Verify Deployment

After deployment, verify services are running:

```bash
# On VPS via SSH
systemctl status thermobot --no-pager | head -5
systemctl status thermoapi --no-pager | head -5

# Health check for API
curl -s http://localhost:8000/api/v1/health | head -c 200
```

**If services failed:**
```
❌ Сервисы не запустились

thermobot: inactive
thermoapi: active

Проверьте логи:
journalctl -u thermobot -n 20

Возможные проблемы:
- Синтаксические ошибки в коде
- Отсутствующие зависимости
- Проблемы с конфигурацией
```

### Step 5: Report Deployment Result

**Success:**
```
✅ Деплой завершён успешно

🖥️ Сервер: 79.174.84.103
📁 Путь: /root/apps/ThermoCalcBot
🌿 Ветка: main
📝 Коммит: {latest-commit-hash}

📊 Статус сервисов:
- thermobot: ✅ active
- thermoapi: ✅ active

🔗 API Health: http://79.174.84.103:8000/api/v1/health
🤖 Telegram: @ThermoCalcBot

Код успешно развёрнут на продакшене!
```

**Failure:**
```
❌ Деплой завершился с ошибками

🖥️ Сервер: 79.174.84.103

📊 Статус сервисов:
- thermobot: ❌ failed
- thermoapi: ✅ active

📋 Действия для диагностики:
1. ssh root@79.174.84.103
2. journalctl -u thermobot -n 50
3. cd /root/apps/ThermoCalcBot && uv run python telegram_bot.py

Требуется ручное вмешательство.
```

## Deployment Checklist

Before proceeding with deployment:

- [ ] On `main` branch
- [ ] All changes committed
- [ ] Changes pushed to origin
- [ ] All tests pass locally
- [ ] VPS credentials in `.env`
- [ ] User confirmed deployment

## Rollback Procedure

If deployment fails and rollback is needed:

```bash
# On VPS
cd /root/apps/ThermoCalcBot

# Find previous commit
git log --oneline -5

# Rollback to previous commit
git checkout {previous-commit-hash}

# Or revert to previous state
git reset --hard HEAD~1

# Restart services
systemctl restart thermobot
systemctl restart thermoapi
```

## Platform-Specific Notes

### Windows

When deploying from Windows:
- Use `pip install --user paramiko` to install dependencies
- Script includes UTF-8 encoding fix for Windows console
- Delete temp files with `rm` (bash) or `del` (cmd)
- Emoji not supported in output (script uses plain text markers like `[INFO]`, `[OK]`, `[FAIL]`)

### Linux/Mac

- Use `pip3 install paramiko` or `uv pip install paramiko`
- Standard UTF-8 support
- Delete temp files with `rm`

## Troubleshooting

### paramiko not found
```bash
# Windows
pip install --user paramiko

# Linux/Mac
pip3 install paramiko
```

### SSH banner timeout
If you get `Error reading SSH protocol banner`, the script includes increased timeouts:
- `timeout=60` - connection timeout
- `banner_timeout=60` - SSH banner timeout
- `auth_timeout=60` - authentication timeout

### UnicodeEncodeError in Windows
The script sets UTF-8 encoding for stdout/stderr. If you still get encoding errors:
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Security Notes

- VPS password stored in `.env` (gitignored)
- SSH connection uses StrictHostKeyChecking=no for automation
- Consider switching to SSH keys for better security in the future
- Increased timeouts may affect security (adjust as needed for your environment)

## Quick Commands Reference

| Action           | Command                                                     |
| ---------------- | ----------------------------------------------------------- |
| Check VPS status | `ssh root@VPS_HOST "systemctl status thermobot thermoapi"`  |
| View bot logs    | `ssh root@VPS_HOST "journalctl -u thermobot -n 50"`         |
| View API logs    | `ssh root@VPS_HOST "journalctl -u thermoapi -n 50"`         |
| Manual restart   | `ssh root@VPS_HOST "systemctl restart thermobot thermoapi"` |

## References

- [VPS_BOT_COMMANDS.md](../../../VPS_BOT_COMMANDS.md) - Full VPS management guide
- [merge-helper](../merge-helper/SKILL.md) - Pre-deployment merge workflow

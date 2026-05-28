---
name: secrets-check
description: Verify secrets and environment variables are properly configured. Use before deployment, after adding new services, or when debugging auth issues.
---

# Secrets Check Skill

Verify that all secrets are properly configured before deployment or when debugging issues.

## When to Use

- Before deploying to production
- After adding a new API integration
- When debugging API errors (401, 403, timeouts)
- After rotating secrets

## Required Environment Variables

### Core (Required)

| Variable | Description | Where Used |
|----------|-------------|------------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API token | Telegram connector |
| `MONGODB_URI` | MongoDB Atlas connection string | Storage layer |
| `NVIDIA_API_KEY` | NVIDIA NIM API key | LLM fallback |
| `APP_SECRET_KEY` | Flask/Quart session secret | Web verification |
| `VERIFY_TOKEN_SECRET` | Token signing secret | Verification flow |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `TOGETHER_API_KEY` | Together AI (legacy) | Not used |
| `DISCORD_BOT_TOKEN` | Discord bot | Skeleton |
| `WHATSAPP_ACCESS_TOKEN` | WhatsApp Cloud API | Skeleton |

## Quick Verification

### Local Development

```bash
# Check .env exists
ls -la .env

# Verify required vars are set (redacted)
grep -E "^(TELEGRAM_BOT_TOKEN|MONGODB_URI|NVIDIA_API_KEY)=" .env | cut -d= -f1

# Check no secrets in code
grep -rE "(nvapi-|mongodb\+srv://[^\"']+:[^\"']+@)" --include="*.py" src/
```

### Render Production

1. Go to Render Dashboard → Your Service → Environment
2. Verify these are set:
   - `TELEGRAM_BOT_TOKEN`
   - `MONGODB_URI`
   - `NVIDIA_API_KEY`
   - `APP_SECRET_KEY`
   - `VERIFY_TOKEN_SECRET`

## Checklist

### Development Setup

- [ ] `.env` file exists (copied from `env.example`)
- [ ] `TELEGRAM_BOT_TOKEN` is set
- [ ] `MONGODB_URI` is set and accessible
- [ ] `NVIDIA_API_KEY` is set (for LLM fallback)
- [ ] `APP_SECRET_KEY` is random (not default)
- [ ] `VERIFY_TOKEN_SECRET` is random (not default)

### Production Setup (Render)

- [ ] All required env vars in Render dashboard
- [ ] MongoDB Atlas IP allowlist includes only Render egress IPs (never use 0.0.0.0/0 in production)
- [ ] Webhook URL configured in Telegram

### Code Security

- [ ] No hardcoded tokens in code
- [ ] `.env` is in `.gitignore`
- [ ] `env.example` has placeholder values only

## Common Issues

### "NVIDIA_API_KEY not set" warning

LLM fallback won't work but bot continues (fail-open).

Fix: Add `NVIDIA_API_KEY` to Render environment.

### MongoDB connection timeout

1. Check `MONGODB_URI` is correct
2. Verify IP allowlist in MongoDB Atlas
3. Check network connectivity from Render

### Telegram webhook not receiving messages

```bash
# Check webhook status
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"

# Set webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-app.onrender.com/hooks/telegram"
```

### 401/403 from NVIDIA API

1. Verify API key is valid
2. Check key has correct permissions
3. Try regenerating key in NVIDIA dashboard

## Secret Rotation

When rotating production secrets:

```bash
# 1. Generate new secret
NEW_SECRET=$(openssl rand -hex 32)
echo "New secret: $NEW_SECRET"

# 2. Update in Render dashboard

# 3. Trigger redeploy (push to main or manual deploy)

# 4. Verify health check
curl https://your-app.onrender.com/health
```

## Related Files

- `env.example` - Template for environment variables
- `docs/RUNBOOK.md` - Full deployment guide
- `src/settings.py` - Settings loading logic

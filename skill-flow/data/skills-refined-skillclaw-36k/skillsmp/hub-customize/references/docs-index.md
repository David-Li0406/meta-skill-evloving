# Documentation Reference

Essential docs for customization workflow. Read these before/during setup.

## Primary Documentation

| Doc | Path | Use When |
|-----|------|----------|
| **Customization Guide** | `docs/CUSTOMIZATION.md` | Main reference for fork setup |
| **DNS Setup** | `docs/DNS_SETUP.md` | Configuring domain and HTTPS |
| **OAuth Setup** | `docs/OAUTH_SETUP.md` | Enabling Claude.ai/ChatGPT access |
| **n8n Integration** | `docs/N8N_SETUP.md` | Adding workflow automation |
| **HITL Setup** | `docs/HITL_SETUP.md` | Human-in-the-loop permissions |

## Quick Links

### docs/CUSTOMIZATION.md
- Company name and branding
- Environment configuration
- User endpoint setup
- Service selection

### docs/DNS_SETUP.md
- Domain configuration
- Caddy reverse proxy
- SSL certificates
- Multi-service routing

### docs/OAUTH_SETUP.md
- Scalekit setup
- OAuth 2.1 flow
- Cloud client configuration

### docs/N8N_SETUP.md
- n8n integration
- Workflow triggers
- API configuration

## Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment template |
| `deploy/docker-compose.yml` | Service definitions |
| `deploy/Caddyfile` | Reverse proxy config |
| `clients/_template/` | User endpoint template |

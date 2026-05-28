---
name: 'new-application'
description: 'Use this when creating a new application in the /apps directory'
---

When creating a web application, frontend:

This skill creates a Next.js app via Cloudflare’s official starter:

```bash
npm create cloudflare@latest -- next-cloudflare2 --framework=next --deploy --git
```

Cursor uses the shared Claude script paths below.

**For Unix/Mac/Linux:**

```bash
.claude/skills/new-application/scripts/create-nextjs-app.sh
```

**For Windows PowerShell:**

```powershell
.claude/skills/new-application/scripts/create-nextjs-app.ps1
```

---
name: new-application
description: Use this skill when creating a new application in the /apps directory.
---

# Skill body

When creating a web application using Next.js, you can utilize Cloudflare’s official starter. Follow the instructions below based on your operating system:

**Create a Next.js app:**

```bash
npm create cloudflare@latest -- next-cloudflare2 --framework=next --deploy --git
```

**For Unix/Mac/Linux:**

```bash
.claude/skills/new-application/scripts/create-nextjs-app.sh
```

**For Windows PowerShell:**

```powershell
.claude/skills/new-application/scripts/create-nextjs-app.ps1
```
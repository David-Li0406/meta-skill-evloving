---
name: deployment-procedures
description: Use this skill when you need to understand the principles and workflows for safe production deployments, including rollback strategies and verification processes.
---

# Deployment Procedures

> Deployment principles and decision-making for safe production releases.
> **Learn to THINK, not memorize scripts.**

## ⚠️ How to Use This Skill

This skill teaches **deployment principles**, not bash scripts to copy.

- Every deployment is unique.
- Understand the WHY behind each step.
- Adapt procedures to your platform.

## 1. Platform Selection

### Decision Tree

```
What are you deploying?
│
├── Static site / JAMstack
│   └── Vercel, Netlify, Cloudflare Pages
│
├── Simple web app
│   ├── Managed → Railway, Render, Fly.io
│   └── Control → VPS + PM2/Docker
│
├── Microservices
│   └── Container orchestration
│
└── Serverless
    └── Edge functions, Lambda
```

### Each Platform Has Different Procedures

| Platform           | Deployment Method          |
| ------------------ | -------------------------- |
| **Vercel/Netlify** | Git push, auto-deploy      |
| **Railway/Render** | Git push or CLI            |
| **VPS + PM2**      | SSH + manual steps         |
| **Docker**         | Image push + orchestration |
| **Kubernetes**     | kubectl apply              |

## 2. Pre-Deployment Principles

### The 4 Verification Categories

| Category         | What to Check                          |
| ---------------- | -------------------------------------- |
| **Code Quality** | Tests passing, linting clean, reviewed |
| **Build**        | Production build works, no warnings    |
| **Environment**  | Env vars set, secrets current          |
| **Safety**       | Backup done, rollback plan ready       |

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Production build successful
- [ ] Environment variables verified
- [ ] Database migrations ready (if any)
- [ ] Rollback plan documented
- [ ] Team notified
- [ ] Monitoring ready

## 3. Deployment Workflow Principles

### The 5-Phase Process

```
1. PREPARE
   └── Verify code, build, env vars

2. BACKUP
   └── Save current state before changing

3. DEPLOY
   └── Execute with monitoring open

4. VERIFY
   └── Health check, logs, key flows

5. CONFIRM or ROLLBACK
   └── All good? Confirm. Issues? Rollback.
```

### Phase Principles

| Phase       | Principle                        |
| ----------- | -------------------------------- |
| **Prepare** | Never deploy untested code       |
| **Backup**  | Can't rollback without backup     |
| **Deploy**  | Watch it happen, don't walk away |
| **Verify**  | Trust but verify                 |
| **Confirm** | Have rollback triggers ready      |
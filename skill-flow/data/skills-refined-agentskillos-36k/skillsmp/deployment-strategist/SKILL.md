---
name: Deployment Strategist
description: Specialized skill for managing deployment pipelines, environment configuration, and post-release verification.
---

# 🚀 Deployment Strategist Skill

This skill focuses on the *operational* success of your application. While the **Release Manager** gets the code committed, the **Deployment Strategist** ensures it runs successfully in the wild.

## 🎯 When to Use
- **Pre-Deployment**: Verifying environment configuration.
- **Post-Deployment**: Sanity checking the live environment.
- **Troubleshooting**: Diagnosing production issues.

## 🛠️ Toolbelt

### 1. The Deployment Health Check
Runs a suite of checks against a target URL (staging or production) to verify critical flows are operational.

```bash
node .agent/skills/deployment-strategist/scripts/health-check.js --url <target-url>
```

### 2. Environment Audit
Scans your environment usage to ensure all required secrets are present (does not reveal values, only checks existence).

```bash
node .agent/skills/deployment-strategist/scripts/audit-env.js
```

## 📊 Deployment Tactics

| Strategy | Description | When to Use |
|:---:|:---|:---|
| **Blue/Green** | Parallel environments. | Major version upgrades. |
| **Canary** | Slow rollout to % of users. | High-risk feature flags. |
| **Rollback** | Immediate revert. | Critical P0 bugs. |

## 🚨 Emergency Procedures
If deployment fails:
1. **Check Logs**: Infrastructure provider logs (Vercel/Netlify/AWS).
2. **Rollback**: Use the hosting provider's rollback feature immediately.
3. **Analyze**: Use `health-check.js` to reproduce issues on staging.

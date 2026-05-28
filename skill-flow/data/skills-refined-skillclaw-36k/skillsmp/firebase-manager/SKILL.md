---
name: firebase_manager
description: Manage Firebase operations including deployment, debugging, and environment configuration.
---

# Firebase Manager Skill

This skill helps automate the management of the RIBH Firebase infrastructure.

## 🛠 Features
- **Health Check**: Run `scripts/health_check.sh` to verify project configuration.
- **Smart Deploy**: Commands for partial or full deployment.
- **Logs Inspection**: Easy access to Cloud Functions logs.

## 🚀 Execution Instructions

### 1. View Logs
To see the last 50 lines of Cloud Functions logs:
```bash
firebase functions:log
```

### 2. Deploy Only Frontend
If you only changed HTML/CSS/JS in `public/`:
```bash
firebase deploy --only hosting
```

### 3. Deploy Only Backend
If you only changed `functions/`:
```bash
firebase deploy --only functions
```

### 4. Sync Secrets
If you updated `.env`, ensure you've updated the Firebase Functions config:
```bash
# Example
firebase functions:config:set resend.key="YOUR_KEY"
```

## 📁 Resources
- `scripts/health_check.sh`: Automated status verification.

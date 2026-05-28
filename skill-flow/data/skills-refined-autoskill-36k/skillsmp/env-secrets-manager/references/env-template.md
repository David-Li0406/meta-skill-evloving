# Standard .env.local Template

```bash
# ============================================
# ACT Ecosystem - Environment Variables
# ============================================
# NEVER COMMIT THIS FILE TO GIT
# Last updated: YYYY-MM-DD
# Project: [Project Name]

# ============================================
# GitHub Integration
# ============================================
GITHUB_TOKEN=GITHUB_TOKEN_PLACEHOLDER
GH_PROJECT_TOKEN=GITHUB_TOKEN_PLACEHOLDER
GITHUB_PROJECT_ID=PVT_xxxx

# ============================================
# Notion Integration
# ============================================
NOTION_TOKEN=NOTION_TOKEN_PLACEHOLDER
NOTION_DATABASE_ID=xxxx
NOTION_WORKSPACE_ID=xxxx

# ============================================
# Supabase (Database)
# ============================================
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxxx

# ============================================
# OpenAI (AI Features)
# ============================================
OPENAI_API_KEY=sk-xxxx

# ============================================
# Google OAuth (Gmail, Calendar)
# ============================================
GOOGLE_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxx
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:3001/api/auth/gmail/callback

# ============================================
# GoHighLevel CRM
# ============================================
GHL_API_KEY=xxxx
GHL_LOCATION_ID=xxxx

# ============================================
# Vercel (Deployment)
# ============================================
VERCEL_ACCESS_TOKEN=xxxx
VERCEL_TEAM_ID=team_xxxx

# ============================================
# Application Secrets
# ============================================
NEXTAUTH_SECRET=xxxx
NEXTAUTH_URL=http://localhost:3001

# ============================================
# Redis (Optional - for caching)
# ============================================
REDIS_URL=redis://nas.local:6379

# ============================================
# Project-Specific
# ============================================
# Add project-specific variables below
```

## Token Validation Example

```javascript
// Validate required tokens on startup
const requiredEnvVars = [
  'NOTION_TOKEN',
  'SUPABASE_SERVICE_ROLE_KEY',
  'GITHUB_TOKEN'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`${envVar} is required`);
  }
}
```

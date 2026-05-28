# Neon CLI Commands Reference

## Installation

### npm
```bash
npm install -g neonctl
```

### Homebrew (macOS)
```bash
brew install neonctl
```

## Authentication

### Login
```bash
# Authenticate with Neon
neonctl auth login

# Or use API key directly
export NEON_API_KEY="your-api-key"
```

## Project Management

### List Projects
```bash
neonctl projects list
```

### Get Project Details
```bash
neonctl projects get <project-id>
```

### Create New Project
```bash
neonctl projects create --name "my-project" --region us-east-2
```

## Branch Management

### List Branches
```bash
neonctl branches list --project-id <project-id>
```

### Create Branch (for development/testing)
```bash
neonctl branches create --project-id <project-id> --name dev --parent main
```

### Delete Branch
```bash
neonctl branches delete <branch-id> --project-id <project-id>
```

## Database Operations

### List Databases
```bash
neonctl databases list --project-id <project-id> --branch-id <branch-id>
```

### Create Database
```bash
neonctl databases create --project-id <project-id> --branch-id <branch-id> --name mydb
```

### Get Connection String
```bash
# Get database connection string
neonctl connection-string <database-name> --project-id <project-id> --branch-id <branch-id>

# With role specified
neonctl connection-string <database-name> --role-name <role> --project-id <project-id>
```

## Useful Patterns

### Quick Setup for New Project
```bash
# 1. Create project
PROJECT_ID=$(neonctl projects create --name "rag-chatbot" --region us-east-2 --output json | jq -r '.id')

# 2. Get connection string
DATABASE_URL=$(neonctl connection-string neondb --project-id $PROJECT_ID)

# 3. Save to .env.local
echo "DATABASE_URL=\"$DATABASE_URL\"" >> .env.local
```

### Reset Development Database
```bash
# 1. Delete dev branch
neonctl branches delete dev --project-id <project-id>

# 2. Create fresh dev branch from main
neonctl branches create --project-id <project-id> --name dev --parent main
```

## Monitoring

### Check Compute Status
```bash
neonctl projects status --project-id <project-id>
```

### View Usage
```bash
neonctl projects consumption --project-id <project-id>
```

## Tips

- **API Keys**: Generate at https://console.neon.tech/app/settings/api-keys
- **Regions**: us-east-2, us-west-2, eu-central-1, ap-southeast-1
- **Free Tier**: 0.5GB storage, 10GB data transfer, autosuspend after 5 min inactivity
- **Branching**: Use branches for testing migrations safely

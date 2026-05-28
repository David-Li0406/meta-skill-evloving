---
name: flow-nexus-platform-management
description: Use this skill for comprehensive management of the Flow Nexus platform, including authentication, sandbox execution, app deployment, payments, and challenges.
---

# Flow Nexus Platform Management

## Overview

This skill provides comprehensive management for the Flow Nexus platform, covering authentication, sandbox execution, app deployment, credit management, and coding challenges. It consolidates multiple command modules into a single interface for streamlined operations.

## Behavioral Classification

**Type**: Autonomous Execution

This skill provides commands that execute immediately when invoked. No interactive decisions are required.

**Command Categories**:
- Authentication: Login, register, profile management
- Sandboxes: Create, execute, manage isolated environments
- App Store: Browse, publish, deploy applications
- Payments: Credits, billing, subscriptions
- Challenges: Coding challenges, achievements, leaderboards
- Storage: File storage, real-time subscriptions

## Quick Start

### Step 1: Authenticate

```javascript
// Register new account
mcp__flow-nexus__user_register({
  email: "dev@example.com",
  password: "SecurePass123!",
  full_name: "Developer Name"
})

// Or login to existing account
mcp__flow-nexus__user_login({
  email: "dev@example.com",
  password: "SecurePass123!"
})
```

### Step 2: Create a Sandbox

```javascript
mcp__flow-nexus__sandbox_create({
  template: "node",
  name: "dev-environment",
  install_packages: ["express", "dotenv"],
  env_vars: { NODE_ENV: "development" }
})
```

### Step 3: Execute Code

```javascript
mcp__flow-nexus__sandbox_execute({
  sandbox_id: "your_sandbox_id",
  code: 'console.log("Hello Flow Nexus!")',
  language: "javascript"
})
```

### Step 4: Deploy an App

```javascript
mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-api",
  variables: { database_url: "postgres://..." }
})
```

## Authentication & User Management

### Registration & Login

**Register New Account**
```javascript
mcp__flow-nexus__user_register({
  email: "user@example.com",
  password: "secure_password",
  full_name: "Your Name",
  username: "unique_username" // optional
})
```

**Login**
```javascript
mcp__flow-nexus__user_login({
  email: "user@example.com",
  password: "your_password"
})
```

### Profile Management

**Get User Profile**
```javascript
mcp__flow-nexus__user_profile({
  user_id: "your_user_id"
})
```

**Update Profile**
```javascript
mcp__flow-nexus__user_update_profile({
  user_id: "your_user_id",
  updates: {
    full_name: "Updated Name",
    bio: "AI Developer and researcher",
    github_username: "yourusername",
    twitter_handle: "@yourhandle"
  }
})
```

## Sandbox Management

### Create & Configure Sandboxes

**Create Sandbox**
```javascript
mcp__flow-nexus__sandbox_create({
  template: "node", // node, python, react, etc.
  name: "my-sandbox",
  env_vars: {
    API_KEY: "your_api_key",
    NODE_ENV: "development"
  },
  install_packages: ["express", "cors"],
  startup_script: "npm run dev",
  timeout: 3600, // seconds
})
```

### Execute Code

**Run Code in Sandbox**
```javascript
mcp__flow-nexus__sandbox_execute({
  sandbox_id: "sandbox_id",
  code: `
    console.log('Hello from sandbox!');
  `,
  language: "javascript",
  capture_output: true,
  timeout: 60 // seconds
})
```

## App Store & Deployment

### Browse & Search

**Search Applications**
```javascript
mcp__flow-nexus__app_search({
  search: "authentication api",
  category: "backend",
  limit: 20
})
```

### Publish Applications

**Publish App to Store**
```javascript
mcp__flow-nexus__app_store_publish_app({
  name: "JWT Authentication Service",
  description: "Production-ready JWT authentication microservice",
  category: "backend",
  version: "1.0.0",
  source_code: sourceCodeString,
  tags: ["auth", "jwt", "express"],
})
```

## Payments & Credits

### Balance & Credits

**Check Credit Balance**
```javascript
mcp__flow-nexus__check_balance()
```

### Purchase Credits

**Create Payment Link**
```javascript
mcp__flow-nexus__create_payment_link({
  amount: 50 // USD
})
```

## Challenges & Achievements

### Browse Challenges

**List Available Challenges**
```javascript
mcp__flow-nexus__challenges_list({
  difficulty: "intermediate",
  category: "algorithms",
  limit: 20
})
```

### Submit Solutions

**Submit Challenge Solution**
```javascript
mcp__flow-nexus__challenge_submit({
  challenge_id: "challenge_id",
  user_id: "your_user_id",
  solution_code: `
    function twoSum(nums, target) {
      // solution code
    }
  `,
  language: "javascript"
})
```

## Storage & Real-time

### File Storage

**Upload File**
```javascript
mcp__flow-nexus__storage_upload({
  bucket: "my-bucket",
  path: "data/users.json",
  content: JSON.stringify(userData, null, 2),
  content_type: "application/json"
})
```

### Real-time Subscriptions

**Subscribe to Database Changes**
```javascript
mcp__flow-nexus__realtime_subscribe({
  table: "tasks",
  event: "INSERT"
})
```

## System Utilities

### Check System Health
```javascript
mcp__flow-nexus__system_health()
```

## Best Practices

### Security
- Never hardcode API keys - use environment variables
- Review audit logs periodically

### Performance
- Clean up unused sandboxes to save credits
- Monitor usage via `user_stats`

## Troubleshooting

### Authentication Issues
- **Login Failed**: Check email/password, verify email first

### Sandbox Issues
- **Sandbox Won't Start**: Check template compatibility, verify credits

### Payment Issues
- **Credits Not Applied**: Allow 5-10 minutes for processing

## Support & Resources

- **Documentation**: https://docs.flow-nexus.ruv.io
- **API Reference**: https://api.flow-nexus.ruv.io/docs

---

**Version**: 2.0.0
**Last Updated**: 2025-01-24